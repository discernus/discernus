#!/usr/bin/env python3
"""
Agent Isolation Test: AnalysisAgent
===================================

This test validates the `AnalysisAgent` in isolation, ensuring it correctly
captures raw LLM output without attempting to parse it.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import unittest
import sys
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.analysis_agent import AnalysisAgent
from discernus.tests.agent_isolation_test_framework import AgentTestHarness

class TestAnalysisAgent(unittest.TestCase):
    """
    Tests for the AnalysisAgent.
    """

    def setUp(self):
        """Set up the test harness for the AnalysisAgent."""
        # Provide a queue of responses for the mock gateway
        self.original_responses = [
            '{"analysis": "This is a raw, messy response for speech a4c8e1d9.", "scores": {"score": 0.5}}',
            '{"analysis": "This is another raw response for speech a1c5e7d2.", "scores": {"score": 0.3}}'
        ]
        # Create a copy for the mock gateway to consume
        self.mock_responses = self.original_responses.copy()
        self.harness = AgentTestHarness(AnalysisAgent, self.mock_responses)

    def test_analysis_agent_loops_and_captures_raw_output(self):
        """
        Test that the AnalysisAgent correctly loops through mock files and
        captures the raw output for each one.
        """
        # Configure the mock to return a corpus with exactly two files
        mock_files = ["sanitized_speech_a4c8e1d9.md", "sanitized_speech_a1c5e7d2.md"]
        mock_paths = []
        
        for filename in mock_files:
            mock_path = MagicMock(spec=Path)
            mock_path.is_file.return_value = True
            mock_path.suffix = '.md'
            mock_path.name = filename
            mock_path.stem = filename.replace('.md', '')
            mock_path.read_text.return_value = f"content of {filename}"
            mock_paths.append(mock_path)
        
        # Simulate the state provided by the orchestrator
        initial_state = {
            'project_path': str(project_root / "projects" / "MVA" / "experiment_1"),
            'corpus_path': str(project_root / "projects" / "MVA" / "experiment_1" / "corpus"),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': "Analyze this: {corpus_text}",
        }
        
        # Patch the rglob method where it's used (in the AnalysisAgent module)
        with patch('discernus.agents.analysis_agent.Path.rglob') as mock_rglob:
            mock_rglob.return_value = mock_paths
            
            # Test the agent
            result = self.harness.test_agent_with_handoff(
                initial_state, 
                expected_keys=['analysis_results']
            )
        
        # Validate the output
        self.assertIn('analysis_results', result)
        analysis_results = result['analysis_results']
        
        self.assertEqual(len(analysis_results), 2)
        
        # Check the first result
        self.assertEqual(analysis_results[0]['raw_response'], self.original_responses[0])
        self.assertTrue(analysis_results[0]['success'])
        
        # Check the second result
        self.assertEqual(analysis_results[1]['raw_response'], self.original_responses[1])
        self.assertTrue(analysis_results[1]['success'])

if __name__ == '__main__':
    unittest.main() 