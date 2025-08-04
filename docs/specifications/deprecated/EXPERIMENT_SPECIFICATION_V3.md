# Experiment Specification (v3.0)

**Version**: 3.0  
**Status**: Active  
**Major Change**: Enhanced Analysis and Statistical Reporting Capabilities

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
  This experiment runs the PDAF v5.0 framework against the presidential
  corpus to analyze political discourse patterns with enhanced statistical rigor.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  The framework will demonstrate reliable dimensional scoring across the corpus
  with statistical confidence measures supporting the analytical claims.

# REQUIRED: A relative path to the framework file to be used.
framework_file: framework.md

# REQUIRED: A relative path to the corpus directory to be analyzed.
corpus: corpus/

# REQUIRED: A list of one or more LiteLLM-compatible model strings.
models:
  - "vertex_ai/gemini-2.5-flash-lite"
  - "vertex_ai/gemini-2.5-pro"

# REQUIRED: The number of times to run the analysis for each model.
runs_per_model: 1

# OPTIONAL: Analysis variant to use from the framework (defaults to 'default')
analysis_variant: default

# NEW v3.0: Enhanced analysis configuration
analysis:
  # Multi-evaluation: Number of independent evaluations per document
  evaluations_per_document: 3
  # Statistical confidence level for analysis
  statistical_confidence: 0.95
  # Variance threshold for flagging inconsistent evaluations  
  variance_threshold: 0.15

# NEW v3.0: Statistical validation requirements
validation:
  # Required statistical tests for synthesis to perform
  required_tests: ["correlation_analysis", "distribution_analysis", "reliability_analysis"]
  # Minimum reliability threshold (Cronbach's alpha)
  reliability_threshold: 0.70
  # Include effect size reporting in results
  effect_size_reporting: true

# NEW v3.0: Enhanced reporting configuration  
reporting:
  # Report format: "academic" (comprehensive) or "summary" (concise)
  format: "academic"
  # Report structure sections to include
  structure:
    - "executive_summary"
    - "hypothesis_testing_results" 
    - "statistical_analysis"
    - "qualitative_insights"
    - "methodology_notes"
    - "limitations"
  # Include statistical work documentation
  show_statistical_work: true
  # Include confidence intervals and effect sizes
  include_confidence_metrics: true

# REQUIRED: A sequence of workflow steps that define the execution pipeline.
workflow:
  # Step 1: Enhanced analysis with multi-evaluation
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment
      - framework
      - corpus
    outputs:
      - analysis_results

  # Step 2: Enhanced synthesis with statistical analysis
  - agent: EnhancedSynthesisAgent
    inputs:
      - analysis_results
      - experiment  # Pass full experiment config for reporting guidance
      - framework   # Pass framework for dimension awareness
    outputs:
      - final_report.md
      - results.csv

# OPTIONAL: Additional hypotheses for multi-hypothesis experiments
hypotheses:
  H1_Reliability: "Framework will maintain inter-evaluation reliability with coefficient > 0.70"
  H2_Validity: "Dimensional scores will show expected correlational patterns"
  H3_Consistency: "Multi-evaluation variance will remain below threshold across corpus"

---

# Human-Readable Experiment Description

This section contains the full human-readable description of the experiment,
including methodology, expected outcomes, and analysis rationale. The v3.0
specification enables enhanced statistical rigor through multi-evaluation
analysis and comprehensive reporting capabilities.
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

### New v3.0 Configuration Sections

#### Analysis Configuration
- **`analysis.evaluations_per_document`**: Number of independent evaluations per document (default: 1)
- **`analysis.statistical_confidence`**: Confidence level for statistical analysis (default: 0.95)
- **`analysis.variance_threshold`**: Threshold for flagging evaluation inconsistencies (default: 0.20)

#### Validation Configuration  
- **`validation.required_tests`**: Statistical tests synthesis agent should perform
- **`validation.reliability_threshold`**: Minimum acceptable reliability coefficient
- **`validation.effect_size_reporting`**: Include effect size metrics in results

#### Reporting Configuration
- **`reporting.format`**: "academic" (comprehensive) or "summary" (concise)
- **`reporting.structure`**: List of report sections to include
- **`reporting.show_statistical_work`**: Document statistical methodology (default: true)
- **`reporting.include_confidence_metrics`**: Include confidence intervals and effect sizes

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

## 6. Migration Guide

### From v2.0 to v3.0

The v3.0 specification is backward compatible with v2.0 experiments. New features are optional and use sensible defaults:

```yaml
# v2.0 experiment (still works)
name: my_experiment
models: ["vertex_ai/gemini-2.5-flash-lite"]
runs_per_model: 1

# v3.0 enhanced experiment (new capabilities)
name: my_experiment  
models: ["vertex_ai/gemini-2.5-flash-lite"]
runs_per_model: 1
analysis:
  evaluations_per_document: 3  # NEW: Multi-evaluation
reporting:
  format: "academic"           # NEW: Enhanced reporting
```

### From v1.x to v3.0

Previous experiment formats using separate CLI parameters are deprecated:

```bash
# DEPRECATED (v1.x pattern)
python3 discernus_cli.py framework.md experiment.md corpus/

# CURRENT (v3.0 pattern)  
python3 discernus_cli.py experiment.md
```

## 7. Implementation Notes

### Multi-Evaluation Analysis
When `analysis.evaluations_per_document > 1`, the analysis agent performs multiple independent evaluations of each document. This enables:
- Reliability assessment through inter-evaluation consistency
- Confidence interval calculation for dimensional scores  
- Detection of evaluation variance beyond acceptable thresholds

### Statistical Enhancement
The v3.0 specification enables synthesis agents to perform rigorous statistical analysis by:
- Accessing experiment configuration for reporting guidance
- Using framework metadata (dimension_groups, calculation_spec) for intelligent analysis
- Generating statistical work documentation for academic transparency

### Backward Compatibility
All v2.0 experiments continue to work unchanged. New v3.0 features activate only when explicitly configured, ensuring smooth migration paths for existing research projects. 