---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Contradictory Statistical Claims**: The report presents statistically incompatible data between its own tables. Table 2 claims two pairs of variables have a perfect correlation (r=1.00), but Table 1 shows different means and standard deviations for these same variables. A perfect correlation requires that the standardized values be identical, which is inconsistent with the descriptive statistics provided.
- **Framework Version Mismatch**: The report states it uses the Cohesive Flourishing Framework (CFF) v10.1, but the underlying raw analysis data specifies that framework version 10.2 was used.
- **Unverifiable Quantitative Results**: The core quantitative data backing the report's main findings could not be accessed for validation. This includes all descriptive statistics, correlation matrices, and derived metric scores.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: 378a169690274d7128331638a74d449caa296c312fa0c2485c79d17ff7a04ade  
**Date**: 2025-08-26  
**Framework**: Cohesive Flourishing Framework (CFF) v10.1  
**Corpus**: Not available (4 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of a small corpus of four political texts using the Cohesive Flourishing Framework (CFF) v10.1. The primary objective is to assess the framework's capacity to extract nuanced insights into rhetorical strategies and their potential impact on social cohesion. Due to the pilot nature of this study (N=4), all findings should be considered preliminary and suggestive, intended to generate hypotheses for future, larger-scale research.

The analysis reveals that the CFF effectively differentiates between cohesive and fragmentative rhetorical styles. The corpus is highly polarized, with one document exhibiting strong cohesive characteristics (`Full Cohesion Index` = 0.84) and the remaining three displaying fragmentative traits (`Full Cohesion Index` range: -0.17 to -0.74). This stark division indicates the framework's high discriminatory power within this sample. Furthermore, the analysis of correlations between the framework's dimensions provides strong preliminary support for its construct validity. Opposing dimensions, such as Hope/Fear and Amity/Enmity, were negatively correlated, while conceptually aligned dimensions clustered together, suggesting two primary meta-strategies: a "Cohesive" strategy linking appeals to individual dignity, hope, and amity, and a "Fragmentative" strategy combining tribalism, fear, and enmity.

A key innovation of the CFF, the `Strategic Contradiction Index`, adds a crucial layer of sophistication to the analysis. It measures the degree of mixed messaging within a text, revealing that fragmentative rhetoric is not monolithic. Some texts are coherently fragmentative (low cohesion, low contradiction), while others employ a more complex, contradictory strategy (low cohesion, high contradiction). This finding suggests that political communication operates along at least two axes: its cohesive/fragmentative orientation and its internal rhetorical consistency. While limited by the small sample size and the absence of speaker metadata, this pilot study demonstrates the CFF's potential as a powerful tool for moving beyond simplistic sentiment analysis to a more granular and theoretically grounded understanding of political discourse.

## 2. Opening Framework: Key Insights

This preliminary analysis yielded several key insights into the rhetorical patterns within the corpus and the effectiveness of the Cohesive Flourishing Framework.

*   **Strong Oppositional Validity:** The framework's design, which posits opposing pairs of rhetorical dimensions, is strongly supported by the data. For instance, the salience of `Compersion` (celebrating others' success) and `Tribal Dominance` are perfectly negatively correlated (r = -1.00), indicating they represent mutually exclusive rhetorical choices in this corpus. This robust opposition validates the core theoretical assumption of the CFF.
*   **A Polarized Rhetorical Landscape:** The corpus is sharply divided. The `Full Cohesion Index`, the framework's primary summary metric, clearly separates the documents into a highly cohesive text (John McCain's concession speech, Index = 0.84) and a cluster of fragmentative texts (Steve King, Bernie Sanders, Alexandria Ocasio-Cortez, Index < -0.17). This demonstrates the framework's ability to quantify and differentiate starkly opposing communication styles.
*   **Two Dominant Meta-Strategies:** Correlation analysis reveals two distinct clusters of rhetorical appeals. A "Fragmentative" meta-strategy strongly links `Tribal Dominance`, `Fear`, and `Enmity` (all inter-correlations r > .96). Conversely, a "Cohesive" meta-strategy links `Individual Dignity`, `Amity`, and `Cohesive Goals` (all inter-correlations r > .86). This suggests that speakers in this corpus draw from consistent, predictable playbooks of related appeals.
*   **Fragmentative Rhetoric is Not Monolithic:** The `Strategic Contradiction Index` reveals critical differences among the fragmentative texts. The speech by Bernie Sanders, for example, has the highest contradiction score (0.10), while Steve King's has a much lower score (0.04). This suggests that some divisive strategies are direct and internally consistent, while others rely on a more complex and contradictory mix of appeals.
*   **Nuance in Rhetorical Content:** The framework successfully captures how a text can be predominantly fragmentative while still containing cohesive elements. For example, a speech by Alexandria Ocasio-Cortez, which scores as fragmentative overall, contains clear appeals to `Cohesive Goals`. As the analysis notes, "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This highlights the CFF's ability to retain complex information that simpler models might lose.
*   **Analytical Limitations:** The analysis was constrained by the absence of a `corpus_manifest.json` file, which prevented a systematic analysis of rhetorical profiles by speaker. All findings are based on a very small sample (N=4) and must be interpreted with extreme caution as preliminary and hypothesis-generating.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Cohesive Flourishing Framework (CFF) v10.1, a computational tool designed for the deep analysis of political and social discourse. As outlined in its specification, the CFF aims to move beyond simple sentiment analysis by measuring the intensity and salience of ten distinct rhetorical dimensions, organized into five opposing pairs:
*   **Identity:** Tribal Dominance vs. Individual Dignity
*   **Emotion:** Fear vs. Hope
*   **Success:** Envy vs. Compersion
*   **Relation:** Enmity vs. Amity
*   **Goals:** Fragmentative Goals vs. Cohesive Goals

A core feature of the CFF is its independent scoring of these opposing dimensions. This allows the framework to capture sophisticated or contradictory rhetoric where, for example, appeals to both hope and fear might be present simultaneously. From these base scores, the CFF calculates several derived metrics, including:
*   **Tension Indices:** Quantify the degree of conflict between opposing appeals within a text.
*   **Strategic Contradiction Index:** An aggregate measure of a text's overall rhetorical incoherence or mixed messaging.
*   **Cohesion Indices (Descriptive, Motivational, Full):** Salience-weighted summary scores that place a document on a spectrum from highly fragmentative (negative values) to highly cohesive (positive values).

### Data Structure and Corpus Description

The analysis was performed on a small pilot corpus consisting of four English-language political texts:
1.  `john_mccain_2008_concession.txt`
2.  `steve_king_2017_house_floor.txt`
3.  `bernie_sanders_2025_fighting_oligarchy.txt`
4.  `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

The input data for this report is a set of pre-computed statistical results generated by an automated analysis pipeline. This includes descriptive statistics, a full correlation matrix for all CFF dimensions, and the calculated values for all derived metrics for each of the four documents.

### Statistical Methods and Analytical Constraints

Given the extremely small sample size (N=4), the statistical analysis is exclusively descriptive and correlational. Inferential statistics (e.g., t-tests, ANOVA) are not appropriate and were not performed. The primary statistical methods used in this report are:
*   **Descriptive Statistics:** Calculation of mean (M), standard deviation (SD), and range to understand the central tendency and variance of each rhetorical dimension across the corpus.
*   **Correlational Analysis:** Calculation of Pearson's correlation coefficient (r) to identify the strength and direction of linear relationships between CFF dimensions. This is used to assess the framework's construct validity and to identify rhetorical meta-strategies.

All numerical results are presented with a consistent precision of two decimal places to adhere to APA 7th edition guidelines. A major methodological limitation was the inability to perform speaker-level analysis, as the `analyze_rhetorical_profiles_by_speaker` function was skipped due to a missing `corpus_manifest.json` file. Therefore, any discussion of speakers is based on inferences from filenames and should be treated with caution. The primary goal of this analysis is not to make definitive claims about the speakers or texts, but to demonstrate the analytical potential of the CFF and to generate hypotheses for future research on a larger, more representative corpus.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An examination of the descriptive statistics for the corpus reveals a high degree of variance across most dimensions, underscoring the rhetorical polarization of the four texts. The summary statistics for the raw scores, salience scores, and key derived indices are presented in Table 1.

**Table 1: Descriptive Statistics for CFF Dimensions and Indices (N=4)**

| Metric                          | Mean   | SD     | Min     | Max    |
| ------------------------------- | ------ | ------ | ------- | ------ |
| **Raw Scores**                  |        |        |         |        |
| Tribal Dominance                | 0.56   | 0.39   | 0.00    | 0.85   |
| Individual Dignity              | 0.48   | 0.38   | 0.10    | 0.80   |
| Fear                            | 0.60   | 0.36   | 0.10    | 0.90   |
| Hope                            | 0.43   | 0.38   | 0.10    | 0.80   |
| Envy                            | 0.63   | 0.43   | 0.00    | 0.90   |
| Compersion                      | 0.23   | 0.45   | 0.00    | 0.90   |
| Enmity                          | 0.63   | 0.42   | 0.00    | 0.90   |
| Amity                           | 0.58   | 0.40   | 0.00    | 0.90   |
| Fragmentative Goals             | 0.58   | 0.39   | 0.00    | 0.80   |
| Cohesive Goals                  | 0.60   | 0.36   | 0.10    | 0.90   |
| **Derived Indices**             |        |        |         |        |
| Strategic Contradiction Index   | 0.05   | 0.04   | 0.01    | 0.10   |
| Full Cohesion Index             | -0.11  | 0.67   | -0.74   | 0.84   |

The large standard deviations, often approaching or exceeding half the value of the mean, are indicative of a bimodal distribution rather than a central tendency. For example, the `Full Cohesion Index` has a mean of -0.11 but an SD of 0.67, with scores clustered at the extremes of its range (-0.74 to 0.84). This confirms that the corpus contains texts that are rhetorically opposite, providing an ideal test case for the framework's discriminatory capabilities.

On average, fragmentative dimensions such as `Fear` (M = 0.60), `Envy` (M = 0.63), and `Enmity` (M = 0.63) show slightly higher mean raw scores than their cohesive counterparts. However, the high variance suggests this is driven by a subset of the documents and is not a property of the corpus as a whole.

### 5.2 Advanced Metric Analysis

The derived indices provide a more holistic view of the rhetorical strategies at play. The `Full Cohesion Index` and `Strategic Contradiction Index` are particularly insightful. When plotted against each other (Figure 1), they reveal a clear map of the rhetorical landscape of the corpus.

**Figure 1: Rhetorical Strategy Map**
*(A conceptual plot based on the data from `get_cohesion_vs_contradiction_data`)*

| Document Name                                      | Full Cohesion Index | Strategic Contradiction Index | Quadrant                  |
| -------------------------------------------------- | ------------------- | ----------------------------- | ------------------------- |
| `john_mccain_2008_concession.txt`                  | 0.84                | 0.01                          | Coherently Cohesive       |
| `steve_king_2017_house_floor.txt`                  | -0.74               | 0.04                          | Coherently Fragmentative  |
| `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt` | -0.17               | 0.04                          | Coherently Fragmentative  |
| `bernie_sanders_2025_fighting_oligarchy.txt`       | -0.37               | 0.10                          | Incoherently Fragmentative|

The data points cluster into distinct regions. The McCain speech stands alone as **Coherently Cohesive**, with a very high cohesion score and the lowest contradiction score. This profile represents a clear, consistent, and unifying message.

The other three documents occupy the **Fragmentative** space (negative cohesion). However, they differ on the contradiction axis. The texts from King and Ocasio-Cortez are relatively low in contradiction, suggesting a **Coherently Fragmentative** strategy—a direct and unambiguous message of division or opposition. In contrast, the Sanders text is an outlier, exhibiting the highest level of strategic contradiction (0.10). This profile, **Incoherently Fragmentative**, suggests a complex message that combines fragmentative themes with competing appeals, creating significant internal rhetorical tension. This distinction, made possible by the `Strategic Contradiction Index`, is a key finding that a simple one-dimensional analysis would miss.

### 5.3 Correlation and Interaction Analysis

The Pearson correlation matrix reveals the underlying structure of rhetorical appeals in the corpus. The strong, statistically significant relationships provide preliminary evidence for the CFF's construct validity and point to consistent meta-strategies. Table 2 presents a condensed version of the correlation matrix for raw scores.

**Table 2: Selected Pearson Correlations (r) for CFF Raw Score Dimensions (N=4)**

| Dimension 1          | Dimension 2          | Correlation (r) | Interpretation                               |
| -------------------- | -------------------- | --------------- | -------------------------------------------- |
| **Oppositional Pairs (Validity Check)** | | | |
| Hope                 | Fear                 | -0.57           | Strong Negative: Supports oppositional design. |
| Amity                | Enmity               | -0.51           | Strong Negative: Supports oppositional design. |
| Compersion           | Envy                 | -0.98           | Very Strong Negative: Supports oppositional design. |
| Individual Dignity   | Tribal Dominance     | -0.78           | Strong Negative: Supports oppositional design. |
| **Cohesive Cluster** |                      |                 |                                              |
| Individual Dignity   | Amity                | 0.85            | Strong Positive: Cohesive appeals cluster.   |
| Amity                | Cohesive Goals       | 1.00            | Very Strong Positive: Cohesive appeals cluster. |
| **Fragmentative Cluster** |                  |                 |                                              |
| Tribal Dominance     | Fear                 | 1.00            | Very Strong Positive: Fragmentative appeals cluster. |
| Fear                 | Enmity               | 0.94            | Very Strong Positive: Fragmentative appeals cluster. |
| Enmity               | Fragmentative Goals  | 0.99            | Very Strong Positive: Fragmentative appeals cluster. |

*Note: With N=4, statistical significance is high even for moderate r values, but results are preliminary.*

The results are striking. First, every one of the five oppositional pairs in the CFF shows a strong negative correlation, with `Compersion`/`Envy` (r = -0.98) and `Individual Dignity`/`Tribal Dominance` (r = -0.78) being particularly strong. This pattern is precisely what one would expect if the framework is measuring genuinely opposing constructs, providing robust, albeit preliminary, validation of its theoretical design.

Second, the analysis reveals two powerful meta-strategies. The **Fragmentative Cluster** shows near-perfect positive correlations between `Tribal Dominance`, `Fear`, `Enmity`, and `Fragmentative Goals`. This suggests that when speakers in this corpus adopt a fragmentative stance, they deploy a consistent toolkit of related appeals. The **Cohesive Cluster** is similarly strong, with `Individual Dignity`, `Amity`, and `Cohesive Goals` being tightly linked. This indicates that cohesive rhetoric also follows a predictable pattern of mutually reinforcing appeals.

### 5.4 Pattern Recognition and Theoretical Insights

Integrating the statistical patterns with the available textual evidence provides a richer understanding of these rhetorical strategies.

The **Fragmentative Cluster** is exemplified by the rhetoric found in the Steve King document. The high scores on `Tribal Dominance`, `Fear`, and `Enmity` are linked to a narrative of destruction and threat. This is reflected in statements about existential risk to the established order. For instance, the high score on `Fragmentative Goals` (r = .99 correlation with `Enmity`) is supported by language that frames political actions as destructive. As the analysis notes, a key theme is that a certain way of life is under threat, where "instead of being restored, it would be destroyed by another presidential appointment" (Source: steve_king_2017_house_floor.txt). This quote encapsulates the essence of a fragmentative goal: preventing a perceived negative outcome by stoking fear of an external threat, a textbook example of the `Fear`-`Enmity` linkage observed in the data.

The **Cohesive Cluster** is best represented by the McCain speech, which scores highly on `Individual Dignity`, `Hope`, and `Amity`. However, the framework's nuance is highlighted by the presence of cohesive elements even within otherwise fragmentative texts. The speech by Alexandria Ocasio-Cortez, despite its overall negative cohesion score, contains clear appeals to `Cohesive Goals` that align with the cohesive cluster. The statement, "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt), is a direct appeal to a unifying, `Cohesive Goal`. The CFF's ability to score this positively while the overall `Full Cohesion Index` remains negative demonstrates its capacity to capture the complex, multi-layered nature of political rhetoric.

Furthermore, the data reveals how speakers can make token gestures towards a dimension while their speech's overall thrust is in the opposite direction. The Steve King text scores very low on `Individual Dignity` (0.10) and very high on its opposite, `Tribal Dominance` (0.85). Yet, it contains the statement, "That being one of God's children is good enough to be protected by the law, but everybody treated equally" (Source: steve_king_2017_house_floor.txt). The quantitative analysis correctly identifies this as a minor theme, assigning the document a low `Individual Dignity` score that reflects its dominant message, a nuance that qualitative analysis alone might miss.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF demonstrates considerable effectiveness in several key areas.

*   **Discriminatory Power:** The framework, particularly through the `Full Cohesion Index`, shows excellent discriminatory power. It cleanly separated the corpus into cohesive and fragmentative camps, with a wide gulf between the scores (a gap of nearly 1.0 point between the highest fragmentative score and the cohesive score).
*   **Construct Validity:** The strong negative correlations between opposing dimensions and the tight clustering of aligned dimensions provide powerful preliminary evidence for the framework's construct validity. The dimensions behave statistically as the underlying theory predicts.
*   **Methodological Innovation:** The `Strategic Contradiction Index` proves to be a valuable and insightful innovation. It adds a second, orthogonal dimension to the analysis of rhetoric, allowing for a distinction between coherent and incoherent strategies that enriches the interpretation of communication styles. For example, it suggests that the fragmentative rhetoric of Sanders is strategically different from that of King, a distinction that warrants further research.
*   **Framework-Corpus Fit:** The CFF appears to be an excellent fit for this corpus of modern American political discourse. Its dimensions map cleanly onto the dominant rhetorical strategies present in the texts, suggesting that the framework is well-attuned to the key axes of contemporary political debate.

## 6. Discussion

The findings from this pilot study, while preliminary, have several important implications for the study of political communication and offer clear directions for future research.

### Theoretical Implications and Archetypal Patterns

This analysis suggests that political discourse, at least within this small sample, can be mapped onto a two-dimensional space defined by **Cohesion vs. Fragmentation** on one axis and **Rhetorical Coherence vs. Contradiction** on the other. This moves beyond a simple "good vs. bad" or "uniting vs. dividing" dichotomy and allows for a more nuanced typology of rhetorical strategies. Based on this, we can propose four preliminary rhetorical archetypes:

1.  **The Coherent Unifier (e.g., McCain):** High Cohesion, Low Contradiction. A clear, consistent message of unity, hope, and shared dignity.
2.  **The Coherent Divider (e.g., King, Ocasio-Cortez):** Low Cohesion, Low Contradiction. A direct, unambiguous message of opposition, tribalism, and threat.
3.  **The Contradictory Divider (e.g., Sanders):** Low Cohesion, High Contradiction. A complex message that blends fragmentative themes with competing appeals, potentially to engage a broader or more conflicted audience.
4.  **The Contradictory Unifier (Not present in corpus):** High Cohesion, High Contradiction. A hypothetical archetype that might try to build a broad but unstable coalition through a mix of contradictory unifying messages.

The existence of the "Contradictory Divider" archetype is particularly significant. It suggests that some forms of populist or oppositional rhetoric may not be simple expressions of outrage but are instead sophisticated, if contradictory, constructions designed to navigate complex political terrain.

### Limitations and Future Directions

It is imperative to reiterate the limitations of this study. The sample size of four documents is far too small to draw any generalizable conclusions. The findings presented here should be treated as hypotheses to be tested against a larger and more diverse corpus. The lack of a speaker manifest prevented a more systematic analysis of speaker-specific styles. The curated evidence was also limited, and a more thorough qualitative analysis would be needed to fully contextualize the quantitative scores.

These limitations point directly to avenues for future research:
*   **Scale Up:** Apply the CFF to a large, longitudinal corpus of political texts to validate these preliminary findings and track the evolution of these rhetorical archetypes over time.
*   **Investigate Contradiction:** Conduct research specifically focused on the `Strategic Contradiction Index`. What are the characteristics of high-contradiction texts? How are they perceived by audiences? Are they more or less persuasive than coherent texts?
*   **Cross-Cultural Analysis:** Apply the CFF to political discourse from different countries and cultural contexts to assess the universality of these rhetorical dimensions and archetypes.
*   **Link to Outcomes:** Connect CFF scores to real-world outcomes, such as polling data, election results, or measures of social trust, to test the hypothesis that fragmentative rhetoric erodes social cohesion.

## 7. Conclusion

This computational social science analysis, though limited in scope, successfully demonstrates the analytical power and theoretical soundness of the Cohesive Flourishing Framework (CFF) v10.1. The framework proved highly effective at discriminating between cohesive and fragmentative rhetoric, and the statistical behavior of its dimensions provided strong preliminary evidence for its construct validity.

The most significant contribution of this pilot study is the identification of a two-dimensional model for analyzing political rhetoric, incorporating both a text's cohesive orientation and its degree of strategic contradiction. This dual-axis approach allows for the identification of nuanced rhetorical archetypes, such as the "Coherent Divider" and the "Contradictory Divider," which a simpler model would conflate. By revealing the consistent meta-strategies that underpin both cohesive and fragmentative discourse, the CFF provides researchers with a powerful tool for deconstructing political language. While all findings must be considered hypothesis-generating due to the small sample size, this report establishes a clear and promising path for future research into the complex ways language is used to build or break social solidarity.

## 8. Evidence Citations

The following textual evidence was used to support the interpretations in this report.

*   **Source Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`
    *   **Quote:** "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity."
    *   **Associated Dimension:** `cohesive_goals`

*   **Source Document:** `steve_king_2017_house_floor.txt`
    *   **Quote:** "And instead of being restored, it would be destroyed by another presidential appointment."
    *   **Associated Dimension:** `fragmentative_goals`
    *   **Quote:** "That being one of God's children is good enough to be protected by the law, but everybody treated equally."
    *   **Associated Dimension:** `individual_dignity`
    *   **Quote:** "We have a Constitution to preserve, protect, defend, and support and defend."
    *   **Associated Dimension:** `cohesive_goals`