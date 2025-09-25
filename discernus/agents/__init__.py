#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Architecture
=========================================

THIN v2.0 compliant agents with minimal intelligence and LLM-driven processing.
"""

# V2 Agents - Production THIN v2.0 architecture
from .analysis_agent.v2_analysis_agent import V2AnalysisAgent
from .statistical_agent.v2_statistical_agent import V2StatisticalAgent
from .intelligent_evidence_retriever.intelligent_evidence_retriever_agent import IntelligentEvidenceRetrievalAgent
from .validation_agent.v2_validation_agent import V2ValidationAgent

# Legacy aliases for backward compatibility
AnalysisAgent = V2AnalysisAgent
StatisticalAgent = V2StatisticalAgent

__all__ = [
    # V2 Agents
    "V2AnalysisAgent",
    "V2StatisticalAgent", 
    "IntelligentEvidenceRetrievalAgent",
    "V2ValidationAgent",
    # Legacy aliases
    "AnalysisAgent",
    "StatisticalAgent",
] 