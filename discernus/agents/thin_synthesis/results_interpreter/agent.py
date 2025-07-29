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
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

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
        
    def interpret_results(self, request: InterpretationRequest) -> InterpretationResponse:
        """
        Generate comprehensive narrative interpretation of results.
        
        Args:
            request: InterpretationRequest containing results and evidence
            
        Returns:
            InterpretationResponse with narrative report
        """
        try:
            # Build the interpretation prompt
            prompt = self._build_interpretation_prompt(request)
            
            # Call LLM for interpretation
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert research analyst and academic writer specializing in statistical interpretation and narrative synthesis.",
                temperature=0.3,  # Moderate creativity for engaging narrative
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
        """Build the comprehensive interpretation prompt."""
        
        # Format statistical results for the prompt
        stats_summary = self._format_statistical_results(request.statistical_results)
        
        # Format curated evidence for the prompt
        evidence_summary = self._format_curated_evidence(request.curated_evidence)
        
        # Count total evidence pieces
        total_evidence = sum(len(evidence_list) for evidence_list in request.curated_evidence.values())
        
        prompt = f"""You are tasked with creating a comprehensive narrative interpretation that synthesizes statistical analysis results with curated evidence. This is the final stage of a breakthrough THIN Code-Generated Synthesis Architecture.

FRAMEWORK SPECIFICATION:
{request.framework_spec}

EXPERIMENT CONTEXT:
{request.experiment_context or "Not provided"}

STATISTICAL ANALYSIS RESULTS:
{stats_summary}

CURATED EVIDENCE ({total_evidence} pieces):
{evidence_summary}

TASK: Create a comprehensive narrative report that:

1. **EXECUTIVE SUMMARY** (150-200 words):
   - Synthesize the most important findings
   - State key conclusions clearly
   - Highlight practical implications

2. **STATISTICAL FINDINGS INTERPRETATION**:
   - Interpret descriptive statistics in context
   - Explain hypothesis test results and their significance
   - Discuss correlation patterns and their meaning
   - Address reliability findings and their implications
   - Connect statistical measures to framework dimensions

3. **EVIDENCE INTEGRATION**:
   - Weave curated evidence throughout the analysis
   - Use evidence to illustrate and support statistical findings
   - Highlight particularly compelling evidence pieces
   - Show how evidence validates or contextualizes the numbers

4. **KEY FINDINGS** (5-7 bullet points):
   - List the most significant discoveries
   - Combine statistical and evidence-based insights
   - Focus on actionable or theoretically important results

5. **METHODOLOGY NOTES**:
   - Acknowledge the post-computation evidence curation approach
   - Discuss sample characteristics and limitations
   - Note reliability assessments and their impact

6. **IMPLICATIONS AND CONCLUSIONS**:
   - Connect findings to the broader framework context
   - Discuss theoretical and practical implications
   - Suggest areas for future investigation

WRITING REQUIREMENTS:
- Academic tone but accessible language
- Integrate quantitative and qualitative insights seamlessly
- Use specific numbers and evidence quotes
- Maintain logical flow between sections
- Ensure conclusions are well-supported by both statistics and evidence
- Aim for 1000-2000 words total

RESPONSE FORMAT:
Structure your response with clear section headers. Begin with the Executive Summary, then proceed through each section systematically. Use evidence quotes and statistical values to support all major claims.

Generate the comprehensive narrative report now:"""

        return prompt
    
    def _format_statistical_results(self, statistical_results: Dict[str, Any]) -> str:
        """Format statistical results for inclusion in the prompt."""
        
        formatted_sections = []
        
        # Descriptive Statistics
        if 'descriptive_stats' in statistical_results:
            desc_stats = statistical_results['descriptive_stats']
            formatted_sections.append("DESCRIPTIVE STATISTICS:")
            
            for dimension, stats in desc_stats.items():
                if isinstance(stats, dict):
                    mean = stats.get('mean', 'N/A')
                    std = stats.get('std', 'N/A')
                    count = stats.get('count', 'N/A')
                    formatted_sections.append(f"  {dimension}: M={mean:.3f}, SD={std:.3f}, N={count}")
        
        # Hypothesis Tests
        if 'hypothesis_tests' in statistical_results:
            hyp_tests = statistical_results['hypothesis_tests']
            formatted_sections.append("\nHYPOTHESIS TESTS:")
            
            for hypothesis, results in hyp_tests.items():
                if isinstance(results, dict):
                    is_sig = results.get('is_significant_alpha_05', False)
                    p_val = results.get('p_value', 'N/A')
                    status = "SIGNIFICANT" if is_sig else "Not significant"
                    formatted_sections.append(f"  {hypothesis}: {status} (p={p_val})")
        
        # Correlations
        if 'correlations' in statistical_results:
            formatted_sections.append("\nCORRELATIONS:")
            correlations = statistical_results['correlations']
            
            if 'overall_virtue_vs_overall_vice' in correlations:
                overall_corr = correlations['overall_virtue_vs_overall_vice']
                if isinstance(overall_corr, dict):
                    corr_val = overall_corr.get('correlation', 'N/A')
                    formatted_sections.append(f"  Virtue-Vice Overall: r={corr_val}")
        
        # Reliability
        if 'reliability_metrics' in statistical_results:
            rel_metrics = statistical_results['reliability_metrics']
            formatted_sections.append("\nRELIABILITY:")
            
            for cluster, metrics in rel_metrics.items():
                if isinstance(metrics, dict):
                    alpha = metrics.get('alpha', 'N/A')
                    meets_threshold = metrics.get('meets_threshold', False)
                    status = "Acceptable" if meets_threshold else "Below threshold"
                    formatted_sections.append(f"  {cluster}: α={alpha:.3f} ({status})")
        
        return "\n".join(formatted_sections)
    
    def _format_curated_evidence(self, curated_evidence: Dict[str, List[Any]]) -> str:
        """Format curated evidence for inclusion in the prompt."""
        
        formatted_sections = []
        
        for category, evidence_list in curated_evidence.items():
            if evidence_list:
                formatted_sections.append(f"\n{category.upper().replace('_', ' ')}:")
                
                for i, evidence in enumerate(evidence_list[:3], 1):  # Limit to top 3 per category
                    # Handle both dataclass and dict evidence formats
                    if hasattr(evidence, 'evidence_text'):
                        text = evidence.evidence_text
                        dimension = evidence.dimension
                        confidence = evidence.confidence
                        connection = evidence.statistical_connection
                    else:
                        text = evidence.get('evidence_text', 'N/A')
                        dimension = evidence.get('dimension', 'N/A')
                        confidence = evidence.get('confidence', 'N/A')
                        connection = evidence.get('statistical_connection', 'N/A')
                    
                    formatted_sections.append(f"  {i}. [{dimension.title()}] \"{text}\"")
                    formatted_sections.append(f"     Confidence: {confidence:.2f} | Connection: {connection}")
        
        return "\n".join(formatted_sections) if formatted_sections else "No curated evidence available."
    
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
                temperature=0.2,
                max_tokens=300
            )
            
            return response_content if metadata.get('success') else "Executive summary generation failed."
            
        except Exception as e:
            self.logger.error(f"Executive summary generation failed: {str(e)}")
            return f"Executive summary generation failed: {str(e)}" 