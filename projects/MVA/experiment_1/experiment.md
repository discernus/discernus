---
# --- Discernus Configuration ---
framework_file: ./cff_v4_mva.md
analysis_variant: fully_normative

# The 'hypotheses' block is a researcher's description of the scientific
# questions being investigated. It is for human consumption and provenance.
hypotheses:
  H1: "At least two of the speeches will show statistically significant differences in CFI scores."
  H2: "At least two of the speeches will show statistically significant similarities in CFI scores even though they express opposed progressive vs conservative worldviews."
  H3: "Three-run analysis of each corpus file across both GPT-4o and Claude 3.5 Sonnet will exhibit a Cronbach's alpha greater than 0.70 for inter-rater reliability."

# The 'models' list specifies which LLMs to run the analysis with.
# The researcher's choice here overrides any 'default_model' in the framework.
models:
  - "openai/gpt-4o"
  - "claude-3-5-sonnet-20240620"

# 'runs_per_model' specifies how many times to run each document through each model,
# which is essential for testing reliability and consistency (see H3).
runs_per_model: 3

# The 'workflow' block defines the sequence of agents to be executed by the
# WorkflowOrchestrator. This is the new, preferred way to define experiments.
workflow:
  - agent: AnalysisAgent
  - agent: CalculationAgent
  - agent: SynthesisAgent
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
      name: "Test for inter-rater reliability across models"
      hypothesis_ref: "H3"
      method: "cronbachs_alpha"
      params:
        # Cronbach's Alpha will be calculated for each of the five core axis scores
        # as well as for the calculated cohesion index.
        data_sources:
          - "scores.identity_axis"
          - "scores.fear_hope_axis"
          - "scores.envy_compersion_axis"
          - "scores.enmity_amity_axis"
          - "scores.goal_axis"
          - "cff_cohesion_index"
---

# MVA Experiment 1: CFF Analysis of Political Discourse

This document outlines the design for the first experiment in our Minimum Viable Architecture (MVA) test. 

**Objective**: To test the newly architected system using a V4-spec compliant framework and a real-world corpus to assess model consistency and the framework's ability to distinguish between different rhetorical styles. 