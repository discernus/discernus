#   Init  

**Module:** `src.visualization.__init__`
**File:** `/Volumes/dev/discernus/src/visualization/__init__.py`
**Package:** `visualization`

Narrative Gravity Visualization Package
=====================================

Centralized visualization system for consistent, professional visualizations.

**Recommended Usage:**
```python
from visualization import create_visualization_engine

# Create themed engine
engine = create_visualization_engine(theme='academic')

# Single analysis
fig = engine.create_single_analysis(wells, scores, title="My Analysis")

# Comparative analysis
fig = engine.create_comparative_analysis(analyses, title="Comparison")

# Dashboard
fig = engine.create_dashboard(analyses, title="Dashboard")
```

**Available Themes:**
- 'academic': Professional publication styling
- 'presentation': High-contrast for presentations
- 'minimal': Clean, modern interface styling
- 'dark': Dark theme for reduced eye strain

## Dependencies

- `engine`
- `plotly_circular`
- `themes`

## Table of Contents

### Functions
- [quick_viz](#quick-viz)

## Functions

### `quick_viz`
```python
quick_viz(wells, scores, title, theme, output_html)
```

Quick visualization creation for simple use cases.

Args:
    wells: Dictionary of well definitions
    scores: Optional narrative scores
    title: Chart title
    theme: Theme name
    output_html: Optional HTML output path
    
Returns:
    Plotly figure

---

*Generated on 2025-06-21 18:56:11*