# Centralized Visualization Architecture
**Version 2.0 - Theme-Aware Unified System**

## 🎯 **Architecture Overview**

The Narrative Gravity Maps platform now uses a **centralized visualization engine** that eliminates scattered matplotlib implementations and provides consistent, theme-aware visualizations across all use cases.

### **Core Principles**
1. **Single Source of Truth**: One visualization engine for all use cases
2. **Theme Consistency**: Professional styling without pixel-pushing
3. **Framework Agnostic**: Works with any well configuration
4. **Publication Ready**: Multiple output formats (HTML, PNG, SVG, PDF)
5. **Maintainable**: Centralized code reduces duplication

## 🏗️ **System Components**

### **1. Centralized Engine**
```python
src/narrative_gravity/visualization/engine.py
```

**Main Class**: `NarrativeGravityVisualizationEngine`
- Theme-aware styling system
- Multiple visualization types (single, comparative, dashboard)
- Publication-ready export capabilities
- Consistent API across all use cases

### **2. Theme System**
```python
src/narrative_gravity/visualization/themes.py
```

**Available Themes**:
- **Academic**: Professional publication styling (Times New Roman, formal colors)
- **Presentation**: High-contrast for demos (large fonts, bright colors)
- **Minimal**: Clean modern interface (Inter font, subtle colors)
- **Dark**: Reduced eye strain (dark background, light text)

### **3. Legacy Compatibility**
```python
src/narrative_gravity/visualization/plotly_circular.py
```

**Maintained For**: Backward compatibility and direct Plotly access
- Direct circular visualizer access
- Legacy code support during migration
- Advanced customization scenarios

## 🚀 **Usage Patterns**

### **Recommended: Centralized Engine**
```python
from narrative_gravity.visualization import create_visualization_engine

# Create themed engine
engine = create_visualization_engine(theme='academic')

# Single analysis
fig = engine.create_single_analysis(
    wells=wells,
    narrative_scores=scores,
    title="Analysis Title",
    output_html="output.html"
)

# Comparative analysis
fig = engine.create_comparative_analysis(
    analyses=[analysis1, analysis2, analysis3],
    title="Comparative Analysis"
)

# Dashboard with multiple analyses
fig = engine.create_dashboard(
    analyses=analyses,
    title="Research Dashboard",
    include_summary=True
)
```

### **Quick Usage: One-liner**
```python
from narrative_gravity.visualization import quick_viz

fig = quick_viz(wells, scores, title="Quick Analysis", theme='presentation')
```

### **Theme Management**
```python
from narrative_gravity.visualization import get_theme, list_themes

# List available themes
themes = list_themes()  # ['academic', 'presentation', 'minimal', 'dark']

# Get theme configuration
theme = get_theme('academic')
print(theme.style)  # Theme styling configuration
print(theme.well_colors)  # Color mappings
```

## 🎨 **Theme System Deep Dive**

### **Theme Structure**
Each theme provides:
- **Style Configuration**: Fonts, sizes, colors, spacing
- **Layout Configuration**: Plotly layout settings
- **Well Color Mapping**: Framework-agnostic color schemes
- **Apply Method**: Automatic figure styling

### **Academic Theme Example**
```python
style = {
    'font_family': 'Times New Roman',
    'title_size': 18,
    'well_marker_size': 16,
    'boundary_color': '#000000',
    'background_color': 'white'
}

well_colors = {
    'integrative': '#1B5E20',      # Dark green
    'disintegrative': '#B71C1C',   # Dark red
    'virtue': '#4A148C',           # Dark purple
    'default': '#424242'           # Dark gray
}
```

### **Creating Custom Themes**
```python
from narrative_gravity.visualization.themes import VisualizationTheme

class CustomTheme(VisualizationTheme):
    def __init__(self):
        super().__init__("custom")
    
    @property
    def style(self):
        return {
            'font_family': 'Custom Font',
            'title_size': 20,
            # ... custom styling
        }
    
    @property
    def well_colors(self):
        return {
            'integrative': '#Custom1',
            'disintegrative': '#Custom2'
        }
```

## 📊 **Migration Strategy**

### **Phase 1: Core System Migration**
**Target Files**: Academic templates, dashboard scripts, export systems

**Before (Scattered)**:
```python
# Multiple different implementations
import matplotlib.pyplot as plt

class CustomCircularVisualizer:
    def plot_circle_boundary(self):
        # Custom matplotlib implementation
        pass
    
    def plot_wells_and_scores(self):
        # Another custom implementation
        pass
```

**After (Centralized)**:
```python
from narrative_gravity.visualization import create_visualization_engine

engine = create_visualization_engine(theme='academic')
fig = engine.create_single_analysis(wells, scores, title)
```

### **Phase 2: Theme Consistency**
**Before**: Pixel-pushing individual charts
```python
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12
ax.set_title("Title", fontsize=16, fontweight='bold')
# ... lots of manual styling
```

**After**: Theme-based styling
```python
engine = create_visualization_engine(theme='academic')
# All styling automatically consistent
```

### **Phase 3: Publication Export**
**Before**: Manual export handling
```python
plt.savefig('output.png', dpi=300, bbox_inches='tight')
# Manual HTML generation
# Manual SVG export
```

**After**: Automated multi-format export
```python
exported = engine.export_for_publication(
    figure=fig,
    output_dir='publication/',
    filename='analysis',
    formats=['html', 'png', 'svg', 'pdf']
)
```

## 🔧 **Implementation Benefits**

### **For Developers**
- **Single codebase**: One visualization system to maintain
- **Consistent API**: Same patterns across all use cases
- **Theme abstraction**: No pixel-pushing required
- **Type safety**: Full TypeScript-style typing

### **For Researchers**
- **Consistent output**: All visualizations look professional
- **Multiple formats**: Interactive and static outputs
- **Publication ready**: Academic-quality styling
- **Customizable**: Themes for different use cases

### **For Platform**
- **Maintainability**: Centralized code reduces bugs
- **Scalability**: Easy to add new visualization types
- **Consistency**: Brand-consistent outputs
- **Performance**: Optimized single system

## 📁 **File Organization**

### **Centralized System**
```
src/narrative_gravity/visualization/
├── __init__.py           # Main exports and convenience functions
├── engine.py             # Centralized visualization engine
├── themes.py             # Theme system and built-in themes
└── plotly_circular.py    # Legacy compatibility layer
```

### **Usage Throughout Codebase**
```
# All these now use centralized system:
src/narrative_gravity/academic/analysis_templates.py    # Templates
src/narrative_gravity/academic/data_export.py          # Export scripts
src/narrative_gravity/corpus/exporter.py               # Corpus analysis
scripts/create_generic_multi_run_dashboard.py          # Dashboards
scripts/generate_experiment_reports.py                 # Reports
```

## 🎯 **Quality Standards**

### **Visualization Consistency**
- ✅ All visualizations use same theme system
- ✅ Framework-agnostic color schemes
- ✅ Professional typography and spacing
- ✅ Consistent interactive behavior

### **Code Quality**
- ✅ Single source of truth for visualization logic
- ✅ Type-safe interfaces with proper documentation
- ✅ Comprehensive error handling and fallbacks
- ✅ Unit tests for all theme and engine functionality

### **Publication Readiness**
- ✅ Multiple export formats (HTML, PNG, SVG, PDF)
- ✅ High-resolution outputs for print
- ✅ Academic styling standards
- ✅ Accessibility considerations

## 🚀 **Migration Checklist**

### **High Priority Files**
- [ ] `src/narrative_gravity/academic/analysis_templates.py`
- [ ] `src/narrative_gravity/academic/data_export.py`
- [ ] `src/narrative_gravity/corpus/exporter.py`
- [ ] `scripts/create_generic_multi_run_dashboard.py`
- [ ] `scripts/create_generic_multi_run_dashboard_no_api.py`

### **Medium Priority Files**
- [ ] `scripts/generate_experiment_reports.py`
- [ ] Academic pipeline integration tests
- [ ] Example and demo files

### **Low Priority Files**
- [ ] Archive/development files
- [ ] Temporary analysis scripts
- [ ] Notebook outputs

## 📈 **Success Metrics**

### **Code Quality**
- **Lines of visualization code**: Target 70% reduction
- **Matplotlib imports**: Target 90% reduction in core files
- **Consistency**: 100% theme compliance in production code

### **User Experience**
- **Styling consistency**: All outputs use professional themes
- **Export capability**: Multi-format support for all visualizations
- **Performance**: Faster generation through optimized single system

### **Maintainability**
- **Bug reduction**: Centralized fixes benefit all visualizations
- **Feature velocity**: New visualization types easy to add
- **Documentation**: Single system easier to document and learn

---

**This centralized architecture transforms Narrative Gravity Maps from a collection of scattered visualization scripts into a professional, maintainable, theme-aware visualization platform.** 