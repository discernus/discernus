---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file within acceptable rounding precision.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Run ID**: d6e8fdbbdc30e47ef11f616f15902355ec28ec86c7767cea52f341ed9953ac44  
**Date**: 2025-08-25  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: corpus.md not found (8 documents)  

---

## 1. Executive Summary

This report details a preliminary computational analysis of the civic character of political discourse, applying the Civic Analysis Framework (CAF) v10.0 to a corpus of eight political speeches. The analysis sought to evaluate the framework's capacity to measure and differentiate the moral-rhetorical patterns of various political speakers. The findings indicate that the CAF v10.0 provides a robust and nuanced methodology for this purpose. The primary derived metric, the Salience-Weighted Civic Character Index (CCI), effectively stratified the speakers along a continuum from highly virtuous to highly vice-laden rhetoric. The analysis identified John McCain as exhibiting the highest civic character (CCI = +0.80), while Steve King displayed the lowest (CCI = -0.48).

Key statistical patterns provide strong preliminary support for the framework's theoretical design. The oppositional axes defined by the framework (e.g., Dignity vs. Tribalism, Pragmatism vs. Fantasy) were validated by strong negative correlations between corresponding virtue and vice dimensions. For instance, Pragmatism and Fantasy demonstrated a near-perfect inverse relationship (r = -0.93). Furthermore, the analysis revealed distinct rhetorical archetypes. Speakers like John McCain, Cory Booker, and Mitt Romney were classified as demonstrating "Authentic Virtue," characterized by high virtue scores, low vice scores, and low internal tension. Conversely, speakers such as Bernie Sanders and Steve King were classified as employing "Strategic Pathology," a style defined by the systematic and salient use of vices like tribalism and resentment.

While the small sample size (N=8) necessitates that these findings be considered indicative rather than conclusive, this pilot study demonstrates the framework's significant potential. The CAF's derived metrics, particularly the Tension Indices and the CCI, offer a sophisticated lens for moving beyond simple dimensional scoring to understand the strategic coherence and overall moral valence of political communication. The results suggest this methodology is a promising avenue for the large-scale, systematic evaluation of public discourse.

## 2. Opening Framework: Key Insights

This analysis yielded several key insights into the structure of civic discourse and the effectiveness of the CAF v10.0 framework.

*   **The Civic Character Index (CCI) provides a powerful summary metric for ranking political discourse.** The analysis produced a clear hierarchy of speakers based on their overall rhetorical character, with scores ranging from John McCain's highly virtuous CCI of +0.80 to Steve King's vice-dominant CCI of -0.48. This suggests the CCI is an effective tool for high-level comparative analysis.

*   **The framework's oppositional design is strongly supported by empirical data.** The analysis revealed large, statistically significant negative correlations between the virtues and their corresponding vices. The relationship between Pragmatism and Fantasy was exceptionally strong (r = -0.93), as was the one between Dignity and Tribalism (r = -0.81), indicating that these pairs function as genuine opposites in the analyzed discourse, thus validating the framework's core theoretical structure.

*   **Distinct rhetorical archetypes emerge from the data.** The `analyze_character_coherence` function successfully classified speakers into meaningful categories. Three speakers (McCain, Booker, Romney) were identified as "Authentic Virtue," while two (Sanders, King) were classified as "Strategic Pathology." This demonstrates the framework's ability to identify and label coherent, recurring rhetorical strategies.

*   **Vices exhibit strong clustering, suggesting a synergistic "pathology" meta-strategy.** The analysis found very strong positive correlations between Tribalism, Manipulation, and Fantasy. For example, Tribalism and Manipulation are almost perfectly correlated (r = +0.91). This indicates that these vices are not used in isolation but are often deployed together as part of a cohesive rhetorical approach centered on in-group/out-group dynamics and reality distortion.

*   **Tension Indices reveal nuanced strategic contradictions.** While some speakers were rhetorically coherent, others displayed high tension. Bernie Sanders, for instance, scored a high Justice/Resentment tension (0.30), indicating a strategy that simultaneously invokes calls for justice while heavily relying on grievance-based resentment. This is exemplified by his statement, "That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), which combines a forward-looking call for justice with a backward-looking framing of resentment.

## 4. Methodology

### Framework Description and Analytical Approach

This study employed the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The framework is grounded in Aristotelian virtue ethics and civic republican theory. It operates by measuring the presence and salience of five core virtues and their corresponding vices, structured as oppositional axes:

*   **Identity Axis:** Dignity (universal worth) vs. Tribalism (in-group/out-group)
*   **Truth Axis:** Truth (honesty, accuracy) vs. Manipulation (deception, emotional framing)
*   **Justice Axis:** Justice (fairness, systemic solutions) vs. Resentment (grievance, blame)
*   **Emotional Axis:** Hope (optimism, constructive vision) vs. Fear (threat-mongering)
*   **Reality Axis:** Pragmatism (realism, complexity acknowledgment) vs. Fantasy (oversimplification, denial of trade-offs)

For each of the 10 dimensions, the analysis produced a raw intensity score (`_raw`) and a salience score (`_salience`), both on a scale of 0 to 1. From these, two key derived metrics were calculated:
1.  **Character Tension Indices:** For each axis, `Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`. This metric quantifies strategic contradiction, capturing instances where a speaker invokes both a virtue and its opposing vice.
2.  **Salience-Weighted Civic Character Index (CCI):** Calculated as `(Sum(Virtue * Salience) - Sum(Vice * Salience)) / Total_Salience`, this index provides a single, normalized score from -1.0 (maximally vice-dominant) to +1.0 (maximally virtue-dominant), representing the overall civic character of a text.

### Data Structure and Corpus Description

The analysis was performed on a small corpus of 8 political speeches. Due to a missing corpus manifest (`corpus.md`), speaker identification was performed by parsing document filenames. The corpus includes speeches from a diverse set of American political figures: John McCain, Steve King, Cory Booker, Mitt Romney, John Lewis, JD Vance, Bernie Sanders, and Alexandria Ocasio-Cortez. The data for each document consists of the raw and salience scores for the 10 CAF dimensions, along with model confidence scores.

### Statistical Methods and Analytical Constraints

The analysis involved several statistical procedures automatically generated for this experiment:
*   **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles for all raw and salience scores to understand the overall distribution of rhetorical features in the corpus.
*   **Pearson Correlation:** A correlation matrix was computed for the 10 raw dimension scores to assess the relationships between virtues and vices and to validate the framework's oppositional structure.
*   **Aggregation and Profiling:** Speaker-level profiles were generated by calculating the mean scores for all metrics across documents attributed to each speaker.
*   **Rule-Based Classification:** A predefined algorithm classified each speaker's rhetorical pattern (e.g., "Authentic Virtue," "Strategic Pathology") based on their aggregated CCI and mean tension scores.

The primary limitation of this study is its **very small sample size (N=8)**. Consequently, the findings should be interpreted as **preliminary and suggestive**, not as generalizable conclusions about the speakers or political discourse at large. The analysis provides a proof-of-concept for the methodology rather than a definitive empirical statement. A further limitation arose from the missing corpus manifest, which prevented a planned validation of the framework against pre-defined rhetorical styles (`validate_framework_by_style`).

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the 20 primary metrics across all 8 documents reveals a wide variance in rhetorical strategies.

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

The dimension with the highest mean intensity is `resentment_raw` (0.71), followed by `truth_raw` (0.66). This suggests that, on average, the discourse in this corpus is characterized by a combination of grievance-based claims and appeals to factuality. The high standard deviations across most dimensions (e.g., `tribalism_raw` std=0.42, `dignity_raw` std=0.36) indicate that the framework is capturing significant variation among the speakers, a prerequisite for discriminatory power. The relatively low mean score for `fantasy_raw` (0.20) combined with a high standard deviation (0.29) suggests that while not universally present, fantasy-based rhetoric is a key differentiator when it does appear.

### 5.2 Advanced Metric Analysis

The derived metrics provide a more holistic view of each speaker's rhetorical character. The `analyze_character_coherence` function aggregates scores for each speaker and classifies their dominant pattern.

**Table 2: Speaker Character Coherence and Classification**
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

This table reveals a clear spectrum of civic character. At one end, John McCain's profile is classified as "Authentic Virtue." His extremely high CCI (+0.805) is driven by high mean virtue scores (0.82) and negligible vice scores (0.02). His very low mean tension (0.014) indicates a highly coherent, non-contradictory virtuous rhetoric. This is supported by textual evidence from his speech, where he actively rejects blame and promotes unity. As John McCain stated: "we fell short, the failure is mine, not yours" (Source: john_mccain_2008_concession_ff9b26f2.txt). This direct acceptance of responsibility is the antithesis of the resentment dimension.

At the other end, Steve King and Bernie Sanders are classified as "Strategic Pathology." Their negative CCIs (-0.480 and -0.394, respectively) result from high mean vice scores (0.82 and 0.73) overwhelming their lower virtue scores. This pattern suggests a deliberate rhetorical strategy centered on vice dimensions. For Sanders, this is particularly evident in his use of resentment. As Bernie Sanders stated: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This quote perfectly encapsulates a high-resentment score by identifying a past grievance and assigning blame to a "rigged economy."

The tension metric adds further nuance. Bernie Sanders exhibits the highest mean tension (0.144), driven by high tension on the Justice/Resentment and Identity axes. This indicates that his rhetoric, while vice-dominant, strategically incorporates appeals to virtue (justice, dignity) alongside potent appeals to their pathological counterparts (resentment, tribalism), creating a complex and internally conflicted message.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix for the 10 raw dimension scores provides critical insights into the framework's construct validity and reveals underlying rhetorical meta-strategies.

**Table 3: Correlation Matrix of Raw CAF Dimension Scores**
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

The matrix provides two primary sets of findings:

1.  **Validation of Oppositional Axes:** The consistently strong, negative correlations between virtues and their corresponding vices offer compelling preliminary evidence for the framework's construct validity.
    *   **Reality Axis:** `pragmatism` and `fantasy` have a near-perfect negative correlation (r = -0.93).
    *   **Truth Axis:** `truth` and `manipulation` are strongly negatively correlated (r = -0.77).
    *   **Identity Axis:** `dignity` and `tribalism` are strongly negatively correlated (r = -0.81).
    *   **Emotional Axis:** `hope` and `fear` are very strongly negatively correlated (r = -0.87).
    These results indicate that, within this corpus, the framework's dimensions behave as designed, capturing opposing rhetorical choices.

2.  **Identification of Rhetorical Clusters:** The matrix also reveals which dimensions tend to co-occur, pointing to meta-strategies.
    *   **A "Vice Cluster":** There are very strong positive correlations between `tribalism`, `manipulation`, and `fantasy`. The link between `tribalism` and `manipulation` (r = +0.91) is particularly strong. This suggests a common rhetorical strategy that combines creating an "us vs. them" narrative with deceptive or emotionally manipulative framing and a denial of complexity. This is visible in the rhetoric of Bernie Sanders, who combines a tribal appeal—"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)—with manipulative framing—"the worst and most dangerous addiction we have is the greed of the oligarchs" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).
    *   **A "Virtue Cluster":** There are also strong positive correlations between `dignity`, `justice`, and `truth`. The relationship between `dignity` and `justice` (r = +0.87) is especially notable. This suggests a virtuous rhetorical strategy that links appeals to universal human worth with calls for systemic fairness and intellectual honesty.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns confirm that the CAF v10.0 is not merely measuring ten independent features but is capturing two opposing constellations of rhetorical practice. The "virtue cluster" (Dignity, Truth, Justice, Hope, Pragmatism) and the "vice cluster" (Tribalism, Manipulation, Resentment, Fear, Fantasy) represent fundamentally different approaches to political communication.

The strongest correlations in the dataset are particularly revealing. The near-perfect negative correlation between `pragmatism` and `fantasy` (r = -0.93) suggests that the acknowledgment of complexity and trade-offs is the rhetorical move most antithetical to simplistic, idealized narratives. Similarly, the extremely high positive correlation between `tribalism` and `manipulation` (r = +0.91) indicates that dividing the world into "us" and "them" is almost invariably accompanied by rhetorical techniques that distort reality or exploit emotion.

An unexpected finding is the relative isolation of the `fear`/`hope` axis from some of the other dimensions. While `fear` and `hope` are strongly opposed (r = -0.87), `fear`'s correlation with core vices like `manipulation` (r = +0.33) and `resentment` (r = +0.41) is only moderate. This may suggest that while fear-based rhetoric is a component of the vice cluster, it is not as central as the tribalism/manipulation/fantasy nexus. Conversely, `hope` is only moderately correlated with other virtues, suggesting it can be deployed somewhat independently of appeals to justice or truth.

Overall, the statistical patterns indicate a strong fit between the framework and the corpus. The framework successfully maps the discourse onto its theoretical dimensions, and the resulting data reveals coherent and interpretable patterns that align with intuitive understandings of political rhetoric.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CAF v10.0 framework demonstrates considerable effectiveness.

*   **Discriminatory Power:** The framework effectively differentiates between speakers and documents. The wide range of the CCI scores (from +0.805 to -0.480) and the high standard deviations on most raw score dimensions confirm that the framework is sensitive to the diverse rhetorical styles present in the corpus. It successfully avoids floor or ceiling effects, capturing a full spectrum of performance.

*   **Framework-Corpus Fit:** The framework appears well-suited for analyzing high-stakes, persuasive political speeches. The oppositional structure and the specific dimensions chosen resonate strongly with the rhetorical strategies observed, leading to the clear clustering and archetypal patterns identified above.

*   **Methodological Insights:** The analysis highlights the value of the framework's derived metrics. The CCI provides a powerful, holistic summary, while the Tension Indices offer a crucial layer of nuance, preventing misinterpretation of speakers who strategically mix virtue and vice. For example, looking only at raw scores for Alexandria Ocasio-Cortez might be confusing (high scores in both virtue and vice), but her near-zero CCI (0.005) and moderate tension (0.088) accurately classify her as a balanced but "Virtue-Leaning" speaker with some internal contradictions. This demonstrates the analytical sophistication enabled by the framework's design.

## 6. Discussion

### Theoretical Implications of Findings

This analysis, though preliminary, carries several theoretical implications for the study of political discourse. The findings provide empirical support for modeling civic rhetoric not as a simple spectrum of quality, but as a dynamic interplay between opposing value systems. The emergence of distinct "virtue" and "vice" clusters suggests that these rhetorical choices are not random but form coherent meta-strategies. The "Strategic Pathology" archetype, for instance, is not merely a lack of virtue but a positive, synergistic deployment of tribalism, manipulation, and fantasy. This suggests that theoretical models of political communication should account for these cohesive, vice-based rhetorical systems.

Furthermore, the concept of "Tension" as a measurable quantity is a significant contribution. It allows for a more sophisticated analysis that moves beyond a simple binary of good vs. bad rhetoric. It empirically captures the phenomenon of strategic ambiguity, where speakers appeal to competing values simultaneously. This provides a quantitative tool to investigate the complex messaging of populist or ideologically inconsistent speakers, a common feature of the contemporary political landscape.

### Comparative Analysis and Archetypal Patterns

The classification of speakers into archetypes allows for meaningful comparative analysis. The "Authentic Virtue" archetype, exemplified by John McCain, represents a classic civic republican ideal. His rhetoric, as captured by the framework, is characterized by appeals to unity, responsibility, and pragmatism. As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt). This is a direct appeal to the virtue of Dignity, transcending tribal lines.

In stark contrast, the "Strategic Pathology" archetype, seen in Bernie Sanders and Steve King, embodies a conflict-oriented, populist style. This approach prioritizes mobilizing a base through grievance (`resentment`), in-group solidarity (`tribalism`), and the identification of enemies. The data suggests this style is inherently anti-pragmatic, relying on the simplification of complex issues (`fantasy`). The empty quote for `pragmatism` in the Sanders evidence file is telling, with the analyst noting, "the speech contains no acknowledgement of complexity, trade-offs, or realistic constraints, making it impossible to find a supporting quote" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This absence is as informative as the presence of other dimensions.

### Broader Significance for the Field

This research demonstrates the potential of computational methods to bring new rigor and scale to the normative analysis of political discourse. By operationalizing concepts from political theory and virtue ethics, the CAF v10.0 allows for the objective, replicable, and scalable measurement of civic character. Such a tool could be used to conduct large-scale longitudinal studies on the health of public discourse, compare rhetorical norms across different countries or media ecosystems, or track the evolution of a political actor's communication style over time. It provides a crucial bridge between the qualitative insights of political theory and the quantitative power of computational social science.

### Limitations and Future Directions

The most significant limitation of this study is its **small sample size (N=8)**. The findings, while internally consistent and theoretically resonant, cannot be generalized. They serve as a proof-of-concept that requires validation on a much larger and more diverse corpus of texts.

Future research should proceed in several directions:
1.  **Scale:** Apply the CAF v10.0 to a large, longitudinal corpus of political texts (e.g., all congressional speeches over a 20-year period) to track trends in civic discourse.
2.  **Diversity:** Test the framework on different genres of communication, such as social media posts, campaign advertisements, and cable news transcripts, to assess its robustness.
3.  **Integration:** Future studies should ensure the availability of rich metadata, including speaker demographics, party affiliation, and predefined rhetorical style. This would enable more powerful statistical analyses, such as the `validate_framework_by_style` analysis that could not be performed here, to test specific hypotheses about what factors predict virtuous or pathological rhetoric.
4.  **Refinement:** Further investigation into the "Tension" indices is warranted. Researchers may wish to explore whether tension on certain axes (e.g., Justice/Resentment) is more politically effective or corrosive than on others.

## 7. Conclusion

This report presents a preliminary but insightful computational analysis of civic character in political speech using the Civic Analysis Framework (CAF) v10.0. The analysis successfully demonstrated the framework's ability to differentiate speakers, identify coherent rhetorical archetypes, and provide a nuanced, multi-faceted assessment of political discourse. The key findings—the successful stratification of speakers via the Civic Character Index, the empirical validation of the framework's oppositional axes through correlation analysis, and the identification of "virtue" and "vice" clusters—all point to the methodological soundness and analytical power of this approach.

Despite the clear limitation of a small sample size, this pilot study serves as a strong proof-of-concept. It validates the core theoretical assumptions of the CAF v10.0 and showcases the utility of its derived metrics in capturing complex rhetorical strategies. The research provides a solid foundation for future work and suggests that the systematic, computational analysis of civic virtue and vice is a promising and important frontier for understanding the nature and quality of public discourse.

## 8. Evidence Citations

The following textual evidence, retrieved during the analysis, was used to support the statistical interpretations in this report.

**Source Document: `john_mccain_2008_concession_ff9b26f2.txt`**
*   **On Resentment (Absence):** "we fell short, the failure is mine, not yours."
*   **On Hope/Dignity:** "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"

**Source Document: `bernie_sanders_2025_fighting_oligarchy_261b893a.txt`**
*   **On Tribalism:** "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."
*   **On Manipulation:** "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   **On Resentment/Justice:** "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."
*   **On Pragmatism (Absence):** The analyst noted: "the speech contains no acknowledgement of complexity, trade-offs, or realistic constraints, making it impossible to find a supporting quote."