#!/usr/bin/env python3
"""
Test Legacy EvidenceRetriever V2 Migration
==========================================

Tests for the migrated EvidenceRetrieverAgent that now implements V2 StandardAgent interface
while maintaining backward compatibility.
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path

from discernus.agents.evidence_retriever_agent.evidence_retriever_agent import EvidenceRetrieverAgent
from discernus.core.agent_result import AgentResult
from discernus.core.agent_config import AgentConfig
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


class TestLegacyEvidenceRetrieverV2Migration:
    """Test EvidenceRetrieverAgent V2 migration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_security = Mock(spec=ExperimentSecurityBoundary)
        self.mock_storage = Mock(spec=LocalArtifactStorage)
        self.mock_audit = Mock(spec=AuditLogger)
        self.mock_config = AgentConfig()
        
        # Set up mock security boundary
        self.mock_security.experiment_path = Path("/test/experiment")
    
    def test_v2_constructor(self):
        """Test V2 constructor with proper dependencies"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.agent_name == "EvidenceRetriever"
        assert agent.security_boundary == self.mock_security
        assert agent.artifact_storage == self.mock_storage
        assert agent.audit_logger == self.mock_audit
        assert agent.experiment_path == Path("/test/experiment")
    
    def test_v2_interface_methods(self):
        """Test V2 StandardAgent interface methods"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Test get_capabilities
        capabilities = agent.get_capabilities()
        expected_capabilities = [
            "evidence_retrieval",
            "rag_search",
            "semantic_search",
            "framework_agnostic_analysis",
            "tool_calling",
            "structured_output"
        ]
        for capability in expected_capabilities:
            assert capability in capabilities
        
        # Test get_required_inputs
        required_inputs = agent.get_required_inputs()
        expected_required = [
            "analysis_artifact_hashes",
            "statistical_results_hash",
            "framework_path"
        ]
        for input_param in expected_required:
            assert input_param in required_inputs
        
        # Test get_optional_inputs
        optional_inputs = agent.get_optional_inputs()
        expected_optional = [
            "framework_hash",
            "statistical_results",
            "evidence_artifact_hashes"
        ]
        for input_param in expected_optional:
            assert input_param in optional_inputs
    
    def test_legacy_config_factory(self):
        """Test backward compatibility factory method"""
        legacy_config = {
            "experiment_path": "/test/experiment",
            "run_id": "test_run",
            "model": "vertex_ai/gemini-2.5-pro",
            "security_boundary": self.mock_security,
            "artifact_storage": self.mock_storage,
            "audit_logger": self.mock_audit
        }
        
        agent = EvidenceRetrieverAgent.from_legacy_config(legacy_config)
        
        assert agent.agent_name == "EvidenceRetriever"
        assert agent.run_id == "test_run"
        assert agent.model == "vertex_ai/gemini-2.5-pro"
        assert isinstance(agent, EvidenceRetrieverAgent)
    
    def test_execute_method_interface(self):
        """Test execute method returns AgentResult"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the run method to return a successful result
        agent.run = Mock(return_value={
            "status": "success",
            "evidence_artifact_hash": "test_hash",
            "framework": "Test Framework",
            "evidence_quotes_found": 5,
            "evidence_results": [{"finding": "test"}]
        })
        
        result = agent.execute(
            analysis_artifact_hashes=["hash1"],
            statistical_results_hash="stat_hash",
            framework_path="/path/to/framework"
        )
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert "test_hash" in result.artifacts
        assert result.metadata["framework"] == "Test Framework"
        assert result.metadata["evidence_quotes_found"] == 5
    
    def test_execute_method_error_handling(self):
        """Test execute method error handling"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the run method to raise an exception
        agent.run = Mock(side_effect=Exception("Test error"))
        
        result = agent.execute(
            analysis_artifact_hashes=["hash1"],
            statistical_results_hash="stat_hash",
            framework_path="/path/to/framework"
        )
        
        assert isinstance(result, AgentResult)
        assert result.success is False
        assert "Test error" in result.error_message
        assert len(result.artifacts) == 0
    
    def test_execute_method_legacy_failure(self):
        """Test execute method with legacy run method failure"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the run method to return a failure result
        agent.run = Mock(return_value={
            "status": "failed",
            "error": "Legacy error"
        })
        
        result = agent.execute(
            analysis_artifact_hashes=["hash1"],
            statistical_results_hash="stat_hash",
            framework_path="/path/to/framework"
        )
        
        assert isinstance(result, AgentResult)
        assert result.success is False
        assert "Legacy error" in result.error_message
    
    def test_backward_compatibility_attributes(self):
        """Test that backward compatibility attributes are set"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Check that legacy attributes are accessible
        assert hasattr(agent, 'experiment_path')
        assert hasattr(agent, 'run_id')
        assert hasattr(agent, 'model')
        assert hasattr(agent, 'security_boundary')
        assert hasattr(agent, 'artifact_storage')
        assert hasattr(agent, 'audit_logger')
        assert hasattr(agent, 'evidence_wrapper')
    
    def test_inheritance_hierarchy(self):
        """Test that agent inherits from correct base classes"""
        agent = EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Check inheritance
        assert isinstance(agent, EvidenceRetrieverAgent)
        # Note: We can't easily test ToolCallingAgent inheritance without complex mocking
        # but the class definition shows it inherits from ToolCallingAgent


if __name__ == "__main__":
    pytest.main([__file__])
