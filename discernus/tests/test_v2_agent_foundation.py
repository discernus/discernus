#!/usr/bin/env python3
"""
Test V2 Agent Foundation
========================

Tests for the V2 agent foundation classes and interfaces.
"""

import pytest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock

from discernus.core.standard_agent import StandardAgent
from discernus.core.agent_base_classes import ToolCallingAgent, ValidationAgent, SynthesisAgent, VerificationAgent
from discernus.core.agent_result import AgentResult, VerificationResult
from discernus.core.run_context import RunContext
from discernus.core.agent_config import AgentConfig, RetryConfig, VerificationConfig


class TestAgentResult:
    """Test AgentResult class"""
    
    def test_agent_result_creation(self):
        """Test basic AgentResult creation"""
        result = AgentResult(
            success=True,
            artifacts=["artifact1", "artifact2"],
            metadata={"key": "value"}
        )
        
        assert result.success is True
        assert len(result.artifacts) == 2
        assert result.metadata["key"] == "value"
        assert result.timestamp is not None
    
    def test_verification_result_creation(self):
        """Test VerificationResult creation"""
        result = VerificationResult(
            verified=True,
            discrepancies=[],
            attestation_data={"confidence": 0.95},
            primary_artifact_id="primary123",
            verification_artifact_id="verify456"
        )
        
        assert result.verified is True
        assert result.success is True  # Should be set automatically
        assert len(result.discrepancies) == 0


class TestRunContext:
    """Test RunContext class"""
    
    def test_run_context_creation(self):
        """Test basic RunContext creation"""
        context = RunContext(
            experiment_id="test_exp",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        
        assert context.experiment_id == "test_exp"
        assert context.framework_path == "/path/to/framework"
        assert context.corpus_path == "/path/to/corpus"
        assert context.start_time is not None
        assert context.last_updated is not None
    
    def test_phase_management(self):
        """Test phase management methods"""
        context = RunContext(
            experiment_id="test_exp",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        
        context.update_phase("analysis")
        assert context.current_phase == "analysis"
        assert "analysis" not in context.completed_phases
        
        context.update_phase("statistical")
        assert context.current_phase == "statistical"
        assert "analysis" in context.completed_phases
    
    def test_artifact_management(self):
        """Test artifact management methods"""
        context = RunContext(
            experiment_id="test_exp",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        
        context.add_artifact("analysis", "artifact123", "hash456")
        assert "artifact123" in context.analysis_artifacts
        assert context.artifact_hashes["artifact123"] == "hash456"
    
    def test_serialization(self):
        """Test RunContext serialization"""
        context = RunContext(
            experiment_id="test_exp",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        
        context_dict = context.to_dict()
        assert context_dict["experiment_id"] == "test_exp"
        
        # Test round-trip serialization
        new_context = RunContext.from_dict(context_dict)
        assert new_context.experiment_id == context.experiment_id


class TestAgentConfig:
    """Test AgentConfig system"""
    
    def test_agent_config_creation(self):
        """Test basic AgentConfig creation"""
        config = AgentConfig(
            model="vertex_ai/gemini-2.5-pro",
            timeout_seconds=600.0
        )
        
        assert config.model == "vertex_ai/gemini-2.5-pro"
        assert config.timeout_seconds == 600.0
        assert config.retry_config is not None
        assert config.verification_config is not None
    
    def test_retry_config(self):
        """Test RetryConfig creation"""
        retry_config = RetryConfig(
            max_retries=5,
            backoff_factor=2.5
        )
        
        assert retry_config.max_retries == 5
        assert retry_config.backoff_factor == 2.5
        assert len(retry_config.retryable_errors) > 0
    
    def test_verification_config(self):
        """Test VerificationConfig creation"""
        verif_config = VerificationConfig(
            enable_verification=True,
            verification_model="vertex_ai/gemini-2.5-flash"
        )
        
        assert verif_config.enable_verification is True
        assert verif_config.verification_model == "vertex_ai/gemini-2.5-flash"
        assert verif_config.verification_retry_config is not None
    
    def test_config_serialization(self):
        """Test config serialization"""
        config = AgentConfig(
            model="test_model",
            parameters={"param1": "value1"}
        )
        
        config_dict = config.to_dict()
        assert config_dict["model"] == "test_model"
        assert config_dict["parameters"]["param1"] == "value1"
        
        # Test round-trip serialization
        new_config = AgentConfig.from_dict(config_dict)
        assert new_config.model == config.model


class TestAgentBaseClasses:
    """Test agent base classes"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_security = Mock()
        self.mock_storage = Mock()
        self.mock_audit = Mock()
        self.mock_config = AgentConfig()
    
    def test_tool_calling_agent(self):
        """Test ToolCallingAgent base class"""
        class ConcreteToolCallingAgent(ToolCallingAgent):
            def execute(self, **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
        
        agent = ConcreteToolCallingAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.tool_calls == []
        assert agent.execution_results == []
        assert "tool_calling" in agent.get_capabilities()
    
    def test_validation_agent(self):
        """Test ValidationAgent base class"""
        class ConcreteValidationAgent(ValidationAgent):
            def execute(self, **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
            
            def validate(self, target_data: Dict[str, Any], **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
        
        agent = ConcreteValidationAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.validation_rules == []
        assert agent.validation_results == []
        assert "validation" in agent.get_capabilities()
    
    def test_synthesis_agent(self):
        """Test SynthesisAgent base class"""
        class ConcreteSynthesisAgent(SynthesisAgent):
            def execute(self, **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
            
            def synthesize(self, source_data: Dict[str, Any], **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
        
        agent = ConcreteSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.synthesis_sources == []
        assert agent.synthesis_metadata == {}
        assert "synthesis" in agent.get_capabilities()
    
    def test_verification_agent(self):
        """Test VerificationAgent base class"""
        class ConcreteVerificationAgent(VerificationAgent):
            def execute(self, **kwargs) -> AgentResult:
                return AgentResult(success=True, artifacts=[], metadata={})
            
            def verify(self, primary_results: Dict[str, Any], computational_work: Dict[str, Any]) -> VerificationResult:
                return VerificationResult(
                    verified=True,
                    discrepancies=[],
                    attestation_data={},
                    primary_artifact_id="test",
                    verification_artifact_id="test"
                )
        
        agent = ConcreteVerificationAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.verification_targets == []
        assert agent.attestation_data == {}
        assert "verification" in agent.get_capabilities()


if __name__ == "__main__":
    pytest.main([__file__])
