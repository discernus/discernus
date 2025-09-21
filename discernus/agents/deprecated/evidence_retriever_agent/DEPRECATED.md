# DEPRECATED: Evidence Retriever Agent

**Status**: DEPRECATED as of 2025-01-21
**Replacement**: `IntelligentEvidenceRetrievalAgent`

## Deprecation Notice

This agent has been superseded by the `IntelligentEvidenceRetrievalAgent` which provides:

- **Strategic Planning**: Gemini Pro-driven evidence curation planning
- **LLM-Driven Curation**: Eliminates RAG dependencies
- **Session Caching**: Cost-optimized evidence processing
- **Dynamic Model Selection**: Intelligent model choice based on evidence volume
- **Atomic Evidence Processing**: Direct processing of atomic evidence artifacts

## Migration Path

The CLI has already been updated to use `IntelligentEvidenceRetrievalAgent`. No action required for existing experiments.

## Files in this Directory

- `v2_evidence_retriever_agent.py` - Original RAG-based evidence retrieval
- `prompt.yaml` - Original evidence retrieval prompt
- `__init__.py` - Package initialization

## Why Deprecated

1. **Architecture**: RAG-based approach was replaced with strategic LLM-driven curation
2. **Functionality**: New agent provides superior evidence selection and organization
3. **Performance**: Session caching and dynamic model selection improve efficiency
4. **Maintenance**: Single agent reduces codebase complexity

## Removal Timeline

This directory will be removed in a future release after confirming no external dependencies exist.
