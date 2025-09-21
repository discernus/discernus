"""
TwoStageSynthesisAgent Package
==============================

A two-stage synthesis agent that prevents hallucination by separating:
- Stage 1: Data-driven analysis from statistical results (no quotes)
- Stage 2: Evidence integration with curated quotes and appendix

This architecture ensures all claims are anchored in statistical data before
evidence is added, preventing analytical drift and unsupported conclusions.
"""

from .two_stage_synthesis_agent import TwoStageSynthesisAgent

__all__ = ['TwoStageSynthesisAgent']
