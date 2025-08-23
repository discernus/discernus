#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Architecture
=========================================

THIN v2.0 compliant agents with minimal intelligence and LLM-driven processing.
"""

# THIN v2.0 Active Agents
from .EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from .automated_derived_metrics import AutomatedDerivedMetricsAgent

__all__ = [
    "EnhancedAnalysisAgent",
    "AutomatedDerivedMetricsAgent",
] 