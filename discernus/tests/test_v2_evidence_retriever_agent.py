#!/usr/bin/env python3
"""
Test V2 EvidenceRetriever Agent (DEPRECATED)
============================================

Tests for the V2 EvidenceRetrieverAgent implementation.
NOTE: This agent has been deprecated. Use IntelligentEvidenceRetrievalAgent instead.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from discernus.agents.deprecated.evidence_retriever_agent.v2_evidence_retriever_agent import V2EvidenceRetrieverAgent
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.agent_config import AgentConfig
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


class TestV2EvidenceRetrieverAgent:
    """Test V2EvidenceRetrieverAgent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_security = Mock(spec=ExperimentSecurityBoundary)
        self.mock_storage = Mock(spec=LocalArtifactStorage)
        self.mock_audit = Mock(spec=AuditLogger)
        self.mock_config = AgentConfig()
        
        # Create agent instance
        self.agent = V2EvidenceRetrieverAgent(
            self.mock_security,
            self.mock_storage,
            self.mock_audit,
            self.mock_config
        )
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.agent_name == "V2EvidenceRetriever"
        assert self.agent.evidence_wrapper is None
        assert self.agent.rag_index is None
        assert "evidence_retrieval" in self.agent.get_capabilities()
    
    def test_get_capabilities(self):
        """Test agent capabilities"""
        capabilities = self.agent.get_capabilities()
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
    
    def test_get_required_inputs(self):
        """Test required inputs"""
        required_inputs = self.agent.get_required_inputs()
        assert "run_context" in required_inputs
        assert len(required_inputs) == 1
    
    def test_get_optional_inputs(self):
        """Test optional inputs"""
        optional_inputs = self.agent.get_optional_inputs()
        assert len(optional_inputs) == 0
    
    def test_execute_missing_run_context(self):
        """Test execute with missing run_context"""
        result = self.agent.execute()
        
        assert result.success is False
        assert "run_context is required" in result.error_message
    
    def test_execute_invalid_run_context(self):
        """Test execute with invalid run_context"""
        result = self.agent.execute(run_context="invalid")
        
        assert result.success is False
        assert "run_context must be a RunContext instance" in result.error_message
    
    def test_execute_missing_framework_path(self):
        """Test execute with missing framework_path"""
        run_context = RunContext(
            experiment_id="test",
            framework_path="",
            corpus_path="/path/to/corpus"
        )
        
        result = self.agent.execute(run_context=run_context)
        
        assert result.success is False
        assert "framework_path not found in RunContext" in result.error_message
    
    def test_execute_missing_statistical_results(self):
        """Test execute with missing statistical_results"""
        run_context = RunContext(
            experiment_id="test",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        
        result = self.agent.execute(run_context=run_context)
        
        assert result.success is False
        assert "statistical_results not found in RunContext" in result.error_message
    
    def test_execute_missing_analysis_artifacts(self):
        """Test execute with missing analysis_artifacts"""
        run_context = RunContext(
            experiment_id="test",
            framework_path="/path/to/framework",
            corpus_path="/path/to/corpus"
        )
        run_context.statistical_results = {"test": "data"}
        
        result = self.agent.execute(run_context=run_context)
        
        assert result.success is False
        assert "analysis_artifacts not found in RunContext" in result.error_message
    
    def test_load_framework_from_path_yaml(self):
        """Test loading framework from YAML file"""
        # Create a temporary YAML file
        import tempfile
        import yaml
        
        framework_data = {
            "name": "Test Framework",
            "version": "1.0.0",
            "description": "A test framework for evidence retrieval"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(framework_data, f)
            temp_path = f.name
        
        try:
            framework_spec = self.agent._load_framework_from_path(temp_path)
            assert framework_spec["name"] == "Test Framework"
            assert framework_spec["version"] == "1.0.0"
        finally:
            import os
            os.unlink(temp_path)
    
    def test_load_framework_from_path_json(self):
        """Test loading framework from JSON file"""
        # Create a temporary JSON file
        import tempfile
        
        framework_data = {
            "name": "Test Framework",
            "version": "1.0.0",
            "description": "A test framework for evidence retrieval"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(framework_data, f)
            temp_path = f.name
        
        try:
            framework_spec = self.agent._load_framework_from_path(temp_path)
            assert framework_spec["name"] == "Test Framework"
            assert framework_spec["version"] == "1.0.0"
        finally:
            import os
            os.unlink(temp_path)
    
    def test_find_evidence_artifacts_from_analysis(self):
        """Test finding evidence artifacts from analysis artifacts"""
        # Mock storage responses
        self.mock_storage.get_artifact.side_effect = [
            json.dumps({
                "evidence_artifacts": ["hash1", "hash2"],
                "other_data": "test"
            }).encode('utf-8'),
            json.dumps({
                "evidence_artifact_hashes": ["hash3", "hash4"],
                "other_data": "test"
            }).encode('utf-8'),
            json.dumps({
                "evidence_data": [{"quote": "test"}],
                "other_data": "test"
            }).encode('utf-8')
        ]
        
        analysis_artifacts = ["artifact1", "artifact2", "artifact3"]
        evidence_hashes = self.agent._find_evidence_artifacts_from_analysis(analysis_artifacts)
        
        # Should find all evidence artifacts
        expected_hashes = ["hash1", "hash2", "hash3", "hash4", "artifact3"]
        assert len(evidence_hashes) == len(expected_hashes)
        for hash_val in expected_hashes:
            assert hash_val in evidence_hashes
    
    def test_extract_key_findings(self):
        """Test extracting key findings from statistical results"""
        statistical_results = {
            "findings": [
                {"dimension": "test1", "significance": 0.05},
                {"dimension": "test2", "significance": 0.01}
            ],
            "key_findings": [
                {"dimension": "test3", "significance": 0.001}
            ],
            "results": {
                "dimension1": {"significance": 0.02, "description": "Test result 1"},
                "dimension2": {"significance": 0.03, "description": "Test result 2"}
            }
        }
        
        findings = self.agent._extract_key_findings(statistical_results)
        
        # Should extract all findings
        assert len(findings) == 5  # 2 from findings + 1 from key_findings + 2 from results
        assert any(f["dimension"] == "test1" for f in findings)
        assert any(f["dimension"] == "test2" for f in findings)
        assert any(f["dimension"] == "test3" for f in findings)
        assert any(f["dimension"] == "dimension1" for f in findings)
        assert any(f["dimension"] == "dimension2" for f in findings)
    
    def test_deduplicate_and_rank_evidence(self):
        """Test deduplicating and ranking evidence"""
        evidence = [
            {"quote_text": "Quote 1", "relevance_score": 0.8},
            {"quote_text": "Quote 2", "relevance_score": 0.9},
            {"quote_text": "Quote 1", "relevance_score": 0.7},  # Duplicate
            {"quote_text": "Quote 3", "relevance_score": 0.6},
            {"quote_text": "Quote 4", "relevance_score": 0.95},
            {"quote_text": "Quote 5", "relevance_score": 0.5}
        ]
        
        result = self.agent._deduplicate_and_rank_evidence(evidence)
        
        # Should remove duplicates and sort by relevance
        assert len(result) == 5  # 5 unique quotes
        assert result[0]["relevance_score"] == 0.95  # Highest score first
        assert result[1]["relevance_score"] == 0.9
        assert result[2]["relevance_score"] == 0.8
        assert result[3]["relevance_score"] == 0.6
        assert result[4]["relevance_score"] == 0.5
    
    def test_calculate_framework_hash(self):
        """Test calculating framework hash"""
        import tempfile
        
        # Create a temporary file with known content
        test_content = "test framework content for hashing"
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(test_content)
            temp_path = f.name
        
        try:
            hash_val = self.agent._calculate_framework_hash(temp_path)
            
            # Should return a valid hash
            assert isinstance(hash_val, str)
            assert len(hash_val) == 64  # SHA256 hash length
            
            # Verify it's consistent
            hash_val2 = self.agent._calculate_framework_hash(temp_path)
            assert hash_val == hash_val2
        finally:
            import os
            os.unlink(temp_path)




if __name__ == "__main__":
    pytest.main([__file__])
