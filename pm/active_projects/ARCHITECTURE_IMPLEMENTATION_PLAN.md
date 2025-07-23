# Discernus Architecture - Implementation Plan

**Last Updated**: July 24, 2025
**Status**: Phase 1 - Batch Processing & Layered Synthesis Foundation
**Architectural Bible**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`

---

## 1. Executive Summary

This document outlines the phased implementation plan for the Discernus System Architecture. It serves as the active project plan, tracking tasks, implementation decisions, and technical discoveries.

The current focus is **Phase 1**, which implements the foundational elements of the new LLM-driven, batch-oriented architecture. This phase directly addresses the brittleness, performance, and security issues discovered during the initial PoC development and leverages the empirical findings from recent Gemini 2.5 experiments.

**Core Objective for Phase 1**:
Build a robust, end-to-end pipeline that demonstrates the **Batch Planner** and **Layered Synthesis** architecture, validated against the "Practical Next Experiment" outlined in the architectural bible.

---

## 2. Implementation Phases

| Phase | Title                                      | Core Deliverables                                                                                                     | Status      |
| :---- | :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :---------- |
| **1** | **Batch & Synthesis Foundation**           | `AnalyseBatchAgent`, `CorpusSynthesisAgent`, `PreTestAgent`, enhanced `OrchestratorAgent` with BatchPlanner logic.      | **In Progress** |
| **2** | **Quality Assurance & Review Loop**        | `ReviewerAgent`, `ModeratorAgent`, and the complete 3-layer synthesis pipeline with adversarial review.               | Not Started |
| **3** | **Production Hardening**                   | Comprehensive security package, advanced cost guards, multi-user support, and result retrieval system.               | Not Started |
| **4** | **Advanced Capabilities & Usability**      | CLI enhancements, non-deterministic averaging, `ValidationAgent`, `PostHocMathAgent`, and composite framework synthesis. | Not Started |

---

## 3. Phase 1 Task List: Batch & Synthesis Foundation

This task list represents the immediate work required to complete Phase 1.

### 3.1. Core Infrastructure & Agent Scaffolding
- [ ] **Create `PreTestAgent`**: Implement the agent responsible for variance estimation using synthetic text generation.
- [ ] **Create `AnalyseBatchAgent`**: Replace `AnalyseChunkAgent`. Must handle multi-document and multi-framework payloads.
- [ ] **Create `CorpusSynthesisAgent`**: Replace `SynthesisAgent`. Must aggregate `batch_summary` artifacts.
- [ ] **Refactor `OrchestratorAgent`**: Integrate the `BatchPlanner` logic.
- [ ] **Update `Router`**: Add new agent types (`AnalyseBatch`, `PreTest`, `CorpusSynthesis`) to the routing map.

### 3.2. Batch Processing Pipeline (End-to-End)
- [ ] **Implement BatchPlanner Logic**: Orchestrator must query the model registry and group documents into batches based on token estimates.
- [ ] **Implement Pre-enqueue Cache Check**: Ensure `OrchestratorAgent` checks for existing batch analysis artifacts before creating `AnalyseBatch` tasks.
- [ ] **Connect `AnalyseBatch` to `CorpusSynthesis`**: Ensure the output of Layer 1 (batch summaries) correctly triggers Layer 2 processing.

### 3.3. Key Technical Challenges & Decisions (To be resolved in Phase 1)

**This section is for logging implementation-specific technical notes, preserving the kind of insights from the original PoC status document.**

#### **The `MockRedisClient` Execution Bridge Problem**
*   **Context**: The `TaskListExecutorAgent` from the PoC correctly used an LLM to interpret a raw task list, but the LLM generated Python code that used a *mock* Redis client instead of executing against the real one.
*   **Problem**: This highlights a critical gap: how do we safely execute LLM-generated orchestration logic?
*   **Phase 1 Decision**: For Phase 1, we will sidestep direct `exec()` of LLM code. The `OrchestratorAgent` (enhanced with BatchPlanner logic) will be the sole authority for enqueuing tasks. It will use LLMs to *plan* but will execute the Redis commands itself. This avoids the security and reliability issues of executing arbitrary LLM code while we focus on the core pipeline. A `SecureCodeExecutorAgent` can be considered in a future phase.

#### **Redis Consumer Group vs. Direct Read Pattern**
*   **Context**: The PoC revealed that having agents act as consumers in a group (`xreadgroup`) for specific task IDs was unreliable.
*   **Discovery**: The correct and reliable pattern is for the `Router` to spawn an agent with a specific `task_id`, and for that agent to fetch its task directly using `xrange(stream, task_id, task_id)`.
*   **Phase 1 Decision**: All new agents must follow the direct-read (`xrange`) pattern. This is a non-negotiable implementation detail for reliability.

---

## 4. Phase 1 Definition of Done

Phase 1 will be considered complete when:
1.  The "Practical Next Experiment" from the architectural bible can be run end-to-end, from `discernus run` to the generation of a `CorpusSynthesisAgent` statistical report.
2.  The system correctly creates and processes batches of documents.
3.  The system correctly applies multiple frameworks to a single batch.
4.  All artifacts (`batch_analysis`, `corpus_synthesis`) are correctly stored in MinIO with content-addressable hashes.
5.  The implementation log in this document is updated with any new technical discoveries or decisions made during development. 