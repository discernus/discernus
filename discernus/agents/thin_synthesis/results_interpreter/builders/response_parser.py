#!/usr/bin/env python3
"""
Response Parser for the Results Interpreter Agent.
"""

from ..agent import InterpretationResponse


def parse_interpretation_response(response_content: str) -> InterpretationResponse:
    """ULTRA-THIN approach: LLM generates perfect report, no parsing needed."""
    word_count = len(response_content.split())

    return InterpretationResponse(
        narrative_report=response_content,
        executive_summary="",
        key_findings=[],
        methodology_notes="",
        statistical_summary={},
        evidence_integration_summary={},
        success=True,
        word_count=word_count
    )


