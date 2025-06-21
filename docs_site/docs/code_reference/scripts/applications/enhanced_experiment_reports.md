# Enhanced Experiment Reports

**Module:** `scripts.applications.enhanced_experiment_reports`
**File:** `/app/scripts/applications/enhanced_experiment_reports.py`
**Package:** `applications`

Enhanced Experiment Report Generator - FIXED VERSION

✅ Uses actual PlotlyCircularVisualizer with proper wells configuration
✅ Checks for existing visualizations from production pipeline first  
✅ Only generates visualizations when production pipeline failed
✅ Uses correct circular visualization interface

## Dependencies

- `argparse`
- `asyncio`
- `datetime`
- `json`
- `markdown`
- `os`
- `pathlib`
- `src.api.analysis_service`
- `src.models`
- `src.visualization.plotly_circular`
- `sys`

## Table of Contents

### Classes
- [EnhancedExperimentReportGenerator](#enhancedexperimentreportgenerator)

## Classes

### EnhancedExperimentReportGenerator

Enhanced experiment report generator with PROPER circular visualization integration.

#### Methods

##### `__init__`
```python
__init__(self, output_base_dir)
```

##### `_load_framework_wells`
```python
_load_framework_wells(self, framework_name: str) -> dict
```

Load wells configuration from framework JSON.

##### `_check_existing_visualizations`
```python
_check_existing_visualizations(self, experiment_id: int) -> dict
```

Check for existing visualizations from production pipeline.

##### `_find_or_create_experiment_dir`
```python
_find_or_create_experiment_dir(self, experiment_id: int) -> Path
```

Find existing experiment directory or create new one.

##### `_extract_comprehensive_data`
```python
_extract_comprehensive_data(self, experiment, runs, session)
```

Extract detailed experiment data.

##### `_find_academic_outputs`
```python
_find_academic_outputs(self, experiment_id: int) -> dict
```

Find existing academic outputs for this experiment.

---

*Generated on 2025-06-21 20:19:04*