# Backlog Item: Implement `RevisionAgent` for Adversarial Workflow

**Description**

The `RevisionAgent` is a role-playing agent that takes the original `synthesis_text` and the `critique_text` (from one or more `CritiqueAgents`) and generates a `revised_synthesis_text`. It is prompted to act as a diligent author, addressing the peer reviewer's concerns and strengthening the original argument.

**Rationale**

This agent closes the loop on the peer review simulation. It incorporates the feedback from the critiques to produce a stronger, more refined synthesis. This step is crucial for turning the adversarial feedback into a constructive improvement of the research output.

**Implementation Tasks**

*   [ ] Create a new agent class, `RevisionAgent`, in `discernus/agents/revision_agent.py`.
*   [ ] The agent should take the `synthesis_text` and the list of `critiques` from the `workflow_state` as input.
*   [ ] It should prompt an LLM to revise the original synthesis based on the critiques.
*   [ ] The agent's output should be the `revised_synthesis_text`, which is added to the `workflow_state`.
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml`.
*   [ ] Create a unit test for the agent.

**Dependencies and Relationships**

*   This agent represents the **conclusion of a two-party (author-critic) review workflow**.
*   **`CritiqueAgent`**: This agent depends on the `critique_text` produced by one or more `CritiqueAgents`.
*   **Alternative Path**: This agent is an alternative to the `RefereeAgent`. A workflow would typically use one or the other to resolve the critique, not both. 