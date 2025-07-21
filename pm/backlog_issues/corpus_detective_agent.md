# Backlog Item: Implement `corpus_detective_agent`

**Description**

The `corpus_detective_agent` is an expert agent responsible for inspecting user-provided corpora at ingestion time. Its primary function is to identify document types, assess quality issues, and detect any gaps in metadata. This agent will leverage the existing `CorpusInspector` infrastructure, which provides robust file reading capabilities for handling messy, real-world directories.

**Rationale**

Automating the initial inspection of corpora is a critical step in ensuring the quality and reliability of research conducted with Discernus. By identifying potential issues early, this agent will help researchers avoid errors and improve the overall integrity of their findings.

**Implementation Tasks**

*   [ ] Create a new agent class, `CorpusDetectiveAgent`, in `discernus/agents/corpus_detective_agent.py`.
*   [ ] The agent should accept a corpus path as input.
*   [ ] Utilize `discernus.core.corpus_inspector.CorpusInspector` to scan the corpus directory.
*   [ ] Implement logic to analyze the findings from the `CorpusInspector` and generate a human-readable summary of the corpus's contents and quality.
*   [ ] The agent should return a structured dictionary containing metadata about the corpus (e.g., file types, count, quality score, potential issues).
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml` so it can be used by the `WorkflowOrchestrator`.
*   [ ] Create a unit test for the `CorpusDetectiveAgent` in `discernus/tests/agents/`. 