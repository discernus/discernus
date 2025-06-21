# Statistical Logger

**Module:** `src.utils.statistical_logger`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/utils/statistical_logger.py`
**Package:** `utils`

Enhanced Statistical Logger with PostgreSQL Backend
Designed for academic research workflows and enterprise analytics

## Dependencies

- `dataclasses`
- `datetime`
- `json`
- `os`
- `pandas`
- `pathlib`
- `psycopg2`
- `psycopg2.extras`
- `pyreadstat`
- `sqlite3`
- `typing`
- `uuid`

## Table of Contents

### Classes
- [RunData](#rundata)
- [JobData](#jobdata)
- [StatisticalLogger](#statisticallogger)

## Classes

### RunData

Individual run data structure - enhanced to capture full LLM interaction

---

### JobData

Multi-run job data structure

---

### StatisticalLogger

Enterprise-grade logging system for narrative gravity analysis
Supports PostgreSQL (preferred) and SQLite (fallback)
Designed for academic research and business intelligence tools

#### Methods

##### `__init__`
```python
__init__(self, pg_config: Dict[Any], db_path: str, prefer_postgresql: bool)
```

Initialize logger with PostgreSQL preference

Args:
    pg_config: PostgreSQL connection config
    db_path: SQLite fallback path
    prefer_postgresql: Use PostgreSQL if available

##### `_get_default_pg_config`
```python
_get_default_pg_config(self) -> Dict[Any]
```

Get default PostgreSQL configuration

##### `_get_connection`
```python
_get_connection(self)
```

Get database connection

##### `execute_query`
```python
execute_query(self, query: str, params: tuple) -> List[tuple]
```

Execute query and return results

##### `_init_postgresql`
```python
_init_postgresql(self)
```

Initialize PostgreSQL with enhanced schema

##### `_init_sqlite`
```python
_init_sqlite(self)
```

Initialize SQLite with enhanced schema (fallback)

##### `log_run`
```python
log_run(self, run_data: [RunData](src/utils/statistical_logger.md#rundata))
```

Log individual run data

##### `log_job`
```python
log_job(self, job_data: [JobData](src/utils/statistical_logger.md#jobdata))
```

Log multi-run job data

##### `log_variance_statistics`
```python
log_variance_statistics(self, job_id: str, well_stats: Dict[Any], framework_info: Dict[Any])
```

Log detailed variance statistics for threshold analysis

##### `log_performance_metrics`
```python
log_performance_metrics(self, job_id: str, model_name: str, framework: str, success_rate: float, avg_cost: float, avg_duration: float, total_variance: float, max_variance: float)
```

Log performance metrics

##### `get_variance_threshold_analysis`
```python
get_variance_threshold_analysis(self) -> Dict[Any]
```

Analyze variance patterns to suggest empirical thresholds

##### `get_model_performance_comparison`
```python
get_model_performance_comparison(self) -> Dict[Any]
```

Compare performance across different models and frameworks

##### `get_full_response_corpus`
```python
get_full_response_corpus(self, filters: Dict[Any]) -> List[Dict]
```

Retrieve full raw response corpus for analysis

Args:
    filters: Dict with optional filters like:
        - model_name: str
        - framework: str
        - speaker: str
        - min_cost: float
        - max_variance: float
        - date_range: tuple of (start_date, end_date)

##### `get_corpus_stats`
```python
get_corpus_stats(self) -> Dict[Any]
```

Get summary statistics of the full response corpus

##### `export_for_academics`
```python
export_for_academics(self, export_format: str, output_dir: str, include_raw_responses: bool) -> Dict[Any]
```

Export data in formats suitable for academic statistical analysis

Args:
    export_format: 'csv', 'spss', 'stata', 'r', 'parquet', 'all'
    output_dir: Directory for export files
    include_raw_responses: Include full text responses
    
Returns:
    Dict mapping format to file path

##### `_get_runs_dataframe`
```python
_get_runs_dataframe(self, include_raw_responses: bool) -> pd.DataFrame
```

Convert runs table to pandas DataFrame

##### `_get_jobs_dataframe`
```python
_get_jobs_dataframe(self) -> pd.DataFrame
```

Convert jobs table to pandas DataFrame

##### `_get_variance_dataframe`
```python
_get_variance_dataframe(self) -> pd.DataFrame
```

Convert variance stats table to pandas DataFrame

##### `_prepare_spss_dataset`
```python
_prepare_spss_dataset(self, df_runs, df_jobs, df_variance) -> pd.DataFrame
```

Prepare dataset optimized for SPSS analysis

##### `_prepare_r_dataset`
```python
_prepare_r_dataset(self, df_runs, df_jobs, df_variance) -> pd.DataFrame
```

Prepare comprehensive dataset for R analysis

##### `_generate_r_script`
```python
_generate_r_script(self, data_file: str, script_file: str)
```

Generate R analysis script for the exported data

##### `get_job_by_id`
```python
get_job_by_id(self, job_id: str) -> Optional[Dict]
```

Retrieve job data by job_id for dashboard generation

##### `get_runs_by_job_id`
```python
get_runs_by_job_id(self, job_id: str) -> List[Dict]
```

Retrieve all runs for a job_id for dashboard generation

##### `get_variance_statistics_by_job_id`
```python
get_variance_statistics_by_job_id(self, job_id: str) -> Optional[Dict]
```

Retrieve variance statistics for a job_id

##### `get_recent_jobs`
```python
get_recent_jobs(self, limit: int) -> List[Dict]
```

Get recent jobs for dashboard selection

##### `get_dashboard_data`
```python
get_dashboard_data(self, job_id: str) -> Optional[Dict]
```

Get complete data needed for dashboard generation from database

---

*Generated on 2025-06-21 12:44:48*