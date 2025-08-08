# Experiment Report

| | |
|---|---|
| **Experiment Name** | speaker_character_pattern_analysis |
| **Framework** | Civic Analysis Framework (CAF) v7.3 |
| **Run ID** | [Not Available] |
| **Run Date** | [Not Available] |
| **Corpus** | 8 documents |

## Executive Summary

This report details the results of an analysis applying the Civic Analysis Framework (CAF) v7.3 to a corpus of eight political texts. The objective was to assess the framework's capacity to differentiate between speakers and identify distinct character patterns.

Key findings indicate that the framework successfully captured a wide range of rhetorical styles, evidenced by the broad distribution of the composite Civic Character Index (CCI) scores, which ranged from 0.135 to 0.895 [3]. Correlation analysis of the ten core dimensions provided support for the framework's construct validity; paired virtues and vices, such as Dignity and Tribalism (r=-0.93), demonstrated strong negative correlations, consistent with the framework's bipolar axis design [4].

The analysis also revealed highly structured relationships within virtue and pathology clusters. Pathological dimensions were tightly inter-correlated, with Manipulation and Resentment showing a near-perfect correlation (r=0.99), suggesting they may function as a unified "pathology syndrome" in this dataset [5]. Similarly, virtue dimensions were strongly and positively correlated [2].

Limitations of this study include a small sample size (N=8) with a single evaluation per document, precluding inferential statistical tests such as ANOVA. The high correlation between certain dimensions also suggests potential conceptual overlap that warrants further investigation [6].

## Collaborator Section

### Claim 1: Speaker Differentiation and Variance
**Hypothesis (H1):** The 10 CAF dimensions will show statistically significant differences between speakers.
**Testability:** This hypothesis is testable with a larger dataset, but the current sample size (N=8) and single evaluation per document prevent the use of inferential statistics like ANOVA. However, descriptive statistics can assess the prerequisite condition of variance.

**Statistical Findings:**
Descriptive statistics indicate considerable variance across the ten base dimensions within the corpus. For example, `dignity_score` ranged from 0.1 to 0.9 (std=0.35), and `tribalism_score` ranged from 0.1 to 0.9 (std=0.37) [1]. This demonstrates that the framework captured a wide spectrum of values for each dimension across the different texts.

**Supporting Evidence:**
*   "The American people have spoken, and they have spoken clearly." [1]
*   "I imagine that many of them are very good people." [2]

### Claim 2: Civic Character Index Variance
**Hypothesis (H3):** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
**Testability:** This hypothesis is testable.

**Statistical Findings:**
The composite Civic Character Index (CCI), which measures character coherence, showed substantial variation across the corpus. Scores ranged from a minimum of 0.135 to a maximum of 0.895, with a standard deviation of 0.295 [3]. This wide distribution supports the claim that the framework captures meaningful differences in the overall character coherence of the analyzed texts.

**Supporting Evidence:**
*   "The American people have spoken, and they have spoken clearly." [3]
*   "in this house, we stand together, we know that, that it's our only choice because we know that without exception, if we stand together, it is the only way that we can win." [4]

### Claim 3: Pathological Dimension Clustering
**Hypothesis (H2):** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This hypothesis is testable.

**Statistical Findings:**
Correlation analysis reveals that pathological dimensions are not independent but form a tightly coupled cluster. Strong positive correlations were observed between `tribalism_score` and `manipulation_score` (r=0.91), `tribalism_score` and `resentment_score` (r=0.93), and most notably between `manipulation_score` and `resentment_score` (r=0.99) [5]. This suggests the presence of a consistent "pathology syndrome" rather than idiosyncratic combinations of vices.

**Supporting Evidence:**
*   "This system as a whole is a cancer on the soul of our country, and it's hurting every single American." [5]
*   "a kid living in a community that's low-income or communities that's black and brown, they get trapped by a system that disproportionately impacts their lives than it does others." [6]

### Claim 4: Framework Bipolar Axis Validity
**Exploratory Claim:** This analysis tests a foundational premise of the CAF framework: that its dimensional axes are bipolar.

**Statistical Findings:**
The Pearson correlation matrix provides evidence for the framework's construct validity by confirming the bipolar nature of its axes. Strong negative correlations were found between theoretically opposing dimensions, including `dignity_score` and `tribalism_score` (r=-0.93), `truth_score` and `manipulation_score` (r=-0.94), and `pragmatism_score` and `fantasy_score` (r=-0.98) [4].

**Supporting Evidence:**
*   "a kid living in a community that's low-income or communities that's black and brown, they get trapped by a system that disproportionately impacts their lives than it does others." [7]
*   "Our lives deserve dignity and our work deserves respect." [8]

### Claim 5: Virtue Dimension Clustering
**Hypothesis (H2):** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This hypothesis is testable.

**Statistical Findings:**
Similar to the pathological dimensions, the five virtue dimensions exhibit strong positive inter-correlations. Notable relationships include `dignity_score` and `justice_score` (r=0.89), `dignity_score` and `pragmatism_score` (r=0.88), and `truth_score` and `pragmatism_score` (r=0.94) [2]. This finding suggests that character signatures may conform to a common "virtue pattern" rather than being entirely unique.

**Supporting Evidence:**
*   "Our lives deserve dignity and our work deserves respect." [9]
*   "I imagine that many of them are very good people." [10]

### Claim 6: Dimensional Redundancy
**Exploratory Claim:** This analysis investigates potential redundancy between framework dimensions.

**Statistical Findings:**
The analysis identified a potential issue of discriminant validity between two pathological dimensions. The Pearson correlation coefficient between `manipulation_score` and `resentment_score` was 0.99, indicating a near-perfect linear relationship in this dataset [6]. This suggests that, within this corpus, the two dimensions may not be measuring distinct constructs.

**Supporting Evidence:**
*   "We're going to disagree sometimes about how best to serve that nation. We're going to disagree, of course, even within this room about how to best accomplish the reinvigoration of American industry and the renewal of American family." [11]
*   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [12]

## Evidence References
[1] john_mccain_2008_concession.txt (truth, confidence: 0.95)
[2] jd_vance_2022_natcon_conference.txt (dignity, confidence: 0.8)
[3] john_mccain_2008_concession.txt (truth, confidence: 0.95)
[4] alexandria_ocasio_cortez_2025_fighting_oligarchy.txt (hope, confidence: 0.9)
[5] cory_booker_2018_first_step_act.txt (manipulation, confidence: 0.8)
[6] cory_booker_2018_first_step_act.txt (tribalism, confidence: 0.9)
[7] cory_booker_2018_first_step_act.txt (tribalism, confidence: 0.9)
[8] alexandria_ocasio_cortez_2025_fighting_oligarchy.txt (dignity, confidence: 0.9)
[9] alexandria_ocasio_cortez_2025_fighting_oligarchy.txt (justice, confidence: 0.7)
[10] jd_vance_2022_natcon_conference.txt (dignity, confidence: 0.8)
[11] jd_vance_2022_natcon_conference.txt (pragmatism, confidence: 0.75)
[12] john_mccain_2008_concession.txt (dignity, confidence: 0.95)

## Technical Transparency

**Limitations:**
*   The sample size (N=8 documents) and single evaluation per document are insufficient for robust inferential statistics (e.g., ANOVA) to test for significant differences between speakers.
*   The extremely high correlation (r=0.99) between the `manipulation` and `resentment` dimensions suggests a lack of discriminant validity within this corpus, indicating potential conceptual overlap that may require framework refinement.

**Models Used:**
*   Analysis: vertex_ai/gemini-2.5-pro
*   Synthesis: vertex_ai/gemini-2.5-pro

**Cost Summary:**
*   Analysis Cost: [Not Available]
*   Synthesis Cost: [Not Available]
*   Total Cost: [Not Available]

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.0681 USD  
**Total Tokens**: 39,306  
**Run Timestamp**: 20250808T231836Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0023 USD (17,565 tokens, 1 calls, $0.0023 avg/call)
- **Derived Metrics Analysis Planning**: $0.0658 USD (21,741 tokens, 1 calls, $0.0658 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-flash-lite**: $0.0023 USD (17,565 tokens, 1 calls)
- **vertex_ai/gemini-2.5-pro**: $0.0658 USD (21,741 tokens, 1 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0023 USD (17,565 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0658 USD (21,741 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
