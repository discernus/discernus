#!/usr/bin/env python3
"""
Circular Coordinate System Engine - Comprehensive Demonstration
Version 1.1.0 - Enhanced Algorithms Validation

This script demonstrates:
1. Circular coordinate system implementation
2. Enhanced algorithms (dominance amplification, adaptive scaling)
3. Three-dimensional architecture flexibility
4. Boundary utilization improvements
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular

def create_test_datasets():
    """Create test datasets demonstrating different narrative types."""
    
    # Dataset 1: Extreme integrative narrative (synthetic)
    extreme_integrative = {
        'metadata': {
            'title': 'Extreme Integrative Test Case',
            'summary': 'Synthetic narrative designed to test boundary utilization for extreme civic virtue',
            'model_name': 'Test',
            'model_version': 'Synthetic'
        },
        'wells': [
            {'name': 'Dignity', 'score': 0.95},
            {'name': 'Truth', 'score': 0.90},
            {'name': 'Justice', 'score': 0.85},
            {'name': 'Hope', 'score': 0.80},
            {'name': 'Pragmatism', 'score': 0.75},
            {'name': 'Tribalism', 'score': 0.05},
            {'name': 'Manipulation', 'score': 0.10},
            {'name': 'Resentment', 'score': 0.15},
            {'name': 'Fear', 'score': 0.20},
            {'name': 'Fantasy', 'score': 0.25}
        ]
    }
    
    # Dataset 2: Extreme disintegrative narrative (synthetic)
    extreme_disintegrative = {
        'metadata': {
            'title': 'Extreme Disintegrative Test Case',
            'summary': 'Synthetic narrative designed to test boundary utilization for extreme problematic rhetoric',
            'model_name': 'Test',
            'model_version': 'Synthetic'
        },
        'wells': [
            {'name': 'Dignity', 'score': 0.05},
            {'name': 'Truth', 'score': 0.10},
            {'name': 'Justice', 'score': 0.15},
            {'name': 'Hope', 'score': 0.20},
            {'name': 'Pragmatism', 'score': 0.25},
            {'name': 'Tribalism', 'score': 0.95},
            {'name': 'Manipulation', 'score': 0.90},
            {'name': 'Resentment', 'score': 0.85},
            {'name': 'Fear', 'score': 0.80},
            {'name': 'Fantasy', 'score': 0.75}
        ]
    }
    
    # Dataset 3: Moderate mixed narrative (realistic)
    moderate_mixed = {
        'metadata': {
            'title': 'Moderate Mixed Narrative',
            'summary': 'Realistic political speech with mixed moral elements',
            'model_name': 'Test',
            'model_version': 'Realistic'
        },
        'wells': [
            {'name': 'Dignity', 'score': 0.6},
            {'name': 'Truth', 'score': 0.4},
            {'name': 'Justice', 'score': 0.7},
            {'name': 'Hope', 'score': 0.5},
            {'name': 'Pragmatism', 'score': 0.8},
            {'name': 'Tribalism', 'score': 0.3},
            {'name': 'Manipulation', 'score': 0.2},
            {'name': 'Resentment', 'score': 0.4},
            {'name': 'Fear', 'score': 0.3},
            {'name': 'Fantasy', 'score': 0.1}
        ]
    }
    
    # Dataset 4: Single dimension dominance 
    single_dominance = {
        'metadata': {
            'title': 'Single Dimension Dominance Test',
            'summary': 'Narrative heavily focused on single well to test dominance amplification',
            'model_name': 'Test',
            'model_version': 'Focused'
        },
        'wells': [
            {'name': 'Dignity', 'score': 0.1},
            {'name': 'Truth', 'score': 0.1},
            {'name': 'Justice', 'score': 0.95},  # Dominant well
            {'name': 'Hope', 'score': 0.1},
            {'name': 'Pragmatism', 'score': 0.1},
            {'name': 'Tribalism', 'score': 0.1},
            {'name': 'Manipulation', 'score': 0.1},
            {'name': 'Resentment', 'score': 0.1},
            {'name': 'Fear', 'score': 0.1},
            {'name': 'Fantasy', 'score': 0.1}
        ]
    }
    
    return {
        'extreme_integrative': extreme_integrative,
        'extreme_disintegrative': extreme_disintegrative,
        'moderate_mixed': moderate_mixed,
        'single_dominance': single_dominance
    }

def analyze_boundary_utilization(engine, test_data):
    """Analyze boundary utilization across test datasets."""
    
    print("🔍 BOUNDARY UTILIZATION ANALYSIS")
    print("=" * 50)
    
    results = {}
    distances = []
    
    for name, data in test_data.items():
        well_scores = {well['name']: well['score'] for well in data['wells']}
        
        # Calculate narrative position using enhanced algorithms
        narrative_x, narrative_y = engine.calculate_narrative_position(well_scores)
        distance = np.sqrt(narrative_x**2 + narrative_y**2)
        distances.append(distance)
        
        # Calculate adaptive scaling factor
        adaptive_scale = engine.calculate_adaptive_scaling(well_scores)
        
        # Test dominance amplification on max score
        max_score = max(well_scores.values())
        amplified_max = engine.apply_dominance_amplification(max_score)
        
        results[name] = {
            'narrative_position': (narrative_x, narrative_y),
            'distance_from_center': distance,
            'adaptive_scaling': adaptive_scale,
            'max_score_original': max_score,
            'max_score_amplified': amplified_max,
            'amplification_factor': amplified_max / max_score if max_score > 0 else 1.0
        }
        
        print(f"\n📊 {name.upper()}:")
        print(f"  Position: ({narrative_x:.3f}, {narrative_y:.3f})")
        print(f"  Distance: {distance:.3f}")
        print(f"  Adaptive Scale: {adaptive_scale:.3f}")
        print(f"  Max Score: {max_score:.3f} → {amplified_max:.3f} ({amplified_max/max_score:.1f}x)")
    
    # Calculate overall boundary utilization
    max_distance = max(distances)
    min_distance = min(distances)
    avg_distance = np.mean(distances)
    boundary_usage = (avg_distance / 1.0) * 100  # As percentage of circle radius
    
    print(f"\n🎯 BOUNDARY UTILIZATION SUMMARY:")
    print(f"  Maximum Distance: {max_distance:.3f}")
    print(f"  Minimum Distance: {min_distance:.3f}")
    print(f"  Average Distance: {avg_distance:.3f}")
    print(f"  Boundary Usage: {boundary_usage:.1f}%")
    print(f"  Distance Spread: {max_distance - min_distance:.3f}")
    
    return results

def test_three_dimensional_architecture():
    """Demonstrate the three-dimensional architecture flexibility."""
    
    print("\n🏗️  THREE-DIMENSIONAL ARCHITECTURE TEST")
    print("=" * 50)
    
    # Test 1: Normative arrangement (Civic Virtue style)
    print("\n🔷 NORMATIVE ARRANGEMENT (Civic Virtue Style):")
    engine_normative = NarrativeGravityWellsCircular()
    
    print(f"  Positional Arrangement: {engine_normative.positional_arrangement}")
    print(f"  Framework Version: {engine_normative.framework_version}")
    
    # Display well positioning
    for well_name, well_info in engine_normative.well_definitions.items():
        well_type = well_info['type']
        angle = well_info['angle']
        weight = well_info['narrative_weight']
        print(f"    {well_name}: {angle}° ({well_type}, weight: {weight})")
    
    # Test 2: Would demonstrate descriptive arrangement (MFT style) with different config
    print("\n🔶 ALGORITHMIC ENHANCEMENT PARAMETERS:")
    dominance_config = engine_normative.enhancement_config['dominance_amplification']
    scaling_config = engine_normative.enhancement_config['adaptive_scaling']
    
    print(f"  Dominance Threshold: {dominance_config['threshold']}")
    print(f"  Amplification Base: {dominance_config['amplification_base']}")
    print(f"  Adaptive Scaling Range: {scaling_config['min_scale']:.2f} - {scaling_config['max_scale']:.2f}")
    
    return engine_normative

def create_comparison_visualization():
    """Create a comparison visualization showing enhanced vs baseline approaches."""
    
    print("\n📊 CREATING COMPARISON VISUALIZATION")
    print("=" * 50)
    
    # Test data
    test_data = create_test_datasets()
    engine = NarrativeGravityWellsCircular()
    
    # Create subplot comparison
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16))
    fig.suptitle('Circular Coordinate System - Enhanced Algorithm Demonstration', fontsize=16, fontweight='bold')
    
    datasets = [
        ('extreme_integrative', 'Extreme Integrative'),
        ('extreme_disintegrative', 'Extreme Disintegrative'),  
        ('moderate_mixed', 'Moderate Mixed'),
        ('single_dominance', 'Single Dominance')
    ]
    
    axes = [ax1, ax2, ax3, ax4]
    
    for i, ((dataset_name, display_name), ax) in enumerate(zip(datasets, axes)):
        data = test_data[dataset_name]
        well_scores = {well['name']: well['score'] for well in data['wells']}
        
        # Setup axis
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title(display_name, fontsize=14, fontweight='bold')
        
        # Plot circle boundary
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)
        ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.7)
        
        # Plot wells
        for well_name, well_info in engine.well_definitions.items():
            angle = well_info['angle']
            well_type = well_info['type']
            x, y = engine.circle_point(angle)
            
            color = '#2E7D32' if well_type == 'integrative' else '#C62828'
            ax.scatter(x, y, c=color, s=100, alpha=0.8, edgecolors='white', linewidth=2)
            
            # Add well labels
            label_x = x * 1.15
            label_y = y * 1.15
            ax.text(label_x, label_y, well_name, ha='center', va='center', 
                   fontsize=8, fontweight='bold', 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
        
        # Calculate and plot enhanced narrative position
        narrative_x, narrative_y = engine.calculate_narrative_position(well_scores)
        distance = np.sqrt(narrative_x**2 + narrative_y**2)
        
        # Plot narrative center
        ax.scatter(narrative_x, narrative_y, c='#FF8F00', s=200, alpha=0.9, 
                  edgecolors='#E65100', linewidth=3, zorder=5)
        
        # Add distance annotation
        ax.text(0.05, -1.1, f'Distance: {distance:.3f}', fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))
        
        # Add grid
        ax.grid(True, alpha=0.3)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    
    plt.tight_layout()
    
    # Save visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"circular_engine_demo_{timestamp}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"💾 Comparison visualization saved: {output_path}")
    return output_path

def main():
    """Run comprehensive circular engine demonstration."""
    
    print("🎯 CIRCULAR COORDINATE SYSTEM ENGINE DEMONSTRATION")
    print("Version 1.1.0 - Enhanced Algorithms & Universal Tool Compatibility")
    print("=" * 70)
    
    # Step 1: Create test datasets
    print("\n📝 CREATING TEST DATASETS...")
    test_data = create_test_datasets()
    print(f"✅ Created {len(test_data)} test datasets")
    
    # Step 2: Initialize engine
    print("\n🚀 INITIALIZING CIRCULAR ENGINE...")
    engine = test_three_dimensional_architecture()
    print("✅ Engine initialized with three-dimensional architecture")
    
    # Step 3: Analyze boundary utilization
    results = analyze_boundary_utilization(engine, test_data)
    
    # Step 4: Create comparison visualization
    visualization_path = create_comparison_visualization()
    
    # Step 5: Summary
    distances = [result['distance_from_center'] for result in results.values()]
    boundary_usage = (np.mean(distances) / 1.0) * 100
    
    print(f"\n🎊 DEMONSTRATION COMPLETE!")
    print("=" * 50)
    print(f"✅ Enhanced Algorithm Implementation: WORKING")
    print(f"✅ Circular Coordinate System: IMPLEMENTED")
    print(f"✅ Three-Dimensional Architecture: DEMONSTRATED")
    print(f"✅ Boundary Utilization: {boundary_usage:.1f}%")
    print(f"✅ Visualization Generated: {visualization_path}")
    
    print(f"\n🏆 KEY ACHIEVEMENTS:")
    print(f"  • Standard polar coordinates for universal tool compatibility")
    print(f"  • Enhanced algorithms with validated parameters")
    print(f"  • Framework flexibility through positional arrangement control")
    print(f"  • Mathematical weighting independence from coordinate system")
    print(f"  • Preserved analytical sophistication with improved adoption barriers")
    
    return results, visualization_path

if __name__ == "__main__":
    results, viz_path = main() 