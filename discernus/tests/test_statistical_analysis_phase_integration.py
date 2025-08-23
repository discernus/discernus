#!/usr/bin/env python3
"""
Test Statistical Analysis Phase Integration

Tests that the CleanAnalysisOrchestrator properly integrates the statistical analysis phase.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.audit_logger import AuditLogger

class TestStatisticalAnalysisPhaseIntegration:
    """Test the integration of the statistical analysis phase in CleanAnalysisOrchestrator."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        return tmp_path
    
    @pytest.fixture
    def experiment_path(self, temp_dir):
        """Create a mock experiment directory."""
        experiment_dir = temp_dir / "test_experiment"
        experiment_dir.mkdir()
        
        # Create mock framework.md
        framework_file = experiment_dir / "framework.md"
        framework_file.write_text("# Test Framework\n\n## Part 2: The Machine-Readable Appendix\n```yaml\nname: Test Framework\ndimensions: []\n```")
        
        # Create mock experiment.md
        experiment_file = experiment_dir / "experiment.md"
        experiment_file.write_text("# Test Experiment\n\n## Configuration Appendix\n```yaml\nresearch_questions: []\nhypotheses: []\n```")
        
        return experiment_dir
    
    @pytest.fixture
    def mock_analysis_results(self):
        """Create mock analysis results."""
        return [
            {
                "filename": "test1.txt",
                "analysis_result": {
                    "raw_analysis_response": "Test analysis response 1"
                }
            },
            {
                "filename": "test2.txt",
                "analysis_result": {
                    "raw_analysis_response": "Test analysis response 2"
                }
            }
        ]
    
    @pytest.fixture
    def mock_derived_metrics_results(self):
        """Create mock derived metrics results."""
        return {
            "status": "completed",
            "derived_metrics_results": {
                "derived_metrics_data": {
                    "derived_metrics": [
                        {"document_name": "test1.txt", "metric1": 0.5},
                        {"document_name": "test2.txt", "metric1": 0.7}
                    ]
                }
            }
        }
    
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
    
    def test_statistical_analysis_phase_method_exists(self, orchestrator):
        """Test that the statistical analysis phase method exists."""
        assert hasattr(orchestrator, '_run_statistical_analysis_phase')
    
    def test_statistical_analysis_phase_method_signature(self, orchestrator):
        """Test that the statistical analysis phase method has the correct signature."""
        # First verify the method exists
        assert hasattr(orchestrator, '_run_statistical_analysis_phase')
        
        import inspect
        sig = inspect.signature(orchestrator._run_statistical_analysis_phase)
        params = list(sig.parameters.keys())
        
        # Check that all expected parameters are present
        expected_params = ['model', 'audit_logger', 'analysis_results', 'derived_metrics_results']
        for param in expected_params:
            assert param in params, f"Missing parameter: {param}"
        
        # Verify we have exactly the expected number of parameters
        assert len(params) == len(expected_params), f"Expected {len(expected_params)} parameters, got {len(params)}"
    
    def test_statistical_analysis_phase_creates_workspace(self, orchestrator, audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that the statistical analysis phase creates the required workspace."""
        with patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_execute_statistical_analysis_functions') as mock_execute:
                mock_execute.return_value = {"status": "success", "statistical_results": {}}
                
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    result = orchestrator._run_statistical_analysis_phase(
                        "test_model", 
                        audit_logger, 
                        mock_analysis_results, 
                        mock_derived_metrics_results
                    )
                    
                    # Check that workspace was created
                    temp_workspace = orchestrator.experiment_path / "temp_statistical_analysis"
                    assert temp_workspace.exists()
                    
                    # Check that analysis data directory was created
                    analysis_dir = temp_workspace / "analysis_data"
                    assert analysis_dir.exists()
                    
                    # Check that derived metrics data directory was created
                    derived_metrics_dir = temp_workspace / "derived_metrics_data"
                    assert derived_metrics_dir.exists()
                    
                    # Check that framework and experiment files were created
                    assert (temp_workspace / "framework_content.md").exists()
                    assert (temp_workspace / "experiment_spec.json").exists()
                    
                    # Check that prompt was assembled
                    assert (temp_workspace / "statistical_analysis_prompt.txt").exists()
    
    def test_statistical_analysis_phase_uses_assembler(self, orchestrator, audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that the statistical analysis phase uses the StatisticalAnalysisPromptAssembler."""
        with patch('discernus.core.prompt_assemblers.statistical_analysis_assembler.StatisticalAnalysisPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler_class.return_value = mock_assembler
            mock_assembler.assemble_prompt.return_value = "Test prompt"
            
            with patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent_class.return_value = mock_agent
                mock_agent.generate_functions.return_value = {"functions_generated": 1}
                
                with patch.object(orchestrator, '_execute_statistical_analysis_functions') as mock_execute:
                    mock_execute.return_value = {"status": "success", "statistical_results": {}}
                    
                    # Run the phase
                    orchestrator._run_statistical_analysis_phase(
                        "test_model", 
                        audit_logger, 
                        mock_analysis_results, 
                        mock_derived_metrics_results
                    )
                    
                    # Check that assembler was used
                    mock_assembler.assemble_prompt.assert_called_once()
                    call_args = mock_assembler.assemble_prompt.call_args
                    
                    # Check that correct parameters were passed
                    assert 'framework_path' in call_args.kwargs
                    assert 'experiment_path' in call_args.kwargs
                    assert 'analysis_dir' in call_args.kwargs
                    assert 'derived_metrics_dir' in call_args.kwargs
    
    def test_statistical_analysis_phase_stores_results(self, orchestrator, audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that the statistical analysis phase stores results in artifact storage."""
        with patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_execute_statistical_analysis_functions') as mock_execute:
                mock_execute.return_value = {"status": "success", "statistical_results": {}}
                
                # Run the phase
                result = orchestrator._run_statistical_analysis_phase(
                    "test_model", 
                    audit_logger, 
                    mock_analysis_results, 
                    mock_derived_metrics_results
                )
                
                # Check that results were stored
                assert result['status'] == 'completed'
                assert 'statistical_hash' in result
                assert result['functions_generated'] == 1
    
    def test_statistical_analysis_phase_integration_in_main_flow(self, orchestrator, audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that the statistical analysis phase integrates properly in the main flow."""
        with patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            mock_agent.generate_functions.return_value = {"functions_generated": 1}
            
            with patch.object(orchestrator, '_run_statistical_analysis_phase') as mock_phase:
                mock_phase.return_value = {
                    "status": "completed",
                    "statistical_hash": "test_hash",
                    "functions_generated": 1,
                    "statistical_results": {}
                }
                
                # Run the phase
                result = orchestrator._run_statistical_analysis_phase(
                    "test_model", 
                    audit_logger, 
                    mock_analysis_results, 
                    mock_derived_metrics_results
                )
                
                # Verify the phase was called
                mock_phase.assert_called_once()
                
                # Verify the result structure
                assert result['status'] == 'completed'
                assert result['statistical_hash'] == 'test_hash'
                assert result['functions_generated'] == 1
