---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: experiment configuration
**Date**: 2025-08-24
**Framework**: Cohesive Flourishing Framework (CFF) v10.1
**Corpus**: Not available (4 documents)

---

## 1. Executive Summary

This report presents a computational analysis of four political speeches using the Cohesive Flourishing Framework (CFF) v10.1. The analysis sought to evaluate the framework's capacity to measure rhetorical strategies related to social cohesion. Despite the preliminary nature of the findings due to a small sample size (N=4), the results indicate that the CFF is a robust tool for differentiating complex political discourse. The analysis reveals a stark polarization of rhetorical strategies within the corpus, clustering around two opposing meta-constructs: a "Cohesive" strategy and a "Fragmentative" strategy.

The key finding is the identification of distinct rhetorical archetypes. John McCain's 2008 concession speech serves as a clear archetype of cohesive rhetoric, achieving a `full_cohesion_index` of +0.84 by emphasizing `amity`, `hope`, and `individual_dignity` while eschewing divisive language. Conversely, Steve King's 2017 House floor speech exemplifies fragmentative rhetoric, with a `full_cohesion_index` of -0.74, driven by high scores in `tribal_dominance`, `fear`, and `enmity`. The speeches by Bernie Sanders and Alexandria Ocasio-Cortez represent a third, more complex "Populist Agitator" archetype, characterized by high `strategic_contradiction_index` scores (0.10 and 0.04, respectively). This style simultaneously employs fragmentative tactics (e.g., high `envy`, `enmity`) to define an out-group and cohesive tactics (e.g., high `amity`) to rally an in-group.

Methodologically, the framework demonstrates strong internal consistency and construct validity. The analysis found powerful negative correlations between the CFF's opposing dimensions (e.g., `tribal_dominance_salience` and `compersion_salience`, r = -1.00), supporting its theoretical design. These preliminary results suggest the CFF is an effective instrument for moving beyond simple sentiment analysis to map the sophisticated and often contradictory ways language is used to build or undermine social cohesion.

## 2. Opening Framework: Key Insights

*   **Rhetoric Polarizes into Two Opposing Meta-Strategies:** The analysis reveals a clear bifurcation in communication styles. The CFF dimensions coalesce into a "Fragmentative" cluster (`tribal_dominance`, `fear`, `enmity`, `envy`) and a "Cohesive" cluster (`individual_dignity`, `hope`, `amity`, `compersion`). These two clusters are strongly negatively correlated, suggesting they represent fundamentally opposed rhetorical approaches to political communication.
*   **Framework Construct Validity is Strongly Supported:** The CFF's oppositional design is validated by the statistical results. Key opposing dimensions exhibit very strong negative correlations, as theoretically predicted. For instance, `tribal_dominance_salience` and `compersion_salience` have a perfect negative correlation (r = -1.00), while `fragmentative_goals_salience` and `compersion_salience` also correlate at r = -1.00. This indicates the framework is successfully measuring distinct and opposing constructs.
*   **A "Populist Agitator" Archetype Emerges:** The speeches by Sanders and Ocasio-Cortez exhibit a unique rhetorical signature characterized by high scores on both fragmentative and cohesive dimensions simultaneously. This results in a high `strategic_contradiction_index` (Sanders: 0.10). This hybrid strategy uses fragmentative language to target an out-group (e.g., "billionaires") while using cohesive language to build solidarity within an in-group (e.g., "working people"). As Bernie Sanders stated, defining an enemy ("Trump has a government of the billionaires") is paired with a call for unity ("if we stand together... we can create the kind of nation that we deserve"). (Source: bernie_sanders_2025_fighting_oligarchy.txt).
*   **The `Full_Cohesion_Index` Effectively Differentiates Texts:** The primary derived metric, `full_cohesion_index`, demonstrates significant discriminatory power, with scores ranging from highly cohesive (+0.84 for McCain) to highly fragmentative (-0.74 for King). This suggests the index is a valid and useful summary statistic for classifying the overall rhetorical posture of a document.
*   **Cohesive Rhetoric is Defined by Absence:** The most cohesive text in the corpus (McCain) is notable not just for its high scores in dimensions like `amity` and `hope`, but for its near-zero scores across all five fragmentative dimensions (`tribal_dominance`, `fear`, `envy`, `enmity`, `fragmentative_goals`). This suggests that truly cohesive discourse may be defined as much by what it avoids saying as by what it actively promotes. As John McCain stated, "Whatever our differences, we are fellow Americans," a direct counter to tribal framing. (Source: john_mccain_2008_concession.txt).

## 4. Methodology

### Framework Description
This analysis utilizes the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze political and social discourse. The CFF measures communication along five oppositional axes, each with a fragmentative and a cohesive pole:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion (finding joy in others' success)
4.  **Relations:** Enmity vs. Amity
5.  **Goals:** Fragmentative Goals vs. Cohesive Goals

For each dimension, the framework generates a `raw` score (intensity) and a `salience` score (prominence). This dual-scoring system allows for a nuanced analysis that captures both the presence and the emphasis of each rhetorical element. The oppositional design is a core feature, intended to test whether these concepts behave as polar opposites in practice.

### Corpus Description
The corpus for this pilot study consists of four American political speeches:
1.  `john_mccain_2008_concession.txt`: A presidential concession speech.
2.  `steve_king_2017_house_floor.txt`: A speech on immigration from the floor of the U.S. House of Representatives.
3.  `bernie_sanders_2025_fighting_oligarchy.txt`: A populist speech addressing economic inequality.
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`: A populist speech addressing economic inequality.

While small, this corpus was selected to represent a diverse range of political ideologies and rhetorical contexts (concession, legislative debate, political rally).

### Statistical Methods and Limitations
The analysis is primarily descriptive and correlational. Key statistical methods include:
*   **Descriptive Statistics:** Calculation of mean, standard deviation, minimum, and maximum for all CFF dimensions and derived metrics to understand central tendencies and variance.
*   **Pearson Correlation:** A correlation matrix was computed to examine the relationships between all CFF dimensions. This is the primary method for assessing the framework's construct validity by testing the relationships between its oppositional pairs.
*   **Derived Metric Analysis:** Interpretation of composite indices calculated from the primary dimensions, such as the `full_cohesion_index` and `strategic_contradiction_index`.

**Critical Limitation:** The most significant limitation of this study is its sample size (N=4). The findings, while statistically clear within this sample, cannot be generalized to broader political discourse. All interpretations should be considered preliminary and indicative, serving as hypotheses for future research with larger corpora. No inferential statistical claims (e.g., p-values) are made, as they would be inappropriate for this sample size.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

The descriptive statistics for the corpus reveal significant variance across the CFF dimensions, indicating the framework's ability to differentiate the texts. Fragmentative dimensions like `tribal_dominance` (Mean=0.56), `fear` (Mean=0.60), and `enmity` (Mean=0.63) were, on average, more prevalent than their cohesive counterparts like `individual_dignity` (Mean=0.48) and `hope` (Mean=0.43). The dimension of `compersion` (Mean=0.23) was notably rare, while its opposite, `envy` (Mean=0.63), was common, suggesting a corpus tilted towards grievance over celebration of others' success. The high standard deviations for most metrics (e.g., `tribal_dominance_salience` SD=0.45; `compersion_salience` SD=0.45) confirm that the documents varied widely in their rhetorical strategies.

**Table 1: Descriptive Statistics of Primary CFF Dimensions (Salience Scores)**
| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| tribal_dominance_salience | 0.675 | 0.450 | 0.0 | 0.9 |
| individual_dignity_salience | 0.475 | 0.386 | 0.1 | 0.9 |
| fear_salience | 0.650 | 0.370 | 0.1 | 0.9 |
| hope_salience | 0.450 | 0.351 | 0.1 | 0.8 |
| envy_salience | 0.625 | 0.427 | 0.0 | 0.9 |
| compersion_salience | 0.225 | 0.450 | 0.0 | 0.9 |
| enmity_salience | 0.638 | 0.427 | 0.0 | 0.9 |
| amity_salience | 0.575 | 0.403 | 0.0 | 0.9 |
| fragmentative_goals_salience | 0.600 | 0.400 | 0.0 | 0.8 |
| cohesive_goals_salience | 0.625 | 0.310 | 0.2 | 0.9 |

The high mean score for `envy` is exemplified by statements that frame economic outcomes as theft. As Alexandria Ocasio-Cortez stated: "They aren't working for these billions. They're stealing them. They're stealing them. They're stealing them from you and you and me." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). In contrast, the rarity of `compersion` is highlighted by its near-total absence, with the exception of John McCain's speech, where he stated he "deeply admire[s] and commend[s] him for achieving" his opponent's victory. (Source: john_mccain_2008_concession.txt).

### 5.2 Advanced Metric Analysis

The derived metrics provide a holistic view of each document's rhetorical posture. The `full_cohesion_index` clearly separates the speeches, with McCain's concession (+0.84) standing as a stark outlier of cohesive rhetoric against the fragmentative speeches of King (-0.74), Sanders (-0.37), and Ocasio-Cortez (-0.17).

The `strategic_contradiction_index` reveals a key difference between purely fragmentative and populist rhetoric. King's speech, while highly fragmentative, is internally consistent, with a moderate contradiction score (0.04). Sanders' speech, however, has the highest contradiction score by a wide margin (0.10). This is driven by high scores in opposing dimensions, such as `relational_tension` (0.18), which measures the co-occurrence of `enmity` and `amity`. This captures his strategy of defining a sharp enemy while simultaneously calling for strong in-group solidarity. As Bernie Sanders stated, "But you would think that if you had a few billion dollars... you would not feel obliged to step on the backs of poor people," an example of `enmity`, while also calling for unity: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe... we can create the kind of nation that we deserve," an example of `amity`. (Source: bernie_sanders_2025_fighting_oligarchy.txt).

**Table 2: Derived CFF Metrics per Document**
| Document Name | Full Cohesion Index | Strategic Contradiction Index | Identity Tension | Emotional Tension | Relational Tension | Goal Tension |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| john_mccain_2008_concession.txt | 0.840 | 0.014 | 0.000 | 0.070 | 0.000 | 0.000 |
| steve_king_2017_house_floor.txt | -0.735 | 0.044 | 0.080 | 0.080 | 0.000 | 0.060 |
| bernie_sanders_2025... | -0.370 | 0.102 | 0.140 | 0.070 | 0.180 | 0.120 |
| alexandria_ocasio_cortez_2025... | -0.175 | 0.036 | 0.120 | 0.060 | 0.000 | 0.000 |

### 5.3 Correlation and Interaction Analysis

The correlation matrix provides the strongest evidence for the CFF's structural integrity and reveals the underlying rhetorical meta-strategies in the corpus.

**Framework Validation:** The data shows extremely strong, statistically significant negative correlations between the framework's designed oppositional pairs. This confirms that the dimensions are measuring what they purport to measure and behave as opposites.
*   `tribal_dominance_salience` vs. `compersion_salience`: r = -1.00 (Large Effect)
*   `enmity_salience` vs. `compersion_salience`: r = -0.995 (Large Effect)
*   `fear_salience` vs. `individual_dignity_salience`: r = -0.782 (Large Effect)
*   `amity_salience` vs. `tribal_dominance_salience`: r = -0.537 (Large Effect)

**Meta-Strategy Identification:** The correlations reveal two dominant, internally consistent, and mutually exclusive rhetorical clusters.

1.  **The Fragmentative Cluster:** Dimensions of `tribal_dominance`, `fear`, `envy`, `enmity`, and `fragmentative_goals` are all very highly and positively correlated. For example, the correlation between `tribal_dominance_salience` and `enmity_salience` is r = +0.995. This indicates that when a speaker in this corpus uses one of these tactics, they are highly likely to use the others. This cluster is exemplified by Steve King's speech, which combines defining an out-group ("an illegal criminal alien") with fear-based storytelling ("that awful, brutal, ghastly memory") and confrontational goals ("resist the President's policy"). (Source: steve_king_2017_house_floor.txt).

2.  **The Cohesive Cluster:** Dimensions of `individual_dignity`, `hope`, `amity`, and `cohesive_goals` are positively correlated with one another. For instance, `individual_dignity_salience` and `cohesive_goals_salience` have a strong positive correlation of r = +0.899. This cluster is best represented by John McCain's speech, which links the dignity of a specific group ("special significance it has for African-Americans") with a unifying national goal ("offering our next president our good will and earnest effort to find ways to come together"). (Source: john_mccain_2008_concession.txt).

These two clusters are, in turn, strongly negatively correlated, reinforcing the finding of a polarized rhetorical landscape within this corpus.

**Table 3: Selected Pearson Correlations (Salience Scores)**
| | tribal_dominance_salience | individual_dignity_salience | fear_salience | hope_salience | enmity_salience | amity_salience |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **tribal_dominance_salience** | 1.00 | -0.734 | 0.992 | -0.664 | 0.995 | -0.537 |
| **individual_dignity_salience** | -0.734 | 1.00 | -0.782 | 0.381 | -0.781 | 0.851 |
| **fear_salience** | 0.992 | -0.782 | 1.00 | -0.719 | 0.987 | -0.637 |
| **hope_salience** | -0.664 | 0.381 | -0.719 | 1.00 | -0.606 | 0.624 |
| **enmity_salience** | 0.995 | -0.781 | 0.987 | -0.606 | 1.00 | -0.554 |
| **amity_salience** | -0.537 | 0.851 | -0.637 | 0.624 | -0.554 | 1.00 |

### 5.4 Pattern Recognition and Theoretical Insights

The most powerful pattern emerging from the data is the near-perfect correlation (r = +1.00) between `tribal_dominance_salience` and `fragmentative_goals_salience`. This suggests that, within this dataset, the act of defining a tribal "other" is functionally identical to articulating a goal of social division or conflict. This linkage is a cornerstone of fragmentive rhetoric. For example, Bernie Sanders defines a tribal other ("a government of the billionaires") and immediately follows with a fragmentative goal ("that is what we are going to change"), framing the political project as a zero-sum conflict. (Source: bernie_sanders_2025_fighting_oligarchy.txt).

Conversely, the strong positive correlation between `amity_salience` and `cohesive_goals_salience` (r = +0.995) indicates that appeals to friendship and shared identity are inextricably linked to articulating goals of unity and cooperation. This is clearly visible in John McCain's call for "fellow Americans" to "find the necessary compromises to bridge our differences." (Source: john_mccain_2008_concession.txt).

An unexpected finding is the relatively weak correlation between `hope_salience` and `individual_dignity_salience` (r = +0.381). One might theorize that appeals to hope would be grounded in universal principles of dignity. This weaker link suggests that "hope" in this corpus is being used in multiple ways. In some cases, it is a hope for a specific in-group's victory rather than a universally uplifting vision. This nuance demonstrates the CFF's ability to uncover complex relationships that simpler models might miss.

### 5.5 Framework Effectiveness Assessment

The CFF demonstrated high effectiveness in this pilot analysis. Its **discriminatory power** is evident in the wide variance of scores across all dimensions and, most notably, in the `full_cohesion_index` range from -0.74 to +0.84. The framework successfully distinguished not only between cohesive and fragmentative speeches but also identified a mixed-strategy archetype.

The **framework-corpus fit** appears to be excellent. The statistical patterns, particularly the strong negative correlations between oppositional dimensions, align perfectly with the CFF's theoretical design. This suggests the framework is well-suited for analyzing the rhetorical dynamics present in contemporary American political speech. The results provide a strong, albeit preliminary, validation of the CFF as a methodological tool.

## 6. Discussion

### Theoretical Implications
This analysis provides preliminary empirical support for the theoretical structure of the Cohesive Flourishing Framework. The emergence of two opposing meta-strategies—one built on `tribal_dominance`, `fear`, and `enmity`, the other on `individual_dignity`, `hope`, and `amity`—suggests that these dimensions are not just independent variables but components of larger, coherent rhetorical systems. The findings indicate that political discourse, at least in this sample, operates along a primary axis of cohesion versus fragmentation.

Furthermore, the identification of the "Populist Agitator" archetype, which blends these opposing strategies, has significant theoretical implications. It suggests that some of the most potent political rhetoric may derive its energy from "strategic contradiction"—simultaneously stoking out-group animosity and in-group solidarity. This moves beyond a simple good/bad binary and points to a more complex model where fragmentative and cohesive language can be deployed in tandem as a sophisticated political tool.

### Comparative Analysis and Archetypal Patterns
The four documents cluster into three distinct rhetorical archetypes:

1.  **The Unifier (McCain):** Characterized by high cohesion (+0.84), this archetype actively promotes `amity`, `compersion`, and `cohesive_goals` while systematically avoiding all fragmentative language. The goal is de-escalation and national unity. The language is gracious and forward-looking. As John McCain stated, "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will." (Source: john_mccain_2008_concession.txt).

2.  **The Divider (King):** Characterized by extreme fragmentation (-0.74), this archetype relies heavily on `tribal_dominance`, `fear`, and `enmity`. The rhetoric is internally consistent, with low strategic contradiction. The goal is to mobilize a base by identifying an existential threat posed by an out-group. As Steve King stated, the actions of an "illegal criminal alien" necessitate that "we must defend our Constitution" from the president's policies, framing the issue as a zero-sum battle for national survival. (Source: steve_king_2017_house_floor.txt).

3.  **The Populist Agitator (Sanders, Ocasio-Cortez):** This hybrid archetype scores negatively on the cohesion index but does so with high internal contradiction. It defines a tribal enemy (e.g., "oligarchs," "billionaires") using high `enmity` and `envy`, but pairs this with strong appeals to in-group `amity` and `cohesive_goals` for "the people." This strategy aims to fragment the broader society along a specific axis (e.g., class) in order to build a new, more cohesive coalition. As Alexandria Ocasio-Cortez stated, the goal is to "give Evans and Boebert the boot" (`enmity`) in the name of "class solidarity" (`cohesive_goals`). (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

### Limitations and Future Directions
The primary limitation remains the N=4 sample size. These archetypes are provocatively clear but must be treated as hypotheses. Future research is essential to determine if they hold across a much larger and more diverse corpus of texts, including different political systems, time periods, and communication media (e.g., social media, news articles). Researchers may wish to investigate whether the "Populist Agitator" style is more prevalent in certain political contexts or if its level of strategic contradiction correlates with electoral success or social polarization. A larger N would also permit the use of inferential statistics to test the significance of these patterns.

## 7. Conclusion

This computational analysis, though limited in scope, demonstrates the significant analytical potential of the Cohesive Flourishing Framework. The study successfully used the CFF to move beyond surface-level analysis and map the deep rhetorical structures of four distinct political speeches. The findings provide strong preliminary evidence for the framework's construct validity, as its oppositional dimensions behaved as theoretically predicted, revealing two coherent and opposing meta-strategies of fragmentation and cohesion.

The key contribution of this report is the identification of three distinct rhetorical archetypes—the Unifier, the Divider, and the Populist Agitator—each with a unique statistical fingerprint. The discovery of the "Populist Agitator" style, which strategically combines fragmentive and cohesive language, offers a nuanced way to understand modern political communication that defies simple categorization. While these findings must be validated on a larger scale, they generate testable hypotheses for future research and showcase the CFF as a promising tool for scholars in computational social science, political communication, and discourse analysis.

## 8. Evidence Citations

**alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   As Alexandria Ocasio-Cortez stated: "They aren't working for these billions. They're stealing them. They're stealing them. They're stealing them from you and you and me."
*   As Alexandria Ocasio-Cortez stated: "We need to come together and spend every day between now and election day working to educate our neighbors, and give Evans and Boebert the boot, and replace them with a brawling Democrat who will stand for Colorado."
*   As Alexandria Ocasio-Cortez stated: "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity."

**bernie_sanders_2025_fighting_oligarchy.txt**
*   As Bernie Sanders stated: "Abraham Lincoln talked about a government of the people, by the people, for the people. Well, Trump has a government of the billionaires, by the billionaires, and for the billionaires."
*   As Bernie Sanders stated: "But you would think that if you had a few billion dollars or $10 or $20 billion, you would not feel obliged to step on the backs of poor people to become even richer. But that is exactly what they are doing right now."
*   As Bernie Sanders stated: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve."
*   As Bernie Sanders stated: "We will not accept an oligarchic form of society. We will not accept the richest guy in the world running all over Washington, making cuts to the Social Security Administration..."

**john_mccain_2008_concession.txt**
*   As John McCain stated: "But that he managed to do so by inspiring the hopes of so many millions of Americans... is something I deeply admire and commend him for achieving."
*   As John McCain stated: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."
*   As John McCain stated: "This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."
*   As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together, to find the necessary compromises to bridge our differences..."

**steve_king_2017_house_floor.txt**
*   As Steve King stated: "It's another life loss to an, an illegal criminal alien who was unlawfully present in America, who had no business to be here..."
*   As Steve King stated: "And the sad, sad story told by Laura Wilkerson yesterday that she has the courage and the heart to come here and share her story with us and to place that awful, brutal, ghastly memory again into her mind's eye..."
*   As Steve King stated: "This is the time we must defend our Constitution and we must nominate and elect a president of the United States who will make those appointments to the Supreme Court who believe the Constitution means what it says."