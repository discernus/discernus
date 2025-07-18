---
# --- Discernus Configuration ---
framework_file: ./framework_snapshot.md
analysis_variant: default

# The 'hypotheses' block is a researcher's description of the scientific
# questions being investigated. It is for human consumption and provenance.
hypotheses:
  H1: "At least two of the speeches will show statistically significant differences in CFI scores."
  H2: "At least two of the speeches will show statistically significant similarities in CFI scores even though they express opposed progressive vs conservative worldviews."
  H3: "Six-run analysis of each corpus file using Gemini 2.5 Pro will exhibit a Cronbach's alpha greater than 0.70 for inter-run reliability across all 10 CFF anchors."

# The 'models' list specifies which LLMs to run the analysis with.
# Using single model with multiple runs for robust reliability testing.
models:
  - "vertex_ai/gemini-2.5-pro"

# 'runs_per_model' specifies how many times to run each document through each model,
# which is essential for testing reliability and consistency (see H3).
runs_per_model: 6

# The 'workflow' block defines the sequence of agents to be executed by the
# WorkflowOrchestrator. This is the new, preferred way to define experiments.
workflow:
  - agent: AnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - analysis_results
  - agent: DataExtractionAgent
    inputs:
      - analysis_results
    outputs:
      - extracted_results
  - agent: CalculationAgent
    inputs:
      - extracted_results
    outputs:
      - calculation_results
  - agent: SynthesisAgent
    inputs:
      - calculation_results
    config:
      output_artifacts:
        - final_mva_report.md
        - mva_results.csv

# DEPRECATED: The 'statistical_plan' block is no longer used by the new
# WorkflowOrchestrator. Its functionality is replaced by the 'CalculationAgent'
# and the 'SynthesisAgent' defined in the 'workflow' block above.
statistical_plan:
  - test:
      name: "Test for significant difference in cohesion between worldviews"
      hypothesis_ref: "H1"
      method: "t-test"
      params:
        data_source: "cff_cohesion_index"
        grouping_variable: "worldview"
  - test:
      name: "Test for inter-run reliability across models"
      hypothesis_ref: "H3"
      method: "cronbachs_alpha"
      params:
        # Cronbach's Alpha will be calculated for each of the ten CFF anchors
        # as well as for the calculated cohesion indices.
        data_sources:
          - "tribal_dominance_score"
          - "individual_dignity_score"
          - "fear_score"
          - "hope_score"
          - "envy_score"
          - "compersion_score"
          - "enmity_score"
          - "amity_score"
          - "fragmentative_goal_score"
          - "cohesive_goal_score"
          - "descriptive_cohesion_index"
          - "motivational_cohesion_index"
          - "full_cohesion_index"

# --- Definition of Success ---
definition_of_success:
  
  # Technical Success Criteria
  technical_success:
    - "Complete pipeline execution without errors through all 4 workflow agents"
    - "All 8 corpus files analyzed successfully across 6 runs (48 total analyses)"
    - "Generation of final_mva_report.md and mva_results.csv artifacts"
    - "Valid JSON output from all AnalysisAgent runs conforming to CFF v4.1 schema"
    - "Successful data extraction, calculation, and synthesis phases"
  
  # Fault Tolerance Validation (NEW)
  fault_tolerance_success:
    - "All LLM responses preserved in llm_archive/ with <1ms persistence"
    - "Individual response files (response_001.txt, response_002.txt, etc.) created"
    - "Session chronolog written in real-time with complete audit trail"
    - "Progressive state checkpoints created after each workflow stage"
    - "Zero data loss if experiment is interrupted and resumed"
    - "Clean individual file outputs instead of monolithic JSON blobs"
  
  # Data Quality Success Criteria
  data_quality_success:
    - "Each analysis contains valid worldview classification (Progressive, Conservative, Libertarian, Other)"
    - "All 10 CFF anchors scored independently on 0.0-1.0 scale with confidence ratings"
    - "Approximately 2 direct quotations per anchor as evidence (minimum 1, maximum 4)"
    - "Overall analysis confidence scores present and reasonable (>0.5 for most analyses)"
    - "Competitive pattern identification (Pure Directional, Competitive Tension, Disengaged, Strategic Balance)"
  
  # Statistical Reliability Success Criteria
  statistical_reliability_success:
    - "Cronbach's alpha ≥ 0.70 for at least 7 of the 10 CFF anchors across 6 runs"
    - "Mean inter-run standard deviation ≤ 0.20 for anchor scores within each corpus file"
    - "Calculated cohesion indices (descriptive, motivational, full) mathematically consistent"
    - "Worldview classifications consistent across runs for each corpus file (≥80% agreement)"
  
  # Analytical Richness Success Criteria
  analytical_richness_success:
    - "Detection of at least 3 different competitive patterns across the 8 corpus files"
    - "Clear differentiation between speeches with different rhetorical styles"
    - "Meaningful variation in anchor scores (not clustering around 0.5)"
    - "Evidence quotations that genuinely support the assigned anchor scores"
    - "Worldview diversity across corpus (not all classified as same worldview)"
  
  # Academic Value Success Criteria
  academic_value_success:
    - "Comprehensive final report with methodology, findings, and interpretation"
    - "Statistical analysis including descriptive statistics and reliability measures"
    - "Clear presentation of hypotheses H1, H2, H3 with supporting evidence"
    - "Structured CSV output suitable for further statistical analysis"
    - "Reproducible results with clear provenance and session logging"
  
  # Minimum Viable Success Threshold
  minimum_viable_success:
    - "At least 80% of analyses complete successfully (≥38 of 48 total analyses)"
    - "At least 6 of 8 corpus files analyzed successfully"
    - "Cronbach's alpha ≥ 0.70 for at least 5 of 10 CFF anchors"
    - "Final report generated with quantitative results and basic interpretation"
    - "Evidence that the new WorkflowOrchestrator architecture functions correctly"
    - "Fault tolerance system prevents data loss and enables session resumption"

---

# MVA Experiment 3: CFF Analysis with Fault Tolerance Validation

This document outlines the design for the third experiment in our Minimum Viable Architecture (MVA) test. 

**Primary Objective**: To validate the fault tolerance implementation by executing the complete CFF analysis pipeline with Research Provenance Guide v3.0 architecture.

**Secondary Objective**: To test the newly architected system using a V4.1-spec compliant framework and a real-world corpus to assess single-model consistency and the framework's ability to distinguish between different rhetorical styles through robust reliability testing.

## Experiment Design

This experiment uses **CFF v4.1 independent anchor scoring** to analyze **8 sanitized political speeches** across **6 runs with Gemini 2.5 Pro** (48 total analyses). The focus is on validating **fault tolerance capabilities** while testing **inter-run reliability** rather than inter-model consistency.

## Key Innovations vs. Experiment 2

1. **v3.0 Directory Structure**: Proper session management with llm_archive/, analysis_results/, system_state/
2. **Immediate LLM Persistence**: All responses saved within <1ms to prevent data loss
3. **Individual File Outputs**: Clean extracted results instead of monolithic JSON blobs
4. **Session Resumption**: Complete audit trail enables workflow recovery
5. **Progressive Checkpoints**: State saved after each workflow stage

## Expected Outcomes

**Success** would demonstrate that:
1. The fault tolerance system prevents data loss and enables reliable recovery
2. The new WorkflowOrchestrator architecture executes reliably end-to-end
3. CFF v4.1 independent anchor scoring produces consistent, meaningful results
4. The framework can distinguish rhetorical patterns across different political discourse styles
5. Our reliability testing methodology (Cronbach's alpha) validates framework stability
6. The complete pipeline from analysis → extraction → calculation → synthesis functions correctly

This experiment serves as the **Definition of Done** proof for both our architectural recovery and fault tolerance implementation, validating that all components work together to produce academically rigorous discourse analysis with production-grade reliability.

## Lessons from Experiment 2

**The Disaster**: Experiment 2 failed due to:
- Monolithic JSON blob requiring 2000 lines of Python parsing
- No saved results despite significant LLM processing costs
- Complete workflow failure after analysis phase
- No recovery mechanism for partial results

**The Solution**: Experiment 3 addresses these issues with:
- Individual file persistence for immediate accessibility
- Real-time session logging for complete audit trail
- Progressive checkpoints for partial result recovery
- LLM archive for forensic analysis and replication 