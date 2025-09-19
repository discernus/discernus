# RAG Removal Plan for V2 Orchestrator

## Overview
This document outlines the specific RAG-related code that needs to be removed from the orchestrator as part of Sprint V2-2. The V2 EvidenceRetrieverAgent now handles all RAG logic internally.

## Code to Remove from CleanAnalysisOrchestrator

### 1. RAG Index Instance Variables
```python
# REMOVE from __init__
self.rag_index = None
```

### 2. RAG Index Building Methods
```python
# REMOVE these methods entirely:
def _build_rag_index(self, audit_logger: AuditLogger) -> None
def _build_and_cache_rag_index(self, audit_logger: AuditLogger) -> None  
def _build_rag_index_with_cache(self, audit_logger: AuditLogger) -> None
def _build_fact_checker_rag_index(self, assets: Dict[str, Any], statistical_results: Dict[str, Any])
```

### 3. RAG Index Manager Import
```python
# REMOVE this import
from .rag_index_manager import RAGIndexManager
```

### 4. RAG Index Cache Manager Import
```python
# REMOVE this import
from .rag_index_cache import RAGIndexCacheManager
```

### 5. RAG Index Building Calls
```python
# REMOVE these calls from run_analysis:
self._build_and_cache_rag_index(audit_logger)
self._build_rag_index_with_cache(audit_logger)
```

### 6. RAG Index References
```python
# REMOVE all references to self.rag_index
self.rag_index = index
if self.rag_index:
    # ... RAG operations
```

## Code to Update

### 1. Evidence Retrieval Phase
```python
# BEFORE (V1):
def _run_evidence_retrieval_phase(self, model, audit_logger, statistical_results, run_id):
    # Complex RAG index building logic
    # Direct evidence retrieval management
    # RAG index passing to agents

# AFTER (V2):
def _run_evidence_retrieval_phase(self, run_context: RunContext):
    # Simple agent coordination
    evidence_agent = V2EvidenceRetrieverAgent(security, storage, audit, config)
    return evidence_agent.execute(run_context=run_context)
```

### 2. Synthesis Phase
```python
# BEFORE (V1):
def _run_synthesis_phase(self, model, audit_logger, statistical_results, evidence_results, run_id):
    # RAG index access for synthesis
    # Complex evidence management

# AFTER (V2):
def _run_synthesis_phase(self, run_context: RunContext):
    # Synthesis agent gets evidence from RunContext
    # No direct RAG index access needed
    synthesis_agent = V2SynthesisAgent(security, storage, audit, config)
    return synthesis_agent.execute(run_context=run_context)
```

## Benefits of RAG Removal

### 1. THIN Architecture
- Orchestrator no longer manages RAG indexes
- Agents handle their own RAG needs
- Orchestrator becomes a simple traffic cop

### 2. Better Separation of Concerns
- EvidenceRetrieverAgent owns all evidence logic
- SynthesisAgent owns all synthesis logic
- Orchestrator only coordinates

### 3. Improved Testability
- Each agent can be tested independently
- No complex RAG setup in orchestrator tests
- Clearer interfaces between components

### 4. Reduced Complexity
- Removes ~500 lines of RAG code from orchestrator
- Eliminates RAG index caching complexity
- Simplifies error handling

## Migration Steps

1. **Create V2 EvidenceRetrieverAgent** ✅ DONE
2. **Remove RAG methods from orchestrator** ← CURRENT STEP
3. **Update evidence retrieval phase to use V2 agent**
4. **Update synthesis phase to use RunContext**
5. **Remove RAG imports and instance variables**
6. **Test V2 orchestrator with V2 agents**

## Files to Modify

- `discernus/core/clean_analysis_orchestrator.py` - Remove RAG code
- `discernus/core/rag_index_manager.py` - Keep (used by agents)
- `discernus/core/rag_index_cache.py` - Keep (used by agents)
- `discernus/agents/evidence_retriever_agent/v2_evidence_retriever_agent.py` - Already done

## Testing Strategy

1. **Unit Tests**: Test V2 EvidenceRetrieverAgent independently
2. **Integration Tests**: Test orchestrator with V2 agents
3. **End-to-End Tests**: Test complete experiment flow
4. **Performance Tests**: Ensure RAG consolidation doesn't impact performance

## Rollback Plan

If issues arise:
1. Keep V1 EvidenceRetrieverAgent as fallback
2. Add feature flag to switch between V1 and V2
3. Maintain backward compatibility during transition
4. Gradual migration of experiments to V2

## Success Criteria

- [ ] All RAG code removed from orchestrator
- [ ] V2 EvidenceRetrieverAgent handles all RAG logic
- [ ] Orchestrator becomes simple traffic cop
- [ ] All tests pass
- [ ] Performance maintained or improved
- [ ] Code complexity reduced by ~500 lines
