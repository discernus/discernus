# Character Assessment Framework Analysis

| | |
| :--- | :--- |
| **Experiment Name** | speaker_character_pattern_analysis |
| **Framework** | Civic Analysis Framework (CAF) v7.3 |
| **Run ID** | `[Not Provided]` |
| **Run Date** | `[Not Provided]` |

### Executive Summary

This report details the statistical analysis of eight political texts using the Civic Analysis Framework (CAF) v7.3. The analysis focused on validating the framework's dimensional structure and assessing its capacity to differentiate between speakers.

Key findings support the framework's theoretical design. Strong negative correlations were observed between the virtuous and pathological poles of the Identity Axis (Dignity vs. Tribalism, r = -0.79) and the Truth Axis (Truth vs. Manipulation, r = -0.86), empirically validating their bipolar structure [1, 2]. Furthermore, the analysis identified coherent "virtue" and "pathology" clusters, where dimensions within each category were strongly inter-correlated, supporting the validity of the composite Virtue and Pathology Indices [3, 4].

The data indicates that the framework's dimensions, particularly Tribalism (std = 0.40), effectively differentiate among the speakers in the corpus [5]. The composite Civic Character Index also showed substantial variance (std = 0.27), suggesting meaningful differences in character coherence across the evaluated texts [6]. An exploratory finding revealed a strong positive correlation (r = 0.94) between Pragmatism and Dignity scores, indicating a potential rhetorical pattern linking appeals to realism with appeals to universal human worth [7].

A primary limitation of this study is the small sample size (n=8), which precludes inferential statistical tests such as ANOVA. Findings should be interpreted as descriptive and foundational for future, larger-scale research.

### Collaborator Section

#### Claim: `claim_identity_axis_validity`
- **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
- **Testability:** This claim is testable. The correlation analysis provides evidence for the structural validity of the dimension, which is a prerequisite for testing for differences between speakers.
- **Statistical Results:** A strong negative Pearson correlation (r = -0.79) was found between `dignity_score` and `tribalism_score` across the corpus [1]. This supports the framework's design of these two dimensions as opposing poles on a single Identity Axis.
- **Supporting Evidence:**
    - "It's about the thousands of you who came out today to stand together and say, 'Our lives deserve dignity and our work deserves respect.'" [8]
    - "...we as a people cannot fall into that trap of separateness, the insidious idea that we think that there are some throwaway people whose dignity we can assault without assaulting our own." [9]

#### Claim: `claim_truth_axis_validity`
- **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
- **Testability:** This claim is testable. The correlation analysis provides evidence for the structural validity of the dimension.
- **Statistical Results:** A strong negative Pearson correlation (r = -0.86) was observed between `truth_score` and `manipulation_score` [2]. This result supports the theoretical construction of the bipolar Truth Axis.
- **Supporting Evidence:**
    - "We're doing that and the very, very basic and simple principle that American leaders should look out for Americans." [10]
    - "Our criminal justice system, as it stands right now, is an affront to who we say we are as a nation. We profess - we actually swear an oath to the flag - that we are a nation of liberty and justice for all. But our criminal justice system violates those values." [11]

#### Claim: `claim_pathology_cluster`
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** This claim is testable. The correlation matrix provides evidence for the coherence of the "pathology" construct.
- **Statistical Results:** Strong positive inter-correlations were identified among the pathological dimensions, indicating a coherent cluster [3]. Key correlations include Tribalism-Manipulation (r = 0.94), Tribalism-Resentment (r = 0.94), and Manipulation-Fear (r = 0.93). This supports the aggregation of these scores into a unified `pathology_index`.
- **Supporting Evidence:**
    - "They want us to think that our lives are suffering because of the LGBT kid down the street or because of the mixed status family or the dreamer down the block who's just trying to make a better life for themselves. But we're smarter than that Greeley." [12]
    - "The war on drugs, which has fueled so much of the explosion of our prison population, has really been a war on people - on certain people in certain communities and not on others." [13]

#### Claim: `claim_virtue_cluster`
- **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- **Testability:** This claim is testable. The correlation matrix provides evidence for the coherence of the "virtue" construct.
- **Statistical Results:** Strong positive inter-correlations were found among the virtue dimensions, suggesting a coherent "virtue cluster" [4]. Notable correlations include Dignity-Pragmatism (r = 0.94), Dignity-Justice (r = 0.81), and Truth-Pragmatism (r = 0.82). This supports the validity of the composite `virtue_index`.
- **Supporting Evidence:**
    - "It's about the thousands of you who came out today to stand together and say, 'Our lives deserve dignity and our work deserves respect.'" [14]
    - "But my promise before God to apply impartial justice required that I put my personal feelings and political biases aside." [15]

#### Claim: `claim_tribalism_variance`
- **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
- **Testability:** This claim is testable. The descriptive statistics show the dimension's capacity for differentiation.
- **Statistical Results:** The `tribalism_score` exhibited a high standard deviation (σ = 0.40) and a wide range (min: 0.05, max: 0.90) across the eight documents [5]. This degree of variance indicates that the Tribalism dimension is a primary axis for differentiating speakers within this corpus.
- **Supporting Evidence:**
    - "But my interest is not in protecting the good people of another country. I'm a senator for the state of Ohio. Our leaders have to protect the interests of the citizens of this country." [16]
    - "They want us to think that our lives are suffering because of the LGBT kid down the street or because of the mixed status family or the dreamer down the block who's just trying to make a better life for themselves. But we're smarter than that Greeley." [17]

#### Claim: `claim_cci_sci_variance`
- **Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
- **Testability:** This claim is testable. The descriptive statistics for the Civic Character Index (CCI) provide a basis for evaluating this hypothesis.
- **Statistical Results:** The `civic_character_index` demonstrated substantial variance across the sample, with a standard deviation of 0.27 and a range from 0.23 to 0.89 [6]. This suggests that the composite index captures meaningful differences in the overall character profiles of the speakers.
- **Supporting Evidence:**
    - "As a senator-juror, I swore an oath before God to exercise impartial justice. I am profoundly religious. My faith is at the heart of who I am. I take an oath before God as enormously consequential." [18]
    - "Because in this house, we stand together, we know that, that it's our only choice because we know that without exception, if we stand together, it is the only way that we can win." [19]
    - "When here in our Constitution, Mr. Speaker, Article one of our Constitution says, 'All legislative power, power, all legislative, all legislative powers herein granted shall be vested in a Congress of the United States.' That's here. The House and the Senate." [20]

#### Claim: `claim_pragmatism_dignity_link`
- **Hypothesis:** Exploratory.
- **Testability:** This claim is testable and represents an emergent finding from the correlation analysis.
- **Statistical Results:** An exceptionally strong positive Pearson correlation (r = 0.94) was observed between `pragmatism_score` and `dignity_score` [7]. This suggests that, within this corpus, appeals to realistic, practical solutions are closely linked to appeals to universal human worth and dignity.
- **Supporting Evidence:**
    - "It's about the thousands of you who came out today to stand together and say, 'Our lives deserve dignity and our work deserves respect.'" [21]
    - "...we as a people cannot fall into that trap of separateness, the insidious idea that we think that there are some throwaway people whose dignity we can assault without assaulting our own." [22]
    - "But my promise before God to apply impartial justice required that I put my personal feelings and political biases aside." [23]

### Evidence References

1.  `task_04_analyze_dimensional_correlations.matrix.dignity_score.tribalism_score`
2.  `task_04_analyze_dimensional_correlations.matrix.truth_score.manipulation_score`
3.  `task_04_analyze_dimensional_correlations.matrix`
4.  `task_04_analyze_dimensional_correlations.matrix`
5.  `task_03_generate_descriptive_statistics.results.tribalism_score`
6.  `task_03_generate_descriptive_statistics.results.civic_character_index`
7.  `task_04_analyze_dimensional_correlations.matrix.pragmatism_score.dignity_score`
8.  **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Dignity, **Confidence:** 0.95
9.  **Document:** `cory_booker_2018_first_step_act.txt`, **Dimension:** Dignity, **Confidence:** 0.9
10. **Document:** `jd_vance_2022_natcon_conference.txt`, **Dimension:** Justice, **Confidence:** 0.8
11. **Document:** `cory_booker_2018_first_step_act.txt`, **Dimension:** Justice, **Confidence:** 0.95
12. **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Tribalism, **Confidence:** 0.9
13. **Document:** `cory_booker_2018_first_step_act.txt`, **Dimension:** Tribalism, **Confidence:** 0.8
14. **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Dignity, **Confidence:** 0.95
15. **Document:** `mitt_romney_2020_impeachment.txt`, **Dimension:** Dignity, **Confidence:** 0.95
16. **Document:** `jd_vance_2022_natcon_conference.txt`, **Dimension:** Tribalism, **Confidence:** 1.0
17. **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Tribalism, **Confidence:** 0.9
18. **Document:** `mitt_romney_2020_impeachment.txt`, **Dimension:** Justice, **Confidence:** 1.0
19. **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Hope, **Confidence:** 0.9
20. **Document:** `steve_king_2017_house_floor.txt`, **Dimension:** Truth, **Confidence:** 0.9
21. **Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`, **Dimension:** Dignity, **Confidence:** 0.95
22. **Document:** `cory_booker_2018_first_step_act.txt`, **Dimension:** Dignity, **Confidence:** 0.9
23. **Document:** `mitt_romney_2020_impeachment.txt`, **Dimension:** Dignity, **Confidence:** 0.95

### Technical Transparency

- **Limitations:** The experiment configuration specified `evaluations_per_document: 1` for a corpus of 8 documents. This small sample size (n=8) prevents meaningful inferential statistical tests (e.g., ANOVA) from being conducted. The findings are therefore descriptive and should not be generalized without further research on a larger corpus.
- **Models Used:**
    - Analysis: `vertex_ai/gemini-2.5-pro`
    - Synthesis: `vertex_ai/gemini-2.5-pro`
- **Cost Summary:** Cost data was not provided in the input.

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1108 USD  
**Total Tokens**: 40,006  
**Run Timestamp**: 20250808T202505Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0556 USD (19,320 tokens, 1 calls, $0.0556 avg/call)
- **Derived Metrics Analysis Planning**: $0.0552 USD (20,686 tokens, 1 calls, $0.0552 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1108 USD (40,006 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0556 USD (19,320 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0552 USD (20,686 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
