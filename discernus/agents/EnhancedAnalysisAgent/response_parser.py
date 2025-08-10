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
    document_hash: str,
    storage: LocalArtifactStorage,
    audit: AuditLogger,
    agent_name: str,
    analysis_provenance: Dict[str, Any],
) -> Tuple[str, str]:
    """
    THIN approach: Extract evidence during analysis time, not post-processing.
    This eliminates the need for LLM calls during evidence extraction.
    """
    raw_response_hash = storage.put_artifact(
        result_content.encode('utf-8'),
        {
            "artifact_type": "raw_analysis_response_v6",
            "document_hash": document_hash,
            "framework_version": "v6.0",
            "framework_hash": analysis_provenance.get("framework_hash", "unknown")
        }
    )

    evidence_list = _extract_evidence_from_analysis_response(result_content, audit, agent_name)

    evidence_artifact = {
        "evidence_metadata": {
            "document_hash": document_hash,
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
            "document_hash": document_hash,
            "extraction_method": "analysis_time_extraction"
        }
    )

    audit.log_agent_event(agent_name, "evidence_extracted", {
        "document_hash": document_hash,
        "evidence_pieces": len(evidence_list),
        "evidence_hash": evidence_hash,
        "approach": "thin_analysis_time_extraction"
    })

    return raw_response_hash, evidence_hash


