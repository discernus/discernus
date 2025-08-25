"""
Revision Agent for making targeted corrections to synthesis reports based on fact-checker feedback.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from ...gateway.llm_gateway import LLMGateway, ModelRegistry
from ...core.audit_logger import AuditLogger


class RevisionAgent:
    """
    Makes targeted corrections to synthesis reports based on fact-checker feedback.
    Designed to preserve author voice while fixing numerical, factual, and tone issues.
    """
    
    # Error thresholds for fail-fast behavior
    MAX_NUMERICAL_ERRORS = 10
    MAX_GRANDIOSE_CLAIMS = 5
    MAX_TOTAL_ISSUES = 15
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro", audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.audit_logger = audit_logger
        self.llm_gateway = LLMGateway(ModelRegistry())
        
        # Load prompt template
        prompt_path = Path(__file__).parent / "prompt.yaml"
        with open(prompt_path, 'r') as f:
            self.prompt_template = yaml.safe_load(f)
    
    def _count_issues_by_type(self, fact_check_results: Dict[str, Any]) -> Dict[str, int]:
        """Count different types of issues from fact-checker results."""
        issue_counts = {
            'numerical_errors': 0,
            'grandiose_claims': 0,
            'factual_errors': 0,
            'total_issues': 0
        }
        
        # Parse fact-check results to categorize issues
        if 'issues' in fact_check_results:
            for issue in fact_check_results['issues']:
                issue_type = issue.get('type', '').lower()
                severity = issue.get('severity', '').lower()
                
                if 'statistic' in issue_type or 'numerical' in issue_type:
                    issue_counts['numerical_errors'] += 1
                elif 'grandiose' in issue_type or 'claim' in issue_type:
                    issue_counts['grandiose_claims'] += 1
                elif severity == 'critical' or 'factual' in issue_type:
                    issue_counts['factual_errors'] += 1
                    
                issue_counts['total_issues'] += 1
        
        return issue_counts
    
    def _validate_revision_feasibility(self, fact_check_results: Dict[str, Any]) -> None:
        """Check if the number of issues is within revision agent capabilities."""
        issue_counts = self._count_issues_by_type(fact_check_results)
        
        if issue_counts['numerical_errors'] > self.MAX_NUMERICAL_ERRORS:
            raise ValueError(f"Too many numerical errors ({issue_counts['numerical_errors']}) for revision agent - synthesis quality insufficient")
        
        if issue_counts['grandiose_claims'] > self.MAX_GRANDIOSE_CLAIMS:
            raise ValueError(f"Too many grandiose claims ({issue_counts['grandiose_claims']}) for revision agent - synthesis quality insufficient")
            
        if issue_counts['total_issues'] > self.MAX_TOTAL_ISSUES:
            raise ValueError(f"Too many total issues ({issue_counts['total_issues']}) for revision agent - synthesis quality insufficient")
    
    def _format_fact_check_feedback(self, fact_check_results: Dict[str, Any]) -> str:
        """Format fact-checker results into clear correction instructions."""
        if not fact_check_results.get('issues'):
            return "No corrections needed - fact-check passed."
        
        feedback_sections = []
        
        # Group issues by type for clearer instructions
        numerical_issues = []
        tone_issues = []
        factual_issues = []
        
        for issue in fact_check_results['issues']:
            issue_type = issue.get('type', '').lower()
            
            if 'statistic' in issue_type or 'numerical' in issue_type:
                numerical_issues.append(issue)
            elif 'grandiose' in issue_type or 'claim' in issue_type:
                tone_issues.append(issue)
            else:
                factual_issues.append(issue)
        
        if numerical_issues:
            feedback_sections.append("NUMERICAL CORRECTIONS REQUIRED:")
            for issue in numerical_issues:
                feedback_sections.append(f"- {issue.get('description', 'Numerical accuracy issue')}")
                if 'suggested_correction' in issue:
                    feedback_sections.append(f"  Correction: {issue['suggested_correction']}")
        
        if tone_issues:
            feedback_sections.append("\nTONE MODERATION REQUIRED:")
            for issue in tone_issues:
                feedback_sections.append(f"- {issue.get('description', 'Tone issue')}")
                if 'suggested_correction' in issue:
                    feedback_sections.append(f"  Suggestion: {issue['suggested_correction']}")
        
        if factual_issues:
            feedback_sections.append("\nFACTUAL CORRECTIONS REQUIRED:")
            for issue in factual_issues:
                feedback_sections.append(f"- {issue.get('description', 'Factual accuracy issue')}")
                if 'suggested_correction' in issue:
                    feedback_sections.append(f"  Correction: {issue['suggested_correction']}")
        
        return "\n".join(feedback_sections)
    
    def revise_report(
        self, 
        draft_report: str, 
        fact_check_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Revise synthesis report based on fact-checker feedback.
        
        Args:
            draft_report: Original synthesis report text
            fact_check_results: Results from fact-checker validation
            
        Returns:
            Dict containing revised report and metadata
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                agent_name="RevisionAgent",
                event_type="revision_start",
                data={
                    "draft_length": len(draft_report),
                    "fact_check_issues": len(fact_check_results.get('issues', []))
                }
            )
        
        # Validate that revision is feasible
        self._validate_revision_feasibility(fact_check_results)
        
        # Format fact-check feedback for the LLM
        correction_instructions = self._format_fact_check_feedback(fact_check_results)
        
        # If no issues, return original report
        if correction_instructions == "No corrections needed - fact-check passed.":
            return {
                "revised_report": draft_report,
                "corrections_made": [],
                "revision_summary": "No revisions needed - fact-check passed"
            }
        
        # Assemble revision prompt
        revision_prompt = f"""
{self.prompt_template['role']}

{self.prompt_template['task']}

{self.prompt_template['constraints']}

{self.prompt_template['tone_guidelines']}

FACT-CHECK FEEDBACK TO ADDRESS:
{correction_instructions}

ORIGINAL REPORT TO REVISE:
{draft_report}

{self.prompt_template['output_format']}

{self.prompt_template['validation']}

Please provide the revised report with the corrections applied:
"""
        
        # Execute revision
        revised_report, metadata = self.llm_gateway.execute_call(
            model=self.model,
            prompt=revision_prompt,
            temperature=0.1  # Low temperature for precise corrections
        )
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                agent_name="RevisionAgent",
                event_type="revision_complete",
                data={
                    "original_length": len(draft_report),
                    "revised_length": len(revised_report),
                    "similarity_ratio": len(revised_report) / len(draft_report) if draft_report else 0
                }
            )
        
        return {
            "revised_report": revised_report,
            "corrections_made": fact_check_results.get('issues', []),
            "revision_summary": f"Applied {len(fact_check_results.get('issues', []))} corrections",
            "llm_metadata": metadata
        }
