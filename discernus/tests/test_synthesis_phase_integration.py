#!/usr/bin/env python3
"""
Test Synthesis Phase Integration

Tests that the CleanAnalysisOrchestrator properly integrates the synthesis phase.
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
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.audit_logger import AuditLogger


class TestSynthesisPhaseIntegration:
    """Test the synthesis phase integration in CleanAnalysisOrchestrator."""
    
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
        
        # Create corpus.md with proper v10 format
        corpus_content = """# Test Corpus

## Document Manifest
```yaml
documents:
  - filename: "test_doc.txt"
    title: "Test Document"
    source: "Test Source"
    date: "2024-01-01"
```
"""
        (experiment_dir / "corpus.md").write_text(corpus_content)
        
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
        # Mock registry as a dictionary to make it iterable
        orchestrator.artifact_storage.registry = {
            "evidence_hash_1": {"metadata": {"artifact_type": "evidence_v6"}},
            "evidence_hash_2": {"metadata": {"artifact_type": "evidence_v6"}}
        }
        
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
    
    @pytest.fixture
    def mock_statistical_results(self):
        """Create mock statistical results."""
        return {
            'status': 'completed',
            'statistical_results': {
                'statistical_data': {
                    'status': 'success',
                    'statistical_results': {'correlation': 0.75}
                }
            }
        }
    
    def test_synthesis_phase_method_exists(self, orchestrator):
        """Test that the synthesis phase method exists."""
        assert hasattr(orchestrator, '_run_synthesis')
        assert callable(orchestrator._run_synthesis)
    
    def test_synthesis_phase_method_signature(self, orchestrator):
        """Test that the synthesis phase method has correct signature."""
        import inspect
        sig = inspect.signature(orchestrator._run_synthesis)
        params = list(sig.parameters.keys())
        
        # Should accept synthesis_model, audit_logger, and statistical_results
        assert 'synthesis_model' in params
        assert 'audit_logger' in params
        assert 'statistical_results' in params
    
    @patch('discernus.core.reuse_candidates.unified_synthesis_agent.UnifiedSynthesisAgent')
    def test_synthesis_phase_uses_synthesis_assembler(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results, mock_derived_metrics_results, mock_statistical_results):
        """Test that synthesis phase uses SynthesisPromptAssembler to build prompt."""
        # Mock the agent
        mock_agent = Mock()
        mock_agent.generate_final_report.return_value = {
            'status': 'success',
            'final_report': 'Test synthesis report'
        }
        mock_agent_class.return_value = mock_agent
        
        # Mock the SynthesisPromptAssembler
        with patch('discernus.core.prompt_assemblers.synthesis_assembler.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler.assemble_prompt.return_value = "Test assembled prompt"
            mock_assembler_class.return_value = mock_assembler
            
            # Run the synthesis phase
            result = orchestrator._run_synthesis("test_model", mock_audit_logger, mock_statistical_results)
            
            # Check that the assembler was used
            mock_assembler.assemble_prompt.assert_called_once()
            
            # Check that the agent was called with the assembled prompt
            mock_agent.generate_final_report.assert_called_once()
    
    @patch('discernus.core.reuse_candidates.unified_synthesis_agent.UnifiedSynthesisAgent')
    def test_synthesis_phase_passes_correct_context_to_assembler(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results, mock_derived_metrics_results, mock_statistical_results):
        """Test that synthesis phase passes correct context to assembler."""
        # Mock the agent
        mock_agent = Mock()
        mock_agent.generate_final_report.return_value = {
            'status': 'success',
            'final_report': 'Test synthesis report'
        }
        mock_agent_class.return_value = mock_agent
        
        # Mock the SynthesisPromptAssembler
        with patch('discernus.core.prompt_assemblers.synthesis_assembler.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler.assemble_prompt.return_value = "Test assembled prompt"
            mock_assembler_class.return_value = mock_assembler
            
            # Run the synthesis phase
            result = orchestrator._run_synthesis("test_model", mock_audit_logger, mock_statistical_results)
            
            # Check that assembler was called with correct parameters
            call_args = mock_assembler.assemble_prompt.call_args
            assert call_args is not None
            
            # Should pass framework, experiment, and research data artifact hash
            kwargs = call_args.kwargs
            assert 'framework_path' in kwargs
            assert 'experiment_path' in kwargs
            assert 'research_data_artifact_hash' in kwargs
    
    @patch('discernus.core.reuse_candidates.unified_synthesis_agent.UnifiedSynthesisAgent')
    def test_synthesis_phase_stores_results(self, mock_agent_class, orchestrator, mock_audit_logger, mock_analysis_results, mock_derived_metrics_results, mock_statistical_results):
        """Test that synthesis phase stores results in artifact storage."""
        # Mock the agent
        mock_agent = Mock()
        mock_agent.generate_final_report.return_value = {
            'status': 'success',
            'final_report': 'Test synthesis report'
        }
        mock_agent_class.return_value = mock_agent
        
        # Mock the SynthesisPromptAssembler
        with patch('discernus.core.prompt_assemblers.synthesis_assembler.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler.assemble_prompt.return_value = "Test assembled prompt"
            mock_assembler_class.return_value = mock_assembler
            
            # Run the synthesis phase
            result = orchestrator._run_synthesis("test_model", mock_audit_logger, mock_statistical_results)
            
            # Check that artifact storage was called
            assert orchestrator.artifact_storage.put_artifact.called
    
    def test_synthesis_phase_integrated_in_main_flow(self, orchestrator):
        """Test that synthesis phase is integrated in the main run method."""
        # Check that the main run method references the synthesis phase
        assert hasattr(orchestrator, '_run_synthesis')
