# Backlog Item: Modify `ExperimentConclusionAgent` for Adversarial Workflow

**Description**

As part of the adversarial synthesis workflow, the `ExperimentConclusionAgent` needs to be updated. It will serve as the final step, consuming all the artifacts from the workflow—including the `revised_synthesis_text` and the `critique_text`—to produce its final methodological audit.

**Rationale**

Incorporating the peer review process into the final audit provides a complete picture of the research process. It allows the `ExperimentConclusionAgent` to comment on the rigor of the synthesis and critique steps, adding another layer of validation to the final output.

**Implementation Tasks**

*   [ ] Modify the `ExperimentConclusionAgent` in `discernus/agents/experiment_conclusion_agent.py`.
*   [ ] Update its `execute` method to accept the `revised_synthesis_text` and `critiques` from the `workflow_state`.
*   [ ] Update the agent's prompt to instruct it to incorporate the peer review artifacts into its final audit.
*   [ ] Ensure the agent's output, the `audit_text`, reflects the new inputs.
*   [ ] Update the unit tests for the `ExperimentConclusionAgent` to cover the new functionality.

**Dependencies and Relationships**

*   This agent is the **final step** in the adversarial synthesis workflow.
*   It is dependent on the outputs of the preceding agents, specifically the `critiques` from the `CritiqueAgent` and the final adjudicated text from either the **`RevisionAgent`** or the **`RefereeAgent`**.
*   Its purpose is to provide a meta-analysis of the entire research and review process. 