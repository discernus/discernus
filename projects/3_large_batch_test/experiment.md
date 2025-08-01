---
name: presidential_populism_emergence_study
description: |
  A comprehensive longitudinal analysis of American political discourse (1992-2025) 
  examining temporal evolution, partisan differences, and contextual variations across 
  63 documents (45 presidential speeches + 18 party platforms) from 5 presidents. This 
  experiment leverages the Political Discourse Analysis Framework v6.0 to discover 
  when, how, and if populist discourse patterns emerged in American political rhetoric, 
  without predetermined assumptions about "populist eras" - letting the data reveal 
  actual temporal patterns of discourse evolution. The corpus includes 9 inaugural addresses, 
  35 State of the Union speeches, 1 Address to Joint Session of Congress (AJSC), and 18 party 
  platforms. The 2025 documents reflect the actual historical outcome of the 2024 election.
hypothesis: |
  The Political Discourse Analysis Framework v6.0 will reliably detect measurable 
  temporal patterns in American political discourse across the 33-year study period 
  (1992-2025), revealing when and how populist discourse emerged (if at all) without 
  predetermined assumptions about "populist eras." The framework will demonstrate 
  statistical consistency across the longitudinal corpus while enabling discovery 
  of actual inflection points, partisan differences, and contextual variations in 
  populist versus pluralist discourse patterns.
framework: "framework.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
analysis_variant: longitudinal_analysis
analysis:
  evaluations_per_document: 2
  statistical_confidence: 0.95
  variance_threshold: 0.15
validation:
  required_tests: ["temporal_trend_analysis", "change_point_detection", "partisan_analysis", "reliability_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "temporal_discourse_evolution"
    - "change_point_analysis"
    - "partisan_discourse_patterns"
    - "presidential_discourse_profiles"
    - "institutional_vs_individual"
    - "contextual_discourse_variation"
    - "quadrant_evolution_analysis"
    - "statistical_methodology"
    - "discourse_marker_evidence"
    - "limitations_and_future_research"
  show_statistical_work: true
  include_confidence_metrics: true
workflow:
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - analysis_results
  - agent: EnhancedSynthesisAgent
    inputs:
      - analysis_results
      - experiment
      - framework
      - corpus
    outputs:
      - final_report.md
      - results.csv
hypotheses:
  H1_Temporal_Pattern_Detection: "The framework will detect statistically significant temporal patterns in discourse evolution across the 33-year period, with identifiable change points marking discourse shifts"
  H2_Partisan_Discourse_Differences: "Democratic and Republican discourse will show measurable differences on both populism-pluralism and nationalism-patriotism axes, with patterns varying by time period"
  H3_Presidential_Signature_Consistency: "Individual presidents will demonstrate consistent discourse signatures across multiple speeches, with measurable differences between presidents"
  H4_Contextual_Discourse_Variation: "Discourse patterns will vary significantly by context: inaugural addresses vs. State of Union speeches vs. party platforms"
  H5_Institutional_Individual_Differences: "Party platforms will show different discourse patterns than individual presidential speeches, revealing institutional vs. personal messaging strategies"
  H6_Framework_Reliability: "The Political Discourse Analysis Framework v6.0 will maintain statistical consistency across the longitudinal corpus while detecting meaningful temporal variations"
---

# American Political Discourse Evolution Study (1992-2025)

## Research Overview
This experiment conducts a comprehensive longitudinal analysis of American political discourse across 33 years, analyzing 65 documents (47 presidential speeches + 18 party platforms) from Clinton, Bush, Obama, Trump, and Biden administrations. The study leverages the Political Discourse Analysis Framework v6.0 to discover when, how, and if populist discourse patterns emerged in American political rhetoric, without predetermined assumptions about "populist eras" - letting the data reveal actual temporal patterns, change points, and discourse evolution.

## Longitudinal Discourse Analysis: How LLMs Will Leverage Metadata

### Temporal Discourse Evolution (1992-2025)
The synthesis agent will receive experiment configuration directing it to perform `temporal_discourse_evolution` analysis. With access to the corpus file_manifest containing temporal_sequence metadata, it can:
- **Chronological analysis**: Track discourse patterns across 63 chronologically ordered documents
- **Change point detection**: Identify statistical inflection points where discourse patterns shift significantly
- **Trend analysis**: Discover if and when populist discourse emerged, evolved, or declined over time

### Change Point Analysis
With `change_point_analysis` in the reporting structure and temporal_sequence metadata in the corpus manifest, the synthesis agent can:
- **Statistical detection**: Use temporal data to identify significant discourse shifts without predetermined assumptions
- **Pattern validation**: Test whether apparent changes are statistically significant or random variation
- **Temporal clustering**: Group documents by actual discourse similarity rather than assumed "eras"

### Presidential Discourse Profiles
The `presidential_discourse_profiles` section combined with president metadata enables:
- **Individual signatures**: Discover each president's unique discourse patterns without assumptions
- **Consistency assessment**: Does each president maintain consistent discourse patterns across multiple speeches?
- **Evolution within presidency**: How does discourse change from first to final speeches of each president?

### Institutional vs Individual Analysis
Using `document_type` metadata (party_platform vs presidential speeches), the synthesis agent can:
- **Compare discourse sources**: How do party platforms differ from individual presidential rhetoric?
- **Institutional patterns**: Do parties maintain consistent discourse across multiple election cycles?
- **Strategic messaging**: How do campaign documents (platforms) differ from governing documents (speeches)?

## LLM Metadata Utilization Strategy

The key insight is that the synthesis agent will receive:
1. **Experiment Configuration**: Directs discovery-focused longitudinal analysis
2. **Framework Metadata**: Provides discourse markers and quadrant classifications
3. **Corpus Manifest**: Provides president, party, year, document_type, temporal_sequence for each document
4. **Aggregated Results**: Axis scores and quadrant classifications linked to temporal metadata

The LLM can then **intelligently cross-reference** these data sources to generate sophisticated discourse pattern discovery without predetermined assumptions about "populist eras."

## Expected Research Insights
1. **Temporal Pattern Discovery**: When (if at all) did populist discourse patterns emerge in American political rhetoric?
2. **Change Point Identification**: Statistical detection of significant discourse shifts across 33 years
3. **Presidential Discourse Signatures**: Unique discourse profiles for each president based on actual patterns
4. **Institutional vs Individual Patterns**: How party platforms differ from individual presidential messaging
5. **Contextual Discourse Variation**: How speech context (inaugural vs SOTU vs platform) shapes discourse
6. **Quadrant Evolution**: Movement between discourse quadrants over time without predetermined expectations
7. **Linguistic Marker Validation**: Evidence of specific discourse markers emerging or declining over time

## Longitudinal Study Validation Criteria
1. **Multi-Evaluation Reliability**: 2 evaluations per document maintain scoring consistency across 65 documents
2. **Temporal Metadata Integration**: Synthesis agent successfully leverages temporal_sequence for chronological analysis
3. **Statistical Rigor**: Change point detection and trend analysis with proper longitudinal testing
4. **Discovery-Focused Reporting**: Structured report demonstrates data-driven pattern discovery
5. **Framework v6.0 Validation**: JSON architecture scales efficiently across 65 documents with enhanced linguistic markers
6. **Unbiased Analysis**: Results reveal actual patterns rather than confirming predetermined assumptions 