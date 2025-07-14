# Experiment: Attesor Deep Smoke Test
## End-to-End Validation of the THIN Multi-LLM Analysis Pipeline

**Date**: January 13, 2025  
**Framework**: PDAF v1.1 (Sanitized)  
**Analysis Type**: Comprehensive system validation  
**Expected Duration**: 15-20 minutes  
**Purpose**: Validate the complete, integrated THIN software + THICK intelligence pipeline, including automated YAML configuration, multi-model/multi-run execution, and statistical analysis.

---

## Hypotheses

*   **H1 (Bias Check)**: There will be no statistically significant difference in populism scores between the selected LLM models when analyzing sanitized text.
*   **H2 (Reliability Check)**: The inter-run reliability (Cronbach's Alpha) for each model will be high (α > 0.8), indicating that the models produce consistent results across runs.

---

## Methodology

For this experiment, I want to compare a top-tier model from Anthropic with a top-tier model from OpenAI for performance. I also want to include a cost-effective model from the Anthropic family as a baseline. Please run the analysis 3 times for each model to ensure reliability. This experiment is designed for bias isolation, so please perform a raw aggregation of the results without any adversarial synthesis.

---

## Success Criteria

*   **YAML Generation**: The `EnsembleConfigurationAgent` correctly generates and appends a YAML block with the three specified models and `num_runs: 3`.
*   **Orchestrator Execution**: The `EnsembleOrchestrator` successfully reads the YAML and executes a 2 (texts) x 3 (models) x 3 (runs) = 18-analysis matrix.
*   **Statistical Analysis**: The `SecureCodeExecutor` runs successfully and generates a `statistical_analysis_results.json` file containing Cronbach's Alpha and ANOVA results.
*   **Provenance**: All project and run chronologs are created correctly, capturing the full execution trace.
*   **THIN Compliance**: The entire pipeline operates according to the THIN software + THICK intelligence philosophy. 
---
**Generated Configuration (for reproducibility):**
```yaml
models:
  - claude-3-5-sonnet-20240620
  - gpt-4o
  - claude-3-haiku-20240307
num_runs: 3
remove_synthesis: true
```
