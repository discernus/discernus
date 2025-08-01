---
name: "simple_character_validation_v7"
description: |
  A minimal test experiment for validating the Discernus v7.0 gasket architecture using 
  the Character Assessment Framework v7.0. This experiment tests MECE Trinity coherence
  (Framework v7.0 + Experiment v7.0 + Corpus v7.0) and Raw Analysis Log processing with 
  a 2-document ideological contrast design (Conservative vs Progressive speakers). 
  Designed as a comprehensive smoke test for validating complete gasket architecture implementation.

hypothesis: |
  Character dimensions will show measurable differences between conservative 
  and progressive speakers, validating the framework's ability to detect 
  ideological character signatures through Raw Analysis Log processing. 
  The gasket architecture will successfully extract, process, and synthesize 
  character coherence patterns across different political approaches.

framework: "../../frameworks/reference/core/caf_v7.0.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 10
analysis_variant: "default"

# 🆕 V7.0 GASKET ARCHITECTURE CONFIGURATION
gasket_workflow:
  validate_trinity_coherence: true
  raw_analysis_log_processing: true
  intelligent_extractor_enabled: true
  parallel_streams: true

# Enhanced v7.0 Analysis Configuration  
analysis:
  statistical_confidence: 0.95
  variance_threshold: 0.20

# Simplified Statistical Validation  
validation:
  required_tests: ["character_correlation_matrix", "mc_sci_reliability", "ideological_comparison"]
  reliability_threshold: 0.60
  effect_size_reporting: true

# Streamlined Academic Reporting
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "character_comparison_analysis"
    - "ideological_signatures"
    - "mc_sci_patterns"
    - "synthesis_validation_results"
    - "statistical_methodology"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Focused Hypothesis Framework
hypotheses:
  H1_Ideological: "Character dimensions will show significant differences between conservative (McCain) and progressive (Sanders) speakers"
  H2_Coherence: "MC-SCI scores will successfully differentiate between gracious institutional discourse and passionate populist critique"
  H3_Architecture: "The v7.0 gasket architecture will successfully process 2-document character analysis with Raw Analysis Log processing"

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

# Simple Character Validation Test

## Overview

This experiment serves as a minimal validation test for the Discernus v6.0 architecture, specifically testing synthesis coordination and JSON-first processing using the Character Assessment Framework v6.0.

## Research Questions

1. Can the synthesis pipeline successfully coordinate character analysis across ideologically contrasting speakers?
2. Do the v6.0 JSON structures flow correctly through the analysis → synthesis pathway?
3. Can the MC-SCI calculations differentiate between institutional vs populist discourse styles?

## Methodology

### Framework
**Character Assessment Framework v6.0** provides:
- 10-dimensional character analysis (5 virtues vs 5 vices)
- Moral Character Strategic Contradiction Index (MC-SCI)
- JSON-first architecture validation
- Character tension mathematics testing

### Minimal Corpus Design
2 political speeches providing ideological contrast:

**Conservative/Institutional**: John McCain 2008 concession speech
**Progressive/Populist**: Bernie Sanders 2025 oligarchy speech

### Expected Outcomes
1. **Character Differentiation**: Measurable differences in virtue/vice patterns between speakers
2. **MC-SCI Validation**: Coherence metrics reflecting discourse styles (institutional grace vs populist intensity)
3. **Architecture Testing**: Successful v6.0 JSON synthesis without coordination failures
4. **Debugging Support**: Clear identification of any synthesis pipeline issues

## Significance

This experiment validates the core v6.0 architecture components in a controlled, minimal environment. Success confirms the synthesis coordination fixes and provides a reliable baseline for more complex factorial experiments.

The 2-document design enables rapid iteration and debugging while maintaining analytical meaningfulness through ideological character contrasts.