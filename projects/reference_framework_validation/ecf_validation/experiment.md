---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
name: ecf_v1_reference_framework_validation

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  This experiment validates the functionality of the Emotional Climate Framework (ECF) v1.0
  by testing its ability to differentiate emotional climate patterns across different types 
  of political discourse (dignity vs tribal, conservative vs progressive) using its 
  6-dimensional emotional assessment.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  Dignity-oriented political speeches will show significantly different emotional climate 
  patterns than tribal speeches, with dignity speeches scoring higher on Amity and Hope 
  dimensions, and tribal speeches scoring higher on Enmity and Fear dimensions, as measured 
  by the ECF v1.0 framework's 6-dimensional structure.

# REQUIRED: A relative path to the framework file to be used.
framework_file: ../../../frameworks/reference/core/ecf_v1.0_refined.md

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
  H1: "Dignity-oriented speeches will score significantly higher on Amity (mean difference > 0.3)"
  H2: "Tribal speeches will score significantly higher on Enmity (mean difference > 0.3)" 
  H3: "Framework will maintain inter-run reliability with Cronbach's alpha > 0.70"

---

# ECF v1.0 Reference Framework Validation

This experiment validates the **Emotional Climate Framework (ECF) v1.0** using a proven 8-speech corpus spanning 62 years (1962-2024) of American political discourse.

## Validation Strategy

The ECF validation leverages the **proven foundation** from `projects/soar_2_cff_poc/` which successfully demonstrated framework validation capabilities:

- **✅ High-Quality Corpus**: 8 carefully selected political speeches representing diverse rhetorical styles and time periods
- **✅ Proven Methodology**: Same corpus and analytical approach that validated CFF functionality  
- **✅ Reference Implementation**: Builds on working SOAR workflow architecture
- **✅ Unified Validation**: Part of comprehensive 4-framework validation suite (ECF, CAF, CHF, CFF)

## Expected Results

**Successful validation should demonstrate:**

1. **Framework Functionality**: ECF properly analyzes emotional climate across all 6 dimensions
2. **Discriminative Power**: Clear differentiation between dignity-oriented vs tribal rhetorical patterns
3. **Dimensional Coherence**: Consistent scoring patterns within expected emotional climate profiles
4. **Statistical Reliability**: Inter-run consistency with acceptable reliability metrics
5. **Evidence Quality**: Meaningful quotations and confidence ratings supporting dimensional scores

**Success Criteria:**
- All 8 speeches analyzed without errors
- Clear differentiation in Amity/Enmity and Hope/Fear dimensions between speech types  
- Cronbach's alpha ≥ 0.70 for framework reliability
- Meaningful evidence quotations supporting dimensional assessments

This validation establishes ECF v1.0 as a reliable tool for computational emotional climate analysis. 