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
    
    def _validate_synthesis_results(self, results: Dict[str, Any], analysis_results: List[Dict[str, Any]], 
                                  statistical_results: Dict[str, Any], has_derived_metrics: bool):
        """Validate synthesis phase results with sophisticated content validation."""
        self.assertIsNotNone(results, "Synthesis results should not be None")
        self.assertIn('synthesis_result', results, "Missing synthesis_result")
        
        synthesis = results['synthesis_result']
        self.assertIn('final_report', synthesis, "Missing final_report")
        
        final_report = synthesis['final_report']
        self.assertIsInstance(final_report, str, "Final report should be a string")
        self.assertGreater(len(final_report), 100, "Final report should be substantial")
        
        # Advanced content validation
        self._validate_report_content_quality(final_report, analysis_results, statistical_results, has_derived_metrics)
        self._validate_evidence_integration(final_report, analysis_results)
        self._validate_statistical_integration(final_report, statistical_results, has_derived_metrics)
        self._validate_report_structure(final_report)
    
    def _validate_report_content_quality(self, final_report: str, analysis_results: List[Dict[str, Any]], 
                                       statistical_results: Dict[str, Any], has_derived_metrics: bool):
        """Validate the quality and completeness of report content."""
        report_lower = final_report.lower()
        
        # Basic content requirements
        self.assertIn('sentiment', report_lower, "Report should mention sentiment")
        self.assertIn('analysis', report_lower, "Report should mention analysis")
        
        # Should contain evidence quotes (not just placeholders)
        self.assertIn('"', final_report, "Report should contain quoted evidence")
        
        # Should mention statistical findings
        self.assertIn('statistical', report_lower, "Report should mention statistical findings")
        
        # Validate document awareness
        doc_names = [r['document_name'] for r in analysis_results]
        for doc_name in doc_names:
            # Report should show awareness of the documents analyzed
            self.assertIn(doc_name.replace('.txt', ''), report_lower, 
                         f"Report should mention document {doc_name}")
        
        # Validate dimensional awareness
        for result in analysis_results:
            dim_scores = result['analysis_result']['dimensional_scores']
            for dim_name in dim_scores.keys():
                # Report should mention the dimensions analyzed
                self.assertIn(dim_name.replace('_', ' '), report_lower, 
                             f"Report should mention dimension {dim_name}")
        
        # Validate derived metrics awareness (micro experiment only)
        if has_derived_metrics:
            self.assertIn('net sentiment', report_lower, "Report should mention net sentiment")
            self.assertIn('sentiment magnitude', report_lower, "Report should mention sentiment magnitude")
    
    def _validate_evidence_integration(self, final_report: str, analysis_results: List[Dict[str, Any]]):
        """Validate that actual evidence quotes from analysis appear in the final report."""
        # Extract evidence quotes from analysis results
        expected_evidence = []
        for result in analysis_results:
            dim_scores = result['analysis_result']['dimensional_scores']
            for dim_name, score_obj in dim_scores.items():
                evidence = score_obj['evidence']
                if evidence and len(evidence.strip()) > 0:
                    expected_evidence.append(evidence.strip())
        
        # At least some evidence should appear in the final report
        evidence_found = 0
        for evidence in expected_evidence:
            if evidence in final_report:
                evidence_found += 1
        
        self.assertGreater(evidence_found, 0, 
                          f"At least one evidence quote should appear in final report. "
                          f"Expected evidence: {expected_evidence[:2]}...")
        
        # Validate that quotes are properly attributed
        self.assertIn('"', final_report, "Report should contain quoted evidence")
        
        # Check for proper citation patterns
        has_citations = any(pattern in final_report.lower() for pattern in [
            'according to', 'as stated in', 'the text shows', 'evidence suggests'
        ])
        self.assertTrue(has_citations, "Report should contain proper citation patterns")
    
    def _validate_statistical_integration(self, final_report: str, statistical_results: Dict[str, Any], 
                                        has_derived_metrics: bool):
        """Validate that statistical findings appear in the final report."""
        stats_data = statistical_results['statistical_data']
        report_lower = final_report.lower()
        
        # Validate descriptive statistics integration
        desc_stats = stats_data['descriptive_statistics']
        for dim_name in ['positive_sentiment', 'negative_sentiment']:
            if dim_name in desc_stats:
                mean_val = desc_stats[dim_name]['mean']
                # Report should mention the actual statistical values
                self.assertIn(str(round(mean_val, 2)), final_report, 
                             f"Report should mention {dim_name} mean value {mean_val}")
        
        # Validate derived metrics integration (micro experiment only)
        if has_derived_metrics:
            for metric_name in ['net_sentiment', 'sentiment_magnitude']:
                if metric_name in desc_stats:
                    mean_val = desc_stats[metric_name]['mean']
                    self.assertIn(str(round(mean_val, 2)), final_report, 
                                 f"Report should mention {metric_name} mean value {mean_val}")
            
            # Validate ANOVA integration
            if 'anova_results' in stats_data:
                anova = stats_data['anova_results']['sentiment_category']
                f_stat = anova['f_statistic']
                p_val = anova['p_value']
                
                # Report should mention ANOVA results
                self.assertIn(str(round(f_stat, 2)), final_report, 
                             f"Report should mention F-statistic {f_stat}")
                self.assertIn(str(round(p_val, 3)), final_report, 
                             f"Report should mention p-value {p_val}")
                
                # Report should interpret significance
                if anova['significant']:
                    self.assertTrue(any(word in report_lower for word in ['significant', 'difference', 'vary']), 
                                  "Report should mention significance when ANOVA is significant")
    
    def _validate_report_structure(self, final_report: str):
        """Validate the structure and quality of the final report."""
        # Should have proper academic structure
        structure_indicators = ['summary', 'findings', 'analysis', 'conclusion', 'results']
        found_indicators = sum(1 for indicator in structure_indicators 
                             if indicator in final_report.lower())
        self.assertGreaterEqual(found_indicators, 2, 
                               "Report should have academic structure with multiple sections")
        
        # Should not contain placeholder text
        placeholder_patterns = [
            'placeholder', 'todo', 'insert', 'replace', 'example text',
            'your analysis here', 'fill in', 'template'
        ]
        for pattern in placeholder_patterns:
            self.assertNotIn(pattern, final_report.lower(), 
                           f"Report should not contain placeholder text: {pattern}")
        
        # Should have reasonable length and coherence
        self.assertGreater(len(final_report), 500, "Report should be substantial")
        self.assertLess(len(final_report), 10000, "Report should not be excessively long")
        
        # Should have proper paragraph structure
        paragraphs = [p.strip() for p in final_report.split('\n\n') if p.strip()]
        self.assertGreaterEqual(len(paragraphs), 3, "Report should have multiple paragraphs")
    
    def _validate_orchestration_completeness(self, results: Dict[str, Any], experiment_name: str):
        """Validate that all orchestration steps completed successfully."""
        # Check that all expected phases are present
        required_phases = ['analysis_results', 'derived_metrics_results', 
                          'statistical_results', 'synthesis_results']
        
        for phase in required_phases:
            self.assertIn(phase, results, f"Missing {phase} in orchestration results")
            self.assertIsNotNone(results[phase], f"{phase} should not be None")
        
        # Validate phase-specific completeness
        self._validate_analysis_phase_completeness(results['analysis_results'], experiment_name)
        self._validate_derived_metrics_phase_completeness(results['derived_metrics_results'], experiment_name)
        self._validate_statistical_phase_completeness(results['statistical_results'], experiment_name)
        self._validate_synthesis_phase_completeness(results['synthesis_results'], experiment_name)
    
    def _validate_analysis_phase_completeness(self, analysis_results: List[Dict[str, Any]], experiment_name: str):
        """Validate analysis phase completed completely."""
        expected_docs = 2 if 'nano' in experiment_name.lower() else 4
        
        self.assertEqual(len(analysis_results), expected_docs, 
                        f"Analysis should process all {expected_docs} documents")
        
        for result in analysis_results:
            # Each document should have complete analysis
            self.assertIn('document_name', result, "Analysis result missing document_name")
            self.assertIn('analysis_result', result, "Analysis result missing analysis_result")
            
            analysis = result['analysis_result']
            self.assertIn('dimensional_scores', analysis, "Analysis missing dimensional_scores")
            
            # All dimensions should be scored
            dim_scores = analysis['dimensional_scores']
            self.assertIn('positive_sentiment', dim_scores, "Missing positive_sentiment")
            self.assertIn('negative_sentiment', dim_scores, "Missing negative_sentiment")
            
            # Each dimension should have complete scoring
            for dim_name, score_obj in dim_scores.items():
                required_fields = ['raw_score', 'salience', 'confidence', 'evidence']
                for field in required_fields:
                    self.assertIn(field, score_obj, f"{dim_name} missing {field}")
                    self.assertIsNotNone(score_obj[field], f"{dim_name}.{field} should not be None")
    
    def _validate_derived_metrics_phase_completeness(self, derived_metrics_results: Dict[str, Any], experiment_name: str):
        """Validate derived metrics phase completed completely."""
        has_derived_metrics = 'micro' in experiment_name.lower()
        
        if not has_derived_metrics:
            self.assertIsNone(derived_metrics_results, "Nano experiment should have no derived metrics")
            return
        
        # Micro experiment should have complete derived metrics
        self.assertIsNotNone(derived_metrics_results, "Micro experiment should have derived metrics")
        self.assertIn('derived_metrics_data', derived_metrics_results, "Missing derived_metrics_data")
        
        derived_data = derived_metrics_results['derived_metrics_data']
        expected_metrics = ['net_sentiment', 'sentiment_magnitude']
        
        for metric_name in expected_metrics:
            self.assertIn(metric_name, derived_data, f"Missing {metric_name} derived metric")
            metric_data = derived_data[metric_name]
            self.assertIsInstance(metric_data, list, f"{metric_name} should be a list")
            self.assertEqual(len(metric_data), 4, f"{metric_name} should have 4 values")
            
            for i, doc_metric in enumerate(metric_data):
                self.assertIn('document_name', doc_metric, f"{metric_name}[{i}] missing document_name")
                self.assertIn('metric_value', doc_metric, f"{metric_name}[{i}] missing metric_value")
                self.assertIsInstance(doc_metric['metric_value'], (int, float), 
                                    f"{metric_name}[{i}] metric_value should be numeric")
    
    def _validate_statistical_phase_completeness(self, statistical_results: Dict[str, Any], experiment_name: str):
        """Validate statistical analysis phase completed completely."""
        self.assertIsNotNone(statistical_results, "Statistical results should not be None")
        self.assertIn('statistical_data', statistical_results, "Missing statistical_data")
        
        stats_data = statistical_results['statistical_data']
        has_derived_metrics = 'micro' in experiment_name.lower()
        
        # Should have descriptive statistics for all dimensions
        self.assertIn('descriptive_statistics', stats_data, "Missing descriptive_statistics")
        desc_stats = stats_data['descriptive_statistics']
        
        for dim_name in ['positive_sentiment', 'negative_sentiment']:
            self.assertIn(dim_name, desc_stats, f"Missing {dim_name} in descriptive statistics")
            dim_stats = desc_stats[dim_name]
            
            required_stats = ['mean', 'std', 'count', 'min', 'max']
            for stat_name in required_stats:
                self.assertIn(stat_name, dim_stats, f"{dim_name} missing {stat_name}")
                self.assertIsNotNone(dim_stats[stat_name], f"{dim_name}.{stat_name} should not be None")
        
        # Micro experiment should have derived metrics statistics
        if has_derived_metrics:
            for metric_name in ['net_sentiment', 'sentiment_magnitude']:
                self.assertIn(metric_name, desc_stats, f"Missing {metric_name} in descriptive statistics")
                metric_stats = desc_stats[metric_name]
                
                for stat_name in ['mean', 'std', 'count']:
                    self.assertIn(stat_name, metric_stats, f"{metric_name} missing {stat_name}")
                    self.assertIsNotNone(metric_stats[stat_name], f"{metric_name}.{stat_name} should not be None")
            
            # Should have ANOVA results
            self.assertIn('anova_results', stats_data, "Missing anova_results")
            anova = stats_data['anova_results']
            self.assertIn('sentiment_category', anova, "Missing sentiment_category ANOVA")
            
            sentiment_anova = anova['sentiment_category']
            anova_fields = ['f_statistic', 'p_value', 'significant', 'df_between', 'df_within']
            for field in anova_fields:
                self.assertIn(field, sentiment_anova, f"ANOVA missing {field}")
                self.assertIsNotNone(sentiment_anova[field], f"ANOVA.{field} should not be None")
    
    def _validate_synthesis_phase_completeness(self, synthesis_results: Dict[str, Any], experiment_name: str):
        """Validate synthesis phase completed completely."""
        self.assertIsNotNone(synthesis_results, "Synthesis results should not be None")
        self.assertIn('synthesis_result', synthesis_results, "Missing synthesis_result")
        
        synthesis = synthesis_results['synthesis_result']
        self.assertIn('final_report', synthesis, "Missing final_report")
        
        final_report = synthesis['final_report']
        self.assertIsInstance(final_report, str, "Final report should be a string")
        self.assertGreater(len(final_report), 100, "Final report should be substantial")
        
        # Should not contain error indicators
        error_indicators = ['error', 'failed', 'exception', 'traceback', 'none', 'null']
        for indicator in error_indicators:
            self.assertNotIn(indicator, final_report.lower(), 
                           f"Final report should not contain error indicator: {indicator}")
        
        # Should contain success indicators
        success_indicators = ['analysis', 'findings', 'results', 'conclusion']
        found_success = sum(1 for indicator in success_indicators 
                          if indicator in final_report.lower())
        self.assertGreaterEqual(found_success, 2, "Final report should contain success indicators")
    
    def _validate_no_unexpected_errors(self, experiment_path: Path, experiment_name: str):
        """Validate that no unexpected errors occurred during orchestration."""
        # Check for error log files
        error_log_path = experiment_path / "logs" / "errors.log"
        if error_log_path.exists():
            error_content = error_log_path.read_text()
            if error_content.strip():
                # Check for critical errors (not just warnings)
                critical_errors = ['exception', 'traceback', 'failed', 'error:', 'critical']
                has_critical_errors = any(error in error_content.lower() for error in critical_errors)
                if has_critical_errors:
                    self.fail(f"Critical errors found in error log: {error_content[:500]}...")
        
        # Check session logs for errors
        session_dir = experiment_path / "session"
        if session_dir.exists():
            for session_run in session_dir.iterdir():
                if session_run.is_dir():
                    error_log = session_run / "logs" / "errors.log"
                    if error_log.exists():
                        error_content = error_log.read_text()
                        if error_content.strip():
                            critical_errors = ['exception', 'traceback', 'failed', 'error:', 'critical']
                            has_critical_errors = any(error in error_content.lower() for error in critical_errors)
                            if has_critical_errors:
                                self.fail(f"Critical errors found in session log: {error_content[:500]}...")
        
        # Check for incomplete runs (should have runs directory with results)
        runs_dir = experiment_path / "runs"
        if not runs_dir.exists():
            self.fail("No runs directory found - experiment may not have completed")
        
        # Check that runs directory has at least one completed run
        completed_runs = [run_dir for run_dir in runs_dir.iterdir() 
                         if run_dir.is_dir() and (run_dir / "results").exists()]
        self.assertGreater(len(completed_runs), 0, "No completed runs found")
        
        # Check that the latest run has all expected result files
        latest_run = max(completed_runs, key=lambda x: x.name)
        results_dir = latest_run / "results"
        
        expected_files = ['final_report.md', 'statistical_results.json', 'experiment_summary.json']
        for expected_file in expected_files:
            file_path = results_dir / expected_file
            self.assertTrue(file_path.exists(), f"Missing expected result file: {expected_file}")
            
            # Check that files are not empty
            if file_path.stat().st_size == 0:
                self.fail(f"Result file is empty: {expected_file}")
    
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
            self._validate_synthesis_results(results['synthesis_results'], results['analysis_results'], 
                                           results['statistical_results'], has_derived_metrics)
            
            print(f"   ✅ Validating orchestration completeness...")
            self._validate_orchestration_completeness(results, experiment_name)
            
            print(f"   ✅ Validating no unexpected errors...")
            self._validate_no_unexpected_errors(experiment_path, experiment_name)
            
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
