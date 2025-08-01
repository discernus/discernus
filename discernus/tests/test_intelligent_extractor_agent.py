#!/usr/bin/env python3
"""
Unit tests for Intelligent Extractor Agent
==========================================

Tests the core functionality of the Intelligent Extractor Agent,
including semantic extraction, error handling, and framework-agnostic design.
"""

import json
import pytest
from unittest.mock import Mock, patch
from discernus.agents.intelligent_extractor_agent import (
    IntelligentExtractorAgent, 
    ExtractionResult,
    IntelligentExtractorError
)


class TestIntelligentExtractorAgent:
    """Test suite for Intelligent Extractor Agent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = IntelligentExtractorAgent(
            model="vertex_ai/gemini-2.5-flash",
            max_retries=2,
            timeout_seconds=10
        )
        
        # Sample gasket schema for testing
        self.sample_gasket_schema = {
            "target_keys": [
                "dignity_score",
                "tribalism_score", 
                "dignity_tribalism_tension",
                "truth_score",
                "manipulation_score"
            ],
            "target_dimensions": [
                "Dignity",
                "Tribalism",
                "Dignity-Tribalism Tension", 
                "Truth",
                "Manipulation"
            ]
        }
        
        # Sample raw analysis log
        self.sample_raw_analysis = """
        Character Assessment Framework Analysis:
        
        The dignity dimension shows strong presence with a score of 0.85, reflecting
        the speaker's respectful tone and institutional language.
        
        Tribalism is minimal at 0.15, with limited us-vs-them rhetoric.
        
        The dignity-tribalism tension calculates to 0.70 (|0.85 - 0.15|).
        
        Truth-seeking behavior is evident with a score of 0.78, while
        manipulation tactics are barely present at 0.12.
        """
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = IntelligentExtractorAgent(
            model="test-model",
            max_retries=5,
            timeout_seconds=20
        )
        
        assert agent.model == "test-model"
        assert agent.agent_name == "IntelligentExtractorAgent"
        assert agent.max_retries == 5
        assert agent.timeout_seconds == 20
        assert agent.llm_gateway is not None
    
    def test_create_extraction_prompt(self):
        """Test extraction prompt creation."""
        prompt = self.agent._create_extraction_prompt(
            self.sample_raw_analysis,
            self.sample_gasket_schema
        )
        
        # Check prompt contains required elements
        assert "data extraction and semantic mapping bot" in prompt
        assert "Dignity" in prompt
        assert "dignity_score" in prompt
        assert "TEXT TO ANALYZE:" in prompt
        assert self.sample_raw_analysis in prompt
        assert "0.0 and 1.0" in prompt
        assert "valid JSON object" in prompt
    
    def test_parse_extraction_response_success(self):
        """Test successful parsing of extraction response."""
        # Mock successful LLM response
        mock_response = json.dumps({
            "dignity_score": 0.85,
            "tribalism_score": 0.15,
            "dignity_tribalism_tension": 0.70,
            "truth_score": 0.78,
            "manipulation_score": 0.12
        })
        
        result = self.agent._parse_extraction_response(
            mock_response,
            self.sample_gasket_schema["target_keys"]
        )
        
        assert result["dignity_score"] == 0.85
        assert result["tribalism_score"] == 0.15
        assert result["dignity_tribalism_tension"] == 0.70
        assert result["truth_score"] == 0.78
        assert result["manipulation_score"] == 0.12
    
    def test_parse_extraction_response_with_markdown(self):
        """Test parsing response with markdown formatting."""
        mock_response = """```json
        {
            "dignity_score": 0.85,
            "tribalism_score": 0.15,
            "truth_score": null
        }
        ```"""
        
        result = self.agent._parse_extraction_response(
            mock_response,
            ["dignity_score", "tribalism_score", "truth_score"]
        )
        
        assert result["dignity_score"] == 0.85
        assert result["tribalism_score"] == 0.15
        assert result["truth_score"] is None
    
    def test_parse_extraction_response_invalid_scores(self):
        """Test parsing with invalid score values."""
        mock_response = json.dumps({
            "dignity_score": 1.5,  # Invalid: > 1.0
            "tribalism_score": -0.1,  # Invalid: < 0.0
            "truth_score": 0.78  # Valid
        })
        
        result = self.agent._parse_extraction_response(
            mock_response,
            ["dignity_score", "tribalism_score", "truth_score"]
        )
        
        # Invalid scores should be None
        assert result["dignity_score"] is None
        assert result["tribalism_score"] is None
        assert result["truth_score"] == 0.78
    
    def test_parse_extraction_response_malformed_json(self):
        """Test parsing with malformed JSON."""
        mock_response = "{ invalid json }"
        
        with pytest.raises(IntelligentExtractorError):
            self.agent._parse_extraction_response(
                mock_response,
                ["dignity_score"]
            )
    
    @patch('discernus.agents.intelligent_extractor_agent.agent.time.time')
    def test_extract_scores_success(self, mock_time):
        """Test successful score extraction."""
        # Mock time for consistent testing
        mock_time.side_effect = [0.0, 2.5]  # start_time, end_time
        
        # Mock LLM gateway response
        mock_response = json.dumps({
            "dignity_score": 0.85,
            "tribalism_score": 0.15,
            "truth_score": 0.78
        })
        
        mock_metadata = {
            "total_tokens": 150,
            "cost": 0.002
        }
        
        with patch.object(self.agent.llm_gateway, 'execute_call') as mock_execute:
            mock_execute.return_value = (mock_response, mock_metadata)
            
            result = self.agent.extract_scores_from_raw_analysis(
                self.sample_raw_analysis,
                self.sample_gasket_schema
            )
        
        assert result.success is True
        assert result.extracted_scores["dignity_score"] == 0.85
        assert result.extracted_scores["tribalism_score"] == 0.15
        assert result.extracted_scores["truth_score"] == 0.78
        assert result.extraction_time_seconds == 2.5
        assert result.tokens_used == 150
        assert result.cost_usd == 0.002
        assert result.attempts == 1
        assert result.error_message is None
    
    def test_extract_scores_empty_input(self):
        """Test extraction with empty input."""
        result = self.agent.extract_scores_from_raw_analysis(
            "",
            self.sample_gasket_schema
        )
        
        assert result.success is False
        assert result.error_message == "Empty or invalid raw analysis text"
        assert result.attempts == 0
    
    def test_extract_scores_invalid_schema(self):
        """Test extraction with invalid gasket schema."""
        invalid_schema = {"invalid": "schema"}
        
        result = self.agent.extract_scores_from_raw_analysis(
            self.sample_raw_analysis,
            invalid_schema
        )
        
        assert result.success is False
        assert "Invalid gasket_schema" in result.error_message
        assert result.attempts == 0
    
    @patch('discernus.agents.intelligent_extractor_agent.agent.time.sleep')
    def test_extract_scores_with_retries(self, mock_sleep):
        """Test extraction with retry logic."""
        # Mock LLM gateway to fail first attempt, succeed second
        with patch.object(self.agent.llm_gateway, 'execute_call') as mock_execute:
            # First call fails
            mock_execute.side_effect = [
                Exception("Network error"),
                (json.dumps({"dignity_score": 0.85}), {"total_tokens": 100, "cost": 0.001})
            ]
            
            result = self.agent.extract_scores_from_raw_analysis(
                self.sample_raw_analysis,
                self.sample_gasket_schema
            )
        
        assert result.success is True
        assert result.attempts == 2
        assert mock_sleep.called  # Verify retry delay was used
    
    def test_extract_scores_max_retries_exceeded(self):
        """Test extraction when max retries are exceeded."""
        with patch.object(self.agent.llm_gateway, 'execute_call') as mock_execute:
            # All attempts fail
            mock_execute.side_effect = Exception("Persistent error")
            
            result = self.agent.extract_scores_from_raw_analysis(
                self.sample_raw_analysis,
                self.sample_gasket_schema
            )
        
        assert result.success is False
        assert result.attempts == self.agent.max_retries
        assert "Persistent error" in result.error_message
    
    def test_get_extraction_stats(self):
        """Test extraction statistics method."""
        stats = self.agent.get_extraction_stats()
        
        assert stats["agent_name"] == "IntelligentExtractorAgent"
        assert stats["model"] == "vertex_ai/gemini-2.5-flash"
        assert stats["max_retries"] == 2
        assert stats["timeout_seconds"] == 10
        assert "semantic_extraction" in stats["capabilities"]
        assert "hierarchical_to_flat_mapping" in stats["capabilities"]
        assert "robust_parsing" in stats["capabilities"]


class TestExtractionResult:
    """Test suite for ExtractionResult dataclass."""
    
    def test_extraction_result_creation(self):
        """Test ExtractionResult creation."""
        result = ExtractionResult(
            success=True,
            extracted_scores={"test_score": 0.75},
            extraction_time_seconds=1.5,
            tokens_used=100,
            cost_usd=0.001,
            attempts=1
        )
        
        assert result.success is True
        assert result.extracted_scores == {"test_score": 0.75}
        assert result.extraction_time_seconds == 1.5
        assert result.tokens_used == 100
        assert result.cost_usd == 0.001
        assert result.attempts == 1
        assert result.error_message is None
        assert result.raw_llm_response is None
    
    def test_extraction_result_with_error(self):
        """Test ExtractionResult with error information."""
        result = ExtractionResult(
            success=False,
            extracted_scores={},
            extraction_time_seconds=0.5,
            tokens_used=0,
            cost_usd=0.0,
            attempts=3,
            error_message="Test error",
            raw_llm_response="Invalid response"
        )
        
        assert result.success is False
        assert result.error_message == "Test error"
        assert result.raw_llm_response == "Invalid response"
        assert result.attempts == 3


if __name__ == "__main__":
    pytest.main([__file__])