#!/usr/bin/env python3
"""Unit tests for the clean fact checker agent implementation."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List
import json

# Import the agent
from discernus.agents.fact_checker_agent.agent import FactCheckerAgent


class TestFactCheckerAgentClean(unittest.TestCase):
    """Test the clean fact checker agent implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mocks
        self.mock_artifact_storage = Mock()
        self.mock_corpus_service = Mock()
        self.mock_gateway = Mock()
        
        # Create agent with mocked dependencies
        self.agent = FactCheckerAgent(
            gateway=self.mock_gateway,
            corpus_index_service=self.mock_corpus_service,
            artifact_storage=self.mock_artifact_storage
        )
        
    def test_discover_synthesis_report(self):
        """Test discovering synthesis report from artifact storage."""
        
        # Mock artifact storage to return synthesis report artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "synthesis_report"}, "hash_id": "hash1"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        test_content = {"content": "Test synthesis report", "content_type": "text"}
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(test_content).encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_synthesis_report()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result["content"], '{"content": "Test synthesis report", "content_type": "text"}')
        self.assertEqual(result["content_type"], "text")
        
    def test_discover_evidence_data(self):
        """Test discovering evidence data from artifact storage."""
        
        # Mock artifact storage to return evidence artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "evidence_collection"}, "hash_id": "hash2"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        mock_content = {"evidence_results": [], "metadata": {"total_quotes": 10}}
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(mock_content).encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_evidence_data()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertIn("evidence_results", result["content"])
        
    def test_discover_framework_spec(self):
        """Test discovering framework specification from artifact storage."""
        
        # Mock artifact storage to return framework artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "framework_specification"}, "hash_id": "hash3"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        mock_content = {"dimensions": ["dim1", "dim2"], "description": "Test framework"}
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(mock_content).encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_framework_spec()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertIn("dimensions", result["content"])
        
    def test_discover_raw_analysis_data(self):
        """Test discovering raw analysis data from artifact storage."""
        
        # Mock artifact storage to return raw analysis artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "raw_analysis_response_v6"}, "hash_id": "hash4"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        mock_content = {
            "document_analyses": [{
                "dimensional_scores": {
                    "dimension_name": {
                        "raw_score": 0.8,
                        "salience": 0.7,
                        "confidence": 0.9
                    }
                }
            }]
        }
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(mock_content).encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_raw_analysis_data()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertIn("document_analyses", result["content"])
        
    def test_discover_derived_metrics_data(self):
        """Test discovering derived metrics data from artifact storage."""
        
        # Mock artifact storage to return derived metrics artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "derived_metrics_results_with_data"}, "hash_id": "hash5"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        mock_content = {
            "identity_tension": 0.75,
            "emotional_balance": 0.82,
            "success_climate": 0.68
        }
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(mock_content).encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_derived_metrics_data()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertIn("identity_tension", result["content"])
        
    def test_discover_statistical_results_data(self):
        """Test discovering statistical results data from artifact storage."""
        
        # Mock artifact storage to return statistical results artifacts
        mock_artifacts = [
            {"metadata": {"artifact_type": "statistical_results_with_data"}, "hash_id": "hash6"}
        ]
        self.mock_artifact_storage.list_artifacts.return_value = mock_artifacts
        
        # Mock artifact content loading
        mock_content = "test_name,test_type,statistic_name,statistic_value,p_value,effect_size\ndescriptives,descriptive_stats,mean,0.5916666666666667,,,48"
        self.mock_artifact_storage.get_artifact.return_value = mock_content.encode('utf-8')
        
        # Test discovery
        result = self.agent._discover_statistical_results_data()
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertIn("descriptives", result["content"])
        
    def test_discover_semantic_index_with_wrapper(self):
        """Test discovering semantic index and wrapper methods."""
        
        # Mock the discovery method to return a fake index
        mock_index = Mock()
        mock_index.get_search_wrapper_methods.return_value = {
            "validate_quote": Mock(),
            "search_documents": Mock(),
            "get_context": Mock()
        }
        
        # Mock artifact storage to return our fake index
        self.mock_artifact_storage.get_artifact.return_value = mock_index
        
        # Mock the artifact storage list_artifacts method to return corpus index artifacts
        self.mock_artifact_storage.list_artifacts.return_value = [
            {"metadata": {"artifact_type": "corpus_index"}, "hash_id": "hash1"}
        ]
        
        # Mock the index to have the required properties
        mock_index.get_capabilities.return_value = ["corpus_search", "quote_validation"]
        
        # Test the discovery
        index, wrapper_methods = self.agent._discover_semantic_index_with_wrapper(
            required_properties=["corpus_search", "quote_validation"]
        )
        
        # Verify we got the index and wrapper methods
        self.assertEqual(index, mock_index)
        self.assertIn("validate_quote", wrapper_methods)
        self.assertIn("search_documents", wrapper_methods)
        
    def test_discover_artifacts_by_type(self):
        """Test discovering artifacts by type."""
        
        # Mock artifact storage to return fake artifacts
        fake_artifacts = [
            {"metadata": {"artifact_type": "corpus_index"}, "hash_id": "hash1"},
            {"metadata": {"artifact_type": "corpus_index"}, "hash_id": "hash2"},
            {"metadata": {"artifact_type": "evidence_index"}, "hash_id": "hash3"}
        ]
        
        self.mock_artifact_storage.list_artifacts.return_value = fake_artifacts
        
        # Test discovery
        corpus_artifacts = self.agent._discover_artifacts_by_type("corpus_index")
        
        # Verify we got the right artifacts with normalized hash field
        self.assertEqual(len(corpus_artifacts), 2)
        self.assertEqual(corpus_artifacts[0]["hash"], "hash1")
        self.assertEqual(corpus_artifacts[1]["hash"], "hash2")
        
    def test_index_has_properties(self):
        """Test checking if an index has required properties."""
        
        # Mock index with properties
        mock_index = Mock()
        mock_index.get_capabilities.return_value = [
            "corpus_search", "quote_validation", "semantic_search"
        ]
        
        # Test property checking
        has_props = self.agent._index_has_properties(
            mock_index, 
            ["corpus_search", "quote_validation"]
        )
        
        self.assertTrue(has_props)
        
        # Test missing properties
        has_props = self.agent._index_has_properties(
            mock_index, 
            ["corpus_search", "missing_property"]
        )
        
        self.assertFalse(has_props)
        
    def test_get_default_corpus_wrappers(self):
        """Test fallback to default corpus wrappers."""
        
        # Test that default wrappers are provided when index doesn't have them
        default_wrappers = self.agent._get_default_corpus_wrappers()
        
        # Verify we get some wrapper methods
        self.assertIsInstance(default_wrappers, dict)
        self.assertIn("validate_quote", default_wrappers)
        self.assertIn("search_documents", default_wrappers)
        
    def test_load_artifact_content(self):
        """Test loading artifact content from storage."""
        
        # Test text content
        test_content = "Test artifact content"
        test_bytes = test_content.encode('utf-8')
        
        # Mock artifact storage to return our test content
        self.mock_artifact_storage.get_artifact.return_value = test_bytes
        
        # Test loading
        result = self.agent._load_artifact_content("test_hash")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result["content"], "Test artifact content")
        self.assertEqual(result["content_type"], "text")
        self.assertEqual(result["size_bytes"], len(test_bytes))
        
    def test_run_method_workflow(self):
        """Test the complete run method workflow."""
        
        # Mock all discovery methods to return valid data
        with patch.object(self.agent, '_discover_synthesis_report') as mock_synth:
            with patch.object(self.agent, '_discover_evidence_data') as mock_evidence:
                with patch.object(self.agent, '_discover_framework_spec') as mock_framework:
                    with patch.object(self.agent, '_discover_semantic_index_with_wrapper') as mock_index:
                        with patch.object(self.agent, '_discover_raw_analysis_data') as mock_raw:
                            with patch.object(self.agent, '_discover_derived_metrics_data') as mock_derived:
                                with patch.object(self.agent, '_discover_statistical_results_data') as mock_stats:
                                    with patch.object(self.agent, '_run_fact_checking') as mock_run:
                                        
                                        # Set up mock returns
                                        mock_synth.return_value = {"content": "Test report"}
                                        mock_evidence.return_value = {"content": "Test evidence"}
                                        mock_framework.return_value = {"content": "Test framework"}
                                        mock_index.return_value = (Mock(), {"search": Mock()})
                                        mock_raw.return_value = {"content": "Test raw data"}
                                        mock_derived.return_value = {"content": "Test derived data"}
                                        mock_stats.return_value = {"content": "Test stats"}
                                        mock_run.return_value = {
                                            "status": "completed",
                                            "findings": [],
                                            "summary": {"total_issues": 0}
                                        }
                                        
                                        # Test the run method
                                        result = self.agent.run()
                                        
                                        # Verify the result
                                        self.assertEqual(result["status"], "completed")
                                        self.assertIn("findings", result)
                                        self.assertIn("summary", result)
                                        
                                        # Verify all discovery methods were called
                                        mock_synth.assert_called_once()
                                        mock_evidence.assert_called_once()
                                        mock_framework.assert_called_once()
                                        mock_index.assert_called_once()
                                        mock_raw.assert_called_once()
                                        mock_derived.assert_called_once()
                                        mock_stats.assert_called_once()
                                        mock_run.assert_called_once()
        
    def test_run_method_failure_handling(self):
        """Test run method handles discovery failures gracefully."""
        
        # Mock synthesis report discovery to fail
        with patch.object(self.agent, '_discover_synthesis_report', return_value=None):
            
            # Test the run method
            result = self.agent.run()
            
            # Verify failure is handled gracefully
            self.assertEqual(result["status"], "failed")
            self.assertIn("No synthesis report found", result["error"])
            self.assertEqual(len(result["findings"]), 0)
            
    def test_prepare_fact_checking_context(self):
        """Test context preparation for LLM fact checking."""
        
        # Test data
        synthesis_report = {"content": "Test report content"}
        evidence_data = {"content": "Test evidence"}
        framework_spec = {"content": "Test framework"}
        corpus_index = Mock()
        search_wrappers = {"search": Mock()}
        raw_analysis = {"content": "Test raw analysis"}
        derived_metrics = {"content": "Test derived metrics"}
        statistical_results = {"content": "Test statistical results"}
        
        # Test context preparation
        context = self.agent._prepare_fact_checking_context(
            synthesis_report, evidence_data, framework_spec, corpus_index,
            search_wrappers, raw_analysis, derived_metrics, statistical_results
        )
        
        # Verify all sections are included
        self.assertIn("SYNTHESIS REPORT TO VALIDATE", context)
        self.assertIn("AVAILABLE EVIDENCE DATA", context)
        self.assertIn("FRAMEWORK SPECIFICATION", context)
        self.assertIn("RAW ANALYSIS DATA", context)
        self.assertIn("DERIVED METRICS DATA", context)
        self.assertIn("STATISTICAL RESULTS DATA", context)
        self.assertIn("CORPUS INDEX CAPABILITIES", context)
        self.assertIn("DISCOVERY METHODS AVAILABLE", context)
        
    def test_log_resource_access(self):
        """Test resource access logging functionality."""
        
        # Test logging with valid resource data
        test_resource = {"content": "Test content", "content_type": "text"}
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            self.agent._log_resource_access("test_resource", test_resource)
            
            # Verify logging occurred
            mock_print.assert_called()
            
        # Test logging with None resource
        with patch('builtins.print') as mock_print:
            self.agent._log_resource_access("missing_resource", None)
            
            # Verify missing resource is logged
            mock_print.assert_called()


if __name__ == "__main__":
    unittest.main()

