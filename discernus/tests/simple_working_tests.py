#!/usr/bin/env python3
"""
Simple Working Tests for AI Agents
==================================

These tests are designed to ACTUALLY WORK out of the box for AI agents.
No complex mock setup, no fragile integration tests, no mysterious failures.

Philosophy: 
- One test, one assertion
- Clear success/failure signals
- Standard Python testing patterns
- Minimal dependencies
- Obvious how to fix when broken

Usage:
    python3 discernus/tests/simple_working_tests.py
    python3 -m unittest discernus.tests.simple_working_tests.TestBasicFunctionality.test_imports_work -v
"""

import unittest
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests that should always pass."""
    
    def test_imports_work(self):
        """Test that core imports work without errors."""
        try:
            from discernus.agents.analysis_agent import AnalysisAgent
            from discernus.agents.calculation_agent import CalculationAgent
            from discernus.agents.data_extraction_agent import DataExtractionAgent
            from discernus.agents.synthesis_agent import SynthesisAgent
            from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
            from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_mock_gateway_basic_functionality(self):
        """Test that MockLLMGateway works with simple responses."""
        from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        
        # Simple queue-based responses
        mock_gateway = MockLLMGateway(["response1", "response2"])
        
        # Test first call
        response1, metadata1 = mock_gateway.execute_call("test_model", "test_prompt")
        self.assertEqual(response1, "response1")
        self.assertTrue(metadata1["success"])
        
        # Test second call
        response2, metadata2 = mock_gateway.execute_call("test_model", "test_prompt")
        self.assertEqual(response2, "response2")
        self.assertTrue(metadata2["success"])
        
        # Test exhausted queue
        response3, metadata3 = mock_gateway.execute_call("test_model", "test_prompt")
        self.assertEqual(response3, "")
        self.assertFalse(metadata3["success"])
        self.assertIn("No mock response found", metadata3["error"])

class TestAgentBasics(unittest.TestCase):
    """Basic agent functionality tests."""
    
    def test_analysis_agent_initializes(self):
        """Test that AnalysisAgent can be created without errors."""
        from discernus.agents.analysis_agent import AnalysisAgent
        from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        
        mock_gateway = MockLLMGateway(['{"test": "response"}'])
        agent = AnalysisAgent(gateway=mock_gateway)  # type: ignore
        self.assertIsNotNone(agent)
        self.assertEqual(agent.gateway, mock_gateway)
    
    def test_calculation_agent_initializes(self):
        """Test that CalculationAgent can be created without errors."""
        from discernus.agents.calculation_agent import CalculationAgent
        
        agent = CalculationAgent()
        self.assertIsNotNone(agent)
    
    def test_data_extraction_agent_initializes(self):
        """Test that DataExtractionAgent can be created without errors."""
        from discernus.agents.data_extraction_agent import DataExtractionAgent
        from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        
        mock_gateway = MockLLMGateway(['{"test": "response"}'])
        agent = DataExtractionAgent(gateway=mock_gateway)  # type: ignore
        self.assertIsNotNone(agent)
        self.assertEqual(agent.gateway, mock_gateway)

class TestSimpleWorkflows(unittest.TestCase):
    """Simple workflow tests that actually work."""
    
    def test_calculation_agent_simple_calculation(self):
        """Test CalculationAgent with a simple calculation that should work."""
        from discernus.agents.calculation_agent import CalculationAgent
        
        agent = CalculationAgent()
        
        # Simple test data that should work
        workflow_state = {
            'framework': {
                'calculation_spec': [
                    {'name': 'simple_test', 'formula': '2 + 3'}
                ]
            },
            'analysis_results': [
                {
                    'success': True,
                    'json_output': {'score': 0.5}
                }
            ]
        }
        
        result = agent.execute(workflow_state, {})
        
        # Verify the calculation was performed
        self.assertIn('analysis_results', result)
        self.assertEqual(len(result['analysis_results']), 1)
        self.assertIn('simple_test', result['analysis_results'][0]['json_output'])
        self.assertEqual(result['analysis_results'][0]['json_output']['simple_test'], 5)
    
    def test_data_extraction_agent_simple_json(self):
        """Test DataExtractionAgent with simple, valid JSON."""
        from discernus.agents.data_extraction_agent import DataExtractionAgent
        from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        
        # Simple JSON response that should work
        mock_gateway = MockLLMGateway(['{"score": 0.8, "category": "positive"}'])
        agent = DataExtractionAgent(gateway=mock_gateway)  # type: ignore
        
        # Simple test data
        workflow_state = {
            'analysis_results': [
                {
                    'agent_id': 'test_agent',
                    'success': True,
                    'raw_response': '{"score": 0.8, "category": "positive"}'
                }
            ]
        }
        
        result = agent.execute(workflow_state, {})
        
        # Verify JSON was extracted
        self.assertIn('analysis_results', result)
        self.assertEqual(len(result['analysis_results']), 1)
        self.assertIn('extracted_json', result['analysis_results'][0])
        self.assertEqual(result['analysis_results'][0]['extracted_json']['score'], 0.8)
        self.assertEqual(result['analysis_results'][0]['extracted_json']['category'], 'positive')
        
        # Verify extraction status
        self.assertTrue(result['analysis_results'][0]['extraction_success'])
        self.assertIsNone(result['analysis_results'][0]['extraction_error'])

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions from the enhanced __init__.py."""
    
    def test_check_test_environment(self):
        """Test that check_test_environment works."""
        from discernus.tests import check_test_environment
        
        status = check_test_environment()
        
        # Should return a dict with expected keys
        self.assertIsInstance(status, dict)
        self.assertIn('python_version', status)
        self.assertIn('working_directory', status)
        self.assertIn('project_root_detected', status)
        self.assertIn('venv_active', status)
        self.assertIn('required_packages', status)
        
        # Should detect project root correctly
        self.assertTrue(status['project_root_detected'])


class TestProvenanceSystem(unittest.TestCase):
    """Test provenance system components for academic integrity."""
    
    def test_chronolog_event_logging(self):
        """Test that chronolog events are logged correctly."""
        from discernus.core.project_chronolog import get_project_chronolog
        import tempfile
        import os
        
        # Create temporary project
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = os.path.join(tmp_dir, 'test_project')
            os.makedirs(project_path)
            
            # Initialize chronolog
            chronolog = get_project_chronolog(project_path)
            
            # Log an event
            event_id = chronolog.log_event('TEST_EVENT', 'test_session', {'test_data': 'test_value'})
            
            # Verify event was logged
            self.assertIsNotNone(event_id)
            self.assertIsInstance(event_id, str)
            
            # Verify chronolog file exists
            chronolog_file = os.path.join(project_path, 'PROJECT_CHRONOLOG_test_project.jsonl')
            self.assertTrue(os.path.exists(chronolog_file))
    
    def test_chronolog_integrity_verification(self):
        """Test that chronolog integrity verification works."""
        from discernus.core.project_chronolog import get_project_chronolog
        import tempfile
        import os
        
        # Create temporary project
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = os.path.join(tmp_dir, 'test_project')
            os.makedirs(project_path)
            
            # Initialize chronolog and log events
            chronolog = get_project_chronolog(project_path)
            chronolog.log_event('TEST_EVENT_1', 'test_session', {'data': 'value1'})
            chronolog.log_event('TEST_EVENT_2', 'test_session', {'data': 'value2'})
            
            # Verify integrity
            result = chronolog.verify_integrity()
            
            # Should pass verification
            self.assertTrue(result['verified'])
            self.assertEqual(result['verified_events'], 2)
            self.assertEqual(len(result['corrupted_events']), 0)
    
    def test_conversation_logger_captures_llm_interactions(self):
        """Test that conversation logger captures LLM messages."""
        from discernus.core.conversation_logger import ConversationLogger
        import tempfile
        import os
        
        # Create temporary project
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = os.path.join(tmp_dir, 'test_project')
            os.makedirs(project_path)
            
            # Initialize conversation logger
            logger = ConversationLogger(project_path)
            
            # Start conversation and log message
            conversation_id = logger.start_conversation('Test text', 'Test question', ['test_agent'])
            logger.log_llm_message(conversation_id, 'test_agent', 'Test response', {'model': 'test_model'})
            
            # Verify conversation file exists
            conversations_dir = os.path.join(project_path, 'conversations')
            self.assertTrue(os.path.exists(conversations_dir))
            
            # Check conversation file was created
            conversation_files = [f for f in os.listdir(conversations_dir) if f.endswith('.jsonl')]
            self.assertEqual(len(conversation_files), 1)
    
    def test_provenance_system_integration(self):
        """Test that provenance integrates with workflow orchestrator."""
        from discernus.core.project_chronolog import log_project_event
        import tempfile
        import os
        
        # Create temporary project
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = os.path.join(tmp_dir, 'test_project')
            os.makedirs(project_path)
            
            # Test the log_project_event convenience function (used by orchestrator)
            event_id = log_project_event(project_path, 'WORKFLOW_TEST', 'test_session', {'test': 'data'})
            
            # Verify event was logged
            self.assertIsNotNone(event_id)
            
            # Verify chronolog file exists
            chronolog_file = os.path.join(project_path, 'PROJECT_CHRONOLOG_test_project.jsonl')
            self.assertTrue(os.path.exists(chronolog_file))
            
            # Verify file contains the event
            with open(chronolog_file, 'r') as f:
                content = f.read()
                self.assertIn('WORKFLOW_TEST', content)
                self.assertIn('test_session', content)


if __name__ == '__main__':
    # Print helpful information for AI agents
    print("🧪 Running Simple Working Tests for AI Agents")
    print("=" * 50)
    print("These tests are designed to ACTUALLY WORK out of the box.")
    print("If any test fails, it indicates a real problem that needs fixing.")
    print("=" * 50)
    
    unittest.main(verbosity=2) 