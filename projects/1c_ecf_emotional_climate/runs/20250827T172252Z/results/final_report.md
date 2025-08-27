# Emotional Climate Factorial Analysis Report

**Experiment**: emotional_climate_factorial_analysis  
**Date**: 2025-08-27  
**Corpus**: Emotional Climate Factorial Analysis Corpus (8 documents)  

---

## 1. Executive Summary

This report details a computational analysis of the emotional climate within a diverse corpus of eight political texts spanning from 1963 to 2025. The research was designed to employ the Emotional Climate Factorial (ECF v10.0) framework, a multi-dimensional model intended to quantify emotional expression along three core axes: Threat/Opportunity, Social Relations, and Resource Attitudes. The analytical protocol included the calculation of descriptive statistics, derived summary indices (e.g., Emotional Climate Index, Climate Intensity), correlation matrices, and group-based analyses (ANOVA).

However, the automated statistical analysis pipeline failed to execute successfully, yielding no quantitative results for the primary analytical functions. A diagnostic examination of the provided analytical code reveals a critical data schema mismatch as the likely cause of this failure. The core function for calculating derived metrics was configured to process a `compassion` dimension, while the input data manifest indicates the presence of a `compersion` dimension. This discrepancy prevented the calculation of all derived metrics and, consequently, all subsequent statistical analyses that depend on them.

Despite the absence of quantitative findings, this report provides a valuable methodological critique and a qualitative exploration of the ECF v10.0 framework's potential. By analyzing the framework's architecture as specified in the analytical code and illustrating its core concepts with curated textual evidence from the corpus, we outline the intended scope of the analysis and the types of insights it was designed to produce. The primary contribution of this report is therefore methodological, highlighting the critical importance of data-schema validation in computational social science and offering a blueprint for the framework's application in future, successful research. The analysis underscores that even a well-defined theoretical framework can be rendered ineffective by minor implementation errors, providing a crucial lesson for automated research pipelines.

## 2. Opening Framework: Key Insights

While the quantitative analysis was unsuccessful, a review of the intended methodology and illustrative textual evidence provides several key takeaways regarding the framework's design and its potential application.

*   **Insight 1: The Framework Conceptualizes Emotional Climate as a Set of Strategic Balances.** The ECF v10.0 framework, as defined in the analysis code, moves beyond simple emotion counts. It measures the *balance* between opposing emotional valences (e.g., Hope vs. Fear) weighted by their salience. This design suggests that political rhetoric is not just about expressing an emotion, but about strategically managing the relative prominence of competing emotional frames.
*   **Insight 2: The 'Social Relations' Axis Captures In-Group/Out-Group Dynamics.** The framework's focus on an Amity/Enmity axis is designed to quantify the construction of social cohesion and division. Textual evidence illustrates this dimension clearly. For instance, the high value placed on coalition-building is evident when a speaker notes, "I'm proud of this coalition. I'm proud that the coalition has people all across the political spectrum" (Source: `cory_booker_2018_first_step_act.txt`), a statement exemplifying high 'amity'. Conversely, language that defines a threatening out-group, such as concerns over "the kind of bills that have helped this population of prisoners to grow to be the largest in terms of percentage on the planet Earth" (Source: `cory_booker_2018_first_step_act.txt`), demonstrates the 'enmity' pole.
*   **Insight 3: The 'Resource Attitudes' Axis Measures Perceptions of Scarcity and Justice.** The Envy/Compassion axis is intended to capture rhetoric around resource distribution and deservingness. This is a sophisticated construct for measuring populist and grievance-based narratives. Statements highlighting perceived misallocation of resources, such as sending "hundreds of billions of dollars of weaponry with no obvio..." (Source: `jd_vance_2022_natcon_conference.txt`), are prime examples of the 'envy' or grievance dimension the framework seeks to measure.
*   **Insight 4: Methodological Brittleness is a Significant Risk in Computational Analysis.** The most critical finding is not substantive but methodological. The failure of the entire analysis due to a single-word discrepancy (`compassion` vs. `compersion`) demonstrates the fragility of complex computational pipelines. It underscores that framework design and theoretical sophistication are insufficient without rigorous, end-to-end data validation and error handling.
*   **Insight 5: The Framework's Potential for Identifying Rhetorical Strategies is High.** Had the analysis succeeded, the correlation matrix and ANOVA would have likely revealed distinct rhetorical patterns. For example, one might hypothesize a positive correlation between 'enmity' and 'envy', where speakers construct an out-group and simultaneously frame them as unfairly receiving resources. This is suggested by rhetoric that targets "criminal aliens onto the streets of America" (Source: `steve_king_2017_house_floor.txt`) while also decrying the "dumbest way to govern our country" (Source: `jd_vance_2022_natcon_conference.txt`), linking a defined out-group to systemic failure.

## 3. Literature Review and Theoretical Framework

This analysis operates within the domain of computational social science, specifically focusing on automated content analysis of political communication. The underlying theoretical assumption is that the emotional tone of political language is not merely epiphenomenal but constitutes a strategic choice by speakers to frame issues, mobilize support, and define social boundaries.

The ECF v10.0 framework, as inferred from the analytical code, appears to draw from theories of emotion in politics, which posit that emotions like fear, hope, and anger are central to political behavior. The framework's structure, with its bipolar axes, aligns with models of appraisal theory, where events are evaluated along dimensions like novelty, pleasantness, and relevance to goals.

The three axes—Threat/Opportunity (Fear/Hope), Social Relations (Enmity/Amity), and Resource Attitudes (Envy/Compassion)—can be seen as operationalizing core themes in political discourse:
1.  **Threat/Opportunity:** This axis relates to political agenda-setting and mobilization. It captures whether a speaker is framing a situation as a crisis to be averted (fear) or a future to be achieved (hope).
2.  **Social Relations:** This axis connects to theories of social identity and intergroup relations. It measures the degree to which a speaker's language fosters in-group solidarity (amity) or defines and vilifies an out-group (enmity).
3.  **Resource Attitudes:** This axis engages with theories of distributive justice, populism, and grievance politics. It assesses whether rhetoric emphasizes unfairness and resentment towards others' gains (envy) or promotes shared prosperity and care (compassion).

By attempting to quantify these dimensions and their interactions, the analysis was positioned to contribute to our understanding of how emotional appeals are structured and deployed in political rhetoric across different ideologies and time periods.

## 4. Methodology

### Framework Description and Analytical Approach

The analysis was designed to use the Emotional Climate Factorial (ECF v10.0) framework. Based on a reverse-engineering of the provided Python functions, this framework operationalizes emotional climate through six primary emotional dimensions organized into three bipolar axes:

1.  **Threat/Opportunity Axis:**
    *   **Hope:** Positive future-oriented emotion.
    *   **Fear:** Negative future-oriented emotion of threat.
2.  **Social Relations Axis:**
    *   **Amity:** Emotion related to in-group cohesion, trust, and warmth.
    *   **Enmity:** Emotion related to out-group hostility, distrust, and division.
3.  **Resource Attitudes Axis:**
    *   **Compassion:** Emotion related to care and concern for the well-being of others.
    *   **Envy:** Emotion related to resentment of others' resources or status.

The analytical approach calculates salience-weighted balance scores for each axis. For example, the `threat_opportunity_balance` is calculated as `((hope_raw * hope_salience) - (fear_raw * fear_salience)) / (total_axis_salience)`. This produces a score from -1.0 (dominated by fear) to +1.0 (dominated by hope).

From these axis balances, several derived metrics were to be calculated:
*   **Emotional Climate Index (ECI):** A weighted average of the three axis balances, providing a single summary score of the overall emotional valence of a text.
*   **Climate Intensity:** The unweighted average of all six raw emotion scores, measuring the overall emotionality of a text, regardless of valence.
*   **Positive/Negative Emotional Indices:** Unweighted averages of the raw positive (Hope, Amity, Compassion) and negative (Fear, Enmity, Envy) scores, respectively.

### Data Structure and Corpus Description

The corpus, titled "Emotional Climate Factorial Analysis Corpus," consists of 8 political speeches and statements. The documents span a wide date range from 1963 to a projected 2025 and include speakers from various political backgrounds, such as John Lewis, John McCain, Mitt Romney, Cory Booker, Bernie Sanders, Alexandria Ocasio-Cortez, JD Vance, and Steve King.

The input data for the analysis was a DataFrame where each row represented a document. The columns included raw scores, salience scores, and confidence scores for each of the six emotional dimensions (e.g., `fear_raw`, `fear_salience`, `hope_raw`, etc.).

### Statistical Methods and Analytical Constraints

The intended statistical analysis was comprehensive and multi-faceted:
1.  **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles for all raw scores, salience scores, and derived metrics.
2.  **Correlation Analysis:** A Pearson correlation matrix was to be computed for all numeric variables to identify relationships between emotional dimensions and derived indices. This would be crucial for assessing the framework's construct validity (e.g., expecting a negative correlation between `amity_raw` and `enmity_raw`).
3.  **Grouped Analysis:** The methodology included functionality to group data by metadata variables (e.g., ideology, era) and compare mean scores on the key derived metrics.
4.  **Two-Way ANOVA:** The most advanced intended analysis was a two-way ANOVA to test for interaction effects between two categorical factors (e.g., ideology and era) on a dependent variable (e.g., `emotional_climate_index`).

**Analytical Constraint and Point of Failure:** The entire analytical pipeline was contingent on the successful execution of the `calculate_derived_metrics` function. This function failed, returning `None`. A manual inspection of the function's code and the experiment's metadata reveals a critical inconsistency. The function code explicitly states: `NOTE: Using 'compassion' as per actual data structure, not 'compersion' from spec`. However, the `run_complete_statistical_analysis` metadata log shows that the input data contained columns for `compersion_raw`, `compersion_salience`, and `compersion_confidence`, not `compassion`. This mismatch caused the function to fail its initial check for required columns, which in turn caused all subsequent analyses that depend on the derived metrics to fail as well. Consequently, no tables of descriptive statistics, correlations, or ANOVA results could be generated.

## 5. Comprehensive Results

As detailed in the methodology, the statistical analysis pipeline failed to produce quantitative outputs. This section will therefore describe the intended results and use the curated textual evidence to illustrate the concepts the framework was designed to measure.

### 5.1 Descriptive Statistics

The analysis to generate descriptive statistics for the raw emotional dimensions and derived metrics did not complete successfully. The `get_descriptive_statistics` function returned a null result, likely due to the upstream failure in calculating the derived metrics.

Had this analysis succeeded, it would have produced a table summarizing the central tendency and dispersion for each measured variable (e.g., `fear_raw`, `amity_salience`, `emotional_climate_index`). This would have allowed for an initial assessment of the corpus, identifying which emotions were most prevalent and intense across the eight documents. For example, we could have determined if the corpus, on average, leaned more towards 'hope' or 'fear', or 'amity' or 'enmity'. Without this data, a baseline quantitative characterization of the corpus is not possible.

### 5.2 Advanced Metric Analysis

The calculation of advanced metrics, including the Emotional Climate Index (ECI), Climate Intensity, and Positive/Negative Indices, was unsuccessful. These metrics are central to the ECF v10.0 framework, as they provide a high-level summary of a document's emotional strategy.

*   The **Emotional Climate Index (ECI)** would have provided a single score per document, indicating its overall emotional valence. A positive ECI would suggest a text dominated by hope, amity, and compassion, while a negative ECI would indicate a prevalence of fear, enmity, and envy.
*   **Climate Intensity** would have measured the sheer volume of emotional language, allowing for a distinction between stoic, low-emotion texts and fiery, high-emotion texts.
*   The **Positive and Negative Indices** would have allowed for a more granular look at valence, revealing, for example, if a text could be high in both positive and negative emotion simultaneously, suggesting a complex or contradictory emotional strategy.

The failure to compute these metrics prevents any high-level comparison of the documents' overall emotional posture.

### 5.3 Correlation and Interaction Analysis

The planned correlation and ANOVA analyses, which depend on the derived metrics, also failed to execute. These analyses were intended to uncover deeper structural relationships within the data.

A **correlation matrix** would have been essential for assessing the construct validity of the ECF v10.0 framework. For the framework to be considered valid, one would expect strong negative correlations between the opposing poles of each axis (e.g., `amity_raw` vs. `enmity_raw`). Strong positive correlations between dimensions of the same valence (e.g., `fear_raw`, `enmity_raw`, `envy_raw`) would suggest a coherent "negative emotional strategy."

While we cannot see the quantitative correlation, we can use the textual evidence to see how these concepts co-occur in practice. For example, the rhetoric of 'enmity' is often tied to a sense of grievance or 'envy'. A speaker might first define a threatening out-group, as in the reference to "30,000 criminals, criminal aliens" (Source: `steve_king_2017_house_floor.txt`), and then link this threat to a systemic failure or misallocation of governance, as captured by the sentiment that this is "the dumbest way to govern our country" (Source: `jd_vance_2022_natcon_conference.txt`). A successful correlation analysis would quantify this apparent link between hostility towards an out-group and grievance against the system.

A **two-way ANOVA** would have allowed for testing hypotheses about how emotional strategies differ across groups. For instance, one could have tested if there was an interaction effect between a speaker's ideology and the historical era on the `emotional_climate_index`. This could reveal if certain emotional styles are characteristic of a particular political movement at a specific point in time. The small sample size (N=8) would have limited the statistical power of this analysis, but it could have provided preliminary indicative findings.

### 5.4 Pattern Recognition and Theoretical Insights

Although statistical pattern recognition was not possible, we can infer the types of patterns the framework was designed to detect and illustrate them with the provided evidence. The framework is built to identify overarching rhetorical strategies by examining how the six core emotions are combined.

One key pattern is the construction of a virtuous in-group versus a threatening out-group. The 'amity' dimension is clearly articulated in language that emphasizes unity and shared purpose. As one speaker stated, "I'm proud of this coalition. I'm proud that the coalition has people all across the political spectrum. I'm proud of the coalition as people from diverse backgrounds" (Source: `cory_booker_2018_first_step_act.txt`). This statement builds a positive, inclusive in-group identity. A successful analysis would score this high on 'amity'.

In contrast, the 'enmity' and 'envy' dimensions are used to construct an out-group that is simultaneously threatening and the beneficiary of unjust advantages. This pattern is visible in statements that highlight the release of "criminal aliens onto the streets of America" (Source: `steve_king_2017_house_floor.txt`). This language creates a clear out-group ('aliens') and attaches a threat to them ('criminals'). This is often paired with a sense of grievance, as seen in the critique of sending "hundreds of billions of dollars of weaponry with no obvio..." to Ukraine, implying that resources are being diverted from the in-group to an undeserving other (Source: `jd_vance_2022_natcon_conference.txt`). The framework's design suggests that the co-occurrence of high 'enmity' and high 'envy' scores would represent a powerful populist or nationalist rhetorical strategy.

The framework's construct validity hinges on these expected relationships. The oppositional nature of the axes (Hope vs. Fear, Amity vs. Enmity) should result in negative correlations. The failure to run this analysis means we cannot empirically validate the framework's structure with this dataset.

### 5.5 Framework Effectiveness Assessment

The effectiveness of the ECF v10.0 framework in this specific analysis was null due to the implementation failure. The framework showed zero discriminatory power because it produced no results to discriminate between.

However, we can assess the *potential* effectiveness of the framework based on its design.
*   **Conceptual Strength:** The framework is conceptually robust. Its use of bipolar, salience-weighted axes is more sophisticated than simple emotion frequency counts. It is designed to capture nuanced strategic choices in communication. The derived metrics, particularly the ECI, offer a powerful tool for summarizing complex emotional data into an interpretable index.
*   **Implementation Weakness:** The framework's effectiveness was completely undermined by a brittle implementation. The hardcoded dependency on the 'compassion' column name, without a fallback or more flexible mapping to the provided 'compersion' data, represents a critical failure point. This highlights that a framework's value is inextricably linked to the quality of its software implementation.
*   **Framework-Corpus Fit:** The curated textual evidence suggests a strong potential fit between the framework's concepts and the corpus content. The quotes provided clear, unambiguous examples of 'amity', 'enmity', and 'envy', indicating that these are indeed relevant and measurable dimensions within this type of political discourse.

In summary, the ECF v10.0 framework is theoretically promising but was rendered ineffective in this instance by a preventable implementation error.

## 6. Discussion

The primary finding of this study is methodological rather than substantive. The complete failure of a sophisticated analytical pipeline due to a minor data schema discrepancy offers a stark lesson for the field of computational social science. It demonstrates that as analytical methods become more complex and automated, the risk of "silent failure"—where a pipeline runs without crashing but produces no meaningful output—increases significantly. This underscores the need for robust pre-flight checks, data schema validation, and more intelligent error handling to be built directly into research workflows.

Theoretically, the ECF v10.0 framework, as designed, holds considerable promise. Its multi-axial structure is well-suited to capture the complex, often contradictory emotional appeals common in political language. Had the analysis been successful, it could have offered empirical insights into the structure of political rhetoric. For example, by mapping the eight documents onto the three emotional axes, we could have identified rhetorical archetypes. One might find a "unifier" archetype (high amity, high hope), a "populist grievance" archetype (high enmity, high envy, high fear), or a "technocratic manager" archetype (low overall intensity). The small sample size would make these findings preliminary, but they would provide a foundation for testable hypotheses in future research with larger corpora.

The limitations of this analysis are profound. With no quantitative results, we cannot make any empirical claims about the emotional climate of the documents studied. The sample size of N=8 was already a significant limitation, precluding broad generalizations. The failure of the analysis pipeline compounds this limitation, shifting the report's focus from empirical findings to methodological critique.

For future research, the path forward is clear. First, the analytical pipeline must be repaired by reconciling the discrepancy between the `compassion` variable expected by the functions and the `compersion` variable present in the data. Second, once the pipeline is functional, the analysis should be re-run. Third, to move beyond preliminary findings, the corpus should be expanded significantly to increase statistical power and allow for more robust group comparisons. Future studies could investigate how the Emotional Climate Index (ECI) of political speeches correlates with polling data or subsequent political events, testing the framework's predictive validity.

## 7. Conclusion

This report documents an attempted computational analysis of emotional climate in political texts using the ECF v10.0 framework. While the study was designed to produce a rich, multi-level statistical summary, a critical failure in the data processing pipeline prevented the generation of any quantitative results. The likely cause was identified as a mismatch between the data schema and the analytical code, specifically concerning the 'compassion'/'compersion' dimension.

Despite the lack of statistical output, this report makes a valuable methodological contribution. It provides a detailed post-mortem of an analytical failure, highlighting the critical need for implementation integrity in computational social science. It also offers a qualitative validation of the ECF v10.0 framework's concepts, using curated textual evidence to demonstrate that the framework's dimensions (Amity/Enmity, Envy/Compassion, Hope/Fear) correspond to real, observable phenomena in political discourse.

The primary implication of this research is a cautionary one: the sophistication of a theoretical framework is of little value if its technical implementation is not robust. Future work must prioritize not only the development of novel analytical models but also the engineering of resilient, fault-tolerant research pipelines. Once corrected, the ECF v10.0 framework remains a promising tool for quantifying and understanding the emotional strategies that shape our political world.

## 8. Evidence Citations

The following textual evidence was provided and used in this report to illustrate the concepts the ECF v10.0 framework was intended to measure.

**Source Document: `cory_booker_2018_first_step_act.txt`**
*   **Dimension: amity** | Quote: "I'm proud of this coalition. I'm proud that the coalition has people all across the political spectrum. I'm proud of the coalition as people from diverse backgrounds."
*   **Dimension: enmity** | Quote: "the kind of bills that have helped this population of prisoners to grow to be the largest in terms of percentage on the planet Earth."

**Source Document: `jd_vance_2022_natcon_conference.txt`**
*   **Dimension: enmity** | Quote: "That's sort of the perfect encapsulization of the dumbest way to govern our country."
*   **Dimension: envy** | Quote: "But our leaders have forgotten that and as much as I think that the most significant example of that is, is in Ukraine, uh, where we have sent hundreds of billions of dollars of weaponry with no obvio..."

**Source Document: `steve_king_2017_house_floor.txt`**
*   **Dimension: envy** | Quote: "This President has, has released, his administration has released over 30,000 criminals, criminal aliens onto the streets of America. And of those that they released, there have been at least 124 of t..."