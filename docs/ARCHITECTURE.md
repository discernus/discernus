# SOAR: Architectural Principles and Components

This document outlines the core architectural philosophy of the Simple Atomic Orchestration Research (SOAR) platform. It is intended for developers and researchers who wish to understand the principles that guide the system's design and evolution.

## The THIN Software + THICK Intelligence Philosophy

The central principle of SOAR is **THIN Software + THICK Intelligence**. This means we strive to keep the software layer as simple and "dumb" as possible, while embedding all of the complex "intelligence" into the LLM agents and the expert-crafted prompts that guide them.

*   **THIN Software**: The Python code should be a simple, reliable, and stateless machine. It provides the *structure* for research—reading files, calling APIs, moving data—but it should not make any intelligent decisions on its own. It is a tool, like a hammer.
*   **THICK Intelligence**: All of the complex "thinking"—experimental design, methodological validation, data interpretation, statistical planning, and even error analysis—is delegated to LLMs. The prompts we write are the equivalent of a skilled carpenter wielding the hammer.

## The Hybrid Intelligence Pattern

This philosophy is implemented through a core architectural pattern we call **Hybrid Intelligence**.

**Pattern**: LLM designs the approach → Secure software executes the task → LLM interprets the results.

This pattern ensures that we get the best of both worlds: the creative, flexible, and context-aware intelligence of LLMs, and the precise, reliable, and mathematically verifiable execution of software.

## Core Architectural Components

The SOAR platform is composed of several key components, each designed to fulfill a specific role within the THIN/THICK architecture.

*   **`soar_cli.py` (The Entry Point)**: The single, user-facing entry point for all SOAR operations. It is responsible for parsing user commands and kicking off the validation and execution workflow.

*   **`ValidationAgent` (The Guardian)**: The rigorous pre-flight check for all experiments. It orchestrates all other configuration agents to ensure that an experiment is not just structurally sound, but also methodologically coherent before any analysis is run. It is responsible for the **Pre-Execution Confirmation** step, ensuring user alignment and oversight.

*   **`EnsembleOrchestrator` (The Conductor)**: The core workflow engine. Once an experiment is validated, the orchestrator takes over. It is a simple, THIN state machine that spawns the necessary analysis agents, gathers their results, and then uses a "coordination LLM" to decide on the next steps (e.g., run synthesis, perform aggregation, etc.).

*   **`ModelRegistry` (The Knowledge Base)**: A pure "knowledge" component. It reads the `models.yaml` file and serves as the single source of truth for all available models and their capabilities (cost, performance, task suitability, fallback priority). It has no execution capabilities.

*   **`LLMGateway` (The Messenger)**: A pure, stateless execution gateway. Its only job is to take a prompt and a specific model identifier and execute the API call. It now includes intelligent retry-and-fallback logic, consulting the `ModelRegistry` to gracefully handle transient API errors.

*   **`SecureCodeExecutor` (The Calculator)**: A sandboxed environment for executing Python code for statistical analysis. This is a critical component of the Hybrid Intelligence pattern, ensuring that all mathematical calculations are performed with verifiable precision, free from the risk of LLM hallucinations.

*   **`ProjectChronolog` (The Scribe)**: The tamper-evident, comprehensive audit trail for the entire project. It captures every event, from initialization to final output, into a single, master log file, ensuring complete academic provenance.

## The Pre-Execution Confirmation Workflow

To prevent wasted effort and ensure methodological rigor, all experiments run via `soar execute` must pass through the following workflow:

1.  **Comprehensive Validation**: The `ValidationAgent` runs, checking for file structure, framework coherence, and statistical plan validity.
2.  **Execution Plan Summary**: If validation passes, the `ValidationAgent` generates a summary of the full execution plan.
3.  **User Confirmation**: The CLI presents this summary to the user and requires explicit "yes" confirmation to proceed.
4.  **Execution**: Only upon user confirmation is the plan handed off to the `EnsembleOrchestrator` for execution.

This workflow embodies the core SOAR principles of rigor, transparency, and user-in-the-loop collaboration. 