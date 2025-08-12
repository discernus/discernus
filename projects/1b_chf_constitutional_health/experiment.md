---
version: "7.0"
name: "presidential_sotu_constitutional_health_trends"
description: |
  This experiment tests whether the Salience-Weighted Constitutional Direction Index 
  of presidential State of the Union rhetoric has declined significantly since 1992. 
  Using the Constitutional Health Framework v7.3, we analyze 37+ SOTU addresses 
  from Clinton (1993-2000) through Biden (2021-2024) to determine if there is a 
  statistically significant downward trend in constitutional health scores over time.

hypothesis: |
  The Salience-Weighted Constitutional Direction Index of presidential State of 
  the Union addresses has declined significantly since 1992, indicating a 
  systematic decrease in constitutional health rhetoric over the past three decades.

framework: "../../frameworks/reference/core/chf_v7.3.md"
framework_version: "v7.3"
corpus_path: "./corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
analysis_variant: "default"

# Declarative statistical analyses to be performed by the MathToolkit.
statistical_analyses:
  - type: "linear_regression"
    dependent_variable: "Salience_Weighted_Constitutional_Direction_Index"
    independent_variables: ["year"]
  - type: "descriptive_stats"
    columns:
      - "Salience_Weighted_Constitutional_Direction_Index"
      - "year"
  - type: "correlation_matrix"
    columns:
      - "Procedural_Health_Score"
      - "Institutional_Health_Score"
      - "Systemic_Health_Score"
      - "Procedural_Pathology_Score"
      - "Institutional_Pathology_Score"
      - "Systemic_Pathology_Score"

# Enhanced v3.0 Analysis Configuration
analysis:
  evaluations_per_document: 3
  statistical_confidence: 0.95
  variance_threshold: 0.15

# Comprehensive Statistical Validation  
validation:
  required_tests: ["temporal_trend_analysis", "constitutional_health_correlation_matrix", "cdi_reliability", "dimensional_relationship_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true
  statistical_requirements: "Corpus contains 37+ SOTU addresses spanning 1993-2024, providing sufficient data for robust time series analysis and regression testing."

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "temporal_trend_analysis"
    - "constitutional_health_patterns"
    - "procedural_dimension_analysis"
    - "institutional_dimension_analysis"
    - "systemic_dimension_analysis"
    - "dimensional_relationship_analysis"
    - "statistical_significance_testing"
    - "effect_size_analysis"
    - "findings_discussion"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Research Hypotheses
hypotheses:
  H1_Temporal_Decline: "Test whether the Salience-Weighted Constitutional Direction Index has declined significantly since 1992"
  H2_Trend_Significance: "Test whether any observed decline is statistically significant (p < 0.05)"
  H3_Effect_Size: "Test the magnitude of any decline (R² for time explaining variance in scores)"
  H4_Dimensional_Contributors: "Test which constitutional health dimensions contribute most to any observed decline"
  H5_Platform_Validation: "Test whether the JSON synthesis architecture successfully processes time series analysis with constitutional health metrics"

# Required Workflow Steps
workflow:
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - raw_analysis_log

  - agent: IntelligentExtractorAgent
    inputs:
      - raw_analysis_log
      - framework
    outputs:
      - structured_data

  - agent: ProductionThinSynthesisPipeline
    inputs:
      - structured_data
      - experiment
      - framework
    outputs:
      - final_report.md
      - statistical_results.json
---

# Constitutional Health Time Series Analysis: Presidential SOTU Rhetoric Trends Since 1992

## Overview

This experiment tests whether the Salience-Weighted Constitutional Direction Index of presidential State of the Union rhetoric has declined significantly since 1992. Using the Constitutional Health Framework v7.3, we analyze 37+ SOTU addresses from Clinton (1993-2000) through Biden (2021-2024) to determine if there is a statistically significant downward trend in constitutional health scores over time. The large corpus size and consistent speech format provide robust data for time series analysis and regression testing.

## Research Questions

1. Has the Salience-Weighted Constitutional Direction Index declined significantly since 1992?
2. What is the magnitude and statistical significance of any observed decline?
3. Which constitutional health dimensions contribute most to any observed decline?
4. How do the trends vary across different presidential administrations?
5. What are the implications of any decline for constitutional discourse quality?

## Methodology

### Framework
**Constitutional Health Framework v7.3** provides:
- 6-dimensional constitutional health analysis (3 health vs 3 pathology dimensions)
- Salience-Weighted Constitutional Direction Index for overall health measurement
- JSON-first architecture with enhanced synthesis integration
- Procedural, institutional, and systemic health mathematics

### Time Series Corpus Design
37+ State of the Union addresses spanning 1993-2024:

**Clinton Administration (1993-2000)**:
- 8 SOTU addresses: 1993-2000
- **Context**: Post-Cold War institutional governance
- **Focus**: Economic prosperity, social programs, international cooperation

**Bush Administration (2001-2008)**:
- 8 SOTU addresses: 2001-2008
- **Context**: Post-9/11 security focus, Iraq/Afghanistan wars
- **Focus**: National security, counterterrorism, economic policy

**Obama Administration (2009-2016)**:
- 8 SOTU addresses: 2009-2016
- **Context**: Financial crisis recovery, healthcare reform
- **Focus**: Economic recovery, healthcare, climate change, immigration

**Trump Administration (2017-2020)**:
- 4 SOTU addresses: 2017-2020
- **Context**: Populist anti-establishment rhetoric
- **Focus**: Immigration, trade, "America First" policies

**Biden Administration (2021-2024)**:
- 4 SOTU addresses: 2021-2024
- **Context**: Post-Trump institutional restoration
- **Focus**: Infrastructure, climate action, democratic institutions

### Enhanced Statistical Analysis
- **Time Series Regression**: Linear regression analysis of Constitutional Direction Index over time
- **Trend Significance Testing**: Statistical significance of any observed decline (p < 0.05)
- **Effect Size Analysis**: R² for time explaining variance in constitutional health scores
- **Administration Comparison**: Constitutional health patterns across different presidencies
- **Dimensional Contribution Analysis**: Which health dimensions contribute most to any decline
- **Reliability Assessment**: Consistency of constitutional health measurement across time

### Expected Outcomes
1. **Temporal Trend Analysis**: Quantified decline (or lack thereof) in constitutional health since 1992
2. **Statistical Significance**: P-value and confidence intervals for any observed trend
3. **Effect Size Measurement**: R² indicating how much variance time explains
4. **Administration Patterns**: Constitutional health signatures of different presidencies
5. **Dimensional Insights**: Which constitutional health aspects show strongest trends

## Significance

This experiment represents the first computational analysis of constitutional health trends in presidential State of the Union rhetoric over three decades. The time series analysis will produce empirical findings on:

1. **Constitutional health trajectory**: Whether presidential rhetoric has systematically declined in constitutional health
2. **Administration effects**: Whether different presidencies show distinct constitutional health patterns
3. **Temporal significance**: Whether any observed changes are statistically meaningful
4. **Democratic discourse quality**: Whether constitutional health correlates with democratic institutional stability

The large corpus size and consistent speech format provide robust data for time series analysis while testing the platform's ability to detect meaningful trends in constitutional discourse health over time.