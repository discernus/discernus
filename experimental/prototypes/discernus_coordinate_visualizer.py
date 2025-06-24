#!/usr/bin/env python3
"""
Discernus Coordinate Visualizer
==============================

Plotly-based coordinate system visualization component using cartographic terminology.
Migrated from PlotlyCircularVisualizer with updated terminology:
- "wells" → "anchors"
- "narrative_position" → "centroid"
- "narrative_scores" → "axis_scores"/"anchor_scores"
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

import sys
sys.path.append('/Volumes/dev/discernus/experimental/prototypes')
from discernus_themes import get_theme, VisualizationTheme


class DiscernusCoordinateVisualizer:
    """
    Plotly-based coordinate system visualizer for DCS (Discernus Coordinate System).
    
    Features:
    - Circular coordinate system with anchors on perimeter
    - Centroid positioning based on anchor scores
    - Theme-aware styling
    - Interactive Plotly visualizations
    - Support for both ASFx and ASFa frameworks
    """
    
    def __init__(self, radius: float = 1.0, figure_size: int = 800, theme: str = 'academic'):
        self.radius = radius
        self.figure_size = figure_size
        self.theme = get_theme(theme)
        
    def plot_coordinate_system(self, 
                             anchors: Dict[str, Dict],
                             axis_scores: Optional[Dict[str, float]] = None,
                             anchor_scores: Optional[Dict[str, float]] = None,
                             title: str = "Discernus Coordinate System",
                             centroid_label: str = "Centroid",
                             output_html: Optional[str] = None,
                             output_png: Optional[str] = None,
                             show: bool = True) -> go.Figure:
        """
        Plot coordinate system with anchors and centroid.
        
        Args:
            anchors: Dictionary of anchor definitions with angles, types, weights
            axis_scores: Scores along framework axes (for ASFx frameworks)
            anchor_scores: Scores toward individual anchors (for ASFa frameworks)
            title: Chart title
            centroid_label: Label for centroid position
            output_html: Path to save interactive HTML
            output_png: Path to save static PNG
            show: Whether to display the figure
            
        Returns:
            Plotly figure object
        """
        # Use whichever scores are provided
        scores = axis_scores or anchor_scores or {}
        
        # Calculate centroid position
        centroid = self.calculate_centroid(anchors, scores)
        
        # Create figure
        fig = go.Figure()
        
        # Add coordinate system boundary (unit circle)
        self._add_coordinate_boundary(fig)
        
        # Add anchors on perimeter
        self._add_anchors(fig, anchors, scores)
        
        # Add centroid if scores provided
        if scores:
            self._add_centroid(fig, centroid, centroid_label)
        
        # Add grid lines and axes
        self._add_coordinate_grid(fig)
        
        # Apply styling
        self._apply_coordinate_styling(fig, title)
        
        # Save outputs if specified
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
            
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png, width=self.figure_size, height=self.figure_size, scale=2)
        
        if show:
            fig.show()
            
        return fig
    
    def create_comparative_coordinate_plot(self, 
                                         analyses: List[Dict[str, Any]],
                                         title: str = "Comparative Coordinate Analysis",
                                         output_html: Optional[str] = None,
                                         show: bool = True) -> go.Figure:
        """
        Create comparative plot showing multiple centroids.
        
        Args:
            analyses: List of analysis dictionaries containing anchors, scores, and metadata
            title: Chart title
            output_html: Path to save interactive HTML
            show: Whether to display the figure
            
        Returns:
            Plotly figure object
        """
        if not analyses:
            return go.Figure()
        
        fig = go.Figure()
        
        # Use first analysis for anchor positions
        anchors = analyses[0].get('anchors', {})
        
        # Add coordinate system boundary
        self._add_coordinate_boundary(fig)
        
        # Add anchors (once, from first analysis)
        self._add_anchors(fig, anchors, {})
        
        # Add centroids for each analysis
        colors = px.colors.qualitative.Set1
        for i, analysis in enumerate(analyses):
            centroid = analysis.get('centroid')
            if centroid is None:
                # Calculate if not provided
                analysis_anchors = analysis.get('anchors', anchors)
                analysis_scores = analysis.get('scores', {})
                centroid = self.calculate_centroid(analysis_anchors, analysis_scores)
            
            color = colors[i % len(colors)]
            analysis_title = analysis.get('title', f'Analysis {i+1}')
            
            self._add_centroid(fig, centroid, analysis_title, color=color)
        
        # Add coordinate grid
        self._add_coordinate_grid(fig)
        
        # Apply styling
        self._apply_coordinate_styling(fig, title)
        
        # Save outputs if specified
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
        
        if show:
            fig.show()
            
        return fig
    
    def calculate_centroid(self, anchors: Dict[str, Dict], scores: Dict[str, float]) -> Tuple[float, float]:
        """
        Calculate centroid position from anchor scores.
        
        Args:
            anchors: Dictionary of anchor definitions with angles, types, weights
            scores: Dictionary of scores for each anchor
            
        Returns:
            Tuple of (x, y) coordinates for centroid position
        """
        total_x = 0.0
        total_y = 0.0
        total_weight = 0.0
        
        for anchor_name, score in scores.items():
            if anchor_name in anchors:
                anchor = anchors[anchor_name]
                angle = anchor['angle']
                weight = abs(anchor.get('weight', 1.0))
                
                # Convert angle to radians and calculate position
                angle_rad = np.radians(angle)
                x = np.cos(angle_rad) * self.radius
                y = np.sin(angle_rad) * self.radius
                
                # Weight the contribution
                weighted_score = score * weight
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # Apply adaptive scaling to keep centroid inside boundary
            scaling_factor = 0.8  # TODO: Make this adaptive based on score distribution
            return (centroid_x * scaling_factor, centroid_y * scaling_factor)
        
        return (0.0, 0.0)
    
    def _add_coordinate_boundary(self, fig: go.Figure):
        """Add coordinate system boundary circle."""
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = self.radius * np.cos(circle_angles)
        circle_y = self.radius * np.sin(circle_angles)
        
        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line=dict(
                color=self.theme.style['boundary_color'], 
                width=self.theme.style['boundary_width']
            ),
            name='Coordinate Boundary',
            showlegend=False,
            hoverinfo='skip'
        ))
    
    def _add_anchors(self, fig: go.Figure, anchors: Dict[str, Dict], scores: Dict[str, float]):
        """Add anchor points on the coordinate system perimeter."""
        for anchor_name, anchor_data in anchors.items():
            angle_rad = np.radians(anchor_data['angle'])
            x = self.radius * np.cos(angle_rad)
            y = self.radius * np.sin(angle_rad)
            
            # Get anchor type color
            anchor_type = anchor_data.get('type', 'default')
            color = self.theme.anchor_colors.get(anchor_type, self.theme.anchor_colors['default'])
            
            # Scale marker size and opacity by score if available
            score = scores.get(anchor_name, 0.5)
            marker_size = self.theme.style['anchor_marker_size'] + (score * 8)
            opacity = 0.6 + (score * 0.4)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[anchor_name],
                textposition='middle center',
                textfont=dict(
                    size=self.theme.style['label_size'],
                    color='white',
                    family=self.theme.style['font_family']
                ),
                marker=dict(
                    size=marker_size,
                    color=color,
                    opacity=opacity,
                    line=dict(width=2, color='white')
                ),
                name=anchor_name,
                showlegend=False,
                hovertemplate=f"<b>{anchor_name}</b><br>" +
                             f"Type: {anchor_type}<br>" +
                             f"Angle: {anchor_data['angle']}°<br>" +
                             f"Score: {score:.3f}<extra></extra>"
            ))
    
    def _add_centroid(self, fig: go.Figure, centroid: Tuple[float, float], 
                     label: str, color: str = 'orange'):
        """Add centroid point to the coordinate system."""
        fig.add_trace(go.Scatter(
            x=[centroid[0]], y=[centroid[1]],
            mode='markers',
            marker=dict(
                size=self.theme.style['centroid_marker_size'],
                color=color,
                symbol='star',
                line=dict(width=2, color='white')
            ),
            name=label,
            showlegend=True,
            hovertemplate=f"<b>{label}</b><br>" +
                         f"Position: ({centroid[0]:.3f}, {centroid[1]:.3f})<br>" +
                         f"Distance from center: {np.sqrt(centroid[0]**2 + centroid[1]**2):.3f}<extra></extra>"
        ))
    
    def _add_coordinate_grid(self, fig: go.Figure):
        """Add coordinate grid lines."""
        # Add horizontal and vertical axes
        fig.add_hline(y=0, line=dict(color=self.theme.style['grid_color'], width=1, dash='dash'))
        fig.add_vline(x=0, line=dict(color=self.theme.style['grid_color'], width=1, dash='dash'))
        
        # Add quarter-circle guides
        for radius in [0.25, 0.5, 0.75]:
            circle_angles = np.linspace(0, 2*np.pi, 100)
            circle_x = radius * np.cos(circle_angles)
            circle_y = radius * np.sin(circle_angles)
            
            fig.add_trace(go.Scatter(
                x=circle_x, y=circle_y,
                mode='lines',
                line=dict(
                    color=self.theme.style['grid_color'], 
                    width=self.theme.style['grid_width'], 
                    dash='dot'
                ),
                showlegend=False,
                hoverinfo='skip',
                opacity=0.3
            ))
    
    def _apply_coordinate_styling(self, fig: go.Figure, title: str):
        """Apply theme-based styling to the coordinate system."""
        # Calculate plot range with padding
        plot_range = [-self.radius * 1.2, self.radius * 1.2]
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    size=self.theme.style['title_size'],
                    family=self.theme.style['font_family']
                ),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                range=plot_range,
                scaleanchor="y",
                scaleratio=1,
                showgrid=True,
                gridcolor=self.theme.style['grid_color'],
                gridwidth=self.theme.style['grid_width'],
                zeroline=True,
                zerolinecolor=self.theme.style['grid_color'],
                showticklabels=False,
                title=""  # Hide axis titles
            ),
            yaxis=dict(
                range=plot_range,
                showgrid=True,
                gridcolor=self.theme.style['grid_color'],
                gridwidth=self.theme.style['grid_width'],
                zeroline=True,
                zerolinecolor=self.theme.style['grid_color'],
                showticklabels=False,
                title=""  # Hide axis titles
            ),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            font=dict(
                family=self.theme.style['font_family'],
                size=self.theme.style['label_size']
            ),
            width=self.figure_size,
            height=self.figure_size,
            margin=dict(l=50, r=50, t=80, b=50)
        )
    
    def create_multi_framework_comparison(self, 
                                        framework_analyses: Dict[str, List[Dict]],
                                        title: str = "Multi-Framework Coordinate Comparison") -> go.Figure:
        """
        Create comparison across multiple frameworks.
        
        Args:
            framework_analyses: Dict mapping framework names to lists of analyses
            title: Chart title
            
        Returns:
            Plotly figure with subplots for each framework
        """
        from plotly.subplots import make_subplots
        
        n_frameworks = len(framework_analyses)
        
        # Determine subplot layout
        if n_frameworks <= 2:
            rows, cols = 1, n_frameworks
        elif n_frameworks <= 4:
            rows, cols = 2, 2
        else:
            rows, cols = 2, 3  # Max 6 frameworks
        
        subplot_titles = list(framework_analyses.keys())
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            specs=[[{"type": "scatter"} for _ in range(cols)] for _ in range(rows)]
        )
        
        for i, (framework_name, analyses) in enumerate(framework_analyses.items()):
            if i >= rows * cols:
                break
                
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            if analyses:
                # Add coordinate system for this framework
                anchors = analyses[0].get('anchors', {})
                
                # Add boundary
                circle_angles = np.linspace(0, 2*np.pi, 100)
                circle_x = self.radius * np.cos(circle_angles)
                circle_y = self.radius * np.sin(circle_angles)
                
                fig.add_trace(go.Scatter(
                    x=circle_x, y=circle_y,
                    mode='lines',
                    line=dict(color='gray', width=1),
                    showlegend=False,
                    hoverinfo='skip'
                ), row=row, col=col)
                
                # Add anchors and centroids
                colors = px.colors.qualitative.Set1
                for j, analysis in enumerate(analyses[:5]):  # Limit to 5 per framework
                    centroid = analysis.get('centroid', (0, 0))
                    
                    fig.add_trace(go.Scatter(
                        x=[centroid[0]], y=[centroid[1]],
                        mode='markers',
                        marker=dict(
                            size=8,
                            color=colors[j % len(colors)],
                            symbol='star'
                        ),
                        name=analysis.get('title', f'{framework_name}_{j}'),
                        showlegend=(row == 1 and col == 1)  # Only show legend for first subplot
                    ), row=row, col=col)
        
        # Update layout
        fig.update_layout(
            title=title,
            font=dict(family=self.theme.style['font_family']),
            height=400 * rows,
            width=400 * cols
        )
        
        # Make all subplots have equal aspect ratio
        for i in range(1, rows * cols + 1):
            row_idx = (i-1)//cols + 1
            col_idx = (i-1)%cols + 1
            fig.update_xaxes(
                range=[-1.2, 1.2], 
                scaleanchor=f"y{i}", 
                scaleratio=1,
                row=row_idx, 
                col=col_idx
            )
            fig.update_yaxes(
                range=[-1.2, 1.2], 
                row=row_idx, 
                col=col_idx
            )
        
        return fig


if __name__ == '__main__':
    print("🗺️ Discernus Coordinate Visualizer Demo")
    print("=" * 50)
    
    # Create visualizer
    viz = DiscernusCoordinateVisualizer(theme='academic')
    
    # Sample anchors
    anchors = {
        'Hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
        'Justice': {'angle': 90, 'type': 'integrative', 'weight': 0.8},
        'Truth': {'angle': 180, 'type': 'integrative', 'weight': 0.8},
        'Fear': {'angle': 270, 'type': 'disintegrative', 'weight': 0.6}
    }
    
    # Sample scores
    axis_scores = {'Hope': 0.8, 'Justice': 0.6, 'Truth': 0.4, 'Fear': 0.2}
    
    # Create plot
    fig = viz.plot_coordinate_system(
        anchors=anchors,
        axis_scores=axis_scores,
        title='Demo Coordinate System - Cartographic Terminology',
        show=False
    )
    
    print("✅ Coordinate system visualization created!")
    print("🎯 Using Plotly with cartographic terminology") 