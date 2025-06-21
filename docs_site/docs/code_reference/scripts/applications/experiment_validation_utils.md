# Experiment Validation Utils

**Module:** `scripts.applications.experiment_validation_utils`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/scripts/applications/experiment_validation_utils.py`
**Package:** `applications`

Experiment Validation Utilities

Comprehensive validation utilities for experiment definitions with
clear error messages and actionable guidance for users.

## Dependencies

- `argparse`
- `dataclasses`
- `enum`
- `json`
- `pathlib`
- `re`
- `typing`
- `yaml`

## Table of Contents

### Classes
- [ValidationSeverity](#validationseverity)
- [ValidationIssue](#validationissue)
- [ValidationReport](#validationreport)
- [ExperimentValidator](#experimentvalidator)

### Functions
- [main](#main)

## Classes

### ValidationSeverity
*Inherits from: Enum*

Validation issue severity levels

---

### ValidationIssue

Individual validation issue

---

### ValidationReport

Complete validation report

#### Methods

##### `add_issue`
```python
add_issue(self, severity: [ValidationSeverity](scripts/applications/experiment_validation_utils.md#validationseverity), category: str, message: str, location: str, suggestion: str, example: Optional[str])
```

Add a validation issue

---

### ExperimentValidator

Comprehensive experiment definition validator

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `validate_experiment_file`
```python
validate_experiment_file(self, file_path: Path) -> [ValidationReport](scripts/applications/experiment_validation_utils.md#validationreport)
```

Main validation entry point

##### `_load_experiment_file`
```python
_load_experiment_file(self, file_path: Path) -> Dict[Any]
```

Load experiment file with proper error handling

##### `_validate_experiment_structure`
```python
_validate_experiment_structure(self, data: Dict[Any], file_path: Path)
```

Validate basic experiment structure

##### `_validate_experiment_meta`
```python
_validate_experiment_meta(self, meta: Dict[Any], file_path: Path)
```

Validate experiment metadata

##### `_validate_components_section`
```python
_validate_components_section(self, components: Dict[Any], file_path: Path)
```

Validate components section

##### `_validate_component_item`
```python
_validate_component_item(self, component: Dict[Any], component_type: str, index: int, file_path: Path)
```

Validate individual component item

##### `_validate_framework_component`
```python
_validate_framework_component(self, framework: Dict[Any], location: str)
```

Validate framework component

##### `_validate_framework_file`
```python
_validate_framework_file(self, file_path: Path, parent_location: str)
```

Validate framework file structure

##### `_validate_corpus_component`
```python
_validate_corpus_component(self, corpus: Dict[Any], location: str)
```

Validate corpus component

##### `_validate_model_component`
```python
_validate_model_component(self, model: Dict[Any], location: str)
```

Validate model component

##### `_validate_execution_section`
```python
_validate_execution_section(self, execution: Dict[Any], file_path: Path)
```

Validate execution section

##### `print_report`
```python
print_report(self, show_suggestions: bool)
```

Print formatted validation report

---

## Functions

### `main`
```python
main()
```

CLI entry point for validation utility

---

*Generated on 2025-06-21 12:44:48*