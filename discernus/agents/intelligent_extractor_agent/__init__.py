"""
Intelligent Extractor Agent - Gasket #2
========================================

Converts Raw Analysis Log to flat JSON structure using LLM intelligence.
Replaces brittle regex/json parsing with semantic LLM-based extraction.
"""

from .agent import IntelligentExtractorAgent, ExtractionResult, IntelligentExtractorError

__all__ = [
    'IntelligentExtractorAgent',
    'ExtractionResult', 
    'IntelligentExtractorError'
]