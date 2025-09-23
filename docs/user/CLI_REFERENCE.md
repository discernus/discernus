# Discernus CLI Reference

**Quick reference for Discernus command-line interface options**

## Core Commands

### `discernus run`

Execute experiments with various modes and options.

```bash
discernus run [EXPERIMENT_PATH] [OPTIONS]
```

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (defaults to current directory)

**Run Mode Options:**
```bash
--analysis-only          # Run analysis only, export CSV, skip synthesis
--statistical-prep       # Run analysis + derived metrics + CSV export
--skip-synthesis         # Run full pipeline, skip synthesis report
```

**Model Options:**
```bash
--analysis-model MODEL           # LLM model for document analysis
--synthesis-model MODEL          # LLM model for synthesis
--validation-model MODEL         # LLM model for validation
--derived-metrics-model MODEL    # LLM model for statistical analysis
```

**Execution Options:**
```bash
--dry-run                # Preview what would be executed
--skip-validation        # Skip experiment coherence validation
--ensemble-runs N        # Number of ensemble runs (3-5 recommended)
--no-auto-commit         # Disable automatic Git commit
```

**Environment Variables:**
```bash
DISCERNUS_NO_AUTO_COMMIT=1       # Disable auto-commit
DISCERNUS_SKIP_SYNTHESIS=1       # Skip synthesis mode
DISCERNUS_STATISTICAL_PREP=1     # Statistical preparation mode
```

### `discernus list`

List all available experiments with their status.

```bash
discernus list
```

**Output**: Table showing experiment names, paths, and readiness status.

### `discernus status`

Show system status and component availability.

```bash
discernus status
```

**Output**: System components status including Python version, Git, LLM models, and available experiments.

### Resume Functionality

Resume experiments from previous phases using the `run` command with resume flags.

```bash
discernus run [EXPERIMENT_PATH] --resume-from-stats      # Resume from statistical phase
discernus run [EXPERIMENT_PATH] --resume-from-analysis   # Resume from analysis phase
```

**Resume Options:**
```bash
--resume-from-stats              # Resume from statistical phase, skip analysis
--resume-from-analysis            # Resume from analysis phase, skip validation and analysis
```

### `discernus archive`

Create complete golden run archives for research transparency and publication.

```bash
discernus archive RUN_DIRECTORY [OPTIONS]
```

**Arguments:**
- `RUN_DIRECTORY`: Path to completed run directory (e.g., `projects/experiment/runs/20250127T143022Z`)

**Options:**
```bash
--output PATH, -o PATH    # Save archive to specific location
--minimal                 # Create minimal archive (excludes logs and artifacts)
```

**Default Behavior:**
- ✅ **Always includes**: Input materials, consolidated provenance, comprehensive documentation, statistical package
- ✅ **Includes by default**: Session logs, artifact content (unless `--minimal` used)
- 📦 **Result**: Self-contained archive ready for peer review, replication research, and archival

## Run Mode Details

### Standard Mode (Default)
```bash
discernus run projects/experiment
```
- **Process**: Analysis → Derived Metrics → Statistical Analysis → Evidence Retrieval → Synthesis
- **Outputs**: Complete research pipeline with final report
- **Git Commit**: `"Complete run: {experiment_name}"`
- **Use Case**: Full research workflow

### Analysis-Only Mode
```bash
discernus run projects/experiment --analysis-only
```
- **Process**: Analysis → CSV Export
- **Outputs**: `scores.csv`, `evidence.csv`, `metadata.csv`
- **Git Commit**: `"Analysis only: {experiment_name}"`
- **Use Case**: Quick data exploration, preliminary analysis

### Statistical Preparation Mode
```bash
discernus run projects/experiment --statistical-prep
```
- **Process**: Analysis → Derived Metrics → CSV Export
- **Outputs**: Enhanced CSVs with derived metrics
- **Git Commit**: `"Statistical prep: {experiment_name}"`
- **Use Case**: Prepare data for external statistical analysis
- **Resume**: Can be resumed later with `discernus run --resume-from-stats`

### Skip Synthesis Mode
```bash
discernus run projects/experiment --skip-synthesis
```
- **Process**: Analysis → Derived Metrics → Statistical Analysis (no synthesis)
- **Outputs**: Complete statistical analysis without final report
- **Git Commit**: `"Skip synthesis: {experiment_name}"`
- **Use Case**: Custom synthesis workflows, batch processing

### Resume Mode
```bash
discernus run projects/experiment --resume-from-stats
```
- **Process**: Load Statistical Prep → Evidence Retrieval → Synthesis
- **Outputs**: Final synthesis report and complete results
- **Git Commit**: `"Resume from stats: {experiment_name}"`
- **Use Case**: Complete synthesis after statistical preparation

## Archive Examples

### Complete Archive (Default)
```bash
discernus archive projects/experiment/runs/20250910T141608Z
```
- **Includes**: Input materials, provenance data, documentation, statistical package, session logs, artifacts
- **Use case**: Publication, peer review, complete replication research

### Minimal Archive
```bash
discernus archive projects/experiment/runs/20250910T141608Z --minimal
```
- **Includes**: Input materials, provenance data, documentation, statistical package
- **Excludes**: Session logs, artifact content
- **Use case**: Quick sharing, basic preservation, smaller file size

## Common Workflows

### Quick Data Exploration
```bash
# Fast analysis for initial exploration
discernus run projects/experiment --analysis-only --no-auto-commit
```

### External Statistical Analysis
```bash
# Prepare data for R/Python/STATA analysis
discernus run projects/experiment --statistical-prep

# Create complete archive (includes statistical package by default)
discernus archive projects/experiment/runs/LATEST_RUN
```

### Iterative Research
```bash
# Initial statistical preparation
discernus run projects/experiment --statistical-prep

# Later: complete with synthesis
discernus run projects/experiment --resume-from-stats

# Archive final results (complete archive by default)
discernus archive projects/experiment/runs/LATEST_RUN
```

### Publication Preparation
```bash
# Complete run
discernus run projects/experiment

# Create publication-ready archive
discernus archive projects/experiment/runs/LATEST_RUN \
  --output publication_materials/
```

### Batch Processing
```bash
# Process multiple experiments without synthesis
for exp in experiment1 experiment2 experiment3; do
  discernus run projects/$exp --skip-synthesis
done

# Later: synthesize selected results
discernus run projects/experiment --resume-from-stats1
```

## Git Integration

### Automatic Commits
- Every successful run is automatically committed to Git
- Commit messages identify the run mode and experiment
- Can be disabled with `--no-auto-commit`

### Commit Message Format
- **Analysis-only**: `"Analysis only: {experiment_name}"`
- **Statistical prep**: `"Statistical prep: {experiment_name}"`
- **Skip synthesis**: `"Skip synthesis: {experiment_name}"`
- **Resume**: `"Resume from stats: {experiment_name}"`
- **Complete**: `"Complete run: {experiment_name}"`

### Git History Example
```bash
git log --oneline
e7fcfff78 Statistical prep: nano_test_experiment
b2a1771ad Analysis only: nano_test_experiment
9528cbef3 Complete run: nano_test_experiment
```

## Error Handling

### Common Issues
```bash
# Git commit disabled for testing
discernus run --no-auto-commit

# Skip validation for problematic experiments
discernus run --skip-validation

# Dry run to preview execution
discernus run --dry-run
```

### Debug Information
- Session logs: `projects/experiment/session/{run_id}/logs/`
- Error logs: `projects/experiment/session/{run_id}/logs/errors.log`
- Application logs: `projects/experiment/session/{run_id}/logs/application.log`

## Model Configuration

### Default Models
- **Analysis**: `vertex_ai/gemini-2.5-flash`
- **Synthesis**: `vertex_ai/gemini-2.5-pro`
- **Validation**: `vertex_ai/gemini-2.5-flash-lite`
- **Derived Metrics**: `vertex_ai/gemini-2.5-pro`

### Custom Model Examples
```bash
# Use different models for different phases
discernus run projects/experiment \
  --analysis-model vertex_ai/gemini-2.5-pro \
  --synthesis-model vertex_ai/gemini-2.5-flash

# Use experimental models (not in fallback chains)
discernus run projects/experiment \
  --analysis-model vertex_ai/gemini-2.5-experimental
```

## Environment Variables

### Available Variables
```bash
DISCERNUS_NO_AUTO_COMMIT=1       # Disable automatic Git commits
DISCERNUS_SKIP_SYNTHESIS=1       # Enable skip synthesis mode
DISCERNUS_STATISTICAL_PREP=1     # Enable statistical preparation mode
DISCERNUS_DRY_RUN=1             # Enable dry run mode
```

### Usage Example
```bash
# Disable auto-commit for all runs in session
export DISCERNUS_NO_AUTO_COMMIT=1
discernus run projects/experiment1
discernus run projects/experiment2
```

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

### Archive Structure
```
archived_run/
├── GOLDEN_RUN_README.md    # Comprehensive documentation
├── results/                # Consolidated results
├── session_logs/          # Complete execution logs (if included)
├── artifacts/             # Actual artifact content (if included)
└── statistical_package/   # Statistical package (if created)
```

---

*For detailed information about the provenance system, see [PROVENANCE_SYSTEM.md](PROVENANCE_SYSTEM.md)*
