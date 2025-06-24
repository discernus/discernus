#!/usr/bin/env python3
"""
Discernus Visualization Engine
=============================

Comprehensive visualization system combining the best of both coordinate system 
and statistical visualization capabilities with production integration.

ALL VISUALIZATIONS USE PLOTLY (no matplotlib/seaborn)
Updated terminology: anchors, axes, centroids, DCS
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import logging
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import json
from datetime import datetime

# Import updated systems
import sys
sys.path.append('/Volumes/dev/discernus/src')
sys.path.append('/Volumes/dev/discernus/experimental/prototypes')

from discernus_themes import get_theme, list_themes, VisualizationTheme

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DiscernusVisualizationEngine:
    """
    Discernus Visualization Engine for DCS (Discernus Coordinate System).
    
    Features:
    - ALL Plotly visualizations (no matplotlib/seaborn)
    - Cartographic terminology (anchors, axes, centroids)
    - Statistical analysis plots
    - Coordinate system visualizations  
    - Framework-aware data preparation
    - Production experiment integration
    - Theme-aware styling
    - Multi-format export
    """
    
    def __init__(self, output_dir: str = "experimental/prototypes/iteration_output", theme: str = 'academic'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_files = {}
        
        # Initialize theme system
        self.theme_name = theme
        self.theme = get_theme(theme)
        
        logger.info(f"✅ Initialized Discernus Visualization Engine")
        logger.info(f"📊 Theme: {self.theme_name}")
        logger.info(f"📁 Output directory: {self.output_dir}")
    
    def generate_comprehensive_visualizations(self, structured_results: Dict, statistical_results: Dict, 
                                            reliability_results: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive visualizations for experiment results.
        
        Args:
            structured_results: Structured experiment data
            statistical_results: Statistical hypothesis testing results  
            reliability_results: Interrater reliability analysis results
            
        Returns:
            Dictionary containing paths to generated visualization files
        """
        logger.info("🎨 Starting comprehensive visualization generation...")
        
        df = structured_results.get('structured_data')
        if df is None or df.empty:
            logger.error("No structured data available for visualization")
            return {'error': 'No data available'}
        
        # Extract framework information
        frameworks_used = df['framework'].unique() if 'framework' in df.columns else ['unknown']
        primary_framework = frameworks_used[0] if len(frameworks_used) > 0 else 'unknown'
        
        # Get anchor columns (updated terminology)
        anchor_columns = [col for col in df.columns if col.startswith('well_')]  # Legacy column naming
        
        logger.info(f"📊 Generating visualizations for {primary_framework} framework")
        logger.info(f"🎯 Found {len(anchor_columns)} anchor score columns")
        
        # Generate ALL visualization types using Plotly
        viz_results = {
            'coordinate_plots': self.create_coordinate_system_plots(df, anchor_columns, primary_framework),
            'statistical_plots': self.create_statistical_analysis_plots(df, anchor_columns, primary_framework),
            'correlation_plots': self.create_correlation_plots(df, anchor_columns, primary_framework),
            'hypothesis_plots': self.create_hypothesis_plots(statistical_results),
            'reliability_plots': self.create_reliability_plots(reliability_results),
            'distribution_plots': self.create_distribution_plots(df, anchor_columns, primary_framework),
            'comparative_dashboard': self.create_comparative_dashboard(df, anchor_columns, statistical_results, primary_framework),
            'generated_files': self.generated_files
        }
        
        logger.info(f"✅ Generated {len(self.generated_files)} visualization files using Plotly")
        return viz_results
    
    def create_coordinate_system_plots(self, df: pd.DataFrame, anchor_columns: List[str], 
                                     framework_name: str) -> Dict[str, str]:
        """Create coordinate system plots using Plotly."""
        logger.info("🗺️ Creating coordinate system plots...")
        
        plots = {}
        
        # Extract anchor configurations (this would need framework manager integration)
        anchors = self._extract_anchor_configuration(df, anchor_columns, framework_name)
        
        if not anchors:
            logger.warning("No anchor configuration available")
            return plots
        
        # Create individual coordinate plots for each analysis
        analyses = []
        for i, row in df.iterrows():
            # Extract anchor scores from row
            anchor_scores = {}
            for anchor_name in anchors.keys():
                anchor_col = f"well_{anchor_name.lower().replace(' ', '_').replace('-', '_')}"
                if anchor_col in df.columns:
                    anchor_scores[anchor_name] = row[anchor_col]
            
            if anchor_scores:
                centroid = self.calculate_centroid(anchors, anchor_scores)
                analyses.append({
                    'title': row.get('text_id', f'Analysis {i}'),
                    'anchors': anchors,
                    'scores': anchor_scores,
                    'centroid': centroid,
                    'metadata': {
                        'framework': framework_name,
                        'model': row.get('model', 'unknown'),
                        'cost': row.get('api_cost', 0.0)
                    }
                })
        
        if analyses:
            # Single coordinate system plot
            single_fig = self._create_single_coordinate_plot(
                analyses[0], 
                title=f'{framework_name.upper()} Framework - Coordinate System'
            )
            
            single_file = self.output_dir / 'coordinate_system_single.html'
            single_fig.write_html(str(single_file))
            plots['single_coordinate'] = str(single_file)
            self.generated_files['single_coordinate'] = str(single_file)
            
            # Comparative coordinate plot if multiple analyses
            if len(analyses) > 1:
                comp_fig = self._create_comparative_coordinate_plot(
                    analyses[:6],  # Limit for clarity
                    title=f'{framework_name.upper()} Framework - Comparative Analysis'
                )
                
                comp_file = self.output_dir / 'coordinate_system_comparative.html'
                comp_fig.write_html(str(comp_file))
                plots['comparative_coordinate'] = str(comp_file)
                self.generated_files['comparative_coordinate'] = str(comp_file)
        
        return plots
    
    def _create_single_coordinate_plot(self, analysis: Dict, title: str) -> go.Figure:
        """Create a single coordinate system plot using Plotly."""
        fig = go.Figure()
        
        anchors = analysis['anchors']
        scores = analysis['scores']
        centroid = analysis['centroid']
        
        # Add coordinate system boundary (unit circle)
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(circle_angles)
        circle_y = np.sin(circle_angles)
        
        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line=dict(color=self.theme.style['boundary_color'], width=self.theme.style['boundary_width']),
            name='Coordinate Boundary',
            showlegend=False
        ))
        
        # Add anchors
        for anchor_name, anchor_data in anchors.items():
            angle_rad = np.radians(anchor_data['angle'])
            x = np.cos(angle_rad)
            y = np.sin(angle_rad)
            
            # Color by anchor type
            color = self.theme.anchor_colors.get(anchor_data.get('type', 'default'), 
                                               self.theme.anchor_colors['default'])
            
            # Scale marker size by score
            score = scores.get(anchor_name, 0.0)
            marker_size = self.theme.style['anchor_marker_size'] + (score * 10)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[anchor_name],
                textposition='middle center',
                marker=dict(
                    size=marker_size,
                    color=color,
                    opacity=0.6 + (score * 0.4),
                    line=dict(width=2, color='white')
                ),
                name=anchor_name,
                showlegend=False,
                hovertemplate=f"<b>{anchor_name}</b><br>Score: {score:.3f}<extra></extra>"
            ))
        
        # Add centroid
        fig.add_trace(go.Scatter(
            x=[centroid[0]], y=[centroid[1]],
            mode='markers',
            marker=dict(
                size=self.theme.style['centroid_marker_size'],
                color='orange',
                symbol='star',
                line=dict(width=2, color='white')
            ),
            name='Centroid',
            showlegend=True,
            hovertemplate=f"<b>Centroid</b><br>Position: ({centroid[0]:.3f}, {centroid[1]:.3f})<extra></extra>"
        ))
        
        # Apply theme styling
        fig.update_layout(
            title=dict(text=title, font=dict(size=self.theme.style['title_size'])),
            xaxis=dict(
                range=[-1.2, 1.2], 
                scaleanchor="y", 
                scaleratio=1,
                showgrid=True,
                gridcolor=self.theme.style['grid_color'],
                gridwidth=self.theme.style['grid_width'],
                zeroline=True,
                zerolinecolor=self.theme.style['grid_color']
            ),
            yaxis=dict(
                range=[-1.2, 1.2],
                showgrid=True,
                gridcolor=self.theme.style['grid_color'],
                gridwidth=self.theme.style['grid_width'],
                zeroline=True,
                zerolinecolor=self.theme.style['grid_color']
            ),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            font=dict(family=self.theme.style['font_family']),
            width=800, height=800
        )
        
        return fig
    
    def _create_comparative_coordinate_plot(self, analyses: List[Dict], title: str) -> go.Figure:
        """Create comparative coordinate plot with multiple centroids."""
        fig = go.Figure()
        
        # Use first analysis for anchor positions
        anchors = analyses[0]['anchors']
        
        # Add coordinate system boundary
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(circle_angles)
        circle_y = np.sin(circle_angles)
        
        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line=dict(color=self.theme.style['boundary_color'], width=self.theme.style['boundary_width']),
            name='Coordinate Boundary',
            showlegend=False
        ))
        
        # Add anchors (once)
        for anchor_name, anchor_data in anchors.items():
            angle_rad = np.radians(anchor_data['angle'])
            x = np.cos(angle_rad)
            y = np.sin(angle_rad)
            
            color = self.theme.anchor_colors.get(anchor_data.get('type', 'default'), 
                                               self.theme.anchor_colors['default'])
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[anchor_name],
                textposition='middle center',
                marker=dict(
                    size=self.theme.style['anchor_marker_size'],
                    color=color,
                    opacity=0.7,
                    line=dict(width=2, color='white')
                ),
                name=anchor_name,
                showlegend=False
            ))
        
        # Add centroids for each analysis
        colors = px.colors.qualitative.Set1
        for i, analysis in enumerate(analyses):
            centroid = analysis['centroid']
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=[centroid[0]], y=[centroid[1]],
                mode='markers',
                marker=dict(
                    size=self.theme.style['centroid_marker_size'],
                    color=color,
                    symbol='star',
                    line=dict(width=2, color='white')
                ),
                name=analysis['title'],
                showlegend=True,
                hovertemplate=f"<b>{analysis['title']}</b><br>Centroid: ({centroid[0]:.3f}, {centroid[1]:.3f})<extra></extra>"
            ))
        
        # Apply theme styling
        fig.update_layout(
            title=dict(text=title, font=dict(size=self.theme.style['title_size'])),
            xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2]),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            font=dict(family=self.theme.style['font_family']),
            width=900, height=800
        )
        
        return fig
    
    def calculate_centroid(self, anchors: Dict[str, Dict], scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate centroid position from anchor scores."""
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
                x = np.cos(angle_rad)
                y = np.sin(angle_rad)
                
                # Weight the contribution
                weighted_score = score * weight
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # Apply adaptive scaling
            scaling_factor = 0.8
            return (centroid_x * scaling_factor, centroid_y * scaling_factor)
        
        return (0.0, 0.0)
    
    def _extract_anchor_configuration(self, df: pd.DataFrame, anchor_columns: List[str], 
                                    framework_name: str) -> Dict[str, Dict]:
        """Extract anchor configuration (would integrate with framework manager)."""
        # Placeholder implementation - in production this would load from framework manager
        anchors = {}
        
        # Extract anchor names from column names
        for col in anchor_columns:
            anchor_name = col.replace('well_', '').replace('_', ' ').title()
            # Assign default angles in a circle
            angle = (len(anchors) * 360 / len(anchor_columns)) % 360
            anchors[anchor_name] = {
                'angle': angle,
                'type': 'integrative' if 'hope' in anchor_name.lower() or 'justice' in anchor_name.lower() else 'disintegrative',
                'weight': 1.0
            }
        
        return anchors
    
    def create_correlation_plots(self, df: pd.DataFrame, anchor_columns: List[str], 
                               framework_name: str) -> Dict[str, str]:
        """Create correlation plots using Plotly."""
        logger.info("🔗 Creating correlation plots with Plotly...")
        
        plots = {}
        
        if len(anchor_columns) < 2:
            return plots
        
        # Calculate correlation matrix
        anchor_data = df[anchor_columns].dropna()
        if anchor_data.empty:
            return plots
        
        correlation_matrix = anchor_data.corr()
        
        # Clean up labels
        labels = [col.replace('well_', '').replace('_', ' ').title() for col in anchor_columns]
        
        # Create Plotly heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=labels,
            y=labels,
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title="Correlation"),
            hoverongaps=False,
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        # Add correlation values as text
        for i, row in enumerate(correlation_matrix.values):
            for j, value in enumerate(row):
                if i != j:  # Don't show diagonal values
                    fig.add_annotation(
                        x=j, y=i,
                        text=f"{value:.2f}",
                        showarrow=False,
                        font=dict(color="white" if abs(value) > 0.5 else "black")
                    )
        
        fig.update_layout(
            title=f'{framework_name.upper()} Framework - Anchor Score Correlations',
            font=dict(family=self.theme.style['font_family']),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            width=800, height=700
        )
        
        corr_file = self.output_dir / 'correlation_matrix.html'
        fig.write_html(str(corr_file))
        plots['correlation_matrix'] = str(corr_file)
        self.generated_files['correlation_matrix'] = str(corr_file)
        
        return plots
    
    def create_statistical_analysis_plots(self, df: pd.DataFrame, anchor_columns: List[str], 
                                        framework_name: str) -> Dict[str, str]:
        """Create statistical analysis plots using Plotly."""
        logger.info("📊 Creating statistical analysis plots with Plotly...")
        
        plots = {}
        
        if not anchor_columns:
            return plots
        
        # Clean up labels
        labels = [col.replace('well_', '').replace('_', ' ').title() for col in anchor_columns]
        
        # Create descriptive statistics plot
        anchor_data = df[anchor_columns].dropna()
        if not anchor_data.empty:
            means = [anchor_data[col].mean() for col in anchor_columns]
            stds = [anchor_data[col].std() for col in anchor_columns]
            
            fig = go.Figure()
            
            # Add bar chart with error bars
            fig.add_trace(go.Bar(
                x=labels,
                y=means,
                error_y=dict(type='data', array=stds, visible=True),
                marker_color=px.colors.qualitative.Set1[0],
                opacity=0.7,
                hovertemplate='<b>%{x}</b><br>Mean: %{y:.3f}<br>Std: %{customdata:.3f}<extra></extra>',
                customdata=stds
            ))
            
            fig.update_layout(
                title=f'{framework_name.upper()} Framework - Anchor Score Statistics',
                xaxis_title='Anchors',
                yaxis_title='Mean Score',
                font=dict(family=self.theme.style['font_family']),
                plot_bgcolor=self.theme.style['background_color'],
                paper_bgcolor=self.theme.style['background_color'],
                xaxis=dict(tickangle=45),
                width=900, height=600
            )
            
            stats_file = self.output_dir / 'statistical_analysis.html'
            fig.write_html(str(stats_file))
            plots['statistical_analysis'] = str(stats_file)
            self.generated_files['statistical_analysis'] = str(stats_file)
        
        return plots
    
    def create_hypothesis_plots(self, statistical_results: Dict) -> Dict[str, str]:
        """Create hypothesis testing plots using Plotly."""
        logger.info("🎯 Creating hypothesis testing plots with Plotly...")
        
        plots = {}
        
        if 'hypothesis_testing' not in statistical_results:
            return plots
        
        hypothesis_data = statistical_results['hypothesis_testing']
        
        # Extract hypothesis information
        hypothesis_names = []
        statuses = []
        
        for h_name, h_results in hypothesis_data.items():
            if isinstance(h_results, dict):
                hypothesis_names.append(h_name.replace('_', ' ').title())
                status = h_results.get('status', 'unknown')
                statuses.append(status)
        
        if hypothesis_names:
            # Create status color mapping
            status_colors = {
                'supported': '#2E7D32',
                'insufficient_data': '#FF9800',
                'not_supported': '#D32F2F',
                'unknown': '#757575'
            }
            
            colors = [status_colors.get(status, status_colors['unknown']) for status in statuses]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=hypothesis_names,
                    y=[1] * len(hypothesis_names),
                    marker_color=colors,
                    opacity=0.8,
                    text=[status.replace('_', ' ').title() for status in statuses],
                    textposition='inside',
                    textfont=dict(color='white', size=12),
                    hovertemplate='<b>%{x}</b><br>Status: %{text}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title='Hypothesis Testing Results',
                yaxis=dict(visible=False),
                font=dict(family=self.theme.style['font_family']),
                plot_bgcolor=self.theme.style['background_color'],
                paper_bgcolor=self.theme.style['background_color'],
                xaxis=dict(tickangle=45),
                width=800, height=500
            )
            
            hyp_file = self.output_dir / 'hypothesis_testing.html'
            fig.write_html(str(hyp_file))
            plots['hypothesis_testing'] = str(hyp_file)
            self.generated_files['hypothesis_testing'] = str(hyp_file)
        
        return plots
    
    def create_reliability_plots(self, reliability_results: Dict) -> Dict[str, str]:
        """Create reliability analysis plots using Plotly."""
        logger.info("🔍 Creating reliability plots with Plotly...")
        
        plots = {}
        
        # Create a simple reliability summary visualization
        fig = go.Figure()
        
        # Add a text annotation for reliability summary
        reliability_text = "Reliability Analysis Complete<br><br>"
        if 'reliability_metrics' in reliability_results:
            metrics = reliability_results['reliability_metrics']
            if 'model_consistency' in metrics:
                consistency = metrics['model_consistency']
                reliability_text += f"Models: {consistency.get('total_models', 'Unknown')}<br>"
                reliability_text += f"Type: {consistency.get('reliability_note', 'Unknown')}<br>"
        
        fig.add_annotation(
            x=0.5, y=0.5,
            text=reliability_text,
            showarrow=False,
            font=dict(size=16, family=self.theme.style['font_family']),
            bgcolor=self.theme.style['annotation_bg'],
            bordercolor=self.theme.style['annotation_border'],
            borderwidth=2,
            borderpad=10,
            xref='paper', yref='paper'
        )
        
        fig.update_layout(
            title='Reliability Analysis Summary',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            font=dict(family=self.theme.style['font_family']),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            width=600, height=400
        )
        
        rel_file = self.output_dir / 'reliability_analysis.html'
        fig.write_html(str(rel_file))
        plots['reliability_analysis'] = str(rel_file)
        self.generated_files['reliability_analysis'] = str(rel_file)
        
        return plots
    
    def create_distribution_plots(self, df: pd.DataFrame, anchor_columns: List[str], 
                                framework_name: str) -> Dict[str, str]:
        """Create distribution plots using Plotly."""
        logger.info("📈 Creating distribution plots with Plotly...")
        
        plots = {}
        
        if not anchor_columns:
            return plots
        
        # Create distribution analysis
        anchor_data = df[anchor_columns].dropna()
        if anchor_data.empty:
            return plots
        
        # Create violin plots for score distributions
        fig = go.Figure()
        
        labels = [col.replace('well_', '').replace('_', ' ').title() for col in anchor_columns]
        colors = px.colors.qualitative.Set1
        
        for i, (col, label) in enumerate(zip(anchor_columns, labels)):
            fig.add_trace(go.Violin(
                y=anchor_data[col],
                name=label,
                box_visible=True,
                meanline_visible=True,
                fillcolor=colors[i % len(colors)],
                opacity=0.6,
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title=f'{framework_name.upper()} Framework - Score Distributions',
            yaxis_title='Anchor Scores',
            font=dict(family=self.theme.style['font_family']),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            xaxis=dict(tickangle=45),
            width=1000, height=600
        )
        
        dist_file = self.output_dir / 'score_distributions.html'
        fig.write_html(str(dist_file))
        plots['score_distributions'] = str(dist_file)
        self.generated_files['score_distributions'] = str(dist_file)
        
        return plots
    
    def create_comparative_dashboard(self, df: pd.DataFrame, anchor_columns: List[str], 
                                   statistical_results: Dict, framework_name: str) -> Dict[str, str]:
        """Create comprehensive dashboard using Plotly subplots."""
        logger.info("🎮 Creating comprehensive dashboard with Plotly...")
        
        plots = {}
        
        if not anchor_columns:
            return plots
        
        # Create subplot dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Coordinate System', 'Score Statistics', 'Score Distributions', 'Correlations'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "violin"}, {"type": "heatmap"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Coordinate system (simplified)
        anchors = self._extract_anchor_configuration(df, anchor_columns, framework_name)
        if anchors and not df.empty:
            # Add boundary circle
            circle_angles = np.linspace(0, 2*np.pi, 100)
            circle_x = np.cos(circle_angles)
            circle_y = np.sin(circle_angles)
            
            fig.add_trace(go.Scatter(
                x=circle_x, y=circle_y,
                mode='lines',
                line=dict(color='gray', dash='dash'),
                name='Boundary',
                showlegend=False
            ), row=1, col=1)
            
            # Add anchors
            for anchor_name, anchor_data in anchors.items():
                angle_rad = np.radians(anchor_data['angle'])
                x = np.cos(angle_rad)
                y = np.sin(angle_rad)
                
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers',
                    marker=dict(size=8, color='blue'),
                    name=anchor_name,
                    showlegend=False
                ), row=1, col=1)
        
        # 2. Score statistics
        anchor_data = df[anchor_columns].dropna()
        if not anchor_data.empty:
            means = [anchor_data[col].mean() for col in anchor_columns]
            labels = [col.replace('well_', '').replace('_', ' ').title() for col in anchor_columns]
            
            fig.add_trace(go.Bar(
                x=labels,
                y=means,
                name='Mean Scores',
                showlegend=False
            ), row=1, col=2)
        
        # 3. Score distributions (simplified)
        if not anchor_data.empty and len(anchor_columns) > 0:
            fig.add_trace(go.Violin(
                y=anchor_data[anchor_columns[0]],
                name='Distribution',
                showlegend=False
            ), row=2, col=1)
        
        # 4. Correlation heatmap (simplified)
        if not anchor_data.empty and len(anchor_columns) > 1:
            correlation_matrix = anchor_data.corr()
            
            fig.add_trace(go.Heatmap(
                z=correlation_matrix.values,
                x=labels,
                y=labels,
                colorscale='RdBu',
                zmid=0,
                showscale=False
            ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title=f'{framework_name.upper()} Framework - Comprehensive Dashboard',
            font=dict(family=self.theme.style['font_family']),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            height=800,
            width=1200
        )
        
        # Update subplot axes
        fig.update_xaxes(scaleanchor="y1", scaleratio=1, row=1, col=1)
        fig.update_yaxes(scaleanchor="x1", row=1, col=1)
        
        dashboard_file = self.output_dir / 'comprehensive_dashboard.html'
        fig.write_html(str(dashboard_file))
        plots['comprehensive_dashboard'] = str(dashboard_file)
        self.generated_files['comprehensive_dashboard'] = str(dashboard_file)
        
        return plots
    
    def export_all_visualizations(self, formats: List[str] = ['html', 'png']) -> Dict[str, Dict[str, str]]:
        """Export all generated visualizations in multiple formats."""
        logger.info(f"📤 Exporting visualizations in formats: {formats}")
        
        export_results = {}
        
        for viz_name, viz_path in self.generated_files.items():
            if viz_path.endswith('.html'):
                # Load the HTML file and export to other formats
                try:
                    import plotly.io as pio
                    fig = pio.read_html(viz_path)
                    
                    viz_exports = {}
                    viz_exports['html'] = viz_path
                    
                    for fmt in formats:
                        if fmt != 'html':
                            export_path = viz_path.replace('.html', f'.{fmt}')
                            if fmt == 'png':
                                fig.write_image(export_path, format='png', scale=2)
                            elif fmt == 'svg':
                                fig.write_image(export_path, format='svg')
                            elif fmt == 'pdf':
                                fig.write_image(export_path, format='pdf')
                            
                            viz_exports[fmt] = export_path
                    
                    export_results[viz_name] = viz_exports
                    
                except Exception as e:
                    logger.warning(f"Failed to export {viz_name}: {e}")
        
        return export_results
    
    def save_visualization_index(self) -> str:
        """Save index of generated visualizations."""
        index_data = {
            'generation_timestamp': datetime.now().isoformat(),
            'visualization_engine': 'DiscernusVisualizationEngine (All Plotly)',
            'theme': self.theme_name,
            'files_generated': self.generated_files,
            'total_files': len(self.generated_files),
            'cartographic_terminology': True,
            'plotly_only': True
        }
        
        index_file = self.output_dir / 'visualization_index.json'
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        logger.info(f"📋 Visualization index saved: {index_file}")
        return str(index_file)


# Convenience functions
def create_visualization_engine(theme: str = 'academic', 
                              output_dir: str = "experimental/prototypes/iteration_output") -> DiscernusVisualizationEngine:
    """Create a Discernus Visualization Engine."""
    return DiscernusVisualizationEngine(output_dir=output_dir, theme=theme)


if __name__ == '__main__':
    print("🗺️ Discernus Visualization Engine")
    print("=" * 50)
    print("Comprehensive visualization system with ALL Plotly visualizations and cartographic terminology")
    
    # Demo initialization
    visualizer = create_visualization_engine(theme='academic')
    print(f"✅ Initialized with {visualizer.theme_name} theme")
    print("🎯 Ready for comprehensive visualization generation!") 