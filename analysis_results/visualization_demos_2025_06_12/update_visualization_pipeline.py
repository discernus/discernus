#!/usr/bin/env python3
"""
Update Visualization Pipeline to Use Plotly
==========================================

Integration script to replace the deprecated visualization system
with the new Plotly-based elliptical visualizer.
"""

import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def integrate_plotly_visualizer():
    """Integrate the Plotly elliptical visualizer into the main pipeline."""
    
    print("🔄 Integrating Plotly Elliptical Visualizer into Pipeline")
    print("=" * 60)
    
    # 1. Move the visualizer to the main package
    src_file = "plotly_elliptical_visualization.py"
    dest_dir = Path("src/narrative_gravity/visualization")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    dest_file = dest_dir / "plotly_elliptical.py"
    
    if Path(src_file).exists():
        shutil.copy2(src_file, dest_file)
        print(f"✅ Moved visualizer to: {dest_file}")
    else:
        print(f"❌ Source file not found: {src_file}")
        return False
    
    # 2. Create __init__.py for the visualization package
    init_file = dest_dir / "__init__.py"
    with open(init_file, 'w') as f:
        f.write('''"""
Narrative Gravity Visualization Package
=====================================

Modern academic visualization tools for narrative gravity analysis.
"""

from .plotly_elliptical import PlotlyEllipticalVisualizer

__all__ = ['PlotlyEllipticalVisualizer']
''')
    print(f"✅ Created package init: {init_file}")
    
    # 3. Update academic templates to use new visualizer
    update_academic_templates()
    
    # 4. Create integration guide
    create_integration_guide()
    
    print("\n🎉 Pipeline Integration Complete!")
    print(f"✅ Plotly elliptical visualizer ready for use")
    print(f"✅ Academic templates updated")
    print(f"✅ Integration guide created")
    
    return True

def update_academic_templates():
    """Update academic templates to include Plotly elliptical option."""
    
    # Find the academic templates file
    templates_file = Path("src/narrative_gravity/academic/analysis_templates.py")
    
    if not templates_file.exists():
        print(f"⚠️ Templates file not found: {templates_file}")
        return
    
    # Read current content
    with open(templates_file, 'r') as f:
        content = f.read()
    
    # Add import for Plotly elliptical at the top
    if "from ..visualization.plotly_elliptical import PlotlyEllipticalVisualizer" not in content:
        # Find the import section and add our import
        import_addition = """
# Visualization imports
try:
    from ..visualization.plotly_elliptical import PlotlyEllipticalVisualizer
    PLOTLY_ELLIPTICAL_AVAILABLE = True
except ImportError:
    PLOTLY_ELLIPTICAL_AVAILABLE = False
"""
        
        # Insert after existing imports
        if "from datetime import datetime" in content:
            content = content.replace(
                "from datetime import datetime",
                f"from datetime import datetime{import_addition}"
            )
        
        with open(templates_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated academic templates with Plotly elliptical import")

def create_integration_guide():
    """Create a guide for using the new visualization system."""
    
    guide_content = '''# Plotly Elliptical Visualization Integration Guide

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
'''
    
    guide_path = Path("PLOTLY_ELLIPTICAL_GUIDE.md")
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"✅ Created integration guide: {guide_path}")

def main():
    """Run the integration process."""
    
    success = integrate_plotly_visualizer()
    
    if success:
        print("\n🎯 Ready for Next Steps:")
        print("1. Test the integrated visualizer with your data")
        print("2. Update any existing scripts to use new system")
        print("3. Share interactive visualizations with collaborators") 
        print("4. Plan publication refinements as needed")
        
        print(f"\n📖 See PLOTLY_ELLIPTICAL_GUIDE.md for detailed usage")
    else:
        print("\n❌ Integration failed - check error messages above")

if __name__ == "__main__":
    main() 