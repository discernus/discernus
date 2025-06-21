# Themes

**Module:** `src.visualization.themes`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/visualization/themes.py`
**Package:** `visualization`

Narrative Gravity Visualization Themes
=====================================

Centralized theming system for consistent, professional visualizations.
Abstracts Plotly styling to avoid pixel-pushing individual charts.

## Dependencies

- `plotly.graph_objects`
- `typing`

## Table of Contents

### Classes
- [VisualizationTheme](#visualizationtheme)
- [AcademicTheme](#academictheme)
- [PresentationTheme](#presentationtheme)
- [MinimalTheme](#minimaltheme)
- [DarkTheme](#darktheme)
- [ThemeManager](#thememanager)

## Classes

### VisualizationTheme

Base class for visualization themes.

#### Methods

##### `__init__`
```python
__init__(self, name: str)
```

##### `style`
```python
style(self) -> Dict[Any]
```

Return theme styling configuration.

##### `layout_config`
```python
layout_config(self) -> Dict[Any]
```

Return Plotly layout configuration.

##### `well_colors`
```python
well_colors(self) -> Dict[Any]
```

Return well type color mapping.

##### `apply_to_figure`
```python
apply_to_figure(self, fig: go.Figure) -> go.Figure
```

Apply theme to a Plotly figure.

---

### AcademicTheme
*Inherits from: [VisualizationTheme](src/visualization/themes.md#visualizationtheme)*

Professional academic publication theme.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `style`
```python
style(self) -> Dict[Any]
```

##### `layout_config`
```python
layout_config(self) -> Dict[Any]
```

##### `well_colors`
```python
well_colors(self) -> Dict[Any]
```

---

### PresentationTheme
*Inherits from: [VisualizationTheme](src/visualization/themes.md#visualizationtheme)*

High-contrast theme for presentations and demos.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `style`
```python
style(self) -> Dict[Any]
```

##### `layout_config`
```python
layout_config(self) -> Dict[Any]
```

##### `well_colors`
```python
well_colors(self) -> Dict[Any]
```

---

### MinimalTheme
*Inherits from: [VisualizationTheme](src/visualization/themes.md#visualizationtheme)*

Clean, minimal theme for modern interfaces.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `style`
```python
style(self) -> Dict[Any]
```

##### `layout_config`
```python
layout_config(self) -> Dict[Any]
```

##### `well_colors`
```python
well_colors(self) -> Dict[Any]
```

---

### DarkTheme
*Inherits from: [VisualizationTheme](src/visualization/themes.md#visualizationtheme)*

Dark theme for modern interfaces and reduced eye strain.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `style`
```python
style(self) -> Dict[Any]
```

##### `layout_config`
```python
layout_config(self) -> Dict[Any]
```

##### `well_colors`
```python
well_colors(self) -> Dict[Any]
```

---

### ThemeManager

Manages visualization themes and provides easy access.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `get_theme`
```python
get_theme(self, theme_name: Optional[str]) -> [VisualizationTheme](src/visualization/themes.md#visualizationtheme)
```

Get theme by name, falling back to default.

##### `list_themes`
```python
list_themes(self) -> list
```

List available theme names.

##### `set_default_theme`
```python
set_default_theme(self, theme_name: str) -> bool
```

Set the default theme.

---

*Generated on 2025-06-21 12:44:47*