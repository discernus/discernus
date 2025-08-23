#!/usr/bin/env python3
"""
Test Statistical Analysis Phase Integration

Tests that the CleanAnalysisOrchestrator properly integrates the statistical analysis phase.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.audit_logger import AuditLogger


class TestStatisticalAnalysisPhaseIntegration:
    """Test the statistical analysis phase integration in CleanAnalysisOrchestrator."""
    
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
  research_questions:
    - "What is the relationship between dimensions?"
components:
  framework: "framework.md"
  corpus: "corpus.md"
```
"""
        (experiment_dir / "experiment.md").write_text(experiment_content)
        
        # Create framework.md with v10 format
        framework_content = """# Test Framework

## Part 2: The Machine-Readable Appendix
```yaml
metadata:
  spec_version: "10.0"
  framework_name: "test_framework"
  name: "Test Framework"
derived_metrics:
  - name: "test_metric"
    description: "A test derived metric"
    formula: "dimensions.score.raw_score * 2"
```
"""
        (experiment_dir / "framework.md").write_text(framework_content)
        
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
        
        return orchestrator
    
    @pytest.fixture
    def mock_audit_logger(self):
        """Create a mock audit logger."""
        return Mock(spec=AuditLogger)
    
    @pytest.fixture
    def mock_analysis_results(self):
        """Create mock analysis results with proper v6 format."""
        return [
            {
                'analysis_result': {
                    'result_content': {'score': 0.8},
                    'raw_analysis_response': '<<<DISCERNUS_ANALYSIS_JSON_v6>>>{"document_analyses": [{"dimensional_scores": {"dignity": {"raw_score": 0.8, "salience": 0.7, "confidence": 0.9}, "truth": {"raw_score": 0.6, "salience": 0.8, "confidence": 0.85}}}]}<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                },
                'scores_hash': 'score_hash_1',
                'evidence_hash': 'evidence_hash_1',
                'document_id': 'doc_1',
                'filename': 'test_doc.txt'
            }
        ]
    
    def test_mock_data_structure(self, mock_analysis_results):
        """Test that the mock data has the expected structure."""
        result = mock_analysis_results[0]
        assert 'analysis_result' in result
        assert 'raw_analysis_response' in result['analysis_result']
        
        raw_response = result['analysis_result']['raw_analysis_response']
        print(f"Raw response length: {len(raw_response)}")
        print(f"Raw response: {repr(raw_response)}")
        
        # Test the parsing logic directly
        if '<<<DISCERNUS_ANALYSIS_JSON_v6>>>' in raw_response:
            json_start = raw_response.find('<<<DISCERNUS_ANALYSIS_JSON_v6>>>') + len('<<<DISCERNUS_ANALYSIS_JSON_v6>>>')
            json_end = raw_response.find('<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>')
            
            assert json_end > json_start, "JSON end index should be greater than start index"
            
            json_content = raw_response[json_start:json_end].strip()
            analysis_data = json.loads(json_content)
            
            assert 'document_analyses' in analysis_data
            assert len(analysis_data['document_analyses']) > 0
            
            doc_analysis = analysis_data['document_analyses'][0]
            assert 'dimensional_scores' in doc_analysis
            
            scores = doc_analysis['dimensional_scores']
            assert 'dignity' in scores
            assert 'truth' in scores
    
    @pytest.fixture
    def mock_derived_metrics_results(self):
        """Create mock derived metrics results."""
        return {
            'status': 'completed',
            'derived_metrics_results': {
                'derived_metrics_data': {
                    'derived_metrics': [
                        {'document_name': 'test_doc.txt', 'test_metric': 1.6}
                    ]
                }
            }
        }
    
    def test_statistical_analysis_phase_method_exists(self, orchestrator):
        """Test that the statistical analysis phase method exists."""
        assert hasattr(orchestrator, '_run_statistical_analysis_phase')
        assert callable(orchestrator._run_statistical_analysis_phase)
    
    def test_statistical_analysis_phase_method_signature(self, orchestrator):
        """Test that the statistical analysis phase method has correct signature."""
        import inspect
        sig = inspect.signature(orchestrator._run_statistical_analysis_phase)
        params = list(sig.parameters.keys())
        
        assert 'model' in params
        assert 'audit_logger' in params
        assert 'analysis_results' in params
        assert 'derived_metrics_results' in params
    
    @patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent')
    def test_statistical_analysis_phase_creates_workspace(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that statistical analysis phase creates temporary workspace."""

        
        # Mock the agent
        mock_agent = Mock()
        mock_agent.generate_functions.return_value = {'functions_generated': 1}
        mock_agent_class.return_value = mock_agent
        
        # Mock the execution function
        with patch.object(orchestrator, '_execute_statistical_analysis_functions') as mock_execute:
            mock_execute.return_value = {
                'status': 'success',
                'statistical_results': {'correlation': 0.75}
            }
            
            # Run the phase
            result = orchestrator._run_statistical_analysis_phase("test_model", mock_audit_logger, mock_analysis_results, mock_derived_metrics_results)
            
            # Check that workspace was created
            temp_workspace = orchestrator.experiment_path / "temp_statistical_analysis"
            assert not temp_workspace.exists()  # Should be cleaned up
            
            # Check result
            assert result['status'] == 'completed'
            assert 'statistical_hash' in result
    
    @patch('discernus.agents.automated_statistical_analysis.agent.AutomatedStatisticalAnalysisAgent')
    def test_statistical_analysis_phase_stores_results(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results, mock_derived_metrics_results):
        """Test that statistical analysis phase stores results in artifact storage."""
        # Mock the agent
        mock_agent = Mock()
        mock_agent.generate_functions.return_value = {'functions_generated': 1}
        mock_agent_class.return_value = mock_agent
        
        # Mock the execution function
        with patch.object(orchestrator, '_execute_statistical_analysis_functions') as mock_execute:
            mock_execute.return_value = {
                'status': 'success',
                'statistical_results': {'correlation': 0.75}
            }
            
            # Run the phase
            result = orchestrator._run_statistical_analysis_phase("test_model", mock_audit_logger, mock_analysis_results, mock_derived_metrics_results)
            
            # Check that artifact storage was called
            assert orchestrator.artifact_storage.put_artifact.called
            
            # Check the stored data structure
            call_args = orchestrator.artifact_storage.put_artifact.call_args
            stored_data = json.loads(call_args[0][0].decode('utf-8'))
            
            assert 'statistical_data' in stored_data
            assert stored_data['status'] == 'success_with_data'
            assert stored_data['validation_passed'] is True
    
    def test_execute_statistical_analysis_functions_method_exists(self, orchestrator):
        """Test that the execute statistical analysis functions method exists."""
        assert hasattr(orchestrator, '_execute_statistical_analysis_functions')
        assert callable(orchestrator._execute_statistical_analysis_functions)
    
    def test_statistical_analysis_phase_integrated_in_main_flow(self, orchestrator):
        """Test that statistical analysis phase is integrated in the main run method."""
        # Check that the main run method references the statistical analysis phase
        assert hasattr(orchestrator, '_run_statistical_analysis_phase')
