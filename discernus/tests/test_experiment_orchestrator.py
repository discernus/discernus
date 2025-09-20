import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd

# from discernus.core.deprecated.experiment_orchestrator import ExperimentOrchestrator

class TestExperimentOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up a mock environment for the orchestrator."""
        # Patch all external dependencies initialized in the orchestrator's constructor
        with patch('discernus.core.experiment_orchestrator.ExperimentSecurityBoundary'), \
             patch('discernus.core.experiment_orchestrator.DiscernusConsole'), \
             patch('discernus.core.experiment_orchestrator.setup_logging'), \
             patch('discernus.core.experiment_orchestrator.get_logger'):
            
            self.orchestrator = ExperimentOrchestrator(
                experiment_path=Path("/fake/experiment")
            )
            # Manually attach mock objects needed for the test
            self.orchestrator.artifact_storage = MagicMock()

    @patch('discernus.core.experiment_orchestrator.AnalysisAgent')
    def test_run_analysis_phase_returns_artifact_paths(self, MockAnalysisAgent):
        """
        Verify that _run_analysis_phase correctly collects and returns artifact paths.
        """
        # 1. Setup Mocks
        mock_agent_instance = MockAnalysisAgent.return_value
        mock_agent_instance.analyze_batch.return_value = {"dimensional_scores": {}}

        # Mock the artifact storage, as the orchestrator now uses it directly
        mock_storage = self.orchestrator.artifact_storage
        mock_storage.put_artifact.return_value = "dummy_hash"
        mock_storage.get_artifact_metadata.return_value = {
            "artifact_path": "artifacts/analysis_result_dummy_hash.json"
        }
        mock_storage.run_folder = Path("/fake/run") # Needed for path construction

        mock_documents = [
            {'filename': 'doc1.txt', 'metadata': {}, 'document_id': 'doc1'},
            {'filename': 'doc2.txt', 'metadata': {}, 'document_id': 'doc2'}
        ]
        
        # Mock config that would be loaded by _load_specs
        mock_config = {
            'framework': 'framework.md',
            'corpus': 'corpus.md',
            'metadata': {'corpus_name': 'Mock Corpus'}
        }
        
        # Mock the physical existence of the document files
        mock_doc_path = MagicMock(spec=Path)
        mock_doc_path.exists.return_value = True
        mock_doc_path.read_text.return_value = "file content"

        # 2. Run the method under test
        # We patch the orchestrator's internal methods for loading data
        with patch.object(self.orchestrator, '_load_specs', return_value=mock_config), \
             patch.object(self.orchestrator, '_load_corpus_documents', return_value=mock_documents), \
             patch('pathlib.Path.read_text', return_value="---\n# Mock Framework\n---"), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.glob', return_value=[Path('doc1.txt'), Path('doc2.txt')]):
            
            # Manually set the config because _load_specs is mocked
            self.orchestrator.config = mock_config

            artifact_paths = self.orchestrator._run_analysis_phase(
                analysis_model="mock_model",
                audit_logger=MagicMock()
            )

        # 3. Assertions
        self.assertEqual(len(artifact_paths), 2)
        self.assertIsInstance(artifact_paths[0], Path)
        self.assertEqual(artifact_paths[0].name, "analysis_result_dummy_hash.json")
        
        # Verify that the agent and storage were called for each document
        self.assertEqual(mock_agent_instance.analyze_batch.call_count, 2)
        self.assertEqual(mock_storage.put_artifact.call_count, 2)
        self.assertEqual(mock_storage.get_artifact_metadata.call_count, 2)

if __name__ == '__main__':
    unittest.main()
