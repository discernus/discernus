---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Fabricated Reference**: Identify potentially fabricated academic references or suspicious citation patterns.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Date**: 2025-08-24T22:26:38.595882  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: 4 documents  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of four political texts using the Cohesive Flourishing Framework (CFF) v10.1. The analysis sought to apply the CFF's dimensional model to a small, diverse corpus to assess the framework's utility in extracting nuanced insights into political rhetoric. Due to the pilot nature of this study (N=4), all findings should be considered indicative and serve as a foundation for future, larger-scale research rather than generalizable conclusions.

The analysis reveals that the CFF effectively differentiates between distinct rhetorical strategies. The framework's derived metrics, particularly the `Full_Cohesion_Index`, successfully quantified a clear divide between cohesive and fragmentative discourse, identifying John McCain's 2008 concession speech as a strong archetype of cohesive rhetoric (Cohesion Index: 0.78) and Steve King's 2017 House floor speech as an archetype of fragmentative rhetoric (Cohesion Index: -0.73). Correlation analysis provides strong preliminary support for the framework's construct validity; opposing dimensions (e.g., `Fear` vs. `Hope`) were strongly negatively correlated, while dimensions within the same rhetorical valence (e.g., `Fear`, `Enmity`, `Tribal_Dominance`) were very strongly positively correlated. This suggests the framework is measuring theoretically consistent and distinct concepts.

The findings indicate that political rhetoric in this corpus clusters into coherent meta-strategies. A "Fragmentative" meta-strategy, characterized by the tight coupling of `Tribal_Dominance`, `Fear`, and `Enmity` (r > 0.96), appears to be a highly consistent rhetorical package. Conversely, a "Cohesive" meta-strategy links `Individual_Dignity`, `Hope`, and `Amity`. The analysis also identified a more complex "Populist-Left" archetype (Sanders, Ocasio-Cortez) that simultaneously employs high levels of fragmentative rhetoric against an out-group (oligarchs) and cohesive rhetoric to build in-group solidarity. The framework's ability to capture this complexity, which would be lost in simpler sentiment models, underscores its potential as a sophisticated tool for computational social science.

## 2. Opening Framework: Key Insights

This pilot analysis yielded several key insights into the structure of political rhetoric as measured by the CFF.

*   **Rhetoric Clusters into Opposing Meta-Strategies:** The data reveals two dominant and opposing rhetorical constellations. A "Fragmentative" strategy tightly bundles appeals to `Tribal_Dominance`, `Fear`, `Enmity`, and `Envy`. A "Cohesive" strategy combines `Individual_Dignity`, `Hope`, `Amity`, and `Compersion`. The extremely high correlations within these clusters (e.g., `Fear` and `Tribal_Dominance`, r = 0.99) suggest they represent coherent, packaged rhetorical approaches.
*   **The `Full_Cohesion_Index` is a Potent Discriminator:** This composite metric effectively captured the overarching rhetorical intent of each document, mapping them onto a single, intuitive scale. It clearly separated the highly cohesive speech by John McCain (`Full_Cohesion_Index` = 0.78) from the highly fragmentative speech by Steve King (`Full_Cohesion_Index` = -0.73), demonstrating the metric's high discriminatory power within this sample.
*   **Framework's Oppositional Design Shows Strong Construct Validity:** The CFF is built on pairs of opposing dimensions. The analysis provides preliminary validation for this design, revealing strong negative correlations between these pairs, such as `Compersion` vs. `Tribal_Dominance` (r = -0.99) and `Hope` vs. `Fear` (r = -0.83). This indicates that the framework successfully measures these as distinct, opposing constructs.
*   **Fragmentative Rhetoric is a Tightly Integrated System:** The analysis suggests that fragmentative appeals are not used in isolation. The near-perfect correlation between `Tribal_Dominance` and `Fragmentative_Goals` (r = 1.0) in this dataset indicates that defining an "us vs. them" dynamic is intrinsically linked to proposing goals that benefit the in-group at the expense of the whole. This is exemplified in rhetoric that frames political struggle as a zero-sum conflict. As Bernie Sanders stated, "We will not accept an oligarchic form of society... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt).
*   **The Framework Captures Complex, Mixed-Motive Rhetoric:** The analysis of speeches by Bernie Sanders and Alexandria Ocasio-Cortez reveals a sophisticated strategy that simple sentiment analysis would miss. They score high on fragmentative dimensions like `Enmity` and `Tribal_Dominance` (directed at an "oligarchy") while also scoring high on cohesive dimensions like `Amity` (directed at their supporters). The CFF's ability to score these independently captures this complex strategy of building in-group solidarity through out-group antagonism.
*   **Rhetorical Contradiction is Low:** The `Strategic_Contradiction_Index`, which measures the simultaneous use of opposing appeals with mismatched salience, was consistently low across all documents (Mean = 0.047). This suggests that the speakers, whether cohesive or fragmentative, employed internally consistent rhetorical strategies, avoiding self-undermining messages.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed for the nuanced analysis of political and social discourse. The CFF moves beyond simplistic positive/negative sentiment analysis by operationalizing a set of ten core dimensions, arranged in five oppositional pairs:
*   **Identity:** Tribal Dominance vs. Individual Dignity
*   **Emotion:** Fear vs. Hope
*   **Success:** Envy vs. Compersion
*   **Relations:** Enmity vs. Amity
*   **Goals:** Fragmentative Goals vs. Cohesive Goals

A key feature of the CFF is that it scores each of the ten dimensions independently for both its presence (`raw` score) and its prominence (`salience` score). This allows the framework to capture sophisticated or contradictory rhetoric where, for example, a text might simultaneously evoke strong appeals to both `Hope` and `Fear`. From these base scores, the framework calculates several derived metrics, including Tension Indices, a `Strategic_Contradiction_Index`, and three composite `Cohesion_Indices` (Descriptive, Motivational, Full) that provide a holistic measure of a text's likely impact on social cohesion.

### Data Structure and Corpus Description

The corpus for this pilot study consists of four American political speeches from distinct speakers and contexts:
1.  `john_mccain_2008_concession.txt`: A presidential concession speech.
2.  `steve_king_2017_house_floor.txt`: A speech from the floor of the House of Representatives.
3.  `bernie_sanders_2025_fighting_oligarchy.txt`: A populist speech focused on economic inequality.
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`: A populist speech with similar themes to the Sanders text.

Each document was processed to generate raw and salience scores for the ten CFF dimensions, which formed the basis for the statistical analysis.

### Statistical Methods and Analytical Constraints

Given the exploratory nature of this study and the very small sample size (N=4), the analysis is exclusively descriptive and correlational. Inferential statistics and tests of significance (e.g., p-values) are not appropriate and have been omitted, as they would be statistically meaningless. The primary methods used were:
1.  **Descriptive Statistics:** Calculation of means, standard deviations, and ranges for all raw scores and derived metrics to understand the central tendencies and variance within the corpus.
2.  **Derived Metric Calculation:** Implementation of the CFF v10.1 formulas to compute Tension, Strategic Contradiction, and Cohesion indices for each document.
3.  **Correlation Analysis:** Computation of a Pearson correlation matrix for all raw scores and derived metrics to identify relationships between rhetorical dimensions and explore the framework's internal structure.

### Limitations and Methodological Choices

The foremost limitation of this study is its **sample size**. With only four documents, the findings cannot be generalized to any broader population of political discourse. The results should be interpreted as a proof-of-concept for the analytical method and a source of preliminary hypotheses for future research. The purpose is not to make definitive claims about the speakers or political rhetoric in general, but to demonstrate the CFF's analytical capabilities on a controlled dataset.

Furthermore, one derived metric, `success_tension`, produced no valid data (NaN values in the correlation matrix). This occurred because the underlying calculation (`min(envy_raw, compersion_raw) * ...`) resulted in a column of zeros, as at least one of the raw scores was zero for every document. This indicates a potential area for refinement in the tension metric formula or suggests that this particular tension is rare in this type of discourse.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the ten core CFF dimensions reveals a corpus characterized by high emotional and relational intensity. Fragmentative dimensions, on average, scored higher than their cohesive counterparts.

**Table 1: Descriptive Statistics of CFF Raw Scores (N=4)**
| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Fragmentative Dimensions** | | | | |
| `tribal_dominance_raw` | 0.575 | 0.386 | 0.0 | 0.8 |
| `fear_raw` | 0.675 | 0.320 | 0.2 | 0.9 |
| `envy_raw` | 0.600 | 0.424 | 0.0 | 0.9 |
| `enmity_raw` | 0.650 | 0.436 | 0.0 | 0.9 |
| `fragmentative_goals_raw` | 0.575 | 0.386 | 0.0 | 0.8 |
| **Cohesive Dimensions** | | | | |
| `individual_dignity_raw` | 0.450 | 0.404 | 0.1 | 0.8 |
| `hope_raw` | 0.475 | 0.377 | 0.0 | 0.9 |
| `compersion_raw` | 0.225 | 0.450 | 0.0 | 0.9 |
| `amity_raw` | 0.600 | 0.408 | 0.0 | 0.9 |
| `cohesive_goals_raw` | 0.650 | 0.311 | 0.2 | 0.9 |

The mean scores for `fear_raw` (0.68), `enmity_raw` (0.65), and `envy_raw` (0.60) are notably higher than those for `hope_raw` (0.48) and `compersion_raw` (0.23). This suggests that, on average, the discourse in this small sample relied more heavily on fragmentative emotional appeals. The high standard deviation for dimensions like `compersion_raw` (0.45) and `individual_dignity_raw` (0.40) indicates significant variation across the documents. This variance is key to the framework's discriminatory power. For instance, the high variance in `Individual Dignity` is illustrated by the stark contrast between texts. The analysis of Steve King's speech notes, "The text does not contain language affirming universal human worth" (Source: steve_king_2017_house_floor.txt), while John McCain's speech explicitly affirms it, recognizing "the special significance it has for African-Americans and for the special pride that must be theirs tonight" (Source: john_mccain_2008_concession.txt). This qualitative difference is successfully captured as quantitative variance.

### 5.2 Advanced Metric Analysis

The derived metrics provide a higher-level view of the rhetorical strategies present in the corpus. The `Full_Cohesion_Index` proved to be a particularly powerful summary statistic.

**Table 2: Summary of Derived Corpus Metrics (N=4)**
| Metric | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| `full_cohesion_index` | -0.106 | 0.638 | -0.727 | 0.784 |
| `strategic_contradiction_index` | 0.047 | 0.030 | 0.024 | 0.090 |
| `identity_tension` | 0.058 | 0.039 | 0.000 | 0.080 |
| `emotional_tension` | 0.070 | 0.082 | 0.000 | 0.160 |
| `relational_tension` | 0.037 | 0.043 | 0.000 | 0.080 |
| `goal_tension` | 0.070 | 0.081 | 0.000 | 0.140 |

The `full_cohesion_index` has a slightly negative mean (-0.11), but its enormous standard deviation (0.64) and range (from -0.73 to 0.78) highlight its effectiveness in distinguishing between the documents. The outlier analysis confirms this: John McCain's speech is the highest-scoring document on cohesion, while Steve King's is the lowest. This aligns with an intuitive reading of the texts, where one is a call for unity and the other is a narrative of threat. McCain's high score is driven by language such as, "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession.txt). King's low score is driven by passages like, "this illegal alien beat this boy to death and then he went and bought gasoline and burned his body" (Source: steve_king_2017_house_floor.txt), a clear example of fear-based, fragmentative rhetoric.

Conversely, the `strategic_contradiction_index` is consistently low across all documents (Mean = 0.047, Max = 0.09). This indicates that the rhetorical strategies, whether cohesive or fragmentative, were internally consistent. Speakers did not tend to undermine their own messages by, for example, making a strong appeal to `Hope` while giving it very low salience compared to a simultaneous appeal to `Fear`.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals the deep structure of the rhetorical patterns in the corpus. The results strongly suggest the existence of two opposing "meta-strategies."

**Table 3: Pearson Correlation Matrix of CFF Raw Scores and Key Derived Metrics (N=4, rounded to 3 d.p.)**
*Note: `success_tension` is excluded as it contained no variance.*
| | tribal_dom | indiv_dig | fear | hope | envy | compersion | enmity | amity | frag_goals | coh_goals | full_cohesion | strat_contra |
| :--- |---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **tribal_dominance_raw** | **1.000** | -0.673 | 0.991 | -0.760 | 0.915 | -0.993 | 0.980 | -0.550 | **1.000** | -0.597 | **-0.953** | 0.407 |
| **individual_dignity_raw**| -0.673 | **1.000** | -0.631 | 0.535 | -0.408 | 0.577 | -0.530 | 0.707 | -0.673 | 0.743 | **0.734** | 0.387 |
| **fear_raw** | 0.991 | -0.631 | **1.000** | -0.834 | 0.883 | -0.989 | 0.967 | -0.612 | 0.991 | -0.653 | **-0.973** | 0.471 |
| **hope_raw** | -0.760 | 0.535 | -0.834 | **1.000** | -0.500 | 0.751 | -0.679 | 0.887 | -0.760 | 0.895 | **0.908** | -0.405 |
| **envy_raw** | 0.915 | -0.408 | 0.883 | -0.500 | **1.000** | -0.943 | 0.973 | -0.173 | 0.915 | -0.227 | **-0.757** | 0.568 |
| **compersion_raw** | -0.993 | 0.577 | -0.989 | 0.751 | -0.943 | **1.000** | -0.994 | 0.490 | -0.993 | 0.536 | **0.930** | -0.513 |
| **enmity_raw** | 0.980 | -0.530 | 0.967 | -0.679 | 0.973 | -0.994 | **1.000** | -0.393 | 0.980 | -0.443 | **-0.886** | 0.538 |
| **amity_raw** | -0.550 | 0.707 | -0.612 | 0.887 | -0.173 | 0.490 | -0.393 | **1.000** | -0.550 | 0.998 | **0.774** | 0.049 |
| **fragmentative_goals_raw**| **1.000** | -0.673 | 0.991 | -0.760 | 0.915 | -0.993 | 0.980 | -0.550 | **1.000** | -0.597 | **-0.953** | 0.407 |
| **cohesive_goals_raw** | -0.597 | 0.743 | -0.653 | 0.895 | -0.227 | 0.536 | -0.443 | 0.998 | -0.597 | **1.000** | **0.808** | 0.043 |
| **full_cohesion_index** | **-0.953** | **0.734** | **-0.973** | **0.908** | **-0.757** | **0.930** | **-0.886** | **0.774** | **-0.953** | **0.808** | **1.000** | -0.329 |
| **strategic_contradiction_index**| 0.407 | 0.387 | 0.471 | -0.405 | 0.568 | -0.513 | 0.538 | 0.049 | 0.407 | 0.043 | -0.329 | **1.000** |

### 5.4 Pattern Recognition and Theoretical Insights

The correlation matrix provides a rich map of rhetorical strategy.

**Strongest Correlations and Practical Significance:**
The most striking pattern is the tight positive correlation among all fragmentative dimensions. `Tribal_Dominance` is almost perfectly correlated with `Fear` (r=0.991), `Enmity` (r=0.980), and `Fragmentative_Goals` (r=1.000). This suggests that these are not independent choices but components of a single, powerful rhetorical engine. When a speaker in this corpus defines a tribal out-group, they almost invariably pair it with fear-inducing narratives about that group and goals that involve defeating or punishing them. This is evident in Steve King's speech, where the out-group ("illegal alien") is the subject of a graphic threat narrative ("beat this boy to death") linked to a fragmentative goal ("Send these people into prison").

**Construct Validity of the Framework:**
The CFF's design is predicated on oppositional pairs. The matrix provides strong, albeit preliminary, evidence for this construct validity. Every pair shows a strong to moderate negative correlation:
*   `Tribal_Dominance` vs. `Individual_Dignity`: r = -0.673
*   `Fear` vs. `Hope`: r = -0.834
*   `Envy` vs. `Compersion`: r = -0.943
*   `Enmity` vs. `Amity`: r = -0.393 (the weakest, but still negative)
*   `Fragmentative_Goals` vs. `Cohesive_Goals`: r = -0.597

The extremely strong negative correlation between `Compersion` and `Envy` (r = -0.943) and `Compersion` and `Enmity` (r = -0.994) is particularly noteworthy. It indicates that rhetoric celebrating an opponent's success is fundamentally incompatible with rhetoric expressing grievance or hostility. John McCain's speech exemplifies `Compersion`, stating that his opponent's success "is something I deeply admire and commend him for achieving" (Source: john_mccain_2008_concession.txt). This is the polar opposite of the `Envy` dimension, illustrated by Bernie Sanders's focus on a "rigged economy" where there has been a "$75 trillion transfer of wealth from the bottom 90% to the top 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt).

**Unexpected Findings and Implications:**
The perfect (r=1.0) correlation between `Tribal_Dominance` and `Fragmentative_Goals` is a powerful finding within this dataset. It implies that, for these speakers, the very act of creating a tribal "other" is synonymous with advocating for a zero-sum, fragmenting policy. This suggests a rhetorical model where group-based identity politics is not merely a descriptive act but is inherently tied to actionable, divisive objectives. This warrants significant further investigation in a larger corpus.

**Framework-Corpus Fit:**
The CFF appears to be an excellent fit for this corpus of political speeches. It produced highly differentiated scores and a correlation matrix with a clear, theoretically coherent structure. The failure of the `success_tension` metric is a notable limitation, suggesting that the formula may be too sensitive to zero-scores in the underlying dimensions. However, the overall performance of the primary dimensions and the composite cohesion indices is strong.

### 5.5 Framework Effectiveness Assessment

The framework demonstrated high effectiveness in two key areas: discriminatory power and the generation of methodological insights.

**Discriminatory Power:** The CFF successfully distinguished not only between opposing political ideologies but also between different rhetorical styles within a similar ideological space. The `Full_Cohesion_Index` placed the four documents in a clear order: McCain (+0.78), Ocasio-Cortez (-0.19), Sanders (-0.30), and King (-0.73). This ordering is intuitively plausible and highlights the framework's ability to move beyond a simple left-right political spectrum to a cohesion-fragmentation spectrum.

**Methodological Insights:** The analysis validates the CFF's core design principle: measuring opposing dimensions independently. A traditional sentiment analyzer might score the Sanders speech as neutral or confused, as it contains strong elements of both `Hope` and `Fear`. As he stated, "in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs" (`Fear`), but also "if we stand together... I have every reason to believe deeply in my heart that... we can create the kind of nation that we deserve" (`Hope`) (Source: bernie_sanders_2025_fighting_oligarchy.txt). The CFF captures this complexity, showing high scores on both dimensions, which is a more accurate representation of the rhetorical strategy than a simple averaged score.

## 6. Discussion

### Theoretical Implications of Findings

This pilot study's findings, while preliminary, suggest that the CFF can operationalize and quantify theoretical concepts of cohesive and fragmentative discourse. The strong clustering of dimensions into two opposing meta-strategies—one built on shared dignity, hope, and amity, the other on tribalism, fear, and enmity—provides empirical support for theories that frame political communication as a contest between universalist and particularist worldviews. The `Full_Cohesion_Index` acts as a quantitative proxy for where a given text falls on this spectrum.

The analysis further suggests that fragmentative rhetoric is not an ad-hoc collection of negative appeals but a systematic, internally coherent strategy. The tight coupling of its components implies that activating one element (e.g., `Fear`) may prime an audience for others (e.g., `Tribal_Dominance`, `Enmity`). This has significant implications for understanding political polarization, suggesting that certain rhetorical packages may be inherently polarizing.

### Comparative Analysis and Archetypal Patterns

The results allow for the identification of three distinct rhetorical archetypes within this small corpus:

1.  **The Civic Cohesion Archetype (McCain):** Characterized by the near-total absence of fragmentative rhetoric and high scores on all cohesive dimensions (`Individual_Dignity`, `Hope`, `Compersion`, `Amity`, `Cohesive_Goals`). The rhetorical goal is explicitly to bridge divides and affirm a shared national identity. This is perfectly captured in the statement, "Whatever our differences, we are fellow Americans" (Source: john_mccain_2008_concession.txt). This archetype produces a very high `Full_Cohesion_Index` and a very low `Strategic_Contradiction_Index`.

2.  **The Threat-Based Fragmentation Archetype (King):** This is the polar opposite of the first archetype. It is defined by high scores on all fragmentative dimensions and near-zero scores on all cohesive dimensions. The discourse is centered on defining an out-group, portraying it as a mortal threat, and advocating for its exclusion or punishment. The lack of `Hope`, `Amity`, or `Compersion` creates a stark, unadulterated message of conflict. The analysis of this text noted a complete "absence of evidence" for `Amity`, stating, "The rhetorical stance is consistently oppositional" (Source: steve_king_2017_house_floor.txt).

3.  **The Populist Antagonism Archetype (Sanders/Ocasio-Cortez):** This is the most complex archetype. It combines high scores on fragmentative dimensions (particularly `Tribal_Dominance`, `Envy`, and `Enmity`) with high scores on cohesive dimensions (`Hope`, `Amity`, `Cohesive_Goals`). The fragmentative rhetoric is targeted at a specific out-group ("oligarchs," "the 1%"), while the cohesive rhetoric is used to build solidarity within the in-group ("the people," "the 99%"). This strategy uses out-group condemnation as the very basis for in-group cohesion. The call to "stand together" is explicitly for the purpose of defeating an enemy, as seen in the quote, "if we stand together... not only will we defeat Trumpism, but we can create the kind of nation that we deserve" (Source: bernie_sanders_2025_fighting_oligarchy.txt). This results in a negative `Full_Cohesion_Index` but reveals a nuanced and powerful political strategy.

### Broader Significance and Future Directions

This analysis serves as a methodological blueprint for applying the CFF to larger and more diverse corpora. The clear patterns emerging from just four documents suggest that a larger-scale analysis could yield significant insights into political communication. Future research should aim to:

*   **Expand the Corpus:** Analyze a large, representative sample of political speeches to test whether the identified archetypes and correlational structures hold.
*   **Temporal Analysis:** Examine how these rhetorical patterns have evolved over time. Has the use of the "Threat-Based Fragmentation" archetype increased?
*   **Audience Response:** Connect CFF scores to real-world outcomes, such as polling data, social media engagement, or election results, to test the hypothesis that cohesion scores correlate with civic health indicators.
*   **Refine Metrics:** Investigate the failure of the `success_tension` metric and explore alternative formulations that are less sensitive to zero-scores.

## 7. Conclusion

This computational social science analysis, though limited in scope, successfully demonstrates the analytical power of the Cohesive Flourishing Framework v10.1. By moving beyond simple sentiment analysis to a multi-dimensional, oppositional model, the CFF was able to quantify and differentiate complex rhetorical strategies in a small sample of political texts.

The study's primary contribution is methodological. It provides a clear proof-of-concept, showing that the framework's constructs have preliminary validity, as evidenced by the strong, theoretically consistent patterns in the correlation matrix. The derived `Full_Cohesion_Index` emerged as a robust and discriminating metric. The analysis generated several testable hypotheses about the structure of political rhetoric, including the existence of coherent "Cohesive" and "Fragmentative" meta-strategies and a more complex "Populist Antagonism" archetype. These findings underscore the value of computational methods that preserve, rather than discard, the complex and often contradictory nature of human communication. While no substantive claims can be made from this pilot study, it establishes a firm foundation and a clear direction for future, more extensive research into the linguistic drivers of social cohesion and fragmentation.

## 8. Evidence Citations

The following textual evidence was used to support the statistical interpretations in this report.

**Source: `john_mccain_2008_concession.txt`**
*   On Individual Dignity: "This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."
*   On Amity: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
*   On Compersion: "But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake or little influence in the election of an American president is something I deeply admire and commend him for achieving."
*   On Tribal Dominance (Contrasting Evidence): "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

**Source: `steve_king_2017_house_floor.txt`**
*   On Individual Dignity (Absence): "The text does not contain language affirming universal human worth. Individuals from the out-group are consistently reduced to their criminal status or actions (e.g., 'an illegal criminal alien drunk driving perpetrator')."
*   On Fear: "this illegal alien beat this boy to death and then he went and bought gasoline and burned his body. He hauled his body out and and put gas and poured gasoline on it and burned this Joshua Wilkerson's body and then he went and took a shower and went to a movie as if it was just another day..."
*   On Amity (Absence): "There are no appeals to friendship, cooperation, common ground, or unity with any of the identified out-groups (political opponents, activist judges, immigrants). The rhetorical stance is consistently oppositional."
*   On Cohesive Goals (In-Group Focused): "Secure our borders. Restore their respect for the rule of law. Save these lives. Send these people into prison."

**Source: `bernie_sanders_2025_fighting_oligarchy.txt`**
*   On Tribal Dominance & Fragmentative Goals: "We will not accept an oligarchic form of society... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%."
*   On Fear: "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   On Hope & Amity: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve."
*   On Envy: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."