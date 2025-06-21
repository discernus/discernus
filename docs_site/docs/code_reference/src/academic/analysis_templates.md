# Analysis Templates

**Module:** `src.academic.analysis_templates`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/academic/analysis_templates.py`
**Package:** `academic`

AI-Generated Analysis Templates - Priority 3

Generates Cursor-assisted analysis code for academic research in multiple languages.
Supports Elena's Week 3 workflow for statistical analysis and visualization.

## Dependencies

- `datetime`
- `json`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `src.utils.database`
- `typing`
- `visualization.plotly_circular`

## Table of Contents

### Classes
- [JupyterTemplateGenerator](#jupytertemplategenerator)
- [RScriptGenerator](#rscriptgenerator)
- [StataIntegration](#stataintegration)

### Functions
- [generate_jupyter_notebook](#generate-jupyter-notebook)
- [generate_r_analysis](#generate-r-analysis)
- [generate_stata_analysis](#generate-stata-analysis)

## Classes

### JupyterTemplateGenerator

Generate Jupyter notebook templates for narrative analysis.

#### Methods

##### `__init__`
```python
__init__(self, database_url: Optional[str])
```

Initialize generator with database connection.

##### `generate_exploration_notebook`
```python
generate_exploration_notebook(self, study_name: str, output_path: str) -> str
```

Generate exploratory data analysis notebook.

##### `_create_markdown_cell`
```python
_create_markdown_cell(self, *content)
```

Create markdown cell.

##### `_create_code_cell`
```python
_create_code_cell(self, code)
```

Create code cell.

##### `_get_imports_code`
```python
_get_imports_code(self)
```

Generate imports code.

##### `_get_data_loading_code`
```python
_get_data_loading_code(self, study_name)
```

Generate data loading code.

##### `_get_overview_code`
```python
_get_overview_code(self)
```

Generate dataset overview code.

##### `_get_reliability_analysis_code`
```python
_get_reliability_analysis_code(self)
```

Generate reliability analysis code.

##### `_get_framework_analysis_code`
```python
_get_framework_analysis_code(self)
```

Generate framework analysis code.

##### `_get_visualization_code`
```python
_get_visualization_code(self)
```

Generate visualization code using centralized system.

---

### RScriptGenerator

Generate R scripts for statistical analysis and visualization.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize R script generator.

##### `generate_statistical_analysis`
```python
generate_statistical_analysis(self, study_name: str, output_path: str) -> str
```

Generate comprehensive R statistical analysis script.

##### `_build_r_analysis_script`
```python
_build_r_analysis_script(self, study_name: str) -> str
```

Build comprehensive R analysis script.

---

### StataIntegration

Generate Stata scripts for publication-grade statistical analysis.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize Stata integration.

##### `generate_publication_analysis`
```python
generate_publication_analysis(self, study_name: str, output_path: str) -> str
```

Generate Stata script for publication-quality analysis.

##### `_build_stata_script`
```python
_build_stata_script(self, study_name: str) -> str
```

Build publication-quality Stata analysis script.

---

## Functions

### `generate_jupyter_notebook`
```python
generate_jupyter_notebook(study_name: str, output_path: str) -> str
```

Quick Jupyter notebook generation.

---

### `generate_r_analysis`
```python
generate_r_analysis(study_name: str, output_path: str) -> str
```

Quick R script generation.

---

### `generate_stata_analysis`
```python
generate_stata_analysis(study_name: str, output_path: str) -> str
```

Quick Stata script generation.

---

*Generated on 2025-06-21 12:44:48*