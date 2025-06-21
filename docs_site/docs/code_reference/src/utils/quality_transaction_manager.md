# Quality Transaction Manager

**Module:** `src.utils.quality_transaction_manager`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/utils/quality_transaction_manager.py`
**Package:** `utils`

Quality Transaction Manager

Implements analysis quality validation for experiments:
- Analysis quality threshold enforcement
- Framework fit score validation
- Statistical significance requirement verification
- LLM response quality assessment

Requirements:
- Any quality uncertainty triggers graceful experiment termination
- Framework fit scores below thresholds indicate invalid analysis
- Statistical significance requirements must be met for meaningful results
- LLM response quality must meet academic standards

## Dependencies

- `dataclasses`
- `datetime`
- `enum`
- `json`
- `logging`
- `re`
- `statistics`
- `typing`

## Table of Contents

### Classes
- [QualityValidationResult](#qualityvalidationresult)
- [QualityThresholds](#qualitythresholds)
- [QualityTransactionState](#qualitytransactionstate)
- [QualityTransactionManager](#qualitytransactionmanager)

## Classes

### QualityValidationResult
*Inherits from: Enum*

Quality validation result codes

---

### QualityThresholds

Quality threshold configuration

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### QualityTransactionState

Quality transaction state for rollback capability

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### QualityTransactionManager

Quality Transaction Integrity Manager

Ensures analysis quality meets academic standards.
Any quality uncertainty results in graceful experiment failure.

#### Methods

##### `__init__`
```python
__init__(self, transaction_id: str, thresholds: [QualityThresholds](src/utils/quality_transaction_manager.md#qualitythresholds))
```

##### `validate_framework_fit_scores`
```python
validate_framework_fit_scores(self, analysis_results: Dict[Any]) -> List[[QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)]
```

🔒 TRANSACTION INTEGRITY: Validate framework fit scores

Args:
    analysis_results: Dictionary containing analysis results with fit scores
    
Returns:
    List of QualityTransactionState with validation results

##### `validate_statistical_significance`
```python
validate_statistical_significance(self, analysis_results: Dict[Any]) -> List[[QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)]
```

🔒 TRANSACTION INTEGRITY: Validate statistical significance requirements

Args:
    analysis_results: Dictionary containing statistical analysis results
    
Returns:
    List of QualityTransactionState with validation results

##### `validate_llm_response_quality`
```python
validate_llm_response_quality(self, llm_responses: List[Dict[Any]]) -> List[[QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)]
```

🔒 TRANSACTION INTEGRITY: Validate LLM response quality

Args:
    llm_responses: List of LLM response dictionaries
    
Returns:
    List of QualityTransactionState with validation results

##### `validate_analysis_variance`
```python
validate_analysis_variance(self, analysis_results: Dict[Any]) -> List[[QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)]
```

🔒 TRANSACTION INTEGRITY: Validate analysis result variance

Args:
    analysis_results: Dictionary containing analysis results with variance measures
    
Returns:
    List of QualityTransactionState with validation results

##### `is_transaction_valid`
```python
is_transaction_valid(self) -> Tuple[Any]
```

🔒 TRANSACTION INTEGRITY: Check if all quality validations are valid

Returns:
    Tuple of (is_valid, error_messages)
    is_valid=False means experiment should terminate

##### `generate_rollback_guidance`
```python
generate_rollback_guidance(self) -> Dict[Any]
```

Generate user guidance for fixing quality transaction failures

Returns:
    Dictionary with specific guidance for each failed quality check

##### `rollback_transaction`
```python
rollback_transaction(self) -> bool
```

🔒 ROLLBACK: Undo any analysis changes made during this transaction

Returns:
    True if rollback successful, False if issues remain

##### `_extract_fit_scores`
```python
_extract_fit_scores(self, analysis_results: Dict[Any]) -> Dict[Any]
```

Extract framework fit scores from analysis results

##### `_extract_statistical_measures`
```python
_extract_statistical_measures(self, analysis_results: Dict[Any]) -> Dict[Any]
```

Extract statistical significance measures from analysis results

##### `_extract_variance_measures`
```python
_extract_variance_measures(self, analysis_results: Dict[Any]) -> Dict[Any]
```

Extract variance measures from analysis results

##### `_validate_response_length`
```python
_validate_response_length(self, response: Dict[Any], response_id: str) -> [QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)
```

Validate LLM response length

##### `_validate_response_coherence`
```python
_validate_response_coherence(self, response: Dict[Any], response_id: str) -> [QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)
```

Validate LLM response coherence

##### `_validate_response_completeness`
```python
_validate_response_completeness(self, response: Dict[Any], response_id: str) -> [QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate)
```

Validate LLM response completeness

##### `_calculate_coherence_score`
```python
_calculate_coherence_score(self, content: str) -> float
```

Calculate coherence score based on structural indicators

##### `_calculate_completeness_score`
```python
_calculate_completeness_score(self, content: str) -> float
```

Calculate completeness score based on expected elements

##### `_get_coherence_indicators`
```python
_get_coherence_indicators(self, content: str) -> Dict[Any]
```

Get detailed coherence indicators for debugging

##### `_get_completeness_indicators`
```python
_get_completeness_indicators(self, content: str) -> Dict[Any]
```

Get detailed completeness indicators for debugging

##### `_log_validation_result`
```python
_log_validation_result(self, state: [QualityTransactionState](src/utils/quality_transaction_manager.md#qualitytransactionstate))
```

Log detailed validation result

---

*Generated on 2025-06-21 12:44:48*