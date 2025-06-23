# Execute Experiment Definition

**Module:** `scripts.applications.execute_experiment_definition`
**File:** `/app/scripts/applications/execute_experiment_definition.py`
**Package:** `applications`

Execution Engine for Declarative Experiment Definitions

This script processes JSON experiment definition files and executes 
complete experiments with quality assurance integration.

Usage:
    python3 scripts/execute_experiment_definition.py path/to/experiment.json [options]

## Dependencies

- `argparse`
- `asyncio`
- `dataclasses`
- `datetime`
- `json`
- `math`
- `pathlib`
- `src.academic.data_export`
- `src.api.analysis_service`
- `src.api_clients.direct_api_client`
- `src.corpus.intelligent_ingestion`
- `src.framework_manager`
- `src.models`
- `src.utils.llm_quality_assurance`
- `sys`
- `typing`
- `uuid`

## Table of Contents

### Classes
- [ExperimentExecutionConfig](#experimentexecutionconfig)
- [DeclarativeExperimentExecutor](#declarativeexperimentexecutor)

## Classes

### ExperimentExecutionConfig

Configuration for experiment execution

---

### DeclarativeExperimentExecutor

Execution engine for declarative JSON experiment definitions

#### Methods

##### `__init__`
```python
__init__(self, config: [ExperimentExecutionConfig](scripts/applications/execute_experiment_definition.md#experimentexecutionconfig))
```

##### `log`
```python
log(self, message: str, level: str)
```

Log message with timestamp

##### `_fix_narrative_position`
```python
_fix_narrative_position(self, analysis_result: Dict[Any], framework_id: str) -> Dict[Any]
```

Fix narrative position calculation using correct framework configuration

---

*Generated on 2025-06-23 10:38:43*