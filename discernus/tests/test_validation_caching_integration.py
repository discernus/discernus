#!/usr/bin/env python3
"""
Integration Tests for Validation Caching

Tests that validation caching works correctly in the orchestrator context,
including cache hits, misses, persistence, and performance metrics.
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


import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.validation_cache import ValidationCacheManager


class TestValidationCachingIntegration(unittest.TestCase):
    """Integration tests for validation caching in orchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_experiment_path = Path(self.temp_dir) / "test_experiment"
        
        # Always create minimal test files for consistent testing
        self._create_minimal_test_files()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_minimal_test_files(self):
        """Create minimal test files for validation testing."""
        self.test_experiment_path.mkdir(parents=True, exist_ok=True)
        
        # Create experiment.md
        experiment_content = """---
name: "test_experiment"
description: "Test experiment for validation caching"
framework: "test_framework.md"
corpus: "test_corpus.md"
questions:
  - "Test question?"
---

# Test Experiment

## Configuration Appendix
```yaml
metadata:
  experiment_name: "test_experiment"
  author: "Test"
  spec_version: "10.0"
components:
  framework: "test_framework.md"
  corpus: "test_corpus.md"
```
"""
        (self.test_experiment_path / "experiment.md").write_text(experiment_content)
        
        # Create framework.md
        framework_content = """# Test Framework

## Configuration Appendix
```yaml
metadata:
  framework_name: "test_framework"
  spec_version: "10.0"
```
"""
        (self.test_experiment_path / "test_framework.md").write_text(framework_content)
        
        # Create corpus.md
        corpus_content = """# Test Corpus

## Document Manifest
```yaml
name: "Test Corpus"
version: "1.0"
documents:
  - filename: "test_doc.txt"
    metadata:
      speaker: "Test Speaker"
```
"""
        (self.test_experiment_path / "test_corpus.md").write_text(corpus_content)
        
        # Create corpus directory and test document
        corpus_dir = self.test_experiment_path / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "test_doc.txt").write_text("Test document content")
    
    def _setup_mock_artifact_storage(self, orchestrator):
        """Set up mock artifact storage with proper registry behavior."""
        orchestrator.artifact_storage = Mock()
        orchestrator.artifact_storage.registry = {}
        
        # Mock put_artifact to populate registry
        def mock_put_artifact(content, metadata):
            artifact_hash = "test_hash_123"
            orchestrator.artifact_storage.registry[artifact_hash] = {
                "metadata": metadata,
                "content": content
            }
            return artifact_hash
        
        orchestrator.artifact_storage.put_artifact.side_effect = mock_put_artifact
        
        # Mock artifact_exists to check registry
        def mock_artifact_exists(artifact_hash):
            return artifact_hash in orchestrator.artifact_storage.registry
        
        orchestrator.artifact_storage.artifact_exists.side_effect = mock_artifact_exists
        
        # Mock get_artifact to return content from registry
        def mock_get_artifact(artifact_hash):
            if artifact_hash in orchestrator.artifact_storage.registry:
                return orchestrator.artifact_storage.registry[artifact_hash]["content"]
            raise KeyError(f"Artifact {artifact_hash} not found")
        
        orchestrator.artifact_storage.get_artifact.side_effect = mock_get_artifact
    
    def test_validation_caching_workflow(self):
        """Test complete validation caching workflow in orchestrator."""
        
        # Create orchestrator with mocked components
        with patch('discernus.core.clean_analysis_orchestrator.ExperimentCoherenceAgent') as mock_agent_class:
            # Mock the coherence agent
            mock_agent = Mock()
            mock_agent.validate_experiment.return_value = Mock(success=True, issues=[])
            mock_agent_class.return_value = mock_agent
            
            # Create orchestrator
            orchestrator = CleanAnalysisOrchestrator(self.test_experiment_path)
            
            # Set up mock artifact storage
            self._setup_mock_artifact_storage(orchestrator)
            
            # Mock audit logger
            orchestrator.audit_logger = Mock()
            
            # Mock config loading
            orchestrator.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
            
            # First run - should cache miss and store result
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            initial_cache_misses = orchestrator.performance_metrics["cache_misses"]
            initial_cache_hits = orchestrator.performance_metrics["cache_hits"]
            
            # Verify first run was a cache miss
            self.assertEqual(initial_cache_misses, 1, "First run should be a cache miss")
            self.assertEqual(initial_cache_hits, 0, "First run should have no cache hits")
            
            # Verify validation agent was called
            mock_agent.validate_experiment.assert_called_once()
            
            # Second run - should cache hit
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            
            # Verify caching worked
            self.assertEqual(orchestrator.performance_metrics["cache_hits"], 1, "Second run should be a cache hit")
            self.assertEqual(orchestrator.performance_metrics["cache_misses"], 1, "No additional cache misses")
            
            # Verify validation agent was not called again
            mock_agent.validate_experiment.assert_called_once()  # Still only called once
    
    def test_cache_invalidation_on_content_change(self):
        """Test that cache misses when content changes."""
        
        with patch('discernus.core.clean_analysis_orchestrator.ExperimentCoherenceAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent.validate_experiment.return_value = Mock(success=True, issues=[])
            mock_agent_class.return_value = mock_agent
            
            orchestrator = CleanAnalysisOrchestrator(self.test_experiment_path)
            
            # Set up mock artifact storage
            self._setup_mock_artifact_storage(orchestrator)
            
            orchestrator.audit_logger = Mock()
            
            # Mock config loading
            orchestrator.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
            
            # First run - cache miss
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            
            # Modify experiment content
            experiment_file = self.test_experiment_path / "experiment.md"
            content = experiment_file.read_text()
            modified_content = content.replace("Test question?", "Modified test question?")
            experiment_file.write_text(modified_content)
            
            # Second run with modified content - should cache miss again
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            
            # Verify both runs were cache misses due to content change
            self.assertEqual(orchestrator.performance_metrics["cache_misses"], 2, "Both runs should be cache misses")
            self.assertEqual(orchestrator.performance_metrics["cache_hits"], 0, "No cache hits due to content change")
            
            # Verify validation agent was called twice
            self.assertEqual(mock_agent.validate_experiment.call_count, 2, "Validation agent should be called twice")
    
    def test_cache_persistence_across_orchestrator_instances(self):
        """Test that cache persists between orchestrator instances."""
        
        with patch('discernus.core.clean_analysis_orchestrator.ExperimentCoherenceAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent.validate_experiment.return_value = Mock(success=True, issues=[])
            mock_agent_class.return_value = mock_agent
            
            # Create first orchestrator instance
            orchestrator1 = CleanAnalysisOrchestrator(self.test_experiment_path)
            
            # Set up mock artifact storage
            self._setup_mock_artifact_storage(orchestrator1)
            
            orchestrator1.audit_logger = Mock()
            
            # Mock config loading
            orchestrator1.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
            
            # First run - cache miss
            orchestrator1._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator1.audit_logger)
            
            # Create second orchestrator instance with same artifact storage
            orchestrator2 = CleanAnalysisOrchestrator(self.test_experiment_path)
            orchestrator2.artifact_storage = orchestrator1.artifact_storage  # Same storage
            orchestrator2.audit_logger = Mock()
            
            # Mock config loading
            orchestrator2.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
            
            # Second run in new instance - should cache hit
            orchestrator2._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator2.audit_logger)
            
            # Verify cache hit occurred
            self.assertEqual(orchestrator2.performance_metrics["cache_hits"], 1, "Second instance should have cache hit")
            self.assertEqual(orchestrator2.performance_metrics["cache_misses"], 0, "Second instance should have no cache misses")
    
    def test_cache_key_determinism(self):
        """Test that cache keys are deterministic across orchestrator instances."""
        
        orchestrator1 = CleanAnalysisOrchestrator(self.test_experiment_path)
        orchestrator2 = CleanAnalysisOrchestrator(self.test_experiment_path)
        
        # Mock artifact storage for both
        for orchestrator in [orchestrator1, orchestrator2]:
            self._setup_mock_artifact_storage(orchestrator)
            orchestrator.audit_logger = Mock()
            orchestrator.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
        
        # Generate cache keys for same content
        cache_key1 = orchestrator1._generate_validation_cache_key("vertex_ai/gemini-2.5-pro")
        cache_key2 = orchestrator2._generate_validation_cache_key("vertex_ai/gemini-2.5-pro")
        
        # Verify keys are identical
        self.assertEqual(cache_key1, cache_key2, "Cache keys should be deterministic")
        self.assertTrue(cache_key1.startswith("validation_"), "Cache key should start with 'validation_'")
    
    def test_cache_performance_metrics_integration(self):
        """Test that cache performance metrics are properly tracked."""
        
        with patch('discernus.core.clean_analysis_orchestrator.ExperimentCoherenceAgent') as mock_agent_class:
            mock_agent = Mock()
            mock_agent.validate_experiment.return_value = Mock(success=True, issues=[])
            mock_agent_class.return_value = mock_agent
            
            orchestrator = CleanAnalysisOrchestrator(self.test_experiment_path)
            
            # Set up mock artifact storage
            self._setup_mock_artifact_storage(orchestrator)
            
            orchestrator.audit_logger = Mock()
            
            # Mock config loading
            orchestrator.config = {
                'framework': 'test_framework.md',
                'corpus': 'test_corpus.md'
            }
            
            # First run - cache miss
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            
            # Verify cache miss metrics
            self.assertEqual(orchestrator.performance_metrics["cache_misses"], 1, "Cache miss should be recorded")
            self.assertEqual(orchestrator.performance_metrics["cache_hits"], 0, "Cache hits should be 0")
            
            # Second run - cache hit
            orchestrator._run_coherence_validation("vertex_ai/gemini-2.5-pro", orchestrator.audit_logger)
            
            # Verify cache hit metrics
            self.assertEqual(orchestrator.performance_metrics["cache_hits"], 1, "Cache hit should be recorded")
            self.assertEqual(orchestrator.performance_metrics["cache_misses"], 1, "Cache misses should remain 1")
            
            # Verify hit rate calculation
            expected_hit_rate = 1 / (1 + 1)  # 1 hit / (1 hit + 1 miss) = 0.5
            actual_hit_rate = orchestrator.performance_metrics["cache_hits"] / (orchestrator.performance_metrics["cache_hits"] + orchestrator.performance_metrics["cache_misses"])
            self.assertEqual(actual_hit_rate, expected_hit_rate, "Cache hit rate should be calculated correctly")


if __name__ == '__main__':
    unittest.main()
