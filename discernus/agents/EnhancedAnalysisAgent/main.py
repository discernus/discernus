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
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from litellm import completion
from litellm.cost_calculator import completion_cost

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
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.yaml for EnhancedAnalysisAgent")
        with open(prompt_path, 'r') as f:
            return yaml.safe_load(f)['template']

    def analyze_batch(self,
                     framework_content: str,
                     corpus_documents: List[Dict[str, Any]],
                     experiment_config: Dict[str, Any],
                     model: str = "vertex_ai/gemini-2.5-flash",
                     current_scores_hash: Optional[str] = None,
                     current_evidence_hash: Optional[str] = None) -> Dict[str, Any]:
        """Performs enhanced batch analysis of documents."""
        start_time = datetime.now(timezone.utc).isoformat()
        framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
        corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) for doc in corpus_documents])
        doc_content_hash = hashlib.sha256(corpus_content.encode()).hexdigest()[:16]
        batch_id = f"batch_{hashlib.sha256(f'{framework_content}{doc_content_hash}{model}'.encode()).hexdigest()[:12]}"

        self.audit.log_agent_event(self.agent_name, "batch_analysis_start", {
            "batch_id": batch_id, "num_documents": len(corpus_documents), "model": model
        })

        cached_result = self.cache.check_cache(batch_id)
        if cached_result:
            document_hashes = cached_result.get('input_artifacts', {}).get('document_hashes', [])
            new_scores_hash, new_evidence_hash = process_json_response(
                cached_result['raw_analysis_response'],
                document_hashes[0] if document_hashes else "unknown_artifact",
                self.storage, self.audit, self.agent_name, {}
            )
            # BUGFIX: Include result_hash for cache hits to match counting logic expectations
            result_hash = self.storage.put_artifact(
                json.dumps(cached_result, indent=2).encode('utf-8'),
                {"artifact_type": "analysis_result", "batch_id": batch_id, "cached": True}
            )
            return {
                "analysis_result": {"batch_id": batch_id, "result_hash": result_hash, "result_content": cached_result, "cached": True},
                "scores_hash": new_scores_hash, "evidence_hash": new_evidence_hash
            }

        documents, document_hashes = self._prepare_documents(corpus_documents, batch_id)
        prompt_text = create_analysis_prompt(self.prompt_template, batch_id, framework_content, documents)
        self.audit.log_agent_event(self.agent_name, "prompt_prepared", {"prompt_length": len(prompt_text)})

        response = self._execute_llm_call(model, prompt_text, batch_id)
        result_content = response.choices[0].message.content

        analysis_provenance = {"framework_hash": framework_hash}
        new_scores_hash, new_evidence_hash = process_json_response(
            result_content, document_hashes[0], self.storage, self.audit, self.agent_name, analysis_provenance
        )

        duration = self._calculate_duration(start_time, datetime.now(timezone.utc).isoformat())
        enhanced_result = self._create_enhanced_result(
            batch_id, model, result_content, new_evidence_hash, start_time, duration,
            framework_hash, document_hashes, experiment_config
        )
        result_hash = self.storage.put_artifact(
            json.dumps(enhanced_result, indent=2).encode('utf-8'),
            {"artifact_type": "analysis_result", "batch_id": batch_id}
        )

        return {
            "analysis_result": {"batch_id": batch_id, "result_hash": result_hash, "duration_seconds": duration},
            "scores_hash": new_scores_hash, "evidence_hash": new_evidence_hash
        }

    def _prepare_documents(self, corpus_documents: List[Dict[str, Any]], batch_id: str) -> tuple[List[Dict[str, Any]], List[str]]:
        """Prepares documents for analysis and returns them along with their hashes."""
        documents, document_hashes = [], []
        for i, doc in enumerate(corpus_documents):
            content_bytes = doc['content'] if isinstance(doc.get('content'), bytes) else str(doc.get('content', '')).encode('utf-8')
            doc_hash = self.storage.put_artifact(content_bytes, {
                "artifact_type": "corpus_document", "original_filename": doc.get('filename', f'doc_{i+1}'), "batch_id": batch_id
            })
            documents.append({
                'index': i + 1, 'hash': doc_hash, 'content': base64.b64encode(content_bytes).decode('utf-8'),
                'filename': doc.get('filename', f'doc_{i+1}')
            })
            document_hashes.append(doc_hash)
        return documents, document_hashes

    def _execute_llm_call(self, model: str, prompt_text: str, batch_id: str) -> Any:
        """Executes the LLM call and handles the response."""
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {"batch_id": batch_id, "model": model})
        completion_params = {"model": model, "messages": [{"role": "user", "content": prompt_text}]}
        if model.startswith("vertex_ai/"):
            completion_params["safety_settings"] = [
                {"category": f"HARM_CATEGORY_{cat}", "threshold": "BLOCK_NONE"}
                for cat in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
            ]
        response = completion(**completion_params)
        if not response or not response.choices or not response.choices[0].message.content:
            raise EnhancedAnalysisAgentError("LLM returned empty response")
        self._log_llm_cost(response, model, batch_id)
        return response

    def _log_llm_cost(self, response: Any, model: str, batch_id: str):
        """Logs the cost of the LLM call."""
        try:
            cost = completion_cost(completion_response=response)
            usage = getattr(response, 'usage', None)
            total_tokens = getattr(usage, 'total_tokens', 0) if usage else 0
            self.audit.log_cost("individual_document_analysis", model, total_tokens, cost, self.agent_name, {"batch_id": batch_id})
        except Exception as e:
            self.audit.log_error("cost_calculation_error", str(e), {"agent": self.agent_name})

    def _create_enhanced_result(self, batch_id, model, analysis_data, evidence_hash, start_time, duration, framework_hash, document_hashes, experiment_config):
        """Creates the final enhanced result dictionary."""
        return {
            "batch_id": batch_id,
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