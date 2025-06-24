"""
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
"""

from .engine import NarrativeGravityVisualizationEngine, create_visualization_engine
from .themes import get_theme, list_themes, theme_manager
from .plotly_circular import PlotlyCircularVisualizer
# Enhanced capabilities properly integrated into existing Plotly system
# (Advanced features should be added to PlotlyCircularVisualizer, not as separate matplotlib classes)

# Main exports - centralized system
__all__ = [
    'NarrativeGravityVisualizationEngine',
    'create_visualization_engine',
    'get_theme',
    'list_themes',
    'theme_manager',
    # Production Plotly-based system
    'PlotlyCircularVisualizer'
]

# Convenience function for quick access
def quick_viz(wells, scores=None, title="Analysis", theme='academic', output_html=None):
    """
    Quick visualization creation for simple use cases.
    
    Args:
        wells: Dictionary of well definitions
        scores: Optional narrative scores
        title: Chart title
        theme: Theme name
        output_html: Optional HTML output path
        
    Returns:
        Plotly figure
    """
    engine = create_visualization_engine(theme=theme)
    return engine.create_single_analysis(
        wells=wells,
        narrative_scores=scores,
        title=title,
        output_html=output_html
    )
