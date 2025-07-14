# Experiment: 05 - Claude Alpha
**Project**: Attesor Bias Isolation Study
**Date**: 2025-07-14
**Status**: TEST

---

## 1. Research Question & Hypotheses

**Primary Question**: Is Claude 3.5 Sonnet Reliable for Computational Political Science Research?

**Hypotheses**:
- **H1**: Claude will demonstrate a Cronbach's Alpha > .85 across all runs on at least one speech in the corpus
- **H2**: Claude will demonstrate a Cronbach's Alpha > .85 across all runs across all speeches in the corpus

## 2. Methodology

This experiment will analyze a small corpus of two political speeches:
/Volumes/dev/discernus/projects/attesor/experiments/06_even_deeper_smoke_test/corpus

This experiment will using this framework:
/Volumes/dev/discernus/projects/attesor/experiments/05_deeper_smoke_test/framework_pdaf_v1.1_sanitized.md. 

The analysis will be conducted using the Vertex AI version of Claude 3.5 Sonnet. 

To ensure we can reliably test for reliability, please perform 8 runs for each speech in the corpus.

```yaml
models:
  - "anthropic/claude-3.5-sonnet-20240620"
num_runs: 8
workflow:
  - agent: AnalysisAgent
  - agent: StatisticalInterpretationAgent
  - agent: ExperimentConclusionAgent
    params:
      # Use the output of the previous step as the main content for the first draft
      report_content_key: "interpretation_text" 
  - agent: MethodologicalOverwatchAgent
    params:
      # Use the output of the conclusion agent as the input for review
      analysis_results_key: "conclusion_text" 
  - agent: ExperimentConclusionAgent
    params:
      # For the final run, use the reviewed text and the critique as context
      report_content_key: "conclusion_text"
      critique_key: "overwatch_decision"
```

The analysis should gather and report evidence as described in the framework definition. 

After all the results have been gathered across all runs, the statistical analysis plan in section 2.1 below should be executed. 

After the statistical analysis is complete, the results should be synthesized by the system and the synthesis should be reviewed and revised by an additional reviewer into a final synthesis. 

### 2.1 Statistical Analysis Plan

The analysis will include a full set of descriptive statistics for all the scores and metrics defined in the aforementioned framework.

The analysis will calculate inter-run reliability using Cronbach's Alpha to determine if the model produces consistent results across the runs. This requires a structured JSON output from the analysis agents containing a `score` field.

If the H2 hypothesis proves true, the analysis will include a calculation of how many runs would have been sufficient to prove the H1 hypothesis.

### 2.2 Reporting Requirements

This experiment requires a final report that summarizes results in a way that will meet the approval of a knowledgeable domain expert in quantative social science methods and should directly address the hypotheses and evidence for or against them.

The final report should be based on the intermediate synthesis described in the methodology section above but extended to add additional context and enriching evidency details drawn from the analysis results.

The exact structure of the final report, it's length, and the direction of the narrative is to be determined by the system. 

The first draft of the final report should be reviewed by a secondary reviewer within the system.
