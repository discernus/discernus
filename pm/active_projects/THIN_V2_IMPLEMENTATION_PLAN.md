# THIN v2.0 Implementation Plan (Roadmap to Production)

**Project**: Discernus Architecture Overhaul  
**Status**: In Progress - Phase 0 Complete
**Target**: Production Release Candidate by September 1, 2025
**Guiding Principle**: This is an opinionated implementation plan. Where a "right way" has been established through architectural principles or empirical testing, this document will provide clear, directive guidance to ensure development (whether by humans or AI assistants) remains aligned with the project's goals.

---

## Part 1: Production Release Goals (The "What")

This section defines the "Definition of Done" for our initial production-ready release. A successful release requires the full implementation and validation of the three **Foundational Pillars** of a durable LLM system.

### **Required Capabilities for Production Release:**

1.  **Pillar 1: Formalized Prompt Management**
    *   All agent prompts must be externalized into version-controlled `.yaml` files.
    *   No prompts may be hardcoded in Python strings.

2.  **Pillar 2: Guaranteed & Validated Structured Output**
    *   All LLM calls that require structured data must use the Function Calling/Tool Use pattern.
    *   **Directive:** The `Instructor` and `Pydantic` libraries **must** be used to compel and validate LLM outputs, completely eliminating brittle string parsing.

3.  **Pillar 3: Systematic Evaluation ("Evals")**
    *   A baseline evaluation pipeline must be in place.
    *   **Directive:** The `promptfoo` library **must** be used to test core agents against a "golden set" of documents to prevent quality regressions.

4.  **Simplified & Robust Core Workflow**
    *   The system must operate on a simple, reliable, one-document-at-a-time basis.
    *   All complex, "THICK" software components (e.g., the `BatchPlannerAgent`) are forbidden.

---

## Part 2: Phased Implementation Plan (The "How")

This is the staged roadmap for achieving our production release goals.

### **Phase 0: Reversion to THIN (Immediate Priority)**

*   **Objective**: Purge all identified THICK patterns from the codebase to restore a clean foundation.
*   **Status**: **✅ COMPLETE** (as of 2025-07-26)

| Task ID | Description | Status |
|---|---|---|
| P0-T1 | Remove Brittle Parsing Logic | **✅ Done** |
| P0-T2 | Remove Complex Batch Planner Agent | **✅ Done** |
| P0-T3 | Simplify Workflow to Single-Document Processing | **✅ Done** |

### **Phase 1: Foundational Reliability (Target: Mid-August)**

*   **Objective**: Implement the core architectural pillars that guarantee reliability and determinism.
*   **Status**: **🔄 ARCHITECTURAL PIVOT** - Moving to CSV-based THIN approach (2025-07-26)

| Task ID | Description | Status |
|---|---|---|
| P1-T1 | **Redesign Analysis Pipeline:** Implement CSV extraction from LLM analysis with simple Instructor metadata only. | **📋 PENDING** |
| P1-T2 | **Redesign Synthesis Pipeline:** LLM processes CSV directly with math verification system. | **📋 PENDING** |
| P1-T3 | **Formalize Pillar 1:** Verify that all agents, without exception, load prompts from `.yaml` files. | **✅ Done** |

**ARCHITECTURAL DECISION (2025-07-26):** After systematic debugging and THIN architecture analysis, we are **abandoning Instructor + Pydantic for complex research data** and adopting a **CSV-based approach** that aligns with core THIN principles and researcher needs.

**Key Discovery:** The Instructor/Pydantic complexity issue revealed deeper architectural misalignment - we were sliding toward THICK patterns to solve a problem that has a simpler THIN solution. The original issue (large batch synthesis context limits) is better solved through CSV + LLM intelligence.

**New Architecture:** 
- **Analysis**: LLM generates complex JSON → Extract scores → Research-grade CSV artifact
- **Synthesis**: CSV + Framework → LLM synthesis with math verification  
- **Research**: CSV download for R/pandas + LLM interpretation as starting point

**Instructor Role Clarification**: Instructor remains **permanently** for simple metadata (batch_id, timestamps, document counts) but is **permanently abandoned** for complex research data (scores, evidence, nested analysis). This is the long-term architectural pattern, not a temporary measure.

**Benefits:** THIN compliance, researcher productivity, system reliability, scalability solution.

**Implementation Plan:** See **[INSTRUCTOR_PYDANTIC_ARCHITECTURAL_FIX.md](INSTRUCTOR_PYDANTIC_ARCHITECTURAL_FIX.md)** for complete reasoning chain and 4-phase implementation roadmap.

### **Phase 2: Quality & Efficiency (Target: September 1st)**

*   **Objective**: Build the infrastructure to systematically measure and protect the quality of our LLM outputs and to begin optimizing for performance.
*   **Status**: In Progress.

| Task ID | Description | Status |
|---|---|---|
| P2-T1 | **Implement Pillar 3:** Create a `promptfoo` evaluation pipeline with an initial "golden set" of test cases for the `EnhancedAnalysisAgent`. | **✅ Done** |
| P2-T2 | **Implement Pillar 4:** Introduce a basic, rule-based model router to use faster, cheaper models for simpler tasks. | Not Started |

---

## Part 3: Current Progress (The "Where We Are")

Our systematic debugging session (2025-07-26) revealed critical architectural limitations that require fundamental design changes.

### **Major Achievements**
*   **THIN Architecture Established:** Successfully purged THICK patterns and implemented direct function call coordination
*   **Prompt Management:** All agents use externalized YAML prompts with version control
*   **Infrastructure Maturity:** Security boundaries, audit logging, artifact storage, and evaluation pipeline operational

### **Critical Blocking Issue Identified**
*   **Instructor + Pydantic Limitation:** Cannot reliably handle complex nested structures (`Dict[str, DocumentAnalysis]`)
*   **Evidence:** Despite perfect prompt engineering and ultra-explicit instructions, `document_analyses` consistently returns empty `{}`
*   **Root Cause:** Architectural mismatch between LLM output capability and Pydantic validation complexity
*   **Cache Invalidation Issues:** Cache keys only use content SHA256, missing agent version/prompt/schema changes

### **Immediate Priority**
*   **Architectural Redesign Required:** Must simplify data models to work within Instructor/Pydantic constraints
*   **Cache System Enhancement:** Implement version-aware cache invalidation
*   **Data Flow Validation:** End-to-end pipeline validation with simplified models

### **Path Forward**
See **[INSTRUCTOR_PYDANTIC_ARCHITECTURAL_FIX.md](INSTRUCTOR_PYDANTIC_ARCHITECTURAL_FIX.md)** for detailed solutions and implementation strategy.

---

## Appendix A: Current Reference Implementation Details

> This appendix contains concrete examples and implementation details that were formerly in the main architecture document. It serves as a snapshot of the *current* technical approach and is subject to change as the project evolves.

### **Core Concepts**

| Term | Plain‑English meaning |
|---|---|
| **Agent** | A stateless worker that reads a task, calls an LLM with a specific prompt, and writes the result. |
| **ThinOrchestrator** | A central coordinator that uses direct Python function calls to manage the sequence of agent operations (e.g., Analyze -> Synthesize). |
| **Artifact** | Any immutable data file (e.g., a JSON analysis result, the final report) saved by its SHA-256 hash to ensure provenance. |

### **High-Level Workflow**

The system follows a simple, linear progression for each experiment:

1.  **Initialization:** The `ThinOrchestrator` is initialized for a specific experiment. It sets up the security boundary, audit logging, and artifact storage for the run.
2.  **Sequential Analysis:** The orchestrator iterates through each document in the corpus one by one, calling the `EnhancedAnalysisAgent` for each.
3.  **Data Consolidation:** The structured data from all analysis runs is extracted and consolidated into a single, memory-efficient object.
4.  **Final Synthesis:** The `EnhancedSynthesisAgent` is called a single time with the complete, consolidated dataset to produce the final report.

### **Example `ThinOrchestrator` Logic**

```python
# A conceptual representation of the direct function call workflow.
class ThinOrchestrator:
    def run_experiment(self, experiment_path: Path):
        # 1. Initialization
        self.initialize_run(experiment_path)
        
        # 2. Sequential Analysis
        all_analysis_results = []
        for document in self.corpus:
            analysis_result = self.analysis_agent.analyze(document, self.framework)
            all_analysis_results.append(analysis_result)
            
        # 3. Data Consolidation
        consolidated_data = self.consolidate(all_analysis_results)

        # 4. Final Synthesis
        final_report = self.synthesis_agent.synthesize(consolidated_data)
        
        self.save_results(final_report)
```

### **File and Directory Structure**

The standard directory structure for a completed experiment run is as follows, ensuring clear organization and easy access to all artifacts and logs:

```
projects/<PROJECT>/<EXPERIMENT>/<RUN_ID>/
├─ corpus/            # Copies of the original input files for this run.
├─ analysis/          # Individual structured JSON analysis artifacts, one per corpus document.
├─ synthesis/         # The final, consolidated JSON object used as input for the report.
├─ reports/           # The final, human-readable academic report in Markdown format.
├─ framework/         # A copy of the framework file used for this run.
├─ logs/              # Detailed, real-time JSONL logs for the orchestrator, agents, and LLM interactions.
├─ manifest.json      # The machine-readable master record of the run, with all hashes and metadata.
└─ artifact_index.html # A human-readable index linking source documents to their analysis artifacts.
```