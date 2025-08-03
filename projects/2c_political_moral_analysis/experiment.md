---
version: "7.0"
name: political_moral_analysis
description: |
  This experiment validates the Moral Foundations Theory v7.0 framework using a diverse corpus 
  of American political speeches spanning 60 years of political discourse. The corpus includes 
  8 speeches from different ideological positions, historical periods (1963-2022), and contexts 
  (electoral, legislative, policy advocacy). This heterogeneous design provides a robust test 
  of the framework's analytical capabilities across varied political discourse contexts while 
  enabling comprehensive moral foundation pattern analysis.
hypothesis: |
  The Moral Foundations Theory v7.0 framework will demonstrate reliable dimensional scoring 
  across diverse political discourse contexts, with measurable variation in moral foundation 
  emphasis patterns between speakers and ideological positions. The framework's tension analysis 
  capabilities will reveal different patterns of moral rhetorical coherence through the Moral 
  Strategic Contradiction Index (MSCI), validating the framework's capacity to detect and 
  quantify moral reasoning patterns in political discourse with statistical confidence.
framework: "framework.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
analysis_variant: default
analysis:
  evaluations_per_document: 2
  statistical_confidence: 0.95
  variance_threshold: 0.15
validation:
  required_tests: ["correlation_analysis", "distribution_analysis", "reliability_analysis"]
  reliability_threshold: 0.70
  effect_size_reporting: true
reporting:
  format: "academic"
  structure:
    - "executive_summary"
    - "hypothesis_testing_results" 
    - "statistical_analysis"
    - "moral_foundation_patterns"
    - "tension_analysis_results"
    - "ideological_variation_analysis"
    - "methodology_notes"
    - "limitations"
  show_statistical_work: true
  include_confidence_metrics: true
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
hypotheses:
  H1_Reliability: "Framework will maintain inter-evaluation reliability with coefficient > 0.70 across all moral foundations"
  H2_Validity: "Moral foundation scores will show expected correlational patterns based on moral psychology theory"
  H3_Consistency: "Multi-evaluation variance will remain below 0.15 threshold across the diverse political corpus"
  H4_Tension_Analysis: "MSCI scores will reveal meaningful patterns of moral coherence/contradiction across ideological positions"
  H5_Ideological_Differentiation: "Moral foundation emphasis patterns will demonstrate measurable variation across progressive, liberal, conservative, and civil rights perspectives"
---

# Political Moral Analysis Experiment

## Overview

This experiment validates the Moral Foundations Theory v6.0 framework using a diverse corpus of American political speeches spanning 60 years of political discourse. The v3.0 experiment specification enables enhanced statistical rigor through multi-evaluation analysis and comprehensive reporting capabilities.

## Research Question

Can computational moral analysis reliably detect and quantify moral foundation patterns across diverse political contexts, speakers, and historical periods with statistical confidence and replicable results?

## Methodology

### Framework
**Moral Foundations Theory v6.0** provides:
- Six moral foundation pairs (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression)
- JSON-first architecture for reliable data generation and synthesis
- Moral Strategic Contradiction Index (MSCI) calculated through explicit mathematical formulas
- Salience-enhanced analysis capturing rhetorical emphasis patterns
- Enhanced reliability through THIN architecture principles

### Enhanced Analysis Features (v3.0)
- **Multi-evaluation**: 2 independent evaluations per document for reliability assessment
- **Statistical validation**: Correlation analysis, distribution analysis, reliability analysis
- **Confidence metrics**: 95% confidence level with variance threshold monitoring
- **Effect size reporting**: Comprehensive statistical documentation

### Corpus Composition
8 diverse political speeches representing:
- **Ideological Spectrum**: Progressive (Sanders, AOC) to Conservative (Romney, McCain, King)
- **Historical Range**: 1963 (Lewis) to 2022 (Vance)
- **Contextual Variety**: Electoral, legislative, policy advocacy, civil rights
- **Quality assurance**: Verified sources, consistent formatting, validated metadata

### Expected Outcomes
1. **Framework Validation**: v6.0 framework successfully processes diverse political discourse with statistical reliability
2. **Ideological Differentiation**: Measurable variation in moral foundation emphasis patterns across political perspectives
3. **Tension Analysis**: MSCI reveals meaningful patterns of moral coherence/contradiction across speakers
4. **Statistical Confidence**: Multi-evaluation approach demonstrates framework reliability with coefficient > 0.70
5. **Methodological Advancement**: Enhanced reporting provides comprehensive academic-quality documentation

## Significance

This experiment establishes the Moral Foundations Theory v6.0 framework as a reliable tool for computational moral analysis in political discourse, providing both theoretical validation and practical demonstration of enhanced statistical capabilities. The v3.0 experiment specification ensures academic-quality rigor suitable for peer review and replication. 