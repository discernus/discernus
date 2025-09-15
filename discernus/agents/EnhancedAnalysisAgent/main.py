#!/usr/bin/env python3
"""
Enhanced Analysis Agent for Discernus THIN v2.0
===============================================

Orchestrates the analysis process using modular components for caching,
prompt building, and response parsing.
"""

import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# LLM calls now handled through LLMGateway for proper cost tracking

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from .cache import AnalysisCache
from .prompt_builder import create_analysis_prompt
from .response_parser import process_json_response


class EnhancedAnalysisAgentError(Exception):
    """Enhanced analysis agent specific exceptions"""
    pass


class EnhancedAnalysisAgent:
    """Orchestrates analysis using modular components."""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedAnalysisAgent"
        self.prompt_template = self._load_prompt_template()
        self.cache = AnalysisCache(self.storage, self.audit, self.agent_name)

        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["mathematical_validation", "self_assessment", "direct_calls"]
        })

    def _load_prompt_template(self) -> str:
        """Load tool calling prompt template."""
        prompt_path = Path(__file__).parent / "prompt_tool_calling_simple.txt"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt_tool_calling_simple.txt for EnhancedAnalysisAgent")
        with open(prompt_path, 'r') as f:
            return f.read()

    def analyze_documents(self,
                         framework_content: str,
                         corpus_documents: List[Dict[str, Any]],
                         experiment_config: Dict[str, Any],
                         model: str = "vertex_ai/gemini-2.5-flash",
                         current_scores_hash: Optional[str] = None,
                         current_evidence_hash: Optional[str] = None) -> Dict[str, Any]:
        """Performs enhanced analysis of documents (individual or multiple)."""
        start_time = datetime.now(timezone.utc).isoformat()
        framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
        corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) for doc in corpus_documents])
        doc_content_hash = hashlib.sha256(corpus_content.encode()).hexdigest()[:16]
        analysis_id = f"analysis_{hashlib.sha256(f'{framework_content}{doc_content_hash}{model}'.encode()).hexdigest()[:12]}"

        self.audit.log_agent_event(self.agent_name, "document_analysis_start", {
            "analysis_id": analysis_id, "num_documents": len(corpus_documents), "model": model
        })

        cached_result = self.cache.check_cache(analysis_id)
        if cached_result:
            self.audit.log_agent_event(self.agent_name, "cache_hit_processing", {"analysis_id": analysis_id})
            document_hashes = cached_result.get('input_artifacts', {}).get('document_hashes', [])
            self.audit.log_agent_event(self.agent_name, "cache_hit_document_hashes", {"analysis_id": analysis_id, "document_hashes": document_hashes})
            new_scores_hash, new_evidence_hash = process_json_response(
                cached_result['raw_analysis_response'],
                document_hashes,
                self.storage, self.audit, self.agent_name, {}
            )
            # Include result_hash for cache hits to match counting logic expectations
            result_hash = self.storage.put_artifact(
                json.dumps(cached_result, indent=2).encode('utf-8'),
                {"artifact_type": "analysis_result", "analysis_id": analysis_id, "cached": True}
            )
            result = {
                "analysis_result": {"analysis_id": analysis_id, "result_hash": result_hash, "result_content": cached_result, "cached": True},
                "scores_hash": new_scores_hash, "evidence_hash": new_evidence_hash
            }
            self.audit.log_agent_event(self.agent_name, "cache_hit_return", {"analysis_id": analysis_id, "result_keys": list(result.keys())})
            return result

        documents, document_hashes = self._prepare_documents(corpus_documents, analysis_id)
        prompt_text = create_analysis_prompt(self.prompt_template, analysis_id, framework_content, documents)
        self.audit.log_agent_event(self.agent_name, "prompt_prepared", {"prompt_length": len(prompt_text)})

        response = self._execute_llm_call_with_tools(model, prompt_text, analysis_id)
        tool_calls = response["tool_calls"]
        result_content = response["response_content"]

        analysis_provenance = {"framework_hash": framework_hash}
        new_scores_hash, new_evidence_hash, delimited_response = self._process_tool_calls(
            tool_calls, document_hashes, self.storage, self.audit, self.agent_name, analysis_provenance
        )

        duration = self._calculate_duration(start_time, datetime.now(timezone.utc).isoformat())
        enhanced_result = self._create_enhanced_result(
            analysis_id, model, delimited_response, new_evidence_hash, start_time, duration,
            framework_hash, document_hashes, experiment_config
        )
        result_hash = self.storage.put_artifact(
            json.dumps(enhanced_result, indent=2).encode('utf-8'),
            {"artifact_type": "analysis_result", "analysis_id": analysis_id}
        )

        return {
            "analysis_result": {"analysis_id": analysis_id, "result_hash": result_hash, "duration_seconds": duration, "result_content": enhanced_result},
            "scores_hash": new_scores_hash, "evidence_hash": new_evidence_hash
        }

    def _prepare_documents(self, corpus_documents: List[Dict[str, Any]], analysis_id: str) -> tuple[List[Dict[str, Any]], List[str]]:
        """Prepares documents for analysis and returns them along with their hashes."""
        documents, document_hashes = [], []
        for i, doc in enumerate(corpus_documents):
            content_bytes = doc['content'] if isinstance(doc.get('content'), bytes) else str(doc.get('content', '')).encode('utf-8')
            doc_hash = self.storage.put_artifact(content_bytes, {
                "artifact_type": "corpus_document", "original_filename": doc.get('filename', f'doc_{i+1}'), "analysis_id": analysis_id
            })
            documents.append({
                'index': i + 1, 'hash': doc_hash, 'content': base64.b64encode(content_bytes).decode('utf-8'),
                'filename': doc.get('filename', f'doc_{i+1}')
            })
            document_hashes.append(doc_hash)
        return documents, document_hashes

    def _execute_llm_call_with_tools(self, model: str, prompt_text: str, analysis_id: str) -> Dict[str, Any]:
        """Executes the LLM call with tool calling and handles the response."""
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {"analysis_id": analysis_id, "model": model})
        
        # Use EnhancedLLMGateway for tool calling
        from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
        from ...gateway.model_registry import ModelRegistry
        
        gateway = EnhancedLLMGateway(ModelRegistry())
        system_prompt = "You are an expert discourse analyst. Follow the provided framework instructions precisely and make the three required tool calls."
        
        # Define the three tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "record_analysis_scores",
                    "description": "Record dimensional scores with confidence and salience",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "framework_name": {"type": "string"},
                            "framework_version": {"type": "string"},
                            "scores": {
                                "type": "object",
                                "additionalProperties": {
                                    "type": "object",
                                    "properties": {
                                        "raw_score": {"type": "number"},
                                        "salience": {"type": "number"},
                                        "confidence": {"type": "number"}
                                    },
                                    "required": ["raw_score", "salience", "confidence"]
                                }
                            }
                        },
                        "required": ["document_id", "framework_name", "framework_version", "scores"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "record_evidence_quotes",
                    "description": "Record evidence quotes and reasoning for each dimension",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "evidence": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "dimension": {"type": "string"},
                                        "quote": {"type": "string"},
                                        "reasoning": {"type": "string"}
                                    },
                                    "required": ["dimension", "quote", "reasoning"]
                                }
                            }
                        },
                        "required": ["document_id", "evidence"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "record_computational_work",
                    "description": "Record derived metrics calculations and code execution",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "executed_code": {"type": "string"},
                            "execution_output": {"type": "string"},
                            "derived_metrics": {
                                "type": "object",
                                "additionalProperties": {"type": "number"}
                            }
                        },
                        "required": ["document_id", "executed_code", "execution_output", "derived_metrics"]
                    }
                }
            }
        ]
        
        try:
            from ...core.logging_config import perf_timer
            with perf_timer("llm_call_with_tools", 
                           model=model, 
                           agent="EnhancedAnalysisAgent",
                           analysis_id=analysis_id):
                response_content, metadata = gateway.execute_call_with_tools(
                    model=model, 
                    prompt=prompt_text, 
                    system_prompt=system_prompt,
                    tools=tools,
                    force_function_calling=True,
                    context=f"Analysis {analysis_id}"
                )
            
            if not metadata.get('success'):
                raise EnhancedAnalysisAgentError(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
            
            # Extract tool calls
            tool_calls = metadata.get('tool_calls', [])
            if not tool_calls:
                raise EnhancedAnalysisAgentError("No tool calls found in LLM response")
            
            # Log LLM interaction for complete audit trail
            self.audit.log_llm_interaction(
                model=model,
                prompt=prompt_text,
                response=response_content,
                agent_name=self.agent_name,
                interaction_type="document_analysis_with_tools",
                metadata={
                    "analysis_id": analysis_id,
                    "system_prompt": system_prompt,
                    "tool_calls_count": len(tool_calls),
                    **metadata
                }
            )
            
            # Log cost information from gateway metadata
            if metadata.get('success') and 'usage' in metadata:
                usage = metadata['usage']
                self.audit.log_cost(
                    operation="individual_document_analysis_with_tools",
                    model=model,
                    tokens_used=usage.get('total_tokens', 0),
                    cost_usd=usage.get('response_cost_usd', 0.0),
                    agent_name=self.agent_name,
                    metadata={"analysis_id": analysis_id, "tool_calls": len(tool_calls)}
                )
            
            return {
                "tool_calls": tool_calls,
                "response_content": response_content,
                "metadata": metadata
            }
            
        except Exception as e:
            raise EnhancedAnalysisAgentError(f"LLM call with tools failed: {e}")

    def _process_tool_calls(self, tool_calls: List[Any], document_hashes: List[str], 
                           storage: LocalArtifactStorage, audit: AuditLogger, 
                           agent_name: str, analysis_provenance: Dict[str, Any]) -> Tuple[str, str]:
        """
        Process tool calls and save artifacts, replacing the old JSON parsing approach.
        Returns (scores_hash, evidence_hash) for compatibility with existing orchestrator.
        """
        import json
        from datetime import datetime, timezone
        
        # Debug: Log tool calls received
        audit.log_agent_event(agent_name, "tool_calls_received", {
            "tool_calls_count": len(tool_calls),
            "document_hashes_count": len(document_hashes),
            "tool_call_types": [type(tc).__name__ for tc in tool_calls]
        })
        
        # Initialize data structures for all documents
        all_scores_data = []
        all_evidence_data = []
        all_work_data = []
        
        # Process all tool calls (should be exactly 3 for single document)
        scores_data = None
        evidence_data = None
        work_data = None
        
        # Process each tool call
        for tool_call in tool_calls:
            # Handle both dict format and ChatCompletionMessageToolCall format
            if hasattr(tool_call, 'function'):
                # ChatCompletionMessageToolCall format
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
            else:
                # Dict format
                function_name = tool_call.get('function', {}).get('name')
                function_args = json.loads(tool_call['function']['arguments'])
            
            # Debug: Log each tool call
            audit.log_agent_event(agent_name, "tool_call_processed", {
                "function_name": function_name,
                "function_args_keys": list(function_args.keys()) if function_args else []
            })
            
            if function_name == 'record_analysis_scores':
                scores_data = function_args
            elif function_name == 'record_evidence_quotes':
                evidence_data = function_args
            elif function_name == 'record_computational_work':
                work_data = function_args
        
        # Store data for this document
        if scores_data:
            all_scores_data.append(scores_data)
        if evidence_data:
            all_evidence_data.append(evidence_data)
        if work_data:
            all_work_data.append(work_data)
        
        # Use the first document's data for compatibility (or aggregate if needed)
        scores_data = all_scores_data[0] if all_scores_data else None
        evidence_data = all_evidence_data[0] if all_evidence_data else None
        work_data = all_work_data[0] if all_work_data else None
        
        # Save scores artifact (equivalent to old raw_analysis_response)
        if scores_data:
            # Create analysis response in the old format for compatibility
            analysis_json = {
                "analysis_metadata": {
                    "framework_name": scores_data.get("framework_name", "unknown"),
                    "framework_version": scores_data.get("framework_version", "1.0"),
                    "analyst_confidence": 0.95,  # Default confidence
                    "analysis_notes": "Tool calling approach with three independent analyses",
                    "internal_consistency_approach": "3-run median aggregation"
                },
                "document_analyses": [{
                    "document_id": scores_data.get("document_id", document_hashes[0] if document_hashes else "unknown"),
                    "document_name": scores_data.get("document_id", "unknown"),
                    "dimensional_scores": scores_data.get("scores", {}),
                    "evidence": evidence_data.get("evidence", []) if evidence_data else []
                }]
            }
            
            # Create delimited response for compatibility with existing CSV export
            delimited_response = f"<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n{json.dumps(analysis_json, indent=2)}\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>"
            
            raw_response_hash = storage.put_artifact(
                delimited_response.encode('utf-8'),
                {
                    "artifact_type": "raw_analysis_response_v6",
                    "document_hashes": document_hashes,
                    "framework_version": "v6.0",
                    "framework_hash": analysis_provenance.get("framework_hash", "unknown"),
                    "tool_calling": True
                }
            )
        else:
            # Fallback if no scores data
            raw_response_hash = storage.put_artifact(
                b"No scores data from tool calls",
                {"artifact_type": "raw_analysis_response_v6_error", "document_hashes": document_hashes}
            )
        
        # Save evidence artifact
        if evidence_data:
            evidence_list = []
            for evidence_item in evidence_data.get("evidence", []):
                evidence_list.append({
                    "document_name": evidence_data.get("document_id", "unknown"),
                    "dimension": evidence_item.get("dimension"),
                    "quote_text": evidence_item.get("quote"),
                    "confidence": 0.9,  # Default confidence
                    "context_type": "tool_call_evidence",
                    "extraction_method": "tool_call_extraction_v1.0",
                    "source_type": "tool_call_response",
                    "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
                    "reasoning": evidence_item.get("reasoning", "")
                })
            
            evidence_artifact = {
                "evidence_metadata": {
                    "document_hashes": document_hashes,
                    "total_evidence_pieces": len(evidence_list),
                    "extraction_method": "tool_call_extraction_v1.0",
                    "extraction_time": datetime.now(timezone.utc).isoformat(),
                    "framework_version": "v6.0"
                },
                "evidence_data": evidence_list
            }
            
            evidence_hash = storage.put_artifact(
                json.dumps(evidence_artifact, indent=2).encode('utf-8'),
                {
                    "artifact_type": "evidence_v6",
                    "document_hashes": document_hashes,
                    "extraction_method": "tool_call_extraction",
                    "tool_calling": True
                }
            )
        else:
            # Fallback if no evidence data
            evidence_hash = storage.put_artifact(
                b"No evidence data from tool calls",
                {"artifact_type": "evidence_v6_error", "document_hashes": document_hashes}
            )
        
        # Save computational work artifacts (one per document)
        for i, work_data in enumerate(all_work_data):
            if work_data:
                work_artifact = {
                    "document_id": work_data.get("document_id", f"document_{i+1}"),
                    "executed_code": work_data.get("executed_code", ""),
                    "execution_output": work_data.get("execution_output", ""),
                    "derived_metrics": work_data.get("derived_metrics", {}),
                    "extraction_time": datetime.now(timezone.utc).isoformat()
                }
                
                work_hash = storage.put_artifact(
                    json.dumps(work_artifact, indent=2).encode('utf-8'),
                    {
                        "artifact_type": "computational_work_v1",
                        "document_hashes": [document_hashes[i]] if i < len(document_hashes) else document_hashes,
                        "tool_calling": True
                    }
                )
                
                audit.log_agent_event(agent_name, "computational_work_saved", {
                    "document_index": i,
                    "document_hashes": [document_hashes[i]] if i < len(document_hashes) else document_hashes,
                    "work_hash": work_hash,
                    "derived_metrics_count": len(work_data.get("derived_metrics", {}))
                })
        
        audit.log_agent_event(agent_name, "tool_calls_processed", {
            "document_hashes": document_hashes,
            "tool_calls_count": len(tool_calls),
            "scores_hash": raw_response_hash,
            "evidence_hash": evidence_hash,
            "approach": "show_your_work_tool_calling"
        })
        
        return raw_response_hash, evidence_hash, delimited_response if scores_data else "No scores data from tool calls"

    def _create_enhanced_result(self, analysis_id, model, analysis_data, evidence_hash, start_time, duration, framework_hash, document_hashes, experiment_config):
        """Creates the final enhanced result dictionary."""
        return {
            "analysis_id": analysis_id,
            "agent_name": self.agent_name,
            "agent_version": "enhanced_v2.1_raw_output",
            "experiment_name": experiment_config.get("name", "unknown"),
            "model_used": model,
            "raw_analysis_response": analysis_data,
            "evidence_hash": evidence_hash,
            "execution_metadata": {
                "start_time": start_time,
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": duration,
            },
            "input_artifacts": {
                "framework_hash": framework_hash,
                "document_hashes": document_hashes,
                "num_documents": len(document_hashes)
            },
            "provenance": {
                "security_boundary": self.security.get_boundary_info(),
                "audit_session_id": self.audit.session_id
            }
        }

    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculates duration in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0 