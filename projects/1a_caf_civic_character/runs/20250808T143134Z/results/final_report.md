# **Experiment Report**

| | |
|---|---|
| **Experiment Name** | speaker_character_pattern_analysis |
| **Framework** | Civic Analysis Framework (CAF) v7.3 |
| **Run ID** | `[Placeholder]` |
| **Date** | `[Placeholder]` |

## **Executive Summary**

This report details the results of an analysis applying the Civic Analysis Framework (CAF) v7.3 to a corpus of eight political texts, each from a different speaker. The primary objective was to assess the framework's capacity to differentiate between speakers and identify coherent character patterns.

Key findings from the analysis indicate that the framework's theoretical structure is robust. The five bipolar axes of civic character (e.g., Dignity vs. Tribalism) are supported by strong negative correlations between their constituent dimensions, as specified in the framework design [1]. The five virtue dimensions (Dignity, Truth, Justice, Hope, Pragmatism) demonstrate positive inter-correlation, as do the five pathology dimensions (Tribalism, Manipulation, Resentment, Fear, Fantasy), suggesting that these groupings represent coherent underlying constructs.

Particularly strong correlations were observed between Dignity and Pragmatism (r = 0.94) and between Tribalism and Manipulation (r = 0.94), suggesting common pairings in rhetorical strategies. The composite `Virtue Index` and `Pathology Index` were, as expected, strongly negatively correlated. While descriptive statistics show considerable variance in both individual dimension scores and the composite `Civic Character Index` across the sample, planned significance testing (e.g., ANOVA) was not conducted.

**Limitations:** The primary limitation of this analysis is the small sample size (N=8), with only one document per speaker. This precludes meaningful statistical significance testing and limits the generalizability of the findings. The results should be interpreted as descriptive and correlational, providing preliminary evidence for the framework's constructs rather than definitive conclusions about the speakers.

## **Collaborator Section**

### **Claim 1: H1 Speaker Differentiation Variance**

*   **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
*   **Testability:** This claim is testable, but significance testing was not performed due to the sample size (n=1 per speaker), which is insufficient for an ANOVA as specified in the experiment design.
*   **Statistical Results:** Descriptive statistics indicate variance across the 10 core dimensions. For example, `dignity_score` ranged from 0.20 to 0.90 (M=0.61, SD=0.32), and `tribalism_score` ranged from 0.05 to 0.90 (M=0.56, SD=0.40) [2]. This variance suggests the framework is capturing differences, though their statistical significance is undetermined.
*   **Supporting Evidence:**
    *   "The American people have spoken, and they have spoken clearly. A little while ago, I had the honor of calling Senator Barack Obama to congratulate him... on being elected the next president of the country that we both love." [1]
    *   "And you don't have to believe, of course, that the 20,000 or at least most of the 20,000 newcomers are bad people. In fact, I imagine that many of them are very good people." [2]

### **Claim 2: Framework Bipolar Axis Validation**

*   **Hypothesis:** Exploratory.
*   **Testability:** This claim is testable.
*   **Statistical Results:** Pearson correlation analysis supports the framework's bipolar axis structure. Strong to moderate negative correlations were found between opposing virtue and pathology dimensions: Dignity/Tribalism (r = -0.79), Truth/Manipulation (r = -0.86), Justice/Resentment (r = -0.45), Hope/Fear (r = -0.62), and Pragmatism/Fantasy (r = -0.87) [3].
*   **Supporting Evidence:**
    *   "They want us to think that our lives are suffering because of the LGBT kid down the street or because of the mixed status family or the dreamer down the block who's just trying to make a better life for themselves. But we're smarter than that Greeley." [3]
    *   "we as a people cannot fall into that trap of separateness, the insidious idea that we think that there are some throwaway people whose dignity we can assault without assaulting our own." [4]

### **Claim 3: H2 Character Signature Structure**

*   **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
*   **Testability:** This claim is testable.
*   **Statistical Results:** The correlation matrix indicates that the framework's virtue and pathology dimensions form coherent clusters. Virtue dimensions are positively correlated with one another (e.g., Dignity/Justice, r = 0.81). Likewise, pathology dimensions are positively correlated (e.g., Tribalism/Resentment, r = 0.94) [3]. This internal consistency is a prerequisite for identifying stable character signatures.
*   **Supporting Evidence:**
    *   "And you don't have to believe, of course, that the 20,000 or at least most of the 20,000 newcomers are bad people. In fact, I imagine that many of them are very good people." [5]
    *   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [6]
    *   "We share those common values because we still live in a nation where the ties that bind us are stronger than the lines that divide us. This bill is a recognition of the fact that we are bound together as a people by the most precious ideals in humanity" [7]

### **Claim 4: H3 Civic Character Index Variance**

*   **Hypothesis:** MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
*   **Testability:** This claim is testable.
*   **Statistical Results:** The derived `civic_character_index` shows substantial variance across the sample of eight speakers, with a mean of 0.56, a standard deviation of 0.27, and a range from 0.23 to 0.89 [4]. This suggests the index is capturing differentiation, though the meaningfulness of this variation cannot be confirmed with significance testing due to sample size.
*   **Supporting Evidence:**
    *   "The American people have spoken, and they have spoken clearly. A little while ago, I had the honor of calling Senator Barack Obama to congratulate him... on being elected the next president of the country that we both love." [8]
    *   "But my interest is not in protecting the good people of another country. I'm a senator for the state of Ohio. Our leaders have to protect the interests of the citizens of this country." [9]
    *   "When here in our Constitution, Mr. Speaker, Article one of our Constitution says, \"All legislative power, power, all legislative, all legislative powers herein granted shall be vested in a Congress of the United States.\" That's here. The House and the Senate." [10]

### **Claim 5: Pattern Dignity-Pragmatism Link**

*   **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
*   **Testability:** This claim is testable.
*   **Statistical Results:** A very strong positive correlation (r = 0.94) was found between `dignity_score` and `pragmatism_score` [3]. This suggests that in the analyzed corpus, appeals to universal human worth are closely linked with appeals to realistic, problem-solving approaches.
*   **Supporting Evidence:**
    *   "It's about the thousands of you who came out today to stand together and say, \"Our lives deserve dignity and our work deserves respect.\"" [11]
    *   "But we will march with the spirit of love and with the spirit of dignity that we have shown here today." [12]
    *   "But my promise before God to apply impartial justice required that I put my personal feelings and political biases aside." [13]

### **Claim 6: Pattern Tribalism-Manipulation Link**

*   **Hypothesis:** Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
*   **Testability:** This claim is testable.
*   **Statistical Results:** A very strong positive correlation (r = 0.94) was found between `tribalism_score` and `manipulation_score` [3]. This indicates a strong relationship between in-group/out-group rhetoric and the use of strategic information distortion or emotional manipulation within this dataset.
*   **Supporting Evidence:**
    *   "The war on drugs, which has fueled so much of the explosion of our prison population, has really been a war on people - on certain people in certain communities and not on others." [14]
    *   "I'm aware that there are people in my party and in my state who will strenuously disapprove of my decision, and in some quarters I will be vehemently denounced." [15]
    *   "They want us to think that our lives are suffering because of the LGBT kid down the street or because of the mixed status family or the dreamer down the block who's just trying to make a better life for themselves. But we're smarter than that Greeley." [16]

### **Claim 7: Composite Index Opposition**

*   **Hypothesis:** Exploratory.
*   **Testability:** This claim is testable.
*   **Statistical Results:** Analysis of the derived `virtue_index` and `pathology_index` scores confirms a strong negative correlation [5]. This finding validates the framework's core tension at an aggregate level, showing that as overall virtue scores increase, overall pathology scores tend to decrease.
*   **Supporting Evidence:**
    *   "And you don't have to believe, of course, that the 20,000 or at least most of the 20,000 newcomers are bad people. In fact, I imagine that many of them are very good people." [17]
    *   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [18]
    *   "Our criminal justice system, as it stands right now, is an affront to who we say we are as a nation. We profess - we actually swear an oath to the flag - that we are a nation of liberty and justice for all. But our criminal justice system violates those values." [19]

### **Claim 8: H1 Speaker Group Differentiation**

*   **Hypothesis:** The 10 CAF dimensions will show statistically significant differences between speakers.
*   **Testability:** This claim is testable, but significance testing (e.g., a t-test) was not performed due to small group sizes.
*   **Statistical Results:** An observational grouping of speakers based on the `expert_categorization` in the corpus manifest reveals a pattern in `civic_character_index` scores. Speakers categorized as "Institutional" (Booker, McCain, Romney) exhibited higher scores (0.83, 0.89, 0.86, respectively) than those categorized as "Populist" (Ocasio-Cortez, Sanders, Vance, King), who scored 0.45, 0.44, 0.23, and 0.24, respectively [5].
*   **Supporting Evidence:**
    *   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." [20]
    *   "But, Greeley, that means our communities choosing and voting for Democrats and elected officials who know how to stand for the working class." [21]
    *   "Abraham Lincoln talked about a government of the people, by the people, for the people." [22]

## **Evidence References**

| Ref. | Document | Dimension | Confidence |
|:---|:---|:---|:---|
| [1] | john_mccain_2008_concession.txt | truth | 1.00 |
| [2] | jd_vance_2022_natcon_conference.txt | Dignity | 0.85 |
| [3] | alexandria_ocasio_cortez_2025_fighting_oligarchy.txt | Tribalism | 0.90 |
| [4] | cory_booker_2018_first_step_act.txt | Dignity | 0.90 |
| [5] | jd_vance_2022_natcon_conference.txt | Dignity | 0.85 |
| [6] | john_mccain_2008_concession.txt | dignity | 0.95 |
| [7] | cory_booker_2018_first_step_act.txt | Hope | 0.90 |
| [8] | john_mccain_2008_concession.txt | truth | 1.00 |
| [9] | jd_vance_2022_natcon_conference.txt | Tribalism | 1.00 |
| [10] | steve_king_2017_house_floor.txt | Truth | 0.90 |
| [11] | alexandria_ocasio_cortez_2025_fighting_oligarchy.txt | Dignity | 0.95 |
| [12] | john_lewis_1963_march_on_washington.txt | Dignity | 0.95 |
| [13] | mitt_romney_2020_impeachment.txt | Dignity | 0.95 |
| [14] | cory_booker_2018_first_step_act.txt | Tribalism | 0.80 |
| [15] | mitt_romney_2020_impeachment.txt | Tribalism | 0.95 |
| [16] | alexandria_ocasio_cortez_2025_fighting_oligarchy.txt | Tribalism | 0.90 |
| [17] | jd_vance_2022_natcon_conference.txt | Dignity | 0.85 |
| [18] | john_mccain_2008_concession.txt | dignity | 0.95 |
| [19] | cory_booker_2018_first_step_act.txt | Justice | 0.95 |
| [20] | john_mccain_2008_concession.txt | dignity | 0.95 |
| [21] | alexandria_ocasio_cortez_2025_fighting_oligarchy.txt | Pragmatism | 0.90 |
| [22] | bernie_sanders_2025_fighting_oligarchy.txt | Dignity | 0.80 |

## **Technical Transparency**

*   **Limitations:** The experiment's primary limitation is the small sample size (N=8), with each of the eight speakers represented by a single text. This sample size is insufficient for the planned statistical significance tests (e.g., ANOVA, t-tests). Consequently, all findings are descriptive and correlational and should not be generalized without further research on a larger, more diverse corpus.
*   **Models Used:**
    *   Analysis: `vertex_ai/gemini-2.5-pro`
    *   Synthesis: `vertex_ai/gemini-2.5-pro`
*   **Cost Summary:** `[Placeholder]`

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1144 USD  
**Total Tokens**: 40,364  
**Run Timestamp**: 20250808T143134Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0554 USD (19,301 tokens, 1 calls, $0.0554 avg/call)
- **Derived Metrics Analysis Planning**: $0.0590 USD (21,063 tokens, 1 calls, $0.0590 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1144 USD (40,364 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0554 USD (19,301 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0590 USD (21,063 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
