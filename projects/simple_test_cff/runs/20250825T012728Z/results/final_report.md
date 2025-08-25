# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: b71e3ca3dff1dee730fad860da502e448fc7e8eeb9285ce52d3856c5d21bcb16  
**Date**: 2025-08-24  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Political Speeches (4 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of a small corpus of four political texts using the Cohesive Flourishing Framework (CFF) v10.1. The primary objective of this exploratory study was to assess the framework's utility in quantifying rhetorical strategies related to social cohesion and to identify preliminary patterns within the discourse. Due to the pilot nature of this analysis (N=4), all findings should be considered indicative and serve as a basis for future, larger-scale research rather than generalizable conclusions.

The analysis reveals a corpus characterized by extreme rhetorical polarization. The central finding is the identification of two distinct and opposing meta-strategies. The first, a "fragmentative" strategy, is characterized by a statistically powerful co-occurrence of appeals to **Tribal Dominance**, **Fear**, **Envy**, and **Enmity**. The second, a "cohesive" strategy, links rhetoric emphasizing **Individual Dignity**, **Hope**, **Amity**, and **Cohesive Goals**. The framework's core oppositional design appears robust in this sample, with strong negative correlations observed between antithetical dimensions (e.g., Hope vs. Fear, r = -0.83), suggesting strong construct validity. The derived `Full Cohesion Index` effectively discriminated between texts, ranging from highly cohesive (+0.78) to highly fragmentative (-0.73), underscoring the deep divisions in the analyzed discourse.

Despite the intense polarization, the documents themselves were found to be rhetorically consistent. The `Strategic Contradiction Index`, which measures the use of mixed or contradictory messaging, remained low across all texts (M = 0.047). This suggests that speakers, regardless of their position on the cohesion spectrum, employed internally coherent rhetorical strategies. While these quantitative patterns are stark, their full meaning is constrained by the absence of qualitative textual evidence for triangulation. This study successfully demonstrates the CFF's potential for mapping complex rhetorical structures but highlights the critical need for mixed-methods approaches to validate and enrich such computational findings.

## 2. Opening Framework: Key Insights

This analysis yielded several key insights into the rhetorical structure of the analyzed corpus and the performance of the Cohesive Flourishing Framework.

*   **Strong Evidence for Oppositional Construct Validity:** The framework's design, which measures opposing concepts on independent scales, is strongly supported by the data. Antithetical dimensions exhibited powerful negative correlations, such as **Compersion** (joy in others' success) and **Tribal Dominance** (r = -0.99), and **Hope** and **Fear** (r = -0.83). This indicates the framework is effectively capturing the intended conceptual tensions in discourse.
*   **Identification of a Dominant "Fragmentative Meta-Strategy":** The analysis uncovered a highly coherent rhetorical pattern linking fragmentative concepts. Appeals to **Tribal Dominance** were almost perfectly correlated with appeals to **Fear** (r = +0.99), **Envy** (r = +0.92), and **Enmity** (r = +0.98). This suggests a unified rhetorical strategy that simultaneously activates group-based identity, threat perception, resentment, and hostility toward an out-group.
*   **A Cohesive Counter-Strategy Emerges:** A corresponding, though slightly less tightly bound, "cohesive meta-strategy" was also identified. Rhetoric centered on **Individual Dignity** was positively correlated with **Hope** (r = +0.54), **Amity** (r = +0.71), and **Cohesive Goals** (r = +0.74). This pattern represents a rhetorical approach grounded in universal dignity, positive future outlooks, and pro-social relationships.
*   **The Corpus is Defined by Extreme Polarization, Not Ambiguity:** The `Full Cohesion Index` revealed a bimodal distribution, with documents clustering at either the highly cohesive or highly fragmentative end of the spectrum. The mean score was close to neutral (-0.11), but this was a product of a very high standard deviation (0.64), not a tendency toward moderate discourse. This points to a corpus where speakers adopt starkly different, rather than blended, rhetorical postures.
*   **Rhetoric is Polarized but Internally Consistent:** The `Strategic Contradiction Index` remained consistently low across all documents (M = 0.047, SD = 0.03). This finding is significant when paired with the high polarization. It suggests that the analyzed speakers are not employing sophisticated, contradictory appeals (e.g., mixing high hope with high fear) but are instead delivering clear, internally consistent, and highly polarized messages.
*   **Outlier Analysis Reveals Rhetorical Archetypes:** The quantitative data clearly identified archetypal documents. John McCain's 2008 concession speech emerged as the exemplar of cohesive rhetoric (`Full Cohesion Index` = +0.78), while Steve King's 2017 floor speech exemplified the fragmentative archetype (`Full Cohesion Index` = -0.73). These extreme cases serve as valuable anchors for understanding the practical meaning of the CFF's metrics.

## 4. Methodology

### 4.1 Framework Description and Analytical Approach

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze political and social discourse. As described in its specification, the CFF moves beyond simple sentiment analysis by measuring a series of paired oppositional dimensions. For example, instead of placing a text on a single continuum from "Hope" to "Fear," it assigns independent scores for both `hope_raw` and `fear_raw`, as well as their respective salience. This approach is designed to capture sophisticated rhetoric where competing appeals may be used simultaneously.

The framework is structured around five core conceptual pairs:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion
4.  **Relations:** Enmity vs. Amity
5.  **Goals:** Fragmentative Goals vs. Cohesive Goals

The analysis calculates several derived metrics, including **Tension Indices** (measuring strategic contradiction), a **Strategic Contradiction Index** (the mean of all tensions), and three nested **Cohesion Indices** (`Descriptive`, `Motivational`, `Full`) that provide an overall measure of a document's rhetorical posture on a scale from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### 4.2 Data and Corpus

The dataset for this analysis consists of quantitative scores for a corpus of four distinct political texts:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

For each document, the data includes raw scores (0-1 scale) and salience scores (0-1 scale) for the ten primary dimensions listed above. The analysis was performed on the complete statistical results generated by a standardized analysis agent, which included descriptive statistics, derived metrics, a full correlation matrix, and outlier identification.

### 4.3 Statistical Methods and Constraints

The analysis is primarily descriptive and correlational, which is appropriate for the exploratory nature of this study and the very small sample size (N=4). The primary statistical methods include:
*   **Descriptive Statistics:** Calculation of mean, standard deviation (SD), minimum, and maximum for all raw scores and derived indices to understand central tendency and variance.
*   **Pearson Correlation:** A correlation matrix was computed to examine the relationships between all raw scores and derived metrics. This is the core method for assessing the CFF's construct validity and identifying rhetorical meta-strategies. Correlation coefficients (r) are interpreted using standard conventions for effect size (small: |r| > 0.1, medium: |r| > 0.3, large: |r| > 0.5).
*   **Outlier Identification:** Documents with the highest and lowest scores on key indices (`Full Cohesion Index`, `Strategic Contradiction Index`) were identified to provide concrete examples for qualitative interpretation.

### 4.4 Limitations

This study is subject to several significant limitations that must be considered when interpreting the results:

1.  **Extremely Small Sample Size:** With a corpus of only four documents (N=4), the statistical findings are not generalizable to any broader population of political discourse. The results are illustrative of patterns within this specific micro-corpus only. Inferential statistics (e.g., p-values) are not meaningful and have been omitted.
2.  **Lack of Qualitative Evidence:** The analysis was conducted solely on the quantitative output. No textual evidence (i.e., quotes from the documents) was available for triangulation. This is a critical omission, as it prevents a deeper, context-rich interpretation of the statistical patterns. For instance, while we can observe a strong correlation between `fear_raw` and `enmity_raw`, we cannot examine the specific language used to construct this association. All interpretations are therefore based on the operational definitions of the framework's dimensions, not on a direct analysis of the discourse itself.
3.  **Potential for Spurious Correlations:** With N=4, any correlation is highly sensitive to the specific characteristics of the individual documents. While the observed patterns are remarkably strong and theoretically coherent, they must be viewed with extreme caution and require validation with a much larger and more diverse corpus.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the ten primary raw scores reveals a corpus characterized by high variance and polarization. The scores are not clustered around a central mean but tend toward the extremes of the 0-1 scale, as indicated by the large standard deviations relative to the means.

**Table 1: Descriptive Statistics of Primary Raw Scores (N=4)**

| Dimension                   | Mean  | Std. Dev. | Min   | Max   | Interpretation of Variance                               |
| --------------------------- | ----- | --------- | ----- | ----- | -------------------------------------------------------- |
| **Fragmentative Dimensions**|       |           |       |       |                                                          |
| `tribal_dominance_raw`      | 0.575 | 0.386     | 0.0   | 0.8   | High variance; documents are either low or high.         |
| `fear_raw`                  | 0.675 | 0.320     | 0.2   | 0.9   | High scores are common, but with significant spread.     |
| `envy_raw`                  | 0.600 | 0.424     | 0.0   | 0.9   | High variance; polarized between presence and absence.   |
| `enmity_raw`                | 0.650 | 0.436     | 0.0   | 0.9   | High variance; polarized between presence and absence.   |
| `fragmentative_goals_raw`   | 0.575 | 0.386     | 0.0   | 0.8   | High variance; documents are either low or high.         |
| **Cohesive Dimensions**     |       |           |       |       |                                                          |
| `individual_dignity_raw`    | 0.450 | 0.404     | 0.1   | 0.8   | High variance; polarized between presence and absence.   |
| `hope_raw`                  | 0.475 | 0.377     | 0.0   | 0.9   | High variance; polarized between presence and absence.   |
| `compersion_raw`            | 0.225 | 0.450     | 0.0   | 0.9   | Very high variance; mostly absent but high in one case.  |
| `amity_raw`                 | 0.600 | 0.408     | 0.0   | 0.9   | High variance; polarized between presence and absence.   |
| `cohesive_goals_raw`        | 0.650 | 0.311     | 0.2   | 0.9   | High scores are common, but with significant spread.     |

The key takeaway from these statistics is the lack of a "typical" document. For nearly every dimension, the standard deviation is large, often approaching or exceeding the mean. This indicates that the documents in the corpus adopt fundamentally different rhetorical stances rather than varying slightly around a common baseline. For example, the scores for `envy_raw` and `compersion_raw` show that documents tend to use one or the other, but not both, leading to high variance. This sets the stage for the strong correlations and polarized index scores observed later.

### 5.2 Advanced Metric Analysis

The derived metrics, which synthesize the primary scores into higher-level indices, confirm the narrative of a polarized but internally consistent corpus.

**Table 2: Descriptive Statistics of Derived Metrics (N=4)**

| Derived Metric                    | Mean    | Std. Dev. | Min     | Max    | Interpretation                                                                                             |
| --------------------------------- | ------- | --------- | ------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| `full_cohesion_index`             | -0.106  | 0.638     | -0.727  | 0.784  | Extremely high variance. The near-zero mean masks a deep split between cohesive and fragmentative texts. |
| `strategic_contradiction_index`   | 0.047   | 0.030     | 0.024   | 0.090  | Consistently low scores across all documents, indicating rhetorically coherent, non-contradictory messaging. |
| `identity_tension`                | 0.058   | 0.039     | 0.000   | 0.080  | Low.                                                                                                       |
| `emotional_tension`               | 0.070   | 0.082     | 0.000   | 0.160  | Low, with one document showing moderate tension.                                                           |
| `relational_tension`              | 0.037   | 0.043     | 0.000   | 0.080  | Low.                                                                                                       |
| `goal_tension`                    | 0.070   | 0.081     | 0.000   | 0.140  | Low.                                                                                                       |

The `Full Cohesion Index` is the most telling metric. Its mean of -0.106 suggests a slight fragmentative tilt, but the massive standard deviation of 0.638 reveals the true story: the corpus is not neutral, but deeply divided. The outlier analysis confirms this:
*   **Most Cohesive Document:** `john_mccain_2008_concession.txt` (`Full Cohesion Index` = 0.784)
*   **Most Fragmentative Document:** `steve_king_2017_house_floor.txt` (`Full Cohesion Index` = -0.727)

Conversely, the `Strategic Contradiction Index` is uniformly low. The highest score recorded was only 0.09 (for the AOC text), far below the theoretical maximum. This indicates that while the speakers chose radically different paths (cohesive vs. fragmentative), they did not mix their messages. They presented rhetorically "pure" arguments, a finding that contradicts theories of sophisticated rhetoric that might predict high-hope and high-fear appeals within the same text to motivate different audiences. The absence of such contradiction in this sample is a significant finding.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix provides the strongest evidence for the existence of coherent, opposing rhetorical meta-strategies. The analysis reveals powerful relationships that validate the framework's structure and uncover how different rhetorical appeals are bundled together in practice.

**Table 3: Selected Pearson Correlations (r) for Raw Scores and Key Indices (N=4)**

| Variable 1                  | Variable 2                  | Correlation (r) | Strength/Interpretation                                                                                             |
| --------------------------- | --------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Oppositional Validity**   |                             |                 |                                                                                                                     |
| `fear_raw`                  | `hope_raw`                  | -0.834          | **Large Negative.** Strong evidence that appeals to fear and hope are used oppositionally in this corpus.             |
| `tribal_dominance_raw`      | `individual_dignity_raw`    | -0.673          | **Large Negative.** Confirms the conceptual opposition between group-based dominance and universal dignity.           |
| `enmity_raw`                | `amity_raw`                 | -0.393          | **Medium Negative.** A weaker but still present opposition between appeals to friendship and hostility.               |
| `compersion_raw`            | `envy_raw`                  | -0.943          | **Large Negative.** Extremely strong opposition; texts that evoke envy do not evoke compersion, and vice-versa.     |
| **Fragmentative Cluster**   |                             |                 |                                                                                                                     |
| `fear_raw`                  | `tribal_dominance_raw`      | +0.991          | **Large Positive.** Near-perfect correlation. An appeal to fear is almost invariably an appeal to tribalism.         |
| `fear_raw`                  | `enmity_raw`                | +0.967          | **Large Positive.** Fear-based rhetoric is tightly coupled with defining an enemy.                                  |
| `fear_raw`                  | `envy_raw`                  | +0.883          | **Large Positive.** Fear is strongly associated with rhetoric of resentment and envy.                               |
| **Cohesive Cluster**        |                             |                 |                                                                                                                     |
| `hope_raw`                  | `amity_raw`                 | +0.887          | **Large Positive.** Hopeful rhetoric is strongly linked to pro-social, friendly relationship-building.               |
| `hope_raw`                  | `cohesive_goals_raw`        | +0.895          | **Large Positive.** Hope is tied to the articulation of unifying, shared goals.                                     |
| `individual_dignity_raw`    | `cohesive_goals_raw`        | +0.743          | **Large Positive.** Rhetoric of universal dignity is linked to shared goals.                                        |
| **Index Validation**        |                             |                 |                                                                                                                     |
| `full_cohesion_index`       | `fear_raw`                  | -0.973          | **Large Negative.** The index is an excellent summary measure, strongly reflecting the presence of fragmentative themes. |
| `full_cohesion_index`       | `hope_raw`                  | +0.908          | **Large Positive.** The index is equally effective at capturing the presence of cohesive themes.                      |

*Note: The correlation for `success_tension` was `NaN` (Not a Number) because there was no variance in the metric; it was zero for all four documents, making correlation mathematically impossible.*

These correlations paint a vivid picture. The fragmentative dimensions (`tribal_dominance`, `fear`, `envy`, `enmity`) are not just loosely related; they form a tightly integrated rhetorical package. A speaker deploying one is extremely likely to deploy the others. The same is true for the cohesive dimensions (`individual_dignity`, `hope`, `amity`, `cohesive_goals`), which also cluster together, albeit with slightly less intensity. This suggests that speakers in this corpus are drawing from one of two distinct, pre-packaged rhetorical playbooks.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns observed allow for the identification of two preliminary rhetorical archetypes.

1.  **The Fragmentative Meta-Strategy:** This strategy, exemplified by the Steve King text, appears to function by constructing a threatened in-group identity. The near-perfect correlation between `tribal_dominance_raw` and `fear_raw` (r = +0.99) is the cornerstone of this strategy. The argument structure seems to be: our group (`tribal_dominance`) is under threat (`fear`), which generates hostility toward an out-group (`enmity`) and resentment over their perceived unfair advantages (`envy`). The inclusion of `fragmentative_goals_raw` (which correlates at r = +1.00 with `tribal_dominance_raw`) indicates this rhetoric is aimed at zero-sum outcomes. The statistical coherence of this cluster is the most powerful finding of this analysis. Without access to the text, one can only speculate, but this pattern is highly consistent with classic populist-nationalist rhetoric.

2.  **The Cohesive Meta-Strategy:** This strategy, exemplified by the John McCain text, operates on an opposing logic. It centers on positive-sum, universalist appeals. The strong link between `hope_raw` and `amity_raw` (r = +0.89) suggests a focus on a positive future achieved through pro-social bonds. The connection to `individual_dignity_raw` (r = +0.54 with `hope_raw`) and `cohesive_goals_raw` (r = +0.89 with `hope_raw`) implies a foundation of universal human value directed toward shared, unifying objectives. This pattern aligns with civic rhetoric that seeks to bridge divides and build broad coalitions.

The starkness of these two opposing patterns, combined with the low `Strategic Contradiction Index`, suggests that the analyzed discourse operates on a single, dominant axis of conflict: **in-group particularism vs. universalist humanism**. The framework successfully maps the rhetorical components of this conflict.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the Cohesive Flourishing Framework (CFF) demonstrates considerable promise, particularly in its discriminatory power and construct validity.

*   **Discriminatory Power:** The framework, especially through its `Full Cohesion Index`, was highly effective at differentiating between texts. The resulting scores spanned a wide range of the theoretical scale (-0.73 to +0.78), indicating that the CFF is sensitive enough to capture vast differences in rhetorical posture. It did not produce a cluster of moderate, undifferentiated scores.
*   **Construct Validity:** The strong negative correlations between opposing dimensions (e.g., `compersion_raw` vs. `envy_raw`, r = -0.94) provide compelling, albeit preliminary, evidence for the framework's construct validity. The dimensions behave as theoretically predicted, measuring distinct and antithetical concepts.
*   **Framework-Corpus Fit:** The CFF appears to be an excellent fit for analyzing polarized political discourse. Its structure is well-suited to mapping the components of cohesive and fragmentative rhetorical strategies. The results were not noisy or random but revealed clear, interpretable, and theoretically meaningful patterns.

The primary weakness revealed is not in the framework itself but in its application in isolation. The quantitative data raises profound questions (e.g., *How* is fear linked to tribalism in the text? What specific metaphors are used?) that it cannot answer. This underscores that the CFF is most powerful when used as the first step in a mixed-methods analysis, guiding subsequent qualitative inquiry.

## 6. Discussion

### 6.1 Theoretical Implications

The findings from this small-scale study, while not generalizable, carry several important theoretical implications for the study of political communication. The identification of two coherent, opposing meta-strategies suggests that political rhetoric may be more constrained and path-dependent than often assumed. Rather than speakers picking and choosing from a wide menu of rhetorical appeals, they may be drawn to one of two dominant, pre-packaged "logics"—one of fragmentation and one of cohesion.

The "fragmentative cluster" (`Fear`, `Enmity`, `Tribalism`, `Envy`) can be theorized as a rhetorical manifestation of social identity theory, where in-group favoritism is amplified by perceived out-group threat. The statistical tightness of this cluster suggests these are not independent appeals but facets of a single, underlying worldview. The "cohesive cluster" (`Hope`, `Amity`, `Dignity`, `Shared Goals`) can be seen as an appeal to a superordinate identity (e.g., citizen, human) that transcends factional divides, a classic tenet of deliberative democratic theory.

Furthermore, the consistently low `Strategic Contradiction Index` challenges the notion that effective political rhetoric is necessarily complex or ambiguous. In this polarized sample, clarity and consistency—albeit in opposing directions—were the norms. This may suggest that in highly contentious environments, the strategic value of a clear, unambiguous message outweighs the potential benefits of nuanced or contradictory appeals that might engage a broader but more divided audience.

### 6.2 Comparative Analysis and Archetypal Patterns

The quantitative results allow for the sketching of preliminary rhetorical archetypes.

*   **The "Cohesive Unifier" (McCain 2008):** This archetype is defined by extremely high scores on cohesive dimensions (`Hope`, `Amity`, `Compersion`, `Individual Dignity`) and near-zero scores on all fragmentative dimensions. The resulting `Full Cohesion Index` is strongly positive (+0.78). This rhetorical style is likely found in moments of civic ritual (like concession speeches) that demand a focus on national unity over partisan victory.

*   **The "Fragmentative Agitator" (King 2017):** This archetype represents the mirror image of the Unifier. It is defined by high scores on `Tribal Dominance`, `Fear`, `Enmity`, and `Envy`, with negligible cohesive rhetoric. The `Full Cohesion Index` is strongly negative (-0.73). This style is likely deployed to mobilize a specific base by emphasizing threat, grievance, and group identity.

*   **The "Populist Challenger" (Sanders/AOC 2025):** The two documents `bernie_sanders_2025_fighting_oligarchy.txt` and `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` represent a more complex archetype. Their `Full Cohesion Index` scores are negative (-0.30 and -0.19, respectively), indicating a predominantly fragmentative leaning. This is driven by high scores in `Tribal Dominance`, `Envy`, and `Enmity`, likely aimed at an "oligarchic" out-group. However, they differ from the pure "Agitator" archetype by also scoring moderately on some cohesive dimensions like `Cohesive Goals` and `Amity`. This suggests a rhetoric that uses fragmentative tactics (defining an enemy) in the service of what is framed as a cohesive, universalist goal (e.g., the good of the many). This complexity makes them particularly interesting subjects for future qualitative analysis.

### 6.3 Limitations and Future Directions

The limitations of this study define its future directions. The most pressing need is to **scale up the analysis**. A larger corpus of hundreds or thousands of documents is required to verify if the powerful correlations and clustering patterns observed here are robust or artifacts of the small sample. A diverse corpus, including different speakers, genres, and time periods, would allow for testing the generalizability of the identified archetypes.

The second, equally critical, direction is **qualitative integration**. A mixed-methods approach is essential. The quantitative findings should be used to purposefully sample texts for in-depth qualitative analysis. For example, a researcher could select the documents with the highest `Emotional Tension` scores to investigate precisely how speakers combine hope and fear. The absence of textual evidence in the current report is its most significant shortcoming; future work must remedy this by linking statistical patterns directly to the language that produces them.

Finally, future research could explore the **predictive power** of the CFF's metrics. Do documents with highly fragmentative scores correlate with real-world outcomes like increased polarization, social unrest, or inter-group hostility? Answering such questions would move the framework from a descriptive tool to a predictive one, with significant implications for understanding the societal impact of discourse.

## 7. Conclusion

This exploratory computational analysis, despite its significant limitations, successfully demonstrates the potential of the Cohesive Flourishing Framework (CFF) to dissect and quantify complex rhetorical strategies in political discourse. The study revealed a starkly polarized micro-corpus, identifying two coherent and opposing meta-strategies—a "fragmentative" one built on tribalism and threat, and a "cohesive" one grounded in universal dignity and hope.

The framework's core design proved robust, with strong evidence for its construct validity emerging from the oppositional correlations between antithetical dimensions. The derived indices, particularly the `Full Cohesion Index` and the `Strategic Contradiction Index`, were effective in capturing the two main features of the corpus: extreme polarization between documents and high internal consistency within documents.

Ultimately, this report serves as a proof of concept and a call for further research. The clear, powerful patterns discovered in this small dataset generate compelling hypotheses about the structure of political rhetoric that now require testing on a larger scale. The most crucial conclusion is methodological: while computational frameworks like the CFF can provide an invaluable "macroscope" to map the contours of discourse, their insights are only fully realized when integrated with the context and nuance that only qualitative analysis can provide.

## 8. Evidence Citations

No textual evidence was available for this analysis. The statistical results were generated by an automated agent without providing the underlying textual data for qualitative validation. This absence is a critical limitation of the present report. All interpretations of the statistical findings are based on the operational definitions of the CFF dimensions. A complete analysis would require citing specific passages from the source documents to illustrate and substantiate each claim. For example, a claim about the high `Fear` score in a document should be supported by a direct quote expressing threat or danger from that document. The lack of such evidence means the link between the quantitative scores and the actual discourse remains a "black box" in this study.