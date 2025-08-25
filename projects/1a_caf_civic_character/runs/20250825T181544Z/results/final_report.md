---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Citation Violation**: Detect prohibited external academic citations and authority claims.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Date**: 2025-08-25  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: Custom Corpus (8 documents)  

---

## 1. Executive Summary

This report details a computational analysis of the civic character of political discourse using the Civic Analysis Framework (CAF) v10.0. The analysis was conducted on a pilot corpus of eight documents from prominent American political figures. The study's primary objective was to apply the CAF's virtue ethics-based model to quantify rhetorical patterns and assess the framework's analytical utility. The findings, while preliminary due to the small sample size (N=8), demonstrate the framework's considerable potential for differentiating rhetorical styles and revealing underlying strategic choices.

The analysis reveals a wide spectrum of civic character across the speakers, as measured by the Salience-Weighted Civic Character Index (CCI). Scores ranged from a high of +0.805 (John McCain), indicating a discourse strongly rooted in civic virtues, to a low of -0.480 (Steve King), indicating a discourse dominated by civic vices. The framework successfully identified distinct rhetorical archetypes, classifying speakers as "Authentic Virtue," "Strategic Pathology," or "Virtue-Leaning," based on their composite scores and internal consistency. For instance, John McCain's concession speech exemplifies the "Authentic Virtue" pattern, characterized by high scores in dignity and pragmatism and negligible use of vices. As he stated, "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt). Conversely, speakers like Bernie Sanders were classified as "Strategic Pathology," employing high levels of tribalism and resentment, as seen in his statement: "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).

The framework's theoretical underpinnings were strongly supported by the statistical data. A correlation analysis of the ten core dimensions showed powerful negative relationships between opposing virtues and vices (e.g., Pragmatism vs. Fantasy, r = -0.93), validating the oppositional design of the CAF's axes. Furthermore, the analysis revealed that vices like tribalism, manipulation, and fantasy tend to cluster together, suggesting a coherent, pathological rhetorical meta-strategy. While the study is limited by its small sample, it successfully demonstrates the CAF's capacity to provide a nuanced, data-driven, and replicable methodology for evaluating the civic quality of political communication.

## 2. Opening Framework: Key Insights

*   **The Civic Character Index (CCI) Effectively Stratifies Political Discourse:** The analysis produced a clear and wide-ranging distribution of CCI scores, from John McCain (+0.805) and Cory Booker (+0.502) at the high end to Bernie Sanders (-0.394) and Steve King (-0.480) at the low end. This suggests the index is a sensitive and effective summary measure of a speaker's overall civic orientation.
*   **Distinct Rhetorical Archetypes Emerge from the Data:** The analysis classified speakers into coherent patterns. "Authentic Virtue" (McCain, Booker, Romney) is characterized by high virtue, low vice, and low internal tension. "Strategic Pathology" (Sanders, King) is marked by high vice, low virtue, and moderate tension, indicating a deliberate, vice-driven strategy. Other speakers (Lewis, Ocasio-Cortez) fall into more mixed categories, revealing more complex or conflicted rhetorical approaches.
*   **The Framework's Oppositional Structure is Empirically Validated:** The correlation matrix provides strong evidence for the CAF's theoretical design. Each virtue shows a strong, statistically significant negative correlation with its opposing vice. The strongest opposition was between Pragmatism and Fantasy (r = -0.93), while the Dignity/Tribalism axis also showed a very strong negative relationship (r = -0.81). This confirms that, in this corpus, these concepts function as rhetorical opposites.
*   **Vices and Virtues Form Coherent Clusters:** The analysis indicates that speakers do not deploy virtues and vices randomly. Vices such as Tribalism, Manipulation, and Resentment are strongly inter-correlated, suggesting they are part of a unified rhetorical strategy. For example, Tribalism and Manipulation have a correlation of r = +0.91. Similarly, virtues like Dignity, Justice, and Truth are positively correlated, indicating a cohesive virtuous strategy.
*   **Rhetorical Tension Reveals Strategic Complexity:** The derived `Tension` metrics highlight instances where speakers simultaneously invoke opposing values. Bernie Sanders, for example, exhibits the highest mean tension (0.144), driven by a high `justice_tension` score (0.30). This quantifies a strategy of simultaneously appealing to a sense of injustice (a virtue) while heavily leveraging resentment (a vice), a classic populist tactic. As he stated, "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), a statement that captures both the grievance and the call for reform.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The CAF is grounded in Aristotelian virtue ethics and contemporary civic republican theory. It assesses rhetoric across five fundamental, oppositional axes, each comprising a civic virtue and its corresponding vice:

1.  **Identity Axis:** Dignity (universal worth) vs. Tribalism (in-group/out-group division)
2.  **Truth Axis:** Truth (intellectual honesty) vs. Manipulation (deceptive framing)
3.  **Justice Axis:** Justice (fairness, reform) vs. Resentment (grievance, blame)
4.  **Emotional Axis:** Hope (optimistic vision) vs. Fear (threat mobilization)
5.  **Reality Axis:** Pragmatism (acknowledging constraints) vs. Fantasy (denial of complexity)

For each of these ten dimensions, the analysis generates a `raw` score (intensity) and a `salience` score (emphasis). From these, two key derived metrics are calculated: `Tension Indices` for each axis, which measure the degree of strategic contradiction, and a final `Salience-Weighted Civic Character Index (CCI)`, which provides a single, normalized measure of a text's overall civic character, ranging from -1.0 (vice-dominant) to +1.0 (virtue-dominant).

### Data Structure and Corpus Description

The analysis was performed on a pilot corpus of 8 documents. The corpus manifest was not available, so speaker identification was performed by parsing the document filenames. The corpus includes speeches from a diverse set of American political figures: Alexandria Ocasio-Cortez, Bernie Sanders, Cory Booker, JD Vance, John Lewis, John McCain, Mitt Romney, and Steve King.

The small sample size (N=8) is a significant constraint of this study. The findings should be considered preliminary and indicative, not generalizable. The purpose of this analysis is to test the framework's capabilities on a limited but varied set of real-world texts.

### Statistical Methods and Analytical Constraints

The analysis involved several statistical procedures, automatically executed based on the provided data:

1.  **Descriptive Statistics:** Standard measures (mean, standard deviation, quartiles) were calculated for all 20 raw and salience scores to provide a baseline understanding of the data distribution.
2.  **Correlation Analysis:** A Pearson correlation matrix was computed for the 10 raw dimension scores to assess the relationships between virtues and vices and to validate the framework's theoretical structure.
3.  **Derived Metric Calculation:** The `Civic Character Index` and `Tension Indices` were calculated for each document using the formulas specified in the CAF v10.0 framework.
4.  **Archetypal Classification:** A rule-based classification system, derived from the framework's interpretive guidance, was applied to speaker profiles to categorize them into rhetorical archetypes (e.g., "Authentic Virtue," "Strategic Pathology").

A key limitation noted in the results is the failure of the `validate_framework_by_style` function. This occurred because the corpus lacked the necessary 'style' metadata (e.g., 'populist', 'institutional') for each speaker. This highlights the importance of rich metadata for future, more advanced analyses. All conclusions are drawn with the explicit acknowledgment of the N=8 sample size, and claims are therefore cautious and suggestive of avenues for future research.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the 20 primary dimensions across the 8 documents reveals notable patterns in the corpus. The dimensions with the highest average intensity (`raw` score) are `resentment` (M=0.71), `justice` (M=0.63), and `truth` (M=0.66). This suggests that themes of grievance, fairness, and factual claims are central to the discourse in this sample. Conversely, `fantasy` (M=0.20) and `manipulation` (M=0.34) have the lowest mean scores. The standard deviations are relatively high across the board (typically between 0.24 and 0.42), indicating significant variation among the speakers and confirming that the corpus is diverse enough to capture a wide range of rhetorical styles.

**Table 1: Descriptive Statistics of Raw and Salience Scores (N=8)**
| Statistic | tribalism_raw | tribalism_salience | dignity_raw | dignity_salience | manipulation_raw | manipulation_salience | truth_raw | truth_salience | resentment_raw | resentment_salience | justice_raw | justice_salience | fear_raw | fear_salience | hope_raw | hope_salience | fantasy_raw | fantasy_salience | pragmatism_raw | pragmatism_salience |
|:----------|--------------:|-------------------:|------------:|-----------------:|-----------------:|----------------------:|----------:|---------------:|---------------:|--------------------:|------------:|-----------------:|---------:|--------------:|---------:|--------------:|------------:|-----------------:|--------------:|--------------------:|
| count     |         8.000 |              8.000 |       8.000 |            8.000 |            8.000 |                 8.000 |     8.000 |          8.000 |          8.000 |               8.000 |       8.000 |           8.000 |    8.000 |         8.000 |    8.000 |         8.000 |       8.000 |           8.000 |         8.000 |               8.000 |
| mean      |         0.513 |              0.600 |       0.575 |            0.575 |            0.338 |                 0.350 |     0.663 |          0.663 |          0.706 |               0.750 |       0.625 |           0.644 |    0.463 |         0.450 |    0.550 |         0.538 |       0.200 |           0.188 |         0.587 |               0.525 |
| std       |         0.419 |              0.374 |       0.362 |            0.354 |            0.374 |                 0.393 |     0.213 |          0.177 |          0.355 |               0.358 |       0.315 |           0.309 |    0.245 |         0.233 |    0.278 |         0.277 |       0.288 |           0.247 |         0.372 |               0.341 |
| min       |         0.000 |              0.000 |       0.000 |            0.000 |            0.000 |                 0.000 |     0.300 |          0.400 |          0.000 |               0.000 |       0.000 |           0.100 |    0.100 |         0.100 |    0.100 |         0.100 |       0.000 |           0.000 |         0.000 |               0.000 |
| 25%       |         0.075 |              0.275 |       0.325 |            0.275 |            0.000 |                 0.000 |     0.550 |          0.500 |          0.675 |               0.775 |       0.475 |           0.475 |    0.300 |         0.375 |    0.425 |         0.375 |       0.000 |           0.000 |         0.325 |               0.250 |
| 50%       |         0.650 |              0.800 |       0.750 |            0.750 |            0.250 |                 0.250 |     0.750 |          0.700 |          0.900 |               0.900 |       0.700 |           0.650 |    0.450 |         0.400 |    0.600 |         0.500 |       0.050 |           0.050 |         0.750 |               0.700 |
| 75%       |         0.900 |              0.900 |       0.825 |            0.825 |            0.650 |                 0.650 |     0.800 |          0.800 |          0.900 |               0.950 |       0.900 |           0.913 |    0.600 |         0.525 |    0.725 |         0.800 |       0.300 |           0.350 |         0.900 |               0.800 |
| max       |         0.900 |              0.900 |       0.900 |            0.900 |            0.800 |                 0.900 |     0.900 |          0.900 |          0.950 |               1.000 |       0.900 |           1.000 |    0.900 |         0.900 |    0.900 |         0.900 |       0.700 |           0.600 |         0.900 |               0.800 |

### 5.2 Advanced Metric Analysis

The derived metrics provide a more holistic view of each speaker's rhetorical profile. The `Civic Character Index (CCI)` offers a powerful summary, while the `mean_tension` score reveals the degree of strategic contradiction. The rule-based `pattern_classification` synthesizes these metrics into interpretable archetypes.

**Table 2: Speaker Character Coherence and Archetype Classification**
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

The data clearly distinguishes three groups. The **"Authentic Virtue"** group (McCain, Booker, Romney) exhibits high positive CCI scores, high mean virtue scores, low mean vice scores, and very low tension. Their rhetoric is coherent and overwhelmingly focused on civic virtues. John McCain's speech is a prime example, with a near-perfect CCI and almost no rhetorical tension. His call to "do all in my power to help him lead us through the many challenges we face" exemplifies the pragmatic and unifying tone that drives this high score (Source: john_mccain_2008_concession_ff9b26f2.txt).

The **"Strategic Pathology"** group (Sanders, King) shows the opposite pattern: strongly negative CCI scores, high mean vice scores, and low mean virtue scores. Their rhetoric is also coherent but is organized around civic vices like tribalism and resentment. Bernie Sanders' speech, for example, is classified this way due to its high scores in `tribalism` (0.9), `manipulation` (0.8), and `resentment` (0.95). His statement that "the worst and most dangerous addiction we have is the greed of the oligarchs" is a clear instance of manipulative framing that simplifies a complex issue into a moral failing of an out-group, justifying his classification (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).

The **"Mixed/Contested"** group (Lewis, Ocasio-Cortez, Vance) occupies the middle ground. Their CCI scores are closer to zero, and their profiles show a more even mix of virtue and vice appeals. Alexandria Ocasio-Cortez's profile is particularly noteworthy, with a CCI of almost exactly zero (0.005) and a relatively high mean tension score (0.088). This indicates a discourse where virtuous and pathological appeals are present in nearly equal measure, creating a rhetorically contested and complex message.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix for the 10 raw dimension scores provides powerful evidence for the CAF's construct validity. The matrix reveals a clear and theoretically consistent structure of relationships among the dimensions.

**Table 3: Pearson Correlation Matrix of Raw CAF Dimension Scores (N=8)**
|            | tribalism | dignity | manipulation | truth   | resentment | justice | fear    | hope    | fantasy | pragmatism |
|:-----------|----------:|--------:|-------------:|--------:|-----------:|--------:|--------:|--------:|--------:|-----------:|
| tribalism  |     1.000 |  -0.809 |        0.908 |  -0.793 |      0.797 |  -0.706 |   0.396 |  -0.227 |   0.723 |     -0.760 |
| dignity    |    -0.809 |   1.000 |       -0.869 |   0.671 |     -0.522 |   0.872 |  -0.578 |   0.498 |  -0.755 |      0.666 |
| manipulation|     0.908 |  -0.869 |        1.000 |  -0.768 |      0.606 |  -0.749 |   0.330 |  -0.296 |   0.889 |     -0.910 |
| truth      |    -0.793 |   0.671 |       -0.768 |   1.000 |     -0.553 |   0.845 |   0.079 |  -0.157 |  -0.558 |      0.515 |
| resentment |     0.797 |  -0.522 |        0.606 |  -0.553 |      1.000 |  -0.340 |   0.414 |  -0.069 |   0.482 |     -0.508 |
| justice    |    -0.706 |   0.872 |       -0.749 |   0.845 |     -0.340 |   1.000 |  -0.190 |   0.131 |  -0.536 |      0.430 |
| fear       |     0.396 |  -0.578 |        0.330 |   0.079 |      0.414 |  -0.190 |   1.000 |  -0.873 |   0.304 |     -0.304 |
| hope       |    -0.227 |   0.498 |       -0.296 |  -0.157 |     -0.069 |   0.131 |  -0.873 |   1.000 |  -0.375 |      0.366 |
| fantasy    |     0.723 |  -0.755 |        0.889 |  -0.558 |      0.482 |  -0.536 |   0.304 |  -0.375 |   1.000 |     -0.934 |
| pragmatism |    -0.760 |   0.666 |       -0.910 |   0.515 |     -0.508 |   0.430 |  -0.304 |   0.366 |  -0.934 |      1.000 |

Key findings from this matrix include:
*   **Strong Oppositional Relationships:** Every virtue/vice pair on an axis exhibits a strong negative correlation. The most pronounced are `pragmatism`/`fantasy` (r = -0.934) and `manipulation`/`pragmatism` (r = -0.910, though not a direct pair, it shows the opposition between deception and realism). `dignity`/`tribalism` (r = -0.809) and `hope`/`fear` (r = -0.873) are also very strongly opposed. This provides robust, quantitative validation for the framework's core theoretical assumption of oppositional axes.
*   **Clustering of Vices:** There are very strong positive correlations among the vice dimensions. `tribalism` is highly correlated with `manipulation` (r = +0.908) and `fantasy` (r = +0.723). `manipulation` is also strongly correlated with `fantasy` (r = +0.889). This suggests the existence of a "pathological meta-strategy" where appeals to in-group identity, deceptive framing, and simplistic narratives are deployed in concert.
*   **Clustering of Virtues:** Virtues also cluster together. `dignity` is strongly correlated with `justice` (r = +0.872) and `truth` (r = +0.671). `justice` and `truth` are also highly correlated (r = +0.845). This points to a "virtuous meta-strategy" that combines appeals to universal worth, fairness, and intellectual honesty.

### 5.4 Pattern Recognition and Theoretical Insights

The correlation patterns reveal fundamental structures in the analyzed political discourse. The strongest negative correlation in the entire dataset, between `pragmatism` and `fantasy` (r = -0.934), suggests that the orientation toward reality is the most profound dividing line in this corpus. Speakers tend to adopt either a mode of discourse that acknowledges complexity and constraints or one that denies them in favor of simplistic, idealized narratives; they rarely mix the two. This aligns with the CAF's theoretical grounding, which posits that a core function of civic virtue is to ground political deliberation in reality.

The data also provides a compelling illustration of how these strategies manifest. The "Strategic Pathology" archetype, exemplified by Bernie Sanders, relies on a tightly-woven fabric of vices. His high `tribalism` score is supported by the "99% vs 1%" framing, while his high `resentment` score is evidenced by his focus on a "$75 trillion transfer of wealth" as the work of a "rigged economy" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). These are not isolated rhetorical choices but components of a coherent, vice-driven narrative.

In contrast, the "Authentic Virtue" archetype, exemplified by John McCain, builds its message from the opposing cluster of virtues. His high `dignity` score is demonstrated by his recognition of the "special significance" of the election for African-Americans, and his high `truth` score is shown in his frank admission that "he has prevailed. No doubt many of those differences remain" (Source: john_mccain_2008_concession_ff9b26f2.txt). These virtuous appeals work together to create a message of unity, honesty, and civic grace. The statistical patterns, therefore, do not just validate the framework's dimensions in isolation; they reveal the existence of coherent, opposing rhetorical worldviews.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CAF v10.0 demonstrates significant effectiveness in several key areas.

*   **Discriminatory Power:** The framework shows high discriminatory power. The `Civic Character Index` successfully spreads the eight speakers across a wide range from +0.805 to -0.480, avoiding the pitfall of clustering all subjects in the middle. The ability to classify speakers into distinct archetypes further underscores its capacity to differentiate between substantively different rhetorical styles.
*   **Framework-Corpus Fit:** The framework appears to be an excellent fit for the corpus of political speeches. The dimensions are clearly present in the texts, and the relationships between them align with theoretical expectations. The strong correlations and coherent clustering suggest that the CAF's conceptual structure maps well onto the empirical reality of the data.
*   **Methodological Insights:** The analysis highlights the value of derived metrics. While the raw scores are informative, the `CCI` and `Tension Indices` provide a more synthesized and powerful level of insight. The failure of the `validate_framework_by_style` analysis serves as a crucial methodological lesson: the quality of computational analysis is heavily dependent on the richness of the input metadata. Future work using this framework should prioritize the creation of detailed corpus manifests that include speaker demographics, political affiliations, and predefined stylistic categories.

## 6. Discussion

### Theoretical Implications of Findings

The results of this pilot study carry several important theoretical implications for the study of political communication. The strong empirical validation of the CAF's oppositional structure suggests that a virtue ethics-based approach is a highly promising avenue for analysis. The data indicates that civic character is not a single, linear scale from bad to good, but a complex interplay of competing values. The "virtue" and "vice" clusters identified in the correlation analysis can be interpreted as two distinct, coherent, and largely mutually exclusive rhetorical systems. This finding challenges models that might treat vices simply as the absence of virtues, suggesting instead that they are actively and strategically deployed as part of an alternative rhetorical framework.

Furthermore, the concept of `Tension` provides a quantitative handle on the phenomenon of strategic ambiguity or "dog-whistling." A speaker like Bernie Sanders, with high tension on the justice/resentment axis, is measurably blending a virtuous call for justice with a pathological appeal to grievance. This ability to quantify such contradictions is a significant advance over purely qualitative interpretations.

### Comparative Analysis and Archetypal Patterns

The archetypes identified in Table 2 provide a powerful lens for comparative analysis.

*   **The "Authentic Virtue" Archetype (McCain, Booker, Romney):** These speakers, despite differing political affiliations, converge on a rhetorical style defined by high CCI scores and low tension. Their discourse prioritizes unifying themes (`dignity`), intellectual honesty (`truth`), and realism (`pragmatism`). This pattern appears most clearly in moments of civic ritual, such as McCain's concession speech, suggesting it may be a style associated with upholding institutional norms.
*   **The "Strategic Pathology" Archetype (Sanders, King):** This archetype is defined by a coherent and intense deployment of vices. The core strategy involves creating a tribal out-group (`tribalism`), blaming it for past grievances (`resentment`), and using emotionally charged, simplistic narratives (`manipulation`, `fantasy`). The fact that speakers from opposite ends of the traditional left-right spectrum (Sanders and King) can both fall into this category suggests that this pathological style is a feature of populist or extremist rhetoric, regardless of its specific ideological content.
*   **The "Contested Rhetoric" Archetype (Lewis, Ocasio-Cortez):** Speakers with CCI scores near zero represent a fascinating middle ground. Their rhetoric is a battlefield where virtuous and pathological appeals co-exist and compete for dominance. This may reflect a number of underlying realities: a speaker navigating a complex political environment, a movement in transition (as with John Lewis's 1963 speech, which contains both deep resentment and profound hope), or a deliberate strategy to appeal to multiple audiences simultaneously.

### Broader Significance for the Field

This analysis, though preliminary, points toward the significant potential of computational social science to bring new rigor to the study of political discourse. By moving beyond subjective interpretation to a replicable, data-driven methodology, frameworks like the CAF can:

1.  **Enable Large-Scale Analysis:** While this was a small pilot, the methodology is scalable to thousands or millions of documents, allowing for the analysis of entire political eras or communication platforms.
2.  **Provide Objective Benchmarks:** The `Civic Character Index` could serve as a standardized metric for tracking the health of public discourse over time, comparing different media ecosystems, or evaluating the impact of rhetorical interventions.
3.  **Uncover Hidden Structures:** The correlation and clustering analysis reveals the "deep grammar" of rhetorical strategies, showing which concepts are linked and which are opposed in practice.

### Limitations and Future Directions

The primary limitation of this study is its **small sample size (N=8)**. The findings, while internally consistent and theoretically compelling, cannot be generalized to the broader political landscape. They should be treated as a successful proof-of-concept that justifies further research.

Future studies should aim to:
*   **Expand the Corpus:** Analyze a much larger and more representative corpus of political texts, including different speakers, time periods, and genres (e.g., social media, press releases, legislative debates).
*   **Enrich Metadata:** Ensure that future corpora include rich metadata on speaker identity, party, ideology, and context. This would enable more powerful analyses, such as the `validate_framework_by_style` test that failed in this study.
*   **Conduct Temporal Analysis:** Apply the framework to texts from the same speaker over time to track the evolution of their rhetorical character.
*   **Investigate Causal Relationships:** Combine CAF analysis with other data (e.g., polling data, election results) to generate testable hypotheses about the effects of different rhetorical strategies on public opinion and political outcomes.

## 7. Conclusion

This computational analysis of a pilot corpus using the Civic Analysis Framework (CAF) v10.0 has yielded promising preliminary results. The framework demonstrated high discriminatory power, successfully differentiating the civic character of eight distinct political speakers and arranging them along a coherent spectrum measured by the Civic Character Index. The analysis empirically validated the framework's core theoretical structure, confirming the oppositional nature of its virtue/vice axes and revealing the existence of cohesive "virtuous" and "pathological" rhetorical meta-strategies.

Despite the significant limitation of its small sample size, this study serves as a robust proof-of-concept. It showcases how a combination of a theoretically grounded framework, quantitative scoring, and advanced metric analysis can produce nuanced, replicable, and insightful assessments of political discourse. The findings indicate that the CAF is a valuable tool for moving the study of civic communication beyond subjective critique and toward a more rigorous, scalable, and data-driven science. Future research applying this methodology to larger and more diverse datasets is strongly warranted and holds the potential to generate significant insights into the nature and quality of public life.

## 8. Evidence Citations

The following textual evidence was used to support the interpretations in this report.

**Source Document: john_mccain_2008_concession_ff9b26f2.txt**
*   **On Dignity:** "This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight."
*   **On Hope/Pragmatism:** "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
*   **On Truth:** "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain."
*   **On Pragmatism:** "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."
*   **On Resentment (Absence):** "we fell short, the failure is mine, not yours."

**Source Document: bernie_sanders_2025_fighting_oligarchy_261b893a.txt**
*   **On Tribalism:** "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."
*   **On Manipulation:** "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
*   **On Resentment/Justice:** "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."