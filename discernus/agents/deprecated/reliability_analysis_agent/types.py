#!/usr/bin/env python3
"""
Reliability Analysis Agent Types
===============================

Shared types for the Reliability Analysis Agent to avoid circular imports.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DimensionValidationResult:
    """Result of framework dimension validation."""
    validation_passed: bool
    missing_required_dimensions: List[str]
    missing_optional_dimensions: List[str]
    present_dimensions: List[str]
    impact_assessment: str
    recommended_action: str
    error_message: Optional[str] = None


@dataclass
class StatisticalHealthResult:
    """Result of statistical health validation."""
    validation_passed: bool
    calculation_failures: List[str]
    perfect_correlations: List[str]
    statistical_warnings: List[str]
    sample_size_assessment: str
    recommended_action: str
    error_message: Optional[str] = None


@dataclass
class PipelineHealthResult:
    """Result of pipeline health assessment."""
    health_status: str
    error_patterns: List[str]
    performance_issues: List[str]
    reliability_metrics: dict
    recommended_actions: List[str]
    alert_level: str


class ReliabilityAnalysisError(Exception):
    """Reliability Analysis Agent specific exceptions."""
    pass
