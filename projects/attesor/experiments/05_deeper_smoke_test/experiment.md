# Experiment: 05 - Deeper Architectural Smoke Test
**Project**: Attesor Bias Isolation Study
**Date**: 2025-07-14
**Status**: DESIGN

---

## 1. Research Question & Hypotheses

**Primary Question**: Does the new intelligent orchestration pipeline function correctly across a multi-provider, multi-run analysis matrix?

**Hypotheses**:
- **H1**: The `ExecutionPlannerAgent` will correctly generate a cost and time estimate and a detailed execution plan for a multi-provider model set (Vertex AI, OpenRouter, Ollama).
- **H2**: The `EnsembleOrchestrator` will successfully execute the plan, making calls to all three provider types.
- **H3**: The `MethodologicalOverwatchAgent` will successfully review the initial results and allow the run to proceed.
- **H4**: The `StatisticalInterpretationAgent` and `ExperimentConclusionAgent` will correctly process the results and append their analyses to create a single, comprehensive final report.

## 2. Methodology

This experiment will analyze a small corpus of two political speeches using this framework:

/Volumes/dev/discernus/projects/attesor/experiments/05_deeper_smoke_test/framework_pdaf_v1.1_sanitized.md. 

The analysis will be conducted using the Vertex AI version of Claude 3.5 Sonnet. To ensure we can test for reliability, please perform six runs for each speech. 

### 2.1. Statistical Analysis Plan

The analysis will calculate inter-run reliability using Cronbach's Alpha to determine if the models produce consistent results across the two runs. This requires a structured JSON output from the analysis agents containing a `score` field. 


### 2.2 Reporting Requirements

This experiment requires a final report that summarizes results in a way that will make sense to an academic reviewer and directly addresses the hypotheses.
