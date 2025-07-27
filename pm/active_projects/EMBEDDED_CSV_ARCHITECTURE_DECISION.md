# Embedded CSV Architecture Decision Record (ADR)

**Date**: January 28, 2025  
**Status**: 📋 PROPOSED - Requires Validation Before Implementation  
**Decision**: Migrate from JSON parsing to embedded CSV extraction for framework-agnostic synthesis  
**Impact**: Core framework specification change affecting all frameworks and orchestration  

---

## Problem Statement

**Current Architecture Failure**: The Hash Cross-Referenced CSV approach suffers from framework coupling. The `SynthesisOrchestrator` contains hardcoded assumptions about framework schemas (`intensity`/`salience` structure, specific dimension names, hardcoded metrics like `mc_sci_score`). This breaks with frameworks using different schemas (e.g., Business Ethics Framework's direct score structure).

**Root Cause**: Attempting to parse diverse JSON schemas in post-processing instead of standardizing the data format at the source.

**Technical Debt**: Framework-specific parsing logic violates THIN principles and creates maintenance burden as new frameworks are added.

---

## Architecture Decision

### **Core Principle: Data Format Standardization at Source**

**Decision**: Frameworks will embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters. The orchestrator becomes a simple text extraction tool, eliminating all schema-specific parsing logic.

### **Why This Approach**

**1. True Framework Agnosticism**  
- Orchestrator has zero knowledge of framework schemas
- New frameworks require zero orchestrator changes
- Framework independence enforced by design, not documentation

**2. THIN Architecture Compliance**  
- LLM intelligence: Format conversion and data structuring
- Software coordination: Simple delimiter extraction and file concatenation
- No complex parsing logic or schema interpretation

**3. Pre-1.0 Clean Slate Advantage**  
- No legacy frameworks to migrate (yet)
- Can mandate uniform contract for all frameworks
- Design the right abstraction instead of building around failures

**4. Calculated Metrics Support**  
- Frameworks include both raw scores and calculated metrics in CSV
- Mathematical verification remains in JSON for audit
- Synthesis agents get rich tabular data without parsing complexity

---

## Technical Specification

### **Framework Contract V5.0 (New)**

Every framework MUST include embedded CSV segments in LLM responses:

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,dimension1,dimension2,calculated_metric1,calculated_metric2
{artifact_id},0.9,0.7,0.54,3.21
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
{artifact_id},dimension1,1,"Supporting evidence quote",primary
{artifact_id},dimension2,1,"Another evidence quote",primary
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>

[Normal JSON analysis continues...]
```

### **Orchestrator Logic (Framework-Agnostic)**

```python
def extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> Tuple[str, str]:
    """Extract pre-formatted CSV segments from LLM response."""
    
    # Extract scores CSV
    scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
    scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
    scores_csv = scores_match.group(1).strip() if scores_match else ""
    
    # Extract evidence CSV  
    evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
    evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
    evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
    
    # Replace placeholder with actual artifact ID
    scores_csv = scores_csv.replace("{artifact_id}", artifact_id)
    evidence_csv = evidence_csv.replace("{artifact_id}", artifact_id)
    
    return scores_csv, evidence_csv
```

**Key Point**: Orchestrator knows nothing about dimensions, metrics, or framework schemas. It only knows how to find text between delimiters.

---

## Prototyping Strategy

### **Phase 1: Isolated Proof of Concept (Week 1)**

**Objective**: Validate embedded CSV extraction without touching production frameworks

**Implementation**:
1. Create `tests/embedded_csv_prototype/` directory
2. Create 2-3 synthetic framework responses with embedded CSV
3. Implement delimiter extraction logic in isolated test
4. Validate CSV aggregation produces correct combined files
5. Test with various dimension sets and calculated metrics

**Success Criteria**:
- [ ] Clean extraction of CSV segments from text
- [ ] Correct aggregation of multiple artifacts
- [ ] Dynamic column discovery for scores CSV
- [ ] Evidence cross-referencing maintains integrity
- [ ] Zero framework-specific assumptions in code

### **Phase 2: Single Framework Migration (Week 2)**

**Objective**: Migrate one existing framework to embedded CSV contract

**Implementation**:
1. Choose simple framework (ECF or CAF) for migration
2. Create Framework V5.0 specification document
3. Update chosen framework's output contract with embedded CSV
4. Test analysis generation produces valid embedded CSV
5. Validate synthesis orchestrator processes migrated framework

**Success Criteria**:
- [ ] Framework generates valid embedded CSV segments
- [ ] Orchestrator extracts and processes correctly
- [ ] Token efficiency gains maintained (hash compression still works)
- [ ] Academic quality preserved (full quotes, proper dimension names)
- [ ] Mathematical verification still functions

### **Phase 3: Cross-Framework Validation (Week 3)**

**Objective**: Prove framework agnosticism with diverse schemas

**Implementation**:
1. Migrate second framework with different schema (Business Ethics)
2. Run both frameworks through same orchestrator code
3. Validate aggregated CSV handles different column sets
4. Test synthesis quality with mixed framework data
5. Document framework migration guidelines

**Success Criteria**:
- [ ] Same orchestrator processes both frameworks
- [ ] Dynamic column discovery works across different schemas  
- [ ] Synthesis quality maintained or improved
- [ ] Zero orchestrator modifications needed for second framework

---

## Risk Mitigation

### **Primary Risk: Framework-Specific Coding Recurrence**

**Manifestation**: Agents adding framework-aware logic to orchestrator during implementation

**Prevention Strategies**:

**1. Code Review Checkpoints**
- [ ] Orchestrator contains zero hardcoded dimension names
- [ ] Orchestrator contains zero hardcoded metric names  
- [ ] Orchestrator contains zero schema-specific parsing logic
- [ ] All framework knowledge resides in framework contracts only

**2. Test-Driven Development**
- Write framework-agnostic tests FIRST
- Tests must pass with synthetic data before real framework integration
- Orchestrator must handle unknown column sets gracefully

**3. Documentation Enforcement**
- Clear ADR stating "orchestrator knows nothing about frameworks"
- Code comments reinforcing framework agnosticism requirement
- Migration guidelines emphasizing contract-only changes

**4. Architecture Reviews**
- Mandatory review before any orchestrator modifications
- Focus question: "Does this change require knowledge of specific frameworks?"
- If yes → reject, move logic to framework contract

### **Secondary Risk: Delimiter Collision**

**Mitigation**: Use highly distinctive delimiters unlikely to appear in academic text
- Include version numbers for future evolution
- Test with large corpus to validate uniqueness
- Design escape sequence if needed

### **Tertiary Risk: LLM Formatting Inconsistency**

**Mitigation**: 
- Clear CSV formatting examples in framework contracts
- Validation prompt asking LLM to self-check CSV format
- Graceful error handling for malformed segments

---

## Success Metrics

### **Technical Metrics**
- **Framework Independence**: Same orchestrator code processes all frameworks
- **Token Efficiency**: Hash compression benefits maintained (>35% reduction)
- **Academic Quality**: Full quotes and proper dimension names preserved
- **Performance**: CSV extraction faster than JSON parsing

### **Architectural Metrics**
- **Lines of Framework-Specific Code**: 0 (target)
- **Orchestrator Modifications per New Framework**: 0 (target)
- **Framework Migration Effort**: Contract change only, no orchestrator changes

### **Quality Metrics**
- **Synthesis Report Quality**: Maintained or improved vs current approach
- **Evidence Cross-Reference Accuracy**: 100% correct artifact linking
- **Calculated Metrics Preservation**: All framework calculations available to synthesis

---

## Decision Consequences

### **Positive Consequences**
- **True Framework Agnosticism**: Architecture supports unlimited framework diversity
- **THIN Compliance**: Clear separation of LLM intelligence and software coordination  
- **Maintainability**: New frameworks require zero orchestrator changes
- **Academic Quality**: Full context preserved without lookup complexity

### **Negative Consequences**
- **Framework Contract Burden**: All frameworks must implement embedded CSV
- **LLM Token Usage**: Additional CSV generation adds token overhead
- **Migration Effort**: Existing frameworks require contract updates
- **Delimiter Dependency**: Architecture depends on reliable delimiter extraction

### **Neutral Consequences**
- **Different Approach**: Represents architectural shift from parsing to extraction
- **Learning Curve**: Team must understand embedded CSV paradigm

---

## Implementation Timeline

```
Week 1: Isolated Prototype
├── Day 1-2: Delimiter extraction logic
├── Day 3-4: CSV aggregation testing  
└── Day 5: Multi-artifact validation

Week 2: Single Framework Migration
├── Day 1-2: Framework V5.0 specification
├── Day 3-4: Framework contract update
└── Day 5: End-to-end validation

Week 3: Cross-Framework Validation  
├── Day 1-2: Second framework migration
├── Day 3-4: Synthesis quality testing
└── Day 5: Documentation and guidelines
```

---

## Approval Gates

### **Gate 1: Prototype Validation**
- [ ] Delimiter extraction works reliably
- [ ] CSV aggregation produces correct output
- [ ] No framework-specific assumptions detected
- **Go/No-Go**: If prototype shows framework coupling, return to design

### **Gate 2: Single Framework Success**
- [ ] Framework generates valid embedded CSV
- [ ] Orchestrator processes without modifications
- [ ] Synthesis quality maintained
- **Go/No-Go**: If orchestrator requires framework-specific changes, return to design

### **Gate 3: Cross-Framework Success**
- [ ] Second framework works with same orchestrator
- [ ] Different schemas handled gracefully
- [ ] Academic quality preserved across frameworks
- **Go/No-Go**: If framework agnosticism fails, return to architecture

---

## Conclusion

The embedded CSV approach represents a fundamental architectural improvement that aligns with THIN principles while solving the framework independence problem. By standardizing data format at the source rather than parsing diverse schemas in post-processing, we achieve true framework agnosticism without complex orchestrator logic.

**Key Success Factor**: Strict enforcement of framework agnosticism during implementation. The orchestrator must remain a simple text extraction tool with zero knowledge of framework internals.

**Next Action**: Execute Phase 1 isolated prototype to validate delimiter extraction and CSV aggregation without touching production frameworks. 