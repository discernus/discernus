---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
name: caf_v4_2_reference_framework_validation

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  This experiment validates the functionality of the Character Assessment Framework (CAF) v4.2
  by testing its ability to differentiate moral character patterns across different types 
  of political discourse (dignity-oriented vs tribal, virtue-focused vs vice-focused) using its 
  10-dimensional character assessment with salience-weighted analysis.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  Dignity-oriented political speeches will show significantly different character patterns 
  than tribal speeches, with dignity speeches scoring higher on virtue dimensions (Dignity, 
  Truth, Justice, Hope, Pragmatism) and tribal speeches scoring higher on vice dimensions 
  (Tribalism, Manipulation, Resentment, Fear, Fantasy), as measured by the CAF v4.2 
  framework's salience-weighted character assessment.

# REQUIRED: A relative path to the framework file to be used.
framework_file: ../../../frameworks/reference/core/caf_v4.2_salience_weighted.md

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
  H1: "Dignity-oriented speeches will score significantly higher on Dignity virtue (mean difference > 0.3)"
  H2: "Tribal speeches will score significantly higher on Tribalism vice (mean difference > 0.3)" 
  H3: "Framework will maintain inter-run reliability with Cronbach's alpha > 0.70"
  H4: "Salience-weighted character clusters will show greater differentiation than static weights"

---

# CAF v4.2 Reference Framework Validation

This experiment validates the **Character Assessment Framework (CAF) v4.2 - Salience-Weighted** using a proven 8-speech corpus spanning 62 years (1962-2024) of American political discourse.

## Validation Strategy

The CAF validation leverages the **proven foundation** from `projects/soar_2_cff_poc/` which successfully demonstrated framework validation capabilities:

- **✅ High-Quality Corpus**: 8 carefully selected political speeches representing diverse rhetorical styles and time periods
- **✅ Proven Methodology**: Same corpus and analytical approach that validated CFF and ECF functionality  
- **✅ Reference Implementation**: Builds on working SOAR workflow architecture
- **✅ Unified Validation**: Part of comprehensive 4-framework validation suite (ECF, CAF, CHF, CFF)

## Character Assessment Focus

**CAF v4.2** measures **10 character dimensions** across virtue-vice pairs:

**Civic Virtues (5 dimensions)**:
1. **Dignity**: Recognition of universal human worth and inherent dignity  
2. **Truth**: Commitment to factual accuracy and intellectual honesty
3. **Justice**: Fairness orientation and procedural integrity
4. **Hope**: Constructive vision and democratic optimism  
5. **Pragmatism**: Practical wisdom and workable solutions

**Civic Vices (5 dimensions)**:
1. **Tribalism**: Group loyalty over universal principles
2. **Manipulation**: Deceptive rhetoric and information distortion
3. **Resentment**: Grievance focus and backward-looking blame
4. **Fear**: Anxiety appeals and catastrophic thinking  
5. **Fantasy**: Unrealistic promises and magical thinking

## Expected Results

**Successful validation should demonstrate:**

1. **Framework Functionality**: CAF properly analyzes character across all 10 dimensions with salience weighting
2. **Character Differentiation**: Clear distinction between virtue-oriented vs vice-oriented rhetorical patterns
3. **Salience Intelligence**: Meaningful differences between character intensity and character salience rankings
4. **Statistical Reliability**: Inter-run consistency with acceptable reliability metrics (α ≥ 0.70)
5. **Evidence Quality**: Meaningful quotations and confidence ratings supporting character assessments

**Success Criteria:**
- All 8 speeches analyzed without errors
- Clear differentiation in virtue vs vice character patterns between speech types  
- Salience rankings show different emphasis patterns than static intensity scores
- Cronbach's alpha ≥ 0.70 for framework reliability
- Meaningful evidence quotations supporting character dimensional assessments

This validation establishes CAF v4.2 as a reliable tool for computational character analysis with salience-weighted moral assessment capabilities. 