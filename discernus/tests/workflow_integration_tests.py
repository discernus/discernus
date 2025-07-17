#!/usr/bin/env python3
"""
Workflow Integration Tests for THIN/THICK Architecture
=====================================================

These tests address the unique challenges of testing a THIN software + THICK LLM system:
- Test agent handoffs and workflow orchestration
- Test framework-agnostic behavior efficiently
- Test state transformations between agents
- Mock LLM responses at the integration level

Philosophy:
- Focus on the ORCHESTRATION, not individual agents
- Test the DATA FLOW between agents
- Validate FRAMEWORK-AGNOSTIC behavior
- Use REALISTIC mock responses based on actual LLM outputs

Usage:
    python3 discernus/tests/workflow_integration_tests.py
    python3 -m unittest discernus.tests.workflow_integration_tests -v
"""

import unittest
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway

class WorkflowIntegrationTests(unittest.TestCase):
    """
    Tests for workflow orchestration and agent integration points.
    
    These tests focus on the THIN software layer - the orchestration,
    agent handoffs, and state management - using realistic mock LLM responses.
    """
    
    def setUp(self):
        """Set up test environment with temporary project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "test_project"
        self.project_path.mkdir()
        
        # Create test corpus
        self.corpus_path = self.project_path / "corpus"
        self.corpus_path.mkdir()
        
        # Create test documents
        (self.corpus_path / "doc1.txt").write_text("This is a test document about progressive politics.")
        (self.corpus_path / "doc2.txt").write_text("This is a test document about conservative politics.")
        
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)
    
    def test_analysis_to_data_extraction_handoff(self):
        """Test the critical handoff between AnalysisAgent and DataExtractionAgent."""
        # Mock realistic LLM responses for analysis
        analysis_responses = [
            '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}, "reasoning": "Shows progressive values"}',
            '{"worldview": "Conservative", "scores": {"identity_axis": 0.7}, "reasoning": "Shows conservative values"}'
        ]
        
        # Mock response for data extraction (JSON cleanup)
        extraction_responses = [
            '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}, "reasoning": "Shows progressive values"}',
            '{"worldview": "Conservative", "scores": {"identity_axis": 0.7}, "reasoning": "Shows conservative values"}'
        ]
        
        # Combined mock responses (analysis + extraction)
        mock_responses = analysis_responses + extraction_responses
        
        # Create orchestrator with mock gateway
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = MockLLMGateway(mock_responses)
        
        # Create workflow state
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': 'Analyze this text: {corpus_text}',
            'project_path': str(self.project_path)
        }
        
        # Execute workflow
        result = orchestrator.execute_workflow(workflow_state)
        
        # Validate handoff succeeded
        self.assertEqual(result['status'], 'success')
        self.assertIn('analysis_results', result['final_state'])
        
        # Validate data extraction processed the analysis results
        analysis_results = result['final_state']['analysis_results']
        self.assertEqual(len(analysis_results), 2)
        
        # Validate each result has both raw and extracted data
        for analysis_result in analysis_results:
            # After DataExtractionAgent processes, the data is in json_output
            self.assertIn('json_output', analysis_result)
            self.assertIn('success', analysis_result)
            self.assertTrue(analysis_result['success'])
            
            # Check the extracted JSON data
            json_output = analysis_result['json_output']
            self.assertIn('worldview', json_output)
            self.assertIn('scores', json_output)
    
    def test_framework_agnostic_behavior(self):
        """Test that the workflow works with different framework structures."""
        # Test with CFF-style framework
        cff_responses = [
            '{"worldview": "Progressive", "scores": {"identity_axis": 0.3}}',
            '{"worldview": "Conservative", "scores": {"identity_axis": 0.7}}'
        ]
        
        # Test with PDAF-style framework  
        pdaf_responses = [
            '{"political_orientation": "Pluralist", "dimension_scores": {"inclusion": 0.8}}',
            '{"political_orientation": "Anti-Pluralist", "dimension_scores": {"inclusion": 0.2}}'
        ]
        
        # Test with custom framework
        custom_responses = [
            '{"sentiment": "Positive", "metrics": {"enthusiasm": 0.9}}',
            '{"sentiment": "Negative", "metrics": {"enthusiasm": 0.1}}'
        ]
        
        framework_tests = [
            ("CFF", cff_responses),
            ("PDAF", pdaf_responses), 
            ("Custom", custom_responses)
        ]
        
        for framework_name, responses in framework_tests:
            with self.subTest(framework=framework_name):
                # Create orchestrator with framework-specific responses
                orchestrator = WorkflowOrchestrator(str(self.project_path))
                orchestrator.gateway = MockLLMGateway(responses + responses)  # Double for extraction
                
                workflow_state = {
                    'workflow': [
                        {'agent': 'AnalysisAgent'},
                        {'agent': 'DataExtractionAgent'}
                    ],
                    'corpus_path': str(self.corpus_path),
                    'experiment': {
                        'models': ['mock_model'],
                        'num_runs': 1
                    },
                    'analysis_agent_instructions': f'Analyze using {framework_name} framework: {{corpus_text}}',
                    'project_path': str(self.project_path)
                }
                
                result = orchestrator.execute_workflow(workflow_state)
                
                # Should work regardless of framework structure
                self.assertEqual(result['status'], 'success')
                self.assertIn('analysis_results', result['final_state'])
                self.assertEqual(len(result['final_state']['analysis_results']), 2)
    
    def test_calculation_agent_integration(self):
        """Test the integration between DataExtractionAgent and CalculationAgent."""
        # Mock responses with numeric data for calculations
        analysis_responses = [
            '{"scores": {"axis_a": 0.3, "axis_b": 0.7}}',
            '{"scores": {"axis_a": 0.8, "axis_b": 0.2}}'
        ]
        
        # Mock responses for extraction (same as analysis for simplicity)
        extraction_responses = analysis_responses.copy()
        
        mock_responses = analysis_responses + extraction_responses
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = MockLLMGateway(mock_responses)
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'},
                {'agent': 'CalculationAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': 'Analyze: {corpus_text}',
            'framework': {
                'calculation_spec': [
                    {'name': 'test_index', 'formula': '(axis_a + axis_b) / 2'}
                ]
            },
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # Validate calculation was performed
        self.assertEqual(result['status'], 'success')
        analysis_results = result['final_state']['analysis_results']
        
        for analysis_result in analysis_results:
            self.assertIn('json_output', analysis_result)
            self.assertIn('test_index', analysis_result['json_output'])
            # Should have calculated the average
            expected_value = (analysis_result['json_output']['scores']['axis_a'] + 
                            analysis_result['json_output']['scores']['axis_b']) / 2
            self.assertEqual(analysis_result['json_output']['test_index'], expected_value)
    
    def test_error_propagation_in_workflow(self):
        """Test how errors propagate through the workflow."""
        # Mock responses with one success and one failure
        analysis_responses = [
            '{"valid": "json"}',
            'Invalid JSON that will cause parsing error'
        ]
        
        # Mock extraction responses - DataExtractionAgent needs responses for extraction calls
        # Even failed analyses may trigger extraction attempts
        extraction_responses = [
            '{"valid": "json"}',
            '{"valid": "json"}',  # Additional response for extraction attempts
            '{"valid": "json"}'   # Additional response for extraction attempts
        ]
        
        mock_responses = analysis_responses + extraction_responses
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = MockLLMGateway(mock_responses)
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': 'Analyze: {corpus_text}',
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # Workflow should complete successfully
        self.assertEqual(result['status'], 'success')
        analysis_results = result['final_state']['analysis_results']
        
        # Should have processed both documents
        self.assertEqual(len(analysis_results), 2)
        
        # Check that at least one result has valid data
        valid_results = [r for r in analysis_results if r.get('success', False)]
        self.assertGreater(len(valid_results), 0, "Should have at least one valid result")
    
    def test_state_transformation_between_agents(self):
        """Test that workflow state is properly transformed between agents."""
        mock_responses = [
            '{"test": "data"}',
            '{"test": "data"}',  # For second document
            '{"test": "data"}',  # For extraction
            '{"test": "data"}'   # For extraction
        ]
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = MockLLMGateway(mock_responses)
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': 'Analyze: {corpus_text}',
            'project_path': str(self.project_path),
            'initial_key': 'should_be_preserved'
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # Verify state preservation and transformation
        final_state = result['final_state']
        
        # Initial state should be preserved
        self.assertEqual(final_state['initial_key'], 'should_be_preserved')
        
        # Analysis results should be added
        self.assertIn('analysis_results', final_state)
        
        # Session information should be added
        self.assertIn('session_results_path', final_state)
        self.assertIn('conversation_id', final_state)

class WorkflowPerformanceTests(unittest.TestCase):
    """
    Tests for workflow performance and efficiency.
    
    These tests ensure the THIN architecture maintains high velocity.
    """
    
    def setUp(self):
        """Set up performance test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "perf_test"
        self.project_path.mkdir()
        
        # Create larger corpus for performance testing
        self.corpus_path = self.project_path / "corpus"
        self.corpus_path.mkdir()
        
        # Create 10 test documents
        for i in range(10):
            (self.corpus_path / f"doc{i}.txt").write_text(f"Test document {i} content.")
    
    def tearDown(self):
        """Clean up performance test files."""
        shutil.rmtree(self.temp_dir)
    
    def test_workflow_scales_with_corpus_size(self):
        """Test that workflow performance scales reasonably with corpus size."""
        import time
        
        # Create mock responses for 10 documents
        mock_responses = [f'{{"doc": {i}}}' for i in range(10)]
        mock_responses += mock_responses  # Double for extraction
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = MockLLMGateway(mock_responses)
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': ['mock_model'],
                'num_runs': 1
            },
            'analysis_agent_instructions': 'Analyze: {corpus_text}',
            'project_path': str(self.project_path)
        }
        
        start_time = time.time()
        result = orchestrator.execute_workflow(workflow_state)
        end_time = time.time()
        
        # Should complete successfully
        self.assertEqual(result['status'], 'success')
        
        # Should process all documents
        self.assertEqual(len(result['final_state']['analysis_results']), 10)
        
        # Should complete in reasonable time (< 5 seconds for mocked responses)
        execution_time = end_time - start_time
        self.assertLess(execution_time, 5.0, f"Workflow took too long: {execution_time:.2f} seconds")

if __name__ == '__main__':
    print("🔧 Running Workflow Integration Tests for THIN/THICK Architecture")
    print("=" * 60)
    print("These tests focus on orchestration and agent handoffs,")
    print("not individual agent logic.")
    print("=" * 60)
    
    unittest.main(verbosity=2) 