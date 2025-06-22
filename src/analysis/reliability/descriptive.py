import logging
from typing import Dict, List
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr, spearmanr

# Import the interpretive functions that were moved to other modules
from .icc import interpret_icc
from .cronbach import interpret_cronbach_alpha

logger = logging.getLogger(__name__)


def calculate_pairwise_correlations(df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[str, any]:
    logger.info("📊 Calculating pairwise correlations...")
    correlations: Dict[str, any] = {}
    for well_col in well_columns:
        well_correlations: Dict[str, any] = {}
        for i, model1 in enumerate(models):
            for model2 in models[i+1:]:
                model1_data = df[df['model'] == model1][well_col].dropna()
                model2_data = df[df['model'] == model2][well_col].dropna()
                if 'text_id' in df.columns:
                    m1_df = df[df['model'] == model1][['text_id', well_col]].dropna()
                    m2_df = df[df['model'] == model2][['text_id', well_col]].dropna()
                    merged = m1_df.merge(m2_df, on='text_id', suffixes=('_1', '_2'))
                    if len(merged) >= 2:
                        pearson_r, pearson_p = pearsonr(merged[f'{well_col}_1'], merged[f'{well_col}_2'])
                        spearman_r, spearman_p = spearmanr(merged[f'{well_col}_1'], merged[f'{well_col}_2'])
                        well_correlations[f"{model1}_vs_{model2}"] = {
                            'pearson_r': float(pearson_r),
                            'pearson_p': float(pearson_p),
                            'spearman_r': float(spearman_r),
                            'spearman_p': float(spearman_p),
                            'n_pairs': len(merged),
                            'significant': pearson_p < 0.05
                        }
        correlations[well_col] = well_correlations
    return correlations


def calculate_coefficient_of_variation(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    logger.info("📊 Calculating coefficient of variation...")
    cv_results: Dict[str, any] = {}
    for well_col in well_columns:
        well_data = df[well_col].dropna()
        if len(well_data) > 0:
            mean_score = well_data.mean()
            std_score = well_data.std()
            cv = (std_score / mean_score) * 100 if mean_score != 0 else 0
            cv_results[well_col] = {
                'coefficient_of_variation': float(cv),
                'mean': float(mean_score),
                'std': float(std_score),
                'interpretation': interpret_cv(cv),
                'sample_size': len(well_data)
            }
    return cv_results


def interpret_cv(cv: float) -> str:
    if cv < 10:
        return 'very_low_variability'
    if cv < 20:
        return 'low_variability'
    if cv < 30:
        return 'moderate_variability'
    if cv < 50:
        return 'high_variability'
    return 'very_high_variability'


def detect_outliers(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    logger.info("🔍 Detecting outliers...")
    outlier_results: Dict[str, any] = {}
    for well_col in well_columns:
        well_data = df[well_col].dropna()
        if len(well_data) > 0:
            z_scores = np.abs(stats.zscore(well_data))
            outliers_z = well_data[z_scores > 2.5]
            q1 = well_data.quantile(0.25)
            q3 = well_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers_iqr = well_data[(well_data < lower_bound) | (well_data > upper_bound)]
            outlier_results[well_col] = {
                'z_score_outliers': {
                    'count': len(outliers_z),
                    'percentage': (len(outliers_z) / len(well_data)) * 100,
                    'values': outliers_z.tolist()
                },
                'iqr_outliers': {
                    'count': len(outliers_iqr),
                    'percentage': (len(outliers_iqr) / len(well_data)) * 100,
                    'values': outliers_iqr.tolist(),
                    'bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)}
                }
            }
    return outlier_results


def analyze_systematic_bias(df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[str, any]:
    logger.info("🔍 Analyzing systematic bias...")
    bias_results: Dict[str, any] = {}
    for well_col in well_columns:
        model_means: Dict[str, any] = {}
        for model in models:
            model_data = df[df['model'] == model][well_col].dropna()
            if len(model_data) > 0:
                model_means[model] = {
                    'mean': float(model_data.mean()),
                    'std': float(model_data.std()),
                    'count': len(model_data)
                }
        if len(model_means) > 1:
            all_means = [stats['mean'] for stats in model_means.values()]
            mean_of_means = np.mean(all_means)
            std_of_means = np.std(all_means)
            if len(models) > 2:
                model_data_lists = []
                for model in models:
                    data = df[df['model'] == model][well_col].dropna()
                    if len(data) > 0:
                        model_data_lists.append(data.values)
                if len(model_data_lists) > 1:
                    try:
                        f_stat, p_value = stats.f_oneway(*model_data_lists)
                        bias_results[well_col] = {
                            'model_means': model_means,
                            'overall_mean': float(mean_of_means),
                            'std_of_means': float(std_of_means),
                            'anova_f_stat': float(f_stat),
                            'anova_p_value': float(p_value),
                            'significant_bias': p_value < 0.05
                        }
                    except Exception as e:
                        logger.warning(f"ANOVA failed for {well_col}: {e}")
                        bias_results[well_col] = {
                            'model_means': model_means,
                            'overall_mean': float(mean_of_means),
                            'std_of_means': float(std_of_means),
                            'error': str(e)
                        }
    return bias_results


def calculate_descriptive_reliability_stats(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    stats_results: Dict[str, any] = {}
    for well_col in well_columns:
        scores = df[well_col].dropna()
        if len(scores) > 0:
            stats_results[well_col] = {
                'count': len(scores),
                'mean': float(scores.mean()),
                'std': float(scores.std()),
                'min': float(scores.min()),
                'max': float(scores.max()),
                'range': float(scores.max() - scores.min()),
                'cv': float((scores.std() / scores.mean()) * 100) if scores.mean() != 0 else 0
            }
    return stats_results


def calculate_internal_consistency(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    try:
        well_matrix = df[well_columns].dropna()
        if well_matrix.empty or well_matrix.shape[1] < 2:
            return {'error': 'Insufficient data for internal consistency analysis'}
        odd_cols = well_columns[::2]
        even_cols = well_columns[1::2]
        if len(odd_cols) > 0 and len(even_cols) > 0:
            odd_scores = well_matrix[odd_cols].sum(axis=1)
            even_scores = well_matrix[even_cols].sum(axis=1)
            if len(odd_scores) > 1 and len(even_scores) > 1:
                split_half_r, split_half_p = pearsonr(odd_scores, even_scores)
                spearman_brown = (2 * split_half_r) / (1 + split_half_r)
                return {
                    'split_half_correlation': float(split_half_r),
                    'split_half_p_value': float(split_half_p),
                    'spearman_brown_coefficient': float(spearman_brown)
                }
        return {'error': 'Could not calculate split-half reliability'}
    except Exception as e:
        return {'error': str(e)}


def generate_reliability_summary(reliability_results: Dict) -> Dict[str, any]:
    summary = {
        'overall_reliability': 'unknown',
        'key_findings': [],
        'recommendations': [],
        'quality_indicators': {}
    }
    
    # Process ICC results using the interpret_icc function
    icc_results = reliability_results.get('icc_analysis', {})
    if icc_results:
        icc_values = [r.get('icc_value') for r in icc_results.values() if r.get('icc_value') is not None]
        if icc_values:
            avg_icc = np.mean(icc_values)
            summary['quality_indicators']['average_icc'] = float(avg_icc)
            
            # Use the interpret_icc function for proper interpretation
            icc_interpretation = interpret_icc(avg_icc)
            summary['key_findings'].append(f"Average ICC: {avg_icc:.3f} ({icc_interpretation})")
            
            # Add specific recommendations based on ICC interpretation
            if 'poor' in icc_interpretation.lower() or 'below' in icc_interpretation.lower():
                summary['recommendations'].append("Consider increasing sample size or improving rater training - ICC indicates poor reliability")
            elif 'moderate' in icc_interpretation.lower():
                summary['recommendations'].append("ICC shows moderate reliability - consider refinements to improve consistency")
    
    # Process Cronbach's Alpha results using the interpret_cronbach_alpha function  
    alpha_result = reliability_results.get('cronbach_alpha', {})
    if alpha_result.get('alpha_value') is not None:
        alpha = alpha_result['alpha_value']
        summary['quality_indicators']['cronbach_alpha'] = float(alpha)
        
        # Use the interpret_cronbach_alpha function for proper interpretation
        alpha_interpretation = interpret_cronbach_alpha(alpha)
        summary['key_findings'].append(f"Cronbach's Alpha: {alpha:.3f} ({alpha_interpretation})")
        
        # Add specific recommendations based on Alpha interpretation
        if 'unacceptable' in alpha_interpretation.lower() or 'poor' in alpha_interpretation.lower():
            summary['recommendations'].append("Review internal consistency - Cronbach's Alpha indicates poor reliability")
        elif 'questionable' in alpha_interpretation.lower():
            summary['recommendations'].append("Consider reviewing scale items - Alpha suggests questionable internal consistency")
    
    # Determine overall reliability using interpretive functions instead of hardcoded thresholds
    icc_good = 'good' in interpret_icc(summary['quality_indicators'].get('average_icc', 0)).lower() or \
               'excellent' in interpret_icc(summary['quality_indicators'].get('average_icc', 0)).lower()
    alpha_good = 'good' in interpret_cronbach_alpha(summary['quality_indicators'].get('cronbach_alpha', 0)).lower() or \
                 'acceptable' in interpret_cronbach_alpha(summary['quality_indicators'].get('cronbach_alpha', 0)).lower() or \
                 'excellent' in interpret_cronbach_alpha(summary['quality_indicators'].get('cronbach_alpha', 0)).lower()
    
    if icc_good and alpha_good:
        summary['overall_reliability'] = 'excellent'
    elif icc_good or alpha_good:
        summary['overall_reliability'] = 'good'
    else:
        summary['overall_reliability'] = 'needs_improvement'
    
    return summary
