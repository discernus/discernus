# Populist Discourse Analysis Framework Analysis Report

**Experiment**: vanderveen_presidential_pdaf_replication  
**Run ID**: [run_id_placeholder]  
**Date**: 2025-08-31  
**Framework**: pdaf_v10_vdv.md  
**Corpus**: corpus.md (57 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of populist discourse in 57 speeches from the 2016 U.S. presidential campaign, utilizing the Populist Discourse Analysis Framework (PDAF) v10.0.0. The study examined rhetoric from six candidates (Trump, Clinton, Sanders, Cruz, Rubio, Kasich) to identify distinct populist styles and test hypotheses regarding candidate, party, and strategic differences. The analysis reveals that a simple monolithic view of populism is insufficient to capture the nuanced rhetorical strategies employed. A one-way ANOVA found no statistically significant difference in the overall salience-weighted populism scores among the candidates (F(5, 46) = 0.84, p = 0.53), refuting the idea that some candidates were simply "more populist" than others.

However, a deeper dimensional analysis uncovers the central finding: the 2016 campaign was a clash of distinct populist *archetypes*. A significant cleavage emerged between "outsider" candidates (Trump, Sanders) and "establishment" figures. Outsiders scored significantly higher on dimensions of **Popular Sovereignty Claims** (p < .001), **Elite Conspiracy/Systemic Corruption** (p = .007), **Authenticity vs. Political Class** (p = .009), and **Nationalist Exclusion** (p < .001). This suggests that anti-establishment positioning was a key rhetorical differentiator. Furthermore, a strong partisan divide was evident in boundary-drawing rhetoric; Republican candidates scored significantly higher on **Nationalist Exclusion** than Democrats (p < .001, d = 1.58), a large effect. Contrary to hypothesis H6, **Economic Populist Appeals** were a cross-party phenomenon, with no significant difference between Democrats (M = 0.71) and Republicans (M = 0.71).

The study also tested the PDAF's novel **Populist Strategic Contradiction Index (PSCI)**, finding no significant correlation between rhetorical contradiction and electoral success (r = 0.07, p = 0.61), challenging the hypothesis that rhetorical consistency is linked to political viability. The PDAF framework demonstrated good internal reliability (Cronbach's α = 0.83) and proved effective in discriminating between different *styles* of populist appeal, highlighting its value in moving beyond binary classification to a more nuanced, multi-dimensional understanding of political discourse.

## 2. Opening Framework: Key Insights

*   **Overall Populism Scores Are Deceiving; Dimensional Styles Are Key:** The analysis found no statistically significant difference in the aggregate `Salience-Weighted Overall Populism Index` across the six candidates (p = 0.53). This crucial finding indicates that a simple measure of "more" or "less" populist is inadequate. The true story lies in *how* candidates construct their populist appeals, revealing distinct rhetorical strategies masked by the overall average.
*   **"Outsider" Status is a Powerful Rhetorical Differentiator:** The most significant patterns emerged when grouping candidates by "outsider" vs. "establishment" status. Outsiders (Trump, Sanders) scored significantly higher on four key dimensions: **Popular Sovereignty Claims** (p < .001), **Elite Conspiracy/Systemic Corruption** (p = .007), **Authenticity vs. Political Class** (p = .009), and **Nationalist Exclusion** (p < .001). This suggests that a core element of 2016 populism was a shared anti-establishment posture, regardless of ideology.
*   **Nationalist Exclusion is a Uniquely Republican Populist Tool:** While populism crossed party lines, the use of nationalist boundary-drawing did not. Republican candidates scored significantly higher on the **Nationalist Exclusion** dimension than their Democratic counterparts (p < .001), with a large effect size (d = 1.58). This indicates that while both parties used populist appeals, the specific strategy of defining the "people" against external cultural or national threats was a hallmark of Republican rhetoric in this campaign.
*   **Economic Populism is a Bipartisan Strategy:** Contrary to the hypothesis that Democrats would score higher on economic populism, the analysis found no significant difference between the parties on the **Economic Populist Appeals** dimension (p = 0.98). The mean scores were nearly identical (M_dem = 0.71, M_rep = 0.71), indicating that framing economic issues as a struggle between ordinary people and economic elites was a common, bipartisan rhetorical strategy.
*   **Rhetorical Contradiction Does Not Correlate with Electoral Success:** The PDAF's innovative `Populist Strategic Contradiction Index (PSCI)` was tested against electoral outcomes. The analysis found no significant correlation (r = 0.07, p = 0.61), falsifying the hypothesis that more successful candidates would exhibit more coherent, less contradictory rhetoric. This suggests that deploying seemingly contradictory populist appeals may not be a political liability.
*   **The PDAF Scale is Internally Consistent:** The framework's nine core dimensions demonstrated good internal reliability, with a Cronbach's alpha of 0.83. This indicates that the dimensions work together cohesively to measure the underlying construct of populist discourse, lending statistical credibility to the framework's design.

## 4. Methodology

### Framework Description
This analysis employs the **Populist Discourse Analysis Framework (PDAF) v10.0.0**, a multi-dimensional tool designed to quantify populist rhetoric. The PDAF moves beyond simple binary classification (populist/non-populist) by measuring discourse across nine distinct dimensions, grouped into three theoretical categories:

1.  **Primary Populist Core Anchors:** Based on the foundational theories of Mudde (2004) and Müller (2016), this category includes `Manichaean People-Elite Framing`, `Crisis-Restoration Temporal Narrative`, `Popular Sovereignty Claims`, and `Anti-Pluralist Exclusion`.
2.  **Populist Mechanism Anchors:** Grounded in mobilization theories, this includes `Elite Conspiracy/Systemic Corruption`, `Authenticity vs. Political Class`, and `Homogeneous People Construction`.
3.  **Boundary Distinction Anchors:** Based on research into social exclusion, this includes `Nationalist Exclusion` and `Economic Populist Appeals`.

A key innovation of the PDAF is its use of **salience-weighting**, where each dimension is scored for both intensity (0.0-1.0) and rhetorical prominence (salience, 0.0-1.0). This allows for the calculation of salience-weighted indices that capture not just the presence of a theme but its strategic emphasis. Furthermore, the framework introduces **Populist Strategic Tension Mathematics**, including the `Populist Strategic Contradiction Index (PSCI)`, which quantifies the degree to which a speaker employs rhetorically contradictory appeals simultaneously.

### Corpus and Data Structure
The analysis was conducted on the **2016 Presidential Campaign Speech Corpus**, a collection of 57 speeches from six major candidates: Hillary Clinton (n=21), Donald Trump (n=22), Bernie Sanders (n=5), Ted Cruz (n=3), Marco Rubio (n=4), and John Kasich (n=2). Each document in the corpus is accompanied by metadata, including `candidate_short`, `party`, `campaign_phase`, `candidate_type` ("outsider," "establishment," "challenger"), and `electoral_success` (a 3-point scale). These metadata fields were used for all statistical grouping and hypothesis testing.

### Statistical Methods
The analysis followed the protocol outlined in the experiment configuration. Key statistical tests included:
*   **One-way ANOVA** to test for differences in the `Salience-Weighted Overall Populism Index` across the six candidates (H1).
*   **Independent samples t-tests** to compare partisan groups (H5, H6) and candidate types (H10) on specific PDAF dimensions.
*   **Pearson correlation** to assess the relationship between the `Populist Strategic Contradiction Index (PSCI)` and the `electoral_success` variable (H8).
*   **Levene's test** for homogeneity of variances to test for differences in rhetorical consistency (H9).
*   **Cronbach's alpha** was calculated to assess the internal reliability of the 9-item PDAF scale.

All statistical tests were conducted at an alpha level of 0.05. Effect sizes (Cohen's d for t-tests, eta-squared for ANOVA) were calculated to determine the magnitude of observed effects. All numerical results are reported to two or three decimal places, following APA 7th edition guidelines.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics and Reliability
The PDAF scale demonstrated good internal consistency across the 57 documents, with a Cronbach's alpha of **α = 0.83**. This indicates that the nine dimensions reliably measure a coherent underlying construct of populist discourse.

Descriptive statistics reveal a wide range of populist expression across the candidates. While the overall populism index did not differ significantly at the aggregate level, dimensional means show clear distinctions. For instance, the mean for `Nationalist Exclusion` among Republicans was **M = 0.61**, compared to **M = 0.19** for Democrats. Conversely, `Economic Populist Appeals` were high for both parties (M_dem = 0.71, M_rep = 0.71). Outsider candidates consistently scored higher than establishment candidates on key dimensions like `Popular Sovereignty Claims` (M_out = 0.68 vs. M_est = 0.34) and `Authenticity vs. Political Class` (M_out = 0.76 vs. M_est = 0.53).

### 5.2 Advanced Metric Analysis: Strategic Contradiction
The `Populist Strategic Contradiction Index (PSCI)` was designed to measure the degree to which speakers deploy rhetorically inconsistent messages. Hypothesis H8 predicted a negative correlation between PSCI and electoral success, suggesting that more successful candidates would be more rhetorically coherent. This hypothesis was **falsified**. The analysis found no significant correlation between PSCI and the `electoral_success` variable (r = 0.07, p = 0.61). This preliminary finding suggests that employing contradictory populist appeals—for instance, simultaneously invoking direct popular will while rejecting pluralism—is not necessarily a strategic liability in a campaign context. This challenges theoretical assumptions about the need for message consistency and highlights an area for future research into the reception and effectiveness of contradictory political messaging.

### 5.3 Correlation and Interaction Analysis

#### Partisan Divides: Nationalism vs. Economic Appeals
The analysis revealed a stark partisan divide in the use of boundary-defining populist rhetoric.
*   **Hypothesis H5 was confirmed.** An independent samples t-test showed that Republican candidates (M = 0.61, SD = 0.34) scored significantly higher on **Nationalist Exclusion** than Democratic candidates (M = 0.19, SD = 0.22), t(48.5) = 5.57, p < .001. The effect size was large (Cohen's d = 1.58), indicating this is a primary rhetorical differentiator between the parties. This is supported by textual evidence, such as Donald Trump's declaration, **"We are going to reject globalism and put America First. It’s going to be America First from now on"** (Source: trump_2016_08_20.txt).
*   **Hypothesis H6 was falsified.** There was no significant difference in the use of **Economic Populist Appeals** between Democrats (M = 0.71, SD = 0.34) and Republicans (M = 0.71, SD = 0.29), t(49.9) = 0.025, p = 0.98. This finding is critical, as it shows that the populist framing of economic grievances against elites was a bipartisan strategy. Both Bernie Sanders, who stated, **"We’re going to create an economy that works for all of us, not just for 1%"** (Source: sanders/primary_season/sanders_2016_03_15.txt), and Donald Trump, who promised to **"take on the big media, big business, and big donors that are bleeding our country dry"** (Source: trump_2016_10_14.txt), heavily utilized this dimension.

#### Candidate Archetypes: "Outsider" vs. "Establishment"
**Hypothesis H10 was confirmed**, as significant differences between "outsider" and "establishment" candidates were found on 4 of the 9 dimensions. This finding is central to the report's narrative, revealing a clear rhetorical archetype.
*   **Popular Sovereignty Claims:** Outsiders (M = 0.68) scored significantly higher than establishment candidates (M = 0.34), t(34.5) = 4.62, p < .001, with a large effect size (d = 1.41). This is exemplified by Ted Cruz's statement that the next president **"will not be chosen by the Washington establishment... But will be chosen by... we the people: the American people"** (Source: cruz/early_primary/cruz_2016_02_01.txt).
*   **Elite Conspiracy/Systemic Corruption:** Outsiders (M = 0.68) scored significantly higher than establishment candidates (M = 0.41), t(38.9) = 2.82, p = .007, with a large effect size (d = 0.86). Donald Trump's claim that **"Big business, elite media and major donors are lining up behind the campaign of my opponent because they know she will keep our rigged system in place"** (Source: trump/convention_period/trump_2016_07_21.txt) is a clear example of this rhetorical strategy.
*   **Authenticity vs. Political Class:** Outsiders (M = 0.76) scored significantly higher than establishment candidates (M = 0.53), t(41.9) = 2.76, p = .009, with a large effect size (d = 0.83). This was a cornerstone of the outsider appeal, as seen in Trump's assertion: **"I am not a politician. I have no special interest. My only interest is you, the American people"** (Source: trump_2016_08_20.txt).
*   **Nationalist Exclusion:** Outsiders (M = 0.56) also scored significantly higher than establishment candidates (M = 0.23), t(30.6) = 3.59, p < .001, with a large effect size (d = 1.10).

### 5.4 Pattern Recognition and Theoretical Insights

The statistical results paint a picture of a political landscape where populism is not a monolithic style but a collection of rhetorical tools deployed in distinct combinations. The non-significant ANOVA result for overall populism is perhaps the most important finding, as it forces a more nuanced, dimensional analysis. It suggests that the 2016 election was not a simple contest between populists and non-populists, but a competition between different *brands* of populism.

The data reveals at least two dominant archetypes:
1.  **The Partisan Nationalist Populist (Republican):** Characterized by high scores on `Nationalist Exclusion`, this style defines "the people" along national and cultural lines and against external threats. As Donald Trump stated, a core principle is that **"Americanism, not globalism, will be our credo"** (Source: trump/convention_period/trump_2016_07_21.txt). This archetype, primarily embodied by Trump and to a lesser extent Cruz, combines this nationalism with strong anti-establishment and anti-elite rhetoric.
2.  **The Economic Justice Populist (Bipartisan, but led by Sanders):** This style is defined by extremely high scores on `Economic Populist Appeals` and `Manichaean People-Elite Framing`, focusing on the struggle between ordinary people and a corrupt economic elite. Bernie Sanders epitomized this, declaring that **"the government of our great country belongs to all of the people and not just a handful of wealthy campaign contributors"** (Source: sanders/early_primary/sanders_2016_02_10.txt). While Clinton also used this framing, as when she stated her goal was an **"economy that works for everyone, not just those at the top"** (Source: clinton/general_election/clinton_2016_10_03.txt), Sanders' rhetoric was more consistently and intensely focused on this dimension.

The "outsider" vs. "establishment" cleavage cuts across these archetypes. Both Trump (nationalist) and Sanders (economic) were "outsiders" who leveraged claims of authenticity, elite conspiracy, and popular sovereignty to challenge the political status quo. This shared anti-establishment posture appears to be a fundamental component of populist appeal in the 2016 context.

### 5.5 Framework Effectiveness Assessment

The PDAF v10.0.0 proved to be a highly effective analytical tool for this corpus. Its primary strength lies in its multi-dimensional structure, which allowed for the identification of distinct rhetorical archetypes that a unidimensional "populism score" would have obscured. The framework's good internal reliability (α = 0.83) suggests its dimensions are measuring a coherent construct.

The framework's discriminatory power is evident in the t-test results. It successfully distinguished between partisan groups on `Nationalist Exclusion` and between candidate types on four separate dimensions. The salience-weighting and the `Populist Strategic Contradiction Index` represent important methodological innovations, although the latter did not support the initial hypothesis (H8). This "negative" result is itself valuable, suggesting that the relationship between rhetorical coherence and political success may be more complex than assumed. The framework appears well-suited to its intended corpus of formal political speeches.

## 6. Discussion

The findings of this analysis have several important theoretical implications. First, they empirically support the argument that populism is a "thin-centered ideology" (Mudde, 2004) that can be attached to different "thick" ideologies (e.g., nationalism on the right, socialism on the left). The data clearly shows how Republican and Democratic candidates used a shared populist toolkit—particularly `Economic Populist Appeals` and `Manichaean Framing`—but attached it to different core concerns.

Second, the analysis highlights the centrality of the "outsider" identity in contemporary populist mobilization. The significant differences on `Authenticity vs. Political Class` and `Elite Conspiracy` for outsider candidates suggest that performing an identity outside the political establishment is a crucial rhetorical strategy. This aligns with Moffitt's (2016) work on "the political style" of populism, where authenticity and anti-establishment performance are key components. As Donald Trump articulated, **"I am an outsider fighting for you. Hillary Clinton is an insider fighting for insiders"** (Source: trump_2016_08_20.txt).

Third, the lack of a significant correlation between the `Populist Strategic Contradiction Index` and electoral success is a provocative finding. It suggests that voters may not penalize, and may even be attracted to, candidates who employ seemingly contradictory appeals. This could be because different appeals resonate with different segments of a coalition, or because the emotional force of populist claims overrides logical inconsistencies. This warrants significant further investigation.

The primary limitation of this study is the small and uneven sample size for some candidates (e.g., Cruz, Kasich), which may have contributed to the non-significant ANOVA result and limits the generalizability of the findings. All results should be considered preliminary and indicative. Future research should apply the PDAF to a larger, more balanced corpus and explore the reception of these populist styles through audience and experimental studies.

## 7. Conclusion

This computational analysis of the 2016 U.S. presidential campaign demonstrates that populist discourse is not a monolithic phenomenon. While the term "populist" was widely applied to multiple candidates, the PDAF framework reveals distinct and divergent rhetorical strategies. The key cleavages were not simply between populist and non-populist candidates, but between "outsider" and "establishment" figures, and between a Republican-led nationalist populism and a bipartisan economic populism.

The study validates the utility of the PDAF as a nuanced measurement tool capable of moving beyond simplistic labels. Its multi-dimensional and salience-weighted approach successfully identified distinct rhetorical archetypes, providing a granular, evidence-based map of the populist landscape. The findings challenge assumptions about the necessity of rhetorical coherence for political success and confirm that while the core populist antagonism of "the people" versus "the elite" is central, the specific ways in which those groups are defined—economically, nationally, or culturally—are what constitute the critical strategic differences in modern political communication.

## 8. Evidence Citations

**Source: clinton/early_primary/clinton_2016_01_26.txt**
*   Hillary Clinton: "You heard from them, they are spouting the same failed economic policies: trickle-down economics; cut taxes on the wealthy; get out of the way of corporations. We have tried that, it does not work."

**Source: clinton/early_primary/clinton_2016_02_01.txt**
*   Hillary Clinton: "be united against a Republican vision and candidates who would drive us apart and divide us."

**Source: clinton_2016_02_27.txt**
*   Hillary Clinton: "too many people at the top, too many corporations have forgotten this basic truth about what makes America great."

**Source: clinton_2016_06_07.txt**
*   Hillary Clinton: "Your efforts have produced a strong majority of the popular vote, victories in a majority of the contests, and after tonight, a majority of pledged delegates."

**Source: clinton_2016_06_22.txt**
*   Hillary Clinton: "Let's make sure that Wall Street corporations and the super rich pay their fair share of taxes."

**Source: clinton/convention_period/clinton_2016_07_13.txt**
*   Hillary Clinton: "We are one people, united and indivisible... It means that we’re in this together, even if that’s not always easy."

**Source: clinton/general_election/clinton_2016_10_03.txt**
*   Hillary Clinton: "to have the kind of economy that works for everyone, not just those at the top."

**Source: clinton/general_election/clinton_2016_11_09.txt**
*   Hillary Clinton: "making our economy work for everyone not just those at the top"

**Source: cruz/early_primary/cruz_2016_02_01.txt**
*   Ted Cruz: "Iowa has sent notice that the Republican nominee and the next president of the United States will not be chosen by the media. Will not be chosen by the Washington establishment. Will not be chosen by the lobbyists. But will be chosen by the most incredible powerful force, where all sovereignty resides in our nation, by we the people: the American people."

**Source: sanders/early_primary/sanders_2016_02_10.txt**
*   Bernie Sanders: "the government of our great country belongs to all of the people and not just a handful of wealthy campaign contributors, and their Super PACs."

**Source: sanders/primary_season/sanders_2016_03_15.txt**
*   Bernie Sanders: "We’re going to create an economy that works for all of us, not just for 1%. And we are going to tell the billionaires and corporate America that they are going to have to start paying their fair share of taxes."

**Source: trump_2016_06_16.txt**
*   Donald Trump: "Our country is in serious trouble. We don't have victories anymore."

**Source: trump/convention_period/trump_2016_07_21.txt**
*   Donald Trump: "Big business, elite media and major donors are lining up behind the campaign of my opponent because they know she will keep our rigged system in place."
*   Donald Trump: "America First. Americanism, not globalism, will be our credo."

**Source: trump_2016_08_20.txt**
*   Donald Trump: "I am not a politician. I have no special interest. My only interest is you, the American people. ... I am an outsider fighting for you. Hillary Clinton is an insider fighting for insiders."
*   Donald Trump: "We are going to reject globalism and put America First. It’s going to be America First from now on."

**Source: trump_2016_10_14.txt**
*   Donald Trump: "We’re going to take on the big media, big business, and big donors that are bleeding our country dry."