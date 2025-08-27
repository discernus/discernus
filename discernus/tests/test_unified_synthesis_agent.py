import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from discernus.agents.unified_synthesis_agent import UnifiedSynthesisAgent
from pathlib import Path

class TestUnifiedSynthesisAgent(unittest.TestCase):

    def setUp(self):
        """Set up common test resources."""
        self.mock_audit_logger = MagicMock()
        # FIX: Configure the mock artifact storage to return valid JSON data
        self.mock_artifact_storage = MagicMock()
        mock_research_data = '{"statistical_results": {"mean": 0.5}}'
        self.mock_artifact_storage.get_artifact.return_value = mock_research_data.encode('utf-8')
        
        # Mock paths for the test
        self.mock_framework_path = Path("mock_framework.md")
        self.mock_experiment_path = Path("mock_experiment.md")

    @patch('pathlib.Path.read_text')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='---\nkey: value')
    @patch('yaml.safe_load')
    def test_generate_final_report_uses_rag_index(self, mock_safe_load, mock_open, mock_read_text):
        """
        Test that generate_final_report accepts a RAG index object and
        uses its 'search' method to retrieve evidence.
        This test will fail until the agent is refactored.
        """
        # Arrange
        mock_safe_load.return_value = {'template': 'Report: {evidence_context}'}
        # Mock the content that would be read from the framework and experiment files
        mock_read_text.return_value = "Mock file content"
        
        agent = UnifiedSynthesisAgent(audit_logger=self.mock_audit_logger, enhanced_mode=False)

        # Create a mock RAG index object with a 'search' method
        mock_rag_index = MagicMock()
        # FIX: The mock return value must match the data structure the agent expects.
        # The agent's implementation looks for a 'source_quote' key.
        mock_rag_index.search.return_value = [{'source_quote': 'mock evidence quote'}]

        # Mock the LLM gateway to prevent actual API calls
        with patch.object(agent.llm_gateway, 'execute_call', return_value=("Final Report with mock evidence quote", {})) as mock_execute_call:
            # Act
            # This call will raise a TypeError because the method signature is incorrect
            agent.generate_final_report(
                framework_path=self.mock_framework_path,
                experiment_path=self.mock_experiment_path,
                research_data_artifact_hash="mock_hash",
                # This is the key change: passing the RAG object instead of hashes
                rag_index=mock_rag_index,
                artifact_storage=self.mock_artifact_storage
            )

            # Assert
            # Verify the RAG index's search method was called
            mock_rag_index.search.assert_called_once()

            # Verify the report contains the evidence from the RAG index
            final_prompt = mock_execute_call.call_args[1]['prompt']
            self.assertIn("mock evidence quote", final_prompt)
            
    def test_placeholder(self):
        """A placeholder test to ensure the file is created correctly."""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
