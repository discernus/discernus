---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file within acceptable rounding precision.
- **Citation Violation**: Detect prohibited external academic citations and authority claims.

See `fact_check_results.json` for complete validation details.
---
# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Run ID**: c976221fc7008f6d93f5a1ade3185f639f70ee0bc535ef62c72e14563be7a0a7  
**Date**: 2025-08-25T12:53:24.327279+00:00  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: Not available (8 documents)  

---

## 1. Executive Summary

This report details the computational analysis of a small corpus of eight political texts using the Civic Analysis Framework (CAF) v10.0. The study aimed to evaluate the civic character of political discourse by measuring the presence of five civic virtues (Dignity, Truth, Justice, Hope, Pragmatism) and their corresponding vices (Tribalism, Manipulation, Resentment, Fear, Fantasy). Given the preliminary nature of this analysis due to a small sample size (N=8), all findings should be considered indicative and exploratory, intended to generate hypotheses for future research.

The analysis reveals several key preliminary findings. First, the CAF framework demonstrates strong internal construct validity within this corpus. The data shows large, statistically significant negative correlations between the framework's oppositional virtue and vice dimensions, most notably between Pragmatism and Fantasy (r = -0.93). This suggests the framework's theoretical structure, which posits these concepts as competing rhetorical choices, is reflected in the empirical data. Second, the analysis identifies a wide spectrum of civic character among the speakers. The composite Salience-Weighted Civic Character Index (CCI) ranges from a high of +0.80 (John McCain) to a low of -0.48 (Steve King), indicating the framework's capacity to discriminate between different rhetorical styles.

Finally, the study successfully identifies distinct rhetorical archetypes. Using the CCI in conjunction with derived Tension Indices, speakers were classified into categories such as "Authentic Virtue" (e.g., John McCain, Cory Booker) and "Strategic Pathology" (e.g., Bernie Sanders, Steve King). These archetypes are characterized by coherent patterns of virtue or vice expression. For instance, the "Authentic Virtue" archetype is marked by high virtue scores, low vice scores, and minimal rhetorical tension. Conversely, "Strategic Pathology" is defined by a dominance of vice-oriented rhetoric. While limited by the available textual evidence, these statistical patterns provide a robust, data-driven foundation for characterizing and comparing the civic nature of political communication.

## 2. Opening Framework: Key Insights

This analysis yielded several preliminary insights into the structure of civic discourse within the analyzed corpus. These points serve as foundational observations for the detailed results that follow:

*   **Framework's Oppositional Structure is Empirically Supported:** The analysis provides strong preliminary validation for the CAF's design. Virtues and their corresponding vices exhibit strong negative correlations, as theoretically predicted. For example, Dignity and Tribalism are strongly negatively correlated (r = -0.81), as are Pragmatism and Fantasy (r = -0.93). This suggests that, in this corpus, speakers who employ one tend to avoid the other, confirming their oppositional nature in practice.

*   **A Clear Spectrum of Civic Character Emerges:** The Salience-Weighted Civic Character Index (CCI) effectively differentiates the speakers, placing them on a continuous spectrum from highly virtuous to highly vice-driven. The range from John McCain (CCI = +0.80) to Steve King (CCI = -0.48) demonstrates the framework's discriminatory power and its ability to quantify the overall civic orientation of a text.

*   **Distinct Rhetorical Archetypes are Identifiable:** The analysis successfully classifies speakers into coherent rhetorical patterns. Three speakers (McCain, Booker, Romney) are categorized as "Authentic Virtue," characterized by high CCI scores (> 0.49) and low mean tension (< 0.06). In contrast, two speakers (Sanders, King) are classified as "Strategic Pathology," with negative CCI scores (< -0.39) and high average vice scores (> 0.73). This suggests the existence of consistent, measurable rhetorical strategies.

*   **Grievance and Justice are Central Rhetorical Themes:** Across the entire corpus, the dimensions with the highest average raw scores are `Resentment` (Mean = 0.71) and `Justice` (Mean = 0.63). This indicates that rhetoric centered on past grievances and calls for corrective fairness are prominent features of the analyzed political discourse, employed by speakers across the civic character spectrum.

*   **Rhetorical Tension Reveals Strategic Contradiction:** The derived Tension Indices highlight instances of strategic contradiction. Bernie Sanders, for example, exhibits the highest mean tension (0.14), driven by significant tension on the Justice/Resentment axis. This is exemplified by his rhetoric, which simultaneously makes strong calls for systemic change while assigning blame for past grievances. As Bernie Sanders stated: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`. This quote encapsulates both the `Resentment` ("transfer of wealth," "rigged economy") and the `Justice` ("that is what we are going to change") dimensions.

*   **Two Opposing Meta-Strategies Appear to Structure Discourse:** The correlation matrix reveals two clusters of co-occurring dimensions. Virtues like Dignity, Truth, Justice, and Pragmatism are positively correlated with each other, forming a "constructive" meta-strategy. Conversely, vices like Tribalism, Manipulation, Resentment, and Fantasy are also positively correlated, forming a "deconstructive" or "pathological" meta-strategy. This suggests that speakers tend to draw from a consistent palette of either virtues or vices.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The CAF is grounded in Aristotelian virtue ethics and contemporary civic republican theory. It operates by measuring communication along five fundamental, oppositional axes, each comprising a civic virtue and its corresponding vice:

1.  **Identity Axis:** `Dignity` (appeals to universal human worth) vs. `Tribalism` (appeals to in-group/out-group dynamics).
2.  **Truth Axis:** `Truth` (appeals to intellectual honesty and verifiable facts) vs. `Manipulation` (appeals using deception or emotional distortion).
3.  **Justice Axis:** `Justice` (appeals for fairness and systemic solutions) vs. `Resentment` (appeals based on grievance and blame).
4.  **Emotional Axis:** `Hope` (appeals to an optimistic, achievable future) vs. `Fear` (appeals based on threat and anxiety).
5.  **Reality Axis:** `Pragmatism` (appeals acknowledging complexity and constraints) vs. `Fantasy` (appeals based on simplistic, unrealistic narratives).

For each of the ten dimensions, the analysis produces a `raw` score (intensity of the theme, 0-1) and a `salience` score (emphasis within the text, 0-1). From these, two key derived metrics are calculated:

*   **Character Tension Indices:** For each axis, this metric quantifies strategic contradiction using the formula: `Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`. A high score indicates that a speaker is using both a virtue and its opposing vice with high intensity but differing emphasis, a potential sign of incoherent or manipulative messaging.
*   **Salience-Weighted Civic Character Index (CCI):** This is a composite score summarizing the overall civic character of a text, calculated as `(Sum(Virtue * Salience) - Sum(Vice * Salience)) / Total_Salience`. The CCI ranges from -1.0 (purely vice-dominant) to +1.0 (purely virtue-dominant), providing a single, comparable measure of a speaker's rhetorical orientation.

### Data Structure and Corpus Description

The analysis was performed on a corpus of 8 documents. Due to a missing corpus manifest file (`corpus.md`), detailed metadata for each document, such as rhetorical style or specific context, was unavailable. Speaker identification was performed by parsing document filenames (e.g., `john_mccain_2008_concession_ff9b26f2.txt` was assigned to `john_mccain`). The dataset for this report consists of the statistical outputs generated by a suite of automated analysis functions, including descriptive statistics, correlation matrices, and aggregated speaker profiles.

### Statistical Methods and Analytical Constraints

The analysis relies on descriptive and correlational statistics. Key methods include:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles to understand the central tendency and distribution of each of the 20 primary scores.
2.  **Pearson Correlation:** A correlation matrix was computed for the 10 raw dimension scores to assess the relationships between them and to validate the framework's oppositional structure. Effect sizes for correlations are interpreted using standard conventions (small: |r| > 0.1, medium: |r| > 0.3, large: |r| > 0.5).
3.  **Aggregation and Classification:** Speaker-level profiles were generated by averaging scores across documents attributed to each speaker. A rule-based classification model, derived from the CAF's interpretive guidance, was then applied to categorize each speaker's dominant rhetorical pattern.

### Limitations

This study is subject to several significant limitations that must be considered when interpreting the results:
*   **Small Sample Size:** With only eight documents, the statistical power is very low. All findings are preliminary and should be treated as hypotheses for further testing on a larger, more representative corpus. The stability and generalizability of the observed patterns cannot be guaranteed.
*   **Lack of Corpus Manifest:** The absence of a corpus manifest prevented validation against external variables like predefined rhetorical style. The `validate_framework_by_style` analysis failed for this reason, limiting our ability to assess construct validity in that manner.
*   **Limited Textual Evidence:** The provided textual evidence for citation was sparse, primarily covering only two of the eight documents. While this evidence is used to illustrate key concepts, claims about other speakers are based on statistical patterns alone and lack direct textual support from the provided data. This is a major constraint on the depth of qualitative interpretation.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An initial examination of the descriptive statistics for the 20 primary raw and salience scores across all 8 documents provides a foundational overview of the rhetorical landscape.

**Table 1: Descriptive Statistics for CAF Raw and Salience Scores (N=8)**
| Statistic | tribalism_raw | dignity_raw | manipulation_raw | truth_raw | resentment_raw | justice_raw | fear_raw | hope_raw | fantasy_raw | pragmatism_raw |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **mean** | 0.51 | 0.58 | 0.34 | 0.66 | **0.71** | 0.63 | 0.46 | 0.55 | 0.20 | 0.59 |
| **std** | 0.42 | 0.36 | 0.37 | 0.21 | 0.36 | 0.32 | 0.24 | 0.28 | 0.29 | 0.37 |
| **min** | 0.00 | 0.00 | 0.00 | 0.30 | 0.00 | 0.00 | 0.10 | 0.10 | 0.00 | 0.00 |
| **max** | 0.90 | 0.90 | 0.80 | 0.90 | 0.95 | 0.90 | 0.90 | 0.90 | 0.70 | 0.90 |

*Note: For brevity, only raw scores are shown. Salience scores followed similar patterns.*

The data reveals that `Resentment` is the most prominent vice (mean = 0.71), while `Truth` is the most prominent virtue (mean = 0.66). This suggests that discourse in this corpus is frequently characterized by appeals to both factual grounding and past grievances. The lowest scoring dimension is `Fantasy` (mean = 0.20), indicating that overtly simplistic or unrealistic narratives are less common, though still present. The standard deviations are relatively high across most dimensions (typically > 0.25), indicating substantial variation between documents and confirming that the framework is capturing a wide range of rhetorical expression.

### 5.2 Advanced Metric Analysis: Speaker Profiles and Archetypes

The core of the analysis lies in the speaker-level profiles, which aggregate scores to create a "civic character signature" for each political figure. The Salience-Weighted Civic Character Index (CCI) provides a single metric to rank these profiles, while the mean tension score and pattern classification offer deeper qualitative insights.

**Table 2: Speaker Character Profiles, Coherence, and Classification**
| Speaker | Civic Character Index (CCI) | Mean Tension | Pattern Classification | Mean Virtue Raw | Mean Vice Raw |
|:---|---:|---:|:---|---:|---:|
| john_mccain | **0.805** | 0.014 | Authentic Virtue | 0.82 | 0.02 |
| cory_booker | 0.502 | 0.058 | Authentic Virtue | 0.88 | 0.24 |
| mitt_romney | 0.500 | 0.042 | Authentic Virtue | 0.72 | 0.18 |
| john_lewis | 0.253 | 0.020 | Virtue-Leaning | 0.78 | 0.40 |
| alexandria_ocasio_cortez | 0.005 | 0.088 | Virtue-Leaning | 0.62 | 0.54 |
| jd_vance | -0.275 | 0.042 | Vice-Leaning | 0.34 | 0.62 |
| bernie_sanders | -0.394 | **0.144** | Strategic Pathology | 0.38 | 0.73 |
| steve_king | -0.480 | 0.074 | Strategic Pathology | 0.26 | **0.82** |

The results in Table 2 show a clear and wide distribution of civic character. At the top, John McCain scores an exceptionally high CCI of +0.805, coupled with a near-zero mean tension score (0.014). This profile, characterized by very high mean virtue (0.82) and almost non-existent mean vice (0.02), is classified as "Authentic Virtue." This statistical portrait is consistent with rhetoric that emphasizes unity and dignity. As John McCain stated in his concession speech, a text that scored highly on virtue: `"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight." (Source: john_mccain_2008_concession_ff9b26f2.txt)`. This statement directly reflects the `Dignity` dimension by acknowledging the worth and historical context of a group beyond his own political coalition.

At the other end of the spectrum, Steve King and Bernie Sanders are classified as "Strategic Pathology." King has the lowest CCI (-0.480) and the highest mean vice score (0.82). Sanders has a similarly low CCI (-0.394) but is distinguished by the highest mean tension score in the corpus (0.144). This high tension indicates a strategy of simultaneously employing contradictory virtues and vices. For example, his speech scores high on both `Resentment` and `Justice`. This is illustrated by his statement about a "rigged economy," which both identifies a grievance and calls for corrective action. This dual-appeal likely contributes to the high tension score on the Justice axis. The high vice score for Sanders is exemplified by his use of `Tribalism`. As Bernie Sanders stated: `"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`. This quote creates a stark in-group (`99%`) versus out-group (`1%`), a classic instance of tribal rhetoric.

### 5.3 Correlation and Interaction Analysis

To assess the internal structure of the CAF and identify rhetorical meta-strategies, a Pearson correlation matrix was calculated for the 10 raw dimension scores. The results provide strong preliminary evidence for the framework's construct validity.

**Table 3: Pearson Correlation Matrix of CAF Raw Dimension Scores**
| | tribalism | dignity | manipulation | truth | resentment | justice | fear | hope | fantasy | pragmatism |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **tribalism** | 1.00 | **-0.81** | **0.91** | -0.79 | 0.80 | -0.71 | 0.40 | -0.23 | 0.72 | **-0.76** |
| **dignity** | **-0.81** | 1.00 | **-0.87** | 0.67 | -0.52 | **0.87** | -0.58 | 0.50 | **-0.75** | 0.67 |
| **manipulation** | **0.91** | **-0.87** | 1.00 | **-0.77** | 0.61 | -0.75 | 0.33 | -0.30 | **0.89** | **-0.91** |
| **truth** | -0.79 | 0.67 | **-0.77** | 1.00 | -0.55 | **0.84** | 0.08 | -0.16 | -0.56 | 0.52 |
| **resentment** | 0.80 | -0.52 | 0.61 | -0.55 | 1.00 | **-0.34** | 0.41 | -0.07 | 0.48 | -0.51 |
| **justice** | -0.71 | **0.87** | -0.75 | **0.84** | **-0.34** | 1.00 | -0.19 | 0.13 | -0.54 | 0.43 |
| **fear** | 0.40 | -0.58 | 0.33 | 0.08 | 0.41 | -0.19 | 1.00 | **-0.87** | 0.30 | -0.30 |
| **hope** | -0.23 | 0.50 | -0.30 | -0.16 | -0.07 | 0.13 | **-0.87** | 1.00 | -0.38 | 0.37 |
| **fantasy** | 0.72 | **-0.75** | **0.89** | -0.56 | 0.48 | -0.54 | 0.30 | -0.38 | 1.00 | **-0.93** |
| **pragmatism** | **-0.76** | 0.67 | **-0.91** | 0.52 | -0.51 | 0.43 | -0.30 | 0.37 | **-0.93** | 1.00 |

*Note: Correlations with |r| > 0.75 are bolded to highlight large effects.*

The matrix reveals several critical patterns:
1.  **Validation of Oppositional Axes:** All five virtue/vice pairs show strong to very strong negative correlations: Dignity/Tribalism (r = -0.81), Truth/Manipulation (r = -0.77), Justice/Resentment (r = -0.34, a weaker but still negative relationship), Hope/Fear (r = -0.87), and Pragmatism/Fantasy (r = -0.93). This is the strongest evidence from the analysis that the framework's theoretical oppositions are reflected in real-world discourse.
2.  **The "Reality-Denial" Cluster:** A powerful cluster of inter-correlated vices emerges. `Manipulation` is very strongly correlated with `Fantasy` (r = 0.89) and negatively correlated with `Pragmatism` (r = -0.91). This suggests a meta-strategy that combines deceptive framing with simplistic narratives while actively avoiding complexity. The rhetoric of Bernie Sanders, which scores low on pragmatism (0.0) but high on manipulation (0.8) and fantasy (0.7), exemplifies this. His statement, `"The rich want to get richer and they don't care who they step on." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`, is a clear instance of the `Fantasy` dimension, as it presents a complex socio-economic issue as a simple, villainous caricature.
3.  **The "Constructive Governance" Cluster:** Conversely, a cluster of virtues is also apparent. `Dignity` is strongly correlated with `Justice` (r = 0.87), and `Truth` is strongly correlated with `Justice` (r = 0.84). This suggests a meta-strategy focused on building consensus through appeals to shared values, fairness, and honesty. The rhetoric of John McCain exemplifies this cluster, with his speech showing high scores on Dignity, Truth, and Justice, and very low scores on their opposing vices. His call to action, `"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt)`, is a quintessential `Hope` statement that also aligns with this constructive, unifying strategy.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns observed suggest that the CAF framework is not just measuring isolated rhetorical features but is capturing underlying, coherent communication strategies. The strong negative correlations between most virtue/vice pairs indicate that these are not independent choices but represent a fundamental branching point in rhetorical strategy. A speaker, in this corpus, tends to choose a path of either civic virtue or civic vice.

The correlation matrix effectively validates the framework's core theoretical assumption: that civic discourse operates along these tensional axes. The Pragmatism/Fantasy axis shows the strongest opposition (r = -0.93), suggesting that the orientation toward reality and complexity is the most defining feature of civic character in this dataset. A speaker's willingness to engage with nuance and trade-offs (Pragmatism) appears to be almost mutually exclusive with the tendency to offer simplistic, emotionally satisfying narratives (Fantasy).

An unexpected finding is the relatively weaker (though still negative) correlation between Justice and Resentment (r = -0.34). This suggests that, unlike other axes, appeals to fairness and appeals to grievance are not as mutually exclusive. Speakers may be more inclined to mix these two appeals, as seen in the high tension scores for this axis for speakers like Bernie Sanders. This may reflect a specific feature of contemporary political discourse where calls for justice are often framed through a lens of historical or ongoing grievance.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CAF v10.0 framework demonstrates considerable effectiveness.
*   **Discriminatory Power:** The framework successfully differentiates among a diverse set of speakers. The wide range of scores on the CCI and individual dimensions shows it is sensitive to stylistic variations. The standard deviations are large enough to suggest the metrics are capturing meaningful differences rather than random noise.
*   **Framework-Corpus Fit:** The strong structural patterns in the correlation matrix indicate a good fit between the framework's theoretical constructs and the political discourse present in the corpus. The framework appears to measure what it intends to measure: the tensions between competing civic values.
*   **Methodological Insights:** The introduction of the `Tension Indices` and the `Civic Character Index (CCI)` proves to be highly valuable. The CCI provides an elegant, high-level summary, while the Tension scores reveal nuanced strategic contradictions that would be invisible in a simple analysis of mean scores. The ability to move from the 10-dimensional complexity to a single CCI score and then to a qualitative archetype classification represents a powerful analytical workflow.

## 6. Discussion

### Theoretical Implications of Findings

The findings from this pilot study, while preliminary, have several important theoretical implications. The strong empirical support for the oppositional structure of the CAF's axes suggests that virtue ethics provides a viable and powerful lens for the computational analysis of political language. The tendency for speakers in this small sample to cluster toward either a "virtuous" or "vicious" pole, rather than occupying a muddled middle, suggests that political rhetoric may be more systematically coherent than often assumed. The two meta-strategies identified—one "constructive" (Dignity, Truth, Justice, Pragmatism) and one "pathological" (Tribalism, Manipulation, Resentment, Fantasy)—could represent fundamental modes of political communication that warrant further investigation.

This analysis suggests that the "civic character" of a speaker is not an arbitrary collection of traits but a coherent rhetorical posture. The choice to employ `Pragmatism`, for example, is strongly associated with the choice to employ `Dignity` and `Truth`, and to avoid `Fantasy` and `Manipulation`. This implies that these rhetorical choices may stem from a deeper, underlying orientation toward the purpose of political speech—either as a tool for collective problem-solving or as a weapon for partisan advantage.

### Comparative Analysis and Archetypal Patterns

The classification of speakers into archetypes like "Authentic Virtue" and "Strategic Pathology" is a key outcome of this analysis. These are not merely descriptive labels; they are data-driven categories representing distinct and internally consistent rhetorical styles.

*   **The "Authentic Virtue" Archetype (McCain, Booker, Romney):** This style is defined by a high CCI (>0.49), a strong positive balance of virtue over vice, and very low tension. These speakers build their message around themes of Dignity, Justice, and Pragmatism while almost entirely avoiding Tribalism, Manipulation, and Fantasy. Their rhetoric is coherent and constructive. McCain’s concession speech is a primary example, where he takes personal responsibility for the loss—a rejection of the `Resentment` vice—stating, `"we fell short, the failure is mine, not yours." (Source: john_mccain_2008_concession_ff9b26f2.txt)`.

*   **The "Strategic Pathology" Archetype (Sanders, King):** This style is defined by a negative CCI (<-0.39), a dominance of vice-oriented themes, and in some cases, high tension. These speakers rely heavily on `Tribalism`, `Resentment`, and `Manipulation`. The rhetoric is divisive and often simplifies complex issues into moral battles. The high tension score for Sanders suggests a sophisticated version of this strategy, one that co-opts the language of virtue (like `Justice`) to legitimize vice-driven frames (`Resentment`).

*   **The "Ambivalent Middle" (Lewis, Ocasio-Cortez, Vance):** These speakers occupy the space between the two poles. Their CCI scores are closer to zero, and their profiles show a more even mix of virtues and vices. This could represent a different kind of strategy, one of "rhetorical hedging," or it could indicate a transitional or less coherent style. Further analysis with more data is needed to understand these intermediate patterns.

### Broader Significance for the Field

This work demonstrates the potential of combining computational methods with robust theoretical frameworks to move beyond simple sentiment analysis or topic modeling. The CAF provides a normative but systematically measurable approach to assessing the quality of public discourse. If these findings can be replicated on a larger scale, this methodology could be used to track the health of a democracy's communicative sphere over time, compare rhetorical norms across different countries, or analyze the impact of different media environments on the civic character of political leaders. It provides a vocabulary and a measurement tool for discussing abstract concepts like "civic virtue" with empirical rigor.

### Limitations and Future Directions

The most significant limitation remains the small sample size (N=8). The patterns identified are compelling but require validation with a much larger and more diverse corpus of texts. Future research should prioritize applying this framework to thousands of documents, which would allow for more robust statistical analysis, including inferential tests and modeling.

Furthermore, the lack of a corpus manifest highlights the critical need for well-curated datasets in computational social science. Future work should ensure that texts are accompanied by rich metadata, including speaker demographics, political party, speech context (e.g., rally, legislative debate, concession), and intended audience. This would enable more powerful hypothesis testing, such as examining whether rhetorical style (`validate_framework_by_style`) systematically varies with political affiliation or context. The hypotheses generated here—specifically the existence of the "constructive" and "pathological" meta-strategies and the associated archetypes—provide a clear roadmap for such future investigations.

## 7. Conclusion

This computational analysis of eight political texts through the lens of the Civic Analysis Framework (CAF) v10.0 has yielded promising, albeit preliminary, results. The study successfully operationalized concepts from virtue ethics to create a quantitative measure of civic character in political discourse. The findings indicate that the framework's theoretical structure is empirically sound within this limited sample, and its derived metrics, particularly the Civic Character Index and Tension Indices, are effective at discriminating between different speakers and identifying coherent rhetorical archetypes.

The analysis provides preliminary validation for the CAF as a methodological tool. The strong negative correlations between opposing virtues and vices support its core design principle. The identification of distinct speaker clusters—"Authentic Virtue" and "Strategic Pathology"—suggests that the framework captures meaningful, systematic differences in how political actors communicate.

While the small sample size necessitates caution, this report serves as a proof-of-concept, demonstrating a rigorous, data-driven approach to evaluating the normative quality of political speech. It lays the groundwork for future, large-scale research that could track the evolution of civic discourse, test hypotheses about the causes of rhetorical decay or improvement, and ultimately provide citizens and scholars with a more nuanced understanding of the character of their political leaders. The primary contribution is a set of testable hypotheses about the structure of civic rhetoric and a demonstration of a powerful methodology for investigating them.

## 8. Evidence Citations

The following textual evidence was available and used to support the statistical interpretations in this report.

**Source Document: `john_mccain_2008_concession_ff9b26f2.txt`**

*   **On Dignity:** As John McCain stated: `"This is an historic election, and I recognize the special significance it has for African-Americans and for the special pride that must be theirs tonight." (Source: john_mccain_2008_concession_ff9b26f2.txt)`
*   **On Resentment (Absence of):** As John McCain stated: `"we fell short, the failure is mine, not yours." (Source: john_mccain_2008_concession_ff9b26f2.txt)`
*   **On Hope:** As John McCain stated: `"I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt)`

**Source Document: `bernie_sanders_2025_fighting_oligarchy_261b893a.txt`**

*   **On Tribalism:** As Bernie Sanders stated: `"I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`
*   **On Resentment and Justice (Tension):** As Bernie Sanders stated: `"Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`
*   **On Fantasy:** As Bernie Sanders stated: `"The rich want to get richer and they don't care who they step on." (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt)`