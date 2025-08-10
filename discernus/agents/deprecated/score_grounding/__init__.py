#!/usr/bin/env python3
"""
Score Grounding Package - THIN Implementation

Provides automatic grounding evidence generation for every numerical score.
Addresses 95.6% evidence loss through systematic score-to-evidence mapping.
"""

from .grounding_evidence_generator import (
    GroundingEvidenceGenerator,
    GroundingEvidenceRequest,
    GroundingEvidenceResponse,
    GroundingEvidence
)

__all__ = [
    'GroundingEvidenceGenerator',
    'GroundingEvidenceRequest', 
    'GroundingEvidenceResponse',
    'GroundingEvidence'
] 