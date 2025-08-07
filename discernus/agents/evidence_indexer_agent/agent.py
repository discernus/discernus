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
            
            # BATCH PROCESSING: Get all summaries and keywords in one LLM call
            summaries_and_keywords = self._get_all_summaries_and_keywords_batch(evidence_list)
            
            # Create index entries using batch results
            index_entries = []
            for i, evidence_item in enumerate(evidence_list):
                summary, keywords = summaries_and_keywords[i] if i < len(summaries_and_keywords) else (evidence_item.get('quote_text', '')[:150], [])
                
                index_entries.append({
                    "id": f"evd_{hashlib.sha1(str(evidence_item).encode()).hexdigest()[:10]}",
                    "d": evidence_item.get('document_name', ''),
                    "dim": evidence_item.get('dimension', ''),
                    "sum": summary,
                    "key": keywords,
                    "original_quote_hash": f"sha256:{hashlib.sha256(evidence_item.get('quote_text', '').encode()).hexdigest()}"
                })
            
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

    def _get_all_summaries_and_keywords_batch(self, evidence_list: List[Dict[str, Any]]) -> List[tuple]:
        """
        Process all evidence quotes in a single LLM call (THIN approach).
        
        Returns:
            List of (summary, keywords) tuples, one per evidence item
        """
        if not evidence_list:
            return []
            
        try:
            # Prepare batch prompt with all quotes
            quotes_section = ""
            for i, evidence_item in enumerate(evidence_list):
                quote_text = evidence_item.get('quote_text', '')[:500]  # Truncate very long quotes
                quotes_section += f"\nQuote {i+1}: \"{quote_text}\"\n"
            
            prompt = f"""You are an expert in semantic analysis. For each of the {len(evidence_list)} quotes below, provide a concise one-sentence summary (max 150 characters) and up to 3 keywords that capture its core meaning.

{quotes_section}

Respond with a JSON array where each element corresponds to the quote number:
[
    {{"summary": "...", "keywords": ["...", "...", "..."]}},
    {{"summary": "...", "keywords": ["...", "...", "..."]}},
    ...
]
"""
            
            # Single LLM call for all evidence
            response_content, _ = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                max_tokens=200,  # Keep existing limit for simple classification task
                json_mode=True
            )
            
            response_array = json.loads(response_content)
            
            # Extract (summary, keywords) tuples
            results = []
            for item in response_array:
                if isinstance(item, dict):
                    summary = item.get("summary", "Summary not available.")
                    keywords = item.get("keywords", [])
                    results.append((summary, keywords))
                else:
                    results.append(("Summary not available.", []))
                    
            # Ensure we have results for all evidence items
            while len(results) < len(evidence_list):
                quote_text = evidence_list[len(results)].get('quote_text', '')
                results.append((quote_text[:150], []))
                
            return results
            
        except Exception as e:
            self.logger.warning(f"Batch processing failed: {e}. Using fallback.")
            # Fallback: return truncated quotes as summaries
            return [(evidence_item.get('quote_text', '')[:150], []) for evidence_item in evidence_list]


