"""
Unified Synthesis Agent for Discernus v10
=========================================

Generates publication-ready research reports using:
- Complete research data (raw scores, derived metrics, statistical results)
- Curated evidence from EvidenceRetriever
- THIN prompting approach with gemini-2.5-pro for reliability

Pure synthesis agent - no external lookups or RAG queries.
"""

from .v2_unified_synthesis_agent import V2UnifiedSynthesisAgent

# Legacy alias for backward compatibility
UnifiedSynthesisAgent = V2UnifiedSynthesisAgent

__all__ = ['V2UnifiedSynthesisAgent', 'UnifiedSynthesisAgent']
