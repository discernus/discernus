# Discernus Agent Design Principles

This document outlines the architectural philosophy and design patterns for creating, organizing, and deploying agents within the Discernus system. Adherence to these principles ensures the system remains modular, maintainable, and methodologically transparent, in line with the project's core THIN (THick INtelligence, THIN software) philosophy.

---

## The Chef's Kitchen Analogy

A useful mental model for our agent architecture is that of a professional chef's kitchen. An entire restaurant (a complex research project) cannot be run by a single, all-in-one "Ultimate Kitchen Machine 5000." Professional-grade results require a combination of specialized tools and skilled, flexible staff, all managed by a head chef who knows how to coordinate them.

-   **The Head Chef:** The Orchestrator, who directs the workflow.
-   **The Recipes:** The `experiment.md` files, which define the final dish to be produced.
-   **The Staff & Tools:** The Agents, each with a specific role and capability.

This analogy helps distinguish our THIN approach from THICK frameworks, which often resemble the all-in-one machine—convenient for simple tasks but lacking the precision, control, and debuggability required for serious, publication-ready work.

---

## Agent Archetypes

We have identified three distinct agent archetypes. Choosing the correct archetype is the first step in designing a new agent.

### 1. The "Tool-Using" Agent (The Specialized Appliance)

-   **Description:** A thin, intelligent wrapper around a specific, deterministic service interaction (e.g., file I/O, database queries, API calls). Its job is highly predictable and its "intelligence" is in the custom Python code that prepares its inputs and handles its outputs.
-   **Analogy:** A high-end stand mixer or a precision immersion circulator. It does one job perfectly.
-   **Key Characteristics:**
    -   Interacts directly with the file system, databases, or external APIs.
    -   Performs a single, well-defined task.
    -   Often contains a hardcoded, specialized prompt.
-   **Governing Principle:** [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle).
-   **Examples:** `StatisticalInterpretationAgent`, `ExperimentConclusionAgent`.

### 2. The "Role-Playing" Agent (The Generalist Consultant)

-   **Description:** A minimal software shell whose behavior is almost entirely defined by a prompt from a central library (e.g., `agent_roles.py`). It is designed to be composed with other agents in complex, conversational workflows.
-   **Analogy:** A skilled but flexible line cook who can perfectly execute any recipe (prompt) they are given.
-   **Key Characteristics:**
    -   Has little to no custom logic.
    -   Behavior is emergent and context-dependent.
    -   Primed for reasoning, critique, and synthesis.
-   **Governing Principle:** [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern). The agent is the context, the prompt is the strategy.
-   **Examples:** The `moderator`, `analysis`, and `adversarial` roles defined in `agent_roles.py`.

### 3. The "Hybrid" Agent (The Standard Pattern)

-   **Description:** A combination of the first two archetypes. It has custom code for specific service interactions but loads a significant portion of its reasoning instructions from a prompt. This should be our default pattern.
-   **Analogy:** A line cook who not only follows a recipe but also knows how to operate the specialized appliances required to execute it.
-   **Key Characteristics:**
    -   Balances the reliability of code with the flexibility of prompts.
    -   Can reliably interact with the environment (like a Tool-User).
    -   Can reason flexibly about its task (like a Role-Player).
-   **Governing Principle:** A pragmatic blend of Single Responsibility and Strategy patterns.
-   **Example:** `ValidationAgent`, which uses Python to handle files but an LLM prompt to perform complex coherence checks on their content.

---

## The Agent Registry

To solve the problem of agent discovery and ensure the system is self-documenting, we will maintain a central `agent_registry.yaml`. This file acts as a machine-readable manifest of all available agents and their capabilities.

-   **Analogy:** The head chef's station (the *pass*), where they can see the capabilities of all available kitchen staff at a glance.
-   **Governing Principle:** [Dependency Injection / Service Location](https://en.wikipedia.org/wiki/Dependency_injection). The Orchestrator asks the registry for an agent with a specific capability rather than creating it directly.

An orchestrator should be "registry-aware," meaning it consults this registry to understand what agents are available and how to use them.

---

## Four Principles for Agent Design

1.  **Principle 1: Choose the Right Archetype.** When creating a new agent, first decide if it's a Tool-User, a Role-Player, or a Hybrid. This forces intentionality in its design.
2.  **Principle 2: Centralize Reusable Prompts.** General-purpose reasoning and workflow roles belong in a central library like `agent_roles.py`. Highly specialized, one-off prompts can remain inside their agent's code.
3.  **Principle 3: Hardcode Service Interactions.** An agent's Python code should handle all deterministic I/O (file paths, database queries). It should pass *content* to the LLM for reasoning, not instructions on how to get the content.
4.  **Principle 4: Register Every Agent.** Every new agent must have an entry in the `agent_registry.yaml`. This is non-negotiable and solves the discovery problem permanently.

---

## The Core Interaction Model: The Intelligent Research Assistant

Beyond the technical architecture of the agents, we must define the core principle of their interaction with the user. The system must be a trustworthy, collaborative partner, not an opaque tool. This is achieved through the **Intelligent Research Assistant** interaction model.

### The Problem: Gatekeeper vs. Ghostwriter

When a system encounters imperfect human input, it typically defaults to one of two unacceptable behaviors:

1.  **The Gatekeeper:** The system is brittle and unhelpful. It fails with an "invalid input" error and forces the user to manually debug the problem. This creates frustration and slows down the research process.
2.  **The Ghostwriter:** The system is dangerous and untrustworthy. It "helpfully" fixes the user's input in the background without their knowledge. This breaks the chain of academic provenance and means the experiment that is run is not the one the researcher specified, invalidating the results.

### The Solution: "Detect, Explain, Propose, Confirm"

Our system rejects both of these models. Instead, it operates on a principle of **interactive and transparent refinement**. It acts as a true research assistant.

The workflow is as follows:

1.  **Detect:** The system uses its intelligence to detect not just syntax errors, but *methodological or logical inconsistencies* in the human-provided assets (e.g., an experiment that calls for a review process but doesn't define the workflow).
2.  **Explain:** It clearly and concisely explains the nature of the problem to the researcher.
3.  **Propose:** It generates a concrete, actionable solution, often in the form of a code diff, showing the exact change needed to resolve the issue.
4.  **Confirm:** The system **stops** and asks for explicit user confirmation before making any changes to user-owned files. The researcher is always the final authority.

This model ensures that by the time an experiment is executed, the assets on disk are methodologically sound and have the explicit, informed consent of the researcher. Every action is logged, every change is approved, and the entire process is transparent and defensible. 