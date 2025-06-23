# Unified Framework Validator

**Module:** `scripts.utilities.unified_framework_validator`
**File:** `/app/scripts/utilities/unified_framework_validator.py`
**Package:** `utilities`

Unified Framework Validator v2.0
===============================

🎯 CONSOLIDATED VALIDATOR - Replaces all fragmented validation systems

Comprehensive framework validation supporting:
- ✅ Dipole-based frameworks (MFT style)
- ✅ Independent wells frameworks (Three Wells style) 
- ✅ YAML format (current standard)
- ✅ Legacy JSON format (migration support)
- ✅ CLI interface for manual validation
- ✅ Importable component for orchestrator integration

Validation Layers:
1. Format Detection & Parsing
2. Structural Validation (architecture-aware)
3. Semantic Consistency Checks
4. Academic Standards Validation
5. Integration & Compatibility Checks

Usage:
    # CLI Interface
    python scripts/utilities/unified_framework_validator.py frameworks/moral_foundations_theory/
    python scripts/utilities/unified_framework_validator.py --all --verbose
    
    # Programmatic Interface  
    from scripts.utilities.unified_framework_validator import UnifiedFrameworkValidator
    validator = UnifiedFrameworkValidator()
    result = validator.validate_framework("frameworks/moral_foundations_theory/")

## Dependencies

- `argparse`
- `dataclasses`
- `datetime`
- `enum`
- `json`
- `math`
- `os`
- `pathlib`
- `re`
- `sys`
- `typing`
- `yaml`

## Table of Contents

### Classes
- [FrameworkArchitecture](#frameworkarchitecture)
- [ValidationSeverity](#validationseverity)
- [ValidationIssue](#validationissue)
- [FrameworkValidationResult](#frameworkvalidationresult)
- [UnifiedFrameworkValidator](#unifiedframeworkvalidator)

### Functions
- [print_validation_report](#print-validation-report)
- [print_summary_report](#print-summary-report)
- [main](#main)

## Classes

### FrameworkArchitecture
*Inherits from: Enum*

Framework architecture types

---

### ValidationSeverity
*Inherits from: Enum*

Validation issue severity levels

---

### ValidationIssue

Individual validation issue

#### Methods

##### `__str__`
```python
__str__(self)
```

---

### FrameworkValidationResult

Comprehensive framework validation results

#### Methods

##### `add_issue`
```python
add_issue(self, severity: [ValidationSeverity](scripts/applications/experiment_validation_utils.md#validationseverity), category: str, message: str, location: str, fix_suggestion: str)
```

Add validation issue

##### `get_issues_by_severity`
```python
get_issues_by_severity(self, severity: [ValidationSeverity](scripts/applications/experiment_validation_utils.md#validationseverity)) -> List[[ValidationIssue](scripts/applications/experiment_validation_utils.md#validationissue)]
```

Get issues of specific severity

##### `get_summary`
```python
get_summary(self) -> Dict[Any]
```

Get issue count summary

---

### UnifiedFrameworkValidator

Unified framework validator supporting multiple architectures and formats.

Consolidates all framework validation logic into single comprehensive system.

#### Methods

##### `__init__`
```python
__init__(self, verbose: bool)
```

##### `validate_framework`
```python
validate_framework(self, framework_path: Union[Any]) -> [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)
```

Main validation entry point.

Args:
    framework_path: Path to framework directory or file
    
Returns:
    FrameworkValidationResult with comprehensive validation results

##### `_detect_and_load_framework`
```python
_detect_and_load_framework(self, framework_path: Path, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> Optional[Dict]
```

Detect framework format and load data

##### `_find_framework_file`
```python
_find_framework_file(self, framework_dir: Path) -> Optional[Path]
```

Find framework file in directory

##### `_detect_architecture`
```python
_detect_architecture(self, framework_data: Dict) -> [FrameworkArchitecture](scripts/utilities/unified_framework_validator.md#frameworkarchitecture)
```

Detect framework architecture from data structure

##### `_validate_structure`
```python
_validate_structure(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate framework structure based on detected architecture

##### `_validate_dipole_structure`
```python
_validate_dipole_structure(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate dipole-based framework structure

##### `_validate_wells_structure`
```python
_validate_wells_structure(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate independent wells framework structure

##### `_validate_legacy_structure`
```python
_validate_legacy_structure(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate legacy JSON framework structure

##### `_validate_semantics`
```python
_validate_semantics(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate semantic consistency

##### `_validate_dipole_semantics`
```python
_validate_dipole_semantics(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate dipole framework semantics

##### `_validate_wells_semantics`
```python
_validate_wells_semantics(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate independent wells semantics

##### `_validate_academic_standards`
```python
_validate_academic_standards(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate academic rigor and standards

##### `_validate_integration`
```python
_validate_integration(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)) -> bool
```

Validate integration compatibility

##### `_extract_framework_metadata`
```python
_extract_framework_metadata(self, framework_data: Dict, result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult))
```

Extract framework metadata for result

##### `_get_nested_value`
```python
_get_nested_value(self, data: Dict, path: str) -> Any
```

Get nested dictionary value using dot notation

##### `_is_valid_citation`
```python
_is_valid_citation(self, citation: str) -> bool
```

Basic citation format validation

##### `validate_all_frameworks`
```python
validate_all_frameworks(self, frameworks_dir: str) -> List[[FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)]
```

Validate all frameworks in directory

---

## Functions

### `print_validation_report`
```python
print_validation_report(result: [FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult), verbose: bool)
```

Print comprehensive validation report

---

### `print_summary_report`
```python
print_summary_report(results: List[[FrameworkValidationResult](scripts/applications/comprehensive_experiment_orchestrator.md#frameworkvalidationresult)])
```

Print summary report for multiple frameworks

---

### `main`
```python
main()
```

CLI main function

---

*Generated on 2025-06-23 10:38:43*