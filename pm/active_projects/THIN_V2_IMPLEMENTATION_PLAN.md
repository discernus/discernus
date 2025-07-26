# THIN v2.0 Implementation Plan (Roadmap to Production)

**Project**: Discernus Architecture Overhaul  
**Status**: In Progress - Phase 0 Underway  
**Target**: Production Release Candidate by September 1, 2025

---

## Part 1: Production Release Goals (The "What")

This section defines the "Definition of Done" for our initial production-ready release. A successful release requires the full implementation and validation of the three **Foundational Pillars** of a durable LLM system.

### **Required Capabilities for Production Release:**

1.  **Pillar 1: Formalized Prompt Management**
    *   All agent prompts must be externalized into version-controlled `.yaml` files.
    *   No prompts may be hardcoded in Python strings.

2.  **Pillar 2: Guaranteed & Validated Structured Output**
    *   All LLM calls that require structured data must use a Function Calling/Tool Use approach.
    *   The `Instructor` and `Pydantic` libraries will be used to compel and validate the LLM's output, completely eliminating brittle string parsing.

3.  **Pillar 3: Systematic Evaluation ("Evals")**
    *   A baseline evaluation pipeline using `promptfoo` must be in place.
    *   This pipeline will test our core agents against a "golden set" of documents to prevent quality regressions in both the structure and the semantic content of the analysis.

4.  **Simplified & Robust Core Workflow**
    *   The system must operate on a simple, reliable, one-document-at-a-time basis.
    *   All complex, "THICK" components (e.g., the software-based `BatchPlannerAgent`) must be removed.

---

## Part 2: Phased Implementation Plan (The "How")

This is the staged roadmap for achieving our production release goals.

### **Phase 0: Reversion to THIN (Immediate Priority)**

*   **Objective**: Purge all identified THICK patterns from the codebase to restore a clean, simple, and maintainable foundation.
*   **Status**: In Progress.

| Task ID | Description | Status |
|---|---|---|
| P0-T1 | Remove Brittle Parsing Logic | **Done** |
| P0-T2 | Remove Complex Batch Planner Agent | **Done** |
| P0-T3 | Simplify Workflow to Single-Document Processing | **Done** |

### **Phase 1: Foundational Reliability (Target: Mid-August)**

*   **Objective**: Implement the core architectural pillars that guarantee reliability and determinism.
*   **Status**: Not Started.

| Task ID | Description |
|---|---|
| P1-T1 | **Implement Pillar 2 (Validated Output):** Refactor `EnhancedAnalysisAgent` to use `Instructor` and `Pydantic` for deterministic JSON output. |
| P1-T2 | **Implement Pillar 2 (Validated Output):** Refactor `EnhancedSynthesisAgent` to use `Instructor` and `Pydantic` for deterministic Markdown report generation. |
| P1-T3 | **Formalize Pillar 1 (Prompt Management):** Verify that all agents, without exception, load prompts from `.yaml` files. |

### **Phase 2: Quality & Efficiency (Target: September 1st)**

*   **Objective**: Build the infrastructure to systematically measure and protect the quality of our LLM outputs and to begin optimizing for performance.
*   **Status**: Not Started.

| Task ID | Description |
|---|---|
| P2-T1 | **Implement Pillar 3 (Systematic Evals):** Create a `promptfoo` evaluation pipeline with an initial "golden set" of test cases for the `EnhancedAnalysisAgent`. |
| P2-T2 | **Implement Pillar 4 (The Router):** Introduce a basic, rule-based model router to use faster, cheaper models for simpler tasks (e.g., JSON extraction, if needed). |

---

## Part 3: Current Progress (The "Where We Are")

Our recent debugging and strategic sessions have been highly productive, leading to a significant leap in architectural maturity.

*   **Key Insight Gained:** We have moved from a reactive, bug-fixing posture to a proactive, architecturally-driven approach. We have identified and documented the 8 Pillars of a Durable LLM System, which now serve as our "constitution."
*   **Core Problem Solved:** We have moved beyond brittle string parsing and have a clear plan to implement a deterministic, tool-based approach for all structured data exchange with LLMs.
*   **THICK Patterns Purged:** We have successfully identified and removed several "THICK" anti-patterns from the codebase, including the complex `BatchPlannerAgent` and the manual JSON extraction logic, simplifying the system dramatically.
*   **Path to Production:** We have a clear, phased, and actionable plan to achieve a production-ready release by our target date of September 1st.