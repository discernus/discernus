"""
Advanced DCS Visualization Engine
================================

Enhanced visualization capabilities for the Discernus Coordinate System implementing
Framework Specification v3.2 advanced features including:
- Theoretical weighting heatmaps
- Arc positioning visualization
- Competitive dynamics overlays
- Temporal evolution plotting
- Framework comparison matrices

Built on the existing RebootPlotlyCircularVisualizer foundation.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
from datetime import datetime

# Import base functionality
from ..reporting.reboot_plotly_circular import RebootPlotlyCircularVisualizer


class AdvancedDCSVisualizer(RebootPlotlyCircularVisualizer):
    """
    Advanced visualization engine extending the base circular visualizer with
    Framework Specification v3.2 enhanced capabilities.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.advanced_style = {
            **self.style,
            "weighting_colorscale": "Viridis",
            "competition_colorscale": "RdYlBu",
            "temporal_colorscale": "Plasma",
            "arc_opacity": 0.3,
            "weighting_resolution": 100,
            "animation_duration": 1000
        }
    
    def plot_with_weighting_heatmap(
        self,
        anchors: Dict,
        signature_scores: Optional[Dict] = None,
        framework_config: Optional[Dict] = None,
        title: str = "DCS with Theoretical Weighting",
        show_anchors: bool = True,
        show_centroid: bool = True,
        weighting_opacity: float = 0.6,
        show: bool = True
    ) -> go.Figure:
        """
        Create circular plot with theoretical weighting heatmap overlay.
        
        Demonstrates Framework Specification v3.2 theoretical weighting modeling
        and arc positioning effects.
        """
        fig = self.create_base_figure(title)
        
        # Generate weighting heatmap
        if framework_config and framework_config.get('positioning_strategy'):
            weighting_data = self._calculate_theoretical_weighting(anchors, framework_config)
            self._add_weighting_heatmap(fig, weighting_data, weighting_opacity)
        
        # Add arc visualizations if specified
        if framework_config and 'arcs' in framework_config.get('positioning_strategy', {}):
            self._add_arc_visualizations(fig, framework_config['positioning_strategy']['arcs'])
        
        # Add standard anchors and centroid
        if show_anchors:
            self._add_enhanced_anchors(fig, anchors)
        
        if signature_scores and show_centroid:
            centroid = self.calculate_centroid(anchors, signature_scores)
            self._add_enhanced_centroid(fig, centroid, signature_scores)
        
        if show:
            fig.show()
        
        return fig
    
    # Backward compatibility
    def plot_with_density_heatmap(self, *args, **kwargs):
        """Deprecated: Use plot_with_weighting_heatmap instead."""
        # Handle parameter name change
        if 'density_opacity' in kwargs:
            kwargs['weighting_opacity'] = kwargs.pop('density_opacity')
        return self.plot_with_weighting_heatmap(*args, **kwargs)
    
    def plot_competitive_dynamics(
        self,
        anchors: Dict,
        competition_config: Dict,
        signature_scores: Optional[Dict] = None,
        title: str = "Competitive Dynamics Analysis",
        show: bool = True
    ) -> go.Figure:
        """
        Visualize competitive relationships between anchors.
        
        Shows Framework Specification v3.2 competitive dynamics with
        dilution effects and semantic space allocation.
        """
        fig = self.create_base_figure(title)
        
        # Add competition relationship lines
        if 'competition_pairs' in competition_config:
            self._add_competition_lines(fig, anchors, competition_config['competition_pairs'])
        
        # Add anchors with competition strength indicators
        self._add_competitive_anchors(fig, anchors, competition_config)
        
        # Add signature with competition effects if provided
        if signature_scores:
            adjusted_scores = self._apply_competition_effects(signature_scores, competition_config)
            centroid = self.calculate_centroid(anchors, adjusted_scores)
            self._add_enhanced_centroid(fig, centroid, adjusted_scores, label="Competitive Centroid")
        
        # Add legend explaining competition visualization
        self._add_competition_legend(fig, competition_config)
        
        if show:
            fig.show()
        
        return fig
    
    def plot_temporal_evolution(
        self,
        anchors: Dict,
        temporal_data: List[Dict],
        title: str = "Temporal Evolution Analysis",
        show_trajectory: bool = True,
        show_velocity: bool = True,
        show: bool = True
    ) -> go.Figure:
        """
        Visualize centroid movement over time.
        
        Demonstrates Framework Specification v3.2 temporal evolution tracking
        with velocity vectors and acceleration analysis.
        """
        fig = self.create_base_figure(title)
        
        # Extract temporal trajectory
        centroids = []
        timestamps = []
        for data_point in temporal_data:
            centroid = self.calculate_centroid(anchors, data_point['signature_scores'])
            centroids.append(centroid)
            timestamps.append(data_point.get('timestamp', len(centroids)))
        
        # Add trajectory path
        if show_trajectory:
            self._add_trajectory_path(fig, centroids, timestamps)
        
        # Add velocity vectors
        if show_velocity and len(centroids) > 1:
            self._add_velocity_vectors(fig, centroids, timestamps)
        
        # Add temporal anchor positions
        self._add_enhanced_anchors(fig, anchors)
        
        # Add temporal evolution statistics
        self._add_temporal_statistics(fig, centroids, timestamps)
        
        if show:
            fig.show()
        
        return fig
    
    def create_framework_comparison_matrix(
        self,
        frameworks: Dict[str, Dict],
        corpus_analysis: Dict[str, List[Dict]],
        title: str = "Framework Comparison Matrix"
    ) -> go.Figure:
        """
        Create side-by-side comparison of multiple frameworks on the same corpus.
        
        Enables Framework Specification v3.2 cross-framework portability analysis.
        """
        n_frameworks = len(frameworks)
        
        # Create subplot grid
        cols = min(3, n_frameworks)
        rows = (n_frameworks + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=list(frameworks.keys()),
            specs=[[{"type": "scatter"} for _ in range(cols)] for _ in range(rows)]
        )
        
        # Add each framework analysis
        for idx, (framework_name, framework_def) in enumerate(frameworks.items()):
            row = (idx // cols) + 1
            col = (idx % cols) + 1
            
            # Get analysis results for this framework
            framework_results = corpus_analysis.get(framework_name, [])
            
            # Create framework-specific visualization
            framework_fig = self.plot_with_weighting_heatmap(
                anchors=framework_def.get('anchors', {}),
                title=f"{framework_name} Analysis",
                show=False
            )
            
            # Add to subplot
            for trace in framework_fig.data:
                fig.add_trace(trace, row=row, col=col)
            
            # Add corpus centroids for this framework
            if framework_results:
                self._add_corpus_centroids(fig, framework_results, row, col)
        
        # Update layout
        fig.update_layout(
            title=title,
            showlegend=False,
            height=400 * rows,
            width=400 * cols
        )
        
        # Lock aspect ratios
        fig.update_xaxes(scaleanchor="y", scaleratio=1, range=[-1.2, 1.2])
        fig.update_yaxes(range=[-1.2, 1.2])
        
        return fig
    
    # Private helper methods
    
    def _calculate_theoretical_weighting(self, anchors: Dict, framework_config: Dict) -> np.ndarray:
        """Calculate theoretical weighting distribution across the coordinate space."""
        # Create grid for weighting calculation
        resolution = self.advanced_style["weighting_resolution"]
        x = np.linspace(-1.2, 1.2, resolution)
        y = np.linspace(-1.2, 1.2, resolution)
        X, Y = np.meshgrid(x, y)
        
        # Initialize weighting array
        weighting = np.zeros_like(X)
        
        # Calculate weighting contribution from each anchor
        for anchor_name, anchor_def in anchors.items():
            angle = np.deg2rad(anchor_def['angle'])
            weight = anchor_def.get('weight', 1.0)
            
            # Anchor position
            anchor_x = np.cos(angle)
            anchor_y = np.sin(angle)
            
            # Gaussian weighting contribution
            sigma = 0.3  # Bandwidth for weighting calculation
            distance_sq = (X - anchor_x)**2 + (Y - anchor_y)**2
            weighting += weight * np.exp(-distance_sq / (2 * sigma**2))
        
        return weighting
    
    def _add_weighting_heatmap(self, fig: go.Figure, weighting_data: np.ndarray, opacity: float):
        """Add theoretical weighting heatmap as background."""
        fig.add_trace(go.Heatmap(
            z=weighting_data,
            x=np.linspace(-1.2, 1.2, weighting_data.shape[1]),
            y=np.linspace(-1.2, 1.2, weighting_data.shape[0]),
            colorscale=self.advanced_style["weighting_colorscale"],
            opacity=opacity,
            showscale=True,
            colorbar=dict(title="Theoretical Weighting"),
            hovertemplate="Weighting: %{z:.3f}<extra></extra>"
        ))
    
    def _add_arc_visualizations(self, fig: go.Figure, arcs_config: Dict):
        """Add arc boundary visualizations."""
        for arc_name, arc_def in arcs_config.items():
            center_angle = arc_def['center_angle']
            span = arc_def['span']
            
            # Calculate arc boundaries
            start_angle = np.deg2rad(center_angle - span/2)
            end_angle = np.deg2rad(center_angle + span/2)
            
            # Create arc visualization
            angles = np.linspace(start_angle, end_angle, 50)
            x_arc = np.cos(angles)
            y_arc = np.sin(angles)
            
            # Add arc boundary
            fig.add_trace(go.Scatter(
                x=x_arc, y=y_arc,
                mode='lines',
                line=dict(color='orange', width=3, dash='dash'),
                opacity=self.advanced_style["arc_opacity"],
                name=f"{arc_name} Arc",
                hovertemplate=f"{arc_name}<br>Span: {span}°<extra></extra>"
            ))
    
    def _add_enhanced_anchors(self, fig: go.Figure, anchors: Dict):
        """Add anchors with enhanced styling and information."""
        for anchor_name, anchor_def in anchors.items():
            angle = np.deg2rad(anchor_def['angle'])
            weight = anchor_def.get('weight', 1.0)
            anchor_type = anchor_def.get('type', 'default')
            
            x = np.cos(angle)
            y = np.sin(angle)
            
            # Size based on weight
            marker_size = 15 + 10 * weight
            
            # Color based on type
            color = self.get_anchor_type_color(anchor_type, 0)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=marker_size,
                    color=color,
                    line=dict(width=2, color='black'),
                    symbol='circle'
                ),
                text=[anchor_name],
                textposition='top center',
                name=anchor_name,
                hovertemplate=f"<b>{anchor_name}</b><br>"
                             f"Angle: {anchor_def['angle']}°<br>"
                             f"Weight: {weight}<br>"
                             f"Type: {anchor_type}<extra></extra>"
            ))
    
    def _add_enhanced_centroid(self, fig: go.Figure, centroid: Tuple[float, float], 
                             signature_scores: Dict, label: str = "Centroid"):
        """Add centroid with enhanced information display."""
        x, y = centroid
        
        # Calculate signature strength
        total_strength = sum(signature_scores.values())
        distance = np.sqrt(x**2 + y**2)
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=25,
                color='red',
                symbol='star',
                line=dict(width=3, color='darkred')
            ),
            text=[label],
            textposition='bottom center',
            name=label,
            hovertemplate=f"<b>{label}</b><br>"
                         f"Position: ({x:.3f}, {y:.3f})<br>"
                         f"Distance: {distance:.3f}<br>"
                         f"Total Strength: {total_strength:.3f}<extra></extra>"
        ))
        
        # Add centroid line
        fig.add_trace(go.Scatter(
            x=[0, x], y=[0, y],
            mode='lines',
            line=dict(color='red', width=2, dash='solid'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    def _add_competition_lines(self, fig: go.Figure, anchors: Dict, competition_pairs: List[Dict]):
        """Add lines showing competitive relationships."""
        for pair in competition_pairs:
            anchor_ids = pair['anchors']
            strength = pair.get('strength', 0.5)
            
            if len(anchor_ids) == 2 and all(aid in anchors for aid in anchor_ids):
                # Get anchor positions
                pos1 = self._get_anchor_position(anchors[anchor_ids[0]])
                pos2 = self._get_anchor_position(anchors[anchor_ids[1]])
                
                # Add competition line
                fig.add_trace(go.Scatter(
                    x=[pos1[0], pos2[0]],
                    y=[pos1[1], pos2[1]],
                    mode='lines',
                    line=dict(
                        color='purple',
                        width=2 + 3 * strength,
                        dash='dot'
                    ),
                    opacity=0.7,
                    name=f"Competition: {anchor_ids[0]} ↔ {anchor_ids[1]}",
                    hovertemplate=f"Competition<br>"
                                 f"{anchor_ids[0]} ↔ {anchor_ids[1]}<br>"
                                 f"Strength: {strength:.2f}<extra></extra>"
                ))
    
    def _get_anchor_position(self, anchor_def: Dict) -> Tuple[float, float]:
        """Get x, y position for an anchor."""
        angle = np.deg2rad(anchor_def['angle'])
        return (np.cos(angle), np.sin(angle))
    
    def _add_competitive_anchors(self, fig: go.Figure, anchors: Dict, competition_config: Dict):
        """Add anchors with competition strength indicators."""
        # Standard anchor plotting with competition effects
        self._add_enhanced_anchors(fig, anchors)
    
    def _apply_competition_effects(self, signature_scores: Dict, competition_config: Dict) -> Dict:
        """Apply competitive dilution effects to signature scores."""
        # Simplified competition effect - reduce scores based on competition strength
        adjusted_scores = signature_scores.copy()
        
        for pair in competition_config.get('competition_pairs', []):
            anchor_ids = pair['anchors']
            strength = pair.get('strength', 0.5)
            
            for anchor_id in anchor_ids:
                if anchor_id in adjusted_scores:
                    # Simple dilution: reduce score based on competition
                    adjusted_scores[anchor_id] *= (1 - 0.1 * strength)
        
        return adjusted_scores
    
    def _add_competition_legend(self, fig: go.Figure, competition_config: Dict):
        """Add legend explaining competition visualization."""
        # Add text annotation explaining the competition visualization
        legend_text = "Competition Effects:<br>"
        legend_text += "• Dotted lines show competitive relationships<br>"
        legend_text += "• Line thickness indicates competition strength<br>"
        legend_text += "• Centroid shows result after competition dilution"
        
        fig.add_annotation(
            x=1.02, y=0.02,
            text=legend_text,
            showarrow=False,
            font=dict(size=10),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=1,
            xanchor="left",
            yanchor="bottom",
            xref="paper",
            yref="paper"
        )
    
    def _add_trajectory_path(self, fig: go.Figure, centroids: List[Tuple[float, float]], timestamps: List):
        """Add temporal trajectory path."""
        x_coords = [c[0] for c in centroids]
        y_coords = [c[1] for c in centroids]
        
        # Add trajectory line
        fig.add_trace(go.Scatter(
            x=x_coords, y=y_coords,
            mode='lines+markers',
            line=dict(color='green', width=3),
            marker=dict(size=8, color='lightgreen'),
            name='Temporal Trajectory',
            hovertemplate="Time: %{text}<br>Position: (%{x:.3f}, %{y:.3f})<extra></extra>",
            text=[f"t{i}" for i in range(len(centroids))]
        ))
        
        # Add start and end markers
        if len(centroids) > 1:
            fig.add_trace(go.Scatter(
                x=[x_coords[0]], y=[y_coords[0]],
                mode='markers+text',
                marker=dict(size=15, color='green', symbol='circle'),
                text=['START'],
                textposition='bottom center',
                name='Start Position'
            ))
            
            fig.add_trace(go.Scatter(
                x=[x_coords[-1]], y=[y_coords[-1]],
                mode='markers+text',
                marker=dict(size=15, color='darkgreen', symbol='square'),
                text=['END'],
                textposition='top center',
                name='End Position'
            ))
    
    def _add_velocity_vectors(self, fig: go.Figure, centroids: List[Tuple[float, float]], timestamps: List):
        """Add velocity vectors showing direction and speed of movement."""
        for i in range(len(centroids) - 1):
            current = centroids[i]
            next_pos = centroids[i + 1]
            
            # Calculate velocity vector
            dx = next_pos[0] - current[0]
            dy = next_pos[1] - current[1]
            magnitude = np.sqrt(dx**2 + dy**2)
            
            if magnitude > 0.01:  # Only show significant movements
                # Scale vector for visibility
                scale = min(0.2, magnitude * 5)
                dx_scaled = dx * scale / magnitude
                dy_scaled = dy * scale / magnitude
                
                # Add arrow
                fig.add_trace(go.Scatter(
                    x=[current[0], current[0] + dx_scaled],
                    y=[current[1], current[1] + dy_scaled],
                    mode='lines',
                    line=dict(color='blue', width=2),
                    showlegend=False,
                    hovertemplate=f"Velocity<br>Magnitude: {magnitude:.3f}<extra></extra>"
                ))
                
                # Add arrowhead
                self._add_arrowhead(fig, current, (dx_scaled, dy_scaled))
    
    def _add_arrowhead(self, fig: go.Figure, start: Tuple[float, float], vector: Tuple[float, float]):
        """Add arrowhead to velocity vector."""
        x_start, y_start = start
        dx, dy = vector
        
        # Calculate arrowhead points
        arrow_length = 0.05
        arrow_angle = np.pi / 6  # 30 degrees
        
        # End point of arrow
        x_end = x_start + dx
        y_end = y_start + dy
        
        # Arrowhead points
        angle = np.arctan2(dy, dx)
        x1 = x_end - arrow_length * np.cos(angle - arrow_angle)
        y1 = y_end - arrow_length * np.sin(angle - arrow_angle)
        x2 = x_end - arrow_length * np.cos(angle + arrow_angle)
        y2 = y_end - arrow_length * np.sin(angle + arrow_angle)
        
        # Add arrowhead
        fig.add_trace(go.Scatter(
            x=[x1, x_end, x2],
            y=[y1, y_end, y2],
            mode='lines',
            line=dict(color='blue', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    def _add_temporal_statistics(self, fig: go.Figure, centroids: List[Tuple[float, float]], timestamps: List):
        """Add temporal evolution statistics."""
        if len(centroids) < 2:
            return
        
        # Calculate statistics
        distances = [np.sqrt(c[0]**2 + c[1]**2) for c in centroids]
        total_distance = sum(np.sqrt((centroids[i+1][0] - centroids[i][0])**2 + 
                                   (centroids[i+1][1] - centroids[i][1])**2)
                           for i in range(len(centroids) - 1))
        
        # Create statistics text
        stats_text = f"Temporal Statistics:<br>"
        stats_text += f"• Total Path Length: {total_distance:.3f}<br>"
        stats_text += f"• Start Distance: {distances[0]:.3f}<br>"
        stats_text += f"• End Distance: {distances[-1]:.3f}<br>"
        stats_text += f"• Net Displacement: {np.sqrt((centroids[-1][0] - centroids[0][0])**2 + (centroids[-1][1] - centroids[0][1])**2):.3f}"
        
        fig.add_annotation(
            x=0.02, y=0.98,
            text=stats_text,
            showarrow=False,
            font=dict(size=10),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=1,
            xanchor="left",
            yanchor="top",
            xref="paper",
            yref="paper"
        )
    
    def _add_corpus_centroids(self, fig: go.Figure, framework_results: List[Dict], row: int, col: int):
        """Add corpus centroid analysis to framework comparison subplot."""
        centroids = [result.get('centroid', (0, 0)) for result in framework_results if 'centroid' in result]
        
        if centroids:
            x_coords = [c[0] for c in centroids]
            y_coords = [c[1] for c in centroids]
            
            # Calculate average centroid
            avg_x = np.mean(x_coords)
            avg_y = np.mean(y_coords)
            
            # Add individual points
            fig.add_trace(go.Scatter(
                x=x_coords, y=y_coords,
                mode='markers',
                marker=dict(size=8, color='lightblue', opacity=0.6),
                showlegend=False,
                hovertemplate="Individual Text<br>Position: (%{x:.3f}, %{y:.3f})<extra></extra>"
            ), row=row, col=col)
            
            # Add average centroid
            fig.add_trace(go.Scatter(
                x=[avg_x], y=[avg_y],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                showlegend=False,
                hovertemplate=f"Average Centroid<br>Position: ({avg_x:.3f}, {avg_y:.3f})<extra></extra>"
            ), row=row, col=col)


def create_showcase_visualization(
    framework_name: str,
    anchors: Dict,
    sample_texts: List[Dict],
    framework_config: Optional[Dict] = None
) -> go.Figure:
    """
    Create a comprehensive showcase visualization for a framework.
    
    This function demonstrates multiple DCS capabilities in a single view:
    - Theoretical weighting mapping
    - Individual text positioning
    - Statistical analysis
    - Framework-specific features
    """
    viz = AdvancedDCSVisualizer()
    
    # Create base plot with weighting if configuration available
    if framework_config:
        fig = viz.plot_with_weighting_heatmap(
            anchors=anchors,
            framework_config=framework_config,
            title=f"{framework_name}: Comprehensive Analysis",
            weighting_opacity=0.4
        )
    else:
        fig = viz.create_base_figure(f"{framework_name}: Comprehensive Analysis")
        viz._add_enhanced_anchors(fig, anchors)
    
    # Add sample text analysis
    if sample_texts:
        centroids = []
        for text_data in sample_texts:
            if 'signature_scores' in text_data:
                centroid = viz.calculate_centroid(anchors, text_data['signature_scores'])
                centroids.append(centroid)
        
        if centroids:
            x_coords = [c[0] for c in centroids]
            y_coords = [c[1] for c in centroids]
            
            # Add individual text positions
            fig.add_trace(go.Scatter(
                x=x_coords, y=y_coords,
                mode='markers',
                marker=dict(size=10, color='lightblue', opacity=0.7),
                name='Sample Texts',
                hovertemplate="Text Position<br>(%{x:.3f}, %{y:.3f})<extra></extra>"
            ))
            
            # Add corpus centroid
            avg_x = np.mean(x_coords)
            avg_y = np.mean(y_coords)
            
            fig.add_trace(go.Scatter(
                x=[avg_x], y=[avg_y],
                mode='markers+text',
                marker=dict(size=20, color='orange', symbol='star'),
                text=['Corpus Centroid'],
                textposition='bottom center',
                name='Corpus Centroid',
                hovertemplate=f"Corpus Centroid<br>Position: ({avg_x:.3f}, {avg_y:.3f})<extra></extra>"
            ))
    
    return fig 