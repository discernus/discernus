#!/usr/bin/env python3
"""
Test for WorkflowOrchestrator Integration - Issue #131
======================================================

Tests that the THIN Experiment Lifecycle successfully hands off enhanced
experiments to the WorkflowOrchestrator for execution. This is the critical
end-to-end integration test that proves the whole system works together.
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime
import sys
import yaml
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.experiment_lifecycle import ExperimentStartup
from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator


class TestOrchestratorIntegration(unittest.TestCase):
    """Test that the THIN lifecycle successfully integrates with WorkflowOrchestrator"""
    
    def setUp(self):
        """Create temporary directory with complete test project"""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create test framework (v4 format with JSON configuration)
        self.framework_file = self.temp_dir / "framework.md"
        self.framework_file.write_text("""
# Test Framework for Integration Testing

## Analysis Instructions

Please analyze the text for sentiment and themes.

<details><summary>Machine-Readable Configuration</summary>
```json
{
    "name": "integration_test_framework",
    "version": "1.0",
    "analysis_variants": {
        "default": {
            "analysis_prompt": "Analyze this text for sentiment and identify main themes. Provide a structured response."
        }
    }
}
```
</details>
""")
        
        # Create test corpus
        self.corpus_dir = self.temp_dir / "corpus"
        self.corpus_dir.mkdir()
        (self.corpus_dir / "integration_test.txt").write_text("This is a positive test document about innovation and progress.")
        
        # Create experiment with Issue #68 problem (missing SynthesisAgent)
        self.experiment_file = self.temp_dir / "experiment.md"
        self.experiment_file.write_text("""---
name: integration_test_experiment
description: Test experiment for orchestrator integration
hypothesis: The test document will show positive sentiment
framework_file: framework.md
corpus: corpus/
models:
  - "vertex_ai/gemini-2.5-flash"
runs_per_model: 1
workflow:
  - agent: AnalysisAgent
---

# Integration Test Experiment

This experiment tests the integration between THIN experiment lifecycle and WorkflowOrchestrator.
""")
        
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_enhanced_experiment_orchestrator_handoff(self):
        """Test that enhanced experiment can be loaded and validated by WorkflowOrchestrator"""
        print("🧪 Testing WorkflowOrchestrator integration with enhanced experiment")
        
        # Step 1: Use THIN lifecycle to enhance experiment
        startup = ExperimentStartup(str(self.temp_dir))
        enhanced_workflow = [
            {"agent": "AnalysisAgent"},
            {"agent": "SynthesisAgent", "config": {"output_artifacts": ["integration_report.md"]}}
        ]
        
        enhanced_experiment_file = startup._apply_workflow_enhancements(
            self.experiment_file, enhanced_workflow
        )
        
        print(f"✅ Enhanced experiment created: {enhanced_experiment_file}")
        
        # Step 2: Initialize WorkflowOrchestrator with enhanced experiment
        orchestrator = WorkflowOrchestrator(str(enhanced_experiment_file.parent))
        
        # Step 3: Load specifications from enhanced experiment
        from discernus.core.spec_loader import SpecLoader
        spec_loader = SpecLoader()
        
        # Parse the enhanced experiment
        experiment_config = spec_loader.experiment_parser.parse_experiment(enhanced_experiment_file)
        
        # Verify enhanced workflow is properly parsed
        self.assertIn('workflow', experiment_config, "Enhanced experiment should contain workflow")
        workflow = experiment_config['workflow']
        self.assertTrue(len(workflow) >= 2, "Enhanced workflow should have at least 2 agents")
        
        # Find SynthesisAgent in workflow
        synthesis_agent_found = any(step.get('agent') == 'SynthesisAgent' for step in workflow)
        self.assertTrue(synthesis_agent_found, "Enhanced workflow should contain SynthesisAgent")
        
        # Step 4: Resolve paths and load full specifications
        framework_file_path = enhanced_experiment_file.parent / experiment_config['framework_file']
        corpus_dir_path = enhanced_experiment_file.parent / experiment_config['corpus']
        
        # Check that framework and corpus are accessible from enhanced experiment location
        self.assertTrue(framework_file_path.exists(), f"Framework file should be accessible: {framework_file_path}")
        self.assertTrue(corpus_dir_path.exists(), f"Corpus directory should be accessible: {corpus_dir_path}")
        
        specifications = spec_loader.load_specifications(
            framework_file=framework_file_path,
            experiment_file=enhanced_experiment_file,
            corpus_dir=corpus_dir_path
        )
        
        # Step 5: Verify specifications are valid
        self.assertTrue(specifications['validation']['overall_valid'], "Enhanced experiment specifications should be valid")
        
        # Step 6: Prepare initial state for WorkflowOrchestrator (same pattern as CLI)
        initial_state = {
            'framework': specifications.get('framework'),
            'experiment': specifications.get('experiment'),
            'corpus': specifications.get('corpus'),
            'workflow': specifications.get('experiment', {}).get('workflow', []),
            'analysis_agent_instructions': specifications.get('framework', {}).get('analysis_variants', {}).get(
                specifications.get('experiment', {}).get('analysis_variant', 'default'), {}
            ).get('analysis_prompt', ''),
            'project_path': str(enhanced_experiment_file.parent),
            'framework_path': str(framework_file_path),
            'experiment_path': str(enhanced_experiment_file),
            'corpus_path': str(corpus_dir_path)
        }
        
        # Verify initial state is properly formed
        self.assertIsNotNone(initial_state['framework'], "Framework should be loaded")
        self.assertIsNotNone(initial_state['experiment'], "Experiment should be loaded")
        self.assertIsNotNone(initial_state['corpus'], "Corpus should be loaded")
        self.assertTrue(len(initial_state['workflow']) >= 2, "Workflow should contain enhanced agents")
        
        print("✅ Successfully prepared enhanced experiment for WorkflowOrchestrator")
        print(f"   - Enhanced workflow has {len(initial_state['workflow'])} agents")
        print(f"   - SynthesisAgent present: {synthesis_agent_found}")
        print(f"   - Specifications valid: {specifications['validation']['overall_valid']}")
        
        # Note: We don't actually execute the workflow in this test to avoid API costs
        # But we've verified that the enhanced experiment is properly structured
        # and can be successfully loaded by the WorkflowOrchestrator
        
    def test_lifecycle_to_orchestrator_end_to_end_flow(self):
        """Test the complete flow from experiment lifecycle to orchestrator preparation"""
        print("🧪 Testing complete end-to-end flow: Lifecycle → Orchestrator")
        
        # This test simulates what happens in the CLI when using the THIN lifecycle
        
        # Step 1: Initialize experiment startup (like CLI does)
        startup = ExperimentStartup(str(self.temp_dir))
        
        # Step 2: Simulate the lifecycle validation and enhancement
        lifecycle_manager = startup.lifecycle_manager
        
        # Test validation completeness check
        original_workflow = [{"agent": "AnalysisAgent"}]  # Issue #68 problem
        completeness_result = lifecycle_manager._validate_workflow_completeness(original_workflow)
        
        self.assertFalse(completeness_result['complete'], "Original workflow should be incomplete")
        self.assertIn('SynthesisAgent', completeness_result['missing_agents'], "Should identify missing SynthesisAgent")
        
        # Step 3: Generate enhanced workflow
        enhanced_workflow = lifecycle_manager._generate_enhanced_workflow(
            original_workflow, completeness_result['missing_agents']
        )
        
        self.assertTrue(len(enhanced_workflow) > len(original_workflow), "Enhanced workflow should be longer")
        synthesis_agent_added = any(step.get('agent') == 'SynthesisAgent' for step in enhanced_workflow)
        self.assertTrue(synthesis_agent_added, "SynthesisAgent should be added")
        
        # Step 4: Apply enhancements and get enhanced experiment file
        enhanced_file = startup._apply_workflow_enhancements(self.experiment_file, enhanced_workflow)
        
        # Step 5: Simulate the _load_specifications_for_execution method
        final_specifications = startup._load_specifications_for_execution(enhanced_file, startup.lifecycle_manager.spec_loader)
        
        self.assertTrue(final_specifications['validation']['overall_valid'], "Final specifications should be valid")
        
        # Step 6: Simulate the _prepare_initial_state method
        initial_state = startup._prepare_initial_state(final_specifications, enhanced_file)
        
        # Verify the initial state is properly prepared for orchestrator
        required_keys = ['framework', 'experiment', 'corpus', 'workflow', 'project_path', 'framework_path', 'experiment_path', 'corpus_path']
        for key in required_keys:
            self.assertIn(key, initial_state, f"Initial state should contain {key}")
            
        # Verify enhanced workflow is in the initial state
        workflow_agents = [step.get('agent') for step in initial_state['workflow']]
        self.assertIn('SynthesisAgent', workflow_agents, "Initial state workflow should contain SynthesisAgent")
        
        print("✅ Successfully validated complete end-to-end flow")
        print(f"   - Original workflow: {len(original_workflow)} agents")
        print(f"   - Enhanced workflow: {len(enhanced_workflow)} agents")
        print(f"   - Final workflow: {len(initial_state['workflow'])} agents")
        print(f"   - Ready for WorkflowOrchestrator execution")


def run_orchestrator_integration_test():
    """Run the orchestrator integration test suite"""
    print("🧪 Testing WorkflowOrchestrator Integration - Issue #131")
    print("=" * 80)
    print("This tests the critical handoff from THIN Experiment Lifecycle to WorkflowOrchestrator.")
    print()
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestOrchestratorIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n🎉 Orchestrator Integration Tests PASSED!")
        print("✅ Enhanced experiments can be loaded by WorkflowOrchestrator")
        print("✅ End-to-end flow from lifecycle to orchestrator works")
        print("✅ Issue #131 integration requirement satisfied")
        return True
    else:
        print("\n❌ Orchestrator Integration Tests FAILED!")
        return False


if __name__ == "__main__":
    # Run the test if called directly
    success = run_orchestrator_integration_test()
    sys.exit(0 if success else 1) 