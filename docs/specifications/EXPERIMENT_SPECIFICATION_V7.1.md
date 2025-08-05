# Experiment Specification (v7.1)

**Version**: 7.1  
**Status**: Active - Current Standard

The `experiment.md` file is a YAML file that defines the complete scope of an analysis run. It acts as the **single source of truth** for an experiment, telling the Discernus system what framework to use, what corpus to analyze, and how to conduct the analysis.

---

## 1. File Structure & Location
The experiment file MUST be a valid YAML file named `experiment.md`. It is typically located at the root of a project directory, alongside the corpus and a link to the framework.

```
my_research_project/
├── experiment.md                 # Experiment v7.1
└── corpus/                       # Corpus v7.1
    ├── corpus.md
    └── ...
```

---

## 2. Schema
The file must contain a single YAML configuration block.

```yaml
# A unique, machine-readable name for the experiment.
name: my_temporal_experiment

# A human-readable description of the research goals.
description: |
  A longitudinal analysis of political discourse to identify temporal shifts
  in rhetorical strategies from 2000-2020.

# Falsifiable hypotheses to be tested.
hypotheses:
  H1_Temporal_Shift: "Mean populism scores will be significantly higher post-2016 (group by 'year')."
  H2_Comparative: "The 'longitudinal_analysis' variant will produce richer temporal insights."

# Path to the Framework v7.2 specification file.
framework: "../../frameworks/reference/my_framework_v7.2.md"

# Path to the Corpus v7.1 directory.
corpus_path: "corpus/"

# REQUIRED: Configuration for the analysis process.
analysis:
  # The specific analysis variant to use from the framework file.
  # If omitted, the 'default' variant is used.
  variant: "longitudinal_analysis"

  # List of LiteLLM-compatible model identifiers for analysis.
  models:
    - "vertex_ai/gemini-2.5-pro"

# OPTIONAL: Configuration for the synthesis process.
synthesis:
  # Model to use for the final report synthesis.
  model: "vertex_ai/gemini-2.5-pro"

# Expected outcomes and success criteria for the experiment.
expected_outcomes:
  statistical_analysis:
    - "Temporal trend analysis with change point detection."
    - "Comparative analysis of document types over time."
  quality_metrics:
    - "Framework score extraction success rate > 95%."
```

---

## 3. Field Specifications

### `name`, `description`, `hypotheses`
- **Purpose**: Define the core research objectives of the experiment.
- **Best Practice**: Hypotheses should be specific, measurable, and falsifiable. For temporal analyses, explicitly state the expected time-based patterns and the corpus metadata field to be used (e.g., "group by 'year'").

### `framework` & `corpus_path`
- **Purpose**: Link the experiment to its required assets. Paths should be relative to the `experiment.md` file.

### `analysis` Block
- **`variant` (string)**: Specifies which `analysis_variant` from the framework's JSON appendix to use. This is the key mechanism for selecting a specialized analytical mode, such as temporal analysis. If this field is omitted, the system will use the `default` variant from the framework.
- **`models` (list)**: A list of one or more LiteLLM model identifiers to be used for the analysis phase.

### `synthesis` Block
- **`model` (string)**: The LiteLLM model identifier to be used for the final synthesis report generation.

### `expected_outcomes`
- **Purpose**: Defines the success criteria for the experiment, including the specific statistical analyses to be performed by the Synthesis Agent.
- **Best Practice for Temporal Analysis**: Clearly state the expected temporal outputs, such as "trend analysis," "period-over-period comparison," or "change point detection." This guides the Synthesis Agent in its final report generation.

---

## 4. Defining Temporal Analyses: A Cohesive Approach
Robust temporal analysis requires coordination between the corpus and the experiment.

1.  **The Corpus Provides the Data**: The `corpus.md` manifest must contain reliable temporal metadata, such as `year` and `temporal_sequence`. (See `CORPUS_SPECIFICATION_V7.1.md`)
2.  **The Experiment Defines the Question**: The `experiment.md` formulates time-based hypotheses and specifies the expected temporal outputs.
3.  **The Framework Provides the Lens**: The `framework.md` can optionally provide a specialized `analysis_variant` (e.g., `longitudinal_analysis`) to instruct the LLM to be "time-aware" during its analysis. The experiment then selects this variant using the `analysis.variant` field.

This coordinated approach ensures that the entire system—from data to analysis to synthesis—is aligned to produce a high-quality temporal analysis.

---

## Conclusion
The Experiment Specification v7.1 provides a clear and powerful way to define research runs. By linking the corpus and framework, and by providing a mechanism to select specialized analysis variants, it enables a wide range of sophisticated analyses, including robust temporal studies.
