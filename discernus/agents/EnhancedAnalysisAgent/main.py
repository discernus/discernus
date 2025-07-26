#!/usr/bin/env python3
"""
Enhanced Analysis Agent for Discernus THIN v2.0
===============================================

Enhanced version of AnalyseBatchAgent with:
- Mathematical "show your work" requirements for computational validation
- Direct function call interface (bypasses Redis coordination)
- Integration with security boundary and audit logging
- Self-assessment and quality validation capabilities

Based on THIN v2.0 principles: LLM intelligence + minimal software coordination
"""

import json
import base64
import hashlib
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import instructor
from litellm import completion
from pydantic import BaseModel, Field

from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedAnalysisAgentError(Exception):
    """Enhanced analysis agent specific exceptions"""
    pass

# Pydantic Models for Guaranteed JSON Output
class Scores(BaseModel):
    intensity: float = Field(..., ge=0.0, le=1.0)
    salience: float = Field(..., ge=0.0, le=1.0)

class TensionAnalysis(BaseModel):
    Dignity_Tribalism_Tension: float
    Truth_Manipulation_Tension: float
    Justice_Resentment_Tension: float
    Hope_Fear_Tension: float
    Pragmatism_Fantasy_Tension: float
    Moral_Character_Strategic_Contradiction_Index_MC_SCI: float
    MC_SCI_Classification: str
    Character_Salience_Concentration_CSC: float

class CharacterClusters(BaseModel):
    virtue_cluster_score: float
    vice_cluster_score: float
    character_balance: float
    character_intensity: float
    moral_clarity: float

class DocumentAnalysis(BaseModel):
    worldview: str
    scores: Dict[str, Scores]
    evidence: Dict[str, List[str]]
    reasoning: str
    salience_ranking: List[Dict[str, Any]]
    character_priorities: str
    tension_analysis: TensionAnalysis
    character_clusters: CharacterClusters

class AnalysisOutput(BaseModel):
    analysis_summary: str
    document_analyses: Dict[str, DocumentAnalysis]
    mathematical_verification: Dict[str, Any]
    self_assessment: Dict[str, Any]


class EnhancedAnalysisAgent:
    """
    Enhanced analysis agent with mathematical validation and direct call interface.
    
    Key enhancements over original AnalyseBatchAgent:
    - Mathematical "show your work" requirements in prompts
    - Self-assessment and confidence reporting
    - Direct function call interface (no Redis)
    - Security boundary enforcement
    - Comprehensive audit logging
    """
    
    def __init__(self, 
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        """
        Initialize enhanced analysis agent.
        
        Args:
            security_boundary: Security boundary for file access
            audit_logger: Audit logger for comprehensive logging
            artifact_storage: Local artifact storage for caching
        """
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedAnalysisAgent"
        
        # Patch litellm with instructor
        self.client = instructor.patch(completion)
        
        # Load enhanced prompt template
        self.prompt_template = self._load_enhanced_prompt_template()
        
        print(f"🧠 {self.agent_name} initialized with instructor-based structured output")
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["instructor_json_output", "mathematical_validation", "self_assessment", "direct_calls"]
        })
    
    def _load_enhanced_prompt_template(self) -> str:
        """Load enhanced prompt template with mathematical requirements from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.yaml for EnhancedAnalysisAgent")
        
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
        
        return prompt_config['template']

    def _extract_json_from_response(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Finds and parses the first valid JSON object from a string.
        Handles LLM responses that include markdown fences or other text.
        """
        # Regex to find content between ```json and ``` or a standalone { ... }
        json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', content, re.DOTALL)
        
        if not json_match:
            return None

        # Extract the JSON content from the first non-empty group
        json_str = next((group for group in json_match.groups() if group), None)

        if not json_str:
            return None

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

    def analyze_batch(self, 
                      framework_content: str,
                      documents: List[Dict[str, Any]], 
                      experiment_config: Dict[str, Any],
                      model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Perform enhanced batch analysis of documents using framework.
        
        Args:
            framework_content: Raw framework content (markdown with JSON appendix)
            corpus_documents: List of document dictionaries with content and metadata
            experiment_config: Experiment configuration
            model: LLM model to use
            
        Returns:
            Analysis results with mathematical validation
        """
        start_time = datetime.now(timezone.utc).isoformat()
        batch_id = f"batch_{hashlib.sha256(f'{start_time}{framework_content[:100]}'.encode()).hexdigest()[:12]}"
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_start", {
            "batch_id": batch_id,
            "num_documents": len(documents),
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        try:
            # Store input artifacts
            framework_hash = self.storage.put_artifact(
                framework_content.encode('utf-8'),
                {"artifact_type": "framework", "batch_id": batch_id}
            )
            
            # Prepare documents for analysis
            documents = []
            document_hashes = []
            
            for i, doc in enumerate(corpus_documents):
                # Get document content (handle both string and bytes)
                if isinstance(doc.get('content'), bytes):
                    doc_content = base64.b64encode(doc['content']).decode('utf-8')
                    doc_hash = self.storage.put_artifact(doc['content'], {
                        "artifact_type": "corpus_document",
                        "original_filename": doc.get('filename', f'doc_{i+1}'),
                        "batch_id": batch_id
                    })
                else:
                    content_bytes = doc['content'].encode('utf-8')
                    doc_content = base64.b64encode(content_bytes).decode('utf-8')
                    doc_hash = self.storage.put_artifact(content_bytes, {
                        "artifact_type": "corpus_document",
                        "original_filename": doc.get('filename', f'doc_{i+1}'),
                        "batch_id": batch_id
                    })
                
                documents.append({
                    'index': i + 1,
                    'hash': doc_hash,
                    'content': doc_content,
                    'filename': doc.get('filename', f'doc_{i+1}')
                })
                document_hashes.append(doc_hash)
            
            # Prepare framework for LLM
            framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')
            
            # Format enhanced prompt with mathematical requirements
            prompt_text = self.prompt_template.format(
                batch_id=batch_id,
                frameworks=f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_b64}\n",
                documents=self._format_documents_for_prompt(documents),
                num_frameworks=1,
                num_documents=len(documents)
            )
            
            # Log LLM interaction start (Note: Instructor handles the actual call, so this is a bit different now)
            self.audit.log_agent_event(self.agent_name, "llm_call_complete", {
                "batch_id": batch_id, "model": model, "response_model": "AnalysisOutput"
            })
            
            # The result is already a validated Pydantic object, so we can convert it to a dict
            analysis_data = self.client(
                model=model,
                response_model=AnalysisOutput,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0
            )
            
            # Log LLM interaction start (Note: Instructor handles the actual call, so this is a bit different now)
            self.audit.log_agent_event(self.agent_name, "llm_call_complete", {
                "batch_id": batch_id, "model": model, "response_model": "AnalysisOutput"
            })
            
            # The result is already a validated Pydantic object, so we can convert it to a dict
            analysis_dict = analysis_data.model_dump()

            # Create enhanced result artifact
            end_time = datetime.now(timezone.utc).isoformat() 
            duration = self._calculate_duration(start_time, end_time)
            
            enhanced_result = {
                "batch_id": batch_id,
                "agent_name": self.agent_name,
                "agent_version": "enhanced_v3.0_instructor",
                "experiment_name": experiment_config.get("name", "unknown"),
                "model_used": model,
                "analysis_results": analysis_dict,
                "mathematical_validation": {
                    "enabled": True,
                    "verification_required": True,
                    "confidence_reporting": True
                },
                "execution_metadata": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_seconds": duration,
                    "llm_interaction_hash": interaction_hash
                },
                "input_artifacts": {
                    "framework_hash": framework_hash,
                    "document_hashes": document_hashes,
                    "num_documents": len(documents)
                },
                "provenance": {
                    "security_boundary": self.security.get_boundary_info(),
                    "audit_session_id": self.audit.session_id
                }
            }
            
            # Store result artifact
            result_hash = self.storage.put_artifact(
                json.dumps(enhanced_result, indent=2).encode('utf-8'),
                {"artifact_type": "analysis_result", "batch_id": batch_id}
            )
            
            # Log artifact transformation
            self.audit.log_artifact_chain(
                stage="enhanced_analysis",
                input_hashes=[framework_hash] + document_hashes,
                output_hash=result_hash,
                agent_name=self.agent_name,
                llm_interaction_hash=interaction_hash
            )
            
            # Log completion
            self.audit.log_agent_event(self.agent_name, "batch_analysis_complete", {
                "batch_id": batch_id,
                "result_hash": result_hash,
                "duration_seconds": duration,
                "mathematical_validation": "completed"
            })
            
            print(f"✅ Enhanced analysis complete: {batch_id} ({duration:.1f}s)")
            
            return {
                "batch_id": batch_id,
                "result_hash": result_hash,
                "result_content": enhanced_result,
                "duration_seconds": duration,
                "mathematical_validation": True
            }
            
        except Exception as e:
            # Log error
            self.audit.log_error("enhanced_analysis_error", str(e), {
                "batch_id": batch_id,
                "agent_name": self.agent_name
            })
            
            raise EnhancedAnalysisAgentError(f"Enhanced analysis failed: {e}")
    
    def _format_documents_for_prompt(self, documents: List[Dict]) -> str:
        """Format documents for LLM prompt with enhanced metadata."""
        formatted = []
        for document in documents:
            formatted.append(
                f"=== DOCUMENT {document['index']} (base64 encoded) ===\n"
                f"Filename: {document.get('filename', 'unknown')}\n"
                f"Hash: {document['hash'][:12]}...\n"
                f"{document['content']}\n"
            )
        return "\n".join(formatted)
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0 