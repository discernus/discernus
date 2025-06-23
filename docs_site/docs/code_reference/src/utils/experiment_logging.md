# Experiment Logging

**Module:** `src.utils.experiment_logging`
**File:** `/app/src/utils/experiment_logging.py`
**Package:** `utils`

Comprehensive Experiment Logging System for Narrative Gravity Analysis
Phase 5: Integration, Testing & Comprehensive Logging

Extends existing logging infrastructure with research-specific capabilities:
- Academic audit trails for institutional compliance
- Experiment lifecycle tracking with hypothesis validation
- Corpus management logging with integrity validation
- Context propagation quality assurance
- Research ethics and reproducibility tracking

## Dependencies

- `dataclasses`
- `datetime`
- `json`
- `logging_config`
- `pathlib`
- `time`
- `traceback`
- `typing`

## Table of Contents

### Classes
- [ExperimentErrorCodes](#experimenterrorcodes)
- [ExperimentRunMetrics](#experimentrunmetrics)
- [AcademicAuditTrail](#academicaudittrail)
- [ExperimentMetricsCollector](#experimentmetricscollector)
- [ExperimentLogger](#experimentlogger)

### Functions
- [get_experiment_logger](#get-experiment-logger)
- [setup_experiment_logging](#setup-experiment-logging)

## Classes

### ExperimentErrorCodes
*Inherits from: [ErrorCodes](src/utils/logging_config.md#errorcodes)*

Extended error codes for experiment orchestrator (E6000-E6999)

---

### ExperimentRunMetrics

Metrics for experiment execution tracking

---

### AcademicAuditTrail

Academic compliance and audit trail information

---

### ExperimentMetricsCollector
*Inherits from: [MetricsCollector](src/utils/logging_config.md#metricscollector)*

Extended metrics collector for experiment orchestrator

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `start_experiment`
```python
start_experiment(self, experiment_id: str, run_id: str, academic_info: Dict[Any]) -> str
```

Start tracking an experiment run

##### `end_experiment`
```python
end_experiment(self, run_id: str, success: bool)
```

End tracking an experiment run

##### `record_component_validation`
```python
record_component_validation(self, run_id: str, component_type: str, success: bool)
```

Record component validation event

##### `record_auto_registration`
```python
record_auto_registration(self, run_id: str, component_type: str, success: bool)
```

Record auto-registration event

##### `record_corpus_processing`
```python
record_corpus_processing(self, run_id: str, files_count: int, success: bool)
```

Record corpus processing event

##### `record_context_propagation`
```python
record_context_propagation(self, run_id: str, success: bool)
```

Record context propagation event

##### `record_hypothesis_validation`
```python
record_hypothesis_validation(self, run_id: str, hypothesis_count: int)
```

Record hypothesis validation event

##### `record_academic_compliance_check`
```python
record_academic_compliance_check(self, run_id: str, check_type: str, result: bool)
```

Record academic compliance check

##### `get_experiment_summary`
```python
get_experiment_summary(self, run_id: str) -> Dict[Any]
```

Get comprehensive experiment run summary

---

### ExperimentLogger
*Inherits from: [StructuredLogger](src/utils/logging_config.md#structuredlogger)*

Research-specific structured logger for experiment orchestrator

#### Methods

##### `__init__`
```python
__init__(self, name: str, experiment_metrics: [ExperimentMetricsCollector](src/utils/experiment_logging.md#experimentmetricscollector))
```

##### `start_experiment_logging`
```python
start_experiment_logging(self, experiment_id: str, experiment_context: Dict[Any], academic_info: Dict[Any]) -> str
```

Start experiment-scoped logging

##### `end_experiment_logging`
```python
end_experiment_logging(self, success: bool)
```

End experiment-scoped logging

##### `log_component_validation`
```python
log_component_validation(self, component_type: str, component_id: str, success: bool, validation_details: Dict[Any])
```

Log component validation with research context

##### `log_auto_registration`
```python
log_auto_registration(self, component_type: str, component_id: str, success: bool, registration_details: Dict[Any])
```

Log auto-registration events

##### `log_corpus_processing`
```python
log_corpus_processing(self, corpus_id: str, files_processed: int, integrity_checks: Dict[Any], success: bool)
```

Log corpus processing with integrity validation

##### `log_context_propagation`
```python
log_context_propagation(self, context_type: str, success: bool, propagation_details: Dict[Any])
```

Log context propagation events

##### `log_hypothesis_validation`
```python
log_hypothesis_validation(self, hypotheses: List[str], validation_results: Dict[Any])
```

Log hypothesis validation with research context

##### `log_academic_compliance`
```python
log_academic_compliance(self, check_type: str, result: bool, compliance_details: Dict[Any])
```

Log academic compliance checks

##### `log_integrity_validation`
```python
log_integrity_validation(self, file_path: str, expected_hash: str, calculated_hash: str, success: bool)
```

Log file integrity validation

##### `generate_experiment_report`
```python
generate_experiment_report(self, run_id: str) -> Dict[Any]
```

Generate comprehensive experiment report

---

## Functions

### `get_experiment_logger`
```python
get_experiment_logger(name: str) -> [ExperimentLogger](src/utils/experiment_logging.md#experimentlogger)
```

Get experiment logger instance

---

### `setup_experiment_logging`
```python
setup_experiment_logging(log_level: str, log_file: str)
```

Setup experiment logging with extended configuration

---

*Generated on 2025-06-23 10:38:43*