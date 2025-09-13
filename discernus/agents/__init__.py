#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Architecture
=========================================

THIN v2.0 compliant agents with minimal intelligence and LLM-driven processing.
"""

# Show Your Work Architecture - Active Agents
from .EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from .EnhancedAnalysisAgent.agent_tool_calling import EnhancedAnalysisAgentToolCalling
from .automated_derived_metrics import AutomatedDerivedMetricsAgent

__all__ = [
    "EnhancedAnalysisAgentMultiTool",
    "EnhancedAnalysisAgentToolCalling", 
    "AutomatedDerivedMetricsAgent",
] 