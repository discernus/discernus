# Data Transaction Manager

**Module:** `src.utils.data_transaction_manager`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/utils/data_transaction_manager.py`
**Package:** `utils`

Data Transaction Manager

Implements data integrity validation for experiments:
- Corpus data integrity and content hash verification
- Text encoding and format validation
- Database schema version compatibility
- Data drift detection and prevention

Requirements:
- Any data uncertainty triggers graceful experiment termination
- Content hash mismatches indicate data drift requiring resolution
- Text encoding issues must be resolved before analysis
- Database schema compatibility enforced across experiment lifecycle

## Dependencies

- `chardet`
- `dataclasses`
- `datetime`
- `enum`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `typing`
- `utils.database`

## Table of Contents

### Classes
- [DataValidationResult](#datavalidationresult)
- [DataTransactionState](#datatransactionstate)
- [DataTransactionManager](#datatransactionmanager)

## Classes

### DataValidationResult
*Inherits from: Enum*

Data validation result codes

---

### DataTransactionState

Data transaction state for rollback capability

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### DataTransactionManager

Data Transaction Integrity Manager

Ensures data validity and handles corpus integrity automatically.
Any data uncertainty results in graceful experiment failure.

#### Methods

##### `__init__`
```python
__init__(self, transaction_id: str)
```

##### `validate_corpus_for_experiment`
```python
validate_corpus_for_experiment(self, corpus_specs: List[Dict[Any]]) -> List[[DataTransactionState](src/utils/data_transaction_manager.md#datatransactionstate)]
```

🔒 TRANSACTION INTEGRITY: Validate corpus data for experiment use

Returns list of transaction states with validation results.
CRITICAL: Any data uncertainty should result in experiment termination.

Args:
    corpus_specs: List of corpus specifications from experiment definition
    
Returns:
    List of DataTransactionState with validation results

##### `validate_database_schema`
```python
validate_database_schema(self) -> [DataTransactionState](src/utils/data_transaction_manager.md#datatransactionstate)
```

🔒 DATABASE INTEGRITY: Validate database schema compatibility

Returns:
    DataTransactionState with schema validation result

##### `is_transaction_valid`
```python
is_transaction_valid(self) -> Tuple[Any]
```

🔒 TRANSACTION INTEGRITY: Check if all data validations are valid

Returns:
    Tuple of (is_valid, error_messages)
    is_valid=False means experiment should terminate

##### `generate_rollback_guidance`
```python
generate_rollback_guidance(self) -> Dict[Any]
```

Generate user guidance for fixing data transaction failures

Returns:
    Dictionary with specific guidance for each failed file

##### `rollback_transaction`
```python
rollback_transaction(self) -> bool
```

🔒 ROLLBACK: Undo any data changes made during this transaction

Returns:
    True if rollback successful, False if issues remain

##### `_resolve_corpus_path`
```python
_resolve_corpus_path(self, file_path: str) -> Path
```

Resolve corpus file path to absolute path

##### `_validate_single_file`
```python
_validate_single_file(self, file_path: Path, expected_hash: Optional[str]) -> [DataTransactionState](src/utils/data_transaction_manager.md#datatransactionstate)
```

Validate a single corpus file

##### `_validate_database_corpus`
```python
_validate_database_corpus(self, corpus_id: str) -> Optional[[DataTransactionState](src/utils/data_transaction_manager.md#datatransactionstate)]
```

Validate corpus that exists in database

##### `_calculate_file_hash`
```python
_calculate_file_hash(self, file_path: Path) -> str
```

Calculate SHA256 hash of file content

##### `_log_validation_result`
```python
_log_validation_result(self, state: [DataTransactionState](src/utils/data_transaction_manager.md#datatransactionstate), corpus_id: str)
```

Log detailed validation result

---

*Generated on 2025-06-21 12:44:48*