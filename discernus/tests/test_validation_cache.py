#!/usr/bin/env python3

"""
Unit tests for Validation Cache Manager

Tests the caching functionality for experiment coherence validation to ensure
proper cache key generation, storage, and retrieval.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime, timezone

# Import the class under test
from discernus.core.deprecated.validation_cache import ValidationCacheManager, ValidationCacheResult


class TestValidationCacheManager(unittest.TestCase):
    """Test cases for Validation Cache Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_artifact_storage = Mock()
        self.mock_audit_logger = Mock()
        
        # Mock artifact storage registry
        self.mock_artifact_storage.registry = {}
        
        # Initialize cache manager
        self.cache_manager = ValidationCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
    
    def test_generate_cache_key_deterministic(self):
        """Test that cache key generation is deterministic."""
        framework_content = "# Test Framework\nSome content"
        experiment_content = "# Test Experiment\nSome experiment"
        corpus_content = "# Test Corpus\nSome corpus"
        model = "vertex_ai/gemini-2.5-pro"
        
        key1 = self.cache_manager.generate_cache_key(
            framework_content, experiment_content, corpus_content, model
        )
        key2 = self.cache_manager.generate_cache_key(
            framework_content, experiment_content, corpus_content, model
        )
        
        self.assertEqual(key1, key2)
        self.assertTrue(key1.startswith("validation_"))
        self.assertEqual(len(key1), 23)  # "validation_" + 12 char hash
    
    def test_generate_cache_key_different_inputs(self):
        """Test that different inputs produce different cache keys."""
        base_framework = "# Test Framework"
        base_experiment = "# Test Experiment"
        base_corpus = "# Test Corpus"
        base_model = "vertex_ai/gemini-2.5-pro"
        
        key1 = self.cache_manager.generate_cache_key(
            base_framework, base_experiment, base_corpus, base_model
        )
        key2 = self.cache_manager.generate_cache_key(
            base_framework + " modified", base_experiment, base_corpus, base_model
        )
        key3 = self.cache_manager.generate_cache_key(
            base_framework, base_experiment, base_corpus, "vertex_ai/gemini-2.5-flash"
        )
        
        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)
    
    def test_check_cache_miss(self):
        """Test cache miss scenario."""
        cache_key = "validation_test123"
        
        result = self.cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_validation)
        self.assertIsNone(result.artifact_hash)
    
    def test_check_cache_hit(self):
        """Test cache hit scenario."""
        cache_key = "validation_test123"
        artifact_hash = "artifact_hash_456"
        
        # Mock validation result
        validation_data = {
            "success": True,
            "issues": [],
            "model": "vertex_ai/gemini-2.5-pro",
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Set up mock registry
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "validation_result",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact retrieval
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(validation_data).encode('utf-8')
        
        result = self.cache_manager.check_cache(cache_key)
        
        self.assertTrue(result.hit)
        self.assertEqual(result.artifact_hash, artifact_hash)
        self.assertEqual(result.cached_validation, validation_data)
        
        # Verify audit logging
        self.mock_audit_logger.log_agent_event.assert_called_once_with(
            "V2ValidationAgent", "cache_hit", {
                "cache_key": cache_key,
                "cached_artifact_hash": artifact_hash,
                "phase": "validation"
            }
        )
    
    def test_store_validation_result(self):
        """Test storing validation result in cache."""
        cache_key = "validation_test123"
        validation_result = {
            "success": True,
            "issues": [],
            "model": "vertex_ai/gemini-2.5-pro",
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
        model = "vertex_ai/gemini-2.5-pro"
        
        # Mock artifact storage
        expected_hash = "stored_artifact_hash"
        self.mock_artifact_storage.put_artifact.return_value = expected_hash
        
        result_hash = self.cache_manager.store_validation_result(cache_key, validation_result, model)
        
        self.assertEqual(result_hash, expected_hash)
        
        # Verify artifact was stored with correct metadata
        self.mock_artifact_storage.put_artifact.assert_called_once()
        call_args = self.mock_artifact_storage.put_artifact.call_args
        stored_content = call_args[0][0]
        stored_metadata = call_args[0][1]
        
        # Verify content
        stored_validation = json.loads(stored_content.decode('utf-8'))
        self.assertEqual(stored_validation, validation_result)
        
        # Verify metadata
        self.assertEqual(stored_metadata["artifact_type"], "validation_result")
        self.assertEqual(stored_metadata["cache_key"], cache_key)
        self.assertEqual(stored_metadata["validation_model"], model)
        self.assertEqual(stored_metadata["success"], True)
        self.assertIn("cached_at", stored_metadata)
        
        # Verify audit logging
        self.mock_audit_logger.log_agent_event.assert_called_once_with(
            "V2ValidationAgent", "cache_store", {
                "cache_key": cache_key,
                "artifact_hash": expected_hash,
                "validation_success": True,
                "phase": "validation"
            }
        )
    
    def test_cache_hit_with_failed_validation(self):
        """Test cache hit with a previously failed validation."""
        cache_key = "validation_test123"
        artifact_hash = "artifact_hash_456"
        
        # Mock failed validation result
        validation_data = {
            "success": False,
            "issues": ["Framework validation failed", "Corpus issues found"],
            "model": "vertex_ai/gemini-2.5-pro",
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Set up mock registry
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "validation_result",
                    "cache_key": cache_key
                }
            }
        }
        
        # Mock artifact retrieval
        self.mock_artifact_storage.get_artifact.return_value = json.dumps(validation_data).encode('utf-8')
        
        result = self.cache_manager.check_cache(cache_key)
        
        self.assertTrue(result.hit)
        self.assertEqual(result.cached_validation["success"], False)
        self.assertEqual(len(result.cached_validation["issues"]), 2)


if __name__ == '__main__':
    unittest.main()
