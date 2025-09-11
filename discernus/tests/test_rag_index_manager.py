#!/usr/bin/env python3
"""
Unit Tests for the RAGIndexManager.

Follows the Test-Driven Development (TDD) methodology.
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
        rag_manager = RAGIndexManager(artifact_storage=self.artifact_storage)
        rag_index = rag_manager.build_index_from_documents(sample_docs)

        # 3. Assert that the index was created and contains the correct number of items
        self.assertIsNotNone(rag_index)
        self.assertEqual(rag_index.count(), 3)

        # 4. Perform a search and verify the result structure
        search_results = rag_index.search("wisdom", 1)
        self.assertEqual(len(search_results), 1)
        
        # 5. Assert that the content is returned directly in the search result
        result_dict = search_results[0]
        self.assertIn("id", result_dict)
        self.assertIn("text", result_dict)
        self.assertIn("score", result_dict)
        self.assertEqual(result_dict["text"], "Brevity is the soul of wit.")


if __name__ == '__main__':
    unittest.main()
