#!/usr/bin/env python3
"""
Comprehensive tests for CleanAnalysisOrchestrator with enhanced features.

Tests all ARCH-003 features:
- Enhanced Error Handling with graceful degradation
- Performance optimization and caching
- Complete testing support
- CLI default switch (deprecation warnings)
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
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
from datetime import datetime, timezone

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError
# Import deprecated orchestrator for testing deprecation
# from discernus.core.deprecated.experiment_orchestrator import ExperimentOrchestrator


class TestCleanAnalysisOrchestratorEnhanced:
    """Test enhanced features of CleanAnalysisOrchestrator."""
    
    @pytest.fixture
    def mock_experiment_path(self, tmp_path):
        """Create a mock experiment directory structure."""
        experiment_dir = tmp_path / "test_experiment"
        experiment_dir.mkdir()
        
        # Create experiment.md
        experiment_file = experiment_dir / "experiment.md"
        experiment_file.write_text("""---
name: Test Experiment
framework: test_framework.md
corpus: test_corpus.md
questions:
  - What is the main theme?
---
## Configuration Appendix
```yaml
metadata:
  experiment_name: test_experiment
```
""")
        
        # Create framework file
        framework_file = experiment_dir / "test_framework.md"
        framework_file.write_text("# Test Framework\n\nTest framework content")
        
        # Create corpus file
        corpus_file = experiment_dir / "test_corpus.md"
        corpus_file.write_text("""# Test Corpus

## Documents
- test_doc1.txt
- test_doc2.txt
""")
        
        # Create corpus directory with test documents
        corpus_dir = experiment_dir / "corpus"
        corpus_dir.mkdir()
        
        (corpus_dir / "test_doc1.txt").write_text("Test document 1 content")
        (corpus_dir / "test_doc2.txt").write_text("Test document 2 content")
        
        # Create shared_cache directory
        shared_cache = experiment_dir / "shared_cache"
        shared_cache.mkdir()
        
        return experiment_dir
    
    @pytest.fixture
    def orchestrator(self, mock_experiment_path):
        """Create a CleanAnalysisOrchestrator instance."""
        return CleanAnalysisOrchestrator(mock_experiment_path)
    
    def test_test_mode_configuration(self, orchestrator):
        """Test test mode configuration methods."""
        # Initially disabled
        assert orchestrator.test_mode is False
        assert orchestrator.mock_llm_calls is False
        assert orchestrator.performance_monitoring is True
        
        # Enable test mode
        orchestrator.enable_test_mode(mock_llm=True, performance_monitoring=False)
        assert orchestrator.test_mode is True
        assert orchestrator.mock_llm_calls is True
        assert orchestrator.performance_monitoring is False
        
        # Disable test mode
        orchestrator.disable_test_mode()
        assert orchestrator.test_mode is False
        assert orchestrator.mock_llm_calls is False
        assert orchestrator.performance_monitoring is True
    
    def test_tuple_key_handling_in_fact_checker_rag(self, orchestrator):
        """
        Test that the orchestrator can handle tuple keys in statistical results
        when building fact-checker RAG indexes.
        
        This test verifies that the _build_fact_checker_rag_index method
        can handle tuple keys without crashing.
        """
        # Create mock statistical results with tuple keys
        mock_statistical_results = {
            'stats_hash': 'test_hash',
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699}
                }
            }
        }
        
        # Mock the artifact storage
        with patch.object(orchestrator, 'artifact_storage') as mock_storage:
            mock_storage.registry = {
                'test_hash': {'metadata': {'artifact_type': 'statistical_results_with_data'}},
                'evidence_hash': {'metadata': {'artifact_type': 'evidence_v6_test'}}
            }
            mock_storage.get_artifact.return_value = b'{"test": "data"}'
            
            # This should not crash with tuple keys
            try:
                result = orchestrator._build_fact_checker_rag_index(
                    mock_statistical_results, 
                    {'report_hash': 'test_report'}
                )
                
                # Verify the method completed successfully
                assert result is not None
                
            except Exception as e:
                pytest.fail(f"Fact-checker RAG building failed with error: {e}")
    
    def test_get_test_configuration(self, orchestrator):
        """Test test configuration retrieval."""
        config = orchestrator.get_test_configuration()
        
        assert "test_mode" in config
        assert "mock_llm_calls" in config
        assert "performance_monitoring" in config
        assert "experiment_path" in config
        assert "security_boundary" in config
        
        assert config["test_mode"] is False
        assert config["experiment_path"] == str(orchestrator.experiment_path)
    
    @patch('discernus.core.clean_analysis_orchestrator.setup_logging')
    @patch('discernus.core.clean_analysis_orchestrator.AuditLogger')
    @patch('discernus.core.clean_analysis_orchestrator.LocalArtifactStorage')
    @patch('discernus.core.clean_analysis_orchestrator.EnhancedManifest')
    @patch('discernus.core.clean_analysis_orchestrator.LLMGateway')
    @patch('discernus.core.clean_analysis_orchestrator.ModelRegistry')
    def test_infrastructure_initialization_with_performance_monitoring(self, mock_model_registry, mock_llm_gateway, 
                                                                    mock_manifest, mock_storage, mock_audit_logger, 
                                                                    mock_setup_logging, orchestrator):
        """Test infrastructure initialization includes performance monitoring."""
        # Mock the storage methods
        mock_storage_instance = Mock()
        mock_storage_instance.put_artifact = Mock(return_value="test_hash")
        mock_storage_instance.get_artifact = Mock(return_value={"test": "data"})
        mock_storage.return_value = mock_storage_instance
        
        # Mock audit logger
        mock_audit_instance = Mock()
        mock_audit_logger.return_value = mock_audit_instance
        
        # Mock manifest
        mock_manifest_instance = Mock()
        mock_manifest.return_value = mock_manifest_instance
        
        # Mock LLM gateway
        mock_gateway_instance = Mock()
        mock_llm_gateway.return_value = mock_gateway_instance
        
        # Mock model registry
        mock_registry_instance = Mock()
        mock_model_registry.return_value = mock_registry_instance
        
        # Initialize infrastructure
        audit_logger = orchestrator._initialize_infrastructure("test_run_id")
        
        # Verify performance monitoring was initialized
        assert hasattr(orchestrator, 'performance_metrics')
        assert 'start_time' in orchestrator.performance_metrics
        assert 'phase_timings' in orchestrator.performance_metrics
        assert 'cache_hits' in orchestrator.performance_metrics
        assert 'cache_misses' in orchestrator.performance_metrics
        
        # Verify cache performance verification was called
        mock_storage_instance.put_artifact.assert_called()
        # Note: get_artifact is called during _verify_caching_performance but only if test data is found
        # The mock registry is empty, so get_artifact won't be called in this test scenario
    
    def test_phase_timing_logging(self, orchestrator):
        """Test phase timing logging functionality."""
        start_time = datetime.now(timezone.utc)
        
        # Log phase timing
        orchestrator._log_phase_timing("test_phase", start_time)
        
        # Verify timing was recorded
        assert "test_phase" in orchestrator.performance_metrics["phase_timings"]
        assert orchestrator.performance_metrics["phase_timings"]["test_phase"] >= 0
    
    def test_performance_summary_generation(self, orchestrator):
        """Test performance summary generation."""
        # Set up some mock performance data
        orchestrator.performance_metrics = {
            "start_time": datetime.now(timezone.utc),
            "phase_timings": {
                "phase1": 5.0,
                "phase2": 10.0
            },
            "cache_hits": 8,
            "cache_misses": 2
        }
        
        summary = orchestrator._get_performance_summary()
        
        assert "total_duration_seconds" in summary
        assert "phase_timings" in summary
        assert "cache_efficiency" in summary
        assert "performance_score" in summary
        
        # Verify cache efficiency calculation
        assert summary["cache_efficiency"]["hits"] == 8
        assert summary["cache_efficiency"]["misses"] == 2
        assert summary["cache_efficiency"]["hit_rate"] == 0.8  # 8/(8+2)
        
        # Verify performance score calculation
        assert 0 <= summary["performance_score"] <= 100
    
    def test_performance_score_calculation(self, orchestrator):
        """Test performance score calculation logic."""
        # Test with good performance
        orchestrator.performance_metrics = {
            "phase_timings": {
                "phase1": 5.0,  # Fast phase
                "phase2": 8.0   # Fast phase
            },
            "cache_hits": 9,
            "cache_misses": 1
        }
        
        score = orchestrator._calculate_performance_score()
        assert score > 90  # Should be high with fast phases and good cache hit rate
        
        # Test with slow performance
        orchestrator.performance_metrics = {
            "phase_timings": {
                "phase1": 40.0,  # Slow phase (>30s)
                "phase2": 50.0   # Slow phase (>30s)
            },
            "cache_hits": 2,
            "cache_misses": 8
        }
        
        score = orchestrator._calculate_performance_score()
        assert score < 70  # Should be lower with slow phases and poor cache hit rate
    
    @patch('discernus.core.clean_analysis_orchestrator.EnhancedAnalysisAgent')
    def test_analysis_phase_with_cache_tracking(self, mock_analysis_agent_class, orchestrator):
        """Test analysis phase includes cache hit/miss tracking."""
        # Mock the analysis agent
        mock_agent = Mock()
        mock_agent.analyze_documents.return_value = {
            'analysis_result': {
                'result_content': {
                    'raw_analysis_response': 'test response'
                }
            },
            'scores_hash': 'test_scores_hash',
            'evidence_hash': 'test_evidence_hash'
        }
        mock_analysis_agent_class.return_value = mock_agent
        
        # Mock artifact storage
        mock_storage = Mock()
        mock_storage.get_artifact.return_value = None  # No cached result
        mock_storage.put_artifact.return_value = "test_hash"
        orchestrator.artifact_storage = mock_storage
        
        # Mock corpus documents
        mock_corpus_docs = [
            {'filename': 'test1.txt', 'document_id': 'doc_1'},
            {'filename': 'test2.txt', 'document_id': 'doc_2'}
        ]
        
        with patch.object(orchestrator, '_load_corpus_documents', return_value=mock_corpus_docs):
            with patch.object(orchestrator, '_prepare_documents_for_analysis', return_value=mock_corpus_docs):
                with patch.object(orchestrator, '_find_corpus_file', return_value=Path("test.txt")):
                    with patch.object(Path, 'read_text', return_value="test content"):
                        # Mock the config to have the required fields
                        orchestrator.config = {'framework': 'test_framework.md', 'questions': ['test question']}
                        
                        results = orchestrator._run_analysis_phase("test_model", Mock())
        
        # Verify cache misses were tracked
        assert orchestrator.performance_metrics["cache_misses"] == 2
        assert orchestrator.performance_metrics["cache_hits"] == 0
        
        # Verify results were generated
        assert len(results) == 2
        assert all('analysis_result' in result for result in results)
    
    def test_graceful_degradation_on_validation_failure(self, orchestrator):
        """Test that validation failures don't block the experiment."""
        # Mock the infrastructure initialization but ensure artifact_storage is set up
        mock_audit_logger = Mock()
        mock_storage = Mock()
        mock_storage.registry = {}  # Provide empty registry to prevent NoneType error
        
        with patch.object(orchestrator, '_initialize_infrastructure', return_value=mock_audit_logger):
            # Set up artifact storage manually since we're mocking infrastructure
            orchestrator.artifact_storage = mock_storage
            
            with patch.object(orchestrator, '_load_specs', return_value={'name': 'test'}):
                with patch.object(orchestrator, '_validate_corpus_files_exist', return_value=[]):
                    with patch.object(orchestrator, '_run_analysis_phase', return_value=[{'test': 'data'}]):
                        with patch.object(orchestrator, '_run_statistical_analysis', return_value={'test': 'stats'}):
                            with patch.object(orchestrator, '_run_synthesis', return_value={'test': 'synthesis'}):
                                with patch.object(orchestrator, '_create_clean_results_directory', return_value=Path("test")):
                                    # Mock coherence validation to fail
                                    with patch.object(orchestrator, '_run_coherence_validation', side_effect=Exception("Validation failed")):
                                        # Should continue with warning
                                        result = orchestrator.run_experiment(skip_validation=False)
                                        
                                        # Verify experiment completed despite validation failure
                                        assert result["status"] == "completed"
                                        assert "warnings" in result
    
    def test_basic_results_directory_creation_on_failure(self, orchestrator):
        """Test basic results directory creation when main creation fails."""
        # Mock the infrastructure initialization but ensure artifact_storage is set up
        mock_audit_logger = Mock()
        mock_storage = Mock()
        mock_storage.registry = {}  # Provide empty registry to prevent NoneType error
        
        with patch.object(orchestrator, '_initialize_infrastructure', return_value=Mock()):
            # Set up artifact storage manually since we're mocking infrastructure
            orchestrator.artifact_storage = mock_storage
            
            with patch.object(orchestrator, '_load_specs', return_value={'name': 'test'}):
                with patch.object(orchestrator, '_validate_corpus_files_exist', return_value=[]):
                    with patch.object(orchestrator, '_run_analysis_phase', return_value=[{'test': 'data'}]):
                        with patch.object(orchestrator, '_run_statistical_analysis', return_value={'test': 'stats'}):
                            with patch.object(orchestrator, '_run_synthesis', return_value={'test': 'synthesis'}):
                                # Mock main results creation to fail
                                with patch.object(orchestrator, '_create_clean_results_directory', side_effect=Exception("Results creation failed")):
                                    # Mock basic results creation
                                    with patch.object(orchestrator, '_create_basic_results_directory', return_value=Path("basic_results")):
                                        result = orchestrator.run_experiment()
                                        
                                        # Verify experiment completed with basic results
                                        assert result["status"] == "completed"
                                        assert "warnings" in result


class TestLegacyOrchestratorDeprecation:
    """Test that legacy orchestrator is properly deprecated and moved to deprecated/ folder."""
    
    @pytest.fixture
    def mock_experiment_path(self, tmp_path):
        """Create a mock experiment directory structure."""
        experiment_dir = tmp_path / "test_experiment"
        experiment_dir.mkdir()
        
        # Create experiment.md
        experiment_file = experiment_dir / "experiment.md"
        experiment_file.write_text("""---
name: Test Experiment
framework: test_framework.md
corpus: test_corpus.md
questions:
  - What is the main theme?
---
## Configuration Appendix
```yaml
metadata:
  experiment_name: test_experiment
```
""")
        
        # Create framework file
        framework_file = experiment_dir / "test_framework.md"
        framework_file.write_text("# Test Framework\n\nTest framework content")
        
        # Create corpus file
        corpus_file = experiment_dir / "test_corpus.md"
        corpus_file.write_text("""# Test Corpus

## Documents
- test_doc1.txt
- test_doc2.txt
""")
        
        # Create corpus directory with test documents
        corpus_dir = experiment_dir / "corpus"
        corpus_dir.mkdir()
        
        (corpus_dir / "test_doc1.txt").write_text("Test document 1 content")
        (corpus_dir / "test_doc2.txt").write_text("Test document 2 content")
        
        # Create shared_cache directory
        shared_cache = experiment_dir / "shared_cache"
        shared_cache.mkdir()
        
        return experiment_dir
    
    def test_legacy_orchestrator_moved_to_deprecated(self):
        """Test that legacy orchestrator is properly moved to deprecated/ folder."""
        from pathlib import Path
        
        # Verify deprecated orchestrator is in deprecated/ folder
        deprecated_path = Path(__file__).parent.parent / "core" / "deprecated" / "experiment_orchestrator.py"
        assert deprecated_path.exists(), "ExperimentOrchestrator should be in deprecated/ folder"
        
        # Verify it's not in the main core directory
        main_path = Path(__file__).parent.parent / "core" / "experiment_orchestrator.py"
        assert not main_path.exists(), "ExperimentOrchestrator should not be in main core/ directory"
    
    def test_clean_orchestrator_is_default(self):
        """Test that CleanAnalysisOrchestrator is the default and available."""
        from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
        
        # Should be able to import without issues
        assert CleanAnalysisOrchestrator is not None
        
        # Should be in main core directory
        main_path = Path(__file__).parent.parent / "core" / "clean_analysis_orchestrator.py"
        assert main_path.exists(), "CleanAnalysisOrchestrator should be in main core/ directory"


if __name__ == "__main__":
    pytest.main([__file__])
