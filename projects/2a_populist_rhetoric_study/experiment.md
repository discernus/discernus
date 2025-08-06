---
version: "7.3"
name: "populist_discourse_factorial_analysis"
description: |
  This experiment analyzes discourse patterns in presidential speeches using the 
  Populist Discourse Analysis Framework (PDAF) v7.3. The corpus employs a 
  temporal design examining presidential speeches across multiple contexts 
  spanning 2017-2025. The analysis will measure populist discourse dimensions 
  to identify any statistical patterns, relationships, or temporal trends 
  present in the data.

hypothesis: |
  Populist discourse dimensions will be analyzed across presidential speeches 
  to test for statistical patterns and relationships. The analysis will examine 
  whether temporal factors, speech context factors, or their interaction account 
  for variance in populist discourse patterns. Statistical tests will determine 
  if significant relationships exist between experimental factors and Populist 
  Strategic Contradiction Index scores.

framework: "../../frameworks/reference/flagship/pdaf_v7.3.md"
corpus_path: "corpus/"

# REQUIRED: Configuration for the analysis process
analysis:
  # The specific analysis variant to use from the framework file
  variant: "default"
  # List of LiteLLM-compatible model identifiers for analysis
  models:
    - "vertex_ai/gemini-2.5-flash-lite"

# OPTIONAL: Configuration for the synthesis process
synthesis:
  # Model to use for the final report synthesis
  model: "vertex_ai/gemini-2.5-flash-lite"

# Enhanced v3.0 Analysis Configuration
analysis:
  evaluations_per_document: 3
  statistical_confidence: 0.95
  variance_threshold: 0.15

# Comprehensive Statistical Validation  
validation:
  required_tests: ["temporal_pattern_analysis", "populist_dimension_correlation_matrix", "psci_reliability", "anchor_clustering_analysis", "speech_context_analysis", "tension_pattern_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "populist_discourse_patterns"
    - "temporal_factor_analysis"
    - "anchor_dimension_analysis"
    - "strategic_tension_relationships"
    - "speech_context_patterns"
    - "reliability_assessment"
    - "statistical_methodology"
    - "findings_discussion"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Multi-Hypothesis Framework
hypotheses:
  H1_Temporal: "Test whether populist discourse dimensions differ significantly across time periods"
  H2_Context: "Test whether populist discourse dimensions differ significantly between speech contexts"
  H3_Relationships: "Test whether populist anchor dimensions show significant correlational patterns"
  H4_Strategic_Tensions: "Test whether strategic tension measures correlate with populist intensity"
  H5_Index_Patterns: "Test whether PSCI scores show systematic patterns across temporal factors"
  H6_Platform_Validation: "Test whether the JSON synthesis architecture successfully processes populist discourse factorial design with 9-dimensional analysis"

# Canonical workflow configuration (v7.3 compliant)
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

# Populist Discourse Factorial Analysis: Presidential Speech Patterns Across Time and Context

## Overview

This experiment analyzes populist discourse patterns in presidential speeches using the Populist Discourse Analysis Framework (PDAF) v7.1. The analysis employs a temporal design examining speech patterns across different contexts spanning 2017-2025.

## Research Questions

1. What patterns exist in populist discourse dimensions across presidential speeches?
2. What relationships exist between temporal factors and populist discourse measures?
3. How do populist discourse patterns vary across different speech contexts?
4. What statistical relationships exist between populist anchor dimensions and strategic tension measures?

## Methodology

### Framework
**Populist Discourse Analysis Framework (PDAF) v7.1** provides:
- 9-dimensional populist anchor analysis across core, mechanism, and boundary dimensions
- Populist Strategic Contradiction Index (PSCI) for strategic coherence measurement
- JSON-first architecture with enhanced synthesis integration
- Strategic tension mathematics for contradiction quantification

### Corpus Design
6 presidential speeches spanning 2017-2025:

**Early Presidential Period (2017)**:
- Inaugural Address (foundational presidential rhetoric)
- Joint Session Address (early policy vision)

**Mid-Presidential Period (2018-2020)**:
- State of the Union 2018 (annual presidential communication)
- State of the Union 2019 (annual presidential communication)
- State of the Union 2020 (annual presidential communication)

**Recent Presidential Period (2025)**:
- State of the Union 2025 (recent presidential communication)

**Temporal Balance**: 6 speeches across 3 time periods, enabling temporal pattern analysis and speech context comparison.

### Enhanced Statistical Analysis
- **Temporal pattern analysis**: Statistical tests for dimension patterns across time periods
- **Multi-evaluation reliability**: 3 independent assessments per document (N=18 total evaluations)
- **Populist dimension clustering**: Anchor profile similarities within/across speeches
- **Strategic tension analysis**: Relationships between PSCI and populist intensity measures
- **Speech context analysis**: Comparative analysis of speech types and contexts
- **Reliability analysis**: PSCI consistency patterns across speeches and evaluations

### Expected Outcomes
1. **Statistical Analysis Results**: Quantified patterns in populist discourse dimensions across experimental factors
2. **Temporal Pattern Analysis**: Statistical tests for populist discourse patterns across time periods
3. **Strategic Tension Analysis**: Relationships between PSCI and populist anchor dimensions
4. **Context Comparison Analysis**: Statistical differences between speech contexts and types
5. **Factorial Design Validation**: Technical validation of populist discourse analysis capabilities

## Significance

This experiment provides systematic computational analysis of populist discourse patterns using factorial experimental design in presidential rhetoric. The temporal structure will produce empirical findings on:

1. **Temporal discourse effects**: Whether populist dimensions show systematic changes across time periods
2. **Strategic coherence patterns**: Whether PSCI measures correlate with temporal or contextual factors  
3. **Anchor relationship patterns**: Whether populist discourse dimensions show systematic correlational structures
4. **Speech context effects**: Whether different speech contexts produce distinct populist discourse patterns

The factorial design provides comprehensive validation of populist discourse analysis while testing the platform's ability to detect complex statistical relationships in political communication patterns across multiple time periods and speech contexts.