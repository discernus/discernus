# Experiment Organization Guide

## Experiment Location Strategy

### Research Experiments vs System Experiments

**Research Experiments** (academic studies, validation research):
- Location: `research_workspaces/{PROJECT_NAME}/experiments/`
- Purpose: Specific research projects with academic goals
- Organization: Grouped with related research assets (frameworks, templates, etc.)

**System Experiments** (infrastructure testing, system validation):
- Location: `experiments/`
- Purpose: General system testing and infrastructure validation
- Organization: Project-wide technical experiments

### Standard Experiment Directory Structure

Each completed experiment should follow this organizational pattern:

```
{LOCATION}/
├── {EXPERIMENT_NAME}/
│   ├── README.md                     # Comprehensive experiment documentation
│   ├── checkpoint.json               # Orchestrator execution status
│   ├── {experiment_config}.json      # Original experiment definition
│   ├── results/                      # Primary results package
│   │   ├── experiment_summary.md     # Human-readable comprehensive analysis
│   │   ├── experiment_results.csv    # Statistical analysis ready data
│   │   ├── experiment_results.json   # Structured results for programmatic use
│   │   ├── runs_summary.csv         # Individual analysis run details
│   │   └── complete_package_info.json # Metadata and reproducibility info
│   ├── analysis/                     # Post-experiment analysis workspace
│   │   ├── statistical_analysis/    # R/Python statistical work
│   │   ├── visualizations/          # Generated charts and graphs
│   │   └── interpretations/         # Research interpretations
│   ├── enhanced_analysis/            # Automated enhanced pipeline outputs
│   │   ├── cross_validation/        # Multi-run consistency analysis
│   │   ├── quality_metrics/         # QA system detailed reports
│   │   └── comparative_analysis/    # Framework comparison results
│   └── documentation/               # Additional experiment-specific docs
│       ├── methodology_notes.md     # Methodological decisions
│       ├── issues_encountered.md    # Problems and solutions
│       └── lessons_learned.md       # Insights for future experiments
```

Where `{LOCATION}` is either:
- `research_workspaces/{PROJECT_NAME}/experiments/` for research experiments
- `experiments/` for system experiments

## Key Principles

### 1. **Self-Contained Experiments**
- Each experiment directory contains **everything** related to that experiment
- Results live **with** the experiment, not scattered in separate exports
- Someone can understand and reproduce the experiment from the directory alone

### 2. **Standardized Results Package**
- `results/` directory contains the core outputs in multiple formats
- CSV for statistical software (R, Stata, SPSS)
- JSON for programmatic processing
- Markdown for human documentation
- Metadata for reproducibility

### 3. **Progressive Analysis Structure**
- `analysis/` for human-driven post-experiment work
- `enhanced_analysis/` for automated pipeline outputs
- `documentation/` for methodological and contextual information

### 4. **Academic Standards**
- Every experiment has comprehensive documentation
- Reproducibility information is preserved
- Results are export-ready for academic software
- Methodology is clearly documented

## File Naming Conventions

### Experiment Names
- Format: `{FRAMEWORK}_{STUDY_TYPE}_{VERSION}_{TIMESTAMP}`
- Example: `MFT_Working_Validation_Study_1.0.0_20250620_141620`

### Result Files
- `experiment_summary.md` - Always use this name for main documentation
- `experiment_results.csv` - Always use this name for statistical data
- `experiment_results.json` - Always use this name for structured data
- `complete_package_info.json` - Always use this name for metadata

## Integration with Production Systems

### Orchestrator Integration ✅ **UPDATED**
- **Orchestrator now detects experiment source location** (research workspace vs system)
- **Results automatically placed in same location** as the experiment
- Enhanced analysis pipeline populates `enhanced_analysis/` in the correct location
- Quality assurance reports integrate into results package

### Technical Implementation
The orchestrator includes these key functions:
- `_determine_experiment_output_location()` - Detects source and determines result location
- `determine_experiment_results_location()` - Utility function for other scripts
- Automatic detection of `research_workspaces` path patterns

### Export System Integration
- Academic export system should look for results **in experiment directories**
- Cross-experiment analysis can aggregate from multiple experiment directories
- Publication packages can be built from experiment directory contents
- **Results stay with experiments** regardless of location

## Migration from Old Pattern

### Old (Problematic) Pattern:
```
experiments/{EXPERIMENT_NAME}/
└── checkpoint.json
exports/random_export_directories/
├── results_for_some_experiment/
└── other_scattered_files/
```

### New (Correct) Pattern:
```
experiments/{EXPERIMENT_NAME}/
├── README.md
├── checkpoint.json
├── results/                # Everything here!
└── analysis/
```

## Benefits of This Organization

1. **Findability**: Results are where you'd expect them (with the experiment)
2. **Reproducibility**: Complete experiment context in one location
3. **Academic Standards**: Professional documentation and data export
4. **Scalability**: Pattern works for small tests or large-scale studies
5. **Collaboration**: Easy to share complete experiment packages

## Example Commands

### For Research Experiments:
```bash
# Navigate to research experiment
cd research_workspaces/june_2025_research_dev_workspace/experiments/MFT_Working_Validation_Study_1.0.0_20250620_141620

# View experiment documentation
cat README.md

# Access results for statistical analysis
open results/experiment_results.csv

# Continue analysis in workspace
mkdir analysis/follow_up_study
cd analysis/follow_up_study
```

### For System Experiments:
```bash
# Navigate to system experiment
cd experiments/{SYSTEM_EXPERIMENT_NAME}

# Same structure and commands apply
cat README.md
open results/experiment_results.csv
```

---
*Organizational pattern established June 20, 2025*
*All future experiments should follow this structure* 