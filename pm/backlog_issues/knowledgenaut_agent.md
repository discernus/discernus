# Backlog Item: Implement `knowledgenaut_agent`

**Description**

The `knowledgenaut_agent` is a specialized research agent with expertise in academic literature discovery and framework interrogation. It will use the existing `UltraThinKnowledgenaut` infrastructure to perform tasks such as searching for relevant academic papers, validating their quality, and synthesizing the findings.

**Rationale**

A key part of rigorous academic research is situating new findings within the existing body of literature. The `knowledgenaut_agent` will automate this process, allowing researchers to quickly understand the current state of knowledge and validate their own analytical frameworks against it.

**Implementation Tasks**

*   [ ] Create a new agent class, `KnowledgenautAgent`, in `discernus/agents/knowledgenaut_agent.py`.
*   [ ] The agent should accept a research question and a framework description as input.
*   [ ] Use `discernus.core.knowledgenaut.UltraThinKnowledgenaut` to perform literature searches and analysis.
*   [ ] The agent should synthesize the results into a clear, human-readable report.
*   [ ] The report should be returned as a structured dictionary containing the literature review, a list of key papers, and an assessment of the provided framework.
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml` to make it available to the `WorkflowOrchestrator`.
*   [ ] Create a unit test for the `KnowledgenautAgent` in `discernus/tests/agents/`. 