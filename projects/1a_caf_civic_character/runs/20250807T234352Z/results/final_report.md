# Experiment Report: speaker_character_pattern_analysis

**Framework:** Civic Analysis Framework (CAF) v7.3
**Run ID:** `[Not Available]`
**Date:** `[Not Available]`

## Executive Summary

This report details the results of an experiment designed to test the Civic Analysis Framework's (CAF) ability to differentiate character patterns among individual speakers. The primary hypothesis, which proposed that the framework's dimensions could yield statistically significant differences between speakers, could not be tested [1]. A one-way ANOVA, the designated statistical test, was not performed due to an insufficient sample size (n=1) for each speaker group.

Despite this limitation, descriptive and correlational analyses provided several key insights. The composite Civic Character Index scores showed considerable variation across the corpus, ranging from a minimum of 0.42 to a maximum of 0.805, suggesting that the framework can capture meaningful, if not statistically validated, differences [2].

Correlation analysis of the framework's ten core dimensions revealed patterns that both support and challenge its theoretical underpinnings. In line with the framework's design, a strong negative correlation (r = -0.93) was observed between Hope and Manipulation, indicating they function as oppositional concepts in the analyzed discourse [3]. Furthermore, pathological dimensions such as Manipulation, Fantasy, and Resentment showed strong positive inter-correlations (r up to 0.96), suggesting they form a coherent rhetorical cluster [4]. A similar, though less strong, relationship was found between the virtues of Truth and Pragmatism (r = 0.82) [5]. Conversely, the analysis found a positive correlation (r = 0.32) between Dignity and Tribalism, which contradicts the framework's assumption of a purely oppositional tension between these two dimensions and warrants further investigation [6].

Overall, the corpus demonstrated a higher mean Virtue Index (0.59) than Pathology Index (0.32), indicating that, on average, the analyzed texts leaned more toward civic virtue than pathology [7]. The primary limitation remains the small sample size, which prevents generalization and statistical validation of speaker differentiation.

## Interpretation of Claims

### Hypothesis 1: Speaker Differentiation
*   **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
*   **Finding:** This hypothesis was not testable. The one-way ANOVA required to determine statistical significance could not be executed because each speaker was represented by only a single document (n=1), providing no within-group variance [1].
*   **Evidence:** The analysis attempt resulted in an F-statistic and p-value of `nan`, confirming the test could not be completed [1].

### Hypothesis 2: Character Score Variation
*   **Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
*   **Finding:** This hypothesis is supported by descriptive statistics, though statistical significance could not be established. The analysis revealed a wide distribution of Civic Character Index scores across the eight documents in the corpus [2].
*   **Evidence:** The Civic Character Index ranged from a minimum of 0.420 to a maximum of 0.805, with a standard deviation of 0.122. This range suggests the framework captured substantial variation between the texts [2].

### Exploratory Finding: Opposition of Hope and Manipulation
*   **Hypothesis:** Exploratory.
*   **Finding:** A strong negative correlation exists between the Hope and Manipulation scores, which aligns with the framework's theoretical structure of virtues and pathologies as oppositional forces [3].
*   **Evidence:** Pearson correlation analysis showed a coefficient of r = -0.93 between `hope_score` and `manipulation_score` [3].

### Exploratory Finding: Pathological Dimension Clustering
*   **Hypothesis:** Exploratory.
*   **Finding:** The pathological dimensions of Manipulation, Fantasy, and Resentment are very strongly and positively inter-correlated, suggesting they are often deployed together as a coherent rhetorical strategy [4].
*   **Evidence:** Strong positive correlations were observed between `manipulation_score` and `fantasy_score` (r = 0.96) and between `manipulation_score` and `resentment_score` (r = 0.85) [4].

### Exploratory Finding: Virtue Dimension Synergy
*   **Hypothesis:** Exploratory.
*   **Finding:** A strong positive correlation between Truth and Pragmatism scores suggests a synergistic relationship, where appeals to factual accuracy and realistic problem-solving co-occur [5].
*   **Evidence:** The Pearson correlation between `truth_score` and `pragmatism_score` was r = 0.82 [5].

### Exploratory Finding: Dignity and Tribalism Tension
*   **Hypothesis:** Exploratory.
*   **Finding:** Analysis revealed a positive correlation between Dignity and Tribalism scores. This finding is contrary to the framework's theoretical model, which posits these dimensions as being in opposition, and suggests a more complex relationship where both appeals may be used simultaneously [6].
*   **Evidence:** The Pearson correlation between `dignity_score` and `tribalism_score` was r = 0.32 [6].

### Exploratory Finding: Overall Corpus Character
*   **Hypothesis:** Exploratory.
*   **Finding:** Across the entire corpus, the mean score for the Virtue Index was substantially higher than for the Pathology Index, suggesting the analyzed discourse was, on average, characterized more by virtuous appeals than pathological ones [7].
*   **Evidence:** The mean `virtue_index` for the corpus was 0.59, while the mean `pathology_index` was 0.32 [7].

## Evidence References

No specific document-level evidence snippets were mapped for this report. The references below indicate the source of the statistical data used for each claim.

[1] `task_05_skipped_speaker_differentiation_anova`
[2] `task_02_generate_descriptive_statistics`
[3] `task_03_analyze_dimensional_correlations`
[4] `task_03_analyze_dimensional_correlations`
[5] `task_03_analyze_dimensional_correlations`
[6] `task_03_analyze_dimensional_correlations`
[7] `task_02_generate_descriptive_statistics`

## Technical Transparency

*   **Known Limitations:** The primary statistical test for speaker differentiation (ANOVA) was not performed due to an insufficient sample size (n=1 per speaker), preventing a statistical conclusion on hypothesis H1. Findings are based on descriptive and correlational data from a small corpus (N=8) and cannot be generalized.
*   **Models Used:** vertex_ai/gemini-2.5-flash-lite
*   **Cost Summary:** Cost data not available.

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1147 USD  
**Total Tokens**: 39,480  
**Run Timestamp**: 20250807T234352Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0512 USD (18,424 tokens, 1 calls, $0.0512 avg/call)
- **Derived Metrics Analysis Planning**: $0.0635 USD (21,056 tokens, 1 calls, $0.0635 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1147 USD (39,480 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0512 USD (18,424 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0635 USD (21,056 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
