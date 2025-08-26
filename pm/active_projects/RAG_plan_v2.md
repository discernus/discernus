# **Project Plan: Hybrid RAG-FactChecker System (v2 Revised)**

This document outlines the strategy, definition of done, and test plan for implementing a hybrid fact-checking system that combines the working synthesis RAG index with direct asset injection for comprehensive validation.

## **Strategic Decision: Hybrid Approach**

**Analysis Summary**: After investigating comprehensive RAG indexing, we determined that a hybrid approach provides 80% of the benefits with 20% of the complexity:

- **✅ Keep Working Synthesis RAG**: Evidence retrieval during report generation (already functional)
- **✅ Add Direct Asset Injection**: Framework, statistical, and metadata validation via 2M token context
- **✅ Reuse Synthesis RAG**: Evidence quote validation using existing RAG index
- **✅ Scalability Confirmed**: Viable up to 6,000 documents (64% context utilization at 4,000 docs)

## **1. Definition of Done**

The project is complete when all of the following criteria are met and verified through automated testing and manual log inspection:

* **1.1. Hybrid Fact-Checking Architecture**: The `FactCheckerAgent` uses synthesis RAG for evidence validation and direct injection for framework/statistical validation.
* **1.2. Comprehensive Validation Coverage**: All six validation checks work reliably with appropriate data sources.
* **1.3. Robust Test Coverage**: A full suite of integration and unit tests validates the hybrid approach.
* **1.4. System Integrity**: No regressions are introduced, and the solution adheres to all architectural principles.
* **1.5. End-to-End Log Transparency**: 
  * All fact-checking actions are meticulously logged in `application.log`.
  * The logs clearly show the progression of each validation check and data source used.
  * Complete traceability of how the agent reached its conclusions for each finding.
* **1.6. Effective Revision Agent Integration**:
  * The `RevisionAgent` correctly consumes structured findings from the `FactCheckerAgent`.
  * For each finding, the `RevisionAgent` performs necessary corrections to the draft report.
  * All revision actions are logged with complete transparency.
  * Final reports are free of fact-checking errors (warning/error blocks become rare exceptions).

## **2. Hybrid Architecture Strategy**

### **Data Source Mapping by Validation Check:**

1. **Evidence Quote Mismatch** → **Synthesis RAG Index** (reuse existing)
2. **Dimension Hallucination** → **Direct Framework Injection** (2M context)
3. **Statistic Mismatch** → **Direct Statistical Results Injection** (2M context)
4. **Grandiose Claims** → **No external data needed** (pattern detection)
5. **Citation Violation** → **No external data needed** (pattern detection)
6. **Fabricated Reference** → **No external data needed** (pattern detection)

### **Token Budget Analysis:**
- 4,000-document experiment: ~1.27M tokens (64% of 2M context)
- Comfortable headroom for fact-checking prompts and responses
- Scalable up to ~6,000 documents before context limits

## **3. Implementation Strategy**

### **Phase 1: Research & Confidence Building** ✅ **COMPLETED**
Research confirmed hybrid approach viability and identified implementation requirements.

### **Phase 2: Test-Driven Infrastructure Development**
1. **Create Integration Test**: `discernus/tests/integration/test_hybrid_fact_checker.py`
2. **Test Hybrid Data Sources**: Verify synthesis RAG + direct injection work together
3. **Test All Six Validation Checks**: Ensure each check uses appropriate data source

### **Phase 3: Implement Hybrid Fact-Checker**
1. **Modify FactCheckerAgent**: Update `_get_evidence_context()` method for hybrid approach
2. **Add Direct Asset Injection**: Create methods to inject framework/statistical data directly
3. **Preserve RAG Integration**: Keep existing synthesis RAG usage for evidence validation
4. **Add Granular Logging**: Log data source and decision process for each check

### **Phase 4: Re-architect RevisionAgent Integration**
1. **Create Integration Test**: `discernus/tests/integration/test_revision_agent.py`
2. **TDD for Revision Logic**: Test full pipeline with known, fixable errors
3. **Implement Revision Agent**: Create systematic error correction based on findings
4. **Add Revision Logging**: Log each correction action with transparency

### **Phase 5: Final Validation**
1. Run all unit and integration tests
2. Execute `1a_caf_civic_character` experiment end-to-end
3. Verify fact-checking accuracy across all six check types
4. Manually inspect logs for complete transparency and traceability

## **4. Technical Implementation Details**

### **Modified FactCheckerAgent Architecture:**

```python
def _get_evidence_context(self, check: Dict[str, str], report_content: str, evidence_index: Any) -> str:
    check_name = check.get('name', '')
    
    if check_name == "Evidence Quote Mismatch":
        # Use existing synthesis RAG index
        return self._query_synthesis_rag_for_quotes(report_content, evidence_index)
    
    elif check_name == "Dimension Hallucination":
        # Direct framework injection (2M token context)
        return self._inject_framework_content_directly()
    
    elif check_name == "Statistic Mismatch":
        # Direct statistical results injection
        return self._inject_statistical_results_directly()
    
    # Other checks (Grandiose Claims, Citation Violation, Fabricated Reference)
    # No external data needed - pattern detection only
    return ""
```

### **Asset Injection Strategy:**
- **Framework Content**: Complete framework specification (~15K tokens)
- **Statistical Results**: Complete statistical analysis (~50K tokens)
- **Experiment Metadata**: Experiment definition and corpus manifest (~9K tokens)
- **Total Direct Injection**: ~74K tokens (leaving 1.9M+ for evidence and processing)

### **Logging Enhancement:**
- Log data source used for each validation check
- Log query/retrieval process for RAG-based checks
- Log asset injection process for direct checks
- Log decision reasoning and confidence levels
- Maintain complete audit trail for revision actions

## **5. Success Criteria**

### **Functional Requirements:**
- [ ] All six validation checks work reliably with appropriate data sources
- [ ] Evidence quotes validated against synthesis RAG index
- [ ] Framework dimensions validated against direct framework injection
- [ ] Statistical claims validated against direct statistical results
- [ ] RevisionAgent successfully corrects identified issues
- [ ] Final reports free of fact-checking errors

### **Quality Requirements:**
- [ ] Complete test coverage for hybrid approach
- [ ] End-to-end logging transparency
- [ ] No performance degradation vs. current system
- [ ] Scalable architecture up to 6,000 documents

### **Integration Requirements:**
- [ ] Seamless integration with existing synthesis RAG
- [ ] No disruption to working synthesis pipeline
- [ ] Maintains all existing architectural principles
- [ ] Compatible with current orchestrator flow

## **6. Risk Mitigation**

**Low Risk**: Hybrid approach builds on proven components
- Synthesis RAG already working for evidence retrieval
- Direct injection already proven with 2M token context
- Minimal new infrastructure required

**Fallback Strategy**: If hybrid approach fails, revert to pure direct injection
- All assets via 2M token context (proven working approach)
- Synthesis RAG remains untouched for evidence synthesis
- No loss of existing functionality

## **7. Effort Estimate**

**Total Effort**: 1-2 days (vs. 1-2+ weeks for comprehensive RAG)

- **Phase 2**: 2-3 hours (TDD test creation)
- **Phase 3**: 4-6 hours (hybrid fact-checker implementation)
- **Phase 4**: 3-4 hours (revision agent integration)
- **Phase 5**: 2-3 hours (validation and testing)

**Confidence Level**: 95% success probability (vs. 60% for comprehensive RAG)