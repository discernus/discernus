---
name: "character_ideology_evolution_hypothesis"
description: |
  This experiment tests whether civic character patterns have systematically evolved 
  across three American political eras AND whether conservative vs. progressive 
  ideological affiliations interact with temporal changes using the Character 
  Assessment Framework v6.0. The corpus creates a 2×3 factorial design: Ideology 
  (Conservative/Progressive) × Era (Civil Rights/Institutional/Populist) spanning 
  60 years (1963-2025). This analysis will reveal whether ideological differences 
  in civic virtue have widened or narrowed over time, and whether populist-era 
  rhetoric shows ideological convergence in character patterns.

hypothesis: |
  Character patterns will show measurable differences across political eras and 
  ideological affiliations. The analysis will test whether temporal evolution, 
  ideological differentiation, or their interaction best explains variance in 
  civic character dimensions. The MC-SCI will reveal whether character coherence 
  patterns correlate with historical period, ideological position, or both.

framework: "caf_v6.1_factorial.md"
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
  required_tests: ["two_way_anova_ideology_era", "character_correlation_matrix", "mc_sci_reliability", "temporal_trend_analysis", "ideological_clustering_analysis", "interaction_effects_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "temporal_character_evolution"
    - "ideological_character_signatures"
    - "ideology_era_interaction_analysis"
    - "populist_convergence_hypothesis"
    - "character_contradiction_patterns"
    - "factorial_design_results"
    - "statistical_methodology"
    - "cross_validation_results"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Multi-Hypothesis Framework
hypotheses:
  H1_Temporal: "Character dimensions will show significant main effects across the three political eras (Civil Rights, Institutional, Populist)"
  H2_Ideological: "Character dimensions will show significant main effects between conservative and progressive speakers"
  H3_Interaction: "Ideology×Era interaction effects will be statistically significant for at least three character dimensions"
  H4_Coherence: "MC-SCI scores will correlate with either temporal period, ideological position, or their interaction"
  H5_Variance: "The factorial model will explain significantly more variance than single-factor models"
  H6_Platform_Validation: "The JSON-only synthesis architecture will successfully process 2×3 factorial design with 10-dimensional character analysis"

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

# The Character-Ideology Evolution Hypothesis: Civic Virtue Patterns Across American Political Eras and Ideological Lines

## Overview

This experiment tests whether civic character patterns have systematically evolved across three American political eras AND whether conservative vs. progressive ideological affiliations interact with these temporal changes using the Character Assessment Framework v6.0. The analysis employs a sophisticated 2×3 factorial design spanning 60 years of American political discourse (1963-2025).

## Research Questions

1. Has American political discourse become measurably less virtuous over time across ideological lines?
2. Do conservatives and progressives exhibit distinct character signatures that persist across eras?
3. Have ideological differences in civic virtue widened or narrowed over time?
4. Does populist-era rhetoric show ideological convergence in character patterns?

## Methodology

### Framework
**Character Assessment Framework v6.0** provides:
- 10-dimensional character analysis (5 virtues vs 5 vices)
- Moral Character Strategic Contradiction Index (MC-SCI) for coherence measurement
- JSON-first architecture with enhanced synthesis integration
- Character tension mathematics for contradiction quantification

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

**Factorial Balance**: 4 Progressive vs 4 Conservative speakers across 3 eras, enabling sophisticated interaction analysis.

### Enhanced Statistical Analysis
- **Two-way ANOVA**: Ideology × Era main effects and interaction analysis
- **Multi-evaluation reliability**: 3 independent assessments per document (N=24 total evaluations)
- **Ideological clustering analysis**: Character profile similarities within/across ideologies
- **Interaction effects analysis**: Where ideology and era effects amplify or cancel
- **MC-SCI reliability analysis**: Character coherence patterns by ideology and era
- **Temporal trend analysis**: Linear regression of character evolution by ideological group

### Expected Outcomes
1. **Statistical Main Effects**: Quantified character dimension differences by ideology and era
2. **Interaction Effect Analysis**: Evidence for or against ideology×era interaction patterns
3. **Character Coherence Patterns**: MC-SCI correlations with experimental factors
4. **Variance Decomposition**: Relative explanatory power of temporal vs ideological factors
5. **Factorial Design Validation**: Comprehensive test of platform's complex statistical capabilities

## Significance

This experiment represents the first computational analysis of civic character patterns using factorial experimental design in American political discourse. The 2×3 factorial structure will produce empirical findings on:

1. **Temporal effects**: Whether character dimensions show systematic changes across political eras
2. **Ideological effects**: Whether character dimensions differentiate conservative and progressive speakers  
3. **Interaction effects**: Whether ideology and era interact to produce unique character patterns
4. **Character coherence**: Whether MC-SCI patterns correlate with experimental factors

The factorial design provides comprehensive validation of the platform's enhanced JSON-only synthesis capabilities while testing its ability to detect complex statistical relationships. This represents a methodological advance beyond single-factor studies, enabling rigorous analysis of multifactorial influences on civic character patterns across six decades of American political discourse. 