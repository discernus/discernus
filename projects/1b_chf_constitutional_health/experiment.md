# Constitutional Health Administration Analysis: Presidential Congressional Address Comparison Across Presidencies

## Abstract

This experiment tests whether the constitutional_health_index of presidential addresses to Congress varies significantly across different presidential administrations. Using the Constitutional Health Framework v10.0, we analyze 48 presidential addresses to Congress from Bush H.W. (1992) through Biden (2021-2025), including State of the Union addresses, inaugural addresses, and joint session speeches, to determine if there are statistically significant differences in constitutional health scores between administrations. The large corpus size and consistent speech format provide robust data for administration comparison and ANOVA testing.

## Research Questions

1. **What patterns emerge in constitutional health across presidential rhetoric?** *(Open-ended pattern discovery)*
2. **Which constitutional dimensions show the most variation and why?** *(Dimensional exploration)*
3. **How do different speech contexts (SOTU vs. Inaugural vs. Joint Session) affect constitutional health?** *(Context effects analysis)*
4. **What rhetorical strategies and linguistic patterns correlate with higher/lower constitutional health scores?** *(Mechanism discovery)*
5. **Are there unexpected constitutional health patterns, outliers, or anomalies that warrant further investigation?** *(Anomaly detection)*

## Hypotheses

### Primary Hypothesis
**H₀**: μ_bush_hw = μ_clinton = μ_bush_w = μ_obama = μ_trump = μ_biden (All administrations have equal constitutional health scores)
**H₁**: At least one administration differs significantly from the others in constitutional health scores

**Test**: One-way ANOVA across 6 presidential administrations (including Bush H.W. 1992 baseline)
**Threshold**: p < 0.05, F > F_critical

### Secondary Hypotheses
**H₂**: μ_trump ≠ μ_bush_w (Trump differs significantly from Republican peer Bush W.)
**H₃**: μ_trump ≠ μ_clinton, μ_obama (Trump differs significantly from Democratic administrations)
**H₄**: μ_biden ≠ μ_clinton, μ_obama (Biden differs significantly from Democratic peers Clinton and Obama)
**H₅**: |μ_biden - μ_trump| > |μ_clinton - μ_bush_w|, |μ_obama - μ_bush_w| (Biden-Trump difference exceeds other cross-party differences)

### Outlier and Response Hypotheses
**H₆**: Trump shows significantly higher variance in constitutional health scores than other administrations (Levene's test)
**H₇**: Biden's constitutional health profile is more similar to Trump than to Clinton/Obama (cluster analysis or distance metrics)

### Statistical Testing Strategy
- **Primary Analysis**: One-way ANOVA comparing Constitutional Direction Index across administrations
- **Post-hoc Testing**: Tukey HSD for pairwise administration comparisons (H₂-H₅)
- **Variance Testing**: Levene's test for homogeneity of variance (H₆ - Trump outlier hypothesis)
- **Distance Analysis**: Euclidean distance between administration profiles in 6-dimensional space (H₇)
- **Cluster Analysis**: Hierarchical clustering to test Biden-Trump similarity vs. Biden-Democrat similarity
- **Effect Size**: η² (eta-squared) for administration effects
- **Reliability**: Cronbach's alpha for each dimension across administrations

## Expected Outcomes

This experiment will produce empirical findings on constitutional health differences across administrations, administration effects, statistical significance, and democratic discourse quality. The analysis will include one-way ANOVA, post-hoc testing, effect size measurement, administration comparison, and dimensional contribution analysis.

## Methodology

### Framework
**Constitutional Health Framework v10.0** provides:
- 6-dimensional constitutional health analysis (3 health vs 3 pathology dimensions)
- constitutional_health_index for overall health measurement
- JSON-first architecture with enhanced synthesis integration
- Procedural, institutional, and systemic health mathematics
- Sequential analysis variants (sequential_*) for higher fidelity results as recommended in framework documentation

### Time Series Corpus Design
**Document Summary Table:**
| Administration | SOTU | Inaugural | Joint Session | Other | Total |
|---|---|---|---|---|---|
| Bush H.W. (baseline) | 1 | 0 | 0 | 0 | 1 |
| Clinton | 9 | 2 | 1 | 0 | 12 |
| Bush W. | 8 | 2 | 1 | 0 | 11 |
| Obama | 9 | 2 | 1 | 0 | 12 |
| Trump | 4 | 2 | 1 | 0 | 7 |
| Biden | 4 | 1 | 1 | 0 | 6 |
| **Total** | **35** | **9** | **4** | **0** | **48** |

48 presidential addresses to Congress spanning 1992-2025:

**Bush H.W. Administration (1992) - Cold War Transition Baseline**:
- 1 SOTU address: 1992
- **Context**: End of Cold War, institutional transition period
- **Focus**: Post-Soviet global order, domestic economic concerns

**Clinton Administration (1993-2000)**:
- 9 SOTU addresses, 2 inaugural addresses, 1 joint session address
- **Context**: Post-Cold War institutional governance
- **Focus**: Economic prosperity, social programs, international cooperation

**Bush W. Administration (2001-2008)**:
- 8 SOTU addresses, 2 inaugural addresses, 1 joint session address
- **Context**: Post-9/11 security focus, Iraq/Afghanistan wars
- **Focus**: National security, counterterrorism, economic policy

**Obama Administration (2009-2016)**:
- 9 SOTU addresses, 2 inaugural addresses, 1 joint session address
- **Context**: Financial crisis recovery, healthcare reform
- **Focus**: Economic recovery, healthcare, climate change, immigration

**Trump Administration (2017-2020)**:
- 4 SOTU addresses, 2 inaugural addresses, 1 joint session address
- **Context**: Populist anti-establishment rhetoric
- **Focus**: Immigration, trade, "America First" policies

**Biden Administration (2021-2024)**:
- 4 SOTU addresses, 1 inaugural address, 1 joint session address
- **Context**: Post-Trump institutional restoration
- **Focus**: Infrastructure, climate action, democratic institutions

### Enhanced Statistical Analysis
- **Administration Comparison**: One-way ANOVA analysis of constitutional_health_index across administrations
- **Statistical Significance Testing**: F-test for administration effects (p < 0.05)
- **Effect Size Analysis**: η² (eta-squared) for administration effects on constitutional health
- **Post-hoc Testing**: Tukey HSD for pairwise administration comparisons
- **Dimensional Contribution Analysis**: Which health dimensions show strongest administration differences
- **Reliability Assessment**: Cronbach's alpha for measurement consistency across administrations

### Expected Outcomes
1. **Administration Comparison Analysis**: Quantified differences in constitutional health across 5 presidential administrations
2. **Statistical Significance**: F-statistic, p-value, and effect size (η²) for administration effects
3. **Pairwise Comparisons**: Tukey HSD results showing which administrations differ significantly
4. **Dimensional Analysis**: Which constitutional health dimensions show strongest administration differences
5. **Reliability Assessment**: Cronbach's alpha for measurement consistency across administrations

## Significance

This experiment represents the first computational analysis of constitutional health differences across presidential administrations using comprehensive presidential addresses to Congress. The administration comparison analysis will produce empirical findings on:

1. **Administration effects**: Whether different presidencies show distinct constitutional health patterns
2. **Statistical significance**: Whether observed differences between administrations are statistically meaningful
3. **Effect magnitude**: How large the differences are between administrations
4. **Democratic discourse quality**: Whether constitutional health varies systematically across different governance approaches

The large corpus size (48 documents) and diverse speech formats (SOTU, inaugural, joint session) provide robust data for administration comparison while testing the platform's ability to detect meaningful differences in constitutional discourse health across different presidencies and speech contexts.

---

# --- Start of Machine-Readable Appendix ---

metadata:
  experiment_name: "presidential_sotu_constitutional_health_trends"
  author: "Discernus Research Team"
  spec_version: "10.0"

components:
  framework: "chf_v10.md"
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---