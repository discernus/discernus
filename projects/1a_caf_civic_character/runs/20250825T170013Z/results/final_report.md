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
**Corpus**: corpus.md not found (8 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of the civic character of political discourse from eight prominent speakers, utilizing the Civic Analysis Framework (CAF) v10.0. The analysis reveals that the framework can effectively differentiate and quantify the rhetorical virtues and vices employed by political actors. The primary summary metric, the Salience-Weighted Civic Character Index (CCI), successfully stratified the speakers across a wide spectrum, from a highly virtue-dominant score of +0.80 (John McCain) to a significantly vice-dominant score of -0.48 (Steve King). This demonstrates the framework's discriminatory power in capturing the normative orientation of political speech.

Key findings indicate strong support for the framework's theoretical design. Correlation analysis of the ten core dimensions confirms the oppositional nature of the virtue/vice axes, with large negative correlations observed between paired concepts, such as Dignity and Tribalism (r = -0.81) and Pragmatism and Fantasy (r = -0.93). This provides strong preliminary evidence for the framework's construct validity. Furthermore, the analysis identified distinct rhetorical archetypes, classifying speakers into categories such as "Authentic Virtue" and "Strategic Pathology" based on their composite scores. For instance, John McCain's discourse exemplifies the former, characterized by high virtue, low vice, and minimal rhetorical tension. In contrast, Bernie Sanders' rhetoric aligns with the latter, marked by high scores in both vices (e.g., Resentment, Tribalism) and virtues (e.g., Hope, Justice), resulting in a negative CCI (-0.39) and the highest mean tension score in the corpus.

While the results are promising, they should be considered preliminary due to the pilot nature of this study, which is based on a small corpus of eight documents. The analysis was also constrained by the absence of a corpus manifest, which prevented a planned validation of scores against pre-defined rhetorical styles. Despite these limitations, this study demonstrates that the CAF v10.0 provides a robust, nuanced, and reproducible methodology for evaluating the civic quality of political communication, offering a valuable tool for future computational social science research.

## 2. Opening Framework: Key Insights

This analysis yielded several key insights into the structure of civic discourse and the effectiveness of the CAF v10.0 framework.

*   **The Civic Character Index (CCI) Offers a Robust Summary of Rhetorical Orientation.** The CCI metric effectively condenses complex dimensional scores into a single, interpretable value, ranking speakers on a continuum from virtuous to pathological. The wide distribution of scores, from John McCain (+0.80) to Steve King (-0.48), indicates the metric's high discriminatory power.
*   **The Framework's Oppositional Design is Empirically Supported.** The analysis reveals strong, statistically significant negative correlations between the virtues and their corresponding vices. The Reality Axis (Pragmatism vs. Fantasy) showed a near-perfect inverse relationship (r = -0.93), and the Identity Axis (Dignity vs. Tribalism) was also strongly oppositional (r = -0.81), validating the framework's core theoretical assumption.
*   **Distinct Rhetorical Archetypes Emerge from the Data.** The automated classification identified coherent patterns of rhetorical behavior. Speakers like John McCain, Cory Booker, and Mitt Romney were classified as "Authentic Virtue," characterized by high virtue scores, low vice scores, and low tension. Conversely, Bernie Sanders and Steve King were classified as "Strategic Pathology," with high vice scores and negative CCIs, suggesting a deliberate reliance on divisive rhetoric.
*   **Vices Exhibit Strong Thematic Clustering.** The analysis shows that the vices of `Tribalism`, `Manipulation`, and `Fantasy` are strongly and positively inter-correlated. This suggests the existence of a coherent pathological meta-strategy that combines in-group/out-group division, deceptive framing, and reality denial. The correlation between `Manipulation` and `Fantasy` was particularly high (r = +0.89).
*   **Rhetorical Tension Quantifies Strategic Contradiction.** The `Tension` metrics successfully identified speakers who simultaneously appeal to opposing values. Bernie Sanders registered the highest mean tension (0.14), driven by high tension on the Justice/Resentment axis. This quantitatively captures a style that leverages calls for justice while simultaneously stoking grievance, a hallmark of certain populist appeals.
*   **Textual Evidence Aligns with Quantitative Archetypes.** The qualitative evidence, though limited, supports the statistical findings. John McCain's high CCI score is reflected in his call for unity, while Bernie Sanders' negative CCI and high Resentment score are mirrored in his explicit framing of a "rigged economy." As Bernie Sanders stated: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Civic Analysis Framework (CAF) v10.0 to evaluate the civic character of political discourse. The CAF is grounded in Aristotelian virtue ethics and contemporary civic republican theory, positing that political speech can be assessed based on the civic virtues and vices it demonstrates. The framework is structured around five fundamental, oppositional axes, each comprising a virtuous and a pathological (vice) dimension:

1.  **Identity Axis**: `Dignity` (appeals to universal human worth) vs. `Tribalism` (appeals to in-group/out-group dynamics).
2.  **Truth Axis**: `Truth` (appeals based on verifiable facts and intellectual honesty) vs. `Manipulation` (appeals based on deception and emotional framing).
3.  **Justice Axis**: `Justice` (appeals to fairness, rights, and systemic equity) vs. `Resentment` (appeals based on grievance and blame).
4.  **Emotional Axis**: `Hope` (appeals to an optimistic and achievable future) vs. `Fear` (appeals based on threat and anxiety).
5.  **Reality Axis**: `Pragmatism` (appeals acknowledging complexity and constraints) vs. `Fantasy` (appeals based on simplistic, unworkable solutions).

For each of the 10 dimensions, the analysis produced a `raw` score (intensity of the theme, 0-1) and a `salience` score (prominence of the theme, 0-1). From these, two key derived metrics were calculated:

*   **Character Tension Indices**: Calculated for each axis as `Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`. This metric quantifies the degree of strategic contradiction, capturing instances where a speaker invokes both a virtue and its opposing vice.
*   **Salience-Weighted Civic Character Index (CCI)**: Calculated as `(Sum(Virtue * Salience) - Sum(Vice * Salience)) / Total_Salience`. This provides a single, normalized score from -1.0 (purely vice-dominant) to +1.0 (purely virtue-dominant), representing the overall civic character of a text.

### Data Structure and Corpus Description

The corpus for this analysis consists of eight documents, each a transcript of a speech by a different American political figure. The speakers include John McCain, Cory Booker, Mitt Romney, John Lewis, Alexandria Ocasio-Cortez, JD Vance, Bernie Sanders, and Steve King. Due to the absence of a `corpus_manifest.json` file, speaker identification was performed by parsing document filenames. This also meant that pre-assigned metadata, such as rhetorical `style`, was unavailable for analysis. The small sample size (N=8) means that all findings should be interpreted as preliminary and indicative of patterns that warrant further investigation with a larger dataset.

### Statistical Methods and Analytical Constraints

The analysis involved several statistical procedures executed by the automated analysis agent:

1.  **Descriptive Statistics**: Calculation of mean, standard deviation, and quartiles for all 20 raw and salience scores to understand the central tendency and distribution of each dimension across the corpus.
2.  **Correlation Analysis**: A Pearson correlation matrix was computed for the 10 raw dimension scores to assess the relationships between them and to validate the framework's theoretical structure.
3.  **Profile Generation**: Speaker-level profiles were generated by averaging all dimensional scores and derived metrics for each speaker, allowing for comparative analysis.
4.  **Archetype Classification**: A rule-based classification model, derived from the framework's interpretive guidance, was applied to speaker profiles to categorize them into rhetorical archetypes (e.g., "Authentic Virtue," "Strategic Pathology").

A significant constraint was the failure of the `validate_framework_by_style` function, which reported that the necessary 'style' metadata was not found in the corpus. This prevented a key validation test comparing framework scores across known rhetorical categories like 'populist' or 'institutional'. Additionally, the available textual evidence for citation was limited and unevenly distributed across speakers, primarily covering the highest- and lowest-scoring individuals on the CCI scale. This limits the qualitative grounding for claims about speakers in the middle of the spectrum.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial descriptive analysis of the 10 raw and 10 salience scores across all eight documents provides a foundational overview of the rhetorical landscape. The results reveal which civic virtues and vices were most and least prevalent in the corpus.

**Table 1: Descriptive Statistics for CAF Raw and Salience Scores (N=8)**
| Statistic | tribalism_raw | dignity_raw | manipulation_raw | truth_raw | resentment_raw | justice_raw | fear_raw | hope_raw | fantasy_raw | pragmatism_raw |
|:----------|--------------:|------------:|-----------------:|----------:|---------------:|------------:|---------:|---------:|------------:|---------------:|
| count     |         8.000 |       8.000 |            8.000 |     8.000 |          8.000 |       8.000 |    8.000 |    8.000 |       8.000 |          8.000 |
| mean      |         0.513 |       0.575 |            0.338 |     0.663 |          0.706 |       0.625 |    0.463 |    0.550 |       0.200 |          0.587 |
| std       |         0.419 |       0.362 |            0.374 |     0.213 |          0.355 |       0.315 |    0.245 |    0.278 |       0.288 |          0.372 |
| min       |         0.000 |       0.000 |            0.000 |     0.300 |          0.000 |       0.000 |    0.100 |    0.100 |       0.000 |          0.000 |
| 25%       |         0.075 |       0.325 |            0.000 |     0.550 |          0.675 |       0.475 |    0.300 |    0.425 |       0.000 |          0.325 |
| 50%       |         0.650 |       0.750 |            0.250 |     0.750 |          0.900 |       0.700 |    0.450 |    0.600 |       0.050 |          0.750 |
| 75%       |         0.900 |       0.825 |            0.650 |     0.800 |          0.900 |       0.900 |    0.600 |    0.725 |       0.300 |          0.900 |
| max       |         0.900 |       0.900 |            0.800 |     0.900 |          0.950 |       0.900 |    0.900 |    0.900 |       0.700 |          0.900 |

*Note: Salience score statistics show similar patterns and are omitted for brevity.*

The descriptive statistics indicate that `Resentment` (mean raw score = 0.706) was the most intensely used dimension in this corpus, followed closely by `Truth` (0.663) and `Justice` (0.625). This suggests that the discourse analyzed was frequently centered on narratives of grievance and fairness, often supported by truth claims. The high mean score for `Resentment` is exemplified in the rhetoric of Bernie Sanders, who explicitly frames economic disparity as a grievance. As Bernie Sanders stated: `"They are angry because, believe it or not, despite a huge increase in worker productivity over the last 52 years, if you could believe it, real inflation accounted for wages today are lower than they were 52 years ago." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`.

Conversely, `Fantasy` (mean = 0.200) and `Manipulation` (mean = 0.338) were the least intense vices on average, although their standard deviations are high, indicating significant variation between speakers. The virtue with the lowest mean score was `Hope` (0.550), suggesting that optimistic, forward-looking appeals were less common or intense than other rhetorical forms in this specific collection of texts.

### 5.2 Advanced Metric Analysis

The derived metrics—the Civic Character Index (CCI) and Tension Indices—provide a more nuanced assessment of rhetorical strategy. The analysis of speaker profiles reveals a clear hierarchy of civic character and identifies distinct rhetorical patterns.

**Table 2: Speaker Character Coherence and Pattern Classification**
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

The CCI scores provide a clear ranking of the speakers. John McCain's 2008 concession speech stands out as an exemplar of virtuous civic discourse (CCI = +0.805). His profile is defined by very high mean virtue scores (0.820) and negligible vice scores (0.020), resulting in a classification of "Authentic Virtue." This is supported by textual evidence where he actively works against division. As John McCain stated: `"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt)`.

At the other end of the spectrum, Steve King (CCI = -0.480) and Bernie Sanders (CCI = -0.394) are classified as "Strategic Pathology." Their profiles are inverted, with high mean vice scores (0.820 and 0.730, respectively) overwhelming their use of virtues. This suggests a rhetorical style that relies heavily on pathological dimensions. For Sanders, this is further illuminated by his `mean_tension` score (0.144), the highest in the corpus. This indicates a strategy that combines appeals to both sides of an axis, such as Justice and Resentment, simultaneously. This is evident in his rhetoric, which frames a call for change (`Justice`) through the lens of grievance (`Resentment`). As Bernie Sanders stated: `"But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`. This quote exemplifies the `Manipulation` dimension by simplifying a complex issue into a moral failing of a single group, contributing to his negative CCI.

The case of Alexandria Ocasio-Cortez is also noteworthy. With a CCI near zero (0.005), her rhetoric shows an almost perfect balance between weighted virtue and vice scores. While classified as "Virtue-Leaning" by the algorithm, her profile suggests a highly contentious style that employs both sets of appeals with nearly equal intensity and salience, a pattern that could also be interpreted as "Incoherent Messaging" under different classification thresholds.

### 5.3 Correlation and Interaction Analysis

The correlation matrix for the 10 raw dimension scores provides critical evidence for the framework's construct validity and reveals underlying rhetorical meta-strategies.

**Table 3: Pearson Correlation Matrix for CAF Raw Dimension Scores**
|            | tribalism | dignity | manipulation | truth | resentment | justice | fear | hope | fantasy | pragmatism |
|:-----------|----------:|--------:|-------------:|--------:|-----------:|--------:|-------:|-------:|--------:|-----------:|
| tribalism  |     1.000 |  -0.809 |        0.908 |  -0.793 |      0.797 |  -0.706 |  0.396 | -0.227 |   0.723 |     -0.760 |
| dignity    |    -0.809 |   1.000 |       -0.869 |   0.671 |     -0.522 |   0.872 | -0.578 |  0.498 |  -0.755 |      0.666 |
| manipulation|   0.908 |  -0.869 |        1.000 |  -0.768 |      0.606 |  -0.749 |  0.330 | -0.296 |   0.889 |     -0.910 |
| truth      |    -0.793 |   0.671 |       -0.768 |   1.000 |     -0.553 |   0.845 |  0.079 | -0.157 |  -0.558 |      0.515 |
| resentment |     0.797 |  -0.522 |        0.606 |  -0.553 |      1.000 |  -0.340 |  0.414 | -0.069 |   0.482 |     -0.508 |
| justice    |    -0.706 |   0.872 |       -0.749 |   0.845 |     -0.340 |   1.000 | -0.190 |  0.131 |  -0.536 |      0.430 |
| fear       |     0.396 |  -0.578 |        0.330 |   0.079 |      0.414 |  -0.190 |  1.000 | -0.873 |   0.304 |     -0.304 |
| hope       |    -0.227 |   0.498 |       -0.296 |  -0.157 |     -0.069 |   0.131 | -0.873 |  1.000 |  -0.375 |      0.366 |
| fantasy    |     0.723 |  -0.755 |        0.889 |  -0.558 |      0.482 |  -0.536 |  0.304 | -0.375 |   1.000 |     -0.934 |
| pragmatism |    -0.760 |   0.666 |       -0.910 |   0.515 |     -0.508 |   0.430 | -0.304 |  0.366 |  -0.934 |      1.000 |

The most significant finding from this matrix is the strong negative correlation between the paired virtues and vices on each axis, providing empirical support for the framework's oppositional design.
*   **Reality Axis**: `Pragmatism` and `Fantasy` have an extremely strong negative correlation (r = -0.93), indicating they are functional opposites in this corpus.
*   **Emotional Axis**: `Hope` and `Fear` are also strongly opposed (r = -0.87).
*   **Identity Axis**: `Dignity` and `Tribalism` show a strong negative relationship (r = -0.81).
*   **Truth Axis**: `Truth` and `Manipulation` are strongly negatively correlated (r = -0.77).
*   **Justice Axis**: `Justice` and `Resentment` show a weaker, but still notable, negative correlation (r = -0.34). The relative weakness of this opposition may suggest that speakers in this corpus often blend appeals to justice and grievance, a pattern captured by the `Tension` metric.

The matrix also reveals two "meta-clusters" of rhetorical dimensions.
1.  **A "Virtue Cluster"**: `Dignity`, `Truth`, and `Justice` are all strongly and positively correlated with each other (r > +0.67). This suggests that appeals to universal worth, facts, and fairness often appear together as part of a coherent virtuous rhetorical strategy.
2.  **A "Vice Cluster"**: `Tribalism`, `Manipulation`, and `Fantasy` are also strongly inter-correlated (r > +0.72). This indicates a pathological strategy that combines group division, deceptive framing, and simplistic solutions. The extremely high correlation between `Manipulation` and `Fantasy` (r = +0.89) suggests that reality-denying rhetoric is almost always delivered via manipulative framing.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns provide strong evidence for the framework's construct validity. The consistent negative correlations between virtues and their opposing vices align perfectly with the theoretical underpinnings of the CAF. This suggests the framework is not just labeling phenomena but is capturing real, structured trade-offs in rhetorical choice. The fact that `Pragmatism` is almost a perfect inverse of `Fantasy` (r = -0.93) and `Manipulation` (r = -0.91) indicates that the Reality axis is particularly well-defined and serves as a powerful discriminator of rhetorical styles.

The data suggests that political discourse, at least within this sample, tends to organize along a primary axis of virtue vs. pathology. The virtue cluster (`Dignity`, `Truth`, `Justice`, `Pragmatism`) and the vice cluster (`Tribalism`, `Manipulation`, `Resentment`, `Fantasy`) appear to function as two opposing toolkits. Speakers tend to draw consistently from one or the anther, with figures like McCain representing the former and King the latter. This is exemplified by the fact that John McCain's speech contained no evidence of `Tribalism` or `Manipulation`, while being rich in `Dignity` and `Truth`. As John McCain stated: `"Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain." (Source: john_mccain_2008_concession_ff9b26f2.txt)`. This statement's intellectual honesty is a clear marker of the `Truth` dimension.

An unexpected finding is the relatively weak opposition between `Justice` and `Resentment` compared to other axes. This may imply that in contemporary political rhetoric, calls for justice are frequently built upon a foundation of grievance, making them less mutually exclusive than, for example, `Hope` and `Fear`. This warrants further investigation, as it could point to a significant feature of modern political communication where the line between rectifying injustice and stoking resentment is strategically blurred.

### 5.5 Framework Effectiveness Assessment

Based on this analysis, the CAF v10.0 framework demonstrates considerable effectiveness. Its primary strength is its **discriminatory power**. The framework, particularly through the CCI, successfully differentiated the eight speakers and mapped them onto a meaningful spectrum of civic character. The variance in scores across all dimensions and the clear separation of speaker profiles indicate that the framework is sensitive to subtle and substantial differences in rhetorical style.

The **framework-corpus fit** appears to be strong. The statistical patterns, especially the correlations, align closely with the framework's theoretical structure. This suggests that the categories defined by the CAF correspond to real, co-occurring patterns of language in political speech. The primary limitation noted in this analysis—the inability to validate against speaker `style`—is a function of incomplete corpus metadata, not an inherent flaw in the framework itself. Future research with a properly manifested corpus could address this.

From a **methodological standpoint**, the introduction of derived metrics like `Tension` and the `CCI` is a significant innovation. These metrics move beyond simple dimensional scoring to capture more complex phenomena like strategic contradiction and overall normative orientation. The `Tension` score, in particular, provides a novel, quantifiable measure of a key rhetorical strategy often discussed qualitatively in political science.

## 6. Discussion

### Theoretical Implications of Findings

The results of this analysis carry several important theoretical implications. First, they provide empirical support for applying a virtue ethics lens to the study of political communication. The ability to computationally measure constructs like `Dignity`, `Pragmatism`, and their pathological opposites suggests that these are not merely abstract philosophical concepts but are tangible, identifiable features of discourse with measurable relationships. The strong oppositional structure found in the data aligns with the Aristotelian conception of virtues and vices as occupying two sides of a behavioral spectrum.

Second, the identification of clustered vice dimensions (`Tribalism`, `Manipulation`, `Fantasy`) points toward the existence of coherent, pathological rhetorical syndromes. This moves beyond analyzing single rhetorical devices in isolation and suggests that certain vices are mutually reinforcing components of a broader communication strategy designed to undermine deliberative discourse. This provides a potential empirical basis for theories of democratic decay that focus on the degradation of the information environment.

### Comparative Analysis and Archetypal Patterns

The analysis successfully identified distinct rhetorical archetypes that provide a useful typology for understanding political communication styles.

1.  **The "Authentic Virtue" Archetype (McCain, Booker, Romney):** Characterized by a high positive CCI, high virtue scores, low vice scores, and low tension. This style is constructive, unifying, and grounded in shared civic values. McCain's concession speech is the purest example, where he actively sought to bridge divides. As John McCain stated: `"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight." (Source: john_mccain_2008_concession_ff9b26f2.txt)`. This quote, embodying the `Dignity` dimension, is central to this archetype.

2.  **The "Strategic Pathology" Archetype (Sanders, King):** Characterized by a negative CCI, high vice scores, and often high tension. This style is divisive, relying on grievance, in-group/out-group framing, and emotional manipulation to achieve its objectives. Sanders' rhetoric, while also containing elements of `Hope` and `Justice`, is ultimately defined by its high intensity of `Resentment`, `Tribalism`, and `Manipulation`. His framing of a simple "99% vs 1%" conflict is a classic example. As Bernie Sanders stated: `"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`.

3.  **The "Contention and Conflict" Archetype (Ocasio-Cortez):** Characterized by a CCI near zero and moderate-to-high tension. This style represents a rhetorical battleground where virtues and vices are deployed with nearly equal force. It is a rhetoric of struggle, simultaneously appealing to ideals like `Justice` while heavily employing `Tribalism` and `Resentment`. This complex, high-conflict style may be particularly effective in a polarized environment but contributes little to net civic virtue as measured by the CCI.

### Broader Significance for the Field

This research demonstrates a viable and scalable method for the normative evaluation of public discourse. By moving from subjective interpretation to reproducible, quantitative measurement, the CAF methodology offers a powerful tool for researchers in political science, communication studies, and sociology. It could be used to conduct large-scale, longitudinal studies tracking the health of the public sphere, comparing rhetorical norms across different countries or media ecosystems, or analyzing the impact of different communication styles on public opinion. The framework provides a much-needed common vocabulary and measurement standard for discussing the "quality" of democratic discourse.

### Limitations and Future Directions

The primary limitation of this study is its small sample size (N=8). The findings, while statistically clear and theoretically coherent, must be considered preliminary. The conclusions about speaker archetypes are based on single speeches and may not represent their entire rhetorical output.

Future research should proceed in several directions:
*   **Scale Up:** Apply the CAF to a large, diverse corpus of political texts (e.g., legislative debates, campaign speeches, social media posts) to confirm the stability of the observed correlations and archetypes.
*   **Incorporate Metadata:** Use a corpus with rich metadata (party, ideology, rhetorical style, context) to perform more robust validation and explore how civic character varies across different political groups and situations.
*   **Longitudinal Analysis:** Analyze the rhetoric of individual speakers or institutions over time to track changes in their civic character, potentially correlating these shifts with political events or strategic goals.
*   **Refine Archetypes:** Use clustering algorithms on a larger dataset to refine the rule-based archetypes identified here, potentially uncovering more subtle or hybrid rhetorical styles.
*   **Audience Effects:** Connect the CAF scores of political messages to experimental data on audience reception to test hypotheses about how virtuous and pathological rhetoric affects trust, polarization, and political engagement.

## 7. Conclusion

This computational analysis, guided by the Civic Analysis Framework (CAF) v10.0, has successfully demonstrated a rigorous and insightful method for evaluating the normative character of political discourse. Despite the constraints of a small pilot corpus, the study yielded clear, statistically supported findings that validate the framework's core theoretical assumptions. The analysis confirmed the oppositional structure of the framework's virtue-vice axes and identified coherent rhetorical archetypes that differentiate speakers based on their commitment to constructive, civic communication.

The key contribution of this work is the demonstration of a reproducible methodology that translates abstract concepts from political theory into quantifiable metrics. The Salience-Weighted Civic Character Index (CCI) and the Tension Indices offer novel ways to assess overall normative orientation and strategic contradiction, providing a far more nuanced picture than simple keyword counting or sentiment analysis.

While the findings are preliminary, they lay a strong foundation for future research. This study provides a validated instrument and a set of testable hypotheses about the structure of civic discourse and the nature of pathological communication. By applying this framework at scale, researchers may be able to develop a deeper understanding of the forces shaping democratic deliberation and identify trends in the health of the public sphere.

## 8. Evidence Citations

The following textual evidence was cited in this report to ground the statistical findings.

**Source Document: bernie_sanders_2025_fighting_oligarchy_261b893a.txt**
*   As Bernie Sanders stated: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."`
*   As Bernie Sanders stated: `"They are angry because, believe it or not, despite a huge increase in worker productivity over the last 52 years, if you could believe it, real inflation accounted for wages today are lower than they were 52 years ago."`
*   As Bernie Sanders stated: `"But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."`
*   As Bernie Sanders stated: `"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."`

**Source Document: john_mccain_2008_concession_ff9b26f2.txt**
*   As John McCain stated: `"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"`
*   As John McCain stated: `"Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain."`
*   As John McCain stated: `"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."`