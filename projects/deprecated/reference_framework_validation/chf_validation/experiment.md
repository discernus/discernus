---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
name: chf_v1_1_reference_framework_validation

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  This experiment validates the functionality of the Constitutional Health Framework (CHF) v1.1
  by testing its ability to differentiate constitutional health patterns across different types 
  of political discourse (constitution-supporting vs constitution-threatening) using its 
  6-dimensional constitutional assessment with salience-enhanced analysis.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  Constitution-supporting political speeches will show significantly different constitutional 
  health patterns than anti-establishment speeches, with supporting speeches scoring higher 
  on constitutional health dimensions (Procedural Legitimacy, Institutional Respect, Systemic 
  Continuity) and anti-establishment speeches scoring higher on constitutional pathology 
  dimensions (Procedural Rejection, Institutional Subversion, Systemic Replacement), as measured 
  by the CHF v1.1 framework's salience-enhanced constitutional assessment.

# REQUIRED: A relative path to the framework file to be used.
framework_file: ../../../frameworks/reference/core/chf_v1.1_salience_enhanced.md

# REQUIRED: A relative path to the corpus directory to be analyzed.
corpus: ../corpus/

# REQUIRED: A list of one or more LiteLLM-compatible model strings.
models:
  - "vertex_ai/gemini-2.5-flash"

# REQUIRED: The number of times to run the analysis for each model.
runs_per_model: 2

# OPTIONAL: Analysis variant to use from the framework (defaults to 'default')
analysis_variant: default

# REQUIRED: A sequence of workflow steps that define the execution pipeline.
workflow:
  # Step 1: Core analysis of the corpus texts
  - agent: AnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - analysis_results
      
  # Step 2: Quality control checkpoint  
  - agent: MethodologicalOverwatchAgent
    config:
      failure_threshold: 0.20
      
  # Step 3: Statistical calculations
  - agent: CalculationAgent
    inputs:
      - analysis_results
    outputs:
      - calculation_results

# OPTIONAL: Additional hypotheses for validation testing
hypotheses:
  H1: "Establishment speeches will score significantly higher on Procedural Legitimacy (mean difference > 0.3)"
  H2: "Anti-establishment speeches will score significantly higher on Institutional Subversion (mean difference > 0.3)" 
  H3: "Framework will maintain inter-run reliability with Cronbach's alpha > 0.70"
  H4: "Salience rankings will reveal constitutional priorities distinct from intensity scores"

---

# CHF v1.1 Reference Framework Validation

This experiment validates the **Constitutional Health Framework (CHF) v1.1 - Salience Enhanced** using a proven 8-speech corpus spanning 62 years (1962-2024) of American political discourse.

## Validation Strategy

The CHF validation leverages the **proven foundation** from `projects/soar_2_cff_poc/` which successfully demonstrated framework validation capabilities:

- **✅ High-Quality Corpus**: 8 carefully selected political speeches representing diverse rhetorical styles and time periods
- **✅ Proven Methodology**: Same corpus and analytical approach that validated CFF and ECF functionality  
- **✅ Reference Implementation**: Builds on working SOAR workflow architecture
- **✅ Unified Validation**: Part of comprehensive 4-framework validation suite (ECF, CAF, CHF, CFF)

## Constitutional Health Focus

**CHF v1.1** measures **6 constitutional dimensions** across health-pathology pairs:

**Constitutional Health Dimensions (3 dimensions)**:
1. **Procedural Legitimacy**: Support for established procedures for political change and governance
2. **Institutional Respect**: Recognition of governing authority and institutional effectiveness  
3. **Systemic Continuity**: Support for constitutional adaptation rather than replacement

**Constitutional Pathology Dimensions (3 dimensions)**:
1. **Procedural Rejection**: Rejection of established procedures in favor of circumvention or force
2. **Institutional Subversion**: Attacks on governing authority and institutional effectiveness
3. **Systemic Replacement**: Calls for constitutional system replacement rather than adaptation

## Cross-System Validation

**Universal Application**: CHF applies across constitutional systems (American document-based, British precedent-based, German Basic Law) by focusing on fundamental constitutional health requirements rather than specific institutional arrangements.

**Key Insight**: All constitutional systems require legitimate procedures, respected institutions, and systemic continuity to maintain democratic governance.

## Expected Results

**Successful validation should demonstrate:**

1. **Framework Functionality**: CHF properly analyzes constitutional health across all 6 dimensions with salience enhancement
2. **Constitutional Differentiation**: Clear distinction between constitution-supporting vs constitution-threatening discourse patterns
3. **Salience Intelligence**: Meaningful differences between constitutional intensity and constitutional salience rankings
4. **Statistical Reliability**: Inter-run consistency with acceptable reliability metrics (α ≥ 0.70)
5. **Evidence Quality**: Meaningful quotations and confidence ratings supporting constitutional assessments

**Success Criteria:**
- All 8 speeches analyzed without errors
- Clear differentiation in constitutional health vs pathology patterns between speech types  
- Salience rankings reveal constitutional priorities distinct from static intensity scores
- Cronbach's alpha ≥ 0.70 for framework reliability
- Meaningful evidence quotations supporting constitutional dimensional assessments

**Constitutional Health Classifications:**
- Optimal Constitutional Health (+0.7 to +1.0): Strong positive across dimensions
- Good Constitutional Health (+0.3 to +0.6): Mostly positive with minor issues
- Mixed Constitutional Health (-0.2 to +0.2): Competing constitutional elements
- Poor Constitutional Health (-0.3 to -0.6): Mostly negative with some resilience
- Constitutional Crisis (-0.7 to -1.0): Strong negative across dimensions

This validation establishes CHF v1.1 as a reliable tool for computational constitutional health analysis with salience-enhanced democratic resilience assessment capabilities. 