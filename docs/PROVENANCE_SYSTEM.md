# Discernus Provenance System

**Complete Research Transparency and Reproducibility Infrastructure**

The Discernus provenance system provides comprehensive tracking, organization, and preservation of research artifacts to ensure full transparency, reproducibility, and auditability of computational research experiments.

## Overview

The provenance system captures and organizes every aspect of a research run:
- **Complete execution logs** (LLM interactions, system events, costs, errors)
- **All artifacts** with content-addressable storage and dependency tracking
- **Input materials** (experiment specifications, frameworks, corpus files)
- **Analysis outputs** (scores, evidence, statistical results, reports)
- **Git-based persistence** with mode-aware commit messages
- **Self-contained archives** for publication and long-term preservation

## Architecture

### Core Components

1. **ProvenanceOrganizer**: Creates human-readable artifact organization with symlinks to shared cache
2. **EnhancedManifest**: Tracks run metadata, modes, resume capabilities, and artifact dependencies
3. **DirectoryStructureReorganizer**: Transforms flat structure into stakeholder-friendly organization
4. **Git Integration**: Automatic commits with mode-aware messages for version control
5. **Archive System**: Creates self-contained packages for publication and archival

### Storage Architecture

```
projects/experiment/
├── runs/20250910T141608Z/           # Individual run directory
│   ├── data/                        # Analysis-ready CSV files
│   │   ├── scores.csv              # Raw dimensional scores
│   │   ├── evidence.csv            # Supporting evidence quotes
│   │   └── metadata.csv            # Provenance summary
│   ├── outputs/                     # Final outputs
│   │   ├── final_report.md         # Complete synthesis report
│   │   └── statistical_results.json # Mathematical analysis
│   ├── inputs/                      # Input materials (copied for replication)
│   │   ├── experiment.md           # Experiment specification
│   │   ├── framework_file.md       # Framework files
│   │   └── corpus/                 # Corpus files
│   ├── provenance/                  # Audit trail and metadata
│   │   ├── consolidated_provenance.json
│   │   └── input_materials_consolidation.json
│   ├── artifacts/                   # Complete provenance artifacts
│   │   ├── analysis_results/       # Raw LLM outputs
│   │   ├── statistical_results/    # Mathematical computations
│   │   ├── evidence/               # Curated evidence
│   │   └── provenance.json         # Artifact dependency map
│   ├── session_logs/                # Complete execution logs
│   │   ├── logs/                   # All log files
│   │   └── manifest.json           # Execution manifest
│   └── statistical_package/         # Researcher-ready package (when applicable)
│       ├── scores.csv              # Analysis data
│       ├── CODEBOOK.md             # Variable descriptions
│       ├── import_python.py        # Python import script
│       ├── import_r.R              # R import script
│       └── import_stata.do         # STATA import script
├── session/                         # Session-specific logs
└── shared_cache/                    # Content-addressable artifact storage
```

## Run Modes and Provenance

### Standard Mode
- **Purpose**: Complete analysis + synthesis pipeline
- **Commit Message**: `"Complete run: {experiment_name}"`
- **Outputs**: Full analysis, statistical results, synthesis report
- **Provenance**: Complete artifact chain from inputs to final outputs

### Analysis-Only Mode
- **Purpose**: Document analysis with CSV export
- **CLI**: `discernus run --analysis-only`
- **Commit Message**: `"Analysis only: {experiment_name}"`
- **Outputs**: Raw analysis scores, evidence, metadata CSVs
- **Provenance**: Analysis artifacts, input materials, execution logs

### Statistical Preparation Mode
- **Purpose**: Analysis + derived metrics + CSV export for external statistical analysis
- **CLI**: `discernus run --statistical-prep`
- **Commit Message**: `"Statistical prep: {experiment_name}"`
- **Outputs**: Analysis scores, derived metrics, evidence CSVs
- **Provenance**: Analysis and derived metrics artifacts, resume capability metadata
- **Resume**: Can be resumed later with `discernus resume`

### Skip Synthesis Mode
- **Purpose**: Full pipeline including statistical analysis, skip synthesis report
- **CLI**: `discernus run --skip-synthesis`
- **Commit Message**: `"Skip synthesis: {experiment_name}"`
- **Outputs**: Complete statistical analysis without final report
- **Provenance**: Full artifact chain except synthesis outputs

### Resume Mode
- **Purpose**: Resume from statistical preparation to complete synthesis
- **CLI**: `discernus resume`
- **Commit Message**: `"Resume from stats: {experiment_name}"`
- **Outputs**: Synthesis report and final outputs
- **Provenance**: Links to original statistical prep run, complete final artifact chain

## CLI Options

### Core Experiment Commands

```bash
# Standard complete run
discernus run projects/experiment

# Analysis-only mode
discernus run projects/experiment --analysis-only

# Statistical preparation mode (for external analysis)
discernus run projects/experiment --statistical-prep

# Skip synthesis mode
discernus run projects/experiment --skip-synthesis

# Resume from statistical preparation
discernus resume projects/experiment
```

### Git Integration Options

```bash
# Disable automatic Git commits
discernus run projects/experiment --no-auto-commit

# Environment variable to disable auto-commit
export DISCERNUS_NO_AUTO_COMMIT=1
discernus run projects/experiment
```

### Archive Commands

```bash
# Basic archive (input materials, provenance, documentation)
discernus archive projects/experiment/runs/20250910T141608Z

# Complete self-contained archive
discernus archive projects/experiment/runs/20250910T141608Z \
  --include-session-logs \
  --include-artifacts \
  --create-statistical-package

# Archive with all options
discernus archive projects/experiment/runs/20250910T141608Z \
  --include-inputs \
  --include-provenance \
  --include-docs \
  --include-session-logs \
  --include-artifacts \
  --create-statistical-package
```

## Archive System

### Archive Types

1. **Basic Archive**: Input materials, consolidated provenance, documentation
2. **Complete Archive**: Includes session logs and actual artifact content
3. **Statistical Package**: Researcher-ready data package with import scripts

### Archive Contents

- **Input Materials**: Experiment specification, framework files, corpus documents
- **Provenance Data**: Consolidated metadata, execution timeline, cost tracking
- **Session Logs**: Complete LLM interactions, system events, error logs
- **Artifact Content**: Actual files (not symlinks) for complete self-containment
- **Statistical Package**: Ready-to-use data with codebook and import scripts
- **Documentation**: Comprehensive README with methodology and usage instructions

### Self-Contained Archives

Archives created with `--include-artifacts` and `--include-session-logs` are completely self-contained:
- No broken symlinks or external dependencies
- All necessary files for complete replication
- Complete LLM interaction history for transparency
- Full audit trail for research integrity verification

## Git Integration

### Automatic Commits

Every successful run is automatically committed to Git with mode-aware commit messages:

```bash
# Example Git history
git log --oneline
e7fcfff78 Statistical prep: nano_test_experiment
b2a1771ad Analysis only: nano_test_experiment
9528cbef3 Complete run: nano_test_experiment
```

### Commit Message Format

- **Analysis-only**: `"Analysis only: {experiment_name}"`
- **Statistical prep**: `"Statistical prep: {experiment_name}"`
- **Skip synthesis**: `"Skip synthesis: {experiment_name}"`
- **Resume**: `"Resume from stats: {experiment_name}"`
- **Complete**: `"Complete run: {experiment_name}"`

### Git Best Practices

- Commit messages are limited to 50 characters per project guidelines
- Uses `git add --force` to override .gitignore for research preservation
- Includes comprehensive error handling and timeout protection
- Can be disabled with `--no-auto-commit` flag for testing or manual control

## Statistical Package Generation

For statistical preparation and skip synthesis modes, the system generates researcher-ready packages:

### Package Contents

- **Data Files**: `scores.csv`, `evidence.csv`, `metadata.csv`
- **Codebook**: `CODEBOOK.md` with detailed variable descriptions
- **Import Scripts**: 
  - `import_python.py` - Python/pandas import
  - `import_r.R` - R import with proper data types
  - `import_stata.do` - STATA import script
- **Documentation**: `README.md` with usage instructions
- **Metadata**: `package_metadata.json` with generation details

### Usage Example

```python
# Python usage
exec(open('statistical_package/import_python.py').read())
# Now you have: scores_df, evidence_df, metadata_df

# R usage
source('statistical_package/import_r.R')
# Now you have: scores.df, evidence.df, metadata.df

# STATA usage
do statistical_package/import_stata.do
```

## Directory Structure Benefits

### For Researchers
- **`data/`**: Immediate access to analysis-ready CSV files
- **`outputs/`**: Clear separation of final reports and results
- **`statistical_package/`**: Ready-to-use package for external analysis tools

### For Replication Researchers
- **`inputs/`**: All input materials needed for exact replication
- **Self-contained**: No external dependencies or broken symlinks
- **Complete documentation**: Clear methodology and file purposes

### For Auditors
- **`provenance/`**: Dedicated audit trail directory
- **`artifacts/`**: Complete provenance chain with actual content
- **`session_logs/`**: Complete execution logs and LLM interactions
- **Git history**: Version control with clear run identification

## Enhanced Manifest System

The enhanced manifest tracks comprehensive run metadata:

```json
{
  "run_metadata": {
    "run_id": "20250910T141608Z",
    "experiment_name": "nano_test_experiment",
    "start_time": "2025-09-10T14:16:08Z",
    "completion_time": "2025-09-10T14:16:09Z"
  },
  "run_mode": {
    "mode_type": "statistical_prep",
    "statistical_prep": true,
    "analysis_only": false,
    "skip_synthesis": false,
    "resume_from_stats": false
  },
  "resume_capability": {
    "can_resume": true,
    "statistical_prep_completed": true,
    "resume_artifacts": ["analysis_hash_123", "metrics_hash_456"],
    "resume_metadata": {
      "analysis_documents": 2,
      "derived_metrics_completed": true,
      "csv_export_completed": true
    }
  },
  "execution_timeline": {
    "phases_completed": ["validation", "analysis", "derived_metrics"],
    "total_duration": 1.23,
    "phase_timings": {...}
  },
  "artifact_summary": {
    "total_artifacts": 15,
    "artifact_types": {...}
  }
}
```

## Best Practices

### For Researchers

1. **Use appropriate modes**: Choose the right mode for your workflow
   - Analysis-only for quick data exploration
   - Statistical-prep for external statistical analysis
   - Standard for complete research pipeline

2. **Archive important runs**: Create self-contained archives for publication
   ```bash
   discernus archive run_directory --include-session-logs --include-artifacts
   ```

3. **Leverage resume capability**: Use statistical-prep mode for iterative analysis
   ```bash
   discernus run --statistical-prep  # Initial analysis
   discernus resume                  # Complete synthesis later
   ```

### For Replication

1. **Use archived runs**: Always work from archived, self-contained runs
2. **Verify Git history**: Check commit messages to understand run types
3. **Follow documentation**: Use the generated README files for guidance

### For Audit

1. **Review complete logs**: Check `session_logs/` for full execution trace
2. **Verify artifact chain**: Trace dependencies through `artifacts/provenance.json`
3. **Check Git provenance**: Verify commit history and timestamps

## Integration with External Tools

### Statistical Analysis Software

The statistical package is designed for seamless integration:

- **Python/Pandas**: Direct CSV import with proper data types
- **R**: Native data frame import with factor conversion
- **STATA**: Complete import with variable labels and formats
- **SPSS**: CSV import with codebook for variable definitions

### Version Control

- **Git integration**: Automatic commits with descriptive messages
- **Branch strategies**: Supports both same-branch and separate-branch workflows
- **Distributed verification**: Git's distributed nature enables independent verification

### Publication Workflows

- **Self-contained archives**: Ready for supplementary material submission
- **Complete documentation**: Methodology and replication instructions included
- **Audit trails**: Full transparency for peer review and replication

## Troubleshooting

### Common Issues

1. **Git commit failures**: Check repository status and permissions
2. **Archive creation errors**: Verify run directory exists and is complete
3. **Resume failures**: Ensure statistical preparation completed successfully

### Debug Options

```bash
# Disable auto-commit for testing
discernus run --no-auto-commit

# Check run status
discernus archive run_directory  # Basic archive to verify completeness
```

### Log Locations

- **Session logs**: `session/{run_id}/logs/`
- **Application logs**: `session/{run_id}/logs/application.log`
- **Error logs**: `session/{run_id}/logs/errors.log`
- **LLM interactions**: `session/{run_id}/logs/llm_interactions.log`

## Future Enhancements

The provenance system is designed for extensibility:

- **Additional archive formats**: Support for different packaging standards
- **Enhanced metadata**: More detailed execution tracking
- **Integration APIs**: Programmatic access to provenance data
- **Visualization tools**: Graphical representation of artifact dependencies

---

*This documentation reflects the provenance system as implemented in Sprint 12: Statistical Preparation Provenance Integration.*
