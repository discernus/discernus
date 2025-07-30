"""
MathToolkit: Pre-built, tested mathematical and statistical functions for Discernus.

This module provides a reliable, predictable set of mathematical operations
that replace the fragile LLM-generated code execution in the synthesis pipeline.

All functions are designed to work with pandas DataFrames and return structured
dictionaries that can be easily serialized to JSON.
"""

import logging
from typing import Dict, List, Any, Optional, Union
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class MathToolkitError(Exception):
    """Custom exception for MathToolkit errors."""
    pass


def calculate_descriptive_stats(dataframe: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
    """
    Calculate descriptive statistics for specified columns.
    
    Args:
        dataframe: Input DataFrame
        columns: List of column names to analyze
        
    Returns:
        Dictionary containing descriptive statistics for each column
    """
    try:
        results = {}
        
        for column in columns:
            if column not in dataframe.columns:
                raise MathToolkitError(f"Column '{column}' not found in DataFrame. Available columns: {list(dataframe.columns)}")
                
            series = dataframe[column].dropna()
            
            if len(series) == 0:
                results[column] = {
                    "error": f"No valid data for column '{column}'"
                }
                continue
            
            stats_dict = {
                "count": int(len(series)),
                "mean": float(series.mean()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "median": float(series.median()),
                "q25": float(series.quantile(0.25)),
                "q75": float(series.quantile(0.75)),
                "skewness": float(series.skew()),
                "kurtosis": float(series.kurtosis())
            }
            
            results[column] = stats_dict
            
        return {
            "type": "descriptive_stats",
            "columns_analyzed": list(results.keys()),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error calculating descriptive stats: {str(e)}")
        raise MathToolkitError(f"Descriptive stats calculation failed: {str(e)}")


def perform_independent_t_test(dataframe: pd.DataFrame, 
                             grouping_variable: str, 
                             dependent_variable: str,
                             group1: Optional[str] = None,
                             group2: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform independent t-test between two groups.
    
    Args:
        dataframe: Input DataFrame
        grouping_variable: Column name containing group labels
        dependent_variable: Column name containing the dependent variable
        group1: First group label (if None, uses first two unique values)
        group2: Second group label (if None, uses first two unique values)
        
    Returns:
        Dictionary containing t-test results
    """
    try:
        # Validate inputs
        if grouping_variable not in dataframe.columns:
            raise MathToolkitError(f"Grouping variable '{grouping_variable}' not found in DataFrame")
        if dependent_variable not in dataframe.columns:
            raise MathToolkitError(f"Dependent variable '{dependent_variable}' not found in DataFrame")
            
        # Get unique groups
        unique_groups = dataframe[grouping_variable].dropna().unique()
        if len(unique_groups) < 2:
            raise MathToolkitError(f"Need at least 2 groups, found {len(unique_groups)}")
            
        # Select groups
        if group1 is None:
            group1 = str(unique_groups[0])
        if group2 is None:
            group2 = str(unique_groups[1])
            
        # Extract data for each group
        group1_data = dataframe[dataframe[grouping_variable] == group1][dependent_variable].dropna()
        group2_data = dataframe[dataframe[grouping_variable] == group2][dependent_variable].dropna()
        
        if len(group1_data) == 0 or len(group2_data) == 0:
            raise MathToolkitError(f"One or both groups have no valid data")
            
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(group1_data) - 1) * group1_data.var() + 
                             (len(group2_data) - 1) * group2_data.var()) / 
                            (len(group1_data) + len(group2_data) - 2))
        cohens_d = (group1_data.mean() - group2_data.mean()) / pooled_std
        
        return {
            "type": "independent_t_test",
            "grouping_variable": grouping_variable,
            "dependent_variable": dependent_variable,
            "group1": {
                "label": group1,
                "n": int(len(group1_data)),
                "mean": float(group1_data.mean()),
                "std": float(group1_data.std())
            },
            "group2": {
                "label": group2,
                "n": int(len(group2_data)),
                "mean": float(group2_data.mean()),
                "std": float(group2_data.std())
            },
            "test_statistic": float(t_stat),
            "p_value": float(p_value),
            "effect_size": float(cohens_d),
            "significant": p_value < 0.05
        }
        
    except Exception as e:
        logger.error(f"Error performing t-test: {str(e)}")
        raise MathToolkitError(f"T-test failed: {str(e)}")


def calculate_pearson_correlation(dataframe: pd.DataFrame, 
                                columns: List[str],
                                method: str = "pearson") -> Dict[str, Any]:
    """
    Calculate correlation matrix for specified columns.
    
    Args:
        dataframe: Input DataFrame
        columns: List of column names to correlate
        method: Correlation method ("pearson" or "spearman")
        
    Returns:
        Dictionary containing correlation matrix and significance tests
    """
    try:
        # Validate inputs
        if method not in ["pearson", "spearman"]:
            raise MathToolkitError(f"Method must be 'pearson' or 'spearman', got '{method}'")
            
        # Filter to requested columns
        available_columns = [col for col in columns if col in dataframe.columns]
        if len(available_columns) < 2:
            raise MathToolkitError(f"Need at least 2 valid columns, found {len(available_columns)}")
            
        # Calculate correlation matrix
        corr_matrix = dataframe[available_columns].corr(method=method)
        
        # Calculate significance tests for each pair
        significance_matrix = {}
        for i, col1 in enumerate(available_columns):
            significance_matrix[col1] = {}
            for j, col2 in enumerate(available_columns):
                if i == j:
                    significance_matrix[col1][col2] = 1.0  # Perfect correlation with self
                else:
                    # Remove rows where either column has NaN
                    clean_data = dataframe[[col1, col2]].dropna()
                    if len(clean_data) < 3:
                        significance_matrix[col1][col2] = None
                    else:
                        if method == "pearson":
                            corr, p_val = pearsonr(clean_data[col1], clean_data[col2])
                        else:  # spearman
                            corr, p_val = spearmanr(clean_data[col1], clean_data[col2])
                        significance_matrix[col1][col2] = float(p_val)
        
        return {
            "type": f"{method}_correlation",
            "columns": available_columns,
            "correlation_matrix": corr_matrix.to_dict(),
            "significance_matrix": significance_matrix,
            "significant_pairs": [
                (col1, col2, corr_matrix.loc[col1, col2], significance_matrix[col1][col2])
                for i, col1 in enumerate(available_columns)
                for j, col2 in enumerate(available_columns)
                if i < j and significance_matrix[col1][col2] is not None and significance_matrix[col1][col2] < 0.05
            ]
        }
        
    except Exception as e:
        logger.error(f"Error calculating correlation: {str(e)}")
        raise MathToolkitError(f"Correlation calculation failed: {str(e)}")


def perform_one_way_anova(dataframe: pd.DataFrame,
                         grouping_variable: str,
                         dependent_variable: str) -> Dict[str, Any]:
    """
    Perform one-way ANOVA to test for differences between multiple groups.
    
    Args:
        dataframe: Input DataFrame
        grouping_variable: Column name containing group labels
        dependent_variable: Column name containing the dependent variable
        
    Returns:
        Dictionary containing ANOVA results
    """
    try:
        # Validate inputs
        if grouping_variable not in dataframe.columns:
            raise MathToolkitError(f"Grouping variable '{grouping_variable}' not found in DataFrame")
        if dependent_variable not in dataframe.columns:
            raise MathToolkitError(f"Dependent variable '{dependent_variable}' not found in DataFrame")
            
        # Get groups
        groups = dataframe.groupby(grouping_variable)[dependent_variable].apply(list)
        group_labels = list(groups.index)
        
        if len(group_labels) < 2:
            raise MathToolkitError(f"Need at least 2 groups for ANOVA, found {len(group_labels)}")
            
        # Filter out NaN values from each group
        clean_groups = []
        for group_name, group_values in groups.items():
            clean_values = [v for v in group_values if pd.notna(v)]
            if len(clean_values) > 0:
                clean_groups.append(clean_values)
        
        if len(clean_groups) < 2:
            raise MathToolkitError(f"Need at least 2 groups with valid data for ANOVA")
            
        # Perform ANOVA
        f_stat, p_value = stats.f_oneway(*clean_groups)
        
        # Calculate group statistics
        group_stats = {}
        for label, values in groups.items():
            values = [v for v in values if pd.notna(v)]
            if len(values) > 0:
                group_stats[str(label)] = {
                    "n": int(len(values)),
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values))
                }
        
        return {
            "type": "one_way_anova",
            "grouping_variable": grouping_variable,
            "dependent_variable": dependent_variable,
            "groups": group_stats,
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "significant": p_value < 0.05
        }
        
    except Exception as e:
        logger.error(f"Error performing ANOVA: {str(e)}")
        raise MathToolkitError(f"ANOVA failed: {str(e)}")


def calculate_effect_sizes(dataframe: pd.DataFrame,
                          grouping_variable: str,
                          dependent_variable: str) -> Dict[str, Any]:
    """
    Calculate effect sizes (eta-squared) for group differences.
    
    Args:
        dataframe: Input DataFrame
        grouping_variable: Column name containing group labels
        dependent_variable: Column name containing the dependent variable
        
    Returns:
        Dictionary containing effect size calculations
    """
    try:
        # Calculate group means and overall mean
        group_means = dataframe.groupby(grouping_variable)[dependent_variable].mean()
        overall_mean = dataframe[dependent_variable].mean()
        
        # Calculate eta-squared (proportion of variance explained)
        ss_between = sum(len(dataframe[dataframe[grouping_variable] == group]) * 
                        (mean - overall_mean) ** 2 
                        for group, mean in group_means.items())
        
        ss_total = sum((value - overall_mean) ** 2 
                      for value in dataframe[dependent_variable].dropna())
        
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return {
            "type": "effect_sizes",
            "grouping_variable": grouping_variable,
            "dependent_variable": dependent_variable,
            "eta_squared": float(eta_squared),
            "effect_size_interpretation": _interpret_eta_squared(eta_squared),
            "group_means": group_means.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error calculating effect sizes: {str(e)}")
        raise MathToolkitError(f"Effect size calculation failed: {str(e)}")


def _interpret_eta_squared(eta_squared: float) -> str:
    """Interpret eta-squared effect size."""
    if eta_squared < 0.01:
        return "negligible"
    elif eta_squared < 0.06:
        return "small"
    elif eta_squared < 0.14:
        return "medium"
    else:
        return "large"


# Registry of available tools for the synthesis pipeline
TOOL_REGISTRY = {
    "descriptive_stats": calculate_descriptive_stats,
    "independent_t_test": perform_independent_t_test,
    "pearson_correlation": lambda df, **kwargs: calculate_pearson_correlation(df, kwargs.get('columns', []), "pearson"),
    "spearman_correlation": lambda df, **kwargs: calculate_pearson_correlation(df, kwargs.get('columns', []), "spearman"),
    "one_way_anova": perform_one_way_anova,
    "effect_sizes": calculate_effect_sizes
}


def execute_analysis_plan(dataframe: pd.DataFrame, analysis_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a complete analysis plan using the MathToolkit.
    
    Args:
        dataframe: Input DataFrame
        analysis_plan: Dictionary containing the analysis plan from AnalysisPlanner
        
    Returns:
        Dictionary containing all analysis results
    """
    try:
        results = {
            "analysis_plan": analysis_plan,
            "results": {},
            "errors": []
        }
        
        # Execute each analysis task
        for task_name, task_config in analysis_plan.get("tasks", {}).items():
            try:
                tool_name = task_config.get("tool")
                if tool_name not in TOOL_REGISTRY:
                    results["errors"].append(f"Unknown tool: {tool_name}")
                    continue
                    
                # Extract parameters
                params = task_config.get("parameters", {})
                
                # Execute the tool
                tool_func = TOOL_REGISTRY[tool_name]
                task_result = tool_func(dataframe, **params)
                
                results["results"][task_name] = task_result
                
            except Exception as e:
                error_msg = f"Task '{task_name}' failed: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
                
        return results
        
    except Exception as e:
        logger.error(f"Analysis plan execution failed: {str(e)}")
        raise MathToolkitError(f"Analysis plan execution failed: {str(e)}") 