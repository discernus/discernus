# Plotly Circular

**Module:** `src.visualization.plotly_circular`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/visualization/plotly_circular.py`
**Package:** `visualization`

## Dependencies

- `datetime`
- `numpy`
- `pathlib`
- `plotly.express`
- `plotly.graph_objects`
- `plotly.subplots`
- `typing`

## Table of Contents

### Classes
- [PlotlyCircularVisualizer](#plotlycircularvisualizer)

## Classes

### PlotlyCircularVisualizer

Plotly-based visualizer for circular coordinate system narrative gravity maps.
Framework-agnostic: supports arbitrary well types, colors, and arrangements.

Features:
- Interactive visualization with hover info
- Publication-ready static exports
- Framework-agnostic well positioning
- Comparative visualization support
- Academic styling defaults

#### Methods

##### `__init__`
```python
__init__(self, circle_radius, type_to_color, figure_size)
```

##### `get_type_color`
```python
get_type_color(self, well_type: str, idx: int) -> str
```

Get color for a well type, using config or fallback palette.

##### `create_base_figure`
```python
create_base_figure(self, title: str) -> go.Figure
```

Create base figure with circle boundary and styling.

##### `calculate_narrative_position`
```python
calculate_narrative_position(self, wells: Dict, narrative_scores: Dict) -> Tuple[Any]
```

Calculate narrative position based on well scores.

##### `plot`
```python
plot(self, wells: Dict, narrative_scores: Optional[Dict], narrative_label: Optional[str], title: Optional[str], output_html: Optional[str], output_png: Optional[str], show: bool) -> go.Figure
```

Create a complete circular visualization.

Args:
    wells: dict of {well_name: {'angle': deg, 'type': str, 'weight': float, ...}}
    narrative_scores: dict of {well_name: score} (optional)
    narrative_label: str (optional)
    title: str (optional)
    output_html: path to save interactive HTML (optional)
    output_png: path to save static PNG (optional, requires kaleido)
    show: whether to display the figure

##### `create_comparison`
```python
create_comparison(self, analyses: List[Dict], title: str, output_html: Optional[str], output_png: Optional[str]) -> go.Figure
```

Create a comparison visualization with multiple analyses.

Args:
    analyses: List of analysis results, each containing wells and scores
    title: Title for the comparison visualization
    output_html: Path to save interactive HTML
    output_png: Path to save static PNG

---

*Generated on 2025-06-21 12:44:47*