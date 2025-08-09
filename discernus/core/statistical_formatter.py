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
        if not self.results or 'results' not in self.results:
            return {
                "anova_summary": None,
                "correlation_summary": None,
                "descriptive_summary": None,
                "notes": "No results provided"
            }

        results = self.results

        anova_rows: List[List[Any]] = []
        correlation_top: List[Dict[str, Any]] = []
        descriptive_rows: List[List[Any]] = []

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
                # Prefer significant_pairs if available
                sig_pairs = task_result.get('significant_pairs', [])
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

        return {
            "anova_summary": anova_summary,
            "correlation_summary": correlation_summary,
            "descriptive_summary": descriptive_summary
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
