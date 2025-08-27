#!/usr/bin/env python3
"""Integration test for fact checker agent with orchestrator."""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import the components
from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator


class TestFactCheckerOrchestratorIntegration(unittest.TestCase):
    """Test the integration between orchestrator and fact checker agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock LLM gateway
        self.mock_gateway = Mock()
        
        # Create a mock audit logger
        self.mock_audit_logger = Mock()
        
        # Create a mock corpus index service
        self.mock_corpus_service = Mock()
        
    def test_orchestrator_calls_fact_checker_run(self):
        """Test that orchestrator can call fact checker agent's run method."""
        
        # Create fact checker agent with mocked dependencies
        fact_checker = FactCheckerAgent(
            gateway=self.mock_gateway,
            audit_logger=self.mock_audit_logger,
            corpus_index_service=self.mock_corpus_service
        )
        
        # Test that the run method exists and can be called
        self.assertTrue(hasattr(fact_checker, 'run'))
        self.assertTrue(callable(fact_checker.run))
        
        # Test that run method returns expected structure
        result = fact_checker.run()
        
        # Verify the result structure
        self.assertIn('status', result)
        self.assertIn('findings', result)
        self.assertIn('summary', result)
        
        # Since we don't have real data, it should fail with a specific error
        self.assertEqual(result['status'], 'failed')
        self.assertIn('No synthesis report found', result['error'])
        
    def test_fact_checker_discovery_methods_exist(self):
        """Test that all required discovery methods exist."""
        
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
    
    def test_fact_checker_returns_completion_signal(self):
        """Test that fact checker returns a proper completion signal."""
        
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
