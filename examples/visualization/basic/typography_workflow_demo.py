#!/usr/bin/env python3
"""
Typography Workflow Demo: "Having Your Cake and Eating It Too"

Shows how Discernus researchers can use distinctive styling by default
but switch to journal compliance with a single line change.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discernus.visualization.discernus_typography import setup_style

# Simple convenience functions
def discernus_style():
    setup_style('discernus')

def nature_style():
    setup_style('nature')

def science_style():
    setup_style('science')

def create_sample_analysis():
    """Create a sample political discourse analysis figure"""
    
    # Generate realistic data
    np.random.seed(42)
    phases = ['Early\nCampaign', 'Mid\nCampaign', 'Final\nPush']
    populism_scores = [0.7, 0.85, 0.95]
    pluralism_scores = [0.8, 0.6, 0.3]
    errors = [0.05, 0.08, 0.06]
    
    x = np.arange(len(phases))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    bars1 = ax.bar(x - width/2, populism_scores, width, 
                   label='Populism', color='#4477AA', alpha=0.8)
    bars2 = ax.bar(x + width/2, pluralism_scores, width,
                   label='Pluralism', color='#228833', alpha=0.8)
    
    # Add error bars
    ax.errorbar(x - width/2, populism_scores, yerr=errors, 
                fmt='none', color='black', capsize=5)
    ax.errorbar(x + width/2, pluralism_scores, yerr=errors,
                fmt='none', color='black', capsize=5)
    
    ax.set_xlabel('Campaign Phase')
    ax.set_ylabel('Discourse Intensity Score')
    ax.set_title('Bolsonaro 2018: Democratic Tension Analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(phases)
    ax.legend(frameon=False)
    ax.set_ylim(0, 1.1)
    
    # Add significance annotation
    ax.annotate('***', xy=(2, 0.95), xytext=(2, 1.02),
                ha='center', va='center', fontweight='bold',
                arrowprops=dict(arrowstyle='-', lw=1))
    ax.text(2, 1.05, 'p < 0.001', ha='center', va='center')
    
    return fig

def demonstrate_workflow():
    """Show the complete workflow from distinctive to compliant"""
    
    print("🎯 DISCERNUS TYPOGRAPHY WORKFLOW")
    print("="*50)
    print("Same code, different contexts!")
    print()
    
    # Step 1: Default Discernus Style
    print("📝 STEP 1: Default Research & Presentation Mode")
    discernus_style()
    fig1 = create_sample_analysis()
    fig1.suptitle('Research Mode: Distinctive Discernus Identity', 
                  fontsize=14, fontweight='bold')
    fig1.savefig('research_mode.pdf', dpi=300, bbox_inches='tight')
    print("✅ Saved: research_mode.pdf (Inter, readable sizes)")
    
    # Step 2: Nature Journal Submission
    print("\n📝 STEP 2: Nature Journal Submission")
    print("   # Just change ONE line:")
    print("   # discernus_style() → nature_style()")
    nature_style()
    fig2 = create_sample_analysis()
    fig2.suptitle('Nature Submission: Journal Compliant', 
                  fontsize=7, fontweight='bold')  # Note smaller title
    fig2.savefig('nature_submission.pdf', dpi=300, bbox_inches='tight')
    print("✅ Saved: nature_submission.pdf (Arial, 5-7pt, Nature compliant)")
    
    # Step 3: Science Journal Alternative
    print("\n📝 STEP 3: Science Journal Alternative")
    print("   # Or switch to Science requirements:")
    print("   # nature_style() → science_style()")
    science_style()
    fig3 = create_sample_analysis()
    fig3.suptitle('Science Submission: Journal Compliant', 
                  fontsize=8, fontweight='bold')
    fig3.savefig('science_submission.pdf', dpi=300, bbox_inches='tight')
    print("✅ Saved: science_submission.pdf (Arial, 6-8pt, Science compliant)")
    
    plt.show()
    
    print("\n🎯 WORKFLOW COMPLETE!")
    print("="*50)
    print("✨ You just had your cake AND ate it too!")
    print()
    print("📁 Three identical analyses, three compliance levels:")
    print("   • research_mode.pdf - Distinctive & readable")
    print("   • nature_submission.pdf - Nature journal ready")  
    print("   • science_submission.pdf - Science journal ready")
    print()
    print("🔄 Same code, zero refactoring needed!")
    print("🎨 Maintains Discernus visual identity in research")
    print("📊 Instant compliance for journal submission")

if __name__ == "__main__":
    demonstrate_workflow() 