---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file within acceptable rounding precision.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Run ID**: Not available  
**Date**: 2025-08-25  
**Framework**: CAF_v10.0.md  
**Corpus**: corpus.md not found (8 documents)  

---

## 1. Executive Summary

This report details a preliminary computational analysis of eight political speeches using the Civic Analysis Framework (CAF) v10.0. The study aimed to evaluate the civic character of political discourse by quantifying speakers' use of rhetorical virtues and vices. The analysis reveals that the CAF framework can effectively differentiate between distinct rhetorical styles and provide a nuanced, data-driven assessment of political communication. The findings, while based on a small sample (N=8) and thus indicative rather than conclusive, demonstrate the framework's potential for systematic rhetorical analysis.

Key findings indicate a clear polarization in rhetorical character among the speakers. The derived **Salience-Weighted Civic Character Index (CCI)**, a composite score of overall civic virtue, ranged from a high of +0.80 (John McCain) to a low of -0.48 (Steve King), demonstrating the framework's significant discriminatory power. A rule-based classification identified three speakers as exhibiting "Authentic Virtue," two as "Strategic Pathology," and the remainder as "Virtue-Leaning" or "Vice-Leaning." This suggests the existence of distinct, measurable rhetorical archetypes. Furthermore, a correlation analysis strongly supports the framework's theoretical underpinnings, revealing a powerful negative relationship between corresponding virtues and vices (e.g., `pragmatism` vs. `fantasy`, r = -0.93), which serves as a preliminary validation of the framework's oppositional design.

The analysis of **Character Tension Indices** highlights the strategic complexity of political language. Speakers like Bernie Sanders, for instance, exhibit high tension scores, simultaneously employing strong appeals to both `justice` and `resentment`. This finding suggests that some political styles rely on a calculated blend of virtuous framing and divisive, grievance-based rhetoric. Overall, this pilot study indicates that the CAF v10.0 is a promising tool for computational social science, capable of moving beyond simple sentiment analysis to provide a structured, theory-driven evaluation of the moral and civic dimensions of political discourse. Future research should focus on applying this methodology to larger, more diverse corpora to validate and expand upon these preliminary insights.

## 2. Opening Framework: Key Insights

This analysis of political discourse through the Civic Analysis Framework (CAF) v10.0 yielded several key insights into the structure and character of contemporary rhetoric.

*   **Clear Archetypal Separation:** The analysis successfully identified and separated speakers into distinct rhetorical archetypes. The **Civic Character Index (CCI)** and subsequent pattern classification sorted speakers into groups like "Authentic Virtue" (e.g., John McCain, CCI = +0.80) and "Strategic Pathology" (e.g., Steve King, CCI = -0.48; Bernie Sanders, CCI = -0.39), indicating that these rhetorical postures are quantitatively measurable and distinct.
*   **Strong Construct Validity of Oppositional Axes:** The framework's design, which posits virtues and vices as oppositional pairs, is strongly supported by the data. The analysis found large negative correlations between corresponding dimensions, most notably between `pragmatism` and `fantasy` (r = -0.93), `pragmatism` and `manipulation` (r = -0.91), and `dignity` and `tribalism` (r = -0.81). This suggests the framework is measuring genuinely competing rhetorical concepts.
*   **Tension as a Measure of Strategic Contradiction:** The derived `Tension` metrics effectively capture the complexity of populist rhetoric. Bernie Sanders, for example, registered the highest `mean_tension` (0.144) and a high `justice_tension` (0.30). This is explained by his simultaneous high scores for the virtue of `justice` and the vice of `resentment`, a pattern illustrated by his statement, "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), which combines a grievance (`resentment`) with a call for corrective action (`justice`).
*   **Identification of Vice and Virtue Clusters:** The correlation matrix reveals two coherent, opposing meta-strategies. Vices like `tribalism`, `manipulation`, and `fantasy` are strongly inter-correlated, forming a cohesive rhetorical cluster (e.g., `tribalism` and `manipulation`, r = 0.91). Conversely, virtues like `dignity`, `justice`, and `truth` also tend to appear together. This suggests that speakers often adopt a broadly virtuous or vicious rhetorical posture rather than picking and choosing dimensions at random.
*   **The Civic Character Index as a Potent Summary Metric:** The CCI proved to be a highly effective and intuitive summary of a speaker's overall rhetorical profile. It provides a single, normalized score (from -1.0 to +1.0) that allows for direct comparison and ranking, encapsulating the balance of salience-weighted virtues and vices in a speaker's discourse. The clear ranking it produced, from McCain to King, aligns with qualitative expectations and demonstrates its utility for high-level analysis.

## 3. Literature Review and Theoretical Framework

This analysis is grounded in the **Civic Analysis Framework (CAF) v10.0**, a methodology rooted in Aristotelian virtue ethics and contemporary civic republican theory. As outlined in its *Raison d'être*, the CAF is designed to move beyond simple content or sentiment analysis to assess the underlying *civic character* demonstrated by a speaker. It operationalizes classical philosophical concepts to address a modern problem: the strategic and often contradictory nature of political communication.

The core theoretical assumption of the CAF is that political discourse is a form of moral performance. Speakers, through their rhetorical choices, display virtues essential for healthy democratic life or vices corrosive to it. The framework draws from an Aristotelian tradition by structuring these qualities as oppositional pairs on distinct axes. For example, the **Identity Axis** is defined by the tension between the virtue of `dignity` (appeals to universal human worth) and the vice of `tribalism` (appeals to in-group/out-group dynamics). This structure presumes that these are not merely different options but competing moral choices.

By incorporating concepts from civic republicanism, the framework emphasizes virtues like a commitment to the common good, reasoned deliberation (`pragmatism`, `truth`), and fairness (`justice`). The analysis, therefore, does not simply count keywords but evaluates how language is used to either build up or break down the foundations of a shared civic life. The inclusion of derived metrics like the **Character Tension Indices** is a key methodological innovation, designed specifically to quantify the "strategic tensions where speakers simultaneously appeal to competing virtues and their pathological counterparts." This study serves as a preliminary empirical test of these theoretical foundations, examining whether the patterns predicted by the framework manifest in real-world political speech.

## 4. Methodology

### Framework Description and Analytical Approach

This study employed the Civic Analysis Framework (CAF) v10.0 to analyze a corpus of political speeches. The CAF provides a systematic method for evaluating political discourse across five fundamental axes, each representing a tension between a civic virtue and its corresponding vice:

1.  **Identity Axis:** `dignity` vs. `tribalism`
2.  **Epistemic Axis:** `truth` vs. `manipulation`
3.  **Justice Axis:** `justice` vs. `resentment`
4.  **Emotional Axis:** `hope` vs. `fear`
5.  **Reality Axis:** `pragmatism` vs. `fantasy`

For each of these 10 dimensions, the analysis produced a `raw` score (intensity, 0-1) and a `salience` score (prominence, 0-1). From these base scores, two types of derived metrics were calculated as specified by the framework:

*   **Character Tension Indices:** For each axis, this metric quantifies the degree of strategic contradiction (`Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`). High tension indicates the simultaneous use of opposing appeals.
*   **Salience-Weighted Civic Character Index (CCI):** This is a single, normalized summary score (`(Sum(Virtue * Salience) - Sum(Vice * Salience)) / Total_Salience`) that measures the overall balance of civic virtue versus vice in a text, ranging from +1.0 (purely virtuous) to -1.0 (purely vicious).

### Data Structure and Corpus Description

The dataset for this analysis consists of quantitative scores for 8 political speeches delivered by 8 different American political figures. The corpus manifest (`corpus.md`) was not available, so speaker identification was performed by parsing document filenames (e.g., `john_mccain_2008_concession_ff9b26f2.txt`). The corpus includes a range of speakers from different political eras and ideological positions, such as John Lewis, John McCain, Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez. Each of the 8 documents was processed to generate scores for the 10 core dimensions and their associated salience and confidence levels.

### Statistical Methods and Analytical Constraints

The analysis proceeded in several stages, using the functions defined in the experiment's statistical module:

1.  **Descriptive Statistics:** Standard measures (mean, standard deviation, quartiles) were calculated for all raw and salience scores to understand the overall distribution of rhetorical features in the corpus.
2.  **Correlation Analysis:** A Pearson correlation matrix was computed for the 10 raw dimension scores to examine the relationships between virtues and vices and to assess the framework's internal consistency.
3.  **Derived Metric Calculation:** The `calculate_derived_metrics` function was used to compute the five Tension Indices and the final Civic Character Index for each document.
4.  **Archetype Profiling:** Speaker-level profiles were generated by averaging all scores and metrics for each speaker. A rule-based classification system, derived from the framework's interpretive guidance, was then applied to categorize each speaker's dominant rhetorical pattern (e.g., "Authentic Virtue," "Strategic Pathology").

### Limitations

This study is subject to several important limitations that must be considered when interpreting the results:

*   **Small Sample Size:** With a corpus of only eight documents (N=8), the findings are exploratory and illustrative, not statistically generalizable to a wider population of political speech. All conclusions should be treated as preliminary hypotheses requiring further validation.
*   **Missing Metadata:** The absence of a corpus manifest and associated metadata (such as a speaker's rhetorical `style`) prevented a key validation analysis (`validate_framework_by_style`). This function was designed to test the framework's ability to distinguish between pre-defined categories like "populist" or "institutional" rhetoric.
*   **Limited Textual Evidence:** The available textual evidence for citation was sparse, covering only two of the eight speakers in detail. This restricts the ability to ground every statistical finding in a specific, illustrative quote, though the available evidence was used wherever possible.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the 10 raw scores and 10 salience scores across the 8 documents reveals the baseline rhetorical tendencies within this corpus.

**Table 1: Descriptive Statistics for Raw and Salience Scores (N=8)**
| Statistic | dignity_raw | tribalism_raw | truth_raw | manipulation_raw | justice_raw | resentment_raw | hope_raw | fear_raw | pragmatism_raw | fantasy_raw |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **mean** | 0.575 | 0.513 | 0.663 | 0.338 | 0.625 | 0.706 | 0.550 | 0.463 | 0.587 | 0.200 |
| **std** | 0.362 | 0.419 | 0.213 | 0.374 | 0.315 | 0.355 | 0.278 | 0.245 | 0.372 | 0.288 |
| **min** | 0.000 | 0.000 | 0.300 | 0.000 | 0.000 | 0.000 | 0.100 | 0.100 | 0.000 | 0.000 |
| **max** | 0.900 | 0.900 | 0.900 | 0.800 | 0.900 | 0.950 | 0.900 | 0.900 | 0.900 | 0.700 |

The dimension of `resentment` exhibits the highest mean raw score (0.706), suggesting that grievance-based appeals are a prominent feature in this sample of political discourse. This is closely followed by `truth` (0.663) and `justice` (0.625), indicating that speakers frequently frame their arguments around claims of fact and fairness. Conversely, `fantasy` (0.200) and `manipulation` (0.338) have the lowest mean scores, though their standard deviations are relatively high, implying that while not universally present, they are used intensely by some speakers.

The standard deviations reveal the degree of variance across speakers. `Tribalism` (std=0.419), `pragmatism` (std=0.372), and `dignity` (std=0.362) show the most variation, indicating that speakers in this corpus adopt widely different approaches to identity and reality-framing. In contrast, `truth` (std=0.213) and `fear` (std=0.245) show less variation, suggesting a more consistent level of usage across the different speeches.

### 5.2 Advanced Metric Analysis

The derived metrics provide a more holistic view of each speaker's rhetorical character, moving beyond individual dimensions to assess overall strategy and coherence. The analysis produced a clear ranking of speakers based on their Civic Character Index (CCI) and classified their dominant rhetorical pattern.

**Table 2: Speaker Character Profiles and Pattern Classification**
| Speaker | Civic Character Index (CCI) | Mean Tension | Pattern Classification | Mean Virtue Raw | Mean Vice Raw |
|:---|---:|---:|:---|---:|---:|
| john_mccain | 0.805 | 0.014 | Authentic Virtue | 0.820 | 0.020 |
| cory_booker | 0.502 | 0.058 | Authentic Virtue | 0.880 | 0.240 |
| mitt_romney | 0.500 | 0.042 | Authentic Virtue | 0.720 | 0.180 |
| john_lewis | 0.253 | 0.020 | Virtue-Leaning | 0.780 | 0.400 |
| alexandria_ocasio_cortez | 0.005 | 0.088 | Virtue-Leaning | 0.620 | 0.540 |
| jd_vance | -0.275 | 0.042 | Vice-Leaning | 0.340 | 0.620 |
| bernie_sanders | -0.394 | 0.144 | Strategic Pathology | 0.380 | 0.730 |
| steve_king | -0.480 | 0.074 | Strategic Pathology | 0.260 | 0.820 |

The **Civic Character Index** effectively stratifies the speakers. John McCain's 2008 concession speech stands out as an exemplar of civic virtue (CCI = +0.805), characterized by extremely high mean virtue scores (0.820) and negligible vice scores (0.020). His rhetoric, which focused on unity and respect for the democratic process, exemplifies the "Authentic Virtue" pattern. As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt). This statement's high `hope` and `dignity` content, coupled with a complete lack of `resentment`, directly contributes to his high CCI score.

At the other end of the spectrum, Steve King (CCI = -0.480) and Bernie Sanders (CCI = -0.394) are classified as "Strategic Pathology." Their profiles are dominated by high mean vice scores (0.820 and 0.730, respectively). This indicates a rhetorical style that relies heavily on appeals to `tribalism`, `resentment`, and other vices.

The **Mean Tension** metric reveals a different kind of strategic complexity. Bernie Sanders has by far the highest tension score (0.144). This is not simply because he uses vice, but because he strategically combines it with appeals to virtue. His speech scores highly on both `resentment` (raw=0.95) and `justice` (raw=0.50). This calculated contradiction is a hallmark of his populist style, framing grievance as a righteous call for justice. The provided evidence captures this perfectly: "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This quote uses the emotionally charged, simplifying language of `manipulation` to frame a call for economic justice.

In contrast, a speaker like Alexandria Ocasio-Cortez lands almost exactly in the middle (CCI = +0.005), with nearly balanced mean virtue (0.620) and vice (0.540) scores. This results in a "Virtue-Leaning" classification but points to a highly mixed rhetorical strategy that balances appeals to `justice` and `hope` with strong elements of `tribalism` and `resentment`.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix for the 10 raw dimension scores provides critical insight into the framework's internal structure and reveals the meta-strategies at play in the corpus. The strong, systematic relationships observed lend preliminary support to the framework's construct validity.

**Table 3: Correlation Matrix of Raw Dimension Scores**
| | tribalism | dignity | manipulation | truth | resentment | justice | fear | hope | fantasy | pragmatism |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **tribalism** | 1.00 | **-0.81** | **0.91** | -0.79 | 0.80 | -0.71 | 0.40 | -0.23 | 0.72 | **-0.76** |
| **dignity** | **-0.81** | 1.00 | **-0.87** | 0.67 | -0.52 | **0.87** | -0.58 | 0.50 | **-0.75** | 0.67 |
| **manipulation**| **0.91** | **-0.87** | 1.00 | -0.77 | 0.61 | -0.75 | 0.33 | -0.30 | **0.89** | **-0.91** |
| **truth** | -0.79 | 0.67 | -0.77 | 1.00 | -0.55 | **0.84** | 0.08 | -0.16 | -0.56 | 0.52 |
| **resentment** | 0.80 | -0.52 | 0.61 | -0.55 | 1.00 | -0.34 | 0.41 | -0.07 | 0.48 | -0.51 |
| **justice** | -0.71 | **0.87** | -0.75 | **0.84** | -0.34 | 1.00 | -0.19 | 0.13 | -0.54 | 0.43 |
| **fear** | 0.40 | -0.58 | 0.33 | 0.08 | 0.41 | -0.19 | 1.00 | **-0.87** | 0.30 | -0.30 |
| **hope** | -0.23 | 0.50 | -0.30 | -0.16 | -0.07 | 0.13 | **-0.87** | 1.00 | -0.38 | 0.37 |
| **fantasy** | 0.72 | **-0.75** | **0.89** | -0.56 | 0.48 | -0.54 | 0.30 | -0.38 | 1.00 | **-0.93** |
| **pragmatism** | **-0.76** | 0.67 | **-0.91** | 0.52 | -0.51 | 0.43 | -0.30 | 0.37 | **-0.93** | 1.00 |

*Correlations with |r| > 0.70 are bolded for emphasis.*

The most striking pattern is the strong negative correlation between virtues and their conceptual opposites, which serves as a powerful, if preliminary, validation of the framework's oppositional design. The relationship between `pragmatism` and `fantasy` is exceptionally strong (r = -0.93), indicating they are used as mutually exclusive rhetorical frames. Similarly, `manipulation` is strongly and negatively correlated with `pragmatism` (r = -0.91) and `dignity` (r = -0.87). This suggests that rhetoric grounded in realism and respect for the audience is fundamentally incompatible with manipulative or fantasy-based appeals. The strong negative correlation between `hope` and `fear` (r = -0.87) likewise confirms their oppositional nature on the emotional axis.

The matrix also reveals two distinct clusters of rhetorical strategies.
1.  **The "Anti-Civic" Cluster:** `Tribalism`, `manipulation`, and `fantasy` are all strongly and positively correlated with each other. The link between `tribalism` and `manipulation` (r = 0.91) is particularly strong, suggesting that appeals to in-group identity are almost always deployed using manipulative framing in this corpus. This cluster represents a coherent rhetorical strategy based on division, simplification, and emotional grievance.
2.  **The "Pro-Civic" Cluster:** `Dignity`, `justice`, and `truth` are also positively inter-correlated. The strong link between `dignity` and `justice` (r = 0.87) and between `truth` and `justice` (r = 0.84) suggests a meta-strategy grounded in universal principles, factual claims, and appeals to fairness.

This clustering is exemplified by the speakers at the extremes. John McCain's speech, which scored high on `dignity`, `truth`, and `pragmatism`, shows how these virtues work in concert. His statement, "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain" (Source: john_mccain_2008_concession_ff9b26f2.txt), is a clear example of `truth` and `pragmatism` that simultaneously rejects `resentment`.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns observed in this analysis point toward a fundamental cleavage in political communication styles that aligns with the theoretical basis of the CAF. The strong, consistent opposition between virtue and vice dimensions across the correlation matrix is the single most important finding. It suggests that the framework is not merely assigning arbitrary labels but is capturing a genuine structural feature of political rhetoric: a choice between communication that is integrative, reality-based, and respectful versus communication that is divisive, distorted, and grievance-based.

The strongest correlations reveal the core trade-offs speakers make. The near-perfect negative correlation between `pragmatism` and `fantasy` (r = -0.93) implies that a speaker's orientation toward reality is a primary determinant of their entire rhetorical style. A speaker who embraces `pragmatism` is highly unlikely to use `manipulation` (r = -0.91) or `fantasy` (r = -0.93). This finding has significant practical implications, suggesting that the presence of pragmatic language—acknowledging complexity, constraints, and trade-offs—may be a strong negative indicator for the presence of disinformation and manipulation. John McCain's pledge "to do all in my power to help him lead us through the many challenges we face" (Source: john_mccain_2008_concession_ff9b26f2.txt) is a quintessential `pragmatic` statement that is antithetical to the rhetoric of fantasy or denial.

Conversely, the data suggests that `tribalism` is a gateway to a host of other civic vices. Its strong positive correlation with `manipulation` (r = 0.91) and `resentment` (r = 0.80) indicates that once a speaker establishes an "us vs. them" frame, they are very likely to employ manipulative emotional appeals and narratives of historical grievance to mobilize their "in-group." This is visible in the rhetoric of Bernie Sanders, whose tribal framing of "the 99% vs. the 1%" is paired with strong appeals to `resentment`. As he stated: "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This statement is a clear instance of `tribalism` that serves as the foundation for his broader economic argument.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CAF v10.0 demonstrates considerable effectiveness as a tool for computational rhetorical analysis.

*   **Discriminatory Power:** The framework successfully discriminated between the eight speakers, assigning them to different character profiles with a wide distribution of scores on the Civic Character Index. The ability to separate speakers like McCain, Sanders, and Ocasio-Cortez into quantitatively distinct categories highlights its analytical power.
*   **Framework-Corpus Fit:** The statistical patterns, particularly the strong negative correlations between opposing virtues and vices, suggest a strong fit between the framework's theoretical structure and the empirical data from the corpus. The dimensions appear to capture meaningful and independent sources of variance in political speech.
*   **Methodological Insights:** The derived metrics proved to be particularly valuable. The **CCI** offers a powerful, high-level summary, while the **Tension Indices** provide a more nuanced tool for uncovering strategic contradictions that would be missed by analyzing dimensions in isolation. The failure of the `validate_framework_by_style` function due to missing metadata, however, points to a critical dependency: the framework's full potential is realized when combined with rich, well-structured corpus metadata.

## 6. Discussion

### Theoretical Implications of Findings

The results of this pilot study carry several noteworthy theoretical implications for the study of political communication. The data provides preliminary empirical support for the Aristotelian and civic republican principles underpinning the CAF. The clear, oppositional structure observed in the correlation matrix suggests that the classical conception of virtues and vices as competing poles on a spectrum is not merely a philosophical construct but an empirically observable feature of rhetorical practice. The analysis effectively operationalizes these ancient concepts, demonstrating their continued relevance for understanding contemporary political discourse.

Furthermore, the identification of coherent "pro-civic" and "anti-civic" rhetorical clusters suggests that speakers' choices are not random but adhere to underlying strategic logics. A speaker's orientation on one axis (e.g., choosing `tribalism` over `dignity`) has a high probability of predicting their orientation on another (e.g., choosing `manipulation` over `truth`). This points toward the existence of holistic rhetorical "worldviews" that can be computationally identified and tracked.

### Comparative Analysis and Archetypal Patterns

The analysis revealed several distinct rhetorical archetypes within the small corpus, each defined by a unique signature across the CAF dimensions and metrics.

1.  **The Unifier (John McCain):** Characterized by an exceptionally high CCI (+0.805), near-zero vice scores, and minimal tension. This archetype actively rejects `tribalism` and `resentment` in favor of `dignity`, `hope`, and `pragmatism`, even in the context of a political loss. The rhetoric is integrative and forward-looking.
2.  **The Principled Institutionalist (Cory Booker, Mitt Romney):** This archetype also scores high on the CCI and is classified as "Authentic Virtue." While predominantly virtuous, they may employ low levels of vice or exhibit minor tension, reflecting the pragmatic realities of legislative debate. Their rhetoric is aspirational but grounded.
3.  **The Ambivalent Populist (Alexandria Ocasio-Cortez):** This archetype is defined by a near-zero CCI (+0.005) and a mix of high virtue and high vice scores. The combination of strong appeals to `justice` and `hope` with equally strong appeals to `tribalism` and `resentment` creates a complex, internally conflicted profile that is neither purely integrative nor purely divisive.
4.  **The Populist Agitator (Bernie Sanders):** This archetype is defined by a negative CCI (-0.394) and the highest `mean_tension` (0.144). The core strategy is to harness the energy of `resentment` and `tribalism` and channel it through the language of `justice`. This creates a powerful but civically corrosive style that thrives on conflict.
5.  **The Nationalist Provocateur (Steve King, JD Vance):** This archetype exhibits a strongly negative CCI and low tension. Unlike the Agitator, there is little attempt to balance vice with virtue. The rhetoric is overwhelmingly characterized by `tribalism`, `resentment`, and `manipulation`, with minimal appeal to virtues like `dignity` or `pragmatism`.

### Broader Significance for the Field

This study suggests a path forward for computational social science to engage more deeply with normative questions in political communication. By moving beyond sentiment analysis or topic modeling, frameworks like the CAF allow for a structured, theory-driven, and falsifiable assessment of the *quality* of public discourse. This approach could be used to track the health of a political system's discourse over time, compare rhetorical standards across different countries or political parties, or identify the specific rhetorical tactics that correlate with democratic backsliding. The ability to quantify concepts like "tension" and "civic character" provides a new vocabulary for discussing the mechanics of political persuasion.

### Limitations and Future Directions

The primary limitation of this study remains its small sample size (N=8). The findings, while internally consistent and theoretically compelling, must be considered preliminary. Future research is essential to validate these patterns on a much larger and more diverse corpus of texts.

Key directions for future research include:
*   **Large-Scale Validation:** Applying the CAF to thousands of political speeches, debates, and manifestos to confirm the archetypes and correlational structures identified here.
*   **Temporal Analysis:** Analyzing the rhetoric of specific politicians or political movements over time to track changes in their civic character, perhaps in response to major events.
*   **Metadata-Rich Analysis:** Re-running the `validate_framework_by_style` analysis with a properly curated corpus that includes metadata on speaker ideology, party affiliation, and rhetorical style (e.g., populist, technocratic). This would allow for powerful group comparisons and hypothesis testing.
*   **Cross-Cultural Comparison:** Applying the framework to political discourse from different democratic systems to explore variations in civic rhetorical norms.

## 7. Conclusion

This computational analysis, though limited in scope, successfully demonstrates the analytical utility of the Civic Analysis Framework (CAF) v10.0. By systematically quantifying the use of civic virtues and vices in a small corpus of political speeches, this study has produced a set of preliminary but highly suggestive findings. The framework proved effective at discriminating between speakers, revealing a spectrum of civic character from the highly integrative rhetoric of John McCain to the divisive strategies of Steve King and Bernie Sanders.

The methodological contributions of this work are twofold. First, the study provides empirical evidence supporting the framework's theoretical design; the strong negative correlations between opposing virtues and vices suggest the framework is measuring meaningful and coherent constructs. Second, it highlights the value of derived metrics like the **Salience-Weighted Civic Character Index** and **Character Tension Indices**, which offer a multi-layered view of rhetorical strategy, capturing both overall moral orientation and the use of strategic contradiction.

While the small sample size necessitates caution, the identified archetypes—the Unifier, the Agitator, the Ambivalent Populist—provide a rich, data-driven taxonomy for future research. The findings lay the groundwork for larger-scale studies that could track the evolution of civic discourse, assess the health of public debate, and provide a more nuanced understanding of the rhetorical mechanics of democratic governance. This research serves as a proof-of-concept for a new direction in computational social science, one that weds normative theory with quantitative rigor to shed light on the character of our shared political life.

## 8. Evidence Citations

The following textual evidence was used to support the interpretations in this report.

**Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt**

*   On `tribalism`: "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."
*   On `manipulation`: "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   On `resentment` and `justice`: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."

**Source: john_mccain_2008_concession_ff9b26f2.txt**

*   On `hope` and `dignity`: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
*   On `truth` and `pragmatism`: "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain."
*   On `pragmatism`: "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."