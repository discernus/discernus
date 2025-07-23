# Discernus Architecture - Implementation Plan

**Last Updated**: July 24, 2025
**Status**: Phase 2 - Batch Intelligence & Dynamic Orchestration
**Architectural Bible**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`

---

## 1. Executive Summary

This document outlines the phased, question-driven implementation plan for the Discernus System Architecture. It serves as the active project plan, tracking tasks, component status, and key technical decisions.

The current focus is **Phase 2**, which builds the foundational agents and proves the core pipeline from batch analysis to a single, deterministic synthesis output. This phase is designed to be a verifiable "hello world" for the new architecture, establishing a solid base before adding the complexity of dynamic orchestration and adversarial review.

**Core Objective for Phase 1**:
To answer "yes" to a sequential chain of questions that culminates in a single, linear workflow from one batch of documents to one deterministic statistical report, proving the core agent mechanics work as designed.

---

## 2. Definitive Agent & Infrastructure Inventory

This is the definitive list of components required for the full architecture.

### Core THIN Infrastructure (Python Services)

| Component | Status | Function |
| :--- | :--- | :--- |
| **`Router`** | **✅ UPGRADED - Phase 2 Ready** | Listens to Redis streams and spawns the correct agent container based on task type. Added `analyse_batch` and `corpus_synthesis` routing. |
| **`Execution Bridge`** | **🟢 NEW - Phase 2 In-Progress** | Thin script (`scripts/execution_bridge.py`) that translates an LLM's plan into Redis tasks. Replaces deprecated agents. |
| **`Artefact Storage`** | **Existing, functioning** | Provides content-addressable storage (put/get by SHA-256 hash). |

### Tier 1: Batch Analysis Agents (LLM-Driven)

| Agent | Status | Function |
| :--- | :--- | :--- |
| **`PreTestAgent`** | **🟡 SCAFFOLDED - Phase 2 In-Progress** | Performs variance estimation to recommend the optimal number of runs. |
| **`AnalyseBatchAgent`**| **✅ BUILT & VALIDATED - Phase 1 Complete** | Workhorse agent for multi-document, multi-framework analysis. **Output is structured data only.** |

### Tier 2: Statistical Synthesis Agent (LLM-Driven)

| Agent | Status | Function |
| :--- | :--- | :--- |
| **`CorpusSynthesisAgent`**| **✅ BUILT & VALIDATED - Phase 1 Complete** | Performs **deterministic mathematical aggregation** of structured data from all Layer 1 batches. |

### Tier 3: Quality Assurance & Synthesis Agents (LLM-Driven)

| Agent | Status | Function |
| :--- | :--- | :--- |
| **`ReviewerAgent`** | **New, needs to be built** | Provides adversarial critique of the finalized Layer 2 statistical report. |
| **`ModeratorAgent`** | **New, needs to be built** | Reconciles reviews and performs the **final qualitative synthesis** to produce the academic narrative. |

### Tier 4: Orchestration Intelligence Agent (LLM-Driven)

| Agent | Status | Function |
| :--- | :--- | :--- |
| **`OrchestratorAgent`**| **✅ UPGRADED - Phase 2 Ready** | The **master planning LLM**. It receives the experiment, calls the `PreTestAgent`, and generates the complete, parallelized execution plan for the `Execution Bridge`. |

---

## 3. Phased Implementation Plan (Question-Driven)

This plan is a series of gates. We only proceed to the next phase once all questions in the current phase can be answered "yes".

### Phase 1: Foundational Agent Implementation & Core Pipeline - ✅ COMPLETE

**Goal:** To prove that the new, core agent types (`AnalyseBatchAgent`, `CorpusSynthesisAgent`) can execute a single, linear workflow from one batch of documents to one synthesis report.

**Outcome: SUCCESS.** All four validation questions were answered "yes" by the automated test runner (`scripts/phase1_test_runner.py`), confirming the foundational pipeline is sound.

**Definition of Done for Phase 1:** We can reliably execute a single, manually-constructed batch analysis and have it result in a final, statistically-sound synthesis report, with all intermediate artifacts correctly stored and linked.

## 📊 Phase 1 Implementation Status (Concluded)

### ✅ Components Completed & Validated

1. **`AnalyseBatchAgent`** - `agents/AnalyseBatchAgent/main.py`
   - ✅ Multi-document, multi-framework batch processing
   - ✅ Structured data output only (no synthesis)
   - ✅ External prompt template (`prompt.yaml`)
   - ✅ Redis task processing with proper error handling
   - ✅ MinIO artifact storage integration
   - ✅ Based on empirical validation (up to 341 documents per batch)

2. **`CorpusSynthesisAgent`** - `agents/CorpusSynthesisAgent/main.py`
   - ✅ Deterministic mathematical aggregation
   - ✅ Statistical report output only (no qualitative narrative)
   - ✅ External prompt template with statistical computation instructions
   - ✅ Cross-batch data validation and error handling
   - ✅ Cost-optimized model usage (gemini-2.5-flash)

3. **Router Updates** - `scripts/router.py`
   - ✅ Added `analyse_batch` and `corpus_synthesis` agent routing
   - ✅ Maintains existing agent compatibility

4. **Testing Framework** - `scripts/phase1_test_runner.py`
   - ✅ Implements all 4 Phase 1 validation questions
   - ✅ Fully automated testing workflow with clear success criteria
   - ✅ Artifact validation and structure checking
   - ✅ Full pipeline testing capability

### ⚙️ Phase 1 Technical Decisions & Refinements

1.  **File Handling - "Binary-First Principle" (Mandatory)**:
    *   **Decision**: All file content MUST be processed as raw binary data, base64 encoded before LLM submission.
    *   **Impact**:
        *   All agents receive file content as base64 strings regardless of apparent format.
        *   LLMs handle all format detection and content decoding internally.
        *   Zero conditional logic based on file type, encoding, or format assumptions.
    *   **Status**: This is a **mandatory** architectural principle with zero exceptions. The negligible token cost overhead (33% increase = fractions of a cent) is vastly outweighed by architectural simplicity and THIN compliance.

---

### Phase 2: Batch Intelligence & Dynamic Orchestration

**Goal:** To empower the `OrchestratorAgent` (the LLM) with the intelligence to automatically break down a large experiment into optimal batches and manage the entire fan-out/fan-in process via the `Execution Bridge`.

**High-Priority Tasks for Phase 2:**
- **Automate the orchestration pipeline:** Fully implement the `Execution Bridge` to translate the `OrchestratorAgent`'s plans into Redis tasks, eliminating all manual `input()` steps from the testing workflow.
- **Testing Framework**: Create `scripts/phase2_test_runner.py` to validate the entire dynamic orchestration pipeline.

**Chain of Questions to Verify Success:**

1.  **Can the `PreTestAgent` analyze a corpus sample and produce a statistically-grounded `recommend_runs` value?**
    *   *Test:* Point the `PreTestAgent` at a sample of the corpus.
    *   *Success:* It returns a JSON object with a justifiable integer for `recommend_runs`.

2.  **Does the `OrchestratorAgent` (LLM) generate a plan that correctly references model registry parameters like `context_window`?**
    *   *Test:* Trigger an experiment run and examine the natural language plan produced by the orchestrator LLM.
    *   *Success:* The plan's text explicitly mentions batching documents based on the model's known capabilities.

3.  **Can the `Execution Bridge` correctly interpret the LLM's plan and create the right number of `AnalyseBatch` tasks in Redis?**
    *   *Test:* Run an experiment with a corpus large enough to require multiple batches.
    *   *Success:* We observe in Redis that the correct number of distinct `AnalyseBatch` tasks are created.

4.  **After all batches are processed, does the `OrchestratorAgent` correctly generate a final plan to "fan-in" all the results into a single `CorpusSynthesis` task?**
    *   *Test:* Run the same multi-batch experiment to completion.
    *   *Success:* We verify that the `Execution Bridge`, following the LLM's plan, creates only **one** `CorpusSynthesis` task, and that its payload contains the artifact hashes from **all** completed `AnalyseBatch` tasks.

**Definition of Done for Phase 2:** We can provide an experiment to the `OrchestratorAgent`, and it will autonomously plan, execute (via the bridge), and aggregate the results from multiple parallel batches into a single, unified statistical synthesis.

---

### Phase 3: Quality Assurance & Moderated Review Loop

**Goal:** To implement the complete 3-layer synthesis pipeline, ensuring that every analysis is stress-tested and quality-assured before being finalized.

**High-Priority Tasks for Phase 3:**
- **Adversarial review**: `ReviewerAgent` and `ModeratorAgent`.
- **Production-grade process management**: Investigate and integrate `Supervisor` to replace `subprocess.Popen` for robust agent spawning.
- **Comprehensive security package**: Implement the static policy gates, runtime sentinel, and sandboxing outlined in the architecture.

**Chain of Questions to Verify Success:**

1.  **Upon completion of the `CorpusSynthesisAgent`, does the system automatically trigger the Layer 3 Review process?**
    *   *Test:* A successful Layer 2 synthesis must result in the creation of new tasks for Layer 3.
    *   *Success:* We observe two new `Reviewer` tasks and one `Moderator` task being enqueued.

2.  **Do the two adversarial `ReviewerAgent` instances produce distinct, critical reviews of the statistical report?**
    *   *Test:* Let the review agents run.
    *   *Success:* We examine the two resulting `review` artifacts and confirm they offer different analytical perspectives on the same set of numbers.

3.  **Does the `ModeratorAgent` successfully ingest both critiques and the statistical report to produce the final, qualitative synthesis?**
    *   *Test:* Let the `ModeratorAgent` run.
    *   *Success:* A final, comprehensive report is created that contains the **qualitative narrative and interpretation**, acknowledging the reviewers' points and grounding its conclusions in the Layer 2 statistics.

4.  **Is the entire debate and final report captured in a human-readable audit trail artifact?**
    *   *Test:* Check the artifacts for the run.
    *   *Success:* An HTML or Markdown file exists that correctly formats the entire conversation from the Layer 2 report through the final moderated synthesis.

**Definition of Done for Phase 3:** A full experiment run now produces a final, quality-assured, and auditable synthesis report that transparently separates its statistical foundation from its qualitative interpretation. 