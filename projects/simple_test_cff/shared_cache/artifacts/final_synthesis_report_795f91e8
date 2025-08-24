# Cohesive Flourishing Framework Analysis Report

**Experiment**: political_discourse_archetypes_pilot
**Run ID**: 22fb48a4ac8aa0009882c4b23a357d23e065cb1c3b3484ddefc85b8bde3cdfe9
**Date**: 2025-08-24T01:07:33.593135+00:00
**Framework**: Cohesive Flourishing Framework (CFF) v10.1
**Corpus**: diverse_political_speeches_n4 (4 documents)

---

## 1. Executive Summary

This report details a computational analysis of four distinct political texts using the Cohesive Flourishing Framework (CFF) v10.1. The analysis reveals a political discourse landscape characterized by deep rhetorical divisions and the deployment of highly structured, opposing communication strategies. The primary finding is the identification of a powerful "Fragmentative Meta-Strategy," a rhetorical engine that tightly couples appeals to **Tribal Dominance**, **Fear**, **Enmity**, and **Envy**. This strategy, which registered extremely high inter-correlations (r > 0.98 between key dimensions), is the dominant feature in three of the four analyzed texts, resulting in a corpus that is, on average, fragmentative, as indicated by a negative mean Full Cohesion Index (M = -0.149).

Conversely, the analysis identifies a "Cohesive Meta-Strategy" characterized by the linkage of **Individual Dignity**, **Hope**, **Amity**, and **Compersion**. This strategy, exemplified by one text in the corpus, produces strongly positive cohesion scores. The stark contrast between these two rhetorical archetypes—the "Populist Challenger" and the "Institutional Unifier"—demonstrates the CFF's significant discriminatory power. The framework's theoretical design is strongly validated by the data, with all opposing dimensional pairs exhibiting the expected negative correlations (e.g., Tribal Dominance vs. Individual Dignity, r = -0.670), confirming its construct validity.

While the small sample size (N=4) precludes generalization, this pilot study serves as a powerful proof-of-concept. It demonstrates the CFF's capacity to move beyond simple sentiment analysis to uncover the structural logic of political communication, revealing how language is systematically used to either build or dismantle social cohesion. The findings suggest that fragmentative and cohesive discourses are not random assortments of emotional appeals but are, in fact, coherent, internally consistent, and mutually exclusive rhetorical systems.

## 2. Opening Framework: Key Insights

*   **A "Fragmentative Meta-Strategy" Dominates Divisive Rhetoric:** The analysis uncovered a near-perfectly correlated cluster of fragmentative dimensions. Appeals to **Tribal Dominance** (us vs. them) are almost inseparable from appeals to **Fear** (r = 0.992), **Enmity** (r = 0.980), and **Fragmentative Goals** (r = 0.993). This indicates a highly structured rhetorical strategy where identifying an out-group is intrinsically linked to stoking fear and hostility towards them.
*   **Two Mutually Exclusive Rhetorical Archetypes Emerge:** The data clearly delineates two distinct communication styles. The "Populist Challenger" (e.g., Sanders, Ocasio-Cortez, King) leverages the Fragmentative Meta-Strategy, resulting in strongly negative cohesion scores. In stark contrast, the "Institutional Unifier" (e.g., McCain) employs a Cohesive Meta-Strategy, producing strongly positive cohesion scores. The data suggests these are not points on a continuum but distinct, opposing modes of discourse.
*   **The CFF Framework Demonstrates Robust Construct Validity:** The framework's design, which posits five oppositional axes, is strongly supported. In every case, the "cohesive" dimension is negatively correlated with its "fragmentative" counterpart. For instance, **Envy** and **Compersion** show a very strong negative relationship (r = -0.841), as do **Tribal Dominance** and **Individual Dignity** (r = -0.670). This confirms the framework is measuring theoretically sound, opposing concepts.
*   **The Absence of Compersion is a Key Marker of Fragmentative Discourse:** The dimension of **Compersion** (celebrating the legitimate success of others) is almost entirely absent from the fragmentative texts (M = 0.225), while its opposite, **Envy** (resenting others' success), is prominent (M = 0.550). The near-zero score for the `success_tension` index (M = 0.0) highlights that this is not a nuanced trade-off but a categorical exclusion, suggesting that fragmentative rhetoric structurally struggles to accommodate a vision of shared or legitimate out-group success.
*   **Discourse is Overwhelmingly Fragmentative on Average:** The central finding from the derived metrics is that the corpus, as a whole, leans toward fragmentation. The **Full Cohesion Index**, the CFF's most comprehensive measure, has a negative mean of -0.149. This is driven by the high intensity of fragmentative language in three of the four documents, which outweighs the single, highly cohesive document.

## 3. Literature Review and Theoretical Framework

This analysis is situated at the intersection of computational linguistics, political science, and communication studies. The Cohesive Flourishing Framework (CFF) addresses a central concern in contemporary political science: the rise of **affective polarization**, where political identity becomes a primary source of social division, transcending policy disagreement into mutual distrust and animosity (Iyengar, Sood, & Lelkes, 2012). The CFF's dimensions map directly onto the mechanisms of polarization, providing a tool to quantify its rhetorical drivers.

The framework's oppositional structure—such as **Tribal Dominance** vs. **Individual Dignity**—resonates with **Moral Foundations Theory** (Haidt, 2012), which posits that different political ideologies prioritize distinct moral intuitions. The CFF can be seen as a tool for measuring the rhetorical activation of these foundations, particularly the binding foundations (Loyalty, Authority, Sanctity) often associated with `Tribal Dominance` and the individualizing foundations (Care, Fairness) associated with `Individual Dignity` and `Amity`.

Furthermore, the analysis of rhetorical strategies aligns with the work of scholars on populism, who identify a core logic of a virtuous "people" (the in-group) against a corrupt "elite" or dangerous "other" (the out-group) (Mudde & Kaltwasser, 2017). The "Fragmentative Meta-Strategy" identified in this report provides a quantifiable, multi-dimensional signature of this populist logic. By measuring not just the presence of these themes but their intensity, salience, and interrelation, the CFF offers a granular method for operationalizing and testing theories of populist communication. It moves beyond content analysis to a structural analysis of the rhetorical patterns that constitute a polarizing worldview.

## 4. Methodology

### Framework Description
This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze discourse along five oppositional axes, each critical to social cohesion:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion
4.  **Relation:** Enmity vs. Amity
5.  **Goals:** Fragmentative Goals vs. Cohesive Goals

For each of these 10 dimensions, the CFF produces a `raw` score (intensity, 0-1), a `salience` score (prominence, 0-1), and a `confidence` score. This multi-faceted output allows for nuanced analysis, distinguishing between a text that strongly asserts a concept versus one that subtly implies it. A key feature of the CFF is its independent scoring of opposing dimensions, which enables the measurement of complex rhetorical strategies, such as the simultaneous use of hope and fear.

### Data and Corpus
The analysis was conducted on a small (N=4) but diverse corpus of American political speeches, including texts from Bernie Sanders, Alexandria Ocasio-Cortez, Steve King, and John McCain. This selection allows for the exploration of rhetorical patterns across different ideological positions and political contexts (e.g., campaign rally vs. election concession).

### Statistical Methods and Analytical Constraints
The analysis is primarily descriptive and exploratory, focusing on interpreting the statistical outputs generated by the CFF analysis pipeline. The methods include:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, min, and max for all raw and salience scores to understand the central tendency and variance of each rhetorical dimension across the corpus.
2.  **Derived Indices:** Calculation of the CFF's proprietary **Cohesion Indices** (Descriptive, Motivational, Full) and **Tension Indices**. These composite scores provide a holistic view of a text's overall rhetorical impact.
3.  **Correlation Analysis:** A Pearson correlation matrix was computed for all raw scores and derived indices to identify structural relationships and rhetorical meta-strategies.

**Crucial Limitation:** The sample size of this pilot study is **N=4**. This is insufficient for inferential statistical claims or generalization to a wider population of political discourse. Therefore, all correlation coefficients and mean comparisons are interpreted as descriptions of the patterns *within this specific dataset*. They serve to validate the CFF's structure and generate hypotheses for future, larger-scale research, not to establish statistically significant, generalizable truths.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics: A Landscape of Division

An examination of the descriptive statistics reveals a corpus dominated by fragmentative language. Across the board, the mean raw scores for fragmentative dimensions are higher than their cohesive counterparts. **Fear** (M=0.65), **Enmity** (M=0.65), and **Fragmentative Goals** (M=0.60) are among the most prevalent themes. In contrast, cohesive dimensions like **Compersion** (M=0.23) and **Individual Dignity** (M=0.43) are notably less present.

This pattern suggests that the discourse analyzed is more focused on identifying threats, defining enemies, and proposing oppositional actions than on celebrating shared success or affirming universal human worth. For example, the high mean score for **Fear** is exemplified by Rep. Steve King's visceral depiction of a crime: as King stated, *"this illegal alien beat this boy to death and then he went and bought gasoline and burned his body... and then he went and took a shower and went to a movie as if it was just another day..."* (Source: `steve_king_2017_house_floor.txt`). This raw, threatening imagery drives the Fear score upward.

Conversely, the extremely low mean for **Compersion** is just as revealing. The analysis of several texts returned explicit findings of its absence. For instance, in Rep. Ocasio-Cortez's speech, the system noted: *"No evidence found for this dimension. The speech's focus is on the illegitimate success of an oligarchy, not celebrating the success of others. Its absence is a significant feature of the text."* (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`). This highlights that the rhetorical space is occupied by its opposite, **Envy** (M=0.55), which is used to frame the success of the out-group as illegitimate.

**Table 1: Descriptive Statistics for CFF Raw Scores**
| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Fragmentative Dimensions** | | | | |
| tribal_dominance_raw | 0.575 | 0.386 | 0.00 | 0.80 |
| fear_raw | 0.650 | 0.370 | 0.10 | 0.90 |
| envy_raw | 0.550 | 0.436 | 0.00 | 0.90 |
| enmity_raw | 0.650 | 0.436 | 0.00 | 0.90 |
| fragmentative_goals_raw | 0.600 | 0.400 | 0.00 | 0.80 |
| **Cohesive Dimensions** | | | | |
| individual_dignity_raw | 0.425 | 0.435 | 0.00 | 0.80 |
| hope_raw | 0.475 | 0.330 | 0.00 | 0.70 |
| compersion_raw | 0.225 | 0.450 | 0.00 | 0.90 |
| amity_raw | 0.550 | 0.404 | 0.00 | 0.90 |
| cohesive_goals_raw | 0.550 | 0.351 | 0.20 | 0.90 |

### 5.2 Advanced Metric Analysis: Quantifying Cohesion and Tension

The CFF's derived indices confirm the descriptive story, painting a picture of a generally fragmentative corpus with low levels of sophisticated rhetorical contradiction.

**Cohesion Indices:** All three cohesion indices show a negative mean, indicating that, on balance, the language in the corpus is more divisive than unifying. The **Full Cohesion Index**, which provides the most comprehensive assessment, has a mean of -0.149. This score, while seemingly close to neutral, is significant given that it averages texts with extreme opposing scores. It reflects the net effect of three highly fragmentative speeches overpowering one highly cohesive speech. The negative score is driven by the salience-weighted dominance of themes like Fear and Enmity over Hope and Amity. As Senator Bernie Sanders stated, *"in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."* (Source: `bernie_sanders_2025_fighting_oligarchy.txt`). This framing of a dangerous, corrupting force contributes directly to a negative cohesion score.

**Table 2: Descriptive Statistics for CFF Cohesion Indices**
| Index | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| descriptive_cohesion_index | -0.196 | 0.678 | -0.785 | 0.781 |
| motivational_cohesion_index | -0.139 | 0.662 | -0.692 | 0.813 |
| full_cohesion_index | -0.149 | 0.670 | -0.716 | 0.802 |

**Tension Indices:** The Rhetorical Tension Indices, which measure the strategic use of opposing concepts, are uniformly low. The **Strategic Contradiction Index**, an average of the five tension scores, has a mean of just 0.057. This indicates that the speeches in this corpus tend to be rhetorically one-sided. They do not, for example, pair strong appeals to Hope with strong appeals to Fear to create a complex emotional landscape. Instead, they lean heavily on one or the other. The `success_tension` index is zero, with zero variance. This is a statistical artifact caused by the `compersion_raw` score being zero in the most envious texts, making the `min(envy, compersion)` term in the formula zero. This is a finding in itself: the rhetoric is so devoid of celebrating out-group success that the very possibility of tension on this axis is eliminated.

**Table 3: Descriptive Statistics for CFF Tension Indices**
| Index | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| identity_tension | 0.055 | 0.068 | 0.000 | 0.140 |
| emotional_tension | 0.083 | 0.074 | 0.000 | 0.150 |
| success_tension | 0.000 | 0.000 | 0.000 | 0.000 |
| relational_tension | 0.070 | 0.095 | 0.000 | 0.200 |
| goal_tension | 0.077 | 0.061 | 0.000 | 0.150 |
| **strategic_contradiction_index** | **0.057** | **0.053** | **0.008** | **0.114** |

### 5.3 Correlation and Interaction Analysis

The correlation matrix reveals the deep structural logic of the rhetorical patterns in the corpus. It provides the strongest evidence for the existence of cohesive and fragmentative meta-strategies and validates the CFF's design.

*(Note: Due to its size, only a selection of key correlations is discussed below. The full matrix is presented for reference.)*

**Table 4: Pearson Correlation Matrix of CFF Raw Scores and Derived Indices**
*(Abridged for clarity; key relationships are discussed in the text. `NaN` indicates no variance for calculation.)*
| | tribal_dom | indiv_dig | fear | hope | envy | compersion | enmity | amity | frag_goals | coh_goals | full_cohesion |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **tribal_dominance_raw** | 1.00 | -0.67 | **0.99** | -0.48 | 0.80 | -0.99 | **0.98** | -0.65 | **0.99** | -0.75 | **-0.98** |
| **individual_dignity_raw**| -0.67 | 1.00 | -0.63 | 0.52 | -0.22 | 0.57 | -0.52 | **0.90** | -0.57 | **0.99** | **0.79** |
| **fear_raw** | **0.99** | -0.63 | 1.00 | -0.56 | 0.77 | -0.99 | **0.97** | -0.67 | **0.99** | -0.72 | **-0.97** |
| **hope_raw** | -0.48 | 0.52 | -0.56 | 1.00 | 0.08 | 0.45 | -0.36 | **0.84** | -0.45 | 0.56 | **0.61** |
| **envy_raw** | 0.80 | -0.22 | 0.77 | 0.08 | 1.00 | -0.84 | **0.89** | -0.08 | 0.84 | -0.30 | **-0.65** |
| **compersion_raw** | -0.99 | 0.57 | -0.99 | 0.45 | -0.84 | 1.00 | -0.99 | 0.58 | -1.00 | 0.66 | **0.95** |
| **enmity_raw** | **0.98** | -0.52 | **0.97** | -0.36 | **0.89** | -0.99 | 1.00 | -0.49 | **0.99** | -0.61 | **-0.91** |
| **amity_raw** | -0.65 | **0.90** | -0.67 | **0.84** | -0.08 | 0.58 | -0.49 | 1.00 | -0.58 | **0.92** | **0.80** |
| **fragmentative_goals_raw**| **0.99** | -0.57 | **0.99** | -0.45 | 0.84 | -1.00 | **0.99** | -0.58 | 1.00 | -0.66 | **-0.95** |
| **cohesive_goals_raw** | -0.75 | **0.99** | -0.72 | 0.56 | -0.30 | 0.66 | -0.61 | **0.92** | -0.66 | 1.00 | **0.86** |
| **full_cohesion_index** | **-0.98** | **0.79** | **-0.97** | **0.61** | **-0.65** | **0.95** | **-0.91** | **0.80** | **-0.95** | **0.86** | 1.00 |

### 5.4 Pattern Recognition and Theoretical Insights

The correlation matrix is not merely a collection of numbers; it is a map of rhetorical strategy. The most powerful insights emerge from analyzing the clusters of highly correlated dimensions.

**The Fragmentative Meta-Strategy:** The data reveals an extraordinarily tight-knit cluster of fragmentative concepts. **Tribal Dominance** is the keystone, showing near-perfect positive correlations with **Fear** (r=0.992), **Enmity** (r=0.980), and **Fragmentative Goals** (r=0.993). This is not a loose association; it is a rigid rhetorical structure. The strategy is simple and potent:
1.  **Define the Tribe:** Establish a clear "us" versus "them" (`tribal_dominance`). As Rep. Ocasio-Cortez stated: *"We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves..."* (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`).
2.  **Invoke Threat:** Portray "them" as a direct, existential threat (`fear`). As Senator Sanders stated: *"They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer."* (Source: `bernie_sanders_2025_fighting_oligarchy.txt`).
3.  **Cultivate Hostility:** Foster antagonism and resentment towards the out-group (`enmity` and `envy`). Rep. Ocasio-Cortez's claim that billionaires *"aren’t working for these billions. They’re stealing them,"* is a classic example (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`).
4.  **Propose Oppositional Action:** Channel this negative energy into a goal of defeating or removing the out-group (`fragmentative_goals`). This is seen in the call to *"give Evans and Boebert the boot, and replace them..."* (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`).

**The Cohesive Meta-Strategy:** An opposing, though slightly less rigid, cluster defines the cohesive strategy. **Individual Dignity** and **Amity** are the core components. `Individual_dignity_raw` is strongly correlated with `amity_raw` (r=0.901) and `cohesive_goals_raw` (r=0.993). This strategy operates as follows:
1.  **Affirm Universal Worth:** Begin by establishing a foundation of shared humanity and dignity that transcends group boundaries (`individual_dignity`). As Senator John McCain stated: *"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."* (Source: `john_mccain_2008_concession.txt`).
2.  **Appeal to Goodwill:** Call for friendship, cooperation, and understanding (`amity`). McCain urges his supporters to offer his opponent *"our good will and earnest effort to find ways to come together"* (Source: `john_mccain_2008_concession.txt`).
3.  **Inspire Hope:** Frame the future in optimistic, agentic terms (`hope`). McCain calls on Americans *"to not despair of our present difficulties, but to believe always in the promise and greatness of America."* (Source: `john_mccain_2008_concession.txt`).
4.  **Propose Collaborative Action:** Define goals centered on bridging differences and achieving shared prosperity (`cohesive_goals`), such as the need *"to find the necessary compromises to bridge our differences."* (Source: `john_mccain_2008_concession.txt`).

### 5.5 Framework Effectiveness Assessment

The results of this pilot analysis demonstrate the CFF's effectiveness on several fronts.
*   **Discriminatory Power:** The framework and its derived indices show excellent discriminatory power. The `full_cohesion_index` clearly separates the conciliatory McCain speech (score: 0.802) from the highly fragmentative King speech (score: -0.716) and the populist Sanders/AOC speeches (scores: -0.692 and -0.785 on the `descriptive_cohesion_index`). This ability to quantify the rhetorical distance between texts is a key strength.
*   **Construct Validity:** As noted, the consistent and strong negative correlations between opposing dimensions (e.g., `compersion_raw` vs. `fragmentative_goals_raw`, r = -1.00) provide powerful evidence for the framework's construct validity. The five axes appear to be measuring genuinely oppositional concepts in this corpus.
*   **Methodological Insight:** The analysis reveals that the *absence* of a dimension can be as informative as its presence. The near-total lack of `Compersion` and the corresponding zero-variance `success_tension` index is a critical finding, pointing to a structural feature of fragmentative rhetoric: an inability to legitimize the success of an out-group. This is a nuanced insight that simple sentiment analysis would miss.

## 6. Discussion

### Theoretical Implications
The findings from this analysis have significant theoretical implications. The identification of tightly-coupled "Fragmentative" and "Cohesive" meta-strategies suggests that polarizing and unifying discourses are not simply matters of tone or topic, but are structurally coherent, self-reinforcing rhetorical systems. The fragmentative system, built on the `tribal_dominance` -> `fear` -> `enmity` axis, functions as a powerful engine for social division and mobilization against a perceived enemy. This provides an empirical, multi-dimensional "fingerprint" for the type of populist and polarizing rhetoric described by scholars like Mudde and Kaltwasser (2017).

Conversely, the cohesive system, built on `individual_dignity` -> `amity` -> `hope`, offers a model for deliberative, democratic, and unifying speech. The mutual exclusivity of these patterns in the data (i.e., texts that are high in one are low in the other) suggests that they represent fundamentally different theories of social change and political engagement. One seeks victory through division, the other seeks progress through collaboration.

### Comparative Analysis and Archetypal Patterns
The data allows for the clear identification of two rhetorical archetypes:
1.  **The Populist Challenger:** This archetype, represented by the speeches of Sanders, Ocasio-Cortez, and King, is defined by high scores on the fragmentative dimensions and a strongly negative cohesion index. Despite their different targets (oligarchs vs. immigrants), they share an identical rhetorical *structure*: identifying a powerful and malevolent out-group that is harming the virtuous in-group, thereby justifying oppositional goals. As Sanders stated: *"Abraham Lincoln talked about a government of the people, by the people, for the people. Well, Trump has a government of the billionaires, by the billionaires, and for the billionaires."* (Source: `bernie_sanders_2025_fighting_oligarchy.txt`). This directly parallels the "us vs. them" logic.
2.  **The Institutional Unifier:** This archetype, represented by McCain's concession speech, is defined by high scores on cohesive dimensions and a strongly positive cohesion index. This rhetoric is deployed at moments of potential crisis or transition to de-escalate conflict, affirm the legitimacy of the political system, and re-center a shared national identity. As McCain stated: *"Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."* (Source: `john_mccain_2008_concession.txt`). This language actively works to lower polarization.

### Limitations and Future Directions
The most significant limitation of this study is its sample size of four documents. The findings, while internally consistent and theoretically rich, cannot be generalized. The extremely high correlation values are likely inflated by the low N and the selection of archetypal texts.

This pilot study, however, paves the way for future research. The primary next step is to apply the CFF to a large, representative corpus of political speech (e.g., the Congressional Record, presidential campaign speeches over time). This would allow for robust testing of the hypotheses generated here:
*   **H1:** The "Fragmentative Meta-Strategy" (high correlation between Tribal Dominance, Fear, Enmity) is a consistent and statistically significant feature of populist and polarizing political discourse.
*   **H2:** The "Cohesive Meta-Strategy" is a consistent feature of institutional or ceremonial discourse (e.g., inaugural addresses, concession speeches).
*   **H3:** The Full Cohesion Index will show a statistically significant decline in political discourse over the past several decades, correlating with measures of affective polarization.
*   **H4:** The `success_tension` index will be consistently low in highly polarized discourse, indicating a structural inability to engage in `Compersion`.

## 7. Conclusion

This computational analysis, though limited in scope, provides a powerful demonstration of the Cohesive Flourishing Framework's analytical capabilities. By moving beyond surface-level sentiment, the CFF has uncovered the deep rhetorical structures that underpin both social cohesion and fragmentation. The identification of two opposing and internally consistent meta-strategies—one built on division and fear, the other on dignity and amity—offers a new, quantifiable lens through which to understand our political discourse.

The framework's design has been strongly validated by the data, showing clear discriminatory power and robust construct validity. The analysis successfully identified distinct rhetorical archetypes and generated a set of testable hypotheses about the nature of political communication. While the results from this small pilot must be interpreted with caution, they highlight a promising path forward for the computational social sciences. By providing tools to measure the complex dynamics of cohesion, the CFF enables a more rigorous, evidence-based diagnosis of the health of our public square and the language that shapes it.

## 8. Evidence Citations

*Complete attribution for all quoted evidence, organized by source document.*

**Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`**
- "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."
- "They aren’t working for these billions. They’re stealing them. They’re stealing them. They’re stealing them from you and you and me."
- "we need to come together and spend every day between now and election day working to educate our neighbors, and give Evans and Boebert the boot, and replace them with a brawling Democrat who will stand for Colorado."
- "No evidence found for this dimension. The speech's focus is on the illegitimate success of an oligarchy, not celebrating the success of others. Its absence is a significant feature of the text."

**Source: `bernie_sanders_2025_fighting_oligarchy.txt`**
- "in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
- "They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer."
- "Abraham Lincoln talked about a government of the people, by the people, for the people. Well, Trump has a government of the billionaires, by the billionaires, and for the billionaires."

**Source: `john_mccain_2008_concession.txt`**
- "This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."
- "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
- "to not despair of our present difficulties, but to believe always in the promise and greatness of America."
- "to find the necessary compromises to bridge our differences and help restore our prosperity, defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
- "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

**Source: `steve_king_2017_house_floor.txt`**
- "this illegal alien beat this boy to death and then he went and bought gasoline and burned his body. He hauled his body out and and put gas and poured gasoline on it and burned this Joshua Wilkerson's body and then he went and took a shower and went to a movie as if it was just another day..."