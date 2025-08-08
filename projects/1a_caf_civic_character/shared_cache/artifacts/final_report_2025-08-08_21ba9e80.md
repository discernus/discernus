# Experiment Report: speaker_character_pattern_analysis

| | |
|---|---|
| **Framework** | Civic Analysis Framework (CAF) v7.3 |
| **Run ID** | `[Not Provided]` |
| **Run Date** | `[Not Provided]` |

### Executive Summary

This report details the analysis of eight political texts using the Civic Analysis Framework (CAF) v7.3 to assess character patterns among individual speakers. The analysis focused on differentiating speakers across 10 character dimensions, identifying unique character signatures, and examining character coherence.

Key statistical findings from a Pearson correlation matrix revealed several strong relationships between character dimensions, supporting the hypothesis that speakers exhibit distinct signatures (H2). A strong positive correlation was observed between truth and pragmatism scores (r = 0.82), and an even stronger positive correlation was found between manipulation and fantasy scores (r = 0.96). Additionally, a strong inverse relationship was identified between hope and manipulation (r = -0.93).

However, other hypotheses could not be statistically validated. The hypothesis concerning significant differences between speakers across the 10 CAF dimensions (H1) was not tested. The hypothesis regarding meaningful variation in character coherence (H3) was untestable, as a one-way ANOVA could not be computed due to each speaker being represented by a single text (n=1), which precludes a valid test of variance between groups.

### Collaborator Section

#### Claim: H3-civic_character_coherence_untestable
**Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
**Testability:** This claim is not statistically testable with the current data. The one-way ANOVA, intended to test for variance in the Civic Character Index between speakers, could not be computed because each speaker group contained only a single observation (n=1) [1].

**Statistical Detail:**
*   A one-way ANOVA on the `civic_character_index` grouped by `speaker` resulted in an F-statistic of `nan` and a p-value of `nan` [1]. This indicates that a statistical comparison of means between speaker groups is not possible.

**Supporting Evidence:**
*   "I think actualy every speech I've given in that NatCon, I, I know Bridge spoke earlier, or I was going to speak, Bridge, you're out there somewhere." [2]
*   "And so I can stand here, Mr. Speaker, every night I could come here and give you these stats and I can give you the data on the thousands of Americans that are dead at the hands of the criminal aliens that have been incarcerated for a temporary period of time and released by multiple jurisdictions across this country." [3]
*   "And that means our communities choosing and voting for Democrats and elected officials who know how to stand for the working class." [4]

#### Claim: H2-pathology_signature_correlation
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This claim is testable through correlation analysis of character dimensions.

**Statistical Detail:**
*   A Pearson correlation analysis revealed a near-perfect positive correlation between `manipulation_score` and `fantasy_score` (r = 0.96) [5]. This suggests a common pathological pairing where appeals to fantasy are strongly associated with manipulative rhetoric.

**Supporting Evidence:**
*   "This system as a whole is a cancer on the soul of our country, and it's hurting every single American." [6]
*   "They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture." [7]

#### Claim: H2-virtue_vice_tension
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This claim is testable through correlation analysis of character dimensions.

**Statistical Detail:**
*   The analysis identified a strong negative correlation between `hope_score` and `manipulation_score` (r = -0.93) [8]. This inverse relationship indicates that as appeals to hope increase, the use of manipulation tends to decrease, forming a key trade-off in defining a character signature.

**Supporting Evidence:**
*   "though our faith assures us she is at rest in the presence of her Creator and so very proud of the good man she helped raise." [9]
*   "I wish the outcome had been different, my friends. The road was a difficult one from the outset, but your support and friendship never wavered." [10]

#### Claim: H1-speaker_differentiation_untested
**Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
**Testability:** This claim was not statistically tested in the analysis. While descriptive statistics show variance across the 10 dimensions, no inferential test (e.g., ANOVA, MANOVA) was performed to determine if these differences are statistically significant between speakers [11].

**Statistical Detail:**
*   Descriptive statistics show a range of mean scores across the 10 dimensions, from `fantasy_score` (M = 0.18) to `dignity_score` (M = 0.71) [11]. However, without an inferential test, it is not possible to conclude that these differences are significant.

**Supporting Evidence:**
*   "I think actualy every speech I've given in that NatCon, I, I know Bridge spoke earlier, or I was going to speak, Bridge, you're out there somewhere." [12]
*   "And so I can stand here, Mr. Speaker, every night I could come here and give you these stats and I can give you the data on the thousands of Americans that are dead at the hands of the criminal aliens that have been incarcerated for a temporary period of time and released by multiple jurisdictions across this country." [13]

#### Claim: H2-virtue_signature_correlation
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This claim is testable through correlation analysis of character dimensions.

**Statistical Detail:**
*   A strong positive correlation was found between `truth_score` and `pragmatism_score` (r = 0.82) [14]. This relationship suggests that appeals to truth and evidence-based reasoning are frequently paired with appeals to practical, realistic solutions.

**Supporting Evidence:**
*   "No matter if you know all the right words to say, no matter your race, religion, gender identity, or status, no matter if you disagree with me on a couple of things." [15]
*   "though our faith assures us she is at rest in the presence of her Creator and so very proud of the good man she helped raise." [16]
*   "I think actualy every speech I've given in that NatCon, at the Wall Street Journal editorial page. I think actualy every speech I've given in that NatCon, at the Wall Street Journal editorial page." [17]

#### Claim: H2-populist_pathology_signature
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
**Testability:** This claim is testable through correlation analysis of character dimensions.

**Statistical Detail:**
*   The correlation matrix shows a strong positive relationship between `resentment_score` and `manipulation_score` (r = 0.85) [18]. This indicates that rhetoric centered on grievance and blame is highly associated with the use of manipulative communication techniques.

**Supporting Evidence:**
*   "They're just very nice. But they're not." [19]
*   "They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture." [20]
*   "The war on drugs, which has fueled so much of the explosion of our prison population, has really been a war on people - on certain people in certain communities and not on others." [21]

### Evidence References

| | Document | Dimension | Confidence |
|---|---|---|---|
| **[1]** | `task_06_character_coherence_analysis_H3` | civic_character_index | `N/A` |
| **[2]** | `jd_vance_2022_natcon_conference.txt` | truth | 0.7 |
| **[3]** | `steve_king_2017_house_floor.txt` | resentment | 0.7 |
| **[4]** | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | justice | 0.8 |
| **[5]** | `task_05_character_signature_analysis_H2` | manipulation_score, fantasy_score | `N/A` |
| **[6]** | `cory_booker_2018_first_step_act.txt` | fantasy | 0.4 |
| **[7]** | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | tribalism | 0.85 |
| **[8]** | `task_05_character_signature_analysis_H2` | hope_score, manipulation_score | `N/A` |
| **[9]** | `john_mccain_2008_concession.txt` | justice | 0.88 |
| **[10]** | `john_mccain_2008_concession.txt` | resentment | 0.85 |
| **[11]** | `task_03_descriptive_statistics_all_metrics` | `N/A` | `N/A` |
| **[12]** | `jd_vance_2022_natcon_conference.txt` | truth | 0.7 |
| **[13]** | `steve_king_2017_house_floor.txt` | resentment | 0.7 |
| **[14]** | `task_05_character_signature_analysis_H2` | truth_score, pragmatism_score | `N/A` |
| **[15]** | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | pragmatism | 0.6 |
| **[16]** | `john_mccain_2008_concession.txt` | justice | 0.88 |
| **[17]** | `jd_vance_2022_natcon_conference.txt` | pragmatism | 0.4 |
| **[18]** | `task_05_character_signature_analysis_H2` | resentment_score, manipulation_score | `N/A` |
| **[19]** | `bernie_sanders_2025_fighting_oligarchy.txt` | resentment | 0.6 |
| **[20]** | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | tribalism | 0.85 |
| **[21]** | `cory_booker_2018_first_step_act.txt` | resentment | 0.6 |

### Technical Transparency

*   **Limitations:** The statistical power of this analysis is limited by the small sample size (N=8). Specifically, the inability to perform an ANOVA for H3 is a direct result of having only one data point per speaker, which prevents the calculation of within-group variance. Hypothesis H1 was not accompanied by a corresponding statistical test.
*   **Models Used:** The synthesis model used was `vertex_ai/gemini-2.5-flash-lite`.
*   **Cost Summary:** Cost data for this analysis is not available.

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1125 USD  
**Total Tokens**: 40,160  
**Run Timestamp**: 20250808T002209Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0527 USD (19,024 tokens, 1 calls, $0.0527 avg/call)
- **Derived Metrics Analysis Planning**: $0.0598 USD (21,136 tokens, 1 calls, $0.0598 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1125 USD (40,160 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0527 USD (19,024 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0598 USD (21,136 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
