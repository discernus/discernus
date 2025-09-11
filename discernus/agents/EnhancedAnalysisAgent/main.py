#!/usr/bin/env python3
"""
Enhanced Analysis Agent for Discernus THIN v2.0
===============================================

Orchestrates the analysis process using modular components for caching,
prompt building, and response parsing.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

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
        """Load prompt template."""
        prompt_path = Path(__file__).parent / "prompt.txt"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.txt for EnhancedAnalysisAgent")
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

        response = self._execute_llm_call(model, prompt_text, analysis_id)
        result_content = response.choices[0].message.content

        analysis_provenance = {"framework_hash": framework_hash}
        new_scores_hash, new_evidence_hash = process_json_response(
            result_content, document_hashes, self.storage, self.audit, self.agent_name, analysis_provenance
        )

        duration = self._calculate_duration(start_time, datetime.now(timezone.utc).isoformat())
        enhanced_result = self._create_enhanced_result(
            analysis_id, model, result_content, new_evidence_hash, start_time, duration,
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

    def _execute_llm_call(self, model: str, prompt_text: str, analysis_id: str) -> Any:
        """Executes the LLM call and handles the response."""
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {"analysis_id": analysis_id, "model": model})
        
        # Use LLMGateway for proper cost tracking instead of calling litellm directly
        from ...gateway.llm_gateway import LLMGateway
        from ...gateway.model_registry import ModelRegistry
        
        gateway = LLMGateway(ModelRegistry())
        system_prompt = "You are an expert discourse analyst. Follow the provided framework instructions precisely."
        
        try:
            from ...core.logging_config import perf_timer
            with perf_timer("llm_call", 
                           model=model, 
                           agent="EnhancedAnalysisAgent",
                           analysis_id=analysis_id):
                response_content, metadata = gateway.execute_call(
                    model=model, 
                    prompt=prompt_text, 
                    system_prompt=system_prompt
                )
            
            if not response_content or not response_content.strip():
                raise EnhancedAnalysisAgentError("LLM returned empty response")
            
            # Log LLM interaction for complete audit trail
            self.audit.log_llm_interaction(
                model=model,
                prompt=prompt_text,
                response=response_content,
                agent_name=self.agent_name,
                interaction_type="document_analysis",
                metadata={
                    "analysis_id": analysis_id,
                    "system_prompt": system_prompt,
                    **metadata
                }
            )
            
            # Log cost information from gateway metadata
            if metadata.get('success') and 'usage' in metadata:
                usage = metadata['usage']
                self.audit.log_cost(
                    operation="individual_document_analysis",
                    model=model,
                    tokens_used=usage.get('total_tokens', 0),
                    cost_usd=usage.get('response_cost_usd', 0.0),
                    agent_name=self.agent_name,
                    metadata={"analysis_id": analysis_id}
                )
            
            # Create a response-like object for compatibility with existing code
            class MockResponse:
                def __init__(self, content, usage_data):
                    self.choices = [MockChoice(content)]
                    self.usage = MockUsage(usage_data)
                    
            class MockChoice:
                def __init__(self, content):
                    self.message = MockMessage(content)
                    
            class MockMessage:
                def __init__(self, content):
                    self.content = content
                    
            class MockUsage:
                def __init__(self, usage_data):
                    self.total_tokens = usage_data.get('total_tokens', 0)
                    self.prompt_tokens = usage_data.get('prompt_tokens', 0)
                    self.completion_tokens = usage_data.get('completion_tokens', 0)
                    
            usage_data = metadata.get('usage', {})
            return MockResponse(response_content, usage_data)
            
        except Exception as e:
            raise EnhancedAnalysisAgentError(f"LLM call failed: {e}")



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