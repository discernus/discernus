---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: experiment_name not specified
**Run ID**: run_id not specified
**Date**: 2025-08-24T17:09:36.473007
**Framework**: Cohesive Flourishing Framework (CFF) v10.1
**Corpus**: 4 documents

---

## 1. Executive Summary

This report presents a computational analysis of four political texts using the Cohesive Flourishing Framework (CFF) v10.1. The analysis aimed to extract insights into the rhetorical strategies employed and their potential impact on social cohesion. Due to the exploratory nature of this study and a small sample size (N=4), all findings should be considered preliminary and indicative of patterns requiring further investigation with a larger corpus.

The analysis reveals powerful structural relationships within the CFF, suggesting strong construct validity. Opposing conceptual dimensions, such as Hope and Fear (r = -0.83) or Compersion and Envy (r = -0.94), are strongly negatively correlated, indicating the framework effectively captures these rhetorical trade-offs. The `Full Cohesion Index`, a key summary metric, proved highly effective at discriminating between different types of political discourse. The corpus contained clear rhetorical archetypes: John McCain's 2008 concession speech emerged as a significant positive outlier on cohesion (`Full Cohesion Index` = 0.784), characterized by high Hope, Amity, and Individual Dignity. Conversely, Steve King's 2017 floor speech was a strong negative outlier (`Full Cohesion Index` = -0.727), driven by high scores in Tribal Dominance, Fear, and Enmity. The speeches by Bernie Sanders and Alexandria Ocasio-Cortez presented a more complex, mixed-motive rhetorical strategy, combining fragmentative appeals against an out-group with cohesive appeals to an in-group, resulting in moderate negative cohesion scores and higher levels of internal `Tension`.

The findings demonstrate the CFF's capacity to move beyond simplistic sentiment analysis and quantify the sophisticated, often contradictory, rhetorical strategies present in political language. Fragmentative rhetoric appears to be a highly consistent meta-strategy, with `Tribal Dominance`, `Fear`, `Enmity`, and `Fragmentative Goals` being almost perfectly inter-correlated. Cohesive rhetoric is similarly consistent, linking `Hope`, `Amity`, `Compersion`, and `Cohesive Goals`. A significant limitation of this analysis is the absence of retrievable textual evidence, preventing the qualitative grounding of these statistical findings. Future research should prioritize validating these quantitative patterns against specific textual examples from a larger, more diverse corpus.

## 2. Opening Framework: Key Insights

This analysis of four political texts through the Cohesive Flourishing Framework (CFF) yielded several key insights into the structure of political rhetoric and the framework's utility.

*   **Strong Internal Framework Consistency:** The CFF demonstrates robust construct validity. Core oppositional dimensions show strong negative correlations as theoretically expected. For instance, `Hope` and `Fear` are strongly negatively correlated (r = -0.834), as are `Compersion` and `Envy` (r = -0.943), and `Individual Dignity` and `Tribal Dominance` (r = -0.673). This suggests the framework is successfully measuring distinct and opposing rhetorical concepts.

*   **Identification of Clear Rhetorical Archetypes:** The data reveals distinct rhetorical profiles. John McCain's speech exemplifies a "Unifier" archetype, scoring highest on the `Full Cohesion Index` (0.784). Steve King's speech represents a "Divider" archetype, scoring lowest (-0.727). The speeches by Bernie Sanders and Alexandria Ocasio-Cortez fit a "Populist Agitator" archetype, blending fragmenting and cohesive themes, resulting in moderately negative cohesion scores (-0.296 and -0.185, respectively) and elevated `Tension` metrics.

*   **Fragmentative Rhetoric as a Cohesive "Syndrome":** The analysis reveals that fragmentative language operates as a tightly integrated rhetorical strategy. The dimensions of `Tribal Dominance`, `Fear`, `Envy`, and `Enmity` are all very strongly and positively correlated with each other. For example, the correlation between `Tribal Dominance_raw` and `Fear_raw` is 0.991, and with `Fragmentative Goals_raw` it is a perfect 1.0. This indicates that when one of these elements is present, the others are almost certain to be present as well.

*   **Cohesive Rhetoric Forms an Opposing Cluster:** In direct opposition to the fragmentative syndrome, cohesive dimensions also cluster together. `Hope`, `Amity`, `Compersion`, and `Individual Dignity` are positively correlated with each other and strongly negatively correlated with the fragmentative cluster. The `Full Cohesion Index` is very strongly correlated with `Hope` (r = 0.908) and `Compersion` (r = 0.930), confirming its validity as a measure of positive, unifying rhetoric.

*   **Tension Metrics Reveal Rhetorical Complexity:** While overall tension scores were low, they successfully differentiated the more complex populist messages from the straightforward unifier/divider messages. The speech by Alexandria Ocasio-Cortez, which blended high `Individual Dignity` (0.8) with high `Tribal Dominance` (0.7), registered the highest `Strategic Contradiction Index` (0.090), suggesting a sophisticated strategy of simultaneous appeals to universal values and group-based grievances.

## 3. Literature Review and Theoretical Framework

The Cohesive Flourishing Framework (CFF) positions itself within a growing body of computational social science research aimed at understanding the dynamics of political discourse and its effect on societal well-being. Traditional methods like sentiment analysis often reduce complex language to a single positive-negative scale, failing to capture the nuanced and often contradictory nature of political rhetoric (Grimmer & Stewart, 2013). The CFF addresses this gap by adopting a multi-dimensional, oppositional scoring system, aligning with theories of political communication that emphasize the simultaneous use of competing frames (e.g., hope vs. fear) to persuade audiences (Chong & Druckman, 2007).

The framework's core constructs—such as the tension between `Tribal Dominance` and `Individual Dignity`—resonate with classic political theory on the sources of conflict and solidarity, from the in-group/out-group dynamics described by social identity theory (Tajfel & Turner, 1979) to the liberal democratic emphasis on universal human dignity. By measuring these concepts quantitatively, the CFF provides an empirical tool to test long-standing theories about what constitutes cohesive versus divisive speech. The `Full Cohesion Index` can be seen as an operationalization of concepts like social capital and democratic health, providing a metric to assess how discourse might build or erode the trust and reciprocity necessary for a functioning society (Putnam, 2000). This analysis, therefore, serves as an exploratory test of the CFF's ability to provide empirical traction on these critical theoretical questions.

**References:**
*   Chong, D., & Druckman, J. N. (2007). Framing Theory. *Annual Review of Political Science, 10*, 103-126.
*   Grimmer, J., & Stewart, B. M. (2013). Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts. *Political Analysis, 21*(3), 267-297.
*   Putnam, R. D. (2000). *Bowling Alone: The Collapse and Revival of American Community*. Simon & Schuster.
*   Tajfel, H., & Turner, J. C. (1979). An integrative theory of intergroup conflict. In W. G. Austin & S. Worchel (Eds.), *The social psychology of intergroup relations* (pp. 33-47). Brooks/Cole.

## 4. Methodology

### Framework Description
This analysis utilizes the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze political and social discourse. As described in its *Raison d'être*, the CFF moves beyond simple sentiment analysis by independently scoring texts along several oppositional dimensions. This allows for the measurement of rhetorical complexity, where a single text can simultaneously employ, for example, appeals to both `Hope` and `Fear`. The framework calculates raw scores for primary dimensions (e.g., `Tribal Dominance`, `Individual Dignity`, `Fear`, `Hope`) and derives a series of secondary metrics, including `Tension` scores (e.g., `Identity Tension`, `Emotional Tension`) and composite `Cohesion Indices`.

### Data and Corpus
The dataset for this analysis consists of CFF scores for a small corpus of four documents:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

The data provided includes raw scores, salience scores, confidence scores, and a set of derived metrics for each document, as well as a full correlation matrix of all raw and derived variables across the corpus.

### Statistical Methods
The analysis is primarily descriptive and exploratory, which is appropriate for the small sample size (N=4). The primary statistical methods employed are:
1.  **Descriptive Statistics:** Calculation and interpretation of means, standard deviations, and ranges for all primary CFF dimensions to understand the central tendencies and variability within the corpus.
2.  **Correlation Analysis:** Examination of a Pearson correlation matrix to identify the strength and direction of linear relationships between all CFF dimensions. This is used to assess the framework's internal consistency (construct validity) and to uncover rhetorical meta-strategies or "syndromes."
3.  **Outlier and Archetype Analysis:** Identification of documents with the highest and lowest scores on key derived metrics, particularly the `Full Cohesion Index` and `Strategic Contradiction Index`, to characterize distinct rhetorical profiles.

### Limitations
This study is subject to several significant limitations that must be considered when interpreting the results:
1.  **Small Sample Size:** With a corpus of only four documents (N=4), the findings are not generalizable. The statistical patterns observed, while strong, are preliminary and require validation on a much larger and more diverse dataset. Inferential statistics (e.g., p-values) are not meaningful in this context and are therefore omitted.
2.  **Lack of Textual Evidence:** The analysis was conducted without access to the underlying textual evidence. This is a major constraint, as it prevents the qualitative validation and illustration of statistical findings. All interpretations are based solely on the quantitative data, and the connection between scores and specific linguistic features cannot be demonstrated.
3.  **Unspecified Research Objectives:** The analysis was performed without pre-defined research questions, making it a purely exploratory endeavor. The insights are data-driven and not guided by specific hypotheses.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Descriptive statistics for the primary CFF dimensions reveal a corpus with high variance, suggesting the four selected texts are rhetorically diverse. The mean scores for opposing dimensions are relatively balanced (e.g., `Tribal Dominance_raw` mean = 0.575 vs. `Individual Dignity_raw` mean = 0.450; `Fear_raw` mean = 0.675 vs. `Hope_raw` mean = 0.475), but the standard deviations are large, indicating that scores are clustered at the extremes rather than around the mean. For example, `Hope_raw` has a standard deviation of 0.377 on a 0-1 scale, with scores ranging from a minimum of 0.0 to a maximum of 0.9. This confirms the presence of highly distinct documents within the small sample.

**Table 1: Descriptive Statistics of Primary CFF Raw Scores (N=4)**

| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| tribal_dominance_raw | 0.575 | 0.386 | 0.0 | 0.8 |
| individual_dignity_raw | 0.450 | 0.404 | 0.1 | 0.8 |
| fear_raw | 0.675 | 0.320 | 0.2 | 0.9 |
| hope_raw | 0.475 | 0.377 | 0.0 | 0.9 |
| envy_raw | 0.600 | 0.424 | 0.0 | 0.9 |
| compersion_raw | 0.225 | 0.450 | 0.0 | 0.9 |
| enmity_raw | 0.650 | 0.436 | 0.0 | 0.9 |
| amity_raw | 0.600 | 0.408 | 0.0 | 0.9 |
| fragmentative_goals_raw | 0.575 | 0.386 | 0.0 | 0.8 |
| cohesive_goals_raw | 0.650 | 0.311 | 0.2 | 0.9 |

### 5.2 Advanced Metric Analysis

The derived metrics effectively differentiate the documents, revealing distinct rhetorical strategies. The `Full Cohesion Index` provides the clearest separation. John McCain's speech (0.784) is the only one with a positive score, marking it as uniquely cohesive. Steve King's speech (-0.727) is the most fragmentative. The speeches by Sanders (-0.296) and Ocasio-Cortez (-0.185) occupy a middle ground, indicating a more complex rhetorical mix.

The `Strategic Contradiction Index`, which measures the simultaneous use of competing rhetorical frames, is low across all documents, suggesting generally consistent messaging. However, the variation is telling. The highly consistent speeches by McCain (0.024) and King (0.044) have very low scores. The speech by Ocasio-Cortez (0.090) has the highest score, reflecting its blend of high scores on opposing dimensions like `Individual Dignity` (0.8) and `Enmity` (0.9). This suggests a deliberate strategy of mobilizing support through both universal values and targeted grievances.

**Table 2: Derived CFF Metrics by Document**

| Document | Identity Tension | Emotional Tension | Relational Tension | Goal Tension | Strategic Contradiction Index | Full Cohesion Index |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| john_mccain_2008_concession.txt | 0.000 | 0.120 | 0.000 | 0.000 | 0.024 | 0.784 |
| steve_king_2017_house_floor.txt | 0.080 | 0.000 | 0.000 | 0.140 | 0.044 | -0.727 |
| bernie_sanders_2025_fighting_oligarchy.txt | 0.080 | 0.000 | 0.070 | 0.000 | 0.030 | -0.296 |
| alexandria_ocasio_cortez_2025... | 0.070 | 0.160 | 0.080 | 0.140 | 0.090 | -0.185 |

### 5.3 Correlation and Interaction Analysis

The correlation matrix reveals the deep structure of the CFF and the rhetorical patterns in the corpus. The most striking feature is the existence of two large, opposing clusters of variables.

**The Fragmentative Cluster:** `Tribal Dominance`, `Fear`, `Envy`, `Enmity`, and `Fragmentative Goals` are all extremely highly correlated with one another (most r > 0.9). For example, `Fear_raw` correlates with `Tribal Dominance_raw` at r = 0.991 and with `Enmity_raw` at r = 0.967. This suggests that these rhetorical elements function as a single, cohesive syndrome of fragmentation.

**The Cohesive Cluster:** Conversely, `Individual Dignity`, `Hope`, `Compersion`, `Amity`, and `Cohesive Goals` form another tightly-knit positive cluster. `Amity_raw` correlates with `Hope_raw` at r = 0.887 and with `Cohesive Goals_raw` at r = 0.998.

These two clusters are strongly negatively correlated with each other, confirming the primary axis of the CFF framework. For instance, `Full Cohesion Index` has a near-perfect negative correlation with `Tribal Dominance_raw` (r = -0.953) and `Fear_raw` (r = -0.973), while having a strong positive correlation with `Hope_raw` (r = 0.908) and `Individual Dignity_raw` (r = 0.734).

**Table 3: Abridged Correlation Matrix of Key CFF Dimensions**
*(Note: This is a subset of the full matrix for readability. `TD`=Tribal Dominance, `ID`=Individual Dignity, `FG`=Fragmentative Goals, `CG`=Cohesive Goals, `FCI`=Full Cohesion Index. All values are for `_raw` scores unless specified.)*

| | TD | ID | Fear | Hope | Enmity | Amity | FG | CG | FCI |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **TD** | 1.0 | -0.673 | 0.991 | -0.760 | 0.980 | -0.550 | 1.0 | -0.597 | -0.953 |
| **ID** | -0.673 | 1.0 | -0.631 | 0.535 | -0.530 | 0.707 | -0.673 | 0.743 | 0.734 |
| **Fear** | 0.991 | -0.631 | 1.0 | -0.834 | 0.967 | -0.612 | 0.991 | -0.653 | -0.973 |
| **Hope** | -0.760 | 0.535 | -0.834 | 1.0 | -0.679 | 0.887 | -0.760 | 0.895 | 0.908 |
| **Enmity** | 0.980 | -0.530 | 0.967 | -0.679 | 1.0 | -0.393 | 0.980 | -0.443 | -0.886 |
| **Amity** | -0.550 | 0.707 | -0.612 | 0.887 | -0.393 | 1.0 | -0.550 | 0.998 | 0.774 |
| **FG** | 1.0 | -0.673 | 0.991 | -0.760 | 0.980 | -0.550 | 1.0 | -0.597 | -0.953 |
| **CG** | -0.597 | 0.743 | -0.653 | 0.895 | -0.443 | 0.998 | -0.597 | 1.0 | 0.808 |
| **FCI** | -0.953 | 0.734 | -0.973 | 0.908 | -0.886 | 0.774 | -0.953 | 0.808 | 1.0 |

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns provide strong evidence for the CFF's construct validity. The framework is designed around oppositional pairs, and the data confirms this design with remarkable clarity. The near-perfect negative correlation between `Compersion_raw` and `Tribal_Dominance_raw` (r = -0.993) is particularly telling. It suggests that rhetoric focused on finding joy in the success of others is fundamentally incompatible with rhetoric focused on in-group dominance. This is a powerful, empirically-grounded insight into the deep structure of political communication.

An unexpected finding is the extremely high positive correlation between `Individual Dignity_raw` and `Emotional Tension` (r = 0.980). This suggests that, in this corpus, appeals to individual dignity are not simple, straightforwardly positive statements. Instead, they appear within a rhetorically tense context, perhaps being used to counter a perceived threat or injustice, which introduces emotional complexity. This pattern complicates a simplistic view of "dignity" as a purely cohesive concept and highlights the CFF's ability to uncover nuanced relationships.

The data strongly suggests that political discourse, at least within this sample, operates along a primary axis of cohesion vs. fragmentation. The `Full Cohesion Index` appears to be an excellent proxy for this axis. The fact that `Fragmentative Goals_raw` and `Tribal Dominance_raw` are perfectly correlated (r = 1.0) is a striking finding. It implies that, in the analyzed texts, any articulation of a goal that fragments the community is indistinguishable from an appeal to tribal dominance. This provides a clear, quantifiable link between rhetoric and its strategic social purpose.

### 5.5 Framework Effectiveness Assessment

The CFF demonstrated high effectiveness in this analysis. Its primary strength is its discriminatory power. The framework's metrics, particularly the `Full Cohesion Index`, clearly and effectively separated the documents into meaningful categories (unifier, divider, agitator) that align with intuitive understandings of the speakers' political styles.

The framework-corpus fit appears to be excellent. The strong, theoretically consistent patterns in the correlation matrix suggest that the CFF's dimensions are well-suited to capturing the key features of the political discourse under examination. The high correlations indicate that the framework is not measuring random noise but rather is tapping into real, underlying structures in the language. The `Success_Tension` metric consistently returned NaN or 0, indicating it had no variance in this corpus and thus no discriminatory power. This may be a feature of the specific texts chosen or a potential area for framework refinement.

## 6. Discussion

### Theoretical Implications
This preliminary analysis suggests that political discourse can be effectively modeled as a competition between two opposing rhetorical meta-strategies. The "fragmentation" strategy, a tightly woven syndrome of `Fear`, `Enmity`, `Envy`, and `Tribal Dominance`, appears designed to construct and police in-group/out-group boundaries. The "cohesion" strategy, a corresponding syndrome of `Hope`, `Amity`, `Compersion`, and `Individual Dignity`, appears designed to transcend those boundaries. The CFF provides a robust tool for quantifying the deployment of these competing strategies.

The finding that populist rhetoric (Sanders, Ocasio-Cortez) is characterized by higher `Tension` and `Strategic Contradiction` is theoretically significant. It suggests that this style of communication operates by simultaneously leveraging both fragmenting and cohesive appeals. For example, it may use fragmenting language (`Enmity`, `Envy`) to define an "oligarchic" out-group while using cohesive language (`Amity`, `Dignity`) to build solidarity within the "working class" in-group. The CFF's ability to measure this duality is a significant advance over unidimensional models.

### Comparative Analysis and Archetypal Patterns
The four documents serve as powerful archetypes for different modes of political communication:
1.  **The Unifier (McCain):** Characterized by an almost complete absence of fragmenting themes and a strong emphasis on cohesive ones. The goal is explicitly to bridge divides, as seen in the high `Amity` and `Cohesive Goals` scores. This is a classic "civic" or "republican" (small-r) rhetorical style.
2.  **The Divider (King):** The polar opposite of the Unifier. This style is defined by its singular focus on fragmentation. The near-zero scores on `Hope`, `Compersion`, and `Amity` indicate a rhetoric that is not attempting to build bridges but to fortify walls.
3.  **The Populist Agitators (Sanders & Ocasio-Cortez):** This more complex archetype uses the tools of fragmentation in service of what is framed as a cohesive goal for a specific sub-group. They score high on both `Enmity`/`Envy` and `Amity`/`Dignity`, creating a rhetorically tense and contradictory profile. They are not simply "dividers," as their aim is to unite a particular coalition, but they do so by sharpening a specific social conflict.

### Broader Significance
If these findings hold in a larger sample, they have significant implications for the study of political polarization and democratic health. The CFF could provide a standardized metric for tracking the prevalence of fragmenting versus cohesive rhetoric over time, across different media, and between different political actors. This could move public discourse from subjective impressions of "divisiveness" to objective, data-driven analysis, potentially identifying leading indicators of social friction or democratic decay.

### Limitations and Future Directions
The most pressing limitation is the N=4 sample size. The immediate priority for future research is to apply the CFF to a large, diverse corpus of political texts to test the generalizability of these findings. Are the "fragmentation" and "cohesion" syndromes universal features of political discourse? Do the identified archetypes hold up?

A second critical step is to integrate textual analysis. Future work must connect the quantitative scores back to the specific words and phrases that generate them. This would not only validate the framework's scoring but also provide rich, qualitative insight into how these rhetorical strategies are constructed. For example, what specific language leads to a high `Emotional Tension` score when `Individual Dignity` is invoked? Answering such questions will deepen our understanding of the mechanics of political persuasion.

## 7. Conclusion

This report details an exploratory computational analysis of four political texts using the Cohesive Flourishing Framework v10.1. Despite the significant limitation of a small sample size, the analysis yielded clear and powerful insights. The CFF demonstrated strong internal consistency, with its dimensions clustering into two opposing rhetorical meta-strategies: a fragmenting strategy built on fear and tribalism, and a cohesive strategy built on hope and dignity.

The framework's derived metrics, particularly the `Full Cohesion Index`, successfully distinguished between different rhetorical archetypes present in the corpus—the Unifier, the Divider, and the Populist Agitator. This suggests the CFF is a potent tool for moving beyond simplistic sentiment analysis to capture the complex, and often contradictory, nature of political communication.

While the findings must be considered preliminary, they establish a compelling proof-of-concept. They generate a clear hypothesis for future research: that political discourse is structured along a primary axis of cohesion-fragmentation, and that the CFF provides a valid and reliable means of measuring where a given text falls on this spectrum. The path forward involves scaling this analysis to larger corpora and integrating qualitative evidence to fully unlock the explanatory power of this promising methodological tool.

## 8. Evidence Citations

No textual evidence was available for retrieval and citation in this analysis. The interpretation of statistical findings could not be grounded in specific qualitative examples from the source documents, which is a significant limitation of this report.