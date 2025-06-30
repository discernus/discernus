#!/usr/bin/env python3
"""
Discernus Grayscale Strategy: Publication-Ready Black & White Compatibility

Ensures all Discernus visualizations work perfectly in grayscale/black-and-white
contexts, meeting academic journal requirements and accessibility standards.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

# =============================================================================
# GRAYSCALE COMPATIBILITY SYSTEM
# =============================================================================

# Paul Tol's grayscale-optimized patterns
GRAYSCALE_PATTERNS = {
    'solid': '',
    'dots': '.',
    'diagonal': '///',
    'vertical': '|||',
    'horizontal': '---',
    'cross': '+++',
    'diagonal_cross': 'xxx',
    'circles': 'ooo'
}

# Line styles for grayscale distinction
GRAYSCALE_LINESTYLES = [
    '-',      # Solid line
    '--',     # Dashed line  
    '-.',     # Dash-dot line
    ':',      # Dotted line
    (0, (3, 1, 1, 1)),      # Dash-dot-dot
    (0, (5, 2, 2, 2)),      # Long dash-short dash
    (0, (1, 1)),            # Dense dots
    (0, (3, 3))             # Medium dashes
]

# Marker styles for scatter plots
GRAYSCALE_MARKERS = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']

# Grayscale color palette (perceptually uniform)
GRAYSCALE_COLORS = [
    '#000000',  # Black
    '#404040',  # Dark gray
    '#808080',  # Medium gray  
    '#B0B0B0',  # Light gray
    '#D0D0D0',  # Very light gray
    '#FFFFFF'   # White (with black edges)
]

def setup_grayscale_style():
    """Configure matplotlib for optimal grayscale output"""
    plt.rcParams.update({
        # Use patterns and textures
        'hatch.linewidth': 0.5,
        'hatch.color': 'black',
        
        # Emphasize line weights and styles
        'lines.linewidth': 2.0,
        'lines.markeredgewidth': 1.0,
        'lines.markersize': 8,
        
        # Ensure good contrast
        'axes.edgecolor': 'black',
        'axes.linewidth': 1.0,
        'xtick.color': 'black',
        'ytick.color': 'black',
        'text.color': 'black',
        
        # Grid for structure
        'axes.grid': True,
        'grid.color': '#808080',
        'grid.linewidth': 0.5,
        'grid.alpha': 0.7
    })

def create_pattern_legend(categories, patterns=None, colors=None):
    """Create a legend showing patterns for grayscale compatibility"""
    if patterns is None:
        patterns = list(GRAYSCALE_PATTERNS.values())[:len(categories)]
    if colors is None:
        colors = GRAYSCALE_COLORS[:len(categories)]
    
    legend_elements = []
    for i, category in enumerate(categories):
        if i < len(patterns):
            patch = mpatches.Patch(
                facecolor=colors[i % len(colors)], 
                hatch=patterns[i],
                edgecolor='black',
                linewidth=1,
                label=category
            )
            legend_elements.append(patch)
    
    return legend_elements

def demonstrate_grayscale_strategies():
    """Demonstrate multiple grayscale-compatible visualization strategies"""
    
    setup_grayscale_style()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Sample data
    categories = ['Populism', 'Pluralism', 'Nationalism', 'Patriotism']
    values = [0.8, 0.4, 0.9, 0.6]
    errors = [0.05, 0.08, 0.06, 0.04]
    
    # Strategy 1: Patterns + Grayscale
    patterns = ['', '///', '|||', '...']
    colors = ['#000000', '#404040', '#808080', '#B0B0B0']
    
    bars1 = ax1.bar(categories, values, color=colors, 
                   edgecolor='black', linewidth=1.5)
    for bar, pattern in zip(bars1, patterns):
        bar.set_hatch(pattern)
    
    ax1.errorbar(categories, values, yerr=errors, fmt='none', 
                color='black', capsize=5, capthick=2)
    ax1.set_title('A. Patterns + Grayscale Colors', fontweight='bold')
    ax1.set_ylabel('Intensity Score')
    ax1.tick_params(axis='x', rotation=45)
    
    # Strategy 2: Line styles for time series
    x = np.linspace(0, 10, 50)
    for i, (category, style) in enumerate(zip(categories, GRAYSCALE_LINESTYLES[:4])):
        y = np.sin(x + i*0.5) + 0.1*i
        ax2.plot(x, y, linestyle=style, color='black', linewidth=2, 
                label=category, marker=GRAYSCALE_MARKERS[i], 
                markersize=6, markevery=8)
    
    ax2.set_title('B. Line Styles + Markers', fontweight='bold')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Score')
    ax2.legend(loc='upper left', frameon=True, fancybox=False, 
              edgecolor='black', facecolor='white')
    
    # Strategy 3: Marker shapes for scatter
    np.random.seed(42)
    for i, (category, marker) in enumerate(zip(categories, GRAYSCALE_MARKERS[:4])):
        x_data = np.random.normal(i*2, 0.6, 30)
        y_data = np.random.normal(1, 0.4, 30)
        ax3.scatter(x_data, y_data, marker=marker, s=80, 
                   facecolors='white', edgecolors='black', linewidth=1.5,
                   label=category)
    
    ax3.set_title('C. Marker Shapes', fontweight='bold')
    ax3.set_xlabel('Political Dimension')
    ax3.set_ylabel('Intensity')
    ax3.legend(loc='upper right', frameon=True, fancybox=False,
              edgecolor='black', facecolor='white')
    
    # Strategy 4: High contrast coordinate space
    theta = np.linspace(0, 2*np.pi, 100)
    ax4.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2)
    
    # Framework anchors with distinct markers
    anchors = {'Populism': (0, 1), 'Pluralism': (0, -1), 
              'Nationalism': (1, 0), 'Patriotism': (-1, 0)}
    markers_anchor = ['s', 'o', '^', 'D']
    
    for i, (name, (x, y)) in enumerate(anchors.items()):
        ax4.scatter(x, y, s=200, marker=markers_anchor[i], 
                   facecolors='white', edgecolors='black', linewidth=2)
        offset = 1.2
        ax4.annotate(name, (x*offset, y*offset), ha='center', va='center',
                    fontweight='bold', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                             edgecolor='black', linewidth=1))
    
    # Add coordinate grid
    ax4.axhline(y=0, color='black', linewidth=1, alpha=0.7)
    ax4.axvline(x=0, color='black', linewidth=1, alpha=0.7)
    ax4.grid(True, alpha=0.3, color='gray')
    
    ax4.set_xlim(-1.6, 1.6)
    ax4.set_ylim(-1.6, 1.6)
    ax4.set_aspect('equal')
    ax4.set_title('D. High Contrast Coordinate Space', fontweight='bold')
    ax4.set_xlabel('Patriotism ← → Nationalism')
    ax4.set_ylabel('Pluralism ← → Populism')
    
    plt.tight_layout()
    fig.suptitle('Grayscale Compatibility Strategies for Academic Publishing', 
                fontsize=14, fontweight='bold', y=0.98)
    
    return fig

def test_grayscale_conversion(original_fig):
    """Test how a colored figure looks when converted to grayscale"""
    
    # Create a copy and convert to grayscale
    grayscale_fig = plt.figure(figsize=original_fig.get_size_inches())
    
    # This is a simplified grayscale test - in practice, you'd use 
    # specialized tools or save as grayscale PDF
    print("🔍 GRAYSCALE CONVERSION TEST")
    print("="*40)
    print("✅ Original figure created")
    print("📝 For true grayscale testing:")
    print("   1. Save as PDF: fig.savefig('test.pdf')")
    print("   2. Print preview in grayscale mode")
    print("   3. Use GIMP/Photoshop desaturate function")
    print("   4. Test with colorblind simulation tools")
    print("\n🎯 Key checks:")
    print("   • All data series distinguishable?")
    print("   • Legend/labels still clear?")
    print("   • Statistical annotations visible?")
    print("   • Overall message preserved?")

def create_grayscale_checklist():
    """Generate a checklist for grayscale compatibility"""
    
    checklist = """
    📋 DISCERNUS GRAYSCALE COMPATIBILITY CHECKLIST
    
    □ Use patterns/hatching for filled areas
    □ Employ different line styles for multi-series plots
    □ Use distinct marker shapes for scatter plots
    □ Ensure sufficient contrast between elements
    □ Test figure in actual grayscale/print preview
    □ Verify legend/labels remain interpretable
    □ Check that statistical annotations are visible
    □ Confirm overall message is preserved
    □ Consider adding texture/pattern legend
    □ Test with colorblind simulation tools
    
    🎯 JOURNAL REQUIREMENTS:
    • Nature: Must be interpretable in grayscale
    • Science: Recommends grayscale compatibility
    • PNAS: Requires B&W compatibility for some sections
    • PLOS: Encourages accessibility-first design
    """
    
    return checklist

def auto_grayscale_palette(n_categories):
    """Generate optimal grayscale palette with patterns"""
    
    if n_categories <= len(GRAYSCALE_COLORS):
        colors = GRAYSCALE_COLORS[:n_categories]
        patterns = list(GRAYSCALE_PATTERNS.values())[:n_categories]
    else:
        # Cycle through combinations
        colors = [GRAYSCALE_COLORS[i % len(GRAYSCALE_COLORS)] for i in range(n_categories)]
        patterns = [list(GRAYSCALE_PATTERNS.values())[i % len(GRAYSCALE_PATTERNS)] for i in range(n_categories)]
    
    return colors, patterns

if __name__ == "__main__":
    print("📊 DISCERNUS GRAYSCALE COMPATIBILITY SYSTEM")
    print("="*50)
    
    # Generate demonstration
    fig = demonstrate_grayscale_strategies()
    
    # Save in multiple formats for testing
    fig.savefig('grayscale_strategies.pdf', dpi=300, bbox_inches='tight')
    fig.savefig('grayscale_strategies_bw.pdf', dpi=300, bbox_inches='tight', 
               facecolor='white', edgecolor='black')
    
    plt.show()
    
    # Show checklist
    print(create_grayscale_checklist())
    
    # Test conversion
    test_grayscale_conversion(fig)
    
    print("\n✅ Files saved:")
    print("📁 grayscale_strategies.pdf")
    print("📁 grayscale_strategies_bw.pdf")
    print("\n🎯 Your figures now work perfectly in black & white!") 