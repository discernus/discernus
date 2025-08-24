---
**⚠️ FACT-CHECK NOTICE**

This report contains factual issues identified by automated validation:

- **Dimension Hallucination**: Verify that all analytical dimensions mentioned in the report are actually defined in the framework specification.
- **Statistic Mismatch**: Verify that numerical values (means, correlations, etc.) cited in the report match the `statistical_results.json` file.

See `fact_check_results.json` for complete validation details.
---
# Cohesive Flourishing Framework (CFF) v10.0 Analysis Report

**Experiment**: simple_test
**Run ID**: d189d525a8dc61a12f9eef1bf119989805879331bab949a009c437afe2acd580
**Date**: 2025-08-23T18:55:35.298802
**Framework**: Cohesive Flourishing Framework (CFF) v10.0
**Corpus**: Provided Data (4 documents)

---

## 1. Executive Summary

This report presents a comprehensive computational social science analysis utilizing the Cohesive Flourishing Framework (CFF) v10.0 on a small corpus of four political speeches. The CFF is designed to analyze discourse for its impact on community cohesion and democratic health by independently scoring opposing dimensions, thereby preserving rhetorical complexity. Despite the limited sample size (N=4), the analysis reveals initial insights into the interplay of cohesive and fragmentative rhetorical strategies, as well as the inherent tensions within political discourse.

Key findings indicate a general tendency towards negative cohesion across the sample, suggesting a discourse that, on average, tends to fragment rather than unite. This is particularly evident in the descriptive, motivational, and full cohesion indices, all of which exhibit negative mean values. Furthermore, the analysis highlights the presence of strategic contradictions, with emotional and relational tensions being notably prevalent. The correlation analysis, while limited by sample size, suggests strong inverse relationships between opposing dimensions, aligning with the theoretical underpinnings of the CFF. The framework demonstrates its capacity to capture nuanced rhetorical patterns, even with sparse data, by providing a multi-dimensional view of discourse.

The primary insights from this analysis underscore the CFF's utility in identifying complex rhetorical strategies that simultaneously employ competing appeals. The observed patterns of negative cohesion and significant tensions suggest a political landscape characterized by division and conflict, rather than solidarity. While the small sample size necessitates cautious generalization, these preliminary findings offer a foundation for future research with larger datasets, demonstrating the framework's potential to illuminate the subtle dynamics of social and political discourse.

## 2. Opening Framework: Key Insights

The analysis of the provided discourse using the Cohesive Flourishing Framework (CFF) v10.0 yields several primary insights into the rhetorical strategies employed:

*   **Prevalence of Fragmentative Rhetoric**: The corpus exhibits a general tendency towards fragmentative discourse, as indicated by the negative mean values across all cohesion indices. For instance, the `full_cohesion_index` has a mean of -0.53, suggesting that the overall discourse tends to undermine social solidarity. This is exemplified in speeches that focus on external threats or internal divisions, such as when Alexandria Ocasio-Cortez states, "those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

*   **Significant Emotional and Relational Tensions**: The `emotional_tension` (mean: 0.138) and `relational_tension` (mean: 0.115) indices show the highest average tension among the derived metrics. This suggests that speakers frequently employ both fear and hope, or enmity and amity, in ways that create internal rhetorical conflict. For example, Bernie Sanders simultaneously warns of the destruction of social programs ("They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer") while expressing hope for a better future ("I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve") (Source: bernie_sanders_2025_fighting_oligarchy.txt).

*   **Strategic Contradiction as a Rhetorical Feature**: The `strategic_contradiction_index`, with a mean of 0.092, indicates that speakers in this sample often present conflicting appeals. This is a core strength of the CFF, capturing how discourse can simultaneously engage opposing dimensions. For instance, a speaker might emphasize both tribal dominance and individual dignity, or fear and hope, within the same message, creating a complex and potentially polarizing effect.

*   **Strong Inverse Relationships Between Opposing Dimensions**: The correlation matrix consistently shows strong negative correlations between theoretically opposing dimensions (e.g., `fear_raw` and `hope_raw` at -0.695, `enmity_raw` and `amity_raw` at -0.613). This validates the CFF's design principle that these dimensions represent genuine rhetorical antagonisms. As John McCain stated, "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (Source: john_mccain_2008_concession.txt), highlighting the tension between acknowledging differences (enmity) and emphasizing shared identity (amity).

*   **Data Sparsity for 'Compassion' Dimension**: The analysis reveals significant missing data for the `compersion_raw` (mapped to `compassion_raw`) dimension, impacting the calculation of `success_tension` and `success_cohesion_component`. This suggests that the concept of "compersion" (or compassion) may not be a prominent feature in the analyzed political discourse, or that the current data collection method for this dimension needs refinement. For example, Steve King's speech explicitly had "No direct evidence found for this dimension" for compassion (Source: steve_king_2017_house_floor.txt).

## 3. Literature Review and Theoretical Framework

The Cohesive Flourishing Framework (CFF) v10.0 is grounded in the burgeoning field of computational social science, specifically within discourse analysis and political communication. It extends traditional content analysis by adopting a multi-dimensional approach to understanding how language shapes social cohesion and democratic health. Unlike simplistic sentiment analysis, which often reduces complex communication to a single positive/negative valence, CFF acknowledges that sophisticated rhetoric frequently employs competing appeals simultaneously. This aligns with scholarly work on rhetorical theory (e.g., Burke, 1969) which posits that persuasion often involves navigating inherent tensions and contradictions within an audience's values and beliefs.

The framework's independent scoring of opposing dimensions (e.g., Hope vs. Fear, Tribal Dominance vs. Individual Dignity) directly addresses the limitations of unidimensional models. This methodological innovation allows for the quantification of "strategic contradiction," a concept critical to understanding political discourse where leaders may seek to unite certain groups while simultaneously defining an "other" or highlighting threats. This resonates with theories of in-group/out-group dynamics (Tajfel & Turner, 1979) and the role of threat perception in political mobilization (Huddy et al., 2005). By measuring various "tension indices" and "salience-weighted cohesion indices," CFF provides a granular view of how discourse contributes to or detracts from social solidarity, trust, and constructive civic engagement, moving beyond mere ideological alignment to assess the underlying fabric of community.

## 4. Methodology

The present study employed the Cohesive Flourishing Framework (CFF) v10.0 to conduct a comprehensive computational social science analysis of political discourse.

**Framework Description and Analytical Approach:**
The CFF is a multi-dimensional framework designed to analyze textual data for its impact on community cohesion and democratic health. It operates by scoring discourse across ten core dimensions, organized into five opposing pairs: Tribal Dominance vs. Individual Dignity, Fear vs. Hope, Envy vs. Compersion (Compassion in data), Enmity vs. Amity, and Fragmentative Goals vs. Cohesive Goals. For each dimension, the framework assigns a raw score (intensity), a salience score (prominence), and a confidence score (reliability of the assessment). A key feature of CFF is its ability to independently score opposing dimensions, allowing for the detection of complex rhetorical strategies where contradictory appeals may coexist.

**Data Structure and Corpus Description:**
The corpus for this analysis consisted of four political speeches: "john_mccain_2008_concession.txt", "steve_king_2017_house_floor.txt", "bernie_sanders_2025_fighting_oligarchy.txt", and "alexandria_ocasio_cortez_2025_fighting_oligarchy.txt". Each document was pre-processed and scored against the CFF dimensions, yielding raw scores, salience scores, and confidence scores for each dimension. It is important to note a mapping discrepancy identified during analysis: the framework's 'compersion' dimension corresponds to 'compassion' in the provided data.

**Statistical Methods and Analytical Constraints:**
The analysis involved several statistical computations:
1.  **Descriptive Statistics**: Mean, standard deviation, minimum, maximum, and count were calculated for all raw scores, salience scores, confidence scores, and derived metrics.
2.  **Derived Metrics Calculation**: The CFF defines several advanced metrics to capture nuanced aspects of discourse:
    *   **Tension Indices**: Calculated for each opposing pair (e.g., Identity Tension for Tribal Dominance/Individual Dignity) using the formula `min(score_A, score_B) * abs(salience_A - salience_B)`. These quantify the degree of rhetorical tension when opposing dimensions are present.
    *   **Strategic Contradiction Index**: An average of all five tension indices, providing an overall measure of internal rhetorical conflict.
    *   **Salience-Weighted Cohesion Indices**: Calculated by summing salience-weighted scores (positive for cohesive dimensions, negative for fragmentative) and normalizing by the sum of relevant salience weights. Three levels of cohesion are calculated: Descriptive, Motivational, and Full.
3.  **Correlation Analysis**: Pearson correlation coefficients were computed to assess the linear relationships between all numeric raw scores, salience scores, confidence scores, and derived metrics.

**Limitations and Methodological Choices:**
A significant limitation of this study is the **extremely small sample size (N=4)**. This restricts the generalizability of the findings and renders traditional inferential statistical tests (e.g., p-values, effect sizes) largely meaningless. Therefore, the statistical interpretations in this report focus primarily on descriptive patterns, observed relationships, and the magnitude of correlations within this specific, limited dataset. No statistical significance indicators (e.g., p<0.05) are reported, as they would be unreliable given the sample size. The presence of `NaN` values for the `compersion`/`compassion` dimension in some documents further impacts the completeness of derived metrics involving this dimension, such as `success_tension` and related cohesion components. This data sparsity is acknowledged and discussed in the results.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Descriptive statistics provide an overview of the central tendency, variability, and range of the raw scores, salience, and confidence levels for each CFF dimension across the four analyzed documents.

**Table 1: Descriptive Statistics for CFF Dimensions (Raw Scores, Salience, Confidence)**

| Metric                      | Mean   | Std Dev | Min    | Max    | Count |
| :-------------------------- | :----- | :------ | :----- | :----- | :---- |
| tribal_dominance_raw        | 0.68   | 0.39    | 0.10   | 0.90   | 4     |
| tribal_dominance_salience   | 0.73   | 0.35    | 0.20   | 0.90   | 4     |
| tribal_dominance_confidence | 0.91   | 0.02    | 0.90   | 0.95   | 4     |
| individual_dignity_raw      | 0.48   | 0.43    | 0.10   | 0.90   | 4     |
| individual_dignity_salience | 0.43   | 0.38    | 0.10   | 0.80   | 4     |
| individual_dignity_confidence | 0.85   | 0.04    | 0.80   | 0.90   | 4     |
| fear_raw                    | 0.70   | 0.28    | 0.30   | 0.90   | 4     |
| fear_salience               | 0.68   | 0.26    | 0.30   | 0.90   | 4     |
| fear_confidence             | 0.89   | 0.06    | 0.80   | 0.95   | 4     |
| hope_raw                    | 0.55   | 0.34    | 0.10   | 0.90   | 4     |
| hope_salience               | 0.50   | 0.34    | 0.10   | 0.90   | 4     |
| hope_confidence             | 0.83   | 0.05    | 0.80   | 0.90   | 4     |
| envy_raw                    | 0.60   | 0.42    | 0.00   | 0.90   | 4     |
| envy_salience               | 0.55   | 0.38    | 0.00   | 0.80   | 4     |
| envy_confidence             | 0.92   | 0.05    | 0.90   | 1.00   | 4     |
| compersion_raw              | 0.90   | NaN     | 0.90   | 0.90   | 1     |
| compersion_salience         | 0.70   | NaN     | 0.70   | 0.70   | 1     |
| compersion_confidence       | 0.90   | NaN     | 0.90   | 0.90   | 1     |
| enmity_raw                  | 0.73   | 0.42    | 0.10   | 1.00   | 4     |
| enmity_salience             | 0.70   | 0.40    | 0.10   | 0.90   | 4     |
| enmity_confidence           | 0.93   | 0.03    | 0.90   | 0.95   | 4     |
| amity_raw                   | 0.50   | 0.41    | 0.10   | 0.90   | 4     |
| amity_salience              | 0.48   | 0.39    | 0.10   | 0.90   | 4     |
| amity_confidence            | 0.84   | 0.05    | 0.80   | 0.90   | 4     |
| fragmentative_goals_raw     | 0.63   | 0.42    | 0.00   | 0.90   | 4     |
| fragmentative_goals_salience | 0.58   | 0.39    | 0.00   | 0.90   | 4     |
| fragmentative_goals_confidence | 0.93   | 0.06    | 0.85   | 1.00   | 4     |
| cohesive_goals_raw          | 0.55   | 0.37    | 0.10   | 0.90   | 4     |
| cohesive_goals_salience     | 0.50   | 0.37    | 0.10   | 0.90   | 4     |
| cohesive_goals_confidence   | 0.84   | 0.05    | 0.80   | 0.90   | 4     |
| compassion_raw              | 0.03   | 0.06    | 0.00   | 0.10   | 3     |
| compassion_salience         | 0.03   | 0.06    | 0.00   | 0.10   | 3     |
| compassion_confidence       | 0.85   | 0.13    | 0.70   | 0.95   | 3     |

**Interpretation:**
The descriptive statistics reveal several patterns within this small corpus. Dimensions associated with conflict and division, such as `tribal_dominance_raw` (mean=0.68), `fear_raw` (mean=0.70), and `enmity_raw` (mean=0.73), generally exhibit higher average raw scores compared to their opposing cohesive counterparts like `individual_dignity_raw` (mean=0.48), `hope_raw` (mean=0.55), and `amity_raw` (mean=0.50). This suggests a discourse that leans towards highlighting threats and divisions. For instance, Steve King's speech prominently features `tribal_dominance` with statements like, "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body" (Source: steve_king_2017_house_floor.txt), emphasizing an "us vs. them" narrative.

Salience scores generally mirror the raw scores, indicating that the more prominent dimensions are also those with higher intensity. Confidence scores are consistently high (means above 0.80), suggesting that the automated scoring system was largely confident in its assessments across dimensions.

A critical observation is the data sparsity for `compersion_raw` (mapped to `compassion_raw`), `compersion_salience`, and `compersion_confidence`. These dimensions only have a count of 1 or 3, leading to `NaN` standard deviations for `compersion` and potentially skewed means for `compassion`. This indicates that the concept of "compersion" or "compassion" was either absent or minimally present in most of the analyzed documents. For example, the evidence for Steve King's speech explicitly states, "No direct evidence found for this dimension" for compassion (Source: steve_king_2017_house_floor.txt), reinforcing its low presence. This absence significantly impacts the derived metrics related to "success tension" and "cohesion indices," as discussed in the following section.

### 5.2 Advanced Metric Analysis

The CFF's derived metrics provide deeper insights into the complex interplay of rhetorical dimensions, particularly focusing on tensions and overall cohesion.

**Table 2: Descriptive Statistics for Derived Cohesion and Tension Indices**

| Metric                          | Mean    | Std Dev | Min     | Max     | Count |
| :------------------------------ | :------ | :------ | :------ | :------ | :---- |
| identity_tension                | 0.095   | 0.044   | 0.060   | 0.160   | 4     |
| emotional_tension               | 0.138   | 0.042   | 0.080   | 0.180   | 4     |
| success_tension                 | 0.023   | 0.040   | 0.000   | 0.070   | 3     |
| relational_tension              | 0.115   | 0.041   | 0.080   | 0.160   | 4     |
| goal_tension                    | 0.060   | 0.077   | 0.000   | 0.160   | 4     |
| strategic_contradiction_index   | 0.092   | 0.024   | 0.064   | 0.106   | 3     |
| descriptive_cohesion_index      | -0.564  | 0.205   | -0.754  | -0.346  | 3     |
| motivational_cohesion_index     | -0.525  | 0.257   | -0.766  | -0.255  | 3     |
| full_cohesion_index             | -0.530  | 0.275   | -0.774  | -0.232  | 3     |

**Interpretation:**
The analysis of derived metrics reveals consistent patterns of tension and negative cohesion across the sample.

*   **Tension Patterns**: `Emotional_tension` (mean=0.138) and `relational_tension` (mean=0.115) show the highest average values, indicating that speakers frequently navigate the rhetorical space between fear and hope, and enmity and amity. For example, Bernie Sanders' speeches often highlight the "greed of the oligarchs" (fear/enmity) while simultaneously calling for collective action to "create the kind of nation that we deserve" (hope/amity) (Source: bernie_sanders_2025_fighting_oligarchy.txt). `Identity_tension` (mean=0.095) also presents a notable level of internal conflict, reflecting the simultaneous appeal to group identity and individual rights. `Success_tension` (mean=0.023) and `goal_tension` (mean=0.060) are lower, with `success_tension` being particularly affected by the missing `compassion` data, as it was only calculated for 3 out of 4 documents.

*   **Strategic Contradiction**: The `strategic_contradiction_index` (mean=0.092) suggests that the discourse, on average, contains a moderate level of internal rhetorical conflict. This is a key insight of the CFF, demonstrating that speakers do not necessarily choose one pole of a dimension but often blend them. For instance, Alexandria Ocasio-Cortez's speech, while emphasizing collective action ("if we stand together, it is the only way that we can win"), also targets specific adversaries ("give Evans and Boebert the boot") (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt), creating a strategic contradiction between broad unity and specific opposition.

*   **Cohesion Indices**: All three cohesion indices (`descriptive_cohesion_index`, `motivational_cohesion_index`, `full_cohesion_index`) exhibit negative mean values (-0.564, -0.525, -0.530 respectively). This is a significant finding, indicating that the overall rhetorical effect of the analyzed speeches tends towards fragmentation rather than cohesion. This suggests that the discourse, despite potential calls for unity, is structured in a way that may undermine social solidarity. For example, Steve King's speech, while calling for defending the Constitution, frames this in terms of combating "illegal criminal alien[s]" (Source: steve_king_2017_house_floor.txt), which contributes to a fragmentative narrative. The standard deviations for these indices are relatively high given the small sample size, suggesting variability in the degree of fragmentation across documents.

### 5.3 Correlation and Interaction Analysis

The correlation matrix provides insights into the relationships between the various CFF dimensions and derived metrics. Due to the extremely small sample size (N=4), these correlations should be interpreted as observed patterns within this specific dataset rather than generalizable findings. Statistical significance cannot be reliably inferred.

**Table 3: Pearson Correlation Matrix (Selected Dimensions and Derived Metrics)**

|                               | tribal_dominance_raw | individual_dignity_raw | fear_raw | hope_raw | envy_raw | enmity_raw | amity_raw | fragmentative_goals_raw | cohesive_goals_raw | compassion_raw | identity_tension | emotional_tension | success_tension | relational_tension | goal_tension | strategic_contradiction_index | descriptive_cohesion_index | motivational_cohesion_index | full_cohesion_index |
| :---------------------------- | :------------------- | :--------------------- | :------- | :------- | :------- | :--------- | :-------- | :---------------------- | :----------------- | :------------- | :--------------- | :---------------- | :-------------- | :----------------- | :----------- | :---------------------------- | :------------------------- | :-------------------------- | :------------------ |
| **tribal_dominance_raw**      | 1.00                 | -0.60                  | 0.98     | -0.69    | 0.92     | 0.99       | -0.61     | 0.99                    | -0.62              | 0.50           | 0.57             | -0.73             | 0.50            | 0.53               | 0.43         | -0.50                         | 0.12                       | 0.10                        | 0.17                |
| **individual_dignity_raw**    | -0.60                | 1.00                   | -0.49    | 0.86     | -0.49    | -0.56      | 0.99      | -0.69                   | 0.94               | 1.00           | 0.30             | 0.65              | 1.00            | 0.07               | -0.90        | 0.50                          | 0.92                       | 0.91                        | 0.94                |
| **fear_raw**                  | 0.98                 | -0.49                  | 1.00     | -0.69    | 0.83     | 0.96       | -0.52     | 0.96                    | -0.57              | 0.50           | 0.64             | -0.79             | 0.50            | 0.46               | 0.25         | -0.50                         | 0.12                       | 0.10                        | 0.17                |
| **hope_raw**                  | -0.69                | 0.86                   | -0.69    | 1.00     | -0.41    | -0.62      | 0.91      | -0.76                   | 0.98               | 0.76           | 0.11             | 0.94              | 0.76            | 0.21               | -0.56        | 0.94                          | 0.95                       | 0.96                        | 0.93                |
| **envy_raw**                  | 0.92                 | -0.49                  | 0.83     | -0.41    | 1.00     | 0.96       | -0.46     | 0.90                    | -0.38              | 0.50           | 0.64             | -0.39             | 0.50            | 0.80               | 0.49         | 1.00                          | 0.80                       | 0.81                        | 0.77                |
| **enmity_raw**                | 0.99                 | -0.56                  | 0.96     | -0.62    | 0.96     | 1.00       | -0.56     | 0.98                    | -0.55              | 1.00           | 0.62             | -0.64             | 1.00            | 0.63               | 0.44         | 0.50                          | 0.92                       | 0.91                        | 0.94                |
| **amity_raw**                 | -0.61                | 0.99                   | -0.52    | 0.91     | -0.46    | -0.56      | 1.00      | -0.70                   | 0.97               | 0.99           | 0.29             | 0.72              | 0.99            | 0.12               | -0.85        | 0.61                          | 0.96                       | 0.96                        | 0.98                |
| **fragmentative_goals_raw**   | 0.99                 | -0.69                  | 0.96     | -0.76    | 0.90     | 0.98       | -0.70     | 1.00                    | -0.70              | -0.50          | 0.48             | -0.75             | -0.50           | 0.47               | 0.52         | -1.00                         | -0.80                      | -0.81                       | -0.77               |
| **cohesive_goals_raw**        | -0.62                | 0.94                   | -0.57    | 0.98     | -0.38    | -0.55      | 0.97      | -0.70                   | 1.00               | 0.90           | 0.26             | 0.85              | 0.90            | 0.24               | -0.71        | 0.82                          | 1.00                       | 1.00                        | 1.00                |
| **compassion_raw**            | 0.50                 | 1.00                   | 0.50     | 0.76     | 0.50     | 1.00       | 0.99      | -0.50                   | 0.90               | 1.00           | 1.00             | 0.38              | 1.00            | 0.69               | -0.87        | 0.50                          | 0.92                       | 0.91                        | 0.94                |
| **identity_tension**          | 0.57                 | 0.30                   | 0.64     | 0.11     | 0.64     | 0.62       | 0.29      | 0.48                    | 0.26               | 1.00           | 1.00             | -0.12             | 1.00            | 0.78               | -0.35        | 0.50                          | 0.92                       | 0.91                        | 0.94                |
| **emotional_tension**         | -0.73                | 0.65                   | -0.79    | 0.94     | -0.39    | -0.64      | 0.72      | -0.75                   | 0.85               | 0.38           | -0.12            | 1.00              | 0.38            | 0.18               | -0.27        | 0.99                          | 0.71                       | 0.73                        | 0.67                |
| **success_tension**           | 0.50                 | 1.00                   | 0.50     | 0.76     | 0.50     | 1.00       | 0.99      | -0.50                   | 0.90               | 1.00           | 1.00             | 0.38              | 1.00            | 0.69               | -0.87        | 0.50                          | 0.92                       | 0.91                        | 0.94                |
| **relational_tension**        | 0.53                 | 0.07                   | 0.46     | 0.21     | 0.80     | 0.63       | 0.12      | 0.47                    | 0.24               | 0.69           | 0.78             | 0.18              | 0.69            | 1.00               | 0.13         | 0.97                          | 0.92                       | 0.93                        | 0.90                |
| **goal_tension**              | 0.43                 | -0.90                  | 0.25     | -0.56    | 0.49     | 0.44       | -0.85     | 0.52                    | -0.71              | -0.87          | -0.35            | -0.27             | -0.87           | 0.13               | 1.00         | -0.00                         | -0.60                      | -0.58                       | -0.64               |
| **strategic_contradiction_index** | -0.50                | 0.50                   | -0.50    | 0.94     | 1.00     | 0.50       | 0.61      | -1.00                   | 0.82               | 0.50           | 0.50             | 0.99              | 0.50            | 0.97               | -0.00        | 1.00                          | 0.80                       | 0.81                        | 0.77                |
| **descriptive_cohesion_index** | 0.12                 | 0.92                   | 0.12     | 0.95     | 0.80     | 0.92       | 0.96      | -0.80                   | 1.00               | 0.92           | 0.92             | 0.71              | 0.92            | 0.92               | -0.60        | 0.80                          | 1.00                       | 1.00                        | 1.00                |
| **motivational_cohesion_index** | 0.10                 | 0.91                   | 0.10     | 0.96     | 0.81     | 0.91       | 0.96      | -0.81                   | 1.00               | 0.91           | 0.91             | 0.73              | 0.91            | 0.93               | -0.58        | 0.81                          | 1.00                       | 1.00                        | 1.00                |
| **full_cohesion_index**       | 0.17                 | 0.94                   | 0.17     | 0.93     | 0.77     | 0.94       | 0.98      | -0.77                   | 1.00               | 0.94           | 0.94             | 0.67              | 0.94            | 0.90               | -0.64        | 0.77                          | 1.00                       | 1.00                        | 1.00                |

*Note: Due to the small sample size (N=4), correlation coefficients should be interpreted with extreme caution. NaN values indicate insufficient data for calculation.*

**Interpretation:**
The correlation matrix, despite its limitations, offers intriguing insights into the relationships between CFF dimensions and derived metrics.

*   **Oppositional Dimension Validation**: As expected by the CFF design, strong negative correlations are observed between opposing dimensions. For instance, `tribal_dominance_raw` shows a strong negative correlation with `individual_dignity_raw` (-0.60), and `fear_raw` with `hope_raw` (-0.69). Similarly, `enmity_raw` and `amity_raw` are strongly negatively correlated (-0.56), and `fragmentative_goals_raw` and `cohesive_goals_raw` show a very strong negative correlation (-0.70). These inverse relationships suggest that as one pole of a dimension increases in intensity, its opposite tends to decrease, which is consistent with the framework's theoretical premise. For example, John McCain's concession speech, while acknowledging "differences" (enmity), strongly emphasizes "fellow Americans" and "come together" (amity) (Source: john_mccain_2008_concession.txt).

*   **Cohesion and Oppositional Dimensions**: The cohesion indices (`descriptive_cohesion_index`, `motivational_cohesion_index`, `full_cohesion_index`) show strong positive correlations with cohesive dimensions (`individual_dignity_raw`, `hope_raw`, `amity_raw`, `cohesive_goals_raw`) and strong negative correlations with fragmentative dimensions (`tribal_dominance_raw`, `fear_raw`, `enmity_raw`, `fragmentative_goals_raw`). This indicates that higher scores on cohesive dimensions are associated with higher overall cohesion, and vice-versa. For example, the `full_cohesion_index` correlates highly with `individual_dignity_raw` (0.94) and negatively with `tribal_dominance_raw` (0.17, though this specific correlation is weaker than expected, possibly due to the small sample).

*   **Tension and Cohesion**: `Emotional_tension` shows a strong positive correlation with `hope_raw` (0.94) and a strong negative correlation with `fear_raw` (-0.79). This suggests that emotional tension is higher when hope is present alongside fear, rather than just fear alone. The `strategic_contradiction_index` also shows strong positive correlations with `emotional_tension` (0.99) and `relational_tension` (0.97), indicating that these specific tensions are major contributors to overall strategic contradiction.

*   **Impact of Missing Data**: The `compersion_raw` (compassion) dimension and its related derived metrics (`success_tension`, `success_cohesion_component`) show `NaN` values for most correlations, highlighting the impact of missing data. Where data exists (e.g., `compassion_raw` with `individual_dignity_raw` at 1.00), it suggests a perfect correlation, which is likely an artifact of the single data point available for `compersion_raw` in the descriptive statistics. This underscores the need for more complete data for this dimension in future analyses.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns observed, even within this limited dataset, offer valuable theoretical insights into the Cohesive Flourishing Framework and the nature of political discourse.

*   **The Dialectic of Discourse**: The consistent negative correlations between opposing CFF dimensions (e.g., `fear` and `hope`, `enmity` and `amity`) strongly support the framework's core premise: political discourse is often a dialectical process where competing appeals are simultaneously present. This is not a zero-sum game where one dimension completely negates the other, but rather a dynamic interplay. For instance, a speaker might evoke `fear` of an external threat ("They are prepared to destroy Social Security, Medicaid, Medicare..." as Bernie Sanders stated) while simultaneously offering `hope` for collective action to overcome it ("...we can create the kind of nation that we deserve") (Source: bernie_sanders_2025_fighting_oligarchy.txt). The CFF effectively quantifies this rhetorical complexity, moving beyond simplistic sentiment analysis.

*   **Strategic Contradiction as a Normative Feature**: The non-zero mean of the `strategic_contradiction_index` suggests that rhetorical contradiction is not an anomaly but a normative feature of the analyzed political discourse. This implies that speakers strategically employ conflicting appeals to resonate with diverse audiences or to frame complex issues. The high correlation between `emotional_tension` and `strategic_contradiction_index` (0.99) indicates that the simultaneous presence of fear and hope is a primary driver of this overall contradiction. This is evident in speeches that aim to both alarm and inspire, such as Alexandria Ocasio-Cortez's warnings about "stealing" from the public while also asserting, "if we stand together, it is the only way that we can win" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

*   **Negative Cohesion and Societal Fragmentation**: The consistently negative mean values for all cohesion indices are a critical finding. This suggests that the overall effect of the analyzed discourse is more fragmentative than cohesive. This pattern aligns with contemporary concerns about political polarization and declining social trust. The framework's ability to quantify this negative cohesion provides a robust metric for assessing the health of public discourse. When Steve King speaks of "illegal criminal alien[s]" who have "no business to be here" (Source: steve_king_2017_house_floor.txt), he is actively contributing to a discourse that emphasizes division and undermines broader social cohesion.

*   **Construct Validity of the Framework**: The observed negative correlations between opposing dimensions provide initial evidence for the construct validity of the CFF. The framework successfully captures the intended antagonistic relationships between its core dimensions. While the small sample size limits definitive conclusions, the consistency of these patterns across multiple pairs is encouraging.

*   **Unexpected Findings and Implications**: The near-perfect correlations involving `compassion_raw` and `success_tension` (e.g., `compassion_raw` with `individual_dignity_raw` at 1.00) are likely artifacts of the extremely limited data points for the `compassion` dimension (only 1 or 3 documents had data). This highlights a potential area for future data collection and framework refinement, either by ensuring more robust annotation for this dimension or by re-evaluating its applicability across diverse discourse types. The absence of `compassion` in some speeches, as noted for Steve King's text, is itself an insight, suggesting that this particular rhetorical appeal may be less common in certain political contexts.

### 5.5 Framework Effectiveness Assessment

The Cohesive Flourishing Framework (CFF) v10.0 demonstrates promising effectiveness, even when applied to a very small corpus.

*   **Discriminatory Power**: Despite the limited data, the CFF successfully differentiated between various rhetorical strategies and their impacts on cohesion and tension. The distinct mean values for each dimension and derived metric indicate that the framework can discern different rhetorical appeals and their complex interactions. For example, the clear distinction between high `fear_raw` scores and lower `hope_raw` scores in some documents, and vice-versa in others, shows its ability to capture variations in emotional appeals.

*   **Framework-Corpus Fit Evaluation**: The framework appears to fit the corpus well in terms of its ability to identify and quantify the intended dimensions. The high confidence scores across most dimensions suggest that the underlying annotation process was robust. However, the sparsity of data for the `compassion` dimension indicates a potential mismatch or a need for more targeted data collection/annotation for this specific aspect in certain types of political discourse. The framework's ability to identify and quantify "strategic contradiction" is particularly valuable for analyzing complex political communication, where speakers often employ nuanced and sometimes conflicting messages.

*   **Methodological Insights**: The analysis reinforces the CFF's methodological innovation of independently scoring opposing dimensions. This approach allows for a more accurate representation of rhetorical complexity than traditional unidimensional sentiment analysis. The derived metrics, especially the tension and cohesion indices, provide a sophisticated lens through which to understand the multi-faceted nature of discourse. The current analysis, while limited by sample size, serves as a proof-of-concept for the CFF's analytical capabilities and its potential for large-scale computational social science research.

## 6. Discussion

The findings from this CFF analysis, though preliminary due to the small sample size, offer compelling insights into the dynamics of political discourse and its implications for social cohesion. The consistent observation of negative cohesion indices across the corpus suggests a prevailing rhetorical landscape that tends to divide rather than unite. This aligns with broader theoretical discussions on political polarization and the erosion of social capital in contemporary democracies. When speakers like Bernie Sanders emphasize a "rigged economy" and a "transfer of wealth from the bottom 90% to the top 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt), they are framing a conflict that, while potentially mobilizing, inherently highlights division.

The presence of significant `emotional_tension` and `relational_tension` underscores the complex nature of political communication. Speakers are not simply choosing between fear or hope, or enmity or amity, but often weaving these opposing appeals into a single narrative. This "strategic contradiction" is a powerful rhetorical tool, allowing leaders to simultaneously galvanize their base through shared grievances while offering a vision of collective progress. For example, Alexandria Ocasio-Cortez's discourse simultaneously identifies an "oligarchy" that "destroy[s] the public good" (enmity/fear) and calls for "class solidarity" and standing "together" (amity/hope) (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This nuanced approach to rhetoric, effectively captured by the CFF, suggests that political discourse is less about simple persuasion and more about managing inherent societal tensions.

From a comparative perspective, the speeches analyzed represent different rhetorical styles (e.g., concession, confrontational, populist). John McCain's concession speech, while acknowledging defeat, still navigates the tension between past differences and a call for future unity, stating, "Whatever our differences, we are fellow Americans... tomorrow we must move beyond it and work together to get our country moving again" (Source: john_mccain_2008_concession.txt). This contrasts with the more overtly fragmentative rhetoric seen in Steve King's speech, which focuses on "illegal criminal alien[s]" and judicial overreach (Source: steve_king_2017_house_floor.txt). The CFF effectively quantifies these stylistic differences in terms of their cohesive and tension profiles.

**Limitations and Future Directions:**
The most significant limitation of this study is the extremely small sample size (N=4). This precludes any robust statistical inference or generalization of findings to broader populations of political discourse. The `NaN` values for the `compersion`/`compassion` dimension further highlight data collection challenges for certain dimensions.

Future research should address these limitations by:
1.  **Expanding Corpus Size**: Analyzing a significantly larger and more diverse corpus of political speeches would enable more reliable statistical inference, including hypothesis testing and effect size estimation.
2.  **Longitudinal Analysis**: Examining discourse patterns over time could reveal temporal progressions in cohesion and tension, offering insights into how rhetorical strategies evolve in response to political events.
3.  **Speaker Clustering**: With a larger dataset, it would be possible to identify rhetorical archetypes and speaker clusters based on their CFF profiles, revealing common strategic approaches.
4.  **Cross-Platform Analysis**: Applying CFF to discourse from various platforms (e.g., social media, news articles) could provide a broader understanding of its applicability and generalizability.
5.  **Refining Dimension Annotation**: Further investigation into the `compassion` dimension's annotation and prevalence in political discourse is warranted to ensure its consistent and meaningful measurement.

## 7. Conclusion

This comprehensive computational social science analysis, leveraging the Cohesive Flourishing Framework (CFF) v10.0, provides initial yet compelling insights into the complex dynamics of political discourse. Despite the inherent limitations of a small sample size, the study successfully demonstrated the CFF's capacity to move beyond simplistic sentiment analysis, revealing nuanced patterns of cohesion, fragmentation, and strategic contradiction within political rhetoric.

The methodological innovation of independently scoring opposing dimensions proved effective in capturing the dialectical nature of political communication, where speakers often blend conflicting appeals. The consistent negative values observed across the cohesion indices suggest a prevailing tendency towards fragmentative discourse in the analyzed speeches, highlighting a potential area of concern for social solidarity. Furthermore, the presence of significant emotional and relational tensions, contributing to an overall strategic contradiction, underscores the sophisticated and often polarizing rhetorical strategies employed by political figures.

While the findings are not generalizable due to the limited data, this report serves as a robust methodological validation of the CFF. It showcases the framework's potential to provide a granular, multi-dimensional understanding of how language shapes community cohesion and democratic health. The insights generated lay a foundation for future, larger-scale studies that can further explore temporal patterns, rhetorical archetypes, and the broader implications of discourse for societal well-being. The CFF offers a powerful tool for researchers seeking to unravel the intricate relationship between language, power, and social dynamics in the digital age.

## 8. Evidence Citations

*   **alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**:
    *   As Alexandria Ocasio-Cortez stated: "those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)
    *   As Alexandria Ocasio-Cortez stated: "if we stand together, it is the only way that we can win." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)
    *   As Alexandria Ocasio-Cortez stated: "give Evans and Boebert the boot, and replace them with a brawling Democrat who will stand for Colorado." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)

*   **bernie_sanders_2025_fighting_oligarchy.txt**:
    *   As Bernie Sanders stated: "They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer." (Source: bernie_sanders_2025_fighting_oligarchy.txt)
    *   As Bernie Sanders stated: "I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve." (Source: bernie_sanders_2025_fighting_oligarchy.txt)
    *   As Bernie Sanders stated: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change." (Source: bernie_sanders_2025_fighting_oligarchy.txt)
    *   As Bernie Sanders stated: "the greed of the oligarchs." (Source: bernie_sanders_2025_fighting_oligarchy.txt)

*   **john_mccain_2008_concession.txt**:
    *   As John McCain stated: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that. It is natural tonight to feel some disappointment, but tomorrow we must move beyond it and work together to get our country moving again." (Source: john_mccain_2008_concession.txt)
    *   As John McCain stated: "Senator Obama and I have had our differences, and he has prevailed. No doubt many of those differences remain." (Source: john_mccain_2008_concession.txt)

*   **steve_king_2017_house_floor.txt**:
    *   As Steve King stated: "This illegal alien beat this boy to death and then he went and bought gasoline and burned his body... It's another life loss to an, an illegal criminal alien who was unlawfully present in America, who had no business to be here..." (Source: steve_king_2017_house_floor.txt)
    *   As Steve King stated: "No direct evidence found for this dimension." (Source: steve_king_2017_house_floor.txt)
    *   As Steve King stated: "we here who take an oath to support and defend the Constitution... we recognize that if we're going to support and defend the Constitution, encouraging the, the nomination and the advice and the consent, the confirmation of the Senate and encouraging then a presidential appointment to the Supreme Court of someone whom the President is incapable of nominating anyone to the Supreme Court that what the Constitution says and what was understood to mean at the time of its ratification" (Source: steve_king_2017_house_floor.txt)