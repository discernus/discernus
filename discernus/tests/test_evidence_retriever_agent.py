#!/usr/bin/env python3
"""
Unit Tests for EvidenceRetrieverAgent
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from discernus.agents.evidence_retriever_agent.evidence_retriever_agent import EvidenceRetrieverAgent
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary

class TestEvidenceRetrieverAgent(unittest.TestCase):
    """Test suite for the EvidenceRetrieverAgent."""

    def setUp(self):
        """Set up a temporary directory for artifacts."""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create experiment structure
        (self.test_dir / "experiment.md").touch()
        self.run_folder = self.test_dir / "runs" / "test_run"
        self.run_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize infrastructure
        self.security_boundary = ExperimentSecurityBoundary(self.test_dir)
        self.artifact_storage = LocalArtifactStorage(
            security_boundary=self.security_boundary,
            run_folder=self.run_folder
        )
        
        # Agent configuration
        self.config = {
            'experiment_path': str(self.test_dir),
            'run_id': 'test_run',
            'artifact_storage': self.artifact_storage,
        }
        
        self.agent = EvidenceRetrieverAgent(self.config)

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_parse_llm_response_with_valid_json_plan(self):
        """
        Test that the agent correctly parses a valid, structured plan from the LLM.
        
        This is the first step in TDD: writing a failing test for the desired functionality.
        The current implementation returns a hardcoded empty plan, so this test will fail.
        """
        # 1. Define a mock LLM response containing a structured plan.
        # This simulates the expected output from the LLM after it analyzes statistical findings.
        mock_llm_response = """
        Here is the evidence retrieval plan you requested.
        ```json
        [
          {
            "finding": "Strong positive correlation (r=0.99) between Fear and Tribal Dominance.",
            "queries": ["fear and tribalism", "threat narratives", "in-group defense"]
          },
          {
            "finding": "John McCain's speech is an outlier with high cohesion (FCI=0.84).",
            "queries": ["unifying rhetoric", "concession speech themes", "civic unity"]
          }
        ]
        ```
        The plan above identifies the two most critical statistical patterns and provides targeted queries for each.
        """

        # 2. Define the expected output after parsing.
        expected_plan = [
          {
            "finding": "Strong positive correlation (r=0.99) between Fear and Tribal Dominance.",
            "queries": ["fear and tribalism", "threat narratives", "in-group defense"]
          },
          {
            "finding": "John McCain's speech is an outlier with high cohesion (FCI=0.84).",
            "queries": ["unifying rhetoric", "concession speech themes", "civic unity"]
          }
        ]

        # 3. Call the method to be tested.
        # This method is currently a stub and will not produce the expected output.
        parsed_plan = self.agent._parse_llm_response(mock_llm_response)

        # 4. Assert that the parsed plan matches the expected structure.
        # This assertion will fail, driving the implementation.
        self.assertEqual(parsed_plan, expected_plan)

    def test_execute_evidence_plan_calls_search_correctly(self):
        """
        Test that the agent executes a plan by calling the evidence wrapper with the correct queries.
        
        This test ensures the agent iterates through the parsed plan and uses the RAG wrapper
        to search for evidence for each finding. It will fail initially because the
        _execute_evidence_plan method is a stub.
        """
        # 1. Define a mock evidence retrieval plan.
        mock_plan = [
            {
                "finding": "Finding A",
                "queries": ["queryA1", "queryA2"]
            },
            {
                "finding": "Finding B",
                "queries": ["queryB1"]
            }
        ]

        # 2. Mock the EvidenceMatchingWrapper to avoid actual RAG calls.
        # We replace the agent's wrapper with a mock that we can monitor.
        self.agent.evidence_wrapper = MagicMock()
        # Configure the mock to return some dummy data to simulate a successful search.
        self.agent.evidence_wrapper.search_evidence.return_value = [
            {"quote_text": "some evidence", "relevance_score": 0.9}
        ]

        # 3. Call the method to be tested.
        results = self.agent._execute_evidence_plan(mock_plan)

        # 4. Assert that the search function was called for each query in the plan.
        self.assertEqual(self.agent.evidence_wrapper.search_evidence.call_count, 3)
        self.agent.evidence_wrapper.search_evidence.assert_any_call("queryA1", limit=3)
        self.agent.evidence_wrapper.search_evidence.assert_any_call("queryA2", limit=3)
        self.agent.evidence_wrapper.search_evidence.assert_any_call("queryB1", limit=3)

        # 5. Assert that the results are structured correctly.
        self.assertEqual(len(results), 2) # Should have one result object per finding.
        self.assertEqual(results[0]['finding']['description'], "Finding A")
        self.assertGreater(len(results[0]['quotes']), 0)


if __name__ == "__main__":
    unittest.main()
