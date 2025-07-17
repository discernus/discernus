# Adversarial Synthesis Workflow Design
**A Peer Review Simulation for the WorkflowOrchestrator**

**Date**: July 17, 2025
**Status**: Proposed

## 1. Objective

To enhance the academic rigor of the `WorkflowOrchestrator` by implementing an automated, multi-agent peer review simulation. This process, known as adversarial synthesis, will identify weaknesses, uncover alternative interpretations, and improve the quality of the final analytical report before it is generated.

This design translates the implicit adversarial architecture of the `EnsembleOrchestrator` into an explicit, modular workflow for the `WorkflowOrchestrator`.

## 2. Triggering the Adversarial Workflow

The adversarial workflow will be triggered if the `experiment.md` contains a specific configuration block:

```yaml
workflow:
  adversarial_synthesis: true
  critique_agents: 2 # Number of independent critiques to generate
```

If this block is not present, the system will default to the current simple, linear workflow.

## 3. New and Modified Agent Roles

This workflow introduces new specialized agent roles:

### a. `SynthesisAgent` (New)
- **Archetype**: Role-Playing
- **Description**: Consumes the raw output from all `AnalysisAgent` runs and generates a single, coherent synthesis of the findings. It identifies the main themes, points of agreement, and points of disagreement across the different models and runs.
- **Inputs**: `analysis_results` from `workflow_state`.
- **Outputs**: `synthesis_text` (a markdown document) added to `workflow_state`.

### b. `CritiqueAgent` (New)
- **Archetype**: Role-Playing
- **Description**: An adversarial agent whose sole purpose is to find flaws in the `synthesis_text`. It is prompted to act as a skeptical peer reviewer, looking for logical fallacies, missed evidence, alternative interpretations, and unsubstantiated claims.
- **Inputs**: `synthesis_text` and original `analysis_results` from `workflow_state`.
- **Outputs**: `critique_text` added to `workflow_state`. The orchestrator will spawn multiple `CritiqueAgents` if requested.

### c. `RevisionAgent` (New)
- **Archetype**: Role-Playing
- **Description**: Takes the original `synthesis_text` and the `critique_text` and generates a `revised_synthesis_text`. It is prompted to act as a diligent author, addressing the peer reviewer's concerns and strengthening the original argument.
- **Inputs**: `synthesis_text`, `critique_text` from `workflow_state`.
- **Outputs**: `revised_synthesis_text` added to `workflow_state`.

### d. `ExperimentConclusionAgent` (Modified Role)
The `ExperimentConclusionAgent` will be the final step. Its prompt will be updated to take the `revised_synthesis_text` and the `critique_text` as additional inputs, allowing it to include the peer review process in its final methodological audit.

## 4. The Adversarial Workflow Sequence

The workflow in `discernus_cli.py` will be dynamically constructed based on the `experiment.md` configuration. If `adversarial_synthesis` is enabled, the workflow will be:

1.  **`AnalysisAgent`**: Runs as normal.
2.  **`MethodologicalOverwatchAgent`**: Runs as normal.
3.  **`SynthesisAgent`**: Generates the initial summary.
4.  **`CritiqueAgent` (xN)**: Runs N times in parallel, generating N independent critiques.
5.  **`RevisionAgent`**: Takes the original synthesis and all critiques to produce a single, improved revision.
6.  **`StatisticalAnalysisAgent`**: Runs as normal.
7.  **`StatisticalInterpretationAgent`**: Runs as normal, but its output will now become the *body* of the final report, not the whole report.
8.  **`ExperimentConclusionAgent`**: Consumes all artifacts, including the revision and critiques, to produce the final audit.

The `WorkflowOrchestrator`'s `_save_final_artifacts` method will then be responsible for assembling the final report from the `revised_synthesis_text`, the interpretation, and the audit.

## 5. State Management

The `workflow_state` dictionary is central to this process. Each agent adds its output to the state, making it available for subsequent agents:

- `AnalysisAgent` -> `analysis_results`
- `SynthesisAgent` -> `synthesis_text`
- `CritiqueAgent` -> `critiques` (a list of strings)
- `RevisionAgent` -> `revised_synthesis_text`
- `StatisticalInterpretationAgent` -> `interpretation_text`
- `ExperimentConclusionAgent` -> `audit_text`

## 6. Implementation Plan

This design can be implemented incrementally:

1.  **Create Agents**: Implement the new `SynthesisAgent`, `CritiqueAgent`, and `RevisionAgent` classes and add them to the `agent_registry.yaml`.
2.  **Update CLI**: Add the logic to `discernus_cli.py` to read the `workflow` configuration from `experiment.md` and dynamically construct the agent list.
3.  **Update Orchestrator**: Modify `_save_final_artifacts` to assemble the final report from the new components (`revised_synthesis_text`, `interpretation_text`, `audit_text`).
4.  **Update ConclusionAgent**: Update the prompt for the `ExperimentConclusionAgent` to incorporate the peer review artifacts.

This design provides a clear, THIN-compliant path to restoring the sophisticated adversarial review capabilities of the past within a modern, flexible, and maintainable architecture. 