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

This experiment will analyze a small corpus of two political speeches using the local `framework_pdaf_v1.1_sanitized.md` file. The analysis will be conducted using the Vertex AI version of Claude 3.5 Sonnet. To ensure we can reliably test for reliability, please perform 8 runs for each speech in the corpus.

The analysis process will proceed in the following stages, in this exact order:
1.  **Analysis**: The `AnalysisAgent` will analyze each text.
2.  **Statistical Calculation**: The `StatisticalAnalysisAgent` will calculate reliability scores (Cronbach's Alpha) and descriptive statistics from the analysis results.
3.  **Initial Interpretation**: The `StatisticalInterpretationAgent` will write a draft interpretation of the statistical results.
4.  **Methodological Review**: The `MethodologicalOverwatchAgent` will review the initial interpretation and provide a critique.
5.  **Final Synthesis**: The `ExperimentConclusionAgent` will generate a final, revised report that incorporates the initial interpretation and the reviewer's critique.

The analysis should gather and report evidence as described in the framework definition. 

After all the results have been gathered across all runs, a full set of descriptive statistics for all the scores and metrics defined in the framework will be calculated. The analysis will also calculate inter-run reliability using Cronbach's Alpha to determine if the model produces consistent results across the runs. This requires a structured JSON output from the analysis agents containing a `score` field.

If the H2 hypothesis proves true, the analysis will include a calculation of how many runs would have been sufficient to prove the H1 hypothesis.

This experiment requires a final report that summarizes results in a way that will meet the approval of a knowledgeable domain expert in quantative social science methods and should directly address the hypotheses and evidence for or against them.

The final report should be based on an intermediate synthesis but extended to add additional context and enriching evidency details drawn from the analysis results.

The first draft of the final report should be reviewed by a secondary reviewer within the system.

A final, revised report should be generated that incorporates the feedback from the reviewer.
