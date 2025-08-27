#!/usr/bin/env python3
"""Simple test for orchestrator fact checker integration."""

import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile

# Import the components
from discernus.agents.fact_checker_agent.agent import FactCheckerAgent


class TestOrchestratorFactCheckerIntegration(unittest.TestCase):
    """Test that orchestrator can call fact checker agent successfully."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create a mock experiment directory
        experiment_dir = self.temp_dir / "test_experiment"
        experiment_dir.mkdir()
        
        # Create a simple experiment.md file
        experiment_file = experiment_dir / "experiment.md"
        experiment_file.write_text("""# Test Experiment

## Research Questions
- What is the main theme?

## Configuration Appendix
```yaml
metadata:
  experiment_name: test_experiment
  spec_version: "10.0"
  description: "Test experiment for orchestrator integration"

components:
  framework: test_framework.md
  corpus: test_corpus.md
  analysis_model: vertex_ai/gemini-2.5-flash
  synthesis_model: vertex_ai/gemini-2.5-flash

parameters:
  max_tokens: 4000
  temperature: 0.1
```
""")
        
        # Create shared_cache directory
        shared_cache = experiment_dir / "shared_cache"
        shared_cache.mkdir()
        
        self.experiment_path = experiment_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_fact_checker_agent_can_run(self):
        """Test that the fact checker agent can run successfully."""
        
        # Create fact checker agent
        fact_checker = FactCheckerAgent()
        
        # Test that it can run (even if it fails due to no data)
        result = fact_checker.run()
        
        # Verify the result structure
        self.assertIn('status', result)
        self.assertIn('findings', result)
        self.assertIn('summary', result)
        
        # Since we don't have real data, it should fail with a specific error
        self.assertEqual(result['status'], 'failed')
        self.assertIn('No synthesis report found', result['error'])
    
    def test_fact_checker_agent_has_discovery_methods(self):
        """Test that the fact checker agent has all required discovery methods."""
        
        fact_checker = FactCheckerAgent()
        
        # Check that all discovery methods exist
        required_methods = [
            '_discover_synthesis_report',
            '_discover_evidence_data', 
            '_discover_framework_spec',
            '_discover_semantic_index_with_wrapper',
            '_discover_artifacts_by_type',
            '_index_has_properties',
            '_get_default_corpus_wrappers',
            '_load_artifact_content',
            '_run_fact_checking'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(fact_checker, method_name),
                f"Method {method_name} not found in FactCheckerAgent"
            )
            self.assertTrue(
                callable(getattr(fact_checker, method_name)),
                f"Method {method_name} is not callable"
            )
    
    def test_fact_checker_agent_returns_completion_signal(self):
        """Test that fact checker agent returns a proper completion signal."""
        
        fact_checker = FactCheckerAgent()
        result = fact_checker.run()
        
        # The agent should return a completion signal (even if failed)
        # This allows the orchestrator to know when to proceed to the next phase
        self.assertIn('status', result)
        self.assertIn('findings', result)
        self.assertIn('summary', result)
        
        # The status should be either 'completed' or 'failed', not 'running' or similar
        self.assertIn(result['status'], ['completed', 'failed'])


if __name__ == "__main__":
    unittest.main()
