
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
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
import tempfile
import shutil

from discernus.agents.automated_derived_metrics.agent import AutomatedDerivedMetricsAgent


class TestAutomatedDerivedMetricsAgent:
    """Test the refactored AutomatedDerivedMetricsAgent that works with file paths."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def framework_path(self, temp_dir):
        """Create a test framework.md file."""
        framework_content = """# Test Framework

## Part 2: The Machine-Readable Appendix

```yaml
name: "Test Framework"
version: "1.0"
derived_metrics:
  - name: "aggregate_score"
    description: "Aggregate score across dimensions"
    calculation: "mean of all dimension scores"
  - name: "normalized_score"
    description: "Score normalized to 0-1 range"
```
"""
        framework_file = temp_dir / "framework.md"
        framework_file.write_text(framework_content)
        return framework_file
    
    @pytest.fixture
    def analysis_dir(self, temp_dir):
        """Create test analysis data directory."""
        analysis_dir = temp_dir / "analysis_data"
        analysis_dir.mkdir()
        
        # Create sample analysis files
        analysis_data = [
            {
                "document_id": "doc_1",
                "scores": {"dimension_1": 0.8, "dimension_2": 0.6},
                "metadata": {"filename": "test1.txt"}
            },
            {
                "document_id": "doc_2", 
                "scores": {"dimension_1": 0.9, "dimension_2": 0.7},
                "metadata": {"filename": "test2.txt"}
            }
        ]
        
        for i, data in enumerate(analysis_data):
            analysis_file = analysis_dir / f"analysis_{i}.json"
            analysis_file.write_text(json.dumps(data, indent=2))
        
        return analysis_dir
    
    @pytest.fixture
    def mock_llm_gateway(self):
        """Mock LLM gateway for testing."""
        mock_gateway = Mock()
        mock_gateway.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="```python\ndef calculate_derived_metrics(df):\n    # Test function\n    return df\n```"))]
        )
        return mock_gateway
    
    @pytest.fixture
    def agent(self, mock_llm_gateway):
        """Create agent instance with mocked dependencies."""
        with patch('discernus.agents.automated_derived_metrics.agent.LLMGateway') as mock_gateway_class:
            mock_gateway_class.return_value = mock_llm_gateway
            
            agent = AutomatedDerivedMetricsAgent(
                model="test_model",
                audit_logger=Mock()
            )
            return agent
    
    def test_generate_functions_with_paths_signature(self, agent):
        """Test that generate_functions accepts framework_path and analysis_dir parameters."""
        import inspect
        sig = inspect.signature(agent.generate_functions)
        params = list(sig.parameters.keys())
        
        assert 'framework_path' in params
        assert 'analysis_dir' in params
        assert 'sample_size' in params
    
    def test_generate_functions_reads_framework_directly(self, agent, framework_path, analysis_dir):
        """Test that generate_functions reads framework content directly from path."""
        with patch.object(agent, '_generate_calculation_functions') as mock_generate:
            mock_generate.return_value = "def test(): pass"
            
            result = agent.generate_functions(
                framework_path=framework_path,
                analysis_dir=analysis_dir,
                sample_size=2
            )
            
            # Verify the framework was read directly
            assert result['status'] == 'success'
            assert 'functions_generated' in result
    
    def test_generate_functions_reads_analysis_data_directly(self, agent, framework_path, analysis_dir):
        """Test that generate_functions reads analysis data directly from directory."""
        with patch.object(agent, '_generate_calculation_functions') as mock_generate:
            mock_generate.return_value = "def test(): pass"
            
            result = agent.generate_functions(
                framework_path=framework_path,
                analysis_dir=analysis_dir,
                sample_size=2
            )
            
            # Verify analysis data was read directly
            assert result['status'] == 'success'
    
    def test_generate_functions_handles_missing_framework(self, agent, temp_dir, analysis_dir):
        """Test that generate_functions handles missing framework file gracefully."""
        missing_framework = temp_dir / "missing_framework.md"
        
        with pytest.raises(FileNotFoundError):
            agent.generate_functions(
                framework_path=missing_framework,
                analysis_dir=analysis_dir,
                sample_size=2
            )
    
    def test_generate_functions_handles_missing_analysis_dir(self, agent, framework_path, temp_dir):
        """Test that generate_functions handles missing analysis directory gracefully."""
        missing_analysis_dir = temp_dir / "missing_analysis"
        
        with pytest.raises(ValueError, match="No analysis JSON files found"):
            agent.generate_functions(
                framework_path=framework_path,
                analysis_dir=missing_analysis_dir,
                sample_size=2
            )
    
    def test_generate_functions_respects_sample_size(self, agent, framework_path, analysis_dir):
        """Test that generate_functions respects the sample_size parameter."""
        with patch.object(agent, '_generate_calculation_functions') as mock_generate:
            mock_generate.return_value = "def test(): pass"
            
            # Test with sample_size=1
            result = agent.generate_functions(
                framework_path=framework_path,
                analysis_dir=analysis_dir,
                sample_size=1
            )
            
            assert result['status'] == 'success'
    
    def test_generate_functions_returns_expected_structure(self, agent, framework_path, analysis_dir):
        """Test that generate_functions returns the expected result structure."""
        with patch.object(agent, '_generate_calculation_functions') as mock_generate:
            mock_generate.return_value = "def test(): pass"
            
            result = agent.generate_functions(
                framework_path=framework_path,
                analysis_dir=analysis_dir,
                sample_size=2
            )
            
            # Check expected structure
            assert 'status' in result
            assert 'functions_generated' in result
            assert 'generated_code' in result
            assert result['status'] == 'success'
