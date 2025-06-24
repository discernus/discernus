import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
import csv
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path
from scipy import stats

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

    def plot_with_chart_modes(self, wells: Dict, detailed_results: Optional[Dict] = None,
                              chart_output_mode: str = "enhanced_only", layout: str = "side_by_side",
                              title: Optional[str] = None, output_html: Optional[str] = None, 
                              output_png: Optional[str] = None, show: bool = True) -> go.Figure:
        """
        Create visualization with support for different chart output modes for academic transparency.
        
        Args:
            wells: dict of {well_name: {'angle': deg, 'type': str, 'weight': float, ...}}
            detailed_results: dict from calculate_narrative_position(return_detailed_results=True)
            chart_output_mode: "raw_only", "enhanced_only", "both_comparison"
            layout: "side_by_side", "overlay", "separate_figures" (for both_comparison mode)
            title: str (optional)
            output_html: path to save interactive HTML (optional)
            output_png: path to save static PNG (optional)
            show: whether to display the figure
        """
        if not detailed_results:
            # Fall back to simple mode without algorithm information
            return self.plot(wells, narrative_scores=None, title=title, 
                           output_html=output_html, output_png=output_png, show=show)
        
        raw_scores = detailed_results.get('raw_scores', {})
        enhanced_scores = detailed_results.get('enhanced_scores', {})
        raw_coords = detailed_results.get('raw_coordinates', (0.0, 0.0))
        enhanced_coords = detailed_results.get('enhanced_coordinates', (0.0, 0.0))
        algorithm_config = detailed_results.get('algorithm_config', {})
        amplification_applied = detailed_results.get('amplification_applied', False)
        
        if chart_output_mode == "raw_only":
            return self._plot_single(wells, raw_scores, raw_coords, 
                                   title=f"{title or 'Analysis'} - Raw Scores", 
                                   subtitle="Raw LLM scores without algorithmic enhancement",
                                   output_html=output_html, output_png=output_png, show=show)
        
        elif chart_output_mode == "enhanced_only":
            subtitle = f"Enhanced scores (amplification {'applied' if amplification_applied else 'not applied'})"
            return self._plot_single(wells, enhanced_scores, enhanced_coords,
                                   title=f"{title or 'Analysis'} - Enhanced Scores",
                                   subtitle=subtitle,
                                   output_html=output_html, output_png=output_png, show=show)
        
        elif chart_output_mode == "both_comparison":
            if layout == "side_by_side":
                return self._plot_side_by_side_comparison(wells, raw_scores, enhanced_scores, 
                                                        raw_coords, enhanced_coords, algorithm_config,
                                                        title=title, output_html=output_html, 
                                                        output_png=output_png, show=show)
            elif layout == "overlay":
                return self._plot_overlay_comparison(wells, raw_scores, enhanced_scores,
                                                   raw_coords, enhanced_coords, algorithm_config,
                                                   title=title, output_html=output_html,
                                                   output_png=output_png, show=show)
            else:
                # Default to side_by_side for unsupported layouts
                return self._plot_side_by_side_comparison(wells, raw_scores, enhanced_scores,
                                                        raw_coords, enhanced_coords, algorithm_config,
                                                        title=title, output_html=output_html,
                                                        output_png=output_png, show=show)
        
        else:
            # Default to enhanced_only for unknown modes
            return self.plot_with_chart_modes(wells, detailed_results, "enhanced_only", layout,
                                            title, output_html, output_png, show)

    def _plot_single(self, wells: Dict, scores: Dict, coordinates: Tuple[float, float],
                     title: str, subtitle: str = "", output_html: Optional[str] = None,
                     output_png: Optional[str] = None, show: bool = True) -> go.Figure:
        """Create a single chart with specified scores and coordinates."""
        fig = self.create_base_figure(title)
        
        # Add subtitle if provided
        if subtitle:
            fig.update_layout(
                title=dict(
                    text=f"{title}<br><sub>{subtitle}</sub>",
                    font=dict(size=self.style['title_size'], family=self.style['font_family'])
                )
            )
        
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
            
            # Include score in label if available
            score_text = f" ({scores.get(well_name, 0.0):.2f})" if well_name in scores else ""
            well_xs.append(x)
            well_ys.append(y)
            well_labels.append(f"{well_name}{score_text}")
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
        
        # Plot narrative position
        narrative_x, narrative_y = coordinates
        fig.add_trace(go.Scatter(
            x=[narrative_x], y=[narrative_y],
            mode='markers+text',
            marker=dict(
                size=self.style['narrative_marker_size'],
                color='orange',
                line=dict(width=3, color='black')
            ),
            text=['Narrative'],
            textposition='bottom right',
            name='Narrative Position',
            hovertemplate='<b>Narrative Position</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
        ))
        
        # Line from center to narrative
        fig.add_trace(go.Scatter(
            x=[0, narrative_x], y=[0, narrative_y],
            mode='lines',
            line=dict(color='orange', width=2, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add metrics
        distance = np.sqrt(narrative_x**2 + narrative_y**2)
        angle_rad = np.arctan2(narrative_y, narrative_x)
        angle_deg = np.degrees(angle_rad) % 360
        
        metrics_text = f'Distance: {distance:.3f}<br>Angle: {angle_deg:.1f}°<br>Position: ({narrative_x:+.3f}, {narrative_y:+.3f})'
        
        fig.add_annotation(
            x=0.05, y=-0.95,
            text=metrics_text,
            showarrow=False,
            font=dict(size=10),
            bgcolor='rgba(173, 216, 230, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.3)',
            borderwidth=1, borderpad=4,
            xanchor='left', yanchor='bottom'
        )
        
        # Save and show
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)
        if show:
            fig.show()
            
        return fig

    def _plot_side_by_side_comparison(self, wells: Dict, raw_scores: Dict, enhanced_scores: Dict,
                                     raw_coords: Tuple[float, float], enhanced_coords: Tuple[float, float],
                                     algorithm_config: Dict, title: Optional[str] = None,
                                     output_html: Optional[str] = None, output_png: Optional[str] = None,
                                     show: bool = True) -> go.Figure:
        """Create side-by-side comparison of raw and enhanced scores."""
        
        # Create subplot figure
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Raw LLM Scores', 'Algorithmically Enhanced Scores'],
            specs=[[{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Create individual plots
        raw_fig = self._plot_single(wells, raw_scores, raw_coords, "Raw Scores", show=False)
        enhanced_fig = self._plot_single(wells, enhanced_scores, enhanced_coords, "Enhanced Scores", show=False)
        
        # Add traces to subplots
        for trace in raw_fig.data:
            fig.add_trace(trace, row=1, col=1)
        for trace in enhanced_fig.data:
            fig.add_trace(trace, row=1, col=2)
        
        # Update layout
        dom_config = algorithm_config.get('dominance_amplification', {})
        scale_config = algorithm_config.get('adaptive_scaling', {})
        
        algorithm_info = f"Algorithm: Dominance threshold {dom_config.get('threshold', 'N/A')}, multiplier {dom_config.get('multiplier', 'N/A')}"
        
        fig.update_layout(
            title=dict(
                text=f"{title or 'Raw vs Enhanced Comparison'}<br><sub>{algorithm_info}</sub>",
                font=dict(size=self.style['title_size'], family=self.style['font_family'])
            ),
            height=self.figure_size,
            width=self.figure_size * 2,
            showlegend=False
        )
        
        # Lock aspect ratio for both subplots
        fig.update_xaxes(scaleanchor="y", scaleratio=1, range=[-1.2, 1.2])
        fig.update_yaxes(range=[-1.2, 1.2])
        
        # Save and show
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)
        if show:
            fig.show()
            
        return fig

    def _plot_overlay_comparison(self, wells: Dict, raw_scores: Dict, enhanced_scores: Dict,
                                raw_coords: Tuple[float, float], enhanced_coords: Tuple[float, float],
                                algorithm_config: Dict, title: Optional[str] = None,
                                output_html: Optional[str] = None, output_png: Optional[str] = None,
                                show: bool = True) -> go.Figure:
        """Create overlay comparison of raw and enhanced scores on same chart."""
        
        fig = self.create_base_figure(title)
        
        # Plot wells (only once)
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
            
            # Show both scores in label
            raw_score = raw_scores.get(well_name, 0.0)
            enhanced_score = enhanced_scores.get(well_name, 0.0)
            well_xs.append(x)
            well_ys.append(y)
            well_labels.append(f"{well_name}<br>Raw: {raw_score:.2f}<br>Enhanced: {enhanced_score:.2f}")
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
        
        # Plot both narrative positions
        raw_x, raw_y = raw_coords
        enhanced_x, enhanced_y = enhanced_coords
        
        # Raw position (blue)
        fig.add_trace(go.Scatter(
            x=[raw_x], y=[raw_y],
            mode='markers+text',
            marker=dict(size=24, color='blue', line=dict(width=2, color='darkblue')),
            text=['Raw'],
            textposition='bottom left',
            name='Raw Position',
            hovertemplate='<b>Raw Position</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
        ))
        
        # Enhanced position (orange)
        fig.add_trace(go.Scatter(
            x=[enhanced_x], y=[enhanced_y],
            mode='markers+text',
            marker=dict(size=28, color='orange', line=dict(width=3, color='darkorange')),
            text=['Enhanced'],
            textposition='bottom right',
            name='Enhanced Position',
            hovertemplate='<b>Enhanced Position</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
        ))
        
        # Lines from center
        fig.add_trace(go.Scatter(
            x=[0, raw_x], y=[0, raw_y],
            mode='lines',
            line=dict(color='blue', width=2, dash='dash'),
            showlegend=False, hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, enhanced_x], y=[0, enhanced_y],
            mode='lines',
            line=dict(color='orange', width=2, dash='solid'),
            showlegend=False, hoverinfo='skip'
        ))
        
        # Algorithm info annotation
        dom_config = algorithm_config.get('dominance_amplification', {})
        algo_text = f"Algorithm: threshold={dom_config.get('threshold', 'N/A')}, multiplier={dom_config.get('multiplier', 'N/A')}"
        
        fig.update_layout(
            title=dict(
                text=f"{title or 'Raw vs Enhanced Overlay'}<br><sub>{algo_text}</sub>",
                font=dict(size=self.style['title_size'], family=self.style['font_family'])
            ),
            showlegend=True
        )
        
        # Save and show
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)
        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)
        if show:
            fig.show()
            
        return fig

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

    # =============================================================================
    # ENHANCED ANALYTICS & ACADEMIC OUTPUT FEATURES
    # =============================================================================
    
    def calculate_multi_run_variance(self, multi_run_data: List[Dict]) -> Dict:
        """
        Calculate variance analysis across multiple LLM runs for reliability assessment.
        
        Args:
            multi_run_data: List of run dictionaries, each containing:
                - 'scores': Dict of foundation scores
                - 'coordinates': Tuple of (x, y) coordinates
                - 'metadata': Dict with run information
        
        Returns:
            Dict with comprehensive variance statistics
        """
        if len(multi_run_data) < 2:
            return {"error": "Need at least 2 runs for variance analysis"}
        
        # Extract scores across runs
        all_scores = {}
        all_coordinates = []
        
        for run in multi_run_data:
            scores = run.get('scores', {})
            coords = run.get('coordinates', (0.0, 0.0))
            all_coordinates.append(coords)
            
            for foundation, score in scores.items():
                if foundation not in all_scores:
                    all_scores[foundation] = []
                all_scores[foundation].append(score)
        
        # Calculate foundation-level statistics
        foundation_stats = {}
        for foundation, score_list in all_scores.items():
            if len(score_list) >= 2:
                foundation_stats[foundation] = {
                    'mean': np.mean(score_list),
                    'std': np.std(score_list),
                    'var': np.var(score_list),
                    'min': np.min(score_list),
                    'max': np.max(score_list),
                    'coefficient_of_variation': np.std(score_list) / np.mean(score_list) if np.mean(score_list) > 0 else 0
                }
        
        # Calculate coordinate-level statistics
        x_coords = [coord[0] for coord in all_coordinates]
        y_coords = [coord[1] for coord in all_coordinates]
        distances = [np.sqrt(x**2 + y**2) for x, y in all_coordinates]
        
        coordinate_stats = {
            'x_mean': np.mean(x_coords),
            'x_std': np.std(x_coords),
            'y_mean': np.mean(y_coords),
            'y_std': np.std(y_coords),
            'distance_mean': np.mean(distances),
            'distance_std': np.std(distances),
            'coordinate_variance': np.var(x_coords) + np.var(y_coords)
        }
        
        # Calculate inter-run correlations
        reliability_metrics = {}
        if len(multi_run_data) >= 3:
            # Pearson correlation between consecutive runs
            correlations = []
            for i in range(len(multi_run_data) - 1):
                run1_scores = list(multi_run_data[i]['scores'].values())
                run2_scores = list(multi_run_data[i + 1]['scores'].values())
                if len(run1_scores) == len(run2_scores) and len(run1_scores) > 1:
                    corr, _ = stats.pearsonr(run1_scores, run2_scores)
                    correlations.append(corr)
            
            reliability_metrics = {
                'inter_run_correlation': np.mean(correlations) if correlations else 0,
                'correlation_std': np.std(correlations) if correlations else 0,
                'overall_reliability': 1 - np.mean([stats['coefficient_of_variation'] for stats in foundation_stats.values()]) if foundation_stats else 0
            }
        
        return {
            'foundation_statistics': foundation_stats,
            'coordinate_statistics': coordinate_stats,
            'reliability_metrics': reliability_metrics,
            'run_count': len(multi_run_data),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def generate_academic_report(self, analysis_data: Dict, output_dir: Path, 
                               include_methodology: bool = True) -> Path:
        """
        Generate comprehensive HTML academic report with methodology and results.
        
        Args:
            analysis_data: Complete analysis data including multi-run variance
            output_dir: Directory to save the report
            include_methodology: Whether to include detailed methodology section
        
        Returns:
            Path to generated HTML report
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"discernus_analysis_report_{timestamp}.html"
        
        # Extract key information
        foundation_stats = analysis_data.get('foundation_statistics', {})
        coordinate_stats = analysis_data.get('coordinate_statistics', {})
        reliability_metrics = analysis_data.get('reliability_metrics', {})
        algorithm_config = analysis_data.get('algorithm_config', {})
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discernus Analysis Report</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .metric-card {{ background: #fff; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; }}
                .metric-title {{ font-weight: bold; color: #495057; margin-bottom: 10px; }}
                .metric-value {{ font-size: 1.2em; color: #28a745; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ border: 1px solid #dee2e6; padding: 8px; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
                .methodology {{ background-color: #e9ecef; padding: 20px; border-radius: 8px; }}
                .algorithm-config {{ background-color: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Discernus Narrative Gravity Analysis Report</h1>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Analysis Type:</strong> Multi-Run Variance Analysis with Algorithm Configuration</p>
            </div>
        """
        
        # Algorithm Configuration Section
        if algorithm_config:
            html_content += f"""
            <div class="section">
                <h2>Algorithm Configuration</h2>
                <div class="algorithm-config">
                    <h3>Dominance Amplification</h3>
                    <ul>
                        <li><strong>Enabled:</strong> {algorithm_config.get('dominance_amplification', {}).get('enabled', 'N/A')}</li>
                        <li><strong>Threshold:</strong> {algorithm_config.get('dominance_amplification', {}).get('threshold', 'N/A')}</li>
                        <li><strong>Multiplier:</strong> {algorithm_config.get('dominance_amplification', {}).get('multiplier', 'N/A')}</li>
                    </ul>
                    
                    <h3>Adaptive Scaling</h3>
                    <ul>
                        <li><strong>Base Scaling:</strong> {algorithm_config.get('adaptive_scaling', {}).get('base_scaling', 'N/A')}</li>
                        <li><strong>Max Scaling:</strong> {algorithm_config.get('adaptive_scaling', {}).get('max_scaling', 'N/A')}</li>
                        <li><strong>Variance Factor:</strong> {algorithm_config.get('adaptive_scaling', {}).get('variance_factor', 'N/A')}</li>
                    </ul>
                </div>
            </div>
            """
        
        # Reliability Metrics
        if reliability_metrics:
            html_content += f"""
            <div class="section">
                <h2>Reliability Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Overall Reliability Index</div>
                        <div class="metric-value">{reliability_metrics.get('overall_reliability', 0):.3f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Inter-Run Correlation</div>
                        <div class="metric-value">{reliability_metrics.get('inter_run_correlation', 0):.3f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Run Count</div>
                        <div class="metric-value">{analysis_data.get('run_count', 0)}</div>
                    </div>
                </div>
            </div>
            """
        
        # Foundation Statistics
        if foundation_stats:
            html_content += """
            <div class="section">
                <h2>Foundation-Level Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Foundation</th>
                            <th>Mean Score</th>
                            <th>Std Dev</th>
                            <th>Coefficient of Variation</th>
                            <th>Range</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for foundation, stats in foundation_stats.items():
                html_content += f"""
                        <tr>
                            <td>{foundation}</td>
                            <td>{stats['mean']:.3f}</td>
                            <td>{stats['std']:.3f}</td>
                            <td>{stats['coefficient_of_variation']:.3f}</td>
                            <td>{stats['min']:.3f} - {stats['max']:.3f}</td>
                        </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
            </div>
            """
        
        # Coordinate Statistics
        if coordinate_stats:
            html_content += f"""
            <div class="section">
                <h2>Coordinate Space Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Mean Position</div>
                        <div class="metric-value">({coordinate_stats.get('x_mean', 0):.3f}, {coordinate_stats.get('y_mean', 0):.3f})</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Position Variance</div>
                        <div class="metric-value">{coordinate_stats.get('coordinate_variance', 0):.4f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Mean Distance from Origin</div>
                        <div class="metric-value">{coordinate_stats.get('distance_mean', 0):.3f}</div>
                    </div>
                </div>
            </div>
            """
        
        # Methodology Section
        if include_methodology:
            html_content += """
            <div class="section">
                <h2>Methodology</h2>
                <div class="methodology">
                    <h3>LLM-Prompting-Amplification Pipeline</h3>
                    <p>This analysis employed the Discernus LLM-prompting-amplification pipeline, which integrates:</p>
                    <ol>
                        <li><strong>LLM Semantic Analysis:</strong> Large Language Models identify nuanced patterns and hierarchical relationships in text</li>
                        <li><strong>Algorithmic Enhancement:</strong> Optional mathematical amplification of computationally-identified dominance patterns</li>
                        <li><strong>Coordinate Positioning:</strong> Integration of enhanced assessments into geometric coordinate space</li>
                    </ol>
                    
                    <h3>Multi-Run Reliability Assessment</h3>
                    <p>Reliability is assessed through multiple independent LLM runs, calculating:</p>
                    <ul>
                        <li>Inter-run correlations for consistency measurement</li>
                        <li>Coefficient of variation for score stability</li>
                        <li>Coordinate variance for positional reliability</li>
                    </ul>
                    
                    <h3>Academic Reporting Standards</h3>
                    <p>Algorithm parameters are fully documented for reproducibility. Enhanced scores reflect the integration of LLM assessment and mathematical amplification, not raw LLM outputs.</p>
                </div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_path
    
    def export_csv_data(self, analysis_data: Dict, output_dir: Path) -> Dict[str, Path]:
        """
        Export analysis data to CSV files for statistical analysis in R/SPSS/etc.
        
        Args:
            analysis_data: Complete analysis data
            output_dir: Directory to save CSV files
        
        Returns:
            Dict mapping data type to file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exported_files = {}
        
        # Export foundation statistics
        foundation_stats = analysis_data.get('foundation_statistics', {})
        if foundation_stats:
            foundation_df_data = []
            for foundation, stats in foundation_stats.items():
                foundation_df_data.append({
                    'foundation': foundation,
                    'mean_score': stats['mean'],
                    'std_dev': stats['std'],
                    'variance': stats['var'],
                    'min_score': stats['min'],
                    'max_score': stats['max'],
                    'coefficient_of_variation': stats['coefficient_of_variation']
                })
            
            foundation_df = pd.DataFrame(foundation_df_data)
            foundation_path = output_dir / f"foundation_statistics_{timestamp}.csv"
            foundation_df.to_csv(foundation_path, index=False)
            exported_files['foundation_statistics'] = foundation_path
        
        # Export coordinate statistics
        coordinate_stats = analysis_data.get('coordinate_statistics', {})
        if coordinate_stats:
            coordinate_df = pd.DataFrame([coordinate_stats])
            coordinate_path = output_dir / f"coordinate_statistics_{timestamp}.csv"
            coordinate_df.to_csv(coordinate_path, index=False)
            exported_files['coordinate_statistics'] = coordinate_path
        
        # Export reliability metrics
        reliability_metrics = analysis_data.get('reliability_metrics', {})
        if reliability_metrics:
            reliability_df = pd.DataFrame([reliability_metrics])
            reliability_path = output_dir / f"reliability_metrics_{timestamp}.csv"
            reliability_df.to_csv(reliability_path, index=False)
            exported_files['reliability_metrics'] = reliability_path
        
        # Export algorithm configuration
        algorithm_config = analysis_data.get('algorithm_config', {})
        if algorithm_config:
            # Flatten algorithm config for CSV
            algo_flat = {}
            for section, params in algorithm_config.items():
                if isinstance(params, dict):
                    for param, value in params.items():
                        algo_flat[f"{section}_{param}"] = value
                else:
                    algo_flat[section] = params
            
            algo_df = pd.DataFrame([algo_flat])
            algo_path = output_dir / f"algorithm_configuration_{timestamp}.csv"
            algo_df.to_csv(algo_path, index=False)
            exported_files['algorithm_configuration'] = algo_path
        
        return exported_files
    
    def generate_r_script(self, csv_files: Dict[str, Path], output_dir: Path) -> Path:
        """
        Generate R script for statistical analysis of exported CSV data.
        
        Args:
            csv_files: Dict mapping data type to CSV file path
            output_dir: Directory to save R script
        
        Returns:
            Path to generated R script
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        r_script_path = output_dir / f"discernus_analysis_{timestamp}.R"
        
        r_script = f"""
# Discernus Analysis R Script
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 
# This script provides statistical analysis of Discernus narrative gravity data
# with configurable algorithms and multi-run reliability assessment.

library(tidyverse)
library(corrplot)
library(psych)

# Set working directory to script location
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# Load data files
"""
        
        # Add data loading commands
        for data_type, file_path in csv_files.items():
            var_name = data_type.replace('_', '.')
            r_script += f"{var_name} <- read.csv('{file_path.name}')\n"
        
        r_script += """

# Foundation Analysis
if(exists('foundation.statistics')) {
  cat("\\n=== FOUNDATION ANALYSIS ===\\n")
  
  # Summary statistics
  print(summary(foundation.statistics))
  
  # Reliability assessment
  cat("\\nMean Coefficient of Variation:", mean(foundation.statistics$coefficient_of_variation), "\\n")
  
  # Foundation comparison plot
  ggplot(foundation.statistics, aes(x = foundation, y = mean_score)) +
    geom_col(fill = "steelblue", alpha = 0.7) +
    geom_errorbar(aes(ymin = mean_score - std_dev, ymax = mean_score + std_dev), 
                  width = 0.2) +
    theme_minimal() +
    labs(title = "Foundation Scores with Standard Deviation",
         x = "Foundation", y = "Mean Score") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  ggsave("foundation_analysis.png", width = 10, height = 6, dpi = 300)
}

# Coordinate Analysis  
if(exists('coordinate.statistics')) {
  cat("\\n=== COORDINATE ANALYSIS ===\\n")
  print(coordinate.statistics)
  
  # Calculate position metrics
  if('x_mean' %in% names(coordinate.statistics) && 'y_mean' %in% names(coordinate.statistics)) {
    distance_from_origin <- sqrt(coordinate.statistics$x_mean^2 + coordinate.statistics$y_mean^2)
    angle_degrees <- atan2(coordinate.statistics$y_mean, coordinate.statistics$x_mean) * 180 / pi
    
    cat("\\nPosition Metrics:\\n")
    cat("Distance from Origin:", distance_from_origin, "\\n")
    cat("Angle (degrees):", angle_degrees, "\\n")
  }
}

# Reliability Analysis
if(exists('reliability.metrics')) {
  cat("\\n=== RELIABILITY ANALYSIS ===\\n")
  print(reliability.metrics)
  
  if('overall_reliability' %in% names(reliability.metrics)) {
    cat("\\nReliability Assessment:\\n")
    if(reliability.metrics$overall_reliability > 0.8) {
      cat("HIGH reliability (>0.8)\\n")
    } else if(reliability.metrics$overall_reliability > 0.6) {
      cat("MODERATE reliability (0.6-0.8)\\n") 
    } else {
      cat("LOW reliability (<0.6) - consider more runs\\n")
    }
  }
}

# Algorithm Configuration Analysis
if(exists('algorithm.configuration')) {
  cat("\\n=== ALGORITHM CONFIGURATION ===\\n")
  print(algorithm.configuration)
  
  # Check for standard configurations
  if('dominance_amplification_threshold' %in% names(algorithm.configuration)) {
    threshold <- algorithm.configuration$dominance_amplification_threshold
    multiplier <- algorithm.configuration$dominance_amplification_multiplier
    
    cat("\\nAlgorithm Settings:\\n")
    cat("Dominance Threshold:", threshold, "\\n")
    cat("Amplification Multiplier:", multiplier, "\\n")
    
    if(threshold == 0.7 && multiplier == 1.1) {
      cat("Using STANDARD algorithm configuration\\n")
    } else {
      cat("Using CUSTOM algorithm configuration\\n")
    }
  }
}

cat("\\n=== ANALYSIS COMPLETE ===\\n")
cat("Charts saved as PNG files in working directory\\n")
"""
        
        with open(r_script_path, 'w', encoding='utf-8') as f:
            f.write(r_script)
        
        return r_script_path
    
    def add_provenance_info(self, fig: go.Figure, algorithm_config: Dict, 
                          analysis_metadata: Dict = None) -> go.Figure:
        """
        Add interactive provenance tracking to Plotly charts.
        
        Args:
            fig: Plotly figure to enhance
            algorithm_config: Algorithm configuration used
            analysis_metadata: Additional metadata about the analysis
        
        Returns:
            Enhanced figure with provenance information
        """
        # Create provenance annotation
        provenance_text = "Algorithm Provenance:<br>"
        
        # Dominance amplification info
        dom_config = algorithm_config.get('dominance_amplification', {})
        if dom_config.get('enabled', False):
            provenance_text += f"Dominance: threshold={dom_config.get('threshold', 'N/A')}, multiplier={dom_config.get('multiplier', 'N/A')}<br>"
        else:
            provenance_text += "Dominance: disabled<br>"
        
        # Adaptive scaling info
        scale_config = algorithm_config.get('adaptive_scaling', {})
        if scale_config.get('enabled', False):
            provenance_text += f"Scaling: {scale_config.get('base_scaling', 'N/A')}-{scale_config.get('max_scaling', 'N/A')}<br>"
        else:
            provenance_text += "Scaling: disabled<br>"
        
        # Analysis metadata
        if analysis_metadata:
            provenance_text += f"Run Count: {analysis_metadata.get('run_count', 'N/A')}<br>"
            provenance_text += f"Timestamp: {analysis_metadata.get('timestamp', 'N/A')}<br>"
        
        # Add as annotation in bottom right
        fig.add_annotation(
            x=1.15, y=-0.95,
            text=provenance_text,
            showarrow=False,
            font=dict(size=9, color='gray'),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1,
            borderpad=4,
            xanchor='left',
            yanchor='bottom',
            xref='paper',
            yref='paper'
        )
        
        # Add hover info to title
        current_title = fig.layout.title.text if fig.layout.title else "Analysis"
        fig.update_layout(
            title=dict(
                text=f"{current_title}<br><sub>Interactive provenance: hover for details</sub>",
                font=dict(size=self.style['title_size'], family=self.style['font_family'])
            )
        )
        
        return fig
    
    def create_multi_run_visualization(self, multi_run_data: List[Dict], 
                                     wells: Dict, title: str = "Multi-Run Analysis",
                                     output_dir: Optional[Path] = None) -> Dict:
        """
        Create comprehensive multi-run visualization with variance analysis.
        
        Args:
            multi_run_data: List of run data dictionaries
            wells: Wells configuration
            title: Chart title
            output_dir: Directory to save outputs
        
        Returns:
            Dict containing figure, variance stats, and file paths
        """
        if len(multi_run_data) < 2:
            raise ValueError("Need at least 2 runs for multi-run analysis")
        
        # Calculate variance statistics
        variance_stats = self.calculate_multi_run_variance(multi_run_data)
        
        # Create the main comparison figure
        fig = self.create_base_figure(f"{title} - Multi-Run Comparison")
        
        # Plot all run positions
        colors = px.colors.qualitative.Set1[:len(multi_run_data)]
        
        for i, run_data in enumerate(multi_run_data):
            coords = run_data.get('coordinates', (0.0, 0.0))
            run_label = f"Run {i+1}"
            
            # Add run position
            fig.add_trace(go.Scatter(
                x=[coords[0]], y=[coords[1]],
                mode='markers+text',
                marker=dict(size=20, color=colors[i], line=dict(width=2, color='black')),
                text=[run_label],
                textposition='top center',
                name=run_label,
                hovertemplate=f'<b>{run_label}</b><br>x: %{{x:.3f}}<br>y: %{{y:.3f}}<extra></extra>'
            ))
            
            # Add line from center
            fig.add_trace(go.Scatter(
                x=[0, coords[0]], y=[0, coords[1]],
                mode='lines',
                line=dict(color=colors[i], width=1, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Add mean position
        mean_x = variance_stats['coordinate_statistics']['x_mean']
        mean_y = variance_stats['coordinate_statistics']['y_mean']
        
        fig.add_trace(go.Scatter(
            x=[mean_x], y=[mean_y],
            mode='markers+text',
            marker=dict(size=30, color='red', symbol='star', line=dict(width=3, color='darkred')),
            text=['Mean'],
            textposition='bottom center',
            name='Mean Position',
            hovertemplate='<b>Mean Position</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
        ))
        
        # Add confidence ellipse if we have enough runs
        if len(multi_run_data) >= 3:
            x_coords = [run['coordinates'][0] for run in multi_run_data]
            y_coords = [run['coordinates'][1] for run in multi_run_data]
            
            # Calculate 95% confidence ellipse
            cov_matrix = np.cov(x_coords, y_coords)
            eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
            
            # 95% confidence
            chi_sq_val = 5.991  # Chi-square value for 95% confidence, 2 DOF
            ellipse_radii = np.sqrt(chi_sq_val * eigenvals)
            
            # Generate ellipse points
            angles = np.linspace(0, 2*np.pi, 100)
            ellipse_x = ellipse_radii[0] * np.cos(angles)
            ellipse_y = ellipse_radii[1] * np.sin(angles)
            
            # Rotate ellipse
            rotation_matrix = eigenvecs
            ellipse_points = np.dot(rotation_matrix, np.array([ellipse_x, ellipse_y]))
            
            # Translate to mean position
            ellipse_x_final = ellipse_points[0] + mean_x
            ellipse_y_final = ellipse_points[1] + mean_y
            
            fig.add_trace(go.Scatter(
                x=ellipse_x_final, y=ellipse_y_final,
                mode='lines',
                line=dict(color='red', dash='dash', width=2),
                name='95% Confidence',
                hovertemplate='95% Confidence Ellipse<extra></extra>'
            ))
        
        # Add variance statistics annotation
        reliability_index = variance_stats['reliability_metrics'].get('overall_reliability', 0)
        coord_variance = variance_stats['coordinate_statistics']['coordinate_variance']
        
        stats_text = f'Runs: {len(multi_run_data)}<br>'
        stats_text += f'Reliability: {reliability_index:.3f}<br>'
        stats_text += f'Coord Variance: {coord_variance:.4f}<br>'
        stats_text += f'Mean Distance: {variance_stats["coordinate_statistics"]["distance_mean"]:.3f}'
        
        fig.add_annotation(
            x=1.02, y=0.98,
            text=stats_text,
            showarrow=False,
            font=dict(size=10),
            bgcolor='rgba(144, 238, 144, 0.8)',
            bordercolor='rgba(0, 100, 0, 0.3)',
            borderwidth=1,
            borderpad=4,
            xanchor='left',
            yanchor='top',
            xref='paper',
            yref='paper'
        )
        
        fig.update_layout(showlegend=True)
        
        # Save outputs if directory provided
        saved_files = {}
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save chart
            chart_path = output_dir / f"multi_run_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(chart_path)
            saved_files['chart'] = chart_path
            
            # Save variance statistics
            stats_path = output_dir / f"variance_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(stats_path, 'w') as f:
                json.dump(variance_stats, f, indent=2, default=str)
            saved_files['statistics'] = stats_path
        
        return {
            'figure': fig,
            'variance_statistics': variance_stats,
            'saved_files': saved_files
        }

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