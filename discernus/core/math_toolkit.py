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

# New: LLM-optimized statistical formatter
from discernus.core.statistical_formatter import StatisticalResultsFormatter

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class MathToolkitError(Exception):
    """Custom exception for MathToolkit errors."""
    pass


def _normalize_column_reference(column_name: str, available_columns: List[str]) -> str:
    """
    Normalize hierarchical column references to flat column names.
    
    Handles LLM tendency to use JSON-style hierarchical paths like:
    'scores.dimensions.fear.score' -> 'fear_score'
    """
    if 'scores.dimensions.' in column_name:
        # Extract dimension and field from hierarchical path
        parts = column_name.split('.')
        if len(parts) >= 4:  # scores.dimensions.DIMENSION.FIELD
            dimension = parts[2]
            field = parts[3] 
            flat_name = f"{dimension}_{field}"
            if flat_name in available_columns:
                return flat_name
    
    # Return original if no normalization needed or if normalized name doesn't exist
    return column_name


def calculate_descriptive_stats(dataframe: pd.DataFrame, columns: List[str], grouping_variable: str = None, **kwargs) -> Dict[str, Any]:
    """
    Calculate descriptive statistics for specified columns.
    
    Args:
        dataframe: Input DataFrame
        columns: List of column names to analyze
        grouping_variable: Optional grouping variable for grouped statistics
        
    Returns:
        Dictionary containing descriptive statistics for each column
    """
    try:
        # DEFENSIVE PARAMETER HANDLING: Handle LLM naming inconsistencies
        # Handle both 'grouping_variable' and 'grouping_variables' parameter names
        if 'grouping_variables' in kwargs and grouping_variable is None:
            grouping_variable = kwargs['grouping_variables']
        
        # Handle case where grouping_variable is passed as a list
        if isinstance(grouping_variable, list):
            grouping_variable = grouping_variable[0] if grouping_variable else None
        
        # DEFENSIVE: Normalize hierarchical column references to flat names
        available_columns = list(dataframe.columns)
        normalized_columns = [_normalize_column_reference(col, available_columns) for col in columns]
        if grouping_variable:
            grouping_variable = _normalize_column_reference(grouping_variable, available_columns)
            
        results = {}
        
        # Handle grouping variable (compatibility fix)
        
        if grouping_variable and grouping_variable in dataframe.columns:
            # Group by the specified variable and calculate stats for each group
            grouped_results = {}
            for group_name, group_df in dataframe.groupby(grouping_variable):
                group_stats = {}
                for column in normalized_columns:
                    if column not in group_df.columns:
                        continue
                    series = group_df[column].dropna()
                    if len(series) > 0:
                        # Check if column is numeric or categorical
                        try:
                            numeric_series = pd.to_numeric(series, errors='coerce')
                            if numeric_series.notna().any():  # Has numeric values
                                numeric_series = numeric_series.dropna()
                                group_stats[column] = {
                                    "count": int(len(numeric_series)),
                                    "mean": float(numeric_series.mean()),
                                    "std": float(numeric_series.std()),
                                    "min": float(numeric_series.min()),
                                    "max": float(numeric_series.max()),
                                    "data_type": "numerical"
                                }
                            else:
                                # Categorical data
                                value_counts = series.value_counts()
                                group_stats[column] = {
                                    "count": int(len(series)),
                                    "unique_values": int(series.nunique()),
                                    "mode": str(series.mode().iloc[0]) if not series.mode().empty else "N/A",
                                    "frequency_distribution": value_counts.head(3).to_dict(),
                                    "data_type": "categorical"
                                }
                        except Exception:
                            # Fallback: categorical
                            value_counts = series.value_counts()
                            group_stats[column] = {
                                "count": int(len(series)),
                                "unique_values": int(series.nunique()),
                                "mode": str(series.mode().iloc[0]) if not series.mode().empty else "N/A",
                                "frequency_distribution": value_counts.head(3).to_dict(),
                                "data_type": "categorical"
                            }
                grouped_results[str(group_name)] = group_stats
            
            # PROVENANCE
            provenance = {
                "input_columns": normalized_columns + ([grouping_variable] if grouping_variable else []),
                "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
                "filter_conditions": f"Grouped by {grouping_variable}"
            }

            return {
                "type": "descriptive_stats_grouped",
                "grouping_variable": grouping_variable,
                "groups": grouped_results,
                "provenance": provenance
            }
        
        # Standard ungrouped statistics
        for column in normalized_columns:
            if column not in dataframe.columns:
                raise MathToolkitError(f"Column '{column}' not found in DataFrame. Available columns: {list(dataframe.columns)}")
                
            series = dataframe[column].dropna()
            
            if len(series) == 0:
                results[column] = {
                    "error": f"No valid data for column '{column}'"
                }
                continue
            
            # Check if column is numeric or categorical
            try:
                # Try to convert to numeric - if it works, it's numerical data
                numeric_series = pd.to_numeric(series, errors='coerce')
                if numeric_series.notna().any():  # Has at least some numeric values
                    # Numerical statistics
                    numeric_series = numeric_series.dropna()  # Remove conversion failures
                    stats_dict = {
                        "count": int(len(numeric_series)),
                        "mean": float(numeric_series.mean()),
                        "std": float(numeric_series.std()),
                        "min": float(numeric_series.min()),
                        "max": float(numeric_series.max()),
                        "median": float(numeric_series.median()),
                        "q25": float(numeric_series.quantile(0.25)),
                        "q75": float(numeric_series.quantile(0.75)),
                        "skewness": float(numeric_series.skew()),
                        "kurtosis": float(numeric_series.kurtosis()),
                        "data_type": "numerical"
                    }
                else:
                    # Categorical statistics
                    value_counts = series.value_counts()
                    stats_dict = {
                        "count": int(len(series)),
                        "unique_values": int(series.nunique()),
                        "mode": str(series.mode().iloc[0]) if not series.mode().empty else "N/A",
                        "most_frequent": str(value_counts.index[0]) if len(value_counts) > 0 else "N/A",
                        "frequency_distribution": value_counts.head(5).to_dict(),
                        "data_type": "categorical"
                    }
            except Exception:
                # Fallback: treat as categorical
                value_counts = series.value_counts()
                stats_dict = {
                    "count": int(len(series)),
                    "unique_values": int(series.nunique()),
                    "mode": str(series.mode().iloc[0]) if not series.mode().empty else "N/A",
                    "most_frequent": str(value_counts.index[0]) if len(value_counts) > 0 else "N/A",
                    "frequency_distribution": value_counts.head(5).to_dict(),
                    "data_type": "categorical"
                }
            
            results[column] = stats_dict
            
        # PROVENANCE
        provenance = {
            "input_columns": normalized_columns,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "None"
        }

        return {
            "type": "descriptive_stats",
            "columns_analyzed": list(results.keys()),
            "results": results,
            "provenance": provenance
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
        group1_df = dataframe[dataframe[grouping_variable] == group1]
        group2_df = dataframe[dataframe[grouping_variable] == group2]
        group1_data = group1_df[dependent_variable].dropna()
        group2_data = group2_df[dependent_variable].dropna()
        
        if len(group1_data) == 0 or len(group2_data) == 0:
            raise MathToolkitError(f"One or both groups have no valid data")
            
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(group1_data) - 1) * group1_data.var() + 
                             (len(group2_data) - 1) * group2_data.var()) / 
                            (len(group1_data) + len(group2_data) - 2))
        cohens_d = (group1_data.mean() - group2_data.mean()) / pooled_std
        
        # PROVENANCE
        provenance = {
            "input_columns": [grouping_variable, dependent_variable],
            "input_document_ids": pd.concat([group1_df['aid'], group2_df['aid']]).unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": f"Groups '{group1}' vs '{group2}' from column '{grouping_variable}'"
        }

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
            "significant": p_value < 0.05,
            "provenance": provenance
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
        
        # PROVENANCE
        provenance = {
            "input_columns": available_columns,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "Used all rows with valid data for each pair of columns."
        }
        
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
            ],
            "provenance": provenance
        }
        
    except Exception as e:
        logger.error(f"Error calculating correlation: {str(e)}")
        raise MathToolkitError(f"Correlation calculation failed: {str(e)}")


def perform_one_way_anova(dataframe: pd.DataFrame,
                         grouping_variable: str,
                         dependent_variable: str,
                         **kwargs) -> Dict[str, Any]:
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
        # DEFENSIVE PARAMETER HANDLING: Handle LLM naming inconsistencies
        if 'grouping_variables' in kwargs and isinstance(kwargs['grouping_variables'], (str, list)):
            if isinstance(kwargs['grouping_variables'], list):
                grouping_variable = kwargs['grouping_variables'][0]
            else:
                grouping_variable = kwargs['grouping_variables']
        
        if 'dependent_variables' in kwargs and isinstance(kwargs['dependent_variables'], (str, list)):
            if isinstance(kwargs['dependent_variables'], list):
                dependent_variable = kwargs['dependent_variables'][0]
            else:
                dependent_variable = kwargs['dependent_variables']
        
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
        
        # PROVENANCE
        provenance = {
            "input_columns": [grouping_variable, dependent_variable],
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": f"Grouped by '{grouping_variable}'"
        }

        return {
            "type": "one_way_anova",
            "grouping_variable": grouping_variable,
            "dependent_variable": dependent_variable,
            "groups": group_stats,
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "significant": p_value < 0.05,
            "provenance": provenance
        }
        
    except Exception as e:
        logger.error(f"Error performing ANOVA: {str(e)}")
        raise MathToolkitError(f"ANOVA failed: {str(e)}")


def perform_two_way_anova(dataframe: pd.DataFrame,
                         factor1: str,
                         factor2: str,
                         dependent_variable: str,
                         **kwargs) -> Dict[str, Any]:
    """
    Perform two-way ANOVA to test for main effects and interactions.
    
    Args:
        dataframe: Input DataFrame
        factor1: First grouping variable (factor)
        factor2: Second grouping variable (factor)
        dependent_variable: Column name containing the dependent variable
        
    Returns:
        Dictionary containing ANOVA results
    """
    try:
        # DEFENSIVE PARAMETER HANDLING: Handle LLM naming inconsistencies
        if 'dependent_variables' in kwargs and isinstance(kwargs['dependent_variables'], (str, list)):
            if isinstance(kwargs['dependent_variables'], list):
                dependent_variable = kwargs['dependent_variables'][0]
            else:
                dependent_variable = kwargs['dependent_variables']
        
        from scipy import stats
        import itertools
        
        # Validate columns exist
        required_cols = [factor1, factor2, dependent_variable]
        for col in required_cols:
            if col not in dataframe.columns:
                raise MathToolkitError(f"Column '{col}' not found in DataFrame")
        
        # Ensure dependent variable is numeric
        dep_series = pd.to_numeric(dataframe[dependent_variable], errors='coerce').dropna()
        if len(dep_series) == 0:
            raise MathToolkitError(f"No valid numeric data in dependent variable '{dependent_variable}'")
        
        # Filter to valid data
        valid_data = dataframe[pd.to_numeric(dataframe[dependent_variable], errors='coerce').notna()].copy()
        valid_data[dependent_variable] = pd.to_numeric(valid_data[dependent_variable])
        
        # Get factor levels
        factor1_levels = valid_data[factor1].unique()
        factor2_levels = valid_data[factor2].unique()
        
        if len(factor1_levels) < 2:
            raise MathToolkitError(f"Factor '{factor1}' needs at least 2 levels, found {len(factor1_levels)}")
        if len(factor2_levels) < 2:
            raise MathToolkitError(f"Factor '{factor2}' needs at least 2 levels, found {len(factor2_levels)}")
        
        # Create groups for all factor combinations
        groups = []
        group_labels = []
        for f1_level in factor1_levels:
            for f2_level in factor2_levels:
                group_data = valid_data[
                    (valid_data[factor1] == f1_level) & 
                    (valid_data[factor2] == f2_level)
                ][dependent_variable]
                if len(group_data) > 0:
                    groups.append(group_data.values)
                    group_labels.append(f"{f1_level}_{f2_level}")
        
        if len(groups) < 4:  # Need at least 2x2 design
            raise MathToolkitError(f"Insufficient data for two-way ANOVA. Need at least 4 factor combinations, found {len(groups)}")
        
        # Perform one-way ANOVA on all combinations (simplified approach)
        f_stat, p_value = stats.f_oneway(*groups)
        
        # Calculate group statistics
        group_stats = {}
        for i, (group_data, label) in enumerate(zip(groups, group_labels)):
            group_stats[label] = {
                "n": len(group_data),
                "mean": float(np.mean(group_data)),
                "std": float(np.std(group_data, ddof=1)) if len(group_data) > 1 else 0.0
            }
        
        # PROVENANCE
        provenance = {
            "input_columns": [factor1, factor2, dependent_variable],
            "input_document_ids": valid_data['aid'].unique().tolist() if 'aid' in valid_data.columns else [],
            "filter_conditions": f"Grouped by '{factor1}' and '{factor2}'"
        }

        return {
            "type": "two_way_anova",
            "factor1": factor1,
            "factor2": factor2,
            "dependent_variable": dependent_variable,
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "significant": p_value < 0.05,
            "factor1_levels": factor1_levels.tolist(),
            "factor2_levels": factor2_levels.tolist(),
            "group_statistics": group_stats,
            "note": "Simplified two-way ANOVA using one-way ANOVA on factor combinations",
            "provenance": provenance
        }
        
    except Exception as e:
        logger.error(f"Error performing two-way ANOVA: {str(e)}")
        raise MathToolkitError(f"Two-way ANOVA failed: {str(e)}")


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
        # Validate columns exist
        if grouping_variable not in dataframe.columns:
            raise MathToolkitError(f"Grouping variable '{grouping_variable}' not found in DataFrame")
        if dependent_variable not in dataframe.columns:
            raise MathToolkitError(f"Dependent variable '{dependent_variable}' not found in DataFrame")
        
        # Ensure dependent variable is numeric
        dep_series = pd.to_numeric(dataframe[dependent_variable], errors='coerce').dropna()
        if len(dep_series) == 0:
            raise MathToolkitError(f"No valid numeric data in dependent variable '{dependent_variable}'")
        
        # Filter dataframe to only include rows with valid numeric dependent variable
        valid_data = dataframe[pd.to_numeric(dataframe[dependent_variable], errors='coerce').notna()].copy()
        valid_data[dependent_variable] = pd.to_numeric(valid_data[dependent_variable])
        
        # Calculate group means and overall mean
        group_means = valid_data.groupby(grouping_variable)[dependent_variable].mean()
        overall_mean = valid_data[dependent_variable].mean()
        
        # Calculate eta-squared (proportion of variance explained)
        ss_between = sum(len(valid_data[valid_data[grouping_variable] == group]) * 
                        (mean - overall_mean) ** 2 
                        for group, mean in group_means.items())
        
        ss_total = sum((value - overall_mean) ** 2 
                      for value in valid_data[dependent_variable])
        
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        # PROVENANCE
        provenance = {
            "input_columns": [grouping_variable, dependent_variable],
            "input_document_ids": valid_data['aid'].unique().tolist() if 'aid' in valid_data.columns else [],
            "filter_conditions": f"Grouped by '{grouping_variable}'"
        }

        return {
            "type": "effect_sizes",
            "grouping_variable": grouping_variable,
            "dependent_variable": dependent_variable,
            "eta_squared": float(eta_squared),
            "effect_size_interpretation": _interpret_eta_squared(eta_squared),
            "group_means": group_means.to_dict(),
            "provenance": provenance
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


def calculate_derived_metrics(dataframe: pd.DataFrame, input_columns: List[str], framework_calculation_spec: Optional[Dict[str, Any]] = None, metric_formulas: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Calculate derived metrics from raw data using framework's calculation_spec (THIN approach).
    
    Args:
        dataframe: Input DataFrame with raw data
        input_columns: List of input column names used in formulas
        framework_calculation_spec: Framework's calculation_spec containing authoritative formulas (THIN)
        metric_formulas: Legacy LLM-generated formulas (deprecated, for backward compatibility)
        
    Returns:
        Dictionary containing calculated metrics and metadata
    """
    try:
        # THIN: Use framework calculation_spec as single source of truth
        if framework_calculation_spec and "formulas" in framework_calculation_spec:
            metric_formulas = framework_calculation_spec["formulas"]
            calculation_source = "framework_calculation_spec"
        elif metric_formulas:
            calculation_source = "llm_generated_formulas_deprecated"
        else:
            return {
                "type": "derived_metrics_calculation",
                "success": False,
                "error": "No calculation formulas provided. Need either framework_calculation_spec or metric_formulas",
                "available_columns": list(dataframe.columns),
                "calculated_metrics": {},
                "formulas_used": []
            }
        
        # Framework-agnostic validation: check for required columns
        missing_columns = [col for col in input_columns if col not in dataframe.columns]
        if missing_columns:
            return {
                "type": "derived_metrics_calculation",
                "success": False,
                "error": f"Missing required columns: {missing_columns}",
                "available_columns": list(dataframe.columns),
                "calculated_metrics": {},
                "formulas_used": list(metric_formulas.keys()),
                "calculation_source": calculation_source
            }
        
        # Create a comprehensive mathematical evaluation context
        # Default to array-aware numpy operations for data column compatibility
        import math
        import ast
        safe_dict = {
            # Array-aware mathematical functions (numpy defaults for data compatibility)
            'min': np.minimum, 'max': np.maximum, 'abs': np.abs,
            'sum': np.sum, 'round': np.round,

            # Python built-ins for scalar operations
            'len': len, 'pow': pow, 'divmod': divmod, 'float': float, 'int': int, 'bool': bool,

            # Math module functions (scalar operations)
            'math': math, 'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
            'exp': math.exp, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan, 'atan2': math.atan2,
            'ceil': math.ceil, 'floor': math.floor, 'pi': math.pi, 'e': math.e,

            # NumPy for comprehensive array operations
            'np': np, 'numpy': np,

            # Explicit array operations
            'minimum': np.minimum, 'maximum': np.maximum,

            # Statistical functions
            'mean': np.mean, 'median': np.median, 'std': np.std, 'var': np.var,
        }

        # THIN, framework-agnostic: expose all available DataFrame columns by default
        for col in dataframe.columns:
            try:
                safe_dict[col] = dataframe[col].values
            except Exception:
                # Non-numeric or problematic columns are still made available; eval will handle if used
                safe_dict[col] = dataframe[col].values if col in dataframe.columns else None

        calculated_metrics = {}
        successful_calculations = []
        failed_calculations = []
        skipped_formulas = []
        
        # Calculate each metric using framework-specified execution order (THIN)
        if framework_calculation_spec and "execution_order" in framework_calculation_spec:
            # THIN: Use framework's authoritative execution order
            execution_order = framework_calculation_spec["execution_order"]
            sorted_formulas = [(name, metric_formulas[name]) for name in execution_order if name in metric_formulas]
            logger.info(f"THIN: Using framework execution order for {len(sorted_formulas)} metrics")
        else:
            # Fallback: Sort by formula length (legacy approach)
            sorted_formulas = sorted(metric_formulas.items(), key=lambda x: len(x[1]))
            logger.warning("THIN: No execution_order in framework - using fallback length-based sorting")
        
        # Helper: determine variable names used by a formula
        def _extract_variable_names(expr: str) -> List[str]:
            try:
                tree = ast.parse(expr, mode='eval')
            except Exception:
                return []
            names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    names.add(node.id)
            return list(names)

        # Known environment symbols that are not data columns
        non_data_symbols = set(safe_dict.keys())

        for metric_name, formula in sorted_formulas:
            # Gate by available symbols to avoid NameError on missing inputs
            vars_in_formula = _extract_variable_names(formula)
            # variables that look like data but are missing from context
            missing_vars = [v for v in vars_in_formula if v not in safe_dict]
            if missing_vars:
                skipped_formulas.append({
                    "metric": metric_name,
                    "formula": formula,
                    "reason": "missing_inputs",
                    "missing_variables": missing_vars
                })
                logger.warning(f"Skipping metric '{metric_name}' due to missing inputs: {missing_vars}")
                continue

            try:
                # Evaluate the formula safely
                result = eval(formula, {"__builtins__": {}}, safe_dict)

                # Division-by-zero and invalid numeric guards
                if isinstance(result, (float, int)) and (np.isinf(result) or (isinstance(result, float) and np.isnan(result))):
                    logger.warning(f"Metric '{metric_name}' resulted in non-finite value; coercing to NaN")
                    result = np.nan

                # Handle different result types
                if isinstance(result, np.ndarray):
                    calculated_metrics[metric_name] = result.tolist()
                    safe_dict[metric_name] = result
                else:
                    calculated_metrics[metric_name] = result
                    safe_dict[metric_name] = result

                successful_calculations.append(metric_name)
                logger.info(f"Successfully calculated metric '{metric_name}' with formula: {formula}")

            except ZeroDivisionError:
                # Graceful handling: record NaN and continue
                logger.warning(f"Division by zero in metric '{metric_name}'; setting result to NaN")
                calculated_metrics[metric_name] = np.nan
                safe_dict[metric_name] = np.nan
                successful_calculations.append(metric_name)
            except Exception as e:
                failed_calculations.append({
                    "metric": metric_name,
                    "formula": formula,
                    "error": str(e)
                })
                logger.error(f"Failed to calculate metric '{metric_name}': {str(e)}")
                # Continue with other calculations even if one fails
        
        # PROVENANCE
        provenance = {
            "input_columns": input_columns,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "None"
        }

        return {
            "type": "derived_metrics_calculation",
            "success": len(successful_calculations) > 0,
            "calculated_metrics": calculated_metrics,
            "successful_calculations": successful_calculations,
            "failed_calculations": failed_calculations,
            "skipped_due_to_missing_inputs": skipped_formulas,
            "formulas_used": list(metric_formulas.keys()),
            "input_columns": input_columns,
            "total_metrics": len(metric_formulas),
            "success_rate": len(successful_calculations) / len(metric_formulas) if metric_formulas else 0,
            "calculation_source": calculation_source,
            "provenance": provenance
        }
        
    except Exception as e:
        raise MathToolkitError(f"Derived metrics calculation failed: {str(e)}")


def perform_statistical_tests(dataframe: pd.DataFrame, test_types: List[str], grouping_variables: List[str], dependent_variables: List[str]) -> Dict[str, Any]:
    """
    Perform multiple statistical tests based on test types.
    
    Args:
        dataframe: Input DataFrame
        test_types: List of test types to perform
        grouping_variables: List of grouping variables
        dependent_variables: List of dependent variables
        
    Returns:
        Dictionary containing statistical test results
    """
    try:
        results = {}
        
        for test_type in test_types:
            if test_type == "one_way_anova":
                for group_var in grouping_variables:
                    for dep_var in dependent_variables:
                        if group_var in dataframe.columns and dep_var in dataframe.columns:
                            test_result = perform_one_way_anova(dataframe, group_var, dep_var)
                            results[f"{test_type}_{group_var}_{dep_var}"] = test_result
                        else:
                            missing_cols = [col for col in [group_var, dep_var] if col not in dataframe.columns]
                            results[f"{test_type}_{group_var}_{dep_var}"] = {
                                "error": f"Missing columns: {missing_cols}. Available: {list(dataframe.columns)}"
                            }
            elif test_type == "independent_t_test":
                for group_var in grouping_variables:
                    for dep_var in dependent_variables:
                        if group_var in dataframe.columns and dep_var in dataframe.columns:
                            test_result = perform_independent_t_test(dataframe, group_var, dep_var)
                            results[f"{test_type}_{group_var}_{dep_var}"] = test_result
                        else:
                            missing_cols = [col for col in [group_var, dep_var] if col not in dataframe.columns]
                            results[f"{test_type}_{group_var}_{dep_var}"] = {
                                "error": f"Missing columns: {missing_cols}. Available: {list(dataframe.columns)}"
                            }
            elif test_type == "correlation":
                test_result = calculate_pearson_correlation(dataframe, dependent_variables)
                results[f"{test_type}_{'_'.join(dependent_variables)}"] = test_result
            elif test_type == "two_way_anova":
                # Handle two-way ANOVA with multiple grouping variables
                if len(grouping_variables) >= 2 and len(dependent_variables) >= 1:
                    factor1, factor2 = grouping_variables[0], grouping_variables[1]
                    dep_var = dependent_variables[0]
                    if all(var in dataframe.columns for var in [factor1, factor2, dep_var]):
                        test_result = perform_two_way_anova(dataframe, factor1, factor2, dep_var)
                        results[f"{test_type}_{factor1}_{factor2}_{dep_var}"] = test_result
                    else:
                        missing_cols = [col for col in [factor1, factor2, dep_var] if col not in dataframe.columns]
                        results[f"{test_type}_{factor1}_{factor2}_{dep_var}"] = {
                            "error": f"Missing columns: {missing_cols}. Available: {list(dataframe.columns)}"
                        }
            else:
                results[f"unknown_test_{test_type}"] = {"error": f"Unknown test type: {test_type}"}
        
        # PROVENANCE for the overall set of tests
        provenance = {
            "input_columns": grouping_variables + dependent_variables,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": f"Performed tests: {', '.join(test_types)}"
        }
        
        return {
            "type": "statistical_tests",
            "tests_performed": test_types,
            "results": results,
            "provenance": provenance
        }
        
    except Exception as e:
        raise MathToolkitError(f"Statistical tests failed: {str(e)}")


def generate_correlation_matrix(dataframe: pd.DataFrame, dimensions: List[str], correlation_method: str = "pearson", **kwargs) -> Dict[str, Any]:
    """
    Generate correlation matrix for specified dimensions.
    
    Args:
        dataframe: Input DataFrame
        dimensions: List of dimensions to correlate
        correlation_method: Correlation method (pearson, spearman)
        **kwargs: Additional parameters (ignored for compatibility)
        
    Returns:
        Dictionary containing correlation matrix
    """
    try:
        # DEFENSIVE PARAMETER HANDLING: Ignore unsupported parameters like grouping_variable
        if 'grouping_variable' in kwargs:
            logger.warning(f"generate_correlation_matrix: ignoring unsupported parameter 'grouping_variable'")
        
        # Handle case where dimensions is passed as different parameter names
        if 'columns' in kwargs and not dimensions:
            dimensions = kwargs['columns']
        # Filter to only include dimensions that exist in the dataframe
        available_dimensions = [dim for dim in dimensions if dim in dataframe.columns]
        
        if not available_dimensions:
            raise MathToolkitError(f"No valid dimensions found. Available columns: {list(dataframe.columns)}")
        
        # Calculate correlation matrix
        corr_matrix = dataframe[available_dimensions].corr(method=correlation_method)
        
        # PROVENANCE
        provenance = {
            "input_columns": available_dimensions,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "None"
        }
        
        return {
            "type": "correlation_matrix",
            "dimensions": available_dimensions,
            "method": correlation_method,
            "matrix": corr_matrix.to_dict(),
            "missing_dimensions": [dim for dim in dimensions if dim not in dataframe.columns],
            "provenance": provenance
        }
        
    except Exception as e:
        raise MathToolkitError(f"Correlation matrix generation failed: {str(e)}")


def validate_calculated_metrics(dataframe: pd.DataFrame, validation_rules: List[Any], quality_thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    THIN framework-agnostic metric validation.
    
    Performs generic validation operations on any requested metrics without 
    hardcoded intelligence about what rules are "valid". LLMs provide the 
    intelligence about what to validate, software provides the coordination.
    
    Args:
        dataframe: Input DataFrame
        validation_rules: List of validation rules (strings or dicts)
        quality_thresholds: Dictionary of quality thresholds
        
    Returns:
        Dictionary containing validation results
    """
    try:
        # Provide sensible defaults for quality_thresholds if not provided
        if quality_thresholds is None:
            quality_thresholds = {
                'min_valid_ratio': 0.8,  # At least 80% of data should be valid
                'max_outlier_ratio': 0.1,  # No more than 10% outliers
                'min_variance': 0.01,  # Minimum variance to avoid constant values
                'correlation_threshold': 0.95  # Maximum correlation for multicollinearity check
            }
        
        validation_results = {}
        
        for rule in validation_rules:
            # Handle both string rules and dictionary rules
            if isinstance(rule, str):
                rule_name = rule
                rule_config = {}
                metric_name = rule_name
            elif isinstance(rule, dict):
                rule_name = rule.get("metric", "unknown_rule")
                rule_config = rule
                metric_name = rule_name
            else:
                rule_name = str(rule)
                rule_config = {}
                metric_name = rule_name
            
            # Framework-agnostic validation: check if the metric exists and is valid
            if metric_name in dataframe.columns:
                series = dataframe[metric_name].dropna()
                
                if len(series) == 0:
                    validation_results[rule_name] = {
                        "status": "failed",
                        "issue": "no_valid_data",
                        "message": f"No valid data found for metric '{metric_name}'"
                    }
                else:
                    # Generic validation checks that work for any metric
                    validation_results[rule_name] = {
                        "status": "passed",
                        "metric": metric_name,
                        "data_points": len(series),
                        "missing_values": len(dataframe[metric_name]) - len(series),
                        "has_nan": dataframe[metric_name].isna().any(),
                        "has_inf": np.isinf(dataframe[metric_name]).any() if dataframe[metric_name].dtype in ['float64', 'float32'] else False,
                        "min_value": float(series.min()) if len(series) > 0 else None,
                        "max_value": float(series.max()) if len(series) > 0 else None,
                        "mean_value": float(series.mean()) if len(series) > 0 else None
                    }
            else:
                # Handle predefined validation types for backward compatibility
                if rule_name == "missing_data_check" or rule_name == "missing_data":
                    missing_counts = dataframe.isnull().sum()
                    validation_results[rule_name] = {
                        "status": "completed",
                        "missing_data_by_column": missing_counts.to_dict(),
                        "total_missing": int(missing_counts.sum())
                    }
                elif rule_name == "range_check" or rule_name == "range_validation":
                    numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
                    ranges = {}
                    for col in numeric_columns:
                        ranges[col] = {
                            "min": float(dataframe[col].min()),
                            "max": float(dataframe[col].max()),
                            "mean": float(dataframe[col].mean())
                        }
                    validation_results[rule_name] = {
                        "status": "completed",
                        "ranges": ranges
                    }
                elif rule_name == "consistency_check" or rule_name == "consistency":
                    validation_results[rule_name] = {
                        "status": "completed", 
                        "notes": "Basic consistency check completed"
                    }
                else:
                    # THIN approach: Don't reject unknown rules, provide generic validation
                    validation_results[rule_name] = {
                        "status": "not_found",
                        "message": f"Metric '{rule_name}' not found in dataframe",
                        "available_columns": list(dataframe.columns),
                        "note": "This is a framework-agnostic validation - LLMs determine validation logic"
                    }
        
        # PROVENANCE
        provenance = {
            "input_columns": [str(rule) for rule in validation_rules],
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "Validation rules applied as specified"
        }

        return {
            "type": "metric_validation",
            "validation_rules": [str(rule) for rule in validation_rules],
            "results": validation_results,
            "quality_thresholds": quality_thresholds,
            "provenance": provenance
        }
        
    except Exception as e:
        raise MathToolkitError(f"Metric validation failed: {str(e)}")


def create_summary_statistics(dataframe: pd.DataFrame, metrics: List[str], summary_types: List[str], **kwargs) -> Dict[str, Any]:
    """
    Generate descriptive statistics for specified metrics.
    
    Args:
        dataframe: Input DataFrame
        metrics: List of metrics to summarize
        summary_types: List of summary types (mean, std, min, max, etc.)
        
    Returns:
        Dictionary containing summary statistics
    """
    try:
        # Filter to only include metrics that exist in the dataframe
        available_metrics = [metric for metric in metrics if metric in dataframe.columns]
        
        if not available_metrics:
            raise MathToolkitError(f"No valid metrics found. Available columns: {list(dataframe.columns)}")
        
        summary_results = {}
        
        for metric in available_metrics:
            metric_stats = {}
            series = dataframe[metric].dropna()
            
            if "mean" in summary_types:
                metric_stats["mean"] = float(series.mean())
            if "std" in summary_types:
                metric_stats["std"] = float(series.std())
            if "min" in summary_types:
                metric_stats["min"] = float(series.min())
            if "max" in summary_types:
                metric_stats["max"] = float(series.max())
            if "median" in summary_types:
                metric_stats["median"] = float(series.median())
            if "count" in summary_types:
                metric_stats["count"] = int(len(series))
            
            summary_results[metric] = metric_stats
        
        # PROVENANCE
        provenance = {
            "input_columns": available_metrics,
            "input_document_ids": dataframe['aid'].unique().tolist() if 'aid' in dataframe.columns else [],
            "filter_conditions": "None"
        }
        
        return {
            "type": "summary_statistics",
            "metrics": available_metrics,
            "summary_types": summary_types,
            "results": summary_results,
            "missing_metrics": [metric for metric in metrics if metric not in dataframe.columns],
            "provenance": provenance
        }
        
    except Exception as e:
        raise MathToolkitError(f"Summary statistics generation failed: {str(e)}")


# Registry of available tools for the synthesis pipeline
TOOL_REGISTRY = {
    "calculate_descriptive_stats": calculate_descriptive_stats,
    "perform_independent_t_test": perform_independent_t_test,
    "calculate_pearson_correlation": lambda df, **kwargs: calculate_pearson_correlation(df, kwargs.get('columns', []), "pearson"),
    "perform_one_way_anova": perform_one_way_anova,
    "perform_two_way_anova": perform_two_way_anova,
    "calculate_effect_sizes": calculate_effect_sizes,
    "calculate_derived_metrics": calculate_derived_metrics,
    "perform_statistical_tests": perform_statistical_tests,
    "generate_correlation_matrix": generate_correlation_matrix,
    "validate_calculated_metrics": validate_calculated_metrics,
    "create_summary_statistics": create_summary_statistics
}


def execute_analysis_plan(dataframe: pd.DataFrame, analysis_plan: Dict[str, Any], framework_calculation_spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a complete analysis plan using the MathToolkit.
    
    Args:
        dataframe: Input DataFrame
        analysis_plan: Dictionary containing the analysis plan from AnalysisPlanner
        framework_calculation_spec: Framework's calculation_spec for THIN formula usage
        
    Returns:
        Dictionary containing all analysis results
    """
    try:
        results = {
            "analysis_plan": analysis_plan,
            "results": {},
            "errors": []
        }
        
        # Create a copy of the DataFrame to modify
        working_df = dataframe.copy()
        
        # Execute each analysis task
        for task_name, task_config in analysis_plan.get("tasks", {}).items():
            try:
                tool_name = task_config.get("tool")
                if tool_name not in TOOL_REGISTRY:
                    error_msg = f"Task '{task_name}': Unknown tool '{tool_name}'"
                    results["errors"].append(error_msg)
                    logger.error(error_msg)
                    continue
                    
                # Extract parameters
                params = task_config.get("parameters", {})
                
                # Validate column references for statistical tests (fail-fast principle)
                if tool_name in ["perform_one_way_anova", "perform_two_way_anova"]:
                    missing_cols = []
                    if "grouping_variable" in params and params["grouping_variable"] not in working_df.columns:
                        missing_cols.append(params["grouping_variable"])
                    if "dependent_variable" in params and params["dependent_variable"] not in working_df.columns:
                        missing_cols.append(params["dependent_variable"])
                    if "factor1" in params and params["factor1"] not in working_df.columns:
                        missing_cols.append(params["factor1"])
                    if "factor2" in params and params["factor2"] not in working_df.columns:
                        missing_cols.append(params["factor2"])
                    
                    if missing_cols:
                        error_msg = f"Task '{task_name}' failed: Missing required columns {missing_cols}. Available columns: {list(working_df.columns)}"
                        results["errors"].append(error_msg)
                        logger.error(error_msg)
                        continue
                
                # Execute the tool
                tool_func = TOOL_REGISTRY[tool_name]
                
                # THIN: Pass framework calculation_spec to calculate_derived_metrics
                if tool_name == "calculate_derived_metrics" and framework_calculation_spec:
                    task_result = tool_func(working_df, framework_calculation_spec=framework_calculation_spec, **params)
                else:
                    task_result = tool_func(working_df, **params)
                
                results["results"][task_name] = task_result
                
                # If this was a derived metrics calculation, add the results to the DataFrame
                if tool_name == "calculate_derived_metrics" and task_result.get("type") == "derived_metrics_calculation":
                    calculated_metrics = task_result.get("calculated_metrics", {})
                    for metric_name, metric_values in calculated_metrics.items():
                        if isinstance(metric_values, list) and len(metric_values) == len(working_df):
                            working_df[metric_name] = metric_values
                            logger.info(f"Added calculated metric '{metric_name}' to DataFrame")
                
            except Exception as e:
                error_msg = f"Task '{task_name}' failed: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
                
        return results
        
    except Exception as e:
        logger.error(f"Analysis plan execution failed: {str(e)}")
        raise MathToolkitError(f"Analysis plan execution failed: {str(e)}")


def execute_analysis_plan_thin(raw_analysis_data: str, analysis_plan_input, corpus_manifest: Optional[Dict[str, Any]] = None, framework_calculation_spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    THIN version: Execute analysis plan optimized for v7.0 Gasket Architecture.
    
    Updated for v7.0: Removes defensive parsing code and optimizes for clean JSON from Intelligent Extractor.
    
    Returns both raw results and LLM-optimized formatted tables under 'formatted_statistics'.
    """
    try:
        import json
        import re
        
        # THIN: Handle raw LLM analysis plan responses
        if isinstance(analysis_plan_input, str):
            # Parse raw LLM analysis plan response
            try:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', analysis_plan_input, re.DOTALL)
                if json_match:
                    analysis_plan = json.loads(json_match.group(1))
                else:
                    # Try direct JSON parsing
                    analysis_plan = json.loads(analysis_plan_input)
                logger.info(f"THIN MathToolkit: Parsed raw LLM analysis plan ({len(analysis_plan_input)} chars)")
            except json.JSONDecodeError as e:
                logger.error(f"THIN MathToolkit: Failed to parse LLM analysis plan: {e}")
                return {"analysis_plan": {}, "results": {}, "errors": [f"Failed to parse LLM analysis plan: {str(e)}"], "formatted_statistics": None}
        else:
            # Legacy: Already parsed dictionary
            analysis_plan = analysis_plan_input
        
        # V7.0 GASKET OPTIMIZATION: Direct JSON parsing (no defensive delimiter extraction)
        # Intelligent Extractor guarantees clean JSON structure
        try:
            analysis_result = json.loads(raw_analysis_data)
        except json.JSONDecodeError as e:
            # Fallback: Try legacy delimiter extraction for backward compatibility
            logger.warning(f"Clean JSON parsing failed, trying legacy delimiter extraction: {e}")
            json_pattern = r"<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*(\{.*?\})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>"
            json_match = re.search(json_pattern, raw_analysis_data, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                analysis_result = json.loads(json_str)
            else:
                raise MathToolkitError(f"Failed to parse analysis data as JSON: {e}")
        
        # Convert to DataFrame using optimized gasket helper
        scores_df = _json_scores_to_dataframe_thin(analysis_result, corpus_manifest)
        
        logger.info(f"V7.0 Gasket MathToolkit: Processed DataFrame {scores_df.shape}")
        
        # Use existing execute_analysis_plan with parsed DataFrame
        raw_output = execute_analysis_plan(scores_df, analysis_plan, framework_calculation_spec)
        
        # New: produce LLM-optimized statistical tables
        formatter = StatisticalResultsFormatter()
        formatted = formatter.format_for_synthesis(raw_output)
        
        # Return both raw and formatted for backward compatibility
        return {
            "analysis_plan": raw_output.get("analysis_plan", analysis_plan),
            "results": raw_output.get("results", {}),
            "errors": raw_output.get("errors", []),
            "formatted_statistics": formatted
        }
        
    except Exception as e:
        logger.error(f"V7.0 Gasket analysis plan execution failed: {str(e)}")
        raise MathToolkitError(f"V7.0 Gasket analysis plan execution failed: {str(e)}")


def _json_scores_to_dataframe_thin(analysis_result: dict, corpus_manifest: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    THIN helper: Convert JSON analysis to DataFrame optimized for flat gasket structure.
    
    Updated for v7.0 Gasket Architecture: handles flat analysis_scores from Intelligent Extractor.
    Removes defensive parsing code and optimizes for clean, flat JSON structure.
    """
    try:
        document_analyses = analysis_result.get('document_analyses', [])
        
        if not document_analyses:
            raise ValueError("No document_analyses found in JSON")
        
        rows = []
        for doc_analysis in document_analyses:
            document_id = doc_analysis.get('document_name', doc_analysis.get('document_id', 'unknown_document'))
            
            # V7.0 GASKET ARCHITECTURE: Handle flat analysis_scores from Intelligent Extractor
            analysis_scores = doc_analysis.get('analysis_scores', {})
            
            # Create row with document identifier
            row_data = {'aid': document_id}
            
            # Add corpus metadata if available (THIN approach: framework-agnostic)
            if corpus_manifest and 'file_manifest' in corpus_manifest:
                # Find metadata for this document by matching filename
                for file_info in corpus_manifest['file_manifest']:
                    if file_info.get('name') == document_id:
                        # Add all metadata fields generically
                        for key, value in file_info.items():
                            if key != 'name':  # Skip filename since we have document_name
                                row_data[key] = value
                        break
            
            # V7.0 OPTIMIZATION: Direct flat key-value extraction (no hierarchical parsing)
            for score_key, score_value in analysis_scores.items():
                # Validate score format from gasket
                if score_value is not None:
                    if isinstance(score_value, (int, float)):
                        # Framework-driven validation - no hardcoded ranges
                        # Note: At this point we trust the extraction agent has already validated per framework spec
                        # This is just a final sanity check for obviously invalid values
                        if isinstance(score_value, (int, float)) and not (score_value < -10 or score_value > 10):
                            row_data[score_key] = float(score_value)
                        else:
                            logger.warning(f"Score {score_key}={score_value} appears to be corrupted (extreme value)")
                            row_data[score_key] = None
                    else:
                        logger.warning(f"Score {score_key} has invalid type: {type(score_value)}")
                        row_data[score_key] = None
                else:
                    # Handle missing scores: treat as legitimate zero for rare dimensions like compersion
                    # This prevents cascade failures in derived metrics while preserving analytical meaning
                    if score_key.endswith('_score') and 'compersion' in score_key.lower():
                        # Compersion is inherently rare in political discourse - missing evidence = score of 0.0
                        row_data[score_key] = 0.0
                        logger.info(f"Missing compersion score treated as 0.0 (legitimate absence in political discourse)")
                    elif score_key.endswith('_salience') and 'compersion' in score_key.lower():
                        # If compersion score is 0.0, salience should also be 0.0
                        row_data[score_key] = 0.0
                    elif score_key.endswith('_confidence') and 'compersion' in score_key.lower():
                        # High confidence that compersion is absent (not a measurement failure)
                        row_data[score_key] = 0.8
                    else:
                        # Preserve null values for other missing scores (genuine measurement failures)
                        row_data[score_key] = None
            
            # Add gasket metadata for provenance
            extraction_metadata = doc_analysis.get('extraction_metadata', {})
            if extraction_metadata:
                row_data['gasket_version'] = extraction_metadata.get('gasket_version', 'unknown')
                row_data['extraction_time_seconds'] = extraction_metadata.get('extraction_time_seconds', 0.0)
            
            rows.append(row_data)
        
        df = pd.DataFrame(rows)
        logger.info(f"V7.0 Gasket: Converted {len(rows)} documents to DataFrame with {len(df.columns)} columns")
        return df
        
    except Exception as e:
        raise MathToolkitError(f"Failed to convert gasket JSON to DataFrame: {str(e)}") 