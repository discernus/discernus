#!/usr/bin/env python3
"""Unit tests for fact checker agent discovery mechanism."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Import the agent
from discernus.agents.fact_checker_agent.agent import FactCheckerAgent


class TestFactCheckerDiscovery(unittest.TestCase):
    """Test the discovery and dynamic loading mechanism."""
    
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
        
    def test_discover_semantic_index_with_wrapper(self):
        """Test discovering a semantic index and its wrapper methods."""
        
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
        
        # Verify we got the right artifacts
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


if __name__ == "__main__":
    unittest.main()

