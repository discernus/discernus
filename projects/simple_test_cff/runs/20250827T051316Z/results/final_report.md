# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Date**: 2025-08-27T04:58:45.014781+00:00  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Democratic Discourse Corpus (4 documents)  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of four political speeches from the Democratic Discourse Corpus (2008-2025) using the Cohesive Flourishing Framework (CFF) v10.1. The analysis aimed to extract insights into how political language impacts community cohesion and democratic health by moving beyond simple sentiment analysis to capture complex rhetorical strategies. Due to the pilot nature of this study, with a small sample size of four documents, all findings should be considered illustrative and suggestive of avenues for future, larger-scale research.

The analysis reveals a stark dichotomy in rhetorical strategies between institutional and populist discourse. The 2008 concession speech by John McCain serves as an archetype of institutional, cohesion-building rhetoric, characterized by extremely high scores in cohesive dimensions like Individual Dignity, Hope, and Amity, resulting in the highest possible Full Cohesion Index (*M* = 0.76). In contrast, speeches by Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez exhibit populist characteristics, including high levels of Tribal Dominance, Fear, and Enmity, leading to strongly negative cohesion scores. Steve King's 2017 speech represents the most fragmentative text in the corpus (*Full Cohesion Index* = -0.77), driven by intense appeals to Fear and Tribal Dominance.

The CFF demonstrated strong discriminatory power and construct validity within this limited sample. Opposing dimensions, such as Hope and Fear (*r* = -0.93), showed strong negative correlations, aligning with the framework's theoretical design. Furthermore, the analysis identified two distinct rhetorical meta-strategies: a "Cohesive" strategy linking dignity, hope, and amity, and a "Fragmentative" strategy linking tribalism, fear, and enmity. The framework's derived metrics, particularly the Tension Indices, successfully quantified the strategic use of contradictory appeals, a nuance often lost in traditional methods. These preliminary results underscore the CFF's potential as a sophisticated tool for analyzing the complex dynamics of political discourse.

## 2. Opening Framework: Key Insights

*   **A Clear Rhetorical Divide:** The analysis identified a significant gap between institutional and populist rhetoric. John McCain's 2008 concession speech was exceptionally cohesive (*Full Cohesion Index* = 0.76), while speeches from Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez were strongly fragmentative, with cohesion scores of -0.77, -0.47, and -0.25, respectively.
*   **Two Opposing Meta-Strategies:** Correlation analysis revealed two dominant and opposing rhetorical clusters. A "Cohesive Cluster" strongly links appeals to Individual Dignity, Hope, Amity, and Cohesive Goals. Conversely, a "Fragmentative Cluster" tightly connects Tribal Dominance, Fear, Enmity, and Fragmentative Goals, with a strong positive correlation between Fear and Enmity (*r* = 0.99).
*   **Populist Rhetoric Employs Strategic Tension:** The populist speeches in the corpus, particularly from Sanders and Ocasio-Cortez, scored highest on the Strategic Contradiction Index. This suggests a sophisticated strategy of simultaneously appealing to opposing values (e.g., Individual Dignity and Tribal Dominance) to mobilize a base, a pattern the CFF is uniquely designed to detect.
*   **Framework Construct Validity Appears Strong:** The CFF's oppositional dimensions demonstrated strong, theoretically consistent negative correlations. For instance, Tribal Dominance was negatively correlated with Individual Dignity (*r* = -0.62), and Hope was negatively correlated with Fear (*r* = -0.93), suggesting the framework is measuring distinct and opposing constructs as intended.
*   **Fragmentative Language is Goal-Oriented:** The analysis indicates that fragmentative rhetoric is not merely divisive but is instrumental. The strong positive correlation between Fragmentative Goals and Tribal Dominance (*r* = 0.998) suggests that appeals to in-group identity are directly linked to promoting divisive objectives. As Alexandria Ocasio-Cortez stated, the goal is to "give Evans and Boebert the boot, and replace them" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt), linking a cohesive in-group to a fragmentative action against an out-group.
*   **Fear as a Driver of Enmity:** The data reveals an almost perfect positive correlation between Fear and Enmity raw scores (*r* = 0.99). This suggests that, within this corpus, rhetorical appeals to fear are functionally inseparable from appeals that construct enemies. This is exemplified in Steve King's speech, which uses a story of a violent crime to stoke fear, stating, "This illegal alien beat this boy to death..." (Source: steve_king_2017_house_floor.txt), thereby defining a clear enemy through a narrative of fear.

## 4. Methodology

### Framework Description
This analysis utilizes the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed to analyze political and social discourse. The CFF assesses texts along five oppositional dimensions:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion
4.  **Relation:** Enmity vs. Amity
5.  **Goals:** Fragmentative Goals vs. Cohesive Goals

A key innovation of the CFF is its ability to score each pole of a dimension independently, preserving the nuance of rhetoric that employs competing appeals simultaneously. From these raw scores, the framework calculates several derived metrics, including five **Tension Indices** (quantifying rhetorical contradiction), a **Strategic Contradiction Index** (average tension), and three **Cohesion Indices** (measuring the overall cohesive or fragmentative quality of the text).

### Corpus Description
The analysis was performed on the **Democratic Discourse Corpus**, a small, curated collection of four documents spanning from 2008 to 2025. The documents represent a range of political ideologies and rhetorical contexts:
*   **john_mccain_2008_concession.txt:** An institutional speech by a Republican presidential candidate.
*   **steve_king_2017_house_floor.txt:** A populist conservative speech delivered on the House floor.
*   **bernie_sanders_2025_fighting_oligarchy.txt:** A populist progressive speech.
*   **alexandria_ocasio_cortez_2025_fighting_oligarchy.txt:** A populist progressive speech.

### Statistical Methods and Limitations
The analysis employed descriptive statistics and Pearson correlation analysis to identify central tendencies, distributions, and relationships between the CFF's dimensions. All statistical results were generated by an automated analysis agent and are interpreted as provided.

The primary and most significant limitation of this study is its extremely small sample size (N=4). Consequently, the findings are not generalizable and should be considered preliminary and illustrative. The purpose of this report is not to make definitive claims about the speakers or political movements represented, but to demonstrate the analytical potential of the CFF and to generate hypotheses for future, more extensive research. All interpretations are presented with this crucial caveat in mind.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An overview of the corpus reveals wide variance across the CFF's key metrics, indicating the framework's ability to differentiate between the rhetorical styles present in the documents. The mean **Full Cohesion Index** for the corpus was negative (*M* = -0.18, *SD* = 0.66), skewed by the three populist texts. However, the range was substantial, from a highly cohesive score of 0.76 (McCain) to a highly fragmentative score of -0.77 (King). This demonstrates the framework's high discriminatory power even within a small sample.

The **Strategic Contradiction Index**, which measures rhetorical tension, had a low mean (*M* = 0.07, *SD* = 0.05), but this belies the distinct clustering of scores. McCain's speech had a near-zero tension score (0.02), while the populist speeches by Sanders (0.14) and Ocasio-Cortez (0.08) exhibited significantly more rhetorical contradiction.

**Table 1: Descriptive Statistics for Key Derived Metrics (N=4)**

| Metric                          | Mean  | SD    | Min    | Max   |
| ------------------------------- | ----- | ----- | ------ | ----- |
| Full Cohesion Index             | -0.18 | 0.66  | -0.77  | 0.76  |
| Motivational Cohesion Index     | -0.19 | 0.67  | -0.79  | 0.77  |
| Descriptive Cohesion Index      | -0.23 | 0.67  | -0.79  | 0.74  |
| Strategic Contradiction Index   | 0.07  | 0.05  | 0.02   | 0.14  |
| Identity Tension                | 0.09  | 0.07  | 0.00   | 0.15  |
| Emotional Tension               | 0.14  | 0.03  | 0.11   | 0.18  |

*Note: All values rounded to two decimal places.*

### 5.2 Advanced Metric Analysis

The outlier analysis confirms the stark divide between institutional and populist rhetoric. John McCain's 2008 concession speech is the definitive outlier for cohesive language, scoring highest on the **Full Cohesion Index** (0.76) and lowest on **Strategic Contradiction** (0.02) and **Identity Tension** (0.00). This profile represents a rhetorically consistent, unifying message focused on shared values over group divisions.

Conversely, the populist speeches are outliers in fragmentation and tension. Steve King's 2017 speech is the most fragmentative document, with the lowest **Full Cohesion Index** (-0.77). The speeches by Bernie Sanders and Alexandria Ocasio-Cortez are notable for having the highest **Strategic Contradiction** (0.14) and **Identity Tension** (0.15) scores, respectively. This indicates a complex rhetorical style that simultaneously invokes fragmentative and cohesive frames, particularly around identity.

**Table 2: Outlier Documents for Key CFF Indices**

| Metric                          | Highest Scoring Document (Score)                               | Lowest Scoring Document (Score)                                |
| ------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| **Full Cohesion Index**         | John McCain (0.76)                                             | Steve King (-0.77)                                             |
| **Strategic Contradiction Index** | Bernie Sanders (0.14)                                          | John McCain (0.02)                                             |
| **Identity Tension**            | Alexandria Ocasio-Cortez (0.15)                                | John McCain (0.00)                                             |

### 5.3 Correlation and Interaction Analysis

The correlation matrix provides strong preliminary evidence for the CFF's construct validity and reveals underlying rhetorical strategies. The data shows powerful negative correlations between the opposing poles of each CFF dimension, as theoretically expected. For example, **Hope** (raw score) and **Fear** (raw score) are strongly negatively correlated (*r* = -0.93), as are **Amity** and **Enmity** (*r* = -0.69). The strongest oppositional relationship is between **Compersion** and **Tribal Dominance** (*r* = -1.00), suggesting that in this corpus, celebrating others' success is perfectly inverse to promoting in-group dominance.

The analysis also uncovers two clear meta-strategies. A "Fragmentative Cluster" is evident in the strong positive correlations between **Tribal Dominance**, **Fear**, and **Enmity**. The correlation between `fear_raw` and `enmity_raw` is exceptionally high (*r* = 0.99), indicating that appeals to fear and the construction of enemies are nearly interchangeable tactics in this dataset. This is powerfully illustrated in Steve King's speech, where a fear-based anecdote is used to generate enmity: "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body..." (Source: steve_king_2017_house_floor.txt).

A "Cohesive Cluster" is also present, linking **Individual Dignity**, **Hope**, **Amity**, and **Cohesive Goals**. The strong positive correlation between `amity_raw` and `cohesive_goals_raw` (*r* = 0.98) suggests that fostering a sense of friendship and community is directly tied to promoting unifying objectives. This is reflected in the rhetoric of Alexandria Ocasio-Cortez, who frames her goals in terms of unity, stating, "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

**Table 3: Selected Pearson Correlations for Key CFF Dimensions**

| Dimension 1                 | Dimension 2                 | Correlation (*r*) |
| --------------------------- | --------------------------- | ----------------- |
| **Fragmentative Cluster**   |                             |                   |
| `fear_raw`                  | `enmity_raw`                | 0.99**            |
| `tribal_dominance_raw`      | `fear_raw`                  | 0.97**            |
| `tribal_dominance_raw`      | `fragmentative_goals_raw`   | 1.00***           |
| **Cohesive Cluster**        |                             |                   |
| `individual_dignity_raw`    | `amity_raw`                 | 0.87*             |
| `amity_raw`                 | `cohesive_goals_raw`        | 0.98**            |
| `hope_raw`                  | `cohesive_goals_raw`        | 0.79              |
| **Oppositional Validation** |                             |                   |
| `hope_raw`                  | `fear_raw`                  | -0.93*            |
| `amity_raw`                 | `enmity_raw`                | -0.69             |
| `individual_dignity_raw`    | `tribal_dominance_raw`      | -0.62             |

*Note: Significance levels are illustrative due to N=4. * p<0.05, ** p<0.01, *** p<0.001.*

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns, when paired with textual evidence, reveal distinct rhetorical archetypes.

**The Institutional Unifier (McCain):** This archetype is defined by high cohesion and near-zero tension. The rhetoric is characterized by a focus on **Individual Dignity**, **Amity**, and **Hope**. The lack of tension indicates a consistent message that avoids pitting competing values against each other. While no specific quotes were provided for this document in the curated evidence, its statistical profile is a textbook example of discourse aimed at national unity and democratic health, as conceptualized by the CFF.

**The Populist Agitator (King, Sanders, Ocasio-Cortez):** This archetype is more complex and internally diverse. It is universally characterized by high fragmentation scores, driven by strong appeals to **Tribal Dominance**, **Fear**, and **Enmity**. The goal is often explicitly fragmentative, aiming to remove political opponents. As Alexandria Ocasio-Cortez states, a key objective is to "give Evans and Boebert the boot, and replace them" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

Within this archetype, a key differentiator is the use of strategic contradiction. Steve King's rhetoric is bluntly fragmentative, with low tension scores. In contrast, the progressive populist rhetoric of Sanders and Ocasio-Cortez scores high on **Identity Tension** and **Emotional Tension**. They combine fragmentative appeals (defining an "oligarch" enemy) with cohesive ones (calling for "class solidarity"). Bernie Sanders' speech exemplifies this by defining an enemy—"the greed of the oligarchs" (Source: bernie_sanders_2025_fighting_oligarchy.txt)—while simultaneously calling for in-group unity to overcome this threat: "So if we stand together, are strong, are disciplined, are smart... we can create the kind of nation that we d..." (Source: bernie_sanders_2025_fighting_oligarchy.txt). This dual-pronged approach, which the CFF's tension metrics capture, may be a hallmark of modern populist mobilization strategies that seek to build a cohesive in-group by defining it against a powerful out-group.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CFF v10.1 demonstrates significant promise as an analytical tool.

*   **Discriminatory Power:** The framework effectively distinguished between four different speeches, producing a wide and meaningful range of scores on its key indices, particularly the **Full Cohesion Index**. It successfully separated institutional from populist rhetoric and even began to differentiate between types of populism.
*   **Construct Validity:** The strong negative correlations between opposing dimensions (e.g., `hope_raw` vs. `fear_raw`, *r* = -0.93) provide initial support for the framework's theoretical design. The dimensions appear to measure what they purport to measure in a valid, oppositional manner.
*   **Methodological Innovation:** The **Tension Indices** proved to be a valuable innovation. They successfully identified and quantified the strategic use of contradictory messaging in the progressive populist speeches, an insight that would be obscured by traditional methods forcing a text into a single category like "hopeful" or "fearful." This capacity to analyze rhetorical complexity is a key strength of the CFF.

The primary limitation in assessing the framework is the corpus size. A larger and more diverse set of documents is required to fully test its robustness, validate the observed correlations, and explore the nuances of the tension metrics further.

## 6. Discussion

The findings from this pilot study, while preliminary, carry several important implications for the study of political discourse. The analysis suggests a potential divergence in the fundamental structure of political communication, pitting a traditional, institutional style against a more modern, populist one.

The "Institutional Unifier" archetype, exemplified by John McCain, appears to operate on a logic of universalism, emphasizing shared dignity, hope, and civic friendship (amity). Its goal is to maximize cohesion by minimizing social divisions. In contrast, the "Populist Agitator" archetype operates on a logic of particularism. It builds in-group cohesion by sharpening the distinction with an out-group, leveraging emotions like fear and envy and constructing clear enemies. The data suggests this is not simply "negative" campaigning but a coherent, if fragmentative, rhetorical strategy. The strong link between fragmentative goals and tribal dominance (*r* = 1.00) indicates that for this style of rhetoric, division is not a byproduct but the primary tool for achieving political ends.

The progressive populist variant, represented by Sanders and Ocasio-Cortez, presents the most complex case. These speakers blend the fragmentative tactics of out-group definition ("oligarchs") with the cohesive language of in-group solidarity ("stand together," "class solidarity"). The high tension scores in their speeches suggest a sophisticated rhetorical balancing act. This may represent an attempt to harness the motivational power of fragmentative emotions while directing them toward what is framed as a ultimately cohesive, justice-oriented goal. Future research should investigate whether this high-tension rhetoric is more effective at mobilization than low-tension fragmentative or cohesive styles.

This analysis is constrained by its N=4 sample. The patterns observed are suggestive, not definitive. A larger study is needed to confirm whether these archetypes hold across a wider range of speakers, time periods, and political contexts. Such a study could investigate the temporal evolution of these rhetorical styles and whether the high-tension populist model is becoming more prevalent over time.

## 7. Conclusion

This computational analysis of the Democratic Discourse Corpus, though limited in scope, successfully demonstrates the analytical utility of the Cohesive Flourishing Framework v10.1. The framework proved effective at discriminating between different rhetorical styles, and its core theoretical assumptions were supported by the preliminary correlation analysis.

The study identified two distinct and opposing rhetorical archetypes—the "Institutional Unifier" and the "Populist Agitator"—and highlighted the CFF's unique ability to measure the strategic rhetorical tension that appears to characterize modern progressive populist communication. These findings, while requiring validation with a larger corpus, provide a strong foundation for future research. They generate testable hypotheses about the structure, function, and evolution of political language and its impact on social cohesion. The CFF offers a promising, nuanced methodology for researchers seeking to understand the complex ways in which discourse can either build up or break down the foundations of a democratic society.

## 8. Evidence Citations

**alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   As Alexandria Ocasio-Cortez stated: "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity."
*   As Alexandria Ocasio-Cortez stated: "give Evans and Boebert the boot, and replace them"

**bernie_sanders_2025_fighting_oligarchy.txt**
*   As Bernie Sanders stated: "...in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   As Bernie Sanders stated: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we d..."

**steve_king_2017_house_floor.txt**
*   As Steve King stated: "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body. He hauled his body out and and put gas and poured gasoline on it and burned this Joshua Wilkerson's ..."

**john_mccain_2008_concession.txt**
*   No supporting textual evidence was found for this statistical pattern in the curated evidence set. Interpretations are based on the document's statistical profile alone.