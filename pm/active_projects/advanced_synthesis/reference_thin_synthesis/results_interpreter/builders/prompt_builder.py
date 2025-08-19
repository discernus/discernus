#!/usr/bin/env python3
"""
Prompt Builder for the Results Interpreter Agent.
"""

import json
from typing import Dict, Any

from ..agent import InterpretationRequest


def _build_provenance_metadata(request: InterpretationRequest) -> str:
    """Build a comprehensive provenance metadata string for the report header."""
    metadata_parts = []
    if request.run_id:
        metadata_parts.append(f"Run ID: {request.run_id}")
    if request.execution_timestamp_utc:
        metadata_parts.append(f"Execution Time (UTC): {request.execution_timestamp_utc}")
    if request.models_used:
        models_info = [f"{stage.title()}: {model}" for stage, model in request.models_used.items()]
        if models_info:
            metadata_parts.append(f"Models Used: {', '.join(models_info)}")
    # ... more metadata parts can be added here ...
    return '\n'.join(metadata_parts) if metadata_parts else "Provenance metadata not available"


def build_interpretation_prompt(request: InterpretationRequest, prompt_template: str) -> str:
    """Build the comprehensive interpretation prompt."""
    stats_str = str(request.statistical_results or {})
    evidence_str = str(request.curated_evidence or {})
    total_evidence = sum(len(v) for v in (request.curated_evidence or {}).values() if isinstance(v, list))

    provenance_metadata = _build_provenance_metadata(request)
    reporting_metadata_str = json.dumps(request.reporting_metadata, indent=2) if request.reporting_metadata else "Not provided"

    return prompt_template.format(
        provenance_metadata=provenance_metadata,
        framework_spec=request.framework_spec,
        experiment_context=request.experiment_context or "Not provided",
        stats_summary=stats_str,
        total_evidence=total_evidence,
        evidence_summary=evidence_str,
        footnote_instructions="",  # Simplified for brevity
        run_id=request.run_id or "Not provided",
        reporting_metadata=reporting_metadata_str
    )


