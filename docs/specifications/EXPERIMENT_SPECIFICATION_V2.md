# Experiment Specification (v2.0)

**Version**: 2.0  
**Status**: Active

The `experiment.md` file is a simple, human-readable YAML file that defines the scope of an analysis run. It acts as a set of pointers, telling the Discernus system *what* to run, not *how* to run it. The "how" is defined in the framework file.

---

## 1. File Structure

The experiment file MUST be a valid YAML file named `experiment.md` or `experiment.yaml`.

---

## 2. Recommended Project Structure

While the system is flexible, we recommend the following directory structure for clarity and reproducibility. The `discernus_cli.py` tool is designed to work seamlessly with this layout.

```
my_research_project/
├── framework.md
├── experiment.md
└── corpus/
    ├── document_01.txt
    ├── document_02.txt
    └── ...
```

*   `framework.md`: Defines the "how" – the analytical framework and instructions for the research agents.
*   `experiment.md`: Defines the "what" – points to the framework, corpus, and models for this specific run.
*   `corpus/`: Contains the raw text files to be analyzed.

To run an experiment, you would execute the CLI from the root of your project directory like so:

```bash
python3 /path/to/discernus/discernus_cli.py framework.md experiment.md corpus/
```

---

## 3. Schema

```yaml
# REQUIRED: A unique, machine-readable name for the experiment.
# Use snake_case.
name: my_first_experiment

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  This experiment runs the PDAF v4.1 framework against the Attesor
  corpus to test for speaker identity bias.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  The sentiment scores for texts from Speaker A will be statistically
  indistinguishable from the scores for the same texts from Speaker B
  when speaker identity is sanitized.

# REQUIRED: A relative path to the framework file to be used.
framework: framework.md

# REQUIRED: A relative path to the corpus directory to be analyzed.
# It is the researcher's responsibility to ensure this directory contains
# the correct version of the corpus (e.g., original, sanitized) for their experiment.
corpus: corpus/

# REQUIRED: A list of one or more LiteLLM-compatible model strings.
models:
  - "openai/gpt-4o"
  - "vertex_ai/gemini-2.5-pro"

# REQUIRED: The number of times to run the analysis for each model.
# A value > 1 is required to calculate inter-run reliability statistics.
num_runs: 3

# REQUIRED: A sequence of workflow steps that define the execution pipeline.
# The WorkflowOrchestrator executes these agents in the order they are listed.
# Each agent's output is added to a master 'workflow_state' dictionary,
# making it available to all subsequent agents.
workflow:
  # Step 1: Core analysis of the corpus texts.
  - agent: AnalysisAgent
    # The AnalysisAgent requires no special configuration. It uses the
    # 'analysis_prompt' from the framework file and the 'corpus' and 'models'
    # from this experiment file to perform its work.

  # Step 2: Quality control checkpoint.
  - agent: MethodologicalOverwatchAgent
    config:
      # If the failure rate of the AnalysisAgent runs exceeds this threshold,
      # the workflow will be terminated to save resources.
      failure_threshold: 0.25

  # Step 3: Perform statistical calculations.
  - agent: CalculationAgent
    # The CalculationAgent uses the 'calculation_spec' from the framework
    # file to perform deterministic math on the scores produced by the
    # AnalysisAgent. It requires no additional configuration here.

  # Step 4: Generate the final report and data artifacts.
  - agent: SynthesisAgent
    config:
      # A list of artifacts to be generated.
      output_artifacts:
        - final_report.md
        - results.csv

# OPTIONAL: A plan for statistical tests to be run after the primary analysis.
# This allows researchers to define the statistical methods needed to
# validate their hypotheses.
# DEPRECATION_NOTICE: The 'statistical_plan' block is being deprecated in favor
# of a more robust 'CalculationAgent' and 'SynthesisAgent' workflow.
# This block is maintained for backward compatibility but will be removed in v3.
statistical_plan:
  - test:
      # A human-readable name for this statistical test.
      name: "Test for significant difference between worldviews"

      # Corresponds to a hypothesis defined in the experiment's prose.
      # This creates a clear link between the research question and the method.
      hypothesis_ref: "H1"

      # The statistical method to be used. The system will have a registry
      # of available tests (e.g., 't-test', 'anova', 'cronbachs_alpha').
      method: "t-test"

      # Parameters specific to the chosen method.
      params:
        # The data to be tested. This name MUST correspond to a calculated
        # metric defined in the framework's 'calculations' block.
        data_source: "cff_cohesion_index"

        # The categorical variable to use for grouping the data. This name
        # MUST correspond to a categorical label returned by the framework's
        # analysis_prompt.
        grouping_variable: "worldview"
``` 