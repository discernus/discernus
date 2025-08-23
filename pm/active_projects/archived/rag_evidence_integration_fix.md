# RAG Evidence Integration Fix Plan

**Issue**: UnifiedSynthesisAgent generates placeholder evidence instead of retrieving actual quotes from the RAG index, resulting in synthesis reports with no corpus awareness or evidence citations.

**Root Cause**: The agent handles txtai search results as `(doc_id, score)` tuples but doesn't access the underlying document store to retrieve actual evidence content.

---

## Detailed Step-by-Step Plan: Fix RAG Evidence Integration (REVISED)

**Key Insight**: The deprecated `ExperimentOrchestrator` has working data integration patterns that we should copy to `CleanAnalysisOrchestrator`.

### **Phase 1: Analysis and Test Setup (TDD)**

**Step 1.1: Create Failing Integration Test**
- Write test that demonstrates current synthesis failure (no evidence, no corpus awareness)
- Test should expect actual evidence quotes and corpus document names
- Run test to confirm it fails with current implementation

**Step 1.2: Create Failing Unit Tests**
- Test complete research data structure (should include raw scores, derived metrics, statistical results)
- Test evidence hash collection and integration
- Test synthesis agent receives all required data
- All tests should fail initially

### **Phase 2: Copy Working Patterns from Deprecated Orchestrator**

**Step 2.1: Copy Complete Research Data Structure**
- Extract `_store_research_artifacts()` pattern from `ExperimentOrchestrator` (lines 728-737)
- Implement in `CleanAnalysisOrchestrator` to create complete research data
- Include: experiment metadata, raw analysis data, derived metrics, statistical results

**Step 2.2: Copy Evidence Hash Collection Pattern**
- Extract evidence collection logic from deprecated orchestrator
- Implement `_collect_evidence_artifact_hashes()` in `CleanAnalysisOrchestrator`
- Ensure evidence hashes are passed to synthesis agent

**Step 2.3: Update Synthesis Agent Call**
- Modify `CleanAnalysisOrchestrator._run_synthesis()` to match deprecated pattern
- Pass both `evidence_artifact_hashes` AND `rag_index` to synthesis agent
- Use complete research data structure instead of just statistical results

### **Phase 3: Fix UnifiedSynthesisAgent to Use Both Data Sources**

**Step 3.1: Update Method Signature**
- Modify `generate_final_report()` to accept `evidence_artifact_hashes` parameter
- Maintain backward compatibility with RAG index parameter
- Update method to use both evidence sources

**Step 3.2: Implement Dual Evidence Access**
- Use evidence artifact hashes for direct evidence access (like deprecated orchestrator)
- Use RAG index for semantic search and retrieval
- Combine both approaches for comprehensive evidence integration

**Step 3.3: Fix Evidence Context Generation**
- Replace placeholder generation with actual evidence retrieval
- Include document names, quotes, and proper attribution
- Ensure corpus awareness through complete research data

### **Phase 4: Validate with TDD**

**Step 4.1: Run Unit Tests**
- Verify complete research data structure test passes
- Confirm evidence hash collection test passes
- Check synthesis agent receives all required data

**Step 4.2: Run Integration Test**
- Execute full experiment with fixed implementation
- Verify integration test now passes (evidence quotes, corpus awareness)
- Compare before/after report quality

**Step 4.3: Regression Testing**
- Run existing test suite to ensure no regressions
- Verify statistical analysis still works correctly
- Confirm RAG index building still functions

### **Phase 5: Clean Up**

**Step 5.1: Update Documentation**
- Document the fix in code comments
- Update any relevant architectural notes
- Remove placeholder comments about "future implementation"

**Step 5.2: Remove Temporary Code**
- Clean up any debug logging added during development
- Remove the placeholder evidence generation code
- Ensure clean, production-ready implementation

### **Specific Deliverables**

1. **Working unit test** demonstrating evidence retrieval
2. **Fixed `UnifiedSynthesisAgent`** that accesses real evidence
3. **Integration test** showing end-to-end improvement
4. **Before/after comparison** of experiment reports
5. **Clean, documented code** ready for production

### **Risk Mitigation**

- Each step has a clear success/failure criterion
- Unit tests prevent regressions
- Changes are isolated to `UnifiedSynthesisAgent`
- Can rollback if integration tests fail

### **Time Estimate**

- Phase 1-2: ~30 minutes (analysis and test creation)
- Phase 3: ~45 minutes (implementation)
- Phase 4-5: ~30 minutes (validation and cleanup)
- **Total: ~2 hours of focused work**

---

## Current Status

- **Created**: 2025-01-22
- **Status**: Planning
- **Priority**: High (blocks synthesis quality)
- **Assigned**: Assistant

## Success Criteria

✅ **Evidence Integration Working**: Synthesis reports contain actual evidence quotes with proper attribution  
✅ **Corpus Awareness**: Reports mention specific documents that were analyzed  
✅ **No Regressions**: Existing functionality continues to work  
✅ **Clean Implementation**: Production-ready code with proper documentation  

## Notes

This plan addresses the core evidence integration issue without attempting broader architectural changes. Each step is measurable and reversible. The fix is isolated to `UnifiedSynthesisAgent` to minimize risk of breaking other components.
