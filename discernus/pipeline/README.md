# Discernus Pipeline Package

Production pipeline code for experiment execution and Stage 6 notebook generation.

## Architecture

```
discernus/pipeline/
├── __init__.py                      # Main pipeline exports
└── notebook_generation/             # Stage 6 notebook generation
    ├── __init__.py                  # Notebook generation exports
    ├── notebook_generator.py        # Core generation logic
    ├── template_selector.py         # Framework pattern selection
    └── templates/                   # Template assets
        ├── universal_stage6_template.ipynb  # Master template
        └── patterns/                # Framework-specific patterns
            ├── competitive_dynamics/
            └── two_axis_orthogonal/
```

## Usage

```python
from discernus.pipeline.notebook_generation import generate_stage6_notebook

# Generate Stage 6 notebook after experiment completion
notebook_path = generate_stage6_notebook(
    experiment_results=results,
    framework_path="path/to/framework.yaml",
    job_id="experiment_job_123",
    output_dir="results/experiment_job_123/"
)
```

## Integration

This package integrates with:
- `discernus.experiments.run_experiment` - Automatic Stage 6 handoff
- `discernus.api.main` - API-driven notebook generation
- Framework Specification v3.2 - Universal framework support

## Migration Notes

**Previous Location:** `templates/` (confusing as production code)  
**New Location:** `discernus/pipeline/` (proper Python package)

This reorganization provides:
- ✅ Clear ownership of production code
- ✅ Proper Python package imports
- ✅ Better testing and documentation
- ✅ Standard package management 