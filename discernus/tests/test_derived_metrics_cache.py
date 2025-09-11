#!/usr/bin/env python3
"""
Tests for DerivedMetricsCacheManager.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pytest
import json
from unittest.mock import Mock, MagicMock
from pathlib import Path

from discernus.core.derived_metrics_cache import DerivedMetricsCacheManager, DerivedMetricsCacheResult


class TestDerivedMetricsCacheManager:
    """Test derived metrics caching functionality."""
    
    @pytest.fixture
    def mock_storage(self):
        """Create a mock artifact storage."""
        storage = Mock()
        storage.registry = {}
        storage.put_artifact = Mock(return_value="test_hash_123")
        storage.get_artifact = Mock(return_value=b'{"test": "cached_data"}')
        return storage
    
    @pytest.fixture
    def mock_audit_logger(self):
        """Create a mock audit logger."""
        audit = Mock()
        audit.log_agent_event = Mock()
        return audit
    
    @pytest.fixture
    def cache_manager(self, mock_storage, mock_audit_logger):
        """Create a cache manager instance."""
        return DerivedMetricsCacheManager(mock_storage, mock_audit_logger)
    
    def test_generate_cache_key_deterministic(self, cache_manager):
        """Test that cache key generation is deterministic."""
        framework_content = "# Test Framework\nSome content"
        analysis_results = [
            {"analysis_result": {"test": "data"}, "filename": "doc1.txt"},
            {"analysis_result": {"test": "data2"}, "filename": "doc2.txt"}
        ]
        model = "vertex_ai/gemini-2.5-pro"
        
        # Generate key twice
        key1 = cache_manager.generate_cache_key(framework_content, analysis_results, model)
        key2 = cache_manager.generate_cache_key(framework_content, analysis_results, model)
        
        # Should be identical
        assert key1 == key2
        assert key1.startswith("derived_metrics_")
    
    def test_generate_cache_key_different_inputs(self, cache_manager):
        """Test that different inputs generate different cache keys."""
        framework_content1 = "# Test Framework 1"
        framework_content2 = "# Test Framework 2"
        analysis_results = [{"analysis_result": {"test": "data"}, "filename": "doc1.txt"}]
        model = "vertex_ai/gemini-2.5-pro"
        
        key1 = cache_manager.generate_cache_key(framework_content1, analysis_results, model)
        key2 = cache_manager.generate_cache_key(framework_content2, analysis_results, model)
        
        # Should be different
        assert key1 != key2
    
    def test_check_cache_miss(self, cache_manager, mock_storage):
        """Test cache miss scenario."""
        # Empty registry means no cache hits
        mock_storage.registry = {}
        
        result = cache_manager.check_cache("test_key")
        
        assert result.hit is False
        assert result.artifact_hash is None
        assert result.cached_functions is None
    
    def test_check_cache_hit(self, cache_manager, mock_storage, mock_audit_logger):
        """Test cache hit scenario."""
        # Set up registry with matching cache entry
        test_cache_key = "derived_metrics_abc123"
        test_artifact_hash = "artifact_hash_456"
        
        mock_storage.registry = {
            test_artifact_hash: {
                "metadata": {
                    "artifact_type": "derived_metrics_functions",
                    "cache_key": test_cache_key
                }
            }
        }
        
        # Mock the cached content
        cached_data = {"functions_generated": 3, "status": "success"}
        mock_storage.get_artifact.return_value = json.dumps(cached_data).encode('utf-8')
        
        result = cache_manager.check_cache(test_cache_key)
        
        assert result.hit is True
        assert result.artifact_hash == test_artifact_hash
        assert result.cached_functions == cached_data
        
        # Verify audit logging
        mock_audit_logger.log_agent_event.assert_called_once_with(
            "DerivedMetricsAgent", "cache_hit", {
                "cache_key": test_cache_key,
                "cached_artifact_hash": test_artifact_hash,
                "phase": "derived_metrics"
            }
        )
    
    def test_store_functions(self, cache_manager, mock_storage, mock_audit_logger):
        """Test storing functions in cache."""
        cache_key = "derived_metrics_test123"
        functions_result = {
            "functions_generated": 5,
            "status": "success",
            "model": "vertex_ai/gemini-2.5-pro"
        }
        
        artifact_hash = cache_manager.store_functions(cache_key, functions_result)
        
        # Verify storage was called
        mock_storage.put_artifact.assert_called_once()
        
        # Check the stored content
        call_args = mock_storage.put_artifact.call_args
        stored_content = call_args[0][0]  # First positional argument (content)
        stored_metadata = call_args[0][1]  # Second positional argument (metadata)
        stored_data = json.loads(stored_content.decode('utf-8'))
        
        assert stored_data == functions_result
        assert stored_metadata["artifact_type"] == "derived_metrics_functions"
        assert stored_metadata["cache_key"] == cache_key
        assert stored_metadata["functions_generated"] == 5
        
        # Verify audit logging
        mock_audit_logger.log_agent_event.assert_called_once_with(
            "DerivedMetricsAgent", "cache_store", {
                "cache_key": cache_key,
                "artifact_hash": "test_hash_123",
                "phase": "derived_metrics"
            }
        )
        
        assert artifact_hash == "test_hash_123"
