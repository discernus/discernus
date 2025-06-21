# Framework Transaction Manager

**Module:** `src.utils.framework_transaction_manager`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/utils/framework_transaction_manager.py`
**Package:** `utils`

Framework Transaction Manager

Implements framework transaction integrity for experiments:
- Framework uncertainty = experiment failure + rollback
- Automatic version detection for changed frameworks
- Database as single source of truth after ingestion
- Comprehensive logging and user guidance

Requirements:
- Any framework validation uncertainty triggers graceful termination
- Framework content changes auto-increment versions
- Complete audit trail of framework decisions

## Dependencies

- `dataclasses`
- `datetime`
- `enum`
- `hashlib`
- `json`
- `logging`
- `models.component_models`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `typing`
- `utils.database`
- `yaml`

## Table of Contents

### Classes
- [FrameworkValidationResult](#frameworkvalidationresult)
- [FrameworkTransactionState](#frameworktransactionstate)
- [FrameworkTransactionManager](#frameworktransactionmanager)

## Classes

### FrameworkValidationResult
*Inherits from: Enum*

Framework validation result codes

---

### FrameworkTransactionState

Framework transaction state for rollback capability

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### FrameworkTransactionManager

Framework Transaction Integrity Manager

Ensures framework validity and handles versioning automatically.
Any uncertainty results in graceful experiment failure.

#### Methods

##### `__init__`
```python
__init__(self, transaction_id: str)
```

##### `validate_framework_for_experiment`
```python
validate_framework_for_experiment(self, framework_name: str, framework_file_path: Optional[Path], expected_version: Optional[str]) -> [FrameworkTransactionState](src/utils/framework_transaction_manager.md#frameworktransactionstate)
```

🔒 TRANSACTION INTEGRITY: Validate framework for experiment use

Returns transaction state with validation result.
CRITICAL: Any uncertainty should result in experiment termination.

Args:
    framework_name: Name of framework to validate
    framework_file_path: Optional path to framework definition file
    expected_version: Optional expected version for validation
    
Returns:
    FrameworkTransactionState with validation result

##### `is_transaction_valid`
```python
is_transaction_valid(self) -> Tuple[Any]
```

🔒 TRANSACTION INTEGRITY: Check if all framework validations are valid

Returns:
    Tuple of (is_valid, error_messages)
    is_valid=False means experiment should terminate

##### `generate_rollback_guidance`
```python
generate_rollback_guidance(self) -> Dict[Any]
```

Generate user guidance for fixing framework transaction failures

Returns:
    Dictionary with specific guidance for each failed framework

##### `rollback_transaction`
```python
rollback_transaction(self) -> bool
```

🔒 ROLLBACK: Undo any framework changes made during this transaction

Returns:
    True if rollback successful, False if issues remain

##### `_get_database_framework`
```python
_get_database_framework(self, framework_name: str, version: Optional[str]) -> Optional[[FrameworkVersion](src/models/component_models.md#frameworkversion)]
```

Get framework from database (single source of truth)

##### `_calculate_framework_hash`
```python
_calculate_framework_hash(self, dipoles_json: Dict, framework_json: Dict) -> str
```

Calculate hash of framework content for change detection

##### `_validate_file_database_consistency`
```python
_validate_file_database_consistency(self, file_path: Path, db_framework: [FrameworkVersion](src/models/component_models.md#frameworkversion)) -> Dict[Any]
```

Validate file content matches database content

##### `_create_new_framework_version`
```python
_create_new_framework_version(self, file_path: Path, framework_name: str, current_version: str) -> Dict[Any]
```

Create new framework version for changed content

##### `_import_framework_to_database`
```python
_import_framework_to_database(self, file_path: Path, framework_name: str, version: str) -> Dict[Any]
```

Import framework from file to database

##### `_generate_next_version`
```python
_generate_next_version(self, current_version: str, framework_name: str) -> str
```

Generate next version number with collision detection for specific framework

##### `_version_exists`
```python
_version_exists(self, session, framework_name: str, version: str) -> bool
```

Check if a version already exists for the specific framework

##### `_log_validation_result`
```python
_log_validation_result(self, state: [FrameworkTransactionState](src/utils/framework_transaction_manager.md#frameworktransactionstate))
```

Log detailed validation result

---

*Generated on 2025-06-21 12:44:48*