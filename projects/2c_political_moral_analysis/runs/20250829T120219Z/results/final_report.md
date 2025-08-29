# Moral Foundations Theory Framework v10.0 Analysis Report

**Experiment**: political_moral_analysis  
**Date**: 2025-08-29  
**Framework**: mft_v10.md  
**Corpus**: corpus.md (8 documents)  

---

## 1. Executive Summary

This report details a computational analysis of moral reasoning in American political discourse using the Moral Foundations Theory (MFT) v10.0 framework. The study analyzed a diverse corpus of eight speeches from prominent political figures spanning from 1963 to 2025. The framework's novel use of salience-weighted analysis and advanced tension mathematics allowed for a nuanced quantification of moral rhetoric, moving beyond the mere presence of moral appeals to measure their strategic emphasis and internal coherence.

The analysis reveals statistically distinct moral profiles that align with, yet also complicate, traditional ideological labels. Progressive speakers like Bernie Sanders and Alexandria Ocasio-Cortez build their arguments predominantly on the Individualizing foundations of Care/Harm and Fairness/Cheating, with a strong focus on combating Oppression. Conversely, conservative figures like Mitt Romney and J.D. Vance utilize a broader moral palette that heavily incorporates the Binding foundations of Authority, Loyalty, and Sanctity. The data shows a strong positive correlation between appeals to prevent Harm and those to stop Cheating (r = 0.86), suggesting a common rhetorical strategy of framing exploitation as a direct cause of suffering. Furthermore, a strong negative correlation between appeals to Authority and concerns about Oppression (r = -0.78) empirically grounds a key tension in political thought.

The framework's Moral Strategic Contradiction Index (MSCI) demonstrated its utility by identifying high levels of moral coherence across the corpus, with John McCain's 2008 concession speech registering as exceptionally coherent (MSCI = 0.02). The analysis also highlights the framework's ability to identify complex moral identities, such as the populist blend of Individualizing and Binding appeals in the rhetoric of J.D. Vance and the primacy of the Liberty/Oppression axis in John Lewis's 1963 civil rights address. While the framework proved effective at differentiating these moral styles, the study's small sample size (N=8) means these findings should be considered preliminary. A key experimental objective, the validation of inter-rater reliability, could not be completed due to insufficient data.

## 2. Opening Framework: Key Insights

*   **Ideological Moral Palettes Are Quantifiably Distinct**: The analysis confirms that progressive and conservative speakers construct their moral arguments using different foundational building blocks. Progressives (Sanders, Ocasio-Cortez) show a high mean score for Individualizing foundations (M = 0.88) and a moderate mean for Binding foundations (M = 0.47). In contrast, key conservative speakers (Romney, Vance, King) display high means for both Individualizing (M = 0.74) and Binding (M = 0.79) foundations, indicating a broader, more encompassing moral appeal.

*   **The Harm/Cheating Nexus is a Core Rhetorical Strategy**: The strongest positive correlation in the dataset is between the Harm and Cheating foundations (r = 0.86). This indicates that speakers frequently link societal harm directly to systemic unfairness, corruption, and exploitation. As Alexandria Ocasio-Cortez argued, "...the last thing they want us to realize is that the division that is actually hurting our country the most is how endless greed is costing the lives of everyone else" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

*   **The Authority-Oppression Axis Defines a Fundamental Political Tension**: The analysis reveals a strong inverse relationship between appeals to Authority and concerns about Oppression (r = -0.78). Speakers who emphasize respect for institutions and hierarchy, like John McCain, score low on Oppression. Conversely, speakers focused on fighting systemic control, like John Lewis, score low on Authority. This finding empirically maps a central conflict in political discourse.

*   **Moral Coherence is a Measurable Rhetorical Tool**: The Moral Strategic Contradiction Index (MSCI) was consistently low across all speeches (corpus M = 0.09), indicating that political speakers, regardless of ideology, tend to construct internally coherent moral arguments. John McCain's concession speech, designed to foster unity, was a paragon of this, with a near-zero MSCI of 0.02, reflecting its singular focus on Loyalty and Authority.

*   **Populist Rhetoric Blends Individualizing and Binding Morality**: The framework identifies a distinct populist moral signature in speakers like J.D. Vance and Steve King, who score high on both Individualizing (M = 0.76) and Binding (M = 0.76) foundations. They combine appeals to protect their in-group from harm (Care/Harm) with strong appeals to national Loyalty and respect for constitutional Authority, challenging simple liberal-conservative classifications.

*   **Moral Identity Can Be Focused or Distributed**: The Moral Salience Concentration (MSC) metric successfully differentiated rhetorical styles. Bernie Sanders exhibited a "Focused Moral Identity" (MSC = 0.39), concentrating heavily on Fairness/Cheating and Oppression. In contrast, J.D. Vance showed a "Distributed Moral Identity" (MSC = 0.15), engaging more evenly across a wider range of moral foundations to construct his nationalist argument.

## 4. Methodology

### Framework Description

This study employed the **Moral Foundations Theory Framework v10.0**, a computational tool designed to systematically analyze moral reasoning in political discourse. The framework is based on Jonathan Haidt's theory of six moral foundations, which are organized into opposing pairs: Care/Harm, Fairness/Cheating (Individualizing foundations); Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation (Binding foundations); and Liberty/Oppression.

A core innovation of this framework is its **salience-weighted analysis**. Unlike traditional methods that only measure the intensity of a moral appeal, this framework also assesses its rhetorical prominence (salience). This dual-track approach enables a more authentic assessment of a speaker's moral priorities. The framework calculates several derived metrics, most notably the **Moral Strategic Contradiction Index (MSCI)**, which quantifies the degree of tension between opposing moral claims (e.g., appealing to both Authority and Subversion with equal emphasis). Low MSCI scores indicate high moral coherence.

### Corpus Description

The analysis was performed on the **Political Moral Analysis Corpus v10.0**, a curated collection of 8 significant American political speeches. The corpus was designed for heterogeneity to robustly test the framework, featuring:
*   **Ideological Diversity**: Speeches from Progressive (Sanders, Ocasio-Cortez), Liberal (Booker), Conservative (McCain, Romney), National Conservative (Vance), Hardline Conservative (King), and Civil Rights (Lewis) perspectives.
*   **Historical Range**: A 60-year span from 1963 (Lewis) to 2025 (Sanders/Ocasio-Cortez).
*   **Contextual Variety**: The speeches encompass electoral, legislative, policy advocacy, and civil rights contexts.

### Statistical Methods and Limitations

The analysis relied on descriptive statistics (means, standard deviations) and Pearson correlation coefficients to identify patterns in the data. Analysis of variance (ANOVA) was used to compare ideological groups. All statistical results were taken from the provided data file and interpreted as given.

A significant limitation of this study is its small sample size (N=8), which means all findings are preliminary and suggestive, not generalizable. While the experimental design called for two independent evaluations per document to assess inter-rater reliability, the final dataset contained only single evaluations. As a result, a key hypothesis regarding statistical reliability (Expected Outcome 4) could not be tested, and the report explicitly notes an error in the reliability analysis: `{'error': 'Insufficient documents with multiple evaluations for ICC.'}`. This is a critical gap in the validation of the framework's application.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Analysis of the moral foundation scores across the eight documents reveals distinct patterns of usage. The Individualizing foundations of **Fairness** (M = 0.83, SD = 0.13) and **Harm** (M = 0.78, SD = 0.21) were, on average, the most intensely invoked foundations, indicating their broad importance in American political discourse. In contrast, the **Liberty** foundation (M = 0.43, SD = 0.34) was used least frequently on average, though its high standard deviation suggests its importance varies significantly between speakers.

The negative-valence foundations, which focus on preventing a moral violation (e.g., Harm, Cheating, Oppression), generally scored higher than their positive-valence counterparts (e.g., Care, Fairness, Liberty). For instance, **Oppression** (M = 0.70) was invoked more intensely than **Liberty** (M = 0.43), and **Harm** (M = 0.78) more than **Care** (M = 0.69). This suggests that political rhetoric in this corpus is more frequently oriented around preventing negative outcomes than promoting positive ones. The foundation of **Subversion** (SD = 0.42) showed the highest variability, indicating that challenging authority is a highly context-dependent and polarizing rhetorical strategy.

**Table 1: Descriptive Statistics of Moral Foundation Scores (Raw and Salience)**
| Foundation | Mean (Raw) | SD (Raw) | Mean (Salience) | SD (Salience) |
| :--- | :---: | :---: | :---: | :---: |
| **Individualizing** | | | | |
| Care | 0.69 | 0.17 | 0.63 | 0.25 |
| Harm | 0.78 | 0.21 | 0.73 | 0.24 |
| Fairness | 0.83 | 0.13 | 0.80 | 0.16 |
| Cheating | 0.74 | 0.31 | 0.69 | 0.31 |
| **Binding** | | | | |
| Loyalty | 0.66 | 0.19 | 0.63 | 0.27 |
| Betrayal | 0.52 | 0.30 | 0.44 | 0.30 |
| Authority | 0.53 | 0.34 | 0.48 | 0.36 |
| Subversion | 0.68 | 0.42 | 0.64 | 0.40 |
| Sanctity | 0.51 | 0.34 | 0.46 | 0.34 |
| Degradation | 0.63 | 0.28 | 0.54 | 0.25 |
| **Liberty** | | | | |
| Liberty | 0.43 | 0.34 | 0.34 | 0.30 |
| Oppression | 0.70 | 0.37 | 0.64 | 0.37 |

*Note: N=8. Scores range from 0.0 to 1.0.*

### 5.2 Advanced Metric Analysis

The framework's derived metrics provided deeper insights into rhetorical strategy. The **Moral Strategic Contradiction Index (MSCI)**, which measures internal coherence, was exceptionally low across all speeches (M = 0.09), suggesting that these public addresses were crafted to be morally consistent. John McCain's 2008 concession speech was a model of coherence (MSCI = 0.02), almost entirely avoiding contradictory moral claims by focusing squarely on appeals to Authority and national Loyalty. As he stated, "The American people have spoken, and they have spoken clearly," and "Whatever our differences, we are fellow Americans" (Source: john_mccain_2008_concession.txt). This demonstrates a deliberate strategy to project unity and stability.

The **Moral Salience Concentration (MSC)** metric successfully distinguished between focused and distributed moral identities. Bernie Sanders' speech yielded a high MSC score of 0.39, classifying it as a "Focused Moral Identity." His rhetoric concentrated intensely on the Fairness/Cheating and Oppression foundations, as seen in his claim that "there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about" (Source: bernie_sanders_2025_fighting_oligarchy.txt). In contrast, J.D. Vance's speech had a low MSC of 0.15, indicating a "Distributed Moral Identity." He drew more evenly from a wide range of foundations—invoking in-group Loyalty, the sanctity of the nation, and the harm caused by elite policies—to construct a broad nationalist argument.

### 5.3 Correlation and Interaction Analysis

The correlation matrix revealed the underlying structure of moral arguments in the corpus. The strongest relationships highlight common rhetorical pairings and fundamental political tensions.

**Key Positive Correlations:**
*   **Harm & Cheating (r = 0.86)**: This very strong correlation indicates that speakers frequently construct a narrative where harm is the direct result of an unfair or corrupt system. This pattern is central to the progressive speeches. Alexandria Ocasio-Cortez explicitly links the two: "...a certain ugly kind of politics, a politics that involves lying to and screwing over working and middle class Americans so that they can steal from our healthcare..." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).
*   **Betrayal & Subversion (r = 0.84)**: This suggests that calls to challenge authority are often justified by framing existing leaders or systems as having betrayed the people. John Lewis exemplified this when he criticized the federal government for indicting peaceful protestors, a betrayal that justified the "serious social revolution" he advocated (Source: john_lewis_1963_march_on_washington.txt).
*   **Authority & Sanctity (r = 0.80)**: This strong relationship shows that respect for authority is often grounded in sacred or transcendent principles. Mitt Romney's impeachment speech is a clear case, where his deference to the Constitution's authority is inseparable from his religious conviction: "I am profoundly religious. My faith is at the heart of who I am. I take an oath before God as enormously consequential" (Source: mitt_romney_2020_impeachment.txt).

**Key Negative Correlations:**
*   **Authority & Oppression (r = -0.78)**: This strong negative correlation empirically validates a core political axis. Speakers emphasizing respect for institutional order, like John McCain, score high on Authority (0.85) and low on Oppression (0.30). Conversely, those focused on fighting systemic control, like John Lewis, score high on Oppression (1.0) and low on Authority (0.30).
*   **Harm & Loyalty (r = -0.73)**: This relationship suggests a tension between universal concerns about harm and group-specific loyalty. Speakers with a broad focus on preventing harm to all (high Harm score) tend to make fewer appeals to in-group solidarity. Cory Booker's speech on criminal justice reform, which frames the system as causing universal harm that "won't affect us all as a whole," has a high Harm score (0.80) and a moderate Loyalty score (0.60) (Source: cory_booker_2018_first_step_act.txt).

### 5.4 Pattern Recognition and Theoretical Insights

The analysis revealed distinct moral archetypes that both align with and challenge the standard MFT model of liberal-conservative differences.

**The Progressive Profile (Care, Fairness, Oppression):** The speeches by Bernie Sanders and Alexandria Ocasio-Cortez were dominated by the Individualizing foundations. Their combined average score for Individualizing foundations was 0.88, while their average for Binding foundations was only 0.47. Their arguments centered on a narrative of a corrupt elite (Cheating) inflicting damage (Harm) on the populace, which necessitates a fight against systemic control (Oppression). Ocasio-Cortez's declaration, "We are witnessing an oligarchy in America... [which] destroy[s] the public good to enrich themselves while millions of Americans pay the price," is the quintessential expression of this moral framework (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

**The Conservative Profile (Authority, Loyalty, Sanctity):** Mitt Romney's impeachment speech provides a powerful example of conservative moral reasoning, with a Binding foundations mean of 0.87. His decision was framed not through partisan loyalty but through a higher loyalty to sacred principles. He argued that violating his oath would "expose my character to history’s rebuke and the censure of my own conscience," grounding his actions in the foundations of Sanctity, Authority (of the Constitution), and Loyalty (to country over party) (Source: mitt_romney_2020_impeachment.txt).

**The Populist Profile (A Blend of Foundations):** The framework's classifications revealed that speakers like J.D. Vance and Steve King do not fit neatly into the traditional conservative profile. They score high on both Individualizing (M = 0.76) and Binding (M = 0.76) foundations. Vance's speech is a prime example, combining appeals to in-group Loyalty ("American leaders should look out for Americans") with arguments about the Harm caused by immigration and the Cheating perpetrated by elites who abuse asylum laws (Source: jd_vance_2022_natcon_conference.txt). This blend of moral appeals is characteristic of a populist strategy that defines a virtuous in-group (the people) suffering at the hands of a corrupt out-group (the elite).

**The Libertarian/Civil Rights Profile (Liberty, Oppression):** John Lewis's 1963 speech stands apart, with perfect scores of 1.0 in Liberty, Oppression, Harm, and Subversion. His moral argument was almost singularly focused on the demand for freedom and the fight against an oppressive state. His cry, "We do not want our freedom gradually, but we want to be free now!" highlights the primacy of the Liberty/Oppression foundation, which in this context of civil rights, becomes the central axis of moral concern, overshadowing other foundations (Source: john_lewis_1963_march_on_washington.txt).

### 5.5 Framework Effectiveness Assessment

The MFT v10.0 framework demonstrated significant discriminatory power. It successfully differentiated the moral rhetoric of speakers from diverse ideological backgrounds, historical eras, and political contexts. The salience and tension metrics provided a more nuanced picture than simple intensity scores, revealing the strategic architecture of moral arguments. For example, it correctly identified the extreme coherence of McCain's concession speech and the focused anti-oligarchy rhetoric of Sanders.

However, the analysis also revealed limitations. The automated ideological classification (`classify_ideological_profile`) proved too rigid. Its strict thresholds failed to capture the nuances of the data, misclassifying several speakers. For example, Romney's speech, which clearly emphasizes Binding foundations (M=0.87) over Individualizing ones (M=0.70), was labeled "Balanced" rather than "Conservative" because his Individualizing score did not fall below the strict 0.4 threshold. This suggests the classification rules require refinement to account for more complex moral profiles like populism. The most significant methodological failure was the inability to perform an inter-rater reliability analysis, which remains a critical next step for validating the framework's application by automated agents.

## 6. Discussion

The findings from this analysis have several important theoretical implications for Moral Foundations Theory and the study of political discourse. The data largely supports the core MFT hypothesis that liberals (progressives in this corpus) emphasize Individualizing foundations while conservatives utilize Binding foundations more heavily. However, the results also introduce critical nuance.

First, the emergence of a "populist" moral profile, characterized by high scores on *both* Individualizing and Binding foundations, suggests that some political strategies work by activating a broad spectrum of moral intuitions simultaneously. Speakers like J.D. Vance and Steve King build a moral case that their in-group is being harmed and treated unfairly (Individualizing) while also being betrayed by elites who subvert the nation's sacred authority (Binding). This hybrid moral appeal may be a key feature of contemporary nationalist populism and warrants further investigation with a larger corpus.

Second, the unique profile of John Lewis's 1963 speech, with its overwhelming focus on the Liberty/Oppression axis, underscores that historical and social context can elevate certain foundations to a position of temporary primacy. For the Civil Rights Movement, the fight for freedom was not merely one moral concern among many but the central organizing principle of their entire political existence. This suggests that while MFT provides a useful menu of moral foundations, the relative importance of each is highly dynamic and context-dependent.

Finally, the framework's salience and tension metrics represent a significant methodological advance. By measuring not just what is said but how much it is emphasized, the analysis moves closer to understanding the speaker's genuine moral priorities. The consistently low MSCI scores suggest that, at least in prepared public speeches, politicians are adept at avoiding overt moral contradictions. Future research could apply this metric to more spontaneous forms of communication, such as interviews or debates, to see if moral tension increases. The strong correlations found, such as Harm/Cheating and Authority/Sanctity, provide an empirical map of the "moral grammar" used in American politics, revealing which concepts are most naturally linked in persuasive rhetoric.

## 7. Conclusion

This computational analysis, guided by the Moral Foundations Theory v10.0 framework, successfully identified and quantified distinct patterns of moral reasoning in a diverse sample of American political speeches. The framework's innovative use of salience and tension metrics enabled a nuanced assessment that confirmed broad ideological patterns, revealed complex populist moral strategies, and highlighted the contextual primacy of certain foundations, such as Liberty in the Civil Rights Movement. The data points to strong, coherent rhetorical structures, particularly the linking of harm with cheating and authority with sanctity.

Despite the preliminary nature of these findings due to the small sample size and the inability to confirm inter-rater reliability, this study serves as a robust proof-of-concept. It demonstrates that computational methods can move beyond simple content analysis to map the strategic and psychological architecture of moral persuasion. Future research should apply this framework to a larger, longitudinal corpus to validate these archetypes, track the evolution of moral rhetoric over time, and further refine the automated classification of complex political ideologies.

## 8. Evidence Citations

**Alexandria Ocasio-Cortez (alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)**
*   "...the last thing they want us to realize is that the division that is actually hurting our country the most is how endless greed is costing the lives of everyone else."
*   "...a certain ugly kind of politics, a politics that involves lying to and screwing over working and middle class Americans so that they can steal from our healthcare..."
*   "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."

**Bernie Sanders (bernie_sanders_2025_fighting_oligarchy.txt)**
*   "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."

**Cory Booker (cory_booker_2018_first_step_act.txt)**
*   "Dr. King said justice is indivisible, and he was right. We cannot separate a system of oppression in our country and think that it won't affect us all as a whole."

**J.D. Vance (jd_vance_2022_natcon_conference.txt)**
*   "The very, very basic and simple principle that American leaders should look out for Americans."

**John Lewis (john_lewis_1963_march_on_washington.txt)**
*   "My friends, let us not forget that we are involved in a serious social revolution."
*   "We do not want our freedom gradually, but we want to be free now!"
*   "In its present form, this bill will not protect the citizens of Danville, Virginia, who must live in constant fear of a police state."

**John McCain (john_mccain_2008_concession.txt)**
*   "The American people have spoken, and they have spoken clearly."
*   "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

**Mitt Romney (mitt_romney_2020_impeachment.txt)**
*   "I am profoundly religious. My faith is at the heart of who I am. I take an oath before God as enormously consequential."
*   "Were I to ignore the evidence that has been presented and disregard what I believe my oath and the Constitution demands of me for the sake of a partisan end, it would, I fear, expose my character to history’s rebuke and the censure of my own conscience."