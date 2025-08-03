---
version: "7.0"
name: "speaker_character_pattern_analysis"
description: |
  This experiment tests the Character Assessment Framework's ability to detect 
  meaningful differences in character patterns between individual speakers. 
  The analysis focuses on three core objectives: speaker differentiation using 
  the 10 CAF dimensions, identification of unique character signatures across 
  the 5 virtues and 5 vices, and examination of MC-SCI character coherence patterns.

hypothesis: |
  The Character Assessment Framework will successfully differentiate between 
  speakers using the 10 character dimensions, reveal distinct character signatures 
  for each speaker across virtues and vices, and demonstrate meaningful variation 
  in MC-SCI character coherence patterns.

framework: "../../frameworks/reference/core/caf_v7.0.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
analysis_variant: "default"

# Analysis Configuration
analysis:
  evaluations_per_document: 1

# Statistical Validation  
validation:
  required_tests: ["speaker_differentiation_anova", "character_signature_analysis", "mc_sci_coherence_patterns"]
  reliability_threshold: 0.70
  effect_size_reporting: true

# Academic Reporting Configuration
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "speaker_differentiation_results"
    - "character_signature_analysis"
    - "mc_sci_coherence_patterns"
    - "qualitative_insights"
    - "statistical_methodology"
    - "framework_validation"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true

# Core Hypothesis Framework
hypotheses:
  H1_Speaker_Differentiation: "The 10 CAF dimensions will show statistically significant differences between speakers"
  H2_Character_Signatures: "Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices"
  H3_MC_SCI_Patterns: "MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence"

# Required Workflow Steps (v7.0 Gasket Architecture)
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
    - "Valid JSON output from all analysis runs conforming to CAF v6.1 schema"
    - "Successful analysis and synthesis phases"
  
  # Data Quality Success Criteria
  data_quality_success:
    - "Each analysis contains valid character dimension scores (0.0-1.0 scale)"
    - "All 10 CAF dimensions scored independently with confidence ratings"
    - "Evidence quotations provided for each character dimension (minimum 1, maximum 3)"
    - "Overall analysis confidence scores present and reasonable (>0.5 for most analyses)"
    - "MC-SCI scores calculated and included in analysis results"
  
  # Statistical Reliability Success Criteria
  statistical_reliability_success:
    - "ANOVA results show statistically significant differences (p < 0.05) for at least 3 of 10 CAF dimensions"
    - "Effect sizes (η²) ≥ 0.10 for significant speaker differences"
    - "MC-SCI scores show meaningful variation across speakers (SD ≥ 0.15)"
    - "Character signature analysis reveals distinct patterns for at least 6 of 8 speakers"
  
  # Framework Validation Success Criteria
  framework_validation_success:
    - "CAF v6.1 framework successfully processes all 8 political speeches"
    - "Character dimensions show appropriate variance (not all clustering around 0.5)"
    - "Virtue and vice dimensions demonstrate expected relationships"
    - "MC-SCI calculations are mathematically consistent"
    - "Evidence quotations genuinely support assigned character scores"
  
  # Academic Value Success Criteria
  academic_value_success:
    - "Comprehensive final report with methodology, findings, and interpretation"
    - "Statistical analysis including ANOVA results, effect sizes, and significance testing"
    - "Clear presentation of hypotheses H1, H2, H3 with supporting evidence"
    - "Professional formatting with tables, charts, and statistical summaries"
    - "Qualitative insights including profiles of highest and lowest MC-SCI scoring speeches"
    - "Reproducible results with clear provenance and methodology documentation"
  
  # Minimum Viable Success Threshold
  minimum_viable_success:
    - "At least 7 of 8 corpus files analyzed successfully"
    - "Statistically significant differences found for at least 2 of 10 CAF dimensions"
    - "MC-SCI scores calculated and show variation across speakers"
    - "Final report generated with quantitative results and basic interpretation"
    - "Evidence that the CAF framework can differentiate between speakers"

---

# Speaker Character Pattern Analysis: Core Framework Validation

## Overview

This experiment provides a focused test of the Character Assessment Framework's core capabilities in detecting meaningful differences between speakers. The analysis examines three fundamental aspects: speaker differentiation using the 10 character dimensions, identification of unique character signatures, and MC-SCI character coherence patterns.

## Research Objectives

1. **Speaker Differentiation**: Can the 10 CAF dimensions meaningfully differentiate between speakers?
2. **Character Signature Identification**: Do speakers exhibit unique patterns across the 5 virtues and 5 vices?
3. **MC-SCI Analysis**: How do character coherence patterns vary between speakers?

## Methodology

### Framework
**Character Assessment Framework v6.1-Factorial** provides:
- 10-dimensional character analysis (5 virtues vs 5 vices)
- Moral Character Strategic Contradiction Index (MC-SCI) for coherence measurement
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
1. **Speaker Differentiation Analysis**: ANOVA testing for significant differences between speakers across all 10 dimensions
2. **Character Signature Analysis**: Identification of unique virtue/vice patterns for each speaker
3. **MC-SCI Coherence Analysis**: Examination of character coherence variation across speakers

### Qualitative Analysis
1. **MC-SCI Extremes Profiling**: Detailed analysis of the speech with the highest MC-SCI score (most coherent character) and the speech with the lowest MC-SCI score (least coherent character)
2. **Character Pattern Walkthrough**: Examination of how virtue and vice dimensions interact to produce high vs. low coherence scores
3. **Evidence Integration**: Analysis of specific quotations and rhetorical strategies that contribute to character coherence or contradiction

### Expected Outcomes
1. **Differentiation Evidence**: Statistical confirmation that speakers differ meaningfully on character dimensions
2. **Signature Profiles**: Distinct character patterns for each speaker
3. **Coherence Patterns**: Meaningful variation in MC-SCI scores across speakers
4. **Qualitative Insights**: Detailed understanding of what produces high vs. low character coherence in political discourse

## Significance

This focused experiment provides essential validation of the Character Assessment Framework's core capabilities. By concentrating on speaker-level analysis, the study will:

1. **Validate Framework Sensitivity**: Demonstrate the framework's ability to capture meaningful variation
2. **Identify Character Signatures**: Reveal distinct character profiles for different political figures
3. **Assess Coherence Patterns**: Examine how character coherence varies between speakers

The simplified design allows for rigorous testing of fundamental framework capabilities while providing clear, interpretable results. 