#!/usr/bin/env python3
"""
Test CLI commands with v10 experiments.

Tests for CLI-004: Fix Broken CLI Commands
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
from click.testing import CliRunner
from discernus.cli import cli


class TestCLICommandsV10:
    """Test CLI commands with v10 experiment format."""

    def create_v10_experiment(self, temp_dir: Path) -> Path:
        """Create a minimal v10 experiment for testing."""
        experiment_path = temp_dir / "test_experiment"
        experiment_path.mkdir()
        
        # Create v10 experiment.md
        experiment_content = """# Test Experiment

## Abstract
This is a test experiment for CLI testing.

## Research Questions
- Can CLI commands handle v10 experiments?

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_cli_experiment"
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
This is a test framework for CLI testing.

---

## Part 2: The Machine-Readable Appendix

```yaml
metadata:
  framework_name: "test_framework"
  spec_version: "10.0"

analysis_variants:
  default:
    analysis_prompt: "Test analysis prompt"
    
output_schema:
  type: "object"
  properties:
    test_score:
      type: "number"
      minimum: 0.0
      maximum: 1.0
```"""

        # Create corpus.md
        corpus_content = """# Test Corpus

Test corpus for CLI testing.

## Document Manifest

```yaml
name: "Test Corpus"
version: "8.0"
total_documents: 1
documents:
  - filename: "test_doc.txt"
    speaker: "Test Speaker"
```"""

        # Write files
        (experiment_path / "experiment.md").write_text(experiment_content)
        (experiment_path / "framework.md").write_text(framework_content)
        (experiment_path / "corpus.md").write_text(corpus_content)
        
        # Create corpus directory and file
        corpus_dir = experiment_path / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "test_doc.txt").write_text("Test document content for analysis.")
        
        return experiment_path

    def test_validate_command_with_v10_experiment(self):
        """Test that validate command works with v10 experiments."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['validate', str(experiment_path)])
            
            # Should succeed (exit code 0)
            assert result.exit_code == 0
            assert "✅ Basic structure is valid" in result.output

    def test_validate_dry_run_with_v10_experiment(self):
        """Test that validate --dry-run works with v10 experiments."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['validate', '--dry-run', str(experiment_path)])
            
            # Should succeed (exit code 0)
            assert result.exit_code == 0
            assert "[DRY RUN]" in result.output

    def test_run_dry_run_with_v10_experiment(self):
        """Test that run --dry-run works with v10 experiments."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['run', '--dry-run', str(experiment_path)])
            
            # Should succeed without the _corpus_file_count error
            assert result.exit_code == 0
            assert "DRY RUN MODE" in result.output

    def test_debug_command_with_v10_experiment(self):
        """Test that debug command works with v10 experiments (should not reference ThinOrchestrator)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            # Use a very short timeout since debug might try to call LLM
            result = runner.invoke(cli, ['debug', str(experiment_path)], catch_exceptions=True)
            
            # Should not fail with ThinOrchestrator error
            assert "ThinOrchestrator" not in str(result.output)
            assert "NameError: name 'ThinOrchestrator' is not defined" not in str(result.output)
            
            # May fail for other reasons (LLM calls, etc.) but not import errors
            if result.exit_code != 0:
                # Check that it's not an import error
                assert "NameError" not in str(result.output)
                assert "not defined" not in str(result.output)

    def test_list_command_works(self):
        """Test that list command works (baseline functionality)."""
        runner = CliRunner()
        result = runner.invoke(cli, ['list'])
        
        # Should succeed
        assert result.exit_code == 0

    def test_status_command_works(self):
        """Test that status command works (baseline functionality)."""
        runner = CliRunner()
        result = runner.invoke(cli, ['status'])
        
        # Should succeed
        assert result.exit_code == 0
        assert "System Status" in result.output
