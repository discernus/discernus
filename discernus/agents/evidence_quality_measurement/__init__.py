"""
Evidence Quality Measurement Agent

Implements Epic #354 requirements for systematic evidence quality measurement
to ensure peer-review ready academic standards.
"""

from .agent import (
    EvidenceQualityMeasurementAgent,
    QualityMeasurementRequest,
    QualityMeasurementResponse,
    EvidenceQualityMetrics
)

__all__ = [
    'EvidenceQualityMeasurementAgent',
    'QualityMeasurementRequest', 
    'QualityMeasurementResponse',
    'EvidenceQualityMetrics'
]
