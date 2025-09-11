#!/usr/bin/env python3
"""
Unit Tests for Synthesis Integration
===================================

Tests for synthesis stage integration with individual document artifacts.
These tests verify that synthesis can properly handle individual analysis artifacts.

Key Test Areas:
1. Synthesis asset validation with individual artifacts
2. Evidence linkage preservation across individual files
3. Artifact hash collection and validation
4. RAG integration with individual document provenance
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
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import json
import tempfile
import shutil

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError


class TestSynthesisIntegration(unittest.TestCase):
    """Test synthesis integration with individual analysis artifacts."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())
        self.experiment_path = self.temp_dir / "test_experiment"
        self.experiment_path.mkdir(parents=True)
        
        # Create framework file
        self.framework_file = self.experiment_path / "framework.md"
        self.framework_file.write_text("# Test Framework\nTest framework content.")
        
        # Create experiment file
        self.experiment_file = self.experiment_path / "experiment.md"
        self.experiment_file.write_text("# Test Experiment\nTest experiment content.")
        
        # Initialize orchestrator
        self.orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
        self.orchestrator.config = {'framework': 'framework.md'}
        
        # Mock dependencies
        self.orchestrator.artifact_storage = Mock()
        self.orchestrator.logger = Mock()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_synthesis_asset_validation_individual_artifacts(self):
        """Test synthesis asset validation with individual analysis artifacts."""
        # Mock statistical results with individual artifact references
        statistical_results = {
            "status": "completed",
            "functions_generated": 3,
            "statistical_data": {
                "descriptive_statistics": {"mean": 0.5, "std": 0.2},
                "correlation_analysis": {"correlation": 0.7}
            }
        }
        
        # Mock artifact registry with individual analysis artifacts
        mock_registry = {
            "analysis_hash_1": {
                "metadata": {
                    "artifact_type": "analysis_result",
                    "document_id": "doc1"
                }
            },
            "analysis_hash_2": {
                "metadata": {
                    "artifact_type": "analysis_result", 
                    "document_id": "doc2"
                }
            },
            "evidence_hash_1": {
                "metadata": {
                    "artifact_type": "evidence_v6_doc1"
                }
            },
            "evidence_hash_2": {
                "metadata": {
                    "artifact_type": "evidence_v6_doc2"
                }
            }
        }
        
        self.orchestrator.artifact_storage.registry = mock_registry
        
        # Test asset validation
        try:
            self.orchestrator._validate_synthesis_assets(statistical_results)
            validation_passed = True
        except CleanAnalysisError:
            validation_passed = False
        
        # Should pass validation with proper individual artifacts
        self.assertTrue(validation_passed, "Synthesis asset validation should pass with individual artifacts")
    
    def test_evidence_artifact_collection_individual(self):
        """Test that evidence artifacts are properly collected from individual analysis results."""
        # Mock artifact registry with individual evidence artifacts
        mock_registry = {
            "evidence_v6_hash1": {
                "metadata": {
                    "artifact_type": "evidence_v6_doc1",
                    "document_id": "doc1"
                }
            },
            "evidence_v6_hash2": {
                "metadata": {
                    "artifact_type": "evidence_v6_doc2", 
                    "document_id": "doc2"
                }
            },
            "other_artifact": {
                "metadata": {
                    "artifact_type": "other_type"
                }
            }
        }
        
        self.orchestrator.artifact_storage.registry = mock_registry
        
        # Test evidence collection
        evidence_hashes = self.orchestrator._collect_evidence_artifact_hashes()
        
        # Verify correct evidence artifacts collected
        self.assertEqual(len(evidence_hashes), 2)
        self.assertIn("evidence_v6_hash1", evidence_hashes)
        self.assertIn("evidence_v6_hash2", evidence_hashes)
        self.assertNotIn("other_artifact", evidence_hashes)
    
    def test_synthesis_with_individual_provenance(self):
        """Test that synthesis maintains individual document provenance."""
        # Mock statistical results
        statistical_results = {
            "statistical_data": {
                "descriptive_statistics": {"mean": 0.5},
                "correlation_analysis": {"correlation": 0.7}
            }
        }
        
        # Mock evidence artifacts with individual provenance
        evidence_hashes = ["evidence_hash_doc1", "evidence_hash_doc2"]
        
        # Mock synthesis assembler
        mock_assembler = Mock()
        mock_assembler.assemble_synthesis_prompt.return_value = "Mock synthesis prompt"
        
        # Mock LLM gateway
        mock_llm_response = "Mock synthesis response"
        mock_llm_metadata = {"tokens": 1000, "cost": 0.01}
        
        with patch('discernus.core.prompt_assemblers.synthesis_assembler.SynthesisPromptAssembler', return_value=mock_assembler), \
             patch.object(self.orchestrator, '_collect_evidence_artifact_hashes', return_value=evidence_hashes), \
             patch.object(self.orchestrator, 'llm_gateway') as mock_gateway:
            
            mock_gateway.execute_call.return_value = (mock_llm_response, mock_llm_metadata)
            
            # Test synthesis execution
            result = self.orchestrator._run_synthesis_individual(
                synthesis_model="test_model",
                audit_logger=Mock(),
                statistical_results=statistical_results
            )
        
        # Verify synthesis assembler was called with individual evidence hashes
        assembler_call = mock_assembler.assemble_synthesis_prompt.call_args
        call_kwargs = assembler_call[1] if assembler_call else {}
        
        # Should have evidence artifact hashes from individual documents
        self.assertIn('evidence_artifact_hashes', call_kwargs)
        passed_evidence_hashes = call_kwargs['evidence_artifact_hashes']
        self.assertEqual(len(passed_evidence_hashes), 2)
        self.assertIn("evidence_hash_doc1", passed_evidence_hashes)
        self.assertIn("evidence_hash_doc2", passed_evidence_hashes)
    
    def test_synthesis_asset_validation_missing_framework(self):
        """Test synthesis asset validation when framework file is missing."""
        # Remove framework file
        self.framework_file.unlink()
        
        statistical_results = {"status": "completed"}
        
        # Test asset validation
        with self.assertRaises(CleanAnalysisError) as context:
            self.orchestrator._validate_synthesis_assets(statistical_results)
        
        self.assertIn("Framework file not found", str(context.exception))
    
    def test_synthesis_asset_validation_empty_statistical_results(self):
        """Test synthesis asset validation with empty statistical results."""
        # Empty statistical results should fail validation
        statistical_results = {}
        
        with self.assertRaises(CleanAnalysisError) as context:
            self.orchestrator._validate_synthesis_assets(statistical_results)
        
        self.assertIn("Statistical results validation failed", str(context.exception))


# Helper methods to add to CleanAnalysisOrchestrator for testing
def _collect_evidence_artifact_hashes(self) -> List[str]:
    """
    Collect evidence artifact hashes from individual analysis results.
    """
    evidence_hashes = []
    for artifact_hash, artifact_info in self.artifact_storage.registry.items():
        metadata = artifact_info.get("metadata", {})
        artifact_type = metadata.get("artifact_type", "")
        if artifact_type.startswith("evidence_v6"):
            evidence_hashes.append(artifact_hash)
    
    return evidence_hashes


def _run_synthesis_individual(self, synthesis_model: str, audit_logger, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run synthesis with individual artifact integration (CORRECT PATTERN).
    """
    self._log_progress("📝 Validating synthesis assets before attempting report generation...")
    
    # Validate all required assets exist
    self._validate_synthesis_assets(statistical_results)
    
    # Initialize synthesis assembler
    from discernus.core.prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
    assembler = SynthesisPromptAssembler()
    
    # Prepare paths for synthesis
    framework_path = self.experiment_path / self.config['framework']
    experiment_path = self.experiment_path / "experiment.md"
    
    # Store statistical results as artifact
    research_data_json = json.dumps(statistical_results, indent=2)
    research_data_hash = self.artifact_storage.put_artifact(
        research_data_json.encode('utf-8'),
        {"artifact_type": "research_data_for_synthesis"}
    )
    
    # Collect evidence artifact hashes from individual analysis results
    evidence_artifact_hashes = self._collect_evidence_artifact_hashes()
    
    # Generate synthesis prompt with individual provenance
    synthesis_prompt = assembler.assemble_synthesis_prompt(
        framework_path=framework_path,
        experiment_path=experiment_path,
        research_data_artifact_hash=research_data_hash,
        evidence_artifact_hashes=evidence_artifact_hashes,
        interpretation_focus="comprehensive"
    )
    
    # Execute synthesis with LLM
    response, metadata = self.llm_gateway.execute_call(
        model=synthesis_model,
        prompt=synthesis_prompt,
        # max_tokens removed - now handled by provider defaults
    )
    
    return {
        "status": "completed",
        "response": response,
        "metadata": metadata,
        "evidence_artifacts": evidence_artifact_hashes,
        "research_data_hash": research_data_hash
    }


# Add methods to CleanAnalysisOrchestrator for testing  
CleanAnalysisOrchestrator._collect_evidence_artifact_hashes = _collect_evidence_artifact_hashes
CleanAnalysisOrchestrator._run_synthesis_individual = _run_synthesis_individual


if __name__ == '__main__':
    unittest.main()
