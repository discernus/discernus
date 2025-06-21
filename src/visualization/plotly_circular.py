import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path

class PlotlyCircularVisualizer:
    """
    Plotly-based visualizer for circular coordinate system narrative gravity maps.
    Framework-agnostic: supports arbitrary well types, colors, and arrangements.
    
    Features:
    - Interactive visualization with hover info
    - Publication-ready static exports
    - Framework-agnostic well positioning
    - Comparative visualization support
    - Academic styling defaults
    """
    def __init__(self, circle_radius=1.0, type_to_color=None, figure_size=900):
        self.circle_radius = circle_radius
        self.type_to_color = type_to_color or {
            'integrative': '#2E7D32',  # Dark green
            'disintegrative': '#C62828'  # Dark red
        }
        self.figure_size = figure_size
        self.fallback_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        
        # Academic styling defaults
        self.style = {
            'font_family': 'Arial',
            'title_size': 16,
            'subtitle_size': 12,
            'axis_title_size': 12,
            'label_size': 10,
            'well_marker_size': 18,
            'narrative_marker_size': 28,
            'grid_color': 'lightgray',
            'grid_width': 1,
            'boundary_color': 'black',
            'boundary_width': 2
        }

    def get_type_color(self, well_type: str, idx: int) -> str:
        """Get color for a well type, using config or fallback palette."""
        if well_type in self.type_to_color:
            return self.type_to_color[well_type]
        return self.fallback_palette[idx % len(self.fallback_palette)]

    def create_base_figure(self, title: str = None) -> go.Figure:
        """Create base figure with circle boundary and styling."""
        fig = go.Figure()
        
        # Draw unit circle
        theta = np.linspace(0, 2 * np.pi, 361)
        x_circle = self.circle_radius * np.cos(theta)
        y_circle = self.circle_radius * np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle,
            mode='lines',
            line=dict(color=self.style['boundary_color'], width=self.style['boundary_width']),
            name='Boundary',
            showlegend=False
        ))
        
        # Add coordinate axes
        fig.add_hline(y=0, line_dash="dot", line_color=self.style['grid_color'], opacity=0.7)
        fig.add_vline(x=0, line_dash="dot", line_color=self.style['grid_color'], opacity=0.7)
        
        # Base layout with locked aspect ratio
        fig.update_layout(
            width=self.figure_size,
            height=self.figure_size,
            title=dict(
                text=title or 'Circular Narrative Gravity Visualization',
                font=dict(size=self.style['title_size'], family=self.style['font_family'])
            ),
            xaxis=dict(
                visible=False,
                range=[-1.2, 1.2],
                showgrid=True,
                gridcolor=self.style['grid_color'],
                gridwidth=self.style['grid_width'],
                scaleanchor="y",  # Lock aspect ratio to y-axis
                scaleratio=1      # 1:1 ratio ensures circle stays circular
            ),
            yaxis=dict(
                visible=False,
                range=[-1.2, 1.2],
                showgrid=True,
                gridcolor=self.style['grid_color'],
                gridwidth=self.style['grid_width']
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False
        )
        
        return fig

    def calculate_narrative_position(self, wells: Dict, narrative_scores: Dict) -> Tuple[float, float]:
        """Calculate narrative position based on well scores."""
        weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0
        
        for well_name, score in narrative_scores.items():
            if well_name in wells:
                angle = wells[well_name]['angle']
                weight = abs(wells[well_name].get('weight', 1.0))
                x = self.circle_radius * np.cos(np.deg2rad(angle))
                y = self.circle_radius * np.sin(np.deg2rad(angle))
                force = score * weight
                weighted_x += x * force
                weighted_y += y * force
                total_weight += force
                
        if total_weight > 0:
            return weighted_x / total_weight, weighted_y / total_weight
        return 0.0, 0.0

    def plot(self, wells: Dict, narrative_scores: Optional[Dict] = None,
            narrative_label: Optional[str] = None, title: Optional[str] = None,
            output_html: Optional[str] = None, output_png: Optional[str] = None,
            show: bool = True) -> go.Figure:
        """
        Create a complete circular visualization.
        
        Args:
            wells: dict of {well_name: {'angle': deg, 'type': str, 'weight': float, ...}}
            narrative_scores: dict of {well_name: score} (optional)
            narrative_label: str (optional)
            title: str (optional)
            output_html: path to save interactive HTML (optional)
            output_png: path to save static PNG (optional, requires kaleido)
            show: whether to display the figure
        """
        fig = self.create_base_figure(title)
        
        # Plot wells
        well_xs, well_ys, well_labels, well_colors = [], [], [], []
        for idx, (well_name, well) in enumerate(wells.items()):
            angle = well['angle']
            well_type = well.get('type', 'default')
            x = self.circle_radius * np.cos(np.deg2rad(angle))
            y = self.circle_radius * np.sin(np.deg2rad(angle))
            color = self.get_type_color(well_type, idx)
            
            # Draw line from center to well
            fig.add_trace(go.Scatter(
                x=[0, x], y=[0, y],
                mode='lines',
                line=dict(color=color, width=1, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            well_xs.append(x)
            well_ys.append(y)
            well_labels.append(f"{well_name} ({angle}°)")
            well_colors.append(color)
        
        # Add wells as markers
        fig.add_trace(go.Scatter(
            x=well_xs, y=well_ys,
            mode='markers+text',
            marker=dict(
                size=self.style['well_marker_size'],
                color=well_colors,
                line=dict(width=2, color='black')
            ),
            text=well_labels,
            textposition='top center',
            name='Wells',
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # Plot narrative position if provided
        if narrative_scores:
            narrative_x, narrative_y = self.calculate_narrative_position(wells, narrative_scores)
            
            # Add narrative marker
            fig.add_trace(go.Scatter(
                x=[narrative_x], y=[narrative_y],
                mode='markers+text',
                marker=dict(
                    size=self.style['narrative_marker_size'],
                    color='orange',
                    line=dict(width=3, color='black')
                ),
                text=[narrative_label or 'Narrative'],
                textposition='bottom right',
                name='Narrative Position',
                hovertemplate='<b>%{text}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
            ))
            
            # Line from center to narrative
            fig.add_trace(go.Scatter(
                x=[0, narrative_x], y=[0, narrative_y],
                mode='lines',
                line=dict(color='orange', width=2, dash='dash'),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add framework-agnostic metrics
            distance = np.sqrt(narrative_x**2 + narrative_y**2)
            angle_rad = np.arctan2(narrative_y, narrative_x)
            angle_deg = np.degrees(angle_rad) % 360  # Convert to 0-360 degrees
            
            metrics_text = f'Distance: {distance:.3f}<br>Angle: {angle_deg:.1f}°<br>Position: ({narrative_x:+.3f}, {narrative_y:+.3f})'
            
            fig.add_annotation(
                x=0.05,
                y=-0.95,
                text=metrics_text,
                showarrow=False,
                font=dict(size=10),
                bgcolor='rgba(173, 216, 230, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.3)',
                borderwidth=1,
                borderpad=4,
                xanchor='left',
                yanchor='bottom'
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

    def create_comparison(self, analyses: List[Dict], title: str = "Comparative Analysis",
                         output_html: Optional[str] = None,
                         output_png: Optional[str] = None) -> go.Figure:
        """
        Create a comparison visualization with multiple analyses.
        
        Args:
            analyses: List of analysis results, each containing wells and scores
            title: Title for the comparison visualization
            output_html: Path to save interactive HTML
            output_png: Path to save static PNG
        """
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[analysis.get('title', f'Analysis {i+1}') 
                          for i, analysis in enumerate(analyses[:4])],
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                  [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Plot each analysis
        for i, analysis in enumerate(analyses[:4]):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            wells = analysis.get('wells', {})
            scores = analysis.get('scores', {})
            
            # Create base visualization for this subplot
            base_fig = self.create_base_figure()
            
            # Add all traces to the subplot
            for trace in base_fig.data:
                fig.add_trace(trace, row=row, col=col)
                
            # Add wells and narrative position
            subplot_fig = self.plot(wells, scores, show=False)
            for trace in subplot_fig.data[1:]:  # Skip the boundary trace
                fig.add_trace(trace, row=row, col=col)
        
        # Update layout with aspect ratio locking for all subplots
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=self.style['title_size'], family=self.style['font_family'])
            ),
            height=self.figure_size * 2,
            width=self.figure_size * 2,
            showlegend=False
        )
        
        # Lock aspect ratio for all subplots to keep circles circular
        fig.update_xaxes(scaleanchor="y", scaleratio=1, range=[-1.2, 1.2])
        fig.update_yaxes(range=[-1.2, 1.2])
        
        # Save outputs
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
            
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)
            
        return fig

if __name__ == '__main__':
    # Example usage with dummy data
    wells = {
        'Hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
        'Justice': {'angle': 72, 'type': 'integrative', 'weight': 0.8},
        'Truth': {'angle': 144, 'type': 'integrative', 'weight': 0.8},
        'Fear': {'angle': 216, 'type': 'disintegrative', 'weight': 0.6},
        'Manipulation': {'angle': 288, 'type': 'disintegrative', 'weight': 0.6}
    }
    scores = {'Hope': 0.9, 'Justice': 0.7, 'Truth': 0.2, 'Fear': 0.1, 'Manipulation': 0.5}
    
    # Single visualization
    viz = PlotlyCircularVisualizer()
    viz.plot(wells, narrative_scores=scores, narrative_label='Example', 
            title='Single Analysis Example', show=True)
    
    # Comparison visualization
    analyses = [
        {'title': 'Analysis 1', 'wells': wells, 'scores': scores},
        {'title': 'Analysis 2', 'wells': wells, 'scores': {k: 1-v for k,v in scores.items()}},
        {'title': 'Analysis 3', 'wells': wells, 'scores': {k: v*0.5 for k,v in scores.items()}},
        {'title': 'Analysis 4', 'wells': wells, 'scores': {k: abs(np.sin(v)) for k,v in scores.items()}}
    ]
    viz.create_comparison(analyses, title='Comparison Example', 
                         output_html='comparison_example.html') 