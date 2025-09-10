"""
Comprehensive Knowledge Curator Agent

This module provides comprehensive knowledge graph indexing for all experiment data types,
enabling cross-domain reasoning and intelligent synthesis for modern AI research platforms.

Technical Co-Founder Showcase Features:
- Unified knowledge architecture across 6 data types
- Cross-domain semantic search and reasoning
- Persistent RAG index with enterprise scalability
- LLM-powered query optimization and refinement
"""

from .agent import (
    ComprehensiveKnowledgeCurator,
    ComprehensiveIndexRequest,
    ComprehensiveIndexResponse,
    KnowledgeQuery,
    KnowledgeResult,
    create_comprehensive_knowledge_curator
)

__all__ = [
    'ComprehensiveKnowledgeCurator',
    'ComprehensiveIndexRequest',
    'ComprehensiveIndexResponse',
    'KnowledgeQuery',
    'KnowledgeResult',
    'create_comprehensive_knowledge_curator'
]
