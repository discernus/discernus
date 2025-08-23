#!/usr/bin/env python3

"""
Unit tests for Cache Integrity

Tests that all cache managers properly handle missing artifacts and don't
report false cache hits when registry metadata exists but artifact files are missing.
"""

import unittest
from unittest.mock import Mock, patch
import json
import tempfile
import shutil
from pathlib import Path

# Import cache managers to test
from discernus.core.derived_metrics_cache import DerivedMetricsCacheManager
from discernus.core.statistical_analysis_cache import StatisticalAnalysisCacheManager
from discernus.core.validation_cache import ValidationCacheManager
from discernus.core.rag_index_cache import RAGIndexCacheManager


class TestCacheIntegrity(unittest.TestCase):
    """Test cache integrity across all cache managers."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_artifact_storage = Mock()
        self.mock_audit_logger = Mock()
        
        # Mock artifact storage registry
        self.mock_artifact_storage.registry = {}
    
    def test_derived_metrics_cache_missing_artifact(self):
        """Test derived metrics cache handles missing artifacts correctly."""
        cache_manager = DerivedMetricsCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "derived_metrics_test123"
        artifact_hash = "missing_artifact_hash"
        
        # Set up registry with metadata but artifact doesn't exist
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "derived_metrics_functions",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact_exists to return False (missing file)
        self.mock_artifact_storage.artifact_exists.return_value = False
        
        # Check cache - should be a miss despite registry metadata
        result = cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_functions)
        
        # Verify artifact_exists was called to check integrity
        self.mock_artifact_storage.artifact_exists.assert_called_once_with(artifact_hash)
    
    def test_statistical_analysis_cache_missing_artifact(self):
        """Test statistical analysis cache handles missing artifacts correctly."""
        cache_manager = StatisticalAnalysisCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "statistical_analysis_test123"
        artifact_hash = "missing_artifact_hash"
        
        # Set up registry with metadata but artifact doesn't exist
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "statistical_analysis_functions",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact_exists to return False (missing file)
        self.mock_artifact_storage.artifact_exists.return_value = False
        
        # Check cache - should be a miss despite registry metadata
        result = cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_functions)
        
        # Verify artifact_exists was called to check integrity
        self.mock_artifact_storage.artifact_exists.assert_called_once_with(artifact_hash)
    
    def test_validation_cache_missing_artifact(self):
        """Test validation cache handles missing artifacts correctly."""
        cache_manager = ValidationCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "validation_test123"
        artifact_hash = "missing_artifact_hash"
        
        # Set up registry with metadata but artifact doesn't exist
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "validation_result",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact_exists to return False (missing file)
        self.mock_artifact_storage.artifact_exists.return_value = False
        
        # Check cache - should be a miss despite registry metadata
        result = cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_validation)
        
        # Verify artifact_exists was called to check integrity
        self.mock_artifact_storage.artifact_exists.assert_called_once_with(artifact_hash)
    
    def test_rag_index_cache_missing_artifact(self):
        """Test RAG index cache handles missing artifacts correctly."""
        cache_manager = RAGIndexCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "rag_index_test123"
        artifact_hash = "missing_artifact_hash"
        
        # Set up registry with metadata but artifact doesn't exist
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "rag_index_cache",
                    "rag_cache_key": cache_key
                }
            }
        }
        
        # Mock artifact_exists to return False (missing file)
        self.mock_artifact_storage.artifact_exists.return_value = False
        
        # Check cache - should be a miss despite registry metadata
        result = cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_index)
        
        # Verify artifact_exists was called to check integrity
        self.mock_artifact_storage.artifact_exists.assert_called_once_with(artifact_hash)
    
    def test_derived_metrics_cache_valid_artifact(self):
        """Test derived metrics cache works correctly when artifact exists."""
        cache_manager = DerivedMetricsCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "derived_metrics_test123"
        artifact_hash = "valid_artifact_hash"
        
        # Mock valid cached functions
        cached_functions = {
            "functions": ["def test_function(): pass"],
            "success": True
        }
        
        # Set up registry with metadata and artifact exists
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "derived_metrics_functions",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact exists and retrieval
        self.mock_artifact_storage.artifact_exists.return_value = True
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(cached_functions).encode('utf-8')
        
        # Check cache - should be a hit
        result = cache_manager.check_cache(cache_key)
        
        self.assertTrue(result.hit)
        self.assertEqual(result.cached_functions, cached_functions)
        self.assertEqual(result.artifact_hash, artifact_hash)
        
        # Verify integrity check was performed
        self.mock_artifact_storage.artifact_exists.assert_called_once_with(artifact_hash)
        self.mock_artifact_storage.get_artifact.assert_called_once_with(artifact_hash)
    
    def test_multiple_artifacts_with_mixed_integrity(self):
        """Test cache behavior when multiple artifacts exist with mixed integrity."""
        cache_manager = DerivedMetricsCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
        
        cache_key = "derived_metrics_test123"
        missing_hash = "missing_artifact_hash"
        valid_hash = "valid_artifact_hash"
        
        # Mock valid cached functions
        cached_functions = {
            "functions": ["def test_function(): pass"],
            "success": True
        }
        
        # Set up registry with multiple artifacts for same cache key
        self.mock_artifact_storage.registry = {
            missing_hash: {
                "metadata": {
                    "artifact_type": "derived_metrics_functions",
                    "cache_key": cache_key
                }
            },
            valid_hash: {
                "metadata": {
                    "artifact_type": "derived_metrics_functions",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact_exists: first missing, second valid
        def mock_artifact_exists(hash_id):
            return hash_id == valid_hash
        
        self.mock_artifact_storage.artifact_exists.side_effect = mock_artifact_exists
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(cached_functions).encode('utf-8')
        
        # Check cache - should find the valid artifact and skip the missing one
        result = cache_manager.check_cache(cache_key)
        
        self.assertTrue(result.hit)
        self.assertEqual(result.cached_functions, cached_functions)
        self.assertEqual(result.artifact_hash, valid_hash)
        
        # Verify both artifacts were checked for integrity
        self.assertEqual(self.mock_artifact_storage.artifact_exists.call_count, 2)


if __name__ == '__main__':
    unittest.main()
