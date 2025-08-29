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

    def test_create_evidence_retrieval_prompt_with_tuple_keys(self):
        """
        Test that the agent can handle statistical results with tuple keys without crashing.
        
        This test reproduces the "keys must be str, int, float, bool or None, not tuple" error
        that was occurring during evidence retrieval.
        """
        # Create mock statistical results with tuple keys (like pandas groupby().agg() produces)
        mock_statistical_results = {
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699},
                    ('constitutional_health_index', 'count'): {'Biden': 6, 'Trump': 7}
                }
            },
            'other_stats': {
                'simple_key': 'simple_value',
                'nested': {
                    ('another_tuple', 'key'): 'nested_value'
                }
            }
        }
        
        # Create a mock framework spec
        mock_framework_spec = {
            'name': 'Test Framework',
            'description': 'A test framework'
        }
        
        # This should not crash with the tuple key error
        try:
            prompt = self.agent._create_evidence_retrieval_prompt(
                mock_framework_spec, 
                mock_statistical_results
            )
            
            # Verify the prompt was created successfully
            self.assertIsInstance(prompt, str)
            self.assertIn('Test Framework', prompt)
            self.assertIn('Biden', prompt)
            self.assertIn('Trump', prompt)
            
            # Verify that tuple keys were converted to strings
            self.assertIn("('constitutional_health_index', 'mean')", prompt)
            self.assertIn("('constitutional_health_index', 'std')", prompt)
            
        except Exception as e:
            self.fail(f"Evidence retrieval prompt creation failed with error: {e}")

    def test_evidence_retrieval_with_tuple_keys_end_to_end(self):
        """
        Test the complete evidence retrieval flow with tuple keys in statistical results.
        
        This test verifies that the entire evidence retrieval process can handle
        tuple keys without crashing, from loading results to creating prompts.
        """
        # Create mock statistical results with tuple keys
        mock_statistical_results = {
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699}
                }
            }
        }
        
        # Mock the LLM gateway to return a valid response
        with patch.object(self.agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = (
                '{"findings": [{"finding": "Test finding", "queries": ["test query"]}]}',
                {}
            )
            
            # Mock the evidence wrapper
            with patch.object(self.agent, '_build_evidence_wrapper') as mock_build:
                mock_wrapper = Mock()
                mock_wrapper.search.return_value = [{'quote': 'Test quote', 'score': 0.8}]
                mock_build.return_value = mock_wrapper
                
                # This should not crash with tuple keys
                try:
                    results = self.agent._llm_driven_evidence_retrieval(
                        {'name': 'Test Framework'}, 
                        mock_statistical_results
                    )
                    
                    # Verify the method completed successfully
                    self.assertIsInstance(results, list)
                    
                except Exception as e:
                    self.fail(f"Evidence retrieval failed with error: {e}")

    def test_load_statistical_results_with_tuple_keys(self):
        """
        Test that statistical results with tuple keys can be loaded and processed.
        
        This test verifies that the _load_statistical_results method can handle
        tuple keys in the stored data without crashing.
        """
        # Create mock statistical results with tuple keys
        mock_statistical_results = {
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699}
                }
            }
        }
        
        # Store the results in artifact storage
        import pickle
        content = pickle.dumps(mock_statistical_results)
        hash_value = self.artifact_storage.put_artifact(content, {"artifact_type": "test"})
        
        # Try to load the results back
        try:
            loaded_results = self.agent._load_statistical_results(hash_value)
            
            # Verify the results were loaded correctly
            self.assertIn('calculate_descriptive_stats_by_admin', loaded_results)
            self.assertIn('administration_stats', loaded_results['calculate_descriptive_stats_by_admin'])
            
            # Verify tuple keys are preserved
            admin_stats = loaded_results['calculate_descriptive_stats_by_admin']['administration_stats']
            self.assertIn(('constitutional_health_index', 'mean'), admin_stats)
            self.assertIn(('constitutional_health_index', 'std'), admin_stats)
            
        except Exception as e:
            self.fail(f"Loading statistical results with tuple keys failed: {e}")

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
