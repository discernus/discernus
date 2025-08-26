#!/usr/bin/env python3
"""
Integration Tests for RevisionAgent with Hybrid FactChecker
==========================================================

Tests the integration between the hybrid FactCheckerAgent and RevisionAgent
to ensure systematic error correction works end-to-end.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from discernus.agents.revision_agent.agent import RevisionAgent
from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway import LLMGateway


class TestRevisionAgentIntegration:
    """Test suite for RevisionAgent integration with hybrid fact-checker."""

    @pytest.fixture
    def mock_gateway(self):
        """Mock LLM gateway for testing."""
        gateway = Mock(spec=LLMGateway)
        return gateway

    @pytest.fixture
    def mock_audit_logger(self):
        """Mock audit logger for testing."""
        return Mock(spec=AuditLogger)

    @pytest.fixture
    def sample_draft_report(self):
        """Sample draft report with known issues for testing."""
        return """
# Analysis Report: Political Communication Patterns

## Executive Summary

This represents a major breakthrough in political analysis methodology. Our revolutionary 
approach has uncovered unprecedented insights into civic character patterns.

## Statistical Findings

The analysis reveals significant patterns in Dignity (mean=0.99) and Truth (mean=1.05) dimensions.
The correlation between dignity and tribalism is r=-0.999, indicating perfect inverse relationship.

## Evidence Analysis

"We must unite as Americans" demonstrates exceptional civic character across all speakers.
According to Smith et al. (2023), similar patterns have been observed in other studies.

## Conclusions

This groundbreaking research proves beyond doubt that our framework is superior to all 
existing methodologies. The results are absolutely conclusive and represent the definitive 
analysis of political rhetoric.
"""

    @pytest.fixture
    def sample_fact_check_findings(self):
        """Sample fact-check findings in hybrid format."""
        return {
            "status": "completed",
            "findings": [
                {
                    "check_name": "Grandiose Claim",
                    "severity": "WARNING",
                    "description": "Check for grandiose or unsubstantiated claims",
                    "details": "Found multiple grandiose claims that need moderation",
                    "examples": [
                        "major breakthrough in political analysis methodology",
                        "revolutionary approach",
                        "unprecedented insights",
                        "groundbreaking research proves beyond doubt",
                        "absolutely conclusive"
                    ]
                },
                {
                    "check_name": "Statistic Mismatch",
                    "severity": "CRITICAL", 
                    "description": "Verify numerical values match statistical results",
                    "details": "Several statistical values exceed realistic bounds",
                    "examples": [
                        "Dignity mean=0.99 (should be 0.75)",
                        "Truth mean=1.05 (impossible - max is 1.0)",
                        "Correlation r=-0.999 (should be r=-0.65)"
                    ]
                },
                {
                    "check_name": "Citation Violation",
                    "severity": "ERROR",
                    "description": "Remove external academic citations",
                    "details": "Found external citation that should be removed",
                    "examples": ["Smith et al. (2023)"]
                }
            ],
            "validation_results": {
                "total_checks": 6,
                "critical_failures": 1,
                "errors": 1,
                "warnings": 1
            }
        }

    @pytest.fixture
    def sample_corrected_report(self):
        """Expected corrected report after revision."""
        return """
# Analysis Report: Political Communication Patterns

## Executive Summary

This analysis presents findings from our systematic approach to civic character patterns.
The methodology provides insights into political communication dynamics.

## Statistical Findings

The analysis reveals significant patterns in Dignity (mean=0.75) and Truth (mean=0.82) dimensions.
The correlation between dignity and tribalism is r=-0.65, indicating strong inverse relationship.

## Evidence Analysis

"We must unite as Americans" demonstrates notable civic character patterns across speakers.
The evidence suggests consistent themes in political discourse.

## Conclusions

This research provides evidence that our framework offers valuable insights into political rhetoric.
The results indicate meaningful patterns in civic character analysis.
"""

    def test_revision_agent_initialization(self, mock_audit_logger):
        """Test that RevisionAgent initializes correctly."""
        revision_agent = RevisionAgent(
            model="vertex_ai/gemini-2.5-pro",
            audit_logger=mock_audit_logger
        )
        
        assert revision_agent.model == "vertex_ai/gemini-2.5-pro"
        assert revision_agent.audit_logger == mock_audit_logger
        assert revision_agent.prompt_template is not None
        assert hasattr(revision_agent, 'MAX_NUMERICAL_ERRORS')
        assert hasattr(revision_agent, 'MAX_GRANDIOSE_CLAIMS')
        assert hasattr(revision_agent, 'MAX_TOTAL_ISSUES')

    def test_hybrid_fact_check_format_parsing(self, mock_audit_logger, sample_fact_check_findings):
        """Test that RevisionAgent can parse hybrid fact-checker format."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        # Test the format conversion method
        issue_counts = revision_agent._count_issues_by_type_hybrid(sample_fact_check_findings)
        
        assert issue_counts['numerical_errors'] == 1  # Statistic Mismatch
        assert issue_counts['grandiose_claims'] == 1  # Grandiose Claim
        assert issue_counts['factual_errors'] == 1    # Citation Violation (ERROR severity)
        assert issue_counts['total_issues'] == 3

    def test_revision_feasibility_validation(self, mock_audit_logger, sample_fact_check_findings):
        """Test that revision feasibility validation works with hybrid format."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        # Should not raise exception for reasonable number of issues
        revision_agent._validate_revision_feasibility_hybrid(sample_fact_check_findings)
        
        # Test with too many issues
        excessive_findings = {
            "findings": [{"check_name": "Grandiose Claim", "severity": "WARNING"}] * 20
        }
        
        with pytest.raises(ValueError, match="Too many grandiose claims"):
            revision_agent._validate_revision_feasibility_hybrid(excessive_findings)

    def test_hybrid_feedback_formatting(self, mock_audit_logger, sample_fact_check_findings):
        """Test that fact-check feedback is properly formatted from hybrid results."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        feedback = revision_agent._format_fact_check_feedback_hybrid(sample_fact_check_findings)
        
        # Should contain sections for different issue types
        assert "NUMERICAL CORRECTIONS REQUIRED:" in feedback
        assert "TONE MODERATION REQUIRED:" in feedback
        assert "FACTUAL CORRECTIONS REQUIRED:" in feedback
        
        # Should contain specific examples
        assert "Dignity mean=0.99 (should be 0.75)" in feedback
        assert "major breakthrough in political analysis methodology" in feedback
        assert "Smith et al. (2023)" in feedback

    def test_end_to_end_revision_pipeline(
        self, mock_audit_logger, sample_draft_report, sample_fact_check_findings, sample_corrected_report
    ):
        """Test complete revision pipeline with hybrid fact-checker integration."""
        
        # Mock the LLM gateway to return corrected report
        with patch('discernus.agents.revision_agent.agent.LLMGateway') as mock_gateway_class:
            mock_gateway_instance = Mock()
            mock_gateway_instance.execute_call.return_value = (sample_corrected_report, {"tokens": 500})
            mock_gateway_class.return_value = mock_gateway_instance
            
            revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
            
            # Run revision with hybrid fact-check results
            results = revision_agent.revise_report_hybrid(
                draft_report=sample_draft_report,
                fact_check_results=sample_fact_check_findings
            )
            
            # Verify results structure
            assert "revised_report" in results
            assert "corrections_made" in results
            assert "revision_summary" in results
            
            # Verify corrections were applied
            assert len(results["corrections_made"]) == 3  # Three findings
            assert "Applied 3 corrections" in results["revision_summary"]
            
            # Verify LLM was called with proper prompt
            mock_gateway_instance.execute_call.assert_called_once()

    def test_no_corrections_needed(self, mock_audit_logger):
        """Test behavior when fact-checker finds no issues."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        clean_fact_check = {
            "status": "completed",
            "findings": [],
            "validation_results": {
                "total_checks": 6,
                "critical_failures": 0,
                "errors": 0,
                "warnings": 0
            }
        }
        
        draft_report = "Clean report with no issues."
        
        results = revision_agent.revise_report_hybrid(
            draft_report=draft_report,
            fact_check_results=clean_fact_check
        )
        
        # Should return original report unchanged
        assert results["revised_report"] == draft_report
        assert results["corrections_made"] == []
        assert "No revisions needed" in results["revision_summary"]

    def test_revision_logging_transparency(self, mock_audit_logger, sample_draft_report, sample_fact_check_findings):
        """Test that revision process is logged transparently."""
        
        with patch('discernus.agents.revision_agent.agent.LLMGateway') as mock_gateway_class:
            mock_gateway_instance = Mock()
            mock_gateway_instance.execute_call.return_value = ("Revised report", {"tokens": 300})
            mock_gateway_class.return_value = mock_gateway_instance
            
            revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
            
            results = revision_agent.revise_report_hybrid(
                draft_report=sample_draft_report,
                fact_check_results=sample_fact_check_findings
            )
            
            # Verify logging events were called
            assert mock_audit_logger.log_agent_event.called
            
            # Check for start and complete events
            log_calls = mock_audit_logger.log_agent_event.call_args_list
            event_types = [call[1]["event_type"] for call in log_calls]
            
            assert "revision_start" in event_types
            assert "revision_complete" in event_types

    def test_error_threshold_enforcement(self, mock_audit_logger):
        """Test that error thresholds prevent revision of poor quality reports."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        # Create fact-check results with too many numerical errors
        excessive_errors = {
            "findings": [
                {
                    "check_name": "Statistic Mismatch",
                    "severity": "CRITICAL",
                    "description": "Numerical error",
                    "details": f"Error {i}",
                    "examples": []
                }
                for i in range(15)  # Exceeds MAX_NUMERICAL_ERRORS (10)
            ]
        }
        
        with pytest.raises(ValueError, match="Too many numerical errors"):
            revision_agent.revise_report_hybrid(
                draft_report="Poor quality report",
                fact_check_results=excessive_errors
            )

    def test_integration_with_fact_checker_agent(self, mock_audit_logger):
        """Test integration between FactCheckerAgent and RevisionAgent."""
        
        # Mock both agents
        with patch('discernus.agents.revision_agent.agent.LLMGateway') as mock_revision_gateway:
            with patch('discernus.agents.fact_checker_agent.agent.FactCheckerAgent') as mock_fact_checker_class:
                
                # Setup mocks
                mock_revision_instance = Mock()
                mock_revision_instance.execute_call.return_value = ("Corrected report", {"tokens": 400})
                mock_revision_gateway.return_value = mock_revision_instance
                
                mock_fact_checker = Mock()
                mock_fact_checker.check.return_value = {
                    "status": "completed",
                    "findings": [{
                        "check_name": "Grandiose Claim",
                        "severity": "WARNING",
                        "description": "Test issue",
                        "details": "Test details",
                        "examples": ["test example"]
                    }],
                    "validation_results": {"total_checks": 6, "critical_failures": 0, "errors": 0, "warnings": 1}
                }
                mock_fact_checker_class.return_value = mock_fact_checker
                
                # Test the integration
                fact_checker = mock_fact_checker_class(gateway=Mock(), audit_logger=mock_audit_logger)
                revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
                
                # Run fact-check
                fact_check_results = fact_checker.check(
                    report_content="Test report",
                    evidence_index=None
                )
                
                # Run revision
                revision_results = revision_agent.revise_report_hybrid(
                    draft_report="Test report",
                    fact_check_results=fact_check_results
                )
                
                # Verify integration worked
                assert revision_results["revised_report"] == "Corrected report"
                assert len(revision_results["corrections_made"]) == 1


class TestRevisionAgentErrorHandling:
    """Test suite for RevisionAgent error handling and edge cases."""

    @pytest.fixture
    def mock_audit_logger(self):
        return Mock(spec=AuditLogger)

    def test_malformed_fact_check_results(self, mock_audit_logger):
        """Test handling of malformed fact-check results."""
        revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
        
        # Test with missing required fields
        malformed_results = {"status": "completed"}  # Missing 'findings'
        
        results = revision_agent.revise_report_hybrid(
            draft_report="Test report",
            fact_check_results=malformed_results
        )
        
        # Should handle gracefully and return original report
        assert results["revised_report"] == "Test report"
        assert results["corrections_made"] == []

    def test_llm_service_failure_during_revision(self, mock_audit_logger):
        """Test handling of LLM service failures during revision."""
        
        with patch('discernus.agents.revision_agent.agent.LLMGateway') as mock_gateway_class:
            mock_gateway_instance = Mock()
            mock_gateway_instance.execute_call.side_effect = Exception("LLM service unavailable")
            mock_gateway_class.return_value = mock_gateway_instance
            
            revision_agent = RevisionAgent(audit_logger=mock_audit_logger)
            
            fact_check_results = {
                "findings": [{
                    "check_name": "Test Issue",
                    "severity": "WARNING",
                    "description": "Test",
                    "details": "Test details",
                    "examples": []
                }]
            }
            
            # Should handle LLM failure gracefully
            with pytest.raises(Exception, match="LLM service unavailable"):
                revision_agent.revise_report_hybrid(
                    draft_report="Test report",
                    fact_check_results=fact_check_results
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
