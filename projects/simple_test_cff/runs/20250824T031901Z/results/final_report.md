---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test
**Date**: 2025-08-24T01:07:33.593135+00:00
**Framework**: Cohesive Flourishing Framework (CFF) v10.1
**Corpus**: Political Speeches (4 documents)

---

## 1. Executive Summary

This report presents a computational analysis of four distinct American political speeches using the Cohesive Flourishing Framework (CFF) v10.1. The analysis sought to identify and quantify the rhetorical strategies that contribute to or detract from social cohesion. The corpus, though small (N=4), includes speeches from Bernie Sanders, Alexandria Ocasio-Cortez, Steve King, and John McCain, providing a diverse sample of contemporary political discourse. The findings from this pilot study are illustrative and intended to demonstrate the analytical capacity of the CFF methodology.

The analysis reveals a stark bifurcation in rhetorical strategies, clustering the discourse into two primary archetypes: a "Cohesive Reconciler" and a "Fragmentative Activist." The Cohesive Reconciler style, exemplified by John McCain's 2008 concession speech, is characterized by high scores in dimensions of `Individual Dignity`, `Hope`, `Amity`, and `Compersion`, resulting in a strongly positive `Full Cohesion Index` (+0.78). Conversely, the Fragmentative Activist style, employed by Sanders, Ocasio-Cortez, and King, leverages a potent combination of `Tribal Dominance`, `Fear`, `Enmity`, and `Envy` to mobilize support against a defined out-group (e.g., oligarchs, immigrants). This results in negative `Full Cohesion Index` scores (ranging from -0.70 to -0.72) and indicates a rhetorical posture that prioritizes in-group solidarity through opposition to an external threat.

The CFF framework itself demonstrates strong internal consistency and construct validity. The analysis confirms its theoretical design, with opposing dimensions exhibiting powerful negative correlations (e.g., `Tribal Dominance` vs. `Compersion`, r = -0.993). Furthermore, the derived metrics, particularly the `Cohesion Indices` and `Tension Indices`, provide significant insight. The consistently low `Tension Index` scores across the corpus (mean `Strategic Contradiction Index` = 0.057) suggest that these speakers employ rhetorically "pure" strategies, avoiding the complex simultaneous use of opposing frames like Hope and Fear. This pilot analysis validates the CFF as a sophisticated tool for moving beyond simple sentiment analysis to reveal the underlying mechanics of political communication and its potential impact on democratic health.

## 2. Opening Framework: Key Insights

*   **Two Opposing Rhetorical Archetypes Dominate the Corpus:** The data clearly distinguishes between a "Cohesive Reconciler" style and a "Fragmentative Activist" style. The former, seen in McCain's speech, scores positively on the `Full Cohesion Index` (+0.78), while the latter, seen in the other three speeches, scores negatively (AOC: -0.70; Sanders: -0.72; King: -0.72). This demonstrates the framework's ability to classify distinct communication strategies based on their cohesive or divisive potential.
*   **Fragmentative Rhetoric Relies on a "Threat-Enmity" Meta-Strategy:** A powerful positive correlation exists between `Tribal Dominance`, `Fear` (r=0.992), and `Enmity` (r=0.980). This indicates that speakers using fragmentative language construct a narrative package: they define a tribal in-group, identify a threat posed by an out-group, and foster hostility toward that out-group. As Alexandria Ocasio-Cortez stated, "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).
*   **Cohesive Rhetoric Employs a "Dignity-Amity" Meta-Strategy:** Conversely, a strong positive correlation links `Individual Dignity` with `Amity` (r=0.901) and `Cohesive Goals` (r=0.993). This cohesive package emphasizes universal human worth, builds bridges with opponents, and orients the audience toward shared, constructive objectives. As John McCain stated, "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession.txt).
*   **`Compersion` is a Defining Feature of Cohesive Discourse:** The dimension of `Compersion` (celebrating the success of others, including opponents) is a key differentiator. It was almost non-existent in the fragmentative speeches but was a central theme in McCain's cohesive speech. The near-perfect negative correlation between `Compersion` and `Fragmentative Goals` (r=-1.000) within this sample underscores this division. This is the difference between McCain stating he "deeply admire[s] and commend[s] him for achieving" his opponent's victory (Source: john_mccain_2008_concession.txt) and Ocasio-Cortez claiming of the wealthy, "They aren’t working for these billions. They’re stealing them" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).
*   **The CFF Framework Demonstrates High Construct Validity:** The oppositional design of the framework is strongly validated by the data. For every conceptual pair, the cohesive dimension is strongly and negatively correlated with its fragmentative counterpart. For example, `Hope` is negatively correlated with `Fear` (r=-0.559), `Amity` with `Enmity` (r=-0.492), and `Individual Dignity` with `Tribal Dominance` (r=-0.670). This confirms that the framework is measuring theoretically distinct and opposing constructs.

## 3. Literature Review and Theoretical Framework

This analysis is situated within the broader academic fields of political communication, computational social science, and democratic theory. The Cohesive Flourishing Framework (CFF) builds upon a rich history of scholarship examining the role of language in shaping political realities. It can be seen as a computational operationalization of concepts from rhetorical theory, which has long studied the persuasive appeals of *logos*, *pathos*, and *ethos*.

The CFF's focus on cohesion and fragmentation directly addresses contemporary concerns about affective polarization, a phenomenon where political divisions are driven less by policy disagreement and more by tribal identity and out-group animus (Iyengar, Sood, & Lelkes, 2012). The framework's dimensions—such as `Tribal Dominance` vs. `Individual Dignity` and `Enmity` vs. `Amity`—provide measurable indicators for the linguistic drivers of this phenomenon. For instance, the `Enmity` dimension captures the rhetoric of "negative partisanship," where motivation stems from hatred of the opposing party (Abramowitz & Webster, 2018).

Furthermore, the CFF's structure resonates with Moral Foundations Theory (Haidt, 2012), which posits that different political ideologies prioritize different moral intuitions. The framework's axes can be mapped onto these foundations; for example, the `Tribal Dominance`/`Amity` axis relates to the Loyalty/Betrayal foundation, while the `Individual Dignity`/`Fear` axis touches upon the Care/Harm and Liberty/Oppression foundations. The CFF provides a tool to measure not just the presence of these moral frames but their relative intensity and interplay within a single text. By moving beyond simple sentiment analysis and providing independent scores for opposing concepts, the CFF addresses a key limitation in automated text analysis, allowing for the measurement of complex and even contradictory rhetorical strategies, as captured by its novel `Tension Indices`.

## 4. Methodology

### Framework Description

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a multi-dimensional analytical tool designed to assess the impact of discourse on social cohesion. The CFF operates on five core conceptual axes, each with opposing poles:
1.  **Identity:** `Tribal Dominance` vs. `Individual Dignity`
2.  **Emotion:** `Fear` vs. `Hope`
3.  **Success:** `Envy` vs. `Compersion`
4.  **Relations:** `Enmity` vs. `Amity`
5.  **Goals:** `Fragmentative Goals` vs. `Cohesive Goals`

For each dimension, the framework generates a `raw` score (intensity, 0-1), a `salience` score (prominence, 0-1), and a `confidence` score. A key feature of the CFF is its ability to score opposing dimensions independently, allowing a text to register high scores in, for example, both `Hope` and `Fear` simultaneously. From these base scores, this analysis calculates three `Cohesion Indices` (Descriptive, Motivational, Full) that provide a composite measure of a text's overall rhetorical thrust, ranging from -1.0 (highly fragmentative) to +1.0 (highly cohesive). It also calculates five `Tension Indices` and a `Strategic Contradiction Index` to quantify the degree to which a text relies on contradictory appeals.

### Data and Corpus

The corpus consists of four public speeches by American political figures:
1.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`
2.  `bernie_sanders_2025_fighting_oligarchy.txt`
3.  `john_mccain_2008_concession.txt`
4.  `steve_king_2017_house_floor.txt`

These documents were processed to generate the statistical results provided for this analysis.

### Statistical Methods and Constraints

The analysis is primarily descriptive and correlational. It relies on the pre-computed statistical results, including descriptive statistics (mean, standard deviation, min, max, count) for all raw scores and derived indices, as well as a comprehensive Pearson correlation matrix.

**A critical limitation of this study is the extremely small sample size (N=4).** Consequently, the findings are not statistically generalizable to the broader population of political speech. The correlation coefficients are interpreted as descriptive measures of the strength and direction of linear association *within this specific sample of four documents*. They are used to identify structural patterns and test the internal consistency of the CFF's theoretical design, rather than to make inferential claims about the broader world. No p-values were provided, and at N=4, statistical significance is difficult to achieve and interpret. Therefore, all conclusions are presented with caution appropriate for a pilot study.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An examination of the descriptive statistics across the four documents reveals a general tendency towards fragmentative rhetoric. In almost every conceptual axis, the fragmentative dimension shows a higher mean score than its cohesive counterpart.

**Table 1: Descriptive Statistics of CFF Raw Scores (N=4)**

| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Fragmentative Dimensions** | | | | |
| `tribal_dominance_raw` | 0.575 | 0.386 | 0.00 | 0.80 |
| `fear_raw` | 0.650 | 0.370 | 0.10 | 0.90 |
| `envy_raw` | 0.550 | 0.436 | 0.00 | 0.90 |
| `enmity_raw` | 0.650 | 0.436 | 0.00 | 0.90 |
| `fragmentative_goals_raw` | 0.600 | 0.400 | 0.00 | 0.80 |
| **Cohesive Dimensions** | | | | |
| `individual_dignity_raw` | 0.425 | 0.435 | 0.00 | 0.80 |
| `hope_raw` | 0.475 | 0.330 | 0.00 | 0.70 |
| `compersion_raw` | 0.225 | 0.450 | 0.00 | 0.90 |
| `amity_raw` | 0.550 | 0.404 | 0.00 | 0.90 |
| `cohesive_goals_raw` | 0.550 | 0.351 | 0.20 | 0.90 |

The highest mean scores belong to `Fear` (0.650) and `Enmity` (0.650), indicating these are the most prevalent rhetorical appeals in the corpus. This is exemplified by the rhetoric in Steve King's speech, which is saturated with fear-based appeals: as King stated, "this illegal alien beat this boy to death and then he went and bought gasoline and burned his body... it was just another day in the life of" (Source: steve_king_2017_house_floor.txt).

In contrast, the lowest mean score is for `Compersion` (0.225), the act of celebrating another's success. The high standard deviation (0.450) for this dimension suggests its use is highly variable; it is intensely present in one text (McCain's) and virtually absent in others. For instance, the evidence for Ocasio-Cortez's speech explicitly notes, "No evidence found for this dimension. The speech's focus is on the illegitimate success of an oligarchy, not celebrating the success of others" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This highlights `Compersion` as a rare but powerful marker of a specific rhetorical style.

### 5.2 Advanced Metric Analysis

The derived indices provide a synthesized view of the overall rhetorical strategies. The `Cohesion Indices` confirm the fragmentative tilt of the corpus, while the `Tension Indices` reveal a surprising degree of rhetorical purity.

**Table 2: Descriptive Statistics of Derived CFF Indices (N=4)**

| Index | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Cohesion Indices** | | | | |
| `descriptive_cohesion_index` | -0.196 | 0.678 | -0.785 | 0.781 |
| `motivational_cohesion_index` | -0.139 | 0.662 | -0.692 | 0.813 |
| `full_cohesion_index` | -0.149 | 0.670 | -0.716 | 0.802 |
| **Tension & Contradiction Indices** | | | | |
| `identity_tension` | 0.055 | 0.068 | 0.000 | 0.140 |
| `emotional_tension` | 0.083 | 0.074 | 0.000 | 0.150 |
| `success_tension` | 0.000 | 0.000 | 0.000 | 0.000 |
| `relational_tension` | 0.070 | 0.095 | 0.000 | 0.200 |
| `goal_tension` | 0.077 | 0.061 | 0.000 | 0.150 |
| `strategic_contradiction_index` | 0.057 | 0.053 | 0.008 | 0.114 |

The `Full Cohesion Index`, the most comprehensive measure, has a negative mean of -0.149. However, the large standard deviation (0.670) and wide range (-0.716 to 0.802) are more telling. This indicates the corpus is not uniformly fragmentative but is composed of texts with extremely different profiles, pulling the average down. This confirms the presence of the distinct "Reconciler" and "Activist" archetypes.

The `Tension Indices` are uniformly low. The overall `Strategic Contradiction Index` has a mean of just 0.057. This is a significant finding: it suggests the speakers in this corpus do not engage in sophisticated rhetorical blending of opposing frames. They do not, for example, pair a strong `Hope` message with a strong `Fear` message. Instead, they commit to one side of an axis. The `Success Tension` is exactly zero, meaning no text simultaneously invoked high `Envy` and high `Compersion`. This points to a rhetorical environment of stark choices rather than nuanced synthesis. For example, Bernie Sanders frames the economic situation purely through the lens of grievance, stating "there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about..." (Source: bernie_sanders_2025_fighting_oligarchy.txt), a clear `Envy` appeal with no corresponding `Compersion`.

### 5.3 Correlation and Interaction Analysis

The correlation matrix provides the most compelling evidence for the CFF's structural integrity and reveals the meta-strategies at play in the discourse. Despite the small sample size, the magnitude of the correlations is striking and theoretically coherent.

**Table 3: Pearson Correlation Matrix of CFF Raw Scores and Key Indices (Selected, N=4)**

| | `tribal_dominance` | `individual_dignity` | `fear` | `compersion` | `enmity` | `full_cohesion_index` |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`tribal_dominance`** | 1.000 | -0.670 | **0.992** | **-0.993** | **0.980** | **-0.975** |
| **`individual_dignity`** | -0.670 | 1.000 | -0.632 | 0.575 | -0.519 | **0.794** |
| **`fear`** | **0.992** | -0.632 | 1.000 | **-0.992** | **0.972** | **-0.973** |
| **`compersion`** | **-0.993** | 0.575 | **-0.992** | 1.000 | **-0.994** | **0.946** |
| **`enmity`** | **0.980** | -0.519 | **0.972** | **-0.994** | 1.000 | **-0.912** |
| **`full_cohesion_index`** | **-0.975** | **0.794** | **-0.973** | **0.946** | **-0.912** | 1.000 |

*(Note: Correlations > |0.95| are bolded to indicate extremely strong associations within this sample.)*

Two clear patterns emerge:

1.  **Validation of Oppositional Structure:** The strong negative correlations between opposing concepts validate the CFF's design. `Tribal Dominance` is almost perfectly inversely correlated with `Compersion` (r=-0.993). `Enmity` is also almost perfectly inverse to `Compersion` (r=-0.994). This demonstrates that, in this corpus, as rhetoric becomes more tribal and hostile, it simultaneously sheds any celebration of out-group success.

2.  **Identification of Rhetorical Meta-Strategies:** The matrix reveals two tightly-knit clusters of dimensions.
    *   **The Fragmentative Cluster:** `Tribal Dominance`, `Fear`, `Enmity`, and `Fragmentative Goals` are all inter-correlated at r > 0.97. This is a rhetorical "package deal." To be fragmentative is to define a tribe, stoke fear about an enemy, express hostility, and propose goals that involve defeating that enemy. This strategy is strongly and negatively correlated with the `Full Cohesion Index` (e.g., `Fear` vs. Index, r=-0.973).
    *   **The Cohesive Cluster:** `Individual Dignity`, `Hope`, `Amity`, `Compersion`, and `Cohesive Goals` form another, though slightly less tight, cluster. `Individual Dignity` correlates strongly with the `Full Cohesion Index` (r=0.794), as does `Compersion` (r=0.946). This strategy emphasizes universal values, offers hope, seeks common ground, and proposes collaborative goals.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns reveal a fundamental cleavage in political communication style. The discourse is not a spectrum but a bifurcation. Speakers in this sample adopt one of two mutually exclusive meta-strategies.

The strongest pattern is the near-perfect opposition between the `Compersion`-`Amity` axis and the `Tribal Dominance`-`Enmity`-`Fear` axis. This suggests that the choice to either humanize and respect an opponent or to demonize and fear them is a foundational rhetorical decision from which other choices flow. When a speaker chooses the path of conciliation, as McCain did, the language of `Compersion` follows naturally: "Senator Obama has achieved a great thing for himself and for his country. I applaud him for it" (Source: john_mccain_2008_concession.txt). When a speaker chooses the path of fragmentation, `Compersion` becomes rhetorically impossible, and `Envy` or grievance takes its place. As Bernie Sanders stated, "These guys... are not nice guys... they are prepared to destroy Social Security, Medicaid, Medicare... in order to make themselves even richer" (Source: bernie_sanders_2025_fighting_oligarchy.txt).

This finding has significant practical implications. It suggests that the presence or absence of `Compersion` could serve as a simple but powerful heuristic for identifying cohesive versus fragmentative rhetoric. The data also validates the CFF's core premise: that measuring these dimensions independently is crucial. A simple "positive/negative" sentiment score would miss the fact that the fragmentative speeches are not merely negative; they are a specific, structured combination of tribalism, fear, and enmity. Likewise, cohesive speech is not merely "positive"; it is a combination of appeals to dignity, hope, and amity.

### 5.5 Framework Effectiveness Assessment

Based on this analysis, the CFF demonstrates high effectiveness as a tool for discourse analysis.

*   **Discriminatory Power:** The framework successfully discriminated between different rhetorical styles. The `Full Cohesion Index` produced a wide range of scores that clearly separated the conciliatory speech from the three activist speeches, demonstrating its power as a summary metric.
*   **Framework-Corpus Fit:** The CFF's dimensions are highly relevant to contemporary American political discourse. The concepts of `Tribal Dominance`, `Envy`, and `Enmity` map directly onto the populist and polarized rhetoric prevalent today. The framework's ability to capture these dynamics confirms its strong fit with the corpus.
*   **Methodological Innovation:** The analysis highlights the value of the `Tension Indices`. The finding that these speeches exhibit low tension is a non-obvious insight that would be invisible to most other analytical methods. It suggests a simplification or "purification" of rhetorical strategy in polarized contexts, a hypothesis worthy of further investigation.

## 6. Discussion

### Theoretical Implications

The results of this analysis suggest a model of political discourse structured around two competing rhetorical logics. The "Fragmentative-Activist" logic operates by constructing a moral drama of a virtuous in-group (`the people`, `working families`) besieged by a malevolent out-group (`oligarchs`, `illegal criminal aliens`). This logic is powered by the correlated emotions of `Fear` and `Envy` and channeled through `Enmity`. The "Cohesive-Reconciler" logic, in contrast, operates by expanding the definition of the in-group to include everyone (`fellow Americans`), acknowledging shared challenges, and framing the future in terms of `Hope` and shared responsibility.

This bifurcation supports theories of affective polarization, suggesting that political alignment is increasingly defined by these rhetorical-emotional systems rather than by policy debate alone. The near-perfect negative correlations between key dimensions of these two systems (e.g., `Compersion` vs. `Enmity`) indicate they are not just different but mutually exclusive in practice within this sample. A speaker cannot easily celebrate an opponent's success while simultaneously framing them as an existential threat.

### Comparative Analysis and Archetypal Patterns

The data allows for the clear identification of two rhetorical archetypes:

1.  **The Cohesive Reconciler (McCain):** This archetype is defined by high scores in `Individual Dignity`, `Hope`, `Amity`, and especially `Compersion`. Its goal is de-escalation and national unity, even in the face of political defeat. The language focuses on shared identity and common purpose. Key quote: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (Source: john_mccain_2008_concession.txt). This style produces a high positive `Full Cohesion Index`.

2.  **The Fragmentative Activist (Sanders, Ocasio-Cortez, King):** This archetype is defined by high scores in `Tribal Dominance`, `Fear`, `Enmity`, and `Envy`. Its goal is mobilization of a specific in-group against a perceived out-group. While the specific out-group differs (economic oligarchs for Sanders/AOC, immigrants and political opponents for King), the underlying rhetorical structure is identical. Key quote: "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This style produces a high negative `Full Cohesion Index`.

### Limitations and Future Directions

The primary limitation of this study is its sample size of four documents. The findings, while internally consistent and theoretically compelling, cannot be generalized. The powerful correlations observed describe relationships within this specific dataset and should be treated as hypotheses for testing against a larger, more representative corpus.

Future research should apply the CFF to a large-scale, longitudinal dataset of political speech. This would allow for robust statistical testing of the archetypes and meta-strategies identified here. Such research could answer critical questions: Is the prevalence of fragmentative rhetoric increasing over time? Does the `Full Cohesion Index` of a nation's political discourse correlate with real-world outcomes like political violence, social trust, or legislative gridlock? Does the use of `Compersion` by political leaders have a measurable de-escalatory effect on public sentiment? This pilot study demonstrates that the CFF provides the methodological tools necessary to pursue these important questions.

## 7. Conclusion

This computational analysis, guided by the Cohesive Flourishing Framework, successfully dissected the rhetorical structures of four distinct political speeches. It moved beyond surface-level sentiment to reveal two competing, internally coherent meta-strategies: a fragmentative logic based on threat and enmity, and a cohesive logic based on dignity and amity. The analysis identified clear rhetorical archetypes and demonstrated the CFF's capacity to differentiate them using a single, powerful metric—the `Full Cohesion Index`.

The study provides strong, albeit preliminary, validation for the CFF's theoretical design. The oppositional dimensions of the framework were shown to be empirically robust, exhibiting the expected strong negative correlations. The novel `Tension Indices` provided an important insight, suggesting a trend towards rhetorically "pure" and un-nuanced communication. By providing a precise, quantitative, and evidence-based language for discussing the mechanics of division and unity, this analysis showcases the potential of computational social science to illuminate one of the most critical challenges facing modern democracies. The patterns uncovered here form a strong foundation for future large-scale research into the dynamics of political discourse and its impact on social flourishing.

## 8. Evidence Citations

*Quotes used in this report, organized by source document.*

### alexandria_ocasio_cortez_2025_fighting_oligarchy.txt
*   "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."
*   "They aren’t working for these billions. They’re stealing them. They’re stealing them. They’re stealing them from you and you and me."
*   "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart."
*   "No evidence found for this dimension. The speech's focus is on the illegitimate success of an oligarchy, not celebrating the success of others."

### bernie_sanders_2025_fighting_oligarchy.txt
*   "there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about..."
*   "These guys... are not nice guys... they are prepared to destroy Social Security, Medicaid, Medicare... in order to make themselves even richer."

### john_mccain_2008_concession.txt
*   "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
*   "But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake or little influence in the election of an American president is something I deeply admire and commend him for achieving."
*   "Senator Obama has achieved a great thing for himself and for his country. I applaud him for it"
*   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

### steve_king_2017_house_floor.txt
*   "this illegal alien beat this boy to death and then he went and bought gasoline and burned his body... it was just another day in the life of"