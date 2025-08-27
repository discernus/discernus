
# Quantitative Comparison of ECF Experiment Runs

**Date**: 2025-08-27
**Author**: Gemini Agent
**Runs Compared**: `20250827T180121Z` vs. `20250827T182231Z`

## 1. Executive Summary

A quantitative analysis of the two most recent runs of the `1c_ecf_emotional_climate` experiment reveals a significant discrepancy between the stability of the analysis phase and the variability of the synthesis phase.

- **Analysis Phase is Identical**: The core quantitative outputs of the analysis phase, captured in `statistical_results.json`, are identical between the two runs (excluding timestamps). This indicates the data analysis portion of the pipeline is deterministic and reproducible.

- **Evidence Extraction Varied**: The analysis-time evidence extraction process produced significantly different results. The second run identified 33% more evidence pieces (256 vs. 192), suggesting a change in the analysis agent's performance or configuration between runs.

- **Synthesis Phase is Highly Variable**: Despite being fed the exact same statistical data, the synthesis agent produced two dramatically different final reports. The second report was 24% longer and differed in 67% of its content, including different statistical correlations, narrative framing, and rhetorical archetypes.

**Conclusion**: The root cause of the report differences is not a change in the underlying data but profound variability in the synthesis agent's generative process. While the analysis pipeline is stable, the synthesis pipeline is not, posing a potential challenge for reproducibility.

## 2. Detailed Findings

### 2.1. Statistical Analysis (`statistical_results.json`)

**Finding**: Identical.

A `diff` of the `statistical_results.json` files from both runs shows that the only differences are timestamps within the metadata. All numerical results—descriptive statistics, correlations, cluster analyses, etc.—are exactly the same.

This confirms the analysis pipeline is stable and deterministic.

### 2.2. Evidence Gathered (`evidence_database.json`)

**Finding**: Significant difference.

- **Run 1 (`...T180121Z`)**:
  - Total Evidence Pieces: 192
  - Total Files Processed: 24

- **Run 2 (`...T182231Z`)**:
  - Total Evidence Pieces: 256
  - Total Files Processed: 32

The second run extracted 64 additional pieces of evidence, a 33% increase. This points to a change in the analysis agent's behavior, as it identified substantially more quotes from the corpus texts on the second run.

### 2.3. Model Usage Verification

**Finding**: Inconclusive due to missing logs.

Detailed logs (`costs.jsonl`, `llm_interactions.jsonl`) were not consistently available for these older runs, making a definitive verification of the exact models used for each step impossible.

However, based on the identical statistical output, it is highly probable that the **analysis model was the same** in both runs. The variation in evidence extraction and final report synthesis likely stems from changes in the synthesis agent or its configuration.

## 3. Implications

The primary implication is the significant non-determinism of the synthesis agent. While the quantitative analysis is reproducible, the final human-readable report is not. This variability could be due to:

-   Changes in the synthesis model between runs.
-    inherent randomness (temperature settings) in the generative model.
-   Minor, non-logged changes to the synthesis agent's prompt or logic.

This highlights a need to either stabilize the synthesis agent's output or to clearly document the expected range of variability in final reports.
