# Minimum Viable Architecture (MVA) Implementation Plan

**Date**: July 16, 2025
**Status**: Chartered

## 1. Overview & Guiding Philosophy

This document outlines the implementation plan for the Discernus Minimum Viable Architecture (MVA). Our guiding philosophy is the **"Show Your Work" Pattern**. This is a purely THIN approach that solves the core challenge of reliable data extraction from LLM analyses.

Instead of trying to parse natural language, we will require the LLM to use its own internal code interpreter to generate a numerical score. It must then return **both the code it wrote and the result it got** in a structured format. Our software's only job is to verify this result with our own `SecureCodeExecutor`, eliminating parsing entirely and maximizing provenance.

This approach is more robust, more elegant, and more aligned with our core principles than any previous plan.

## 2. Bounding the Domain: MECE Use Cases

Our MVA will be designed to service the most critical use cases first, while being built on a foundation that can expand to cover all four.

| | **Simple Workflow** | **Complex Workflow** |
| :--- | :--- | :--- |
| **Analyze Content** | **1. The "Quick Look"** | **2. The "Standard Study"** |
| **Analyze Process** | **3. The "Framework Bake-off"** | **4. The "Methodological Test"** |

*   Our MVA must excel at use cases **#1 and #2**.

## 3. Phased Implementation Plan

### **Phase 1: Implement the "Show Your Work" Pattern**
*   **Goal**: Refactor the core analysis workflow to use the "Show Your Work" pattern.
*   **Actions**:
    1.  Modify the prompt in `EnsembleOrchestrator._run_analysis_agent` to instruct the LLM to return a structured object containing `analysis_text` and `score_calculation: {code, result}`.
    2.  Modify the logic in `EnsembleOrchestrator._run_analysis_agent` to receive this object.
    3.  Call the `SecureCodeExecutor` to run the `code` from the response and verify it matches the `result`.
    4.  Add the verified score to the agent's return dictionary.
    5.  Clean up the now-obsolete "Two-Step" extraction logic from the `EnsembleOrchestrator` and `StatisticalAnalysisAgent`.
*   **Definition of Done**: The `simple_experiment` runs successfully with the `EnsembleOrchestrator`, producing a valid `statistical_analysis_results.json` file where the score has been extracted and verified using this new method.

### **Phase 2: Establish the `WorkflowOrchestrator` Foundation**
*   **Goal**: Migrate the now-working "Show Your Work" logic into the more flexible `WorkflowOrchestrator`.
*   **Actions**:
    1.  Create a dedicated `AnalysisAgent` class.
    2.  Move the prompt and verification logic from the `EnsembleOrchestrator` into this new agent.
    3.  Modify `discernus_cli.py` to use the `WorkflowOrchestrator` and a simple, default workflow.
*   **Definition of Done**: The `simple_experiment` runs successfully using the `WorkflowOrchestrator`.

### **Phase 3: Implement the Planner Agent & Event-Driven Capabilities**
*   **Goal**: Achieve the full MVA by implementing the "Planner Agent" and the "Walkie-Talkie" patterns.
*   **Actions**:
    1.  Enhance `ProjectCoherenceAnalyst` to generate a default workflow from a natural language goal.
    2.  Implement the Redis Pub/Sub channel for outlier detection.
*   **Definition of Done**: All original MVA deliverables (functional core, planner agent, and operational walkie-talkie) are met.

## 4. MVA Definition of Done (Overall)

The MVA project is "Done" when Phase 3 is complete and the system can robustly execute our core use cases using a flexible, planner-driven, and event-aware architecture. 