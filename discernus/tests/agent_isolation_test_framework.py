#!/usr/bin/env python3
"""
Agent Isolation Test Framework
==============================

This framework allows testing individual agents in isolation by mocking
upstream and downstream agents. As the Cursor assistant, I can simulate
realistic handoffs to test specific agents without expensive LLM calls.
"""

import unittest
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway

class AgentTestHarness:
    """
    Test harness for isolated agent testing.
    """
    
    def __init__(self, agent_class, mock_responses: Optional[List[str] | Dict[str, str]] = None):
        """Initialize the test harness for a specific agent."""
        self.agent_class = agent_class
        
        # The Mock Gateway now expects a list (queue) of responses.
        # If we get a dict, we'll use its values as the queue.
        if isinstance(mock_responses, dict):
            response_queue = list(mock_responses.values())
        else:
            response_queue = mock_responses or []
            
        self.mock_gateway = MockLLMGateway(response_queue)
        
    def test_agent_with_handoff(self, 
                               upstream_data: Dict[str, Any], 
                               step_config: Optional[Dict[str, Any]] = None,
                               expected_keys: Optional[List[str]] = None,
                               mock_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Test an agent with realistic upstream data handoff.
        
        Args:
            upstream_data: Simulated data from upstream agents
            step_config: Configuration for this agent step
            expected_keys: Expected keys in the output
            mock_files: A list of mock filenames to simulate directory listing.
            
        Returns:
            Agent output for validation
        """
        # Create agent instance
        try:
            # Try to create agent with gateway (for agents that need LLM)
            agent = self.agent_class(gateway=self.mock_gateway)
        except TypeError:
            # Create agent without gateway (for agents that don't need LLM)
            agent = self.agent_class()
        
        # Execute agent within a mocked file system context if needed
        if mock_files:
            # We use the 'patch' context manager from unittest.mock to intercept
            # the file system calls made by the agent.
            with patch('pathlib.Path.iterdir') as mock_iterdir:
                # Create MagicMock objects for each mock file
                mock_paths = [MagicMock(spec=Path, is_file=lambda: True, name=f) for f in mock_files]
                for p, f in zip(mock_paths, mock_files):
                    p.name = f
                    # We can also mock read_text if needed
                    p.read_text.return_value = f"content of {f}"

                mock_iterdir.return_value = mock_paths
                result = agent.execute(upstream_data, step_config or {})
        else:
            result = agent.execute(upstream_data, step_config or {})
        
        # Validate expected keys if provided
        if expected_keys:
            for key in expected_keys:
                if key not in result:
                    raise AssertionError(f"Expected key '{key}' not found in agent output")
        
        return result

class TestAnalysisAgent(unittest.TestCase):
    """
    Isolated tests for AnalysisAgent.
    """
    
    def setUp(self):
        """Set up test scenarios for AnalysisAgent."""
        self.mock_responses = {
            # CFF analysis response
            '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}}': '''
            Here is my analysis:
            ```json
            {"worldview": "Progressive", "scores": {"identity_axis": 0.3}}
            ```
            Analysis complete.
            ''',
            
            # PDAF analysis response
            '{"political_orientation": "Anti-Pluralist", "dimension_scores": {"exclusion_dimension": 0.8}}': '''
            Based on the PDAF framework:
            ```json
            {"political_orientation": "Anti-Pluralist", "dimension_scores": {"exclusion_dimension": 0.8}}
            ```
            End of analysis.
            '''
        }
        
        from discernus.agents.analysis_agent import AnalysisAgent
        self.harness = AgentTestHarness(AnalysisAgent, self.mock_responses)
    
    def test_analysis_agent_basic_handoff(self):
        """Test AnalysisAgent with basic upstream handoff."""
        # Simulate upstream data from orchestrator
        upstream_data = {
            'project_path': str(project_root / "projects" / "MVA" / "experiment_1"),
            'corpus_path': str(project_root / "projects" / "MVA" / "experiment_1" / "corpus"),
            'experiment': {
                'models': ['test_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': '''
            You are analyzing political discourse. Return JSON with:
            {"worldview": "Progressive", "scores": {"identity_axis": 0.3}}
            '''
        }
        
        # Test the agent
        result = self.harness.test_agent_with_handoff(
            upstream_data, 
            expected_keys=['analysis_results']
        )
        
        # Validate output structure
        self.assertIn('analysis_results', result)
        self.assertIsInstance(result['analysis_results'], list)
        
        # Check that results have expected structure
        if result['analysis_results']:
            first_result = result['analysis_results'][0]
            expected_result_keys = ['agent_id', 'corpus_file', 'model_name', 'run_num', 'success']
            for key in expected_result_keys:
                self.assertIn(key, first_result)

class TestCalculationAgent(unittest.TestCase):
    """
    Isolated tests for CalculationAgent.
    """
    
    def setUp(self):
        """Set up test scenarios for CalculationAgent."""
        from discernus.agents.calculation_agent import CalculationAgent
        self.harness = AgentTestHarness(CalculationAgent)
    
    def test_calculation_agent_with_cff_data(self):
        """Test CalculationAgent with CFF framework data."""
        # Simulate upstream data from DataExtractionAgent
        upstream_data = {
            'framework': {
                'calculation_spec': [
                    {
                        'name': 'cff_cohesion_index',
                        'formula': '(fear_hope_axis + enmity_amity_axis) / 2'
                    }
                ]
            },
            'analysis_results': [
                {
                    'success': True,
                    'json_output': {
                        'worldview': 'Progressive',
                        'scores': {
                            'identity_axis': 0.3,
                            'fear_hope_axis': -0.2,
                            'enmity_amity_axis': -0.6
                        }
                    }
                }
            ]
        }
        
        # Test the agent
        result = self.harness.test_agent_with_handoff(
            upstream_data,
            expected_keys=['analysis_results']
        )
        
        # Validate that calculation was performed
        self.assertIn('analysis_results', result)
        analysis_result = result['analysis_results'][0]
        self.assertIn('cff_cohesion_index', analysis_result['json_output'])
        self.assertEqual(analysis_result['json_output']['cff_cohesion_index'], (-0.2 + -0.6) / 2)
    
    def test_calculation_agent_with_pdaf_data(self):
        """Test CalculationAgent with PDAF framework data."""
        # Simulate upstream data from DataExtractionAgent
        upstream_data = {
            'framework': {
                'calculation_spec': [
                    {
                        'name': 'populism_threat_score',
                        'formula': 'exclusion_dimension * 0.7 + authority_dimension * 0.3'
                    }
                ]
            },
            'analysis_results': [
                {
                    'success': True,
                    'json_output': {
                        'political_orientation': 'Anti-Pluralist',
                        'dimension_scores': {
                            'exclusion_dimension': 0.8,
                            'authority_dimension': 0.6,
                            'populism_dimension': 0.9
                        }
                    }
                }
            ]
        }
        
        # Test the agent
        result = self.harness.test_agent_with_handoff(
            upstream_data,
            expected_keys=['analysis_results']
        )
        
        # Validate that calculation was performed
        self.assertIn('analysis_results', result)
        analysis_result = result['analysis_results'][0]
        self.assertIn('populism_threat_score', analysis_result['json_output'])
        expected_score = 0.8 * 0.7 + 0.6 * 0.3
        self.assertEqual(analysis_result['json_output']['populism_threat_score'], expected_score)
    
    def test_calculation_agent_no_numeric_data(self):
        """Test CalculationAgent when no numeric data is available."""
        # Simulate upstream data with no numeric values
        upstream_data = {
            'framework': {
                'calculation_spec': [
                    {
                        'name': 'test_calculation',
                        'formula': 'some_score * 2'
                    }
                ]
            },
            'analysis_results': [
                {
                    'success': True,
                    'json_output': {
                        'text_analysis': 'This is just text',
                        'categories': ['positive', 'negative'],
                        'notes': 'No numeric data here'
                    }
                }
            ]
        }
        
        # Test the agent
        result = self.harness.test_agent_with_handoff(
            upstream_data,
            expected_keys=['analysis_results']
        )
        
        # Validate that result is returned but no calculation performed
        self.assertIn('analysis_results', result)
        analysis_result = result['analysis_results'][0]
        self.assertNotIn('test_calculation', analysis_result['json_output'])

class TestDataExtractionAgent(unittest.TestCase):
    """
    Isolated tests for DataExtractionAgent.
    """
    
    def setUp(self):
        """Set up test scenarios for DataExtractionAgent."""
        self.mock_responses = {
            # Clean JSON extraction responses
            '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}}': '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}}',
            '{"political_orientation": "Anti-Pluralist"}': '{"political_orientation": "Anti-Pluralist"}'
        }
        
        from discernus.agents.data_extraction_agent import DataExtractionAgent
        self.harness = AgentTestHarness(DataExtractionAgent, self.mock_responses)
    
    def test_data_extraction_agent_messy_json(self):
        """Test DataExtractionAgent with messy JSON responses."""
        # Simulate upstream data from AnalysisAgent with messy responses
        upstream_data = {
            'analysis_results': [
                {
                    'agent_id': 'test_agent_1',
                    'success': True,
                    'raw_response': '''
                    Here is my analysis:
                    ```json
                    {"worldview": "Progressive", "scores": {"identity_axis": 0.3}}
                    ```
                    That completes the analysis.
                    '''
                },
                {
                    'agent_id': 'test_agent_2',
                    'success': True,
                    'raw_response': '''
                    Based on the framework:
                    ```json
                    {"political_orientation": "Anti-Pluralist"}
                    ```
                    End of analysis.
                    '''
                }
            ]
        }
        
        # Test the agent
        result = self.harness.test_agent_with_handoff(
            upstream_data,
            expected_keys=['analysis_results']
        )
        
        # Validate that JSON was extracted
        self.assertIn('analysis_results', result)
        self.assertEqual(len(result['analysis_results']), 2)
        
        # Check first result
        first_result = result['analysis_results'][0]
        self.assertIn('json_output', first_result)
        self.assertEqual(first_result['json_output']['worldview'], 'Progressive')
        
        # Check second result
        second_result = result['analysis_results'][1]
        self.assertIn('json_output', second_result)
        self.assertEqual(second_result['json_output']['political_orientation'], 'Anti-Pluralist')

class TestSynthesisAgent(unittest.TestCase):
    """
    Isolated tests for SynthesisAgent (through orchestrator due to complexity).
    """
    
    def setUp(self):
        """Set up test scenarios for SynthesisAgent."""
        self.mock_responses = {
            "Synthesize the following information into a clear": "# Test Synthesis Report\n\nThis is a test report."
        }
    
    def test_synthesis_agent_csv_generation(self):
        """Test SynthesisAgent CSV generation with diverse data."""
        from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
        
        # Simulate upstream data from CalculationAgent
        upstream_data = {
            'workflow': [
                {'agent': 'SynthesisAgent', 'config': {'output_artifacts': ['test_report.md', 'test_results.csv']}}
            ],
            'experiment': {'name': 'Test Synthesis'},
            'framework': {'name': 'Test Framework'},
            'analysis_results': [
                {
                    'agent_id': 'test_cff_agent',
                    'corpus_file': 'test_doc.txt',
                    'success': True,
                    'model_name': 'test_model',
                    'run_num': 1,
                    'json_output': {
                        'worldview': 'Progressive',
                        'scores': {'identity_axis': 0.3, 'fear_hope_axis': -0.2},
                        'cff_cohesion_index': 0.05
                    }
                },
                {
                    'agent_id': 'test_pdaf_agent',
                    'corpus_file': 'test_doc2.txt',
                    'success': True,
                    'model_name': 'test_model',
                    'run_num': 1,
                    'json_output': {
                        'political_orientation': 'Anti-Pluralist',
                        'dimension_scores': {'exclusion_dimension': 0.8},
                        'populism_threat_score': 0.65
                    }
                }
            ]
        }
        
        # Execute through orchestrator
        project_path = project_root / "projects" / "MVA" / "experiment_1"
        orchestrator = WorkflowOrchestrator(str(project_path))
        orchestrator.gateway = MockLLMGateway(self.mock_responses)
        
        result = orchestrator.execute_workflow(upstream_data)
        
        # Validate successful completion
        self.assertEqual(result['status'], 'success')
        
        # Check CSV generation
        csv_path = orchestrator.session_results_path / "test_results.csv"
        if csv_path.exists():
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            # Should have 2 rows (one for each result)
            self.assertEqual(len(df), 2)
            
            # Should have framework-agnostic columns
            self.assertIn('scores_identity_axis', df.columns)
            self.assertIn('dimension_scores_exclusion_dimension', df.columns)
            self.assertIn('cff_cohesion_index', df.columns)
            self.assertIn('populism_threat_score', df.columns)

if __name__ == '__main__':
    unittest.main() 