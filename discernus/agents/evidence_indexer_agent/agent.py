import pandas as pd
import json
import hashlib
import logging
import os
import sys
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Import LLM gateway from main codebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

@dataclass
class IndexingRequest:
    evidence_data: bytes
    model: str

@dataclass
class IndexingResponse:
    intelligent_index: bytes
    success: bool
    error_message: Optional[str] = None
    index_artifact_hash: Optional[str] = None

class EvidenceIndexerAgent:
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger

    def generate_index(self, request: IndexingRequest) -> IndexingResponse:
        try:
            # Parse JSON evidence data
            evidence_json = json.loads(request.evidence_data.decode('utf-8'))
            evidence_list = evidence_json.get('evidence_data', [])
            
            index_entries = [self._create_index_entry(evidence_item) for evidence_item in evidence_list]
            
            output_jsonl = "\n".join([json.dumps(entry) for entry in index_entries])
            
            return IndexingResponse(
                intelligent_index=output_jsonl.encode('utf-8'),
                success=True
            )
        except Exception as e:
            return IndexingResponse(
                intelligent_index=b"",
                success=False,
                error_message=str(e)
            )

    def _create_index_entry(self, evidence_item: Dict[str, Any]) -> Dict[str, Any]:
        quote_text = evidence_item.get('quote_text', '')
        
        summary, keywords = self._get_summary_and_keywords(quote_text, self.model)

        return {
            "id": f"evd_{hashlib.sha1(str(evidence_item).encode()).hexdigest()[:10]}",
            "d": evidence_item.get('document_name', ''),
            "dim": evidence_item.get('dimension', ''),
            "sum": summary,
            "key": keywords,
            "original_quote_hash": f"sha256:{hashlib.sha256(quote_text.encode()).hexdigest()}"
        }

    def _get_summary_and_keywords(self, quote_text: str, model: str) -> (str, List[str]):
        prompt = f"""
        You are an expert in semantic analysis. For the following quote, provide a concise one-sentence summary (max 150 characters) and up to 3 keywords that capture its core meaning.

        Quote: "{quote_text}"

        Respond in the following JSON format:
        {{
            "summary": "...",
            "keywords": ["...", "...", "..."]
        }}
        """
        
        try:
            response_content, _ = self.llm_gateway.execute_call(
                model=model,
                prompt=prompt,
                max_tokens=200,
                json_mode=True
            )
            
            response_json = json.loads(response_content)
            summary = response_json.get("summary", "Summary not available.")
            keywords = response_json.get("keywords", [])
            return summary, keywords
        except Exception as e:
            # Fallback in case of LLM failure
            return quote_text[:150], []


