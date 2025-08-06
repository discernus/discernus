---
name: "democratic_discourse_cohesion_study"
description: |
  A comparative analysis of social cohesion patterns in contrasting approaches to democratic discourse: 
  institutional gracious concession versus populist anti-establishment critique. This study examines 
  how different rhetorical strategies impact social fabric and democratic resilience using the 
  Cohesive Flourishing Framework v7.3 to analyze two paradigmatic examples of American political communication.

# Framework version compliance (v7.3)
framework_version: "v7.3"



# Falsifiable hypotheses to be tested
hypotheses:
  H1_Institutional_Cohesion: "McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition"
  H2_Populist_Fragmentation: "Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning"
  H3_Democratic_Patterns: "The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches"

# Success criteria for validation
success_criteria:
  technical_success:
    - "Complete pipeline execution without errors through all workflow agents"
    - "Both corpus documents analyzed successfully with CFF v7.3 framework"
    - "Generation of final_report.md and statistical_results.json artifacts"
    - "Valid JSON output conforming to CFF v7.3 schema"
  
  analytical_success:
    - "Clear differentiation between institutional vs populist cohesion signatures"
    - "Strategic contradiction analysis reveals sophisticated rhetorical patterns"
    - "Framework score extraction success rate > 95%"
    - "Evidence quality meets academic standards with direct textual support"
  
  research_success:
    - "Hypotheses H1-H3 receive clear empirical support or refutation"
    - "Democratic resilience implications clearly articulated"
    - "Comparative analysis provides actionable insights for political communication"

# Path to the Framework v7.3 specification file
framework: "../../frameworks/reference/flagship/cff_v7.3.md"

# Path to the Corpus v7.1 directory
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

# Validation requirements for academic rigor
validation:
  required_tests:
    - "speaker_differentiation_analysis"
    - "cohesion_signature_comparison" 
    - "strategic_contradiction_analysis"
    - "democratic_resilience_assessment"
  reliability_threshold: 0.80
  effect_size_reporting: true
  confidence_intervals: true

# Expected outcomes and success criteria for the experiment
expected_outcomes:
  statistical_analysis:
    - "Social cohesion comparative analysis between institutional and populist discourse"
    - "Strategic contradiction analysis measuring rhetorical tension patterns"
    - "Democratic resilience impact assessment across CFF dimensions"
  quality_metrics:
    - "Framework score extraction success rate > 95%"
    - "Clear differentiation between institutional vs populist cohesion signatures"

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