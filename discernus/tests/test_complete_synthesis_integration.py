#!/usr/bin/env python3
"""
Complete Synthesis Integration Test
==================================

Tests that synthesis produces reports with:
1. Actual evidence quotes (not placeholders)
2. Corpus document awareness
3. Complete research data integration

This test should FAIL initially and pass after implementing the fix.
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

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator


class TestCompleteSynthesisIntegration(unittest.TestCase):
    """Integration test for complete synthesis with evidence and corpus awareness."""
    
    def setUp(self):
        """Set up test experiment directory with real content."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.experiment_path = self.temp_dir / "test_experiment"
        self.experiment_path.mkdir(parents=True)
        
        # Create realistic framework content
        framework_content = """# Test Framework v1.0

## Part 1: The Scholarly Document

This framework analyzes civic discourse patterns.

## Part 2: The Machine-Readable Appendix

```yaml
name: "Test Framework"
version: "1.0"
dimensions:
  - name: "truth"
    description: "Truth vs manipulation"
  - name: "justice" 
    description: "Justice vs resentment"
```
"""
        
        # Create realistic experiment content
        experiment_content = """# Test Experiment

## Research Objectives

Analyze civic character patterns in political discourse.

## Configuration Appendix

```yaml
name: "test_civic_analysis"
framework: "framework.md"
corpus: "corpus"
questions:
  - "What civic virtues are present?"
  - "How do speakers balance competing values?"
```
"""
        
        # Write files
        (self.experiment_path / "framework.md").write_text(framework_content)
        (self.experiment_path / "experiment.md").write_text(experiment_content)
        
        # Create corpus directory with sample documents
        corpus_dir = self.experiment_path / "corpus"
        corpus_dir.mkdir()
        
        (corpus_dir / "speech1.txt").write_text("We must pursue justice and truth in our democracy.")
        (corpus_dir / "speech2.txt").write_text("The people deserve honest leadership and fair treatment.")
        
        # Mock audit logger
        self.mock_audit_logger = Mock()
    
    def tearDown(self):
        """Clean up test files."""
        shutil.rmtree(self.temp_dir)
    
    def test_synthesis_includes_actual_evidence_quotes(self):
        """Test that synthesis report contains actual evidence quotes, not placeholders."""
        
        # Create orchestrator and initialize it properly
        orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
        orchestrator.config = {"framework": "framework.md"}
        
        # Mock the statistical analysis to return realistic data
        mock_statistical_results = {
            "statistical_data": {
                "descriptive_statistics": {"mean_truth": 0.75, "mean_justice": 0.68},
                "correlation_analysis": {"truth_justice_correlation": 0.45}
            },
            "status": "completed"
        }
        
        # Mock analysis results with evidence
        mock_analysis_results = [
            {
                "document_name": "speech1.txt",
                "analysis_result": {"truth": 0.8, "justice": 0.7},
                "evidence_data": [
                    {
                        "quote_text": "We must pursue justice and truth in our democracy.",
                        "dimension": "truth",
                        "confidence": 0.9,
                        "document_name": "speech1.txt"
                    }
                ]
            },
            {
                "document_name": "speech2.txt", 
                "analysis_result": {"truth": 0.7, "justice": 0.65},
                "evidence_data": [
                    {
                        "quote_text": "The people deserve honest leadership and fair treatment.",
                        "dimension": "justice",
                        "confidence": 0.85,
                        "document_name": "speech2.txt"
                    }
                ]
            }
        ]
        
        # Mock the orchestrator methods and synthesis agent
        with patch.object(orchestrator, '_run_statistical_analysis', return_value=mock_statistical_results), \
             patch.object(orchestrator, '_load_corpus_documents', return_value=[{"filename": "speech1.txt"}, {"filename": "speech2.txt"}]), \
             patch.object(orchestrator, '_run_analysis_phase', return_value=mock_analysis_results), \
             patch.object(orchestrator, '_build_rag_index'), \
             patch('discernus.core.reuse_candidates.unified_synthesis_agent.UnifiedSynthesisAgent') as mock_agent_class:
            
            # Mock synthesis agent to return report with evidence (what we expect after fix)
            mock_agent = Mock()
            mock_agent.generate_final_report.return_value = {
                "final_report": "# Test Report\n\nAs stated in speech1.txt: 'We must pursue justice and truth in our democracy.' This demonstrates high truth scores."
            }
            mock_agent_class.return_value = mock_agent
            
            # Run synthesis
            try:
                result = orchestrator._run_synthesis(
                    synthesis_model="test_model",
                    audit_logger=self.mock_audit_logger,
                    statistical_results=mock_statistical_results
                )
                
                # Get the final report
                final_report = result.get("synthesis_result", {}).get("final_report", "")
                
                # ASSERTIONS - These should FAIL initially
                
                # 1. Report should contain actual evidence quotes
                self.assertIn("We must pursue justice and truth in our democracy", final_report,
                             "Report should contain actual evidence quotes, not placeholders")
                
                # 2. Report should mention specific corpus documents
                self.assertIn("speech1.txt", final_report,
                             "Report should mention specific corpus documents by name")
                
                # 3. Report should not contain placeholder text
                self.assertNotIn("Evidence from document", final_report,
                                "Report should not contain placeholder evidence text")
                
                # 4. Report should show corpus awareness
                self.assertIn("corpus", final_report.lower(),
                             "Report should demonstrate awareness of what corpus was analyzed")
                
            except Exception as e:
                self.fail(f"Synthesis failed with error: {e}")
    
    def test_synthesis_receives_complete_research_data(self):
        """Test that synthesis agent receives complete research data structure."""
        
        # This test verifies the data structure matches the deprecated orchestrator pattern
        orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
        orchestrator.config = {"framework": "framework.md"}
        
        # Mock analysis results
        mock_analysis_results = [
            {"document_name": "speech1.txt", "analysis_result": {"truth": 0.8}},
            {"document_name": "speech2.txt", "analysis_result": {"truth": 0.7}}
        ]
        
        mock_statistical_results = {
            "statistical_data": {"descriptive_statistics": {"mean_truth": 0.75}},
            "status": "completed"
        }
        
        # Capture what gets passed to synthesis agent
        captured_research_data = {}
        
        def capture_synthesis_call(*args, **kwargs):
            # Capture the research data that gets passed
            research_data_hash = kwargs.get('research_data_artifact_hash')
            if research_data_hash and hasattr(orchestrator, 'artifact_storage'):
                try:
                    data_content = orchestrator.artifact_storage.get_artifact(research_data_hash)
                    captured_research_data.update(json.loads(data_content.decode('utf-8')))
                except:
                    pass
            return {"final_report": "Mock report"}
        
        with patch.object(orchestrator, '_run_statistical_analysis', return_value=mock_statistical_results), \
             patch.object(orchestrator, '_load_corpus_documents', return_value=[{"filename": "speech1.txt"}]), \
             patch.object(orchestrator, '_run_analysis_phase', return_value=mock_analysis_results), \
             patch.object(orchestrator, '_build_rag_index'), \
             patch('discernus.core.reuse_candidates.unified_synthesis_agent.UnifiedSynthesisAgent') as mock_agent_class:
            
            mock_agent = Mock()
            mock_agent.generate_final_report.side_effect = capture_synthesis_call
            mock_agent_class.return_value = mock_agent
            
            # Run synthesis
            orchestrator._run_synthesis(
                synthesis_model="test_model",
                audit_logger=self.mock_audit_logger,
                statistical_results=mock_statistical_results
            )
            
            # ASSERTIONS - These should FAIL initially
            
            # 1. Should have complete research data structure
            self.assertIn('experiment_metadata', captured_research_data,
                         "Research data should include experiment metadata")
            
            # 2. Should include raw analysis data
            self.assertIn('raw_analysis_data', captured_research_data,
                         "Research data should include raw analysis data")
            
            # 3. Should include derived metrics
            self.assertIn('derived_metrics_data', captured_research_data,
                         "Research data should include derived metrics data")
            
            # 4. Should include statistical results
            self.assertIn('statistical_results', captured_research_data,
                         "Research data should include statistical results")


if __name__ == '__main__':
    unittest.main()
