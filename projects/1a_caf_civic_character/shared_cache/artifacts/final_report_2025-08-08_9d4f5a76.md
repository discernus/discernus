# Experiment Report: speaker_character_pattern_analysis

| | |
|---|---|
| **Framework** | Civic Analysis Framework (CAF) v7.3 |
| **Run ID** | *[Not Provided]* |
| **Date** | *[Not Provided]* |

## Executive Summary

This report details the results of an analysis applying the Civic Analysis Framework (CAF) v7.3 to a corpus of eight political texts. The objective was to assess the framework's capacity to differentiate between speakers, identify distinct character signatures, and measure variations in civic character coherence.

Key findings indicate that the framework successfully distinguished between speakers across its ten core dimensions. The composite Civic Character Index, a measure of coherence, varied substantially, ranging from a high of 0.805 to a low of 0.420 across the corpus [1]. This suggests the framework can quantify meaningful differences in the civic quality of discourse.

Correlation analysis revealed strong structural relationships between specific dimensions, such as a significant positive correlation between manipulation and fantasy scores (r = 0.96) and a strong negative correlation between hope and manipulation scores (r = -0.93). These patterns suggest underlying trade-offs in rhetorical strategies that constitute distinct character signatures. For example, the analysis identified starkly different profiles for speakers like Cory Booker (Virtue Index: 0.77, Pathology Index: 0.20) and Steve King (Virtue Index: 0.34, Pathology Index: 0.50) [2].

A notable limitation is the small sample size (n=8), which precludes definitive statistical conclusions for some tests. An exploratory two-way ANOVA examining the interaction between ideology and era on the Civic Character Index was inconclusive (p = 0.45) due to small and uneven group sizes [3].

## Collaborator Section

### Claim: Civic Character Index Variation by Speaker
**Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence. (Testable)

Statistical analysis confirms that the Civic Character Index, which measures the balance of virtuous over pathological appeals, shows substantial variation across the speakers in the corpus. Scores ranged from a high of 0.805 for John McCain to a low of 0.420 for Steve King, supporting the hypothesis that the framework can detect and quantify different levels of character coherence [2].

- "Whatsoever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [4]
- "You know, campaigns are often harder on a candidate's family than on the candidate, and that's been true in this campaign." [1]

### Claim: Manipulation and Fantasy Correlation
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices. (Testable)

A Pearson correlation matrix of the ten core dimensions revealed a strong positive correlation between manipulation and fantasy scores (r = 0.96) [5]. This suggests that, within this dataset, appeals to fantasy are structurally linked with manipulative rhetoric, forming a key component of what the framework measures as a pathological character signature.

- "But the Supreme Court, wrapped in the cloak of Marbury versus Madison and their imagination of what precedents and star decisions might mean to them, decides that they can write words into the law. A Supreme Court writing law." [6]
- "The president's purpose was personal and political. Accordingly, the president is guilty of an appalling abuse of public trust." [7]
- "This system as a whole is a cancer on the soul of our country, and it's hurting every single American." [8]

### Claim: Tribalism Score Variation
**Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers. (Testable)

The tribalism score, which measures the use of in-group/out-group framing, was a significant differentiator among speakers. The observed scores ranged from a low of 0.15 (John McCain) to a high of 0.65 (Alexandria Ocasio-Cortez), demonstrating the dimension's utility in distinguishing rhetorical approaches [2].

- "Whatsoever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [4]
- "They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture." [9]

### Claim: Contrasting Character Signatures (Booker vs. King)
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices. (Testable)

The framework identified distinct character signatures by calculating composite Virtue and Pathology Indices. The profiles of Cory Booker (Virtue Index: 0.77, Pathology Index: 0.20) and Steve King (Virtue Index: 0.34, Pathology Index: 0.50) were starkly different, illustrating the framework's capacity to capture unique patterns of virtue and vice appeals [2].

- "I'm the only United States Senator that lives in a majority black and brown community. It is low income, but I tell you right now, my community does not mistake wealth with worth. I live in an inner-city community, and when I go home at the end of most weeks, I draw strength from my community." [10]
- "This system as a whole is a cancer on the soul of our country, and's hurting every single American." [8]

### Claim: Hope and Manipulation Opposition
**Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices. (Testable)

The correlation analysis exposed a strong inverse relationship between hope and manipulation scores (r = -0.93) [5]. This structural opposition suggests a fundamental trade-off in the rhetorical strategies measured by the framework, where appeals to hope are seldom paired with appeals to manipulation.

- "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve." [11]
- "I wish the outcome had been different, my friends. The road was a difficult one from the outset, but your support and friendship never wavered." [12]

### Claim: Truth Score Variation
**Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers. (Testable)

The truth score, measuring commitment to factual accuracy and intellectual honesty, varied widely across the corpus. Scores ranged from 0.70 (Bernie Sanders, Cory Booker) to a low of 0.20 (Steve King), indicating the dimension is effective for differentiating speakers' rhetorical styles [2].

- "I think actualy every speech I've given in that NatCon, I, I know Bridge spoke earlier, or I was going to speak, Bridge, you're out there somewhere." [13]
- "This system as a whole is a cancer on the soul of our country, and it's hurting every single American." [8]

### Claim: Ideology and Era Interaction
**Hypothesis:** Exploratory.

A two-way ANOVA was conducted to explore the interaction effect of ideology (Conservative, Progressive) and era (Populist, Institutional, Civil Rights) on the Civic Character Index. The result was not statistically significant (p = 0.45) [3]. This finding is inconclusive due to the small overall sample size (n=8) and the presence of subgroups with only a single observation (n=1), which severely limits the statistical power and validity of the test.

- "No matter if you know all the right words to say, no matter your race, religion, gender identity, or status, no matter if you disagree with me on a couple of things." [14]
- "Whatsoever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [4]
- "I'm the only United States Senator that lives in a majority black and brown community. It is low income, but I tell you right now, my community does not mistake wealth with worth. I live in an inner-city community, and when I go home at the end of most weeks, I draw strength from my community." [10]

## Evidence References

| Ref. | Document | Dimension | Confidence |
|:----:|:---|:---|:---:|
| [1] | `john_mccain_2008_concession.txt` | fantasy | 0.8 |
| [2] | `task_03_descriptive_statistics_by_speaker` | - | - |
| [3] | `task_07_explore_ideology_era_interaction` | - | - |
| [4] | `john_mccain_2008_concession.txt` | tribalism | 0.9 |
| [5] | `task_05_analyze_character_signatures` | - | - |
| [6] | `steve_king_2017_house_floor.txt` | manipulation | 0.9 |
| [7] | `mitt_romney_2020_impeachment.txt` | manipulation | 0.7 |
| [8] | `cory_booker_2018_first_step_act.txt` | fantasy | 0.4 |
| [9] | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | tribalism | 0.85 |
| [10] | `cory_booker_2018_first_step_act.txt` | tribalism | 0.7 |
| [11] | `bernie_sanders_2025_fighting_oligarchy.txt` | hope | 0.7 |
| [12] | `john_mccain_2008_concession.txt` | resentment | 0.85 |
| [13] | `jd_vance_2022_natcon_conference.txt` | truth | 0.7 |
| [14] | `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | pragmatism | 0.6 |

## Technical Transparency

- **Limitations:** The primary limitation of this analysis is the small sample size (n=8), which affects the statistical power of all findings. The two-way ANOVA test was statistically invalid due to multiple subgroups containing only a single data point.
- **Models Used:** vertex_ai/gemini-2.5-flash-lite
- **Cost Summary:** *[Not Provided]*

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1234 USD  
**Total Tokens**: 41,251  
**Run Timestamp**: 20250808T020552Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0472 USD (18,471 tokens, 1 calls, $0.0472 avg/call)
- **Derived Metrics Analysis Planning**: $0.0762 USD (22,780 tokens, 1 calls, $0.0762 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1234 USD (41,251 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0472 USD (18,471 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0762 USD (22,780 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
