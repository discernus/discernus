"""
Unit tests for SynthesisPromptAssembler functionality.

This test module focuses on testing the prompt assembly logic in isolation
to verify it can build rich, context-filled prompts from various data sources.
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
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import json
import yaml

from discernus.core.prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
from discernus.core.local_artifact_storage import LocalArtifactStorage


class TestSynthesisPromptAssembler:
    """Test the SynthesisPromptAssembler functionality."""
    
    @pytest.fixture
    def assembler(self):
        """Create assembler instance for testing."""
        return SynthesisPromptAssembler()
    
    @pytest.fixture
    def mock_artifact_storage(self):
        """Mock artifact storage for testing."""
        storage = Mock(spec=LocalArtifactStorage)
        
        # Mock research data
        research_data = {
            "experiment_metadata": {"name": "test_experiment", "framework": "test_framework"},
            "raw_analysis_data": [{"score1": 0.8, "document_name": "doc1.txt"}],
            "derived_metrics_data": [{"aggregate_score": 0.85}],
            "statistical_results": {"means": {"score1": 0.8}, "std_devs": {"score1": 0.1}}
        }
        storage.get_artifact.return_value = json.dumps(research_data).encode('utf-8')
        
        return storage
    
    @pytest.fixture
    def sample_framework_content(self):
        """Sample framework content for testing."""
        return """# Civic Character Framework

## Part 1: The Scholarly Document

This framework analyzes civic character in political discourse...

### Theoretical Foundation

Democratic values and civic engagement are fundamental...

## Part 2: The Machine-Readable Appendix

```yaml
name: "Civic Character Framework"
version: "10.0"
dimensions:
  - name: "democratic_values"
    description: "Commitment to democratic principles"
  - name: "civic_engagement" 
    description: "Active participation in civic life"
```"""
    
    @pytest.fixture
    def sample_experiment_content(self):
        """Sample experiment content for testing."""
        return """# Civic Character Study

This experiment examines civic character in political discourse...

## Research Questions

1. How do political leaders demonstrate civic character?
2. What patterns emerge in civic engagement?

## Configuration Appendix

```yaml
name: "Civic Character Study"
framework: "framework.md"
corpus: "corpus.md"
hypotheses:
  - "Political leaders show varying levels of civic character"
  - "Civic engagement correlates with democratic values"
```"""
    
    def test_assembler_accepts_correct_parameters(self, assembler, mock_artifact_storage):
        """Test that assemble_prompt accepts the correct parameters."""
        # Test the method signature
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        research_data_hash = "hash123"
        evidence_artifacts = ["evidence1", "evidence2"]
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            # This should not raise an exception
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_hash,
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=evidence_artifacts
            )
            
            # Should return a string
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_assembler_reads_and_parses_framework_content(self, assembler, mock_artifact_storage, sample_framework_content):
        """Test that assembler reads and parses framework content correctly."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading to return sample content
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = [sample_framework_content, "# Experiment"]
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should contain framework content
            assert "Civic Character Framework" in result
            assert "democratic_values" in result or "Democratic values" in result
    
    def test_assembler_reads_and_parses_experiment_content(self, assembler, mock_artifact_storage, sample_experiment_content):
        """Test that assembler reads and parses experiment content correctly."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading to return sample content
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = ["# Framework", sample_experiment_content]
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should contain experiment content
            assert "Civic Character Study" in result
            assert "Research Questions" in result or "research question" in result.lower()
    
    def test_assembler_loads_research_data_from_artifact(self, assembler, mock_artifact_storage):
        """Test that assembler loads research data from artifact storage."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        research_data_hash = "research_hash_123"
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_hash,
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should have called get_artifact with the research data hash
            mock_artifact_storage.get_artifact.assert_called_with(research_data_hash)
            
            # Should contain statistical information
            assert "statistical" in result.lower() or "mean" in result.lower()
    
    def test_assembler_produces_properly_formatted_prompt(self, assembler, mock_artifact_storage):
        """Test that assembler produces a properly formatted prompt."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=["evidence1", "evidence2"]
            )
            
            # Should be substantial content
            assert len(result) > 100
            
            # Should be properly formatted text
            assert isinstance(result, str)
            
            # Should contain key sections (based on current assembler implementation)
            # Note: This tests the current assembler, not the intended new interface
            result_lower = result.lower()
            assert any(keyword in result_lower for keyword in [
                "experiment", "framework", "analysis", "synthesis", "report"
            ])
    
    def test_assembler_handles_missing_or_malformed_data_gracefully(self, assembler):
        """Test that assembler handles missing or malformed data gracefully."""
        framework_path = Path("nonexistent_framework.md")
        experiment_path = Path("nonexistent_experiment.md")
        
        # Mock artifact storage that returns invalid data
        mock_storage = Mock(spec=LocalArtifactStorage)
        mock_storage.get_artifact.return_value = b"invalid json data"
        
        # Mock file reading to raise FileNotFoundError
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = FileNotFoundError("File not found")
            
            # Should handle errors gracefully (not crash)
            try:
                result = assembler.assemble_prompt(
                    framework_path=framework_path,
                    experiment_path=experiment_path,
                    research_data_artifact_hash="hash123",
                    artifact_storage=mock_storage,
                    evidence_artifacts=[]
                )
                # If it doesn't crash, it should still return a string
                assert isinstance(result, str)
            except Exception as e:
                # If it does raise an exception, it should be a reasonable one
                assert isinstance(e, (FileNotFoundError, json.JSONDecodeError, KeyError))
    
    def test_assembler_includes_evidence_context_information(self, assembler, mock_artifact_storage):
        """Test that assembler includes evidence context information."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        evidence_artifacts = ["evidence1", "evidence2", "evidence3"]
        
        # Mock evidence data
        mock_artifact_storage.get_artifact.side_effect = [
            # First call for research data
            json.dumps({"statistical_results": {"means": {"score": 0.8}}}).encode(),
            # Subsequent calls for evidence data
            json.dumps(["quote1", "quote2"]).encode(),
            json.dumps(["quote3", "quote4", "quote5"]).encode(),
            json.dumps(["quote6"]).encode()
        ]
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=evidence_artifacts
            )
            
            # Should mention evidence availability
            result_lower = result.lower()
            assert any(keyword in result_lower for keyword in [
                "evidence", "quote", "textual", "pieces"
            ])
    
    def test_assembler_loads_external_yaml_prompt_template(self, assembler):
        """Test that assembler loads external YAML prompt template."""
        # The assembler should load a YAML template on initialization
        assert hasattr(assembler, 'prompt_template')
        assert assembler.prompt_template is not None
        
        # Should be a dictionary (parsed YAML)
        assert isinstance(assembler.prompt_template, dict)
        
        # Should have a template key (based on current implementation)
        assert 'template' in assembler.prompt_template
    
    def test_assembler_handles_template_variable_substitution(self, assembler, mock_artifact_storage):
        """Test that assembler handles template variable substitution."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should not contain template variables (like {experiment_metadata})
            assert "{experiment_metadata}" not in result
            assert "{framework_content}" not in result
            assert "{research_data}" not in result
    
    def test_assembler_creates_statistical_summary(self, assembler, mock_artifact_storage):
        """Test that assembler creates statistical summary from research data."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock research data with statistical results
        research_data = {
            "statistical_results": {
                "means": {"score1": 0.85, "score2": 0.72},
                "std_devs": {"score1": 0.12, "score2": 0.08},
                "counts": {"total_documents": 10}
            }
        }
        mock_artifact_storage.get_artifact.return_value = json.dumps(research_data).encode()
        
        # Mock file reading
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.return_value = "# Test Content"
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should contain statistical information
            result_lower = result.lower()
            assert any(keyword in result_lower for keyword in [
                "0.85", "0.72", "mean", "statistical", "score"
            ])
    
    def test_assembler_error_handling_for_missing_template(self):
        """Test that assembler handles missing template file gracefully."""
        # Mock the template file to not exist
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            # Should raise FileNotFoundError when template is missing
            with pytest.raises(FileNotFoundError):
                SynthesisPromptAssembler()
    
    def test_assembler_parses_yaml_from_framework_appendix(self, assembler, mock_artifact_storage, sample_framework_content):
        """Test that assembler correctly parses YAML from framework appendix."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading to return framework with YAML appendix
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = [sample_framework_content, "# Experiment"]
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should contain information from the YAML (framework name or dimensions)
            assert "Civic Character Framework" in result or "democratic_values" in result
    
    def test_assembler_parses_yaml_from_experiment_appendix(self, assembler, mock_artifact_storage, sample_experiment_content):
        """Test that assembler correctly parses YAML from experiment appendix."""
        framework_path = Path("framework.md")
        experiment_path = Path("experiment.md")
        
        # Mock file reading to return experiment with YAML appendix
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = ["# Framework", sample_experiment_content]
            
            result = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash="hash123",
                artifact_storage=mock_artifact_storage,
                evidence_artifacts=[]
            )
            
            # Should contain information from the experiment YAML
            assert "Civic Character Study" in result or "hypotheses" in result.lower()
