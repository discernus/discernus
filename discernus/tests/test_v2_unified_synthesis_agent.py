#!/usr/bin/env python3
"""
Test V2 UnifiedSynthesisAgent
============================

Tests for the V2-compliant UnifiedSynthesisAgent that implements the StandardAgent interface
and consumes V2-native artifacts through RunContext.
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from datetime import datetime

from discernus.agents.unified_synthesis_agent.v2_unified_synthesis_agent import V2UnifiedSynthesisAgent
from discernus.core.agent_result import AgentResult
from discernus.core.agent_config import AgentConfig
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.run_context import RunContext


class TestV2UnifiedSynthesisAgent:
    """Test V2UnifiedSynthesisAgent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_security = Mock()
        self.mock_storage = Mock()
        self.mock_audit = Mock()
        self.mock_config = AgentConfig()
        
        # Set up mock security boundary
        self.mock_security.experiment_path = Path("/test/experiment")
        
        # Mock storage responses
        self.mock_storage.store_artifact.return_value = "test_artifact_hash_123"
        
        # Mock LLM gateway
        self.mock_llm_gateway = Mock()
        self.mock_llm_gateway.execute_call.return_value = (
            "Test synthesis report content",
            {"usage": {"total_tokens": 1000, "response_cost_usd": 0.05}}
        )
    
    def test_v2_constructor(self):
        """Test V2 constructor with proper dependencies"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        assert agent.agent_name == "V2UnifiedSynthesisAgent"
        assert agent.security == self.mock_security
        assert agent.storage == self.mock_storage
        assert agent.audit == self.mock_audit
        assert agent.model == self.mock_config.model
    
    def test_v2_interface_methods(self):
        """Test V2 StandardAgent interface methods"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Test get_capabilities
        capabilities = agent.get_capabilities()
        expected_capabilities = [
            "synthesis",
            "report_generation",
            "summarization",
            "academic_report_generation",
            "evidence_integration",
            "statistical_synthesis",
            "multi_audience_synthesis",
            "tool_calling",
            "structured_output"
        ]
        for capability in expected_capabilities:
            assert capability in capabilities
        
        # Test get_required_inputs
        required_inputs = agent.get_required_inputs()
        expected_required = [
            "analysis_results",
            "statistical_results",
            "framework_path",
            "experiment_path"
        ]
        for input_param in expected_required:
            assert input_param in required_inputs
        
        # Test get_optional_inputs
        optional_inputs = agent.get_optional_inputs()
        expected_optional = [
            "evidence",
            "derived_metrics",
            "computational_work",
            "verification_results"
        ]
        for input_param in expected_optional:
            assert input_param in optional_inputs
    
    def test_execute_method_success(self):
        """Test execute method with successful synthesis"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the LLM gateway
        agent.llm_gateway = self.mock_llm_gateway
        
        # Create a valid RunContext
        run_context = RunContext(
            experiment_id="test_run_001",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus"
        )
        run_context.analysis_results = {"documents": [{"id": "doc1", "content": "test"}]}
        run_context.statistical_results = {"finding_1": "significant result"}
        run_context.evidence = [{"quote_text": "test quote", "document_name": "doc1"}]
        run_context.metadata = {"test": "data"}
        
        # Mock file reading and Path.exists
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value="test content"):
            mock_file.return_value.read.return_value = "test content"
    
            result = agent.execute(run_context)
        
        assert isinstance(result, AgentResult)
        assert result.success is True
        assert len(result.artifacts) == 1
        assert result.artifacts[0]["type"] == "synthesis_report"
        assert "test_artifact_hash_123" in result.artifacts[0]["hash"]
    
    def test_execute_method_validation_failure(self):
        """Test execute method with invalid RunContext"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Create an invalid RunContext (missing required fields)
        run_context = RunContext(
            experiment_id="test_run_001",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus"
        )
        # Missing analysis_results, statistical_results, and metadata
        
        result = agent.execute(run_context)
        
        assert isinstance(result, AgentResult)
        assert result.success is False
        assert "RunContext missing required synthesis inputs" in result.error_message
    
    def test_synthesize_method(self):
        """Test synthesize method from SynthesisAgent base class"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the LLM gateway
        agent.llm_gateway = self.mock_llm_gateway
        
        source_data = {
            "analysis_results": {"documents": [{"id": "doc1", "content": "test"}]},
            "statistical_results": {"finding_1": "significant result"},
            "evidence": [{"quote_text": "test quote", "document_name": "doc1"}],
            "metadata": {
                "framework_path": "/test/framework.yaml",
                "experiment_path": "/test/experiment.md"
            }
        }
        
        # Mock file reading and Path.exists
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value="test content"):
            mock_file.return_value.read.return_value = "test content"
            
            result = agent.synthesize(source_data, run_id="test_run_002")
        
        assert isinstance(result, AgentResult)
        assert result.success is True
    
    def test_legacy_config_factory(self):
        """Test backward compatibility factory method"""
        legacy_config = {
            "model": "vertex_ai/gemini-2.5-pro",
            "enhanced_mode": True,
            "security_boundary": self.mock_security,
            "artifact_storage": self.mock_storage,
            "audit_logger": self.mock_audit
        }
        
        agent = V2UnifiedSynthesisAgent.from_legacy_config(legacy_config)
        
        assert agent.agent_name == "V2UnifiedSynthesisAgent"
        assert agent.model == "vertex_ai/gemini-2.5-pro"
        assert agent.enhanced_mode is True
        assert isinstance(agent, V2UnifiedSynthesisAgent)
    
    def test_legacy_config_factory_missing_dependencies(self):
        """Test legacy config factory with missing dependencies"""
        legacy_config = {
            "model": "vertex_ai/gemini-2.5-pro",
            "enhanced_mode": True
            # Missing security_boundary, artifact_storage, audit_logger
        }
        
        with pytest.raises(ValueError, match="Legacy config must provide"):
            V2UnifiedSynthesisAgent.from_legacy_config(legacy_config)
    
    def test_prepare_research_data_context(self):
        """Test research data context preparation"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        inputs = {
            "analysis_results": {"documents": [{"id": "doc1", "content": "test"}]},
            "statistical_results": {"finding_1": "significant result"},
            "derived_metrics": {"metric_1": 0.85}
        }
        
        context = agent._prepare_research_data_context(inputs)
        
        assert "Complete Research Data:" in context
        assert "analysis_results" in context
        assert "statistical_results" in context
        assert "derived_metrics" in context
    
    def test_prepare_evidence_context_with_evidence(self):
        """Test evidence context preparation with evidence"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        evidence = [
            {
                "quote_text": "This is a test quote",
                "document_name": "test_doc.pdf",
                "confidence": 0.95
            },
            {
                "quote_text": "Another test quote",
                "document_name": "test_doc2.pdf",
                "confidence": 0.87
            }
        ]
        
        context = agent._prepare_evidence_context(evidence)
        
        assert "EVIDENCE AVAILABLE FOR SYNTHESIS" in context
        assert "Found 2 evidence pieces" in context
        assert "This is a test quote" in context
        assert "test_doc.pdf" in context
    
    def test_prepare_evidence_context_no_evidence(self):
        """Test evidence context preparation without evidence"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        evidence = []
        
        context = agent._prepare_evidence_context(evidence)
        
        assert "No evidence available for synthesis" in context
    
    def test_convert_tuple_keys_for_repr(self):
        """Test tuple key conversion for safe repr serialization"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Test data with tuple keys
        test_data = {
            ("key1", "key2"): "value1",
            "normal_key": "value2",
            "nested": {
                ("nested_key1", "nested_key2"): "nested_value",
                "normal_nested": "normal_value"
            }
        }
        
        converted = agent._convert_tuple_keys_for_repr(test_data)
        
        assert converted["('key1', 'key2')"] == "value1"
        assert converted["normal_key"] == "value2"
        assert converted["nested"]["('nested_key1', 'nested_key2')"] == "nested_value"
        assert converted["nested"]["normal_nested"] == "normal_value"
    
    def test_load_enhanced_prompt_template(self):
        """Test loading enhanced prompt template"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock the prompt file
        mock_prompt_content = {
            "template": "Test template with {placeholder}"
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('yaml.safe_load', return_value=mock_prompt_content):
                template = agent._load_enhanced_prompt_template()
        
        assert template == mock_prompt_content
    
    def test_load_enhanced_prompt_template_fallback(self):
        """Test fallback to basic template when enhanced template fails"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        # Mock file not found
        with patch('builtins.open', side_effect=FileNotFoundError):
            template = agent._load_enhanced_prompt_template()
        
        assert "template" in template
    
    def test_assemble_experiment_metadata(self):
        """Test experiment metadata assembly"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        inputs = {
            "experiment_name": "test_experiment",
            "run_id": "test_run_001",
            "framework_name": "test_framework.yaml",
            "analysis_results": {"documents": [{"id": "doc1"}]},
            "evidence": [{"quote_text": "test"}]
        }
        
        metadata = agent._assemble_experiment_metadata(inputs)
        
        assert "test_experiment" in metadata
        assert "test_run_001" in metadata
        assert "test_framework.yaml" in metadata
        assert "Document Count: 1" in metadata
        assert "Evidence Count: 1" in metadata
    
    def test_store_synthesis_results(self):
        """Test storing synthesis results as artifact"""
        agent = V2UnifiedSynthesisAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
        
        run_context = RunContext(
            experiment_id="test_run_001",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus"
        )
        
        synthesis_result = {
            "final_report": "Test synthesis report",
            "llm_metadata": {"usage": {"total_tokens": 1000}}
        }
        
        artifact_hash = agent._store_synthesis_results(synthesis_result, run_context)
        
        assert artifact_hash == "test_artifact_hash_123"
        self.mock_storage.store_artifact.assert_called_once()
        
        # Verify artifact content
        call_args = self.mock_storage.store_artifact.call_args
        artifact_content = call_args[1]["content"].decode('utf-8')
        artifact_data = json.loads(artifact_content)
        
        assert artifact_data["agent_name"] == "V2UnifiedSynthesisAgent"
        assert artifact_data["experiment_id"] == "test_run_001"
        assert "Test synthesis report" in artifact_data["synthesis_result"]["final_report"]


def mock_open():
    """Mock open function for file operations"""
    return MagicMock()


if __name__ == "__main__":
    pytest.main([__file__])
