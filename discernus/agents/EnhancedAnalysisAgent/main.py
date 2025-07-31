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
from litellm import completion
from litellm.cost_calculator import completion_cost

from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedAnalysisAgentError(Exception):
    """Enhanced analysis agent specific exceptions"""
    pass


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
        
        # Load enhanced prompt template
        self.prompt_template = self._load_enhanced_prompt_template()
        
        print(f"🧠 {self.agent_name} initialized with mathematical validation")
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["mathematical_validation", "self_assessment", "direct_calls"]
        })
    
    def _load_enhanced_prompt_template(self) -> str:
        """Load enhanced prompt template with mathematical requirements from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.yaml for EnhancedAnalysisAgent")
        
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
        
        return prompt_config['template']
    
    def _load_json_prompt_template(self) -> str:
        """Load v6.0 JSON prompt template for frameworks with separation of concerns."""
        prompt_path = Path(__file__).parent / "prompt_v6.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt_v6.yaml for EnhancedAnalysisAgent")
        
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
        
        return prompt_config['template']
    

    
    def _process_json_response(self, result_content: str, document_hash: str, 
                              current_scores_hash: Optional[str], 
                              current_evidence_hash: Optional[str]) -> Tuple[str, str]:
        """
        Fully THIN approach: Store complete raw LLM response as artifact.
        Let downstream synthesis pipeline handle ALL parsing and interpretation.
        """
        # Store the complete raw LLM response as artifact (fully THIN principle)
        raw_response_hash = self.storage.put_artifact(
            result_content.encode('utf-8'),
            {
                "artifact_type": "raw_analysis_response_v6",
                "document_hash": document_hash,
                "framework_version": "v6.0",
                "framework_hash": self.analysis_provenance.get("framework_hash", "unknown")
            }
        )
        
        self.audit.log_agent_event(self.agent_name, "raw_response_stored", {
            "document_hash": document_hash,
            "response_artifact_hash": raw_response_hash,
            "response_length": len(result_content),
            "approach": "fully_thin_raw_storage"
        })
        
        # Return raw response hash as both scores and evidence for v6.0 pipeline
        return raw_response_hash, raw_response_hash



    def analyze_batch(self, 
                     framework_content: str,
                     corpus_documents: List[Dict[str, Any]], 
                     experiment_config: Dict[str, Any],
                     model: str = "vertex_ai/gemini-2.5-flash",
                     current_scores_hash: Optional[str] = None,
                     current_evidence_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform enhanced batch analysis of documents using framework.
        
        Args:
            framework_content: Raw framework content (markdown with JSON appendix)
            corpus_documents: List of document dictionaries with content and metadata
            experiment_config: Experiment configuration
            model: LLM model to use
            current_scores_hash: Hash of the current scores.csv artifact
            current_evidence_hash: Hash of the current evidence.csv artifact
            
        Returns:
            Analysis results with mathematical validation and updated CSV artifact hashes
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Calculate framework hash for provenance tracking (Issue #208)
        framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
        
        # Calculate corpus hash for complete provenance
        corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) for doc in corpus_documents])
        corpus_hash = hashlib.sha256(corpus_content.encode('utf-8')).hexdigest()
        
        # Store provenance context for artifact metadata
        self.analysis_provenance = {
            "framework_hash": framework_hash,
            "corpus_hash": corpus_hash,
            "analysis_model": model,
            "analysis_timestamp": start_time,
            "agent_name": self.agent_name
        }
        
        # Create deterministic batch_id for perfect caching (THIN principle)
        # Hash based on framework + document contents only, not timestamp
        doc_content_hash = hashlib.sha256(corpus_content.encode()).hexdigest()[:16]
        batch_id = f"batch_{hashlib.sha256(f'{framework_content}{doc_content_hash}'.encode()).hexdigest()[:12]}"
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_start", {
            "batch_id": batch_id,
            "num_documents": len(corpus_documents),
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        try:
            # THIN approach: No framework parsing - let LLM handle framework interpretation
            # Framework content will be passed directly to LLM via YAML prompt
            
            # Check if analysis result is already cached (THIN perfect caching)
            # Create the same result structure we would store to check if it exists
            analysis_cache_key = f"analysis_{batch_id}"
            
            # Try to find existing analysis result in artifact registry
            for artifact_hash, artifact_info in self.storage.registry.items():
                if (artifact_info.get("metadata", {}).get("artifact_type") == "analysis_result" and
                    artifact_info.get("metadata", {}).get("batch_id") == batch_id):
                    
                    # Cache hit! Return the cached analysis result
                    print(f"💾 Cache hit for analysis: {batch_id}")
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_result = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(self.agent_name, "cache_hit", {
                        "batch_id": batch_id,
                        "cached_artifact_hash": artifact_hash
                    })

                    # THIN approach: Process cached result without framework parsing
                    document_hashes = cached_result.get('input_artifacts', {}).get('document_hashes', [])
                    
                    # Process cached response (THIN approach - no framework version detection)
                    new_scores_hash, new_evidence_hash = self._process_json_response(
                        cached_result['raw_analysis_response'], 
                        document_hashes[0] if document_hashes else "unknown_artifact",
                        current_scores_hash, 
                        current_evidence_hash
                    )
                    
                    return {
                        "analysis_result": {
                            "batch_id": batch_id,
                            "result_hash": artifact_hash,
                            "result_content": cached_result,
                            "duration_seconds": 0.0,  # Instant cache hit
                            "mathematical_validation": True,
                            "cached": True
                        },
                        "scores_hash": new_scores_hash,
                        "evidence_hash": new_evidence_hash
                    }
            
            # No cache hit - proceed with analysis
            print(f"🔍 No cache hit for {batch_id} - performing analysis...")
            
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
            
            # THIN approach: Always use JSON prompt template, no framework version detection
            framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')
            
            # Load JSON prompt template (only v6.0+ supported)
            json_prompt_template = self._load_json_prompt_template()
            
            # Format prompt with framework and documents
            prompt_text = json_prompt_template.format(
                batch_id=batch_id,
                frameworks=f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_b64}\n",
                documents=self._format_documents_for_prompt(documents),
                num_frameworks=1,
                num_documents=len(documents)
            )
            
            self.audit.log_agent_event(self.agent_name, "prompt_prepared", {
                "prompt_length": len(prompt_text),
                "approach": "thin_no_parsing"
            })
            
            # Log LLM interaction start
            self.audit.log_agent_event(self.agent_name, "llm_call_start", {
                "batch_id": batch_id,
                "model": model,
                "prompt_length": len(prompt_text),
                "mathematical_validation": True
            })
            
            # Call LLM with enhanced mathematical validation prompt
            # Removed temperature setting per Issue #211 debugging - let LLM use default
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Extract and validate response
            if not response or not response.choices:
                raise EnhancedAnalysisAgentError("LLM returned empty response")
            
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                raise EnhancedAnalysisAgentError("LLM returned empty content")
            
            # Extract cost and usage information from LLM response
            try:
                # Get usage data from response
                usage_obj = getattr(response, 'usage', None)
                prompt_tokens = getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0
                completion_tokens = getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0
                total_tokens = getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0
                
                # Calculate cost using LiteLLM's cost calculator
                response_cost = 0.0
                try:
                    response_cost = completion_cost(completion_response=response)
                except Exception as cost_err:
                    print(f"⚠️ Could not calculate cost: {cost_err}")
                    response_cost = 0.0
                
                # Log cost information to audit system
                self.audit.log_cost(
                    operation="individual_document_analysis",
                    model=model,
                    tokens_used=total_tokens,
                    cost_usd=response_cost,
                    agent_name=self.agent_name,
                    metadata={
                        "document_hash": document_hashes[0] if document_hashes else "unknown",
                        "batch_id": batch_id,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens
                    }
                )
                
                print(f"💰 Document analysis cost: ${response_cost:.6f} ({total_tokens:,} tokens)")
                
            except Exception as e:
                print(f"⚠️ Error extracting cost information: {e}")
                # Continue processing even if cost extraction fails
            
            # THIN approach: Always process as raw response (no framework version detection)
            self.audit.log_agent_event(self.agent_name, "processing_raw_response", {
                "response_length": len(result_content),
                "approach": "thin_raw_storage"
            })
            
            # Process raw LLM response (THIN approach)
            new_scores_hash, new_evidence_hash = self._process_json_response(
                result_content, document_hashes[0], current_scores_hash, current_evidence_hash
            )

            # Store raw LLM response - let synthesis agent handle any format (THIN principle)
            analysis_data = result_content

            # Log LLM interaction
            interaction_hash = self.audit.log_llm_interaction(
                model=model,
                prompt=prompt_text,
                response=result_content,
                agent_name=self.agent_name,
                metadata={
                    "batch_id": batch_id,
                    "mathematical_validation": True,
                    "tokens_input": len(prompt_text.split()),
                    "tokens_output": len(result_content.split())
                }
            )
            
            # Create enhanced result artifact
            end_time = datetime.now(timezone.utc).isoformat() 
            duration = self._calculate_duration(start_time, end_time)
            
            enhanced_result = {
                "batch_id": batch_id,
                "agent_name": self.agent_name,
                "agent_version": "enhanced_v2.1_raw_output",
                "experiment_name": experiment_config.get("name", "unknown"),
                "model_used": model,
                "raw_analysis_response": analysis_data,  # Raw LLM response - no parsing
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
                "analysis_result": {
                    "batch_id": batch_id,
                    "result_hash": result_hash,
                    "result_content": enhanced_result,
                    "duration_seconds": duration,
                    "mathematical_validation": True
                },
                "scores_hash": new_scores_hash,
                "evidence_hash": new_evidence_hash
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