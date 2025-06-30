# Discernus Visualization Examples

This directory contains comprehensive examples demonstrating the Discernus design system for publication-quality computational social science visualizations.

## Organization

### 📚 `basic/`
**Start here** - Fundamental demonstrations of individual design system components:

- `typography_workflow_demo.py` - Shows the "cake and eat it too" typography system
- `color_palette_demo.py` - *(coming soon)* Color theory and accessibility
- `grayscale_demo.py` - *(coming soon)* Black & white compatibility

**Perfect for:** Learning the basics, understanding individual features

### 🚀 `advanced/`
**Real-world usage** - Complete workflows and production-ready examples:

- `complete_workflow_demo.py` - Full Inter → grayscale → journal compliance pipeline
- `academic_demo_no_latex.py` - 2+ sigma academic quality without LaTeX dependencies
- `multi_framework_comparison.py` - *(coming soon)* Comparing multiple frameworks

**Perfect for:** Production use, complex analyses, journal submissions

### 🎨 `gallery/`
**Visual showcase** - Curated examples demonstrating best practices:

- `academic_visualization_demo.py` - Industry-standard academic visualization showcase
- `good_vs_bad_examples.py` - *(coming soon)* Design principles in action
- `journal_compliance_showcase.py` - *(coming soon)* Nature/Science compliance examples

**Perfect for:** Understanding design principles, showcasing capabilities

## Quick Start

### 1. Learn the Basics
```bash
cd basic/
python3 typography_workflow_demo.py
```

### 2. See Real-World Usage  
```bash
cd advanced/
python3 complete_workflow_demo.py
```

### 3. Explore the Gallery
```bash
cd gallery/
python3 academic_visualization_demo.py
```

## Design System Features Demonstrated

### 🎯 **Typography System**
- **Inter** typography for distinctive identity
- **Arial** fallback for journal compliance
- One-line switching between modes
- Nature/Science journal specifications

### ♿ **Accessibility Standards**
- **WCAG 2.1 AA** compliance
- **Colorblind-safe** palettes (Paul Tol)
- **Grayscale compatibility** with patterns
- **High contrast** modes

### 📊 **Academic Compliance**
- **Nature journal** specifications (89mm/183mm columns)
- **5-7pt typography** requirements
- **Vector formats** (EPS/PDF) for publication
- **300 DPI** export standards

### 🎨 **Visual Quality**
- **2+ standard deviation** aesthetic quality
- **Industry-standard libraries** (SciencePlots, ColorBrewer)
- **Research-backed** color theory
- **Publication-ready** by default

## Integration with Core Library

All examples use the core Discernus visualization library:

```python
from discernus.visualization import setup_style

# Distinctive identity mode
setup_style('discernus')

# Grayscale compatible mode  
setup_style('discernus', grayscale_mode=True)

# Journal compliance mode
setup_style('nature')  # or 'science', 'pnas'
```

## Output Files

Generated files are automatically saved to:
- `outputs/examples/` - Individual example outputs
- `outputs/gallery/` - Showcase and comparison outputs

## Documentation

For complete design system documentation, see:
- `1_docs/visualization/design_guide.md` - Main design guide
- `1_docs/visualization/typography_guide.md` - Typography details  
- `1_docs/visualization/grayscale_guide.md` - B&W compatibility
- `1_docs/visualization/accessibility_guide.md` - WCAG compliance

## Contributing

When adding new examples:

1. **Basic examples:** Single-feature demonstrations
2. **Advanced examples:** Complete workflows and real-world usage
3. **Gallery examples:** Best practice showcases and comparisons

Ensure all examples:
- Include comprehensive comments
- Generate output files in `outputs/`
- Demonstrate accessibility features
- Follow the established naming patterns

---

*The Discernus design system enables computational social science researchers to create publication-quality visualizations with distinctive identity, universal accessibility, and seamless journal compliance.* 