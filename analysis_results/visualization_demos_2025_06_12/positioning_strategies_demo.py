#!/usr/bin/env python3
"""
Comprehensive demo of all positioning strategies for framework developers
Shows: Clustered Dipoles, Individual Angles, Even Distribution, Custom Clusters
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular
import numpy as np
import matplotlib.pyplot as plt
import json

def demo_all_positioning_strategies():
    """Demonstrate all positioning strategies with visual comparison"""
    
    print("🎯 POSITIONING STRATEGIES DEMO - Framework Developer Options")
    print("=" * 70)
    
    # Create 2x2 subplot grid
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    
    # Strategy 1: Clustered Dipoles (Current CV Framework)
    demo_clustered_dipoles(ax1)
    
    # Strategy 2: Individual Angles (Maximum Control)
    demo_individual_angles(ax2)
    
    # Strategy 3: Even Distribution (Neutral/Descriptive)
    demo_even_distribution(ax3)
    
    # Strategy 4: Custom Clusters (Horizontal Political)
    demo_custom_clusters(ax4)
    
    # Overall title
    fig.suptitle('Framework Developer Positioning Strategy Options\n' +
                'Choose Based on Theoretical Goals and Visual Rhetoric Needs', 
                fontsize=18, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.3, wspace=0.3)
    
    # Save demonstration
    output_path = 'positioning_strategies_demo.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print(f"\n💾 Positioning strategies demo saved to: {output_path}")
    print("✅ ALL POSITIONING STRATEGIES DEMONSTRATED!")
    
    return output_path

def demo_clustered_dipoles(ax):
    """Demo Strategy 1: Clustered Dipoles (Normative Frameworks)"""
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    
    # Draw circle
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # Load current CV framework (clustered)
    engine = NarrativeGravityWellsCircular()
    engine.config_dir = "frameworks/civic_virtue"
    engine._load_framework_config()
    
    # Plot wells
    integrative_angles = []
    disintegrative_angles = []
    
    for well_name, well_config in engine.well_definitions.items():
        angle = well_config['angle']
        well_type = well_config['type']
        
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        if well_type == 'integrative':
            color = '#2E7D32'
            integrative_angles.append(angle)
            ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='darkgreen', linewidth=2)
        else:
            color = '#C62828'
            disintegrative_angles.append(angle)
            ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='darkred', linewidth=2)
        
        ax.annotate(well_name, (x, y), xytext=(3, 3), textcoords='offset points', fontsize=8)
    
    # Add clustering metrics
    integrative_span = max(integrative_angles) - min(integrative_angles)
    disintegrative_span = max(disintegrative_angles) - min(disintegrative_angles)
    
    ax.set_title(f'Strategy 1: Clustered Dipoles\n' +
                f'(Civic Virtue Framework)\n' +
                f'Integrative: {integrative_span}° span\n' +
                f'Disintegrative: {disintegrative_span}° span\n' +
                f'Use: Normative moral hierarchy', 
                fontsize=10, fontweight='bold')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

def demo_individual_angles(ax):
    """Demo Strategy 2: Individual Angles (Maximum Control)"""
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    
    # Draw circle
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # Example: Custom research framework with precise positioning
    custom_wells = {
        'Primary_Force': {'angle': 30, 'type': 'integrative', 'weight': 1.0},
        'Supporting_Element': {'angle': 75, 'type': 'integrative', 'weight': 0.8},
        'Balancing_Factor': {'angle': 150, 'type': 'integrative', 'weight': 0.6},
        'Opposition_A': {'angle': 210, 'type': 'disintegrative', 'weight': -1.0},
        'Opposition_B': {'angle': 270, 'type': 'disintegrative', 'weight': -0.8},
        'Weak_Counter': {'angle': 330, 'type': 'disintegrative', 'weight': -0.4}
    }
    
    for well_name, well_config in custom_wells.items():
        angle = well_config['angle']
        well_type = well_config['type']
        
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        if well_type == 'integrative':
            color = '#1976D2'
            ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='navy', linewidth=2)
        else:
            color = '#D32F2F'
            ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='darkred', linewidth=2)
        
        # Show exact angles
        ax.annotate(f'{well_name}\n({angle}°)', (x, y), xytext=(3, 3), 
                   textcoords='offset points', fontsize=7, ha='left')
    
    ax.set_title('Strategy 2: Individual Angles\n' +
                '(Maximum Control)\n' +
                'Framework developer specifies\n' +
                'exact angle for each well\n' +
                'Use: Precise theoretical needs', 
                fontsize=10, fontweight='bold')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

def demo_even_distribution(ax):
    """Demo Strategy 3: Even Distribution (Neutral/Descriptive)"""
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    
    # Draw circle
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # Example: 8 moral foundations evenly distributed
    foundations = ['Care', 'Fairness', 'Loyalty', 'Authority', 'Sanctity', 'Liberty', 'Oppression', 'Harm']
    num_wells = len(foundations)
    angle_step = 360 / num_wells
    
    for i, foundation in enumerate(foundations):
        angle = i * angle_step
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        # Use neutral colors for descriptive framework
        color = '#757575'
        ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='black', linewidth=2)
        ax.annotate(f'{foundation}\n({angle:.0f}°)', (x, y), xytext=(3, 3), 
                   textcoords='offset points', fontsize=7, ha='left')
    
    ax.set_title('Strategy 3: Even Distribution\n' +
                '(Moral Foundations Style)\n' +
                'Wells evenly spaced around circle\n' +
                'No visual hierarchy implied\n' +
                'Use: Descriptive frameworks', 
                fontsize=10, fontweight='bold')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

def demo_custom_clusters(ax):
    """Demo Strategy 4: Custom Clusters (Non-vertical emphasis)"""
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    
    # Draw circle
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.3)
    
    # Example: Left-Right Political Framework (horizontal clustering)
    left_wells = [
        ('Progressive', 160),
        ('Equality', 170),
        ('Reform', 180),
        ('Social_Justice', 190),
        ('Cooperation', 200)
    ]
    
    right_wells = [
        ('Conservative', 340),
        ('Tradition', 350),
        ('Order', 0),
        ('Individual', 10),
        ('Competition', 20)
    ]
    
    # Plot left cluster (progressive)
    for well_name, angle in left_wells:
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        ax.scatter(x, y, c='#1E88E5', s=100, alpha=0.8, edgecolors='navy', linewidth=2)
        ax.annotate(well_name, (x, y), xytext=(3, 3), textcoords='offset points', fontsize=7)
    
    # Plot right cluster (conservative)
    for well_name, angle in right_wells:
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        ax.scatter(x, y, c='#E53935', s=100, alpha=0.8, edgecolors='darkred', linewidth=2)
        ax.annotate(well_name, (x, y), xytext=(3, 3), textcoords='offset points', fontsize=7)
    
    # Add cluster labels
    ax.text(-1.0, 0, 'LEFT\nCLUSTER', ha='center', va='center', fontsize=10, 
           fontweight='bold', color='blue')
    ax.text(1.0, 0, 'RIGHT\nCLUSTER', ha='center', va='center', fontsize=10, 
           fontweight='bold', color='red')
    
    ax.set_title('Strategy 4: Custom Clusters\n' +
                '(Political Left-Right)\n' +
                'Horizontal clustering for\n' +
                'left-right political emphasis\n' +
                'Use: Non-vertical frameworks', 
                fontsize=10, fontweight='bold')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

if __name__ == "__main__":
    demo_all_positioning_strategies() 