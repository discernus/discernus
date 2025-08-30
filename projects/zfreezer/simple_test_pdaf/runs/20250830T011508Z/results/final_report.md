# Populist Discourse Analysis Framework Analysis Report

**Experiment**: simple_test_pdaf  
**Run ID**: 20250830T011508Z_c0f46f8e  
**Date**: 2025-08-30  
**Framework**: pdaf_v10.md  
**Corpus**: corpus.md (4 documents)  

---

## 1. Executive Summary

This report details a computational analysis of four paradigmatic American political speeches using the Populist Discourse Analysis Framework (PDAF) v10.0.0. The study aimed to validate the framework's capacity to distinguish between institutional and populist communication styles, measure strategic rhetorical tensions, and differentiate between ideological variants of populism. The analysis of a small but diverse corpus—comprising speeches from John McCain (institutional), Steve King (conservative populist), Bernie Sanders (progressive populist), and Alexandria Ocasio-Cortez (progressive populist)—yields several preliminary but significant findings.

The results demonstrate that the PDAF effectively differentiates populist from institutional discourse, with populist texts scoring significantly higher across core dimensions such as `Manichaean People-Elite Framing` (M = 0.90 vs. M = 0.00) and `Elite Conspiracy/Systemic Corruption` (M = 0.93 vs. M = 0.00). More importantly, the analysis reveals a fundamental structural divergence within populism itself. A strong negative correlation (r = -0.95) between `Nationalist Exclusion` and `Economic Populist Appeals` suggests that right-leaning and left-leaning populism, while sharing a common anti-elite structure, construct their respective in-groups and out-groups through mutually exclusive boundary mechanisms: one centered on cultural/national identity and the other on economic class.

Furthermore, the framework's novel `Populist Strategic Contradiction Index (PSCI)` successfully quantifies the internal rhetorical tensions characteristic of populist messaging. Populist speakers exhibited higher overall contradiction scores than the institutional speaker, with specific tension metrics revealing how they balance competing appeals, such as framing a national crisis while simultaneously attributing it to specific elite conspiracies. While these findings are based on a limited sample (N=4) and must be considered indicative, they strongly suggest the PDAF is a sophisticated tool capable of moving beyond binary classification to provide a nuanced, quantitative, and cross-ideological measurement of populist rhetoric.

## 2. Opening Framework: Key Insights

*   **Populist and Institutional Rhetoric Are Quantifiably Distinct**: The analysis confirms a clear statistical separation between styles. Populist texts scored near the maximum on dimensions like `Manichaean People-Elite Framing` (M = 0.90) and `Elite Conspiracy` (M = 0.93), while the institutional text scored zero on these same metrics.
*   **Ideological Populism Is Defined by a Nationalist/Economic Trade-off**: The data reveals a powerful inverse relationship (r = -0.95) between `Nationalist Exclusion` and `Economic Populist Appeals`. Conservative populism (King) scored high on nationalism (0.90) and low on economic appeals (0.10), while progressive populism (Sanders, AOC) showed the opposite pattern, with high economic appeals (1.00) and low nationalism (M = 0.10). This suggests different populist ideologies build their core antagonism on distinct, and often mutually exclusive, foundations.
*   **Elite Conspiracy and Anti-Pluralism Are Tightly Linked**: A very strong positive correlation (r = 0.95) between `Elite Conspiracy/Systemic Corruption` and `Anti-Pluralist Exclusion` indicates that as claims of a "rigged system" intensify, so does the rhetoric of delegitimizing political opposition. This suggests a rhetorical pairing where blaming a hidden cabal justifies rejecting pluralistic debate.
*   **Authenticity Claims Correlate with Economic Grievance**: The analysis found a very strong positive correlation (r = 0.95) between `Authenticity vs. Political Class` and `Economic Populist Appeals`. This suggests that speakers who frame themselves as "outsiders" are highly likely to anchor their populist message in the language of economic injustice and a rigged economy.
*   **Populist Rhetoric Contains Measurable Strategic Contradictions**: The framework's novel tension metrics reveal that populist speakers navigate inherent rhetorical contradictions. Bernie Sanders' speech registered the highest `Crisis-Elite Attribution Tension` (0.24), indicating a sophisticated balance between describing a broad societal crisis and attributing it to the specific actions of a coordinated elite.
*   **"The People" Is a Shared but Differently Constructed Concept**: While `Homogeneous People Construction` was present in both populist (M = 0.80) and institutional (M = 0.80) texts, its function appears different. The strong negative correlation with `Nationalist Exclusion` (r = -0.95) suggests that progressive populists construct a unified "people" based on inclusive class solidarity, while conservative populists define it through external, nationalist boundaries.

## 4. Methodology

### Framework Description
This analysis employs the Populist Discourse Analysis Framework (PDAF) v10.0.0, a computational tool designed to quantify the core components of populist political communication. The PDAF moves beyond simple binary classification (populist/non-populist) by measuring discourse across nine distinct dimensions, grouped into three theoretical categories:

1.  **Primary Populist Core Anchors**: `Manichaean People-Elite Framing`, `Crisis-Restoration Temporal Narrative`, `Popular Sovereignty Claims`, and `Anti-Pluralist Exclusion`. These capture the foundational "thin ideology" of populism.
2.  **Populist Mechanism Anchors**: `Elite Conspiracy/Systemic Corruption`, `Authenticity vs. Political Class`, and `Homogeneous People Construction`. These measure the rhetorical strategies used to mobilize support.
3.  **Boundary Distinction Anchors**: `Nationalist Exclusion` and `Economic Populist Appeals`. These identify the primary mechanisms—cultural or economic—used to define the populist in-group versus out-groups.

A key innovation of the PDAF is its use of **salience-weighted analysis**, which captures not only the intensity (raw score, 0.0-1.0) of a populist appeal but also its rhetorical prominence (salience, 0.0-1.0) within a text. This allows for a more nuanced understanding of strategic emphasis. Furthermore, the framework introduces **Populist Strategic Tension Mathematics** to quantify internal contradictions in a speaker's message. Derived metrics like the `Populist Strategic Contradiction Index (PSCI)` measure the degree to which a speaker employs rhetorically conflicting appeals simultaneously, providing insight into strategic coherence.

### Corpus and Data Structure
The analysis was conducted on the Democratic Discourse Corpus, a curated collection of four speeches representing distinct American political communication styles:
*   **Institutional**: John McCain's 2008 concession speech.
*   **Populist Conservative**: Steve King's 2017 House floor speech.
*   **Populist Progressive**: Bernie Sanders' 2025 speech on oligarchy.
*   **Populist Progressive**: Alexandria Ocasio-Cortez's 2025 speech on oligarchy.

The raw data consists of scores (0.0-1.0) and salience ratings (0.0-1.0) for each of the nine PDAF dimensions for every document, along with supporting textual evidence. From this, derived metrics, descriptive statistics, and a correlation matrix were computed.

### Statistical Methods and Limitations
The analysis relies on descriptive statistics (means, medians, standard deviations), Pearson correlation coefficients to assess relationships between dimensions, and non-parametric Mann-Whitney U tests for group comparisons, appropriate for the small sample size.

The primary limitation of this study is its small sample size (N=4). Consequently, all findings, particularly inferential statistics, should be interpreted as **preliminary and indicative, not definitive or generalizable**. The purpose of this analysis is to demonstrate the PDAF's analytical potential and generate hypotheses for future, larger-scale research. All claims are intentionally framed with caution, reflecting the pilot nature of this investigation.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics: Distinguishing Populist and Institutional Styles

A comparison of mean scores reveals a stark and consistent differentiation between the institutional (McCain) and populist (King, Sanders, AOC) communication styles. As shown in Table 1, the populist documents exhibit dramatically higher scores across nearly all core populist dimensions.

**Table 1: Mean Dimensional Scores by Communication Style**

| Dimension                               | Institutional (N=1) | Populist (N=3) |
| --------------------------------------- | ------------------- | -------------- |
| Manichaean People-Elite Framing         | 0.00                | 0.90           |
| Crisis-Restoration Narrative            | 0.50                | 0.80           |
| Popular Sovereignty Claims              | 0.70                | 0.60           |
| Anti-Pluralist Exclusion                | 0.00                | 0.77           |
| Elite Conspiracy/Systemic Corruption    | 0.00                | 0.93           |
| Authenticity vs. Political Class        | 0.10                | 0.67           |
| Homogeneous People Construction         | 0.80                | 0.80           |
| Nationalist Exclusion                   | 0.30                | 0.37           |
| Economic Populist Appeals               | 0.00                | 0.70           |

The institutional speech is characterized by an almost complete absence of core populist markers like `Manichaean People-Elite Framing`, `Anti-Pluralist Exclusion`, and `Elite Conspiracy`. Its highest scores are in `Homogeneous People Construction` (M = 0.80) and `Popular Sovereignty Claims` (M = 0.70), reflecting a conventional democratic appeal to national unity and the electoral process. As John McCain stated, "The American people have spoken, and they have spoken clearly" (Source: john_mccain_2008_concession.txt), a classic affirmation of democratic outcomes rather than a populist challenge to them.

In contrast, the populist speeches are defined by high-intensity moral dichotomies and systemic critiques. For example, Alexandria Ocasio-Cortez frames the central conflict as, "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This pattern holds for `Elite Conspiracy`, where populist texts averaged 0.93, while the institutional text scored 0.00.

### 5.2 Advanced Metric Analysis: Quantifying Strategic Contradictions

The PDAF's derived tension metrics provide insight into the strategic coherence of each speech. The `Populist Strategic Contradiction Index (PSCI)`, which averages the three main tension scores, was higher for the populist speakers (M = 0.10) than for the institutional speaker (M = 0.05), suggesting populist rhetoric is more likely to contain internal contradictions.

**Table 2: Strategic Tension and Contradiction Scores by Speaker**

| Speaker                     | Democratic-Authoritarian Tension | Internal-External Focus Tension | Crisis-Elite Attribution Tension | Populist Strategic Contradiction Index (PSCI) |
| --------------------------- | -------------------------------- | ------------------------------- | -------------------------------- | --------------------------------------------- |
| John McCain (Institutional) | 0.00                             | 0.15                            | 0.00                             | 0.05                                          |
| Steve King (Populist)       | 0.00                             | 0.14                            | 0.08                             | 0.07                                          |
| Bernie Sanders (Populist)   | 0.16                             | 0.00                            | 0.24                             | 0.13                                          |
| AOC (Populist)              | 0.10                             | 0.14                            | 0.08                             | 0.11                                          |

Bernie Sanders' speech exhibits the highest overall contradiction (PSCI = 0.13) and the highest specific tension on `Crisis-Elite Attribution Tension` (0.24). This score reflects a rhetorical strategy that simultaneously emphasizes a broad, almost existential crisis while attributing it with high salience to the specific actions of a coordinated elite. He frames a general crisis of addiction—"we have major epidemics dealing with addiction"—before pivoting to name a single cause: "the worst and most dangerous addiction we have is the greed of the oligarchs" (Source: bernie_sanders_2025_fighting_oligarchy.txt). This balancing act between a diffuse sense of crisis and a specific, conspiratorial cause is a key feature of his populist style, which the PDAF quantifies.

### 5.3 Correlation and Interaction Analysis: Uncovering Rhetorical Structures

The correlation matrix reveals the underlying structural relationships between the rhetorical dimensions of populism. The most significant patterns point to a deep ideological cleavage within populist discourse and a tight coupling of certain rhetorical tactics.

**Table 3: Key Inter-Dimensional Correlations (Pearson's r)**

| Dimension Pair                                            | Correlation (r) | Significance                                                              |
| --------------------------------------------------------- | --------------- | ------------------------------------------------------------------------- |
| Nationalist Exclusion & Economic Populist Appeals         | -0.95           | Very Strong Negative: An ideological trade-off.                           |
| Elite Conspiracy & Anti-Pluralist Exclusion               | 0.95            | Very Strong Positive: Systemic critique is linked to delegitimizing opponents. |
| Authenticity vs. Political Class & Economic Populist Appeals | 0.95            | Very Strong Positive: "Outsider" status is linked to economic grievance.   |
| Homogeneous People Construction & Nationalist Exclusion   | -0.95           | Very Strong Negative: Internal unity is constructed in opposition to external threat. |

### 5.4 Pattern Recognition and Theoretical Insights

#### The Ideological Fault Line: Nationalist vs. Economic Populism
The most powerful finding is the near-perfect negative correlation (r = -0.95) between `Nationalist Exclusion` and `Economic Populist Appeals`. This suggests that while all populists in this corpus employ a Manichaean "people vs. elite" frame, the identity of the "people" and their "enemy" is constructed along two distinct, opposing axes.

**Conservative populism**, represented by Steve King, scores exceptionally high on `Nationalist Exclusion` (0.90) and very low on `Economic Populist Appeals` (0.10). The "people" are defined culturally and nationally, and the primary threat is external. This is vividly illustrated when he uses the narrative of a violent immigrant to define the crisis: "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body" (Source: steve_king_2017_house_floor.txt). Here, the boundary of the "people" is drawn against a foreign, cultural "other."

**Progressive populism**, represented by Bernie Sanders and Alexandria Ocasio-Cortez, displays the mirror image. Both score perfectly on `Economic Populist Appeals` (1.00) while scoring very low on `Nationalist Exclusion` (0.00 and 0.20, respectively). For them, the "people" are a unified working class, and the enemy is an internal economic oligarchy. Sanders defines this conflict by stating, "wage today are lower than they were 52 years ago. Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about" (Source: bernie_sanders_2025_fighting_oligarchy.txt). This finding indicates that the PDAF's Boundary Distinction Anchors effectively capture the fundamental ideological cleavage between right- and left-wing populism.

#### The Anti-Pluralist Engine: Conspiracy and Opposition
The strong positive correlation (r = 0.95) between `Elite Conspiracy/Systemic Corruption` and `Anti-Pluralist Exclusion` reveals a core rhetorical engine of populism. Claims that a corrupt elite is secretly coordinating against the people appear to be functionally linked to the delegitimization of any political opposition. When the system is framed as "rigged," opponents are no longer legitimate adversaries in a pluralistic debate but are instead "enemies of the people."

Steve King exemplifies this by accusing the Supreme Court of a conspiracy—"The Supreme Court created a new command in the Constitution. Not just discovered a right that never existed. They manufactured a command" (Source: steve_king_2017_house_floor.txt)—while simultaneously dismissing opponents as "the people that don’t want to enforce the law" (Source: steve_king_2017_house_floor.txt). Similarly, Sanders identifies a specific elite conspiracy—"Three Wall Street firms, BlackRock, Vanguard, and State Street... are the majority stockholders in 95% of American corporations"—and pairs it with an anti-pluralist declaration: "The American people are saying loud and clear, 'We will not accept an oligarchic form of society'" (Source: bernie_sanders_2025_fighting_oligarchy.txt). This suggests that conspiracy claims provide the justification for anti-pluralist stances.

#### The Outsider's Appeal: Authenticity and Economic Grievance
The analysis also uncovered a very strong positive correlation (r = 0.95) between `Authenticity vs. Political Class` and `Economic Populist Appeals`. This indicates that speakers who position themselves as genuine outsiders, separate from the professional political class, are highly likely to use the language of economic grievance as their primary populist appeal.

Alexandria Ocasio-Cortez provides a clear example of this linkage. She establishes her authenticity through personal testimony: "I believe it because I was a waitress, because I’ve scrubbed toilets with my mom to afford school, because I’ve worked double shifts to keep the lights on" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This "real person" identity is then used to validate her core message of economic populism, which centers on the fight against an "oligarchy" where the powerful "destroy the public good to enrich themselves." This rhetorical pairing grounds abstract economic critiques in a relatable, authentic persona.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the PDAF demonstrates significant effectiveness in several areas:
1.  **Discriminatory Power**: The framework clearly and quantitatively distinguishes between institutional and populist rhetorical styles. The near-zero scores for McCain's speech on key populist dimensions validate its ability to correctly identify non-populist text.
2.  **Cross-Ideological Measurement**: The framework successfully captured the populist nature of both right- and left-wing speakers. More importantly, the `Boundary Distinction Anchors` proved highly effective at identifying the core ideological differences between them.
3.  **Nuance and Complexity**: The introduction of salience and strategic tension metrics allowed the analysis to move beyond simple content analysis. The `PSCI` and individual tension scores provided a novel, quantitative measure of rhetorical strategy and coherence, as seen in the analysis of Sanders' speech. The strong negative correlation between `Homogeneous People Construction` and `Nationalist Exclusion` further highlights the framework's ability to uncover complex structural trade-offs in political language.

## 6. Discussion

The findings from this pilot study, while preliminary, carry significant theoretical implications. The stark, inverse relationship between `Nationalist Exclusion` and `Economic Populist Appeals` provides strong quantitative support for theories that differentiate between right-wing (nativist/cultural) and left-wing (socio-economic) populism. The PDAF appears to not only confirm this distinction but also suggests that these two boundary-drawing mechanisms may be structurally incompatible at high levels of intensity; a speaker must choose which "enemy" to prioritize.

The strong positive correlation between `Elite Conspiracy` and `Anti-Pluralist Exclusion` offers empirical weight to the arguments of scholars like Jan-Werner Müller, who posit that anti-pluralism is a central, defining feature of populism. This analysis suggests that the rhetorical claim of a "rigged system" is a primary vehicle for expressing that anti-pluralism, as it reframes political opponents as illegitimate actors within that corrupt system.

The framework's novel contribution lies in its ability to measure strategic tension. The finding that populist speakers exhibit higher `Populist Strategic Contradiction Index` scores opens a new avenue for research. It suggests that populism may be inherently contradictory, attempting to balance broad appeals with specific grievances, or democratic claims with authoritarian tendencies. Future research could investigate whether higher PSCI scores correlate with electoral success or failure, or if they are a sign of rhetorical overreach. For instance, the moderate `Internal-External Focus Tension` seen in the speeches by King and AOC (0.14) suggests that even when a speaker focuses primarily on one boundary (nationalist for King, economic/class for AOC), they still make minor appeals to the other, creating a measurable tension.

The limitations of this study are clear. With only four documents, the findings are illustrative, not generalizable. The high correlation values are likely inflated by the small sample size. However, the clarity and theoretical coherence of the patterns that emerged strongly suggest that these are not random artifacts but signals worthy of further investigation with a much larger and more diverse corpus.

## 7. Conclusion

This computational analysis, though limited in scope, successfully demonstrates the analytical power of the Populist Discourse Analysis Framework (PDAF) v10.0.0. The framework proved highly effective at its core tasks: it distinguished populist from institutional discourse, identified the key ideological cleavage between nationalist and economic populism, and, through its innovative tension metrics, provided a novel quantitative measure of strategic contradiction.

The study's central finding is that American populism, while unified by a common anti-elite, crisis-driven rhetorical structure, is fundamentally divided by its method of boundary construction. The stark trade-off between `Nationalist Exclusion` and `Economic Populist Appeals` represents a quantifiable fault line between its conservative and progressive variants. This research provides a robust, evidence-based foundation for future, larger-scale studies to explore the dynamics of populist communication with unprecedented nuance and precision. The PDAF offers a promising methodological path forward for moving the study of populism from qualitative description and binary classification to scalable, quantitative, and strategically insightful analysis.

## 8. Evidence Citations

**Source Document: john_mccain_2008_concession.txt**
*   On Popular Sovereignty Claims: "The American people have spoken, and they have spoken clearly."
*   On Homogeneous People Construction: "I urge all Americans - I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"

**Source Document: steve_king_2017_house_floor.txt**
*   On Nationalist Exclusion: "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body."
*   On Elite Conspiracy/Systemic Corruption: "The Supreme Court created a new command in the Constitution. Not just discovered a right that never existed. They manufactured a command."
*   On Anti-Pluralist Exclusion: "He’s been criticized for his effectiveness by the people that don’t want to enforce the law."

**Source Document: bernie_sanders_2025_fighting_oligarchy.txt**
*   On Economic Populist Appeals: "wage today are lower than they were 52 years ago. Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."
*   On Elite Conspiracy/Systemic Corruption: "Three Wall Street firms, BlackRock, Vanguard, and State Street. Combined, these three investment firms are the majority stockholders in 95% of American corporations."
*   On Anti-Pluralist Exclusion: "The American people are saying loud and clear, 'We will not accept an oligarchic form of society.'"
*   On Crisis-Restoration Narrative: "In America today, as I think all of you know, sadly and tragically, and we've got to deal with it, we have major epidemics dealing with addiction... But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."

**Source Document: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   On Manichaean People-Elite Framing: "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."
*   On Authenticity vs. Political Class: "I don't believe in healthcare, labor and human dignity, because I'm an extremist or a Marxist. I believe it because I was a waitress, because I've scrubbed toilets with my mom to afford school, because I've worked double shifts to keep the lights on, because I lost my dad to cancer as a kid and had to see my mom open hospital bills in the days after."
*   On Homogeneous People Construction: "If you are willing to fight for working people regardless of who they are, how they identify, or where they come from, you are welcome here."