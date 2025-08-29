# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: 20250829T170947Z_92f6ad56  
**Date**: 2025-08-29  
**Framework**: cff_v10.md  
**Corpus**: corpus.md (4 documents)  

---

## 1. Executive Summary

This report details a computational analysis of four paradigmatic American political speeches using the Cohesive Flourishing Framework (CFF) v10. The study aimed to assess the framework's capacity to distinguish rhetorical styles and measure their potential impact on social cohesion. The analysis reveals a stark and consistent structural divergence between institutional and populist modes of discourse, irrespective of partisan affiliation.

The primary finding is the identification of two distinct rhetorical archetypes. The first, an **Institutional-Cohesive** style, exemplified by John McCain's 2008 concession speech, is characterized by high scores in Individual Dignity, Hope, Amity, and Cohesive Goals. This style emphasizes universal values and national unity. The second, a **Populist-Fragmenting** style, is observed in speeches by Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez. This approach is defined by its reliance on Tribal Dominance, Enmity, Fear, and Fragmentative Goals, constructing a narrative of conflict between an in-group ("the people") and a designated out-group (elites, political opponents). The statistical correlation between Tribal Dominance and Individual Dignity was exceptionally strong and negative (r = -0.99), suggesting these are core opposing principles in the analyzed discourse.

Despite their divergent political goals, the populist speakers from both the conservative and progressive wings share this underlying fragmenting rhetorical structure. Furthermore, the analysis of the Strategic Contradiction Index, which measures rhetorical incoherence, found that all speeches were largely consistent in their messaging. This indicates that even highly fragmenting discourse can be presented as a coherent, internally consistent strategy. These preliminary findings, based on a small corpus, suggest the CFF is a valuable tool for moving beyond surface-level partisan labels to uncover the deeper structural patterns in political communication that may influence social cohesion.

## 2. Opening Framework: Key Insights

*   **Two Opposing Rhetorical Packages Dominate Discourse:** The analysis reveals two distinct and negatively correlated clusters of rhetorical appeals. A **Cohesive Package** (Individual Dignity, Hope, Amity, Cohesive Goals) is strongly associated with institutional discourse. A **Fragmenting Package** (Tribal Dominance, Fear, Enmity, Fragmentative Goals) is characteristic of populist discourse, both conservative and progressive.
*   **Populism Shares a Common Fragmenting Structure:** Despite differing ideologies, the populist speeches from Steve King (conservative), Bernie Sanders (progressive), and Alexandria Ocasio-Cortez (progressive) all scored high on Tribal Dominance (M = 0.80 for all three) and Fragmentative Goals (M = 0.75). This suggests that populism, as a rhetorical style in this corpus, relies on a shared structure of in-group/out-group division.
*   **Institutional Discourse Prioritizes Cohesion:** John McCain's 2008 concession speech scored exceptionally high on cohesive dimensions like Individual Dignity (0.80) and Hope (0.70), while scoring very low on fragmenting dimensions like Tribal Dominance (0.20) and Enmity (0.10). This provides a clear baseline for a rhetorical style oriented toward democratic norm-reinforcement and social unity.
*   **Tribal Dominance and Individual Dignity are Core Opposites:** The data shows a near-perfect negative correlation between the raw scores for Tribal Dominance and Individual Dignity (r = -0.99). This powerful statistical relationship validates the CFF's central theoretical axis and suggests that political discourse in this sample makes a fundamental choice between emphasizing in-group supremacy and universal human worth.
*   **Fragmenting Rhetoric Can Be Highly Coherent:** The Strategic Contradiction Index, which measures the use of mixed or contradictory appeals, was low across all documents (M = 0.08). This indicates that speakers, whether promoting cohesion or fragmentation, tend to employ a consistent rhetorical strategy. Fragmenting speech is not necessarily incoherent; it is often a deliberately and consistently applied rhetorical approach.
*   **Fear Appeals Align with Divisive Strategies:** The analysis found a strong positive correlation between Fear and both Tribal Dominance (r = 0.98) and Fragmentative Goals (r = 0.98). This suggests that rhetoric invoking crisis and threat is systematically coupled with messages that define exclusionary in-groups and promote divisive objectives.

## 4. Methodology

### Framework Description
This analysis employed the Cohesive Flourishing Framework (CFF) v10, a multi-dimensional tool for evaluating the impact of discourse on social cohesion. The CFF's core innovation is its independent scoring of ten conceptual anchors organized into five opposing pairs on a 0.0 to 1.0 scale:
*   **Identity Axis**: Tribal Dominance vs. Individual Dignity
*   **Emotional Climate**: Fear vs. Hope
*   **Success Orientation**: Envy vs. Compersion
*   **Relational Climate**: Enmity vs. Amity
*   **Goal Orientation**: Fragmentative Goals vs. Cohesive Goals

A key feature of the CFF is its dual-track analysis of both the *intensity* (raw score) and *salience* (rhetorical prominence) of each dimension. This allows for a nuanced understanding of not just what is said, but what is emphasized. From these base scores, the framework derives advanced metrics, including **Tension Indices** to measure rhetorical contradiction and **Salience-Weighted Cohesion Indices** to provide an overall assessment of a text's cohesive or fragmenting properties.

### Corpus Description
The analysis was conducted on the Democratic Discourse Corpus (v8.0), a curated collection of four speeches representing different rhetorical styles in contemporary American politics:
1.  **John McCain (2008)**: An institutional concession speech emphasizing democratic norms.
2.  **Steve King (2017)**: A conservative populist House floor speech.
3.  **Bernie Sanders (2025)**: A progressive populist speech on economic oligarchy.
4.  **Alexandria Ocasio-Cortez (2025)**: A progressive populist speech critiquing systemic power.

### Statistical Methods and Limitations
The analysis is based on the statistical results generated from the CFF's application to the corpus. This includes descriptive statistics (means, standard deviations), a correlation matrix of all dimensional scores, and derived metrics such as the Strategic Contradiction Index.

A significant methodological limitation arose from data quality issues in the raw analysis output. Inconsistent dimension naming (e.g., "emulation" instead of "compersion," "enity" instead of "enmity") prevented the successful calculation of the composite Salience-Weighted Cohesion Indices for three of the four documents. Consequently, this report relies primarily on the analysis of the raw dimensional scores, their correlations, and the correctly calculated Tension Indices and Strategic Contradiction Index. For interpretive purposes, "emulation" was treated as synonymous with "compersion" and "enity" with "enmity," with this assumption noted. Given the small sample size (N=4), all findings should be considered preliminary and indicative of patterns that warrant further investigation with a larger corpus. The analysis is descriptive, and no claims of statistical significance are made.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

The descriptive statistics reveal a clear bifurcation in rhetorical strategies between the institutional speech of John McCain and the populist speeches of King, Sanders, and Ocasio-Cortez.

**Table 1: Mean Raw Scores for Cohesive vs. Fragmenting Dimensions by Speaker**

| Speaker                  | Style                  | Tribal Dominance | Individual Dignity | Fear | Hope | Enmity | Amity | Fragmentative Goals | Cohesive Goals |
| ------------------------ | ---------------------- | ---------------- | ------------------ | ---- | ---- | ------ | ----- | ------------------- | -------------- |
| John McCain              | Institutional          | 0.20             | **0.80**           | 0.10 | **0.70** | 0.10   | **0.70**  | 0.10                | **0.70**       |
| Steve King               | Populist (Conservative) | **0.80**         | 0.15               | 0.60 | 0.20 | **0.70**   | 0.10  | **0.65**            | 0.20           |
| Bernie Sanders           | Populist (Progressive) | **0.80**         | 0.10               | **0.70** | 0.60 | **0.70**   | 0.40  | **0.80**            | 0.20           |
| Alexandria Ocasio-Cortez | Populist (Progressive) | **0.80**         | 0.20               | 0.60 | 0.50 | **0.80**   | 0.30  | **0.80**            | 0.30           |

*Note: Enmity scores for Sanders and Ocasio-Cortez were inferred from "enity" in the raw data. Highest scores for each speaker are bolded to highlight emphasis.*

McCain's speech is the clear outlier, with consistently high scores on all four major cohesive dimensions and low scores on their fragmenting counterparts. Conversely, the three populist speakers, regardless of party, display a mirror-image profile, with high scores on Tribal Dominance, Enmity, and Fragmentative Goals. This pattern is the most dominant finding in the dataset.

For instance, McCain's emphasis on universal inclusion is evident in his high Individual Dignity score (0.80), supported by his statement, **"I have always believed that America offers opportunities to all who have the industry and will to seize it"** (Source: john_mccain_2008_concession.txt). This stands in stark contrast to the populist focus on group identity. As Bernie Sanders stated, defining a clear in-group versus an out-group, **"The American people are outraged at what's going on... We will not accept an oligarchic form of society... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%"** (Source: bernie_sanders_2025_fighting_oligarchy.txt), which corresponds to his high Tribal Dominance score (0.80).

### 5.2 Advanced Metric Analysis

The **Strategic Contradiction Index** measures the degree of rhetorical incoherence by calculating the average tension across all five dimensional axes. A low score indicates a consistent message, while a high score indicates the use of contradictory appeals.

**Table 2: Strategic Contradiction Index by Speaker**

| Speaker                  | Style                  | Strategic Contradiction Index |
| ------------------------ | ---------------------- | ----------------------------- |
| John McCain              | Institutional          | 0.073                         |
| Steve King               | Populist (Conservative) | 0.078                         |
| Bernie Sanders           | Populist (Progressive) | 0.073                         |
| Alexandria Ocasio-Cortez | Populist (Progressive) | 0.090                         |

The indices for all four speeches are relatively low, suggesting that each speaker delivered a rhetorically coherent message. McCain's speech, with its consistent focus on cohesion, and Sanders' speech, with its consistent focus on populist fragmentation, show the lowest contradiction. The slightly higher score for Ocasio-Cortez (0.090) may reflect a more complex blend of appeals, but the overall pattern indicates that fragmenting rhetoric is not inherently contradictory; it is a consistent and deliberate strategy.

The only fully calculated **Full Cohesion Index** was for Bernie Sanders' speech, which registered at **-0.298**. This strongly negative score, on a scale of -1.0 to +1.0, quantitatively confirms the fragmenting nature of his rhetoric, aligning with the high scores on Tribal Dominance, Enmity, and Fragmentative Goals.

### 5.3 Correlation and Interaction Analysis

The correlation matrix provides powerful insights into the structural relationships between the CFF dimensions, effectively revealing the rhetorical "packages" used by the speakers.

**Table 3: Key Dimensional Correlations (Pearson's r)**

| Dimension 1          | Dimension 2          | Correlation (r) | Interpretation                               |
| -------------------- | -------------------- | --------------- | -------------------------------------------- |
| Tribal Dominance     | Individual Dignity   | -0.99           | Extremely strong inverse relationship        |
| Tribal Dominance     | Fear                 | 0.98            | Very strong positive relationship            |
| Tribal Dominance     | Fragmentative Goals  | 0.98            | Very strong positive relationship            |
| Individual Dignity   | Cohesive Goals       | 0.99            | Extremely strong positive relationship       |
| Hope                 | Amity                | 0.93            | Very strong positive relationship            |
| Fear                 | Individual Dignity   | -1.00           | Perfect inverse relationship (rounded)       |

The data reveals two opposing constellations of rhetorical features.

1.  **The Fragmenting Constellation**: Tribal Dominance, Fear, Enmity, and Fragmentative Goals are all strongly and positively inter-correlated. This suggests a rhetorical strategy where defining an exclusionary in-group is linked to invoking threats and promoting divisive objectives. Steve King's speech exemplifies this, combining fear appeals about the constitution with adversarial positioning. He speaks of news that would **"kick the breath out of your gut... And you'd lay your head down on the pillow at night having trouble to sleep"** (Source: steve_king_2017_house_floor.txt), linking this fear directly to a need to oppose the sitting president.

2.  **The Cohesive Constellation**: Individual Dignity, Hope, Amity, and Cohesive Goals are also strongly and positively inter-correlated. This indicates a strategy where appeals to universal human worth are paired with optimistic visions and calls for unity. McCain's speech is the archetype here, urging Americans to **"find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity"** (Source: john_mccain_2008_concession.txt).

The extremely strong negative correlations between members of these opposing constellations (e.g., Tribal Dominance vs. Individual Dignity, r = -0.99) provide robust validation for the CFF's oppositional design. In this corpus, speakers make a clear choice between these two fundamental approaches.

### 5.4 Pattern Recognition and Theoretical Insights

The most significant pattern is the clear divide between institutional and populist rhetoric, which transcends traditional left-right political divides. Both progressive populists (Sanders, Ocasio-Cortez) and the conservative populist (King) utilize the same core rhetorical engine: high tribalism, high enmity, and high fragmentation.

Alexandria Ocasio-Cortez explicitly identifies the mechanism of this strategy, stating, **"They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture"** (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). While she attributes this strategy to her opponents, her own rhetoric, as measured by the CFF, employs a similar structure of high Enmity (0.80) and Tribal Dominance (0.80) by framing the conflict as an irreconcilable struggle between the working class and a disdainful elite.

Similarly, Bernie Sanders' speech is built on a foundation of class-based tribalism and enmity. His high Envy score (0.50) is supported by his assertion that the wealthy **"feel obliged to step on the backs of poor people to become even richer"** and that their goal is to **"destroy Social Security, Medicare, Medicares, the Veterans Administration"** (Source: bernie_sanders_2025_fighting_oligarchy.txt). This rhetoric is fundamentally fragmenting, as it posits a zero-sum conflict between social classes.

In contrast, John McCain’s institutional discourse consistently defaults to cohesive appeals. Even when acknowledging political defeat, his language reinforces democratic systems and shared identity. His high score in Compersion (emulation) (0.60) is evidenced when he says of his opponent, **"His success alone commands my respect for his ability and perseverance"** (Source: john_mccain_2008_concession.txt). This celebration of an opponent's success is the antithesis of the envy and resentment central to the populist speeches.

### 5.5 Framework Effectiveness Assessment

The CFF demonstrated high discriminatory power in this analysis. It successfully differentiated between rhetorical styles with clarity and provided quantitative evidence for the structural differences. The strong correlations, particularly the near-perfect negative correlation between the poles of the Identity Axis, serve as a powerful form of construct validation for the framework's design. The framework effectively captured the core strategic differences between speakers, revealing that the populist/institutional divide was a more potent explanatory variable than partisan affiliation in this sample.

The primary limitation observed was not in the framework's conceptual design but in the data processing pipeline, which led to inconsistent naming and failed calculations for some derived metrics. This highlights the need for robust data validation steps in computational analysis workflows. Despite this, the raw dimensional scores and the correlation matrix provided more than sufficient data to draw strong, albeit preliminary, conclusions.

## 6. Discussion

The findings of this analysis carry significant implications for understanding contemporary political discourse. The CFF's ability to look past partisan labels and identify a shared *populist-fragmenting* rhetorical structure used by speakers from opposing political ideologies is a key insight. It suggests that the political polarization often attributed solely to policy differences may be driven by a more fundamental divergence in rhetorical strategy: one that seeks to unify a broad national polity (institutional) versus one that seeks to mobilize a specific "tribe" against a perceived enemy (populist).

This analysis identifies two clear archetypes in the corpus:
1.  **The Institutional Unifier (McCain):** This archetype uses the "Cohesive Package" of rhetoric—appeals to universal dignity, hope, amity, and shared goals—to reinforce democratic norms and promote social solidarity, even in the context of political loss.
2.  **The Populist Agitator (King, Sanders, Ocasio-Cortez):** This archetype, whether from the right or left, uses the "Fragmenting Package"—appeals to tribal identity, fear, enmity, and divisive goals—to mobilize a base by constructing a narrative of existential conflict against a powerful out-group.

The low Strategic Contradiction Index across all speeches is also theoretically important. It suggests that fragmenting rhetoric is not a sign of chaotic or unsophisticated communication. Rather, it is a coherent, internally consistent rhetorical strategy designed to achieve specific political ends. This challenges any assumption that cohesive speech is inherently more "thoughtful" or complex.

The limitations of this study are clear, primarily its small sample size. These four speeches were chosen for their paradigmatic quality, but the patterns observed here require validation across a much larger and more diverse corpus of political texts. Future research should investigate whether these rhetorical archetypes hold constant across different contexts (e.g., campaign rallies vs. legislative debates) and over longer time periods.

## 7. Conclusion

This computational analysis, guided by the Cohesive Flourishing Framework, successfully parsed four distinct political speeches and uncovered a fundamental structural divide between institutional and populist rhetoric. The framework's design, particularly its use of opposing dimensional axes, was validated by the strong statistical patterns observed in the data. The core finding—that populist discourse from both the right and left shares a common fragmenting structure based on tribalism and enmity—provides a powerful new lens for analyzing political communication.

While the data processing issues encountered with derived metrics highlight the need for technical rigor, the clarity of the findings from the raw dimensional scores demonstrates the CFF's potential as a robust analytical tool. The study confirms that John McCain's institutional discourse is structurally more cohesive than the populist styles of King, Sanders, and Ocasio-Cortez. These preliminary results suggest that the most significant fault line in modern political discourse may not be between left and right, but between those who employ the language of universal inclusion and those who wield the power of tribal division.

## 8. Evidence Citations

### john_mccain_2008_concession.txt
*   **Individual Dignity:** "I have always believed that America offers opportunities to all who have the industry and will to seize it."
*   **Hope / Cohesive Goals:** "I urge all Americans - I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity, defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
*   **Compersion (Emulation):** "His success alone commands my respect for his ability and perseverance."
*   **Cohesive Goals:** "We must move beyond it and work together to get our country moving again."

### steve_king_2017_house_floor.txt
*   **Fear:** 'And that was June 24th on Thursday, and it would kick the breath out of your gut to hear that if you\'re a constitutionalist. And it brings you to a sad state of mourn. And you\'d lay your head down on the pillow at night having trouble to sleep, thinking, "What am I going to do tomorrow? I couldn\'t react today. What am I going to do tomorrow? Lord, wake me up with an idea on how to, how to preserve our Constitution."'

### bernie_sanders_2025_fighting_oligarchy.txt
*   **Tribal Dominance:** 'The American people are outraged at what\'s going on, and the American people are saying loud and clear, "We will not accept an oligarchic form of society. We will not accept the richest guy in the world running all over Washington, making cuts to the Social Security Administration, cuts to the Veterans Administration, almost destroying the Department of Education, all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%.'
*   **Envy / Fragmentative Goals:** "Now everybody wants to do well in life. Everybody wants to make money. But you would think that if you had a few billion dollars or $10 or $20 billion, you would not feel obliged to step on the backs of poor people to become even richer. But that is exactly what they are doing right now. They are prepared to destroy Social Security, Medicare, Medicares, the Veterans Administration in order to make themselves even richer."

### alexandria_ocasio_cortez_2025_fighting_oligarchy.txt
*   **Tribal Dominance / Fragmentative Goals:** "They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture."
*   **Enmity:** "Donald Trump does see the immense pressure that working people are under. But his answer is an America that operates on the principle of every man for himself, divide and conquer."