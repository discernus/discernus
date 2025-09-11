#!/usr/bin/env python3
"""
Test CleanAnalysisOrchestrator v10 parsing functionality.

Tests for CLI-001: Fix CleanAnalysisOrchestrator v10 Parsing
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


import pytest
import tempfile
from pathlib import Path
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError


class TestCleanAnalysisOrchestratorV10Parsing:
    """Test v10 experiment parsing in CleanAnalysisOrchestrator."""

    def test_parse_v10_machine_readable_appendix_delimited_format(self):
        """Test parsing v10 experiment with delimited machine-readable appendix."""
        v10_experiment_content = """# Test Experiment

## Abstract
This is a test experiment for v10 parsing.

## Research Questions
- Can we parse v10 experiments correctly?

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_v10_experiment"
  author: "Test Author"
  spec_version: "10.0"

components:
  framework: "test_framework.md"
  corpus: "test_corpus.md"

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(v10_experiment_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            config = orchestrator._load_specs()

            # Verify parsed configuration
            assert config['metadata']['experiment_name'] == "test_v10_experiment"
            assert config['metadata']['author'] == "Test Author"
            assert config['metadata']['spec_version'] == "10.0"
            assert config['components']['framework'] == "test_framework.md"
            assert config['components']['corpus'] == "test_corpus.md"

    def test_parse_v10_configuration_appendix_format(self):
        """Test parsing v10 experiment with Configuration Appendix format."""
        v10_experiment_content = """# Test Experiment

## Abstract
This is a test experiment for v10 parsing.

## Research Questions
- Can we parse v10 experiments correctly?

---

## Configuration Appendix
```yaml
metadata:
  experiment_name: "test_config_appendix"
  author: "Test Author"
  spec_version: "10.0"

components:
  framework: "test_framework.md"
  corpus: "test_corpus.md"
```"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(v10_experiment_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            config = orchestrator._load_specs()

            # Verify parsed configuration
            assert config['metadata']['experiment_name'] == "test_config_appendix"
            assert config['metadata']['author'] == "Test Author"
            assert config['metadata']['spec_version'] == "10.0"
            assert config['components']['framework'] == "test_framework.md"
            assert config['components']['corpus'] == "test_corpus.md"

    def test_reject_v7_frontmatter_format(self):
        """Test that v7.3 frontmatter format is rejected with clear error."""
        v7_experiment_content = """---
name: "old_experiment"
framework: "old_framework.md"
corpus: "old_corpus.md"
---

# Old Format Experiment

This uses the old v7.3 frontmatter format."""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(v7_experiment_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            
            with pytest.raises(CleanAnalysisError) as exc_info:
                orchestrator._load_specs()
            
            assert "v10.0 machine-readable appendix" in str(exc_info.value)
            assert "v7.3 frontmatter" in str(exc_info.value)

    def test_missing_experiment_file(self):
        """Test error handling when experiment.md doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            
            # The SecurityBoundary will catch this before the orchestrator can
            from discernus.core.security_boundary import SecurityError
            
            with pytest.raises(SecurityError) as exc_info:
                orchestrator = CleanAnalysisOrchestrator(experiment_path)
            
            assert "missing experiment.md" in str(exc_info.value)

    def test_invalid_yaml_in_appendix(self):
        """Test error handling for invalid YAML in appendix."""
        invalid_yaml_content = """# Test Experiment

## Abstract
This has invalid YAML.

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_invalid_yaml"
  invalid_yaml: [unclosed_list
  spec_version: "10.0"

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(invalid_yaml_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            
            with pytest.raises(CleanAnalysisError) as exc_info:
                orchestrator._load_specs()
            
            assert "Failed to parse experiment.md YAML" in str(exc_info.value)

    def test_missing_required_fields(self):
        """Test error handling for missing required fields."""
        missing_fields_content = """# Test Experiment

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_missing_fields"
  # Missing spec_version

components:
  # Missing framework and corpus

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(missing_fields_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            
            with pytest.raises(CleanAnalysisError) as exc_info:
                orchestrator._load_specs()
            
            # Should catch missing required fields
            assert "required field" in str(exc_info.value).lower() or "missing" in str(exc_info.value).lower()

    def test_non_v10_spec_version(self):
        """Test rejection of non-v10 spec versions."""
        old_version_content = """# Test Experiment

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_old_version"
  author: "Test Author"
  spec_version: "8.0"

components:
  framework: "test_framework.md"
  corpus: "test_corpus.md"

# --- End of Machine-Readable Appendix ---"""

        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = Path(temp_dir)
            experiment_file = experiment_path / "experiment.md"
            experiment_file.write_text(old_version_content, encoding='utf-8')

            orchestrator = CleanAnalysisOrchestrator(experiment_path)
            
            with pytest.raises(CleanAnalysisError) as exc_info:
                orchestrator._load_specs()
            
            assert "v10.0" in str(exc_info.value)
            assert "8.0" in str(exc_info.value)
