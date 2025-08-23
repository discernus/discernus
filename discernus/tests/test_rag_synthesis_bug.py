#!/usr/bin/env python3
"""
Unit Test for RAG Synthesis Bug
===============================

Reproduces the "tuple indices must be integers or slices, not str" error
that occurs when UnifiedSynthesisAgent tries to process txtai search results.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from discernus.core.reuse_candidates.unified_synthesis_agent import UnifiedSynthesisAgent


class TestRAGSynthesisBug(unittest.TestCase):
    """Test to reproduce and fix the RAG synthesis tuple indexing bug."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create mock files
        self.framework_path = self.temp_dir / "framework.md"
        self.framework_path.write_text("# Test Framework\nTest content")
        
        self.experiment_path = self.temp_dir / "experiment.md"
        self.experiment_path.write_text("# Test Experiment\nTest content")
        
        # Mock audit logger
        self.mock_audit_logger = Mock()
        
        # Mock artifact storage
        self.mock_artifact_storage = Mock()
        self.mock_artifact_storage.put_artifact.return_value = "mock_hash"
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_rag_synthesis_handles_tuples_correctly(self):
        """Test that RAG synthesis now correctly handles txtai tuple results (bug was fixed)."""
        
        # Create agent
        agent = UnifiedSynthesisAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=self.mock_audit_logger
        )
        
        # Create mock RAG index that returns tuples (like real txtai)
        mock_rag_index = Mock()
        # This is what txtai actually returns: list of (id, score) tuples
        mock_rag_index.search.return_value = [
            ("doc_id_1", 0.85),
            ("doc_id_2", 0.72)
        ]
        
        # Mock the synthesis assembler to avoid file system dependencies
        mock_assembler = Mock()
        mock_assembler.assemble_prompt.return_value = "Mock synthesis prompt"
        
        # Mock the LLM gateway to prevent actual API calls
        with patch.object(agent.llm_gateway, 'execute_call', return_value=("Mock report", {})), \
             patch('discernus.core.reuse_candidates.unified_synthesis_agent.SynthesisPromptAssembler', return_value=mock_assembler):
            
            # This should now work without errors (the bug has been fixed)
            result = agent.generate_final_report(
                framework_path=self.framework_path,
                experiment_path=self.experiment_path,
                research_data_artifact_hash="mock_hash",
                rag_index=mock_rag_index,
                artifact_storage=self.mock_artifact_storage
            )
        
        # Verify we get a proper result (no more tuple indexing error)
        self.assertIn("final_report", result)
        self.assertEqual(result["final_report"], "Mock report")
        
        # Verify the RAG index was called properly
        mock_rag_index.search.assert_called_once_with(query="general context", limit=5)
    
    def test_rag_synthesis_with_proper_handling(self):
        """Test that RAG synthesis works when txtai results are handled properly."""
        
        # Create agent
        agent = UnifiedSynthesisAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=self.mock_audit_logger
        )
        
        # Create mock RAG index that returns tuples (like real txtai)
        mock_rag_index = Mock()
        # This should now work with the fix - tuples are handled properly
        mock_rag_index.search.return_value = [
            ("doc_id_1", 0.85),
            ("doc_id_2", 0.72)
        ]
        
        # Mock the synthesis assembler
        mock_assembler = Mock()
        mock_assembler.assemble_prompt.return_value = "Mock synthesis prompt"
        
        # Mock the LLM gateway
        with patch.object(agent.llm_gateway, 'execute_call', return_value=("Mock report", {})), \
             patch('discernus.core.reuse_candidates.unified_synthesis_agent.SynthesisPromptAssembler', return_value=mock_assembler):
            
            # This should work without errors now that tuples are handled properly
            result = agent.generate_final_report(
                framework_path=self.framework_path,
                experiment_path=self.experiment_path,
                research_data_artifact_hash="mock_hash",
                rag_index=mock_rag_index,
                artifact_storage=self.mock_artifact_storage
            )
        
        # Verify we get a proper result
        self.assertIn("final_report", result)
        self.assertEqual(result["final_report"], "Mock report")
        
        # Verify the RAG index was called
        mock_rag_index.search.assert_called_once_with(query="general context", limit=5)


if __name__ == '__main__':
    unittest.main()
