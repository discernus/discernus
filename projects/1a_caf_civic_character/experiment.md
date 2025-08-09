---
version: "7.3"
name: "speaker_character_pattern_analysis"
description: |
  This experiment tests the Civic Analysis Framework's ability to detect 
  meaningful differences in character patterns between individual speakers. 
  The analysis focuses on three core objectives: speaker differentiation using 
  the 10 CAF dimensions, identification of unique character signatures across 
  the 5 virtues and 5 vices, and examination of civic character coherence patterns 
  using the Civic Character Index and pattern classifications.

hypothesis: |
  The Civic Analysis Framework will be used to analyze and compare the character 
  profiles of eight political speeches using the 10 character dimensions, revealing 
  distinct character signatures across virtues and vices, and demonstrating variation 
  in civic character coherence patterns as measured by the Civic Character Index 
  and pattern classifications.

framework: "framework.md"
corpus_path: "corpus/"

# REQUIRED: Configuration for the analysis process
analysis:
  # The specific analysis variant to use from the framework file
  variant: "default"
  # List of LiteLLM-compatible model identifiers for analysis
  # Use Pro for analysis (better quality)
  models:
    - "vertex_ai/gemini-2.5-pro"

# OPTIONAL: Configuration for the synthesis process
synthesis:
  # Model to use for the final report synthesis
  # Use Pro for synthesis (better report quality)
  model: "vertex_ai/gemini-2.5-pro"

# Analysis Configuration
analysis:
  evaluations_per_document: 1
  # Use Pro for analysis (better quality)
  models:
    - "vertex_ai/gemini-2.5-pro"

# Synthesis Configuration  
synthesis:
  # Use Pro for synthesis (better report quality)
  model: "vertex_ai/gemini-2.5-pro"

# Statistical Validation  
validation:
  # required_tests: ["speaker_differentiation_anova", "character_signature_analysis", "civic_character_coherence_patterns"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "speaker_differentiation_results"
    - "character_signature_analysis"
    - "civic_character_coherence_patterns"
    - "qualitative_insights"
    - "statistical_methodology"
    - "framework_validation"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Core Hypothesis Framework
hypotheses:
  H1_Speaker_Differentiation: "The 10 CAF dimensions will be used to describe and compare the character profiles of the eight speakers based on the selected speeches"
  H2_Character_Signatures: "Each speech will exhibit a distinct character signature across the 5 virtues and 5 vices"
  H3_Civic_Character_Patterns: "Civic Character Index scores will demonstrate variation across the eight speeches, indicating different levels of character coherence"

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

# --- Definition of Success ---
definition_of_success:
  
  # Technical Success Criteria
  technical_success:
    - "Complete pipeline execution without errors through all workflow agents"
    - "All 8 corpus files analyzed successfully"
    - "Generation of final_report.md and statistical_results.json artifacts"
    - "Valid JSON output from all analysis runs conforming to CAF v7.1 schema"
    - "Successful analysis and synthesis phases"
  
  # Data Quality Success Criteria
  data_quality_success:
    - "Each analysis contains valid character dimension scores (0.0-1.0 scale)"
    - "All 10 CAF dimensions scored independently with confidence ratings"
    - "Evidence quotations provided for each character dimension (minimum 1, maximum 3)"
    - "Overall analysis confidence scores present and reasonable (>0.5 for most analyses)"
    - "Civic Character Index scores calculated and included in analysis results"
  
  # Statistical Reliability Success Criteria
  statistical_reliability_success:
    - "Descriptive statistical analysis shows variation across speeches for at least 3 of 10 CAF dimensions"
    - "Civic Character Index scores show measurable variation across speeches (range ≥ 0.30)"
    - "Character signature analysis reveals distinct patterns for at least 6 of 8 speeches"
    - "Quantitative comparison of character profiles demonstrates framework differentiation capability"
  
  # Framework Validation Success Criteria
  framework_validation_success:
    - "CAF v7.1 framework successfully processes all 8 political speeches"
    - "Character dimensions show appropriate variance (not all clustering around 0.5)"
    - "Virtue and vice dimensions demonstrate expected relationships"
    - "Civic Character Index calculations are mathematically consistent"
    - "Evidence quotations genuinely support assigned character scores"
  
  # Academic Value Success Criteria
  academic_value_success:
    - "Comprehensive final report with methodology, findings, and interpretation"
    - "Statistical analysis including ANOVA results, effect sizes, and significance testing"
    - "Clear presentation of hypotheses H1, H2, H3 with supporting evidence"
    - "Professional formatting with tables, charts, and statistical summaries"
    - "Qualitative insights including profiles of highest and lowest Civic Character Index scoring speeches"
    - "Reproducible results with clear provenance and methodology documentation"
  
  # Minimum Viable Success Threshold
  minimum_viable_success:
    - "At least 7 of 8 corpus files analyzed successfully"
    - "Measurable differences found across speeches for at least 2 of 10 CAF dimensions"
    - "Civic Character Index scores calculated and show variation across speeches"
    - "Final report generated with quantitative results and basic interpretation"
    - "Evidence that the CAF framework can differentiate between speech character profiles"

---

# Speaker Character Pattern Analysis: Core Framework Validation

## Overview

This experiment provides a focused test of the Civic Analysis Framework's core capabilities in detecting meaningful differences between speakers. The analysis examines three fundamental aspects: speaker differentiation using the 10 character dimensions, identification of unique character signatures, and civic character coherence patterns.

## Research Objectives

1. **Speaker Differentiation**: Can the 10 CAF dimensions meaningfully differentiate between speakers?
2. **Character Signature Identification**: Do speakers exhibit unique patterns across the 5 virtues and 5 vices?
3. **Civic Character Analysis**: How do character coherence patterns vary between speakers?

## Methodology

### Framework
**Character Assessment Framework v7.1** provides:
- 10-dimensional character analysis (5 virtues vs 5 vices)
- Civic Character Index and Salience-Weighted Civic Character Index for coherence measurement
- JSON-first architecture with enhanced synthesis integration

### Corpus
8 political speeches from diverse speakers:
- John Lewis - March on Washington speech (1963)
- John McCain - 2008 concession speech
- Mitt Romney - 2020 impeachment speech  
- Cory Booker - 2018 First Step Act speech
- Bernie Sanders - 2025 oligarchy speech
- Alexandria Ocasio-Cortez - 2025 oligarchy speech
- JD Vance - 2022 NatCon conference speech
- Steve King - 2017 House floor speech

### Statistical Analysis
1. **Speech Differentiation Analysis**: Descriptive comparison of character patterns across the eight speeches using all 10 dimensions
2. **Character Signature Analysis**: Identification of unique virtue/vice patterns for each speech
3. **Civic Character Coherence Analysis**: Examination of character coherence variation across speeches

### Qualitative Analysis
1. **Civic Character Extremes Profiling**: Detailed analysis of the speech with the highest Civic Character Index score (most coherent character) and the speech with the lowest Civic Character Index score (least coherent character)
2. **Character Pattern Walkthrough**: Examination of how virtue and vice dimensions interact to produce high vs. low coherence scores
3. **Evidence Integration**: Analysis of specific quotations and rhetorical strategies that contribute to character coherence or contradiction

### Expected Outcomes
1. **Differentiation Evidence**: Statistical confirmation that speakers differ meaningfully on character dimensions
2. **Signature Profiles**: Distinct character patterns for each speaker
3. **Coherence Patterns**: Meaningful variation in Civic Character Index scores across speakers
4. **Qualitative Insights**: Detailed understanding of what produces high vs. low character coherence in political discourse

## Significance

This focused experiment provides essential validation of the Character Assessment Framework's core capabilities. By concentrating on speaker-level analysis, the study will:

1. **Validate Framework Sensitivity**: Demonstrate the framework's ability to capture meaningful variation
2. **Identify Character Signatures**: Reveal distinct character profiles for different political figures
3. **Assess Coherence Patterns**: Examine how character coherence varies between speakers

The simplified design allows for rigorous testing of fundamental framework capabilities while providing clear, interpretable results. 