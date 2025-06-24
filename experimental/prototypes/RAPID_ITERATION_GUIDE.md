# Rapid Iteration Guide: Discernus Visualization Engine

**Version**: 1.0  
**Date**: 2025-06-24  
**Purpose**: Fast visualization development without production pipeline overhead

## 🎯 **Overview**

This guide shows you how to rapidly iterate on both visualization **function** and **appearance** using the Discernus Visualization Engine without running end-to-end production pipelines.

## 🚀 **Quick Start Workflow**

### **1. Setup Environment**
```bash
# Navigate to iteration workspace
cd experimental/prototypes

# Verify systems are working
python3 discernus_visualization_engine.py
```

### **2. Load Static Results**

#### **Option A: Create Sample Data (Fastest)**
```python
import pandas as pd
from discernus_visualization_engine import create_visualization_engine

# Create sample moral foundations data
sample_data = {
    'text_id': ['climate_article', 'political_speech', 'healthcare_debate'],
    'framework': ['moral_foundations', 'moral_foundations', 'moral_foundations'],
    'model': ['gpt-4-turbo', 'gpt-4-turbo', 'gpt-4-turbo'],
    'api_cost': [0.002, 0.003, 0.002],
    'well_care': [0.85, 0.45, 0.90],
    'well_fairness': [0.70, 0.80, 0.75],
    'well_loyalty': [0.30, 0.85, 0.40],
    'well_authority': [0.25, 0.75, 0.30],
    'well_sanctity': [0.20, 0.60, 0.35]
}

df = pd.DataFrame(sample_data)
```

#### **Option B: Load Production Results**
```python
# Load from production experiment
experiment_path = "../../experiments/System_Health_Test_v1.0.0_20250624_095635"
results_file = f"{experiment_path}/experiment_results.json"

import json
with open(results_file, 'r') as f:
    production_results = json.load(f)

# Extract structured data
df = pd.DataFrame(production_results['structured_results']['structured_data'])
```

### **3. Initialize Visualization Engine**
```python
# Create engine with your preferred theme
engine = create_visualization_engine(theme='academic')

# Or try different themes
# engine = create_visualization_engine(theme='presentation')
# engine = create_visualization_engine(theme='publication')
```

### **4. Generate Initial Visualizations**
```python
# Prepare results in expected format
structured_results = {'structured_data': df}
statistical_results = {'hypothesis_testing': {'test_hypothesis': {'status': 'supported'}}}
reliability_results = {'reliability_metrics': {'model_consistency': {'total_models': 3}}}

# Generate all visualizations
viz_results = engine.generate_comprehensive_visualizations(
    structured_results, statistical_results, reliability_results
)

print("✅ Initial visualizations generated!")
print(f"📁 Files created: {len(engine.generated_files)}")
```

## ⚡ **Rapid Iteration Workflows**

### **Scenario 1: Coordinate System Appearance**

#### **Make Changes:**
```python
# Edit coordinate system styling
from discernus_coordinate_visualizer import DiscernusCoordinateVisualizer

# Try different themes or create custom styling
coord_viz = DiscernusCoordinateVisualizer(
    radius=1.0,           # Try: 0.8, 1.2
    figure_size=800,      # Try: 600, 1000
    theme='academic'      # Try: 'presentation', 'publication'
)

# Define anchors with different positioning
anchors = {
    'Care': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
    'Fairness': {'angle': 72, 'type': 'integrative', 'weight': 1.0},
    'Loyalty': {'angle': 144, 'type': 'binding', 'weight': 1.0},
    'Authority': {'angle': 216, 'type': 'binding', 'weight': 1.0},
    'Sanctity': {'angle': 288, 'type': 'binding', 'weight': 1.0}
}

# Quick sample scores
axis_scores = {'Care': 0.8, 'Fairness': 0.6, 'Loyalty': 0.4, 'Authority': 0.3, 'Sanctity': 0.2}
```

#### **Refresh & View:**
```python
# Generate updated plot
fig = coord_viz.plot_coordinate_system(
    anchors=anchors,
    axis_scores=axis_scores,
    title='Rapid Iteration Test - Updated Styling',
    output_html='iteration_output/quick_test.html',
    show=False
)

print("🔄 Updated visualization generated!")
print("📂 Open: iteration_output/quick_test.html")
```

### **Scenario 2: Theme Switching**

#### **Make Changes:**
```python
# Switch themes instantly
for theme_name in ['academic', 'presentation', 'publication']:
    engine = create_visualization_engine(theme=theme_name)
    
    # Generate with new theme
    viz_results = engine.generate_comprehensive_visualizations(
        structured_results, statistical_results, reliability_results
    )
    
    # Move files to theme-specific folder
    import shutil, os
    theme_dir = f'iteration_output/theme_{theme_name}'
    os.makedirs(theme_dir, exist_ok=True)
    
    for file_path in engine.generated_files.values():
        if file_path.endswith('.html'):
            filename = os.path.basename(file_path)
            shutil.copy(file_path, f'{theme_dir}/{filename}')
    
    print(f"✅ {theme_name} theme visualizations ready!")
```

### **Scenario 3: Mathematical Changes**

#### **Make Changes:**
```python
# Test different centroid calculation approaches
class CustomCoordinateVisualizer(DiscernusCoordinateVisualizer):
    def calculate_centroid(self, anchors, scores):
        # EXPERIMENT: Different scaling approaches
        total_x = 0.0
        total_y = 0.0
        total_weight = 0.0
        
        for anchor_name, score in scores.items():
            if anchor_name in anchors:
                anchor = anchors[anchor_name]
                angle = anchor['angle']
                weight = abs(anchor.get('weight', 1.0))
                
                # Convert angle to radians
                angle_rad = np.radians(angle)
                x = np.cos(angle_rad) * self.radius
                y = np.sin(angle_rad) * self.radius
                
                # EXPERIMENT: Try different weighting
                # Option 1: Linear weighting (current)
                weighted_score = score * weight
                
                # Option 2: Quadratic weighting
                # weighted_score = (score ** 2) * weight
                
                # Option 3: Logarithmic weighting  
                # weighted_score = np.log(1 + score) * weight
                
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # EXPERIMENT: Different scaling factors
            scaling_factor = 0.9  # Try: 0.6, 0.8, 1.0
            return (centroid_x * scaling_factor, centroid_y * scaling_factor)
        
        return (0.0, 0.0)

# Test custom math
custom_viz = CustomCoordinateVisualizer(theme='academic')
```

#### **Refresh & Compare:**
```python
# Generate with custom math
fig_custom = custom_viz.plot_coordinate_system(
    anchors=anchors,
    axis_scores=axis_scores,
    title='Custom Math Test',
    output_html='iteration_output/custom_math_test.html',
    show=False
)

# Compare with original
fig_original = coord_viz.plot_coordinate_system(
    anchors=anchors,
    axis_scores=axis_scores,
    title='Original Math',
    output_html='iteration_output/original_math_test.html',
    show=False
)

print("🔄 Math comparison ready!")
print("📂 Compare: custom_math_test.html vs original_math_test.html")
```

### **Scenario 4: Statistical Plot Customization**

#### **Make Changes:**
```python
# Customize statistical visualizations
class CustomDiscernusEngine(DiscernusVisualizationEngine):
    def create_correlation_plots(self, df, anchor_columns, framework_name):
        """EXPERIMENT: Different correlation visualization approaches."""
        import plotly.graph_objects as go
        import plotly.express as px
        
        plots = {}
        
        if len(anchor_columns) < 2:
            return plots
        
        # Calculate correlation matrix
        anchor_data = df[anchor_columns].dropna()
        if anchor_data.empty:
            return plots
        
        correlation_matrix = anchor_data.corr()
        labels = [col.replace('well_', '').replace('_', ' ').title() for col in anchor_columns]
        
        # EXPERIMENT: Try different color schemes
        # Option 1: RdBu (current)
        colorscale = 'RdBu'
        
        # Option 2: Viridis
        # colorscale = 'Viridis'
        
        # Option 3: Custom
        # colorscale = [[0, 'red'], [0.5, 'white'], [1, 'blue']]
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=labels,
            y=labels,
            colorscale=colorscale,
            zmid=0,
            colorbar=dict(title="Correlation"),
            hoverongaps=False,
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        # EXPERIMENT: Different annotation styles
        for i, row in enumerate(correlation_matrix.values):
            for j, value in enumerate(row):
                if i != j:
                    fig.add_annotation(
                        x=j, y=i,
                        text=f"{value:.2f}",
                        showarrow=False,
                        font=dict(
                            color="white" if abs(value) > 0.5 else "black",
                            size=12  # Try: 10, 14, 16
                        )
                    )
        
        fig.update_layout(
            title=f'{framework_name.upper()} Framework - Correlation Analysis (Custom)',
            font=dict(family=self.theme.style['font_family']),
            plot_bgcolor=self.theme.style['background_color'],
            paper_bgcolor=self.theme.style['background_color'],
            width=900,   # EXPERIMENT: Try different sizes
            height=700
        )
        
        corr_file = self.output_dir / 'custom_correlation_matrix.html'
        fig.write_html(str(corr_file))
        plots['custom_correlation_matrix'] = str(corr_file)
        self.generated_files['custom_correlation_matrix'] = str(corr_file)
        
        return plots

# Test custom statistical plots
custom_engine = CustomDiscernusEngine(theme='academic')
```

## 🔄 **Hot-Reload Development Session**

### **Interactive Development Script**
Create `quick_iterate.py`:

```python
#!/usr/bin/env python3
"""
Quick iteration script for rapid visualization development.
Monitors for code changes and regenerates visualizations automatically.
"""

import time
import os
from pathlib import Path
import pandas as pd
from discernus_visualization_engine import create_visualization_engine

def load_sample_data():
    """Load consistent sample data for iteration."""
    return pd.DataFrame({
        'text_id': ['climate_article', 'political_speech', 'healthcare_debate'],
        'framework': ['moral_foundations', 'moral_foundations', 'moral_foundations'],
        'model': ['gpt-4-turbo', 'gpt-4-turbo', 'gpt-4-turbo'],
        'api_cost': [0.002, 0.003, 0.002],
        'well_care': [0.85, 0.45, 0.90],
        'well_fairness': [0.70, 0.80, 0.75],
        'well_loyalty': [0.30, 0.85, 0.40],
        'well_authority': [0.25, 0.75, 0.30],
        'well_sanctity': [0.20, 0.60, 0.35]
    })

def generate_quick_viz(theme='academic'):
    """Generate visualization quickly."""
    print(f"🔄 Generating with {theme} theme...")
    
    # Load data
    df = load_sample_data()
    
    # Create engine
    engine = create_visualization_engine(theme=theme)
    
    # Generate
    structured_results = {'structured_data': df}
    statistical_results = {'hypothesis_testing': {'test': {'status': 'supported'}}}
    reliability_results = {'reliability_metrics': {'model_consistency': {'total_models': 3}}}
    
    viz_results = engine.generate_comprehensive_visualizations(
        structured_results, statistical_results, reliability_results
    )
    
    print(f"✅ Generated {len(engine.generated_files)} files")
    return engine.generated_files

if __name__ == '__main__':
    print("🚀 Quick Iteration Session")
    print("=" * 50)
    
    while True:
        theme = input("Theme (academic/presentation/publication) or 'q' to quit: ").strip()
        
        if theme.lower() == 'q':
            break
            
        if theme in ['academic', 'presentation', 'publication']:
            files = generate_quick_viz(theme)
            print(f"📂 Open files in iteration_output/")
            print("🔄 Ready for next iteration...")
        else:
            print("❌ Invalid theme. Try: academic, presentation, publication")
```

### **Run Interactive Session:**
```bash
python3 quick_iterate.py
```

## 📊 **File Structure During Iteration**

```
experimental/prototypes/
├── iteration_output/           # Generated visualization files
│   ├── coordinate_*.html      # Coordinate system plots
│   ├── comparative_*.html     # Comparative analyses  
│   ├── correlation_*.html     # Statistical correlations
│   ├── hypothesis_*.html      # Hypothesis testing
│   └── comprehensive_*.html   # Dashboard views
├── theme_academic/            # Theme-specific outputs
├── theme_presentation/        
└── custom_experiments/        # Custom math/styling tests
```

## 🎯 **Iteration Strategies**

### **Visual Iteration**
1. **Theme switching** - Instant professional styling changes
2. **Color scheme experiments** - Try different palettes
3. **Layout modifications** - Adjust spacing, sizing, positioning
4. **Typography changes** - Font families, sizes, weights

### **Functional Iteration**  
1. **Mathematical approaches** - Different centroid calculations
2. **Scaling factors** - Adjust coordinate system scaling
3. **Anchor positioning** - Experiment with angle arrangements
4. **Statistical methods** - Alternative correlation displays

### **Data Iteration**
1. **Sample data variations** - Test different score distributions
2. **Framework comparisons** - Switch between moral foundations, etc.
3. **Scale testing** - Few vs many data points
4. **Edge case handling** - Missing data, extreme values

## ⚡ **Speed Tips**

### **Fastest Iteration Cycle:**
```python
# 1. Keep engine instance alive
engine = create_visualization_engine(theme='academic')

# 2. Modify only what you need
engine.theme_name = 'presentation'  # Quick theme switch
engine.theme = get_theme('presentation')

# 3. Generate single plots instead of comprehensive
from discernus_coordinate_visualizer import DiscernusCoordinateVisualizer
coord_viz = DiscernusCoordinateVisualizer(theme='presentation')

# 4. Use show=False, save to predictable locations
fig = coord_viz.plot_coordinate_system(
    anchors=anchors, axis_scores=scores,
    output_html='iteration_output/current_test.html',
    show=False
)

# 5. Open same file each time for instant refresh
print("📂 Refresh: iteration_output/current_test.html")
```

### **Browser Workflow:**
1. Keep `iteration_output/current_test.html` open in browser
2. Run iteration script
3. Refresh browser tab (Cmd+R / Ctrl+R)
4. See changes immediately

## 🔧 **Troubleshooting**

### **Common Issues:**
- **Import errors**: Check you're in `experimental/prototypes/` directory
- **Theme not found**: Verify theme name spelling in `discernus_themes.py`
- **File not found**: Check `iteration_output/` directory exists
- **Plotly errors**: Usually styling/layout parameter issues

### **Debug Mode:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed engine operations
engine = create_visualization_engine(theme='academic')
```

## 🎯 **Integration Back to Production**

When you're satisfied with your iterations:

1. **Document changes** in your iteration notes
2. **Test with production data** using real experiment results  
3. **Update production systems** in `src/analysis/visualization.py`
4. **Migrate theme changes** to production theme system
5. **Update orchestrator** to use new visualization patterns

## 📝 **Best Practices**

- **Save interesting iterations** with descriptive filenames
- **Document mathematical changes** in comments
- **Test edge cases** (missing data, extreme values)  
- **Compare themes** side-by-side before choosing
- **Keep sample data consistent** for fair comparisons
- **Use version control** to track successful iterations

---

**🚀 You now have a complete rapid iteration environment that lets you experiment with both visualization function and appearance without the overhead of running full production pipelines!** 