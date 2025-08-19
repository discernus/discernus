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
                        mean_val = stats.get('mean', None)
                        std_val = stats.get('std', None)
                        cv_val = None
                        try:
                            if mean_val is not None and std_val is not None and float(mean_val) != 0:
                                cv_val = float(std_val) / abs(float(mean_val))
                        except Exception:
                            cv_val = None
                        descriptive_rows.append([
                            col,
                            float(mean_val) if mean_val is not None else None,
                            float(std_val) if std_val is not None else None,
                            float(stats.get('min', 0.0)) if stats.get('min') is not None else None,
                            float(stats.get('max', 0.0)) if stats.get('max') is not None else None,
                            cv_val
                        ])
            
            # Reliability analysis (Cronbach's alpha) - for unidimensional frameworks
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
            
            # Oppositional validation - for oppositional frameworks
            elif rtype in ('oppositional_validation',):
                axis_name = task_result.get('axis_name', task_name)
                correlation = task_result.get('negative_correlation')
                is_oppositional = task_result.get('is_oppositional', False)
                discriminant_p = task_result.get('discriminant_validity_p')
                
                if correlation is not None:
                    reliability_rows.append([
                        axis_name,
                        float(correlation),
                        "✓" if is_oppositional else "✗",
                        discriminant_p if discriminant_p is not None else "N/A"
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
                "headers": ["Dimension", "Mean", "Std Dev", "Min", "Max", "CV"],
                "rows": descriptive_rows
            }

        reliability_summary = None
        if reliability_rows:
            # Determine if we have oppositional validation or traditional reliability
            has_oppositional = any(len(row) >= 4 for row in reliability_rows)
            
            if has_oppositional:
                reliability_summary = {
                    "table_format": "Oppositional Construct Validation",
                    "headers": ["Axis", "Correlation", "Oppositional", "Discriminant p-value"],
                    "rows": reliability_rows
                }
            else:
                reliability_summary = {
                    "table_format": "Measurement Reliability Table", 
                    "headers": ["Dimension", "Cronbach's Alpha", "95% CI"],
                    "rows": reliability_rows
                }

        # Deterministic fit diagnostics to avoid LLM arithmetic
        fit_diagnostics = None
        if anova_summary or reliability_summary:
            alpha_threshold = 0.70
            significance_alpha = 0.05
            significant_dims = []
            if anova_summary and anova_summary.get("rows"):
                for row in anova_summary["rows"]:
                    # row: [dimension, f, p, significant, (optional df, df, eta2)]
                    dim = row[0]
                    is_sig = bool(row[3])
                    pval = row[2]
                    # Trust provided significant flag; fallback to p-value if needed
                    if is_sig or (pval is not None and pval < significance_alpha):
                        significant_dims.append(dim)
            reliability_ok_dims = []
            reliability_poor_dims = []
            if reliability_summary and reliability_summary.get("rows"):
                for row in reliability_summary["rows"]:
                    dim = row[0]
                    alpha_val = row[1]
                    if alpha_val is not None and float(alpha_val) >= alpha_threshold:
                        reliability_ok_dims.append(dim)
                    else:
                        reliability_poor_dims.append(dim)
            combined_fit_dims = sorted(list(set(significant_dims).intersection(set(reliability_ok_dims))))
            # Diagnostics lists for refinement
            failed_significance = sorted([d for d in reliability_ok_dims if d not in significant_dims])
            failed_reliability = sorted([d for d in significant_dims if d not in reliability_ok_dims])
            total_dims = 0
            # Prefer ANOVA row count as denominator; else reliability
            if anova_summary and anova_summary.get("rows"):
                total_dims = len({r[0] for r in anova_summary["rows"]})
            elif reliability_summary and reliability_summary.get("rows"):
                total_dims = len({r[0] for r in reliability_summary["rows"]})
            fit_percent = (len(combined_fit_dims) / total_dims) if total_dims > 0 else None
            fit_diagnostics = {
                "thresholds": {
                    "significance_alpha": significance_alpha,
                    "reliability_alpha_threshold": alpha_threshold
                },
                "counts": {
                    "total_dimensions": total_dims,
                    "significant_dimensions": len(significant_dims),
                    "acceptable_reliability_dimensions": len(reliability_ok_dims),
                    "combined_fit_dimensions": len(combined_fit_dims)
                },
                "percentages": {
                    "combined_fit_percentage": fit_percent
                },
                "dimensions": {
                    "significant": sorted(list(set(significant_dims))),
                    "acceptable_reliability": sorted(list(set(reliability_ok_dims))),
                    "combined_fit": combined_fit_dims,
                    "failed_significance": failed_significance,
                    "failed_reliability": failed_reliability,
                    "poor_reliability": sorted(list(set(reliability_poor_dims)))
                }
            }

        return {
            "anova_summary": anova_summary,
            "correlation_summary": correlation_summary,
            "descriptive_summary": descriptive_summary,
            "reliability_summary": reliability_summary,
            "fit_diagnostics": fit_diagnostics,
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
