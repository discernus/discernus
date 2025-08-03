---
version: "7.0"
name: star_wars_bar_nested_nightmare_test
description: |
  Test experiment for the Star Wars Bar exotic framework collection. This experiment
  validates the Nested Nightmare Framework v7.0 against synthetic galactic governance
  texts to stress-test the system's ability to handle deeply hierarchical analytical
  structures while maintaining v7.0 compliance.
  
  This is a controlled test using synthetic content with known ground truth to validate
  that exotic frameworks can achieve creative compliance with Imperial Standards.

hypothesis: |
  The Nested Nightmare Framework will successfully analyze contextual depth across
  multiple hierarchical levels while maintaining gasket architecture compliance.
  Flash Lite may struggle with hierarchical coherence, while Pro models should
  handle the nested complexity effectively.

research_questions:
  - "Can the gasket architecture handle 16+ target keys from deeply nested schemas?"
  - "Does the intelligent extractor successfully parse complex hierarchical JSON output?"
  - "How does Flash Lite performance compare to Pro models on nested analytical tasks?"
  - "Are the derived metrics (contextual depth index, hierarchical coherence index) calculated correctly?"
  - "Does the framework maintain v7.0 compliance while achieving creative complexity?"

success_criteria:
  technical:
    - All 16 target keys successfully extracted from analysis output
    - Derived metrics calculated correctly using specified formulas
    - No gasket architecture violations or parsing errors
    - Statistical analysis completes without column reference errors
  
  data_quality:
    - Contextual scores show appropriate differentiation across hierarchical levels
    - Coherence scores reflect actual cross-level consistency
    - Evidence extraction captures reasoning from each analytical level
    - Confidence scores reflect analytical uncertainty appropriately
  
  framework_validation:
    - Framework passes Validation Agent approval for v7.0 compliance
    - Creative compliance features work as intended
    - No violations of THIN architecture principles
    - System handles exotic features gracefully
  
  model_comparison:
    - Document performance differences between Flash Lite and Pro models
    - Validate that more capable models handle complexity better
    - Identify specific failure modes for lighter models
    - Confirm architectural robustness across model capabilities

framework: "../../frameworks/star_wars_bar/exotic_frameworks/nested_nightmare_v7.0.md"
corpus_path: "corpus/"
model: "vertex_ai/gemini-2.5-pro"
analysis_variant: "default"

workflow:
  version: "7.0"
  architecture: "gasket"
  agents:
    - "EnhancedAnalysisAgent"
    - "IntelligentExtractorAgent" 
    - "ProductionThinSynthesisPipeline"

expected_documents: 1
expected_dimensions: 8
expected_derived_metrics: 3
---