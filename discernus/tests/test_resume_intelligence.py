#!/usr/bin/env python3
"""
Test Suite: Intelligent Resume System
=====================================

Comprehensive tests for Issue #132 intelligent experiment resumption.
Tests all phases of the intelligent resumption pipeline:
1. State Discovery & Analysis  
2. Workflow Change Detection
3. Resource Validation
4. User Experience & Guidance
5. Provenance-Compliant Handoff

Tests follow patterns established in Issue #131.
"""

import unittest
import tempfile
import shutil
import json
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Test environment setup
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from discernus.core.experiment_lifecycle import ExperimentResumption, ResumeAnalysisResult
from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway


class TestResumeIntelligence(unittest.TestCase):
    """Test suite for intelligent experiment resumption functionality"""
    
    def setUp(self):
        """Set up test environment with mock project structure"""
        # Create temporary project directory
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_path = self.temp_dir / "test_project"
        self.project_path.mkdir()
        
        # Create basic experiment file
        self.experiment_file = self.project_path / "experiment.md"
        self.experiment_file.write_text(self._create_test_experiment_content())
        
        # Create framework file
        self.framework_file = self.project_path / "framework.md"
        self.framework_file.write_text(self._create_test_framework_content())
        
        # Create corpus directory
        self.corpus_dir = self.project_path / "corpus"
        self.corpus_dir.mkdir()
        (self.corpus_dir / "test_document.txt").write_text("Test corpus content.")
        
        # Initialize resumption system with mocked LLM components
        with patch('discernus.core.experiment_lifecycle.ModelRegistry'), \
             patch('discernus.core.experiment_lifecycle.LLMGateway'), \
             patch('discernus.core.experiment_lifecycle.TrueValidationAgent'), \
             patch('discernus.core.experiment_lifecycle.ProjectCoherenceAnalyst'):
            
            self.resumption = ExperimentResumption(str(self.project_path))
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_experiment_content(self) -> str:
        """Create realistic experiment.md content for testing"""
        return """# Test Experiment

## Experiment Configuration

```yaml
name: "Test Experiment for Resume Intelligence"
description: "Testing intelligent resumption capabilities"
framework_file: "framework.md"
corpus: "corpus"

workflow:
  - agent: "AnalysisAgent"
    model: "vertex_ai/gemini-2.5-pro"
    runs: 1
  - agent: "DataExtractionAgent" 
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "CalculationAgent"
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "SynthesisAgent"
    model: "vertex_ai/gemini-2.5-pro"
    runs: 1
```
"""
    
    def _create_test_framework_content(self) -> str:
        """Create minimal framework content for testing"""
        return """# Test Framework

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "Test Framework",
  "version": "1.0",
  "analysis_variants": {
    "primary": {
      "anchors": [
        {"id": "test_anchor_1", "label": "Test Concept 1"},
        {"id": "test_anchor_2", "label": "Test Concept 2"}
      ]
    }
  }
}
```
</details>
"""
    
    def _create_test_state_file(self, completed_steps: int = 1, session_path: str = None) -> Path:
        """Create realistic state file for testing"""
        # Create results directory structure
        results_dir = self.project_path / "results"
        results_dir.mkdir(exist_ok=True)
        
        session_name = session_path or "session_20250722_120000_abcd1234"
        session_dir = results_dir / session_name
        session_dir.mkdir(exist_ok=True)
        
        # Create state file content
        state_data = {
            "session_id": session_name,
            "session_results_path": f"results/{session_name}",
            "conversation_id": "conversation_20250722_120000_efgh5678",
            "framework_file": "framework.md",
            "corpus_path": "corpus",
            "workflow": [
                {"agent": "AnalysisAgent", "model": "vertex_ai/gemini-2.5-pro", "runs": 1},
                {"agent": "DataExtractionAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "CalculationAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "SynthesisAgent", "model": "vertex_ai/gemini-2.5-pro", "runs": 1}
            ],
            "analysis_results": {"test": "completed analysis data"}
        }
        
        # Create state file with appropriate name
        state_filename = f"state_after_step_{completed_steps}_{'AnalysisAgent' if completed_steps == 1 else 'DataExtractionAgent'}.json"
        state_file = session_dir / state_filename
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
        
        return state_file
    
    def test_state_discovery_finds_latest_file(self):
        """Test Phase 1: State Discovery - finds most recent state file"""
        # Create multiple state files with different timestamps
        older_file = self._create_test_state_file(1, "session_20250722_110000_old")
        newer_file = self._create_test_state_file(2, "session_20250722_130000_new")
        
        # Ensure newer file has later timestamp
        import time
        time.sleep(0.1)
        newer_file.touch()
        
        # Test discovery
        found_file = self.resumption._find_latest_state_file()
        self.assertEqual(found_file, newer_file)
        
    def test_state_discovery_handles_no_files(self):
        """Test Phase 1: State Discovery - handles missing state files gracefully"""
        found_file = self.resumption._find_latest_state_file()
        self.assertIsNone(found_file)
        
    def test_resume_step_determination_partial_file(self):
        """Test Phase 1: Resume Step Detection - handles partial state files"""
        workflow = [{"agent": "AnalysisAgent"}, {"agent": "DataExtractionAgent"}]
        
        # Test partial state file (should resume from same step)
        partial_file = self.project_path / "state_step_1_partial.json"
        step = self.resumption._determine_resume_step(partial_file, workflow)
        self.assertEqual(step, 1)
        
    def test_resume_step_determination_completed_file(self):
        """Test Phase 1: Resume Step Detection - handles completed state files"""
        workflow = [{"agent": "AnalysisAgent"}, {"agent": "DataExtractionAgent"}]
        
        # Test completed state file (should resume from next step)
        completed_file = self.project_path / "state_after_step_1_AnalysisAgent.json"
        step = self.resumption._determine_resume_step(completed_file, workflow)
        self.assertEqual(step, 2)
        
    def test_resume_step_determination_fallback(self):
        """Test Phase 1: Resume Step Detection - fallback to step 1"""
        workflow = [{"agent": "AnalysisAgent"}, {"agent": "DataExtractionAgent"}]
        
        # Test unrecognized filename (should fallback to step 1)
        unknown_file = self.project_path / "unknown_state_file.json"
        step = self.resumption._determine_resume_step(unknown_file, workflow)
        self.assertEqual(step, 1)
        
    def test_resource_validation_missing_framework(self):
        """Test Phase 2: Resource Validation - detects missing framework"""
        state_data = {"framework_file": "nonexistent_framework.md"}
        warnings = self.resumption._validate_resumption_resources(state_data)
        
        self.assertEqual(len(warnings), 1)
        self.assertIn("Framework file not found", warnings[0])
        
    def test_resource_validation_missing_corpus(self):
        """Test Phase 2: Resource Validation - detects missing corpus"""
        state_data = {"corpus_path": "nonexistent_corpus"}
        warnings = self.resumption._validate_resumption_resources(state_data)
        
        self.assertEqual(len(warnings), 1)
        self.assertIn("Corpus directory not found", warnings[0])
        
    def test_resource_validation_all_present(self):
        """Test Phase 2: Resource Validation - validates existing resources"""
        state_data = {
            "framework_file": "framework.md",
            "corpus_path": "corpus"
        }
        warnings = self.resumption._validate_resumption_resources(state_data)
        self.assertEqual(len(warnings), 0)
        
    def test_user_guidance_generation_continue(self):
        """Test Phase 3: User Guidance - generates appropriate continue message"""
        guidance = self.resumption._generate_user_guidance("continue", [], [])
        self.assertIn("Ready to resume", guidance)
        
    def test_user_guidance_generation_workflow_changed(self):
        """Test Phase 3: User Guidance - handles workflow changes"""
        workflow_changes = ["Step 1 agent changed: was AnalysisAgent, now AnalysisAgent"]
        guidance = self.resumption._generate_user_guidance("workflow_changed", workflow_changes, [])
        
        self.assertIn("Workflow changes detected", guidance)
        self.assertIn("Step 1 agent changed", guidance)
        
    def test_user_guidance_generation_resource_warnings(self):
        """Test Phase 3: User Guidance - handles resource warnings"""
        resource_warnings = ["Framework file not found: missing_framework.md"]
        guidance = self.resumption._generate_user_guidance("resource_warnings", [], resource_warnings)
        
        self.assertIn("Resource warnings detected", guidance)
        self.assertIn("Framework file not found", guidance)


class TestResumeAnalysisIntegration(unittest.TestCase):
    """Integration tests for complete resume analysis pipeline"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_path = self.temp_dir / "integration_test_project"
        self.project_path.mkdir()
        
        # Create complete project structure
        self._setup_complete_project()
        
        # Initialize resumption system with mocked LLM components
        with patch('discernus.core.experiment_lifecycle.ModelRegistry'), \
             patch('discernus.core.experiment_lifecycle.LLMGateway'), \
             patch('discernus.core.experiment_lifecycle.TrueValidationAgent'), \
             patch('discernus.core.experiment_lifecycle.ProjectCoherenceAnalyst'):
            
            self.resumption = ExperimentResumption(str(self.project_path))
    
    def tearDown(self):
        """Clean up integration test environment"""
        shutil.rmtree(self.temp_dir)
    
    def _setup_complete_project(self):
        """Set up complete project with experiment, framework, corpus, and state"""
        # Create experiment file
        experiment_content = """# Integration Test Experiment

## Experiment Configuration

```yaml
name: "Integration Test"
framework_file: "framework.md"
corpus: "corpus"

workflow:
  - agent: "AnalysisAgent"
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "DataExtractionAgent"
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "SynthesisAgent"
    model: "vertex_ai/gemini-2.5-pro"
```
"""
        (self.project_path / "experiment.md").write_text(experiment_content)
        
        # Create framework file
        framework_content = """# Integration Test Framework

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "Integration Framework",
  "version": "1.0",
  "analysis_variants": {
    "primary": {
      "anchors": [
        {"id": "integration_anchor", "label": "Integration Test Concept"}
      ]
    }
  }
}
```
</details>
"""
        (self.project_path / "framework.md").write_text(framework_content)
        
        # Create corpus
        corpus_dir = self.project_path / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "test_doc.txt").write_text("Integration test corpus content.")
        
        # Create state file
        self._create_integration_state_file()
    
    def _create_integration_state_file(self):
        """Create realistic state file for integration testing"""
        results_dir = self.project_path / "results"
        results_dir.mkdir()
        session_dir = results_dir / "session_20250722_140000_integration"
        session_dir.mkdir()
        
        state_data = {
            "session_id": "session_20250722_140000_integration",
            "session_results_path": "results/session_20250722_140000_integration",
            "conversation_id": "conversation_20250722_140000_test",
            "framework_file": "framework.md",
            "corpus_path": "corpus",
            "workflow": [
                {"agent": "AnalysisAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "DataExtractionAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "SynthesisAgent", "model": "vertex_ai/gemini-2.5-pro"}
            ],
            "analysis_results": {"integration": "test analysis data"}
        }
        
        state_file = session_dir / "state_after_step_1_AnalysisAgent.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
    
    def test_analyze_resumption_context_success(self):
        """Integration Test: Complete successful resumption analysis"""
        async def run_test():
            result = await self.resumption._analyze_resumption_context(None, None)
            
            # Verify analysis result structure
            self.assertIsInstance(result, ResumeAnalysisResult)
            self.assertTrue(result.can_resume)
            self.assertTrue(result.state_integrity)
            self.assertEqual(result.resume_step, 2)  # Should resume from step 2
            self.assertEqual(result.total_steps, 3)
            self.assertEqual(len(result.completed_steps), 1)  # AnalysisAgent completed
            self.assertEqual(len(result.remaining_steps), 2)  # DataExtractionAgent and SynthesisAgent remain
            
        asyncio.run(run_test())
    
    def test_analyze_resumption_context_no_state_files(self):
        """Integration Test: Handles missing state files gracefully"""
        # Remove results directory to simulate no state files
        shutil.rmtree(self.project_path / "results")
        
        async def run_test():
            result = await self.resumption._analyze_resumption_context(None, None)
            
            self.assertFalse(result.can_resume)
            self.assertEqual(result.resumption_strategy, "no_state_found")
            self.assertIn("No state files found", result.user_guidance)
            
        asyncio.run(run_test())
    
    def test_analyze_resumption_context_corrupted_state(self):
        """Integration Test: Handles corrupted state files"""
        # Create corrupted state file
        results_dir = self.project_path / "results"
        session_dir = results_dir / "session_corrupted"
        session_dir.mkdir(exist_ok=True, parents=True)
        
        corrupted_file = session_dir / "state_after_step_1_AnalysisAgent.json"
        corrupted_file.write_text("{ invalid json content")
        
        async def run_test():
            result = await self.resumption._analyze_resumption_context(None, None)
            
            self.assertFalse(result.can_resume)
            self.assertEqual(result.resumption_strategy, "corrupted_state")
            self.assertIn("corrupted or unreadable", result.user_guidance)
            
        asyncio.run(run_test())
        
    def test_workflow_change_detection_no_changes(self):
        """Integration Test: Workflow change detection - no changes"""
        state_data = {
            "workflow": [
                {"agent": "AnalysisAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "DataExtractionAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "SynthesisAgent", "model": "vertex_ai/gemini-2.5-pro"}
            ]
        }
        
        async def run_test():
            changes = await self.resumption._detect_workflow_changes(state_data)
            # Should detect no changes since experiment.md matches state
            self.assertEqual(len(changes), 0)
            
        asyncio.run(run_test())
    
    def test_workflow_change_detection_agent_changes(self):
        """Integration Test: Workflow change detection - agent changes"""
        # Modify experiment file to have different agents
        modified_experiment = """# Modified Integration Test Experiment

## Experiment Configuration

```yaml
name: "Modified Integration Test"
framework_file: "framework.md"
corpus: "corpus"

workflow:
  - agent: "AnalysisAgent"  # Changed from AnalysisAgent
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "DataExtractionAgent"
    model: "vertex_ai/gemini-2.5-pro"
  - agent: "SynthesisAgent"
    model: "vertex_ai/gemini-2.5-pro"
```
"""
        (self.project_path / "experiment.md").write_text(modified_experiment)
        
        state_data = {
            "workflow": [
                {"agent": "AnalysisAgent", "model": "vertex_ai/gemini-2.5-pro"},  # Original agent
                {"agent": "DataExtractionAgent", "model": "vertex_ai/gemini-2.5-pro"},
                {"agent": "SynthesisAgent", "model": "vertex_ai/gemini-2.5-pro"}
            ]
        }
        
        async def run_test():
            changes = await self.resumption._detect_workflow_changes(state_data)
            
            # Should detect the agent change
            self.assertTrue(len(changes) > 0)
            self.assertTrue(any("agent changed" in change for change in changes))
            
        asyncio.run(run_test())


class TestResumeExecutionIntegration(unittest.TestCase):
    """Integration tests for resume execution and WorkflowOrchestrator handoff"""
    
    def setUp(self):
        """Set up execution integration test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_path = self.temp_dir / "execution_test_project"
        self.project_path.mkdir()
        
        # Create minimal project structure
        self._setup_execution_project()
        
        # Initialize resumption system with mocked LLM components
        with patch('discernus.core.experiment_lifecycle.ModelRegistry'), \
             patch('discernus.core.experiment_lifecycle.LLMGateway'), \
             patch('discernus.core.experiment_lifecycle.TrueValidationAgent'), \
             patch('discernus.core.experiment_lifecycle.ProjectCoherenceAnalyst'):
            
            self.resumption = ExperimentResumption(str(self.project_path))
    
    def tearDown(self):
        """Clean up execution test environment"""
        shutil.rmtree(self.temp_dir)
    
    def _setup_execution_project(self):
        """Set up project for execution testing"""
        # Create basic files
        (self.project_path / "experiment.md").write_text("# Test\n```yaml\nworkflow:\n  - agent: AnalysisAgent\n```")
        (self.project_path / "framework.md").write_text("# Framework")
        
        corpus_dir = self.project_path / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "test.txt").write_text("Test content")
        
        # Create state file
        results_dir = self.project_path / "results"
        results_dir.mkdir()
        session_dir = results_dir / "session_execution_test"
        session_dir.mkdir()
        
        state_data = {
            "session_id": "session_execution_test",
            "session_results_path": "results/session_execution_test",
            "workflow": [{"agent": "AnalysisAgent"}],
            "framework_file": "framework.md",
            "corpus_path": "corpus"
        }
        
        state_file = session_dir / "state_after_step_1_AnalysisAgent.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
    
    @patch('discernus.core.experiment_lifecycle.WorkflowOrchestrator')
    def test_execute_resumption_with_provenance(self, mock_orchestrator_class):
        """Integration Test: Execute resumption with provenance audit trail"""
        # Setup mock orchestrator
        mock_orchestrator = Mock()
        mock_orchestrator.project_path = str(self.project_path)
        mock_orchestrator.session_results_path = self.project_path / "results" / "session_execution_test"
        mock_orchestrator.session_id = "session_execution_test"
        mock_orchestrator.workflow_state = {}
        mock_orchestrator._execute_step = Mock(return_value={"step_output": "test"})
        mock_orchestrator._save_state_snapshot = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Create analysis result
        analysis = ResumeAnalysisResult(
            can_resume=True,
            state_file=self.project_path / "results" / "session_execution_test" / "state_after_step_1_AnalysisAgent.json",
            resume_step=2,
            total_steps=2,
            workflow_changes=[],
            resource_warnings=[],
            resumption_strategy="continue",
            user_guidance="Ready to resume",
            state_integrity=True,
            completed_steps=["Step 1: AnalysisAgent"],
            remaining_steps=["Step 2: SynthesisAgent"]
        )
        
        workflow_steps = [
            {"agent": "AnalysisAgent"},
            {"agent": "SynthesisAgent"}
        ]
        
        state_data = {"session_results_path": "results/session_execution_test"}
        
        # Execute resumption with provenance
        result = self.resumption._execute_resumption_with_provenance(
            mock_orchestrator, state_data, 2, workflow_steps, analysis
        )
        
        # Verify results
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["session_id"], "session_execution_test")
        self.assertTrue(result["intelligent_resumption"])
        self.assertIn("resumption_audit", result)
        
        # Verify audit trail was created
        audit_data = result["resumption_audit"]
        self.assertEqual(audit_data["resume_step"], 2)
        self.assertEqual(audit_data["resumption_strategy"], "continue")
        self.assertTrue(audit_data["intelligent_analysis"])
        
        # Verify orchestrator was called correctly
        mock_orchestrator._execute_step.assert_called_once()
        mock_orchestrator._save_state_snapshot.assert_called_once()


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2) 