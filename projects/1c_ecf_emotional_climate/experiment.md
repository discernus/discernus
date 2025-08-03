---
version: "7.0"
name: "emotional_climate_factorial_analysis"
description: |
  This experiment analyzes emotional climate patterns in political discourse 
  using the Emotional Climate Framework v7.0. The corpus employs a 2×3 factorial 
  design examining Ideology (Conservative/Progressive) × Era (Civil Rights/
  Institutional/Populist) spanning 60 years (1963-2025). The analysis will 
  measure emotional climate dimensions across experimental factors to identify 
  any statistical patterns, relationships, or interactions present in the data.

hypothesis: |
  Emotional climate dimensions will be analyzed across political eras and 
  ideological affiliations to test for statistical differences. The analysis 
  will examine whether temporal factors, ideological factors, or their interaction 
  account for variance in fear/hope, enmity/amity, and envy/compersion patterns. 
  Statistical tests will determine if significant relationships exist between 
  experimental factors and emotional climate dimensions.

framework: "../../frameworks/reference/core/ecf_v7.0.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
analysis_variant: "default"

# Enhanced v3.0 Analysis Configuration
analysis:
  evaluations_per_document: 3
  statistical_confidence: 0.95
  variance_threshold: 0.15

# Comprehensive Statistical Validation  
validation:
  required_tests: ["two_way_anova_ideology_era", "emotional_climate_correlation_matrix", "climate_axis_reliability", "dimensional_trajectory_analysis", "factor_clustering_analysis", "climate_pattern_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "emotional_climate_patterns"
    - "ideological_factor_analysis"
    - "fear_hope_axis_analysis"
    - "enmity_amity_axis_analysis"
    - "envy_compersion_axis_analysis"
    - "dimensional_relationship_analysis"
    - "temporal_pattern_analysis"
    - "factorial_design_results"
    - "findings_discussion"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Multi-Hypothesis Framework
hypotheses:
  H1_Temporal: "Test whether emotional climate dimensions differ significantly across political eras"
  H2_Ideological: "Test whether emotional climate dimensions differ significantly between ideological groups"
  H3_Interaction: "Test whether ideology×era interaction effects exist for emotional climate patterns"
  H4_Axis_Relationships: "Test whether the three emotional axes show distinct statistical patterns across experimental factors"
  H5_Temporal_Patterns: "Test whether emotional climate dimensions show systematic patterns across time periods"
  H6_Platform_Validation: "Test whether the JSON synthesis architecture successfully processes factorial design with 6-dimensional analysis"

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

# Emotional Climate Factorial Analysis: Psychological Atmosphere Patterns Across American Political Eras and Ideological Lines

## Overview

This experiment analyzes emotional climate patterns in political discourse using the Emotional Climate Framework v6.0. The analysis employs a 2×3 factorial design examining ideology and era factors spanning 60 years of American political discourse (1963-2025).

## Research Questions

1. What patterns exist in emotional climate dimensions across political eras?
2. What relationships exist between ideological affiliation and emotional climate dimensions?
3. How do emotional climate patterns vary across the interaction of ideology and era?
4. What statistical relationships exist between experimental factors and emotional atmosphere measures?

## Methodology

### Framework
**Emotional Climate Framework v6.0** provides:
- 6-dimensional emotional climate analysis across 3 axes (fear/hope, enmity/amity, envy/compersion)
- Emotional atmosphere measurement independent of rhetorical strategy
- JSON-first architecture with enhanced synthesis integration
- Psychological environment quantification for audience response prediction

### 2×3 Factorial Corpus Design
8 political speeches creating a balanced Ideology × Era experimental matrix:

**Civil Rights Era (1963)**:
- **Progressive**: John Lewis - March on Washington speech

**Institutional Era (2008-2020)**:
- **Conservative**: John McCain - 2008 concession speech
- **Conservative**: Mitt Romney - 2020 impeachment speech  
- **Progressive**: Cory Booker - 2018 First Step Act speech

**Populist Era (2022-2025)**:
- **Progressive**: Bernie Sanders - 2025 oligarchy speech
- **Progressive**: Alexandria Ocasio-Cortez - 2025 oligarchy speech
- **Conservative**: JD Vance - 2022 NatCon conference speech
- **Conservative**: Steve King - 2017 House floor speech

**Factorial Balance**: 4 Progressive vs 4 Conservative speakers across 3 eras, enabling sophisticated emotional climate interaction analysis.

### Enhanced Statistical Analysis
- **Two-way ANOVA**: Ideology × Era main effects and interaction analysis for emotional climate
- **Multi-evaluation reliability**: 3 independent assessments per document (N=24 total evaluations)
- **Emotional climate clustering**: Emotional atmosphere profile similarities within/across ideologies
- **Emotional axis trajectory analysis**: How fear/hope, enmity/amity, envy/compersion evolve over time
- **Climate polarization analysis**: Emotional distance patterns by ideology and era
- **Cross-axis correlation analysis**: Relationships between different emotional dimensions

### Expected Outcomes
1. **Statistical Analysis Results**: Quantified patterns in emotional climate dimensions across experimental factors
2. **Pattern Analysis**: Statistical tests for emotional climate patterns across time and ideology
3. **Axis Relationship Analysis**: Relationships between fear/hope, enmity/amity, and envy/compersion dimensions
4. **Interaction Effect Analysis**: Statistical tests for interaction patterns between ideology and era
5. **Factorial Design Validation**: Technical validation of emotional climate analysis capabilities

## Significance

This experiment represents the first computational analysis of emotional climate patterns using factorial experimental design in American political discourse. The 2×3 factorial structure will produce empirical findings on:

1. **Temporal emotional climate effects**: Whether emotional atmosphere shows systematic changes across political eras
2. **Ideological emotional signatures**: Whether emotional climate dimensions differentiate conservative and progressive speakers  
3. **Emotional climate interactions**: Whether ideology and era interact to produce unique emotional atmosphere patterns
4. **Democratic discourse psychology**: Whether emotional climate correlates with political stability and democratic health

The factorial design provides comprehensive validation of emotional climate analysis while testing the platform's ability to detect complex psychological relationships in political discourse across six decades of American political development. This analysis will reveal the emotional foundations underlying political communication patterns and their evolution over time.