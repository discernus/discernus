"""
Narrative Gravity Visualization Themes
=====================================

Centralized theming system for consistent, professional visualizations.
Abstracts Plotly styling to avoid pixel-pushing individual charts.
"""

from typing import Dict, Any, Optional
import plotly.graph_objects as go


class VisualizationTheme:
    """Base class for visualization themes."""
    
    def __init__(self, name: str):
        self.name = name
        
    @property
    def style(self) -> Dict[str, Any]:
        """Return theme styling configuration."""
        raise NotImplementedError
        
    @property
    def layout_config(self) -> Dict[str, Any]:
        """Return Plotly layout configuration."""
        raise NotImplementedError
        
    @property
    def well_colors(self) -> Dict[str, str]:
        """Return well type color mapping."""
        raise NotImplementedError
        
    def apply_to_figure(self, fig: go.Figure) -> go.Figure:
        """Apply theme to a Plotly figure."""
        fig.update_layout(**self.layout_config)
        return fig


class AcademicTheme(VisualizationTheme):
    """Professional academic publication theme."""
    
    def __init__(self):
        super().__init__("academic")
        
    @property
    def style(self) -> Dict[str, Any]:
        return {
            'font_family': 'Times New Roman',
            'title_size': 18,
            'subtitle_size': 14,
            'axis_title_size': 12,
            'label_size': 10,
            'well_marker_size': 16,
            'narrative_marker_size': 24,
            'grid_color': '#E0E0E0',
            'grid_width': 1,
            'boundary_color': '#000000',
            'boundary_width': 2,
            'background_color': 'white',
            'annotation_bg': 'rgba(248, 249, 250, 0.9)',
            'annotation_border': 'rgba(52, 58, 64, 0.3)'
        }
    
    @property
    def layout_config(self) -> Dict[str, Any]:
        style = self.style
        return {
            'font': {'family': style['font_family'], 'size': style['label_size']},
            'title': {
                'font': {'size': style['title_size'], 'family': style['font_family']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': style['background_color'],
            'paper_bgcolor': style['background_color'],
            'showlegend': False
        }
    
    @property
    def well_colors(self) -> Dict[str, str]:
        return {
            'integrative': '#1B5E20',    # Dark green
            'disintegrative': '#B71C1C', # Dark red
            'progressive': '#0D47A1',    # Dark blue
            'conservative': '#E65100',   # Dark orange
            'virtue': '#4A148C',         # Dark purple
            'vice': '#3E2723',          # Dark brown
            'default': '#424242'         # Dark gray
        }


class PresentationTheme(VisualizationTheme):
    """High-contrast theme for presentations and demos."""
    
    def __init__(self):
        super().__init__("presentation")
        
    @property
    def style(self) -> Dict[str, Any]:
        return {
            'font_family': 'Arial',
            'title_size': 24,
            'subtitle_size': 18,
            'axis_title_size': 16,
            'label_size': 14,
            'well_marker_size': 22,
            'narrative_marker_size': 32,
            'grid_color': '#BDBDBD',
            'grid_width': 2,
            'boundary_color': '#000000',
            'boundary_width': 3,
            'background_color': 'white',
            'annotation_bg': 'rgba(255, 235, 59, 0.9)',
            'annotation_border': 'rgba(0, 0, 0, 0.5)'
        }
    
    @property
    def layout_config(self) -> Dict[str, Any]:
        style = self.style
        return {
            'font': {'family': style['font_family'], 'size': style['label_size']},
            'title': {
                'font': {'size': style['title_size'], 'family': style['font_family']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': style['background_color'],
            'paper_bgcolor': style['background_color'],
            'showlegend': False
        }
    
    @property
    def well_colors(self) -> Dict[str, str]:
        return {
            'integrative': '#2E7D32',    # Bright green
            'disintegrative': '#D32F2F', # Bright red
            'progressive': '#1976D2',    # Bright blue
            'conservative': '#F57C00',   # Bright orange
            'virtue': '#7B1FA2',         # Bright purple
            'vice': '#5D4037',          # Brown
            'default': '#616161'         # Gray
        }


class MinimalTheme(VisualizationTheme):
    """Clean, minimal theme for modern interfaces."""
    
    def __init__(self):
        super().__init__("minimal")
        
    @property
    def style(self) -> Dict[str, Any]:
        return {
            'font_family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
            'title_size': 16,
            'subtitle_size': 12,
            'axis_title_size': 10,
            'label_size': 9,
            'well_marker_size': 14,
            'narrative_marker_size': 20,
            'grid_color': '#F5F5F5',
            'grid_width': 1,
            'boundary_color': '#9E9E9E',
            'boundary_width': 1.5,
            'background_color': '#FAFAFA',
            'annotation_bg': 'rgba(255, 255, 255, 0.95)',
            'annotation_border': 'rgba(0, 0, 0, 0.1)'
        }
    
    @property
    def layout_config(self) -> Dict[str, Any]:
        style = self.style
        return {
            'font': {'family': style['font_family'], 'size': style['label_size']},
            'title': {
                'font': {'size': style['title_size'], 'family': style['font_family']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': style['background_color'],
            'paper_bgcolor': style['background_color'],
            'showlegend': False,
            'margin': {'l': 40, 'r': 40, 't': 60, 'b': 40}
        }
    
    @property
    def well_colors(self) -> Dict[str, str]:
        return {
            'integrative': '#43A047',    # Material green
            'disintegrative': '#E53935', # Material red
            'progressive': '#1E88E5',    # Material blue
            'conservative': '#FB8C00',   # Material orange
            'virtue': '#8E24AA',         # Material purple
            'vice': '#6D4C41',          # Material brown
            'default': '#757575'         # Material gray
        }


class DarkTheme(VisualizationTheme):
    """Dark theme for modern interfaces and reduced eye strain."""
    
    def __init__(self):
        super().__init__("dark")
        
    @property
    def style(self) -> Dict[str, Any]:
        return {
            'font_family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
            'title_size': 16,
            'subtitle_size': 12,
            'axis_title_size': 10,
            'label_size': 9,
            'well_marker_size': 16,
            'narrative_marker_size': 22,
            'grid_color': '#424242',
            'grid_width': 1,
            'boundary_color': '#BDBDBD',
            'boundary_width': 2,
            'background_color': '#1E1E1E',
            'text_color': '#FFFFFF',
            'annotation_bg': 'rgba(66, 66, 66, 0.9)',
            'annotation_border': 'rgba(189, 189, 189, 0.3)'
        }
    
    @property
    def layout_config(self) -> Dict[str, Any]:
        style = self.style
        return {
            'font': {
                'family': style['font_family'], 
                'size': style['label_size'],
                'color': style['text_color']
            },
            'title': {
                'font': {
                    'size': style['title_size'], 
                    'family': style['font_family'],
                    'color': style['text_color']
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': style['background_color'],
            'paper_bgcolor': style['background_color'],
            'showlegend': False,
            'margin': {'l': 40, 'r': 40, 't': 60, 'b': 40}
        }
    
    @property
    def well_colors(self) -> Dict[str, str]:
        return {
            'integrative': '#66BB6A',    # Light green
            'disintegrative': '#EF5350', # Light red
            'progressive': '#42A5F5',    # Light blue
            'conservative': '#FFA726',   # Light orange
            'virtue': '#AB47BC',         # Light purple
            'vice': '#8D6E63',          # Light brown
            'default': '#BDBDBD'         # Light gray
        }


class ThemeManager:
    """Manages visualization themes and provides easy access."""
    
    def __init__(self):
        self.themes = {
            'academic': AcademicTheme(),
            'presentation': PresentationTheme(),
            'minimal': MinimalTheme(),
            'dark': DarkTheme()
        }
        self.default_theme = 'academic'
    
    def get_theme(self, theme_name: Optional[str] = None) -> VisualizationTheme:
        """Get theme by name, falling back to default."""
        if theme_name is None:
            theme_name = self.default_theme
        
        if theme_name not in self.themes:
            print(f"⚠️  Theme '{theme_name}' not found, using '{self.default_theme}'")
            theme_name = self.default_theme
            
        return self.themes[theme_name]
    
    def list_themes(self) -> list:
        """List available theme names."""
        return list(self.themes.keys())
    
    def set_default_theme(self, theme_name: str) -> bool:
        """Set the default theme."""
        if theme_name in self.themes:
            self.default_theme = theme_name
            return True
        return False


# Global theme manager instance
theme_manager = ThemeManager()


def get_theme(theme_name: Optional[str] = None) -> VisualizationTheme:
    """Convenience function to get a theme."""
    return theme_manager.get_theme(theme_name)


def list_themes() -> list:
    """Convenience function to list available themes."""
    return theme_manager.list_themes()


if __name__ == '__main__':
    # Demo all themes
    print("🎨 Available Visualization Themes:")
    print("=" * 40)
    
    for theme_name in list_themes():
        theme = get_theme(theme_name)
        print(f"\n📋 {theme_name.upper()} THEME")
        print(f"   Font: {theme.style['font_family']}")
        print(f"   Colors: {len(theme.well_colors)} well types")
        print(f"   Style: {theme.style['title_size']}pt titles")
        
    print(f"\n✅ Default theme: {theme_manager.default_theme}") 