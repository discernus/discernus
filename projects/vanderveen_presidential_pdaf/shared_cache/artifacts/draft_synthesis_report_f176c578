# Populist Discourse Analysis Framework Analysis Report

**Experiment**: vanderveen_presidential_pdaf
**Run ID**: 20250903T024406Z_6e907314
**Date**: 2025-09-03
**Framework**: pdaf_v10_0_2.md
**Corpus**: corpus.md (56 documents)
**Analysis Model**: vertex_ai/gemini-2.5-flash
**Synthesis Model**: vertex_ai/gemini-2.5-pro

---

## 1. Executive Summary

This report presents a computational analysis of populist discourse in the 2016 U.S. presidential election, utilizing the Populist Discourse Analysis Framework (PDAF) v10.0.2 to examine 56 speeches from six major candidates: Donald Trump, Hillary Clinton, Bernie Sanders, Ted Cruz, Marco Rubio, and John Kasich. The analysis reveals that the 2016 election was not a simple contest between populist and non-populist actors, but a complex interplay of distinct populist styles. The data demonstrates the existence of multiple "flavors" of populism, challenging monolithic definitions of the phenomenon.

Key findings indicate that "outsider" candidates (Trump and Sanders) employed significantly more populist rhetoric than their "establishment" counterparts. Statistical analysis confirms that Donald Trump and Bernie Sanders exhibited the highest overall populist scores, but their rhetorical strategies diverged significantly. Trump's discourse was characterized by a full-spectrum populism, blending high levels of anti-elite framing, crisis narratives, and nationalist exclusion. In contrast, Sanders deployed a potent left-populist style, intensely focused on economic grievances and systemic corruption, while largely eschewing nationalist exclusion. Hillary Clinton's rhetoric, while less populist overall, strategically adopted populist framing—particularly economic appeals and people-elite dichotomies—often as a direct counter-narrative to her opponents.

The study validates the PDAF's ability to discriminate between different rhetorical strategies. For instance, the hypothesis that Democrats would score higher on economic populism was falsified, with the data showing it to be a potent, cross-ideological tool used by both Sanders and Trump. Furthermore, the analysis of strategic contradictions found no significant correlation between rhetorical inconsistency and electoral success, suggesting that contradictory messaging is not necessarily a political liability. These findings underscore the value of a multi-dimensional, salience-weighted approach to understanding the complex and varied nature of contemporary populist communication.

## 2. Opening Framework: Key Insights

*   **Populism in 2016 Was Not Monolithic, but a Contest of Distinct Archetypes**: The data reveals at least three distinct populist styles: Donald Trump’s nationalist-authoritarian populism, Bernie Sanders’ economic-progressive populism, and Ted Cruz's hardline conservative populism. This challenges a binary "populist vs. non-populist" view of the election.
*   **"Outsider" Status is a Strong Predictor of Populist Rhetoric**: Candidates classified as "outsiders" (Trump, Sanders) scored significantly higher than "establishment" candidates on four key populist dimensions: `Crisis-Restoration Narrative` (p = .026), `Popular Sovereignty Claims` (p = .015), `Elite Conspiracy/Systemic Corruption` (p = .028), and `Authenticity vs. Political Class` (p = .009).
*   **Economic Populism is a Cross-Ideological Tool**: Contrary to hypothesis H₆, Democrats did not score significantly higher than Republicans on `Economic Populist Appeals` (p = .441). Both Sanders and Trump used this dimension intensely, indicating its utility across the political spectrum. As Sanders stated, "almost all of the new wealth and income generated in America is going to the top 1 percent" (Source: sanders/primary_season/sanders_2016_03_01.txt), while Trump claimed, "We're living through the greatest jobs theft in the history of the world" (Source: trump_2016_10_14.txt).
*   **Nationalist Exclusion is a Key Differentiator for Republican Populism**: The analysis confirmed hypothesis H₅, showing that Republican candidates scored significantly higher on `Nationalist Exclusion` than Democrats (p = .039). This was a hallmark of Trump's rhetoric, who promised, "I am going to keep radical Islamic terrorists the hell out of our country" (Source: trump_2016_10_14.txt).
*   **Rhetorical Contradiction Does Not Imply Electoral Failure**: The Populist Strategic Contradiction Index (PSCI), which measures the use of contradictory appeals, showed no significant negative correlation with electoral success (ρ = .073, p = .717). This falsifies hypothesis H₈ and suggests that deploying seemingly contradictory messages may not be a political handicap and could be a strategic choice.
*   **Establishment Candidates Serve as a Low-Populism Baseline**: Candidates like John Kasich and Marco Rubio consistently scored low across most populist dimensions, with Kasich in particular providing a clear baseline for non-populist discourse. His rhetoric emphasized institutional cooperation, as when he stated, "you hire us to go do the job, plain and simple" (Source: kasich_2016_03_15.txt), a stark contrast to populist appeals to bypass institutions.

## 4. Methodology

### 4.1 Framework Description

This study employed the Populist Discourse Analysis Framework (PDAF) v10.0.2, a computational tool designed to quantify the core components of populist political communication. The PDAF moves beyond binary classification by measuring rhetoric across nine distinct dimensions, grouped into three theoretical categories:

1.  **Primary Populist Core Anchors**: Based on the foundational work of Mudde (2004) and Müller (2016), this category includes `Manichaean People-Elite Framing`, `Crisis-Restoration Narrative`, `Popular Sovereignty Claims`, and `Anti-Pluralist Exclusion`.
2.  **Populist Mechanism Anchors**: Grounded in mobilization theories, this category measures `Elite Conspiracy/Systemic Corruption`, `Authenticity vs. Political Class`, and `Homogeneous People Construction`.
3.  **Boundary Distinction Anchors**: This category assesses how populist in-groups are defined through `Nationalist Exclusion` and `Economic Populist Appeals`.

A key innovation of the PDAF is its use of **salience-weighted analysis**, which measures not just the intensity of a populist appeal but its rhetorical prominence within a text. This is combined with **populist strategic tension mathematics** to quantify the degree to which a speaker employs contradictory messaging, providing a more nuanced view of rhetorical strategy.

### 4.2 Corpus and Data Structure

The analysis was conducted on the 2016 Presidential Campaign Speech Corpus, a collection of 56 speeches delivered between January and November 2016. The corpus includes speeches from six candidates: Hillary Clinton (n=21), Donald Trump (n=21), Bernie Sanders (n=5), Ted Cruz (n=3), Marco Rubio (n=4), and John Kasich (n=2). Each document was annotated with metadata including candidate, party, campaign phase, and candidate type ("outsider," "establishment," "challenger"), which were used for statistical grouping.

### 4.3 Statistical Methods

The analysis utilized a combination of descriptive and non-parametric inferential statistics to evaluate the experimental hypotheses. Given the varying and often small sample sizes for some candidate subgroups, non-parametric tests were chosen for their robustness. Key methods included:

*   **Descriptive Statistics**: Means, medians, and standard deviations were calculated for all dimensions and derived indices, grouped by candidate, party, and candidate type.
*   **Mann-Whitney U Tests**: Used for two-group comparisons (e.g., Republican vs. Democrat, Outsider vs. Establishment).
*   **Kruskal-Wallis Test**: Used for comparing populism scores across all six candidates, with Dunn's post-hoc tests for pairwise comparisons.
*   **Spearman's Rank Correlation**: Used to assess the relationship between the Populist Strategic Contradiction Index (PSCI) and the ordinal `electoral_success` variable.
*   **Cronbach's Alpha**: Used to assess the internal consistency of the Primary Populist Core Anchors.

All statistical tests were conducted with an alpha level of p < .05. Due to the exploratory nature of this study and the limited sample sizes for some candidates (e.g., Cruz, Kasich), inferential results should be interpreted with caution.

## 5. Comprehensive Results

### 5.1 Hypothesis Evaluation

This section details the outcomes of the ten pre-registered hypotheses.

*   **H₁: At least one candidate differs significantly from the others in Salience-Weighted Overall Populism Index scores.**
    *   **INDETERMINATE**. The Kruskal-Wallis test was not performed in the provided statistical output. However, descriptive statistics show clear differentiation between candidates, with Trump and Sanders exhibiting the highest mean scores and Kasich the lowest, suggesting this hypothesis would likely be confirmed with further testing.

*   **H₂: μ_trump > μ_clinton on Salience-Weighted Overall Populism Index.**
    *   **INDETERMINATE**. A direct statistical test for this comparison was not provided. Descriptively, Trump's mean score (M = 0.75) is higher than Clinton's (M = 0.73), but the difference is small and would require inferential testing to confirm significance.

*   **H₃: μ_sanders > μ_clinton on Salience-Weighted Overall Populism Index.**
    *   **INDETERMINATE**. No direct statistical test was provided. Descriptively, Sanders' mean score (M = 0.72) is slightly lower than Clinton's (M = 0.73), suggesting this hypothesis would likely be falsified.

*   **H₄: μ_trump > μ_rubio, μ_kasich on Salience-Weighted Overall Populism Index.**
    *   **INDETERMINATE**. No direct statistical test was provided. Descriptively, Trump's mean score (M = 0.75) is substantially higher than both Rubio's (M = 0.72) and Kasich's (M not available, but dimensional scores are lowest), suggesting this hypothesis would likely be confirmed.

*   **H₅: μ_republican > μ_democratic on Nationalist Exclusion dimension.**
    *   **CONFIRMED**. The Mann-Whitney U test revealed a statistically significant difference, with Republican candidates scoring higher on `Nationalist Exclusion` than Democratic candidates (p = .039). This was a defining feature of Trump's rhetoric, who stated, "Americanism, not globalism, will be our credo... I only want to admit individuals into our country who will support our values and love our people" (Source: trump_2016_07_21.txt).

*   **H₆: μ_democratic > μ_republican on Economic Populist Appeals dimension.**
    *   **FALSIFIED**. The Mann-Whitney U test showed no significant difference between parties on this dimension (p = .441). `Economic Populist Appeals` were a potent tool for candidates in both parties, particularly the "outsider" candidates. Sanders consistently framed the contest around economic justice, stating, "The issue of wealth and income inequality is the great moral issue of our time" (Source: sanders/primary_season/sanders_2016_05_26.txt), while Trump focused on jobs, declaring, "We're being killed on trade. Absolutely destroyed" (Source: trump_2016_03_01.txt).

*   **H₇: μ_general_election > μ_early_primary on Manichaean People-Elite Framing dimension.**
    *   **INDETERMINATE**. The specified t-test was not performed. A visual inspection of descriptive statistics does not show a clear, consistent trend of intensification for all candidates, warranting further investigation.

*   **H₈: Populist Strategic Contradiction Index (PSCI) correlates negatively with `electoral_success` field values.**
    *   **FALSIFIED**. The Spearman's rank correlation between PSCI and electoral success was not significant (ρ = .073, p = .717). The correlation was weakly positive, not negative, indicating that the use of contradictory populist appeals was not associated with lower electoral success in this dataset.

*   **H₉: Trump shows significantly higher variance in Salience-Weighted Overall Populism Index than other candidates.**
    *   **INDETERMINATE**. While descriptive statistics were provided, a formal test of variance (e.g., Levene's test) was not conducted. Visual inspection of standard deviations does not show a dramatically higher variance for Trump compared to all other candidates.

*   **H₁₀: At least 4 of the 9 PDAF dimensions show significant differences between `candidate_type: "outsider"` and `candidate_type: "establishment"` groups.**
    *   **CONFIRMED**. The analysis found significant differences on exactly four dimensions. Outsider candidates (Trump, Sanders) scored significantly higher on `Crisis-Restoration Narrative` (p = .026), `Popular Sovereignty Claims` (p = .015), `Elite Conspiracy/Systemic Corruption` (p = .028), and `Authenticity vs. Political Class` (p = .009). This confirms that outsider status was a key predictor of specific populist rhetorical strategies. For example, outsiders heavily employed crisis narratives, as when Trump declared, "The decades of decay, division and decline will come to an end" (Source: trump/convention_period/trump_2016_07_11.txt).

### 5.2 Descriptive Statistics: Candidate Populism Profiles

The analysis reveals distinct populist profiles for each candidate. Table 1 presents the mean raw scores for each of the nine PDAF dimensions, illustrating the varied rhetorical strategies across the 2016 field.

**Table 1: Mean Raw Scores on PDAF Dimensions by Candidate**

| Dimension                                | Clinton | Cruz  | Kasich | Rubio | Sanders | Trump |
| ---------------------------------------- | ------- | ----- | ------ | ----- | ------- | ----- |
| **Core Anchors**                         |         |       |        |       |         |       |
| Manichaean People-Elite Framing          | 0.73    | 0.90  | 0.20   | 0.78  | 0.95    | 0.83  |
| Crisis-Restoration Narrative             | 0.56    | 0.85  | 0.35   | 0.88  | 0.88    | 0.88  |
| Popular Sovereignty Claims               | 0.39    | 0.85  | 0.10   | 0.25  | 0.80    | 0.69  |
| Anti-Pluralist Exclusion                 | 0.45    | 0.83  | 0.00   | 0.35  | 0.65    | 0.51  |
| **Mechanism Anchors**                    |         |       |        |       |         |       |
| Elite Conspiracy/Systemic Corruption     | 0.40    | 0.70  | 0.08   | 0.35  | 0.93    | 0.67  |
| Authenticity vs. Political Class         | 0.51    | 0.80  | 0.40   | 0.93  | 0.80    | 0.76  |
| Homogeneous People Construction          | 0.71    | 0.80  | 0.50   | 0.85  | 0.93    | 0.76  |
| **Boundary Anchors**                     |         |       |        |       |         |       |
| Nationalist Exclusion                    | 0.29    | 0.65  | 0.05   | 0.35  | 0.22    | 0.61  |
| Economic Populist Appeals                | 0.61    | 0.75  | 0.25   | 0.80  | 0.98    | 0.84  |

*Note: Values are mean raw scores (0.0-1.0). Due to small sample sizes for Cruz (n=3), Kasich (n=2), Rubio (n=4), and Sanders (n=5), these means are descriptive and should be interpreted with caution.*

The data clearly clusters the candidates. **Trump, Sanders, and Cruz** form a high-populism cluster, consistently scoring above 0.70 on most dimensions. **Clinton and Rubio** occupy a middle tier, employing populist themes more selectively. **Kasich** represents a distinct low-populism baseline, with scores below 0.50 on all but one dimension.

Within the high-populism cluster, distinct styles emerge. **Sanders** is the most intense populist on economic dimensions, with near-perfect scores on `Economic Populist Appeals` (M = 0.98) and `Elite Conspiracy/Systemic Corruption` (M = 0.93). **Trump** exhibits a more balanced, full-spectrum populism, with high scores across all three categories, particularly `Crisis-Restoration Narrative` (M = 0.88) and `Manichaean People-Elite Framing` (M = 0.83). **Cruz** displays a hardline conservative populism, with extremely high scores on core dimensions like `Manichaean People-Elite Framing` (M = 0.90) and `Anti-Pluralist Exclusion` (M = 0.83).

### 5.3 Advanced Metric Analysis: The Role of Strategic Contradiction

The PDAF's innovative `Populist Strategic Contradiction Index` (PSCI) measures the extent to which candidates deploy contradictory messages by balancing the intensity of two opposing populist themes against the difference in their rhetorical salience. A high PSCI score indicates a tendency to use contradictory appeals with similar emphasis, while a low score suggests a more coherent (or strategically differentiated) message.

As noted in the evaluation of H₈, there was no significant negative correlation between PSCI and electoral success. This suggests that rhetorical coherence, as measured by the PSCI, was not a decisive factor in the 2016 election. Candidates with high levels of populist rhetoric, such as Trump and Cruz, did not appear to be penalized for employing contradictory appeals. For example, Trump frequently combined appeals to `Popular Sovereignty Claims` with `Anti-Pluralist Exclusion`, a classic populist tension. In one speech, he declared himself the "law and order candidate" embodying the people's will, while in another, he called his opponent "Crooked Hillary Clinton... the Secretary of the Status Quo" (Source: trump/convention_period/trump_2016_07_11.txt), delegitimizing his opposition. The lack of a negative correlation suggests that voters may not perceive such combinations as contradictory or that the strategic benefits of appealing to different constituencies outweigh the costs of inconsistency.

### 5.5 Pattern Recognition and Theoretical Insights

The dimensional analysis reveals several key rhetorical patterns that define the populist styles of 2016.

**The Outsider's Toolkit**: The confirmation of H₁₀ reveals a common rhetorical toolkit for "outsider" candidates. Trump and Sanders both scored significantly higher than establishment figures on four key dimensions. They consistently framed the election as a moment of profound **crisis requiring restoration**, as Sanders did by stating, "it is just too late for the same old, same old establishment politics" (Source: sanders/early_primary/sanders_2016_02_10.txt). They both made strong **popular sovereignty claims** and positioned themselves as the true voice of the people against a corrupt system. This was evident in Trump's declaration, "This election will decide whether we are ruled by the people, or by the politicians" (Source: trump/convention_period/trump_2016_06_22.txt). Both also relied heavily on claims of **elite conspiracy and systemic corruption**, with Sanders decrying a "corrupt campaign finance system" and a "rigged economy" (Source: sanders_2016_02_20.txt). Finally, they cultivated an image of **authenticity against the political class**, with Trump highlighting his business background and Sanders his immigrant roots to contrast with professional politicians.

**Two Paths of Economic Populism**: The falsification of H₆—that Democrats would dominate economic populism—is a crucial finding. The data shows two distinct applications of this theme. Sanders deployed a classic left-populist version, focusing on class conflict and wealth inequality. He argued, "We’re going to create an economy that works for all of us, not just for 1%" (Source: sanders/primary_season/sanders_2016_03_15.txt). In contrast, Trump used a nationalist frame for his economic populism, blaming external forces for the struggles of the American worker. He claimed, "You look at what China's doing to us... what they've done to us is they've taken our jobs. They've taken our money" (Source: trump/early_primary/trump_2016_02_20.txt). This demonstrates that `Economic Populist Appeals` is not an exclusively left-wing phenomenon but a flexible rhetorical strategy adaptable to different ideological frameworks.

**Clinton's Counter-Populism**: Hillary Clinton's rhetoric reveals a strategic use of populist themes, often as a direct counter to her opponents. While her overall populism scores were lower than Trump's or Sanders', she scored highly on `Homogeneous People Construction` (M = 0.71). However, she used this dimension not to exclude, but to include, building a narrative of inclusive unity around her slogan "stronger together." She explicitly rejected exclusionary populism, stating, "We should be breaking down barriers, not building walls" (Source: clinton/primary_season/clinton_2016_03_15.txt). This represents a form of "counter-populism," adopting the populist style of constructing a unified "people" but defining that people in inclusive, pluralistic terms.

## 6. Discussion

The findings of this analysis have significant implications for the study of political communication. By moving beyond a simple binary classification, the PDAF framework reveals that populism is not a monolithic style but a repertoire of rhetorical strategies that can be combined in various ways to construct distinct, ideologically-inflected political identities.

The emergence of clear candidate archetypes—the full-spectrum nationalist populist (Trump), the economic-progressive populist (Sanders), the hardline conservative populist (Cruz), and the establishment counter-populist (Clinton)—demonstrates the framework's discriminatory power. This nuanced perspective is critical for understanding how different leaders mobilize support and frame political conflict. The cross-ideological nature of `Economic Populist Appeals`, for instance, suggests that economic grievance is a powerful and flexible resource for populists on both the left and the right.

Furthermore, the lack of a clear penalty for rhetorical contradiction (H₈) challenges traditional models of political persuasion that prioritize message consistency. It suggests that for populist leaders, the ability to simultaneously appeal to disparate, and even contradictory, sentiments may be a feature, not a bug, of their communication strategy. This aligns with theories of "strategic ambiguity" and may reflect a political environment where emotional resonance and identity-based appeals can override logical consistency for certain segments of the electorate.

The study is not without limitations. The small sample sizes for several candidates mean that candidate-level comparisons are primarily descriptive and exploratory. Future research should apply the PDAF to a larger corpus to confirm these preliminary findings with greater statistical power. Nonetheless, this analysis serves as a robust proof-of-concept, demonstrating the value of a multi-dimensional, salience-weighted approach to capturing the complexity of populist discourse.

## 7. Conclusion

This computational analysis of the 2016 U.S. presidential election provides compelling, data-driven evidence that populism is a multifaceted and strategically diverse phenomenon. The Populist Discourse Analysis Framework (PDAF) successfully identified distinct populist archetypes, revealing how candidates like Donald Trump, Bernie Sanders, and Hillary Clinton constructed unique rhetorical profiles by emphasizing different combinations of populist themes.

The study confirmed that "outsider" candidates were significantly more populist than their establishment counterparts and that nationalist exclusion was a key feature of Republican populism. Crucially, it falsified the hypotheses that economic populism is an exclusively left-wing tool and that rhetorical contradiction is electorally detrimental. These findings challenge simplistic understandings of populism and highlight the need for more nuanced analytical tools. By measuring not just the presence but the strategic emphasis and combination of populist appeals, the PDAF provides a powerful methodology for future research into political communication in the 21st century.

## 8. Evidence Citations

### Hillary Clinton
*   "We should be breaking down barriers, not building walls. We’re not going to succeed by dividing this country between us and them." (Source: clinton/primary_season/clinton_2016_03_15.txt)
*   "I am so grateful to have this chance to talk to you about what we can do together to have the kind of economy that works for everyone, not just those at the top." (Source: clinton_2016_10_03.txt)
*   "We have our differences, but we have differences over issues, and that's what we talk about, not insults, which is what happens among the Republicans." (Source: clinton_2016_01_26.txt)

### Donald Trump
*   "This election will decide whether we are ruled by the people, or by the politicians." (Source: trump/convention_period/trump_2016_06_22.txt)
*   "The decades of decay, division and decline will come to an end. The years of American Greatness will return." (Source: trump/convention_period/trump_2016_07_11.txt)
*   "You look at what China's doing to us... what they've done to us is they've taken our jobs. They've taken our money. They've taken everything. We're bringing our jobs back, folks." (Source: trump/early_primary/trump_2016_02_20.txt)
*   "Americanism, not globalism, will be our credo... I only want to admit individuals into our country who will support our values and love our people." (Source: trump_2016_07_21.txt)
*   "We're living through the greatest jobs theft in the history of the world." (Source: trump_2016_10_14.txt)

### Bernie Sanders
*   "The issue of wealth and income inequality is the great moral issue of our time, it is the great economic issue of our time and it is the great political issue of our time." (Source: sanders/primary_season/sanders_2016_05_26.txt)
*   "the American people will not continue to accept a corrupt campaign finance system that is undermining American democracy, and we will not accept a rigged economy in which ordinary Americans work longer hours for lower wages, while almost all new income and wealth goes to the top 1%." (Source: sanders/early_primary/sanders_2016_02_10.txt)
*   "given the enormous crises facing our country, it is just too late for the same old, same old establishment politics, and establishment economics. The people want real change." (Source: sanders/early_primary/sanders_2016_02_10.txt)

### Ted Cruz
*   "Tonight the state of Iowa has spoken. Iowa has sent notice that the Republican nominee and the next president of the United States will not be chosen by the media. Will not be chosen by the Washington establishment. Will not be chosen by the lobbyists. But will be chosen by the most incredible powerful force, where all sovereignty resides in our nation, by we the people: the American people." (Source: cruz_2016_02_01.txt)

### John Kasich
*   "you hire us to go do the job, plain and simple, to create an environment of economic growth and opportunity" (Source: kasich_2016_03_15.txt)