#!/usr/bin/env python3
"""
Nano and Micro Integration Tests
===============================

Comprehensive integration tests using real LLMs to validate the complete pipeline
with nano and micro experiments. These tests use Gemini 2.5 Flash Lite for all
stages to keep costs minimal while providing real-world validation.

Test Strategy:
- Clean slate: Delete runs/sessions/logs/shared_cache before each test
- Real LLMs: Use Gemini 2.5 Flash Lite for all stages (analysis, calculation, synthesis)
- Complete pipeline: Test end-to-end from corpus ingestion to final report
- Comprehensive validation: Assert on analysis quality, derived metrics, statistics, and synthesis

Cost: ~$0.001 per test run (fractions of a penny)
"""

import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path
from typing import Dict, Any, List
import time

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError
from discernus.core.audit_logger import AuditLogger


class TestNanoMicroIntegration(unittest.TestCase):
    """Integration tests for nano and micro experiments using real LLMs."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with experiment paths."""
        cls.test_experiments_dir = Path(__file__).parent / "experiments"
        cls.nano_experiment_path = cls.test_experiments_dir / "nano_test_experiment"
        cls.micro_experiment_path = cls.test_experiments_dir / "micro_test_experiment"
        
        # Verify experiments exist
        assert cls.nano_experiment_path.exists(), f"Nano experiment not found at {cls.nano_experiment_path}"
        assert cls.micro_experiment_path.exists(), f"Micro experiment not found at {cls.micro_experiment_path}"
        
        # Set model to use for all tests (cost-effective)
        cls.test_model = "vertex_ai/gemini-2.5-flash-lite"
        
        print(f"\n🧪 Integration Test Setup:")
        print(f"   Nano experiment: {cls.nano_experiment_path}")
        print(f"   Micro experiment: {cls.micro_experiment_path}")
        print(f"   Test model: {cls.test_model}")
        print(f"   Estimated cost per test: ~$0.001")
    
    def setUp(self):
        """Set up each test with clean directories."""
        self.start_time = time.time()
        
    def tearDown(self):
        """Clean up after each test."""
        duration = time.time() - self.start_time
        print(f"   ⏱️  Test completed in {duration:.1f}s")
    
    def _clean_experiment_directories(self, experiment_path: Path):
        """Clean all run artifacts from experiment directory."""
        dirs_to_clean = ['runs', 'session', 'shared_cache', 'logs', 'temp_derived_metrics']
        
        for dir_name in dirs_to_clean:
            dir_path = experiment_path / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   🧹 Cleaned {dir_name}/")
    
    def _validate_analysis_results(self, results: List[Dict[str, Any]], expected_docs: int):
        """Validate analysis phase results."""
        self.assertIsInstance(results, list, "Analysis results should be a list")
        self.assertEqual(len(results), expected_docs, f"Should have {expected_docs} analysis results")
        
        for i, result in enumerate(results):
            self.assertIn('document_name', result, f"Result {i} missing document_name")
            self.assertIn('analysis_result', result, f"Result {i} missing analysis_result")
            
            analysis = result['analysis_result']
            self.assertIn('dimensional_scores', analysis, f"Result {i} missing dimensional_scores")
            
            # Validate dimensional scores structure
            dim_scores = analysis['dimensional_scores']
            self.assertIn('positive_sentiment', dim_scores, "Missing positive_sentiment dimension")
            self.assertIn('negative_sentiment', dim_scores, "Missing negative_sentiment dimension")
            
            # Validate score objects
            for dim_name, score_obj in dim_scores.items():
                self.assertIn('raw_score', score_obj, f"{dim_name} missing raw_score")
                self.assertIn('salience', score_obj, f"{dim_name} missing salience")
                self.assertIn('confidence', score_obj, f"{dim_name} missing confidence")
                self.assertIn('evidence', score_obj, f"{dim_name} missing evidence")
                
                # Validate score ranges
                self.assertGreaterEqual(score_obj['raw_score'], 0.0, f"{dim_name} raw_score below 0")
                self.assertLessEqual(score_obj['raw_score'], 1.0, f"{dim_name} raw_score above 1")
                self.assertGreaterEqual(score_obj['salience'], 0.0, f"{dim_name} salience below 0")
                self.assertLessEqual(score_obj['salience'], 1.0, f"{dim_name} salience above 1")
                self.assertGreaterEqual(score_obj['confidence'], 0.0, f"{dim_name} confidence below 0")
                self.assertLessEqual(score_obj['confidence'], 1.0, f"{dim_name} confidence above 1")
                self.assertIsInstance(score_obj['evidence'], str, f"{dim_name} evidence should be string")
                self.assertGreater(len(score_obj['evidence']), 0, f"{dim_name} evidence should not be empty")
    
    def _validate_derived_metrics_results(self, results: Dict[str, Any], has_derived_metrics: bool):
        """Validate derived metrics phase results."""
        if not has_derived_metrics:
            # Nano experiment has no derived metrics
            self.assertIsNone(results, "Nano experiment should have no derived metrics")
            return
        
        # Micro experiment should have derived metrics
        self.assertIsNotNone(results, "Micro experiment should have derived metrics")
        self.assertIn('derived_metrics_data', results, "Missing derived_metrics_data")
        
        derived_data = results['derived_metrics_data']
        self.assertIn('net_sentiment', derived_data, "Missing net_sentiment derived metric")
        self.assertIn('sentiment_magnitude', derived_data, "Missing sentiment_magnitude derived metric")
        
        # Validate derived metrics structure
        for metric_name, metric_data in derived_data.items():
            self.assertIsInstance(metric_data, list, f"{metric_name} should be a list")
            self.assertGreater(len(metric_data), 0, f"{metric_name} should not be empty")
            
            for i, doc_metric in enumerate(metric_data):
                self.assertIn('document_name', doc_metric, f"{metric_name}[{i}] missing document_name")
                self.assertIn('metric_value', doc_metric, f"{metric_name}[{i}] missing metric_value")
                self.assertIsInstance(doc_metric['metric_value'], (int, float), f"{metric_name}[{i}] metric_value should be numeric")
    
    def _validate_statistical_results(self, results: Dict[str, Any], has_derived_metrics: bool):
        """Validate statistical analysis results."""
        self.assertIsNotNone(results, "Statistical results should not be None")
        self.assertIn('statistical_data', results, "Missing statistical_data")
        
        stats_data = results['statistical_data']
        
        # Should have descriptive statistics
        self.assertIn('descriptive_statistics', stats_data, "Missing descriptive_statistics")
        desc_stats = stats_data['descriptive_statistics']
        
        # Validate dimensional statistics
        for dim_name in ['positive_sentiment', 'negative_sentiment']:
            self.assertIn(dim_name, desc_stats, f"Missing {dim_name} in descriptive statistics")
            dim_stats = desc_stats[dim_name]
            self.assertIn('mean', dim_stats, f"{dim_name} missing mean")
            self.assertIn('std', dim_stats, f"{dim_name} missing std")
            self.assertIn('count', dim_stats, f"{dim_name} missing count")
            
            # Validate statistical values
            self.assertGreaterEqual(dim_stats['mean'], 0.0, f"{dim_name} mean below 0")
            self.assertLessEqual(dim_stats['mean'], 1.0, f"{dim_name} mean above 1")
            self.assertGreaterEqual(dim_stats['std'], 0.0, f"{dim_name} std below 0")
            self.assertGreater(dim_stats['count'], 0, f"{dim_name} count should be positive")
        
        # Micro experiment should have derived metrics statistics
        if has_derived_metrics:
            for metric_name in ['net_sentiment', 'sentiment_magnitude']:
                self.assertIn(metric_name, desc_stats, f"Missing {metric_name} in descriptive statistics")
                metric_stats = desc_stats[metric_name]
                self.assertIn('mean', metric_stats, f"{metric_name} missing mean")
                self.assertIn('std', metric_stats, f"{metric_name} missing std")
                self.assertIn('count', metric_stats, f"{metric_name} missing count")
        
        # Should have ANOVA results for micro experiment
        if has_derived_metrics:
            self.assertIn('anova_results', stats_data, "Missing anova_results")
            anova = stats_data['anova_results']
            self.assertIn('sentiment_category', anova, "Missing sentiment_category ANOVA")
            
            sentiment_anova = anova['sentiment_category']
            self.assertIn('f_statistic', sentiment_anova, "Missing F-statistic")
            self.assertIn('p_value', sentiment_anova, "Missing p-value")
            self.assertIn('significant', sentiment_anova, "Missing significance flag")
            
            # Validate ANOVA values
            self.assertGreaterEqual(sentiment_anova['f_statistic'], 0.0, "F-statistic should be non-negative")
            self.assertGreaterEqual(sentiment_anova['p_value'], 0.0, "p-value should be non-negative")
            self.assertLessEqual(sentiment_anova['p_value'], 1.0, "p-value should be <= 1.0")
            self.assertIsInstance(sentiment_anova['significant'], bool, "Significance should be boolean")
    
    def _validate_synthesis_results(self, results: Dict[str, Any]):
        """Validate synthesis phase results."""
        self.assertIsNotNone(results, "Synthesis results should not be None")
        self.assertIn('synthesis_result', results, "Missing synthesis_result")
        
        synthesis = results['synthesis_result']
        self.assertIn('final_report', synthesis, "Missing final_report")
        
        final_report = synthesis['final_report']
        self.assertIsInstance(final_report, str, "Final report should be a string")
        self.assertGreater(len(final_report), 100, "Final report should be substantial")
        
        # Validate report content
        self.assertIn('sentiment', final_report.lower(), "Report should mention sentiment")
        self.assertIn('analysis', final_report.lower(), "Report should mention analysis")
        
        # Should contain evidence quotes
        self.assertIn('"', final_report, "Report should contain quoted evidence")
        
        # Should mention statistical findings
        self.assertIn('statistical', final_report.lower(), "Report should mention statistical findings")
    
    def _run_experiment_test(self, experiment_path: Path, experiment_name: str, expected_docs: int, has_derived_metrics: bool):
        """Run a complete experiment test with validation."""
        print(f"\n🧪 Testing {experiment_name} experiment...")
        
        # Clean slate
        self._clean_experiment_directories(experiment_path)
        
        # Initialize orchestrator
        orchestrator = CleanAnalysisOrchestrator(experiment_path)
        
        try:
            # Run complete experiment
            print(f"   🚀 Running {experiment_name} with {self.test_model}...")
            results = orchestrator.run_experiment(
                analysis_model=self.test_model,
                synthesis_model=self.test_model,
                validation_model=self.test_model,
                derived_metrics_model=self.test_model,
                skip_validation=False
            )
            
            # Validate results structure
            self.assertIsInstance(results, dict, "Results should be a dictionary")
            self.assertIn('analysis_results', results, "Missing analysis_results")
            self.assertIn('derived_metrics_results', results, "Missing derived_metrics_results")
            self.assertIn('statistical_results', results, "Missing statistical_results")
            self.assertIn('synthesis_results', results, "Missing synthesis_results")
            
            # Validate each phase
            print(f"   ✅ Validating analysis results...")
            self._validate_analysis_results(results['analysis_results'], expected_docs)
            
            print(f"   ✅ Validating derived metrics results...")
            self._validate_derived_metrics_results(results['derived_metrics_results'], has_derived_metrics)
            
            print(f"   ✅ Validating statistical results...")
            self._validate_statistical_results(results['statistical_results'], has_derived_metrics)
            
            print(f"   ✅ Validating synthesis results...")
            self._validate_synthesis_results(results['synthesis_results'])
            
            print(f"   🎉 {experiment_name} test passed!")
            return results
            
        except CleanAnalysisError as e:
            self.fail(f"{experiment_name} experiment failed with CleanAnalysisError: {e}")
        except Exception as e:
            self.fail(f"{experiment_name} experiment failed with unexpected error: {e}")
    
    def test_nano_experiment_integration(self):
        """Test nano experiment: basic pipeline validation with 2 documents."""
        results = self._run_experiment_test(
            experiment_path=self.nano_experiment_path,
            experiment_name="Nano",
            expected_docs=2,
            has_derived_metrics=False
        )
        
        # Additional nano-specific validations
        analysis_results = results['analysis_results']
        
        # Should have one positive and one negative document
        doc_names = [r['document_name'] for r in analysis_results]
        self.assertIn('positive_test.txt', doc_names, "Should have positive test document")
        self.assertIn('negative_test.txt', doc_names, "Should have negative test document")
        
        # Find positive and negative documents
        positive_doc = next(r for r in analysis_results if 'positive' in r['document_name'])
        negative_doc = next(r for r in analysis_results if 'negative' in r['document_name'])
        
        # Positive document should have higher positive sentiment
        pos_score = positive_doc['analysis_result']['dimensional_scores']['positive_sentiment']['raw_score']
        neg_score = negative_doc['analysis_result']['dimensional_scores']['positive_sentiment']['raw_score']
        self.assertGreater(pos_score, neg_score, "Positive document should have higher positive sentiment")
        
        # Negative document should have higher negative sentiment
        pos_neg_score = positive_doc['analysis_result']['dimensional_scores']['negative_sentiment']['raw_score']
        neg_neg_score = negative_doc['analysis_result']['dimensional_scores']['negative_sentiment']['raw_score']
        self.assertGreater(neg_neg_score, pos_neg_score, "Negative document should have higher negative sentiment")
    
    def test_micro_experiment_integration(self):
        """Test micro experiment: complete pipeline with derived metrics and statistics."""
        results = self._run_experiment_test(
            experiment_path=self.micro_experiment_path,
            experiment_name="Micro",
            expected_docs=4,
            has_derived_metrics=True
        )
        
        # Additional micro-specific validations
        analysis_results = results['analysis_results']
        
        # Should have 2 positive and 2 negative documents
        doc_names = [r['document_name'] for r in analysis_results]
        positive_docs = [name for name in doc_names if 'positive' in name]
        negative_docs = [name for name in doc_names if 'negative' in name]
        
        self.assertEqual(len(positive_docs), 2, "Should have 2 positive documents")
        self.assertEqual(len(negative_docs), 2, "Should have 2 negative documents")
        
        # Validate derived metrics calculations
        derived_metrics = results['derived_metrics_results']['derived_metrics_data']
        
        # Check net sentiment calculations
        net_sentiment_data = derived_metrics['net_sentiment']
        self.assertEqual(len(net_sentiment_data), 4, "Should have net sentiment for all 4 documents")
        
        # Check sentiment magnitude calculations
        sentiment_magnitude_data = derived_metrics['sentiment_magnitude']
        self.assertEqual(len(sentiment_magnitude_data), 4, "Should have sentiment magnitude for all 4 documents")
        
        # Validate statistical analysis
        stats_data = results['statistical_results']['statistical_data']
        
        # Should have ANOVA results
        anova = stats_data['anova_results']['sentiment_category']
        self.assertIsNotNone(anova['f_statistic'], "Should have F-statistic")
        self.assertIsNotNone(anova['p_value'], "Should have p-value")
        
        # Should have group statistics
        self.assertIn('group_statistics', stats_data, "Missing group statistics")
        group_stats = stats_data['group_statistics']
        self.assertIn('positive', group_stats, "Missing positive group statistics")
        self.assertIn('negative', group_stats, "Missing negative group statistics")
    
    def test_experiment_cleanup_and_isolation(self):
        """Test that experiments run in isolation without interference."""
        print(f"\n🧪 Testing experiment isolation...")
        
        # Run nano experiment first
        self._clean_experiment_directories(self.nano_experiment_path)
        orchestrator1 = CleanAnalysisOrchestrator(self.nano_experiment_path)
        results1 = orchestrator1.run_experiment(
            analysis_model=self.test_model,
            synthesis_model=self.test_model,
            validation_model=self.test_model,
            derived_metrics_model=self.test_model,
            skip_validation=False
        )
        
        # Run micro experiment second
        self._clean_experiment_directories(self.micro_experiment_path)
        orchestrator2 = CleanAnalysisOrchestrator(self.micro_experiment_path)
        results2 = orchestrator2.run_experiment(
            analysis_model=self.test_model,
            synthesis_model=self.test_model,
            validation_model=self.test_model,
            derived_metrics_model=self.test_model,
            skip_validation=False
        )
        
        # Verify both experiments completed successfully
        self.assertIsNotNone(results1, "Nano experiment should complete")
        self.assertIsNotNone(results2, "Micro experiment should complete")
        
        # Verify different document counts
        self.assertEqual(len(results1['analysis_results']), 2, "Nano should have 2 documents")
        self.assertEqual(len(results2['analysis_results']), 4, "Micro should have 4 documents")
        
        # Verify different derived metrics
        self.assertIsNone(results1['derived_metrics_results'], "Nano should have no derived metrics")
        self.assertIsNotNone(results2['derived_metrics_results'], "Micro should have derived metrics")
        
        print(f"   ✅ Experiment isolation test passed!")


if __name__ == '__main__':
    # Set up test environment
    print("🧪 Nano and Micro Integration Tests")
    print("=" * 50)
    print("Using real LLMs for comprehensive pipeline validation")
    print("Model: vertex_ai/gemini-2.5-flash-lite")
    print("Estimated cost: ~$0.003 for full test suite")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)
