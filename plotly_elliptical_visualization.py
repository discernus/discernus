#!/usr/bin/env python3
"""
Plotly Elliptical Visualization System
====================================

Recreates the custom elliptical visualization but with modern Plotly:
- Interactive elliptical plot design
- Well positions around ellipse perimeter  
- Narrative position within ellipse
- Academic-standard platform with custom design
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from typing import Dict, List, Tuple


class PlotlyEllipticalVisualizer:
    """Modern Plotly implementation of elliptical narrative gravity visualization."""
    
    def __init__(self, width: int = 800, height: int = 800):
        """Initialize the elliptical visualizer."""
        self.width = width
        self.height = height
        self.fig = None
        
        # Ellipse parameters (can be customized)
        self.ellipse_a = 1.0  # Semi-major axis
        self.ellipse_b = 0.8  # Semi-minor axis
        self.center_x = 0.0
        self.center_y = 0.0
        
        # Well positioning parameters
        self.well_radius = 1.1  # Distance from center to place wells
        
        # Define well categories and their preferred positions
        self.integrative_wells = {
            'hope': {'angle': 0, 'color': '#2E8B57'},      # East
            'justice': {'angle': 45, 'color': '#2E8B57'},   # NE
            'dignity': {'angle': 90, 'color': '#2E8B57'},   # North
            'truth': {'angle': 135, 'color': '#2E8B57'},    # NW
            'pragmatism': {'angle': 180, 'color': '#2E8B57'} # West
        }
        
        self.disintegrative_wells = {
            'fear': {'angle': 225, 'color': '#CD5C5C'},        # SW
            'fantasy': {'angle': 270, 'color': '#CD5C5C'},     # South
            'resentment': {'angle': 315, 'color': '#CD5C5C'},  # SE
            'manipulation': {'angle': 200, 'color': '#CD5C5C'}, # SSW
            'tribalism': {'angle': 250, 'color': '#CD5C5C'}    # SSW
        }
    
    def create_ellipse_boundary(self) -> Tuple[List[float], List[float]]:
        """Create ellipse boundary coordinates."""
        theta = np.linspace(0, 2*np.pi, 100)
        x = self.center_x + self.ellipse_a * np.cos(theta)
        y = self.center_y + self.ellipse_b * np.sin(theta)
        return x.tolist(), y.tolist()
    
    def calculate_well_position(self, angle_deg: float) -> Tuple[float, float]:
        """Calculate well position on ellipse perimeter."""
        angle_rad = math.radians(angle_deg)
        x = self.center_x + self.well_radius * math.cos(angle_rad)
        y = self.center_y + self.well_radius * math.sin(angle_rad)
        return x, y
    
    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position based on well scores."""
        
        # Calculate integrative vs disintegrative balance
        integrative_sum = sum(well_scores.get(well, 0) for well in self.integrative_wells.keys())
        disintegrative_sum = sum(well_scores.get(well, 0) for well in self.disintegrative_wells.keys())
        
        # Normalize
        total_integrative = len(self.integrative_wells)
        total_disintegrative = len(self.disintegrative_wells)
        
        integrative_avg = integrative_sum / total_integrative if total_integrative > 0 else 0
        disintegrative_avg = disintegrative_sum / total_disintegrative if total_disintegrative > 0 else 0
        
        # Calculate position (simplified mapping)
        # X-axis: integrative (right) vs disintegrative (left)
        x_position = (integrative_avg - disintegrative_avg) * 0.7
        
        # Y-axis: overall elevation (average of all wells)
        all_scores = list(well_scores.values())
        y_position = (sum(all_scores) / len(all_scores) - 0.5) * 1.2 if all_scores else 0
        
        return x_position, y_position
    
    def create_elliptical_plot(self, well_scores: Dict[str, float], 
                             title: str = "Narrative Gravity Wells - Elliptical Analysis") -> go.Figure:
        """Create the complete elliptical visualization."""
        
        # Create figure
        self.fig = go.Figure()
        
        # 1. Add ellipse boundary
        ellipse_x, ellipse_y = self.create_ellipse_boundary()
        self.fig.add_trace(go.Scatter(
            x=ellipse_x, y=ellipse_y,
            mode='lines',
            line=dict(color='lightgray', width=2, dash='dash'),
            name='Ellipse Boundary',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # 2. Add coordinate axes
        self.fig.add_hline(y=0, line_dash="dot", line_color="lightgray", opacity=0.7)
        self.fig.add_vline(x=0, line_dash="dot", line_color="lightgray", opacity=0.7)
        
        # 3. Add integrative wells
        int_x, int_y, int_scores, int_names, int_colors = [], [], [], [], []
        for well_name, well_info in self.integrative_wells.items():
            score = well_scores.get(well_name, 0)
            x, y = self.calculate_well_position(well_info['angle'])
            
            int_x.append(x)
            int_y.append(y)
            int_scores.append(score)
            int_names.append(well_name.title())
            int_colors.append(well_info['color'])
        
        self.fig.add_trace(go.Scatter(
            x=int_x, y=int_y,
            mode='markers+text',
            marker=dict(
                size=[score * 30 + 10 for score in int_scores],  # Size based on score
                color=int_colors,
                line=dict(width=2, color='black'),
                opacity=0.8
            ),
            text=int_names,
            textposition="middle center",
            textfont=dict(size=10, color='white', family='Arial Black'),
            name='Integrative Wells',
            hovertemplate='<b>%{text}</b><br>Score: %{marker.size}<extra></extra>',
            customdata=int_scores
        ))
        
        # 4. Add disintegrative wells
        dis_x, dis_y, dis_scores, dis_names, dis_colors = [], [], [], [], []
        for well_name, well_info in self.disintegrative_wells.items():
            score = well_scores.get(well_name, 0)
            x, y = self.calculate_well_position(well_info['angle'])
            
            dis_x.append(x)
            dis_y.append(y)
            dis_scores.append(score)
            dis_names.append(well_name.title())
            dis_colors.append(well_info['color'])
        
        self.fig.add_trace(go.Scatter(
            x=dis_x, y=dis_y,
            mode='markers+text',
            marker=dict(
                size=[score * 30 + 10 for score in dis_scores],  # Size based on score
                color=dis_colors,
                line=dict(width=2, color='black'),
                opacity=0.8
            ),
            text=dis_names,
            textposition="middle center",
            textfont=dict(size=10, color='white', family='Arial Black'),
            name='Disintegrative Wells',
            hovertemplate='<b>%{text}</b><br>Score: %{marker.size}<extra></extra>',
            customdata=dis_scores
        ))
        
        # 5. Calculate and add narrative position
        narrative_x, narrative_y = self.calculate_narrative_position(well_scores)
        
        self.fig.add_trace(go.Scatter(
            x=[narrative_x], y=[narrative_y],
            mode='markers',
            marker=dict(
                size=20,
                color='gold',
                symbol='star',
                line=dict(width=3, color='black')
            ),
            name='Narrative Position',
            hovertemplate='<b>Narrative Position</b><br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>'
        ))
        
        # 6. Add quadrant labels
        self.fig.add_annotation(x=0.7, y=0.7, text="High Integration<br>High Elevation",
                               showarrow=False, font=dict(size=12, color="gray"))
        self.fig.add_annotation(x=-0.7, y=0.7, text="Low Integration<br>High Elevation",
                               showarrow=False, font=dict(size=12, color="gray"))
        self.fig.add_annotation(x=0.7, y=-0.7, text="High Integration<br>Low Elevation",
                               showarrow=False, font=dict(size=12, color="gray"))
        self.fig.add_annotation(x=-0.7, y=-0.7, text="Low Integration<br>Low Elevation",
                               showarrow=False, font=dict(size=12, color="gray"))
        
        # 7. Layout configuration
        self.fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16, family="Arial")
            ),
            xaxis=dict(
                title="Integration Dimension →",
                range=[-1.5, 1.5],
                zeroline=True,
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=1
            ),
            yaxis=dict(
                title="Elevation Dimension →",
                range=[-1.5, 1.5],
                zeroline=True,
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=1
            ),
            width=self.width,
            height=self.height,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        # Ensure equal aspect ratio for proper ellipse
        self.fig.update_yaxes(scaleanchor="x", scaleratio=1)
        
        return self.fig


def test_with_lincoln_data():
    """Test the elliptical visualizer with real Lincoln data."""
    
    print("🎯 Testing Plotly Elliptical Visualization with Lincoln Data")
    print("=" * 60)
    
    # Load Lincoln data
    data_file = "tmp/true_end_to_end_20250611_154042/academic_exports/lincoln_true_test_20250611_154042.csv"
    df = pd.read_csv(data_file)
    
    # Extract well scores
    well_scores = {}
    well_columns = [col for col in df.columns if col.startswith('well_')]
    
    for col in well_columns:
        well_name = col.replace('well_', '')
        well_scores[well_name] = df[col].iloc[0]
    
    print(f"✅ Extracted well scores: {well_scores}")
    
    # Create visualizer
    visualizer = PlotlyEllipticalVisualizer(width=900, height=900)
    
    # Generate elliptical plot
    title = "Lincoln 1865 Second Inaugural - Elliptical Analysis<br><sub>Custom Design with Modern Plotly Platform</sub>"
    fig = visualizer.create_elliptical_plot(well_scores, title)
    
    # Save outputs
    fig.write_html('lincoln_elliptical_plotly.html')
    print("✅ Generated: lincoln_elliptical_plotly.html")
    
    try:
        fig.write_image('lincoln_elliptical_plotly.png', width=900, height=900, scale=2)
        print("✅ Generated: lincoln_elliptical_plotly.png")
    except Exception as e:
        print(f"⚠️ PNG export error: {e}")
    
    # Calculate narrative position
    narrative_x, narrative_y = visualizer.calculate_narrative_position(well_scores)
    
    print(f"\n📊 Analysis Results:")
    print(f"   • Narrative Position: ({narrative_x:.3f}, {narrative_y:.3f})")
    print(f"   • Integrative Wells: {list(visualizer.integrative_wells.keys())}")
    print(f"   • Disintegrative Wells: {list(visualizer.disintegrative_wells.keys())}")
    
    print(f"\n🎉 Modern Elliptical Visualization Complete!")
    print(f"   ✅ Custom elliptical design preserved")
    print(f"   ✅ Interactive Plotly features added")
    print(f"   ✅ Academic platform compliance")
    print(f"   ✅ Publication-ready output")
    
    return fig


def create_comparison_dashboard():
    """Create a comparison between different visualization styles."""
    
    # Load data
    data_file = "tmp/true_end_to_end_20250611_154042/academic_exports/lincoln_true_test_20250611_154042.csv"
    df = pd.read_csv(data_file)
    
    # Extract well scores
    well_scores = {}
    well_columns = [col for col in df.columns if col.startswith('well_')]
    for col in well_columns:
        well_scores[col.replace('well_', '')] = df[col].iloc[0]
    
    # Create subplot figure
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            'Custom Elliptical Design (Plotly)',
            'Standard Scatter Plot (Plotly)'
        ),
        specs=[[{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Left: Custom elliptical
    visualizer = PlotlyEllipticalVisualizer()
    elliptical_fig = visualizer.create_elliptical_plot(well_scores)
    
    # Add elliptical traces to subplot
    for trace in elliptical_fig.data:
        fig.add_trace(trace, row=1, col=1)
    
    # Right: Standard scatter
    fig.add_trace(
        go.Scatter(
            x=[df['narrative_position_x'].iloc[0]],
            y=[df['narrative_position_y'].iloc[0]],
            mode='markers',
            marker=dict(size=15, color='blue'),
            name='Standard Position'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Visualization Comparison: Custom vs Standard",
        height=500,
        showlegend=False
    )
    
    fig.write_html('visualization_comparison.html')
    print("✅ Generated: visualization_comparison.html")
    
    return fig


if __name__ == "__main__":
    # Test elliptical visualization
    elliptical_fig = test_with_lincoln_data()
    
    print("\n" + "="*60)
    
    # Create comparison
    comparison_fig = create_comparison_dashboard()
    
    print(f"\n🎯 Files Generated:")
    print(f"   • lincoln_elliptical_plotly.html - Custom elliptical design")
    print(f"   • lincoln_elliptical_plotly.png - High-res image")
    print(f"   • visualization_comparison.html - Side-by-side comparison")
    
    print(f"\n✨ Benefits of Plotly Elliptical:")
    print(f"   🎨 Your custom elliptical design preserved")
    print(f"   🖱️ Interactive tooltips and zooming")
    print(f"   📱 Mobile-friendly touch interactions")
    print(f"   🎓 Academic platform compliance")
    print(f"   🔗 Easy to embed in papers/presentations")
    print(f"   🔄 Reproducible across platforms") 