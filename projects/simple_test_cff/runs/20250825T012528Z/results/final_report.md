# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: d84da983e65470855d4c08debc27876892e45875a1ff342017d6a90e18fca9cf  
**Date**: 2025-08-24  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Political Speeches (4 documents)  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of a small corpus (N=4) of political speeches using the Cohesive Flourishing Framework (CFF) v10.1. The analysis aimed to explore the framework's utility in identifying and quantifying rhetorical patterns related to social cohesion. Despite the significant limitation of the small sample size, which precludes inferential claims, the descriptive and correlational findings offer valuable initial insights into both the corpus's rhetorical strategies and the framework's internal structure.

The analysis reveals a highly structured, bipolar rhetorical landscape within the corpus. Dimensions designated by the CFF as "cohesive" (e.g., Hope, Amity, Individual Dignity) are strongly and negatively correlated with their "fragmentative" counterparts (e.g., Fear, Enmity, Tribal Dominance). This oppositional structure provides preliminary support for the framework's construct validity. Two dominant and opposing rhetorical meta-strategies emerged: a "Fragmentative Cluster" linking appeals to Tribal Dominance, Fear, and Enmity (r > 0.96), and a "Cohesive Cluster" connecting appeals to Individual Dignity, Hope, and Amity. The derived `Full Cohesion Index` proved effective at discriminating between documents, identifying one speech as highly cohesive (Index = 0.78) and others as highly fragmentative (Index = -0.73).

Overall, this pilot study suggests that the CFF is a promising tool for moving beyond simple sentiment analysis to map complex rhetorical strategies. The framework successfully captured consistent, opposing linguistic patterns and quantified them in a way that differentiates texts along a cohesion-fragmentation spectrum. However, all findings must be considered exploratory. Future research with a larger, more diverse corpus is essential to validate these patterns, substantiate the framework's effectiveness, and enable more generalizable conclusions about political discourse.

## 2. Opening Framework: Key Insights

This preliminary analysis yielded several key insights into the rhetorical composition of the corpus and the performance of the Cohesive Flourishing Framework.

*   **Strong Bipolar Structure Suggests Construct Validity:** The analysis revealed strong, consistent negative correlations between opposing CFF dimensions. For instance, `Fear` and `Hope` are strongly negatively correlated (r = -0.834), as are `Envy` and `Compersion` (r = -0.943). This indicates that, within this corpus, speakers who use fragmentative language tend to avoid cohesive language, providing initial, descriptive support for the framework's design.
*   **A "Fragmentative Rhetorical Cluster" Was Identified:** The dimensions of `Tribal Dominance`, `Fear`, `Enmity`, and `Fragmentative Goals` are almost perfectly inter-correlated (r > 0.98 in most cases). This suggests the presence of a consistent and potent meta-strategy that bundles these divisive appeals together.
*   **A "Cohesive Rhetorical Cluster" Emerged as the Opposite Pole:** A corresponding, though slightly less tightly bound, cluster of cohesive dimensions was also identified. `Individual Dignity`, `Hope`, `Amity`, and `Cohesive Goals` were all positively correlated with one another, representing a distinct rhetorical alternative to the fragmentative strategy.
*   **The `Full Cohesion Index` Demonstrates High Discriminatory Power:** The primary derived metric, the `Full Cohesion Index`, showed a wide range across the four documents, from a highly cohesive score of +0.78 (`john_mccain_2008_concession.txt`) to a highly fragmentative score of -0.73 (`steve_king_2017_house_floor.txt`). This suggests the index is effective at capturing and quantifying the overall rhetorical leaning of a text.
*   **Rhetoric in the Corpus is Consistent, Not Contradictory:** The `Strategic Contradiction Index`, designed to measure the use of mixed or contradictory messaging, was consistently low across all documents (Mean = 0.05). This indicates that the analyzed speeches employ clear, internally consistent rhetorical strategies, rather than attempting to balance opposing appeals like hope and fear simultaneously.
*   **Small Sample Size Necessitates Caution:** It is critical to emphasize that with a sample size of N=4, these findings are purely descriptive and exploratory. They demonstrate the potential of the CFF but cannot be generalized. The patterns observed require validation with a substantially larger dataset.

## 3. Literature Review and Theoretical Framework

The analysis of political and social discourse has increasingly moved from simple positive/negative sentiment analysis towards more nuanced, multidimensional models. Traditional methods often fail to capture the complexity of rhetorical strategy, forcing texts into binary classifications (e.g., "hopeful" or "fearful") that obscure the sophisticated interplay of communicative appeals. This limitation is particularly acute in political science and sociology, where language is understood not merely as an expression of emotion, but as a strategic tool for building coalitions, defining identity, and mobilizing action.

The Cohesive Flourishing Framework (CFF) v10.1, as described in its *Raison d'être*, positions itself as a direct response to this methodological gap. It is grounded in the theoretical assumption that social cohesion is not a monolithic concept but is built or eroded through distinct, and often competing, linguistic appeals. By independently scoring opposing dimensions—such as `Hope` vs. `Fear`, or `Individual Dignity` vs. `Tribal Dominance`—the CFF aims to preserve this crucial rhetorical information. This approach allows for the analysis of not only the dominant message but also the "strategic contradictions" within a text, where a speaker might, for example, pair a message of hope for an in-group with a message of fear regarding an out-group.

This study, therefore, uses the CFF not just as a measurement tool but as an analytical lens. The core theoretical proposition being tested is whether political discourse, when viewed through the CFF, exhibits structured, identifiable patterns of co-occurring rhetorical appeals. The discovery of strong correlations and distinct dimensional clusters would lend support to the theory that political rhetoric is often deployed in predictable "packages" or meta-strategies, which the CFF is designed to detect. This analysis serves as a preliminary, empirical exploration of these theoretical claims.

## 4. Methodology

### 4.1 Framework Description
This study employs the Cohesive Flourishing Framework (CFF) v10.1. The CFF is a multi-dimensional analytical tool designed to assess the impact of discourse on social cohesion. It operates by assigning scores across ten primary "raw" dimensions, organized into five oppositional pairs: Identity (`Individual Dignity` vs. `Tribal Dominance`), Emotion (`Hope` vs. `Fear`), Success (`Compersion` vs. `Envy`), Relations (`Amity` vs. `Enmity`), and Goals (`Cohesive Goals` vs. `Fragmentative Goals`). For each dimension, a `salience` score is also assigned, representing its prominence within the text.

From these base scores, the CFF calculates several derived metrics. **Tension Indices** quantify the degree of strategic contradiction within each oppositional pair. The **Strategic Contradiction Index** provides an overall measure of a text's rhetorical consistency. Finally, three **Cohesion Indices** (`Descriptive`, `Motivational`, `Full`) provide a holistic, salience-weighted measure of a document's orientation towards social cohesion or fragmentation, with scores ranging from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### 4.2 Corpus Description
The analysis was conducted on a small pilot corpus (N=4) of American political speeches. The documents, identified from the statistical output, include:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

This corpus, while not representative, provides a set of diverse political viewpoints for this preliminary methodological exploration.

### 4.3 Statistical Methods
The analysis is primarily descriptive and correlational, appropriate for the exploratory nature of this pilot study. The following methods were used:
*   **Descriptive Statistics:** Means, standard deviations, and ranges were calculated for all raw scores and derived metrics to understand the central tendencies and variance within the corpus.
*   **Pearson Correlation:** A correlation matrix was computed to examine the relationships between all CFF raw dimensions and derived metrics. The Pearson correlation coefficient (r) is used here as a descriptive measure of the strength and direction of linear association between variables within this specific sample.
*   **Outlier Identification:** Documents with the highest and lowest scores on the `Full Cohesion Index` and `Strategic Contradiction Index` were identified to facilitate qualitative interpretation of extreme cases.

### 4.4 Analytical Constraints and Limitations
This study is subject to two major limitations that must be considered when interpreting the results:

1.  **Extremely Small Sample Size:** With a corpus of only four documents (N=4), the study is a pilot analysis. The results are not generalizable, and no inferential statistical claims (e.g., statistical significance, p-values) can be made. All findings should be interpreted as preliminary and indicative of potential patterns that require validation on a much larger dataset.
2.  **Absence of Qualitative Evidence:** The analysis was performed on pre-computed numerical scores, and no corresponding textual evidence was available for citation or qualitative triangulation. This prevents a deeper, context-rich interpretation of *how* these rhetorical scores manifest in the source texts. Consequently, this report is a purely quantitative analysis, and all interpretations are based solely on the provided statistical data.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics of CFF Dimensions

An initial examination of the descriptive statistics for the ten raw CFF dimensions provides a baseline understanding of the corpus's rhetorical content. On average, the fragmentative dimensions of `Fear` (M=0.68), `Envy` (M=0.60), and `Enmity` (M=0.65) were more prevalent than their cohesive counterparts `Hope` (M=0.48), `Compersion` (M=0.23), and `Amity` (M=0.60). This suggests a slight overall tilt towards fragmentative rhetoric in this small sample. The standard deviations are relatively large across most dimensions, indicating substantial variation between the four speeches.

**Table 1: Descriptive Statistics for CFF Raw and Salience Scores (N=4)**

| Dimension                      | Mean  | Std. Dev. | Min   | Max   |
| ------------------------------ | ----- | --------- | ----- | ----- |
| `tribal_dominance_raw`         | 0.575 | 0.386     | 0.0   | 0.8   |
| `tribal_dominance_salience`    | 0.675 | 0.386     | 0.1   | 0.9   |
| `individual_dignity_raw`       | 0.450 | 0.404     | 0.1   | 0.8   |
| `individual_dignity_salience`  | 0.450 | 0.412     | 0.1   | 0.9   |
| `fear_raw`                     | 0.675 | 0.320     | 0.2   | 0.9   |
| `fear_salience`                | 0.700 | 0.271     | 0.3   | 0.9   |
| `hope_raw`                     | 0.475 | 0.377     | 0.0   | 0.9   |
| `hope_salience`                | 0.525 | 0.411     | 0.0   | 0.9   |
| `envy_raw`                     | 0.600 | 0.424     | 0.0   | 0.9   |
| `envy_salience`                | 0.600 | 0.424     | 0.0   | 0.9   |
| `compersion_raw`               | 0.225 | 0.450     | 0.0   | 0.9   |
| `compersion_salience`          | 0.250 | 0.500     | 0.0   | 1.0   |
| `enmity_raw`                   | 0.650 | 0.436     | 0.0   | 0.9   |
| `enmity_salience`              | 0.675 | 0.386     | 0.1   | 0.9   |
| `amity_raw`                    | 0.600 | 0.408     | 0.0   | 0.9   |
| `amity_salience`               | 0.650 | 0.443     | 0.0   | 1.0   |
| `fragmentative_goals_raw`      | 0.575 | 0.386     | 0.0   | 0.8   |
| `fragmentative_goals_salience` | 0.575 | 0.403     | 0.0   | 0.9   |
| `cohesive_goals_raw`           | 0.650 | 0.311     | 0.2   | 0.9   |
| `cohesive_goals_salience`      | 0.675 | 0.320     | 0.2   | 0.9   |

### 5.2 Advanced Metric Analysis

Analysis of the derived CFF metrics reveals the overall rhetorical posture of the documents. The mean `Full Cohesion Index` for the corpus is slightly negative (M = -0.11), confirming the tendency towards fragmentation observed in the raw scores. However, the large standard deviation (SD = 0.64) and wide range (Min = -0.73, Max = 0.78) highlight the index's ability to differentiate sharply between the documents.

The `Strategic Contradiction Index` is notably low (M = 0.05, SD = 0.03), suggesting that the speeches in this corpus employ rhetorically consistent messaging. They tend to commit to either a cohesive or a fragmentative strategy, rather than mixing them. The `success_tension` metric was 0 for all documents, resulting in a standard deviation of 0. This indicates that in every speech, narratives of success were framed exclusively through either `Envy` or `Compersion`, never both, pointing to a highly polarized treatment of this theme.

**Table 2: Summary of Corpus-Wide Derived Metrics (N=4)**

| Metric                          | Mean    | Std. Dev. | Min     | Median  | Max     |
| ------------------------------- | ------- | --------- | ------- | ------- | ------- |
| `identity_tension`              | 0.058   | 0.039     | 0.000   | 0.075   | 0.080   |
| `emotional_tension`             | 0.070   | 0.082     | 0.000   | 0.060   | 0.160   |
| `success_tension`               | 0.000   | 0.000     | 0.000   | 0.000   | 0.000   |
| `relational_tension`            | 0.037   | 0.043     | 0.000   | 0.035   | 0.080   |
| `goal_tension`                  | 0.070   | 0.081     | 0.000   | 0.070   | 0.140   |
| `strategic_contradiction_index` | 0.047   | 0.030     | 0.024   | 0.037   | 0.090   |
| `descriptive_cohesion_index`    | -0.172  | 0.666     | -0.787  | -0.337  | 0.772   |
| `motivational_cohesion_index`   | -0.099  | 0.644     | -0.732  | -0.231  | 0.800   |
| `full_cohesion_index`           | -0.106  | 0.638     | -0.727  | -0.240  | 0.784   |

The outlier analysis confirms these findings. The document with the highest `Full Cohesion Index` is `john_mccain_2008_concession.txt` (+0.78), while the lowest is `steve_king_2017_house_floor.txt` (-0.73). Conversely, the document with the highest (though still low) `Strategic Contradiction Index` is `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` (0.09), suggesting a slightly more complex, though still largely consistent, rhetorical mix.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals a powerful and highly structured set of relationships between the CFF dimensions, providing the strongest evidence for the framework's internal logic and the presence of rhetorical meta-strategies in the corpus.

**Table 3: Pearson Correlation Matrix for CFF Raw Scores and Key Derived Metrics (N=4, rounded to 3 decimal places)**
*(Note: `success_tension` is excluded as its variance was zero, making correlation calculation impossible.)*

| Variable                        | tribal_dom | indiv_dig | fear_raw | hope_raw | envy_raw | compersion | enmity_raw | amity_raw | frag_goals | coh_goals | full_cohesion | strat_contra |
| ------------------------------- | ---------- | --------- | -------- | -------- | -------- | ---------- | ---------- | --------- | ---------- | --------- | ------------- | ------------ |
| **tribal_dominance_raw**        | **1.000**  | -0.673    | 0.991    | -0.760   | 0.915    | -0.993     | 0.980      | -0.550    | **1.000**  | -0.597    | **-0.953**    | 0.407        |
| **individual_dignity_raw**      | -0.673     | **1.000** | -0.631   | 0.535    | -0.408   | 0.577      | -0.530     | 0.707     | -0.673     | 0.743     | **0.734**     | 0.387        |
| **fear_raw**                    | 0.991      | -0.631    | **1.000**| -0.834   | 0.883    | -0.989     | 0.967      | -0.612    | 0.991      | -0.653    | **-0.973**    | 0.471        |
| **hope_raw**                    | -0.760     | 0.535     | -0.834   | **1.000**| -0.500   | 0.751      | -0.679     | 0.887     | -0.760     | 0.895     | **0.908**     | -0.405       |
| **envy_raw**                    | 0.915      | -0.408    | 0.883    | -0.500   | **1.000**| -0.943     | 0.973      | -0.173    | 0.915      | -0.227    | **-0.757**    | 0.568        |
| **compersion_raw**              | -0.993     | 0.577     | -0.989   | 0.751    | -0.943   | **1.000**  | -0.994     | 0.490     | -0.993     | 0.536     | **0.930**     | -0.513       |
| **enmity_raw**                  | 0.980      | -0.530    | 0.967    | -0.679   | 0.973    | -0.994     | **1.000**  | -0.393    | 0.980      | -0.443    | **-0.886**    | 0.538        |
| **amity_raw**                   | -0.550     | 0.707     | -0.612   | 0.887    | -0.173   | 0.490      | -0.393     | **1.000** | -0.550     | 0.998     | **0.774**     | 0.049        |
| **fragmentative_goals_raw**     | **1.000**  | -0.673    | 0.991    | -0.760   | 0.915    | -0.993     | 0.980      | -0.550    | **1.000**  | -0.597    | **-0.953**    | 0.407        |
| **cohesive_goals_raw**          | -0.597     | 0.743     | -0.653   | 0.895    | -0.227   | 0.536      | -0.443     | 0.998     | -0.597     | **1.000** | **0.808**     | 0.043        |
| **full_cohesion_index**         | **-0.953** | **0.734** | **-0.973**| **0.908**| **-0.757**| **0.930** | **-0.886** | **0.774** | **-0.953** | **0.808** | **1.000**     | -0.329       |
| **strategic_contradiction_index**| 0.407      | 0.387     | 0.471    | -0.405   | 0.568    | -0.513     | 0.538      | 0.049     | 0.407      | 0.043     | -0.329        | **1.000**    |

### 5.4 Pattern Recognition and Theoretical Insights

The correlation matrix provides a clear map of the rhetorical strategies present in the corpus.

*   **Validation of Oppositional Structure:** The CFF is built on five pairs of opposing concepts. The data provides strong descriptive validation for this structure. The negative correlations between `Fear`/`Hope` (r=-0.834), `Envy`/`Compersion` (r=-0.943), and `Tribal Dominance`/`Individual Dignity` (r=-0.673) are all moderate to very strong. This indicates that as scores on one dimension increase, scores on its theoretical opposite tend to decrease, suggesting the framework is measuring genuinely oppositional constructs. The correlation between `Enmity`/`Amity` (r=-0.393) is weaker, suggesting a more complex relationship where expressions of friendship towards an in-group do not preclude hostility towards an out-group to the same degree.

*   **The Fragmentative Meta-Strategy:** A powerful cluster of fragmentative dimensions is evident. `Tribal Dominance`, `Fear`, `Envy`, and `Enmity` are all highly and positively inter-correlated (r values from 0.883 to 0.991). Notably, `fragmentative_goals_raw` is perfectly correlated (r=1.000) with `tribal_dominance_raw`, suggesting that in this dataset, any appeal to fragmentative goals is indistinguishable from an appeal to tribal dominance. This points to a unified rhetorical strategy that combines group-based identity, fear-mongering, resentment, and hostility.

*   **The Cohesive Meta-Strategy:** A corresponding cohesive cluster also exists. `Individual Dignity`, `Hope`, `Compersion`, `Amity`, and `Cohesive Goals` are all positively correlated with each other. The near-perfect correlation between `Amity` and `Cohesive Goals` (r=0.998) suggests that appeals to cohesive goals in this corpus are almost always framed through the lens of friendship and solidarity.

*   **Cohesion Index as a Summary Variable:** The `full_cohesion_index` performs exactly as designed. It is strongly and negatively correlated with every fragmentative raw score (e.g., r=-0.973 with `fear_raw`) and strongly and positively correlated with every cohesive raw score (e.g., r=0.908 with `hope_raw`). This confirms it is a valid and reliable summary of a document's overall rhetorical posture as measured by the CFF.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CFF demonstrates notable effectiveness in several areas.

*   **Discriminatory Power:** The framework, and particularly its `Full Cohesion Index`, effectively separates the documents across a wide spectrum of scores. It does not simply cluster all documents in the middle but identifies clear rhetorical outliers, which is a key function for any useful analytical tool.
*   **Framework-Corpus Fit:** The highly structured correlation matrix suggests an excellent fit between the CFF's theoretical constructs and the rhetorical patterns present in this political corpus. The data did not produce random or noisy correlations; instead, it revealed a clear, bipolar structure that aligns perfectly with the framework's design.
*   **Methodological Insight:** The analysis highlights the value of measuring opposing dimensions independently. The low `Strategic Contradiction Index` scores across the board is a finding in itself, suggesting that the political rhetoric in this sample is more polarized and less nuanced than might be assumed. A simple unidimensional "cohesion" score would have missed this insight into rhetorical consistency.

## 6. Discussion

### 6.1 Theoretical Implications
The findings from this pilot study, while preliminary, carry significant theoretical implications for the study of political discourse. The emergence of two distinct and opposing rhetorical "clusters" suggests that political language, at least within this sample, is not an ad-hoc collection of appeals but is often deployed in structured, predictable packages. The "Fragmentative Cluster" (`Tribal Dominance`, `Fear`, `Envy`, `Enmity`) and the "Cohesive Cluster" (`Individual Dignity`, `Hope`, `Compersion`, `Amity`) appear to function as coherent, alternative meta-strategies for political communication.

This bipolar structure challenges analytical approaches that treat such concepts in isolation. The data suggests that an appeal to `Fear` is highly likely to be accompanied by an appeal to `Enmity` and `Tribal Dominance`. This implies that analyses focused on a single dimension (e.g., only fear appeals) may miss the broader strategic context in which that appeal is embedded. The CFF's multidimensional approach appears well-suited to capturing this strategic packaging.

### 6.2 Comparative Analysis and Archetypal Patterns
The data allows for the identification of distinct rhetorical archetypes.
*   **The Unifier:** John McCain's 2008 concession speech (Full Cohesion Index = +0.78) exemplifies the cohesive archetype. It is characterized by high scores in `Hope`, `Amity`, `Compersion`, and `Individual Dignity`, and near-zero scores in their fragmentative opposites.
*   **The Divider:** Steve King's 2017 speech (Full Cohesion Index = -0.73) represents the fragmentative archetype. It scores high on `Tribal Dominance`, `Fear`, and `Enmity`, and low on their cohesive counterparts.
*   **The Populist Agitator:** The speeches by Bernie Sanders and Alexandria Ocasio-Cortez present more complex, though still fragmentative, profiles (Indices of -0.30 and -0.19, respectively). They score high on fragmentative dimensions like `Envy` and `Enmity`, likely directed at an "oligarchy" or elite out-group, but may mix this with some cohesive language for their in-group, resulting in a less extreme overall score than the King speech.

The consistently low `Strategic Contradiction Index` across all four archetypes is a key finding. It suggests that these speakers, despite their different goals, all rely on rhetorically consistent messaging. They do not, for instance, try to balance high `Fear` with high `Hope`. This points towards a highly polarized and unambiguous communication environment.

### 6.3 Limitations and Future Directions
The primary limitation of this study is its sample size of four documents. This makes it impossible to generalize findings or test for statistical significance. The results should be seen as a proof-of-concept for the analytical method, not as a definitive statement about political discourse. The second major limitation is the lack of qualitative textual data, which prevents a deeper interpretation of the quantitative scores.

Future research should proceed in several directions:
1.  **Scale:** The analysis must be replicated on a large and diverse corpus of texts to determine if the strong bipolar structure and rhetorical clusters observed here are a general feature of political discourse or an artifact of this small sample.
2.  **Qualitative Triangulation:** A crucial next step is to conduct in-depth qualitative analysis of the documents identified as outliers (e.g., McCain and King). This would help to understand *how* the linguistic features of the text produce the high and low scores on the CFF dimensions, providing a rich, contextualized validation of the quantitative results.
3.  **Investigate Weaker Links:** The relatively weaker correlation between `Enmity` and `Amity` (r=-0.393) warrants further investigation. This could be a statistical anomaly due to the small sample, or it could point to a genuine nuance in rhetoric where it is possible to express amity for an in-group without directly attacking an out-group.

## 7. Conclusion

This computational social science analysis, though constrained by a small pilot dataset, successfully demonstrates the analytical potential of the Cohesive Flourishing Framework v10.1. The study moved beyond surface-level metrics to uncover deep structural patterns within the rhetorical composition of four political speeches. The findings provide strong preliminary evidence for the CFF's construct validity, as its theoretically opposed dimensions were shown to be empirically opposed in the data.

The key contribution of this report is the identification of two coherent and opposing rhetorical meta-strategies—a "Fragmentative Cluster" and a "Cohesive Cluster"—which appear to define a primary axis of variation in this political corpus. The framework's derived metrics, particularly the `Full Cohesion Index` and the `Strategic Contradiction Index`, proved effective in quantifying a document's overall rhetorical posture and its internal consistency.

While no definitive conclusions about political discourse can be drawn from a sample of four, this pilot study serves as a successful methodological demonstration. It establishes a clear path for future research: to validate these structural findings on a larger scale and to integrate quantitative scoring with qualitative analysis to build a richer, more robust understanding of how language shapes our social and political worlds.

## 8. Evidence Citations

A critical component of a comprehensive computational social science analysis is the triangulation of quantitative findings with qualitative textual evidence. This process involves citing specific passages from the source documents that exemplify the rhetorical patterns identified in the statistical data.

**However, for this analysis, no textual evidence was retrieved or made available.**

Therefore, it is not possible to provide the direct textual support that would typically accompany each major finding. This absence represents a significant limitation of the current report, and a key priority for future work would be to link the quantitative scores back to the source texts to provide concrete, qualitative examples for the observed patterns.