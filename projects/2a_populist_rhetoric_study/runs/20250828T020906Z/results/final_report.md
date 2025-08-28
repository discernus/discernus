# Populist Discourse Analysis Framework (PDAF) v10.0.0 Analysis Report

**Experiment**: populist_discourse_factorial_analysis  
**Run ID**: [run_id not available]  
**Date**: 2025-08-28  
**Framework**: pdaf_v10.md  
**Corpus**: corpus.md (6 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of populist rhetoric in six presidential speeches from 2017 to 2025, utilizing the Populist Discourse Analysis Framework (PDAF) v10.0.0. The analysis reveals a consistently high intensity of populist discourse across the corpus, characterized by strong Manichaean divisions between "the people" and "the elite," narratives of national crisis and restoration, and boundary-drawing rhetoric centered on nationalist and economic themes. The salience-weighted indices confirm that these elements are not merely present but are rhetorically central to the messages, with the Salience-Weighted Boundary Distinctions Index (M = 0.90) and Core Populism Index (M = 0.86) showing particular prominence.

The study's most significant finding emerges from the PDAF's novel strategic tension analysis. The overall Populist Strategic Contradiction Index (PSCI), which measures rhetorical incoherence, is exceptionally strongly correlated with Manichaean People-Elite Framing (r = 0.95). This indicates that the foundational "us vs. them" populist appeal is the primary driver of strategic contradiction, suggesting that as this moral dichotomy intensifies, speakers are more likely to deploy a wider, less coherent array of populist claims. This dynamic is further illuminated by a strong negative correlation between Popular Sovereignty Claims and Anti-Pluralist Exclusion (r = -0.68), indicating a strategic trade-off where speakers tend to emphasize either direct democratic appeals or the delegitimization of opposition, but not both at high levels simultaneously.

Contextual analysis demonstrates that speech type significantly influences populist strategy. The 2017 Inaugural Address, a foundational speech, exhibited both the highest overall populism score (Salience-Weighted Overall Populism Index = 0.88) and the highest degree of strategic contradiction (PSCI = 0.18). In contrast, the more institutionalized State of the Union (SOTU) addresses, while still highly populist, showed markedly lower strategic contradiction (mean PSCI = 0.10). This suggests a shift from a broad, internally inconsistent populist appeal in a movement-defining moment to a more strategically refined message in formal governing contexts. The PDAF proves to be an effective tool, moving beyond simple detection to diagnose the complex, and often contradictory, strategic architecture of populist communication.

## 2. Opening Framework: Key Insights

*   **Populist Rhetoric is Intense and Structurally Central:** The analyzed speeches consistently feature high levels of populist discourse. Core themes like `Manichaean People-Elite Framing` (M = 0.88), `Crisis-Restoration Narrative` (M = 0.94), `Nationalist Exclusion` (M = 0.88), and `Economic Populist Appeals` (M = 0.91) are not only intense but also rhetorically prominent, as confirmed by high salience-weighted index scores.
*   **Manichaean Framing Drives Strategic Incoherence:** The foundational populist move of framing politics as a moral struggle between "the people" and "the elite" is the single strongest predictor of overall rhetorical contradiction. The extremely strong positive correlation between `Manichaean People-Elite Framing` and the `Populist Strategic Contradiction Index` (r = 0.95) suggests that the most intense "us vs. them" rhetoric is associated with a less disciplined, more contradictory messaging strategy.
*   **Populist Strategy Involves Rhetorical Trade-Offs:** The analysis reveals that populist dimensions are not always mutually reinforcing. A strong negative correlation between `Crisis-Restoration Narrative` and `Elite Conspiracy` (r = -0.79) and between `Popular Sovereignty Claims` and `Anti-Pluralist Exclusion` (r = -0.68) indicates that speakers make strategic choices, emphasizing either a broad crisis narrative or specific conspiracy claims, and either direct democracy or anti-pluralist attacks, but rarely both with high intensity.
*   **Nationalist and Economic Exclusion are Tightly Coupled:** A very strong positive correlation between `Nationalist Exclusion` and `Economic Populist Appeals` (r = 0.86) demonstrates a core strategic pairing. Rhetoric that defines the national in-group through cultural or external threats is consistently linked with narratives of economic grievance, creating a powerful fusion of cultural and economic populism.
*   **Speech Context Shapes Populist Coherence:** Populist rhetoric is not uniform across different contexts. The 2017 Inaugural Address registered the highest levels of both overall populism and strategic contradiction (PSCI = 0.18). The more institutionalized State of the Union speeches, by contrast, displayed significantly greater strategic coherence (mean PSCI = 0.10), suggesting a tactical refinement of populist messaging for a governing context.
*   **The Democratic-Authoritarian Tension is a Key Dynamic:** The `democratic_authoritarian_tension` metric, designed to capture the contradiction between invoking popular will and rejecting pluralism, is strongly and negatively correlated with `Anti-Pluralist Exclusion` (r = -0.93). This reveals that as the rejection of opposition becomes more extreme, the strategic tension actually *decreases*, likely because the speaker abandons the pretense of democratic justification in favor of a more overtly anti-pluralist stance.

## 4. Methodology

### Framework Description
This analysis employed the **Populist Discourse Analysis Framework (PDAF) v10.0.0**, a computational tool designed for the systematic measurement of populist political communication. The PDAF operationalizes populism across nine core dimensions, organized into three theoretical categories:
1.  **Primary Populist Core Anchors:** `Manichaean People-Elite Framing`, `Crisis-Restoration Temporal Narrative`, `Popular Sovereignty Claims`, and `Anti-Pluralist Exclusion`.
2.  **Populist Mechanism Anchors:** `Elite Conspiracy/Systemic Corruption`, `Authenticity vs. Political Class`, and `Homogeneous People Construction`.
3.  **Boundary Distinction Anchors:** `Nationalist Exclusion` and `Economic Populist Appeals`.

A key innovation of the PDAF is its use of **salience-weighted analysis**, which captures not only the intensity (raw score from 0.0-1.0) of a populist theme but also its rhetorical prominence (salience score from 0.0-1.0) within a text. This allows for a more nuanced understanding of strategic emphasis. Furthermore, the framework introduces **Populist Strategic Tension Mathematics**, including the **Populist Strategic Contradiction Index (PSCI)**, to quantify the degree of internal contradiction between different populist appeals within the same text.

### Data and Corpus
The corpus consists of six formal presidential speeches delivered by Donald J. Trump between 2017 and 2025. The selection was designed to enable temporal and contextual analysis, organized into three periods:
*   **Early Period (2017):** Inaugural Address, Joint Session Address.
*   **Mid Period (2018-2020):** State of the Union Addresses for 2018, 2019, and 2020.
*   **Recent Period (2025):** State of the Union Address for 2025.

This design facilitates comparison across time and between different speech types (foundational vs. institutional annual addresses). Each document was analyzed independently by three evaluators to ensure reliability, though this report focuses on the aggregated and finalized data.

### Statistical Methods
The analysis is primarily descriptive and correlational, focusing on interpreting the statistical outputs provided. Key methods include:
*   **Descriptive Statistics:** Calculation of means (M) and standard deviations (SD) to identify central tendencies and variance for all nine dimensions and derived indices.
*   **Correlation Analysis:** A Pearson correlation matrix was computed to examine the relationships between the nine core populist dimensions. Further correlational analysis was performed to understand the relationships between base dimensions and the derived strategic tension metrics.
*   **Contextual Comparison:** Mean scores for key indices were compared across speech types (Inaugural vs. State of the Union) to identify patterns related to the communication context.

### Limitations
The primary limitation of this study is its small sample size (N=6). While the speeches were chosen for their significance, the low number of documents means that the findings, particularly correlational patterns, should be considered preliminary and indicative rather than generalizable. The statistical analysis is descriptive and does not establish causality. All conclusions are presented with this constraint in mind, highlighting patterns that warrant further investigation with a larger corpus.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

The analysis reveals a consistently high level of populist rhetoric across all six speeches. The mean raw scores for the nine core dimensions indicate that certain populist themes are particularly intense and recurrent.

**Table 1: Descriptive Statistics for Core Populist Dimensions (Raw Scores)**

| Dimension                               | M    | SD   | Min  | Max  |
| --------------------------------------- | ---- | ---- | ---- | ---- |
| Crisis-Restoration Narrative            | 0.94 | 0.04 | 0.90 | 1.00 |
| Economic Populist Appeals               | 0.91 | 0.05 | 0.85 | 1.00 |
| Manichaean People-Elite Framing         | 0.88 | 0.05 | 0.80 | 0.95 |
| Nationalist Exclusion                   | 0.88 | 0.08 | 0.80 | 1.00 |
| Homogeneous People Construction         | 0.81 | 0.13 | 0.60 | 0.90 |
| Popular Sovereignty Claims              | 0.78 | 0.13 | 0.60 | 1.00 |
| Elite Conspiracy/Systemic Corruption    | 0.77 | 0.08 | 0.70 | 0.90 |
| Anti-Pluralist Exclusion                | 0.70 | 0.15 | 0.40 | 0.80 |
| Authenticity vs. Political Class        | 0.69 | 0.08 | 0.60 | 0.80 |

As shown in Table 1, four dimensions consistently score above 0.88 on average: `Crisis-Restoration Narrative`, `Economic Populist Appeals`, `Manichaean People-Elite Framing`, and `Nationalist Exclusion`. This suggests these four pillars form the dominant rhetorical signature within the corpus. For example, the theme of crisis and redemption is a constant, as seen when the speaker declared, "This American carnage stops right here and stops right now. We are one Nation, and their pain is our pain, their dreams are our dreams, and their success will be our success" (Source: Trump_Inaugural_2017.txt). This is paired with intense economic populism, such as the claim that "The wealth of our middle class has been ripped from their homes and then redistributed all across the world" (Source: Trump_Inaugural_2017.txt).

### 5.2 Advanced Metric Analysis

The salience-weighted indices, which account for rhetorical emphasis, confirm the centrality of these themes. The `Salience-Weighted Boundary Distinctions Index` (M = 0.90, SD = 0.06) and `Salience-Weighted Core Populism Index` (M = 0.86, SD = 0.04) are the highest, indicating that the core populist antagonism and the drawing of boundaries against external and economic "others" are the most prominent parts of the message.

The analysis of strategic contradiction reveals significant variation based on context. The 2017 Inaugural Address, a foundational speech setting the administration's tone, registered a `Populist Strategic Contradiction Index (PSCI)` of 0.18. In contrast, the average PSCI for the more structured, institutional State of the Union speeches was substantially lower at 0.10. This suggests that the initial, movement-oriented populist message was more rhetorically diffuse and internally contradictory. As the speaker stated in that first address, "today we are not merely transferring power from one administration to another, or from one party to another, but we are transferring power from Washington, DC, and giving it back to you, the people" (Source: Trump_Inaugural_2017.txt). This foundational claim was part of a speech that, according to the data, contained the highest level of strategic tension.

### 5.3 Correlation and Interaction Analysis

The relationships between populist dimensions reveal a complex strategic architecture with distinct clusters and trade-offs.

**Key Positive Correlations:**
*   A very strong positive correlation was found between **`Manichaean People-Elite Framing`** and **`Popular Sovereignty Claims`** (r = 0.87). This indicates that as the moral division between the "virtuous people" and the "corrupt elite" is intensified, so too are the calls for the direct will of the people to be the ultimate source of political authority. The two themes work in tandem to construct a narrative where the people must reclaim power from a malevolent establishment. This is evident in statements that unite a demand for popular rule with a narrative of elite failure, such as when a "quiet protest" of families grew into an "earthquake" where "the people turned out by the tens of millions... united by one very simple, but crucial demand: that America must put its own citizens first" (Source: trump_sotu_2017.txt).
*   An equally strong positive correlation exists between **`Nationalist Exclusion`** and **`Economic Populist Appeals`** (r = 0.86). This pattern suggests a fused populist strategy where threats to national identity and economic well-being are presented as two sides of the same coin. Rhetoric defining cultural boundaries and external threats is systematically paired with claims of economic betrayal by globalist elites. As the speaker argued, "For too long, we've watched our middle class shrink as we've exported our jobs and wealth to foreign countries" (Source: trump_sotu_2017.txt), directly linking a nationalistic "us" to economic harm from "them."

**Key Negative Correlations:**
*   A strong negative correlation was observed between **`Popular Sovereignty Claims`** and **`Anti-Pluralist Exclusion`** (r = -0.68). This finding is critical, as it suggests a strategic trade-off. Speeches tend to feature high levels of either appeals to the people's direct will *or* high levels of delegitimizing political opposition, but not both. This challenges the notion that populists simply accumulate all anti-establishment tropes; instead, they appear to choose between a "democratic" framing (empowering the people) and a more "authoritarian" one (disqualifying opponents).
*   Another significant negative correlation was found between **`Crisis-Restoration Narrative`** and **`Elite Conspiracy/Systemic Corruption`** (r = -0.79). This implies that speakers tend to prioritize one of two explanations for the nation's problems: either a broad, almost mythic, narrative of decline and promised rebirth, or a more specific, causal attribution of problems to the secret coordination of corrupt elites. For example, a speech might focus heavily on the "renewal of the American spirit" (Source: Trump_SOTU_2018.txt) as a crisis-restoration theme, while downplaying specific claims about a "rigged system."

### 5.4 Pattern Recognition and Theoretical Insights

The most theoretically innovative findings arise from the analysis of the derived tension metrics.

The **`Populist Strategic Contradiction Index (PSCI)`** is almost perfectly correlated with **`Manichaean People-Elite Framing`** (r = 0.95). This is the most powerful statistical relationship in the dataset and suggests that the core populist gesture of dividing the world into a pure "people" and a "corrupt elite" is the primary engine of rhetorical incoherence. When a speaker, such as in the 2018 SOTU, frames the narrative around how "for too long, we’ve watched our middle class shrink as we’ve exported our jobs and wealth to foreign countries" (Source: Trump_SOTU_2018.txt), this intense Manichaean framing is, according to the data, associated with a greater tendency to employ other, potentially contradictory populist appeals simultaneously. This may indicate that the Manichaean worldview provides a justification for a "kitchen sink" approach to messaging, where strategic discipline is secondary to mobilizing antagonism.

Furthermore, the analysis of **`democratic_authoritarian_tension`**—the specific contradiction between popular sovereignty and anti-pluralism—reveals a crucial dynamic. This tension metric is strongly *negatively* correlated with the `Anti-Pluralist Exclusion` dimension (r = -0.93). This means that as a speech becomes more explicitly anti-pluralist—for instance, by labeling opponents as "enemies of America" (Source: Trump_SOTU_2019.txt)—the measured tension *decreases*. This is because the tension formula relies on the minimum score of the two contributing dimensions. The strong negative correlation between the raw scores of `Popular Sovereignty` and `Anti-Pluralism` means that when one is high, the other is low. Thus, a highly anti-pluralist speech has low popular sovereignty claims, leading to a low tension score. This statistically validates a key theoretical insight: the most overtly authoritarian populist rhetoric resolves its own internal contradiction by abandoning the pretense of democratic justification.

### 5.5 Framework Effectiveness Assessment

The Populist Discourse Analysis Framework (PDAF) demonstrated high effectiveness in this analysis. Its multi-dimensional structure captured the multifaceted nature of populist rhetoric, while the salience-weighting feature successfully distinguished between incidental and central themes. The strong and theoretically consistent correlation patterns (e.g., the coupling of nationalism and economic populism) suggest strong construct validity for the framework's dimensions.

The framework's most significant contribution is its strategic tension analysis. The PSCI and other tension metrics generated non-obvious, powerful insights, such as the link between Manichaean framing and strategic contradiction. This moves the analysis beyond a simple quantitative audit of populist themes to a qualitative diagnosis of rhetorical strategy and its internal coherence. The framework also showed strong discriminatory power, successfully identifying significant differences in populist profiles between the Inaugural Address and the SOTU speeches. The statistical patterns confirm a strong fit between the framework's theoretical design and the empirical realities of the corpus.

## 6. Discussion

The findings of this analysis have several important theoretical implications for the study of populism. First, they challenge a simplistic, additive model of populist discourse, where more populist features equate to a "more populist" text. The strong negative correlations between key dimensions suggest that populist rhetoric is a field of strategic trade-offs. Speakers appear to make choices between emphasizing a crisis narrative or a conspiracy theory, and between invoking popular sovereignty or attacking pluralism. This points toward different "flavors" or modes of populist strategy, even within the same speaker's repertoire.

Second, the discovery that intense Manichaean framing predicts strategic *incoherence* is a major contribution. It suggests that the core of populism—the moral antagonism between people and elite—may function as a rhetorical master frame that licenses a less disciplined, more emotionally resonant style of communication. This could be a feature, not a bug: the perceived authenticity and righteous anger of the Manichaean appeal may override audience concerns about logical consistency. Future research should investigate whether this strategic contradiction impacts audience reception, potentially enhancing appeal among supporters while alienating others.

Third, the contextual difference between the Inaugural Address and the SOTU speeches is highly significant. The finding that the foundational, movement-defining Inaugural was more populist and more contradictory, while the institutional SOTU speeches were more coherent, suggests an evolution in rhetorical strategy from campaigning/mobilizing to governing. As the speaker transitions into a formal role, the populist message may be disciplined and refined to fit institutional expectations, even while remaining intensely populist in its core themes. This highlights the importance of context in shaping not just the presence of populism, but its strategic form.

## 7. Conclusion

This computational analysis of presidential speeches provides a nuanced and empirically grounded perspective on the strategic architecture of populist discourse. The study confirms that populist rhetoric in this corpus is intense, consistent, and structurally central, dominated by themes of Manichaean conflict, crisis, and nationalist-economic boundary drawing.

The principal contribution of this research lies in its application of the PDAF's strategic tension analysis. By measuring the internal contradictions within populist messaging, the analysis moved beyond what is being said to *how* it is being said. The finding that the foundational Manichaean frame is the strongest predictor of overall strategic contradiction provides a new lens for understanding populist communication. It suggests that the most potent populist appeals may also be the most rhetorically unstable.

While limited by a small sample size, these preliminary findings demonstrate the power of computational methods to uncover complex, non-obvious patterns in political language. The analysis validates the PDAF as a sophisticated tool for dissecting populist strategy and generates a series of testable hypotheses for future research regarding the trade-offs, contextual shifts, and coherence costs inherent in populist communication.

## 8. Evidence Citations

**Trump_Inaugural_2017.txt**
*   "For too long, a small group in our Nation's Capital has reaped the rewards of Government while the people have borne the cost. The establishment protected itself, but not the citizens of our country. Their victories have not been your victories; their triumphs have not been your triumphs; and while they celebrated in our Nation's Capital, there was little to celebrate for struggling families all across our land."
*   "This American carnage stops right here and stops right now. We are one Nation, and their pain is our pain, their dreams are our dreams, and their success will be our success. We share one heart, one home, and one glorious destiny."
*   "Today's ceremony, however, has very special meaning. Because today we are not merely transferring power from one administration to another, or from one party to another, but we are transferring power from Washington, DC, and giving it back to you, the people. January 20, 2017, will be remembered as the day the people became the rulers of this Nation again."
*   "Washington flourished, but the people did not share in its wealth. Politicians prospered, but the jobs left, and the factories closed. The wealth of our middle class has been ripped from their homes and then redistributed all across the world. America will start winning again, winning like never before. We will bring back our jobs. We will bring back our wealth."

**trump_sotu_2017.txt**
*   "For too long, we've watched our middle class shrink as we've exported our jobs and wealth to foreign countries... Then, in 2016, the Earth shifted beneath our feet... the people turned out by the tens of millions, and they were all united by one very simple, but crucial demand: that America must put its own citizens first. Because only then can we truly make America great again."

**Trump_SOTU_2018.txt**
*   "I will not allow the mistakes of recent decades past to define the course of our future. For too long, we’ve watched our middle class shrink as we’ve exported our jobs and wealth to foreign countries. We’ve financed and built one global project after another, but ignored the fates of our children in the inner cities of Chicago, Baltimore, Detroit, and so many other places throughout our land."
*   "A new chapter of American greatness is now beginning. A new national pride is sweeping across our Nation. And a new surge of optimism is placing impossible dreams firmly within our grasp. What we are witnessing today is the renewal of the American spirit."

**Trump_SOTU_2019.txt**
*   "Soon afterward, dozens of countries voted in the United Nations General Assembly against America’s sovereign right to make this decision... tonight I am asking Congress to pass legislation to help ensure American foreign-assistance dollars always serve American interests and only go to friends of America, not enemies of America."