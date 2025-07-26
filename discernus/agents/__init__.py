#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Enhanced Agents
============================================

Enhanced agents for the THIN v2.0 architecture with mathematical validation
and direct function call interfaces.
"""

# THIN v2.0 Enhanced Agents
from .EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from .EnhancedSynthesisAgent.main import EnhancedSynthesisAgent
from .batch_planner_agent import BatchPlannerAgent

# Legacy agents (for backward compatibility)
from .AnalyseBatchAgent.main import AnalyseBatchAgent
from .SynthesisAgent.main import SynthesisAgent  
from .ReportAgent.main import ReportAgent

__all__ = [
    # THIN v2.0 Enhanced Agents
    "EnhancedAnalysisAgent",
    "EnhancedSynthesisAgent",
    "BatchPlannerAgent",
    
    # Legacy Agents
    "AnalyseBatchAgent",
    "SynthesisAgent", 
    "ReportAgent",
] 