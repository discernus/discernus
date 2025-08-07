# **Experiment Report: speaker_character_pattern_analysis**
- **Framework:** Civic Analysis Framework (CAF) v7.3
- **Run ID:** `[Placeholder]`
- **Date:** `[Placeholder]`

## **Executive Summary**

This report details an analysis of eight political texts using the Civic Analysis Framework (CAF) v7.3 to assess its capacity to differentiate speaker character. The analysis identified coherent "virtuous" and "pathological" character signatures within the data. A virtuous signature was observed through a strong positive correlation between truth and pragmatism scores (r = 0.82). A pathological signature was evident in the strong positive correlations between manipulation, fantasy, and resentment scores (r = 0.96 and r = 0.85, respectively). These findings support the framework's theoretical construction of opposing virtue/pathology axes, further evidenced by strong negative correlations between truth/manipulation (r = -0.72) and hope/manipulation (r = -0.93).

Descriptively, the corpus showed wide variation in the Civic Character Index (0.420 to 0.805) and a higher mean Virtue Index (0.590) compared to the mean Pathology Index (0.320). However, a primary experimental hypothesis—that the framework could produce statistically significant differentiation between speakers—could not be tested. The one-way ANOVA test was invalid (p=nan) due to an experimental design with only one sample per speaker, a significant limitation of this study.

## **Collaborator Analysis**

This section provides a detailed review of the statistical findings as they relate to the predefined experimental hypotheses.

### **Claim: h1_speaker_differentiation_anova_invalid**
- **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
- **Testability:** False. The one-way ANOVA test for differentiation on the `civic_character_index` could not be completed.
- **Summary:** The experimental design included only one observation per speaker (n=1), which is insufficient for calculating within-group variance, a prerequisite for the F-statistic. Therefore, no statistical conclusion can be drawn regarding the framework's ability to differentiate between speakers.
- **Evidence:**
    - The one-way ANOVA test returned a p-value of `nan`, indicating the test was invalid [1].

### **Claim: h2_pathological_signature_correlation**
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** True.
- **Summary:** Correlation analysis of the pathological dimensions reveals a strong, coherent pattern. The dimensions of manipulation, fantasy, and resentment are highly inter-correlated, suggesting they form a consistent "pathological signature" in the analyzed discourse.
- **Evidence:**
    - A very strong positive correlation was observed between `manipulation_score` and `fantasy_score` (r = 0.96) [2].
    - A strong positive correlation was observed between `manipulation_score` and `resentment_score` (r = 0.85) [3].

### **Claim: h2_virtuous_signature_correlation**
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** True.
- **Summary:** The virtuous dimensions of truth and pragmatism are strongly correlated, suggesting they form a coherent "virtuous signature." This signature is defined by a commitment to evidence-based reasoning and realistic problem-solving.
- **Evidence:**
    - A strong positive correlation was found between `truth_score` and `pragmatism_score` (r = 0.82) [4].

### **Claim: h3_cci_variation_descriptive**
- **Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
- **Testability:** True (Descriptive).
- **Summary:** While inferential statistical testing was not possible, descriptive statistics show a wide range in the `civic_character_index` across the sample. This variation suggests that the framework is capturing substantial differences in the civic character of the analyzed texts, though the source of this variation cannot be statistically attributed to the speakers themselves.
- **Evidence:**
    - The `civic_character_index` across the eight documents ranged from a minimum of 0.420 to a maximum of 0.805 [5].

### **Claim: framework_axis_opposition_truth_manipulation**
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** True.
- **Summary:** The analysis provides empirical support for the framework's theoretical construction of the Truth Axis as a bipolar dimension. The strong negative correlation between truth and manipulation scores validates that these concepts operate in opposition within the analyzed texts, which is a foundational requirement for identifying distinct character signatures.
- **Evidence:**
    - A strong negative correlation was observed between `truth_score` and `manipulation_score` (r = -0.72) [6].

### **Claim: framework_axis_opposition_hope_manipulation**
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** True.
- **Summary:** The data shows a very strong inverse relationship between appeals to hope and appeals to manipulation. This supports the framework's premise that virtuous and pathological appeals are fundamentally opposed, a key principle for defining coherent character signatures.
- **Evidence:**
    - A very strong negative correlation was found between `hope_score` and `manipulation_score` (r = -0.93) [7].

### **Claim: descriptive_virtue_vs_pathology_index**
- **Hypothesis:** Exploratory.
- **Testability:** True.
- **Summary:** On average, the analyzed corpus of political discourse scored higher on the Virtue Index than the Pathology Index. This indicates that, in aggregate, the texts leaned more toward appeals to virtue (dignity, truth, justice, hope, pragmatism) than to pathology (tribalism, manipulation, resentment, fear, fantasy).
- **Evidence:**
    - The mean `virtue_index` for the corpus was 0.590 [8].
    - The mean `pathology_index` for the corpus was 0.320 [9].

## **Evidence References**

All statistical evidence is derived from the analysis of the eight documents in the corpus, as listed in the `provenance` of each statistical task.

1.  **Source:** `task_06_hypothesis_testing_h1_speaker_differentiation`. **Metric:** `p_value`. **Value:** `nan`.
2.  **Source:** `task_05_character_signature_analysis`. **Metric:** Pearson correlation (`manipulation_score`, `fantasy_score`). **Value:** 0.96.
3.  **Source:** `task_05_character_signature_analysis`. **Metric:** Pearson correlation (`manipulation_score`, `resentment_score`). **Value:** 0.85.
4.  **Source:** `task_05_character_signature_analysis`. **Metric:** Pearson correlation (`truth_score`, `pragmatism_score`). **Value:** 0.82.
5.  **Source:** `task_04_descriptive_stats_derived_indices`. **Metric:** Range of `civic_character_index`. **Value:** Min: 0.420, Max: 0.805.
6.  **Source:** `task_05_character_signature_analysis`. **Metric:** Pearson correlation (`truth_score`, `manipulation_score`). **Value:** -0.72.
7.  **Source:** `task_05_character_signature_analysis`. **Metric:** Pearson correlation (`hope_score`, `manipulation_score`). **Value:** -0.93.
8.  **Source:** `task_04_descriptive_stats_derived_indices`. **Metric:** Mean of `virtue_index`. **Value:** 0.590.
9.  **Source:** `task_04_descriptive_stats_derived_indices`. **Metric:** Mean of `pathology_index`. **Value:** 0.320.

## **Technical Transparency**

- **Limitations:** The primary limitation of this study is the experimental design, which included only one document per speaker (n=1). This sample size precluded the use of ANOVA to test for statistically significant differences between speakers, rendering Hypothesis H1 untestable. Conclusions about character signatures are based on correlational data across the entire corpus and cannot be attributed to individual speakers.
- **Models Used:**
    - **Synthesis:** `vertex_ai/gemini-2.5-flash-lite`
- **Cost Summary:** `[Placeholder]`

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1271 USD  
**Total Tokens**: 40,722  
**Run Timestamp**: 20250807T234741Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0550 USD (18,807 tokens, 1 calls, $0.0550 avg/call)
- **Derived Metrics Analysis Planning**: $0.0721 USD (21,915 tokens, 1 calls, $0.0721 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1271 USD (40,722 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0550 USD (18,807 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0721 USD (21,915 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
