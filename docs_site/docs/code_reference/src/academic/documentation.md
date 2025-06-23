# Documentation

**Module:** `src.academic.documentation`
**File:** `/app/src/academic/documentation.py`
**Package:** `academic`

Academic Documentation Generators - Priority 3

Automated generation of methodology papers, statistical reports, and academic documentation.
Supports Elena's Week 5 workflow for publication preparation.

## Dependencies

- `datetime`
- `json`
- `pandas`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `src.utils.database`
- `typing`

## Table of Contents

### Classes
- [MethodologyPaperGenerator](#methodologypapergenerator)
- [StatisticalReportFormatter](#statisticalreportformatter)

### Functions
- [generate_methodology_paper](#generate-methodology-paper)
- [generate_results_report](#generate-results-report)

## Classes

### MethodologyPaperGenerator

Generate methodology papers from experimental data and development sessions.

#### Methods

##### `__init__`
```python
__init__(self, database_url: Optional[str])
```

Initialize generator with database connection.

##### `generate_methodology_section`
```python
generate_methodology_section(self, study_name: str, include_development_process: bool, output_path: str) -> str
```

Generate comprehensive methodology section for academic papers.

Args:
    study_name: Study identifier for data retrieval
    include_development_process: Include component development methodology
    output_path: Directory for output files
    
Returns:
    Path to generated methodology document

##### `_gather_methodology_data`
```python
_gather_methodology_data(self, study_name: str) -> Dict[Any]
```

Gather data about experimental methodology.

##### `_build_methodology_content`
```python
_build_methodology_content(self, data: Dict[Any], include_development: bool) -> str
```

Build comprehensive methodology content.

---

### StatisticalReportFormatter

Format statistical results for academic publication.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize report formatter.

##### `generate_results_section`
```python
generate_results_section(self, analysis_results: Dict[Any], study_name: str, output_path: str) -> str
```

Generate results section with properly formatted statistics.

Args:
    analysis_results: Statistical analysis results
    study_name: Study identifier
    output_path: Directory for output files
    
Returns:
    Path to generated results document

##### `_build_results_content`
```python
_build_results_content(self, results: Dict[Any], study_name: str) -> str
```

Build formatted results section.

##### `format_apa_statistics`
```python
format_apa_statistics(self, stat_type: str, **kwargs) -> str
```

Format statistics in APA style.

---

## Functions

### `generate_methodology_paper`
```python
generate_methodology_paper(study_name: str, output_path: str) -> str
```

Quick methodology paper generation.

---

### `generate_results_report`
```python
generate_results_report(results: Dict[Any], study_name: str, output_path: str) -> str
```

Quick results report generation.

---

*Generated on 2025-06-23 10:38:43*