#!/usr/bin/env python3
"""
Unit Tests for the RAGIndexManager.

Follows the Test-Driven Development (TDD) methodology.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

# This import will fail initially, which is expected in TDD.
from discernus.core.rag_index_manager import RAGIndexManager
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary


class TestRAGIndexManager(unittest.TestCase):
    """Test suite for the RAGIndexManager."""

    def setUp(self):
        """Set up a temporary directory for artifacts."""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # The security boundary requires an experiment.md file to exist.
        (self.test_dir / "experiment.md").touch()
        
        # The artifact storage requires a run folder to exist.
        self.run_folder = self.test_dir / "runs" / "test_run"
        self.run_folder.mkdir(parents=True, exist_ok=True)
        
        # Correctly instantiate the security boundary with only the path.
        self.security_boundary = ExperimentSecurityBoundary(self.test_dir)
        self.artifact_storage = LocalArtifactStorage(
            self.security_boundary, run_folder=self.run_folder
        )

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_build_index_and_retrieve_content(self):
        """
        Verify that the manager can build an index and that content is stored and retrievable.
        This is the core functionality test.
        """
        # 1. Define sample documents
        sample_docs = [
            {"id": "doc1", "content": "The quick brown fox jumps over the lazy dog."},
            {"id": "doc2", "content": "A journey of a thousand miles begins with a single step."},
            {"id": "doc3", "content": "Brevity is the soul of wit."},
        ]

        # 2. Instantiate the manager and build the index
        from discernus.core.audit_logger import AuditLogger
        audit_logger = AuditLogger(
            security_boundary=self.security_boundary,
            run_folder=self.run_folder
        )
        rag_manager = RAGIndexManager(
            storage=self.artifact_storage,
            audit=audit_logger,
            security=self.security_boundary
        )

        # 3. Calculate expected cache key
        cache_key = rag_manager.get_corpus_cache_key(sample_docs)

        # 4. Build the index
        rag_manager.build_index_from_corpus(sample_docs, cache_key)

        # 5. Assert that the index was created and contains the correct number of items
        self.assertIsNotNone(rag_manager.embeddings)
        self.assertEqual(rag_manager.embeddings.count(), 3)

        # 6. Perform a search and verify the result structure
        search_results = rag_manager.search("wisdom", 1)
        self.assertEqual(len(search_results), 1)

        # 7. Assert that the content is returned directly in the search result
        result_dict = search_results[0]
        self.assertIn("id", result_dict)
        self.assertIn("text", result_dict)
        self.assertIn("score", result_dict)
        self.assertEqual(result_dict["text"], "Brevity is the soul of wit.")

    def test_deterministic_index_building(self):
        """
        Test that the same corpus documents always produce the same cache key.
        This ensures deterministic behavior.
        """
        # 1. Define identical sample documents (same content, different order)
        sample_docs_1 = [
            {"id": "doc1", "content": "The quick brown fox jumps over the lazy dog."},
            {"id": "doc2", "content": "A journey of a thousand miles begins with a single step."},
            {"id": "doc3", "content": "Brevity is the soul of wit."},
        ]

        sample_docs_2 = [
            {"id": "doc3", "content": "Brevity is the soul of wit."},  # Different order
            {"id": "doc1", "content": "The quick brown fox jumps over the lazy dog."},
            {"id": "doc2", "content": "A journey of a thousand miles begins with a single step."},
        ]

        # 2. Instantiate the manager
        from discernus.core.audit_logger import AuditLogger
        audit_logger = AuditLogger(
            security_boundary=self.security_boundary,
            run_folder=self.run_folder
        )
        rag_manager = RAGIndexManager(
            storage=self.artifact_storage,
            audit=audit_logger,
            security=self.security_boundary
        )

        # 3. Calculate cache keys - should be identical despite different ordering
        cache_key_1 = rag_manager.get_corpus_cache_key(sample_docs_1)
        cache_key_2 = rag_manager.get_corpus_cache_key(sample_docs_2)

        # 4. Assert that cache keys are identical (deterministic)
        self.assertEqual(cache_key_1, cache_key_2,
                        "Cache keys should be identical for same content regardless of document order")


if __name__ == '__main__':
    unittest.main()
