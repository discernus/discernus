# Backlog Item: Implement `RefereeAgent` for Adversarial Arbitration

**Description**

The `RefereeAgent` is an impartial arbiter that resolves disagreements between an initial analysis and an adversarial critique. It acts as a neutral third party, examining the evidence presented by both sides and making a final judgment to ensure the integrity and robustness of the findings. This concept has been a long-standing part of the project's vision for a rigorous, automated peer review process.

**Rationale**

While a two-party author/critic model (`SynthesisAgent` and `CritiqueAgent`) is valuable, a three-party model that includes a `RefereeAgent` provides a more robust simulation of academic peer review. The referee's role is not to simply revise a document, but to render a judgment on the validity of a critique, forcing a higher standard of evidence for both the synthesis and the challenge. This prevents a simple "he said, she said" scenario and moves toward a conclusion based on the merits of the arguments.

**Relationship to Other Agents**

This agent is a key component of the three-party adversarial workflow:

1.  **`SynthesisAgent`**: Acts as the **Author**, creating the initial analysis from the data.
2.  **`CritiqueAgent`**: Acts as the **Critic**, challenging the synthesis and providing counter-arguments.
3.  **`RefereeAgent`**: Acts as the **Judge**. It receives the `synthesis_text`, the `critique_text`, and the original evidence. It then arbitrates the dispute, deciding which claims are valid. Its output would be a final, adjudicated text or a set of binding recommendations for revision.

**Implementation Tasks**

*   [ ] Create a new agent class, `RefereeAgent`, in `discernus/agents/referee_agent.py`.
*   [ ] The agent should accept the `synthesis_text`, the `critique_text`, and the original data/evidence from the `workflow_state`.
*   [ ] Develop a prompt that instructs the agent to act as a neutral judge, carefully weighing the arguments and evidence from both the synthesis and the critique.
*   [ ] The agent's output should be a final, adjudicated document or a set of findings that resolves the dispute. This output should be added to the `workflow_state`.
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml`.
*   [ ] Create a unit test for the `RefereeAgent` that simulates a disagreement and verifies the agent's ability to arbitrate.

**Dependencies and Relationships**

*   This agent represents the **conclusion of a three-party (author-critic-judge) review workflow**.
*   **`CritiqueAgent`**: This agent depends on the `critique_text` produced by one or more `CritiqueAgents`. It also requires the original `synthesis_text` from the `SynthesisAgent`.
*   **Alternative Path**: This agent is an alternative to the `RevisionAgent`. A workflow would typically use one or the other to resolve the critique, not both. This agent provides a more formal arbitration. 