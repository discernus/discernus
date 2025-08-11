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
                df_between = task_result.get('df_between')
                df_within = task_result.get('df_within')
                effect_size = task_result.get('effect_size')
                row = [dimension, f_stat, p_value, significant]
                # Append optional fields if available
                if df_between is not None and df_within is not None:
                    row.extend([int(df_between), int(df_within)])
                if effect_size is not None:
                    row.append(float(effect_size))
                anova_rows.append(row)

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
                    reliability_rows.append([
                        dimension,
                        alpha_value,
                        [ci_lower, ci_upper],
                    ])

        # Assemble tables
        anova_summary = None
        if anova_rows:
            # Determine headers dynamically based on presence of optional fields
            has_df = any(len(r) >= 6 for r in anova_rows)
            has_effect = any((len(r) == 7) or (len(r) >= 7) for r in anova_rows)
            headers = ["Dimension", "F-Statistic", "P-Value", "Significant"]
            if has_df:
                headers.extend(["DF Between", "DF Within"])
            if has_effect:
                headers.append("Eta Squared")
            anova_rows_sorted = sorted(
                anova_rows,
                key=lambda row: (0.0 if row[1] is None else -row[1])  # sort by F desc, None last
            )
            anova_summary = {
                "table_format": "ANOVA Results Table",
                "headers": headers,
                "rows": anova_rows_sorted
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
                "rows": correlation_sorted
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
                "headers": ["Dimension", "Cronbach's Alpha", "95% CI"],
                "rows": reliability_rows
            }

        return {
            "anova_summary": anova_summary,
            "correlation_summary": correlation_summary,
            "descriptive_summary": descriptive_summary,
            "reliability_summary": reliability_summary,
        }

    def _interpret_reliability(self, alpha: float) -> str:
        """DEPRECATED: Basic interpretation text for Cronbach's Alpha."""
        if alpha >= 0.9:
            return "Excellent"
        elif alpha >= 0.8:
            return "Good"
        elif alpha >= 0.7:
            return "Acceptable"
        elif alpha >= 0.6:
            return "Questionable"
        elif alpha >= 0.5:
            return "Poor"
        else:
            return "Unacceptable"
