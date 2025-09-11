#!/usr/bin/env python3
"""
Unit tests for SynthesisPromptAssembler
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


import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from discernus.core.prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler


class TestSynthesisPromptAssembler:
    """Test suite for SynthesisPromptAssembler"""
    
    def test_assemble_prompt_successfully(self):
        """Test that the assembler creates a comprehensive synthesis prompt."""
        
        # Mock framework content
        framework_content = """# Test Framework v10.0

## Part 1: The Scholarly Document

### Section 1: Abstract & Raison d'être
This framework analyzes test dimensions for research purposes.

## Part 2: The Machine-Readable Appendix

```yaml
metadata:
  framework_name: "test_framework"
  framework_version: "10.0.0"

dimensions:
  - { name: "dimension1", description: "Test dimension 1" }
  - { name: "dimension2", description: "Test dimension 2" }
```"""

        # Mock experiment content
        experiment_content = """# Test Experiment

## Research Objectives
This experiment tests the framework on sample data.

## Configuration Appendix

```yaml
metadata:
  experiment_name: "test_experiment"
  spec_version: "10.0"

hypotheses:
  - name: "Test Hypothesis"
    description: "Framework will capture meaningful variance"
```"""

        # Mock research data
        research_data = {
            "experiment_metadata": {"name": "test_experiment"},
            "statistical_results": {
                "descriptive_statistics": {"mean": 0.5, "std": 0.2},
                "correlations": {"dim1_dim2": 0.3}
            }
        }

        # Mock evidence data
        evidence_data = {
            "evidence_data": [
                {"dimension": "dimension1", "quote_text": "Test quote 1"},
                {"dimension": "dimension2", "quote_text": "Test quote 2"}
            ]
        }

        # Mock artifact storage
        mock_storage = Mock()
        mock_storage.get_artifact.side_effect = [
            json.dumps(research_data).encode('utf-8'),  # research data
            json.dumps(evidence_data).encode('utf-8')   # evidence data
        ]

        # Mock file system
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = [framework_content, experiment_content]
            
            # Create assembler and test
            assembler = SynthesisPromptAssembler()
            
            prompt = assembler.assemble_prompt(
                framework_path=Path("test_framework.md"),
                experiment_path=Path("test_experiment.md"),
                research_data_artifact_hash="test_hash",
                artifact_storage=mock_storage,
                evidence_artifacts=["evidence_hash1"]
            )
            
            # Validate prompt content
            assert "You are an expert research analyst" in prompt
            assert "Test Framework v10.0" in prompt
            assert "Test Hypothesis" in prompt
            assert "2 pieces of textual evidence" in prompt
            assert "STATISTICAL ANALYSIS RESULTS:" in prompt
            assert "## Executive Summary" in prompt
            assert "## Results" in prompt
            assert "## Conclusion" in prompt
            
            # Verify storage calls
            assert mock_storage.get_artifact.call_count == 2
