#!/usr/bin/env python3
"""
Enhanced Academic Visualization Templates
========================================

Replaces custom visualization system with industry-standard academic tools.
Generates publication-ready R, Python, and interactive visualization code.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.narrative_gravity.academic.analysis_templates import (
    JupyterTemplateGenerator, RScriptGenerator, StataIntegration
)


class ModernVisualizationGenerator:
    """Generate modern academic visualization templates."""
    
    def __init__(self):
        self.jupyter_gen = JupyterTemplateGenerator()
        self.r_gen = RScriptGenerator()
        self.stata_gen = StataIntegration()
    
    def generate_plotly_template(self, study_name: str) -> str:
        """Generate modern Plotly-based visualization template."""
        
        template = f'''#!/usr/bin/env python3
"""
Modern Academic Visualization: {study_name}
Interactive publication-quality charts using Plotly
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Set publication theme
pio.templates.default = "plotly_white"

def load_and_prepare_data():
    """Load academic data export."""
    # Load from your academic export
    df = pd.read_csv('academic_exports/{study_name}.csv')
    
    # Parse well scores if they're in JSON format
    if 'raw_scores' in df.columns:
        well_scores = df['raw_scores'].apply(lambda x: eval(x) if isinstance(x, str) else x)
        well_df = pd.json_normalize(well_scores)
        df = pd.concat([df, well_df], axis=1)
    
    return df

def create_narrative_position_plot(df):
    """Modern replacement for custom elliptical visualization."""
    
    fig = px.scatter(
        df, 
        x='narrative_position_x', 
        y='narrative_position_y',
        color='framework_config_id',
        size='framework_fit_score',
        hover_data=['llm_model', 'exp_name'],
        title='Narrative Position Analysis (Modern Academic Standard)',
        labels={{
            'narrative_position_x': 'Integrative Axis →',
            'narrative_position_y': 'Elevation Axis →',
            'framework_config_id': 'Framework'
        }}
    )
    
    # Add reference lines
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Academic styling
    fig.update_layout(
        font=dict(size=12),
        width=800, height=600,
        title_font_size=16
    )
    
    return fig

def create_well_scores_dashboard(df):
    """Comprehensive well scores visualization."""
    
    # Get well columns
    well_cols = [col for col in df.columns if col.startswith('well_')]
    
    if not well_cols:
        print("No well score columns found")
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Well Scores Distribution',
            'Framework Comparison', 
            'Model Performance',
            'Correlation Matrix'
        ),
        specs=[[{{"type": "box"}}, {{"type": "bar"}}],
               [{{"type": "violin"}}, {{"type": "heatmap"}}]]
    )
    
    # 1. Well scores distribution
    well_data = df[well_cols].melt()
    fig.add_trace(
        go.Box(y=well_data['value'], x=well_data['variable'], name='Well Scores'),
        row=1, col=1
    )
    
    # 2. Framework comparison (mean scores)
    framework_means = df.groupby('framework_config_id')[well_cols].mean()
    for framework in framework_means.index:
        fig.add_trace(
            go.Bar(x=well_cols, y=framework_means.loc[framework], name=framework),
            row=1, col=2
        )
    
    # 3. Model performance
    if 'llm_model' in df.columns and 'coherence' in df.columns:
        fig.add_trace(
            go.Violin(y=df['coherence'], x=df['llm_model'], name='Coherence'),
            row=2, col=1
        )
    
    # 4. Well correlations
    if len(well_cols) > 1:
        corr_matrix = df[well_cols].corr()
        fig.add_trace(
            go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                colorscale='RdBu',
                zmid=0
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=800,
        title_text="Comprehensive Well Scores Analysis",
        showlegend=False
    )
    
    return fig

def create_publication_figure(df):
    """Create publication-ready figure for academic papers."""
    
    fig = go.Figure()
    
    # Add narrative positions by framework
    for framework in df['framework_config_id'].unique():
        framework_data = df[df['framework_config_id'] == framework]
        
        fig.add_trace(go.Scatter(
            x=framework_data['narrative_position_x'],
            y=framework_data['narrative_position_y'],
            mode='markers',
            name=framework,
            marker=dict(
                size=10,
                opacity=0.7,
                line=dict(width=1, color='black')
            )
        ))
    
    # Academic formatting
    fig.update_layout(
        title=dict(
            text="Narrative Gravity Analysis",
            font=dict(size=16, family="Times New Roman")
        ),
        xaxis_title="Integrative Dimension",
        yaxis_title="Elevation Dimension", 
        font=dict(family="Times New Roman", size=12),
        plot_bgcolor='white',
        width=600, height=450,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left", 
            x=0.01
        )
    )
    
    # Add reference lines
    fig.add_hline(y=0, line_dash="dash", line_color="lightgray")
    fig.add_vline(x=0, line_dash="dash", line_color="lightgray")
    
    return fig

def main():
    """Generate all modern visualizations."""
    
    print("📊 Generating Modern Academic Visualizations")
    print("=" * 50)
    
    # Load data
    df = load_and_prepare_data()
    print(f"✅ Loaded {{len(df)}} analysis records")
    
    # Generate visualizations
    print("🎨 Creating narrative position plot...")
    narrative_fig = create_narrative_position_plot(df)
    narrative_fig.write_html('narrative_position_modern.html')
    narrative_fig.write_image('narrative_position_modern.png', width=800, height=600, scale=2)
    
    print("🎨 Creating well scores dashboard...")
    dashboard_fig = create_well_scores_dashboard(df)
    if dashboard_fig:
        dashboard_fig.write_html('well_scores_dashboard.html')
        dashboard_fig.write_image('well_scores_dashboard.png', width=1200, height=800, scale=2)
    
    print("🎨 Creating publication figure...")
    pub_fig = create_publication_figure(df)
    pub_fig.write_html('publication_figure.html')
    pub_fig.write_image('publication_figure.png', width=600, height=450, scale=3)
    
    print("\\n✅ Modern visualizations completed!")
    print("📁 Files generated:")
    print("   • narrative_position_modern.html (Interactive)")
    print("   • narrative_position_modern.png (Publication)")
    print("   • well_scores_dashboard.html (Interactive)")
    print("   • well_scores_dashboard.png (Publication)")
    print("   • publication_figure.html (Interactive)")
    print("   • publication_figure.png (Publication-ready)")

if __name__ == "__main__":
    main()
'''
        
        # Save the template
        output_path = Path("modern_visualization_template.py")
        with open(output_path, 'w') as f:
            f.write(template)
        
        return str(output_path)
    
    def generate_enhanced_r_template(self, study_name: str) -> str:
        """Enhanced R template with modern ggplot2 + plotly."""
        
        template = f'''# Enhanced Academic Visualization in R
# Study: {study_name}
# Modern ggplot2 + plotly for publication-quality figures

library(tidyverse)
library(plotly)
library(corrplot)
library(viridis)
library(patchwork)  # For combining plots

# Load data
df <- read_csv("academic_exports/{study_name}.csv")

# Modern Narrative Position Plot (replaces custom elliptical)
narrative_plot <- df %>%
  ggplot(aes(x = narrative_position_x, y = narrative_position_y)) +
  geom_point(aes(color = framework_config_id, size = framework_fit_score),
             alpha = 0.7) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.5) +
  scale_color_viridis_d(name = "Framework") +
  scale_size_continuous(name = "Fit Score", range = c(2, 8)) +
  theme_minimal() +
  theme(
    text = element_text(family = "Times", size = 12),
    plot.title = element_text(size = 14, hjust = 0.5)
  ) +
  labs(
    title = "Narrative Position Analysis",
    x = "Integrative Dimension →",
    y = "Elevation Dimension →",
    caption = "Source: Narrative Gravity Wells Analysis"
  )

# Save publication version
ggsave("narrative_position_publication.png", narrative_plot,
       width = 8, height = 6, dpi = 300, bg = "white")

# Interactive version
narrative_interactive <- ggplotly(narrative_plot)
htmlwidgets::saveWidget(narrative_interactive, "narrative_position_interactive.html")

# Well Scores Comparison (modern academic style)
well_cols <- df %>% select(starts_with("well_")) %>% names()

if (length(well_cols) > 0) {{
  well_data <- df %>%
    select(framework_config_id, all_of(well_cols)) %>%
    pivot_longer(all_of(well_cols), names_to = "well", values_to = "score") %>%
    mutate(well = str_remove(well, "well_"))
  
  well_plot <- well_data %>%
    ggplot(aes(x = reorder(well, score, FUN = median), y = score)) +
    geom_violin(aes(fill = well), alpha = 0.7, show.legend = FALSE) +
    geom_boxplot(width = 0.2, alpha = 0.8) +
    facet_wrap(~framework_config_id, scales = "free_x") +
    coord_flip() +
    scale_fill_viridis_d() +
    theme_minimal() +
    theme(
      text = element_text(family = "Times", size = 10),
      strip.text = element_text(size = 12, face = "bold")
    ) +
    labs(
      title = "Well Scores Distribution by Framework",
      x = "Civic Virtue Wells",
      y = "Score (0-1 scale)"
    )
  
  ggsave("well_scores_comparison.png", well_plot,
         width = 12, height = 8, dpi = 300, bg = "white")
}}

# Framework Performance Dashboard
performance_plot <- df %>%
  ggplot(aes(x = framework_config_id)) +
  geom_bar(aes(fill = success), position = "fill") +
  scale_fill_manual(values = c("FALSE" = "#d73027", "TRUE" = "#1a9850")) +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal() +
  theme(
    text = element_text(family = "Times", size = 12),
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  labs(
    title = "Framework Success Rate",
    x = "Framework",
    y = "Success Rate",
    fill = "Success"
  )

ggsave("framework_performance.png", performance_plot,
       width = 10, height = 6, dpi = 300, bg = "white")

cat("✅ Enhanced R visualizations completed!\\n")
cat("📁 Generated files:\\n")
cat("   • narrative_position_publication.png\\n")
cat("   • narrative_position_interactive.html\\n") 
cat("   • well_scores_comparison.png\\n")
cat("   • framework_performance.png\\n")
'''
        
        # Save the template
        output_path = Path("enhanced_r_template.R")
        with open(output_path, 'w') as f:
            f.write(template)
        
        return str(output_path)

def main():
    """Generate enhanced visualization templates."""
    
    print("🚀 Generating Enhanced Academic Visualization Templates")
    print("=" * 60)
    
    generator = ModernVisualizationGenerator()
    
    # Generate modern Python template
    python_template = generator.generate_plotly_template("lincoln_true_test")
    print(f"✅ Generated modern Python template: {python_template}")
    
    # Generate enhanced R template  
    r_template = generator.generate_enhanced_r_template("lincoln_true_test")
    print(f"✅ Generated enhanced R template: {r_template}")
    
    print("\n🎯 Next Steps:")
    print("1. Run these templates with your real Lincoln data")
    print("2. Compare output quality with custom system")
    print("3. Choose your preferred academic standard")
    print("4. Update your pipeline to use modern tools")
    
    print("\n📊 Benefits:")
    print("   • Publication-ready by default")
    print("   • Interactive versions for presentations")
    print("   • Reproducible across platforms")
    print("   • Journal editor acceptance")

if __name__ == "__main__":
    main() 