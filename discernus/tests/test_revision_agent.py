"""
Unit tests for RevisionAgent
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from discernus.agents.revision_agent.agent import RevisionAgent


class TestRevisionAgent(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.mock_audit_logger = Mock()
        self.agent = RevisionAgent(audit_logger=self.mock_audit_logger)
        
        # Mock LLM gateway to avoid actual API calls
        self.agent.llm_gateway = Mock()
        self.agent.llm_gateway.execute_call.return_value = (
            "Revised report with corrections applied", 
            {"model": "test", "tokens": 100}
        )
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_count_issues_by_type(self):
        """Test issue categorization from fact-check results."""
        fact_check_results = {
            "issues": [
                {"type": "statistical_mismatch", "severity": "critical"},
                {"type": "grandiose_claim", "severity": "medium"},
                {"type": "numerical_accuracy", "severity": "high"},
                {"type": "factual_error", "severity": "critical"}
            ]
        }
        
        issue_counts = self.agent._count_issues_by_type(fact_check_results)
        
        self.assertEqual(issue_counts['numerical_errors'], 2)  # statistical + numerical
        self.assertEqual(issue_counts['grandiose_claims'], 1)
        self.assertEqual(issue_counts['factual_errors'], 1)
        self.assertEqual(issue_counts['total_issues'], 4)
    
    def test_validate_revision_feasibility_success(self):
        """Test that feasible revisions pass validation."""
        fact_check_results = {
            "issues": [
                {"type": "statistical_mismatch", "severity": "medium"},
                {"type": "grandiose_claim", "severity": "low"}
            ]
        }
        
        # Should not raise exception
        self.agent._validate_revision_feasibility(fact_check_results)
    
    def test_validate_revision_feasibility_too_many_numerical_errors(self):
        """Test that too many numerical errors triggers failure."""
        fact_check_results = {
            "issues": [{"type": "numerical_accuracy", "severity": "high"}] * 15
        }
        
        with self.assertRaises(ValueError) as context:
            self.agent._validate_revision_feasibility(fact_check_results)
        
        self.assertIn("Too many numerical errors", str(context.exception))
    
    def test_validate_revision_feasibility_too_many_total_issues(self):
        """Test that too many total issues triggers failure."""
        fact_check_results = {
            "issues": [{"type": "various_issue", "severity": "medium"}] * 20
        }
        
        with self.assertRaises(ValueError) as context:
            self.agent._validate_revision_feasibility(fact_check_results)
        
        self.assertIn("Too many total issues", str(context.exception))
    
    def test_format_fact_check_feedback(self):
        """Test formatting of fact-check results into correction instructions."""
        fact_check_results = {
            "issues": [
                {
                    "type": "statistical_mismatch",
                    "description": "Correlation value incorrect",
                    "suggested_correction": "Use -0.85 instead of -0.8"
                },
                {
                    "type": "grandiose_claim", 
                    "description": "Overstated significance",
                    "suggested_correction": "Replace 'revolutionary' with 'notable'"
                }
            ]
        }
        
        feedback = self.agent._format_fact_check_feedback(fact_check_results)
        
        self.assertIn("NUMERICAL CORRECTIONS REQUIRED", feedback)
        self.assertIn("TONE MODERATION REQUIRED", feedback)
        self.assertIn("Correlation value incorrect", feedback)
        self.assertIn("Use -0.85 instead of -0.8", feedback)
        self.assertIn("Replace 'revolutionary' with 'notable'", feedback)
    
    def test_format_fact_check_feedback_no_issues(self):
        """Test formatting when no issues are found."""
        fact_check_results = {"issues": []}
        
        feedback = self.agent._format_fact_check_feedback(fact_check_results)
        
        self.assertEqual(feedback, "No corrections needed - fact-check passed.")
    
    def test_revise_report_no_issues(self):
        """Test revision when fact-check passes with no issues."""
        draft_report = "This is a perfect report with no issues."
        fact_check_results = {"issues": []}
        
        result = self.agent.revise_report(draft_report, fact_check_results)
        
        self.assertEqual(result["revised_report"], draft_report)
        self.assertEqual(result["corrections_made"], [])
        self.assertEqual(result["revision_summary"], "No revisions needed - fact-check passed")
        
        # Should not call LLM if no corrections needed
        self.agent.llm_gateway.execute_call.assert_not_called()
    
    def test_revise_report_with_corrections(self):
        """Test revision when corrections are needed."""
        draft_report = "This revolutionary analysis proves unprecedented results."
        fact_check_results = {
            "issues": [
                {
                    "type": "grandiose_claim",
                    "description": "Overstated language",
                    "suggested_correction": "Use measured academic tone"
                }
            ]
        }
        
        result = self.agent.revise_report(draft_report, fact_check_results)
        
        self.assertEqual(result["revised_report"], "Revised report with corrections applied")
        self.assertEqual(len(result["corrections_made"]), 1)
        self.assertIn("Applied 1 corrections", result["revision_summary"])
        
        # Should call LLM for revision
        self.agent.llm_gateway.execute_call.assert_called_once()
        
        # Check that prompt contains correction instructions
        call_args = self.agent.llm_gateway.execute_call.call_args
        prompt = call_args[1]['prompt']
        self.assertIn("TONE MODERATION REQUIRED", prompt)
        self.assertIn("Overstated language", prompt)
    
    def test_revise_report_audit_logging(self):
        """Test that audit events are logged correctly."""
        draft_report = "Test report"
        fact_check_results = {
            "issues": [{"type": "test_issue", "description": "Test"}]
        }
        
        self.agent.revise_report(draft_report, fact_check_results)
        
        # Check audit logging calls
        self.assertEqual(self.mock_audit_logger.log_agent_event.call_count, 2)
        
        # Check start event
        start_call = self.mock_audit_logger.log_agent_event.call_args_list[0]
        self.assertEqual(start_call[1]['agent_name'], "RevisionAgent")
        self.assertEqual(start_call[1]['event_type'], "revision_start")
        
        # Check complete event  
        complete_call = self.mock_audit_logger.log_agent_event.call_args_list[1]
        self.assertEqual(complete_call[1]['agent_name'], "RevisionAgent")
        self.assertEqual(complete_call[1]['event_type'], "revision_complete")


if __name__ == '__main__':
    unittest.main()
