"""
txtai Evidence Curator Agent

This module provides txtai-based evidence curation for scalable, accurate
evidence retrieval from large evidence pools while maintaining perfect
academic provenance.
"""

from .agent import (
    TxtaiEvidenceCurator,
    TxtaiCurationRequest, 
    TxtaiCurationResponse,
    EvidenceQuery,
    EvidenceResult,
    create_txtai_evidence_curator
)

__all__ = [
    'TxtaiEvidenceCurator',
    'TxtaiCurationRequest',
    'TxtaiCurationResponse', 
    'EvidenceQuery',
    'EvidenceResult',
    'create_txtai_evidence_curator'
]
