#!/usr/bin/env python3
"""
Score Validation Orchestrator - THIN Implementation

Delegates score validation intelligence to LLM rather than building complex validation logic.
Provides <5 minute academic validation workflow for any numerical score.

THIN Principles:
- LLM provides validation intelligence
- Software provides coordination and data flow
- Framework-agnostic validation
- Durable infrastructure
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


@dataclass
class ScoreValidationRequest:
    """Request for score validation."""
    document_name: str
    score_name: str
    score_value: float
    confidence: float
    framework_name: str
    analysis_artifact_path: str
    corpus_manifest_path: str


@dataclass
class ScoreValidationResult:
    """Result of score validation."""
    success: bool
    validation_time_seconds: float
    score_grounding: Dict[str, Any]
    evidence_quality: Dict[str, Any]
    academic_validation: Dict[str, Any]
    recommendations: List[str]
    error_message: Optional[str] = None


class ScoreValidationOrchestrator:
    """
    THIN score validation orchestrator.
    
    Delegates validation intelligence to LLM rather than building complex validation logic.
    Provides <5 minute academic validation workflow.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash-lite",
                 audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.agent_name = "ScoreValidationOrchestrator"
        self.audit_logger = audit_logger
        
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load externalized YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "model": model,
                    "architecture": "thin_score_validation",
                    "capabilities": ["score_grounding", "evidence_validation", "academic_validation"]
                }
            )
    
    def _load_prompt_template(self) -> str:
        """Load externalized YAML prompt template."""
        import os
        import yaml
        
        # Find prompt.yaml in orchestrator directory
        orchestrator_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(orchestrator_dir, 'score_validation_prompt.yaml')
        
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
        """Create default THIN score validation prompt template."""
        import yaml
        
        default_prompt = {
            'template': '''
You are validating a numerical score from computational social science research.

SCORE TO VALIDATE:
Document: {document_name}
Score: {score_name} = {score_value} (confidence: {confidence})
Framework: {framework_name}

ANALYSIS CONTEXT:
{analysis_context}

VALIDATION TASK:
Provide comprehensive academic validation for this score in <5 minutes:

1. **Score Grounding**: Verify the score has clear textual evidence
2. **Evidence Quality**: Assess the strength and relevance of supporting evidence  
3. **Academic Validation**: Evaluate research credibility and methodology
4. **Recommendations**: Suggest improvements if needed

RESPONSE FORMAT:
Return a JSON object with this structure:
{{
    "score_grounding": {{
        "evidence_found": true/false,
        "primary_evidence": "key supporting text",
        "evidence_context": "broader context",
        "grounding_strength": "strong/medium/weak"
    }},
    "evidence_quality": {{
        "relevance": "high/medium/low",
        "specificity": "high/medium/low", 
        "context_adequacy": "high/medium/low",
        "quality_score": 0.0-1.0
    }},
    "academic_validation": {{
        "methodology_sound": true/false,
        "transparency_adequate": true/false,
        "peer_review_ready": true/false,
        "validation_confidence": 0.0-1.0
    }},
    "recommendations": ["list", "of", "improvements"],
    "validation_summary": "Brief academic validation summary"
}}

Be specific and actionable. Focus on academic standards and research credibility.
'''
        }
        
        with open(prompt_path, 'w') as f:
            yaml.dump(default_prompt, f, default_flow_style=False)
    
    def validate_score(self, request: ScoreValidationRequest) -> ScoreValidationResult:
        """
        THIN: Delegate score validation to LLM intelligence.
        
        Provides <5 minute academic validation workflow.
        """
        start_time = time.time()
        
        try:
            # Load analysis context from artifact
            analysis_context = self._load_analysis_context(request.analysis_artifact_path)
            print(f"DEBUG: Analysis context loaded: {len(analysis_context)} characters")
            print(f"DEBUG: Context preview: {analysis_context[:200]}...")
            
            # Create validation prompt
            validation_prompt = self.prompt_template.format(
                document_name=request.document_name,
                score_name=request.score_name,
                score_value=request.score_value,
                confidence=request.confidence,
                framework_name=request.framework_name,
                analysis_context=analysis_context
            )
            
            # Delegate validation to LLM (THIN approach)
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=validation_prompt,
                temperature=0.1  # Low temperature for consistent validation
            )
            
            # Parse LLM validation response
            validation_data = self._parse_validation_response(response_content)
            
            validation_time = time.time() - start_time
            
            # Log validation attempt
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "score_validation",
                    {
                        "document": request.document_name,
                        "score": request.score_name,
                        "validation_time": validation_time,
                        "success": True
                    }
                )
            
            return ScoreValidationResult(
                success=True,
                validation_time_seconds=validation_time,
                score_grounding=validation_data.get("score_grounding", {}),
                evidence_quality=validation_data.get("evidence_quality", {}),
                academic_validation=validation_data.get("academic_validation", {}),
                recommendations=validation_data.get("recommendations", [])
            )
            
        except Exception as e:
            validation_time = time.time() - start_time
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "score_validation_error",
                    {
                        "document": request.document_name,
                        "score": request.score_name,
                        "validation_time": validation_time,
                        "error": str(e)
                    }
                )
            
            return ScoreValidationResult(
                success=False,
                validation_time_seconds=validation_time,
                score_grounding={},
                evidence_quality={},
                academic_validation={},
                recommendations=[],
                error_message=str(e)
            )
    
    def _load_analysis_context(self, analysis_artifact_path: str) -> str:
        """Load analysis context from artifact file."""
        try:
            # Convert symlink path to actual shared_cache path
            artifact_path = Path(analysis_artifact_path)
            if artifact_path.is_symlink():
                # Extract filename and use shared_cache path
                filename = artifact_path.name
                experiment_path = artifact_path.parent.parent.parent.parent  # Go up to experiment root
                actual_path = experiment_path / "shared_cache" / "artifacts" / filename
                analysis_artifact_path = str(actual_path)
            
            with open(analysis_artifact_path, 'r') as f:
                analysis_data = json.load(f)
            
            # Extract relevant analysis context for multi-document format
            if 'document_analyses' in analysis_data:
                # Find the specific document analysis
                for doc_analysis in analysis_data['document_analyses']:
                    if 'analysis_scores' in doc_analysis:
                        # Return the analysis scores and evidence for this document
                        context = {
                            'analysis_scores': doc_analysis['analysis_scores'],
                            'evidence': doc_analysis.get('evidence', [])
                        }
                        return json.dumps(context, indent=2)
            
            # Fallback for other formats
            if 'raw_analysis_log' in analysis_data:
                return analysis_data['raw_analysis_log'][:2000]  # Limit context size
            elif 'analysis_scores' in analysis_data:
                return json.dumps(analysis_data['analysis_scores'], indent=2)
            else:
                return str(analysis_data)
                
        except Exception as e:
            return f"Error loading analysis context: {str(e)}"
    
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM validation response."""
        try:
            # Extract JSON from response
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                if json_end != -1:
                    json_content = response[json_start:json_end].strip()
                    return json.loads(json_content)
                else:
                    return json.loads(response)
            else:
                return json.loads(response)
                
        except Exception as e:
            # Return minimal validation result on parsing error
            return {
                "score_grounding": {"evidence_found": False, "grounding_strength": "unknown"},
                "evidence_quality": {"quality_score": 0.0},
                "academic_validation": {"validation_confidence": 0.0},
                "recommendations": [f"Error parsing validation response: {str(e)}"]
            }
    
    def generate_validation_report(self, result: ScoreValidationResult, request: ScoreValidationRequest) -> str:
        """Generate academic validation report."""
        report = f"""# Score Validation Report

**Document**: {request.document_name}
**Score**: {request.score_name} = {request.score_value} (confidence: {request.confidence})
**Framework**: {request.framework_name}
**Validation Time**: {result.validation_time_seconds:.1f} seconds

## Score Grounding
- **Evidence Found**: {result.score_grounding.get('evidence_found', 'Unknown')}
- **Primary Evidence**: {result.score_grounding.get('primary_evidence', 'Not provided')}
- **Grounding Strength**: {result.score_grounding.get('grounding_strength', 'Unknown')}

## Evidence Quality
- **Relevance**: {result.evidence_quality.get('relevance', 'Unknown')}
- **Specificity**: {result.evidence_quality.get('specificity', 'Unknown')}
- **Quality Score**: {result.evidence_quality.get('quality_score', 0.0):.2f}

## Academic Validation
- **Methodology Sound**: {result.academic_validation.get('methodology_sound', False)}
- **Transparency Adequate**: {result.academic_validation.get('transparency_adequate', False)}
- **Peer Review Ready**: {result.academic_validation.get('peer_review_ready', False)}
- **Validation Confidence**: {result.academic_validation.get('validation_confidence', 0.0):.2f}

## Recommendations
{chr(10).join(f"- {rec}" for rec in result.recommendations)}

---
*Generated by Discernus Score Validation Pipeline (THIN Architecture)*
"""
        return report 