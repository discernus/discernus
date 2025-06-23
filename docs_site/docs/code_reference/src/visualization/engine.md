# Engine

**Module:** `src.visualization.engine`
**File:** `/app/src/visualization/engine.py`
**Package:** `visualization`

Narrative Gravity Visualization Engine
=====================================

Centralized, theme-aware visualization engine for consistent, professional 
visualizations across the entire platform.

## Dependencies

- `datetime`
- `numpy`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.subplots`
- `plotly_circular`
- `themes`
- `typing`

## Table of Contents

### Classes
- [NarrativeGravityVisualizationEngine](#narrativegravityvisualizationengine)

### Functions
- [create_visualization_engine](#create-visualization-engine)

## Classes

### NarrativeGravityVisualizationEngine

Centralized visualization engine for Narrative Gravity Maps.

Features:
- Theme-aware styling (academic, presentation, minimal, dark)
- Multiple visualization types (single, comparative, dashboard)
- Consistent API across all use cases
- Publication-ready outputs
- Interactive and static export options

#### Methods

##### `__init__`
```python
__init__(self, theme: str, figure_size: int)
```

##### `set_theme`
```python
set_theme(self, theme_name: str) -> bool
```

Change the visualization theme.

##### `create_single_analysis`
```python
create_single_analysis(self, wells: Dict[Any], narrative_scores: Optional[Dict[Any]], title: str, narrative_label: str, output_html: Optional[str], output_png: Optional[str], show: bool) -> go.Figure
```

Create a single analysis visualization.

Args:
    wells: Dictionary of well definitions
    narrative_scores: Optional scores for narrative positioning
    title: Chart title
    narrative_label: Label for narrative position
    output_html: Path to save interactive HTML
    output_png: Path to save static PNG
    show: Whether to display the figure
    
Returns:
    Plotly figure object

##### `create_comparative_analysis`
```python
create_comparative_analysis(self, analyses: List[Dict[Any]], title: str, output_html: Optional[str], output_png: Optional[str], show: bool) -> go.Figure
```

Create a comparative analysis visualization.

Args:
    analyses: List of analysis dictionaries
    title: Chart title
    output_html: Path to save interactive HTML
    output_png: Path to save static PNG
    show: Whether to display the figure
    
Returns:
    Plotly figure object

##### `create_dashboard`
```python
create_dashboard(self, analyses: List[Dict[Any]], title: str, include_summary: bool, output_html: Optional[str], output_png: Optional[str], show: bool) -> go.Figure
```

Create a comprehensive dashboard visualization.

Args:
    analyses: List of analysis dictionaries
    title: Dashboard title
    include_summary: Whether to include summary statistics
    output_html: Path to save interactive HTML
    output_png: Path to save static PNG
    show: Whether to display the figure
    
Returns:
    Plotly figure object

##### `_calculate_summary_stats`
```python
_calculate_summary_stats(self, analyses: List[Dict[Any]]) -> str
```

Calculate summary statistics for dashboard.

##### `export_for_publication`
```python
export_for_publication(self, figure: go.Figure, output_dir: str, filename: str, formats: List[str]) -> Dict[Any]
```

Export figure in multiple publication-ready formats.

Args:
    figure: Plotly figure to export
    output_dir: Directory to save files
    filename: Base filename (without extension)
    formats: List of formats to export
    
Returns:
    Dictionary mapping format to filepath

##### `get_theme_info`
```python
get_theme_info(self) -> Dict[Any]
```

Get information about the current theme.

---

## Functions

### `create_visualization_engine`
```python
create_visualization_engine(theme: str, figure_size: int) -> [NarrativeGravityVisualizationEngine](src/visualization/engine.md#narrativegravityvisualizationengine)
```

Create a themed visualization engine.

---

*Generated on 2025-06-23 10:38:43*