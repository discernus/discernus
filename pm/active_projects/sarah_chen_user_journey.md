# The Sarah Chen User Journey: A Parable for System Design

This document captures a critical user journey constructed to test the philosophical and architectural principles of the Discernus platform. "Sarah Chen" is a persona representing a competent, expert researcher who wants to use the platform for a real-world scientific task. Her journey reveals the core value proposition of the system and clarifies what it must—and must not—do.

## 1. The Researcher's Goal

Sarah Chen is a political scientist who has published extensively on ideological rhetoric. She downloads Discernus to test a hypothesis: is the well-regarded Constitutional Health Framework (CHF) biased against conservative or progressive ideologies?

To do this, she needs to add a new dimension to the framework that classifies the speaker's ideology. She is an expert in this domain and has her own robust, nuanced mental model of what defines these categories.

## 2. The Seductive Shortcut

Sarah's friend Lars, an LLM researcher, gives her some pragmatic advice: "Don't bother defining a huge list of linguistic markers. It's a deep hole. Just trust the LLM to know what 'progressive' or 'conservative' rhetoric is. It's read everything. Just ask it to classify the text."

This advice is appealing because it is easy and leverages the power of the tool. Following it, Sarah creates a forked version of the framework called `chf_v1.1_ideology_enhanced.md`. She updates the narrative and modifies the `analysis_prompt` to instruct the agent to classify the speaker's ideology, but provides no explicit markers.

## 3. The Dangerous False Positive

To check her work, Sarah uploads her modified framework and the official Discernus `FRAMEWORK_SPECIFICATION.md` to a generic LLM like ChatGPT and asks, "Is this a valid framework?"

The LLM, an excellent pattern-matcher, correctly identifies that she has followed the *syntactic* rules of the specification and gives her a confident "Yes." This provides a dangerous false sense of security.

## 4. The First-Order Insight: The Need for Methodological Guardrails

The first-order insight is that the Discernus system cannot be a passive tool. It needs an immune system. The validation system should act as a methodological gatekeeper. In this initial conception, the agent would reject Sarah's framework with a clear error:

**Initial (Incorrect) Response:** `REJECTED: Framework dimension "Ideological Stance" is not methodologically falsifiable. You must provide explicit linguistic markers.`

This response, while technically correct from a rigid-rules perspective, is ultimately paternalistic and fails to serve the expert user.

## 5. The Second-Order Insight: The Expert Workflow

The deeper insight comes from understanding Sarah's true intent. She is not a novice asking the LLM to discover what "progressive" means. She is an expert using the LLM as a tireless research assistant to perform a high-throughput classification task.

Her real workflow is:
1.  **Generate First Pass**: Use the LLM to apply ideological labels to thousands of documents.
2.  **Check the Receipts**: Use her own expertise to audit the LLM's classifications, correcting them where necessary.
3.  **Analyze**: Use the final, human-validated data set to conduct her primary analysis of framework bias.

The system, as initially conceived, has no way to support this legitimate, expert-driven workflow.

## 6. The Core Philosophical Shift: From Gatekeeper to Virtual Colleague

This journey forces a critical refinement of the platform's philosophy.

-   **The Goal is NOT Infallibility**: The system does not need to be perfect or prevent all user errors. It just needs to be **20% better than the alternative** (e.g., paying undergraduates to manually code speeches).
-   **The Goal is Informed Consent**: The system's primary duty is not to *prevent* a researcher from making a choice, but to ensure they understand the **trade-offs** of that choice.
-   **The User is a Competent Professional**: We must build for a peer, not a novice.

Therefore, the `PreTestAgent`'s role shifts from a rigid "Gatekeeper" to a helpful "Peer Reviewer." It does not reject Sarah's project. Instead, it generates a permanent **Methodological Advisory Report** that becomes part of the run's provenance.

**Corrected Response:** `PROCEEDING WITH ADVISORIES. The dimension "Ideological Stance" relies on the agent's latent knowledge, as no explicit markers were provided. The resulting classifications are not grounded in an explicit researcher-defined model and should be carefully validated before use in publication.`

This respects Sarah's expertise, allows her to proceed with her valid workflow, and ensures that the methodological trade-offs are documented for future reference.

## 7. Enshrined Architectural Principles

This user journey leads us to three core principles that must guide all future development:

1.  **English is our Programming Language**: The system is controlled through structured, human-readable prose. Intelligence lives in the words, not in complex code.
2.  **Humans are our Operating System**: The platform serves and empowers competent professionals. It trusts their judgment and workflows.
3.  **The Platform is a Virtual Colleague**: It acts as a tireless assistant, offering professional advice and handling tedious tasks, but the final scientific judgment and validation always rests with the human researcher. 