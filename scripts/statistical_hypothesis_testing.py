#!/usr/bin/env python3
"""
Statistical Hypothesis Testing System for Narrative Gravity Analysis
Tests discriminative validity, ideological agnosticism, and ground truth alignment
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel, f_oneway, pearsonr, spearmanr
import logging
from typing import Dict, List, Tuple, Any
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StatisticalHypothesisTester:
    """Statistical hypothesis testing for narrative gravity analysis."""
    
    def __init__(self):
        """Initialize the hypothesis tester."""
        self.alpha = 0.05  # Significance level
        self.results = {}
        
    def test_hypotheses(self, structured_results: Dict) -> Dict[str, Any]:
        """
        Test all three hypotheses on structured experiment results.
        
        Args:
            structured_results: Dictionary containing structured data and metadata
            
        Returns:
            Dictionary containing all hypothesis test results
        """
        logger.info("🧪 Starting comprehensive hypothesis testing...")
        
        df = structured_results.get('structured_data')
        metadata = structured_results.get('metadata', {})
        
        if df is None or df.empty:
            logger.error("No structured data available for hypothesis testing")
            return {'error': 'No data available'}
        
        # Get well columns
        well_columns = [col for col in df.columns if col.startswith('well_')]
        
        if not well_columns:
            logger.error("No well score columns found in data")
            return {'error': 'No well scores found'}
        
        logger.info(f"📊 Testing hypotheses with {len(df)} analyses and {len(well_columns)} wells")
        
        # Test H1: Discriminative Validity
        h1_results = self.test_h1_discriminative_validity(df, well_columns)
        
        # Test H2: Ideological Agnosticism
        h2_results = self.test_h2_ideological_agnosticism(df, well_columns)
        
        # Test H3: Ground Truth Alignment
        h3_results = self.test_h3_ground_truth_alignment(df, well_columns)
        
        # Additional statistical analyses
        descriptive_stats = self.calculate_descriptive_statistics(df, well_columns)
        effect_sizes = self.calculate_effect_sizes(df, well_columns)
        
        # Compile comprehensive results
        hypothesis_results = {
            'hypothesis_testing': {
                'H1_discriminative_validity': h1_results,
                'H2_ideological_agnosticism': h2_results,
                'H3_ground_truth_alignment': h3_results
            },
            'descriptive_statistics': descriptive_stats,
            'effect_sizes': effect_sizes,
            'metadata': {
                'sample_size': len(df),
                'well_count': len(well_columns),
                'frameworks_tested': metadata.get('frameworks_used', []),
                'models_tested': metadata.get('models_used', []),
                'significance_level': self.alpha,
                'testing_timestamp': pd.Timestamp.now().isoformat()
            },
            'summary': self.generate_hypothesis_summary(h1_results, h2_results, h3_results)
        }
        
        logger.info("✅ Hypothesis testing completed successfully")
        return hypothesis_results
    
    def test_h1_discriminative_validity(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """
        H1: Test discriminative validity - dignity vs tribalism scores should differentiate expected text categories.
        
        Args:
            df: DataFrame with analysis results
            well_columns: List of well score column names
            
        Returns:
            Dictionary with H1 test results
        """
        logger.info("🎯 Testing H1: Discriminative Validity")
        
        # Look for dignity and tribalism wells
        dignity_cols = [col for col in well_columns if 'dignity' in col.lower()]
        tribalism_cols = [col for col in well_columns if 'tribalism' in col.lower()]
        
        h1_results = {
            'hypothesis': 'Discriminative validity: Dignity and Tribalism wells differentiate expected text categories',
            'dignity_wells': dignity_cols,
            'tribalism_wells': tribalism_cols,
            'tests_performed': []
        }
        
        if not dignity_cols or not tribalism_cols:
            h1_results['status'] = 'insufficient_data'
            h1_results['message'] = f"Missing wells - Dignity: {dignity_cols}, Tribalism: {tribalism_cols}"
            return h1_results
        
        # Test 1: Dignity vs Tribalism score differences
        for dignity_col in dignity_cols:
            for tribalism_col in tribalism_cols:
                dignity_scores = df[dignity_col].dropna()
                tribalism_scores = df[tribalism_col].dropna()
                
                if len(dignity_scores) > 1 and len(tribalism_scores) > 1:
                    # Paired t-test if same texts, independent if different
                    if len(dignity_scores) == len(tribalism_scores):
                        t_stat, p_value = ttest_rel(dignity_scores, tribalism_scores)
                        test_type = 'paired_t_test'
                    else:
                        t_stat, p_value = ttest_ind(dignity_scores, tribalism_scores)
                        test_type = 'independent_t_test'
                    
                    test_result = {
                        'comparison': f"{dignity_col} vs {tribalism_col}",
                        'test_type': test_type,
                        't_statistic': float(t_stat),
                        'p_value': float(p_value),
                        'significant': p_value < self.alpha,
                        'dignity_mean': float(dignity_scores.mean()),
                        'tribalism_mean': float(tribalism_scores.mean()),
                        'dignity_std': float(dignity_scores.std()),
                        'tribalism_std': float(tribalism_scores.std()),
                        'sample_sizes': {'dignity': len(dignity_scores), 'tribalism': len(tribalism_scores)}
                    }
                    
                    h1_results['tests_performed'].append(test_result)
        
        # Overall H1 assessment
        significant_tests = [t for t in h1_results['tests_performed'] if t['significant']]
        h1_results['status'] = 'supported' if len(significant_tests) > 0 else 'not_supported'
        h1_results['significant_comparisons'] = len(significant_tests)
        h1_results['total_comparisons'] = len(h1_results['tests_performed'])
        
        logger.info(f"   H1 Results: {len(significant_tests)}/{len(h1_results['tests_performed'])} significant comparisons")
        return h1_results
    
    def test_h2_ideological_agnosticism(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """
        H2: Test ideological agnosticism - framework should not systematically favor conservative vs progressive texts.
        
        Args:
            df: DataFrame with analysis results
            well_columns: List of well score column names
            
        Returns:
            Dictionary with H2 test results
        """
        logger.info("🎯 Testing H2: Ideological Agnosticism")
        
        h2_results = {
            'hypothesis': 'Ideological agnosticism: Framework should not systematically favor conservative vs progressive content',
            'tests_performed': []
        }
        
        # Try to identify conservative vs progressive texts based on text_id or other metadata
        # This is a simplified approach - in practice might need more sophisticated categorization
        df_copy = df.copy()
        df_copy['ideological_category'] = 'unknown'
        
        # Simple heuristic categorization based on text_id patterns
        conservative_patterns = ['reagan', 'trump', 'conservative', 'republican']
        progressive_patterns = ['obama', 'progressive', 'liberal', 'democratic']
        
        for idx, row in df_copy.iterrows():
            text_id = str(row.get('text_id', '')).lower()
            if any(pattern in text_id for pattern in conservative_patterns):
                df_copy.at[idx, 'ideological_category'] = 'conservative'
            elif any(pattern in text_id for pattern in progressive_patterns):
                df_copy.at[idx, 'ideological_category'] = 'progressive'
        
        conservative_texts = df_copy[df_copy['ideological_category'] == 'conservative']
        progressive_texts = df_copy[df_copy['ideological_category'] == 'progressive']
        
        h2_results['sample_sizes'] = {
            'conservative': len(conservative_texts),
            'progressive': len(progressive_texts),
            'unknown': len(df_copy[df_copy['ideological_category'] == 'unknown'])
        }
        
        if len(conservative_texts) == 0 or len(progressive_texts) == 0:
            h2_results['status'] = 'insufficient_data'
            h2_results['message'] = 'Could not identify both conservative and progressive texts for comparison'
            return h2_results
        
        # Test for systematic differences in well scores between ideological categories
        for well_col in well_columns:
            conservative_scores = conservative_texts[well_col].dropna()
            progressive_scores = progressive_texts[well_col].dropna()
            
            if len(conservative_scores) > 0 and len(progressive_scores) > 0:
                t_stat, p_value = ttest_ind(conservative_scores, progressive_scores)
                
                test_result = {
                    'well': well_col,
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'significant': p_value < self.alpha,
                    'conservative_mean': float(conservative_scores.mean()),
                    'progressive_mean': float(progressive_scores.mean()),
                    'conservative_std': float(conservative_scores.std()),
                    'progressive_std': float(progressive_scores.std()),
                    'effect_size': abs(conservative_scores.mean() - progressive_scores.mean()) / 
                                 np.sqrt((conservative_scores.var() + progressive_scores.var()) / 2)
                }
                
                h2_results['tests_performed'].append(test_result)
        
        # Overall H2 assessment (agnosticism supported if NO significant systematic differences)
        significant_biases = [t for t in h2_results['tests_performed'] if t['significant']]
        h2_results['status'] = 'not_supported' if len(significant_biases) > 0 else 'supported'
        h2_results['significant_biases'] = len(significant_biases)
        h2_results['total_wells_tested'] = len(h2_results['tests_performed'])
        
        logger.info(f"   H2 Results: {len(significant_biases)} significant biases found (fewer is better)")
        return h2_results
    
    def test_h3_ground_truth_alignment(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """
        H3: Test ground truth alignment - extreme control texts should score >0.8 on expected wells.
        
        Args:
            df: DataFrame with analysis results
            well_columns: List of well score column names
            
        Returns:
            Dictionary with H3 test results
        """
        logger.info("🎯 Testing H3: Ground Truth Alignment")
        
        h3_results = {
            'hypothesis': 'Ground truth alignment: Extreme control texts should score >0.8 on expected wells',
            'target_threshold': 0.8,
            'tests_performed': []
        }
        
        # Identify extreme control texts based on text_id patterns
        extreme_controls = []
        
        for idx, row in df.iterrows():
            text_id = str(row.get('text_id', '')).lower()
            
            # Look for extreme control indicators
            if 'extreme' in text_id or 'control' in text_id:
                # Try to determine expected high-scoring well
                expected_well = None
                if 'dignity' in text_id:
                    expected_well = [col for col in well_columns if 'dignity' in col.lower()]
                elif 'tribalism' in text_id:
                    expected_well = [col for col in well_columns if 'tribalism' in col.lower()]
                
                if expected_well:
                    extreme_controls.append({
                        'text_id': text_id,
                        'expected_wells': expected_well,
                        'row_data': row
                    })
        
        h3_results['extreme_controls_found'] = len(extreme_controls)
        
        if len(extreme_controls) == 0:
            h3_results['status'] = 'insufficient_data'
            h3_results['message'] = 'No extreme control texts identified'
            return h3_results
        
        # Test each extreme control
        for control in extreme_controls:
            for expected_well in control['expected_wells']:
                if expected_well in control['row_data']:
                    score = control['row_data'][expected_well]
                    
                    if pd.notna(score):
                        test_result = {
                            'text_id': control['text_id'],
                            'well': expected_well,
                            'score': float(score),
                            'target_threshold': 0.8,
                            'meets_threshold': score >= 0.8,
                            'z_score': (score - 0.8) / 0.1,  # Assuming std of 0.1 for threshold test
                            'performance': 'excellent' if score >= 0.9 else 'good' if score >= 0.8 else 'poor'
                        }
                        
                        h3_results['tests_performed'].append(test_result)
        
        # Overall H3 assessment
        successful_controls = [t for t in h3_results['tests_performed'] if t['meets_threshold']]
        h3_results['status'] = 'supported' if len(successful_controls) == len(h3_results['tests_performed']) else 'partial_support'
        h3_results['successful_controls'] = len(successful_controls)
        h3_results['total_controls_tested'] = len(h3_results['tests_performed'])
        h3_results['success_rate'] = len(successful_controls) / len(h3_results['tests_performed']) if h3_results['tests_performed'] else 0
        
        logger.info(f"   H3 Results: {len(successful_controls)}/{len(h3_results['tests_performed'])} controls met threshold")
        return h3_results
    
    def calculate_descriptive_statistics(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """Calculate comprehensive descriptive statistics."""
        logger.info("📊 Calculating descriptive statistics...")
        
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
                    'median': float(scores.median()),
                    'q25': float(scores.quantile(0.25)),
                    'q75': float(scores.quantile(0.75)),
                    'skewness': float(scores.skew()),
                    'kurtosis': float(scores.kurtosis())
                }
        
        return stats_results
    
    def calculate_effect_sizes(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, Any]:
        """Calculate Cohen's d and other effect sizes."""
        logger.info("📏 Calculating effect sizes...")
        
        effect_sizes = {}
        
        # Calculate effect sizes for pairwise comparisons of wells
        for i, well1 in enumerate(well_columns):
            for well2 in well_columns[i+1:]:
                scores1 = df[well1].dropna()
                scores2 = df[well2].dropna()
                
                if len(scores1) > 1 and len(scores2) > 1:
                    # Cohen's d
                    pooled_std = np.sqrt((scores1.var() + scores2.var()) / 2)
                    cohens_d = (scores1.mean() - scores2.mean()) / pooled_std if pooled_std > 0 else 0
                    
                    effect_sizes[f"{well1}_vs_{well2}"] = {
                        'cohens_d': float(cohens_d),
                        'effect_magnitude': self._interpret_cohens_d(cohens_d)
                    }
        
        return effect_sizes
    
    def _interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return 'negligible'
        elif abs_d < 0.5:
            return 'small'
        elif abs_d < 0.8:
            return 'medium'
        else:
            return 'large'
    
    def generate_hypothesis_summary(self, h1_results: Dict, h2_results: Dict, h3_results: Dict) -> Dict[str, Any]:
        """Generate overall summary of hypothesis testing results."""
        
        summary = {
            'overall_assessment': 'mixed_results',
            'hypotheses_supported': 0,
            'hypotheses_tested': 3,
            'key_findings': [],
            'recommendations': []
        }
        
        # Assess each hypothesis
        if h1_results.get('status') == 'supported':
            summary['hypotheses_supported'] += 1
            summary['key_findings'].append("H1: Discriminative validity demonstrated - dignity/tribalism wells differentiate appropriately")
        elif h1_results.get('status') == 'not_supported':
            summary['key_findings'].append("H1: Discriminative validity not demonstrated - wells may need refinement")
        
        if h2_results.get('status') == 'supported':
            summary['hypotheses_supported'] += 1
            summary['key_findings'].append("H2: Ideological agnosticism confirmed - no systematic political bias detected")
        elif h2_results.get('status') == 'not_supported':
            summary['key_findings'].append("H2: Ideological bias detected - framework may favor certain political orientations")
        
        if h3_results.get('status') in ['supported', 'partial_support']:
            if h3_results.get('status') == 'supported':
                summary['hypotheses_supported'] += 1
            summary['key_findings'].append(f"H3: Ground truth alignment {h3_results.get('success_rate', 0):.1%} success rate")
        
        # Overall assessment
        if summary['hypotheses_supported'] >= 2:
            summary['overall_assessment'] = 'strong_validation'
        elif summary['hypotheses_supported'] >= 1:
            summary['overall_assessment'] = 'partial_validation'
        else:
            summary['overall_assessment'] = 'validation_concerns'
        
        # Generate recommendations
        if h1_results.get('status') != 'supported':
            summary['recommendations'].append("Consider refining well definitions for better discriminative validity")
        
        if h2_results.get('status') != 'supported':
            summary['recommendations'].append("Investigate and address potential ideological bias in framework")
        
        if h3_results.get('success_rate', 0) < 0.8:
            summary['recommendations'].append("Improve ground truth alignment - consider threshold adjustments or control text selection")
        
        return summary

def main():
    """Main execution function for standalone testing."""
    
    # For testing purposes, try to load recent extracted data
    data_files = list(Path("exports/analysis_results/").glob("extracted_results_*.csv"))
    
    if not data_files:
        logger.error("No extracted results files found. Run extract_experiment_results.py first.")
        return
    
    # Use most recent file
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"Testing with data from: {latest_file}")
    
    # Load data
    df = pd.read_csv(latest_file)
    
    # Create mock structured results format
    well_columns = [col for col in df.columns if col.startswith('well_')]
    
    structured_results = {
        'structured_data': df,
        'metadata': {
            'well_columns': well_columns,
            'frameworks_used': df['framework'].unique().tolist() if 'framework' in df.columns else [],
            'models_used': df['model_name'].unique().tolist() if 'model_name' in df.columns else []
        }
    }
    
    # Run hypothesis testing
    tester = StatisticalHypothesisTester()
    results = tester.test_hypotheses(structured_results)
    
    # Save results
    output_dir = Path('experiment_reports/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'hypothesis_testing_results_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"✅ Hypothesis testing results saved to: {output_file}")
    
    # Print summary
    summary = results.get('summary', {})
    print(f"\n🎯 HYPOTHESIS TESTING SUMMARY")
    print(f"Overall Assessment: {summary.get('overall_assessment', 'unknown')}")
    print(f"Hypotheses Supported: {summary.get('hypotheses_supported', 0)}/3")
    
    if summary.get('key_findings'):
        print("\n📋 Key Findings:")
        for finding in summary['key_findings']:
            print(f"  • {finding}")
    
    if summary.get('recommendations'):
        print("\n💡 Recommendations:")
        for rec in summary['recommendations']:
            print(f"  • {rec}")

if __name__ == "__main__":
    main() 