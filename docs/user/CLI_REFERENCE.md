# Discernus CLI Reference

**Quick reference for Discernus command-line interface options**

## Core Commands

### `discernus run`

Execute V2 experiments with phase selection and advanced options.

```bash
discernus run [EXPERIMENT_PATH] [OPTIONS]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Phase Selection Options:**
```bash
--from PHASE              # Start from this phase (default: validation)
--to PHASE                # End at this phase (default: synthesis)
```

**Available Phases:**
- `validation` - Experiment structure and coherence validation
- `analysis` - Document analysis and scoring
- `statistical` - Statistical analysis and derived metrics
- `evidence` - Evidence retrieval and fact-checking
- `synthesis` - Final report synthesis

**Advanced Options:**
```bash
--verbose-trace           # Enable comprehensive function-level tracing
--trace-filter COMPONENT # Filter tracing to specific components
--skip-validation         # Skip experiment coherence validation
```

**Examples:**
```bash
# Complete experiment (default)
discernus run projects/experiment

# Analysis and statistical phases only
discernus run projects/experiment --from analysis --to statistical

# Evidence retrieval and synthesis only
discernus run projects/experiment --from evidence --to synthesis

# Validation phase only
discernus run projects/experiment --from validation --to validation

# Debug with tracing
discernus run projects/experiment --verbose-trace --trace-filter statistical
```

### `discernus validate`

Validate experiment structure and configuration.

```bash
discernus validate [EXPERIMENT_PATH]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Output**: Validation results with blocking issues, quality issues, and suggestions.

### `discernus artifacts`

Show experiment artifacts and cache status for resumption.

```bash
discernus artifacts [EXPERIMENT_PATH]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Output**: Recent runs, artifact counts, and cache status.

### `discernus costs`

Show cost breakdown for experiment runs.

```bash
discernus costs [EXPERIMENT_PATH] [OPTIONS]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Options:**
```bash
--detailed              # Show detailed cost breakdown by agent and model
--session               # Show costs for current session only
```

### `discernus status`

Show system status and component availability.

```bash
discernus status
```

**Output**: System components status including Python version, Git, LLM models, and available experiments.

### `discernus export-csv`

Export experiment data to CSV format for further analysis.

```bash
discernus export-csv [EXPERIMENT_PATH] [OPTIONS]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Options:**
```bash
--output FILE              # Output CSV file path (default: export.csv)
```

**Output**: CSV file containing:
- Raw scores for each dimension (raw_score, salience, confidence)
- Derived metrics for each dimension
- Evidence quotes supporting each dimension
- Document identifiers for tracking

**Examples:**
```bash
# Export to default export.csv
discernus export-csv projects/experiment

# Export to custom file
discernus export-csv projects/experiment --output analysis_data.csv
```

## Common Workflows

### Quick Data Exploration
```bash
# Fast analysis for initial exploration
discernus run projects/experiment --from analysis --to statistical

# Check experiment status
discernus validate projects/experiment
```

### Iterative Research
```bash
# Initial analysis and statistical preparation
discernus run projects/experiment --from analysis --to statistical

# Later: complete with synthesis
discernus run projects/experiment --from evidence --to synthesis
```

### Debugging and Troubleshooting
```bash
# Debug with comprehensive tracing
discernus run projects/experiment --verbose-trace --trace-filter statistical

# Check artifacts and cache status
discernus artifacts projects/experiment

# View cost breakdown
discernus costs projects/experiment --detailed
```

### Batch Processing
```bash
# Process multiple experiments
for exp in experiment1 experiment2 experiment3; do
  discernus run projects/$exp --from analysis --to statistical
done

# Later: synthesize selected results
discernus run projects/experiment --from evidence --to synthesis
```

## Phase Details

### Validation Phase
- **Purpose**: Validate experiment structure, framework, and corpus configuration
- **Outputs**: Validation report with issues and suggestions
- **Use Case**: Pre-flight checks before running experiments

### Analysis Phase
- **Purpose**: Analyze documents and generate scores based on framework
- **Outputs**: Analysis results, scores, evidence
- **Use Case**: Core document analysis and scoring

### Statistical Phase
- **Purpose**: Perform statistical analysis and generate derived metrics
- **Outputs**: Statistical results, correlation matrices, reliability measures
- **Use Case**: Quantitative analysis and statistical validation

### Evidence Phase
- **Purpose**: Retrieve and validate evidence for synthesis
- **Outputs**: Evidence retrieval results, fact-checking results
- **Use Case**: Evidence gathering and validation

### Synthesis Phase
- **Purpose**: Generate final research report
- **Outputs**: Synthesis report, final documentation
- **Use Case**: Final report generation and documentation

## Output Directories

### Run Structure
```
projects/experiment/runs/20250910T141608Z/
├── data/                    # Analysis-ready CSV files
├── outputs/                 # Final reports and results
├── inputs/                  # Input materials (for replication)
├── provenance/             # Audit trail and metadata
├── artifacts/              # Complete provenance artifacts
├── session_logs/           # Complete execution logs
└── statistical_package/    # Researcher-ready package (when created)
```

## Error Handling

### Common Issues
```bash
# Skip validation for problematic experiments
discernus run --skip-validation

# Debug with detailed tracing
discernus run projects/experiment --verbose-trace --trace-filter analysis

# Check system status
discernus status
```

### Debug Information
- Session logs: `projects/experiment/runs/{run_id}/session_logs/`
- Error logs: `projects/experiment/runs/{run_id}/logs/errors.log`
- Application logs: `projects/experiment/runs/{run_id}/logs/application.log`

## Model Configuration

### Default Models
- **Analysis**: `vertex_ai/gemini-2.5-flash`
- **Synthesis**: `vertex_ai/gemini-2.5-pro`
- **Validation**: `vertex_ai/gemini-2.5-flash-lite`
- **Statistical**: `vertex_ai/gemini-2.5-pro`

### Model Selection
Model selection is handled automatically by the system based on the phase and task requirements. The V2 architecture uses intelligent model selection to optimize for both cost and performance.

## Environment Variables

### Available Variables
```bash
DISCERNUS_VERBOSE_TRACE=1     # Enable verbose tracing globally
DISCERNUS_SKIP_VALIDATION=1   # Skip validation globally
```

### Usage Example
```bash
# Enable verbose tracing for all runs in session
export DISCERNUS_VERBOSE_TRACE=1
discernus run projects/experiment1
discernus run projects/experiment2
```

---

*For detailed information about the provenance system, see [PROVENANCE_SYSTEM.md](PROVENANCE_SYSTEM.md)*