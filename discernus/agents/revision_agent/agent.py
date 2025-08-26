"""
Revision Agent for making targeted corrections to synthesis reports based on fact-checker feedback.
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from ...core.audit_logger import AuditLogger
from ...core.hybrid_corpus_service import HybridCorpusService


class RevisionAgent:
    """An agent for correcting synthesis reports based on fact checker findings."""

    def __init__(self, gateway, audit_logger: AuditLogger, corpus_index_service: HybridCorpusService = None):
        self.gateway = gateway
        self.audit_logger = audit_logger
        self.corpus_index_service = corpus_index_service
        self.revision_strategies = self._load_revision_strategies()

    def _load_revision_strategies(self) -> Dict[str, Any]:
        """Loads the revision strategies from the agent's directory."""
        import yaml
        import os
        agent_dir = os.path.dirname(__file__)
        strategies_path = os.path.join(agent_dir, 'revision_strategies.yaml')
        if not os.path.exists(strategies_path):
            # Return default strategies if file doesn't exist
            return self._get_default_strategies()
        with open(strategies_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _get_default_strategies(self) -> Dict[str, Any]:
        """Default revision strategies if no YAML file exists."""
        return {
            "quote_corrections": {
                "significant_drift": "replace_with_canonical",
                "major_drift": "replace_with_canonical",
                "hallucination": "remove_and_warn"
            },
            "statistical_corrections": {
                "invalid_correlation": "remove_and_warn",
                "unrealistic_percentage": "flag_for_review",
                "vague_claim": "add_context_warning"
            },
            "framework_corrections": {
                "undefined_dimension": "remove_and_warn",
                "missing_definition": "add_definition_warning"
            },
            "attribution_corrections": {
                "missing_source": "add_source_warning",
                "vague_attribution": "clarify_attribution"
            }
        }

    def revise_report(
        self,
        draft_report: str,
        fact_checker_report: Dict[str, Any],
        assets: Dict[str, Any],
        corpus_index_service: HybridCorpusService = None,
    ) -> Dict[str, Any]:
        """
        Revise the draft report based on fact checker findings.

        Args:
            draft_report: Content of the draft report to revise
            fact_checker_report: Report from the fact checker agent
            assets: Dictionary containing all synthesis assets
            corpus_index_service: Corpus index service for quote lookup

        Returns:
            Dictionary containing the revised report and revision summary
        """
        # Use provided service or fall back to instance service
        index_service = corpus_index_service or self.corpus_index_service
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                agent_name="RevisionAgent",
                event_type="revision_start",
                data={"report_length": len(draft_report), "findings_count": len(fact_checker_report.get('findings', []))}
            )

        revised_report = draft_report
        revision_summary = {
            "status": "completed",
            "revisions_applied": 0,
            "warnings_added": 0,
            "failed_revisions": 0,
            "revision_details": []
        }

        findings = fact_checker_report.get('findings', [])
        
        for finding in findings:
            revision_result = self._apply_revision(
                finding, revised_report, assets, index_service
            )
            
            if revision_result['success']:
                revised_report = revision_result['revised_text']
                revision_summary['revisions_applied'] += 1
                revision_summary['revision_details'].append({
                    'finding_type': finding.get('check_name'),
                    'action': revision_result['action'],
                    'details': revision_result['details']
                })
            else:
                revision_summary['failed_revisions'] += 1
                revision_summary['revision_details'].append({
                    'finding_type': finding.get('check_name'),
                    'action': 'failed',
                    'details': revision_result['details']
                })

        # Add revision summary to the report
        final_report = self._add_revision_summary(revised_report, revision_summary)
        
        return {
            "revised_report": final_report,
            "revision_summary": revision_summary,
            "original_length": len(draft_report),
            "revised_length": len(final_report)
        }

    def _apply_revision(
        self, finding: Dict[str, Any], current_report: str, assets: Dict[str, Any], 
        corpus_index_service: HybridCorpusService
    ) -> Dict[str, Any]:
        """
        Apply a specific revision based on a finding.
        
        Returns:
            Dictionary with revision result
        """
        check_name = finding.get('check_name', '')
        
        if check_name == "Quote Validation":
            return self._revise_quote(finding, current_report, corpus_index_service)
        elif check_name == "Statistical Verification":
            return self._revise_statistics(finding, current_report, assets)
        elif check_name == "Framework Compliance":
            return self._revise_framework(finding, current_report, assets)
        elif check_name == "Evidence Attribution":
            return self._revise_attribution(finding, current_report, assets)
        else:
            return {
                'success': False,
                'action': 'unknown_check',
                'details': f'Unknown check type: {check_name}',
                'revised_text': current_report
            }

    def _revise_quote(
        self, finding: Dict[str, Any], current_report: str, 
        corpus_index_service: HybridCorpusService
    ) -> Dict[str, Any]:
        """Revise quotes based on validation findings."""
        quote_validation = finding.get('quote_validation', {})
        drift_level = quote_validation.get('drift_level', 'unknown')
        quote = quote_validation.get('quote', '')
        canonical_text = quote_validation.get('canonical_text', '')
        
        if not quote:
            return {
                'success': False,
                'action': 'no_quote_found',
                'details': 'No quote found in finding',
                'revised_text': current_report
            }

        if drift_level in ['significant_drift', 'major_drift'] and canonical_text:
            # Replace with canonical text
            revised_text = current_report.replace(quote, canonical_text)
            return {
                'success': True,
                'action': 'replaced_with_canonical',
                'details': f'Replaced drifted quote with canonical text',
                'revised_text': revised_text
            }
        
        elif drift_level == 'hallucination':
            # Remove hallucinated quote and add warning
            warning = f"\n\n> **WARNING**: The following quote was removed as it could not be validated against source material: \"{quote[:100]}{'...' if len(quote) > 100 else ''}\"\n\n"
            revised_text = current_report.replace(quote, '')
            revised_text = warning + revised_text
            return {
                'success': True,
                'action': 'removed_hallucination',
                'details': f'Removed hallucinated quote and added warning',
                'revised_text': revised_text
            }
        
        else:
            return {
                'success': False,
                'action': 'no_action_needed',
                'details': f'Quote drift level {drift_level} does not require revision',
                'revised_text': current_report
            }

    def _revise_statistics(
        self, finding: Dict[str, Any], current_report: str, assets: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Revise statistical claims based on validation findings."""
        description = finding.get('description', '')
        
        if 'Invalid correlation coefficient' in description:
            # Remove invalid correlation and add warning
            examples = finding.get('examples', [])
            if examples:
                invalid_value = examples[0]
                warning = f"\n\n> **WARNING**: The following invalid statistical claim was removed: {invalid_value}\n\n"
                revised_text = current_report.replace(invalid_value, '')
                revised_text = warning + revised_text
                return {
                    'success': True,
                    'action': 'removed_invalid_statistic',
                    'details': f'Removed invalid correlation coefficient and added warning',
                    'revised_text': revised_text
                }
        
        elif '100% value' in description:
            # Add context warning
            warning = "\n\n> **NOTE**: Claims of 100% accuracy or completeness should be interpreted with caution and may require additional context.\n\n"
            revised_text = warning + current_report
            return {
                'success': True,
                'action': 'added_context_warning',
                'details': 'Added warning about 100% claims',
                'revised_text': revised_text
            }
        
        return {
            'success': False,
            'action': 'no_action_needed',
            'details': 'Statistical finding does not require revision',
            'revised_text': current_report
        }

    def _revise_framework(
        self, finding: Dict[str, Any], current_report: str, assets: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Revise framework compliance issues."""
        description = finding.get('description', '')
        
        if 'dimension hallucination' in description.lower():
            # Add warning about undefined dimensions
            warning = "\n\n> **WARNING**: This report mentions analytical dimensions that may not be fully defined in the framework specification. Please verify all dimension references.\n\n"
            revised_text = warning + current_report
            return {
                'success': True,
                'action': 'added_dimension_warning',
                'details': 'Added warning about undefined dimensions',
                'revised_text': revised_text
            }
        
        return {
            'success': False,
            'action': 'no_action_needed',
            'details': 'Framework finding does not require revision',
            'revised_text': current_report
        }

    def _revise_attribution(
        self, finding: Dict[str, Any], current_report: str, assets: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Revise evidence attribution issues."""
        description = finding.get('description', '')
        
        if 'attribution phrases without specific sources' in description:
            # Add warning about vague attribution
            warning = "\n\n> **NOTE**: This report contains attribution phrases that may benefit from more specific source references for better traceability.\n\n"
            revised_text = warning + current_report
            return {
                'success': True,
                'action': 'added_attribution_warning',
                'details': 'Added warning about vague attribution',
                'revised_text': revised_text
            }
        
        return {
            'success': False,
            'action': 'no_action_needed',
            'details': 'Attribution finding does not require revision',
            'revised_text': current_report
        }

    def _add_revision_summary(self, report: str, revision_summary: Dict[str, Any]) -> str:
        """Add a revision summary to the end of the report."""
        summary = f"""
## Revision Summary

This report has been automatically revised based on fact-checking findings:

- **Revisions Applied**: {revision_summary['revisions_applied']}
- **Warnings Added**: {revision_summary['warnings_added']}
- **Failed Revisions**: {revision_summary['failed_revisions']}

### Revision Details

"""
        
        for detail in revision_summary['revision_details']:
            summary += f"- **{detail['finding_type']}**: {detail['action']} - {detail['details']}\n"
        
        summary += "\n---\n*Report automatically revised by Discernus Revision Agent*"
        
        return report + summary
