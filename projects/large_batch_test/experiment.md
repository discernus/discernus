---
# REQUIRED: A unique, machine-readable name for the experiment.
name: presidential_character_evolution_study

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  A comprehensive character assessment of US presidential rhetoric (1993-2025) analyzing 
  temporal evolution, party differences, and contextual variations across 47 speeches from 
  5 presidents. This experiment leverages the corpus's rich metadata structure to test 
  both system scalability and substantive research capabilities using the Character 
  Assessment Framework v5.0.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  Presidential character dimensions will demonstrate measurable patterns across temporal, 
  partisan, and contextual dimensions, with the Character Assessment Framework v5.0 
  reliably detecting these patterns while maintaining statistical consistency across 
  the 47-document corpus spanning 33 years of American political discourse.

# REQUIRED: A relative path to the framework file to be used.
framework: framework.md

# REQUIRED: A relative path to the corpus directory to be analyzed.
corpus_path: corpus/

# REQUIRED: A list of one or more LiteLLM-compatible model strings.
models:
  - "vertex_ai/gemini-2.5-flash-lite"

# REQUIRED: The number of times to run the analysis for each model.
runs_per_model: 1

# OPTIONAL: Analysis variant to use from the framework (defaults to 'default')
analysis_variant: default

# NEW v3.0: Enhanced analysis configuration
analysis:
  # Multi-evaluation for reliability assessment
  evaluations_per_document: 3
  # Statistical confidence level  
  statistical_confidence: 0.95
  # Variance threshold for evaluation consistency
  variance_threshold: 0.15

# NEW v3.0: Statistical validation requirements
validation:
  # Statistical tests for corpus analysis
  required_tests: ["correlation_analysis", "temporal_analysis", "group_comparison", "reliability_analysis"]
  # Minimum reliability threshold
  reliability_threshold: 0.70
  # Include effect size reporting
  effect_size_reporting: true

# NEW v3.0: Enhanced reporting configuration leveraging corpus metadata
reporting:
  # Comprehensive academic format
  format: "academic"
  # Structured sections utilizing corpus dimensions
  structure:
    - "executive_summary"
    - "temporal_evolution_analysis"    # 1993-2025 character trends
    - "partisan_character_profiles"    # Democrat vs Republican patterns  
    - "presidential_individual_analysis"  # Per-president character assessment
    - "contextual_speech_analysis"     # Inaugural vs SOTU differences
    - "statistical_methodology"       # Multi-evaluation reliability
    - "corpus_metadata_utilization"   # How metadata informed analysis
    - "limitations_and_future_research"
  # Documentation of statistical work
  show_statistical_work: true
  # Include confidence metrics and effect sizes
  include_confidence_metrics: true

# REQUIRED: Enhanced workflow with corpus-aware synthesis
workflow:
  # Step 1: Multi-evaluation analysis with corpus awareness
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment     # Gets analysis configuration
      - framework      # CAF v5.0 with virtue/vice groupings
      - corpus         # 47 speeches with rich metadata
    outputs:
      - analysis_results

  # Step 2: Corpus-intelligent synthesis leveraging metadata
  - agent: EnhancedSynthesisAgent
    inputs:
      - analysis_results
      - experiment     # Gets reporting structure and requirements
      - framework      # Gets dimension_groups for intelligent analysis
      - corpus         # Gets file_manifest for metadata-driven insights
    outputs:
      - final_report.md
      - results.csv

# OPTIONAL: Research hypotheses leveraging corpus structure
hypotheses:
  H1_Temporal_Evolution: "Character dimensions will show measurable evolution across the 33-year span (1993-2025) with detectable shift points"
  H2_Partisan_Profiles: "Democratic presidents (Clinton, Obama, Biden) will show higher dignity/hope scores than Republican presidents (Bush, Trump)" 
  H3_Contextual_Variation: "Inaugural addresses will score significantly higher on hope and lower on fear than State of Union addresses"
  H4_Individual_Consistency: "Individual presidents will maintain consistent character profiles across multiple speeches despite temporal variation"
  H5_Crisis_Response: "Character profiles will show detectable changes during crisis periods (9/11, financial crisis, COVID-19)"
  H6_System_Scalability: "Multi-evaluation analysis maintains reliability across 47 documents with CSV architecture scaling efficiently"

---

# Presidential Character Evolution Study (1993-2025)

## Research Overview
This experiment conducts a comprehensive character assessment of US presidential rhetoric across 33 years, analyzing 47 speeches from Clinton, Bush, Obama, Trump, and Biden. The study leverages the corpus's rich temporal and partisan structure to test both substantive research hypotheses and system scalability capabilities.

## Corpus Intelligence: How LLMs Will Leverage Metadata

### Temporal Analysis (1993-2025)
The synthesis agent will receive experiment configuration directing it to perform `temporal_evolution_analysis`. With access to the corpus file_manifest containing year metadata, it can:
- **Group speeches by decade**: 1990s (9), 2000s (15), 2010s (13), 2020s (10)
- **Identify historical inflection points**: Pre/post 9/11, financial crisis, Trump era, COVID-19
- **Track character evolution**: How dignity/hope/fear scores change over time

### Partisan Character Profiling
With `partisan_character_profiles` in the reporting structure and party metadata in the corpus manifest, the synthesis agent can:
- **Compare party aggregates**: Democrat (28 speeches) vs Republican (19 speeches)
- **Test partisan hypotheses**: "Democrats score higher on dignity/hope than Republicans"
- **Individual vs party patterns**: How much does individual character vs party affiliation matter?

### Presidential Individual Analysis
The `presidential_individual_analysis` section combined with president metadata enables:
- **Per-president character profiles**: Clinton's pragmatism, Bush's crisis leadership, Obama's hope
- **Consistency assessment**: Does each president maintain character across multiple speeches?
- **Evolution within presidency**: How does character change from first to final speeches?

### Contextual Speech Analysis
Using `speech_type` metadata (inaugural vs sotu), the synthesis agent can:
- **Compare speech contexts**: Aspirational inaugurals vs operational SOTU addresses
- **Test contextual hypotheses**: "Inaugurals score higher on hope, lower on fear"
- **Temporal context**: How do crisis SOTUs differ from normal SOTUs?

## LLM Metadata Utilization Strategy

The key insight is that the synthesis agent will receive:
1. **Experiment Configuration**: Tells it what analysis to perform
2. **Framework Metadata**: Provides dimension_groups (virtues vs vices) for intelligent grouping
3. **Corpus Manifest**: Provides president, party, year, speech_type for each document
4. **Aggregated Results**: CSV data with character scores linked to artifact IDs

The LLM can then **intelligently cross-reference** these data sources to generate sophisticated analysis without hardcoded templates.

## Expected Research Insights
1. **Temporal Trends**: Character evolution across 33 years of American politics
2. **Partisan Differences**: Systematic character differences between parties
3. **Individual Signatures**: Unique character profiles for each president
4. **Contextual Variation**: How speech context shapes character expression
5. **Crisis Response**: Character changes during national crises

## System Validation Criteria
1. **Multi-Evaluation Reliability**: 3 evaluations per document maintain consistency
2. **Metadata Integration**: Synthesis agent successfully leverages corpus structure
3. **Statistical Rigor**: Temporal and group comparisons with proper statistical testing
4. **Academic Reporting**: Structured report demonstrates corpus-intelligent analysis
5. **Scalability Proof**: 47-document processing with efficient CSV architecture 