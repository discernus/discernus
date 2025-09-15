#!/usr/bin/env python3
"""
Response Parser for the Enhanced Analysis Agent.

Handles parsing of LLM responses and extraction of evidence.
"""

import json
import re
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


def _extract_evidence_from_analysis_response(result_content: str, audit: AuditLogger, agent_name: str) -> List[Dict[str, Any]]:
    """
    Extract evidence from analysis response without LLM calls.
    This is deterministic text processing, not LLM interpretation.
    """
    # Extract JSON from delimited format
    json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
    json_match = re.search(json_pattern, result_content, re.DOTALL)

    if not json_match:
        return []

    try:
        analysis_data = json.loads(json_match.group(1).strip())
        document_analyses = analysis_data.get('document_analyses', [])

        evidence_list = []
        for doc_analysis in document_analyses:
            doc_name = doc_analysis.get('document_name', 'unknown')
            evidence_items = doc_analysis.get('evidence', [])

            for evidence in evidence_items:
                evidence_list.append({
                    "document_name": doc_name,
                    "dimension": evidence.get('dimension'),
                    "quote_text": evidence.get('quote_text'),
                    "confidence": evidence.get('confidence'),
                    "context_type": evidence.get('context_type'),
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response",
                    "extraction_timestamp": datetime.now(timezone.utc).isoformat()
                })
        return evidence_list
    except json.JSONDecodeError as e:
        audit.log_agent_event(agent_name, "evidence_extraction_failed", {
            "error": str(e),
            "response_length": len(result_content)
        })
        return []


def process_json_response(
    result_content: str,
    document_hashes: List[str],
    storage: LocalArtifactStorage,
    audit: AuditLogger,
    agent_name: str,
    analysis_provenance: Dict[str, Any],
) -> Tuple[str, str]:
    """
    THIN approach: Extract evidence during analysis time, not post-processing.
    This eliminates the need for LLM calls during evidence extraction.
    """
    # Replace placeholder document ID with the actual document hash
    # This is a critical fix for data integrity. The LLM is instructed to use
    # a placeholder, which we replace here with the content-addressable hash.

    json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
    json_match = re.search(json_pattern, result_content, re.DOTALL)

    if json_match:
        try:
            json_str = json_match.group(1).strip()
            analysis_data = json.loads(json_str)
            document_analyses = analysis_data.get('document_analyses', [])

            if len(document_analyses) == len(document_hashes):
                for i, doc_analysis in enumerate(document_analyses):
                    # Replace the placeholder with the actual document hash
                    if doc_analysis.get('document_id') == '[DOCUMENT_ID_PLACEHOLDER]':
                        doc_analysis['document_id'] = document_hashes[i]
                
                # Re-serialize the JSON with the correct document IDs
                updated_json_str = json.dumps(analysis_data, indent=2)
                result_content = result_content.replace(json_match.group(1).strip(), updated_json_str)

        except json.JSONDecodeError as e:
            # If JSON is malformed, we proceed with the original content
            pass
        except Exception as e:
            # Re-raise the exception so it bubbles up
            raise


    raw_response_hash = storage.put_artifact(
        result_content.encode('utf-8'),
        {
            "artifact_type": "raw_analysis_response_v6",
            "document_hashes": document_hashes,
            "framework_version": "v6.0",
            "framework_hash": analysis_provenance.get("framework_hash", "unknown")
        }
    )

    evidence_list = _extract_evidence_from_analysis_response(result_content, audit, agent_name)

    evidence_artifact = {
        "evidence_metadata": {
            "document_hashes": document_hashes,
            "total_evidence_pieces": len(evidence_list),
            "extraction_method": "analysis_time_extraction_v1.0",
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
            "extraction_method": "analysis_time_extraction"
        }
    )

    audit.log_agent_event(agent_name, "evidence_extracted", {
        "document_hashes": document_hashes,
        "evidence_pieces": len(evidence_list),
        "evidence_hash": evidence_hash,
        "approach": "thin_analysis_time_extraction"
    })

    return raw_response_hash, evidence_hash


