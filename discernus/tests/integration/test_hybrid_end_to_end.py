#!/usr/bin/env python3
"""
End-to-End Integration Test for Hybrid RAG-FactChecker System
============================================================

Tests the complete pipeline from FactCheckerAgent through RevisionAgent
to ensure the hybrid approach works end-to-end.
"""

import pytest
import json
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
from discernus.agents.revision_agent.agent import RevisionAgent
from discernus.core.audit_logger import AuditLogger


class TestHybridEndToEnd:
    """End-to-end test suite for hybrid RAG-FactChecker system."""

    @pytest.fixture
    def mock_audit_logger(self):
        """Mock audit logger for testing."""
        return Mock(spec=AuditLogger)

    @pytest.fixture
    def sample_problematic_report(self):
        """Sample report with multiple types of issues."""
        return """
# Political Analysis Report

## Executive Summary

This represents a revolutionary breakthrough in political analysis methodology.
Our unprecedented approach has uncovered absolutely conclusive evidence.

## Statistical Findings

The analysis reveals patterns in Dignity (mean=0.99) and Truth (mean=1.05) dimensions.
The correlation between dignity and tribalism is r=-0.999, indicating perfect relationship.

## Evidence Analysis

"We must unite as Americans" demonstrates exceptional civic character.
According to Smith et al. (2023), similar patterns have been observed.

## Conclusions

This groundbreaking research proves beyond doubt that our framework is superior.
The results are absolutely definitive and represent the ultimate analysis.
"""

    @pytest.fixture
    def mock_synthesis_rag_index(self):
        """Mock synthesis RAG index for evidence validation."""
        rag_index = Mock()
        rag_index.search.return_value = [
            (0, 0.95),  # High relevance match
        ]
        rag_index.documents = [
            {
                'id': 0,
                'text': 'We must unite as Americans in this challenging time',
                'metadata': {'source_type': 'evidence', 'filename': 'test_speech.txt'}
            }
        ]
        return rag_index

    def test_complete_hybrid_pipeline(
        self, mock_audit_logger, sample_problematic_report, mock_synthesis_rag_index
    ):
        """Test complete pipeline: fact-check → revision → final report."""
        
        # Mock LLM responses for fact-checker
        fact_checker_responses = [
            # Dimension Hallucination - pass
            ('```json\n{"issues_found": false, "details": "No dimension issues"}\n```', {"tokens": 80}),
            # Statistic Mismatch - fail
            ('```json\n{"issues_found": true, "details": "Statistical values exceed bounds", "examples": ["mean=0.99 should be 0.75", "mean=1.05 impossible (max 1.0)", "r=-0.999 should be r=-0.65"]}\n```', {"tokens": 120}),
            # Evidence Quote Mismatch - pass
            ('```json\n{"issues_found": false, "details": "Quote found in evidence"}\n```', {"tokens": 90}),
            # Grandiose Claim - fail
            ('```json\n{"issues_found": true, "details": "Multiple grandiose claims found", "examples": ["revolutionary breakthrough", "unprecedented approach", "absolutely conclusive", "proves beyond doubt"]}\n```', {"tokens": 110}),
            # Citation Violation - fail
            ('```json\n{"issues_found": true, "details": "External citation found", "examples": ["Smith et al. (2023)"]}\n```', {"tokens": 85}),
            # Fabricated Reference - pass
            ('```json\n{"issues_found": false, "details": "No fabricated references"}\n```', {"tokens": 75}),
        ]
        
        # Mock corrected report from revision agent
        corrected_report = """
# Political Analysis Report

## Executive Summary

This analysis presents findings from our systematic approach to political analysis.
The methodology provides insights into political communication patterns.

## Statistical Findings

The analysis reveals patterns in Dignity (mean=0.75) and Truth (mean=0.82) dimensions.
The correlation between dignity and tribalism is r=-0.65, indicating strong relationship.

## Evidence Analysis

"We must unite as Americans" demonstrates notable civic character patterns.
The evidence suggests consistent themes in political discourse.

## Conclusions

This research provides evidence that our framework offers valuable insights.
The results indicate meaningful patterns in political communication analysis.
"""
        
        # Setup mocks directly
        mock_fc_gateway = Mock()
        mock_fc_gateway.execute_call.side_effect = fact_checker_responses
        
        with patch('discernus.agents.revision_agent.agent.LLMGateway') as mock_rev_gateway_class:
            # Setup revision agent mock
            mock_rev_gateway = Mock()
            mock_rev_gateway.execute_call.return_value = (corrected_report, {"tokens": 400})
            mock_rev_gateway_class.return_value = mock_rev_gateway
            
            # Step 1: Run fact-checker
            fact_checker = FactCheckerAgent(
                gateway=mock_fc_gateway,
                audit_logger=mock_audit_logger
            )
            
            fact_check_results = fact_checker.check(
                report_content=sample_problematic_report,
                evidence_index=mock_synthesis_rag_index
            )
            
            # Verify fact-checker found issues
            assert "findings" in fact_check_results
            findings = fact_check_results["findings"]
            assert len(findings) == 3  # Should find 3 issues (Statistic, Grandiose, Citation)
            
            # Verify specific findings
            finding_names = [f["check_name"] for f in findings]
            assert "Statistic Mismatch" in finding_names
            assert "Grandiose Claim" in finding_names
            assert "Citation Violation" in finding_names
            
            # Step 2: Run revision agent
            revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
            
            revision_results = revision_agent.revise_report_hybrid(
                draft_report=sample_problematic_report,
                fact_check_results=fact_check_results
            )
            
            # Verify revision results
            assert "revised_report" in revision_results
            assert "corrections_made" in revision_results
            assert "revision_summary" in revision_results
            
            # Verify corrections were applied
            assert len(revision_results["corrections_made"]) == 3
            assert "Applied 3 corrections" in revision_results["revision_summary"]
            assert revision_results["revised_report"] == corrected_report
            
            # Verify RAG index was used for evidence validation
            assert mock_synthesis_rag_index.search.called
            
            # Verify logging occurred
            assert mock_audit_logger.log_agent_event.called

    def test_hybrid_data_source_routing(
        self, mock_audit_logger, mock_synthesis_rag_index
    ):
        """Test that hybrid system routes to correct data sources."""
        
        test_report = 'Test report with quote: "We must unite as Americans" and statistics mean=0.75'
        
        # Mock LLM responses - all pass
        responses = [('```json\n{"issues_found": false, "details": "No issues"}\n```', {"tokens": 80})] * 6
        
        mock_gateway = Mock()
        mock_gateway.execute_call.side_effect = responses
        
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        results = fact_checker.check(
            report_content=test_report,
            evidence_index=mock_synthesis_rag_index
        )
        
        # Verify RAG index was used for evidence validation
        assert mock_synthesis_rag_index.search.called
        
        # Verify all checks were executed
        assert results["validation_results"]["total_checks"] == 6

    def test_error_handling_in_pipeline(self, mock_audit_logger):
        """Test error handling throughout the hybrid pipeline."""
        
        # Test fact-checker with LLM failure
        mock_gateway = Mock()
        mock_gateway.execute_call.side_effect = Exception("LLM service down")
        
        fact_checker = FactCheckerAgent(
            gateway=mock_gateway,
            audit_logger=mock_audit_logger
        )
        
        # Should handle gracefully and return error findings
        results = fact_checker.check(
            report_content="Test report",
            evidence_index=None
        )
        
        # Should have error findings for each failed check
        assert "findings" in results
        assert len(results["findings"]) == 6  # All 6 checks should have errors

    def test_no_issues_pipeline(self, mock_audit_logger, mock_synthesis_rag_index):
        """Test pipeline when no issues are found."""
        
        clean_report = """
# Clean Analysis Report

## Findings
The analysis reveals patterns in Dignity (mean=0.75) and Truth (mean=0.82) dimensions.

## Evidence
"We must unite as Americans" demonstrates civic character patterns.

## Conclusions
This research provides evidence of meaningful patterns in the data.
"""
        
        # Mock all checks pass
        responses = [('```json\n{"issues_found": false, "details": "No issues"}\n```', {"tokens": 80})] * 6
        
        mock_fc_gateway = Mock()
        mock_fc_gateway.execute_call.side_effect = responses
        
        fact_checker = FactCheckerAgent(
            gateway=mock_fc_gateway,
            audit_logger=mock_audit_logger
        )
        
        fact_check_results = fact_checker.check(
            report_content=clean_report,
            evidence_index=mock_synthesis_rag_index
        )
        
        # Should find no issues
        assert len(fact_check_results["findings"]) == 0
        
        # Revision agent should return original report unchanged
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        revision_results = revision_agent.revise_report_hybrid(
            draft_report=clean_report,
            fact_check_results=fact_check_results
        )
        
        assert revision_results["revised_report"] == clean_report
        assert len(revision_results["corrections_made"]) == 0
        assert "No revisions needed" in revision_results["revision_summary"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
