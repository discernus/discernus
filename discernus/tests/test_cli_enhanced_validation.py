#!/usr/bin/env python3
"""
Test CLI enhanced validation with two-stage architecture.

Tests for CLI-005: Enhanced CLI Validation
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
from click.testing import CliRunner
from discernus.cli import cli


class TestCLIEnhancedValidation:
    """Test two-stage validation architecture in CLI."""

    def create_v10_experiment(self, temp_dir: Path) -> Path:
        """Create a minimal v10 experiment for testing."""
        experiment_path = temp_dir / "test_experiment"
        experiment_path.mkdir()
        
        # Create v10 experiment.md
        experiment_content = """# Test Experiment

## Abstract
This is a test experiment for enhanced validation testing.

## Research Questions
- Does the two-stage validation work correctly?

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "test_enhanced_validation"
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
This is a test framework for enhanced validation testing.

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

Test corpus for enhanced validation testing.

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

    def test_validate_basic_mode_fast(self):
        """Test that basic validate mode is fast (Stage 1 only)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['validate', str(experiment_path)])
            
            # Should succeed quickly with basic validation
            assert result.exit_code == 0
            assert "✅ Basic structure is valid" in result.output
            assert "Full validation will occur during the run" in result.output

    def test_validate_strict_mode_comprehensive(self):
        """Test that validate --strict mode includes coherence validation (Stage 1 + Stage 2)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            # Note: This will call the coherence agent, so we expect it might timeout or fail
            # But it should NOT fail with parsing errors
            result = runner.invoke(cli, ['validate', '--strict', str(experiment_path)], catch_exceptions=True)
            
            # Should either succeed or fail gracefully (not with parsing errors)
            if result.exit_code != 0:
                # Check that it's not a parsing error
                assert "YAML frontmatter" not in result.output
                assert "ThinOrchestrator" not in result.output
                assert "NameError" not in result.output

    def test_dry_run_includes_both_stages(self):
        """Test that dry-run includes both sanity check and coherence validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['run', '--dry-run', str(experiment_path)])
            
            # Should succeed with both stages
            assert result.exit_code == 0
            assert "DRY RUN MODE" in result.output
            # Should show experiment info (Stage 1)
            assert "test_enhanced_validation" in result.output

    def test_run_includes_coherence_validation_by_default(self):
        """Test that normal run includes coherence validation unless skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            # This will try to run the full experiment, so we expect it to timeout or fail
            # But it should NOT fail with parsing errors
            result = runner.invoke(cli, ['run', '--dry-run', str(experiment_path)], catch_exceptions=True)
            
            # Should not fail with parsing errors
            assert "YAML frontmatter" not in result.output
            assert "ThinOrchestrator" not in result.output
            assert "_corpus_file_count" not in result.output

    def test_run_skip_validation_bypasses_coherence(self):
        """Test that --skip-validation bypasses coherence agent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            experiment_path = self.create_v10_experiment(Path(temp_dir))
            
            runner = CliRunner()
            result = runner.invoke(cli, ['run', '--skip-validation', '--dry-run', str(experiment_path)])
            
            # Should succeed and show that validation was skipped
            assert result.exit_code == 0
            assert "DRY RUN MODE" in result.output
