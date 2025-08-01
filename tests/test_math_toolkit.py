"""
Unit tests for the MathToolkit module.

These tests validate that our pre-built mathematical functions work correctly
and return properly structured results.
"""

import unittest
import pandas as pd
import numpy as np
from discernus.core.math_toolkit import (
    calculate_descriptive_stats,
    perform_independent_t_test,
    calculate_pearson_correlation,
    perform_one_way_anova,
    calculate_effect_sizes,
    execute_analysis_plan,
    MathToolkitError
)


class TestMathToolkit(unittest.TestCase):
    """Test cases for MathToolkit functions."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data for testing
        np.random.seed(42)
        
        # Sample data with groups
        n_samples = 100
        self.test_data = pd.DataFrame({
            'group': ['A'] * 50 + ['B'] * 50,
            'score': np.concatenate([
                np.random.normal(75, 10, 50),  # Group A: mean=75
                np.random.normal(85, 10, 50)   # Group B: mean=85
            ]),
            'confidence': np.random.uniform(0.5, 1.0, n_samples),
            'justice_score': np.random.normal(70, 15, n_samples),
            'temperance_score': np.random.normal(65, 12, n_samples)
        })
        
        # Add some NaN values to test robustness
        self.test_data.loc[5, 'score'] = np.nan
        self.test_data.loc[15, 'confidence'] = np.nan
    
    def test_calculate_descriptive_stats(self):
        """Test descriptive statistics calculation."""
        result = calculate_descriptive_stats(self.test_data, ['score', 'confidence'])
        
        # Check structure
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'descriptive_stats')
        self.assertIn('columns_analyzed', result)
        self.assertIn('results', result)
        
        # Check results for each column
        for col in ['score', 'confidence']:
            self.assertIn(col, result['results'])
            stats = result['results'][col]
            
            # Check that all required statistics are present
            required_stats = ['count', 'mean', 'std', 'min', 'max', 'median', 'q25', 'q75']
            for stat in required_stats:
                self.assertIn(stat, stats)
                self.assertIsInstance(stats[stat], (int, float))
    
    def test_perform_independent_t_test(self):
        """Test independent t-test calculation."""
        result = perform_independent_t_test(
            self.test_data, 
            'group', 
            'score'
        )
        
        # Check structure
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'independent_t_test')
        self.assertIn('test_statistic', result)
        self.assertIn('p_value', result)
        self.assertIn('significant', result)
        self.assertIn('group1', result)
        self.assertIn('group2', result)
        
        # Check that p-value is reasonable (should be very small given our setup)
        self.assertLess(result['p_value'], 0.001)
        self.assertTrue(result['significant'])
        
        # Check group statistics
        for group_key in ['group1', 'group2']:
            group_stats = result[group_key]
            self.assertIn('label', group_stats)
            self.assertIn('n', group_stats)
            self.assertIn('mean', group_stats)
            self.assertIn('std', group_stats)
    
    def test_calculate_pearson_correlation(self):
        """Test Pearson correlation calculation."""
        result = calculate_pearson_correlation(
            self.test_data, 
            ['score', 'confidence', 'justice_score']
        )
        
        # Check structure
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'pearson_correlation')
        self.assertIn('columns', result)
        self.assertIn('correlation_matrix', result)
        self.assertIn('significance_matrix', result)
        
        # Check correlation matrix structure
        corr_matrix = result['correlation_matrix']
        self.assertIn('score', corr_matrix)
        self.assertIn('confidence', corr_matrix)
        self.assertIn('justice_score', corr_matrix)
        
        # Check that diagonal correlations are 1.0
        self.assertEqual(corr_matrix['score']['score'], 1.0)
        self.assertEqual(corr_matrix['confidence']['confidence'], 1.0)
        self.assertEqual(corr_matrix['justice_score']['justice_score'], 1.0)
    
    def test_perform_one_way_anova(self):
        """Test one-way ANOVA calculation."""
        result = perform_one_way_anova(
            self.test_data,
            'group',
            'score'
        )
        
        # Check structure
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'one_way_anova')
        self.assertIn('f_statistic', result)
        self.assertIn('p_value', result)
        self.assertIn('significant', result)
        self.assertIn('groups', result)
        
        # Check that p-value is reasonable
        self.assertLess(result['p_value'], 0.001)
        self.assertTrue(result['significant'])
        
        # Check group statistics
        groups = result['groups']
        self.assertIn('A', groups)
        self.assertIn('B', groups)
    
    def test_calculate_effect_sizes(self):
        """Test effect size calculation."""
        result = calculate_effect_sizes(
            self.test_data,
            'group',
            'score'
        )
        
        # Check structure
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'effect_sizes')
        self.assertIn('eta_squared', result)
        self.assertIn('effect_size_interpretation', result)
        self.assertIn('group_means', result)
        
        # Check that eta_squared is reasonable (0-1 range)
        self.assertGreaterEqual(result['eta_squared'], 0)
        self.assertLessEqual(result['eta_squared'], 1)
        
        # Check effect size interpretation
        self.assertIn(result['effect_size_interpretation'], 
                     ['negligible', 'small', 'medium', 'large'])
    
    def test_execute_analysis_plan(self):
        """Test complete analysis plan execution."""
        # Create a simple analysis plan
        analysis_plan = {
            "experiment_summary": "Test analysis",
            "tasks": {
                "descriptive_analysis": {
                    "tool": "calculate_descriptive_stats",
                    "parameters": {"columns": ["score", "confidence"]},
                    "purpose": "Calculate basic statistics"
                },
                "group_comparison": {
                    "tool": "perform_independent_t_test",
                    "parameters": {
                        "grouping_variable": "group",
                        "dependent_variable": "score"
                    },
                    "purpose": "Compare groups"
                }
            }
        }
        
        result = execute_analysis_plan(self.test_data, analysis_plan)
        
        # Check structure
        self.assertIn('analysis_plan', result)
        self.assertIn('results', result)
        self.assertIn('errors', result)
        
        # Check that both tasks were executed
        self.assertIn('descriptive_analysis', result['results'])
        self.assertIn('group_comparison', result['results'])
        
        # Check that no errors occurred
        self.assertEqual(len(result['errors']), 0)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with non-existent column
        with self.assertRaises(MathToolkitError):
            calculate_descriptive_stats(self.test_data, ['non_existent_column'])
        
        # Test t-test with non-existent grouping variable
        with self.assertRaises(MathToolkitError):
            perform_independent_t_test(
                self.test_data,
                'non_existent_group',
                'score'
            )
        
        # Test correlation with insufficient columns
        with self.assertRaises(MathToolkitError):
            calculate_pearson_correlation(self.test_data, ['score'])
    
    def test_nan_handling(self):
        """Test that NaN values are handled gracefully."""
        # Create data with many NaN values
        nan_data = pd.DataFrame({
            'group': ['A', 'B', 'A', 'B'],
            'score': [1.0, np.nan, 3.0, np.nan],
            'confidence': [0.8, 0.9, np.nan, np.nan]
        })
        
        # Should not raise an error
        result = calculate_descriptive_stats(nan_data, ['score', 'confidence'])
        self.assertIn('score', result['results'])
        self.assertIn('confidence', result['results'])


if __name__ == '__main__':
    unittest.main() 