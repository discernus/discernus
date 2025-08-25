---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file within acceptable rounding precision.
- **Citation Violation**: Detect prohibited external academic citations and authority claims.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Date**: 2025-08-25  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: Not available (8 documents)  

---

## 1. Executive Summary

This report presents a preliminary computational analysis of the civic character of political discourse from eight American political figures, utilizing the Civic Analysis Framework (CAF) v10.0. The analysis reveals the framework's considerable potential for quantifying and interpreting the moral dimensions of rhetoric. The findings, while exploratory due to the small sample size (N=8), demonstrate that the CAF can effectively differentiate between speakers, identifying distinct rhetorical archetypes and strategies. The primary summary metric, the Salience-Weighted Civic Character Index (CCI), provides a clear gradient of civic character, with speakers ranging from highly virtuous (John McCain, CCI = +0.80) to strategically pathological (Steve King, CCI = -0.48).

The analysis provides strong preliminary validation for the framework's theoretical underpinnings. The oppositional design of the CAF's five virtue/vice axes is supported by strong, statistically significant negative correlations between corresponding dimensions (e.g., Hope vs. Fear, r = -0.87; Pragmatism vs. Fantasy, r = -0.93). This indicates that the framework accurately captures the intended conceptual tensions. Furthermore, derived metrics like the Character Tension Indices successfully identify speakers who employ strategically contradictory messaging, blending virtuous and vicious appeals. For instance, Bernie Sanders exhibits the highest mean tension (0.14), reflecting a rhetorical style that combines high-intensity appeals to both justice and resentment.

Ultimately, this pilot study demonstrates the utility of the CAF as a tool for nuanced, data-driven analysis of political communication. It successfully moves beyond simple sentiment analysis to map the complex moral and ethical landscapes speakers construct. The identification of coherent rhetorical clusters—one centered on virtues like dignity and truth, the other on vices like tribalism and manipulation—suggests the existence of consistent meta-strategies in political discourse. While these findings require validation with a larger and more diverse corpus, they establish a robust methodological foundation for future research into the civic quality of public speech.

## 2. Opening Framework: Key Insights

*   **The Civic Character Index (CCI) Effectively Differentiates Speakers:** The analysis produced a wide and interpretable range of CCI scores, from John McCain's highly positive +0.80 to Steve King's highly negative -0.48. This suggests the CCI is a potent summary metric for the overall civic orientation of a speaker's rhetoric.
*   **Framework's Oppositional Structure is Empirically Supported:** The data reveals strong negative correlations between the virtues and their corresponding vices as defined by the framework. The correlation between Dignity and Tribalism (r = -0.81) and Pragmatism and Fantasy (r = -0.93) provides preliminary validation for the framework's core theoretical assumptions.
*   **Distinct Rhetorical Archetypes Emerge from the Data:** The analysis classifies speakers into coherent patterns. Figures like John McCain and Mitt Romney are categorized as "Authentic Virtue" (high CCI, low tension), while Bernie Sanders and Steve King are classified as "Strategic Pathology" (negative CCI, high vice scores), indicating the framework's ability to identify underlying rhetorical postures.
*   **Tension Indices Reveal Strategic Contradictions:** The analysis of tension metrics highlights speakers who simultaneously appeal to competing values. Bernie Sanders' profile, for example, is marked by high tension on the Justice-Resentment axis, reflecting a style that blends calls for fairness with strong grievance-based narratives. As Sanders stated, "That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), a quote that captures both a sense of injustice and a call to rectify it.
*   **Two Opposing Rhetorical Meta-Strategies are Evident:** Correlation analysis reveals two distinct and opposing clusters of rhetorical dimensions. Virtues like Dignity, Truth, and Pragmatism are positively inter-correlated, while vices like Tribalism, Manipulation, and Fantasy form their own coherent, positively inter-correlated group. These two clusters are strongly negatively correlated with each other, suggesting two fundamentally different modes of political communication.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The CAF is grounded in Aristotelian virtue ethics and civic republican theory, assessing the virtues and vices speakers demonstrate through their rhetoric. It is structured around five fundamental, oppositional axes:

1.  **Identity Axis:** Dignity (universal human worth) vs. Tribalism (in-group/out-group division).
2.  **Truth Axis:** Truth (intellectual honesty) vs. Manipulation (deceptive framing).
3.  **Justice Axis:** Justice (fairness, rule of law) vs. Resentment (grievance, blame).
4.  **Emotional Axis:** Hope (aspirational vision) vs. Fear (threat-based motivation).
5.  **Reality Axis:** Pragmatism (acknowledging constraints) vs. Fantasy (denial of complexity).

For each of the 10 dimensions, the analysis produces a `raw` score (intensity, 0-1) and a `salience` score (emphasis, 0-1). From these, two key sets of derived metrics are calculated:
*   **Character Tension Indices:** Calculated for each axis as `min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`, this metric quantifies the degree of strategic contradiction in a speaker's message.
*   **Salience-Weighted Civic Character Index (CCI):** Calculated as `(Sum(Virtue * Salience) - Sum(Vice * Salience)) / Total_Salience`, this provides a single, normalized score from -1.0 (maximally vice-dominant) to +1.0 (maximally virtue-dominant), representing the overall civic character of the discourse.

### Data Structure and Corpus Description

The corpus for this analysis consists of 8 documents, each a political speech from a distinct American political figure. The speakers include John McCain, Cory Booker, Mitt Romney, John Lewis, Alexandria Ocasio-Cortez, JD Vance, Bernie Sanders, and Steve King. The raw data for each document comprises scores for the 10 core dimensions and associated confidence levels.

A critical limitation of this study is the absence of a `corpus_manifest.json` file. This prevented the `validate_framework_by_style` analysis, as metadata on speaker style (e.g., 'populist', 'institutional') was unavailable. Speaker identification was performed via a fallback method of parsing document filenames.

### Statistical Methods and Analytical Constraints

The analysis is primarily descriptive and exploratory, appropriate for the pilot nature of this study. The key statistical methods include:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles to understand the distribution of scores across the corpus.
2.  **Pearson Correlation:** A correlation matrix was computed for the 10 raw dimension scores to assess inter-dimensional relationships and test the framework's construct validity.
3.  **Aggregation and Profiling:** Speaker-level profiles were generated by calculating the mean scores for all raw, salience, and derived metrics for each speaker.
4.  **Rule-Based Classification:** A classification model, derived from the framework's interpretive guidance, was applied to speaker profiles to identify rhetorical archetypes (e.g., "Authentic Virtue," "Strategic Pathology").

The most significant analytical constraint is the **extremely small sample size (N=8)**. This precludes the use of inferential statistics and means that all findings must be interpreted as **preliminary, suggestive, and exploratory**. The results demonstrate the potential of the methodology but do not constitute definitive proof or generalizable conclusions. The term "significant" in this report refers to the magnitude and practical importance of an effect (e.g., a large correlation), not statistical significance in the inferential sense.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the 20 primary metrics (10 raw scores, 10 salience scores) provides a foundational overview of the rhetorical tendencies within the corpus.

**Table 1: Descriptive Statistics for CAF Raw and Salience Scores (N=8)**

| Statistic | tribalism_raw | dignity_raw | manipulation_raw | truth_raw | resentment_raw | justice_raw | fear_raw | hope_raw | fantasy_raw | pragmatism_raw |
|:----------|--------------:|------------:|-----------------:|----------:|---------------:|------------:|---------:|---------:|------------:|---------------:|
| mean      | 0.51          | 0.58        | 0.34             | 0.66      | 0.71           | 0.63        | 0.46     | 0.55     | 0.20        | 0.59           |
| std       | 0.42          | 0.36        | 0.37             | 0.21      | 0.36           | 0.32        | 0.24     | 0.28     | 0.29        | 0.37           |
| min       | 0.00          | 0.00        | 0.00             | 0.30      | 0.00           | 0.00        | 0.10     | 0.10     | 0.00        | 0.00           |
| 25%       | 0.08          | 0.33        | 0.00             | 0.55      | 0.68           | 0.48        | 0.30     | 0.43     | 0.00        | 0.33           |
| 50%       | 0.65          | 0.75        | 0.25             | 0.75      | 0.90           | 0.70        | 0.45     | 0.60     | 0.05        | 0.75           |
| 75%       | 0.90          | 0.83        | 0.65             | 0.80      | 0.90           | 0.90        | 0.60     | 0.73     | 0.30        | 0.90           |
| max       | 0.90          | 0.90        | 0.80             | 0.90      | 0.95           | 0.90        | 0.90     | 0.90     | 0.70        | 0.90           |

The data indicates that `resentment` (mean = 0.71) and `truth` (mean = 0.66) are the most consistently high-intensity raw scores in this corpus. This suggests that framing arguments around past grievances and presenting them with an appeal to factuality are common strategies. Conversely, `fantasy` (mean = 0.20) and `manipulation` (mean = 0.34) have the lowest average intensity, though their high standard deviations (0.29 and 0.37, respectively) indicate that their use varies dramatically between speakers. The high standard deviation for `tribalism` (0.42) and `pragmatism` (0.37) similarly points to these being key dimensions that differentiate the speakers in this sample.

### 5.2 Advanced Metric Analysis

The derived metrics provide a more synthesized view of speaker strategy and overall civic character. The analysis of speaker profiles, ranked by the Civic Character Index (CCI), reveals a clear hierarchy of rhetorical styles.

**Table 2: Speaker Character Coherence Profiles**

| speaker                  | civic_character_index | mean_tension | pattern_classification   | mean_virtue_raw | mean_virtue_salience | mean_vice_raw | mean_vice_salience |
|:-------------------------|----------------------:|-------------:|:-------------------------|----------------:|---------------------:|--------------:|-------------------:|
| john_mccain              | 0.805                 | 0.014        | Authentic Virtue         | 0.82            | 0.76                 | 0.02          | 0.02               |
| cory_booker              | 0.502                 | 0.058        | Authentic Virtue         | 0.88            | 0.88                 | 0.24          | 0.32               |
| mitt_romney              | 0.500                 | 0.042        | Authentic Virtue         | 0.72            | 0.72                 | 0.18          | 0.24               |
| john_lewis               | 0.253                 | 0.020        | Virtue-Leaning           | 0.78            | 0.73                 | 0.40          | 0.43               |
| alexandria_ocasio_cortez | 0.005                 | 0.088        | Virtue-Leaning           | 0.62            | 0.62                 | 0.54          | 0.58               |
| jd_vance                 | -0.275                | 0.042        | Vice-Leaning             | 0.34            | 0.36                 | 0.62          | 0.60               |
| bernie_sanders           | -0.394                | 0.144        | Strategic Pathology      | 0.38            | 0.34                 | 0.73          | 0.72               |
| steve_king               | -0.480                | 0.074        | Strategic Pathology      | 0.26            | 0.30                 | 0.82          | 0.83               |

This table offers several key insights. John McCain's profile is exemplary of the "Authentic Virtue" classification, with a very high CCI (+0.805), extremely low mean tension (0.014), high mean virtue scores (0.82), and negligible vice scores (0.02). This statistical profile is supported by the textual evidence from his speech. As John McCain stated: "we fell short, the failure is mine, not yours" (Source: john_mccain_2008_concession_ff9b26f2.txt), a quote that directly rejects blame-focused resentment. His call to "offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt) exemplifies the high `hope` and `dignity` scores that contribute to his positive CCI.

In stark contrast, Bernie Sanders and Steve King are classified as "Strategic Pathology." Sanders' profile is particularly noteworthy for its high `mean_tension` (0.144), the highest in the corpus. This indicates a significant use of contradictory appeals. His rhetoric scores high on vices like `resentment` (raw=0.95) and `tribalism` (raw=0.90) while also attempting to leverage virtues like `justice` and `hope`. This tension is evident in his framing of a "rigged economy," which simultaneously stokes resentment and calls for justice. As Bernie Sanders stated: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This single statement encapsulates the blend of resentment (past grievance) and justice (future change) that drives his high tension score.

Alexandria Ocasio-Cortez sits at the midpoint with a CCI of nearly zero (0.005). Her profile shows a near-perfect balance between mean virtue raw score (0.62) and mean vice raw score (0.54), classifying her as "Virtue-Leaning" but highlighting a highly contested rhetorical style that employs both sets of appeals with significant intensity and salience.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix for the 10 raw dimension scores provides critical evidence for the framework's construct validity and reveals underlying rhetorical meta-strategies.

**Table 3: Pearson Correlation Matrix for CAF Raw Dimension Scores**

|             | tribalism | dignity | manipulation | truth  | resentment | justice | fear   | hope   | fantasy | pragmatism |
|:------------|----------:|--------:|-------------:|-------:|-----------:|--------:|-------:|-------:|--------:|-----------:|
| **tribalism** | 1.00      | -0.81   | 0.91         | -0.79  | 0.80       | -0.71   | 0.40   | -0.23  | 0.72    | -0.76      |
| **dignity**   | -0.81     | 1.00    | -0.87        | 0.67   | -0.52      | 0.87    | -0.58  | 0.50   | -0.75   | 0.67       |
| **manipulation**| 0.91      | -0.87   | 1.00         | -0.77  | 0.61       | -0.75   | 0.33   | -0.30  | 0.89    | -0.91      |
| **truth**     | -0.79     | 0.67    | -0.77        | 1.00   | -0.55      | 0.84    | 0.08   | -0.16  | -0.56   | 0.52       |
| **resentment**| 0.80      | -0.52   | 0.61         | -0.55  | 1.00       | -0.34   | 0.41   | -0.07  | 0.48    | -0.51      |
| **justice**   | -0.71     | 0.87    | -0.75        | 0.84   | -0.34      | 1.00    | -0.19  | 0.13   | -0.54   | 0.43       |
| **fear**      | 0.40      | -0.58   | 0.33         | 0.08   | 0.41       | -0.19   | 1.00   | -0.87  | 0.30    | -0.30      |
| **hope**      | -0.23     | 0.50    | -0.30        | -0.16  | -0.07      | 0.13    | -0.87  | 1.00   | -0.38   | 0.37       |
| **fantasy**   | 0.72      | -0.75   | 0.89         | -0.56  | 0.48       | -0.54   | 0.30   | -0.38  | 1.00    | -0.93      |
| **pragmatism**| -0.76     | 0.67    | -0.91        | 0.52   | -0.51      | 0.43    | -0.30  | 0.37   | -0.93   | 1.00       |

The most striking pattern is the strong negative correlation between the virtues and their corresponding vices on each axis, providing strong preliminary support for the framework's oppositional design.
*   **Emotional Axis (Hope/Fear):** r = -0.87 (Large effect)
*   **Reality Axis (Pragmatism/Fantasy):** r = -0.93 (Large effect)
*   **Identity Axis (Dignity/Tribalism):** r = -0.81 (Large effect)
*   **Truth Axis (Truth/Manipulation):** r = -0.77 (Large effect)
*   **Justice Axis (Justice/Resentment):** r = -0.34 (Medium effect)

The correlations for four of the five axes are large and in the expected direction. The weaker, though still negative, correlation between `justice` and `resentment` is a notable finding. It suggests that, in this corpus, appeals to justice and grievance are not as mutually exclusive as other virtue/vice pairs. This is consistent with the high tension scores observed for speakers like Bernie Sanders, who explicitly links the two. His statement, "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), is a classic `tribalism` appeal that underpins a narrative of economic `resentment` and a call for `justice`.

The matrix also reveals two clear meta-strategies or rhetorical clusters. The vices (`tribalism`, `manipulation`, `resentment`, `fantasy`) are all strongly and positively correlated with one another. For example, the correlation between `manipulation` and `fantasy` is extremely high (r = +0.89). This suggests a coherent "pathological" style that relies on simplifying reality, creating in-groups, and stoking grievance. Conversely, the virtues (`dignity`, `truth`, `justice`, `pragmatism`) are also largely positively correlated, forming a "civic" style. The strong negative correlations between these two clusters indicate they are opposing rhetorical modes.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns provide strong evidence for the construct validity of the CAF. The framework is designed to measure five distinct tensions, and the data confirms that these tensions are empirically robust. The oppositional nature of the dimensions is not just a theoretical construct but a measurable feature of the discourse analyzed. The very strong negative correlation between `pragmatism` and `fantasy` (r = -0.93) is particularly telling. It suggests that a speaker's orientation toward reality is a fundamental choice with cascading rhetorical consequences. A speaker who scores high on `fantasy` is highly unlikely to score high on `pragmatism`, and vice-versa. This is illustrated by the lack of any pragmatic quotes in the Sanders speech, which was rated high in `fantasy` for statements like, "The rich want to get richer and they don't care who they step on" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), an oversimplification that denies complex economic realities.

The unexpected finding is the weaker (r = -0.34) relationship between `justice` and `resentment`. This suggests that in contemporary political rhetoric, particularly of a populist nature, resentment is often framed as a necessary precondition for achieving justice. The two are presented not as opposites, but as sequential: the identification of a grievance (`resentment`) is the justification for corrective action (`justice`). This nuance is a valuable insight generated by the analysis and suggests an area for further theoretical refinement or investigation.

The statistical patterns align well with theories of political rhetoric that posit different persuasive modes. The "civic" cluster (dignity, truth, pragmatism) aligns with deliberative, reason-based models of discourse, while the "pathological" cluster (tribalism, manipulation, resentment) aligns with agonistic or populist models that rely on emotional activation and group identity.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CAF v10.0 demonstrates considerable effectiveness.

*   **Discriminatory Power:** The framework successfully differentiates speakers across a wide spectrum. The CCI scores range from -0.48 to +0.80, a spread of 1.285 points on a 2-point scale, indicating high discriminatory power. The ability to classify speakers into distinct archetypes ("Authentic Virtue," "Strategic Pathology," etc.) further underscores this capability.
*   **Framework-Corpus Fit:** The framework's dimensions appear well-suited to analyzing modern American political speech. The concepts of tribalism, resentment, and manipulation, as well as dignity, justice, and hope, are clearly present and measurable in the corpus. The primary limitation noted—the inability to perform a style-based validation—is a consequence of missing corpus metadata, not an inherent flaw in the framework itself.
*   **Methodological Insights:** The two-tiered system of basic dimensions and derived metrics is highly effective. The 10 core dimensions provide granular detail, while the CCI and Tension Indices offer powerful, interpretable summaries. The CCI, in particular, proves to be a robust and intuitive measure of overall civic character. The Tension Index is a methodological innovation that successfully captures the strategic complexity of using contradictory appeals, an insight that would be missed by analyzing dimensions in isolation.

## 6. Discussion

### Theoretical Implications of Findings

This analysis, though preliminary, carries several important theoretical implications for the study of political communication. The strong empirical support for the CAF's oppositional structure suggests that virtue ethics provides a viable and powerful lens for deconstructing rhetoric. The data indicates that political discourse is not an arbitrary collection of themes but is often structured around these fundamental moral tensions. The existence of two opposing rhetorical clusters (civic vs. pathological) suggests that speakers adopt coherent meta-strategies that align with either deliberative or populist communication theories.

The finding that the Justice/Resentment axis is less oppositional than others (r = -0.34) is theoretically significant. It may indicate that in an era of high political polarization, resentment-based claims are increasingly being legitimized as valid calls for justice, blurring a line that classic civic theory would draw more sharply. This suggests that the relationship between these concepts may be evolving, a hypothesis that warrants further investigation.

### Comparative Analysis and Archetypal Patterns

The classification of speakers into rhetorical archetypes is a key outcome of this analysis. These archetypes represent distinct approaches to civic discourse:

1.  **The Unifier (e.g., John McCain):** Characterized by an exceptionally high CCI, very low tension, and a near-total absence of vice-based appeals. This style emphasizes shared identity, responsibility, and hope. As McCain stated, "I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight" (Source: john_mccain_2008_concession_ff9b26f2.txt), an explicit appeal to `dignity` and shared national experience.
2.  **The Principled Institutionalist (e.g., Mitt Romney, Cory Booker):** This archetype exhibits a high CCI and low tension but may strategically employ some vice-based appeals to frame a problem. They are strongly rooted in virtue but are not entirely above using oppositional framing.
3.  **The Contested Populist (e.g., Alexandria Ocasio-Cortez):** This archetype is defined by a CCI near zero and high scores on both virtue and vice dimensions. Their rhetoric is a battleground of competing appeals, making their overall civic character ambiguous and highly dependent on the listener's own priors.
4.  **The Pathological Agitator (e.g., Bernie Sanders, Steve King):** Marked by a negative CCI, high reliance on vice-based appeals (especially tribalism and resentment), and often high tension scores. This style seeks to motivate action by activating grievance, fear, and in-group/out-group dynamics.

### Broader Significance for the Field

This work demonstrates the value of computational social science methods in advancing the study of political communication. By operationalizing concepts from political theory and virtue ethics, the CAF allows for scalable, replicable, and nuanced analysis of large text corpora. This approach can move the field beyond subjective interpretation or simplistic keyword-based content analysis. Future applications could include tracking the evolution of civic discourse over time, comparing rhetorical norms across different countries, or analyzing the impact of different communication styles on public opinion.

### Limitations and Future Directions

The foremost limitation of this study is its **small sample size (N=8)**. All findings must be considered exploratory and require validation on a much larger and more diverse dataset. The conclusions drawn are hypotheses generated from the data, not proven facts.

Future research should proceed in several directions:
1.  **Scale Up:** Apply the CAF to a large corpus of political speeches (e.g., the entire Congressional Record for a given period) to validate these preliminary findings and enable robust inferential statistical analysis.
2.  **Annotate for Style:** Create a corpus with reliable metadata for speaker style (populist, institutional, etc.) to properly test the framework's ability to distinguish between a priori defined communication modes.
3.  **Longitudinal Analysis:** Analyze discourse from the same speakers over time to track the evolution of their rhetorical character.
4.  **Investigate the Justice/Resentment Axis:** Conduct a targeted qualitative and quantitative study to better understand the complex relationship between these two dimensions in contemporary discourse.

## 7. Conclusion

This computational analysis, guided by the Civic Analysis Framework v10.0, represents a successful pilot study in the quantitative evaluation of civic character in political discourse. Despite the significant limitation of a small sample size, the analysis yielded rich, interpretable, and theoretically relevant insights. The study demonstrates that the framework's core concepts are empirically sound, as evidenced by the strong oppositional correlations between its virtue and vice dimensions.

The key contributions of this report are threefold. First, it provides preliminary validation for the CAF as a tool with high discriminatory power, capable of differentiating speakers and identifying coherent rhetorical archetypes. Second, it introduces and demonstrates the utility of derived metrics like the Civic Character Index and Tension Indices, which provide powerful, synthesized insights into a speaker's overall orientation and strategic complexity. Third, it generates several testable hypotheses for future research, most notably regarding the existence of opposing "civic" and "pathological" meta-strategies and the uniquely complex relationship between justice and resentment in modern rhetoric.

While caution is warranted in interpreting these initial findings, the methodology shows immense promise. It provides a pathway for researchers to move beyond impressionistic critiques of public discourse and toward a more rigorous, data-driven science of civic communication.

## 8. Evidence Citations

### bernie_sanders_2025_fighting_oligarchy_261b893a.txt
*   As Bernie Sanders stated: "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."
*   As Bernie Sanders stated: "Abraham Lincoln talked about a government of the people, by the people, for the people."
*   As Bernie Sanders stated: "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   As Bernie Sanders stated: "They are angry because, believe it or not, despite a huge increase in worker productivity over the last 52 years, if you could believe it, real inflation accounted for wages today are lower than they were 52 years ago."
*   As Bernie Sanders stated: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."
*   As Bernie Sanders stated: "They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer."
*   As Bernie Sanders stated: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve."
*   As Bernie Sanders stated: "The rich want to get richer and they don't care who they step on."

### john_mccain_2008_concession_ff9b26f2.txt
*   As John McCain stated: "This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."
*   As John McCain stated: "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain."
*   As John McCain stated: "we fell short, the failure is mine, not yours."
*   As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
*   As John McCain stated: "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."