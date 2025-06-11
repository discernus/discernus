#!/usr/bin/env python3
"""
Test Modern Academic Visualization with Real Lincoln Data
========================================================

Demonstrates the difference between custom and modern academic visualization
using the actual Lincoln 1865 analysis results from the true end-to-end test.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from pathlib import Path

# Set publication theme
pio.templates.default = "plotly_white"

def load_lincoln_data():
    """Load the real Lincoln analysis data."""
    
    # Use the actual Lincoln data from our true end-to-end test
    data_file = "tmp/true_end_to_end_20250611_154042/academic_exports/lincoln_true_test_20250611_154042.csv"
    
    print(f"📂 Loading Lincoln data from: {data_file}")
    df = pd.read_csv(data_file)
    
    print(f"✅ Loaded {len(df)} analysis records with {len(df.columns)} variables")
    print(f"📊 Columns: {list(df.columns)}")
    
    return df

def create_modern_narrative_plot(df):
    """Modern replacement for the custom elliptical visualization."""
    
    print("🎨 Creating modern narrative position plot...")
    
    # Create interactive scatter plot
    fig = px.scatter(
        df, 
        x='narrative_position_x', 
        y='narrative_position_y',
        color='framework_config_id',
        size='framework_fit_score',
        hover_data=['llm_model', 'exp_name', 'success'],
        title='Lincoln 1865 - Modern Narrative Position Analysis<br><sub>Interactive Academic Standard (Replaces Custom System)</sub>',
        labels={
            'narrative_position_x': 'Integrative Axis →',
            'narrative_position_y': 'Elevation Axis →',
            'framework_config_id': 'Framework'
        }
    )
    
    # Add reference lines
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, 
                  annotation_text="Neutral Elevation")
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5,
                  annotation_text="Neutral Integration")
    
    # Academic styling
    fig.update_layout(
        font=dict(size=12, family="Arial"),
        width=900, height=700,
        title_font_size=16,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_well_scores_analysis(df):
    """Comprehensive well scores visualization."""
    
    print("🎨 Creating modern well scores analysis...")
    
    # Get well columns
    well_cols = [col for col in df.columns if col.startswith('well_')]
    
    if not well_cols:
        print("❌ No well score columns found")
        return None
    
    print(f"✅ Found {len(well_cols)} well score columns: {well_cols}")
    
    # Create the analysis figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Lincoln 1865: Well Scores Distribution',
            'Integrative vs Disintegrative Wells', 
            'Individual Well Scores',
            'Success Rate Analysis'
        ),
        specs=[
            [{"type": "box"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "pie"}]
        ]
    )
    
    # 1. Well scores distribution (Box plot)
    well_data = df[well_cols].melt(var_name='well', value_name='score')
    well_data['well'] = well_data['well'].str.replace('well_', '')
    
    for well in well_data['well'].unique():
        well_scores = well_data[well_data['well'] == well]['score']
        fig.add_trace(
            go.Box(y=well_scores, name=well, showlegend=False),
            row=1, col=1
        )
    
    # 2. Integrative vs Disintegrative comparison
    integrative_wells = ['dignity', 'truth', 'hope', 'justice', 'pragmatism']
    disintegrative_wells = ['tribalism', 'manipulation', 'fantasy', 'resentment', 'fear']
    
    int_scores = [df[f'well_{well}'].iloc[0] for well in integrative_wells if f'well_{well}' in df.columns]
    dis_scores = [df[f'well_{well}'].iloc[0] for well in disintegrative_wells if f'well_{well}' in df.columns]
    
    categories = ['Integrative Wells', 'Disintegrative Wells']
    mean_scores = [np.mean(int_scores) if int_scores else 0, np.mean(dis_scores) if dis_scores else 0]
    
    fig.add_trace(
        go.Bar(x=categories, y=mean_scores, 
               marker_color=['green', 'red'],
               showlegend=False),
        row=1, col=2
    )
    
    # 3. Individual well scores (scatter)
    individual_wells = [col.replace('well_', '').title() for col in well_cols]
    individual_scores = [df[col].iloc[0] for col in well_cols]
    
    fig.add_trace(
        go.Scatter(
            x=individual_wells, 
            y=individual_scores,
            mode='markers+lines',
            marker=dict(size=10, color=individual_scores, colorscale='RdYlGn'),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 4. Success analysis
    success_count = df['success'].sum()
    total_count = len(df)
    fig.add_trace(
        go.Pie(
            labels=['Success', 'Failure'],
            values=[success_count, total_count - success_count],
            marker_colors=['green', 'red'],
            showlegend=False
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text="Lincoln 1865 Second Inaugural - Modern Academic Analysis",
        title_font_size=16,
        font=dict(size=12)
    )
    
    return fig

def create_publication_ready_figure(df):
    """Create publication-ready figure for academic papers."""
    
    print("🎨 Creating publication-ready figure...")
    
    fig = go.Figure()
    
    # Add the analysis point
    fig.add_trace(go.Scatter(
        x=[df['narrative_position_x'].iloc[0]],
        y=[df['narrative_position_y'].iloc[0]],
        mode='markers',
        marker=dict(
            size=15,
            color='darkblue',
            line=dict(width=2, color='black'),
            symbol='circle'
        ),
        name='Lincoln 1865',
        hovertemplate=(
            '<b>Lincoln 1865 Second Inaugural</b><br>' +
            'Integrative Position: %{x:.3f}<br>' +
            'Elevation Position: %{y:.3f}<br>' +
            '<extra></extra>'
        )
    ))
    
    # Add quadrant labels
    fig.add_annotation(x=0.3, y=0.3, text="High Integration<br>High Elevation", 
                      showarrow=False, font=dict(size=10, color="gray"))
    fig.add_annotation(x=-0.3, y=0.3, text="Low Integration<br>High Elevation",
                      showarrow=False, font=dict(size=10, color="gray"))
    fig.add_annotation(x=0.3, y=-0.3, text="High Integration<br>Low Elevation",
                      showarrow=False, font=dict(size=10, color="gray"))
    fig.add_annotation(x=-0.3, y=-0.3, text="Low Integration<br>Low Elevation",
                      showarrow=False, font=dict(size=10, color="gray"))
    
    # Academic formatting
    fig.update_layout(
        title=dict(
            text="Lincoln's Second Inaugural Address (1865)<br><sub>Narrative Gravity Analysis</sub>",
            font=dict(size=16, family="Times New Roman")
        ),
        xaxis_title="Integrative Dimension",
        yaxis_title="Elevation Dimension", 
        font=dict(family="Times New Roman", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=600, height=450,
        xaxis=dict(
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgray',
            range=[-0.5, 0.5]
        ),
        yaxis=dict(
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgray',
            range=[-0.5, 0.5]
        )
    )
    
    return fig

def main():
    """Test modern visualization with real Lincoln data."""
    
    print("🎯 Testing Modern Academic Visualization with Real Lincoln Data")
    print("=" * 70)
    
    # Load actual data
    df = load_lincoln_data()
    
    # Display data preview
    print("\n📊 Data Preview:")
    print(df.head())
    
    print(f"\n📈 Key Analysis Results:")
    print(f"   • Experiment: {df['exp_name'].iloc[0]}")
    print(f"   • Model: {df['llm_model'].iloc[0]}")
    print(f"   • Success: {df['success'].iloc[0]}")
    print(f"   • Narrative Position: ({df['narrative_position_x'].iloc[0]:.3f}, {df['narrative_position_y'].iloc[0]:.3f})")
    print(f"   • Framework Fit: {df['framework_fit_score'].iloc[0]:.3f}")
    
    # Generate modern visualizations
    print("\n🚀 Generating Modern Academic Visualizations...")
    
    # 1. Modern narrative position plot
    narrative_fig = create_modern_narrative_plot(df)
    narrative_fig.write_html('lincoln_modern_narrative.html')
    print("✅ Generated: lincoln_modern_narrative.html (Interactive)")
    
    # 2. Comprehensive well scores analysis
    well_fig = create_well_scores_analysis(df)
    if well_fig:
        well_fig.write_html('lincoln_modern_wells.html')
        print("✅ Generated: lincoln_modern_wells.html (Interactive)")
    
    # 3. Publication-ready figure
    pub_fig = create_publication_ready_figure(df)
    pub_fig.write_html('lincoln_publication_ready.html')
    # Save high-resolution PNG for papers
    try:
        pub_fig.write_image('lincoln_publication_ready.png', width=600, height=450, scale=3)
        print("✅ Generated: lincoln_publication_ready.png (Publication)")
    except Exception as e:
        print(f"⚠️ PNG export requires kaleido: pip install kaleido")
    
    print("\n🎉 Modern Visualization Demo Complete!")
    print("\n📁 Generated Files:")
    print("   • lincoln_modern_narrative.html - Interactive narrative analysis")
    print("   • lincoln_modern_wells.html - Comprehensive well scores dashboard")
    print("   • lincoln_publication_ready.html - Publication-ready figure")
    print("   • lincoln_publication_ready.png - High-res image for papers")
    
    print("\n🔥 Benefits Over Custom System:")
    print("   ✅ Interactive tooltips and zooming")
    print("   ✅ Publication-ready styling by default")
    print("   ✅ Reproducible across platforms")
    print("   ✅ Standard academic tool (Plotly)")
    print("   ✅ Journal editor acceptance")
    print("   ✅ Easy to modify and extend")
    
    print("\n🎯 Next Step: Open the HTML files in your browser!")

if __name__ == "__main__":
    main() 