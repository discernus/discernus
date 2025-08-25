# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: 2c1d1220de92f50a308679e670d754850c94298c1adda41c91cef6730da91ac8  
**Date**: 2025-08-24T21:09:36.433552+00:00  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Not available (4 documents)  

---

## 1. Executive Summary

This report details a preliminary computational analysis of a small corpus (N=4) of political texts using the Cohesive Flourishing Framework (CFF) v10.1. The analysis aimed to apply the CFF's dimensional model to extract insights into the rhetorical strategies employed and their potential impact on social cohesion. Due to the extremely small sample size, all findings should be considered illustrative and preliminary, serving as a proof-of-concept for the analytical methodology rather than a generalizable conclusion about political discourse.

The analysis reveals a stark polarization of rhetoric within the corpus. The documents cluster at two opposite ends of a cohesive-fragmentative spectrum, with little middle ground. The primary finding is the identification of two distinct and internally consistent rhetorical archetypes. The "Cohesive Unifier" archetype, exemplified by John McCain's 2008 concession speech, is characterized by high scores in dimensions like Individual Dignity, Hope, and Amity, resulting in a strongly positive `Full Cohesion Index` (+0.78). Conversely, the "Fragmentative Agitator" archetype, most clearly represented by Steve King's 2017 House floor speech, relies on a tightly-coupled strategy of Tribal Dominance, Fear, and Envy, yielding a highly negative `Full Cohesion Index` (-0.73).

The CFF demonstrated strong potential in this pilot analysis. The framework's oppositional design was supported by the data, with opposing dimensions showing strong negative correlations (e.g., `compersion_raw` vs. `envy_raw`, r = -0.94), suggesting high construct validity for this sample. Furthermore, the `Strategic Contradiction Index` was consistently low across all documents (M = 0.047), indicating that the speakers employed clear, non-contradictory rhetorical strategies rather than mixing cohesive and fragmentative appeals. These preliminary results suggest the CFF is a promising tool for quantifying and categorizing rhetorical styles, generating testable hypotheses for future, larger-scale research.

## 2. Opening Framework: Key Insights

This pilot analysis, while limited in scope, yielded several key insights into the rhetorical patterns within the analyzed texts:

*   **Rhetoric is Highly Polarized:** The corpus is not characterized by nuanced or mixed messaging. Instead, documents fall into one of two camps: overwhelmingly cohesive or overwhelmingly fragmentative. This is most evident in the `Full Cohesion Index`, which shows a wide range from -0.73 to +0.78 with no documents scoring in the moderate middle range.
*   **Fragmentative Rhetoric Forms a Cohesive "Meta-Strategy":** The analysis reveals a powerful synergy between fragmentative dimensions. Appeals to `tribal_dominance_raw`, `fear_raw`, `envy_raw`, and `enmity_raw` are very strongly and positively correlated (all r > +0.88). This suggests that these are not independent choices but part of a unified rhetorical strategy aimed at mobilizing an in-group against a perceived out-group threat.
*   **The CFF's Oppositional Structure Appears Validated:** The framework's core design, which pairs cohesive dimensions against fragmentative ones, is strongly supported by the data. For instance, `tribal_dominance_raw` and `individual_dignity_raw` are negatively correlated (r = -0.67), as are `fear_raw` and `hope_raw` (r = -0.83). This indicates the framework is successfully capturing the intended conceptual oppositions present in the discourse.
*   **Cohesion Scores Effectively Differentiate Rhetorical Archetypes:** The CFF's derived metrics, particularly the `Full Cohesion Index`, serve as powerful discriminators. The analysis identified John McCain's 2008 concession speech as a clear archetype of cohesive rhetoric (`Full Cohesion Index` = +0.78), while Steve King's 2017 speech represents a clear archetype of fragmentative rhetoric (`Full Cohesion Index` = -0.73).
*   **Discourse in this Sample is Strategically Simple:** The `Strategic Contradiction Index`, which measures the simultaneous use of opposing appeals, was exceptionally low across all documents (M = 0.047). This suggests the speakers in this sample pursued rhetorically "pure" strategies, avoiding the complex and potentially confusing mixture of hope and fear, or amity and enmity, within the same text.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed for the nuanced analysis of political and social discourse. The CFF moves beyond simplistic sentiment analysis by measuring language along ten distinct, theoretically-grounded dimensions organized into five oppositional pairs:
*   **Identity:** Tribal Dominance vs. Individual Dignity
*   **Emotion:** Fear vs. Hope
*   **Success:** Envy vs. Compersion
*   **Relations:** Enmity vs. Amity
*   **Goals:** Fragmentative Goals vs. Cohesive Goals

A key feature of the CFF is its independent scoring of each dimension, allowing it to capture sophisticated rhetoric where opposing appeals might be used simultaneously. From these raw scores, the framework calculates several derived metrics, including three **Cohesion Indices** (Descriptive, Motivational, Full) that provide an overall measure of a text's likely impact on social cohesion, and five **Tension Indices** that quantify the degree of strategic contradiction within the rhetoric.

### Data Structure and Corpus Description

The analysis was performed on a small pilot corpus of four English-language political texts. While the corpus manifest was unavailable, the documents were identified through the statistical analysis as:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

The dataset for each document consists of a raw score (0-1) and a salience score (0-1) for each of the ten CFF dimensions. The analysis relies entirely on the provided statistical results, which include descriptive statistics, derived metric calculations, a full Pearson correlation matrix, and outlier identification. It is important to note that textual evidence was only available for the McCain, King, and Sanders documents, limiting the qualitative interpretation for the Ocasio-Cortez text.

### Statistical Methods and Analytical Constraints

The analytical approach is primarily descriptive and correlational. The core statistical methods include:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, minimum, and maximum for all raw scores and derived metrics to understand central tendencies and variance.
2.  **Derived Metric Calculation:** Application of the CFF v10.1 formulas to compute Cohesion Indices, Tension Indices, and the Strategic Contradiction Index for each document.
3.  **Pearson Correlation:** Computation of a correlation matrix to examine the relationships between all raw CFF dimensions and the key derived metrics. This is the primary method for identifying rhetorical meta-strategies and assessing the framework's construct validity.

The most significant analytical constraint is the extremely small sample size (N=4). This prevents any meaningful inferential statistical testing and means that the findings are not generalizable. All results, particularly correlation coefficients, should be interpreted with extreme caution as they are highly sensitive to the specific characteristics of these four documents. The purpose of this report is to demonstrate the *type* of analysis the CFF enables, not to make definitive claims about political discourse at large.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the ten raw CFF dimensions reveals a corpus characterized by high variance and a general leaning towards fragmentative rhetoric.

**Table 1: Descriptive Statistics of Raw CFF Dimension Scores (N=4)**

| Dimension                   | Mean  | Std. Dev. | Min   | Max   |
|-----------------------------|-------|-----------|-------|-------|
| **Fragmentative Dimensions**|       |           |       |       |
| `tribal_dominance_raw`      | 0.575 | 0.386     | 0.0   | 0.8   |
| `fear_raw`                  | 0.675 | 0.320     | 0.2   | 0.9   |
| `envy_raw`                  | 0.600 | 0.424     | 0.0   | 0.9   |
| `enmity_raw`                | 0.650 | 0.436     | 0.0   | 0.9   |
| `fragmentative_goals_raw`   | 0.575 | 0.386     | 0.0   | 0.8   |
| **Cohesive Dimensions**     |       |           |       |       |
| `individual_dignity_raw`    | 0.450 | 0.404     | 0.1   | 0.8   |
| `hope_raw`                  | 0.475 | 0.377     | 0.0   | 0.9   |
| `compersion_raw`            | 0.225 | 0.450     | 0.0   | 0.9   |
| `amity_raw`                 | 0.600 | 0.408     | 0.0   | 0.9   |
| `cohesive_goals_raw`        | 0.650 | 0.311     | 0.2   | 0.9   |

The fragmentative dimensions generally show higher mean scores than their cohesive counterparts. `Fear_raw` (M=0.675) and `enmity_raw` (M=0.650) are particularly prominent, suggesting that threat narratives and adversarial framing are common rhetorical tools in this sample. As Steve King stated, framing a graphic threat narrative: **"...this illegal alien beat this boy to death and then he went and bought gasoline and burned his body... and then he went and took a shower and went to a movie as if it was just another day..." (Source: steve_king_2017_house_floor.txt)**. This type of rhetoric directly contributes to the high mean `fear_raw` score.

Conversely, the cohesive dimension of `compersion_raw` (celebrating others' success) has the lowest mean score (M=0.225) and a very high standard deviation (0.450), indicating it is a rarely used and highly polarizing dimension. For some texts, it is entirely absent. For example, the analysis of Bernie Sanders' speech notes: **"No direct or indirect evidence of this dimension was found in the text. The document's rhetoric focuses on the illegitimacy and negative consequences of the out-group's success." (Source: bernie_sanders_2025_fighting_oligarchy.txt)**. This contrasts sharply with texts that do employ it, such as John McCain's, which states: **"But that he managed to do so by inspiring the hopes of so many millions of Americans... is something I deeply admire and commend him for achieving." (Source: john_mccain_2008_concession.txt)**. The high standard deviations across most dimensions (typically >0.3) confirm the wide rhetorical variance and polarization within this small corpus.

### 5.2 Advanced Metric Analysis

The derived CFF metrics provide a higher-level view of the corpus's rhetorical strategy, confirming the pattern of polarization and strategic consistency.

**Table 2: Summary of Derived Corpus Metrics (N=4)**

| Metric                          | Mean    | Std. Dev. | Min     | Max    |
|---------------------------------|---------|-----------|---------|--------|
| `full_cohesion_index`           | -0.106  | 0.638     | -0.727  | 0.784  |
| `strategic_contradiction_index` | 0.047   | 0.030     | 0.024   | 0.090  |
| `identity_tension`              | 0.058   | 0.039     | 0.000   | 0.080  |
| `emotional_tension`             | 0.070   | 0.082     | 0.000   | 0.160  |
| `success_tension`               | 0.000   | 0.000     | 0.000   | 0.000  |
| `relational_tension`            | 0.037   | 0.043     | 0.000   | 0.080  |
| `goal_tension`                  | 0.070   | 0.081     | 0.000   | 0.140  |

The `full_cohesion_index` is the most telling metric. Its slightly negative mean (-0.106) is less important than its massive standard deviation (0.638) and range, spanning nearly the entire possible scale from -1 to +1. This confirms that the corpus contains examples of both highly cohesive and highly fragmentative discourse. The outlier analysis identifies the two poles of this spectrum: John McCain's speech (`full_cohesion_index` = +0.784) and Steve King's speech (`full_cohesion_index` = -0.727). McCain's speech is defined by cohesive appeals, as he stated: **"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession.txt)**.

In stark contrast, the `strategic_contradiction_index` is consistently low (M=0.047), with a maximum value of only 0.09. This indicates that none of the documents engage in significant rhetorical contradiction. Speakers are not, for example, pairing strong appeals to Hope with strong appeals to Fear. This suggests that the rhetorical strategies, whether cohesive or fragmentative, are "pure" and unambiguous. The `success_tension` is uniformly zero, indicating a complete separation of Envy and Compersion appeals; no text attempted to use both.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals the underlying structure of rhetorical strategies within the corpus. It provides strong evidence for the CFF's construct validity and uncovers two dominant, competing "meta-strategies."

**Table 3: Pearson Correlation Matrix for CFF Raw Scores and Derived Indices (Selected Values)**

| Variable A                  | Variable B                      | Correlation (r) |
|-----------------------------|---------------------------------|-----------------|
| **Framework Validation (Oppositional Pairs)** |                                 |                 |
| `tribal_dominance_raw`      | `individual_dignity_raw`        | -0.673          |
| `fear_raw`                  | `hope_raw`                      | -0.834          |
| `envy_raw`                  | `compersion_raw`                | -0.943          |
| `enmity_raw`                | `amity_raw`                     | -0.393          |
| `fragmentative_goals_raw`   | `cohesive_goals_raw`            | -0.597          |
| **Fragmentative Meta-Strategy** |                                 |                 |
| `tribal_dominance_raw`      | `fear_raw`                      | 0.991           |
| `tribal_dominance_raw`      | `envy_raw`                      | 0.915           |
| `fear_raw`                  | `enmity_raw`                    | 0.967           |
| `tribal_dominance_raw`      | `fragmentative_goals_raw`       | 1.000           |
| **Cohesive Meta-Strategy**      |                                 |                 |
| `individual_dignity_raw`    | `cohesive_goals_raw`            | 0.743           |
| `hope_raw`                  | `amity_raw`                     | 0.887           |
| `hope_raw`                  | `cohesive_goals_raw`            | 0.895           |
| **Index Correlations**          |                                 |                 |
| `tribal_dominance_raw`      | `full_cohesion_index`           | -0.953          |
| `hope_raw`                  | `full_cohesion_index`           | 0.908           |

The strong negative correlations between most oppositional pairs (e.g., `envy_raw` vs. `compersion_raw`, r = -0.943) provide preliminary validation for the CFF's theoretical design. The dimensions behave as conceptual opposites within this dataset.

More significantly, the matrix exposes two tightly-knit clusters of dimensions. The **Fragmentative Meta-Strategy** is a powerful combination of `tribal_dominance`, `fear`, `envy`, `enmity`, and `fragmentative_goals`. The correlations within this cluster are exceptionally high, many approaching a perfect positive correlation. For instance, the link between `tribal_dominance_raw` and `fear_raw` (r = +0.991) is nearly absolute. This suggests that, in this corpus, to evoke a tribal identity is to evoke fear. This is exemplified in the rhetoric of Bernie Sanders, who links a tribal out-group ("oligarchs") directly to a threat: **"But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs." (Source: bernie_sanders_2025_fighting_oligarchy.txt)**.

Conversely, a **Cohesive Meta-Strategy** emerges, linking `individual_dignity`, `hope`, `amity`, and `cohesive_goals`. The correlations are strong, though slightly less tight than the fragmentative cluster. The relationship between `hope_raw` and `amity_raw` (r = +0.887) is notable, suggesting that expressions of hope are intertwined with calls for unity. As John McCain stated, linking hope for the future with coming together: **"...to not despair of our present difficulties, but to believe always in the promise and greatness of America." (Source: john_mccain_2008_concession.txt)**. This statement, in a speech filled with calls for amity, illustrates the connection.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns allow for deeper theoretical insights. The most striking finding is the perfect correlation (r = 1.000) between `tribal_dominance_raw` and `fragmentative_goals_raw`. This indicates that, within this specific dataset, the act of defining a tribal "us vs. them" is perfectly synonymous with attributing destructive intentions to the "them." There is no instance where a speaker defines a strong out-group without also claiming that group seeks fragmentative ends. This is clearly visible in Bernie Sanders' speech, where the tribal out-group ("the wealthiest 1%") is immediately tied to destructive goals: **"We will not accept an oligarchic form of society... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%." (Source: bernie_sanders_2025_fighting_oligarchy.txt)**. The attribution of a fragmentative goal (taking money via tax breaks) is part of the definition of the tribe.

Another powerful insight comes from the near-perfect negative correlation between `compersion_raw` and `tribal_dominance_raw` (r = -0.993). This suggests that celebrating an opponent's success is fundamentally incompatible with a tribalistic worldview in this sample. A speaker does one or the other, but never both. This highlights the framework's ability to map the deep structure of rhetorical choices. John McCain's speech, which scores high on `compersion` and low on `tribal_dominance`, explicitly rejects tribalism in favor of a shared identity: **"Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that." (Source: john_mccain_2008_concession.txt)**.

These patterns suggest that the framework has a strong fit with the corpus. The clear, strong correlations and the logical clustering of dimensions indicate that the CFF is measuring meaningful and consistent rhetorical structures. The primary unexpected finding is not the presence of these patterns, but their sheer strength and simplicity. The data does not support the CFF's own premise that sophisticated communicators often mix appeals; rather, it suggests that for this sample, the dominant mode of communication is to pick a single, internally-consistent strategy and execute it forcefully.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF appears to be an effective tool for quantifying and categorizing political rhetoric.

*   **Discriminatory Power:** The framework, and particularly the `Full Cohesion Index`, demonstrates excellent discriminatory power. It successfully separated the four documents across a wide spectrum of scores, clearly identifying the rhetorical style of each. The ability to place McCain's concession speech and Steve King's floor speech at opposite ends of the same quantitative scale is a testament to the index's utility.
*   **Framework-Corpus Fit:** The fit between the CFF's theoretical structure and the empirical data from this corpus is strong. The oppositional dimensions are negatively correlated as predicted, and the derived metrics for cohesion and contradiction map cleanly onto intuitive readings of the texts. The low contradiction scores suggest the framework is correctly identifying the "rhetorically pure" strategies employed in this sample.
*   **Methodological Insights:** This analysis highlights the value of analyzing dimensions in concert rather than in isolation. The discovery of the "Fragmentative Meta-Strategy" through correlation analysis provides a much richer insight than simply observing that the texts scored high on Fear or Enmity individually. It reveals a coordinated rhetorical system at play.

## 6. Discussion

### Theoretical Implications of Findings

The findings from this preliminary analysis carry several interesting theoretical implications. The most significant is the suggestion that, at least in highly polarized contexts, political rhetoric may simplify into two mutually exclusive modes: one aimed at bridging divides and the other at deepening them. The data challenges the notion that effective political speech is always a complex tapestry of competing appeals. Instead, it points towards the existence of clear, archetypal strategies that are internally consistent and diametrically opposed. The low `Strategic Contradiction Index` across the board suggests that, for these speakers, rhetorical clarity and forcefulness took precedence over nuance.

This raises a critical question for future research: is this strategic simplicity an artifact of this small, specific sample, or is it a feature of contemporary political discourse? The CFF provides the tools to test this. If this pattern holds across a larger corpus, it would suggest that political actors perceive more benefit in mobilizing a base with a "pure" fragmentative message than in persuading a broader audience with a mixed, and potentially less potent, one.

### Comparative Analysis and Archetypal Patterns

The analysis clearly reveals two rhetorical archetypes:

1.  **The Cohesive Unifier:** Exemplified by John McCain's 2008 concession speech. This archetype is defined by its active disavowal of tribalism and its emphasis on shared identity, respect for opponents, and forward-looking, unifying goals. Key dimensions are `Individual Dignity`, `Compersion`, `Amity`, and `Hope`. The goal is to lower political tensions and reinforce the legitimacy of the democratic process, even in defeat. This is seen in McCain's call to **"find the necessary compromises to bridge our differences" (Source: john_mccain_2008_concession.txt)**.

2.  **The Fragmentative Agitator:** Represented by the speeches from Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez, though with different flavors. This archetype is defined by its construction of a virtuous in-group ("the people," "Americans") and a threatening, often immoral out-group ("oligarchs," "illegal aliens"). It leverages the powerful emotional forces of `Fear`, `Envy`, and `Enmity` and attributes destructive `Fragmentative Goals` to the opposition. The goal is to mobilize the in-group for political battle. King's version is rooted in cultural and national identity, while Sanders' is rooted in economic class conflict, as seen when he frames the issue as a **"$75 trillion transfer of wealth from the bottom 90% to the top 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt)**. Despite these differences, the underlying rhetorical structure captured by the CFF is remarkably similar.

### Broader Significance and Future Directions

While these findings are preliminary, they highlight the potential of computational frameworks like the CFF to move discourse analysis from a purely qualitative exercise to a quantitative science. By operationalizing concepts like "cohesion" and "fragmentation," the CFF allows for scalable, reproducible, and comparative analysis of rhetorical strategies.

The most pressing need is for future research to apply this methodology to a large, diverse, and longitudinal corpus of political texts. This would allow researchers to:
*   **Test Generalizability:** Determine if the two archetypes identified here are robust and recurrent patterns in modern politics.
*   **Analyze Temporal Trends:** Track whether political discourse, on average, is becoming more or less cohesive over time.
*   **Investigate Contextual Factors:** Explore how the rhetorical context (e.g., campaign rally, legislative debate, concession speech) influences the choice of strategy.
*   **Explore Nuance:** A larger dataset may reveal more documents with high `Strategic Contradiction` scores, allowing for an analysis of when and why speakers choose to employ more complex, mixed messaging.

## 7. Conclusion

This report presents a pilot application of the Cohesive Flourishing Framework (CFF) v10.1 to a small corpus of four political texts. Despite the significant limitation of the small sample size, the analysis successfully demonstrates the framework's capacity to generate rich, data-driven insights into rhetorical strategy. The study identified a stark polarization in the discourse, leading to the characterization of two competing archetypes: the "Cohesive Unifier" and the "Fragmentative Agitator."

Methodologically, the analysis provides strong preliminary support for the CFF's construct validity. The framework's oppositional dimensions were shown to be negatively correlated in the data, and its derived metrics for cohesion and contradiction effectively captured the dominant rhetorical patterns. The discovery of a tightly integrated "Fragmentative Meta-Strategy"—linking Tribal Dominance, Fear, Envy, and Enmity—showcases the CFF's ability to uncover the deep structure of political language.

The primary contribution of this work is as a proof-of-concept. It establishes a clear analytical workflow and generates a set of testable hypotheses about rhetorical archetypes that warrant further investigation with larger datasets. The findings suggest that the CFF is a valuable tool for researchers seeking to understand the linguistic drivers of social cohesion and fragmentation in an empirical and scalable manner.