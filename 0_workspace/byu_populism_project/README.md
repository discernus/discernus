# BYU Populism Project Workspace

## Overview
This workspace contains experiments for validating computational social science methodologies in collaboration with BYU researchers. The primary focus is replicating and extending the Tamaki & Fuks (2019) Democratic Tension Axis Model using LLM-based discourse analysis.

## Workspace Structure

### Self-Contained Experiments
Each experiment is organized as a **self-contained unit** with everything needed for that specific analysis:

```
experiments/
├── experiment_name/                    # Experiment folder (descriptive name)
│   ├── experiment_name.yaml          # Experiment definition (matches folder name)
│   └── results/                       # All results for this experiment
│       ├── 2025-06-30_11-29-01/     # Timestamped run
│       │   ├── stage6_interactive_analysis.ipynb
│       │   └── run_metadata.json     # Provenance (job ID, models, etc.)
│       └── 2025-06-30_14-33-22/     # Another run
└── another_experiment/
    ├── another_experiment.yaml
    └── results/
```

### Current Experiments
- **`byu_bolsonaro_minimal/`** - Minimal debug configuration (1 speech, 2 models)
- **`byu_bolsonaro_debug/`** - Debug configuration for rapid iteration  
- **`byu_bolsonaro_validation/`** - Full validation experiment

## Experiment Guidelines

### Naming Conventions
- **Experiment folders**: Use descriptive names (e.g., `byu_bolsonaro_minimal`)
- **YAML files**: Must match folder name exactly (e.g., `byu_bolsonaro_minimal.yaml`)
- **Results folders**: Auto-generated with timestamps (`YYYY-MM-DD_HH-MM-SS`)

### File Organization
- **Keep everything together**: Each experiment folder contains its YAML + all results
- **Self-documenting**: YAML filename is meaningful even when separated from folder
- **Chronological results**: Multiple runs are organized by timestamp for easy comparison

## Runtime Behavior

### Experiment Execution
The Discernus runtime automatically:

1. **Discovers experiments** by scanning for `experiment_name/experiment_name.yaml` files
2. **Creates results folders** within each experiment's directory structure
3. **Generates timestamped runs** so multiple executions don't overwrite each other
4. **Preserves provenance** with metadata files linking results to database job IDs

### Stage 6 Handoff
After each successful experiment:
- **Analysis notebook** is auto-generated in the timestamped results folder
- **Run metadata** is saved with job ID, models used, and generation timestamp
- **Jupyter paths** are provided for immediate interactive analysis

### Example Execution
```bash
# Run experiment (from project root)
python3 ../../discernus/experiments/run_experiment.py experiments/byu_bolsonaro_minimal/byu_bolsonaro_minimal.yaml

# Results automatically appear in:
# experiments/byu_bolsonaro_minimal/results/2025-06-30_11-29-01/
```

## Research Workflow Benefits

### Perfect for Collaboration
- **Share one folder** - collaborator gets experiment + all results
- **Version control friendly** - results track with experiment evolution
- **No lost connections** - impossible to separate experiment from its results

### Ideal for Academic Work
- **Publication ready** - each experiment folder is a complete research unit
- **Reproducible** - YAML + results + metadata provide full audit trail
- **Archivable** - zip one folder to preserve entire experiment lineage

### Scales Naturally
- **Individual experiments** stay organized as separate units
- **Multiple runs** accumulate chronologically for comparison
- **Clean workspace** - no global results soup to navigate

## BYU Collaboration Notes

This structure supports the strategic goals for BYU partnership:
- **Demo ready** - experiments run quickly with clear organization
- **Academic validation** - results integrate smoothly with research workflows  
- **Charter customer experience** - professional, research-grade tooling

The self-contained structure demonstrates Discernus value while naturally creating scaling challenges that drive enterprise conversion when researchers have dozens of experiments.

---

**Ready to transform computational social science research! 🚀** 