#!/usr/bin/env python3
"""
Unit Tests for the LocalArtifactStorage.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary


class TestLocalArtifactStorage(unittest.TestCase):
    """Test suite for the LocalArtifactStorage."""

    def setUp(self):
        """Set up a temporary directory for artifacts."""
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / "experiment.md").touch()
        self.run_folder = self.test_dir / "runs" / "test_run"
        self.run_folder.mkdir(parents=True, exist_ok=True)
        
        self.security_boundary = ExperimentSecurityBoundary(self.test_dir)
        self.storage = LocalArtifactStorage(
            self.security_boundary, run_folder=self.run_folder
        )

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_put_and_get_directory_artifact(self):
        """
        Verify that the storage can handle a directory as an artifact.
        """
        # 1. Create a source directory with some content
        source_dir = Path(tempfile.mkdtemp())
        (source_dir / "file1.txt").write_text("hello")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "file2.txt").write_text("world")

        # 2. Store the directory as an artifact
        # This method does not exist yet and will cause a failure.
        dir_hash = self.storage.put_directory_artifact(
            source_dir, {"artifact_type": "rag_index"}
        )
        self.assertIsNotNone(dir_hash)

        # 3. Retrieve the path to the stored directory
        # This method also does not exist yet.
        retrieved_dir_path = self.storage.get_directory_artifact_path(dir_hash)
        self.assertTrue(retrieved_dir_path.is_dir())

        # 4. Verify the contents of the retrieved directory
        self.assertTrue((retrieved_dir_path / "file1.txt").exists())
        self.assertEqual((retrieved_dir_path / "file1.txt").read_text(), "hello")
        self.assertTrue((retrieved_dir_path / "subdir" / "file2.txt").exists())
        self.assertEqual((retrieved_dir_path / "subdir" / "file2.txt").read_text(), "world")

        # 5. Clean up the source directory
        shutil.rmtree(source_dir)


if __name__ == '__main__':
    unittest.main()
