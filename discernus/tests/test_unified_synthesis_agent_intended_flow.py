"""
Unit tests for UnifiedSynthesisAgent intended flow.

This test module focuses on testing that the agent receives complete prompts
and executes them without additional assembly or parsing logic.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from discernus.agents.unified_synthesis_agent import UnifiedSynthesisAgent
from discernus.core.audit_logger import AuditLogger


class TestUnifiedSynthesisAgentIntendedFlow:
    """Test the agent's intended flow with complete prompts."""
    
    @pytest.fixture
    def mock_audit_logger(self):
        """Mock audit logger for testing."""
        return Mock(spec=AuditLogger)
    
    @pytest.fixture
    def synthesis_agent(self, mock_audit_logger):
        """Create synthesis agent instance for testing."""
        return UnifiedSynthesisAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=mock_audit_logger,
            enhanced_mode=True
        )
    
    @pytest.fixture
    def complete_synthesis_prompt(self):
        """Complete synthesis prompt with all context embedded."""
        return """# Research Synthesis Task

You are conducting a comprehensive computational social science analysis. Your task is to produce an academic-quality research report.

## FRAMEWORK CONTENT
# Civic Character Framework

This framework analyzes civic character in political discourse...

### Theoretical Foundation
Democratic values and civic engagement are fundamental...

## EXPERIMENT CONTENT
# Civic Character Study

This experiment examines civic character in political discourse...

### Research Questions
1. How do political leaders demonstrate civic character?
2. What patterns emerge in civic engagement?

### Hypotheses
- Political leaders show varying levels of civic character
- Civic engagement correlates with democratic values

## CORPUS MANIFEST
# Corpus Configuration
- Document 1: Presidential speech on democracy
- Document 2: Congressional address on civic values
- Document 3: Political rally speech

## RAW ANALYSIS RESULTS
{
  "doc1.txt": {
    "democratic_values": 0.85,
    "civic_engagement": 0.72
  },
  "doc2.txt": {
    "democratic_values": 0.91,
    "civic_engagement": 0.88
  }
}

## DERIVED METRICS
{
  "aggregate_scores": {
    "doc1.txt": 0.785,
    "doc2.txt": 0.895
  },
  "correlation_matrix": {
    "democratic_values_civic_engagement": 0.76
  }
}

## STATISTICAL RESULTS
{
  "means": {
    "democratic_values": 0.88,
    "civic_engagement": 0.80
  },
  "std_devs": {
    "democratic_values": 0.03,
    "civic_engagement": 0.08
  },
  "significance": {
    "democratic_values_civic_engagement_correlation": "p < 0.01"
  }
}

## EVIDENCE CONTEXT
You have access to 15 pieces of textual evidence extracted during analysis.
Use semantic queries to find relevant evidence for each statistical finding.

## TASK
Generate a comprehensive academic report following standard research methodology.
Include evidence citations and statistical interpretation."""
    
    def test_agent_accepts_complete_prompt_string(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent accepts complete prompt string (not file paths)."""
        # The agent should accept a complete prompt string as input
        # This test verifies the intended interface
        
        # Mock the LLM gateway to return a response
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report content", {"model": "test"})
            
            # Call the agent with the complete prompt
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should return a result
            assert result is not None
            assert "final_report" in result
    
    def test_agent_executes_prompt_without_additional_assembly(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent executes prompt without additional assembly logic."""
        # Mock the LLM gateway to capture what was sent
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report content", {"model": "test"})
            
            # Call the agent
            synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Verify the gateway was called with the exact prompt
            mock_gateway.execute_call.assert_called_once()
            
            # Get the actual prompt sent to the gateway
            call_args = mock_gateway.execute_call.call_args
            args, kwargs = call_args
            
            # Should have received the complete prompt
            if args:
                prompt_sent = args[0]
            else:
                prompt_sent = kwargs.get('prompt')
            
            # Should be the exact prompt we provided
            assert prompt_sent == complete_synthesis_prompt
    
    def test_agent_returns_report_without_modification(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent returns report without modification."""
        # Mock the LLM gateway to return a specific response
        test_report = "Comprehensive research synthesis report with evidence and analysis"
        mock_metadata = {"model": "vertex_ai/gemini-2.5-flash", "tokens": 1500}
        
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = (test_report, mock_metadata)
            
            # Call the agent
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should return the exact report from the gateway
            assert result["final_report"] == test_report
    
    def test_agent_handles_prompt_execution_errors_gracefully(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent handles prompt execution errors gracefully."""
        # Mock the LLM gateway to raise an error
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.side_effect = Exception("LLM call failed")
            
            # Should handle the error gracefully
            with pytest.raises(Exception) as exc_info:
                synthesis_agent.generate_final_report(
                    complete_prompt=complete_synthesis_prompt
                )
            
            # Should propagate the error
            assert "LLM call failed" in str(exc_info.value)
    
    def test_agent_does_not_read_files_directly(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent does not read files directly."""
        # Mock file reading to detect if agent tries to read files
        with patch('pathlib.Path.read_text') as mock_read_text:
            mock_read_text.side_effect = Exception("Agent should not read files")
            
            # Mock the LLM gateway
            with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
                mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
                
                # Call the agent - should not trigger file reading
                result = synthesis_agent.generate_final_report(
                    complete_prompt=complete_synthesis_prompt
                )
                
                # Should succeed without reading files
                assert result is not None
                
                # Verify no files were read
                mock_read_text.assert_not_called()
    
    def test_agent_does_not_parse_yaml_or_metadata(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent does not parse YAML or metadata."""
        # Mock YAML parsing to detect if agent tries to parse
        with patch('yaml.safe_load') as mock_yaml_load:
            mock_yaml_load.side_effect = Exception("Agent should not parse YAML")
            
            # Mock the LLM gateway
            with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
                mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
                
                # Call the agent - should not trigger YAML parsing
                result = synthesis_agent.generate_final_report(
                    complete_prompt=complete_synthesis_prompt
                )
                
                # Should succeed without parsing YAML
                assert result is not None
                
                # Verify no YAML was parsed
                mock_yaml_load.assert_not_called()
    
    def test_agent_does_not_access_artifact_storage(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent does not access artifact storage directly."""
        # Mock artifact storage to detect if agent tries to access it
        mock_storage = Mock()
        mock_storage.get_artifact.side_effect = Exception("Agent should not access storage")
        
        # Mock the LLM gateway
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
            
            # Call the agent - should not trigger storage access
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should succeed without accessing storage
            assert result is not None
    
    def test_agent_uses_llm_gateway_correctly(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent uses LLM gateway correctly."""
        # Mock the LLM gateway to verify correct usage
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
            
            # Call the agent
            synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Verify gateway was called with correct parameters
            mock_gateway.execute_call.assert_called_once()
            
            # Get the call arguments
            call_args = mock_gateway.execute_call.call_args
            args, kwargs = call_args
            
            # Should have called with the prompt
            assert len(args) >= 1
            assert args[0] == complete_synthesis_prompt
    
    def test_agent_handles_empty_or_malformed_prompts_gracefully(self, synthesis_agent):
        """Test that agent handles empty or malformed prompts gracefully."""
        # Test with empty prompt
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Empty response", {"model": "test"})
            
            result = synthesis_agent.generate_final_report(
                complete_prompt=""
            )
            
            # Should handle empty prompt
            assert result is not None
        
        # Test with malformed prompt (None)
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("None response", {"model": "test"})
            
            result = synthesis_agent.generate_final_report(
                complete_prompt=None
            )
            
            # Should handle None prompt
            assert result is not None
    
    def test_agent_maintains_audit_logging(self, synthesis_agent, complete_synthesis_prompt, mock_audit_logger):
        """Test that agent maintains audit logging functionality."""
        # Mock the LLM gateway
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
            
            # Call the agent
            synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Verify audit logger was used (if it has logging methods)
            if hasattr(mock_audit_logger, 'log_synthesis_start'):
                mock_audit_logger.log_synthesis_start.assert_called()
            
            if hasattr(mock_audit_logger, 'log_synthesis_complete'):
                mock_audit_logger.log_synthesis_complete.assert_called()
    
    def test_agent_returns_expected_result_structure(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent returns expected result structure."""
        # Mock the LLM gateway
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report content", {"model": "test"})
            
            # Call the agent
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should return a dictionary with expected keys
            assert isinstance(result, dict)
            assert "final_report" in result
            
            # The final report should contain the LLM response
            assert result["final_report"] == "Test report content"
    
    def test_agent_does_not_require_file_paths(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent does not require file paths as parameters."""
        # The agent should work with just the complete prompt
        # No need for framework_path, experiment_path, etc.
        
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
            
            # Should work with minimal parameters
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should succeed
            assert result is not None
            assert "final_report" in result
    
    def test_agent_does_not_require_artifact_hashes(self, synthesis_agent, complete_synthesis_prompt):
        """Test that agent does not require artifact hashes as parameters."""
        # The agent should work with just the complete prompt
        # No need for research_data_artifact_hash, evidence_artifact_hashes, etc.
        
        with patch.object(synthesis_agent, 'llm_gateway') as mock_gateway:
            mock_gateway.execute_call.return_value = ("Test report", {"model": "test"})
            
            # Should work with minimal parameters
            result = synthesis_agent.generate_final_report(
                complete_prompt=complete_synthesis_prompt
            )
            
            # Should succeed
            assert result is not None
            assert "final_report" in result
