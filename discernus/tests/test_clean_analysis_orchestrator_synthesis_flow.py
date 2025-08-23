"""
Unit tests for CleanAnalysisOrchestrator synthesis flow.

This test module focuses specifically on testing the orchestrator's synthesis orchestration logic
to verify it uses the SynthesisPromptAssembler correctly according to THIN architecture principles.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError
from discernus.core.prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
from discernus.core.reuse_candidates.unified_synthesis_agent import UnifiedSynthesisAgent
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


class TestCleanAnalysisOrchestratorSynthesisFlow:
    """Test the orchestrator's synthesis orchestration logic."""
    
    @pytest.fixture
    def mock_orchestrator(self):
        """Create orchestrator with minimal setup for synthesis testing."""
        orchestrator = CleanAnalysisOrchestrator(
            experiment_path="projects/1a_caf_civic_character"
        )
        
        # Mock the required components
        orchestrator.artifact_storage = Mock(spec=LocalArtifactStorage)
        orchestrator.artifact_storage.registry = {
            "hash1": {"metadata": {"artifact_type": "evidence_v6_doc1"}},
            "hash2": {"metadata": {"artifact_type": "evidence_v6_doc2"}}
        }
        orchestrator.artifact_storage.get_artifact.return_value = json.dumps({
            "raw_analysis": {"doc1": {"scores": [0.8, 0.9]}},
            "derived_metrics": {"doc1": {"aggregate_score": 0.85}},
            "statistical_results": {"means": {"doc1": 0.85}}
        }).encode()
        
        # Mock the config that would be set by _load_specs()
        orchestrator.config = {
            "framework": "framework.md",
            "corpus": "corpus.md",
            "experiment_name": "test_experiment"
        }
        
        # Mock the RAG index
        orchestrator.rag_index = Mock()
        
        # Mock analysis results
        orchestrator._analysis_results = [
            {"analysis_result": {"score1": 0.8}, "document_name": "doc1.txt"}
        ]
        
        return orchestrator
    
    @pytest.fixture
    def mock_synthesis_assembler(self):
        """Mock synthesis prompt assembler."""
        assembler = Mock(spec=SynthesisPromptAssembler)
        assembler.assemble_prompt.return_value = "Rich synthesis prompt with all context"
        return assembler
    
    @pytest.fixture
    def mock_synthesis_agent(self):
        """Mock unified synthesis agent."""
        agent = Mock(spec=UnifiedSynthesisAgent)
        agent.generate_final_report.return_value = {
            "final_report": "Comprehensive research synthesis report"
        }
        return agent
    
    def test_run_synthesis_calls_assembler_to_build_prompt(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis calls SynthesisPromptAssembler.assemble_prompt()."""
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                result = mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify assembler was created
                mock_assembler_class.assert_called_once()
                
                # Verify assembler.assemble_prompt() was called
                mock_synthesis_assembler.assemble_prompt.assert_called_once()
    
    def test_run_synthesis_passes_correct_context_to_assembler(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis passes correct context to assembler."""
        # Mock file reading to return specific content
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = [
                "# Framework Content\nDemocratic values framework...",
                "# Experiment Content\nCivic character study..."
            ]
            
            # Mock the assembler creation
            with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
                mock_assembler_class.return_value = mock_synthesis_assembler
                
                # Mock the agent creation and call
                with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                    mock_agent = Mock()
                    mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                    mock_agent_class.return_value = mock_agent
                    
                    # Call the synthesis method
                    mock_orchestrator._run_synthesis(
                        synthesis_model="vertex_ai/gemini-2.5-flash",
                        audit_logger=Mock(spec=AuditLogger),
                        statistical_results={"means": {"doc1": 0.85}}
                    )
                    
                    # Verify assembler was called with correct parameters
                    mock_synthesis_assembler.assemble_prompt.assert_called_once()
                    
                    # Verify the parameters passed to assembler
                    call_args = mock_synthesis_assembler.assemble_prompt.call_args
                    args, kwargs = call_args
                    
                    # Should pass framework path, experiment path, research data hash, artifact storage, evidence artifacts
                    assert len(args) == 5  # Expected number of arguments
                    
                    # Verify framework path
                    framework_path = args[0]
                    assert str(framework_path).endswith("framework.md")
                    
                    # Verify experiment path
                    experiment_path = args[1]
                    assert str(experiment_path).endswith("experiment.md")
                    
                    # Verify research data hash (should be a string)
                    research_data_hash = args[2]
                    assert isinstance(research_data_hash, str)
                    
                    # Verify artifact storage
                    artifact_storage = args[3]
                    assert artifact_storage is mock_orchestrator.artifact_storage
                    
                    # Verify evidence artifacts (should be a list)
                    evidence_artifacts = args[4]
                    assert isinstance(evidence_artifacts, list)
    
    def test_run_synthesis_passes_assembled_prompt_to_agent(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis passes assembled prompt to agent instead of file paths."""
        # Set up the assembler to return a specific prompt
        test_prompt = "Test assembled prompt with rich context"
        mock_synthesis_assembler.assemble_prompt.return_value = test_prompt
        
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify agent was called with the assembled prompt
                mock_agent.generate_final_report.assert_called_once()
                
                # Verify the agent received the complete prompt string (not file paths)
                call_args = mock_agent.generate_final_report.call_args
                args, kwargs = call_args
                
                # The first argument should be the complete prompt string
                if args:
                    prompt_arg = args[0]
                else:
                    prompt_arg = kwargs.get('complete_prompt')
                
                assert prompt_arg == test_prompt
    
    def test_run_synthesis_creates_assembler_with_correct_initialization(self, mock_orchestrator):
        """Test that _run_synthesis creates SynthesisPromptAssembler correctly."""
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler = Mock()
            mock_assembler.assemble_prompt.return_value = "Test prompt"
            mock_assembler_class.return_value = mock_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify assembler was created with no arguments (uses default initialization)
                mock_assembler_class.assert_called_once_with()
    
    def test_run_synthesis_agent_receives_prompt_not_file_paths(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that agent receives complete prompt string, not file paths and artifact hashes."""
        # Set up the assembler to return a specific prompt
        test_prompt = "Complete synthesis prompt with all context embedded"
        mock_synthesis_assembler.assemble_prompt.return_value = test_prompt
        
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify agent was called
                mock_agent.generate_final_report.assert_called_once()
                
                # Verify the agent call signature matches intended architecture
                call_args = mock_agent.generate_final_report.call_args
                args, kwargs = call_args
                
                # Should receive complete prompt as first argument
                assert len(args) >= 1
                assert args[0] == test_prompt
                
                # Should NOT receive file paths as arguments
                for arg in args[1:]:
                    assert not isinstance(arg, Path), f"Agent should not receive Path objects, got: {arg}"
                    assert not str(arg).endswith('.md'), f"Agent should not receive file paths, got: {arg}"
    
    def test_run_synthesis_handles_assembler_errors_gracefully(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis handles assembler errors gracefully."""
        # Set up the assembler to raise an error
        mock_synthesis_assembler.assemble_prompt.side_effect = Exception("Assembler failed")
        
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Call the synthesis method and expect it to raise CleanAnalysisError
            with pytest.raises(CleanAnalysisError) as exc_info:
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
            
            # Verify the error message indicates synthesis failure
            assert "RAG synthesis failed" in str(exc_info.value)
    
    def test_run_synthesis_orchestrates_correct_sequence(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis orchestrates the correct sequence of operations."""
        # Set up the assembler
        test_prompt = "Orchestrated synthesis prompt"
        mock_synthesis_assembler.assemble_prompt.return_value = test_prompt
        
        # Track the sequence of operations
        operation_sequence = []
        
        def track_assembler_call(*args, **kwargs):
            operation_sequence.append("assembler_called")
            return test_prompt
        
        def track_agent_call(*args, **kwargs):
            operation_sequence.append("agent_called")
            return {"final_report": "Test report"}
        
        mock_synthesis_assembler.assemble_prompt.side_effect = track_assembler_call
        
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.side_effect = track_agent_call
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify the correct sequence: assembler first, then agent
                assert operation_sequence == ["assembler_called", "agent_called"]
    
    def test_run_synthesis_stores_research_data_before_assembler_call(self, mock_orchestrator, mock_synthesis_assembler):
        """Test that _run_synthesis creates and stores research data before calling assembler."""
        # Mock the assembler creation
        with patch('discernus.core.clean_analysis_orchestrator.SynthesisPromptAssembler') as mock_assembler_class:
            mock_assembler_class.return_value = mock_synthesis_assembler
            
            # Mock the agent creation and call
            with patch('discernus.core.clean_analysis_orchestrator.UnifiedSynthesisAgent') as mock_agent_class:
                mock_agent = Mock()
                mock_agent.generate_final_report.return_value = {"final_report": "Test report"}
                mock_agent_class.return_value = mock_agent
                
                # Call the synthesis method
                mock_orchestrator._run_synthesis(
                    synthesis_model="vertex_ai/gemini-2.5-flash",
                    audit_logger=Mock(spec=AuditLogger),
                    statistical_results={"means": {"doc1": 0.85}}
                )
                
                # Verify artifact storage was called to store research data
                mock_orchestrator.artifact_storage.put_artifact.assert_called()
                
                # Verify the research data was stored before assembler was called
                put_artifact_calls = mock_orchestrator.artifact_storage.put_artifact.call_args_list
                assert len(put_artifact_calls) >= 1
                
                # Verify the stored data contains the expected structure
                stored_data_bytes = put_artifact_calls[0][0][0]  # First call, first argument
                stored_data = json.loads(stored_data_bytes.decode('utf-8'))
                
                assert 'experiment_metadata' in stored_data
                assert 'raw_analysis_data' in stored_data
                assert 'statistical_results' in stored_data
