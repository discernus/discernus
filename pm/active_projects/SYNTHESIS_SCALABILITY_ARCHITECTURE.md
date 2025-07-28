# Synthesis Scalability Architecture & Implementation Plan

**Date**: January 28, 2025  
**Status**: ✅ ACTIVE - This is the canonical architecture and plan of record  
**Decision**: Migrate to Embedded CSV Architecture to solve synthesis scalability bottlenecks  
**Impact**: Core framework specification change affecting all frameworks and orchestration

---

## 1. Strategic Context & Vision

### **Architectural Philosophy**
This document outlines the best architectural path forward based on our **current visibility window** into the rapidly evolving LLM landscape. We recognize that today's constraints (context windows, output token limits, mathematical reliability) will likely change, but we must build a robust, flexible architecture that solves today's problems while being adaptable for tomorrow's opportunities.

Our core mission is to enable **framework-based text analysis at unprecedented scale**. This architecture is designed to make Discernus the market leader in this domain, capable of processing corpora 10-100x larger than current academic or commercial standards.

### **The Core Problem: Synthesis Bottlenecks**
Our research revealed that synthesis fails at scale due to a **"perfect storm"** of interacting constraints:

1.  **Massive Input Volume**: Academic-grade analysis produces ~16,000 characters of data *per document*, with 80% of that being evidence and mathematical proofs not essential for synthesis.
2.  **Output Token Limits**: Synthesis agents attempt to generate 6,000+ token reports, which are truncated by the ~8K output limits of current-generation LLMs (Gemini, Llama, etc.). This is the **primary operational bottleneck**.
3.  **LLM Mathematical Unreliability**: Alternative models like Llama Scout, while cost-effective, exhibit systematic mathematical errors (e.g., 15x error on MC-SCI calculations), making them unsuitable for statistical synthesis.

**Conclusion**: The bottleneck is **architectural, not model-specific**. No LLM can solve this problem without a change in how we structure and present data for synthesis.

---

## 2. Architecture Decision: Embedded CSV

### **Core Principle: Data Format Standardization at Source**
Frameworks will embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters. The orchestrator becomes a simple, framework-agnostic text extraction tool, eliminating all schema-specific parsing logic and dramatically reducing the input data volume for synthesis.

### **Technical Specification**
Every framework MUST include these embedded CSV segments:

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
```

### **Benefits of this Architecture**
1.  **Solves Output Token Bottleneck**: Reduces synthesis input by ~95%, leading to smaller, more focused output that fits within current token limits.
2.  **Enforces Mathematical Reliability**: Provides clean, structured tabular data for reliable statistical processing, mitigating LLM calculation errors.
3.  **True Framework Agnosticism**: Orchestrator has zero knowledge of framework schemas.
4.  **THIN Compliance**: Clear separation of LLM intelligence (scoring, CSV generation) and software coordination (extraction, aggregation).
5.  **Preserves Academic Rigor**: The full, verbose JSON with evidence and proofs is still saved for audit and deep analysis, while the synthesis-ready CSV is used for scaling.

---

## 3. Post-CSV Scalability Projections

This architecture represents a **generational leap in scale capability**.

### **Input & Output Projections**
-   **Input Compression**: ~95% reduction (from ~22K chars/doc to ~1K chars/doc).
-   **Output Size**: ~1,500-2,500 tokens (fits comfortably within 8K limits).

### **Realistic Upper Bounds (Conservative)**
-   **Academic Quality Synthesis**: **3,000-5,000 documents** per synthesis run.
-   **Statistical-Only Synthesis**: **5,000-8,000 documents** per synthesis run.

### **Market Positioning**
-   **Current Academic Practice**: 10-50 documents.
-   **Post-CSV Discernus**: 3,000-8,000 documents (**60-800x improvement**).

---

## 4. Implementation & Prototyping Plan

We will follow a phased approach to de-risk this architectural transition.

### **Phase 1: Isolated Proof of Concept (Week 1)**
-   **Objective**: Validate embedded CSV extraction and aggregation in isolation.
-   **Tasks**: Create synthetic framework responses, implement delimiter extraction logic, and test aggregation.
-   **Success Criteria**: Clean extraction, correct aggregation, and zero framework-specific logic.

### **Phase 2: Single Framework Migration (Week 2)**
-   **Objective**: Migrate one existing framework (e.g., CAF) to the new V5.0 contract.
-   **Tasks**: Update framework output contract, test generation, and validate end-to-end processing.
-   **Success Criteria**: Valid CSV generation, correct orchestrator processing, and preserved academic quality.

### **Phase 3: Cross-Framework Validation (Week 3)**
-   **Objective**: Prove true framework agnosticism with a second, differently structured framework.
-   **Tasks**: Migrate a second framework, run both through the same orchestrator, and validate results.
-   **Success Criteria**: Zero orchestrator modifications needed for the second framework.

---

## 5. Risk Mitigation & Governance

### **Primary Risk: Framework-Specific Logic Creep**
-   **Mitigation**: Mandatory code reviews, TDD with framework-agnostic tests, and strict architectural governance enforcing the "zero orchestrator knowledge" rule.

### **Secondary Risk: Delimiter Collision / LLM Formatting**
-   **Mitigation**: Use versioned, highly unique delimiters. Include self-checking validation steps in framework prompts.

### **Approval Gates**
1.  **Prototype Validation**: Go/No-Go based on successful, framework-agnostic extraction.
2.  **Single Framework Success**: Go/No-Go based on successful end-to-end processing with no orchestrator changes.
3.  **Cross-Framework Success**: Go/No-Go based on successful processing of multiple, diverse frameworks with the same orchestrator code.

---

## 6. Conclusion

The Embedded CSV Architecture is the critical path to unlocking large-scale synthesis. It directly addresses the primary bottlenecks of output token limits and mathematical unreliability by standardizing data at the source. This plan provides a structured, de-risked approach to implementation.

## 🎯 **Phase 1: Isolated Proof of Concept** ✅ **COMPLETE**

**Major Breakthrough**: All success criteria validated through comprehensive testing.

### **✅ Validation Results**
- **CSV Extraction**: Regex patterns successfully extract embedded CSV sections from LLM responses
- **Framework Agnosticism**: Dynamic column discovery works across different framework schemas
- **Streaming Aggregation**: Append-only CSV files support scalable synthesis without memory constraints  
- **Evidence Cross-Referencing**: Artifact IDs maintain complete traceability between scores and evidence
- **LLM Compliance**: Gemini 2.5 Pro reliably produces the exact embedded CSV format required

### **🔬 Test Artifacts**
Complete validation suite in `tests/embedded_csv_prototype/`:
- `test_delimiter_extraction.py`: Validates regex extraction logic
- `test_csv_aggregation.py`: Validates streaming aggregation mechanics
- `test_llm_compliance.py`: Validates LLM can produce required format
- `csv_compliance_test.txt`: Real prompt test achieving 100% compliance

**Next Action**: Execute **Phase 2: Framework Integration**. 