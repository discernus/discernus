#!/usr/bin/env python3
"""
Unit tests for RAG Index Cache Manager

Tests the caching functionality for txtai RAG indexes to ensure
proper cache key generation, storage, and retrieval.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from pathlib import Path
import json

# Import the class under test
from discernus.core.rag_index_cache import RAGIndexCacheManager, RAGCacheResult


class TestRAGIndexCacheManager(unittest.TestCase):
    """Test cases for RAG Index Cache Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_artifact_storage = Mock()
        self.mock_audit_logger = Mock()
        
        # Mock artifact storage registry
        self.mock_artifact_storage.registry = {}
        
        # Initialize cache manager
        self.cache_manager = RAGIndexCacheManager(
            self.mock_artifact_storage,
            self.mock_audit_logger
        )
    
    def test_generate_cache_key_deterministic(self):
        """Test that cache key generation is deterministic."""
        evidence_hashes = ["hash1", "hash2", "hash3"]
        
        # Generate key multiple times
        key1 = self.cache_manager.generate_cache_key(evidence_hashes)
        key2 = self.cache_manager.generate_cache_key(evidence_hashes)
        
        # Should be identical
        self.assertEqual(key1, key2)
        self.assertTrue(key1.startswith("rag_index_"))
        self.assertEqual(len(key1), 26)  # "rag_index_" + 16 char hash
    
    def test_generate_cache_key_different_inputs(self):
        """Test that different inputs generate different cache keys."""
        evidence_hashes1 = ["hash1", "hash2", "hash3"]
        evidence_hashes2 = ["hash1", "hash2", "hash4"]
        
        key1 = self.cache_manager.generate_cache_key(evidence_hashes1)
        key2 = self.cache_manager.generate_cache_key(evidence_hashes2)
        
        # Should be different
        self.assertNotEqual(key1, key2)
    
    def test_generate_cache_key_order_independent(self):
        """Test that cache key is independent of hash order."""
        evidence_hashes1 = ["hash1", "hash2", "hash3"]
        evidence_hashes2 = ["hash3", "hash1", "hash2"]
        
        key1 = self.cache_manager.generate_cache_key(evidence_hashes1)
        key2 = self.cache_manager.generate_cache_key(evidence_hashes2)
        
        # Should be identical (order independent)
        self.assertEqual(key1, key2)
    
    def test_generate_cache_key_empty_list(self):
        """Test cache key generation with empty evidence list."""
        key = self.cache_manager.generate_cache_key([])
        self.assertEqual(key, "rag_index_empty")
    
    def test_check_cache_miss(self):
        """Test cache miss scenario."""
        cache_key = "rag_index_test123"
        
        # Empty registry = cache miss
        result = self.cache_manager.check_cache(cache_key)
        
        self.assertFalse(result.hit)
        self.assertIsNone(result.cached_index)
        self.assertEqual(result.cache_key, cache_key)
    
    def test_check_cache_hit(self):
        """Test cache hit scenario."""
        cache_key = "rag_index_test123"
        artifact_hash = "artifact_hash_123"
        
        # Mock registry with cached index
        self.mock_artifact_storage.registry = {
            artifact_hash: {
                "metadata": {
                    "artifact_type": "rag_index_cache",
                    "rag_cache_key": cache_key
                }
            }
        }
        
        # Mock successful index loading
        mock_index = Mock()
        with patch.object(self.cache_manager, '_load_index_from_artifact', return_value=mock_index):
            result = self.cache_manager.check_cache(cache_key)
        
        self.assertTrue(result.hit)
        self.assertEqual(result.cached_index, mock_index)
        self.assertEqual(result.cache_key, cache_key)
        self.assertEqual(result.artifact_hash, artifact_hash)
    
    def test_store_index_with_directory_handling(self):
        """Test storing RAG index with proper directory handling."""
        cache_key = "rag_index_test123"
        evidence_count = 5
        
        # Mock txtai index
        mock_index = Mock()
        
        # Use real temporary directory for this test
        import tempfile
        import tarfile
        
        with tempfile.TemporaryDirectory() as real_temp_dir:
            temp_path = Path(real_temp_dir)
            
            # Mock mkdtemp to return our controlled temp directory
            with patch('discernus.core.rag_index_cache.tempfile.mkdtemp', return_value=str(temp_path)):
                # Create a fake index directory that txtai.save would create
                index_dir = temp_path / "rag_index"
                index_dir.mkdir()
                (index_dir / "config").write_text('{"test": "config"}')
                (index_dir / "embeddings").write_bytes(b'fake_embeddings')
                
                # Mock the index.save to create our fake directory
                def mock_save(path):
                    # The directory already exists from our setup above
                    pass
                mock_index.save = mock_save
                
                # Mock artifact storage
                self.mock_artifact_storage.put_artifact.return_value = "stored_hash_123"
                
                # Store index
                result_hash = self.cache_manager.store_index(cache_key, mock_index, evidence_count)
        
        # Verify artifact was stored
        self.mock_artifact_storage.put_artifact.assert_called_once()
        call_args = self.mock_artifact_storage.put_artifact.call_args
        stored_data, stored_metadata = call_args[0]
        
        # Verify the stored data is a valid tar.gz file
        self.assertTrue(len(stored_data) > 0)
        
        # Verify it's actually a gzip file by checking magic number
        self.assertTrue(stored_data.startswith(b'\x1f\x8b'))  # gzip magic number
        
        # Verify metadata
        self.assertEqual(stored_metadata["artifact_type"], "rag_index_cache")
        self.assertEqual(stored_metadata["rag_cache_key"], cache_key)
        self.assertEqual(stored_metadata["evidence_count"], evidence_count)
        
        self.assertEqual(result_hash, "stored_hash_123")
    
    def test_load_index_from_artifact_with_tar_handling(self):
        """Test loading RAG index from artifact with proper tar.gz handling."""
        artifact_hash = "artifact_hash_123"
        
        # Create a real tar.gz file with fake txtai index structure
        import tempfile
        import tarfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create fake txtai index directory
            index_dir = temp_path / "rag_index"
            index_dir.mkdir()
            (index_dir / "config").write_text('{"test": "config"}')
            (index_dir / "embeddings").write_bytes(b'fake_embeddings')
            
            # Create tar.gz file
            tar_path = temp_path / "test_index.tar.gz"
            with tarfile.open(tar_path, 'w:gz') as tar:
                tar.add(index_dir, arcname='rag_index')
            
            # Read the tar.gz data
            mock_index_data = tar_path.read_bytes()
        
        # Mock artifact retrieval
        self.mock_artifact_storage.get_artifact.return_value = mock_index_data
        
        # Mock txtai Embeddings to avoid loading actual models
        mock_embeddings = Mock()
        with patch('discernus.core.rag_index_cache.Embeddings', return_value=mock_embeddings):
            result = self.cache_manager._load_index_from_artifact(artifact_hash)
        
        # Verify artifact was retrieved
        self.mock_artifact_storage.get_artifact.assert_called_once_with(artifact_hash)
        
        # Verify embeddings was loaded with correct path
        mock_embeddings.load.assert_called_once()
        load_path = mock_embeddings.load.call_args[0][0]
        self.assertTrue(load_path.endswith('rag_index'))
        
        self.assertEqual(result, mock_embeddings)
    
    def test_load_index_from_artifact_failure(self):
        """Test handling of index loading failure."""
        artifact_hash = "artifact_hash_123"
        
        # Mock artifact retrieval failure
        self.mock_artifact_storage.get_artifact.side_effect = Exception("Storage error")
        
        result = self.cache_manager._load_index_from_artifact(artifact_hash)
        
        self.assertIsNone(result)
        self.mock_audit_logger.log_error.assert_called_once()
    
    def test_get_cache_stats(self):
        """Test cache statistics generation."""
        # Mock registry with cached indexes
        self.mock_artifact_storage.registry = {
            "hash1": {
                "metadata": {
                    "artifact_type": "rag_index_cache",
                    "rag_cache_key": "rag_index_abc123",
                    "evidence_count": 5,
                    "created_at": "2025-01-23T10:00:00Z",
                    "index_size_bytes": 1024
                }
            },
            "hash2": {
                "metadata": {
                    "artifact_type": "rag_index_cache",
                    "rag_cache_key": "rag_index_def456",
                    "evidence_count": 10,
                    "created_at": "2025-01-23T11:00:00Z",
                    "index_size_bytes": 2048
                }
            },
            "hash3": {
                "metadata": {
                    "artifact_type": "other_artifact"
                }
            }
        }
        
        stats = self.cache_manager.get_cache_stats()
        
        self.assertEqual(stats["total_cached_indexes"], 2)
        self.assertEqual(stats["total_cache_size_bytes"], 3072)
        self.assertEqual(len(stats["cache_keys"]), 2)
        
        # Check first cache entry
        cache_entry = stats["cache_keys"][0]
        self.assertEqual(cache_entry["cache_key"], "rag_index_abc123")
        self.assertEqual(cache_entry["evidence_count"], 5)
        self.assertEqual(cache_entry["size_bytes"], 1024)


if __name__ == '__main__':
    unittest.main()
