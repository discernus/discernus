# Results

**Module:** `src.analysis.results`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/analysis/results.py`
**Package:** `analysis`

Extract and parse experiment results from the database.
Integrates with existing StatisticalLogger and framework systems.

## Dependencies

- `framework_manager`
- `json`
- `logging`
- `models.models`
- `os`
- `pandas`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `sys`
- `typing`
- `utils.database`
- `utils.statistical_logger`
- `yaml`

## Table of Contents

### Classes
- [ExperimentResultsExtractor](#experimentresultsextractor)

## Classes

### ExperimentResultsExtractor

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize the extractor using both StatisticalLogger and production database.

##### `_get_framework_wells`
```python
_get_framework_wells(self, framework_name: str) -> List[str]
```

Get the list of wells defined for a specific framework.

##### `_get_framework_yaml_path`
```python
_get_framework_yaml_path(self, framework_name: str) -> Optional[str]
```

Map framework name to its YAML file path.

##### `extract_results`
```python
extract_results(self, execution_results: Dict) -> Dict
```

Extract and structure experiment results for enhanced analysis.

Args:
    execution_results: Raw experiment execution results
    
Returns:
    Dictionary containing structured data and metadata

##### `extract_experiment_results_by_name`
```python
extract_experiment_results_by_name(self, experiment_name: str) -> pd.DataFrame
```

Extract experiment results by experiment name from production database.

Args:
    experiment_name: Name of the experiment (e.g., "IDITI_Framework_Validation_Study")
    
Returns:
    DataFrame containing experiment results

##### `extract_experiment_results`
```python
extract_experiment_results(self, experiment_id: str) -> pd.DataFrame
```

Extract experiment results using StatisticalLogger (legacy method).

Args:
    experiment_id: Unique identifier for the experiment
    
Returns:
    DataFrame containing experiment results

##### `validate_data_completeness`
```python
validate_data_completeness(self, df: pd.DataFrame) -> Tuple[Any]
```

Validate data completeness and quality.

Args:
    df: DataFrame containing experiment results
    
Returns:
    Tuple of (is_valid, list_of_issues)

##### `export_to_csv`
```python
export_to_csv(self, df: pd.DataFrame, output_path: str)
```

Export results to CSV file.

Args:
    df: DataFrame to export
    output_path: Path to save CSV file

---

*Generated on 2025-06-21 12:44:47*