#!/usr/bin/env python3
"""
Validator for the Results Interpreter Agent.
"""

from typing import Optional

from ..agent import InterpretationRequest


def validate_required_data(request: InterpretationRequest) -> Optional[str]:
    """
    Minimal THIN validation - just ensure we have data to work with.
    """
    if not request.statistical_results:
        return "No statistical results provided"
    if not request.curated_evidence:
        return "No curated evidence provided"
    if not request.framework_spec or not request.framework_spec.strip():
        return "No framework specification provided"
    return None


