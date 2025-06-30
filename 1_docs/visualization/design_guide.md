# Discernus Visualization Design Guide

*Essential Standards for Computational Social Science*

---

## **What is Discernus?**

Discernus is an open-source platform designed to be the essential professional workbench and infrastructure layer for computational social science text analysis—analogous to what Posit provides for R, but purpose-built for the demands of rigorous, transparent, and scalable text-based research.

**Our mission:**
Empower researchers and analysts with tools that are functionally robust, visually distinctive, and publication-ready by default—raising the bar for clarity, reproducibility, and accessibility in computational social science.

---

## **Why Design Standards Matter**

Discernus figures and visualizations must:

* **Communicate clearly**—no distractions, no ambiguities
* **Meet or exceed leading journal requirements** out of the box
* **Be accessible** to all audiences, including those with color vision deficiencies and those relying on black-and-white prints
* **Set a visible standard** for scientific quality and integrity

*We believe that beautiful, accessible figures should be the norm, not the exception.*

---

## **Discernus Visualization Standards**

### 1. **Typography Strategy: Distinctive + Compliant**

Discernus uses a **tiered typography system** that maintains visual identity while ensuring seamless academic compliance.

#### **Tier 1: Discernus Identity (Default)**
* **Primary Font:** Inter (modern, interface-optimized)
* **Fallback Chain:** Inter → Source Sans Pro → Arial → Helvetica → sans-serif
* **Why Inter:**
  - Highly distinctive, contemporary tech-forward aesthetic
  - Designed specifically for user interfaces and screen reading
  - Superior character differentiation (crucial for data visualization)
  - Excellent readability at small sizes (optimized for digital)
  - Modern computational research aesthetic (used by GitHub, Figma)

#### **Tier 2: Academic Journal Compliance (Auto-switch)**
* **Journals requiring specific fonts:** Auto-fallback to Arial/Helvetica
* **Size compliance:** Auto-scale to journal requirements (5-7pt for Nature)
* **Export modes:** PDF exports can embed fonts, ensuring consistency

#### **Smart Typography Configuration**
```python
# Discernus Typography System
DISCERNUS_FONTS = {
    'primary': ['Inter', 'Source Sans Pro', 'Arial', 'Helvetica', 'sans-serif'],
    'academic_fallback': ['Arial', 'Helvetica', 'sans-serif'],
    'monospace': ['JetBrains Mono', 'Source Code Pro', 'Consolas', 'Monaco', 'monospace']
}

# Automatic journal compliance
def setup_journal_style(journal='nature'):
    """Auto-configure for specific journal requirements"""
    if journal == 'nature':
        font_config = {
            'family': 'sans-serif',
            'sans-serif': ['Arial', 'Helvetica'],
            'title': 7, 'label': 6, 'tick': 5
        }
    elif journal == 'discernus':
        font_config = {
            'family': 'sans-serif', 
            'sans-serif': DISCERNUS_FONTS['primary'],
            'title': 12, 'label': 10, 'tick': 9
        }
    
    plt.rcParams.update(font_config)
```

#### **The "One-Click Compliance" Approach**
```python
# In any Discernus notebook
import discernus.viz as dv

# Default: Distinctive Discernus style
dv.setup_style()  # Uses Source Sans Pro, larger sizes

# Journal submission: One line change
dv.setup_style('nature')  # Auto-switches to Arial, 5-7pt
dv.setup_style('science')  # Auto-switches to journal requirements

# All existing code works unchanged!
```

---

### 2. **Color Palettes & Grayscale Strategy**

#### **Primary Color Palette**
* **Paul Tol's "Bright" Palette**—maximal colorblind safety, visually distinctive, and good in grayscale:

  | Color  | Hex     | Grayscale Value |
  | ------ | ------- | --------------- |
  | Blue   | #4477AA | Dark gray (30%) |
  | Green  | #228833 | Medium gray (50%) |
  | Yellow | #CCBB44 | Light gray (75%) |
  | Red    | #EE6677 | Medium gray (60%) |
  | Gray   | #BBBBBB | Light gray (73%) |

#### **Grayscale Compatibility (CRITICAL)**
* **Pattern/Texture System:** Use hatching patterns for filled areas
  - Solid (no pattern), diagonal (///), vertical (|||), dots (...)
* **Line Style Variations:** Employ different line styles for multi-series
  - Solid (-), dashed (--), dash-dot (-.), dotted (:)
* **Marker Shape Strategy:** Use distinct shapes for scatter plots
  - Circle (o), square (s), triangle (^), diamond (D)
* **High Contrast Mode:** All elements must have >70% contrast difference

#### **Academic Journal Requirements**
* **Nature:** Must be interpretable in grayscale/black-and-white
* **Science:** Strongly recommends grayscale compatibility
* **PNAS:** Requires B&W compatibility for some article types
* **PLOS:** Mandates accessibility-first design approach

#### **Implementation**
```python
# Color + pattern approach
import discernus.visualization as dv

# Default colorful mode
dv.setup_style('discernus')

# Grayscale-compatible mode  
dv.setup_style('discernus', grayscale_mode=True)

# Auto-generate grayscale patterns
colors, patterns = dv.auto_grayscale_palette(n_categories=4)
```

---

### 3. **Layout and Chart Conventions**

* **Gridlines:** Only horizontal, light gray, thin
* **Axes:** Minimal ticks, subtle lines, no heavy borders
* **Legend:** Outside plot if possible, else direct labeling
* **Panels/facets:** Consistent panel labeling (a), (b), (c), upper-left, bold, lower-case
* **No chartjunk:** No 3D, no pie charts, no excessive effects
* **Figure Size:**

  * Single-column: 3.5" wide (9 cm)
  * Double-column: 7.2" wide (18 cm)
  * Max height: 5" (12 cm)
  * Export: PDF/SVG (vector) and 600dpi PNG

#### **Smart Text Positioning with adjustText**

For scatter plots and data point labeling, Discernus uses the `adjustText` library for professional text positioning:

```python
from adjustText import adjust_text

# For scatter plot point labels
texts = []
for i, (x, y) in enumerate(data_points):
    text = ax.text(x, y, f'Point {i}', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    texts.append(text)

# Apply smart positioning for data labels
adjust_text(texts, ax=ax,
           force_text=(0.1, 0.2),      # Repel labels from each other
           force_static=(0.1, 0.2),    # Repel labels from data points
           expand=(1.1, 1.2),          # Expand bounding boxes
           ensure_inside_axes=True,    # Keep labels inside plot
           arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7, lw=1))
```

**Best for:**
* ✅ Scatter plot point labeling
* ✅ Data point annotations with many overlapping labels
* ✅ Dynamic positioning where semantic position isn't critical

**For coordinate space anchors**, use manual positioning with smart alignment:
```python
# For framework anchors that should stay near semantic positions
for name, (x, y) in anchor_positions.items():
    # Position outside circle with proper alignment
    label_x = x * 1.15  # Just outside unit circle
    label_y = y * 1.15
    
    # Smart alignment to avoid edge clipping
    ha = 'left' if x > 0.1 else 'right' if x < -0.1 else 'center'
    va = 'bottom' if y > 0.1 else 'top' if y < -0.1 else 'center'
    
    ax.text(label_x, label_y, name, ha=ha, va=va, weight='bold')
```

---

### 4. **Sample Notebook Template**

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

plt.rcParams.update({
    "font.family": "Inter",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "axes.edgecolor": "#222222",
    "axes.linewidth": 0.8,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

TOL_COLORS = ['#4477AA', '#228833', '#CCBB44', '#EE6677', '#BBBBBB']

sns.set_theme(
    context='notebook',
    style='whitegrid',
    palette=TOL_COLORS,
    font='Inter',
    font_scale=1.1,
)

# Example data
np.random.seed(42)
x = np.linspace(0, 10, 30)
df = pd.DataFrame({
    'x': np.tile(x, 3),
    'y': np.concatenate([
        np.sin(x) + np.random.normal(0, 0.2, len(x)),
        np.sin(x + 0.5) + np.random.normal(0, 0.2, len(x)),
        np.sin(x + 1) + np.random.normal(0, 0.2, len(x))
    ]),
    'group': np.repeat(['Group A', 'Group B', 'Group C'], len(x))
})

fig, ax = plt.subplots(figsize=(7.2, 4))
sns.lineplot(
    data=df,
    x='x', y='y',
    hue='group',
    style='group',
    markers=True,
    dashes=True,
    ax=ax
)
ax.set_title('(a) Example Publication-Ready Plot', loc='left', fontweight='bold')
ax.set_xlabel("X Axis Label")
ax.set_ylabel("Y Axis Label")
ax.legend(title='', frameon=False, loc='upper right')
sns.despine()
plt.tight_layout()
plt.savefig("figure_a.pdf")
plt.savefig("figure_a.png", dpi=600)
plt.show()
```

---

### 5. **Visual Design Checklist**

Add this markdown cell to every notebook:

```markdown
## Visualization Checklist

- [x] Uses Paul Tol colorblind-safe palette
- [x] All text set in Inter, 11–13pt
- [x] Direct labeling or clear legend
- [x] No chartjunk, gridlines minimal
- [x] Exported as PDF and 600dpi PNG
- [x] Grayscale/print previewed for accessibility
- [x] Figure size: 7.2" x 4" (double-column width)
- [x] Clear, informative title and axes
- [x] Uses adjustText for complex label positioning
```

---

### 6. **"Bad vs. Good" Visualization Gallery**

| Bad Example                                                                                               | Good Example                                                                                                              |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| ![Bad Example](https://i.imgur.com/RaOBP4D.png)<br>*Chartjunk, illegible font, low contrast, legend-only* | ![Good Example](https://i.imgur.com/AVSmJPd.png)<br>*Discernus Standard: clean font, palette, gridlines, direct labeling* |
| ![Bad Bar](https://i.imgur.com/EkslElj.png)<br>*Saturated, 3D, vertical text*                             | ![Good Bar](https://i.imgur.com/nqVPUlJ.png)<br>*Discernus Standard: muted palette, horizontal text, clear layout*        |
| ![Bad Facet](https://i.imgur.com/ErEqbPS.png)<br>*Cluttered, inconsistent*                                | ![Good Facet](https://i.imgur.com/JM1G3wM.png)<br>*Discernus Standard: aligned, labeled, colorblind safe*                 |

> **See `/docs/visual_gallery.ipynb` for a complete set with annotations.**

---

### 7. **Linting and Enforcement**

#### **Discernus Visual Linter (prototype)**

* Checks for forbidden plot types (`plt.pie`)
* Ensures use of approved palettes and font
* Warns on nonstandard figure sizes, missing checklist cell, or chartjunk

```python
import nbformat

def lint_notebook(filename):
    nb = nbformat.read(open(filename), as_version=4)
    findings = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            code = cell['source']
            if 'plt.pie' in code:
                findings.append("Pie charts are not Discernus Standard.")
            if 'Comic Sans' in code:
                findings.append("Comic Sans is forbidden—use Inter/Lato/Roboto.")
            if '#e5e5e5' not in code and 'grid' in code:
                findings.append("Use minimal, light gray gridlines.")
    return findings

print(lint_notebook('analysis.ipynb'))
```

* Integrate with [pre-commit](https://pre-commit.com/) or nbQA for automated checks.
* Every template must include the "Visualization Checklist" markdown cell.

---

### 8. **Contributor Guidance**

1. **Start with the Discernus template notebooks.**
2. **Import `viz_style.py` for color/font standards.**
3. **Preview every figure in grayscale.**
4. **Check your notebook with the Discernus linter before PR/commit.**
5. **Consult the visual gallery to ensure your figures meet the standard.**
6. **Ask for feedback—raising the bar is everyone's responsibility.**

---

### **References and Further Reading**

* [Paul Tol's Color Schemes](https://personal.sron.nl/~pault/)
* [ColorBrewer](https://colorbrewer2.org/)
* [Nature Graphics Guide (PDF)](https://www.nature.com/documents/nature-graphics-guide.pdf)
* [APA Figure Guidelines](https://apastyle.apa.org/style-grammar-guidelines/tables-figures/figures)
* [Okabe & Ito Palette](https://jfly.uni-koeln.de/color/)
* [nbQA: Notebook Quality Assurance](https://nbqa.readthedocs.io/en/latest/)

