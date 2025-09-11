#!/usr/bin/env python3
"""
Test enhanced basic validation with file existence checks.

Tests for enhanced Stage 1 validation (Approach 2)
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
import tempfile
from pathlib import Path
from discernus.cli import validate_experiment_structure


class TestEnhancedBasicValidation:
    """Test enhanced Stage 1 validation with file existence checks."""

    def create_valid_v10_experiment(self, temp_dir: Path) -> Path:
        """Create a valid v10 experiment for testing."""
        experiment_path = temp_dir / "test_experiment"
        experiment_path.mkdir()
        
        # Create v10 experiment.md
        experiment_content = """# Test Experiment

## Abstract
This is a valid test experiment.

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_validation"
  author: "Test Author"
  spec_version: "10.0"

components:
  framework: "framework.md"
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---"""

        # Create framework.md
        framework_content = """# Test Framework v10.0

## Part 1: The Scholarly Document

### Section 1: Abstract & Raison d'être
This is a test framework.

---

## Part 2: The Machine-Readable Appendix

```yaml
metadata:
  framework_name: "test_framework"
  spec_version: "10.0"
```"""

        # Create corpus.md
        corpus_content = """# Test Corpus

Test corpus description.

## Document Manifest

```yaml
name: "Test Corpus"
version: "8.0"
total_documents: 2
documents:
  - document_id: "doc1"
    filename: "document1.txt"
    speaker: "Speaker 1"
  - document_id: "doc2"
    filename: "document2.txt"
    speaker: "Speaker 2"
```"""

        # Write files
        (experiment_path / "experiment.md").write_text(experiment_content)
        (experiment_path / "framework.md").write_text(framework_content)
        (experiment_path / "corpus.md").write_text(corpus_content)
        
        # Create corpus directory and files
        corpus_dir = experiment_path / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "document1.txt").write_text("Content of document 1")
        (corpus_dir / "document2.txt").write_text("Content of document 2")
        
        return experiment_path

    def test_valid_experiment_passes_enhanced_validation(self):
        """Test that a valid experiment passes enhanced validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is True
            assert "✅" in message
            assert config["name"] == "test_validation"

    def test_missing_framework_file_detected(self):
        """Test detection of missing framework file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Remove framework file
            (experiment_path / "framework.md").unlink()
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "framework.md" in message.lower()
            assert "not found" in message.lower() or "missing" in message.lower()

    def test_missing_corpus_file_detected(self):
        """Test detection of missing corpus manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Remove corpus manifest
            (experiment_path / "corpus.md").unlink()
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "corpus.md" in message.lower()
            assert "not found" in message.lower() or "missing" in message.lower()

    def test_missing_corpus_document_detected(self):
        """Test detection of missing corpus documents referenced in manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Remove one corpus document
            (experiment_path / "corpus" / "document1.txt").unlink()
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "document1.txt" in message
            assert "corpus" in message.lower()

    def test_wrong_framework_reference_detected(self):
        """Test detection of wrong framework filename in experiment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Change experiment to reference wrong framework file
            experiment_file = experiment_path / "experiment.md"
            content = experiment_file.read_text()
            content = content.replace('framework: "framework.md"', 'framework: "nonexistent.md"')
            experiment_file.write_text(content)
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "nonexistent.md" in message
            assert "framework" in message.lower()

    def test_wrong_corpus_reference_detected(self):
        """Test detection of wrong corpus filename in experiment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Change experiment to reference wrong corpus file
            experiment_file = experiment_path / "experiment.md"
            content = experiment_file.read_text()
            content = content.replace('corpus: "corpus.md"', 'corpus: "missing_corpus.md"')
            experiment_file.write_text(content)
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "missing_corpus.md" in message
            assert "corpus" in message.lower()

    def test_corpus_count_mismatch_detected(self):
        """Test detection of corpus document count mismatch."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_valid_v10_experiment(Path(temp_dir))
            
            # Change corpus manifest to wrong count
            corpus_file = experiment_path / "corpus.md"
            content = corpus_file.read_text()
            content = content.replace('total_documents: 2', 'total_documents: 5')
            corpus_file.write_text(content)
            
            valid, message, config = validate_experiment_structure(experiment_path)
            
            assert valid is False
            assert "total_documents" in message or "count" in message.lower()
            assert "mismatch" in message.lower() or "inconsistent" in message.lower()
