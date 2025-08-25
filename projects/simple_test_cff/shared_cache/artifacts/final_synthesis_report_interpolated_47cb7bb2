# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: c50749fa73b3c03b0423c1aa8b3b186c5d3cba40ad449a625d39d554b2201090  
**Date**: 2025-08-24T21:09:36.433552+00:00  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: [Corpus filename not specified] (4 documents)  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of four political texts using the Cohesive Flourishing Framework (CFF) v10.1. The analysis reveals a corpus characterized by extreme rhetorical polarization. The documents cluster into two distinct profiles: one text exhibiting exceptionally high cohesive rhetoric and three texts displaying strongly fragmentative rhetoric. The primary finding is the identification of two opposing, internally consistent communication strategies. The fragmentative strategy is defined by a tight coupling of language invoking Tribal Dominance, Fear, Envy, and Enmity (average inter-correlation *r* > 0.9). Conversely, the cohesive strategy links appeals to Individual Dignity, Hope, Amity, and Compersion.

The CFF's derived metrics effectively quantify these patterns. The `Full Cohesion Index`, a composite measure of a text's overall impact on social cohesion, ranged dramatically from a highly fragmentative -0.73 to a highly cohesive +0.78, demonstrating the framework's discriminatory power. Furthermore, the `Strategic Contradiction Index` remained low across all documents (M = 0.047), indicating that each text, whether cohesive or fragmentative, employed a consistent and non-contradictory rhetorical strategy. The strong, theoretically-consistent negative correlations between opposing dimensions (e.g., Hope vs. Fear, *r* = -0.83) provide preliminary support for the framework's construct validity.

However, the findings of this report must be interpreted with significant caution. The analysis is based on an extremely small sample size (N=4), rendering the results exploratory and not generalizable. Furthermore, a critical limitation was the absence of retrievable textual evidence, which prevents the qualitative validation necessary to ground these statistical patterns in specific rhetorical examples. While the quantitative results are stark and suggestive, they represent a proof-of-concept for the CFF methodology rather than a definitive statement on the political discourse analyzed. Future research with a larger, more diverse corpus and integrated qualitative evidence is essential to validate and expand upon these initial insights.

## 2. Opening Framework: Key Insights

This analysis of a small but diverse political corpus using the Cohesive Flourishing Framework (CFF) yielded several key insights into the structure of political rhetoric.

*   **Extreme Rhetorical Polarization:** The corpus is not moderately divided but split into extreme opposites. The `Full Cohesion Index` scores show a clear bifurcation: one document scores +0.78 (highly cohesive), while the other three score -0.19, -0.30, and -0.73 (moderately to highly fragmentative). This suggests that the analyzed discourse operates at the poles of the cohesion-fragmentation spectrum.
*   **Identification of a "Fragmentative Rhetoric" Cluster:** The analysis reveals a powerful and consistent syndrome of fragmentative language. The dimensions of Tribal Dominance, Fear, Envy, and Enmity are exceptionally highly correlated (average Pearson's *r* > 0.9). This suggests that when speakers in this corpus use one of these fragmentative appeals, they almost invariably use the others, creating a unified narrative of threat, grievance, and out-group hostility.
*   **Identification of a "Cohesive Rhetoric" Cluster:** In direct opposition, a cohesive rhetorical strategy emerges, linking appeals to Individual Dignity, Hope, Amity, and Compersion. These dimensions are positively correlated with each other and strongly negatively correlated with the fragmentative cluster. For instance, the `Full Cohesion Index` correlates at *r* = 0.91 with Hope and *r* = -0.97 with Fear.
*   **Preliminary Validation of CFF's Oppositional Design:** The framework's structure, which pairs opposing concepts (e.g., Hope vs. Fear), appears robust. All five pairs of oppositional raw scores demonstrate strong to moderate negative correlations, such as `compersion_raw` vs. `envy_raw` (*r* = -0.94) and `tribal_dominance_raw` vs. `individual_dignity_raw` (*r* = -0.67). This indicates that the framework effectively measures these concepts as distinct and opposing poles.
*   **Rhetorical Consistency is the Norm:** The `Strategic Contradiction Index`, which measures the use of mixed or contradictory messaging, was consistently low across all four documents (M = 0.047, SD = 0.030). This finding is significant: it suggests that the speakers, regardless of their position on the cohesion spectrum, deliver internally consistent messages without simultaneously making strong appeals to opposing values.

## 3. Literature Review and Theoretical Framework

This study is situated at the intersection of computational social science, political communication, and social psychology. The Cohesive Flourishing Framework (CFF) addresses a central challenge in discourse analysis: how to measure the latent potential of language to either strengthen or weaken social bonds and democratic health. Traditional methods like sentiment analysis often classify text along a single positive-negative axis, failing to capture the complex, often simultaneous, deployment of varied rhetorical appeals (Pang & Lee, 2008).

The CFF's design is theoretically grounded in the concept of **affective polarization**, the tendency of citizens to feel more negatively toward opposing political parties and their members (Iyengar, Sood, & Lelkes, 2012). The framework's dimensions—such as Enmity vs. Amity and Tribal Dominance vs. Individual Dignity—are designed to operationalize the specific linguistic strategies that fuel this divide. By measuring these dimensions independently, the CFF can detect sophisticated strategies, such as "dog whistles" or contradictory messaging, that simpler models would miss.

Furthermore, the framework's focus on dimensions like Hope, Fear, Envy, and Compersion draws from psychological theories of intergroup relations and emotion (Smith & Mackie, 2008). Fear and Enmity are well-documented drivers of out-group derogation, while Hope and Amity can foster pro-social behavior and reconciliation. The CFF posits that the relative salience and intensity of these appeals in public discourse can serve as a leading indicator of a society's trajectory toward either social fragmentation or cohesive flourishing. This analysis, therefore, serves as an empirical test of the CFF's ability to quantify these theoretical constructs in real-world political texts.

## 4. Methodology

### Framework Description
This analysis employed the Cohesive Flourishing Framework (CFF) v10.1, a computational tool for analyzing political and social discourse. The CFF measures text along ten core dimensions, arranged in five oppositional pairs:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion
4.  **Relations:** Enmity vs. Amity
5.  **Goals:** Fragmentative Goals vs. Cohesive Goals

For each dimension, the framework generates a `raw` score (intensity, 0-1) and a `salience` score (prominence, 0-1). From these, it calculates several derived metrics, including Tension Indices, a `Strategic Contradiction Index`, and three composite `Cohesion Indices` (Descriptive, Motivational, Full) that provide an overall measure of a document's rhetorical effect, ranging from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### Corpus Description
The corpus consists of four American political texts:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

This small, purposively selected corpus includes texts from different political ideologies, time periods, and contexts (e.g., a concession speech, a floor speech, and campaign-style speeches).

### Statistical Methods
The analysis was conducted using the automated statistical functions generated for this experiment. The primary methods included:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation (SD), minimum, and maximum for all raw scores, salience scores, and derived metrics to understand central tendencies and distributions.
2.  **Pearson Correlation Analysis:** A correlation matrix was computed for all raw scores and derived metrics to identify relationships between rhetorical dimensions and validate the framework's oppositional structure.
3.  **Outlier Identification:** Documents with the highest and lowest scores on the `Full Cohesion Index` and `Strategic Contradiction Index` were identified to facilitate archetypal analysis.

### Analytical Constraints and Limitations
This study is subject to two severe limitations that must be acknowledged.
1.  **Extremely Small Sample Size:** With a sample of only four documents (N=4), the statistical findings are purely exploratory and cannot be generalized. The results should be viewed as a preliminary, indicative proof-of-concept for the CFF methodology. Inferences about statistical significance are not appropriate, and all observed patterns require validation on a much larger corpus.
2.  **Absence of Textual Evidence:** The automated analysis pipeline did not retrieve supporting textual evidence (quotes) for the quantitative scores. This is a critical omission. Without the ability to ground high scores for `Fear` or `Amity` in the actual words used by the speakers, the interpretation remains abstract. This prevents qualitative validation of the model's scoring and limits the depth of the analysis. All interpretations of what the scores *mean* are based on the theoretical definitions of the CFF dimensions, not on a direct analysis of the source text.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Descriptive statistics for the 20 primary raw and salience scores reveal a corpus with high variability, indicating significant rhetorical differences among the four documents. The standard deviations for most dimensions are large relative to their means, confirming that the texts are not rhetorically uniform.

For example, `tribal_dominance_raw` has a mean of 0.58 but a standard deviation of 0.39, with scores spanning from 0.0 to 0.8. Its cohesive counterpart, `individual_dignity_raw`, shows a similar pattern (M=0.45, SD=0.40). This high variance is observed across most oppositional pairs, including Fear (M=0.68, SD=0.32) vs. Hope (M=0.48, SD=0.38) and Enmity (M=0.65, SD=0.44) vs. Amity (M=0.60, SD=0.41). This suggests the corpus contains strong examples of both fragmentative and cohesive rhetoric, making it well-suited for testing the framework's discriminatory power.

**Table 1: Descriptive Statistics for CFF Raw and Salience Scores (N=4)**
| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Raw Scores** | | | | |
| tribal_dominance_raw | 0.58 | 0.39 | 0.00 | 0.80 |
| individual_dignity_raw | 0.45 | 0.40 | 0.10 | 0.80 |
| fear_raw | 0.68 | 0.32 | 0.20 | 0.90 |
| hope_raw | 0.48 | 0.38 | 0.00 | 0.90 |
| envy_raw | 0.60 | 0.42 | 0.00 | 0.90 |
| compersion_raw | 0.23 | 0.45 | 0.00 | 0.90 |
| enmity_raw | 0.65 | 0.44 | 0.00 | 0.90 |
| amity_raw | 0.60 | 0.41 | 0.00 | 0.90 |
| fragmentative_goals_raw | 0.58 | 0.39 | 0.00 | 0.80 |
| cohesive_goals_raw | 0.65 | 0.31 | 0.20 | 0.90 |
| **Salience Scores** | | | | |
| tribal_dominance_salience | 0.68 | 0.39 | 0.10 | 0.90 |
| individual_dignity_salience | 0.45 | 0.41 | 0.10 | 0.90 |
| fear_salience | 0.70 | 0.27 | 0.30 | 0.90 |
| hope_salience | 0.53 | 0.41 | 0.00 | 0.90 |
| envy_salience | 0.60 | 0.42 | 0.00 | 0.90 |
| compersion_salience | 0.25 | 0.50 | 0.00 | 1.00 |
| enmity_salience | 0.68 | 0.39 | 0.10 | 0.90 |
| amity_salience | 0.65 | 0.44 | 0.00 | 1.00 |
| fragmentative_goals_salience | 0.58 | 0.40 | 0.00 | 0.90 |
| cohesive_goals_salience | 0.68 | 0.32 | 0.20 | 0.90 |

### 5.2 Advanced Metric Analysis

Analysis of the CFF's derived metrics provides a higher-level view of the rhetorical strategies within the corpus. The `Full Cohesion Index` starkly illustrates the corpus's polarization. The mean score is slightly negative (M = -0.11, SD = 0.64), but this average obscures a bimodal distribution. As shown in Table 2, John McCain's speech is a strong positive outlier, while Steve King's is a strong negative outlier.

**Table 2: Outlier Documents by Key Derived Metrics**
| Metric | Document | Score |
| :--- | :--- | :--- |
| **Full Cohesion Index (Highest)** | john_mccain_2008_concession.txt | 0.784 |
| **Full Cohesion Index (Lowest)** | steve_king_2017_house_floor.txt | -0.727 |
| **Strategic Contradiction (Highest)** | alexandria_ocasio_cortez_2025... | 0.090 |
| **Strategic Contradiction (Lowest)** | john_mccain_2008_concession.txt | 0.024 |

The `Strategic Contradiction Index` is consistently low across all documents (M = 0.047, Max = 0.090), suggesting that each speaker employed an internally consistent rhetorical approach. They did not, for example, pair strong appeals to Hope with strong appeals to Fear. This indicates clear, unambiguous messaging, whether aimed at cohesion or fragmentation. The `success_tension` metric was uniformly zero, indicating that no document simultaneously invoked high levels of both Envy and Compersion.

**Table 3: Summary of Corpus-Level Derived Metrics (N=4)**
| Metric | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| identity_tension | 0.058 | 0.039 | 0.000 | 0.080 |
| emotional_tension | 0.070 | 0.082 | 0.000 | 0.160 |
| success_tension | 0.000 | 0.000 | 0.000 | 0.000 |
| relational_tension | 0.037 | 0.043 | 0.000 | 0.080 |
| goal_tension | 0.070 | 0.081 | 0.000 | 0.140 |
| **strategic_contradiction_index** | **0.047** | **0.030** | **0.024** | **0.090** |
| descriptive_cohesion_index | -0.172 | 0.666 | -0.787 | 0.772 |
| motivational_cohesion_index | -0.099 | 0.644 | -0.732 | 0.800 |
| **full_cohesion_index** | **-0.106** | **0.638** | **-0.727** | **0.784** |

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals the underlying structure of rhetorical strategies in the corpus. The results provide strong, albeit preliminary, support for the CFF's theoretical design and uncover two dominant, opposing meta-strategies.

**Framework Construct Validation:**
A key test for an oppositional framework is whether its paired dimensions are negatively correlated. The CFF performs well on this measure. All five pairs show moderate to strong negative correlations:
*   `compersion_raw` vs. `envy_raw`: **r = -0.94**
*   `hope_raw` vs. `fear_raw`: **r = -0.83**
*   `tribal_dominance_raw` vs. `individual_dignity_raw`: **r = -0.67**
*   `cohesive_goals_raw` vs. `fragmentative_goals_raw`: **r = -0.60**
*   `amity_raw` vs. `enmity_raw`: **r = -0.39**

This pattern suggests the framework is successfully measuring distinct and opposing rhetorical concepts. The extremely strong negative correlation between Compersion and Envy is particularly notable.

**Meta-Strategy Identification:**
The matrix clearly shows two tightly clustered sets of dimensions.
1.  **The Fragmentative Cluster:** `tribal_dominance_raw`, `fear_raw`, `envy_raw`, and `enmity_raw` are all exceptionally highly correlated with one another. For instance, the correlation between `fear_raw` and `tribal_dominance_raw` is *r* = 0.99, and between `enmity_raw` and `envy_raw` is *r* = 0.97. This indicates a powerful rhetorical syndrome where appeals to group-based dominance, fear of outsiders, grievance, and hostility are deployed in unison.
2.  **The Cohesive Cluster:** `individual_dignity_raw`, `hope_raw`, `amity_raw`, and `cohesive_goals_raw` are all positively correlated with one another. For example, `hope_raw` correlates with `cohesive_goals_raw` at *r* = 0.89 and with `amity_raw` at *r* = 0.89. This suggests a pro-social strategy built on appeals to universal dignity, optimism, friendship, and shared constructive goals.

These two clusters are, as expected, strongly negatively correlated with each other. For example, `fear_raw` has a correlation of *r* = -0.98 with the `descriptive_cohesion_index`. This confirms that the composite cohesion metrics are accurately capturing the latent divide revealed by the raw score correlations.

**Table 4: Abridged Pearson Correlation Matrix for Key CFF Dimensions (N=4)**
| | tribal_dom_raw | indiv_dig_raw | fear_raw | hope_raw | enmity_raw | amity_raw | full_cohesion_idx |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **tribal_dom_raw** | 1.00 | -0.67 | **0.99** | -0.76 | **0.98** | -0.55 | **-0.95** |
| **indiv_dig_raw** | -0.67 | 1.00 | -0.63 | 0.54 | -0.53 | 0.71 | **0.73** |
| **fear_raw** | **0.99** | -0.63 | 1.00 | -0.83 | **0.97** | -0.61 | **-0.97** |
| **hope_raw** | -0.76 | 0.54 | -0.83 | 1.00 | -0.68 | **0.89** | **0.91** |
| **enmity_raw** | **0.98** | -0.53 | **0.97** | -0.68 | 1.00 | -0.39 | **-0.89** |
| **amity_raw** | -0.55 | 0.71 | -0.61 | **0.89** | -0.39 | 1.00 | **0.77** |
| **full_cohesion_idx**| **-0.95** | **0.73** | **-0.97** | **0.91** | **-0.89** | **0.77** | 1.00 |
*(Note: `tribal_dom_raw` is an alias for `tribal_dominance_raw`, etc. Correlations > |0.85| are bolded for emphasis.)*

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns reveal a political discourse that is not just polarized, but structurally organized into two mutually exclusive rhetorical systems. The near-perfect correlations within the "Fragmentative Cluster" (Fear, Enmity, Envy, Tribal Dominance) are the most significant finding. This suggests that, in this dataset, these are not independent rhetorical choices but components of a single, integrated "threat narrative." A speaker invoking one element almost certainly invokes them all. This has profound implications, suggesting that attempts to mitigate one aspect (e.g., Enmity) may fail unless the entire rhetorical structure is addressed. Unfortunately, without textual evidence, it is impossible to illustrate *how* this narrative is constructed.

Conversely, the "Cohesive Cluster" (Hope, Amity, Individual Dignity, Cohesive Goals) represents an equally integrated "opportunity narrative." The strong positive correlations here suggest a pro-social strategy that links optimism for the future with respect for individuals and a call for friendly, collaborative action.

The framework's construct validity is strongly supported by these findings. The `Full Cohesion Index` acts as a near-perfect summary of this divide, correlating positively with every cohesive dimension and negatively with every fragmentative one. This indicates the derived metric is not an arbitrary composite but a meaningful reflection of the underlying rhetorical structure. The unexpected finding is the *strength* and *consistency* of these patterns. Even in a diverse set of speeches, the rhetorical "packages" hold together with remarkable integrity.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CFF v10.1 demonstrates high effectiveness in two key areas:

1.  **Discriminatory Power:** The framework successfully discriminated between different types of political rhetoric. The `Full Cohesion Index` spread of 1.51 points (from -0.73 to +0.78) on a 2-point scale shows that the framework is highly sensitive to the differences between the documents. It did not produce a cluster of ambiguous, middle-of-the-road scores; instead, it clearly identified and quantified the extreme polarization present in the corpus.

2.  **Framework-Corpus Fit:** The CFF appears to be an excellent fit for analyzing this type of polarized political discourse. The strong correlations and clear clustering suggest that the framework's dimensions map well onto the actual rhetorical strategies being used by the speakers. The low `Strategic Contradiction Index` scores further indicate that the framework's oppositional design is well-suited to a context where speakers tend to adopt one consistent stance rather than a mixed, contradictory one.

## 6. Discussion

### Theoretical Implications
The findings, while preliminary, have significant theoretical implications. The identification of tightly-bound "rhetorical clusters" suggests that political communication may operate via pre-packaged, internally coherent narratives. The "Fragmentative Cluster" can be theorized as a linguistic operationalization of an **ingroup-outgroup threat response**, where appeals to tribal identity are reinforced by emotions of fear and grievance (envy) and directed at a hostile "other" (enmity). The "Cohesive Cluster" may represent a **superordinate identity strategy**, where appeals to universal human dignity are coupled with pro-social emotions (hope, amity) to foster cooperation toward shared goals. The fact that these two clusters appear mutually exclusive in this data suggests a deep structural logic to political polarization.

### Comparative Analysis and Archetypal Patterns
The analysis reveals clear rhetorical archetypes.
*   **The Unifying Concession (John McCain):** This archetype is defined by the near-total absence of fragmentative rhetoric and the highest scores on all cohesive dimensions (Hope, Amity, Compersion, Individual Dignity). Its `Full Cohesion Index` of +0.78 makes it the model of cohesive discourse in this corpus.
*   **The Nativist Attack (Steve King):** This archetype represents the opposite pole. It scores highest on Tribal Dominance, Fear, and Enmity, and near-zero on all cohesive dimensions. Its `Full Cohesion Index` of -0.73 defines it as a purely fragmentative text.
*   **Populist Grievance (Bernie Sanders & Alexandria Ocasio-Cortez):** Interestingly, these two speakers, while ideologically distinct from King, produce scores that are structurally similar in their fragmentative nature, though less extreme. They score high on Envy, Enmity, and Tribal Dominance, but also mix in some appeals to Hope or Amity, resulting in moderately negative cohesion scores (-0.30 and -0.19, respectively). This suggests a populist rhetorical structure that identifies an "elite" out-group (fuelling Enmity and Envy) while simultaneously trying to build a "people's" in-group.

### Broader Significance
If these patterns hold in a larger corpus, they would suggest that political discourse is becoming more strategically "packaged." The low contradiction scores imply that speakers are becoming more disciplined in their messaging, avoiding appeals that might dilute their core narrative. This could lead to more effective mobilization of a base but also deepen societal divides by making cross-cutting appeals—which might bridge divides—rhetorically obsolete.

### Limitations and Future Directions
The limitations of this study dictate the path for future research.
1.  **Corpus Expansion:** The most urgent need is to replicate this analysis on a large, diverse corpus of political texts to see if these tight rhetorical clusters and archetypes are generalizable or an artifact of this small sample.
2.  **Qualitative Integration:** Future work must integrate textual evidence. A key research question would be: *What specific phrases, metaphors, and arguments correspond to high scores on dimensions like Envy or Compersion?* This qualitative grounding is essential for validating and enriching the quantitative findings.
3.  **Temporal Analysis:** A longitudinal corpus could be used to track the evolution of these rhetorical clusters over time. Are they a recent phenomenon? Do they intensify during election cycles? Answering these questions would provide invaluable insight into the dynamics of political polarization.

## 7. Conclusion

This exploratory study successfully demonstrated the application of the Cohesive Flourishing Framework v10.1 to a small set of political texts. The analysis yielded a clear and compelling, albeit preliminary, picture of a deeply polarized discourse organized around two opposing and internally consistent meta-strategies: a fragmentative "threat narrative" and a cohesive "opportunity narrative." The framework's metrics proved highly effective at discriminating between these strategies and quantifying their intensity, with the `Full Cohesion Index` and `Strategic Contradiction Index` offering powerful summary insights.

The strong negative correlations between the CFF's oppositional dimensions provide initial support for its construct validity. However, the conclusions of this report must be heavily qualified. The extremely small sample size (N=4) and the complete lack of supporting textual evidence mean that these findings should be treated as a set of testable hypotheses, not as established facts. The study serves as a successful proof-of-concept for the CFF's analytical potential, highlighting the urgent need for follow-up research that is broader in scale and deeper in qualitative integration.

## 8. Evidence Citations

In this automated analysis, the process for retrieving specific textual evidence to support the statistical findings did not yield any results. Therefore, it is not possible to provide direct quotes from the source documents to illustrate and validate the quantitative scores. This absence of qualitative data is a significant limitation of the present report. All interpretations of the dimensional scores are based on the CFF's theoretical definitions rather than on an analysis of the specific language used in the texts.