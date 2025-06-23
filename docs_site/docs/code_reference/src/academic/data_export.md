# Data Export

**Module:** `src.academic.data_export`
**File:** `/app/src/academic/data_export.py`
**Package:** `academic`

Academic Data Export Pipeline

Converts experimental data from PostgreSQL into publication-ready formats
for statistical analysis in R, Stata, Python, and other academic tools.

Supports Elena's Week 3 workflow for academic tool integration.

## Dependencies

- `datetime`
- `json`
- `numpy`
- `pandas`
- `pathlib`
- `pyreadstat`
- `sqlalchemy`
- `sqlalchemy.orm`
- `src.utils.database`
- `src.utils.llm_quality_assurance`
- `tempfile`
- `typing`
- `zipfile`

## Table of Contents

### Classes
- [AcademicDataExporter](#academicdataexporter)
- [ReplicationPackageBuilder](#replicationpackagebuilder)
- [QAEnhancedDataExporter](#qaenhanceddataexporter)

### Functions
- [export_qa_enhanced_academic_data](#export-qa-enhanced-academic-data)
- [export_academic_data](#export-academic-data)

## Classes

### AcademicDataExporter

Export experimental data in academic-standard formats.

Supports Elena's statistical analysis workflow with proper
variable naming, data dictionaries, and metadata preservation.

#### Methods

##### `__init__`
```python
__init__(self, database_url: Optional[str])
```

Initialize exporter with database connection.

##### `export_experiments_data`
```python
export_experiments_data(self, start_date: Optional[str], end_date: Optional[str], framework_names: Optional[List[str]], study_name: Optional[str], output_dir: str) -> Dict[Any]
```

Export comprehensive experimental data for academic analysis.

Args:
    start_date: ISO date string for filtering (e.g., '2025-06-01')
    end_date: ISO date string for filtering
    framework_names: List of framework names to include
    study_name: Study identifier for output naming
    output_dir: Directory for output files
    
Returns:
    Dict mapping format names to output file paths

##### `export_component_analysis_data`
```python
export_component_analysis_data(self, component_type: str, include_development_sessions: bool, output_dir: str) -> Dict[Any]
```

Export component development and performance data.

Supports analysis of prompt engineering, framework development,
and weighting methodology evolution for methodology papers.

##### `_build_comprehensive_query`
```python
_build_comprehensive_query(self, start_date: Optional[str], end_date: Optional[str], framework_names: Optional[List[str]]) -> str
```

Build comprehensive SQL query for experimental data.

##### `_build_component_query`
```python
_build_component_query(self, component_type: str, include_sessions: bool) -> str
```

Build query for component development analysis.

##### `_prepare_academic_dataframe`
```python
_prepare_academic_dataframe(self, df: pd.DataFrame) -> pd.DataFrame
```

Prepare dataframe for academic analysis with proper variable naming.

##### `_prepare_component_dataframe`
```python
_prepare_component_dataframe(self, df: pd.DataFrame) -> pd.DataFrame
```

Prepare component development data for academic analysis.

##### `_expand_raw_scores`
```python
_expand_raw_scores(self, df: pd.DataFrame) -> pd.DataFrame
```

Expand JSON raw scores into individual columns.

##### `_expand_performance_metrics`
```python
_expand_performance_metrics(self, df: pd.DataFrame) -> pd.DataFrame
```

Expand JSON performance metrics into individual columns.

##### `_generate_data_dictionary`
```python
_generate_data_dictionary(self, df: pd.DataFrame) -> Dict[Any]
```

Generate comprehensive data dictionary for academic documentation.

##### `_generate_component_dictionary`
```python
_generate_component_dictionary(self, df: pd.DataFrame, component_type: str) -> Dict[Any]
```

Generate data dictionary for component development data.

---

### ReplicationPackageBuilder

Generate comprehensive replication packages for academic publication.

Supports Elena's Week 5 workflow for academic documentation and reproducibility.

#### Methods

##### `__init__`
```python
__init__(self, database_url: Optional[str])
```

Initialize package builder.

##### `build_replication_package`
```python
build_replication_package(self, study_name: str, study_description: str, data_filters: Optional[Dict], include_code: bool, include_documentation: bool, output_path: str) -> str
```

Build complete replication package for academic publication.

Args:
    study_name: Name of the study for package identification
    study_description: Description for documentation
    data_filters: Filters for data export (start_date, end_date, frameworks)
    include_code: Include analysis code and templates
    include_documentation: Include methodology documentation
    output_path: Directory for output package
    
Returns:
    Path to generated replication package ZIP file

##### `_generate_readme`
```python
_generate_readme(self, package_dir: Path, study_name: str, description: str, data_files: Dict[Any])
```

Generate comprehensive README for replication package.

##### `_generate_data_documentation`
```python
_generate_data_documentation(self, package_dir: Path, data_files: Dict[Any])
```

Generate detailed data documentation.

##### `_include_analysis_templates`
```python
_include_analysis_templates(self, package_dir: Path)
```

Include analysis code templates in multiple languages.

##### `_include_methodology_docs`
```python
_include_methodology_docs(self, package_dir: Path)
```

Include methodology documentation.

---

### QAEnhancedDataExporter
*Inherits from: [AcademicDataExporter](src/academic/data_export.md#academicdataexporter)*

Quality Assurance Enhanced Data Exporter.

Extends AcademicDataExporter with integrated 6-layer quality assurance
validation before academic data export. Adds QA confidence scores and
quality metadata to all exported datasets.

Phase 1 of QA integration: Core QA validation with enhanced data output.

#### Methods

##### `__init__`
```python
__init__(self, database_url: Optional[str])
```

Initialize QA-enhanced exporter with database connection and QA system.

##### `export_experiments_data`
```python
export_experiments_data(self, start_date: Optional[str], end_date: Optional[str], framework_names: Optional[List[str]], study_name: Optional[str], output_dir: str, include_qa_validation: bool, qa_confidence_threshold: float) -> Dict[Any]
```

Export experimental data with integrated quality assurance validation.

Args:
    start_date: ISO date string for filtering (e.g., '2025-06-01')
    end_date: ISO date string for filtering
    framework_names: List of framework names to include
    study_name: Study identifier for output naming
    output_dir: Directory for output files
    include_qa_validation: Whether to run QA validation on exported data
    qa_confidence_threshold: Minimum confidence threshold for inclusion
    
Returns:
    Dict mapping format names to output file paths, with QA report

##### `_validate_analysis_quality`
```python
_validate_analysis_quality(self, df: pd.DataFrame, confidence_threshold: float) -> pd.DataFrame
```

Run quality assurance validation on experimental data.

Args:
    df: Raw experimental data from database
    confidence_threshold: Minimum confidence for inclusion
    
Returns:
    DataFrame with QA validation results and confidence scores

##### `_extract_framework_name`
```python
_extract_framework_name(self, row: pd.Series) -> str
```

Extract framework name from database row.

##### `_parse_raw_scores`
```python
_parse_raw_scores(self, raw_scores: Any) -> Dict[Any]
```

Parse raw scores from database format.

##### `_generate_qa_enhanced_data_dictionary`
```python
_generate_qa_enhanced_data_dictionary(self, df: pd.DataFrame) -> Dict[Any]
```

Generate enhanced data dictionary including QA field descriptions.

##### `_generate_qa_summary`
```python
_generate_qa_summary(self, df: pd.DataFrame) -> Dict[Any]
```

Generate QA validation summary statistics.

---

## Functions

### `export_qa_enhanced_academic_data`
```python
export_qa_enhanced_academic_data(study_name: str, include_qa_validation: bool, **kwargs) -> Dict[Any]
```

Convenience function to export QA-enhanced academic data.

Args:
    study_name: Study identifier for output naming
    include_qa_validation: Whether to run QA validation (default: True)
    **kwargs: Additional arguments passed to QAEnhancedDataExporter.export_experiments_data()
    
Returns:
    Dict mapping format names to output file paths

---

### `export_academic_data`
```python
export_academic_data(study_name: str, **kwargs) -> Dict[Any]
```

Legacy convenience function maintained for backward compatibility.

Args:
    study_name: Study identifier for output naming
    **kwargs: Additional arguments passed to AcademicDataExporter.export_experiments_data()
    
Returns:
    Dict mapping format names to output file paths

---

*Generated on 2025-06-23 10:38:43*