#!/usr/bin/env python3
"""
Discernus Typography System: Distinctive + Compliant

Provides automatic font switching between Discernus identity and journal compliance.
Enables "having your cake and eating it too" - distinctive but standards-compliant.
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# =============================================================================
# DISCERNUS TYPOGRAPHY SYSTEM
# =============================================================================

DISCERNUS_FONTS = {
    'primary': ['Inter', 'Source Sans Pro', 'Arial', 'Helvetica', 'sans-serif'],
    'academic_fallback': ['Arial', 'Helvetica', 'sans-serif'],
    'monospace': ['JetBrains Mono', 'Source Code Pro', 'SF Mono', 'Consolas', 'Monaco', 'monospace']
}

TYPOGRAPHY_PROFILES = {
    'discernus': {
        'title': 12,
        'subtitle': 10,
        'label': 10,
        'tick': 9,
        'legend': 9,
        'annotation': 9.5,
        'font_family': DISCERNUS_FONTS['primary'],
        'description': 'Distinctive Discernus identity style'
    },
    'discernus_grayscale': {
        'title': 12,
        'subtitle': 10,
        'label': 10,
        'tick': 9,
        'legend': 9,
        'annotation': 9.5,
        'font_family': DISCERNUS_FONTS['primary'],
        'description': 'Discernus identity + grayscale compatibility'
    },
    'nature': {
        'title': 7,
        'subtitle': 6,
        'label': 6,
        'tick': 5,
        'legend': 5,
        'annotation': 5.5,
        'font_family': DISCERNUS_FONTS['academic_fallback'],
        'description': 'Nature journal compliance (5-7pt)'
    },
    'science': {
        'title': 8,
        'subtitle': 7,
        'label': 7,
        'tick': 6,
        'legend': 6,
        'annotation': 6.5,
        'font_family': DISCERNUS_FONTS['academic_fallback'],
        'description': 'Science journal compliance'
    },
    'pnas': {
        'title': 8,
        'subtitle': 7,
        'label': 7,
        'tick': 6,
        'legend': 6,
        'annotation': 6.5,
        'font_family': DISCERNUS_FONTS['academic_fallback'],
        'description': 'PNAS journal compliance'
    }
}

def check_font_availability():
    """Check which Discernus fonts are available on the system"""
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    discernus_status = {}
    for category, fonts in DISCERNUS_FONTS.items():
        discernus_status[category] = []
        for font in fonts:
            if font in available_fonts or font in ['sans-serif', 'monospace']:
                discernus_status[category].append(f"✅ {font}")
            else:
                discernus_status[category].append(f"❌ {font}")
    
    return discernus_status

def setup_style(profile='discernus', show_info=True, grayscale_mode=False):
    """
    Configure matplotlib with Discernus typography profiles
    
    Parameters:
    -----------
    profile : str
        Typography profile ('discernus', 'nature', 'science', 'pnas')
    show_info : bool
        Display configuration information
    grayscale_mode : bool
        Apply grayscale-compatible settings
    """
    
    if profile not in TYPOGRAPHY_PROFILES:
        raise ValueError(f"Profile '{profile}' not found. Available: {list(TYPOGRAPHY_PROFILES.keys())}")
    
    config = TYPOGRAPHY_PROFILES[profile]
    
    # Base matplotlib configuration
    base_config = {
        'font.family': 'sans-serif',
        'font.sans-serif': config['font_family'],
        'font.size': config['tick'],
        
        # Typography hierarchy
        'axes.titlesize': config['title'],
        'axes.labelsize': config['label'],
        'xtick.labelsize': config['tick'],
        'ytick.labelsize': config['tick'],
        'legend.fontsize': config['legend'],
        
        # Professional styling
        'axes.titleweight': 'bold',
        'axes.labelweight': 'normal',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.5,
        'axes.grid': True,
        'axes.axisbelow': True,
        'grid.alpha': 0.3,
        
        # Export quality
        'figure.dpi': 200,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.format': 'pdf',
        
        # Font embedding for PDF
        'pdf.fonttype': 42,
        'ps.fonttype': 42
    }
    
    # Add grayscale-specific settings if enabled
    if grayscale_mode or 'grayscale' in profile:
        grayscale_config = {
            # Enhanced contrast for B&W
            'axes.linewidth': 1.0,
            'lines.linewidth': 2.0,
            'lines.markeredgewidth': 1.0,
            'grid.alpha': 0.5,
            'grid.color': '#808080',
            
            # Pattern support
            'hatch.linewidth': 0.5,
            'hatch.color': 'black',
            
            # High contrast elements
            'axes.edgecolor': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'text.color': 'black'
        }
        base_config.update(grayscale_config)
    
    plt.rcParams.update(base_config)
    
    if show_info:
        print(f"🎯 Discernus Typography: {profile.upper()}")
        print(f"📝 {config['description']}")
        print(f"🔤 Font: {config['font_family'][0]}")
        print(f"📏 Sizes: Title({config['title']}pt), Label({config['label']}pt), Tick({config['tick']}pt)")
        print("="*50)

def demonstrate_typography_profiles():
    """Demonstrate all typography profiles side by side"""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    profiles = ['discernus', 'nature', 'science', 'pnas']
    
    for i, profile in enumerate(profiles):
        ax = axes[i//2, i%2]
        
        # Temporarily apply profile
        setup_style(profile, show_info=False)
        
        # Generate sample data
        np.random.seed(42)
        x = np.linspace(0, 10, 50)
        y1 = np.sin(x) + np.random.normal(0, 0.1, 50)
        y2 = np.cos(x) + np.random.normal(0, 0.1, 50)
        
        # Create plot demonstrating typography
        ax.plot(x, y1, label='Series A', linewidth=2)
        ax.plot(x, y2, label='Series B', linewidth=2)
        
        # Typography demonstration
        ax.set_title(f'{profile.upper()} Profile', fontweight='bold')
        ax.set_xlabel('X-axis Label')
        ax.set_ylabel('Y-axis Label')
        ax.legend(frameon=False)
        ax.grid(True, alpha=0.3)
        
        # Add typography info annotation
        config = TYPOGRAPHY_PROFILES[profile]
        info_text = f"Title: {config['title']}pt\nLabel: {config['label']}pt\nTick: {config['tick']}pt"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               fontsize=config['tick'], verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.suptitle('Discernus Typography System: Distinctive + Compliant', 
                fontsize=14, fontweight='bold', y=0.98)
    
    return fig

def font_installation_guide():
    """Provide guidance for installing optimal Discernus fonts"""
    
    print("📁 DISCERNUS FONT INSTALLATION GUIDE")
    print("="*50)
    
    status = check_font_availability()
    
    for category, fonts in status.items():
        print(f"\n{category.upper()} FONTS:")
        for font in fonts:
            print(f"  {font}")
    
    print("\n💡 INSTALLATION RECOMMENDATIONS:")
    print("1. Inter: Download from https://rsms.me/inter/ (PRIMARY CHOICE)")
    print("2. JetBrains Mono: Download from https://jetbrains.com/mono/")
    print("3. Source Sans Pro: Download from Adobe Fonts or Google Fonts")
    print("\n🎯 Fallback Strategy:")
    print("- Discernus automatically falls back to Arial/Helvetica")
    print("- All profiles maintain visual consistency")
    print("- Journal compliance guaranteed regardless of font availability")

def create_typography_comparison():
    """Create a detailed comparison showing distinctive vs compliant styling"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sample data
    categories = ['Populism', 'Pluralism', 'Nationalism', 'Patriotism']
    values = [0.8, 0.4, 0.9, 0.6]
    
    # Left panel: Discernus distinctive style
    setup_style('discernus', show_info=False)
    bars1 = ax1.bar(categories, values, color=['#4477AA', '#66CCEE', '#228833', '#CCBB44'])
    ax1.set_title('Discernus Identity Style', fontweight='bold')
    ax1.set_ylabel('Intensity Score')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add size annotations
    ax1.text(0.02, 0.98, 'Large, readable text\nDistinctive identity\nInter (UI-optimized)', 
            transform=ax1.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.8))
    
    # Right panel: Academic compliance style
    setup_style('nature', show_info=False)
    bars2 = ax2.bar(categories, values, color=['#4477AA', '#66CCEE', '#228833', '#CCBB44'])
    ax2.set_title('Nature Journal Compliance', fontweight='bold')
    ax2.set_ylabel('Intensity Score')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add size annotations
    ax2.text(0.02, 0.98, 'Compact text (5-7pt)\nJournal compliant\nArial/Helvetica', 
            transform=ax2.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    fig.suptitle('Typography Strategy: Same Code, Different Contexts', 
                fontsize=14, fontweight='bold', y=0.98)
    
    return fig

if __name__ == "__main__":
    print("🎯 DISCERNUS TYPOGRAPHY SYSTEM")
    print("Distinctive Identity + Academic Compliance")
    print("="*50)
    
    # Check font availability
    font_installation_guide()
    
    print("\n📊 DEMONSTRATION:")
    
    # Show all profiles
    fig1 = demonstrate_typography_profiles()
    fig1.savefig('discernus_typography_profiles.pdf', dpi=300, bbox_inches='tight')
    
    # Show comparison
    fig2 = create_typography_comparison()
    fig2.savefig('discernus_typography_comparison.pdf', dpi=300, bbox_inches='tight')
    
    plt.show()
    
    print("\n✅ Files saved:")
    print("📁 discernus_typography_profiles.pdf")  
    print("📁 discernus_typography_comparison.pdf")
    print("\n🎯 This system gives you BOTH distinctive identity AND compliance!") 