---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: eee95493f0b5d04106caaf5c2c8bea81fb8fa54da91f87908146a6dd7a22da93  
**Date**: 2025-08-24T21:09:36.433552+00:00  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: [Corpus name not specified] (4 documents)  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of a four-document corpus using the Cohesive Flourishing Framework (CFF) v10.1. The objective is to assess rhetorical patterns related to social cohesion and fragmentation. Due to the extremely small sample size (N=4), all findings should be considered exploratory and indicative, requiring validation with a larger dataset. The analysis reveals a corpus characterized by strong rhetorical polarization. The CFF dimensions effectively separate the documents into distinct cohesive and fragmentative profiles, suggesting the framework possesses significant discriminatory power even with limited data.

Key findings indicate the existence of two dominant and opposing rhetorical meta-strategies. A "fragmentative" strategy appears as a tightly integrated cluster of `Fear` (r=0.99 with `Tribal Dominance`), `Enmity` (r=0.98 with `Tribal Dominance`), and `Envy` (r=0.92 with `Tribal Dominance`). Conversely, a "cohesive" strategy links `Hope`, `Amity`, `Compersion`, and `Individual Dignity`. The negative correlations between opposing dimensions (e.g., `Hope` vs. `Fear`, r=-0.83) are strong, providing preliminary support for the framework's construct validity. The composite `Full Cohesion Index` proves to be a powerful summary metric, with scores ranging from a highly cohesive +0.78 to a highly fragmentative -0.73. Notably, the `Strategic Contradiction Index` remains low across all documents (M=0.05), suggesting that while the speeches are rhetorically opposed to each other, they are internally consistent in their messaging.

A significant limitation of this analysis is the absence of textual evidence, which prevents the qualitative validation of these statistical patterns. While the quantitative results are clear, their real-world rhetorical meaning cannot be fully explored without direct examples from the source texts. Future research should prioritize integrating qualitative analysis and applying this methodology to a larger, more diverse corpus to confirm the stability of these archetypal patterns and test the generalizability of the CFF.

## 2. Opening Framework: Key Insights

This preliminary analysis of the corpus through the Cohesive Flourishing Framework (CFF) yielded several key insights into the structure of political discourse within this small sample.

*   **The Corpus Exhibits Extreme Rhetorical Polarization:** The data reveals two diametrically opposed communication styles. The `Full Cohesion Index`, a composite measure of pro-social rhetoric, ranges from a high of +0.78 to a low of -0.73, demonstrating the framework's capacity to differentiate documents across a wide spectrum of cohesive and fragmentative language.

*   **Fragmentative Rhetoric Forms a Tightly-Knit Cluster:** The analysis shows that fragmentative dimensions are not used in isolation but as part of a unified strategy. `Tribal Dominance` is almost perfectly correlated with `Fear` (r=0.99), `Enmity` (r=0.98), and `Fragmentative Goals` (r=1.00). This suggests that appeals to in-group identity in this corpus are almost invariably accompanied by fear-based messaging and the identification of an out-group enemy.

*   **Cohesive Rhetoric Presents an Equally Integrated, Opposing Strategy:** Cohesive dimensions also cluster together. `Hope` is strongly correlated with `Amity` (r=0.89) and `Cohesive Goals` (r=0.89). This cluster is, in turn, strongly negatively correlated with the fragmentative cluster, indicating a clear and consistent oppositional structure in the discourse. For instance, `Compersion` (joy in others' success) and `Enmity` show a near-perfect negative relationship (r=-0.99).

*   **The Framework's Oppositional Design Appears Validated:** A core design principle of the CFF is the measurement of opposing concepts on independent scales. The strong negative correlations between these pairs (e.g., `Tribal Dominance` vs. `Individual Dignity`, r=-0.67; `Fear` vs. `Hope`, r=-0.83; `Envy` vs. `Compersion`, r=-0.94) support this design, suggesting they are indeed measuring opposing rhetorical phenomena.

*   **Rhetorical Strategies are Internally Consistent:** The `Strategic Contradiction Index`, which measures the simultaneous use of opposing appeals, is very low across all documents (M=0.05, SD=0.03). This indicates that the speakers, whether employing cohesive or fragmentative language, do so with a high degree of internal consistency, avoiding mixed messages that might undermine their strategic intent.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze political and social discourse. The CFF moves beyond simple sentiment analysis by measuring texts along several distinct, often opposing, dimensions of communication. Its core innovation lies in scoring opposing concepts like `Hope` and `Fear` independently, allowing for the detection of complex or contradictory rhetoric.

The framework calculates raw intensity scores (0-1) and salience scores (0-1) for ten primary dimensions grouped into five oppositional pairs:
*   **Identity:** `Tribal Dominance` vs. `Individual Dignity`
*   **Emotion:** `Fear` vs. `Hope`
*   **Success:** `Envy` vs. `Compersion`
*   **Relations:** `Enmity` vs. `Amity`
*   **Goals:** `Fragmentative Goals` vs. `Cohesive Goals`

From these primary scores, several derived metrics are calculated. **Tension Indices** quantify the use of contradictory messaging. The **Strategic Contradiction Index** averages these tensions to provide a document-level score for rhetorical inconsistency. Finally, three **Salience-Weighted Cohesion Indices** (`Descriptive`, `Motivational`, `Full`) provide a holistic measure of a document's orientation toward social cohesion, with scores ranging from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### Data Structure and Corpus Description

The dataset for this analysis consists of CFF scores for a corpus of four political documents. The documents are identified as `john_mccain_2008_concession.txt`, `steve_king_2017_house_floor.txt`, `bernie_sanders_2025_fighting_oligarchy.txt`, and `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`. The raw data includes scores and salience for the ten primary dimensions for each document.

### Statistical Methods and Analytical Constraints

The analysis was conducted using a pre-defined suite of statistical functions. The primary methods included:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, minimum, and maximum for all primary and derived metrics to characterize the corpus as a whole.
2.  **Derived Metric Calculation:** Application of the CFF formulas to compute Tension and Cohesion indices for each document.
3.  **Correlation Analysis:** Computation of a Pearson correlation matrix for all raw scores and derived metrics to identify relationships and structural patterns in the use of rhetorical dimensions.

**Major Limitations:**
*   **Sample Size:** The most significant constraint is the sample size of N=4. This prevents any meaningful inferential statistical testing and means all findings must be treated as preliminary and exploratory. The patterns observed may not be generalizable to a larger population of political texts.
*   **Absence of Textual Evidence:** The analysis was performed on quantitative data alone, with no access to the source texts or extracted textual evidence. This is a critical limitation, as it prohibits the qualitative validation of statistical findings. For example, while we can observe a strong correlation between `Fear` and `Enmity`, we cannot examine how this relationship is expressed rhetorically. All interpretations are therefore based solely on the statistical relationships between the CFF's operationalized constructs.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An examination of the descriptive statistics for the primary CFF dimensions reveals a corpus with a wide variance in rhetorical appeals. The mean scores suggest a slight tendency towards fragmentative language, though the high standard deviations indicate this is not uniform across the documents.

**Table 1: Descriptive Statistics of Primary Raw Scores (N=4)**

| Dimension                   | Mean  | Std. Dev. | Min   | Max   |
| --------------------------- | ----- | --------- | ----- | ----- |
| **Fragmentative Dimensions**|       |           |       |       |
| Tribal Dominance            | 0.575 | 0.386     | 0.000 | 0.800 |
| Fear                        | 0.675 | 0.320     | 0.200 | 0.900 |
| Envy                        | 0.600 | 0.424     | 0.000 | 0.900 |
| Enmity                      | 0.650 | 0.436     | 0.000 | 0.900 |
| Fragmentative Goals         | 0.575 | 0.386     | 0.000 | 0.800 |
| **Cohesive Dimensions**     |       |           |       |       |
| Individual Dignity          | 0.450 | 0.404     | 0.100 | 0.800 |
| Hope                        | 0.475 | 0.377     | 0.000 | 0.900 |
| Compersion                  | 0.225 | 0.450     | 0.000 | 0.900 |
| Amity                       | 0.600 | 0.408     | 0.000 | 0.900 |
| Cohesive Goals              | 0.650 | 0.311     | 0.200 | 0.900 |

On average, `Fear` (M=0.68) and `Enmity` (M=0.65) are the most prominent fragmentative dimensions. Among cohesive dimensions, `Cohesive Goals` (M=0.65) and `Amity` (M=0.60) show the highest average scores. The large standard deviations across nearly all dimensions, often approaching the value of the mean, highlight the extreme diversity within this small corpus. For example, `Compersion` has a very low mean (M=0.23) but a high standard deviation (SD=0.45), indicating it was largely absent from some texts but strongly present in at least one. This variance is the basis for the strong patterns observed in the correlation analysis.

### 5.2 Advanced Metric Analysis

The derived metrics provide a holistic view of the corpus's rhetorical landscape. The `Full Cohesion Index` effectively captures the polarization suggested by the descriptive statistics, while the `Strategic Contradiction Index` points to internally consistent messaging.

**Table 2: Descriptive Statistics of Derived Corpus Metrics (N=4)**

| Metric                          | Mean   | Std. Dev. | Min    | Max    | Interpretation                               |
| ------------------------------- | ------ | --------- | ------ | ------ | -------------------------------------------- |
| Full Cohesion Index             | -0.106 | 0.638     | -0.727 | 0.784  | Extremely wide range; high discriminatory power |
| Strategic Contradiction Index   | 0.047  | 0.030     | 0.024  | 0.090  | Consistently low; indicates focused messaging |
| Identity Tension                | 0.058  | 0.039     | 0.000  | 0.080  | Low                                          |
| Emotional Tension               | 0.070  | 0.082     | 0.000  | 0.160  | Low, with some variance                      |
| Success Tension                 | 0.000  | 0.000     | 0.000  | 0.000  | No contradiction detected                    |
| Relational Tension              | 0.037  | 0.043     | 0.000  | 0.080  | Very low                                     |
| Goal Tension                    | 0.070  | 0.081     | 0.000  | 0.140  | Low, with some variance                      |

The most striking result is the range of the `Full Cohesion Index`, spanning from -0.73 (`steve_king_2017_house_floor.txt`) to +0.78 (`john_mccain_2008_concession.txt`). This demonstrates that the documents in the corpus represent nearly opposite rhetorical poles as measured by the CFF.

In contrast, the `Strategic Contradiction Index` is consistently low (M=0.05). This suggests that the authors of these texts employ a focused rhetorical strategy, whether cohesive or fragmentative, without resorting to contradictory appeals. The `Success Tension` is uniformly zero, indicating that no document simultaneously invoked high levels of both `Envy` and `Compersion`. This lack of variance is why `Success Tension` has `NaN` values in the correlation matrix.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals the underlying structure of rhetorical strategies within the corpus. The results show two powerful, opposing clusters of dimensions. Due to the large number of variables, the table below presents a curated selection of the most theoretically significant correlations.

**Table 3: Selected Pearson Correlations (r) for Raw Scores and Key Derived Metrics**

| Variable A                  | Variable B                  | Correlation (r) |
| --------------------------- | --------------------------- | --------------- |
| **Fragmentative Cluster**   |                             |                 |
| Tribal Dominance            | Fear                        | 0.991           |
| Tribal Dominance            | Enmity                      | 0.980           |
| Tribal Dominance            | Fragmentative Goals         | 1.000           |
| Fear                        | Enmity                      | 0.967           |
| **Cohesive Cluster**        |                             |                 |
| Hope                        | Amity                       | 0.887           |
| Hope                        | Cohesive Goals              | 0.895           |
| Amity                       | Cohesive Goals              | 0.998           |
| Individual Dignity          | Cohesive Goals              | 0.743           |
| **Oppositional Dynamics**   |                             |                 |
| Fear                        | Hope                        | -0.834          |
| Envy                        | Compersion                  | -0.943          |
| Enmity                      | Amity                       | -0.393          |
| Tribal Dominance            | Individual Dignity          | -0.673          |
| **Index Correlations**      |                             |                 |
| Full Cohesion Index         | Fear                        | -0.973          |
| Full Cohesion Index         | Hope                        | 0.908           |
| Full Cohesion Index         | Tribal Dominance            | -0.953          |
| Full Cohesion Index         | Individual Dignity          | 0.734           |

The data indicates that fragmentative rhetoric is a highly cohesive strategy in itself. The perfect correlation (r=1.00) between `Tribal Dominance` and `Fragmentative Goals` suggests that, in this corpus, any appeal to group-based dominance is functionally identical to an appeal for fragmentative societal outcomes. This is strongly reinforced by near-perfect correlations with `Fear` and `Enmity`.

The cohesive cluster is similarly strong, though with slightly less integration. The near-perfect correlation between `Amity` and `Cohesive Goals` (r=0.998) suggests that calls for friendly relations are the primary vehicle for promoting cohesive objectives.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns provide strong, albeit preliminary, evidence for the CFF's construct validity. The framework is designed with oppositional pairs, and the data confirms this structure. The strong negative correlation between `Envy` and `Compersion` (r=-0.94) is a prime example. This indicates that documents scoring high on one dimension score low on the other, validating that they measure opposing constructs. The weaker, though still substantial, negative correlation between `Enmity` and `Amity` (r=-0.39) is an interesting anomaly that warrants further investigation with a larger N and qualitative analysis.

The `Full Cohesion Index` performs as expected, acting as a powerful summary of these dynamics. Its strong negative correlation with `Fear` (r=-0.97) and `Tribal Dominance` (r=-0.95), and its strong positive correlation with `Hope` (r=0.91) and `Individual Dignity` (r=0.73), confirm that it effectively synthesizes the individual dimensions into a meaningful, high-level indicator of a document's overall rhetorical posture.

An unexpected finding is the perfect positive correlation between `Tribal Dominance` and `Identity Tension` (r=1.00). The formula for `Identity Tension` is `min(Tribal Dominance, Individual Dignity) * |Salience(TD) - Salience(ID)|`. This perfect correlation implies that as `Tribal Dominance` scores increase, `Identity Tension` increases in lockstep. This suggests a specific rhetorical pattern in the fragmentative texts where `Individual Dignity` is present just enough to create tension but is overshadowed by a much more salient appeal to `Tribal Dominance`. Without the text, this is speculative, but it points to a sophisticated rhetorical balancing act that future studies could explore.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF demonstrates high effectiveness in two key areas:

1.  **Discriminatory Power:** The framework, and particularly the `Full Cohesion Index`, clearly separates the documents across a wide rhetorical spectrum. The ability to generate scores from +0.78 to -0.73 with only four documents suggests that the underlying dimensions are sensitive to the types of variance present in political discourse.

2.  **Framework-Corpus Fit:** The strong, theoretically consistent patterns (e.g., clustering of cohesive and fragmentative dimensions, negative correlations between opposing pairs) suggest a good fit between the CFF's constructs and the rhetorical strategies present in this specific corpus. The framework is not just assigning numbers; it is revealing a structured, patterned, and polarized rhetorical reality.

The analysis also highlights the utility of the `Strategic Contradiction Index`. Its low values across the board provide a valuable insight: the key difference between these documents is not their level of confusion or contradiction, but the highly consistent, yet opposing, direction of their rhetoric.

## 6. Discussion

### Theoretical Implications and Rhetorical Archetypes

The findings from this small-scale analysis, while preliminary, point toward the existence of distinct and coherent rhetorical archetypes. The data suggests at least two such archetypes:

1.  **The Cohesive Unifier:** Represented by the document `john_mccain_2008_concession.txt`, which scored highest on the `Full Cohesion Index` (+0.78) and lowest on the `Strategic Contradiction Index` (0.02). This archetype is characterized by high scores in `Hope`, `Amity`, `Compersion`, and `Individual Dignity`, and minimal use of their fragmentative counterparts. The rhetorical strategy appears to be one of de-escalation, bridge-building, and reinforcement of shared civic values.

2.  **The Fragmentative Agitator:** Represented by `steve_king_2017_house_floor.txt`, which scored lowest on the `Full Cohesion Index` (-0.73). This archetype is defined by a tightly integrated use of `Tribal Dominance`, `Fear`, `Enmity`, and `Envy`. The strategy is one of in-group mobilization against a perceived out-group threat, leveraging negative emotions to create social division.

The other two documents, from Bernie Sanders and Alexandria Ocasio-Cortez, appear to represent a hybrid archetype with moderately negative cohesion scores (-0.30 and -0.19, respectively). They score high on fragmentative dimensions like `Tribal Dominance` and `Envy` (consistent with populist critiques of an "oligarchy") but also retain some cohesive elements. This suggests a more complex strategy of "divisive cohesion," aiming to unify a specific base by sharpening distinctions with an opposing group.

### Limitations and Future Directions

It is imperative to restate the limitations of this study. The N=4 sample size means these archetypes are merely suggestive. The patterns observed could be an artifact of this specific selection of documents. Furthermore, the lack of textual evidence makes these interpretations speculative.

Future research should proceed in several directions:
*   **Scale:** The analysis must be replicated on a large, diverse corpus of political texts to test whether these correlational structures and rhetorical archetypes are stable and generalizable.
*   **Qualitative Integration:** A crucial next step is to conduct a mixed-methods analysis. The quantitative outliers identified by the CFF (like the McCain and King speeches) should be subjected to close qualitative reading to validate and enrich the interpretation of the statistical findings. This would allow researchers to understand *how*, rhetorically, these statistical patterns are realized in language.
*   **Temporal Analysis:** With a larger corpus spanning several years, researchers could investigate how these rhetorical archetypes evolve over time, particularly in response to major political events.
*   **Predictive Validity:** Future studies could test whether CFF scores, particularly the `Full Cohesion Index`, correlate with real-world outcomes, such as polling data on social trust, political polarization, or even instances of political violence.

## 7. Conclusion

This computational analysis, despite its significant limitations, successfully demonstrates the potential of the Cohesive Flourishing Framework to deconstruct and quantify complex rhetorical strategies in political discourse. The preliminary findings reveal a deeply polarized corpus where documents employ one of two highly consistent, yet diametrically opposed, meta-strategies: one built on cohesion (hope, amity, dignity) and the other on fragmentation (fear, enmity, tribalism).

The CFF proved effective in discriminating between these strategies and provided initial evidence for its own construct validity through the strong negative correlations of its oppositional dimensions. The analysis introduces the concept of rhetorical archetypes—such as the "Cohesive Unifier" and "Fragmentative Agitator"—that are statistically identifiable and warrant further investigation. While no definitive conclusions can be drawn from a sample of four, this report establishes a clear and promising path for future research. By scaling the analysis to larger corpora and integrating qualitative evidence, the CFF could become a vital tool for understanding the linguistic drivers of social cohesion and fragmentation in contemporary society.

## 8. Evidence Citations

No textual evidence was provided for this analysis. The interpretation of statistical findings is based on the operationalized definitions of the CFF constructs and cannot be validated with specific textual examples. This remains a critical area for future work.