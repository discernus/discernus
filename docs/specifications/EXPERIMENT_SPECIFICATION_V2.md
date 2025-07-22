# Experiment Specification (v2.0)

**Version**: 2.0  
**Status**: Active

The `experiment.md` file is a simple, human-readable YAML file that defines the complete scope of an analysis run. It acts as the **single source of truth** for experiment configuration, telling the Discernus system what framework to use, what corpus to analyze, and how to run it.

---

## 1. File Structure

The experiment file MUST be a valid YAML file named `experiment.md` containing a YAML configuration block with the header `# --- Discernus Configuration ---`.

---

## 2. Recommended Project Structure

The system uses a **single-source-of-truth** architecture where the experiment file defines all paths and configuration:

```
my_research_project/
├── framework.md                  # Analytical framework (referenced by experiment)
├── experiment.md                 # Single source of truth for experiment config
└── corpus/                       # Corpus directory (referenced by experiment)
    ├── document_01.txt
    ├── document_02.txt
    └── ...
```

To run an experiment, execute the CLI with a single parameter:

```bash
python3 /path/to/discernus/discernus_cli.py experiment.md
```

The experiment file defines the framework and corpus paths, eliminating parameter conflicts.

---

## 3. Schema

```yaml
---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
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
framework_file: framework.md

# REQUIRED: A relative path to the corpus directory to be analyzed.
corpus: corpus/

# REQUIRED: A list of one or more LiteLLM-compatible model strings.
models:
  - "openai/gpt-4o"
  - "vertex_ai/gemini-2.5-pro"

# REQUIRED: The number of times to run the analysis for each model.
# A value > 1 is required to calculate inter-run reliability statistics.
runs_per_model: 3

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
      failure_threshold: 0.25

  # Step 3: Statistical calculations
  - agent: CalculationAgent
    inputs:
      - analysis_results
    outputs:
      - calculation_results

  # Step 4: Generate final report and artifacts
  - agent: SynthesisAgent
    inputs:
      - calculation_results
    config:
      output_artifacts:
        - final_report.md
        - results.csv

# OPTIONAL: Additional hypotheses for multi-hypothesis experiments
hypotheses:
  H1: "At least two speeches will show statistically significant differences in scores"
  H2: "Framework will maintain inter-run reliability with Cronbach's alpha > 0.70"

---

# Human-Readable Experiment Description

This section contains the full human-readable description of the experiment,
including methodology, expected outcomes, and analysis rationale.
``` 

## 4. Field Specifications

### Required Fields

- **`name`**: Unique identifier for the experiment (snake_case recommended)
- **`description`**: Human-readable purpose statement
- **`hypothesis`**: Primary falsifiable hypothesis being tested  
- **`framework_file`**: Relative path to the framework specification file
- **`corpus`**: Relative path to the corpus directory
- **`models`**: List of LiteLLM-compatible model identifiers
- **`runs_per_model`**: Number of analysis runs per model (integer ≥ 1)
- **`workflow`**: Ordered list of agent execution steps

### Optional Fields

- **`analysis_variant`**: Framework variant to use (defaults to 'default')
- **`hypotheses`**: Additional numbered hypotheses for complex experiments

### Path Resolution

All paths (`framework_file`, `corpus`) are resolved relative to the experiment file's directory.

## 5. CLI Usage

The Discernus CLI uses a **single-parameter pattern** to eliminate configuration conflicts:

```bash
# Run experiment (single source of truth)
python3 discernus_cli.py path/to/experiment.md

# All configuration comes from experiment.md:
# - framework_file: which framework to use
# - corpus: which corpus to analyze  
# - models: which LLMs to run
# - workflow: which agents to execute
```

This eliminates the anti-pattern of potential conflicts between CLI parameters and experiment configuration.

## 6. Migration from v1.x

Previous experiment formats using separate CLI parameters are deprecated:

```bash
# DEPRECATED (v1.x pattern)
python3 discernus_cli.py framework.md experiment.md corpus/

# CURRENT (v2.0 pattern)  
python3 discernus_cli.py experiment.md
```

The experiment file now contains all configuration as the single source of truth. 