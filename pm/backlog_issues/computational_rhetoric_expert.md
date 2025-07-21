# Backlog Item: Implement `computational_rhetoric_expert`

**Description**

The `computational_rhetoric_expert` is an agent specialized in the analysis of rhetorical devices and persuasive discourse within a corpus. This agent will provide a more nuanced understanding of the texts being analyzed by focusing on how language is used to persuade and influence.

**Rationale**

While other agents may focus on the substance of an argument, the `computational_rhetoric_expert` will provide a complementary analysis of its style and structure. This will enable a more complete and multi-faceted understanding of the texts, which is particularly important in fields like political science, marketing, and communication.

**Implementation Tasks**

*   [ ] Create a new agent class, `ComputationalRhetoricExpert`, in `discernus/agents/computational_rhetoric_expert.py`.
*   [ ] The agent should accept a text or corpus as input.
*   [ ] Implement logic to identify and analyze rhetorical devices (e.g., metaphors, analogies, appeals to emotion). This may involve using existing NLP libraries or prompting an LLM with a specialized role.
*   [ ] The agent should produce a report summarizing the rhetorical strategies used in the text.
*   [ ] The output should be a structured dictionary containing the analysis.
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml`.
*   [ ] Create a unit test for the `ComputationalRhetoricExpert` in `discernus/tests/agents/`. 