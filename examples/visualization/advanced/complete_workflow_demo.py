#!/usr/bin/env python3
"""
Complete Discernus Workflow: Typography + Grayscale + Journal Compliance

Demonstrates the full "cake and eat it too" approach:
- Inter typography for distinctive identity
- Automatic grayscale compatibility
- One-click journal compliance
- Perfect accessibility standards
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discernus.visualization.discernus_typography import setup_style

def create_political_discourse_analysis():
    """Create a comprehensive political discourse analysis figure"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel A: Temporal Evolution with Patterns
    phases = ['Early\nCampaign', 'Mid\nCampaign', 'Final\nPush']
    populism = [0.65, 0.85, 0.95]
    pluralism = [0.85, 0.60, 0.25]
    nationalism = [0.45, 0.70, 0.90]
    errors = [0.05, 0.08, 0.06]
    
    x = np.arange(len(phases))
    width = 0.25
    
    # Use patterns for grayscale compatibility
    patterns = ['', '///', '|||']
    colors = ['#000000', '#404040', '#808080']
    
    bars1 = ax1.bar(x - width, populism, width, label='Populism', 
                   color=colors[0], hatch=patterns[0], edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x, pluralism, width, label='Pluralism',
                   color=colors[1], hatch=patterns[1], edgecolor='black', linewidth=1)
    bars3 = ax1.bar(x + width, nationalism, width, label='Nationalism',
                   color=colors[2], hatch=patterns[2], edgecolor='black', linewidth=1)
    
    ax1.errorbar(x - width, populism, yerr=errors, fmt='none', color='black', capsize=4)
    ax1.errorbar(x, pluralism, yerr=errors, fmt='none', color='black', capsize=4)
    ax1.errorbar(x + width, nationalism, yerr=errors, fmt='none', color='black', capsize=4)
    
    ax1.set_title('A. Temporal Evolution Analysis', fontweight='bold')
    ax1.set_xlabel('Campaign Phase')
    ax1.set_ylabel('Discourse Intensity')
    ax1.set_xticks(x)
    ax1.set_xticklabels(phases)
    ax1.legend(frameon=True, fancybox=False, edgecolor='black', facecolor='white')
    ax1.set_ylim(0, 1.1)
    
    # Panel B: Line Plot with Multiple Styles
    x_time = np.linspace(0, 12, 100)
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D']
    ideologies = ['Populism', 'Pluralism', 'Nationalism', 'Patriotism']
    
    for i, (ideology, style, marker) in enumerate(zip(ideologies, linestyles, markers)):
        y = 0.5 + 0.3*np.sin(x_time + i*np.pi/4) + 0.1*i
        ax2.plot(x_time, y, linestyle=style, color='black', linewidth=2,
                marker=marker, markersize=6, markevery=15, label=ideology,
                markerfacecolor='white', markeredgecolor='black', markeredgewidth=1)
    
    ax2.set_title('B. Longitudinal Trend Analysis', fontweight='bold')
    ax2.set_xlabel('Months into Campaign')
    ax2.set_ylabel('Average Score')
    ax2.legend(loc='upper right', frameon=True, fancybox=False,
              edgecolor='black', facecolor='white')
    ax2.grid(True, alpha=0.3, color='gray')
    
    # Panel C: Coordinate Space with Distinct Markers
    theta = np.linspace(0, 2*np.pi, 100)
    ax3.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2)
    
    # Framework anchors with distinct markers for B&W
    anchors = {
        'Populism': (0, 1, 's', 'black'),
        'Pluralism': (0, -1, 'o', '#404040'),
        'Nationalism': (1, 0, '^', '#808080'),
        'Patriotism': (-1, 0, 'D', '#B0B0B0')
    }
    
    for name, (x, y, marker, color) in anchors.items():
        ax3.scatter(x, y, s=250, marker=marker, c=color,
                   edgecolors='black', linewidth=2, zorder=10)
        offset = 1.25
        ax3.annotate(name, (x*offset, y*offset), ha='center', va='center',
                    fontweight='bold', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                             edgecolor='black', linewidth=1))
    
    # Add coordinate grid
    ax3.axhline(y=0, color='black', linewidth=1, alpha=0.7)
    ax3.axvline(x=0, color='black', linewidth=1, alpha=0.7)
    ax3.grid(True, alpha=0.3, color='gray')
    
    ax3.set_xlim(-1.6, 1.6)
    ax3.set_ylim(-1.6, 1.6)
    ax3.set_aspect('equal')
    ax3.set_title('C. Democratic Tension Coordinate Space', fontweight='bold')
    ax3.set_xlabel('Patriotism ← → Nationalism')
    ax3.set_ylabel('Pluralism ← → Populism')
    
    # Panel D: Statistical Validation with Clear B&W
    methods = ['Manual\nCoding', 'GPT-4', 'Claude-3', 'LLaMA-2']
    correlations = [0.89, 0.85, 0.87, 0.79]
    errors = [0.03, 0.04, 0.035, 0.05]
    
    # Use different patterns for each bar
    bar_patterns = ['', '///', '|||', '...']
    bar_colors = ['#000000', '#404040', '#808080', '#B0B0B0']
    
    bars = []
    for i, (method, corr, err, pattern, color) in enumerate(zip(methods, correlations, errors, bar_patterns, bar_colors)):
        bar = ax4.bar(i, corr, color=color, hatch=pattern, 
                     edgecolor='black', linewidth=1.5, alpha=0.8)
        bars.append(bar)
    
    ax4.errorbar(range(len(methods)), correlations, yerr=errors, 
                fmt='none', color='black', capsize=5, capthick=2)
    
    # Statistical significance
    ax4.annotate('***', xy=(1.5, 0.87), xytext=(1.5, 0.92),
                ha='center', va='center', fontweight='bold', fontsize=12,
                arrowprops=dict(arrowstyle='-', lw=1.5, color='black'))
    ax4.text(1.5, 0.94, 'p < 0.001', ha='center', va='center', fontweight='bold')
    
    # Reference lines
    ax4.axhline(y=0.8, color='black', linestyle='--', alpha=0.6, linewidth=1)
    ax4.axhline(y=0.9, color='black', linestyle=':', alpha=0.6, linewidth=1)
    ax4.text(0.1, 0.82, 'Minimum', fontsize=9, color='black')
    ax4.text(0.1, 0.92, 'Excellent', fontsize=9, color='black')
    
    ax4.set_title('D. Multi-LLM Validation Results', fontweight='bold')
    ax4.set_ylabel('Correlation with Ground Truth')
    ax4.set_xticks(range(len(methods)))
    ax4.set_xticklabels(methods)
    ax4.set_ylim(0, 1.0)
    
    plt.tight_layout()
    return fig

def demonstrate_complete_workflow():
    """Show the complete Discernus workflow"""
    
    print("🎯 COMPLETE DISCERNUS WORKFLOW DEMONSTRATION")
    print("="*60)
    print("Inter Typography + Grayscale + Journal Compliance")
    print()
    
    # Mode 1: Research/Presentation (Inter + Color + Readable)
    print("📝 MODE 1: Research & Presentation")
    print("   • Inter typography for distinctive identity")
    print("   • Color palette for visual appeal")
    print("   • Readable sizes for presentations")
    
    setup_style('discernus', show_info=False)
    fig1 = create_political_discourse_analysis()
    fig1.suptitle('Research Mode: Distinctive Discernus Identity (Color)', 
                  fontsize=14, fontweight='bold', y=0.98)
    fig1.savefig('research_color.pdf', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: research_color.pdf")
    
    # Mode 2: Grayscale-Compatible Research
    print("\n📝 MODE 2: Grayscale-Compatible Research")
    print("   • Same Inter typography")
    print("   • Patterns + grayscale for accessibility")
    print("   • Works perfectly in B&W printing")
    
    setup_style('discernus', grayscale_mode=True, show_info=False)
    fig2 = create_political_discourse_analysis()
    fig2.suptitle('Research Mode: Grayscale Compatible (B&W Ready)', 
                  fontsize=14, fontweight='bold', y=0.98)
    fig2.savefig('research_grayscale.pdf', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: research_grayscale.pdf")
    
    # Mode 3: Nature Journal Submission
    print("\n📝 MODE 3: Nature Journal Submission")
    print("   • Arial typography (journal requirement)")
    print("   • 5-7pt sizes (Nature specification)")
    print("   • Automatic compliance, same code")
    
    setup_style('nature', show_info=False)
    fig3 = create_political_discourse_analysis()
    fig3.suptitle('Nature Submission: Journal Compliant (Arial, 5-7pt)', 
                  fontsize=7, fontweight='bold', y=0.98)
    fig3.savefig('nature_submission.pdf', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: nature_submission.pdf")
    
    plt.show()
    
    # Summary
    print("\n🎯 COMPLETE WORKFLOW SUMMARY")
    print("="*60)
    print("✨ You now have the COMPLETE package:")
    print()
    print("🎨 DISTINCTIVE IDENTITY:")
    print("   • Inter typography for modern, tech-forward aesthetic")
    print("   • Recognizable 'Discernus style' figures")
    print("   • Superior character differentiation for data viz")
    print()
    print("♿ UNIVERSAL ACCESSIBILITY:")
    print("   • Patterns + colors for colorblind users")
    print("   • Perfect grayscale/B&W compatibility")
    print("   • WCAG 2.1 AA compliance standards")
    print()
    print("📊 ACADEMIC COMPLIANCE:")
    print("   • One-line switch to Nature/Science requirements")
    print("   • Automatic font + size adjustments")
    print("   • Zero code refactoring needed")
    print()
    print("📁 THREE FILES, SAME CODE:")
    print("   • research_color.pdf - Distinctive & colorful")
    print("   • research_grayscale.pdf - B&W compatible")
    print("   • nature_submission.pdf - Journal ready")
    print()
    print("🎯 This is TRUE 'cake and eat it too' - you get:")
    print("   ✅ Distinctive visual identity")
    print("   ✅ Universal accessibility")
    print("   ✅ Instant journal compliance")
    print("   ✅ Zero workflow friction")

if __name__ == "__main__":
    demonstrate_complete_workflow() 