#!/usr/bin/env python3
"""
Unit Tests for CleanAnalysisOrchestrator Analysis Phase
=====================================================

Tests for the critical analysis phase that was affected by the batch processing regression.
These tests use mocked dependencies to avoid API calls and focus on the orchestration logic.

Key Test Areas:
1. Individual document processing loop (vs batch processing)
2. Artifact storage for each document 
3. Error handling and partial failures
4. Integration with AnalysisAgent
5. Path resolution and corpus validation
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import json
import tempfile
import shutil
from typing import Dict, Any, List

# Import the class under test
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError


class TestCleanAnalysisOrchestratorAnalysis(unittest.TestCase):
    """Test the analysis phase of CleanAnalysisOrchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test experiment
        self.temp_dir = Path(tempfile.mkdtemp())
        self.experiment_path = self.temp_dir / "test_experiment"
        self.experiment_path.mkdir(parents=True)
        
        # Create mock experiment files
        self.experiment_file = self.experiment_path / "experiment.md"
        self.framework_file = self.experiment_path / "framework.md"
        self.corpus_file = self.experiment_path / "corpus.md"
        
        # Mock experiment content
        self.experiment_content = """---
name: "test_experiment"
description: "Test experiment for unit testing"
framework: "framework.md"
corpus: "corpus.md"
questions:
  - "Test question 1"
  - "Test question 2"
---

# Test Experiment
Test experiment for unit testing.
"""
        
        # Mock framework content
        self.framework_content = """# Test Framework
Test framework for unit testing with proper structure.
"""
        
        # Mock corpus content with document manifest
        self.corpus_content = """# Test Corpus

## Document Manifest

```yaml
name: "Test Corpus"
version: "1.0"
total_documents: 2

documents:
  - filename: "doc1.txt"
    document_id: "doc1"
    metadata:
      author: "Author 1"
      year: 2023
  - filename: "doc2.txt" 
    document_id: "doc2"
    metadata:
      author: "Author 2"
      year: 2024
```
"""
        
        # Write mock files
        self.experiment_file.write_text(self.experiment_content)
        self.framework_file.write_text(self.framework_content)
        self.corpus_file.write_text(self.corpus_content)
        
        # Create corpus directory and documents
        self.corpus_dir = self.experiment_path / "corpus"
        self.corpus_dir.mkdir()
        (self.corpus_dir / "doc1.txt").write_text("Content of document 1")
        (self.corpus_dir / "doc2.txt").write_text("Content of document 2")
        
        # Create shared_cache directory structure
        self.shared_cache = self.experiment_path / "shared_cache" / "artifacts"
        self.shared_cache.mkdir(parents=True)
        
        # Initialize orchestrator
        self.orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
        
        # Mock the config loading
        self.orchestrator.config = {
            'name': 'test_experiment',
            'description': 'Test experiment for unit testing',
            'framework': 'framework.md',
            'corpus': 'corpus.md',
            'questions': ['Test question 1', 'Test question 2']
        }
        
        # Mock dependencies
        self.mock_security = Mock()
        self.mock_audit_logger = Mock()
        self.mock_artifact_storage = Mock()
        self.mock_analysis_agent = Mock()
        
        # Configure artifact storage mock properly
        self.mock_artifact_storage.registry = {}
        self.mock_artifact_storage.put_artifact.return_value = "mock_hash"
        
        # Assign mocks to orchestrator
        self.orchestrator.security = self.mock_security
        self.orchestrator.audit_logger = self.mock_audit_logger
        self.orchestrator.artifact_storage = self.mock_artifact_storage
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_individual_document_processing_loop(self):
        """Test that analysis processes documents individually, not as a batch."""
        # Mock analysis agent response for individual document
        mock_individual_response = {
            "batch_id": "batch_individual_123",
            "agent_name": "AnalysisAgent",
            "experiment_name": "test_experiment",
            "raw_analysis_response": "Mock individual analysis response",
            "evidence_hash": "mock_evidence_hash",
            "execution_metadata": {"duration_seconds": 30.0}
        }
        
        # Configure analysis agent to return individual responses
        self.mock_analysis_agent.analyze_batch.return_value = mock_individual_response
        
        # Configure artifact storage
        self.mock_artifact_storage.put_artifact.return_value = "mock_artifact_hash"
        
        # Mock the _run_analysis_phase method to use individual processing
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            # Mock corpus documents
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}},
                {'filename': 'doc2.txt', 'metadata': {'author': 'Author 2'}}
            ]
            
            with patch.object(self.orchestrator, '_find_corpus_file') as mock_find_file:
                # Mock file finding
                mock_find_file.side_effect = [
                    self.corpus_dir / "doc1.txt",
                    self.corpus_dir / "doc2.txt"
                ]
                
                with patch('discernus.agents.analysis_agent.main.AnalysisAgent') as mock_agent_class:
                    # Configure the mock agent properly
                    mock_agent_instance = Mock()
                    mock_agent_instance.analyze_batch.return_value = mock_individual_response
                    mock_agent_class.return_value = mock_agent_instance
                    
                    # Call the method that should use individual processing
                    results = self.orchestrator._run_analysis_phase_individual(
                        analysis_model="test_model",
                        audit_logger=self.mock_audit_logger
                    )
        
        # Verify that analyze_batch was called twice (once per document)
        self.assertEqual(mock_agent_instance.analyze_batch.call_count, 2)
        
        # Verify each call was made with a single document
        calls = mock_agent_instance.analyze_batch.call_args_list
        for call_args, call_kwargs in calls:
            corpus_documents = call_kwargs['corpus_documents']
            self.assertEqual(len(corpus_documents), 1, "Each call should process exactly one document")
        
        # Verify artifact storage was called for each document
        self.assertEqual(self.mock_artifact_storage.put_artifact.call_count, 2)
        
        # Verify results structure
        self.assertEqual(len(results), 2, "Should return results for both documents")
    
    def test_batch_processing_detection(self):
        """Test that we can detect when batch processing is being used incorrectly."""
        # Mock analysis agent response for batch processing (WRONG)
        mock_batch_response = {
            "batch_id": "batch_all_docs_456", 
            "agent_name": "AnalysisAgent",
            "experiment_name": "test_experiment",
            "raw_analysis_response": "Mock batch analysis response for ALL documents",
            "evidence_hash": "mock_batch_evidence_hash",
            "execution_metadata": {"duration_seconds": 120.0}
        }
        
        self.mock_analysis_agent.analyze_batch.return_value = mock_batch_response
        
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}},
                {'filename': 'doc2.txt', 'metadata': {'author': 'Author 2'}}
            ]
            
            with patch('discernus.core.clean_analysis_orchestrator.AnalysisAgent') as mock_agent_class:
                mock_agent_class.return_value = self.mock_analysis_agent
                
                # Call the current (broken) batch processing method
                results = self.orchestrator._run_analysis_phase_batch(
                    analysis_model="test_model", 
                    audit_logger=self.mock_audit_logger
                )
        
        # Verify that analyze_batch was called only once (batch processing - WRONG)
        self.assertEqual(self.mock_analysis_agent.analyze_batch.call_count, 1)
        
        # Verify the call was made with ALL documents at once (WRONG)
        call_args, call_kwargs = self.mock_analysis_agent.analyze_batch.call_args_list[0]
        corpus_documents = call_kwargs['corpus_documents']
        self.assertEqual(len(corpus_documents), 2, "Batch processing incorrectly processes all documents at once")
        
        # This demonstrates the problem: only 1 result instead of 2
        self.assertEqual(len(results), 1, "Batch processing returns single result instead of individual results")
    
    def test_artifact_storage_per_document(self):
        """Test that each document gets its own artifact stored."""
        mock_response = {
            "batch_id": "batch_individual_789",
            "agent_name": "AnalysisAgent", 
            "experiment_name": "test_experiment",
            "raw_analysis_response": "Mock analysis response",
            "evidence_hash": "mock_evidence_hash"
        }
        
        self.mock_analysis_agent.analyze_batch.return_value = mock_response
        self.mock_artifact_storage.put_artifact.side_effect = ["hash1", "hash2"]
        
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}},
                {'filename': 'doc2.txt', 'metadata': {'author': 'Author 2'}}
            ]
            
            with patch.object(self.orchestrator, '_find_corpus_file') as mock_find_file:
                mock_find_file.side_effect = [
                    self.corpus_dir / "doc1.txt",
                    self.corpus_dir / "doc2.txt"  
                ]
                
                with patch('discernus.core.clean_analysis_orchestrator.AnalysisAgent') as mock_agent_class:
                    mock_agent_class.return_value = self.mock_analysis_agent
                    
                    results = self.orchestrator._run_analysis_phase_individual(
                        analysis_model="test_model",
                        audit_logger=self.mock_audit_logger
                    )
        
        # Verify artifact storage calls
        self.assertEqual(self.mock_artifact_storage.put_artifact.call_count, 2)
        
        # Verify each artifact has proper metadata
        calls = self.mock_artifact_storage.put_artifact.call_args_list
        for i, (call_args, call_kwargs) in enumerate(calls):
            content = call_args[0]  # First argument is content
            metadata = call_args[1]  # Second argument is metadata
            
            # Verify content is JSON-encoded analysis result
            self.assertIsInstance(content, bytes)
            
            # Verify metadata structure
            self.assertIn('artifact_type', metadata)
            self.assertEqual(metadata['artifact_type'], 'analysis_result')
            self.assertIn('document_id', metadata)
    
    def test_error_handling_partial_failures(self):
        """Test handling when some documents fail analysis."""
        # Mock analysis agent to fail on second document
        def mock_analyze_side_effect(*args, **kwargs):
            corpus_docs = kwargs['corpus_documents']
            if corpus_docs[0]['filename'] == 'doc1.txt':
                return {
                    "batch_id": "batch_success",
                    "agent_name": "EnhancedAnalysisAgent",
                    "raw_analysis_response": "Success response"
                }
            else:
                raise Exception("Analysis failed for doc2.txt")
        
        self.mock_analysis_agent.analyze_batch.side_effect = mock_analyze_side_effect
        self.mock_artifact_storage.put_artifact.return_value = "success_hash"
        
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}},
                {'filename': 'doc2.txt', 'metadata': {'author': 'Author 2'}}
            ]
            
            with patch.object(self.orchestrator, '_find_corpus_file') as mock_find_file:
                mock_find_file.side_effect = [
                    self.corpus_dir / "doc1.txt",
                    self.corpus_dir / "doc2.txt"
                ]
                
                with patch('discernus.core.clean_analysis_orchestrator.AnalysisAgent') as mock_agent_class:
                    mock_agent_class.return_value = self.mock_analysis_agent
                    
                    results = self.orchestrator._run_analysis_phase_individual(
                        analysis_model="test_model",
                        audit_logger=self.mock_audit_logger
                    )
        
        # Verify both documents were attempted
        self.assertEqual(self.mock_analysis_agent.analyze_batch.call_count, 2)
        
        # Verify only successful document was stored
        self.assertEqual(self.mock_artifact_storage.put_artifact.call_count, 1)
        
        # Verify results include both success and failure
        self.assertEqual(len(results), 2)
        
        # Check success result
        success_result = next(r for r in results if r['document'] == 'doc1.txt')
        self.assertEqual(success_result['status'], 'success')
        self.assertIn('artifact_path', success_result)
        
        # Check failure result
        failure_result = next(r for r in results if r['document'] == 'doc2.txt') 
        self.assertEqual(failure_result['status'], 'failed')
        self.assertIn('error', failure_result)
    
    def test_corpus_validation_before_analysis(self):
        """Test that corpus files are validated before starting analysis."""
        # Remove one corpus file to simulate missing file
        (self.corpus_dir / "doc2.txt").unlink()
        
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}},
                {'filename': 'doc2.txt', 'metadata': {'author': 'Author 2'}}
            ]
            
            # Should detect missing file during validation
            missing_files = self.orchestrator._validate_corpus_files_exist()
            
            self.assertIn('doc2.txt', missing_files)
            self.assertEqual(len(missing_files), 1)
    
    def test_experiment_config_structure(self):
        """Test that experiment config is properly structured for analysis agent."""
        with patch.object(self.orchestrator, '_load_corpus_documents') as mock_load_docs:
            mock_load_docs.return_value = [
                {'filename': 'doc1.txt', 'metadata': {'author': 'Author 1'}}
            ]
            
            with patch.object(self.orchestrator, '_find_corpus_file') as mock_find_file:
                mock_find_file.return_value = self.corpus_dir / "doc1.txt"
                
                with patch('discernus.core.clean_analysis_orchestrator.AnalysisAgent') as mock_agent_class:
                    mock_agent_class.return_value = self.mock_analysis_agent
                    
                    self.mock_analysis_agent.analyze_batch.return_value = {
                        "batch_id": "test",
                        "raw_analysis_response": "test"
                    }
                    
                    self.orchestrator._run_analysis_phase_individual(
                        analysis_model="test_model",
                        audit_logger=self.mock_audit_logger
                    )
        
        # Verify experiment config structure passed to analysis agent
        call_args, call_kwargs = self.mock_analysis_agent.analyze_batch.call_args_list[0]
        experiment_config = call_kwargs['experiment_config']
        
        self.assertIn('name', experiment_config)
        self.assertIn('description', experiment_config)
        self.assertIn('questions', experiment_config)
        self.assertEqual(experiment_config['name'], 'test_experiment')
        self.assertIsInstance(experiment_config['questions'], list)


# Helper methods to add to CleanAnalysisOrchestrator for testing
def _run_analysis_phase_individual(self, analysis_model: str, audit_logger) -> List[Dict[str, Any]]:
    """
    Individual document processing method (CORRECT PATTERN).
    This is what should replace the current batch processing method.
    """
    self._log_progress("📊 Starting individual document analysis...")
    
    framework_content = (self.experiment_path / self.config['framework']).read_text(encoding='utf-8')
    
    from discernus.agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
    analysis_agent = EnhancedAnalysisAgent(
        security_boundary=self.security,
        audit_logger=audit_logger,
        artifact_storage=self.artifact_storage
    )
    
    documents = self._load_corpus_documents()
    self._log_progress(f"📋 Analyzing {len(documents)} documents individually...")
    
    results = []
    for i, doc_manifest in enumerate(documents):
        doc_filename = doc_manifest.get('filename')
        if not doc_filename:
            self._log_progress(f"⚠️ Skipping document {i+1} due to missing filename in manifest.")
            continue
        
        # Find and load document
        doc_path = self._find_corpus_file(self.experiment_path / "corpus", doc_filename)
        if not doc_path.exists():
            self._log_progress(f"⚠️ Skipping missing document: {doc_filename}")
            results.append({"document": doc_filename, "status": "failed", "error": "File not found"})
            continue
        
        doc_content = doc_path.read_text(encoding='utf-8')
        doc_metadata = doc_manifest.get('metadata', {})
        
        self._log_progress(f"📄 Analyzing document {i+1}/{len(documents)}: {doc_filename}")
        
        try:
            # CRITICAL: Individual processing - single document per call
            analysis_data = analysis_agent.analyze_batch(
                framework_content=framework_content,
                corpus_documents=[{'filename': doc_filename, 'content': doc_content, 'metadata': doc_metadata}],
                experiment_config=self.config,
                model=analysis_model,
            )
            
            # Store individual artifact
            artifact_hash = self.artifact_storage.put_artifact(
                json.dumps(analysis_data).encode('utf-8'),
                {
                    'artifact_type': 'analysis_result',
                    'document_id': doc_manifest.get('document_id', doc_filename)
                }
            )
            
            results.append({
                "document": doc_filename,
                "artifact_hash": artifact_hash,
                "status": "success"
            })
            
        except Exception as e:
            self._log_progress(f"❌ Analysis failed for document {doc_filename}: {e}")
            results.append({"document": doc_filename, "status": "failed", "error": str(e)})
    
    successful_analyses = [r for r in results if r['status'] == 'success']
    self._log_progress(f"✅ Individual analysis complete: {len(successful_analyses)}/{len(documents)} documents processed.")
    
    return results


def _run_analysis_phase_batch(self, analysis_model: str, audit_logger) -> List[Dict[str, Any]]:
    """
    Batch processing method (INCORRECT PATTERN - FOR COMPARISON).
    This demonstrates the current broken approach.
    """
    self._log_progress("📊 Starting batch document analysis...")
    
    framework_content = (self.experiment_path / self.config['framework']).read_text(encoding='utf-8')
    
    from discernus.agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
    analysis_agent = EnhancedAnalysisAgent(
        security_boundary=self.security,
        audit_logger=audit_logger,
        artifact_storage=self.artifact_storage
    )
    
    documents = self._load_corpus_documents()
    self._log_progress(f"📋 Analyzing {len(documents)} documents in batch...")
    
    # Prepare ALL documents for batch processing (WRONG)
    prepared_documents = []
    for doc_manifest in documents:
        doc_filename = doc_manifest.get('filename')
        if not doc_filename:
            continue
        
        doc_path = self._find_corpus_file(self.experiment_path / "corpus", doc_filename)
        if not doc_path.exists():
            continue
        
        doc_content = doc_path.read_text(encoding='utf-8')
        prepared_documents.append({
            'filename': doc_filename,
            'content': doc_content,
            'metadata': doc_manifest.get('metadata', {})
        })
    
    try:
        # PROBLEM: Batch processing - ALL documents in one call
        analysis_result = analysis_agent.analyze_batch(
            framework_content=framework_content,
            corpus_documents=prepared_documents,  # ALL DOCUMENTS AT ONCE
            experiment_config=self.config,
            model=analysis_model
        )
        
        return [analysis_result]  # Single result for all documents
        
    except Exception as e:
        self._log_progress(f"❌ Batch analysis failed: {str(e)}")
        raise CleanAnalysisError(f"Analysis phase failed: {str(e)}")


# Add methods to CleanAnalysisOrchestrator for testing
CleanAnalysisOrchestrator._run_analysis_phase_individual = _run_analysis_phase_individual
CleanAnalysisOrchestrator._run_analysis_phase_batch = _run_analysis_phase_batch


if __name__ == '__main__':
    unittest.main()
