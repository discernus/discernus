#!/usr/bin/env python3
"""
Grounding Evidence Generator - THIN Implementation

Automatically generates "Score Grounding Evidence" for every numerical score,
providing immediate academic validation through clear score-to-evidence mapping.

THIN Principles:
- LLM provides grounding intelligence
- Software provides coordination and data flow
- Framework-agnostic grounding generation
- Durable infrastructure
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from discernus.core.evidence_confidence_calibrator import EvidenceConfidenceCalibrator, ConfidenceCalibrationRequest


@dataclass
class GroundingEvidence:
    """Structure for score grounding evidence."""
    document_id: str
    dimension: str
    score: float
    score_confidence: float
    grounding_evidence: Dict[str, Any]
    evidence_hash: str
    generation_timestamp: str


@dataclass
class GroundingEvidenceRequest:
    """Request for grounding evidence generation."""
    analysis_scores: Dict[str, Any]  # Raw analysis scores from Intelligent Extractor
    evidence_data: bytes  # Evidence data from analysis
    framework_spec: str
    document_name: str
    min_confidence_threshold: float = 0.6


@dataclass
class GroundingEvidenceResponse:
    """Response containing grounding evidence for all scores."""
    grounding_evidence: List[GroundingEvidence]
    generation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert to JSON-serializable format for artifact storage."""
        return {
            'grounding_evidence': [asdict(evidence) for evidence in self.grounding_evidence],
            'generation_summary': self.generation_summary,
            'success': self.success,
            'error_message': self.error_message
        }


class GroundingEvidenceGenerator:
    """
    THIN grounding evidence generator.
    
    Delegates grounding intelligence to LLM rather than building complex hardcoded logic.
    Provides automatic score-to-evidence mapping for academic validation.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash-lite",
                 audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.agent_name = "GroundingEvidenceGenerator"
        self.audit_logger = audit_logger
        
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load externalized YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Initialize confidence calibrator
        self.confidence_calibrator = EvidenceConfidenceCalibrator(model=model, audit_logger=audit_logger)
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "model": model,
                    "architecture": "thin_grounding_generation",
                    "capabilities": ["score_grounding", "evidence_mapping", "academic_validation"]
                }
            )
    
    def _load_prompt_template(self) -> str:
        """Load externalized YAML prompt template."""
        import os
        import yaml
        
        # Find prompt.yaml in generator directory
        generator_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(generator_dir, 'grounding_prompt.yaml')
        
        if not os.path.exists(prompt_path):
            # Create default prompt template
            self._create_default_prompt_template(prompt_path)
        
        # Load prompt template
        with open(prompt_path, 'r') as f:
            prompt_content = f.read()
            prompt_data = yaml.safe_load(prompt_content)
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")
        
        return prompt_data['template']
    
    def _create_default_prompt_template(self, prompt_path: str):
        """Create default THIN grounding evidence prompt template."""
        import yaml
        
        default_prompt = {
            'template': '''
You are generating grounding evidence for numerical scores from computational social science research.

ANALYSIS SCORES:
{analysis_scores}

EVIDENCE DATA:
{evidence_data}

FRAMEWORK SPECIFICATION:
{framework_spec}

DOCUMENT: {document_name}

TASK:
Generate grounding evidence for every numerical score. Each score must have:
1. **Primary Evidence**: Key supporting text from the document
2. **Context**: Broader context around the evidence
3. **Reasoning**: Clear explanation of how evidence supports the score
4. **Confidence**: Evidence quality assessment (0.0-1.0)

GROUNDING EVIDENCE STRUCTURE:
For each score, create:
{{
    "document_id": "{document_name}",
    "dimension": "score_dimension_name",
    "score": 0.75,
    "score_confidence": 0.8,
    "grounding_evidence": {{
        "primary_quote": "key supporting text",
        "context": "broader context around the quote",
        "evidence_confidence": 0.8,
        "reasoning": "clear explanation of how evidence supports score",
        "validation_type": "direct_textual_support"
    }}
}}

Return a JSON array of grounding evidence for all scores.
Be specific and actionable. Focus on academic standards and research credibility.
'''
        }
        
        with open(prompt_path, 'w') as f:
            yaml.dump(default_prompt, f, default_flow_style=False)
    
    def generate_grounding_evidence(self, request: GroundingEvidenceRequest) -> GroundingEvidenceResponse:
        """
        THIN: Delegate grounding evidence generation to LLM intelligence.
        
        Generates grounding evidence for every numerical score to address 95.6% evidence loss.
        """
        start_time = time.time()
        
        try:
            # Parse analysis scores to extract numerical scores
            numerical_scores = self._extract_numerical_scores(request.analysis_scores)
            
            if not numerical_scores:
                return GroundingEvidenceResponse(
                    grounding_evidence=[],
                    generation_summary={"warning": "No numerical scores found"},
                    success=True
                )
            
            # Create grounding prompt
            grounding_prompt = self.prompt_template.format(
                analysis_scores=json.dumps(numerical_scores, indent=2),
                evidence_data=str(request.evidence_data)[:2000],  # Limit context size
                framework_spec=request.framework_spec,
                document_name=request.document_name
            )
            
            # Delegate grounding generation to LLM (THIN approach)
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=grounding_prompt,
                max_tokens=4000  # Allow comprehensive grounding generation
            )
            
            # Parse LLM grounding response
            grounding_evidence_list = self._parse_grounding_response(response_content, request.document_name)
            
            # Apply confidence calibration to grounding evidence
            calibrated_evidence_list = self._calibrate_grounding_confidence(
                grounding_evidence_list, request
            )
            
            generation_time = time.time() - start_time
            
            # Log grounding generation
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "grounding_generation",
                    {
                        "document": request.document_name,
                        "scores_grounded": len(grounding_evidence_list),
                        "generation_time": generation_time,
                        "success": True
                    }
                )
            
            # Generate summary
            generation_summary = self._generate_grounding_summary(
                grounding_evidence_list, 
                len(numerical_scores),
                generation_time
            )
            
            return GroundingEvidenceResponse(
                grounding_evidence=calibrated_evidence_list,
                generation_summary=generation_summary,
                success=True
            )
            
        except Exception as e:
            generation_time = time.time() - start_time
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "grounding_generation_error",
                    {
                        "document": request.document_name,
                        "generation_time": generation_time,
                        "error": str(e)
                    }
                )
            
            return GroundingEvidenceResponse(
                grounding_evidence=[],
                generation_summary={},
                success=False,
                error_message=str(e)
            )
    
    def _extract_numerical_scores(self, analysis_scores: Dict[str, Any]) -> Dict[str, float]:
        """Extract numerical scores from analysis results."""
        numerical_scores = {}
        
        # Handle different analysis score structures
        if isinstance(analysis_scores, dict):
            for key, value in analysis_scores.items():
                if isinstance(value, (int, float)):
                    numerical_scores[key] = float(value)
                elif isinstance(value, dict):
                    # Handle nested score structures
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            numerical_scores[f"{key}_{sub_key}"] = float(sub_value)
        
        return numerical_scores
    
    def _parse_grounding_response(self, response_content: str, document_name: str) -> List[GroundingEvidence]:
        """Parse LLM grounding response into structured grounding evidence."""
        try:
            # Extract JSON from response
            if '```json' in response_content:
                json_start = response_content.find('```json') + 7
                json_end = response_content.find('```', json_start)
                if json_end != -1:
                    json_content = response_content[json_start:json_end].strip()
                    grounding_data = json.loads(json_content)
                else:
                    grounding_data = json.loads(response_content)
            else:
                grounding_data = json.loads(response_content)
            
            # Convert to GroundingEvidence objects
            grounding_evidence_list = []
            for item in grounding_data:
                # Create evidence hash
                evidence_hash = self._create_evidence_hash(
                    item.get('grounding_evidence', {}).get('primary_quote', ''),
                    document_name,
                    item.get('dimension', '')
                )
                
                grounding_evidence = GroundingEvidence(
                    document_id=item.get('document_id', document_name),
                    dimension=item.get('dimension', ''),
                    score=float(item.get('score', 0.0)),
                    score_confidence=float(item.get('score_confidence', 0.0)),
                    grounding_evidence=item.get('grounding_evidence', {}),
                    evidence_hash=evidence_hash,
                    generation_timestamp=time.strftime('%Y-%m-%dT%H:%M:%SZ')
                )
                
                grounding_evidence_list.append(grounding_evidence)
            
            return grounding_evidence_list
            
        except Exception as e:
            logging.error(f"Failed to parse grounding response: {str(e)}")
            return []
    
    def _create_evidence_hash(self, evidence_text: str, document_name: str, dimension: str) -> str:
        """Create a hash for evidence verification."""
        import hashlib
        content = f"{document_name}:{dimension}:{evidence_text}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    
    def _calibrate_grounding_confidence(self, grounding_evidence_list: List[GroundingEvidence], 
                                       request: GroundingEvidenceRequest) -> List[GroundingEvidence]:
        """Apply confidence calibration to grounding evidence."""
        calibrated_evidence = []
        
        for evidence in grounding_evidence_list:
            # Create confidence calibration request
            calibration_request = ConfidenceCalibrationRequest(
                evidence_text=evidence.grounding_evidence.get('primary_quote', ''),
                context=evidence.grounding_evidence.get('context', ''),
                dimension=evidence.dimension,
                score=evidence.score,
                original_confidence=evidence.grounding_evidence.get('evidence_confidence', 0.5),
                framework_spec=request.framework_spec,
                document_name=request.document_name
            )
            
            # Calibrate confidence
            calibration_response = self.confidence_calibrator.assess_confidence(calibration_request)
            
            if calibration_response.success:
                # Update grounding evidence with calibrated confidence
                evidence.grounding_evidence['evidence_confidence'] = calibration_response.assessment.confidence
                evidence.grounding_evidence['confidence_reasoning'] = calibration_response.assessment.reasoning
                evidence.grounding_evidence['quality_indicators'] = calibration_response.assessment.quality_indicators
                evidence.grounding_evidence['academic_validation'] = calibration_response.assessment.academic_validation
            
            calibrated_evidence.append(evidence)
        
        return calibrated_evidence
    
    def _generate_grounding_summary(self, grounding_evidence: List[GroundingEvidence], 
                                   total_scores: int, generation_time: float) -> Dict[str, Any]:
        """Generate summary of grounding evidence generation."""
        return {
            "total_scores": total_scores,
            "grounded_scores": len(grounding_evidence),
            "coverage_percentage": (len(grounding_evidence) / total_scores * 100) if total_scores > 0 else 0,
            "generation_time_seconds": generation_time,
            "average_evidence_confidence": sum(
                evidence.grounding_evidence.get('evidence_confidence', 0.0) 
                for evidence in grounding_evidence
            ) / len(grounding_evidence) if grounding_evidence else 0.0,
            "high_confidence_evidence": sum(
                1 for evidence in grounding_evidence 
                if evidence.grounding_evidence.get('evidence_confidence', 0.0) >= 0.8
            )
        } 