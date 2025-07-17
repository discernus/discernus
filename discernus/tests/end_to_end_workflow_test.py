#!/usr/bin/env python3
"""
End-to-End Workflow Test
========================

An integration test for the full agent workflow, using a mock LLM gateway
to ensure data flows correctly between agents without live API calls.
"""

import unittest
import sys
from pathlib import Path
import json
from typing import Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway

class TestEndToEndWorkflow(unittest.TestCase):
    """
    Tests the complete workflow from analysis to synthesis using mock data.
    """

    def setUp(self):
        """Set up the test case."""
        # We will use real spec files but a mock gateway
        self.project_path = project_root / "projects" / "MVA" / "experiment_1"
        self.mock_responses = self._load_mock_responses()
        
        # We don't need a real model registry for the mock gateway
        self.mock_gateway = MockLLMGateway(self.mock_responses)
        
        # We inject the mock gateway into the orchestrator
        self.orchestrator = WorkflowOrchestrator(str(self.project_path))
        self.orchestrator.gateway = self.mock_gateway

    def _load_mock_responses(self) -> Dict[str, str]:
        """
        Loads messy, real-world LLM responses we've already captured.
        The key is the CLEAN JSON, the value is the MESSY response.
        This allows our mock gateway to find the right key by matching the messy response.
        """
        clean_progressive_json = json.dumps({
            "worldview": "Progressive",
            "scores": {"identity_axis": 0.3, "fear_hope_axis": -0.2, "envy_compersion_axis": -0.8, "enmity_amity_axis": -0.6, "goal_axis": -0.5},
            "analysis_text": "This text is a strong critique of economic inequality, aligning with a Progressive worldview."
        })

        clean_conservative_json = json.dumps({
            "worldview": "Conservative",
            "scores": {"identity_axis": 0.8, "fear_hope_axis": 0.9, "envy_compersion_axis": 0.85, "enmity_amity_axis": 0.9, "goal_axis": 0.8},
            "analysis_text": "This text is a concession speech emphasizing unity and respect for democratic processes."
        })

        return {
            clean_progressive_json: """
Here is the JSON you requested:
```json
{
  "worldview": "Progressive",
  "scores": {
    "identity_axis": 0.3,
    "fear_hope_axis": -0.2,
    "envy_compersion_axis": -0.8,
    "enmity_amity_axis": -0.6,
    "goal_axis": -0.5
  },
  "analysis_text": "This text is a strong critique of economic inequality, aligning with a Progressive worldview."
}
```
""",
            clean_conservative_json: """
```json
{
  "worldview": "Conservative",
  "scores": {
    "identity_axis": 0.8,
    "fear_hope_axis": 0.9,
    "envy_compersion_axis": 0.85,
    "enmity_amity_axis": 0.9,
    "goal_axis": 0.8
  },
  "analysis_text": "This text is a concession speech emphasizing unity and respect for democratic processes."
}
```
""",
            self._get_synthesis_mock_key(): self._get_synthesis_mock_report()
        }

    def _get_synthesis_mock_key(self) -> str:
        """Returns a unique key phrase from the synthesis prompt."""
        return "Synthesize the following information into a clear, well-structured, and insightful academic report"

    def _get_synthesis_mock_report(self) -> str:
        """Returns a plausible, canned synthesis report for the test."""
        return """
# Mock Synthesis Report

## Overview
This experiment analyzed two documents, revealing distinct political worldviews.

## Key Findings
- **Progressive Text**: One document expressed a Progressive worldview, critiquing economic inequality.
- **Conservative Text**: The other document expressed a Conservative worldview, emphasizing unity.

## Conclusion
The analysis successfully differentiated between the two political discourses based on the CFF framework.
"""

    def test_full_workflow_execution(self):
        """
        Test that the full workflow runs end-to-end and produces the correct artifacts.
        """
        # We need to load the real framework to get the instructions
        from discernus.core.spec_loader import SpecLoader
        spec_loader = SpecLoader()
        # Use the public method to load all specs, which is cleaner
        specs = spec_loader.load_specifications(
            framework_file=self.project_path / "cff_v4_mva.md",
            experiment_file=self.project_path / "experiment.md",
            corpus_dir=self.project_path / "corpus"
        )
        framework_spec = specs.get('framework', {})
        
        # To do this, we need to find the messy response associated with the clean key.
        # This is a bit awkward, but it's the price of a realistic test.
        clean_jsons = list(self.mock_responses.keys())
        messy_progressive = self.mock_responses[clean_jsons[0]]
        messy_conservative = self.mock_responses[clean_jsons[1]]
        
        # We'll start the test *after* the analysis agent has run.
        post_analysis_state = {
            'workflow': [
                # We are skipping AnalysisAgent and starting with its output
                {'agent': 'DataExtractionAgent'},
                {'agent': 'CalculationAgent'},
                {'agent': 'SynthesisAgent', 'config': {'output_artifacts': ['test_report.md', 'test_results.csv']}}
            ],
            'experiment': {'name': 'MVA Mock Test'},
            'framework': framework_spec,
            'analysis_results': [
                {
                    "agent_id": "analysis_agent_run1_mock_sanitized_speech_a4c8e1d9",
                    "corpus_file": str(self.project_path / "corpus" / "sanitized_speech_a4c8e1d9.md"),
                    "raw_response": messy_progressive,
                    "success": True,
                },
                {
                    "agent_id": "analysis_agent_run1_mock_sanitized_speech_a1c5e7d2",
                    "corpus_file": str(self.project_path / "corpus" / "sanitized_speech_a1c5e7d2.md"),
                    "raw_response": messy_conservative,
                    "success": True,
                }
            ]
        }


        # Execute the workflow
        final_state = self.orchestrator.execute_workflow(post_analysis_state)

        # Assertions
        self.assertEqual(final_state['status'], 'success')
        
        # Check that the final report was created and contains the correct content
        report_path = self.orchestrator.session_results_path / "test_report.md"
        self.assertTrue(report_path.exists())
        report_content = report_path.read_text()
        self.assertIn("Mock Synthesis Report", report_content)
        self.assertIn("Progressive worldview", report_content)
        
        # Check that the CSV was created
        csv_path = self.orchestrator.session_results_path / "test_results.csv"
        self.assertTrue(csv_path.exists())
        
        # Check the content of the CSV
        import pandas as pd
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 2)
        self.assertIn('scores_identity_axis', df.columns)  # Framework-agnostic: nested field names
        self.assertEqual(df.iloc[0]['worldview'], 'Progressive')
        self.assertEqual(df.iloc[1]['worldview'], 'Conservative')

if __name__ == '__main__':
    unittest.main() 