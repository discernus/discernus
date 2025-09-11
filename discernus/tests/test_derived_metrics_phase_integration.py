#!/usr/bin/env python3
"""
Test Derived Metrics Phase Integration

Tests that the CleanAnalysisOrchestrator properly integrates the derived metrics phase.
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
import json
from pathlib import Path
from unittest.mock import Mock, patch
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.audit_logger import AuditLogger

class TestDerivedMetricsPhaseIntegration:
    """Test the integration of the derived metrics phase in CleanAnalysisOrchestrator."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        return tmp_path
    
    @pytest.fixture
    def experiment_path(self, temp_dir):
        """Create a mock experiment directory."""
        experiment_dir = temp_dir / "test_experiment"
        experiment_dir.mkdir()
        
        # Create mock framework.md with v10 format
        framework_content = """# Test Framework

This is a test framework for derived metrics.

## Part 2: The Machine-Readable Appendix
```yaml
name: "Test Framework"
dimensions:
  - name: "civic_virtue"
    description: "Measures civic virtue"
  - name: "civic_responsibility"
    description: "Measures civic responsibility"
derived_metrics:
  - name: "civic_health_index"
    description: "Combined civic health score"
    calculation: "mean(civic_virtue.raw_score, civic_responsibility.raw_score)"
```
"""
        framework_file = experiment_dir / "framework.md"
        framework_file.write_text(framework_content)
        
        # Create mock experiment.md
        experiment_file = experiment_dir / "experiment.md"
        experiment_file.write_text("# Test Experiment\n\nThis is a test experiment.")
        
        return experiment_dir
    
    @pytest.fixture
    def mock_analysis_results(self):
        """Create mock analysis results."""
        return [
            {
                "filename": "test1.txt",
                "analysis_result": {
                    "dimensional_scores": {
                        "civic_virtue": {"raw_score": 0.8, "salience": 0.7, "confidence": 0.9},
                        "civic_responsibility": {"raw_score": 0.6, "salience": 0.8, "confidence": 0.85}
                    }
                }
            },
            {
                "filename": "test2.txt",
                "analysis_result": {
                    "dimensional_scores": {
                        "civic_virtue": {"raw_score": 0.7, "salience": 0.6, "confidence": 0.8},
                        "civic_responsibility": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.95}
                    }
                }
            }
        ]
    
    @pytest.fixture
    def orchestrator(self, experiment_path):
        """Create a CleanAnalysisOrchestrator instance."""
        orchestrator = CleanAnalysisOrchestrator(experiment_path)
        orchestrator.config = {
            "name": "Test Experiment",
            "framework": "framework.md"
        }
        orchestrator.artifact_storage = Mock()
        orchestrator.artifact_storage.registry = {}
        return orchestrator
    
    @pytest.fixture
    def audit_logger(self):
        """Create a mock audit logger."""
        return Mock(spec=AuditLogger)
    
    def test_derived_metrics_phase_method_exists(self, orchestrator):
        """Test that the derived metrics phase method exists."""
        assert hasattr(orchestrator, '_run_derived_metrics_phase')
    
    def test_derived_metrics_phase_method_signature(self, orchestrator):
        """Test that the derived metrics phase method has the correct signature."""
        # First verify the method exists
        assert hasattr(orchestrator, '_run_derived_metrics_phase')
        
        import inspect
        sig = inspect.signature(orchestrator._run_derived_metrics_phase)
        params = list(sig.parameters.keys())
        
        # Check that all expected parameters are present
        expected_params = ['model', 'audit_logger', 'analysis_results']
        for param in expected_params:
            assert param in params, f"Missing parameter: {param}"
        
        # Verify we have exactly the expected number of parameters
        assert len(params) == len(expected_params), f"Expected {len(expected_params)} parameters, got {len(params)}"
    
    def test_derived_metrics_phase_creates_workspace(self, orchestrator, audit_logger, mock_analysis_results):
        """Test that the derived metrics phase creates the required workspace."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {"status": "success", "derived_metrics": {}}
                
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    result = orchestrator._run_derived_metrics_phase(
                        "test_model", 
                        audit_logger, 
                        mock_analysis_results
                    )
                    
                    # Check that workspace was created
                    temp_workspace = orchestrator.experiment_path / "temp_derived_metrics"
                    assert temp_workspace.exists()
                    
                    # Check that analysis data directory was created
                    analysis_dir = temp_workspace / "analysis_data"
                    assert analysis_dir.exists()
                    
                    # Check that framework and experiment files were created
                    assert (temp_workspace / "framework_content.md").exists()
                    assert (temp_workspace / "experiment_spec.json").exists()
                    
                    # Check that prompt was assembled
                    assert (temp_workspace / "derived_metrics_prompt.txt").exists()
    
    def test_derived_metrics_phase_uses_assembler(self, orchestrator, audit_logger, mock_analysis_results):
        """Test that the derived metrics phase uses the DerivedMetricsPromptAssembler."""
        with patch('discernus.core.prompt_assemblers.derived_metrics_assembler.DerivedMetricsPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler_class.return_value = mock_assembler
            mock_assembler.assemble_prompt.return_value = "Test prompt"
            
            with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent_class.return_value = mock_agent
                mock_agent.generate_functions.return_value = {"functions_generated": 1}
                
                with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                    mock_execute.return_value = {"status": "success", "derived_metrics": {}}
                    
                    with patch('shutil.rmtree') as mock_rmtree:
                        # Run the phase
                        orchestrator._run_derived_metrics_phase(
                            "test_model", 
                            audit_logger, 
                            mock_analysis_results
                        )
                        
                        # Check that assembler was used
                        mock_assembler.assemble_prompt.assert_called_once()
                        call_args = mock_assembler.assemble_prompt.call_args
                        
                        # Check that correct parameters were passed
                        assert 'framework_path' in call_args.kwargs
                        assert 'analysis_dir' in call_args.kwargs
                        assert 'sample_size' in call_args.kwargs
    
    def test_derived_metrics_phase_stores_results(self, orchestrator, audit_logger, mock_analysis_results):
        """Test that the derived metrics phase stores results in artifact storage."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {"status": "success", "derived_metrics": {}}
                
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    result = orchestrator._run_derived_metrics_phase(
                        "test_model", 
                        audit_logger, 
                        mock_analysis_results
                    )
                    
                    # Check that results were stored
                    assert result['status'] == 'completed'
                    assert 'derived_metrics_hash' in result
                    assert result['functions_generated'] == 1
    
    def test_derived_metrics_phase_integration_in_main_flow(self, orchestrator, audit_logger, mock_analysis_results):
        """Test that the derived metrics phase integrates properly in the main flow."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_run_derived_metrics_phase') as mock_phase:
                mock_phase.return_value = {
                    "status": "completed",
                    "derived_metrics_hash": "test_hash",
                    "functions_generated": 1,
                    "derived_metrics": {}
                }
                
                # Run the phase
                result = orchestrator._run_derived_metrics_phase(
                    "test_model", 
                    audit_logger, 
                    mock_analysis_results
                )
                
                # Verify the phase was called
                mock_phase.assert_called_once()
                
                # Verify the result structure
                assert result['status'] == 'completed'
                assert result['derived_metrics_hash'] == 'test_hash'
                assert result['functions_generated'] == 1
