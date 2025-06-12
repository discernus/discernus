#!/usr/bin/env python3
"""
Side-by-side comparison: Old spread-out positioning vs New clustered positioning
Demonstrates the visual impact of proper integrative/disintegrative clustering
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular
import numpy as np
import matplotlib.pyplot as plt

def create_clustered_comparison():
    """Create side-by-side comparison of old vs new positioning"""
    
    print("📊 CLUSTERED POSITIONING COMPARISON")
    print("=" * 50)
    
    # Create side-by-side subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # --- LEFT PLOT: OLD SPREAD-OUT POSITIONING ---
    ax1.set_aspect('equal')
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    
    # Draw circle
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax1.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # OLD positioning (spread-out)
    old_wells = {
        # Integrative - SPREAD OUT (20°-160° = 140° span!)
        'Dignity': {'angle': 90, 'type': 'integrative'},
        'Truth': {'angle': 45, 'type': 'integrative'},
        'Justice': {'angle': 135, 'type': 'integrative'},
        'Hope': {'angle': 20, 'type': 'integrative'},
        'Pragmatism': {'angle': 160, 'type': 'integrative'},
        # Disintegrative - SPREAD OUT (200°-340° = 140° span!)
        'Tribalism': {'angle': 270, 'type': 'disintegrative'},
        'Manipulation': {'angle': 315, 'type': 'disintegrative'},
        'Resentment': {'angle': 225, 'type': 'disintegrative'},
        'Fantasy': {'angle': 340, 'type': 'disintegrative'},
        'Fear': {'angle': 200, 'type': 'disintegrative'}
    }
    
    integrative_angles_old = []
    disintegrative_angles_old = []
    
    for well_name, well_config in old_wells.items():
        angle = well_config['angle']
        well_type = well_config['type']
        
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        if well_type == 'integrative':
            color = '#2E7D32'
            integrative_angles_old.append(angle)
            ax1.scatter(x, y, c=color, s=120, alpha=0.8, edgecolors='darkgreen', linewidth=2)
        else:
            color = '#C62828'
            disintegrative_angles_old.append(angle)
            ax1.scatter(x, y, c=color, s=120, alpha=0.8, edgecolors='darkred', linewidth=2)
        
        # Add labels
        ax1.annotate(well_name, (x, y), xytext=(5, 5), textcoords='offset points', 
                    fontsize=9, fontweight='bold')
    
    # --- RIGHT PLOT: NEW CLUSTERED POSITIONING ---
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.3, 1.3)
    ax2.set_ylim(-1.3, 1.3)
    ax2.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # Load the current (clustered) framework
    engine = NarrativeGravityWellsCircular()
    engine.config_dir = "frameworks/civic_virtue"
    engine._load_framework_config()
    
    integrative_angles_new = []
    disintegrative_angles_new = []
    
    for well_name, well_config in engine.well_definitions.items():
        angle = well_config['angle']
        well_type = well_config['type']
        
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        if well_type == 'integrative':
            color = '#2E7D32'
            integrative_angles_new.append(angle)
            ax2.scatter(x, y, c=color, s=120, alpha=0.8, edgecolors='darkgreen', linewidth=2)
        else:
            color = '#C62828'
            disintegrative_angles_new.append(angle)
            ax2.scatter(x, y, c=color, s=120, alpha=0.8, edgecolors='darkred', linewidth=2)
        
        # Add labels
        ax2.annotate(well_name, (x, y), xytext=(5, 5), textcoords='offset points', 
                    fontsize=9, fontweight='bold')
    
    # Add clustering zones (visual emphasis)
    # Old plot - wide spread zones
    integrative_span_old = max(integrative_angles_old) - min(integrative_angles_old)
    disintegrative_span_old = max(disintegrative_angles_old) - min(disintegrative_angles_old)
    
    # New plot - tight clusters
    integrative_span_new = max(integrative_angles_new) - min(integrative_angles_new)
    disintegrative_span_new = max(disintegrative_angles_new) - min(disintegrative_angles_new)
    
    # Add hemisphere labels
    ax1.text(0, 1.1, 'INTEGRATIVE\n(Civic Virtue)', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='darkgreen')
    ax1.text(0, -1.1, 'DISINTEGRATIVE\n(Rhetorical Forces)', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkred')
    
    ax2.text(0, 1.1, 'INTEGRATIVE\n(Civic Virtue)', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='darkgreen')
    ax2.text(0, -1.1, 'DISINTEGRATIVE\n(Rhetorical Forces)', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkred')
    
    # Titles and metrics
    ax1.set_title(f'❌ OLD: Spread-Out Positioning\n' + 
                 f'Integrative span: {integrative_span_old}°\n' +
                 f'Disintegrative span: {disintegrative_span_old}°\n' +
                 f'(Looks like neutral political compass)', 
                 fontsize=12, fontweight='bold', color='darkred')
    
    ax2.set_title(f'✅ NEW: Clustered Positioning\n' + 
                 f'Integrative span: {integrative_span_new}°\n' +
                 f'Disintegrative span: {disintegrative_span_new}°\n' +
                 f'(Clear moral hierarchy)', 
                 fontsize=12, fontweight='bold', color='darkgreen')
    
    # Remove axes
    for ax in [ax1, ax2]:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    
    # Overall title
    fig.suptitle('Civic Virtue Framework: Clustering Impact on Visual Rhetoric\n' +
                'Framework Developer Controls Angle Positioning for Normative Emphasis', 
                fontsize=16, fontweight='bold', y=0.95)
    
    # Add improvement metrics
    improvement_text = (
        f"CLUSTERING IMPROVEMENT:\n"
        f"• Integrative: {integrative_span_old}° → {integrative_span_new}° "
        f"({((integrative_span_old - integrative_span_new) / integrative_span_old * 100):.0f}% tighter)\n"
        f"• Disintegrative: {disintegrative_span_old}° → {disintegrative_span_new}° "
        f"({((disintegrative_span_old - disintegrative_span_new) / disintegrative_span_old * 100):.0f}% tighter)\n"
        f"• Visual Impact: Clear moral hierarchy vs neutral distribution"
    )
    
    fig.text(0.5, 0.02, improvement_text, ha='center', va='bottom', 
            fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85, bottom=0.15)
    
    # Save visualization
    output_path = 'cv_clustering_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # Summary statistics
    print("\n📈 CLUSTERING IMPROVEMENT METRICS:")
    print("-" * 40)
    print(f"OLD POSITIONING (Spread-Out):")
    print(f"  • Integrative span: {integrative_span_old}° (too wide)")
    print(f"  • Disintegrative span: {disintegrative_span_old}° (too wide)")
    print(f"  • Visual effect: Neutral political compass")
    
    print(f"\nNEW POSITIONING (Clustered):")
    print(f"  • Integrative span: {integrative_span_new}° (tight cluster)")
    print(f"  • Disintegrative span: {disintegrative_span_new}° (tight cluster)")
    print(f"  • Visual effect: Clear moral hierarchy")
    
    print(f"\nIMPROVEMENT:")
    print(f"  • Integrative: {((integrative_span_old - integrative_span_new) / integrative_span_old * 100):.0f}% tighter")
    print(f"  • Disintegrative: {((disintegrative_span_old - disintegrative_span_new) / disintegrative_span_old * 100):.0f}% tighter")
    print(f"  • Framework intent: ✅ PRESERVED")
    
    print(f"\n💾 Comparison saved to: {output_path}")
    print("✅ CLUSTERED POSITIONING SUCCESSFULLY IMPLEMENTED!")
    
    return output_path

if __name__ == "__main__":
    create_clustered_comparison() 