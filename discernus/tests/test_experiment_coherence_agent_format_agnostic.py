#!/usr/bin/env python3
"""
Test ExperimentCoherenceAgent format-agnostic validation.

Tests for CLI-003: Fix coherence agent validation gap
"""

import pytest
import tempfile
from pathlib import Path
from discernus.agents.experiment_coherence_agent.agent import ExperimentCoherenceAgent


class TestExperimentCoherenceAgentFormatAgnostic:
    """Test format-agnostic validation in ExperimentCoherenceAgent."""

    def test_validate_v10_delimited_format(self):
        """Test validation of v10 experiment with delimited machine-readable appendix."""
        experiment_content = """# Test CAF Experiment

## Abstract
This tests the delimited format used by CAF experiment.

## Research Questions
- Does the coherence agent handle delimited format?

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_caf_format"
  author: "Test Author"
  spec_version: "10.0"

components:
  framework: "framework.md"
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---"""

        framework_content = """# Test Framework v10.0

This is a test framework.

---

## Part 2: The Machine-Readable Appendix

```yaml
metadata:
  framework_name: "test_framework"
  spec_version: "10.0"
```"""

        corpus_content = """# Test Corpus

Test corpus description.

## Document Manifest

```yaml
name: "Test Corpus"
version: "8.0"
total_documents: 1
documents:
  - filename: "test_doc.txt"
    speaker: "Test Speaker"
```"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            
            # Create files
            (experiment_path / "experiment.md").write_text(experiment_content)
            (experiment_path / "framework.md").write_text(framework_content)
            (experiment_path / "corpus.md").write_text(corpus_content)
            (experiment_path / "corpus").mkdir()
            (experiment_path / "corpus" / "test_doc.txt").write_text("Test document content")

            # Test that agent can load files without parsing errors
            agent = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-flash")
            
            # Should not raise parsing errors
            experiment_spec = agent._load_artifact(experiment_path, "experiment.md")
            framework_spec = agent._find_and_load_framework(experiment_path)
            corpus_manifest = agent._find_and_load_corpus(experiment_path)
            current_specs = agent._load_current_specifications()
            
            assert "test_caf_format" in experiment_spec
            assert "Test Framework v10.0" in framework_spec
            assert "Test Corpus" in corpus_manifest
            assert "EXPERIMENT_SPECIFICATION.md" in current_specs

    def test_validate_v10_appendix_format(self):
        """Test validation of v10 experiment with Configuration Appendix format."""
        experiment_content = """# Test Simple Experiment

## Abstract
This tests the appendix format used by simple_test experiments.

---

## Configuration Appendix
```yaml
metadata:
  experiment_name: "test_simple_format"
  author: "Test Author"
  spec_version: "10.0"

components:
  framework: "framework.md"
  corpus: "corpus.md"
```"""

        framework_content = """# Test Framework v10.0

This is a test framework.

---

## Part 2: The Machine-Readable Appendix

```yaml
metadata:
  framework_name: "test_framework"
  spec_version: "10.0"
```"""

        corpus_content = """# Test Corpus

Test corpus description.

## Document Manifest

```yaml
name: "Test Corpus"
version: "8.0"
total_documents: 1
documents:
  - filename: "test_doc.txt"
    speaker: "Test Speaker"
```"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            
            # Create files
            (experiment_path / "experiment.md").write_text(experiment_content)
            (experiment_path / "framework.md").write_text(framework_content)
            (experiment_path / "corpus.md").write_text(corpus_content)
            (experiment_path / "corpus").mkdir()
            (experiment_path / "corpus" / "test_doc.txt").write_text("Test document content")

            # Test that agent can load files without parsing errors
            agent = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-flash")
            
            # Should not raise parsing errors
            experiment_spec = agent._load_artifact(experiment_path, "experiment.md")
            framework_spec = agent._find_and_load_framework(experiment_path)
            corpus_manifest = agent._find_and_load_corpus(experiment_path)
            current_specs = agent._load_current_specifications()
            
            assert "test_simple_format" in experiment_spec
            assert "Test Framework v10.0" in framework_spec
            assert "Test Corpus" in corpus_manifest
            assert "EXPERIMENT_SPECIFICATION.md" in current_specs

    def test_missing_framework_file(self):
        """Test error handling when framework file is missing."""
        experiment_content = """# Test Experiment

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_missing_framework"
  spec_version: "10.0"

components:
  framework: "missing_framework.md"
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            (experiment_path / "experiment.md").write_text(experiment_content)

            agent = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-flash")
            
            with pytest.raises(ValueError) as exc_info:
                agent._find_and_load_framework(experiment_path)
            
            assert "No framework file found" in str(exc_info.value)

    def test_missing_corpus_file(self):
        """Test error handling when corpus file is missing."""
        experiment_content = """# Test Experiment

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_missing_corpus"
  spec_version: "10.0"

components:
  framework: "framework.md"
  corpus: "missing_corpus.md"

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            (experiment_path / "experiment.md").write_text(experiment_content)
            (experiment_path / "framework.md").write_text("# Test Framework")

            agent = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-flash")
            
            with pytest.raises(ValueError) as exc_info:
                agent._find_and_load_corpus(experiment_path)
            
            assert "No corpus manifest found" in str(exc_info.value)
