---
name: "democratic_discourse_cohesion_study"
description: |
  A comparative analysis of social cohesion patterns across four distinct approaches to democratic discourse: 
  institutional gracious concession, populist progressive critique, populist conservative rhetoric, and 
  populist progressive advocacy. This study examines how different rhetorical strategies impact social 
  fabric and democratic resilience using the Cohesive Flourishing Framework v7.3 to analyze four 
  paradigmatic examples of American political communication spanning 2008-2025.

# Framework version compliance (v7.3)
framework_version: "v7.3"

# Falsifiable hypotheses to be tested
hypotheses:
  H1_Institutional_Cohesion: "McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) compared to populist discourse styles"
  H2_Populist_Spectrum: "Populist discourse (Sanders, King, AOC) will show higher fragmentative elements (tribal dominance, enmity) but with varying strategic contradiction patterns across progressive and conservative variants"
  H3_Discourse_Differentiation: "The four discourse types will exhibit distinct social cohesion signatures: institutional (McCain) showing highest cohesion, populist conservative (King) showing highest fragmentation, and populist progressive (Sanders, AOC) showing moderate patterns with strategic tensions"
  H4_Temporal_Consistency: "Discourse style will be a stronger predictor of cohesion patterns than temporal factors (2008 vs 2025 speeches)"

# Path to the Framework v7.3 specification file
framework: "../../frameworks/reference/flagship/cff_v7.3.md"

# Path to the Corpus v7.3 directory
corpus_path: "corpus/"

# REQUIRED: Configuration for the analysis process
analysis:
  version: "v7.3"
  gasket_version: "v7.3"
  variant: "default"
  models:
    - "vertex_ai/gemini-2.5-flash"

# OPTIONAL: Configuration for the synthesis process
synthesis:
  version: "v7.3"
  gasket_version: "v7.3"
  model: "vertex_ai/gemini-2.5-flash"

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

This study examines how different approaches to democratic discourse impact social cohesion and democratic resilience. By analyzing four paradigmatic examples of American political communication—McCain's 2008 gracious concession, Sanders' 2025 anti-oligarchy critique, King's 2017 cultural identity speech, and Ocasio-Cortez's 2025 economic inequality address—we investigate the social cohesion signatures across institutional and populist democratic discourse styles.

## Research Questions

1. How do institutional democratic norms (McCain's concession) compare to populist discourse styles (Sanders, King, AOC) in terms of social cohesion patterns?
2. What differences emerge between populist progressive (Sanders, AOC) and populist conservative (King) discourse in their social cohesion signatures?
3. Do temporal factors (2008 vs 2017 vs 2025) influence cohesion patterns independent of discourse style?
4. What strategic contradictions emerge across different populist variants, and how do they compare to institutional discourse coherence?

## Methodology

### Framework
**Cohesive Flourishing Framework (CFF) v7.3** provides:
- 5-axis social cohesion analysis (Identity, Emotional Climate, Success Orientation, Relational Climate, Goal Orientation)
- Strategic Contradiction Index measuring rhetorical tension deployment
- Salience-weighted social cohesion calculations
- Democratic resilience impact assessment

### Corpus Design
Four paradigmatic examples of American democratic discourse spanning 2008-2025:

**Institutional Democratic Norms**: John McCain's 2008 concession speech
- Exemplifies gracious democratic transition
- Tests institutional cohesion patterns (dignity, hope, amity)
- Represents established democratic procedural norms

**Populist Progressive Critique**: Bernie Sanders' 2025 anti-oligarchy speech  
- Exemplifies populist economic justice rhetoric
- Tests fragmentative elements with strategic contradictions
- Represents progressive outsider challenge to established power

**Populist Conservative Rhetoric**: Steve King's 2017 cultural identity speech
- Exemplifies populist conservative cultural discourse
- Tests fragmentative patterns with cultural identity focus
- Represents conservative populist boundary-setting rhetoric

**Populist Progressive Advocacy**: Alexandria Ocasio-Cortez's 2025 economic inequality address
- Exemplifies populist progressive systemic critique
- Tests moderate cohesion with justice-focused messaging
- Represents generational progressive populist approach

### Expected Outcomes
1. **Cohesion Hierarchy**: McCain (institutional) > AOC (populist progressive) > Sanders (populist progressive) > King (populist conservative) in overall cohesion indices
2. **Strategic Contradiction Patterns**: Progressive populists (Sanders, AOC) will exhibit sophisticated rhetorical tensions balancing critique with democratic ideals, while King will show more direct fragmentative patterns
3. **Discourse Style Differentiation**: Four distinct social cohesion profiles corresponding to institutional, populist progressive, and populist conservative approaches
4. **Temporal Independence**: Discourse style will predict cohesion patterns more strongly than temporal factors (2008 vs 2017 vs 2025)
5. **Democratic Resilience Insights**: Understanding how different populist variants impact democratic fabric differently

## Significance

This comparative analysis addresses a critical gap in political communication research: understanding how different democratic discourse styles impact social cohesion and democratic resilience. The study provides empirical measurement of theoretical distinctions between institutional and populist democratic approaches, with additional insights into progressive versus conservative populist variants.

The four contrasting discourse types enable precise measurement of social cohesion dimensions while maintaining high analytical validity through paradigmatic case selection spanning 17 years of American political communication. Results inform broader questions about democratic communication strategies, populist discourse diversity, and their differential societal impacts.
