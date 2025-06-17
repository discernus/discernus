"""
Narrative Gravity Visualization Engine
=====================================

Centralized, theme-aware visualization engine for consistent, professional 
visualizations across the entire platform.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any
from datetime import datetime
from pathlib import Path

from .themes import get_theme, VisualizationTheme
from .plotly_circular import PlotlyCircularVisualizer


class NarrativeGravityVisualizationEngine:
    """
    Centralized visualization engine for Narrative Gravity Maps.
    
    Features:
    - Theme-aware styling (academic, presentation, minimal, dark)
    - Multiple visualization types (single, comparative, dashboard)
    - Consistent API across all use cases
    - Publication-ready outputs
    - Interactive and static export options
    """
    
    def __init__(self, theme: str = 'academic', figure_size: int = 900):
        self.theme_name = theme
        self.theme = get_theme(theme)
        self.figure_size = figure_size
        
        # Initialize themed circular visualizer
        self.circular_viz = PlotlyCircularVisualizer(
            circle_radius=1.0,
            type_to_color=self.theme.well_colors,
            figure_size=figure_size
        )
        
        # Override circular visualizer styling with theme
        self.circular_viz.style = self.theme.style
        
    def set_theme(self, theme_name: str) -> bool:
        """Change the visualization theme."""
        try:
            self.theme = get_theme(theme_name)
            self.theme_name = theme_name
            
            # Update circular visualizer
            self.circular_viz.type_to_color = self.theme.well_colors
            self.circular_viz.style = self.theme.style
            
            return True
        except Exception as e:
            print(f"⚠️  Failed to set theme '{theme_name}': {e}")
            return False
    
    def create_single_analysis(self, 
                              wells: Dict[str, Dict],
                              narrative_scores: Optional[Dict[str, float]] = None,
                              title: str = "Narrative Gravity Analysis",
                              narrative_label: str = "Narrative",
                              output_html: Optional[str] = None,
                              output_png: Optional[str] = None,
                              show: bool = True) -> go.Figure:
        """
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
        """
        fig = self.circular_viz.plot(
            wells=wells,
            narrative_scores=narrative_scores,
            narrative_label=narrative_label,
            title=title,
            output_html=output_html,
            output_png=output_png,
            show=show
        )
        
        # Apply theme
        fig = self.theme.apply_to_figure(fig)
        
        return fig
    
    def create_comparative_analysis(self,
                                   analyses: List[Dict[str, Any]],
                                   title: str = "Comparative Narrative Analysis",
                                   output_html: Optional[str] = None,
                                   output_png: Optional[str] = None,
                                   show: bool = True) -> go.Figure:
        """
        Create a comparative analysis visualization.
        
        Args:
            analyses: List of analysis dictionaries
            title: Chart title
            output_html: Path to save interactive HTML
            output_png: Path to save static PNG
            show: Whether to display the figure
            
        Returns:
            Plotly figure object
        """
        fig = self.circular_viz.create_comparison(
            analyses=analyses,
            title=title,
            output_html=output_html,
            output_png=output_png
        )
        
        # Apply theme to main figure
        fig = self.theme.apply_to_figure(fig)
        
        if show:
            fig.show()
            
        return fig
    
    def create_dashboard(self,
                        analyses: List[Dict[str, Any]],
                        title: str = "Narrative Gravity Dashboard",
                        include_summary: bool = True,
                        output_html: Optional[str] = None,
                        output_png: Optional[str] = None,
                        show: bool = True) -> go.Figure:
        """
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
        """
        # Determine subplot layout
        n_analyses = len(analyses)
        if n_analyses <= 2:
            rows, cols = 1, n_analyses
        elif n_analyses <= 4:
            rows, cols = 2, 2
        elif n_analyses <= 6:
            rows, cols = 2, 3
        else:
            rows, cols = 3, 3  # Max 9 analyses
            
        # Create subplot titles
        subplot_titles = []
        for i, analysis in enumerate(analyses[:rows*cols]):
            subplot_titles.append(analysis.get('title', f'Analysis {i+1}'))
        
        # Create subplots
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            specs=[[{"type": "scatter"} for _ in range(cols)] for _ in range(rows)]
        )
        
        # Add each analysis
        for i, analysis in enumerate(analyses[:rows*cols]):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            wells = analysis.get('wells', {})
            scores = analysis.get('scores', {})
            
            # Create individual visualization
            single_fig = self.create_single_analysis(
                wells=wells,
                narrative_scores=scores,
                title="",  # Title handled by subplot
                show=False
            )
            
            # Add traces to subplot
            for trace in single_fig.data:
                fig.add_trace(trace, row=row, col=col)
        
        # Update layout with theme
        layout_config = self.theme.layout_config.copy()
        layout_config.update({
            'title': {
                'text': title,
                'font': {'size': self.theme.style['title_size'], 'family': self.theme.style['font_family']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'height': self.figure_size * rows,
            'width': self.figure_size * cols,
            'showlegend': False
        })
        
        fig.update_layout(**layout_config)
        
        # Update subplot axes with aspect ratio locking to keep circles circular
        for i in range(1, rows*cols + 1):
            row_idx = (i-1)//cols + 1
            col_idx = (i-1)%cols + 1
            fig.update_xaxes(
                visible=False, 
                range=[-1.2, 1.2], 
                scaleanchor=f"y{i}", 
                scaleratio=1,
                row=row_idx, 
                col=col_idx
            )
            fig.update_yaxes(
                visible=False, 
                range=[-1.2, 1.2], 
                row=row_idx, 
                col=col_idx
            )
        
        # Add summary if requested
        if include_summary and len(analyses) > 1:
            summary_stats = self._calculate_summary_stats(analyses)
            fig.add_annotation(
                x=0.02, y=0.98,
                text=summary_stats,
                showarrow=False,
                font=dict(size=10),
                bgcolor=self.theme.style['annotation_bg'],
                bordercolor=self.theme.style['annotation_border'],
                borderwidth=1,
                borderpad=4,
                xanchor='left',
                yanchor='top',
                xref='paper',
                yref='paper'
            )
        
        # Save outputs
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
            
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)
            
        if show:
            fig.show()
            
        return fig
    
    def _calculate_summary_stats(self, analyses: List[Dict[str, Any]]) -> str:
        """Calculate summary statistics for dashboard."""
        if not analyses:
            return ""
        
        # Calculate average distances and positions
        distances = []
        positions = []
        
        for analysis in analyses:
            wells = analysis.get('wells', {})
            scores = analysis.get('scores', {})
            
            if wells and scores:
                pos_x, pos_y = self.circular_viz.calculate_narrative_position(wells, scores)
                distance = np.sqrt(pos_x**2 + pos_y**2)
                distances.append(distance)
                positions.append((pos_x, pos_y))
        
        if not distances:
            return ""
        
        avg_distance = np.mean(distances)
        std_distance = np.std(distances)
        max_distance = np.max(distances)
        min_distance = np.min(distances)
        
        return (
            f"<b>Summary Statistics</b><br>"
            f"Analyses: {len(analyses)}<br>"
            f"Avg Distance: {avg_distance:.3f}<br>"
            f"Distance Range: {min_distance:.3f} - {max_distance:.3f}<br>"
            f"Std Deviation: {std_distance:.3f}"
        )
    
    def export_for_publication(self,
                             figure: go.Figure,
                             output_dir: str,
                             filename: str,
                             formats: List[str] = ['html', 'png', 'svg', 'pdf']) -> Dict[str, str]:
        """
        Export figure in multiple publication-ready formats.
        
        Args:
            figure: Plotly figure to export
            output_dir: Directory to save files
            filename: Base filename (without extension)
            formats: List of formats to export
            
        Returns:
            Dictionary mapping format to filepath
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        exported_files = {}
        
        for format_type in formats:
            filepath = output_path / f"{filename}.{format_type}"
            
            try:
                if format_type == 'html':
                    figure.write_html(str(filepath))
                elif format_type == 'png':
                    figure.write_image(str(filepath), format='png', scale=2)
                elif format_type == 'svg':
                    figure.write_image(str(filepath), format='svg')
                elif format_type == 'pdf':
                    figure.write_image(str(filepath), format='pdf')
                else:
                    print(f"⚠️  Unsupported format: {format_type}")
                    continue
                    
                exported_files[format_type] = str(filepath)
                
            except Exception as e:
                print(f"⚠️  Failed to export {format_type}: {e}")
        
        return exported_files
    
    def get_theme_info(self) -> Dict[str, Any]:
        """Get information about the current theme."""
        return {
            'name': self.theme_name,
            'style': self.theme.style,
            'well_colors': self.theme.well_colors,
            'layout_config': self.theme.layout_config
        }


# Convenience function for quick access
def create_visualization_engine(theme: str = 'academic', 
                               figure_size: int = 900) -> NarrativeGravityVisualizationEngine:
    """Create a themed visualization engine."""
    return NarrativeGravityVisualizationEngine(theme=theme, figure_size=figure_size)


if __name__ == '__main__':
    # Demo the visualization engine
    print("🎨 Narrative Gravity Visualization Engine Demo")
    print("=" * 50)
    
    # Create engine with academic theme
    engine = create_visualization_engine(theme='academic')
    
    # Sample data
    wells = {
        'Hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
        'Justice': {'angle': 72, 'type': 'integrative', 'weight': 0.8},
        'Truth': {'angle': 144, 'type': 'integrative', 'weight': 0.8},
        'Fear': {'angle': 216, 'type': 'disintegrative', 'weight': 0.6},
        'Manipulation': {'angle': 288, 'type': 'disintegrative', 'weight': 0.6}
    }
    
    scores = {'Hope': 0.9, 'Justice': 0.7, 'Truth': 0.2, 'Fear': 0.1, 'Manipulation': 0.5}
    
    # Create single analysis
    fig = engine.create_single_analysis(
        wells=wells,
        narrative_scores=scores,
        title='Demo Analysis - Academic Theme',
        show=False
    )
    
    print(f"✅ Created visualization with {engine.theme_name} theme")
    print(f"📊 Theme info: {engine.get_theme_info()['name']}")
    print("🎯 Visualization engine ready for use!") 