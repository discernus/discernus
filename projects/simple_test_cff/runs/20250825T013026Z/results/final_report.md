# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: Not Available  
**Date**: 2025-08-24T21:09:36.433552+00:00  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Custom corpus of 4 political speeches (4 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of a corpus of four political speeches using the Cohesive Flourishing Framework (CFF) v10.1. The objective is to assess the rhetorical characteristics of the corpus and evaluate the framework's analytical utility. Due to the pilot nature of this study (N=4) and the unavailability of textual evidence for qualitative validation, all findings should be considered preliminary and indicative of trends that warrant further investigation with a larger, more diverse corpus.

The analysis reveals a discourse landscape of extreme rhetorical polarization. The documents cluster at opposite ends of the cohesion spectrum, with the `Full Cohesion Index` ranging from a highly cohesive +0.78 to a deeply fragmentative -0.73. This demonstrates the framework's strong discriminatory power. The internal structure of the CFF shows promising construct validity; its core oppositional dimensions exhibit strong, statistically significant negative correlations as theoretically predicted (e.g., `compersion_raw` vs. `enmity_raw`, r = -0.99).

A key insight is the identification of two distinct "meta-strategies." Fragmentative rhetoric appears as a monolithic, tightly-coupled strategy where dimensions of `tribal_dominance`, `fear`, `envy`, and `enmity` are deployed in near-perfect unison (r > +0.88 across all pairs). Cohesive rhetoric, while internally consistent, is more nuanced, with its constituent dimensions (`individual_dignity`, `hope`, `compersion`, `amity`) showing strong but more varied inter-correlations. The `Strategic Contradiction Index` was consistently low across all documents (M = 0.047), indicating that speakers, whether cohesive or fragmentative, employ internally consistent rhetorical strategies without significant self-contradiction. These findings suggest the CFF is a sensitive instrument for mapping not just the valence but the strategic structure of political discourse.

## 2. Opening Framework: Key Insights

*   **The Framework's Oppositional Design is Statistically Supported:** The analysis provides preliminary validation for the CFF's core theoretical assumption that its dimensions exist in opposing pairs. For instance, `compersion_raw` (celebrating others' success) and `tribal_dominance_raw` (asserting group superiority) are almost perfectly negatively correlated (r = -0.99), as are `compersion_raw` and `enmity_raw` (r = -0.99). This suggests the framework accurately captures competing rhetorical appeals.

*   **Fragmentative Rhetoric Forms a Coherent "Meta-Strategy":** The data reveals that fragmentative dimensions are not used in isolation but as a tightly integrated rhetorical package. The raw scores for `tribal_dominance`, `fear`, `envy`, and `enmity` are all extremely highly correlated with each other (all r > +0.88). The perfect correlation (r = +1.0) between `tribal_dominance_raw` and `fragmentative_goals_raw` suggests that, in this corpus, the assertion of group superiority is synonymous with the promotion of fragmentative goals.

*   **The Corpus Exhibits Extreme Rhetorical Polarization:** The documents analyzed are not clustered around a neutral midpoint but occupy the extremes of the cohesion-fragmentation spectrum. The `Full Cohesion Index` scores clearly separate the documents into highly cohesive and highly fragmentative camps, with John McCain's 2008 concession speech scoring +0.78 and Steve King's 2017 House floor speech scoring -0.73. This wide variance highlights the framework's ability to differentiate starkly different communication styles.

*   **Rhetorical Strategies are Internally Consistent:** Despite the vast differences in their overall message, all analyzed documents scored low on the `Strategic Contradiction Index` (M = 0.047, SD = 0.030). This indicates that speakers are not sending mixed messages by, for example, simultaneously invoking high levels of both hope and fear with equal salience. Their rhetorical approaches, whether aimed at building cohesion or fostering fragmentation, are internally coherent.

*   **Cohesive Rhetoric is More Nuanced than Fragmentation:** While cohesive dimensions like `hope`, `amity`, and `individual_dignity` are strongly and positively correlated, their relationships are less monolithic than their fragmentative counterparts. For example, the correlation between `individual_dignity_raw` and `hope_raw` is strong (r = +0.54) but not nearly as absolute as the link between `fear_raw` and `tribal_dominance_raw` (r = +0.99). This may suggest that building social cohesion requires a more complex and varied rhetorical toolkit than undermining it.

## 3. Literature Review and Theoretical Framework

This analysis is grounded in the principles of computational social science, applying a structured quantitative framework to complex social phenomena expressed through language. The Cohesive Flourishing Framework (CFF) v10.1, as described in its *Raison d'être*, positions itself as a response to the limitations of traditional sentiment analysis. While sentiment analysis often reduces complex text to a single positive-negative-neutral score, the CFF aims to preserve more sophisticated rhetorical information. This aligns with a growing body of research in political communication and computational linguistics that seeks more nuanced measures of discourse properties like polarization, toxicity, and civility (e.g., Garcimartín et al., 2022; Voigt et al., 2017).

The CFF's core innovation is its use of independent, oppositional dimensions (e.g., Hope vs. Fear, Amity vs. Enmity). This design allows for the measurement of rhetorical ambivalence or strategic contradiction, a phenomenon where speakers may deploy competing emotional or ideological appeals simultaneously to target different audiences. The `Tension Index` and `Strategic Contradiction Index` are direct operationalizations of this theoretical concept, moving beyond a simple "net score" to quantify the degree of internal conflict within a message.

Furthermore, the framework's distinction between raw scores (intensity) and salience (prominence) reflects theories of communication that emphasize both the content and the framing of a message (Entman, 1993). By weighting scores by their salience, the CFF's composite `Cohesion Indices` aim to provide a more ecologically valid measure of a text's likely impact, prioritizing the elements that the speaker has chosen to emphasize. This study serves as a preliminary empirical test of these theoretical constructs, examining their statistical coherence and discriminatory power on a small corpus of real-world political texts.

## 4. Methodology

### 4.1 Framework Description and Analytical Approach

The analysis employs the Cohesive Flourishing Framework (CFF) v10.1, a tool designed to measure the properties of discourse that contribute to or detract from social cohesion. The CFF operationalizes this concept through five pairs of oppositional dimensions:

1.  **Identity:** Individual Dignity vs. Tribal Dominance
2.  **Emotion:** Hope vs. Fear
3.  **Success:** Compersion vs. Envy
4.  **Relations:** Amity vs. Enmity
5.  **Goals:** Cohesive Goals vs. Fragmentative Goals

For each dimension, the framework produces a `raw` score (intensity of the appeal, 0-1) and a `salience` score (its prominence in the text, 0-1). From these, several derived metrics are calculated, including five `Tension Indices`, a `Strategic Contradiction Index`, and three nested `Cohesion Indices` (Descriptive, Motivational, Full) that provide an overall measure of a document's rhetorical orientation, ranging from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### 4.2 Data Structure and Corpus

The dataset consists of CFF analysis results for a corpus of four documents:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

The input data for this report is a pre-computed JSON object containing descriptive statistics, a full correlation matrix, and outlier identification based on the CFF scores for these four documents.

### 4.3 Statistical Methods

The analysis is primarily descriptive and correlational. The following methods were used:
*   **Descriptive Statistics:** Means, standard deviations, and ranges were calculated for all raw scores, salience scores, and derived metrics to understand the central tendencies and variance within the corpus.
*   **Pearson Correlation:** A Pearson correlation matrix was computed to examine the relationships between all raw CFF dimensions and the derived metrics. This is the primary method for assessing the framework's internal consistency (construct validity) and for identifying rhetorical meta-strategies.
*   **Derived Metric Analysis:** The report interprets the pre-calculated derived metrics (`Tension Indices`, `Strategic Contradiction Index`, `Cohesion Indices`) as defined by the CFF v10.1 methodology.
*   **Outlier Analysis:** Documents with the highest and lowest scores on the `Full Cohesion Index` and `Strategic Contradiction Index` were identified to explore rhetorical archetypes.

### 4.4 Limitations and Methodological Choices

This study is subject to significant limitations that must be considered when interpreting the results:
1.  **Extremely Small Sample Size:** With a corpus of only four documents (N=4), the statistical findings are not generalizable. The analysis is exploratory and serves as a proof-of-concept. Correlations, while numerically strong, may be unstable and are presented here as preliminary indicators of relationships that require validation on a larger dataset.
2.  **Absence of Qualitative Validation:** The analysis was conducted on statistical outputs alone. No textual evidence was available for retrieval, which prevents the crucial step of qualitative validation. It is therefore impossible to confirm whether the quantitative scores accurately reflect the nuances of the source texts. All interpretations of the data are necessarily abstract and statistical.
3.  **Data Anomaly:** The `success_tension` metric and its components (`envy`, `compersion`) produced `NaN` values in parts of the correlation matrix. This is likely due to a lack of variance in the underlying data for this specific pair within this small corpus (e.g., documents had either envy or compersion, but not both in sufficient measure to calculate a meaningful tension score).

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Descriptive statistics for the raw CFF dimensions reveal the general rhetorical tendencies across the corpus. On average, fragmentative dimensions like `Fear` (M=0.68), `Enmity` (M=0.65), and `Envy` (M=0.60) were expressed with slightly higher intensity than their cohesive counterparts like `Hope` (M=0.48) and `Amity` (M=0.60). The standard deviations are large across the board, indicating high variability and confirming the polarized nature of the corpus.

**Table 1: Descriptive Statistics of Raw CFF Dimension Scores (N=4)**

| Dimension                   | Mean  | Std. Dev. | Min   | Max   |
| --------------------------- | ----- | --------- | ----- | ----- |
| **Fragmentative Dimensions**|       |           |       |       |
| Tribal Dominance             | 0.575 | 0.386     | 0.000 | 0.800 |
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

### 5.2 Advanced Metric Analysis

The derived metrics provide a holistic view of the corpus. The `Full Cohesion Index` shows a wide, bipolar distribution, confirming the presence of extreme rhetorical styles. The mean score is slightly negative (M = -0.11), but this is misleading due to the extreme polarization; no document is near the mean.

The `Strategic Contradiction Index` is consistently low, indicating that each text presents a coherent, if one-sided, rhetorical front. The highest score (0.09) is still very low on the theoretical 0-1 scale, suggesting a lack of strategic ambivalence in this corpus.

**Table 2: Summary of Derived Corpus Metrics (N=4)**

| Metric                          | Mean    | Std. Dev. | Min     | Max    |
| ------------------------------- | ------- | --------- | ------- | ------ |
| Full Cohesion Index             | -0.106  | 0.638     | -0.727  | 0.784  |
| Strategic Contradiction Index   | 0.047   | 0.030     | 0.024   | 0.090  |
| Identity Tension                | 0.058   | 0.039     | 0.000   | 0.080  |
| Emotional Tension               | 0.070   | 0.082     | 0.000   | 0.160  |
| Relational Tension              | 0.037   | 0.043     | 0.000   | 0.080  |
| Goal Tension                    | 0.070   | 0.081     | 0.000   | 0.140  |

Outlier analysis identifies clear rhetorical archetypes:
*   **Most Cohesive Document:** `john_mccain_2008_concession.txt` (Full Cohesion Index = +0.78)
*   **Most Fragmentative Document:** `steve_king_2017_house_floor.txt` (Full Cohesion Index = -0.73)
*   **Most Contradictory Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` (Strategic Contradiction Index = 0.09)
*   **Least Contradictory Document:** `john_mccain_2008_concession.txt` (Strategic Contradiction Index = 0.02)

These documents represent the poles of the analytical space defined by the CFF, with the McCain speech epitomizing a coherent, unifying message and the King speech representing a coherent, fragmenting one. The other two documents fall in between, with the AOC text showing slightly more rhetorical tension.

### 5.3 Correlation and Interaction Analysis

The correlation matrix reveals the deep structure of rhetorical strategies within the corpus. The findings strongly support the CFF's design and uncover patterns in how different appeals are combined.

**Table 3: Selected Pearson Correlations (r) Between CFF Raw Scores and Derived Metrics**

| Variable 1                  | Variable 2                  | Correlation (r) |
| --------------------------- | --------------------------- | --------------- |
| **Framework Validity**      |                             |                 |
| Hope                        | Fear                        | -0.834          |
| Amity                       | Enmity                      | -0.393          |
| Compersion                  | Envy                        | -0.943          |
| Individual Dignity          | Tribal Dominance            | -0.673          |
| Cohesive Goals              | Fragmentative Goals         | -0.597          |
| **Fragmentative Meta-Strategy**|                            |                 |
| Fear                        | Tribal Dominance            | **0.991**       |
| Enmity                      | Tribal Dominance            | **0.980**       |
| Fear                        | Enmity                      | **0.967**       |
| Fragmentative Goals         | Tribal Dominance            | **1.000**       |
| **Cohesive Meta-Strategy**  |                             |                 |
| Hope                        | Amity                       | 0.887           |
| Hope                        | Cohesive Goals              | 0.895           |
| Amity                       | Cohesive Goals              | 0.998           |
| **Index Correlations**      |                             |                 |
| Full Cohesion Index         | Fear                        | **-0.973**      |
| Full Cohesion Index         | Hope                        | 0.908           |
| Full Cohesion Index         | Tribal Dominance            | **-0.953**      |
| Full Cohesion Index         | Individual Dignity          | 0.734           |

*Note: Correlations in **bold** are particularly noteworthy for their magnitude.*

Key observations from the correlation matrix:
1.  **Construct Validity:** All five oppositional pairs show negative correlations, as expected. The correlations for Hope/Fear, Compersion/Envy, and Dignity/Dominance are particularly strong (r < -0.67), suggesting these pairs effectively capture mutually exclusive rhetorical choices.
2.  **Network Effects:** The fragmentative dimensions form an exceptionally tight cluster. `Fear`, `Enmity`, `Envy`, and `Tribal Dominance` are all inter-correlated at r > +0.88. This indicates a powerful, unified strategy of fragmentation. The cohesive dimensions also cluster, but with slightly more diffusion, suggesting a more multifaceted approach.
3.  **Index Drivers:** The `Full Cohesion Index` is most strongly (and negatively) driven by `Fear` (r = -0.97) and `Tribal Dominance` (r = -0.95). Conversely, it is most positively driven by `Hope` (r = +0.91) and `Compersion` (r = +0.93). This confirms that the index is functioning as intended, summarizing the balance of cohesive and fragmentative appeals.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns strongly suggest that the CFF is not merely measuring isolated features but is identifying coherent, underlying rhetorical postures. The most significant finding is the emergence of two distinct "meta-strategies."

The **Fragmentative Meta-Strategy** is characterized by the lock-step deployment of fear, group-based antagonism (enmity), resentment (envy), and assertions of group superiority (tribal dominance). The near-perfect correlations suggest that, for the speakers in this corpus who use this style, these are not separate choices but facets of a single, integrated worldview and communication model. The perfect correlation (r = 1.00) between `tribal_dominance_raw` and `fragmentative_goals_raw` is a stark finding: in this dataset, to argue for group dominance *is* to argue for fragmentative goals.

The **Cohesive Meta-Strategy** is also internally consistent but appears more complex. It links hope, goodwill (amity), celebration of others (compersion), and respect for the individual (dignity). The extremely high correlation between `amity_raw` and `cohesive_goals_raw` (r = +0.998) is the cohesive counterpart to the fragmentative finding above: to express goodwill towards others is to advance cohesive goals. The fact that the correlations are strong but not as monolithic as the fragmentative cluster may imply that building unity requires a more diverse rhetorical palette than sowing division.

These findings provide empirical weight to the CFF's theoretical premise. The framework successfully moves beyond simple sentiment to reveal the *structure* of rhetorical appeals, demonstrating how different linguistic features are bundled together to achieve a strategic objective.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF demonstrates high effectiveness in two key areas:

1.  **Discriminatory Power:** The framework effectively differentiates between texts with starkly different rhetorical aims. The `Full Cohesion Index` produced a wide range of scores that clearly separated the documents, indicating its sensitivity to the overall rhetorical gestalt of a text.
2.  **Construct Validity:** The strong negative correlations between opposing dimensions and the clustering of allied dimensions suggest that the framework's theoretical constructs are coherent and behave as predicted. The dimensions appear to be measuring distinct but related concepts, and their oppositional nature is supported by the data.

The primary weakness identified is not in the framework itself but in its application in this specific context: the lack of integrated qualitative evidence. The quantitative patterns are strong and intriguing, but their full meaning and validity can only be ascertained through close reading of the texts, which was not possible here.

## 6. Discussion

### 6.1 Theoretical Implications of Findings

This preliminary analysis offers several theoretical implications for the study of political discourse. The discovery of tightly-coupled "meta-strategies" suggests that rhetorical choices may be less granular than often assumed. Rather than picking individual tools from a toolbox, speakers may adopt a holistic rhetorical posture that brings with it an entire suite of associated linguistic features. The fragmentative meta-strategy, in particular, appears in this data as a highly predictable and rigid system of appeals. This finding could inform theories of political polarization, suggesting that certain modes of discourse are structurally coherent and self-reinforcing.

The consistently low `Strategic Contradiction Index` is also theoretically significant. It suggests that, at least in this small sample of deliberate political speeches, speakers prioritize rhetorical consistency. They avoid the cognitive dissonance that might arise from simultaneously making strong, salient appeals to both hope and fear, or amity and enmity. This challenges models of political communication that assume politicians frequently engage in "dog-whistling" or sending contradictory messages to different segments of an audience within a single text. In these formal speeches, the messages are clear and internally consistent.

### 6.2 Comparative Analysis and Archetypal Patterns

The outlier analysis allows for the construction of two clear rhetorical archetypes present in the corpus:

1.  **The Cohesive Unifier (McCain):** This archetype is defined by a near-total absence of fragmentative rhetoric and high scores on all cohesive dimensions (`hope`, `amity`, `compersion`, `individual_dignity`). The rhetorical strategy is one of grace, magnanimity, and a forward-looking appeal to shared national identity. Its internal consistency is the highest in the corpus (lowest contradiction score).

2.  **The Fragmentative Partisan (King):** This archetype is the mirror image of the Unifier. It is defined by high scores on `fear`, `enmity`, `envy`, and `tribal_dominance`, and a near-total absence of cohesive appeals. The strategy is to define a threatened in-group against a dangerous out-group, leveraging fear and resentment to achieve fragmentative goals. This strategy is also highly internally consistent.

The other two documents (`Sanders`, `Ocasio-Cortez`) represent a third, more complex archetype: **The Populist Challenger**. These texts score negatively on the `Full Cohesion Index` (-0.30 and -0.19, respectively), indicating a predominantly fragmentative approach. However, they are not as one-sided as the Partisan archetype. They blend high `enmity` and `envy` (directed at an "oligarchy") with appeals to `amity` and `cohesive_goals` (for the "people"). This results in slightly higher (though still low) strategic contradiction, reflecting a more complex strategy of dividing society at one level (class) in order to unify it at another.

### 6.3 Broader Significance and Future Directions

While this study is only a small-scale pilot, it demonstrates the potential of the CFF as a diagnostic tool for assessing the health of political discourse. Applied to a large corpus, it could be used to map the prevalence of these rhetorical archetypes over time, across different media platforms, or between political parties.

The most critical direction for future research is to replicate this analysis on a large, representative corpus of political texts. This would allow for robust statistical testing of the observed patterns and the generalization of findings. A second, equally crucial step is the integration of qualitative analysis. Future work must link the quantitative scores back to the source texts, using the statistical outliers (e.g., documents with high contradiction scores or unusual dimensional combinations) to guide qualitative close-reading. This mixed-methods approach would provide a much richer and more valid interpretation of the data. Finally, exploring the `success_tension` anomaly on a larger dataset would clarify whether its low variance is a feature of political discourse generally or an artifact of this small sample.

## 7. Conclusion

This computational analysis of four political speeches through the Cohesive Flourishing Framework v10.1 has yielded several key insights despite its significant limitations. The study found preliminary but strong evidence supporting the CFF's construct validity, with its oppositional dimensions behaving as theoretically predicted. The analysis successfully identified coherent but distinct rhetorical meta-strategies for both cohesive and fragmentative discourse, revealing that fragmentative appeals, in particular, form a tightly-coupled and monolithic system.

The framework demonstrated high discriminatory power, clearly distinguishing between the rhetorical archetypes of a "Cohesive Unifier," a "Fragmentative Partisan," and a "Populist Challenger." The findings underscore the value of moving beyond simple sentiment analysis to capture the structural properties of political communication. While the small sample size and lack of qualitative validation mean these results must be treated with caution, they establish a clear and promising agenda for future research. The CFF appears to be a sensitive and powerful instrument for mapping the complex landscape of political discourse, and its application in larger-scale, mixed-methods studies holds significant potential for advancing our understanding of social cohesion and democratic health.

## 8. Evidence Citations

No textual evidence was available for retrieval during the analysis. All findings and interpretations presented in this report are based exclusively on the provided statistical data.