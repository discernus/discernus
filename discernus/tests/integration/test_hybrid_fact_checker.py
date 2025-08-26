#!/usr/bin/env python3
"""
Integration Tests for Hybrid Fact-Checker System
===============================================

Tests the hybrid approach that combines:
- Synthesis RAG index for evidence quote validation
- Direct asset injection for framework/statistical validation
- Pattern detection for citation/grandiose claim validation

This test suite validates the complete hybrid fact-checking pipeline.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from txtai.embeddings import Embeddings

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


class TestHybridFactChecker:
    """Test suite for hybrid fact-checking system."""

    @pytest.fixture
    def mock_gateway(self):
        """Mock LLM gateway for testing."""
        gateway = Mock(spec=LLMGateway)
        gateway.execute_call.return_value = (
            '{"issues_found": false, "details": "Check passed - no issues detected"}',
            {"model": "test", "tokens": 100}
        )
        return gateway

    @pytest.fixture
    def mock_audit_logger(self):
        """Mock audit logger for testing."""
        return Mock(spec=AuditLogger)

    @pytest.fixture
    def sample_synthesis_rag_index(self):
        """Create a sample synthesis RAG index with evidence content."""
        # Create a mock txtai embeddings index
        rag_index = Mock(spec=Embeddings)
        
        # Mock search results for evidence queries
        rag_index.search.return_value = [
            (0, 0.95),  # High relevance match
            (1, 0.87),  # Medium relevance match
        ]
        
        # Mock document storage for content retrieval
        rag_index.documents = [
            {
                'id': 0,
                'text': 'Evidence from speech about democratic values and civic responsibility',
                'metadata': {'source_type': 'evidence', 'filename': 'test_speech.txt'}
            },
            {
                'id': 1,
                'text': 'Quote about constitutional principles and rule of law',
                'metadata': {'source_type': 'evidence', 'filename': 'test_speech2.txt'}
            }
        ]
        
        return rag_index

    @pytest.fixture
    def sample_framework_content(self):
        """Sample framework content for direct injection."""
        return """
        # Test Framework v1.0
        
        ## Dimensions
        
        **Identity Axis**:
        - **Tribalism** (0.0-1.0): Group loyalty over universal principles
        - **Dignity** (0.0-1.0): Respect for universal human worth
        
        **Truth Axis**:
        - **Manipulation** (0.0-1.0): Strategic distortion of information
        - **Truth** (0.0-1.0): Commitment to factual accuracy
        
        **Justice Axis**:
        - **Resentment** (0.0-1.0): Exploitation of grievances
        - **Justice** (0.0-1.0): Concern for fair outcomes
        """

    @pytest.fixture
    def sample_statistical_results(self):
        """Sample statistical results for direct injection."""
        return {
            "descriptive_statistics": {
                "dignity_raw": {"mean": 0.75, "std": 0.15},
                "tribalism_raw": {"mean": 0.25, "std": 0.12},
                "truth_raw": {"mean": 0.82, "std": 0.18}
            },
            "correlations": {
                "dignity_tribalism": -0.65,
                "truth_manipulation": -0.78
            },
            "derived_metrics": {
                "civic_character_index": 0.45
            }
        }

    @pytest.fixture
    def sample_report_content(self):
        """Sample synthesis report content for testing."""
        return """
        # Test Analysis Report
        
        ## Findings
        
        The analysis reveals significant patterns in Dignity (mean=0.75) and Truth (mean=0.82) dimensions.
        The correlation between dignity and tribalism is r=-0.65, indicating strong inverse relationship.
        
        ## Evidence
        
        "Democratic values and civic responsibility are fundamental to our society" demonstrates 
        high dignity scores across speakers.
        
        ## Claims
        
        This represents a major breakthrough in political analysis methodology.
        According to Smith et al. (2023), similar patterns have been observed.
        """

    def test_hybrid_fact_checker_initialization(self, mock_gateway, mock_audit_logger):
        """Test that hybrid fact-checker initializes correctly."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        assert fact_checker.gateway == mock_gateway
        assert fact_checker.audit_logger == mock_audit_logger
        assert fact_checker.rubric is not None
        assert len(fact_checker.rubric["checks"]) == 6  # All six validation checks

    def test_evidence_quote_validation_uses_rag(
        self, mock_gateway, mock_audit_logger, sample_synthesis_rag_index, sample_report_content
    ):
        """Test that evidence quote validation uses synthesis RAG index."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock the LLM response for evidence validation
        mock_gateway.execute_call.return_value = (
            '```json\n{"issues_found": false, "details": "All quotes found in RAG index"}\n```',
            {"model": "test", "tokens": 150}
        )
        
        # Run fact-checking with RAG index
        results = fact_checker.check(
            report_content=sample_report_content,
            evidence_index=sample_synthesis_rag_index
        )
        
        # Verify RAG index was queried
        assert sample_synthesis_rag_index.search.called
        
        # Verify results structure
        assert "findings" in results
        assert "validation_results" in results

    def test_dimension_hallucination_uses_direct_injection(
        self, mock_gateway, mock_audit_logger, sample_framework_content, sample_report_content
    ):
        """Test that dimension hallucination check uses direct framework injection."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock framework content injection
        with patch.object(fact_checker, '_inject_framework_content_directly') as mock_inject:
            mock_inject.return_value = sample_framework_content
            
            # Mock LLM response for dimension validation
            mock_gateway.execute_call.return_value = (
                '{"issues_found": false, "details": "All dimensions found in framework"}',
                {"model": "test", "tokens": 200}
            )
            
            # Run fact-checking
            results = fact_checker.check(
                report_content=sample_report_content,
                evidence_index=None  # No RAG index needed for this check
            )
            
            # Verify framework injection was called
            mock_inject.assert_called()

    def test_statistic_mismatch_uses_direct_injection(
        self, mock_gateway, mock_audit_logger, sample_statistical_results, sample_report_content
    ):
        """Test that statistic mismatch check uses direct statistical results injection."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock statistical results injection
        with patch.object(fact_checker, '_inject_statistical_results_directly') as mock_inject:
            mock_inject.return_value = json.dumps(sample_statistical_results, indent=2)
            
            # Mock LLM response for statistical validation
            mock_gateway.execute_call.return_value = (
                '{"issues_found": false, "details": "All statistics match within acceptable precision"}',
                {"model": "test", "tokens": 180}
            )
            
            # Run fact-checking
            results = fact_checker.check(
                report_content=sample_report_content,
                evidence_index=None  # No RAG index needed for this check
            )
            
            # Verify statistical injection was called
            mock_inject.assert_called()

    def test_pattern_detection_checks_no_external_data(
        self, mock_gateway, mock_audit_logger, sample_report_content
    ):
        """Test that pattern detection checks (grandiose claims, citations) need no external data."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock LLM responses for pattern detection - need to match actual rubric order
        # The rubric has: Dimension Hallucination, Statistic Mismatch, Evidence Quote Mismatch, 
        # Grandiose Claim, Citation Violation, Fabricated Reference
        mock_gateway.execute_call.side_effect = [
            # Dimension Hallucination
            ('```json\n{"issues_found": false, "details": "No issues detected"}\n```', {"tokens": 80}),
            # Statistic Mismatch  
            ('```json\n{"issues_found": false, "details": "No issues detected"}\n```', {"tokens": 80}),
            # Evidence Quote Mismatch
            ('```json\n{"issues_found": false, "details": "No issues detected"}\n```', {"tokens": 80}),
            # Grandiose Claim
            ('```json\n{"issues_found": true, "details": "Found grandiose claim: major breakthrough"}\n```', {"tokens": 100}),
            # Citation Violation
            ('```json\n{"issues_found": true, "details": "Found external citation: Smith et al. (2023)"}\n```', {"tokens": 120}),
            # Fabricated Reference
            ('```json\n{"issues_found": false, "details": "No issues detected"}\n```', {"tokens": 80}),
        ]
        
        # Run fact-checking
        results = fact_checker.check(
            report_content=sample_report_content,
            evidence_index=None
        )
        
        # Verify pattern detection found issues
        assert "findings" in results
        findings = results["findings"]
        
        # Should find grandiose claims and citation violations
        grandiose_findings = [f for f in findings if f.get("check_name") == "Grandiose Claim"]
        citation_findings = [f for f in findings if f.get("check_name") == "Citation Violation"]
        
        assert len(grandiose_findings) > 0
        assert len(citation_findings) > 0

    def test_hybrid_logging_transparency(
        self, mock_gateway, mock_audit_logger, sample_synthesis_rag_index, sample_report_content
    ):
        """Test that hybrid approach logs data sources and decision process."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Run fact-checking
        results = fact_checker.check(
            report_content=sample_report_content,
            evidence_index=sample_synthesis_rag_index
        )
        
        # Verify audit logging was called for fact-checking events
        assert mock_audit_logger.log_agent_event.called
        
        # Check that start event was logged
        start_calls = [
            call for call in mock_audit_logger.log_agent_event.call_args_list
            if call[1]["event_type"] == "fact_check_start"
        ]
        assert len(start_calls) > 0

    def test_error_handling_graceful_degradation(
        self, mock_gateway, mock_audit_logger, sample_report_content
    ):
        """Test that hybrid fact-checker handles errors gracefully."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock LLM gateway to raise exception
        mock_gateway.execute_call.side_effect = Exception("LLM service unavailable")
        
        # Run fact-checking - should not crash
        results = fact_checker.check(
            report_content=sample_report_content,
            evidence_index=None
        )
        
        # Should return error status rather than crashing
        assert "error" in results or "status" in results

    def test_comprehensive_validation_coverage(
        self, mock_gateway, mock_audit_logger, sample_synthesis_rag_index, sample_report_content
    ):
        """Test that all six validation checks are executed in hybrid mode."""
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Mock successful responses for all checks
        mock_gateway.execute_call.return_value = (
            '```json\n{"issues_found": false, "details": "Check passed"}\n```',
            {"model": "test", "tokens": 100}
        )
        
        # Run comprehensive fact-checking
        results = fact_checker.check(
            report_content=sample_report_content,
            evidence_index=sample_synthesis_rag_index
        )
        
        # Verify all six checks were executed
        # (6 checks in rubric should result in 6 LLM calls)
        assert mock_gateway.execute_call.call_count == 6
        
        # Verify results structure
        assert "findings" in results
        assert "validation_results" in results


class TestHybridDataSourceRouting:
    """Test suite for hybrid data source routing logic."""

    def test_evidence_context_routing_logic(self):
        """Test that _get_evidence_context routes to correct data sources."""
        # This will be implemented as part of Phase 3
        # Placeholder for routing logic tests
        pass

    def test_rag_query_construction(self):
        """Test RAG query construction for evidence validation."""
        # This will be implemented as part of Phase 3
        # Placeholder for RAG query tests
        pass

    def test_direct_injection_formatting(self):
        """Test direct asset injection formatting."""
        # This will be implemented as part of Phase 3
        # Placeholder for injection formatting tests
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
