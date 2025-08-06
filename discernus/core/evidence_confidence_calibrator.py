#!/usr/bin/env python3
"""
Evidence Confidence Calibrator - THIN Implementation

Addresses systematic under-calibration while maintaining accuracy.
Improves evidence confidence distribution for academic validation.
"""

import json
import logging
import time
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


@dataclass
class ConfidenceAssessment:
    """Structured confidence assessment result."""
    confidence: float
    reasoning: str
    quality_indicators: Dict[str, Any]
    calibration_factors: Dict[str, float]
    academic_validation: Dict[str, Any]


@dataclass
class ConfidenceCalibrationRequest:
    """Request for confidence calibration."""
    evidence_text: str
    context: str
    dimension: str
    score: float
    original_confidence: float
    framework_spec: str
    document_name: str


@dataclass
class ConfidenceCalibrationResponse:
    """Response containing calibrated confidence assessment."""
    assessment: ConfidenceAssessment
    calibration_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None


class EvidenceConfidenceCalibrator:
    """
    Calibrates evidence confidence scores for academic validation.
    
    Addresses systematic under-calibration while maintaining accuracy.
    Uses THIN approach: delegates calibration intelligence to LLM.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash-lite",
                 audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.agent_name = "EvidenceConfidenceCalibrator"
        self.audit_logger = audit_logger
        
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load externalized YAML calibration guidance
        self.calibration_guidance = self._load_calibration_guidance()
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "model": model,
                    "architecture": "thin_confidence_calibration",
                    "capabilities": ["confidence_assessment", "academic_validation", "quality_calibration"]
                }
            )
    
    def _load_calibration_guidance(self) -> str:
        """Load externalized YAML calibration guidance."""
        import os
        import yaml
        
        # Find calibration guidance in core directory
        core_dir = os.path.dirname(__file__)
        guidance_path = os.path.join(core_dir, 'confidence_calibration_guidance.yaml')
        
        if not os.path.exists(guidance_path):
            # Create default calibration guidance
            self._create_default_calibration_guidance(guidance_path)
        
        # Load calibration guidance
        with open(guidance_path, 'r') as f:
            guidance_content = f.read()
            guidance_data = yaml.safe_load(guidance_content)
        
        if 'guidance' not in guidance_data:
            raise ValueError(f"Calibration guidance file missing 'guidance' key: {guidance_path}")
        
        return guidance_data['guidance']
    
    def _create_default_calibration_guidance(self, guidance_path: str):
        """Create default THIN confidence calibration guidance."""
        import yaml
        
        default_guidance = {
            'guidance': '''
CONFIDENCE CALIBRATION GUIDANCE FOR ACADEMIC VALIDATION

HIGH CONFIDENCE (0.8-1.0):
- Direct textual support with unambiguous meaning
- Multiple reinforcing evidence points
- Clear logical connection to analytical dimension
- Strong contextual alignment with framework concepts
- Minimal interpretive elements

MEDIUM CONFIDENCE (0.6-0.8):
- Strong textual support with minor interpretive elements
- Clear evidence with some contextual dependency
- Good alignment with framework concepts
- Moderate interpretive elements
- Some contextual uncertainty

LOW CONFIDENCE (0.0-0.6):
- Weak or indirect textual support
- Highly interpretive or context-dependent
- Limited alignment with framework concepts
- Significant interpretive elements
- High contextual uncertainty

CALIBRATION FACTORS:
- Textual Clarity: 0.3 weight
- Contextual Alignment: 0.3 weight
- Framework Relevance: 0.2 weight
- Interpretive Complexity: 0.2 weight

ACADEMIC VALIDATION CRITERIA:
- Publication Quality: Evidence supports peer review
- Replicability: Clear reasoning for confidence level
- Transparency: Explicit confidence factors
- Research Standards: Meets academic publication requirements
'''
        }
        
        with open(guidance_path, 'w') as f:
            yaml.dump(default_guidance, f, default_flow_style=False)
    
    def assess_confidence(self, request: ConfidenceCalibrationRequest) -> ConfidenceCalibrationResponse:
        """
        Enhanced confidence assessment with calibration guidance.
        
        THIN approach: Delegates calibration intelligence to LLM.
        """
        start_time = time.time()
        
        try:
            # Create calibration prompt
            calibration_prompt = self._create_calibration_prompt(request)
            
            # Delegate calibration to LLM (THIN approach)
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=calibration_prompt,
                max_tokens=2000  # Allow comprehensive calibration
            )
            
            # Parse LLM calibration response
            assessment = self._parse_calibration_response(response_content, request)
            
            calibration_time = time.time() - start_time
            
            # Log confidence calibration
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "confidence_calibration",
                    {
                        "document": request.document_name,
                        "dimension": request.dimension,
                        "original_confidence": request.original_confidence,
                        "calibrated_confidence": assessment.confidence,
                        "calibration_time": calibration_time,
                        "success": True
                    }
                )
            
            # Generate calibration summary
            calibration_summary = self._generate_calibration_summary(
                request, assessment, calibration_time
            )
            
            return ConfidenceCalibrationResponse(
                assessment=assessment,
                calibration_summary=calibration_summary,
                success=True
            )
            
        except Exception as e:
            calibration_time = time.time() - start_time
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "confidence_calibration_error",
                    {
                        "document": request.document_name,
                        "calibration_time": calibration_time,
                        "error": str(e)
                    }
                )
            
            return ConfidenceCalibrationResponse(
                assessment=ConfidenceAssessment(
                    confidence=request.original_confidence,
                    reasoning="Calibration failed, using original confidence",
                    quality_indicators={},
                    calibration_factors={},
                    academic_validation={}
                ),
                calibration_summary={},
                success=False,
                error_message=str(e)
            )
    
    def _create_calibration_prompt(self, request: ConfidenceCalibrationRequest) -> str:
        """Create calibration prompt with guidance."""
        return f"""
You are calibrating evidence confidence for academic validation.

CALIBRATION GUIDANCE:
{self.calibration_guidance}

EVIDENCE TO CALIBRATE:
- Text: "{request.evidence_text}"
- Context: "{request.context}"
- Dimension: "{request.dimension}"
- Score: {request.score}
- Original Confidence: {request.original_confidence}

FRAMEWORK SPECIFICATION:
{request.framework_spec}

DOCUMENT: {request.document_name}

TASK:
Assess the confidence of this evidence using the calibration guidance.
Provide a calibrated confidence score with detailed reasoning.

REQUIRED OUTPUT FORMAT:
{{
    "confidence": 0.85,
    "reasoning": "Clear explanation of confidence level",
    "quality_indicators": {{
        "textual_clarity": 0.9,
        "contextual_alignment": 0.8,
        "framework_relevance": 0.85,
        "interpretive_complexity": 0.2
    }},
    "calibration_factors": {{
        "textual_clarity_weight": 0.3,
        "contextual_alignment_weight": 0.3,
        "framework_relevance_weight": 0.2,
        "interpretive_complexity_weight": 0.2
    }},
    "academic_validation": {{
        "publication_quality": true,
        "replicability": "Clear reasoning provided",
        "transparency": "Explicit factors shown",
        "research_standards": "Meets academic requirements"
    }}
}}

Return only valid JSON. Focus on academic standards and research credibility.
"""
    
    def _parse_calibration_response(self, response_content: str, request: ConfidenceCalibrationRequest) -> ConfidenceAssessment:
        """Parse LLM calibration response into structured assessment."""
        try:
            # Extract JSON from response
            if '```json' in response_content:
                json_start = response_content.find('```json') + 7
                json_end = response_content.find('```', json_start)
                if json_end != -1:
                    json_content = response_content[json_start:json_end].strip()
                    calibration_data = json.loads(json_content)
                else:
                    calibration_data = json.loads(response_content)
            else:
                calibration_data = json.loads(response_content)
            
            # Create structured assessment
            assessment = ConfidenceAssessment(
                confidence=float(calibration_data.get('confidence', request.original_confidence)),
                reasoning=calibration_data.get('reasoning', 'No reasoning provided'),
                quality_indicators=calibration_data.get('quality_indicators', {}),
                calibration_factors=calibration_data.get('calibration_factors', {}),
                academic_validation=calibration_data.get('academic_validation', {})
            )
            
            return assessment
            
        except Exception as e:
            logging.error(f"Failed to parse calibration response: {str(e)}")
            # Return fallback assessment
            return ConfidenceAssessment(
                confidence=request.original_confidence,
                reasoning="Calibration parsing failed, using original confidence",
                quality_indicators={},
                calibration_factors={},
                academic_validation={}
            )
    
    def _generate_calibration_summary(self, request: ConfidenceCalibrationRequest, 
                                    assessment: ConfidenceAssessment, 
                                    calibration_time: float) -> Dict[str, Any]:
        """Generate summary of confidence calibration."""
        confidence_change = assessment.confidence - request.original_confidence
        
        return {
            "original_confidence": request.original_confidence,
            "calibrated_confidence": assessment.confidence,
            "confidence_change": confidence_change,
            "calibration_time_seconds": calibration_time,
            "quality_indicators": assessment.quality_indicators,
            "academic_validation": assessment.academic_validation,
            "calibration_success": True
        }
    
    def batch_calibrate_confidence(self, requests: list[ConfidenceCalibrationRequest]) -> list[ConfidenceCalibrationResponse]:
        """Batch calibrate multiple evidence confidence assessments."""
        responses = []
        
        for request in requests:
            response = self.assess_confidence(request)
            responses.append(response)
        
        return responses
    
    def analyze_confidence_distribution(self, responses: list[ConfidenceCalibrationResponse]) -> Dict[str, Any]:
        """Analyze confidence distribution across batch calibration."""
        if not responses:
            return {"error": "No responses to analyze"}
        
        confidences = [response.assessment.confidence for response in responses if response.success]
        
        if not confidences:
            return {"error": "No successful calibrations"}
        
        high_confidence = sum(1 for c in confidences if c >= 0.8)
        medium_confidence = sum(1 for c in confidences if 0.6 <= c < 0.8)
        low_confidence = sum(1 for c in confidences if c < 0.6)
        
        total = len(confidences)
        
        return {
            "total_evidence": total,
            "high_confidence_count": high_confidence,
            "medium_confidence_count": medium_confidence,
            "low_confidence_count": low_confidence,
            "high_confidence_percentage": (high_confidence / total * 100) if total > 0 else 0,
            "medium_confidence_percentage": (medium_confidence / total * 100) if total > 0 else 0,
            "low_confidence_percentage": (low_confidence / total * 100) if total > 0 else 0,
            "average_confidence": sum(confidences) / len(confidences),
            "confidence_range": {"min": min(confidences), "max": max(confidences)}
        } 