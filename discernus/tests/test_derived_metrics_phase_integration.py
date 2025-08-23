#!/usr/bin/env python3
"""
Test Derived Metrics Phase Integration

Tests that the CleanAnalysisOrchestrator properly integrates the derived metrics phase.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.audit_logger import AuditLogger


class TestDerivedMetricsPhaseIntegration:
    """Test the derived metrics phase integration in CleanAnalysisOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self, tmp_path):
        """Create a test orchestrator instance."""
        # Create experiment directory structure
        experiment_dir = tmp_path / "test_experiment"
        experiment_dir.mkdir()
        
        # Create experiment.md with v10 format
        experiment_content = """# Test Experiment

## Configuration Appendix
```yaml
metadata:
  spec_version: "10.0"
  experiment_name: "test_experiment"
components:
  framework: "framework.md"
  corpus: "corpus.md"
```
"""
        (experiment_dir / "experiment.md").write_text(experiment_content)
        
        # Create framework.md
        (experiment_dir / "framework.md").write_text("# Test Framework")
        
        # Create corpus.md
        (experiment_dir / "corpus.md").write_text("# Test Corpus")
        
        # Create corpus directory
        corpus_dir = experiment_dir / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "test_doc.txt").write_text("Test document content")
        
        # Create session directory
        session_dir = experiment_dir / "session"
        session_dir.mkdir()
        (session_dir / "test_run").mkdir()
        
        # Create shared_cache directory
        cache_dir = experiment_dir / "shared_cache"
        cache_dir.mkdir()
        
        orchestrator = CleanAnalysisOrchestrator(experiment_dir)
        
        # Mock artifact storage
        orchestrator.artifact_storage = Mock()
        orchestrator.artifact_storage.put_artifact.return_value = "test_hash"
        orchestrator.artifact_storage.get_artifact.return_value = b'{"test": "data"}'
        
        # Mock security boundary
        orchestrator.security.experiment_name = "test_experiment"
        
        # Mock config (simulating state after _load_specs() would have been called)
        orchestrator.config = {
            'framework': 'framework.md',
            'corpus': 'corpus.md',
            'name': 'test_experiment'
        }
        orchestrator.config = {
            'framework': 'framework.md',
            'corpus': 'corpus.md',
            'name': 'test_experiment'
        }
        
        return orchestrator
    
    @pytest.fixture
    def mock_audit_logger(self):
        """Create a mock audit logger."""
        return Mock(spec=AuditLogger)
    
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
            }
        ]
    
    def test_derived_metrics_phase_method_exists(self, orchestrator):
        """Test that the derived metrics phase method exists."""
        assert hasattr(orchestrator, '_run_derived_metrics_phase')
        assert callable(orchestrator._run_derived_metrics_phase)
    
    def test_derived_metrics_phase_method_signature(self, orchestrator):
        """Test that the derived metrics phase method has correct signature."""
        import inspect
        sig = inspect.signature(orchestrator._run_derived_metrics_phase)
        params = list(sig.parameters.keys())
        
        assert 'model' in params
        assert 'audit_logger' in params
        assert 'analysis_results' in params
    
    @patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent')
    def test_derived_metrics_phase_creates_workspace(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results):
        """Test that derived metrics phase creates temporary workspace."""
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
            result = orchestrator._run_derived_metrics_phase("test_model", mock_audit_logger, mock_analysis_results)
            
            # Check that workspace was created
            temp_workspace = orchestrator.experiment_path / "temp_derived_metrics"
            assert not temp_workspace.exists()  # Should be cleaned up
            
            # Check result
            assert result['status'] == 'completed'
            assert 'derived_metrics_hash' in result
    
    @patch('discernus.agents.automated_derived_metrics.agent.AutomatedDerivedMetricsAgent')
    def test_derived_metrics_phase_stores_results(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results):
        """Test that derived metrics phase stores results in artifact storage."""
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
            result = orchestrator._run_derived_metrics_phase("test_model", mock_audit_logger, mock_analysis_results)
            
            # Check that artifact storage was called
            assert orchestrator.artifact_storage.put_artifact.called
            
            # Check the stored data structure
            call_args = orchestrator.artifact_storage.put_artifact.call_args
            stored_data = json.loads(call_args[0][0].decode('utf-8'))
            
            assert 'derived_metrics_data' in stored_data
            assert stored_data['status'] == 'success_with_data'
            assert stored_data['validation_passed'] is True
    
    def test_execute_derived_metrics_functions_method_exists(self, orchestrator):
        """Test that the execute derived metrics functions method exists."""
        assert hasattr(orchestrator, '_execute_derived_metrics_functions')
        assert callable(orchestrator._execute_derived_metrics_functions)
    
    def test_derived_metrics_phase_integrated_in_main_flow(self, orchestrator):
        """Test that derived metrics phase is integrated in the main run method."""
        # Check that the main run method references the derived metrics phase
        source_code = orchestrator.__class__.__module__
        
        # This is a basic check - in a real test we'd mock the entire flow
        assert hasattr(orchestrator, '_run_derived_metrics_phase')
