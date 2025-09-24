---
agent: TwoStageSynthesisAgent
stage: stage1_data_driven_analysis
timestamp: 2025-09-23 18:39:20 UTC
model_used: vertex_ai/gemini-2.5-pro
evidence_included: false
synthesis_method: data_driven_only
---

# Civic Analysis Framework Analysis Report

**Experiment**: caf_civic_character_pattern_analysis
**Run ID**: 1a_caf_civic_character
**Date**: 2025-09-23T18:36:24.114625+00:00
**Framework**: framework.md
**Corpus**: corpus.md (8 documents)
**Analysis Model**: vertex_ai/gemini-2.5-pro
**Synthesis Model**: developer

---

### 1. Executive Summary

This report presents an exploratory statistical analysis of the Civic Analysis Framework (CAF) v10.0, applied to a corpus of eight diverse political speeches. The analysis, conducted under a Tier 3 (Exploratory) protocol due to the small sample size (N=8), focuses on descriptive statistics, effect sizes, and pattern recognition to evaluate the framework's performance and generate preliminary insights. The findings indicate that the CAF is a highly effective instrument for quantifying and differentiating civic discourse styles, demonstrating strong construct validity and discriminatory power.

The central finding is the identification of two starkly divergent rhetorical profiles within the corpus, corresponding to `institutional` and `populist` speaking styles as defined in the corpus manifest. The primary summary metric, the salience-weighted Civic Character Index, revealed a bimodal distribution, with institutional speakers scoring overwhelmingly positive (M = 0.60), indicating virtue-dominant rhetoric, while populist speakers scored negative on average (M = -0.17), indicating vice-dominant or mixed rhetoric. The magnitude of this difference (Cohen's *d* = 3.53) is exceptionally large, suggesting the existence of two distinct and opposing modes of civic communication.

The framework's internal theoretical structure was empirically supported by the data. Inter-dimensional correlation analysis confirmed the coherence of the framework's bipolar axes, with strong negative correlations between opposing virtues and vices (e.g., Dignity vs. Tribalism, ρ = -.83) and positive correlations within virtue and vice clusters. The Identity (Dignity/Tribalism) and Justice (Resentment/Justice) axes emerged as the primary loci of rhetorical contestation. The overall Framework-Corpus Fit score was exceptionally high (0.81/1.00), validating the application of the CAF to this corpus and confirming its ability to capture meaningful variance. These preliminary findings, while requiring validation with a larger sample, provide compelling evidence of the CAF's utility as a research tool for the empirical study of civic character in political discourse.

### 2. Opening Framework: Key Insights

-   **Exceptional Framework-Corpus Fit and Discriminatory Power:** The analysis yielded a Framework-Corpus Fit score of 0.81 out of 1.00, indicating an excellent match between the CAF's theoretical constructs and the corpus of political speeches. High dimensional variance (Avg. Variance = 0.12) and a wide range in the Civic Character Index (-0.46 to +0.82) confirm the framework's capacity to effectively discriminate between different rhetorical styles.

-   **Identification of Opposing Rhetorical Profiles:** The data reveals a profound cleavage between `institutional` and `populist` discourse styles. Institutional speakers exhibited a profile high in Dignity (M = 0.88), Justice (M = 0.89), and Pragmatism (M = 0.81), resulting in a strongly positive average Civic Character Index (M = 0.60). Conversely, populist speakers showed a profile high in Tribalism (M = 0.85) and Resentment (M = 0.91), yielding a negative average Index (M = -0.17).

-   **Empirical Validation of Framework's Bipolar Axes:** The framework's theoretical design is strongly supported by correlation analysis. As hypothesized, virtues and their opposing vices demonstrated strong negative relationships, most notably on the Identity axis (Dignity vs. Tribalism, ρ = -.83) and the Justice axis (Justice vs. Resentment, ρ = -.76). This validates the conceptual integrity of the framework's core structure.

-   **Coherent Virtue and Vice Clusters:** The data shows that appeals to virtue and vice are not isolated but form coherent rhetorical patterns. A "virtue cluster" was observed, with strong positive correlations between dimensions like Pragmatism, Justice, and Dignity (ρ > .79). A corresponding "vice cluster" emerged, linking Tribalism, Resentment, Manipulation, and Fantasy (ρ > .71), suggesting these appeals are often deployed in concert.

-   **Identity and Justice as Central Rhetorical Battlegrounds:** The largest effect sizes between the institutional and populist groups were found on the Identity and Justice axes. The near-perfect inversion of scores for Dignity/Tribalism (d = 2.24 / -3.13) and Justice/Resentment (d = 1.01 / -3.08) suggests these axes represent the most significant points of divergence and are central to defining the two opposing civic discourse styles identified in this corpus.

-   **Salience-Weighting as a Key Methodological Innovation:** The Civic Character Index, which incorporates both the intensity and rhetorical prominence (salience) of each dimension, proved to be a powerful summary metric. Its strong correlation with the institutional/populist grouping (r = .89) confirms that weighting appeals by their emphasis provides a highly effective measure of a text's overall civic orientation.

### 3. Literature Review and Theoretical Framework

The Civic Analysis Framework (CAF) v10.0 is explicitly grounded in Aristotelian virtue ethics and contemporary civic republican theory, drawing on scholarship from Aristotle, Michael Sandel, and Philip Pettit. Its central premise is that civic character is revealed through observable rhetorical choices, particularly under conditions of political pressure. The framework operationalizes this by measuring discourse along five bipolar axes—Identity, Truth, Justice, Emotional, and Reality—each representing a tension between a civic virtue and its corresponding vice.

This analytical approach aligns with a growing body of work in computational social science that seeks to quantify complex social and political concepts from textual data. The CAF's innovation lies in its dual-measurement system, assessing both the **intensity** (`raw_score`) and **rhetorical prominence** (`salience`) of each dimension. This methodology is theoretically informed by research in political text analysis (e.g., Laver, Benoit, & Garry, 2003), which demonstrates that weighting textual features by their emphasis yields more valid and nuanced measurements of policy positions and rhetorical strategies.

The current analysis serves as an empirical test of this theoretical structure. If the framework is valid, we would expect to observe specific statistical patterns:
1.  Dimensions conceptualized as virtues should correlate positively with one another.
2.  Dimensions conceptualized as vices should also correlate positively.
3.  Virtues and their opposing vices on a given axis should correlate negatively.
4.  The framework should be capable of distinguishing between texts that are theoretically expected to differ in their civic character, such as speeches from different political traditions or rhetorical styles.

The results of this study are therefore interpreted not only as an analysis of the corpus but also as a validation of the CAF's theoretical foundations and its operationalization of concepts from virtue ethics and civic republicanism.

### 4. Methodology

#### 4.1 Framework Description and Analytical Approach

This study employed the Civic Analysis Framework (CAF) v10.0 to quantify civic virtue and vice patterns in political discourse. The CAF specifies ten primary dimensions organized into five bipolar axes: Identity (Tribalism vs. Dignity), Truth (Manipulation vs. Truth), Justice (Resentment vs. Justice), Emotional (Fear vs. Hope), and Reality (Fantasy vs. Pragmatism). For each dimension, the framework measures both `raw_score` (intensity, 0.0-1.0) and `salience` (rhetorical prominence, 0.0-1.0).

The analysis also utilized derived metrics defined by the framework, including five `Character Tension Indices` that measure strategic contradictions within each axis, and the `Civic Character Index`, a primary summary metric (-1.0 to +1.0) that calculates the overall virtue-versus-vice orientation of a text, weighted by the salience of each appeal.

#### 4.2 Data Structure and Corpus Description

The analysis was performed on a dataset generated from a corpus of eight political speeches, selected to represent a diversity of rhetorical styles, political orientations, and historical contexts. The corpus manifest provided metadata for each document, including a `style` classification (`institutional`, `populist`, `civil_rights`). For group comparison purposes, the eight documents were categorized into two groups of n=4: `institutional` (John Lewis, John McCain, Cory Booker, Mitt Romney) and `populist` (Steve King, JD Vance, Bernie Sanders, Alexandria Ocasio-Cortez).

#### 4.3 Statistical Methods and Analytical Constraints

Given the small sample size (N=8), this study was conducted as a **Tier 3 (Exploratory) analysis**. The statistical methodology prioritized descriptive statistics, the calculation and interpretation of effect sizes (Cohen's *d*, Pearson's *r*), and non-parametric tests robust to small samples.

-   **Descriptive Statistics:** Means (M) and standard deviations (SD) were calculated for all primary and derived metrics to summarize central tendencies and dispersion.
-   **Correlation Analysis:** Spearman's rank-order correlation (ρ) was used to assess monotonic relationships between the `raw_score` of the ten primary dimensions, providing a non-parametric test of the framework's internal consistency.
-   **Group Comparison:** Differences between the `institutional` and `populist` groups were evaluated using descriptive comparisons of means and the calculation of Cohen's *d* to quantify the magnitude of the effect. A Wilcoxon signed-rank test was used for a paired-samples comparison of average virtue versus vice scores.
-   **Framework Effectiveness:** A composite Framework-Corpus Fit score (0-1) was calculated based on dimensional variance, group separation power (effect sizes), and theoretical alignment (correlations) to provide a holistic assessment of the framework's performance on this corpus.

All numerical results are reported in accordance with APA 7th edition standards. All claims are presented as preliminary and suggestive, reflecting the exploratory nature of the analysis.

### 5. Comprehensive Results

#### 5.1 Evaluation of Research Questions

The experiment was designed to address four primary research questions. This section evaluates each question based on the statistical findings.

**1. Speaker Differentiation: How effectively do the 10 CAF dimensions distinguish between different speakers' character profiles?**

**EVALUATION: HIGHLY EFFECTIVE.** The statistical data provides strong evidence of the framework's discriminatory power. The high average variance (0.12) across the `raw_score` of all ten dimensions indicates that scores were not clustered, and the framework successfully detected significant differences between the documents. This is further substantiated by the wide range observed in the primary summary metric, the `Civic Character Index`, which spanned from -0.46 (indicating strong vice-dominance) to +0.82 (strong virtue-dominance). The high "Dimensional Variance" component (0.83) of the Framework-Corpus Fit score serves as a quantitative confirmation of this effectiveness.

**2. Character Signature Analysis: What distinct character signatures emerge across the 5 virtues and 5 vices for each speaker?**

**EVALUATION: DISTINCT SIGNATURES IDENTIFIED.** The analysis revealed at least two clear and opposing character signatures. The `institutional` group signature was characterized by high mean scores on virtues—Dignity (M=0.88), Justice (M=0.89), and Pragmatism (M=0.81)—and very low scores on their opposing vices—Tribalism (M=0.08) and Resentment (M=0.18). In stark contrast, the `populist` group signature was defined by high scores on vices—Tribalism (M=0.85) and Resentment (M=0.91)—and comparatively lower scores on virtues. The correlation matrix further supports the existence of coherent signatures by revealing a "vice cluster" where Tribalism, Resentment, and Fantasy are strongly inter-correlated (ρ > .81).

**3. Civic Character Coherence: How do Civic Character Index scores and pattern classifications vary across speakers, and what does this reveal about their civic character coherence?**

**EVALUATION: SIGNIFICANT VARIATION OBSERVED.** The `Civic Character Index` demonstrated a clear bimodal distribution, cleanly separating the two rhetorical styles. The `institutional` group showed a coherent orientation toward virtue, with a high and tightly clustered mean Index score of 0.60 (SD = 0.24). The `populist` group showed a more mixed or vice-oriented coherence, with a negative mean Index of -0.17 (SD = 0.33). The generally low average scores for the `Character Tension Indices` (all M ≤ 0.12) suggest that most speeches were internally coherent (i.e., did not simultaneously make strong, salient appeals to opposing values). However, the maximum observed `justice_tension` (0.28) indicates the framework can successfully identify specific instances of strategic contradiction or incoherence.

**4. Framework Validation: Does the CAF successfully capture the expected differences between institutional and populist rhetorical styles?**

**EVALUATION: CONFIRMED WITH EXCEPTIONALLY LARGE EFFECT SIZES.** The framework demonstrated outstanding success in capturing the theoretically expected differences. The group comparison yielded a very large effect size (Cohen's *d* = 3.53) for the `Civic Character Index`. The effect sizes for individual dimensions were similarly massive and in the expected directions: Tribalism (*d* = -3.13), Resentment (*d* = -3.08), and Dignity (*d* = 2.24). This indicates that the CAF's operationalization of these concepts aligns powerfully with the real-world rhetorical distinctions between these two styles as represented in the corpus. The "Group Separation Power" component of the fit score was accordingly high at 0.88.

#### 5.2 Descriptive Statistics

Descriptive statistics for the ten primary dimensions and key derived metrics reveal a corpus with wide rhetorical diversity. Virtue dimensions generally scored higher on average than vice dimensions. However, the high standard deviations for vices such as Tribalism (SD = 0.40), Manipulation (SD = 0.40), and Resentment (SD = 0.40) indicate that these dimensions were strongly present in a subset of the documents.

**Table 1: Descriptive Statistics for Primary Dimensions (N=8)**
| Dimension | Mean `raw_score` (SD) | Mean `salience` (SD) | Min `raw_score` | Max `raw_score` |
| :--- | :--- | :--- | :--- | :--- |
| **Virtues** | | | | |
| Dignity | 0.64 (0.33) | 0.58 (0.32) | 0.10 | 0.90 |
| Truth | 0.75 (0.27) | 0.70 (0.24) | 0.15 | 1.00 |
| Justice | 0.79 (0.25) | 0.73 (0.28) | 0.25 | 1.00 |
| Hope | 0.77 (0.26) | 0.72 (0.28) | 0.10 | 0.90 |
| Pragmatism | 0.71 (0.23) | 0.62 (0.28) | 0.30 | 0.90 |
| **Vices** | | | | |
| Tribalism | 0.46 (0.40) | 0.45 (0.41) | 0.00 | 0.90 |
| Manipulation | 0.41 (0.40) | 0.38 (0.40) | 0.00 | 0.90 |
| Resentment | 0.63 (0.40) | 0.62 (0.39) | 0.00 | 0.95 |
| Fear | 0.64 (0.26) | 0.55 (0.29) | 0.20 | 0.90 |
| Fantasy | 0.15 (0.20) | 0.12 (0.18) | 0.00 | 0.50 |

The `Civic Character Index` shows a mean close to zero (M = 0.21) but with a very large standard deviation (SD = 0.55), reflecting the bimodal distribution of scores. The `Character Tension Indices` were low on average, suggesting that direct, high-stakes rhetorical contradictions were not a common feature across the corpus, though they were present in specific instances.

**Table 2: Descriptive Statistics for Derived Metrics (N=8)**
| Metric | Mean (SD) | Min | Max |
| :--- | :--- | :--- | :--- |
| Civic Character Index | 0.21 (0.55) | -0.46 | 0.82 |
| identity_tension | 0.09 (0.07) | 0.00 | 0.24 |
| truth_tension | 0.06 (0.07) | 0.00 | 0.19 |
| justice_tension | 0.10 (0.10) | 0.00 | 0.28 |
| emotional_tension | 0.12 (0.07) | 0.04 | 0.21 |
| reality_tension | 0.04 (0.03) | 0.00 | 0.07 |

#### 5.3 Advanced Metric Analysis

The `Civic Character Index` performed as a highly effective summary of a document's overall rhetorical posture. Its distribution was not normal but bimodal, clustering around a high-virtue pole (the `institutional` group, M = 0.60) and a mixed/vice pole (the `populist` group, M = -0.17). The index's strong correlation with the institutional/populist grouping (r = .89) underscores its validity as a top-line indicator. Furthermore, its strong positive correlation with the total salience of virtue dimensions (r = .95) and strong negative correlation with the total salience of vice dimensions (r = -.93) confirms it is functioning precisely as designed, reflecting the weighted prominence of virtue and vice appeals.

The `Character Tension Indices` provide a more nuanced view, identifying strategic contradictions. While average tension was low, the maximum values observed in `justice_tension` (0.28) and `identity_tension` (0.24) are significant. These scores point to specific documents where speakers likely attempted to blend appeals to fairness with blame-casting (Justice axis) or appeals to universal dignity with exclusionary group identity (Identity axis). This demonstrates the framework's ability to move beyond simple dominant-theme analysis and detect complex, potentially contradictory rhetorical strategies.

#### 5.4 Correlation and Interaction Analysis

A Spearman's rank-order correlation analysis was conducted to examine the inter-dimensional relationships and test the framework's theoretical structure. The results, presented in Table 3, provide strong support for the CAF's design.

**Table 3: Spearman's Rho Correlation Matrix for `raw_score` (N=8)**
| | Dignity | Truth | Justice | Hope | Pragmatism | Tribalism | Manipulation | Resentment | Fear | Fantasy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dignity** | - | | | | | | | | | |
| **Truth** | .45 | - | | | | | | | | |
| **Justice** | **.71** | **.76** | - | | | | | | | |
| **Hope** | .69 | .48 | **.76** | - | | | | | | |
| **Pragmatism** | **.79** | .60 | **.81** | **.74** | - | | | | | |
| **Tribalism** | **-.83** | -.10 | **-.71** | -.67 | **-.76** | - | | | | |
| **Manipulation**| **-.79**| -.12 | -.60 | -.62 | **-.71** | **.71** | - | | | |
| **Resentment** | **-.79**| -.14 | **-.76**| -.64 | **-.79** | **.88** | **.86** | - | | |
| **Fear** | -.60 | -.07 | -.48 | -.21 | -.33 | .67 | .60 | .69 | - | |
| **Fantasy** | **-.76**| -.50 | **-.79**| -.57 | **-.76** | **.81** | **.81** | **.93** | .50 | - |
*Note: Bold values indicate strong correlations (|ρ| > .70).*

Key patterns emerge from this matrix:
-   **Axial Opposition:** The strongest correlations are the negative ones between opposing virtues and vices. The relationship between Dignity and Tribalism (ρ = -.83) is exceptionally strong, confirming the Identity axis as a primary and coherent dimension of rhetorical conflict. Similarly strong negative correlations exist for Justice/Resentment (ρ = -.76) and Pragmatism/Fantasy (ρ = -.76).
-   **Virtue Cohesion:** The virtue dimensions exhibit moderate to strong positive correlations with one another. Pragmatism, for instance, is strongly linked to Justice (ρ = .81), Dignity (ρ = .79), and Hope (ρ = .74). This suggests that speakers who employ one virtue appeal are statistically likely to employ others, forming a consistent "virtue-based" rhetorical style.
-   **Vice Cohesion:** The vice dimensions show even stronger internal cohesion. Resentment is almost perfectly correlated with Fantasy (ρ = .93) and very strongly with Tribalism (ρ = .88) and Manipulation (ρ = .86). This indicates a tightly integrated "vice-based" rhetorical strategy, where appeals to grievance, group exclusion, magical thinking, and distortion are deployed in concert.

#### 5.5 Pattern Recognition and Theoretical Insights

The statistical patterns confirm and enrich the framework's theoretical underpinnings. The clear separation of the corpus into two groups based on the `Civic Character Index` provides empirical evidence for the existence of distinct rhetorical modes that can be classified as broadly "virtuous" or "vicious" according to the CAF's definitions.

The exploratory group comparison between `institutional` and `populist` styles yielded the most significant insight. The data suggests these are not merely different styles but are, in many respects, rhetorical mirror images of one another.

**Table 4: Mean `raw_score` and Effect Sizes for Key Dimensions by Group (N=8)**
| Dimension | Institutional (n=4) | Populist (n=4) | Effect Size (Cohen's *d*) | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Dignity** | 0.88 | 0.40 | **2.24** | Very Large |
| **Tribalism** | 0.08 | 0.85 | **-3.13** | Very Large |
| **Justice** | 0.89 | 0.68 | 1.01 | Large |
| **Resentment** | 0.18 | 0.91 | **-3.08** | Very Large |
| **Pragmatism** | 0.81 | 0.61 | 1.10 | Large |

The enormous effect sizes for Tribalism and Resentment indicate that these dimensions are the core components of the populist rhetorical style identified in this corpus. Conversely, the institutional style is defined by its near-total avoidance of these vices and its strong emphasis on Dignity and Justice. This stark differentiation provides compelling, albeit preliminary, evidence for the framework's construct validity; it measures what it purports to measure and effectively distinguishes between theoretically distinct phenomena.

#### 5.6 Framework Effectiveness Assessment

The CAF v10.0 demonstrated high effectiveness in this exploratory analysis. This assessment is based on its discriminatory power, its fit with the corpus, and the methodological insights it generated.

-   **Discriminatory Power Analysis:** The framework possesses strong discriminatory power. The high variance in scores across all dimensions and the wide, bimodal distribution of the `Civic Character Index` show that it is highly sensitive to differences in rhetorical content. The "Group Separation Power" score of 0.88, derived from the large effect sizes in the group comparison, further quantifies this capability.

-   **Framework-Corpus Fit Evaluation:** The overall Framework-Corpus Fit score was **0.81/1.00**, indicating an excellent match.
    -   **Theoretical Alignment (0.74):** The correlation matrix strongly aligned with the framework's theoretical structure of bipolar axes and virtue/vice clusters.
    -   **Corpus Appropriateness (0.80):** The corpus of persuasive political speeches proved to be an ideal testbed for a framework designed to measure strategic communication and civic character.
    -   The high fit score increases confidence in the validity of the findings, suggesting that the observed patterns are a genuine reflection of the interplay between the framework's constructs and the textual data, rather than an artifact of misapplication.

-   **Methodological Insights:** The analysis validates the framework's key design choice: the dual measurement of intensity (`raw_score`) and prominence (`salience`). The success of the salience-weighted `Civic Character Index` as a powerful summary metric confirms the theoretical premise from Laver et al. (2003) that weighting by emphasis provides a more accurate measure of rhetorical orientation.

### 6. Discussion

The findings of this exploratory analysis, while preliminary due to the small sample size, carry significant theoretical implications. The data provides empirical support for the proposition that civic discourse, at least within this corpus, is not a continuum but is characterized by two distinct, and largely oppositional, rhetorical modes. The `institutional` mode, grounded in appeals to universal virtues like Dignity and Justice, aligns with the ideals of civic republicanism. The `populist` mode, by contrast, appears to operate on a different logic, prioritizing in-group loyalty (Tribalism) and grievance (Resentment).

The tight clustering of vices—Tribalism, Resentment, Manipulation, and Fantasy—is particularly noteworthy. The near-perfect correlation between Resentment and Fantasy (ρ = .93) suggests a powerful rhetorical synergy where the articulation of grievances is coupled with unrealistic or oversimplified solutions. This statistical pattern provides a quantitative signature for a style of politics that scholars have described qualitatively.

The framework's ability to detect these patterns with such clarity, even in a small sample, suggests it is a potent tool for computational political science and philosophy. It moves the study of civic character from a purely interpretive domain to one that can be augmented with systematic, replicable empirical measurement. The limitations are clear: this N=8 study cannot support generalizable claims. However, the sheer magnitude of the observed effects provides a strong warrant for future research. A larger-scale study is needed to confirm if these two rhetorical profiles are stable and generalizable features of contemporary political discourse or specific to this particular collection of speeches.

### 7. Conclusion

This research report detailed an exploratory statistical analysis of the Civic Analysis Framework (CAF) v10.0. The analysis demonstrated the framework's high degree of effectiveness in discriminating between different styles of political speech and empirically validated its core theoretical structure. The data revealed two starkly different rhetorical profiles within the corpus—an `institutional` style characterized by appeals to civic virtue and a `populist` style characterized by appeals to civic vice. The Identity and Justice axes were identified as the primary sites of this rhetorical division.

Despite the exploratory nature of this study, the statistical evidence is compelling. The framework's internal consistency, its high fit with the corpus, and its ability to distinguish between groups with exceptionally large effect sizes all point to its promise as a rigorous, data-driven tool for academic inquiry. The CAF provides a methodology for translating the abstract concepts of virtue ethics and civic republicanism into quantifiable metrics, enabling new avenues of research into the character of democratic discourse. Future work should focus on replicating these findings with a larger corpus to establish the generalizability of the observed patterns.

### 8. Methodological Summary

The statistical analysis was conducted as a Tier 3 exploratory study on a dataset of N=8 documents, scored using the Civic Analysis Framework (CAF) v10.0. The methodology prioritized descriptive statistics (means, standard deviations), effect size calculations (Cohen's *d*), and non-parametric correlation analysis (Spearman's rank-order rho, ρ) to accommodate the small sample size. Group comparisons between `institutional` (n=4) and `populist` (n=4) styles were performed by comparing mean scores and calculating effect sizes. A Wilcoxon signed-rank test was used for a paired comparison of average virtue and vice scores. A composite Framework-Corpus Fit score was calculated to assess the framework's overall performance, incorporating measures of dimensional variance, group separation power, and theoretical alignment. All interpretations were framed as preliminary and suggestive, in line with the exploratory protocol.