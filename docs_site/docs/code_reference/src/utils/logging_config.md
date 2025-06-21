# Logging Config

**Module:** `src.utils.logging_config`
**File:** `/app/src/utils/logging_config.py`
**Package:** `utils`

Centralized logging configuration for Narrative Gravity Analysis.
Implements Epic 1 requirement F: Validation & Logging with structured logs and metrics.

## Dependencies

- `datetime`
- `json`
- `logging`
- `logging.config`
- `pathlib`
- `traceback`
- `typing`

## Table of Contents

### Classes
- [ErrorCodes](#errorcodes)
- [MetricsCollector](#metricscollector)
- [StructuredLogger](#structuredlogger)

### Functions
- [setup_logging](#setup-logging)
- [get_logger](#get-logger)

## Classes

### ErrorCodes

---

### MetricsCollector

Centralized metrics collection for Epic 1 requirement F.
Tracks success/failure rates, API costs, processing times.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `record_ingestion_attempt`
```python
record_ingestion_attempt(self, success: bool, documents: int, chunks: int, validation_errors: int)
```

Record corpus ingestion metrics.

##### `record_job_event`
```python
record_job_event(self, event_type: str, job_id: int)
```

Record job processing events.

##### `record_task_event`
```python
record_task_event(self, event_type: str, task_id: int, api_cost: float)
```

Record task processing events.

##### `record_api_request`
```python
record_api_request(self, success: bool, cost: float, rate_limited: bool)
```

Record API usage metrics.

##### `update_system_health`
```python
update_system_health(self, database_status: str, redis_status: str)
```

Update system health metrics.

##### `increment_metric`
```python
increment_metric(self, metric_name: str, tags: Dict[Any])
```

Increment a metric by 1. Added for backward compatibility with auth system.

##### `get_summary`
```python
get_summary(self) -> Dict[Any]
```

Get summary metrics for monitoring.

---

### StructuredLogger

Structured logger with error codes and stack traces.
Implements Epic 1 requirement F: Validation & Logging.

#### Methods

##### `__init__`
```python
__init__(self, name: str)
```

##### `_log_structured`
```python
_log_structured(self, level: str, message: str, error_code: str, extra_data: Dict[Any], exception: Exception)
```

Log with structured format including error codes and stack traces.

##### `info`
```python
info(self, message: str, extra_data: Dict[Any])
```

Log info message with structured format.

##### `warning`
```python
warning(self, message: str, error_code: str, extra_data: Dict[Any])
```

Log warning with optional error code.

##### `error`
```python
error(self, message: str, error_code: str, extra_data: Dict[Any], exception: Exception)
```

Log error with error code and optional exception details.

##### `critical`
```python
critical(self, message: str, error_code: str, extra_data: Dict[Any], exception: Exception)
```

Log critical error with error code and exception details.

---

## Functions

### `setup_logging`
```python
setup_logging(log_level: str, log_file: str)
```

Configure centralized logging for the entire application.

Args:
    log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_file: Optional file path for log output

---

### `get_logger`
```python
get_logger(name: str) -> [StructuredLogger](src/utils/logging_config.md#structuredlogger)
```

Get a structured logger instance for a module.

---

*Generated on 2025-06-21 20:19:04*