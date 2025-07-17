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

# OPTIONAL: Specifies which analysis variant from the framework to run.
# If omitted, the system will use the 'default' variant.
# The available variants are defined in the framework's embedded YAML config.
analysis_variant: descriptive_only
``` 