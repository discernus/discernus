#!/usr/bin/env python3
"""
ResultsInterpreter Agent

This agent receives statistical results and curated evidence and synthesizes
them into a comprehensive, human-readable narrative report.

Key Design Principles:
- Narrative synthesis: Combines quantitative and qualitative insights
- Evidence integration: Weaves statistical findings with supporting evidence
- Framework alignment: Interprets results within the analytical framework context
- Academic quality: Produces peer-review ready analysis
- Scalable output: No token limits due to focused synthesis approach
"""

import json
import logging
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Import LLM gateway from main codebase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

@dataclass
class InterpretationRequest:
    """Request structure for results interpretation."""
    statistical_results: Dict[str, Any]
    curated_evidence: Dict[str, List[Any]]
    framework_spec: str
    experiment_context: Optional[str] = None
    interpretation_focus: str = "comprehensive"  # "comprehensive", "statistical", "narrative"

@dataclass
class InterpretationResponse:
    """Response structure containing the final narrative report."""
    narrative_report: str
    executive_summary: str
    key_findings: List[str]
    methodology_notes: str
    statistical_summary: Dict[str, Any]
    evidence_integration_summary: Dict[str, Any]
    success: bool
    word_count: int
    error_message: Optional[str] = None

class ResultsInterpreter:
    """
    Synthesizes statistical results and curated evidence into narrative reports.
    
    This agent leverages LLM intelligence to create human-readable, academically
    rigorous interpretations that integrate quantitative findings with qualitative
    evidence in a coherent narrative.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        """
        Initialize the ResultsInterpreter.
        
        Args:
            model: LLM model to use for interpretation (Pro for better synthesis)
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load the prompt template from YAML file."""
        prompt_file = Path(__file__).parent / "prompt.yaml"
        with open(prompt_file, 'r') as f:
            config = yaml.safe_load(f)
            return config['template']
        
    def interpret_results(self, request: InterpretationRequest) -> InterpretationResponse:
        """
        Generate comprehensive narrative interpretation of results.
        
        Args:
            request: InterpretationRequest containing results and evidence
            
        Returns:
            InterpretationResponse with narrative report
        """
        try:
            # CRITICAL: Validate required data before proceeding
            validation_error = self._validate_required_data(request)
            if validation_error:
                self.logger.error(f"Results interpretation failed - missing required data: {validation_error}")
                return InterpretationResponse(
                    narrative_report="",
                    executive_summary="",
                    key_findings=[],
                    methodology_notes="",
                    statistical_summary={},
                    evidence_integration_summary={},
                    success=False,
                    word_count=0,
                    error_message=f"CRITICAL: Missing required data for interpretation - {validation_error}"
                )
            
            # Build the interpretation prompt
            prompt = self._build_interpretation_prompt(request)
            
            # Call LLM for interpretation
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                max_tokens=8000   # Allow for comprehensive reports
            )
            
            if not response_content or not metadata.get('success'):
                return InterpretationResponse(
                    narrative_report="",
                    executive_summary="",
                    key_findings=[],
                    methodology_notes="",
                    statistical_summary={},
                    evidence_integration_summary={},
                    success=False,
                    word_count=0,
                    error_message=metadata.get('error', 'Empty response from LLM')
                )
            
            # Parse the LLM response
            return self._parse_interpretation_response(response_content, request)
            
        except Exception as e:
            self.logger.error(f"Results interpretation failed: {str(e)}")
            return InterpretationResponse(
                narrative_report="",
                executive_summary="",
                key_findings=[],
                methodology_notes="",
                statistical_summary={},
                evidence_integration_summary={},
                success=False,
                word_count=0,
                error_message=str(e)
            )
    
    def _build_interpretation_prompt(self, request: InterpretationRequest) -> str:
        """Build the comprehensive interpretation prompt using YAML template (THIN architecture)."""
        
        # THIN approach: Pass raw data to LLM as strings
        # Let LLM handle any data structure without JSON serialization
        
        # Defensive checks: ensure inputs are not None
        if request.statistical_results is None:
            request.statistical_results = {}
        if request.curated_evidence is None:
            request.curated_evidence = {}
        
        # Convert data to strings - let LLM handle interpretation
        stats_str = str(request.statistical_results)
        evidence_str = str(request.curated_evidence)
        
        # Count total evidence pieces
        total_evidence = sum(len(evidence_list) for evidence_list in request.curated_evidence.values())
        
        # Use YAML template with raw data
        prompt = self.prompt_template.format(
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context or "Not provided",
            stats_summary=stats_str,
            total_evidence=total_evidence,
            evidence_summary=evidence_str
        )

        return prompt
    
    def _validate_required_data(self, request: InterpretationRequest) -> Optional[str]:
        """
        Minimal THIN validation - just ensure we have data to work with.
        Let the LLM handle data structure understanding.
        
        Returns:
            None if validation passes, error message string if validation fails
        """
        # Basic checks only - no hardcoded expectations
        if not request.statistical_results:
            return "No statistical results provided"
        
        if not request.curated_evidence:
            return "No curated evidence provided"
        
        if not request.framework_spec or not request.framework_spec.strip():
            return "No framework specification provided"
        
        # Let the LLM figure out what's in the data
        return None
    
    # THIN approach: No formatting methods needed - pass raw data as base64
    
    # THIN approach: No formatting methods needed - pass raw data as base64
    
    def _extract_speaker_name(self, document_id: str) -> str:
        """Extract speaker name from document ID if it follows the expected pattern."""
        # Expected pattern: speaker_name_year_context.txt
        # Example: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt
        
        if not document_id or document_id == '{artifact_id}':
            return document_id
        
        # Remove .txt extension if present
        if document_id.endswith('.txt'):
            document_id = document_id[:-4]
        
        # Split by underscores and try to extract speaker name
        parts = document_id.split('_')
        if len(parts) >= 3:
            # Look for patterns like "firstname_lastname_year_context"
            # Try to find where the year starts (4-digit number)
            for i, part in enumerate(parts):
                if len(part) == 4 and part.isdigit():
                    # Everything before the year is likely the speaker name
                    speaker_parts = parts[:i]
                    if speaker_parts:
                        # Convert to proper name format
                        speaker_name = ' '.join(part.title() for part in speaker_parts)
                        return speaker_name
        
        # Fallback: return the original ID
        return document_id
    
    def _parse_interpretation_response(self, response_content: str, 
                                     request: InterpretationRequest) -> InterpretationResponse:
        """Parse the LLM interpretation response into structured format."""
        
        # Extract sections from the response
        executive_summary = self._extract_section(response_content, "executive summary")
        key_findings = self._extract_key_findings(response_content)
        methodology_notes = self._extract_section(response_content, "methodology")
        
        # Calculate word count
        word_count = len(response_content.split())
        
        # Generate statistical summary
        statistical_summary = self._generate_statistical_summary(request.statistical_results)
        
        # Generate evidence integration summary
        evidence_integration_summary = self._generate_evidence_integration_summary(request.curated_evidence)
        
        return InterpretationResponse(
            narrative_report=response_content,
            executive_summary=executive_summary,
            key_findings=key_findings,
            methodology_notes=methodology_notes,
            statistical_summary=statistical_summary,
            evidence_integration_summary=evidence_integration_summary,
            success=True,
            word_count=word_count
        )
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the narrative report."""
        
        import re
        
        # Look for section headers (various formats)
        patterns = [
            f"#{1,3}\\s*{section_name}.*?\\n(.*?)(?=\\n#{1,3}|$)",
            f"\\*\\*{section_name}.*?\\*\\*\\n(.*?)(?=\\n\\*\\*|$)",
            f"{section_name.upper()}.*?\\n(.*?)(?=\\n[A-Z][A-Z]|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Fallback: return first 200 words if no section found
        words = text.split()[:200]
        return " ".join(words) + "..." if len(words) == 200 else " ".join(words)
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from the narrative report."""
        
        import re
        
        # Look for bullet points or numbered lists in key findings section
        key_findings_section = self._extract_section(text, "key findings")
        
        # Extract bullet points or numbered items
        patterns = [
            r"[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)",
            r"\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)"
        ]
        
        findings = []
        for pattern in patterns:
            matches = re.findall(pattern, key_findings_section, re.MULTILINE)
            if matches:
                findings.extend([match.strip() for match in matches])
                break
        
        # If no structured findings found, create from first few sentences
        if not findings:
            sentences = key_findings_section.split('.')[:5]
            findings = [sent.strip() + '.' for sent in sentences if sent.strip()]
        
        return findings[:7]  # Limit to 7 findings
    
    def _generate_statistical_summary(self, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of statistical results."""
        
        summary = {
            'total_dimensions_analyzed': 0,
            'significant_hypotheses': 0,
            'total_hypotheses': 0,
            'reliability_clusters_assessed': 0,
            'correlation_matrices_generated': 0
        }
        
        if 'descriptive_stats' in statistical_results:
            summary['total_dimensions_analyzed'] = len(statistical_results['descriptive_stats'])
        
        if 'hypothesis_tests' in statistical_results:
            hyp_tests = statistical_results['hypothesis_tests']
            summary['total_hypotheses'] = len(hyp_tests)
            
            significant = 0
            for results in hyp_tests.values():
                if isinstance(results, dict) and results.get('is_significant_alpha_05', False):
                    significant += 1
            summary['significant_hypotheses'] = significant
        
        if 'reliability_metrics' in statistical_results:
            summary['reliability_clusters_assessed'] = len(statistical_results['reliability_metrics'])
        
        if 'correlations' in statistical_results:
            correlations = statistical_results['correlations']
            matrix_count = sum(1 for key in correlations.keys() if 'matrix' in key.lower())
            summary['correlation_matrices_generated'] = matrix_count
        
        return summary
    
    def _generate_evidence_integration_summary(self, curated_evidence: Dict[str, List[Any]]) -> Dict[str, Any]:
        """Generate a summary of evidence integration."""
        
        total_evidence = sum(len(evidence_list) for evidence_list in curated_evidence.values())
        
        # Calculate evidence distribution
        evidence_by_category = {category: len(evidence_list) 
                              for category, evidence_list in curated_evidence.items()}
        
        # Calculate average confidence if available
        all_confidences = []
        for evidence_list in curated_evidence.values():
            for evidence in evidence_list:
                if hasattr(evidence, 'confidence'):
                    all_confidences.append(evidence.confidence)
                elif isinstance(evidence, dict) and 'confidence' in evidence:
                    all_confidences.append(evidence['confidence'])
        
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0
        
        return {
            'total_evidence_integrated': total_evidence,
            'evidence_categories': len(curated_evidence),
            'evidence_by_category': evidence_by_category,
            'average_evidence_confidence': round(avg_confidence, 3),
            'integration_approach': 'post_computation_curation'
        }
    
    def generate_executive_summary_only(self, request: InterpretationRequest) -> str:
        """Generate just an executive summary for quick insights."""
        
        # Simplified prompt for executive summary only
        stats_summary = self._format_statistical_results(request.statistical_results)
        evidence_summary = self._format_curated_evidence(request.curated_evidence)
        
        prompt = f"""Create a concise executive summary (150-200 words) that synthesizes these research findings:

FRAMEWORK: {request.framework_spec[:200]}...

STATISTICAL RESULTS:
{stats_summary}

KEY EVIDENCE:
{evidence_summary[:500]}...

Focus on the most important discoveries, their practical implications, and key conclusions. Write for an executive audience."""
        
        try:
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an executive research consultant creating concise, impactful summaries.",
                max_tokens=300
            )
            
            return response_content if metadata.get('success') else "Executive summary generation failed."
            
        except Exception as e:
            self.logger.error(f"Executive summary generation failed: {str(e)}")
            return f"Executive summary generation failed: {str(e)}" 