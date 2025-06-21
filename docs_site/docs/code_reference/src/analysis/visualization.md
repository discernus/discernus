# Visualization

**Module:** `src.analysis.visualization`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/analysis/visualization.py`
**Package:** `analysis`

Framework-Aware Visualization Generator for Narrative Gravity Analysis
Uses production NarrativeGravityVisualizationEngine for consistent, theme-aware visualizations

## Dependencies

- `framework_manager`
- `json`
- `logging`
- `matplotlib.pyplot`
- `numpy`
- `pandas`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.subplots`
- `seaborn`
- `typing`
- `visualization.engine`
- `warnings`

## Table of Contents

### Classes
- [VisualizationGenerator](#visualizationgenerator)

## Classes

### VisualizationGenerator

Framework-aware visualization generator using production visualization engine.

#### Methods

##### `__init__`
```python
__init__(self, output_dir: str)
```

Initialize the visualization generator with production engine.

##### `generate_visualizations`
```python
generate_visualizations(self, structured_results: Dict, statistical_results: Dict, reliability_results: Dict) -> Dict[Any]
```

Generate comprehensive visualizations using production visualization engine.

Args:
    structured_results: Structured experiment data
    statistical_results: Statistical hypothesis testing results
    reliability_results: Interrater reliability analysis results
    
Returns:
    Dictionary containing paths to generated visualization files

##### `_get_framework_wells`
```python
_get_framework_wells(self, framework_name: str) -> List[str]
```

Get the list of wells defined for a specific framework.

##### `_prepare_framework_data`
```python
_prepare_framework_data(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict
```

Prepare data in format expected by production visualization engine.

##### `create_production_narrative_plots`
```python
create_production_narrative_plots(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict[Any]
```

Create narrative gravity plots using production visualization engine.

##### `create_framework_correlation_plots`
```python
create_framework_correlation_plots(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict[Any]
```

Create correlation matrix showing only framework-defined wells.

##### `create_production_dashboard`
```python
create_production_dashboard(self, df: pd.DataFrame, well_columns: List[str], statistical_results: Dict, framework_name: str) -> Dict[Any]
```

Create interactive dashboard using production visualization components.

##### `create_descriptive_plots`
```python
create_descriptive_plots(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict[Any]
```

Create minimal descriptive plots for statistical overview.

##### `create_hypothesis_plots`
```python
create_hypothesis_plots(self, statistical_results: Dict) -> Dict[Any]
```

Create plots for hypothesis testing results.

##### `create_reliability_plots`
```python
create_reliability_plots(self, reliability_results: Dict) -> Dict[Any]
```

Create minimal reliability plots.

##### `create_distribution_plots`
```python
create_distribution_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Create distribution plots (minimal version).

##### `save_visualization_index`
```python
save_visualization_index(self) -> str
```

Save index of generated visualizations.

---

*Generated on 2025-06-21 12:44:47*