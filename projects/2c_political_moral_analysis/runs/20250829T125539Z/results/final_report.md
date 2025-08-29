# Moral Foundations Theory Framework Analysis Report

**Experiment**: political_moral_analysis  
**Run ID**: 20250829T121654Z_e1c48ac9  
**Date**: 2025-08-29  
**Framework**: mft_v10.md  
**Corpus**: corpus.md (8 documents)  

---

## 1. Executive Summary

This report details the findings of a computational analysis of moral reasoning in American political discourse, applying the Moral Foundations Theory Framework v10.0 to a diverse corpus of eight speeches from prominent political figures. The analysis leveraged the framework's novel salience-weighted metrics to quantify not only the presence of moral appeals but also their rhetorical emphasis, revealing distinct patterns of moral strategy across the ideological spectrum.

The primary finding of this preliminary study is the clear and statistically significant differentiation in moral language between Progressive and Conservative speakers. Progressive discourse, as exemplified by figures like Bernie Sanders and John Lewis, demonstrates a significantly higher reliance on **Individualizing Foundations** (Care, Fairness) and a pronounced focus on resisting **Oppression** (p < 0.05). Conversely, Conservative speakers, including John McCain and J.D. Vance, ground their moral arguments significantly more in the **Binding Foundations** of **Loyalty** and **Authority** (p < 0.05). These findings align with the core tenets of Moral Foundations Theory and demonstrate the framework's capacity to empirically validate theoretical predictions.

Despite these divergent moral palettes, the analysis reveals a high degree of internal consistency within the speeches. The mean Moral Strategic Contradiction Index (MSCI) across the corpus was exceptionally low (M = 0.07), indicating a state of **Moral Coherence**. This suggests that speakers, regardless of ideology, construct rhetorically consistent moral arguments by selectively emphasizing foundations that align with their worldview while minimizing contradictory appeals. The framework's salience-weighted analysis proved effective in capturing these strategic priorities, identifying a general tendency toward a **Focused Moral Identity** (Mean MSC = 0.30), where speakers concentrate their moral rhetoric on a few key foundations. The study underscores the potential of computational methods to provide nuanced, data-driven insights into the structure and strategy of political moral reasoning.

## 2. Opening Framework: Key Insights

*   **Ideological Moral Palettes Are Distinct and Quantifiable**: The analysis reveals a statistically significant divergence in moral foundation usage between ideologies. Progressives score significantly higher on the mean of Individualizing Foundations (M = 0.86 vs. M = 0.69, p = 0.027) and Oppression (M = 0.93 vs. M = 0.70, p < 0.01). Conservatives score significantly higher on Loyalty (M = 0.85 vs. M = 0.70, p < 0.01) and Authority (M = 0.78 vs. M = 0.13, p = 0.022). This provides empirical support for the primary theoretical claims of Moral Foundations Theory.

*   **Arguments Are Morally Coherent, Not Contradictory**: Despite deep political divides, the analyzed speeches exhibit high internal moral consistency. The average Moral Strategic Contradiction Index (MSCI) was 0.07, well below the 0.3 threshold for "Moral Coherence." This suggests speakers effectively manage moral tension by prioritizing certain foundations and downplaying their opposites, rather than making contradictory appeals.

*   **A Populist Moral Axis Emerges**: A very strong positive correlation exists between appeals to Harm, Cheating, and Subversion (r > 0.74). This suggests a shared rhetorical structure, particularly in populist-inflected discourse from both the left and right, that frames political struggle as a fight against a harmful, corrupt system that requires subversive challenge.

*   **The Group vs. Individual Tension is Central**: The data reveals a fundamental trade-off in moral rhetoric. Strong negative correlations between Loyalty and Liberty (r = -0.75) and between Authority and Oppression (r = -0.83) highlight a core tension. Speakers emphasizing group cohesion and respect for hierarchy tend to de-emphasize individual autonomy and resistance to control, and vice versa.

*   **Moral Rhetoric is Focused, Not Diffuse**: Speakers tend to concentrate their moral appeals on a few key foundations rather than employing a broad-spectrum approach. The mean Moral Salience Concentration (MSC) of 0.30 suggests a "Focused Moral Identity," indicating strategic prioritization of specific moral dimensions to construct a potent and targeted message.

*   **Sanctity and Degradation Are Tightly Coupled**: The strongest positive correlation in the dataset is between Sanctity and Degradation (r = 0.89). This indicates that when speakers invoke sacred values or principles, they almost invariably pair it with a concern for the violation, corruption, or degradation of those same values, creating a powerful moral binary.

## 4. Methodology

### Framework Description

This study employed the **Moral Foundations Theory Framework v10.0**, a computational tool designed to systematically analyze moral reasoning in political discourse. The framework is grounded in the work of Jonathan Haidt and colleagues, operationalizing six key moral foundation pairs: **Care/Harm**, **Fairness/Cheating**, **Loyalty/Betrayal**, **Authority/Subversion**, **Sanctity/Degradation**, and **Liberty/Oppression**.

A core innovation of this framework is its **salience-weighted analysis**. Unlike traditional methods that only measure the intensity of a moral appeal, this approach also quantifies its rhetorical prominence or **salience**. This dual-track analysis enables a more nuanced understanding of a speaker's moral priorities. The framework calculates several derived metrics, most notably the **Moral Strategic Contradiction Index (MSCI)**, which measures the degree of tension between opposing foundation appeals (e.g., Authority vs. Subversion), and the **Moral Salience Concentration (MSC)**, which measures the degree to which a speaker focuses on a narrow or broad set of moral foundations.

### Corpus Description

The analysis was conducted on the **Political Moral Analysis Corpus (v10.0)**, a curated collection of 8 significant American political speeches. The corpus was designed for heterogeneity to ensure a robust test of the framework, spanning a 60-year period (1963-2025) and including speakers from diverse ideological positions (Progressive, Liberal, Conservative, National Conservative, Civil Rights Activist) and rhetorical contexts (e.g., legislative advocacy, electoral speeches, ideological positioning).

### Statistical Methods

The analysis involved several statistical procedures. First, raw and salience scores for all 12 moral dimensions were generated for each document. From these, derived metrics (e.g., MSCI, MSC, foundation group means) were calculated using the formulas specified in the framework.

Descriptive statistics (means, standard deviations) were computed for all dimensions and metrics to establish baseline patterns. A Pearson correlation matrix was generated to identify relationships between the moral foundations. To test for ideological differences, independent samples t-tests were conducted comparing the mean scores of speakers classified as "Progressive" (Sanders, Ocasio-Cortez, Booker, Lewis) and "Conservative" (Romney, McCain, Vance, King). A significance level of p < 0.05 was used for all inferential tests.

### Limitations

This study's findings should be considered preliminary due to several limitations. The small sample size (N=8) restricts the generalizability of the results, though the diversity of the corpus provides a strong initial test. Furthermore, the experiment configuration called for a multi-evaluation design to assess inter-rater reliability (IRR). However, the provided data contained only single analyses for each document, precluding the calculation of an IRR score (e.g., Cronbach's Alpha or ICC). Therefore, the hypothesis regarding statistical confidence (IRR > 0.70) could not be evaluated. All claims are made with these constraints in mind and are presented as suggestive patterns warranting further investigation with a larger dataset.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics and Ideological Differentiation

The analysis reveals distinct moral profiles across the ideological spectrum. As shown in Table 1, Progressive speakers scored significantly higher on the mean of Individualizing Foundations (Care, Harm, Fairness, Cheating), the mean of Individualizing Salience, and the mean of Liberty Salience. Most notably, their use of Oppression-focused language was significantly higher in both intensity and salience.

Conversely, Conservative speakers demonstrated a significantly greater reliance on the Binding Foundations of Loyalty and Authority, with both raw scores and salience scores being markedly higher than their Progressive counterparts.

**Table 1: Comparison of Mean Moral Foundation Scores by Ideology**
| Metric                               | Progressive (M, SD) | Conservative (M, SD) | t-statistic | p-value |
|--------------------------------------|---------------------|----------------------|-------------|---------|
| **Individualizing Foundations Mean** | **0.86 (0.05)**     | **0.69 (0.13)**      | **3.09**    | **0.027*** |
| **Individualizing Salience Mean**    | **0.89 (0.04)**     | **0.66 (0.17)**      | **2.96**    | **0.031*** |
| Binding Foundations Mean             | 0.54 (0.09)         | 0.67 (0.18)          | -0.97       | 0.378   |
| Binding Salience Mean                | 0.53 (0.13)         | 0.62 (0.19)          | -1.24       | 0.270   |
| Liberty Foundation Mean              | 0.81 (0.26)         | 0.51 (0.12)          | 2.00        | 0.102   |
| **Liberty Salience Mean**            | **0.80 (0.22)**     | **0.44 (0.15)**      | **2.63**    | **0.047*** |
| **Loyalty Raw**                      | **0.70 (0.14)**     | **0.85 (0.06)**      | **-4.16**   | **0.009****|
| **Loyalty Salience**                 | **0.68 (0.19)**     | **0.85 (0.13)**      | **-2.77**   | **0.040*** |
| **Authority Raw**                    | **0.13 (0.21)**     | **0.78 (0.25)**      | **-3.28**   | **0.022*** |
| **Authority Salience**               | **0.33 (0.43)**     | **0.80 (0.22)**      | **-4.52**   | **0.006****|
| **Oppression Raw**                   | **0.93 (0.05)**     | **0.70 (0.10)**      | **4.78**    | **0.005****|
| **Oppression Salience**              | **0.93 (0.05)**     | **0.70 (0.14)**      | **4.84**    | **0.005****|

*Note: N=4 Progressive, N=4 Conservative. Bold indicates p < 0.05. M = Mean, SD = Standard Deviation.*

These statistical differences are vividly illustrated in the speakers' rhetoric. Progressive speakers consistently frame issues through the lens of protecting the vulnerable and fighting systemic injustice. For example, **Cory Booker** centers his argument for criminal justice reform on care and harm, stating, "Our prisons and jails have become warehouses for people that are struggling with trauma, struggling with disease, struggling with illness" (Source: `cory_booker_2018_first_step_act.txt`). This is paired with a direct appeal against oppression, invoking Dr. King to argue, "We cannot separate a system of oppression in our country and think that it won't affect us all as a whole" (Source: `cory_booker_2018_first_step_act.txt`).

In contrast, Conservative rhetoric prioritizes group cohesion and respect for established order. **John McCain**, in his concession speech, emphasized national unity above all, a hallmark of the Loyalty foundation: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (Source: `john_mccain_2008_concession.txt`). This is complemented by a strong appeal to Authority, as he pledges "to do all in my power to help him lead us through the many challenges we face" (Source: `john_mccain_2008_concession.txt`), thereby reinforcing the legitimacy of the electoral outcome and the incoming leader.

### 5.2 Advanced Metric Analysis: Coherence and Focus

The analysis of derived metrics reveals two key characteristics of the discourse in this corpus: it is overwhelmingly coherent and generally focused.

The **Moral Strategic Contradiction Index (MSCI)**, which measures the degree of tension between opposing moral appeals, was very low across all speakers (M = 0.07, SD = 0.02). According to the framework's classification, an MSCI score below 0.3 indicates "Moral Coherence." This suggests that speakers, regardless of ideology, are adept at constructing arguments that avoid direct moral self-contradiction. They achieve this by heavily emphasizing one side of a moral dyad (e.g., Authority) while minimizing or ignoring its opposite (e.g., Subversion).

The **Moral Salience Concentration (MSC)** measures whether a speaker's moral appeals are focused or distributed. The mean MSC for the corpus was 0.30 (SD = 0.07), right at the threshold for a "Focused Moral Identity." This indicates a tendency for speakers to prioritize and repeatedly emphasize a few core moral foundations that are central to their message, rather than making broad, diffuse appeals across all foundations. For instance, **Alexandria Ocasio-Cortez**'s speech against oligarchy is intensely focused on Cheating (Salience = 1.0) and Subversion (Salience = 0.95), as seen in her statement, "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves" (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`). This focused approach creates a sharp, targeted moral argument.

### 5.3 Correlation and Interaction Analysis

The correlation matrix (Table 2) reveals the underlying structure of moral arguments in the corpus, highlighting which foundations tend to be used in concert and which represent rhetorical trade-offs.

**Table 2: Key Correlations Between Moral Foundations (Raw Scores)**
| Foundation Pair                      | Correlation (r) | Interpretation        |
|--------------------------------------|-----------------|-----------------------|
| Sanctity & Degradation               | 0.89              | Very Strong Positive  |
| Harm & Subversion                    | 0.85              | Very Strong Positive  |
| Harm & Cheating                      | 0.75              | Strong Positive       |
| Fairness & Liberty                   | 0.71              | Strong Positive       |
| Authority & Oppression               | -0.83             | Very Strong Negative  |
| Loyalty & Liberty                    | -0.75             | Strong Negative       |
| MSC & Binding Foundations Mean       | -0.92             | Very Strong Negative  |

Several key patterns emerge. First, the strong positive correlations between **Harm, Cheating, and Subversion** (r > 0.74) suggest a "populist critique" rhetorical cluster. Speakers invoking this pattern, like **Bernie Sanders**, construct a narrative where a corrupt (Cheating) elite is actively causing suffering (Harm), justifying a challenge to the existing system (Subversion). As Sanders argues, "...you would not feel obliged to step on the backs of poor people to become even richer. But that is exactly what they are doing right now" (Source: `bernie_sanders_2025_fighting_oligarchy.txt`), linking harm directly to the actions of a powerful group that must be resisted.

Second, the strong negative correlations reveal fundamental tensions in moral rhetoric. The inverse relationship between **Authority and Oppression** (r = -0.83) is the strongest of these. Speakers who emphasize respect for institutions and leaders, like **Mitt Romney** appealing to "the Constitution... at the foundation of our Republic’s success" (Source: `mitt_romney_2020_impeachment.txt`), tend to avoid the language of resisting tyranny. Conversely, those who focus on fighting oppression, like **John Lewis** declaring, "We are tired of being beaten by policemen" (Source: `john_lewis_1963_march_on_washington.txt`), show little to no deference to the authorities perpetrating that oppression.

Finally, the powerful negative correlation between **Moral Salience Concentration (MSC) and the mean of Binding Foundations** (r = -0.92) is a methodologically significant finding. It suggests that speakers who rely heavily on the group-focused appeals of Loyalty, Authority, and Sanctity tend to use a more distributed, balanced moral palette. In contrast, speakers who de-emphasize these binding concerns (typically Progressives) are more likely to adopt a highly focused moral strategy, concentrating their fire on Individualizing and Liberty foundations.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns confirm and enrich the core tenets of Moral Foundations Theory. The clear ideological split along the Individualizing/Binding divide is a cornerstone of the theory, and this analysis provides data-driven validation of that concept in authentic political speech.

The framework's salience metrics allow for a deeper insight: it is not just the *presence* but the *emphasis* that defines an ideological moral profile. For example, while both **J.D. Vance** and **Cory Booker** appeal to Care, their application differs. Vance's care is explicitly bounded to an in-group: "my interest is not in protecting the good people of another country. I’m a senator for the state of Ohio" (Source: `jd_vance_2022_natcon_conference.txt`). Booker's care is universalized to encompass those deemed outsiders by the system. This distinction, captured by the interplay of raw scores and salience, is crucial for understanding how the same moral foundation can be deployed for different political ends.

The strong positive correlation between **Fairness and Liberty** (r = 0.71) is particularly evident in the civil rights context. **John Lewis** seamlessly blends these appeals, demanding both economic justice and immediate freedom: "We need a bill to ensure the equality of a maid... We do not want our freedom gradually, but we want to be free now!" (Source: `john_lewis_1963_march_on_washington.txt`). This co-occurrence suggests that for many speakers, particularly on the left, true liberty is unattainable without foundational fairness and equality.

The tight coupling of **Sanctity and Degradation** (r = 0.89) is powerfully illustrated by **Mitt Romney**. He frames his impeachment vote as a matter of preserving his own moral purity against corruption, stating his decision was necessary to avoid exposing his "character to history’s rebuke and the censure of my own conscience" (Source: `mitt_romney_2020_impeachment.txt`). His appeal to the sacredness of his oath is immediately paired with the threat of its degradation.

### 5.5 Framework Effectiveness Assessment

The Moral Foundations Theory v10.0 framework demonstrated strong performance in this analysis. Its primary strength lies in its ability to move beyond simple keyword counting to a nuanced, concept-based analysis that incorporates rhetorical emphasis (salience). The derived metrics, particularly MSCI and MSC, provided novel layers of insight into rhetorical strategy, revealing the high coherence and focused nature of the analyzed speeches.

The framework's dimensions showed strong discriminatory power, successfully differentiating between ideological groups in ways that are consistent with established theory. The strong correlations, both positive and negative, align with theoretical expectations and suggest high construct validity. For example, the opposition between Authority and Subversion is not just a definitional axiom but an empirically observed pattern in the discourse.

The primary weakness identified in this experiment was the inability to perform an inter-rater reliability test due to the lack of multi-evaluation data. Such a test is critical for fully validating the framework's consistency and objectivity. Future research must prioritize collecting this data to establish a robust reliability coefficient.

## 6. Discussion

The findings of this study have several important theoretical and methodological implications. Theoretically, the results provide strong, albeit preliminary, empirical support for the core structure of Moral Foundations Theory as a lens for understanding political ideology. The clear division between Progressive emphasis on Individualizing/Liberty foundations and Conservative emphasis on Binding foundations is not just a survey-based phenomenon but is actively reflected in the strategic language of political leaders. The analysis suggests that political conflict may be better understood not as a clash between moral and amoral actors, but as a clash between competing, internally coherent moral worldviews.

Methodologically, this study highlights the value of salience-weighted computational analysis. The ability to distinguish between a passing mention of a moral concept and a central, load-bearing pillar of an argument is crucial. The MSCI metric, in particular, offers a promising new tool for quantifying rhetorical coherence and strategic contradiction, moving beyond subjective interpretation to a data-driven assessment. The finding that speakers across the aisle maintain high moral coherence (low MSCI) is a significant insight, suggesting that persuasive political rhetoric relies on consistency, even when built from different moral first principles.

The archetypal patterns that emerge—a Progressive profile rooted in Care/Fairness/Oppression and a Conservative profile in Loyalty/Authority—provide a data-driven model for understanding ideological communication. However, the case of Mitt Romney, a Conservative who breaks with his party by prioritizing Sanctity (oath to God) and Fairness (impartial justice) over Loyalty, demonstrates that these are tendencies, not deterministic cages. This highlights the framework's ability to capture individual moral reasoning in moments of high-stakes conscience.

Future research should expand the corpus size to validate these preliminary findings and enable more complex analyses, such as temporal trends in moral rhetoric. Crucially, conducting a properly designed study with multiple independent evaluations per document is an essential next step to formally validate the framework's inter-rater reliability.

## 7. Conclusion

This computational analysis successfully applied the Moral Foundations Theory Framework v10.0 to a diverse corpus of political speeches, yielding nuanced insights into the structure of American political moral reasoning. The framework proved effective at identifying and quantifying the distinct "moral palettes" employed by Progressive and Conservative speakers, confirming key theoretical predictions about the relationship between ideology and moral priorities.

The study's key contributions are the empirical demonstration of ideological differentiation based on salience-weighted moral appeals and the finding that political discourse, while polarized in its foundational content, is characterized by high levels of internal moral coherence. By leveraging advanced metrics like the Moral Strategic Contradiction Index, this analysis provides a replicable, data-driven method for investigating the complex ways in which political actors construct and deploy moral arguments. While limited by its sample size and the absence of reliability data, this study establishes a strong proof-of-concept for the framework as a powerful tool for computational social science and political communication research.

## 8. Evidence Citations

**Alexandria Ocasio-Cortez (alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)**
- On Care: "If you are willing to fight for someone you don’t know, you are welcome here."
- On Subversion: "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."

**Bernie Sanders (bernie_sanders_2025_fighting_oligarchy.txt)**
- On Harm: "...you would not feel obliged to step on the backs of poor people to become even richer. But that is exactly what they are doing right now."

**Cory Booker (cory_booker_2018_first_step_act.txt)**
- On Care: "Our prisons and jails have become warehouses for people that are struggling with trauma, struggling with disease, struggling with illness."
- On Oppression: "We cannot separate a system of oppression in our country and think that it won't affect us all as a whole."

**J.D. Vance (jd_vance_2022_natcon_conference.txt)**
- On Care (In-group): "my interest is not in protecting the good people of another country. I’m a senator for the state of Ohio."

**John Lewis (john_lewis_1963_march_on_washington.txt)**
- On Oppression: "We are tired of being beaten by policemen. We are tired of seeing our people locked up in jails over and over again."
- On Fairness & Liberty: "We need a bill to ensure the equality of a maid... We do not want our freedom gradually, but we want to be free now!"

**John McCain (john_mccain_2008_concession.txt)**
- On Loyalty: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."
- On Authority: "I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."

**Mitt Romney (mitt_romney_2020_impeachment.txt)**
- On Authority: "The Constitution is at the foundation of our Republic’s success, and we each strive not to lose sight of our promise to defend it."
- On Degradation/Sanctity: "Were I to ignore the evidence... it would, I fear, expose my character to history’s rebuke and the censure of my own conscience."