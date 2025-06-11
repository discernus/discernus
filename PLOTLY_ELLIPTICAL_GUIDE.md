# Plotly Elliptical Visualization Integration Guide

## Quick Start

```python
from src.narrative_gravity.visualization import PlotlyEllipticalVisualizer

# Create visualizer
visualizer = PlotlyEllipticalVisualizer(width=900, height=900)

# Your well scores (from analysis)
well_scores = {
    'hope': 0.855,
    'justice': 0.849,
    'dignity': 0.673,
    # ... other wells
}

# Generate elliptical plot
fig = visualizer.create_elliptical_plot(
    well_scores, 
    title="Your Analysis Title"
)

# Save outputs
fig.write_html('analysis_elliptical.html')  # Interactive
fig.write_image('analysis_elliptical.png')  # Publication
```

## Integration Points

### 1. Academic Data Export
- Elliptical visualizations automatically generated alongside CSV/JSON exports
- Both interactive (HTML) and static (PNG) versions created
- Compatible with existing academic pipeline

### 2. Jupyter Notebooks
- Use `visualizer.create_elliptical_plot()` in notebook cells
- Interactive plots display inline
- Easy to iterate and refine

### 3. Publication Pipeline
- High-resolution PNG export for papers
- Customizable styling for journal requirements
- SVG export also available for vector graphics

## Customization Options

### Design Parameters
```python
visualizer = PlotlyEllipticalVisualizer(
    width=1200,           # Plot width
    height=1000,          # Plot height
)

# Customize ellipse shape
visualizer.ellipse_a = 1.2    # Semi-major axis
visualizer.ellipse_b = 0.9    # Semi-minor axis
visualizer.well_radius = 1.3  # Well positioning radius
```

### Well Positioning
```python
# Modify well angles (degrees)
visualizer.integrative_wells['hope']['angle'] = 30
visualizer.disintegrative_wells['fear']['angle'] = 210
```

### Colors and Styling
```python
# Change well colors
visualizer.integrative_wells['hope']['color'] = '#1f77b4'
visualizer.disintegrative_wells['fear']['color'] = '#d62728'
```

## Refinement Roadmap

### For Publication (Future)
1. **Journal-specific styling**
   - Font families (Times New Roman, Arial, etc.)
   - Color schemes (grayscale for some journals)
   - Size specifications (column width, etc.)

2. **Advanced features**
   - Confidence intervals around narrative position
   - Animation between time periods
   - Multi-analysis comparison overlays

3. **Print optimization**
   - Vector graphics (SVG/PDF) for scalability
   - High-DPI rendering for print quality
   - Color-blind friendly palettes

## Current vs Deprecated System

| Feature | Deprecated | New Plotly |
|---------|------------|-------------|
| Interactivity | ❌ Static only | ✅ Full interactive |
| Platform | ❌ Custom/fragile | ✅ Industry standard |
| Export formats | ❌ Limited | ✅ HTML, PNG, SVG, PDF |
| Mobile support | ❌ None | ✅ Responsive |
| Journal acceptance | ❌ Questionable | ✅ Widely accepted |
| Maintenance | ❌ High effort | ✅ Maintained by Plotly |

## Next Steps

1. **Test with your data** - Run visualizations on your existing analyses
2. **Integrate into workflow** - Update scripts to use new visualizer  
3. **Gather feedback** - Share interactive versions with collaborators
4. **Refine for publication** - Customize when ready to submit papers

The system is ready for immediate use and can be refined iteratively!
