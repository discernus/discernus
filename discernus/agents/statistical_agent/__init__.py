#!/usr/bin/env python3
"""
Discernus Statistical Agent - THIN v2.0 Architecture
===================================================

THIN statistical agent that performs comprehensive statistical analysis using 
LLM internal execution with minimal tool calling for verification.
"""

from .v2_statistical_agent import V2StatisticalAgent

# Legacy alias for backward compatibility
StatisticalAgent = V2StatisticalAgent

__all__ = [
    "V2StatisticalAgent", 
    "StatisticalAgent",
]
