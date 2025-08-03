---
version: "7.0"
name: "cohesive_flourishing_factorial_analysis"
description: |
  This experiment analyzes discourse patterns in presidential speeches using the 
  Cohesive Flourishing Framework (CFF) v7.0. The corpus employs a temporal design 
  examining presidential speeches across different contexts spanning 2017-2025. 
  The analysis will measure cohesion and strategic framing dimensions to identify 
  any statistical patterns, relationships, or temporal trends present in the data.

hypothesis: |
  Discourse framing dimensions will be analyzed across presidential speeches to 
  test for statistical patterns and relationships. The analysis will examine whether 
  temporal factors, speech context factors, or their interaction account for 
  variance in cohesion and strategic framing patterns. Statistical tests will 
  determine if significant relationships exist between experimental factors and 
  Strategic Contradiction Index scores.

framework: "../../frameworks/reference/flagship/cff_v7.0.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 3
analysis_variant: "default"

# Enhanced v3.0 Analysis Configuration
analysis:
  evaluations_per_document: 3
  statistical_confidence: 0.95
  variance_threshold: 0.15

# Comprehensive Statistical Validation  
validation:
  required_tests: ["temporal_pattern_analysis", "framing_dimension_correlation_matrix", "sci_reliability", "axis_clustering_analysis", "speech_context_analysis", "strategic_tension_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "framing_discourse_patterns"
    - "temporal_factor_analysis"
    - "dimensional_axis_analysis"
    - "strategic_cohesion_relationships"
    - "speech_context_patterns"
    - "tension_pattern_analysis"
    - "reliability_assessment"
    - "statistical_methodology"
    - "findings_discussion"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Multi-Hypothesis Framework
hypotheses:
  H1_Temporal: "Test whether framing dimensions differ significantly across time periods"
  H2_Context: "Test whether framing dimensions differ significantly between speech contexts"
  H3_Axis_Relationships: "Test whether opposing dimensional axes show significant correlational patterns"
  H4_Strategic_Cohesion: "Test whether strategic tension measures correlate with framing intensity"
  H5_Index_Patterns: "Test whether SCI scores show systematic patterns across temporal factors"
  H6_Platform_Validation: "Test whether the JSON synthesis architecture successfully processes framing factorial design with 10-dimensional analysis"

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

# Computational Framing Factorial Analysis: Presidential Speech Patterns Across Time and Context

## Overview

This experiment analyzes computational framing patterns in presidential speeches using the Cohesive Flourishing Framework v6.0. The analysis employs a temporal design examining speech patterns across different contexts spanning 2017-2025.

## Research Questions

1. What patterns exist in discourse framing dimensions across presidential speeches?
2. What relationships exist between temporal factors and strategic framing measures?
3. How do framing patterns vary across different speech contexts and types?
4. What statistical relationships exist between opposing dimensional axes and strategic tension measures?

## Methodology

### Framework
**Cohesive Flourishing Framework v6.0** provides:
- 10-dimensional framing analysis across 5 strategic axes (Identity, Emotional, Success, Relational, Goal)
- Strategic Contradiction Index (SCI) for coherence measurement
- JSON-first architecture with enhanced synthesis integration
- Tension mathematics for strategic contradiction quantification

### Corpus Design
5 presidential speeches spanning 2017-2025:

**Early Presidential Period (2017)**:
- Inaugural Address (foundational presidential rhetoric)
- State of the Union 2017 (early presidential communication)

**Mid Presidential Period (2018)**:
- State of the Union 2018 (mid-term presidential communication)

**Late Presidential Period (2020)**:
- State of the Union 2020 (late first-term presidential communication)

**Recent Presidential Period (2025)**:
- State of the Union 2025 (recent presidential communication)

**Temporal Balance**: 5 speeches across 4 time periods, enabling temporal pattern analysis and speech context comparison.

### Enhanced Statistical Analysis
- **Temporal pattern analysis**: Statistical tests for dimension patterns across time periods
- **Multi-evaluation reliability**: 3 independent assessments per document (N=15 total evaluations)
- **Framing dimension clustering**: Axis profile similarities within/across speeches
- **Strategic tension analysis**: Relationships between SCI and framing intensity measures
- **Speech context analysis**: Comparative analysis of inaugural vs. SOTU speech patterns
- **Reliability analysis**: SCI consistency patterns across speeches and evaluations

### Expected Outcomes
1. **Statistical Analysis Results**: Quantified patterns in framing dimensions across experimental factors
2. **Temporal Pattern Analysis**: Statistical tests for framing patterns across time periods
3. **Strategic Tension Analysis**: Relationships between SCI and dimensional axis patterns
4. **Context Comparison Analysis**: Statistical differences between speech contexts and types
5. **Factorial Design Validation**: Technical validation of computational framing analysis capabilities

## Significance

This experiment provides systematic computational analysis of framing patterns using factorial experimental design in presidential rhetoric. The temporal structure will produce empirical findings on:

1. **Temporal framing effects**: Whether framing dimensions show systematic changes across time periods
2. **Strategic coherence patterns**: Whether SCI measures correlate with temporal or contextual factors  
3. **Axis relationship patterns**: Whether opposing framing dimensions show systematic tension structures
4. **Speech context effects**: Whether different speech contexts produce distinct framing patterns

The factorial design provides comprehensive validation of computational framing analysis while testing the platform's ability to detect complex statistical relationships in political communication patterns across multiple time periods and speech contexts.