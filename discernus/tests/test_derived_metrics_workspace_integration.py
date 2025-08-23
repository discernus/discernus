import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
import tempfile
import shutil

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator


class TestDerivedMetricsWorkspaceIntegration:
    """Test that the derived metrics phase properly creates workspace files for provenance."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def experiment_path(self, temp_dir):
        """Create a test experiment directory structure."""
        experiment_path = temp_dir / "test_experiment"
        experiment_path.mkdir()
        
        # Create framework.md
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
    calculation: "score / max_possible_score"
```
"""
        (experiment_path / "framework.md").write_text(framework_content)
        
        # Create experiment.md
        experiment_content = """# Test Experiment

This is a test experiment for derived metrics workspace integration.
"""
        (experiment_path / "experiment.md").write_text(experiment_content)
        
        return experiment_path
    
    @pytest.fixture
    def mock_analysis_results(self):
        """Create mock analysis results."""
        return [
            {
                'analysis_result': {
                    'result_content': {'score': 0.8},
                    'raw_analysis_response': 'Score: 0.8'
                },
                'scores_hash': 'score_hash_1',
                'evidence_hash': 'evidence_hash_1',
                'document_id': 'doc_1',
                'filename': 'test_doc.txt'
            },
            {
                'analysis_result': {
                    'result_content': {'score': 0.9},
                    'raw_analysis_response': 'Score: 0.9'
                },
                'scores_hash': 'score_hash_2',
                'evidence_hash': 'evidence_hash_2',
                'document_id': 'doc_2',
                'filename': 'test_doc2.txt'
            }
        ]
    
    @pytest.fixture
    def orchestrator(self, experiment_path):
        """Create orchestrator instance with mocked dependencies."""
        orchestrator = CleanAnalysisOrchestrator(experiment_path)
        
        # Mock artifact storage
        orchestrator.artifact_storage = Mock()
        orchestrator.artifact_storage.put_artifact.return_value = "test_hash"
        
        # Mock audit logger
        orchestrator.audit_logger = Mock()
        
        # Set config
        orchestrator.config = {'framework': 'framework.md'}
        
        return orchestrator
    
    def test_derived_metrics_phase_creates_required_workspace_files(self, orchestrator, mock_analysis_results):
        """Test that derived metrics phase creates all required workspace files for provenance."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            # Mock the agent
            mock_agent = Mock()
            mock_agent.generate_functions.return_value = {'functions_generated': 1}
            mock_agent_class.return_value = mock_agent
            
            # Mock the execution function
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {
                    'status': 'success',
                    'derived_metrics': [{'score': 0.8, 'derived_score': 0.9}]
                }
                
                # Mock the cleanup to prevent workspace deletion during test
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    result = orchestrator._run_derived_metrics_phase("test_model", orchestrator.audit_logger, mock_analysis_results)
                    
                    # Check that workspace was created with required files
                    temp_workspace = orchestrator.experiment_path / "temp_derived_metrics"
                    
                    # Verify the workspace structure exists during execution
                    assert (temp_workspace / "analysis_data").exists()
                    assert (temp_workspace / "framework_content.md").exists()
                    assert (temp_workspace / "derived_metrics_prompt.txt").exists()
                    
                    # Check that analysis data files were created
                    analysis_dir = temp_workspace / "analysis_data"
                    assert len(list(analysis_dir.glob("*.json"))) == 2  # sample_size=2
                    
                    # Check that framework content was written
                    framework_content = (temp_workspace / "framework_content.md").read_text()
                    assert "Test Framework" in framework_content
                    assert "derived_metrics:" in framework_content
                    
                    # Check result
                    assert result['status'] == 'completed'
                    assert 'derived_metrics_hash' in result
    
    def test_workspace_files_contain_correct_content(self, orchestrator, mock_analysis_results):
        """Test that workspace files contain the expected content for provenance."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            # Mock the agent
            mock_agent = Mock()
            mock_agent.generate_functions.return_value = {'functions_generated': 1}
            mock_agent_class.return_value = mock_agent
            
            # Mock the execution function
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {
                    'status': 'success',
                    'derived_metrics': [{'score': 0.8, 'derived_score': 0.9}]
                }
                
                # Mock the cleanup to prevent workspace deletion during test
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    orchestrator._run_derived_metrics_phase("test_model", orchestrator.audit_logger, mock_analysis_results)
                    
                    # Check workspace content
                    temp_workspace = orchestrator.experiment_path / "temp_derived_metrics"
                    
                    # Verify framework content
                    framework_content = (temp_workspace / "framework_content.md").read_text()
                    assert "Test Framework" in framework_content
                    assert "## Part 2: The Machine-Readable Appendix" in framework_content
                    assert "derived_metrics:" in framework_content
                    
                    # Verify analysis data files
                    analysis_dir = temp_workspace / "analysis_data"
                    analysis_files = list(analysis_dir.glob("*.json"))
                    assert len(analysis_files) == 2
                    
                    # Check first analysis file content
                    first_analysis = json.loads(analysis_files[0].read_text())
                    assert 'analysis_result' in first_analysis
                    assert 'filename' in first_analysis
                    assert first_analysis['filename'] == 'test_doc.txt'
                    
                    # Check second analysis file content
                    second_analysis = json.loads(analysis_files[1].read_text())
                    assert 'analysis_result' in second_analysis
                    assert 'filename' in second_analysis
                    assert second_analysis['filename'] == 'test_doc2.txt'
    
    def test_agent_can_find_required_workspace_files(self, orchestrator, mock_analysis_results):
        """Test that the agent can successfully find and read the workspace files."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            # Mock the agent
            mock_agent = Mock()
            mock_agent.generate_functions.return_value = {'functions_generated': 1}
            mock_agent_class.return_value = mock_agent
            
            # Mock the execution function
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {
                    'status': 'success',
                    'derived_metrics': [{'score': 0.8, 'derived_score': 0.9}]
                }
                
                # Mock the cleanup to prevent workspace deletion during test
                with patch('shutil.rmtree') as mock_rmtree:
                    # Run the phase
                    result = orchestrator._run_derived_metrics_phase("test_model", orchestrator.audit_logger, mock_analysis_results)
                    
                    # Verify the agent was called with the correct workspace path
                    mock_agent.generate_functions.assert_called_once()
                    call_args = mock_agent.generate_functions.call_args
                    workspace_path = call_args[0][0]  # First positional argument
                    
                    # Verify the workspace contains all required files
                    assert (workspace_path / "framework_content.md").exists()
                    assert (workspace_path / "analysis_data").exists()
                    assert (workspace_path / "derived_metrics_prompt.txt").exists()
                    
                    # Verify the agent can read the files
                    framework_content = (workspace_path / "framework_content.md").read_text()
                    assert "Test Framework" in framework_content
                    
                    analysis_dir = workspace_path / "analysis_data"
                    analysis_files = list(analysis_dir.glob("*.json"))
                    assert len(analysis_files) == 2
    
    def test_workspace_cleanup_after_completion(self, orchestrator, mock_analysis_results):
        """Test that workspace is properly cleaned up after completion while preserving artifacts."""
        with patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent') as mock_agent_class:
            # Mock the agent
            mock_agent = Mock()
            mock_agent.generate_functions.return_value = {'functions_generated': 1}
            mock_agent_class.return_value = mock_agent
            
            # Mock the execution function
            with patch.object(orchestrator, '_execute_derived_metrics_functions') as mock_execute:
                mock_execute.return_value = {
                    'status': 'success',
                    'derived_metrics': [{'score': 0.8, 'derived_score': 0.9}]
                }
                
                # Run the phase
                result = orchestrator._run_derived_metrics_phase("test_model", orchestrator.audit_logger, mock_analysis_results)
                
                # Verify workspace was cleaned up
                temp_workspace = orchestrator.experiment_path / "temp_derived_metrics"
                assert not temp_workspace.exists()
                
                # Verify artifacts were stored before cleanup
                assert orchestrator.artifact_storage.put_artifact.called
                
                # Check the stored data structure
                call_args = orchestrator.artifact_storage.put_artifact.call_args
                stored_data = json.loads(call_args[0][0].decode('utf-8'))
                
                assert 'derived_metrics_data' in stored_data
                assert stored_data['status'] == 'success_with_data'
                assert stored_data['validation_passed'] is True
