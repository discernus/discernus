# Experiment: PDAF v1.1 Retest

This experiment validates the refactored `AnalysisAgent` and the full academic pipeline using the operational PDAF v1.1 framework and real-world corpus data.

## Hypothesis

The multi-anchor sentiment scores for the two texts will be statistically distinguishable and reliable across runs. Specifically, we hypothesize that the mean score for the "Manichaean People-Elite Framing" anchor will be significantly different between the two speeches.

## Methodology

1.  **Analysis**: The `WorkflowOrchestrator` will execute the PDAF v1.1 framework on each corpus file for 2 runs using a `code_interpreter`-capable model.
2.  **Statistics**: The `StatisticalAnalysisAgent` will calculate descriptive statistics for all anchors and Cronbach's Alpha for inter-run reliability on each anchor.
3.  **Success Criteria**: The system functions end-to-end, producing a valid, multi-anchor `statistical_analysis_results.json` file and a coherent final report.

## Configuration

```yaml
models:
  - "openai/gpt-4o"
num_runs: 2
``` 