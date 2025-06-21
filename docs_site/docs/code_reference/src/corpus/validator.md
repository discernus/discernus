# Validator

**Module:** `src.corpus.validator`
**File:** `/Volumes/dev/discernus/src/corpus/validator.py`
**Package:** `corpus`

Corpus Validator - Integrity checking and FAIR data compliance validation.

Provides:
- File integrity validation (existence, hashes, permissions)
- Metadata completeness checking
- FAIR data principles compliance assessment
- Academic standards validation

## Dependencies

- `dataclasses`
- `datetime`
- `pathlib`
- `re`
- `registry`
- `typing`

## Table of Contents

### Classes
- [ValidationResult](#validationresult)
- [CorpusValidator](#corpusvalidator)

## Classes

### ValidationResult

Results of corpus validation.

#### Methods

##### `summary`
```python
summary(self) -> str
```

Generate human-readable validation summary.

---

### CorpusValidator

Comprehensive corpus validation for integrity and academic standards.

Validates:
- File integrity (existence, content hashes, permissions)
- Metadata completeness and consistency
- FAIR data principles compliance
- Academic citation standards
- Text ID uniqueness and format

#### Methods

##### `__init__`
```python
__init__(self, registry: Optional[[CorpusRegistry](src/corpus/registry.md#corpusregistry)])
```

##### `validate_corpus`
```python
validate_corpus(self, corpus_name: Optional[str]) -> [ValidationResult](src/corpus/validator.md#validationresult)
```

Comprehensive corpus validation.

Args:
    corpus_name: Optional corpus name to validate specific corpus
    
Returns:
    ValidationResult with all validation findings

##### `validate_document`
```python
validate_document(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument)) -> Dict[Any]
```

Validate a single document.

Returns:
    Dictionary with validation issues by category

##### `check_fair_compliance`
```python
check_fair_compliance(self, corpus_name: Optional[str]) -> Dict[Any]
```

Check FAIR data principles compliance.

Returns:
    Dictionary with compliance scores (0.0-1.0) for each FAIR principle

##### `generate_compliance_report`
```python
generate_compliance_report(self, corpus_name: Optional[str]) -> str
```

Generate comprehensive FAIR compliance report.

##### `_validate_file_integrity`
```python
_validate_file_integrity(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), result: [ValidationResult](src/corpus/validator.md#validationresult)) -> bool
```

Validate file exists and content matches hash.

##### `_validate_metadata`
```python
_validate_metadata(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), result: [ValidationResult](src/corpus/validator.md#validationresult)) -> bool
```

Validate required metadata fields.

##### `_validate_text_id`
```python
_validate_text_id(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), result: [ValidationResult](src/corpus/validator.md#validationresult), text_ids_seen: Set[str]) -> bool
```

Validate text_id format and uniqueness.

##### `_check_fair_compliance`
```python
_check_fair_compliance(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), result: [ValidationResult](src/corpus/validator.md#validationresult)) -> None
```

Check FAIR data principles compliance.

##### `_check_academic_standards`
```python
_check_academic_standards(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), result: [ValidationResult](src/corpus/validator.md#validationresult)) -> None
```

Check academic citation and metadata standards.

---

*Generated on 2025-06-21 18:56:11*