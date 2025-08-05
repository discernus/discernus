---
name: "democratic_discourse_cohesion_study"
description: |
  A comparative analysis of social cohesion patterns in contrasting approaches to democratic discourse: 
  institutional gracious concession versus populist anti-establishment critique. This study examines 
  how different rhetorical strategies impact social fabric and democratic resilience using the 
  Cohesive Flourishing Framework v7.3 to analyze two paradigmatic examples of American political communication.

hypothesis: |
  McCain's institutional concession discourse will demonstrate higher social cohesion indices 
  (dignity, hope, amity, cohesive goals) while Sanders' populist critique will show higher 
  fragmentative elements (tribal dominance, enmity) but with strategic contradictions reflecting 
  sophisticated rhetorical positioning. The analysis will reveal distinct social cohesion signatures 
  between institutional democratic norms and populist democratic renewal approaches.

framework: "../../frameworks/reference/flagship/cff_v7.3.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 3
analysis_variant: "default"

# 🆕 V7.3 SOCIAL COHESION ANALYSIS CONFIGURATION
gasket_workflow:
  enhanced_metadata_extraction: true
  intelligent_extractor_enabled: true
  advanced_pattern_matching: true
  metadata_scores_required: true

# Social Cohesion Analysis Configuration  
analysis:
  statistical_confidence: 0.95
  variance_threshold: 0.20
  focus_dimensions: ["identity_axis", "emotional_climate_axis", "relational_climate_axis"]

# Social Cohesion Validation  
validation:
  required_tests: ["cohesion_correlation_matrix", "strategic_contradiction_analysis", "democratic_impact_assessment"]
  reliability_threshold: 0.60
  effect_size_reporting: true

# Streamlined Academic Reporting
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "social_cohesion_comparative_analysis"
    - "democratic_discourse_patterns"
    - "strategic_contradiction_analysis"
    - "democratic_resilience_implications"
    - "statistical_methodology"
    - "limitations_and_future_research"
  show_statistical_work: true
  include_confidence_metrics: true

# Research Hypotheses Framework
hypotheses:
  H1_Institutional_Cohesion: "McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition"
  H2_Populist_Fragmentation: "Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning"
  H3_Democratic_Patterns: "The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches"

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

# Democratic Discourse and Social Cohesion: A Comparative Study

## Overview

This study examines how different approaches to democratic discourse impact social cohesion and democratic resilience. By analyzing two paradigmatic examples of American political communication—McCain's 2008 gracious concession and Sanders' 2025 anti-oligarchy critique—we investigate the social cohesion signatures of institutional versus populist democratic discourse.

## Research Questions

1. How do institutional democratic norms (gracious concession) compare to populist democratic critique in terms of social cohesion patterns?
2. What strategic contradictions emerge in populist discourse, and how do they differ from institutional discourse coherence?
3. Do these contrasting discourse types exhibit measurably different impacts on democratic resilience and social fabric?

## Methodology

### Framework
**Cohesive Flourishing Framework (CFF) v7.3** provides:
- 5-axis social cohesion analysis (Identity, Emotional Climate, Success Orientation, Relational Climate, Goal Orientation)
- Strategic Contradiction Index measuring rhetorical tension deployment
- Salience-weighted social cohesion calculations
- Democratic resilience impact assessment

### Corpus Design
Two paradigmatic examples of American democratic discourse:

**Institutional Democratic Norms**: John McCain's 2008 concession speech
- Exemplifies gracious democratic transition
- Tests institutional cohesion patterns (dignity, hope, amity)
- Represents established democratic procedural norms

**Populist Democratic Critique**: Bernie Sanders' 2025 anti-oligarchy speech  
- Exemplifies populist democratic renewal rhetoric
- Tests fragmentative elements with strategic contradictions
- Represents outsider challenge to established power

### Expected Outcomes
1. **Cohesion Differentiation**: McCain will show higher overall cohesion indices reflecting institutional democratic values
2. **Strategic Contradiction Patterns**: Sanders will exhibit sophisticated rhetorical tensions balancing populist critique with democratic ideals
3. **Democratic Signature Analysis**: Distinct social cohesion profiles corresponding to institutional vs. populist approaches
4. **Resilience Implications**: Insights into how different discourse types impact democratic fabric

## Significance

This comparative analysis addresses a critical gap in political communication research: understanding how different democratic discourse styles impact social cohesion and democratic resilience. The study provides empirical measurement of theoretical distinctions between institutional and populist democratic approaches.

The contrasting discourse types enable precise measurement of social cohesion dimensions while maintaining high analytical validity through paradigmatic case selection. Results inform broader questions about democratic communication strategies and their societal impacts.