#!/usr/bin/env python3
"""
Analysis Agent - THIN v2.0 Architecture
=======================================

Production analysis agent with 6-step THIN approach featuring inline markup,
comprehensive logging, and full orchestrator compatibility.
"""

from .v2_analysis_agent import V2AnalysisAgent

# Legacy alias for backward compatibility  
AnalysisAgent = V2AnalysisAgent

__all__ = [
    "V2AnalysisAgent",
    "AnalysisAgent",
]
