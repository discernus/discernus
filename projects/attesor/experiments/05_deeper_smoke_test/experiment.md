# Experiment: 05 - Deeper Architectural Smoke Test
**Project**: Attesor Bias Isolation Study
**Date**: 2024-07-17
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

This experiment will analyze a small corpus of two political speeches using the PDAF v1.1 framework. The analysis will be conducted using a matrix of three different models from three distinct provider types, with two runs for each combination to test for reliability.

We will use our preferred top-tier managed model (the Vertex AI version of Claude 3.5 Sonnet), the specialized uncensored reasoning model from OpenRouter (Perplexity's r1-1776), and our local Mistral model. To ensure we can test for reliability, please perform two runs for each model. This experiment requires a full adversarial synthesis at the end.

The primary goal is not the analytical substance of the results, but the validation of the end-to-end system architecture. However, we do hope that the final report will be substantive with regard to analysis of the corpus and be human readable and make sense to an academic reviewer.

### 2.1. Statistical Analysis Plan

The analysis will calculate inter-run reliability using Cronbach's Alpha to determine if the models produce consistent results across the two runs. This requires a structured JSON output from the analysis agents containing a `score` field. 
---
**Generated Configuration (for reproducibility):**
```yaml
models:
- vertex_ai/gemini-2.5-pro
- anthropic/claude-3-5-sonnet-20240620
num_runs: 2
remove_synthesis: false
```
