"""
Theoretical Weighting Visualization
===================================

Specialized visualization tools for theoretical weighting analysis in the DCS.
Implements Framework Specification v3.2 theoretical weighting modeling capabilities.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy import stats


class TheoreticalWeightingVisualizer:
    """
    Specialized visualizer for theoretical weighting analysis and mapping.
    """
    
    def __init__(self, resolution: int = 100):
        self.resolution = resolution
        self.style = {
            "weighting_colorscale": "Viridis",
            "contour_colorscale": "Blues", 
            "overlay_opacity": 0.6
        }
    
    def create_weighting_heatmap(
        self,
        anchors: Dict,
        title: str = "Theoretical Weighting Distribution",
        show_contours: bool = True,
        show: bool = True
    ) -> go.Figure:
        """
        Create theoretical weighting heatmap showing anchor influence zones.
        """
        # Calculate weighting grid
        weighting_grid = self._calculate_weighting_grid(anchors)
        
        # Create coordinate grids
        x_coords = np.linspace(-1.2, 1.2, self.resolution)
        y_coords = np.linspace(-1.2, 1.2, self.resolution)
        
        fig = go.Figure()
        
        # Add weighting heatmap
        fig.add_trace(go.Heatmap(
            z=weighting_grid,
            x=x_coords,
            y=y_coords,
            colorscale=self.style["weighting_colorscale"],
            opacity=self.style["overlay_opacity"],
            colorbar=dict(title="Theoretical Weighting"),
            hovertemplate="Weighting: %{z:.3f}<extra></extra>"
        ))
        
        # Add contour lines if requested
        if show_contours:
            fig.add_trace(go.Contour(
                z=weighting_grid,
                x=x_coords,
                y=y_coords,
                colorscale=self.style["contour_colorscale"],
                showscale=False,
                opacity=0.4,
                line=dict(width=1),
                hovertemplate="Weighting Level: %{z:.3f}<extra></extra>"
            ))
        
        # Add unit circle boundary
        theta = np.linspace(0, 2*np.pi, 361)
        fig.add_trace(go.Scatter(
            x=np.cos(theta),
            y=np.sin(theta),
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add anchors
        self._add_weighting_anchors(fig, anchors)
        
        # Layout
        fig.update_layout(
            title=title,
            xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2]),
            showlegend=True
        )
        
        if show:
            fig.show()
        
        return fig
    
    def _calculate_weighting_grid(self, anchors: Dict) -> np.ndarray:
        """Calculate theoretical weighting across coordinate space."""
        x = np.linspace(-1.2, 1.2, self.resolution)
        y = np.linspace(-1.2, 1.2, self.resolution)
        X, Y = np.meshgrid(x, y)
        
        weighting = np.zeros_like(X)
        
        for anchor_name, anchor_def in anchors.items():
            angle = np.deg2rad(anchor_def['angle'])
            weight = anchor_def.get('weight', 1.0)
            
            # Anchor position
            anchor_x = np.cos(angle)
            anchor_y = np.sin(angle)
            
            # Gaussian kernel
            sigma = 0.25  # Bandwidth
            distance_sq = (X - anchor_x)**2 + (Y - anchor_y)**2
            weighting += weight * np.exp(-distance_sq / (2 * sigma**2))
        
        return weighting
    
    def _add_weighting_anchors(self, fig: go.Figure, anchors: Dict):
        """Add anchor markers to weighting plot."""
        for anchor_name, anchor_def in anchors.items():
            angle = np.deg2rad(anchor_def['angle'])
            weight = anchor_def.get('weight', 1.0)
            
            x = np.cos(angle)
            y = np.sin(angle)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=15 + 10*weight,
                    color='white',
                    line=dict(width=3, color='black')
                ),
                text=[anchor_name],
                textposition='top center',
                name=anchor_name,
                hovertemplate=f"<b>{anchor_name}</b><br>Weight: {weight}<extra></extra>"
            )) 