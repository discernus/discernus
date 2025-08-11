#!/usr/bin/env python3
"""
Statistical Results Formatter

Formats MathToolkit raw results into LLM-optimized JSON tables suitable for
sequential synthesis. Ensures JSON-serializable native types and compact tables.

THIN: This module performs deterministic formatting only. No computation.
"""
from typing import Dict, Any, List, Optional
import pandas as pd


class StatisticalResultsFormatter:
    """Formats raw statistical results from MathToolkit into LLM-optimized JSON tables."""

    def __init__(self, statistical_results: Dict[str, Any]):
        """
        Initializes the formatter with the raw statistical results.

        Args:
            statistical_results: The raw output from MathToolkit's execute_analysis_plan_thin.
        """
        self.results = statistical_results.get("results", {})
        self.errors = statistical_results.get("errors", [])
        self.warnings = statistical_results.get("warnings", [])

    def format_all(self) -> Dict[str, Any]:
        """Formats all available statistical results into a structured dictionary."""
        if not self.results:
            return {
                "anova_summary": None,
                "correlation_summary": None,
                "descriptive_summary": None,
                "reliability_summary": None,
                "framework_fit_assessment": None,
                "notes": "No results provided"
            }

        # self.results already contains the results section from MathToolkit
        results = self.results

        anova_rows: List[List[Any]] = []
        correlation_top: List[Dict[str, Any]] = []
        descriptive_rows: List[List[Any]] = []
        reliability_rows: List[List[Any]] = []

        # Aggregate across tasks
        for task_name, task_result in results.items():
            if not isinstance(task_result, dict):
                continue
            rtype = task_result.get('type', '')

            # One-way ANOVA row format
            if rtype == 'one_way_anova':
                dimension = task_result.get('dependent_variable', task_name)
                f_stat = float(task_result.get('f_statistic', 0.0)) if task_result.get('f_statistic') is not None else None
                p_value = float(task_result.get('p_value', 1.0)) if task_result.get('p_value') is not None else None
                significant = bool(task_result.get('significant', False))
                anova_rows.append([dimension, f_stat, p_value, significant])

            # Correlation matrices (pearson/spearman)
            elif rtype in ('pearson_correlation', 'spearman_correlation', 'correlation_matrix'):
                # Handle correlation_matrix format from MathToolkit
                corr_matrix = task_result.get('correlation_matrix', {})
                for row_var, row_data in corr_matrix.items():
                    if not isinstance(row_data, dict):
                        continue
                    for col_var, corr_value in row_data.items():
                        # Skip self-correlations and NaN values
                        if row_var == col_var or corr_value != corr_value:  # NaN check
                            continue
                        # Only include upper triangle to avoid duplicates
                        if row_var < col_var:
                            correlation_top.append({
                                "dimensions": f"{row_var}↔{col_var}",
                                "correlation": float(corr_value) if corr_value is not None else None,
                                "p_value": None  # P-values not available in current MathToolkit output
                            })
                
                # Fallback: try significant_pairs if available
                sig_pairs = task_result.get('significant_pairs', [])
                if not correlation_top and sig_pairs:
                    for entry in sig_pairs:
                        # entry can be a tuple (col1, col2, corr, pval)
                        try:
                            col1, col2, corr, pval = entry
                        except Exception:
                            # Or dict shape
                            col1 = entry.get('col1')
                            col2 = entry.get('col2')
                            corr = entry.get('correlation')
                            pval = entry.get('p_value')
                        if col1 is None or col2 is None:
                            continue
                        correlation_top.append({
                            "dimensions": f"{col1}↔{col2}",
                            "correlation": float(corr) if corr is not None else None,
                            "p_value": float(pval) if pval is not None else None
                        })

            # Descriptive statistics (ungrouped)
            elif rtype == 'descriptive_stats':
                results_map = task_result.get('results', {})
                for col, stats in results_map.items():
                    # Only include numerical columns to keep compact
                    if isinstance(stats, dict) and stats.get('data_type') == 'numerical':
                        descriptive_rows.append([
                            col,
                            float(stats.get('mean', 0.0)) if stats.get('mean') is not None else None,
                            float(stats.get('std', 0.0)) if stats.get('std') is not None else None,
                            float(stats.get('min', 0.0)) if stats.get('min') is not None else None,
                            float(stats.get('max', 0.0)) if stats.get('max') is not None else None
                        ])
            
            # Reliability analysis (Cronbach's alpha)
            elif rtype in ('cronbach_alpha', 'reliability_analysis'):
                dimension = task_result.get('dimension', task_name)
                alpha = task_result.get('cronbach_alpha')
                if alpha is not None:
                    alpha_value = float(alpha)
                    ci_lower = task_result.get('confidence_interval', {}).get('lower', alpha_value - 0.1)
                    ci_upper = task_result.get('confidence_interval', {}).get('upper', alpha_value + 0.1)
                    interpretation = self._interpret_reliability(alpha_value)
                    reliability_rows.append([
                        dimension,
                        alpha_value,
                        f"[{ci_lower:.2f}, {ci_upper:.2f}]",
                        interpretation
                    ])

        # Assemble tables
        anova_summary = None
        if anova_rows:
            anova_rows_sorted = sorted(
                anova_rows,
                key=lambda row: (0.0 if row[1] is None else -row[1])  # sort by F desc, None last
            )
            anova_summary = {
                "table_format": "ANOVA Results Table",
                "headers": ["Dimension", "F-Statistic", "P-Value", "Significant"],
                "rows": anova_rows_sorted,
                "interpretation": self._interpret_anova(anova_rows_sorted)
            }

        correlation_summary = None
        if correlation_top:
            # Keep top 10 strongest correlations by absolute value
            correlation_sorted = sorted(
                correlation_top,
                key=lambda x: 0.0 if x.get('correlation') is None else -abs(x['correlation'])
            )[:10]
            correlation_summary = {
                "table_format": "Correlation Summary",
                "rows": correlation_sorted,
                "interpretation": self._interpret_correlations(correlation_sorted)
            }

        descriptive_summary = None
        if descriptive_rows:
            descriptive_summary = {
                "table_format": "Descriptive Statistics",
                "headers": ["Dimension", "Mean", "Std Dev", "Min", "Max"],
                "rows": descriptive_rows
            }

        reliability_summary = None
        if reliability_rows:
            reliability_summary = {
                "table_format": "Measurement Reliability Table",
                "headers": ["Dimension", "Cronbach's Alpha", "95% CI", "Interpretation"],
                "rows": reliability_rows,
                "interpretation": self._interpret_overall_reliability(reliability_rows)
            }

        # Framework fit assessment based on available statistical data
        framework_fit_assessment = self._assess_framework_fit(
            anova_summary, reliability_summary, descriptive_summary
        )

        return {
            "anova_summary": anova_summary,
            "correlation_summary": correlation_summary,
            "descriptive_summary": descriptive_summary,
            "reliability_summary": reliability_summary,
            "framework_fit_assessment": framework_fit_assessment
        }

    def _interpret_anova(self, rows: List[List[Any]]) -> str:
        """Basic interpretation text for ANOVA table."""
        if not rows:
            return "No ANOVA results."
        sig_count = sum(1 for r in rows if bool(r[3]))
        total = len(rows)
        return f"{sig_count}/{total} dimensions show significant differences."

    def _interpret_correlations(self, rows: List[Dict[str, Any]]) -> str:
        if not rows:
            return "No significant correlations."
        strong = [r for r in rows if r.get('correlation') is not None and abs(r['correlation']) >= 0.6]
        return f"{len(strong)} strong associations (|r| ≥ 0.6) among top pairs."

    def _interpret_reliability(self, alpha: float) -> str:
        """Interpret Cronbach's alpha value."""
        if alpha >= 0.9:
            return "Excellent"
        elif alpha >= 0.8:
            return "Good"
        elif alpha >= 0.7:
            return "Acceptable"
        elif alpha >= 0.6:
            return "Questionable"
        else:
            return "Poor"

    def _interpret_overall_reliability(self, rows: List[List[Any]]) -> str:
        """Overall interpretation of reliability results."""
        if not rows:
            return "No reliability data available."
        
        excellent = sum(1 for r in rows if r[3] == "Excellent")
        good = sum(1 for r in rows if r[3] == "Good") 
        acceptable = sum(1 for r in rows if r[3] == "Acceptable")
        questionable = sum(1 for r in rows if r[3] == "Questionable")
        poor = sum(1 for r in rows if r[3] == "Poor")
        
        total = len(rows)
        reliable = excellent + good + acceptable
        
        if reliable >= total * 0.8:
            return f"Strong measurement reliability: {reliable}/{total} dimensions acceptable or better."
        elif reliable >= total * 0.6:
            return f"Moderate measurement reliability: {reliable}/{total} dimensions acceptable or better."
        else:
            return f"Weak measurement reliability: {reliable}/{total} dimensions acceptable or better."

    def _assess_framework_fit(self, anova_summary: Optional[Dict], 
                             reliability_summary: Optional[Dict],
                             descriptive_summary: Optional[Dict]) -> Dict[str, Any]:
        """
        Assess framework fit based on available statistical data using descriptive approach.
        
        Comprehensive validation: ANOVA + Reliability data
        Internal consistency validation: Reliability data only
        Descriptive pattern analysis: Descriptive statistics only
        """
        # Determine validation approach based on available data
        has_anova = anova_summary is not None
        has_reliability = reliability_summary is not None
        has_descriptive = descriptive_summary is not None
        
        if has_anova and has_reliability:
            quality_level = "Comprehensive statistical validation"
            assessment = self._comprehensive_fit_assessment(anova_summary, reliability_summary)
        elif has_reliability:
            quality_level = "Internal consistency validation"
            assessment = self._reliability_fit_assessment(reliability_summary)
        elif has_descriptive:
            quality_level = "Descriptive pattern analysis"
            assessment = self._descriptive_fit_assessment(descriptive_summary)
        else:
            quality_level = "Limited validation"
            assessment = "Insufficient statistical data for framework fit assessment."
        
        return {
            "quality_level": quality_level,
            "framework_fit_conclusion": assessment,
            "data_available": {
                "anova": has_anova,
                "reliability": has_reliability, 
                "descriptive": has_descriptive
            }
        }

    def _comprehensive_fit_assessment(self, anova_summary: Dict, reliability_summary: Dict) -> str:
        """Comprehensive assessment: ANOVA + Reliability data available."""
        anova_interp = anova_summary.get('interpretation', '')
        reliability_interp = reliability_summary.get('interpretation', '')
        
        # Extract key metrics
        anova_rows = anova_summary.get('rows', [])
        reliability_rows = reliability_summary.get('rows', [])
        
        significant_dimensions = sum(1 for r in anova_rows if r[3])  # significant flag
        total_dimensions = len(anova_rows)
        reliable_dimensions = sum(1 for r in reliability_rows if r[3] in ["Excellent", "Good", "Acceptable"])
        
        if significant_dimensions >= total_dimensions * 0.7 and reliable_dimensions >= len(reliability_rows) * 0.7:
            return f"Strong framework fit: {significant_dimensions}/{total_dimensions} dimensions show significant variation with {reliable_dimensions}/{len(reliability_rows)} reliable measurements."
        elif significant_dimensions >= total_dimensions * 0.5 and reliable_dimensions >= len(reliability_rows) * 0.6:
            return f"Moderate framework fit: {significant_dimensions}/{total_dimensions} dimensions show significant variation with {reliable_dimensions}/{len(reliability_rows)} reliable measurements."
        else:
            return f"Weak framework fit: {significant_dimensions}/{total_dimensions} dimensions show significant variation with {reliable_dimensions}/{len(reliability_rows)} reliable measurements."

    def _reliability_fit_assessment(self, reliability_summary: Dict) -> str:
        """Reliability assessment: Internal consistency data available."""
        reliability_rows = reliability_summary.get('rows', [])
        reliable_dimensions = sum(1 for r in reliability_rows if r[3] in ["Excellent", "Good", "Acceptable"])
        total = len(reliability_rows)
        
        if reliable_dimensions >= total * 0.8:
            return f"Good measurement quality: {reliable_dimensions}/{total} dimensions show acceptable reliability."
        elif reliable_dimensions >= total * 0.6:
            return f"Moderate measurement quality: {reliable_dimensions}/{total} dimensions show acceptable reliability."
        else:
            return f"Poor measurement quality: {reliable_dimensions}/{total} dimensions show acceptable reliability."

    def _descriptive_fit_assessment(self, descriptive_summary: Dict) -> str:
        """Descriptive assessment: Pattern analysis using variance indicators."""
        desc_rows = descriptive_summary.get('rows', [])
        if not desc_rows:
            return "No descriptive statistics available for framework fit assessment."
        
        # Use variance as a proxy for framework fit (higher variance = better discrimination)
        variance_indicators = []
        for row in desc_rows:
            mean = row[1]
            std = row[2]
            if mean is not None and std is not None and mean != 0:
                cv = std / abs(mean)  # coefficient of variation
                variance_indicators.append(cv)
        
        if variance_indicators:
            avg_cv = sum(variance_indicators) / len(variance_indicators)
            if avg_cv >= 0.3:
                return f"Good score variance: Average CV = {avg_cv:.2f} suggests framework dimensions discriminate well."
            elif avg_cv >= 0.2:
                return f"Moderate score variance: Average CV = {avg_cv:.2f} suggests reasonable discrimination."
            else:
                return f"Low score variance: Average CV = {avg_cv:.2f} suggests limited discrimination."
        else:
            return "Unable to assess framework fit from available descriptive statistics."
