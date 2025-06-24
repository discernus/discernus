"""
Interrater Reliability Analysis System for Multi-LLM Narrative Gravity Analysis
Calculates ICC, Cronbach's Alpha, and other reliability metrics
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import logging
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import json
from sklearn.metrics import cohen_kappa_score
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InterraterReliabilityAnalyzer:
    """Interrater reliability analysis for multi-LLM studies."""
    
    def __init__(self):
        """Initialize the reliability analyzer."""
        self.reliability_results = {}
        
    def analyze_reliability(self, structured_results: Dict) -> Dict[str, Any]:
        """
        Analyze interrater reliability for multi-LLM studies.
        
        Args:
            structured_results: Dictionary containing structured data and metadata
            
        Returns:
            Dictionary containing comprehensive reliability analysis
        """
        logger.info("🔍 Starting interrater reliability analysis...")
        
        df = structured_results.get('structured_data')
        metadata = structured_results.get('metadata', {})
        
        if df is None or df.empty:
            logger.error("No structured data available for reliability analysis")
            return {'error': 'No data available'}
        
        # Get foundation/anchor score columns (updated from deprecated "well_" terminology)
        # Look for current foundation names from Moral Foundations Theory
        foundation_names = ['Care', 'Fairness', 'Loyalty', 'Authority', 'Sanctity', 'Liberty', 
                           'Harm', 'Oppression']  # Including bipolar opposites
        
        # Find columns that match foundation names (case-insensitive)
        foundation_columns = []
        for col in df.columns:
            if col in foundation_names or col.lower() in [f.lower() for f in foundation_names]:
                foundation_columns.append(col)
        
        # Fallback: look for any numeric columns that might be scores
        if not foundation_columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Exclude metadata columns
            exclude_cols = ['text_id', 'model', 'timestamp', 'run_id', 'analysis_id']
            foundation_columns = [col for col in numeric_cols if col not in exclude_cols]
        
        if not foundation_columns:
            logger.error("No foundation score columns found in data")
            return {'error': 'No foundation scores found'}
        
        # Check if we have multiple raters (models) for reliability analysis
        models = df['model'].unique() if 'model' in df.columns else []
        
        if len(models) < 2:
            logger.warning(f"Only {len(models)} model(s) found - reliability analysis requires multiple raters")
            return self._single_rater_analysis(df, well_columns, metadata)
        
        logger.info(f"🎯 Analyzing reliability with {len(models)} models and {len(well_columns)} wells")
        
        # Perform comprehensive reliability analysis
        reliability_results = {
            'metadata': {
                'models_analyzed': list(models),
                'well_count': len(well_columns),
                'sample_size': len(df),
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            },
            'icc_analysis': self.calculate_icc(df, well_columns),
            'cronbach_alpha': self.calculate_cronbach_alpha(df, well_columns),
            'pairwise_correlations': self.calculate_pairwise_correlations(df, well_columns, models),
            'coefficient_of_variation': self.calculate_coefficient_of_variation(df, well_columns),
            'outlier_analysis': self.detect_outliers(df, well_columns, models),
            'systematic_bias_analysis': self.analyze_systematic_bias(df, well_columns, models),
            'reliability_summary': {}
        }
        
        # Generate overall reliability summary
        reliability_results['reliability_summary'] = self.generate_reliability_summary(reliability_results)
        
        logger.info("✅ Interrater reliability analysis completed")
        return reliability_results
    
    def _single_rater_analysis(self, df: pd.DataFrame, well_columns: List[str], metadata: Dict) -> Dict[str, Any]:
        """Analysis for single-rater scenarios (descriptive only)."""
        logger.info("📊 Performing single-rater descriptive analysis...")
        
        return {
            'analysis_type': 'single_rater_descriptive',
            'metadata': {
                'model_count': 1,
                'well_count': len(well_columns),
                'sample_size': len(df),
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            },
            'descriptive_statistics': self.calculate_descriptive_reliability_stats(df, well_columns),
            'internal_consistency': self.calculate_internal_consistency(df, well_columns),
            'message': 'Single rater detected - full reliability analysis requires multiple raters'
        }
    
    def calculate_icc(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate Intraclass Correlation Coefficient (ICC) for each well.
        
        Args:
            df: DataFrame with analysis results
            well_columns: List of well score column names
            
        Returns:
            Dictionary with ICC results for each well
        """
        logger.info("📊 Calculating Intraclass Correlation Coefficients (ICC)...")
        
        icc_results = {}
        
        for well_col in well_columns:
            try:
                # Pivot data to have raters as columns
                well_data = df.pivot_table(
                    values=well_col, 
                    index='text_id' if 'text_id' in df.columns else df.index,
                    columns='model' if 'model' in df.columns else 'rater',
                    aggfunc='mean'
                ).dropna()
                
                if well_data.shape[0] < 2 or well_data.shape[1] < 2:
                    icc_results[well_col] = {
                        'icc_value': None,
                        'interpretation': 'insufficient_data',
                        'message': f'Insufficient data: {well_data.shape[0]} texts, {well_data.shape[1]} raters'
                    }
                    continue
                
                # Calculate ICC(2,1) - two-way random effects, single measurement
                icc_value = self._calculate_icc_two_way(well_data.values)
                
                icc_results[well_col] = {
                    'icc_value': float(icc_value) if icc_value is not None else None,
                    'interpretation': self._interpret_icc(icc_value) if icc_value is not None else 'calculation_failed',
                    'sample_size': well_data.shape[0],
                    'rater_count': well_data.shape[1],
                    'mean_score': float(well_data.values.mean()),
                    'std_score': float(well_data.values.std())
                }
                
            except Exception as e:
                logger.warning(f"Could not calculate ICC for {well_col}: {e}")
                icc_results[well_col] = {
                    'icc_value': None,
                    'interpretation': 'calculation_error',
                    'error': str(e)
                }
        
        return icc_results
    
    def _calculate_icc_two_way(self, data: np.ndarray) -> Optional[float]:
        """Calculate ICC(2,1) using ANOVA approach."""
        try:
            n_subjects, n_raters = data.shape
            
            # Calculate means
            subject_means = np.mean(data, axis=1)
            rater_means = np.mean(data, axis=0)
            grand_mean = np.mean(data)
            
            # Calculate sum of squares
            ss_total = np.sum((data - grand_mean) ** 2)
            ss_between_subjects = n_raters * np.sum((subject_means - grand_mean) ** 2)
            ss_between_raters = n_subjects * np.sum((rater_means - grand_mean) ** 2)
            ss_error = ss_total - ss_between_subjects - ss_between_raters
            
            # Calculate mean squares
            ms_between_subjects = ss_between_subjects / (n_subjects - 1)
            ms_between_raters = ss_between_raters / (n_raters - 1)
            ms_error = ss_error / ((n_subjects - 1) * (n_raters - 1))
            
            # Calculate ICC(2,1)
            if ms_error == 0:
                return 1.0  # Perfect agreement
            
            icc = (ms_between_subjects - ms_error) / (ms_between_subjects + (n_raters - 1) * ms_error + n_raters * (ms_between_raters - ms_error) / n_subjects)
            
            return max(0.0, min(1.0, icc))  # Clamp between 0 and 1
            
        except Exception as e:
            logger.warning(f"ICC calculation failed: {e}")
            return None
    
    def _interpret_icc(self, icc_value: float) -> str:
        """Interpret ICC value according to standard guidelines."""
        if icc_value is None:
            return 'unknown'
        elif icc_value < 0.5:
            return 'poor'
        elif icc_value < 0.75:
            return 'moderate'
        elif icc_value < 0.9:
            return 'good'
        else:
            return 'excellent'
    
    def calculate_cronbach_alpha(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate Cronbach's Alpha for internal consistency.
        
        Args:
            df: DataFrame with analysis results
            well_columns: List of well score column names
            
        Returns:
            Dictionary with Cronbach's Alpha results
        """
        logger.info("📊 Calculating Cronbach's Alpha...")
        
        try:
            # Create matrix of well scores
            well_matrix = df[well_columns].dropna()
            
            if well_matrix.empty or well_matrix.shape[1] < 2:
                return {
                    'alpha_value': None,
                    'interpretation': 'insufficient_data',
                    'message': 'Need at least 2 wells with data'
                }
            
            # Calculate Cronbach's Alpha
            n_items = well_matrix.shape[1]
            item_variances = well_matrix.var(axis=0, ddof=1)
            total_variance = well_matrix.sum(axis=1).var(ddof=1)
            
            if total_variance == 0:
                alpha = 1.0
            else:
                alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
            
            return {
                'alpha_value': float(alpha),
                'interpretation': self._interpret_cronbach_alpha(alpha),
                'n_items': n_items,
                'sample_size': len(well_matrix),
                'item_statistics': {
                    well: {
                        'mean': float(well_matrix[well].mean()),
                        'std': float(well_matrix[well].std()),
                        'item_total_correlation': float(well_matrix[well].corr(well_matrix.drop(columns=[well]).sum(axis=1)))
                    } for well in well_columns if well in well_matrix.columns
                }
            }
            
        except Exception as e:
            logger.warning(f"Cronbach's Alpha calculation failed: {e}")
            return {
                'alpha_value': None,
                'interpretation': 'calculation_error',
                'error': str(e)
            }
    
    def _interpret_cronbach_alpha(self, alpha: float) -> str:
        """Interpret Cronbach's Alpha value."""
        if alpha is None:
            return 'unknown'
        elif alpha < 0.6:
            return 'poor'
        elif alpha < 0.7:
            return 'questionable'
        elif alpha < 0.8:
            return 'acceptable'
        elif alpha < 0.9:
            return 'good'
        else:
            return 'excellent'
    
    def calculate_pairwise_correlations(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[str, Any]:
        """Calculate pairwise correlations between raters (models)."""
        logger.info("📊 Calculating pairwise correlations...")
        
        correlations = {}
        
        for well_col in well_columns:
            well_correlations = {}
            
            # Get data for each model pair
            for i, model1 in enumerate(models):
                for model2 in models[i+1:]:
                    model1_data = df[df['model'] == model1][well_col].dropna()
                    model2_data = df[df['model'] == model2][well_col].dropna()
                    
                    # Find common text IDs if available
                    if 'text_id' in df.columns:
                        model1_df = df[df['model'] == model1][['text_id', well_col]].dropna()
                        model2_df = df[df['model'] == model2][['text_id', well_col]].dropna()
                        
                        merged = model1_df.merge(model2_df, on='text_id', suffixes=('_1', '_2'))
                        
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
    
    def calculate_coefficient_of_variation(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """Calculate coefficient of variation for each well across raters."""
        logger.info("📊 Calculating coefficient of variation...")
        
        cv_results = {}
        
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
                    'interpretation': self._interpret_cv(cv),
                    'sample_size': len(well_data)
                }
        
        return cv_results
    
    def _interpret_cv(self, cv: float) -> str:
        """Interpret coefficient of variation."""
        if cv < 10:
            return 'very_low_variability'
        elif cv < 20:
            return 'low_variability'
        elif cv < 30:
            return 'moderate_variability'
        elif cv < 50:
            return 'high_variability'
        else:
            return 'very_high_variability'
    
    def detect_outliers(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[str, Any]:
        """Detect outliers in rater scores."""
        logger.info("🔍 Detecting outliers...")
        
        outlier_results = {}
        
        for well_col in well_columns:
            well_data = df[well_col].dropna()
            
            if len(well_data) > 0:
                # Z-score method
                z_scores = np.abs(stats.zscore(well_data))
                outliers_z = well_data[z_scores > 2.5]  # 2.5 sigma threshold
                
                # IQR method
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
    
    def analyze_systematic_bias(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[str, Any]:
        """Analyze systematic bias between raters."""
        logger.info("🔍 Analyzing systematic bias...")
        
        bias_results = {}
        
        for well_col in well_columns:
            model_means = {}
            
            for model in models:
                model_data = df[df['model'] == model][well_col].dropna()
                if len(model_data) > 0:
                    model_means[model] = {
                        'mean': float(model_data.mean()),
                        'std': float(model_data.std()),
                        'count': len(model_data)
                    }
            
            # Calculate overall statistics
            if len(model_means) > 1:
                all_means = [stats['mean'] for stats in model_means.values()]
                mean_of_means = np.mean(all_means)
                std_of_means = np.std(all_means)
                
                # Test for significant differences (ANOVA if multiple models)
                if len(models) > 2:
                    model_data_lists = []
                    for model in models:
                        model_data = df[df['model'] == model][well_col].dropna()
                        if len(model_data) > 0:
                            model_data_lists.append(model_data.values)
                    
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
    
    def calculate_descriptive_reliability_stats(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """Calculate descriptive statistics for reliability assessment."""
        stats_results = {}
        
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
    
    def calculate_internal_consistency(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """Calculate internal consistency measures for single rater."""
        try:
            well_matrix = df[well_columns].dropna()
            
            if well_matrix.empty or well_matrix.shape[1] < 2:
                return {'error': 'Insufficient data for internal consistency analysis'}
            
            # Split-half reliability (odd-even split)
            odd_cols = well_columns[::2]
            even_cols = well_columns[1::2]
            
            if len(odd_cols) > 0 and len(even_cols) > 0:
                odd_scores = well_matrix[odd_cols].sum(axis=1)
                even_scores = well_matrix[even_cols].sum(axis=1)
                
                if len(odd_scores) > 1 and len(even_scores) > 1:
                    split_half_r, split_half_p = pearsonr(odd_scores, even_scores)
                    
                    # Spearman-Brown prophecy formula
                    spearman_brown = (2 * split_half_r) / (1 + split_half_r)
                    
                    return {
                        'split_half_correlation': float(split_half_r),
                        'split_half_p_value': float(split_half_p),
                        'spearman_brown_coefficient': float(spearman_brown),
                        'interpretation': self._interpret_cronbach_alpha(spearman_brown)
                    }
            
            return {'error': 'Could not calculate split-half reliability'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_reliability_summary(self, reliability_results: Dict) -> Dict[str, Any]:
        """Generate overall reliability summary."""
        
        summary = {
            'overall_reliability': 'unknown',
            'key_findings': [],
            'recommendations': [],
            'quality_indicators': {}
        }
        
        # Analyze ICC results
        icc_results = reliability_results.get('icc_analysis', {})
        if icc_results:
            icc_values = [r.get('icc_value') for r in icc_results.values() if r.get('icc_value') is not None]
            if icc_values:
                avg_icc = np.mean(icc_values)
                summary['quality_indicators']['average_icc'] = float(avg_icc)
                summary['key_findings'].append(f"Average ICC: {avg_icc:.3f} ({self._interpret_icc(avg_icc)})")
        
        # Analyze Cronbach's Alpha
        alpha_result = reliability_results.get('cronbach_alpha', {})
        if alpha_result.get('alpha_value') is not None:
            alpha = alpha_result['alpha_value']
            summary['quality_indicators']['cronbach_alpha'] = float(alpha)
            summary['key_findings'].append(f"Cronbach's Alpha: {alpha:.3f} ({self._interpret_cronbach_alpha(alpha)})")
        
        # Overall assessment
        icc_good = summary['quality_indicators'].get('average_icc', 0) >= 0.75
        alpha_good = summary['quality_indicators'].get('cronbach_alpha', 0) >= 0.7
        
        if icc_good and alpha_good:
            summary['overall_reliability'] = 'excellent'
        elif icc_good or alpha_good:
            summary['overall_reliability'] = 'good'
        else:
            summary['overall_reliability'] = 'needs_improvement'
        
        # Generate recommendations
        if not icc_good:
            summary['recommendations'].append("Consider increasing sample size or improving rater training")
        
        if not alpha_good:
            summary['recommendations'].append("Review internal consistency - some wells may be measuring different constructs")
        
        return summary 