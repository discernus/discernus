# Discernus Visualization Documentation

Complete documentation for the Discernus design system, enabling publication-quality visualizations with distinctive identity, universal accessibility, and seamless journal compliance.

## 📚 Documentation

### **[Design Guide](design_guide.md)** - Start Here!
The comprehensive Discernus visual design guide covering typography, colors, layouts, and standards.

**What's included:**
- Inter typography system with journal compliance
- Paul Tol colorblind-safe palettes  
- Grayscale compatibility strategies
- Nature/Science journal specifications
- Code examples and implementation guides

### Coming Soon

- **Typography Guide** - Detailed Inter font system and academic compliance
- **Grayscale Guide** - Complete B&W compatibility strategies  
- **Accessibility Guide** - WCAG 2.1 AA compliance standards
- **Journal Compliance** - Specific requirements for major journals

## 🚀 Quick Start

```python
from discernus.visualization import setup_style

# Distinctive Discernus identity
setup_style('discernus')

# Journal compliance (one line change!)
setup_style('nature')  # or 'science', 'pnas'

# Grayscale compatibility
setup_style('discernus', grayscale_mode=True)
```

## 🎯 Key Features

### **Typography: "Cake and Eat It Too"**
- **Inter** for distinctive, modern identity
- **Automatic fallback** to Arial for journal compliance
- **One-line switching** between modes
- **Zero code refactoring** needed

### **Universal Accessibility** 
- **Colorblind-safe** palettes (Paul Tol standards)
- **Grayscale compatibility** with patterns/textures
- **WCAG 2.1 AA** compliance
- **High contrast** modes

### **Academic Standards**
- **Nature journal** specifications (89mm/183mm columns)
- **2+ standard deviation** aesthetic quality
- **Industry libraries** (SciencePlots, ColorBrewer)
- **Publication-ready** vector outputs

## 📖 Examples

Complete examples are available in `examples/visualization/`:

- **Basic:** `typography_workflow_demo.py` - Learn the fundamentals
- **Advanced:** `complete_workflow_demo.py` - Full production workflow  
- **Gallery:** `academic_visualization_demo.py` - Showcase quality

## 🎨 Design Philosophy

**Distinctive + Compliant**: Researchers shouldn't choose between visual identity and journal requirements. Discernus provides both through intelligent design system architecture.

**Accessibility First**: All visualizations work for colorblind users, in grayscale/B&W printing, and meet WCAG standards by default.

**Zero Friction**: One-line changes switch between research presentation mode and journal submission mode using the same codebase.

---

*The Discernus design system represents 2+ standard deviation quality in academic visualization - combining distinctive identity with universal accessibility and seamless compliance.* 