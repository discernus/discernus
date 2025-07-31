---
name: "constitutional_health_factorial_analysis"
description: |
  This experiment analyzes constitutional health patterns across American political 
  discourse using the Constitutional Health Framework v6.0. The corpus employs a 
  2×3 factorial design examining Ideology (Conservative/Progressive) × Era 
  (Civil Rights/Institutional/Populist) spanning 60 years (1963-2025). The analysis 
  will measure constitutional health dimensions across experimental factors to 
  identify any statistical patterns, relationships, or interactions present in 
  the data.

hypothesis: |
  Constitutional health dimensions will be analyzed across political eras and 
  ideological affiliations to test for statistical differences. The analysis will 
  examine whether temporal factors, ideological factors, or their interaction 
  account for variance in constitutional health patterns. Statistical tests will 
  determine if significant relationships exist between experimental factors and 
  Constitutional Direction Index scores.

framework: "../../frameworks/reference/core/chf_v6.0.md"
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
  required_tests: ["two_way_anova_ideology_era", "constitutional_health_correlation_matrix", "cdi_reliability", "dimensional_relationship_analysis", "factor_clustering_analysis", "temporal_pattern_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "constitutional_health_patterns"
    - "ideological_factor_analysis"
    - "procedural_dimension_analysis"
    - "institutional_dimension_analysis"
    - "systemic_dimension_analysis"
    - "dimensional_relationship_analysis"
    - "factorial_design_results"
    - "statistical_methodology"
    - "findings_discussion"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Multi-Hypothesis Framework
hypotheses:
  H1_Temporal: "Test whether constitutional health dimensions differ significantly across political eras"
  H2_Ideological: "Test whether constitutional health dimensions differ significantly between ideological groups"
  H3_Interaction: "Test whether ideology×era interaction effects exist for constitutional health patterns"
  H4_Index_Relationships: "Test whether Constitutional Direction Index scores correlate with experimental factors"
  H5_Dimensional_Structure: "Test whether health and pathology dimensions show inverse relationships"
  H6_Platform_Validation: "Test whether the JSON synthesis architecture successfully processes factorial design with 6-dimensional analysis"

# Required Workflow Steps
workflow:
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - analysis_results

  - agent: ProductionThinSynthesisPipeline
    inputs:
      - analysis_results
      - experiment
      - framework
    outputs:
      - final_report.md
      - statistical_results.json
---

# Constitutional Health Factorial Analysis: Patterns Across American Political Eras and Ideological Lines

## Overview

This experiment analyzes constitutional health patterns across American political discourse using the Constitutional Health Framework v6.0. The analysis employs a 2×3 factorial design examining ideology and era factors spanning 60 years of American political discourse (1963-2025).

## Research Questions

1. What patterns exist in constitutional health dimensions across political eras?
2. What relationships exist between ideological affiliation and constitutional health dimensions?
3. How do constitutional health patterns vary across the interaction of ideology and era?
4. What statistical relationships exist between experimental factors and constitutional health measures?

## Methodology

### Framework
**Constitutional Health Framework v6.0** provides:
- 6-dimensional constitutional health analysis (3 health vs 3 pathology dimensions)
- Constitutional Direction Index (CDI) for overall health measurement
- JSON-first architecture with enhanced synthesis integration
- Procedural, institutional, and systemic health mathematics

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

**Factorial Balance**: 4 Progressive vs 4 Conservative speakers across 3 eras, enabling sophisticated constitutional health interaction analysis.

### Enhanced Statistical Analysis
- **Two-way ANOVA**: Ideology × Era main effects and interaction analysis for constitutional health
- **Multi-evaluation reliability**: 3 independent assessments per document (N=24 total evaluations)
- **Constitutional health clustering**: Health profile similarities within/across ideologies
- **Health vs. pathology trajectory analysis**: How constitutional discourse health evolves over time
- **CDI reliability analysis**: Constitutional direction patterns by ideology and era
- **Procedural-institutional-systemic health correlation**: Inter-dimensional health relationships

### Expected Outcomes
1. **Statistical Analysis Results**: Quantified patterns in constitutional health dimensions across experimental factors
2. **Interaction Effect Analysis**: Statistical tests for interaction patterns between ideology and era
3. **Index Correlation Analysis**: Relationships between Constitutional Direction Index and experimental factors
4. **Temporal Pattern Analysis**: Constitutional health patterns across time periods
5. **Factorial Design Validation**: Technical validation of constitutional health analysis capabilities

## Significance

This experiment represents the first computational analysis of constitutional health patterns using factorial experimental design in American political discourse. The 2×3 factorial structure will produce empirical findings on:

1. **Temporal constitutional health effects**: Whether constitutional health shows systematic changes across political eras
2. **Ideological constitutional signatures**: Whether constitutional health dimensions differentiate conservative and progressive speakers  
3. **Constitutional health interactions**: Whether ideology and era interact to produce unique constitutional health patterns
4. **Democratic discourse health**: Whether constitutional health correlates with historical democratic stability

The factorial design provides comprehensive validation of constitutional health analysis while testing the platform's ability to detect complex statistical relationships in democratic discourse health patterns across six decades of American political development.