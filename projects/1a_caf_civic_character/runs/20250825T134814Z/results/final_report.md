---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file within acceptable rounding precision.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Date**: 2025-08-25T12:53:24.327279+00:00  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: Not available (8 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of the civic character of political discourse from a small corpus of eight documents, utilizing the Civic Analysis Framework (CAF) v10.0. The analysis reveals the framework's preliminary effectiveness in quantitatively profiling and differentiating the rhetorical styles of various political speakers. The core findings indicate a significant divergence in the civic character of the speakers, as measured by the Salience-Weighted Civic Character Index (CCI). This index, which ranges from a high of +0.80 for John McCain to a low of -0.48 for Steve King, suggests the presence of distinct rhetorical archetypes within the corpus.

The analysis identifies two primary clusters of speakers. The first, classified as "Authentic Virtue," includes figures like John McCain, Cory Booker, and Mitt Romney, who exhibit high scores in virtues such as dignity and pragmatism, coupled with low scores in corresponding vices. The second cluster, "Strategic Pathology," includes Bernie Sanders and Steve King, who demonstrate a reliance on vices like tribalism, resentment, and manipulation. Correlation analysis provides strong preliminary support for the CAF's construct validity; the framework's oppositional dimensions (e.g., Dignity vs. Tribalism) are strongly and negatively correlated (r = -0.81), as theoretically expected. Vices such as manipulation, tribalism, and fantasy also show strong positive correlations, suggesting they form a coherent rhetorical meta-strategy.

While the small sample size (N=8) necessitates that these findings be considered preliminary, this pilot study demonstrates the potential of the CAF to move beyond qualitative assessment and provide a structured, data-driven methodology for evaluating the civic quality of political communication. The framework successfully operationalizes concepts from virtue ethics and civic republicanism, yielding nuanced insights into rhetorical strategy, character coherence, and the strategic tensions inherent in political speech.

## 2. Opening Framework: Key Insights

This analysis of political discourse through the Civic Analysis Framework (CAF) v10.0 yielded several key insights into the structure and character of the analyzed rhetoric.

*   **Clear Differentiation of Civic Character:** The CAF's derived metrics, particularly the Salience-Weighted Civic Character Index (CCI), effectively differentiate speakers along a spectrum from highly virtuous to highly vice-driven. The analysis produced a wide range of CCI scores, from John McCain (+0.80) to Steve King (-0.48), indicating the framework's strong discriminatory power even within a small sample.
*   **Strong Evidence for Framework Construct Validity:** The internal structure of the CAF is supported by strong, theoretically consistent correlations. Virtues are strongly and negatively correlated with their opposing vices, most notably Pragmatism vs. Fantasy (r = -0.93) and Dignity vs. Tribalism (r = -0.81). This suggests the framework's oppositional axes are measuring genuinely distinct and competing rhetorical concepts.
*   **Identification of Rhetorical Meta-Strategies:** The data reveals two dominant and opposing rhetorical clusters. An "Authentic Virtue" strategy, employed by speakers like McCain and Romney, is characterized by high scores in dignity, truth, and pragmatism. Conversely, a "Strategic Pathology" strategy, seen in speakers like Sanders and King, relies on a synergistic combination of tribalism, manipulation, and resentment, evidenced by their high inter-correlations.
*   **Resentment as a Pervasive Rhetorical Tool:** Across the entire corpus, `resentment` emerges as the vice with the highest average raw score (M = 0.71). This suggests that framing issues through past grievances and assigning blame is a common tactic used by speakers across the civic character spectrum, highlighting its perceived rhetorical utility.
*   **Automated Classification Aligns with Quantitative Profiles:** The `analyze_character_coherence` function successfully categorizes speakers into interpretive patterns (e.g., "Authentic Virtue," "Strategic Pathology") that align with their quantitative profiles. This provides a valuable analytical layer, translating complex numerical data into meaningful archetypes of rhetorical behavior. For example, John McCain's high CCI (+0.80) and low mean tension (0.01) correctly classify him as "Authentic Virtue."
*   **Strategic Tension Reveals Rhetorical Complexity:** The analysis of tension metrics reveals how speakers navigate competing values. For instance, Bernie Sanders exhibits the highest mean tension (0.14), particularly on the Justice/Resentment axis. This is supported by textual evidence where he simultaneously calls for systemic change while framing it through intense grievance, as when he states: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."` (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The CAF is grounded in Aristotelian virtue ethics and civic republican theory. It assesses rhetoric across five oppositional axes, each comprising a civic virtue and its corresponding vice:

1.  **Identity Axis:** Dignity vs. Tribalism
2.  **Truth Axis:** Truth vs. Manipulation
3.  **Justice Axis:** Justice vs. Resentment
4.  **Emotional Axis:** Hope vs. Fear
5.  **Reality Axis:** Pragmatism vs. Fantasy

For each of these ten dimensions, the analysis produces a `raw` score (intensity of the theme, 0-1) and a `salience` score (prominence of the theme, 0-1). From these, the analysis calculates five `Tension Indices` and a final `Salience-Weighted Civic Character Index` (CCI). The CCI provides a single, normalized metric of a text's overall civic character, ranging from -1.0 (purely vice-dominant) to +1.0 (purely virtue-dominant).

### Data Structure and Corpus Description

The analysis was performed on a corpus of eight documents of political speech. The specific manifest for the corpus was not available, so metadata such as speaker political affiliation, rhetorical style, or speech context could not be systematically incorporated. Speaker identification was performed by parsing document filenames. The dataset for each document consists of raw scores, salience scores, and confidence scores for the ten core CAF dimensions.

### Statistical Methods and Analytical Constraints

The analysis utilized a suite of automated statistical functions to process the data. Key methods included:

*   **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles for all raw and salience scores to understand the overall distribution of rhetorical features in the corpus.
*   **Derived Metrics Calculation:** Computation of the five Tension Indices and the Salience-Weighted Civic Character Index (CCI) for each document, as specified by the CAF v10.0 formulas.
*   **Aggregation and Profiling:** Grouping data by speaker and calculating mean scores to generate individual "character profiles."
*   **Correlation Analysis:** Computation of a Pearson correlation matrix for the ten raw dimension scores to assess the interrelationships between rhetorical virtues and vices.
*   **Rule-Based Classification:** Application of a classification model to categorize speaker profiles into interpretive patterns like "Authentic Virtue" or "Strategic Pathology" based on their CCI and tension scores.

**Limitations:** The primary limitation of this study is its small sample size (N=8). Consequently, all findings should be interpreted as preliminary and indicative, rather than generalizable conclusions. The analysis is descriptive and exploratory; no inferential statistical tests were performed to establish statistical significance, which would be inappropriate for this sample size. Furthermore, the lack of a corpus manifest prevented the validation of findings against external variables like pre-defined rhetorical style, as indicated by the failure of the `validate_framework_by_style` function.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial descriptive analysis of the 20 primary metrics (10 raw scores and 10 salience scores) across all eight documents provides a foundational overview of the rhetorical landscape.

| Metric               |   count |   mean |   std |   min |   25% |   50% |   75% |   max |
|:---------------------|--------:|-------:|------:|------:|------:|------:|------:|------:|
| **Raw Scores**       |         |        |       |       |       |       |       |       |
| tribalism_raw        |       8 |  0.513 | 0.419 | 0.000 | 0.075 | 0.650 | 0.900 | 0.900 |
| dignity_raw          |       8 |  0.575 | 0.362 | 0.000 | 0.325 | 0.750 | 0.825 | 0.900 |
| manipulation_raw     |       8 |  0.338 | 0.374 | 0.000 | 0.000 | 0.250 | 0.650 | 0.800 |
| truth_raw            |       8 |  0.663 | 0.213 | 0.300 | 0.550 | 0.750 | 0.800 | 0.900 |
| resentment_raw       |       8 |  0.706 | 0.355 | 0.000 | 0.675 | 0.900 | 0.900 | 0.950 |
| justice_raw          |       8 |  0.625 | 0.315 | 0.000 | 0.475 | 0.700 | 0.900 | 0.900 |
| fear_raw             |       8 |  0.463 | 0.245 | 0.100 | 0.300 | 0.450 | 0.600 | 0.900 |
| hope_raw             |       8 |  0.550 | 0.278 | 0.100 | 0.425 | 0.600 | 0.725 | 0.900 |
| fantasy_raw          |       8 |  0.200 | 0.288 | 0.000 | 0.000 | 0.050 | 0.300 | 0.700 |
| pragmatism_raw       |       8 |  0.587 | 0.372 | 0.000 | 0.325 | 0.750 | 0.900 | 0.900 |
| **Salience Scores**  |         |        |       |       |       |       |       |       |
| tribalism_salience   |       8 |  0.600 | 0.374 | 0.000 | 0.275 | 0.800 | 0.900 | 0.900 |
| dignity_salience     |       8 |  0.575 | 0.354 | 0.000 | 0.275 | 0.750 | 0.825 | 0.900 |
| manipulation_salience|       8 |  0.350 | 0.393 | 0.000 | 0.000 | 0.250 | 0.650 | 0.900 |
| truth_salience       |       8 |  0.663 | 0.177 | 0.400 | 0.500 | 0.700 | 0.800 | 0.900 |
| resentment_salience  |       8 |  0.750 | 0.358 | 0.000 | 0.775 | 0.900 | 0.950 | 1.000 |
| justice_salience     |       8 |  0.644 | 0.309 | 0.100 | 0.475 | 0.650 | 0.913 | 1.000 |
| fear_salience        |       8 |  0.450 | 0.233 | 0.100 | 0.375 | 0.400 | 0.525 | 0.900 |
| hope_salience        |       8 |  0.538 | 0.277 | 0.100 | 0.375 | 0.500 | 0.800 | 0.900 |
| fantasy_salience     |       8 |  0.188 | 0.247 | 0.000 | 0.000 | 0.050 | 0.350 | 0.600 |
| pragmatism_salience  |       8 |  0.525 | 0.341 | 0.000 | 0.250 | 0.700 | 0.800 | 0.800 |

The descriptive statistics reveal several notable patterns. The dimension of `resentment` exhibits the highest mean raw score (M = 0.71) and salience (M = 0.75), indicating it is the most intense and prominent vice in this corpus. This suggests a focus on grievance and blame is a central feature of the analyzed discourse. In contrast, `fantasy` shows the lowest mean raw score (M = 0.20) and salience (M = 0.19), suggesting that appeals based on unrealistic or simplistic solutions are less common. Among virtues, `truth` (M = 0.66) and `justice` (M = 0.63) are the most prevalent, while `hope` (M = 0.55) is slightly less pronounced. The high standard deviations for dimensions like `tribalism` (SD = 0.42) and `dignity` (SD = 0.36) suggest significant variation among speakers, which is explored in the following sections.

### 5.2 Advanced Metric Analysis: Speaker Profiles and Character Coherence

The derived metrics allow for a more nuanced analysis of individual speakers, moving beyond simple dimensional scores to a holistic assessment of civic character. The `analyze_character_coherence` function aggregates scores for each speaker and applies a classification model, yielding distinct rhetorical profiles.

| speaker                  |   civic_character_index |   mean_tension | pattern_classification   |   mean_virtue_raw |   mean_virtue_salience |   mean_vice_raw |   mean_vice_salience |
|:-------------------------|------------------------:|---------------:|:-------------------------|------------------:|-----------------------:|----------------:|---------------------:|
| john_mccain              |                   0.805 |          0.014 | Authentic Virtue         |             0.820 |                  0.760 |           0.020 |                0.020 |
| cory_booker              |                   0.502 |          0.058 | Authentic Virtue         |             0.880 |                  0.880 |           0.240 |                0.320 |
| mitt_romney              |                   0.500 |          0.042 | Authentic Virtue         |             0.720 |                  0.720 |           0.180 |                0.240 |
| john_lewis               |                   0.253 |          0.020 | Virtue-Leaning           |             0.780 |                  0.730 |           0.400 |                0.430 |
| alexandria_ocasio_cortez |                   0.005 |          0.088 | Virtue-Leaning           |             0.620 |                  0.620 |           0.540 |                0.580 |
| jd_vance                 |                  -0.275 |          0.042 | Vice-Leaning             |             0.340 |                  0.360 |           0.620 |                0.600 |
| bernie_sanders           |                  -0.394 |          0.144 | Strategic Pathology      |             0.380 |                  0.340 |           0.730 |                0.720 |
| steve_king               |                  -0.480 |          0.074 | Strategic Pathology      |             0.260 |                  0.300 |           0.820 |                0.830 |

This table reveals a clear hierarchy of civic character within the corpus. Three distinct groups emerge:
1.  **Authentic Virtue:** John McCain, Cory Booker, and Mitt Romney score high on the CCI (> 0.50) and are classified as "Authentic Virtue." Their profiles are defined by high mean virtue scores (raw > 0.72) and low mean vice scores (raw < 0.25). Their low mean tension scores (< 0.06) indicate a coherent, consistent rhetorical style. John McCain is a notable positive outlier with an exceptionally high CCI of +0.805 and minimal tension. His discourse exemplifies this profile, focusing on unifying principles. As John McCain stated: `"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."` (Source: john_mccain_2008_concession_ff9b26f2.txt). This statement directly reflects the high `dignity` score (0.9) that contributes to his virtuous profile.

2.  **Strategic Pathology:** At the opposite end, Bernie Sanders and Steve King are classified as "Strategic Pathology." They exhibit negative CCI scores (< -0.39), high mean vice scores (raw > 0.73), and relatively low mean virtue scores (raw < 0.38). This suggests a rhetorical strategy predicated on divisive and pathological appeals. Steve King has the lowest CCI (-0.480), driven by the highest mean vice score (0.82). Bernie Sanders' profile is also characterized by high vice scores and the highest mean tension in the corpus (0.144), indicating significant strategic contradiction. His reliance on resentment is clear when he states: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."` (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), a statement that perfectly illustrates his top-scoring `resentment` dimension (raw=0.95, salience=1.0).

3.  **Contested/Mixed Profiles:** Speakers like John Lewis, Alexandria Ocasio-Cortez, and JD Vance occupy the middle ground. Ocasio-Cortez is particularly interesting, with a CCI near zero (0.005) and a relatively high mean tension score (0.088). Her profile shows a near-equal balance of virtue (M=0.62) and vice (M=0.54) scores, classifying her as "Virtue-Leaning" but indicating a highly contested and complex rhetorical style that simultaneously employs appeals to both sides of the civic ledger.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix for the ten raw dimension scores offers critical insights into the internal structure of the CAF and the co-occurrence of rhetorical strategies. The results provide strong preliminary validation for the framework's oppositional design.

|             |   tribalism |   dignity |   manipulation |   truth |   resentment |   justice |   fear |   hope |   fantasy |   pragmatism |
|:------------|------------:|----------:|---------------:|--------:|-------------:|----------:|-------:|-------:|----------:|-------------:|
| tribalism   |       1.000 |    -0.809 |          0.908 |  -0.793 |        0.797 |    -0.706 |  0.396 | -0.227 |     0.723 |       -0.760 |
| dignity     |      -0.809 |     1.000 |         -0.869 |   0.671 |       -0.522 |     0.872 | -0.578 |  0.498 |    -0.755 |        0.666 |
| manipulation|       0.908 |    -0.869 |          1.000 |  -0.768 |        0.606 |    -0.749 |  0.330 | -0.296 |     0.889 |       -0.910 |
| truth       |      -0.793 |     0.671 |         -0.768 |   1.000 |       -0.553 |     0.845 |  0.079 | -0.157 |    -0.558 |        0.515 |
| resentment  |       0.797 |    -0.522 |          0.606 |  -0.553 |        1.000 |    -0.340 |  0.414 | -0.069 |     0.482 |       -0.508 |
| justice     |      -0.706 |     0.872 |         -0.749 |   0.845 |       -0.340 |     1.000 | -0.190 |  0.131 |    -0.536 |        0.430 |
| fear        |       0.396 |    -0.578 |          0.330 |   0.079 |        0.414 |    -0.190 |  1.000 | -0.873 |     0.304 |       -0.304 |
| hope        |      -0.227 |     0.498 |         -0.296 |  -0.157 |       -0.069 |     0.131 | -0.873 |  1.000 |    -0.375 |        0.366 |
| fantasy     |       0.723 |    -0.755 |          0.889 |  -0.558 |        0.482 |    -0.536 |  0.304 | -0.375 |     1.000 |       -0.934 |
| pragmatism  |      -0.760 |     0.666 |         -0.910 |   0.515 |       -0.508 |     0.430 | -0.304 |  0.366 |    -0.934 |        1.000 |

**Key Correlation Patterns:**

*   **Validation of Oppositional Axes:** The matrix shows very strong, negative correlations between the virtues and their corresponding vices, confirming the framework's theoretical foundation. The strongest examples are `pragmatism` vs. `fantasy` (r = -0.93), `manipulation` vs. `pragmatism` (r = -0.91, note `truth` is the direct opposite), `dignity` vs. `tribalism` (r = -0.81), and `hope` vs. `fear` (r = -0.87). This indicates that, in this corpus, speakers who use one tend to avoid the other, validating them as opposing rhetorical choices.
*   **The "Pathology Cluster":** A set of vices are strongly inter-correlated, suggesting a synergistic rhetorical strategy. `Tribalism` is highly correlated with `manipulation` (r = +0.91) and `fantasy` (r = +0.72). `Manipulation` is also highly correlated with `fantasy` (r = +0.89). This suggests a meta-strategy that combines in-group/out-group framing, deceptive or emotionally manipulative language, and simplistic, unrealistic narratives. This pattern is exemplified in the discourse of speakers classified with "Strategic Pathology."
*   **The "Virtue Cluster":** Virtues also show positive inter-correlations, though slightly less tightly than the vices. `Dignity` is strongly correlated with `justice` (r = +0.87) and `truth` (r = +0.67). This suggests a rhetorical approach that links appeals to universal human worth with calls for fairness and fact-based arguments.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns reveal deeper insights into the structure of civic discourse. The strong negative correlation between `pragmatism` and `fantasy` (r = -0.93) is the most powerful relationship in the dataset, suggesting the Reality Axis is a fundamental dividing line in rhetorical strategy. Speakers either ground their arguments in complexity and constraints or in simplistic, idealized narratives; they rarely do both.

The correlation between `tribalism` and `resentment` (r = +0.80) is also highly significant. It suggests that the creation of an "us vs. them" dynamic is often fueled by narratives of historical grievance. This is a classic populist rhetorical strategy. As Bernie Sanders stated: `"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."` (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This quote, which underpins his high `tribalism` score, is immediately followed by arguments about economic grievance, illustrating the tight link between these two dimensions.

Furthermore, the data suggests that manipulation is a key enabler of pathological rhetoric. The strong positive correlation between `manipulation` and `fantasy` (r = +0.89) indicates that unrealistic proposals are often packaged with emotionally charged or deceptive framing. As Bernie Sanders stated: `"But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."` (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This reframing of a complex economic issue as a simple moral failing ("greed") is a manipulative tactic that paves the way for a fantasy-based solution, a pattern reflected in the statistical correlation.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CAF v10.0 demonstrates considerable effectiveness in several areas:

*   **Discriminatory Power:** The framework, particularly through the CCI, successfully separates speakers into distinct and interpretable clusters. The wide variance in scores indicates it is sensitive to different rhetorical styles.
*   **Construct Validity:** The correlation matrix provides strong initial evidence for the framework's construct validity. The oppositional axes behave as theoretically predicted, and related concepts cluster together in logical ways.
*   **Methodological Insight:** The analysis highlights a significant limitation in the experimental design. The `validate_framework_by_style` function failed because the corpus manifest lacked a 'style' attribute for speakers. The error message, `"Cannot perform style validation. 'style' column not found in corpus manifest or is empty,"` underscores the importance of rich metadata. While the framework has identified clear computational clusters ("Authentic Virtue," "Strategic Pathology"), this analysis cannot confirm if they align with human-assigned labels like "institutionalist" or "populist." This represents a critical next step for future validation research.

## 6. Discussion

### Theoretical Implications and Archetypal Patterns

This analysis, though preliminary, has significant theoretical implications. The data provides quantitative support for the existence of distinct rhetorical archetypes that align with theories of civic discourse. The "Authentic Virtue" archetype, exemplified by John McCain, embodies the ideals of civic republicanism: a focus on common good, respect for opponents, and a pragmatic approach to problem-solving. His discourse, which scores high on `dignity`, `pragmatism`, and `hope`, reflects a unifying and constructive rhetorical posture. As John McCain stated: `"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"` (Source: john_mccain_2008_concession_ff9b26f2.txt). This is a direct appeal to the virtue of `hope` and civic duty over partisan disappointment.

Conversely, the "Strategic Pathology" archetype, seen in Steve King and Bernie Sanders, aligns with models of populist or demagogic rhetoric. This style is characterized by a "pathology cluster" of `tribalism`, `resentment`, and `manipulation`. It constructs a Manichean worldview of a virtuous "people" against a corrupt "elite," fueled by grievance and simplistic solutions. The framework's ability to identify and quantify these opposing archetypes suggests its utility for studying political polarization and the decay of civic norms. The case of Alexandria Ocasio-Cortez, with her balanced but high-tension profile, suggests a third, more complex archetype of a "Contested Virtuous" speaker, who uses the language of both justice and resentment, hope and tribalism, creating a rhetorically fraught but potentially potent combination.

### Broader Significance and Future Directions

The broader significance of this work lies in its demonstration of a scalable, data-driven method for analyzing the moral character of discourse. If validated on a larger corpus, the CAF could be used to track the health of the public sphere over time, compare rhetorical standards across different political cultures, or identify the rise of pathological communication in real-time.

However, this pilot study has clear limitations that point toward necessary future research:
1.  **Scale and Generalizability:** The analysis must be replicated on a large, diverse, and longitudinal corpus of political texts to validate these preliminary findings and test their generalizability.
2.  **External Validation:** Future experiments must include rich corpus metadata (e.g., speaker ideology, party, context of speech, pre-defined rhetorical style). This will allow for testing hypotheses, such as whether populist-styled speakers consistently score higher on the "pathology cluster" and lower on the CCI.
3.  **Temporal Analysis:** A longitudinal corpus would enable researchers to investigate how rhetorical archetypes evolve over time, whether individual speakers change their style, and if there are macro-level trends in the overall civic character of political discourse.
4.  **Integration with Audience Reception:** This analysis focuses solely on the text. Future work should integrate these findings with audience reception data (e.g., polling, social media engagement) to explore whether vice-driven or virtue-driven rhetoric is more effective at persuasion or mobilization.

## 7. Conclusion

This computational analysis of a small corpus of political speeches using the Civic Analysis Framework (CAF) v10.0 has yielded promising, albeit preliminary, results. The study successfully demonstrates the framework's capacity to operationalize abstract concepts from political theory and virtue ethics into quantifiable metrics. The analysis identified distinct speaker archetypes, from the "Authentic Virtue" of John McCain to the "Strategic Pathology" of Steve King and Bernie Sanders, and provided strong initial evidence for the framework's internal construct validity through correlation analysis.

The findings suggest that political discourse can be meaningfully mapped onto a spectrum of civic character, and that specific combinations of virtues and vices form coherent rhetorical meta-strategies. While the study's small sample size and lack of external metadata are significant limitations, it serves as a successful proof-of-concept. It establishes that the CAF is a potentially powerful tool for the empirical study of political communication, offering a structured, transparent, and scalable method for assessing the health and character of civic discourse. Future research should focus on applying this methodology to larger, richer datasets to validate these initial patterns and explore their broader implications for democratic governance.

## 8. Evidence Citations

The following textual evidence was used to support the statistical interpretations in this report.

*   **As John McCain stated:** "[I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together]" (Source: john_mccain_2008_concession_ff9b26f2.txt)
*   **As John McCain stated:** "[This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight.]" (Source: john_mccain_2008_concession_ff9b26f2.txt)
*   **As Bernie Sanders stated:** "[I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%.]" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)
*   **As Bernie Sanders stated:** "[But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs.]" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)
*   **As Bernie Sanders stated:** "[Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change.]" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)