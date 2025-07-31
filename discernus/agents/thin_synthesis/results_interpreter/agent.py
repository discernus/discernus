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
    footnote_registry: Optional[Dict[int, Dict[str, str]]] = None
    
    # Provenance metadata for report headers
    run_id: Optional[str] = None
    models_used: Optional[Dict[str, str]] = None  # {"analysis": "model", "synthesis": "model"}
    execution_timestamp_utc: Optional[str] = None
    execution_timestamp_local: Optional[str] = None
    framework_name: Optional[str] = None
    framework_version: Optional[str] = None
    corpus_info: Optional[Dict[str, Any]] = None
    
    # Error and warning tracking
    notable_errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    quality_alerts: Optional[List[str]] = None

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
        
        # Build footnote instructions if available
        footnote_instructions = ""
        if request.footnote_registry:
            footnote_instructions = f"""

CRITICAL FOOTNOTE REQUIREMENTS:
You must use numbered footnotes [1], [2], [3] etc. to cite evidence. Each piece of evidence has been assigned a footnote number.

Footnote Registry (Evidence Hash Verification):
{str(request.footnote_registry)}

INSTRUCTIONS FOR EVIDENCE CITATIONS:
1. When referencing evidence, you MUST use the assigned footnote number in brackets [1], [2], etc.
2. DO NOT create new evidence - only reference evidence with existing footnote numbers
3. Multiple citations should be formatted as [1,2,3] or [1],[2],[3]
4. The footnote registry above shows the hash verification for each piece of evidence
5. If you cannot find a footnote number for evidence, DO NOT cite it - this prevents hallucination
6. MANDATORY: You must include a "References" section at the end listing all footnotes with their full evidence text

REFERENCES SECTION FORMAT:
For each footnote number you use, include the full entry in the References section:
[1] [Speaker from artifact_id]: "[Complete evidence_text from registry]" (Document: [artifact_id])
[2] [Speaker from artifact_id]: "[Complete evidence_text from registry]" (Document: [artifact_id])

Example in text: "The analysis reveals strong civic virtue patterns [1], particularly in procedural legitimacy [2,3]."
Example References section:
## References
[1] John McCain: "This is a historic election, and I recognize the special significance it has for African-Americans" (Document: john_mccain_2008_concession)
[2] Bernie Sanders: "We must fight against oligarchy and economic inequality" (Document: bernie_sanders_2025_fighting_oligarchy)
"""
        
        # Build provenance metadata string
        provenance_metadata = self._build_provenance_metadata(request)
        
        # Use YAML template with raw data
        prompt = self.prompt_template.format(
            provenance_metadata=provenance_metadata,
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context or "Not provided",
            stats_summary=stats_str,
            total_evidence=total_evidence,
            evidence_summary=evidence_str,
            footnote_instructions=footnote_instructions,
            run_id=request.run_id or "Not provided"
        )

        return prompt
    
    def _build_provenance_metadata(self, request: InterpretationRequest) -> str:
        """Build a comprehensive provenance metadata string for the report header."""
        
        metadata_parts = []
        
        # Run ID
        if request.run_id:
            metadata_parts.append(f"Run ID: {request.run_id}")
        
        # Execution timestamps
        if request.execution_timestamp_utc and request.execution_timestamp_local:
            metadata_parts.append(f"Execution Time (UTC): {request.execution_timestamp_utc}")
            metadata_parts.append(f"Execution Time (Local): {request.execution_timestamp_local}")
        elif request.execution_timestamp_utc:
            metadata_parts.append(f"Execution Time (UTC): {request.execution_timestamp_utc}")
        elif request.execution_timestamp_local:
            metadata_parts.append(f"Execution Time (Local): {request.execution_timestamp_local}")
        
        # Models used
        if request.models_used:
            models_info = []
            for stage, model in request.models_used.items():
                models_info.append(f"{stage.title()}: {model}")
            if models_info:
                metadata_parts.append(f"Models Used: {', '.join(models_info)}")
        
        # Framework information
        framework_info = []
        if request.framework_name:
            framework_info.append(f"Framework: {request.framework_name}")
        if request.framework_version:
            framework_info.append(f"Version: {request.framework_version}")
        if framework_info:
            metadata_parts.append(' '.join(framework_info))
        
        # Corpus information
        if request.corpus_info:
            corpus_details = []
            if 'document_count' in request.corpus_info:
                corpus_details.append(f"Documents: {request.corpus_info['document_count']}")
            if 'corpus_type' in request.corpus_info:
                corpus_details.append(f"Type: {request.corpus_info['corpus_type']}")
            if 'date_range' in request.corpus_info:
                corpus_details.append(f"Range: {request.corpus_info['date_range']}")
            if corpus_details:
                metadata_parts.append(f"Corpus: {', '.join(corpus_details)}")
        
        # Error and warning information
        error_sections = []
        
        if request.notable_errors:
            error_list = []
            for i, error in enumerate(request.notable_errors[:3], 1):  # Limit to 3 most important
                error_list.append(f"  {i}. {error}")
            error_sections.append(f"Notable Errors:\n" + "\n".join(error_list))
        
        if request.warnings:
            warning_list = []
            for i, warning in enumerate(request.warnings[:3], 1):  # Limit to 3 most important
                warning_list.append(f"  {i}. {warning}")
            error_sections.append(f"Warnings:\n" + "\n".join(warning_list))
            
        if request.quality_alerts:
            alert_list = []
            for i, alert in enumerate(request.quality_alerts[:2], 1):  # Limit to 2 most important
                alert_list.append(f"  {i}. {alert}")
            error_sections.append(f"Quality Alerts:\n" + "\n".join(alert_list))
        
        # Combine all sections
        all_sections = metadata_parts + error_sections
        
        if all_sections:
            return '\n'.join(all_sections)
        else:
            return "Provenance metadata not available"
    
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
        """ULTRA-THIN approach: LLM generates perfect report, no parsing needed."""
        
        # ULTRA-THIN: The LLM generated a perfect markdown report
        # No parsing, no software intelligence, just trust the LLM
        word_count = len(response_content.split())
        
        return InterpretationResponse(
            narrative_report=response_content,  # This is the ONLY deliverable that matters
            executive_summary="",  # Unused by downstream - LLM includes in narrative
            key_findings=[],       # Unused by downstream - LLM includes in narrative
            methodology_notes="",  # Unused by downstream - LLM includes in narrative
            statistical_summary={},  # Unused by downstream - LLM includes in narrative
            evidence_integration_summary={},  # Unused by downstream - LLM includes in narrative
            success=True,
            word_count=word_count
        )
    
    # REMOVED: _extract_section_thin - ULTRA-THIN approach doesn't parse LLM output
    # The LLM generates perfect markdown with all sections included
    
    # REMOVED: _extract_key_findings_thin - ULTRA-THIN approach doesn't parse LLM output
    # The LLM generates perfect markdown with key findings included in proper sections
    
    # REMOVED: _generate_statistical_summary - ULTRA-THIN approach
    # The LLM analyzes statistical results and includes summary in the narrative report
    # No need for software to duplicate this intelligence
    
    # REMOVED: _generate_evidence_integration_summary - ULTRA-THIN approach  
    # The LLM analyzes evidence integration and includes summary in the narrative report
    # No need for software to duplicate this intelligence
    
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