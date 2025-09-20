#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Architecture
=========================================

THIN v2.0 compliant agents with minimal intelligence and LLM-driven processing.
"""

# Analysis Agent - Production THIN v2.0 with 6-step approach
from .analysis_agent.main import AnalysisAgent
from .automated_derived_metrics import AutomatedDerivedMetricsAgent

# Statistical Agent - THIN v2.0 with LLM internal execution
from .statistical_agent.main import StatisticalAgent

__all__ = [
    "AnalysisAgent",
    "AutomatedDerivedMetricsAgent",
    "StatisticalAgent",
] 