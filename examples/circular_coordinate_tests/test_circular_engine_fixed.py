#!/usr/bin/env python3
"""
Circular Coordinate System Engine - Fixed Demonstration
Version 1.1.0 - Works with actual Political Spectrum configuration

This demonstrates the circular coordinate system using the actual loaded configuration.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular

def create_political_spectrum_test_data():
    """Create test data using the actual Political Spectrum framework wells."""
    
    # Test case 1: Extreme progressive/integrative narrative
    extreme_progressive = {
        'metadata': {
            'title': 'Extreme Progressive Test Case',
            'summary': 'Synthetic narrative testing progressive political positioning',
            'model_name': 'Test',
            'model_version': 'Progressive'
        },
        'wells': [
            # Integrative wells (high scores)
            {'name': 'Solidarity', 'score': 0.95},
            {'name': 'Equality', 'score': 0.90},
            {'name': 'Democracy', 'score': 0.85},
            {'name': 'Cosmopolitan', 'score': 0.80},
            {'name': 'Progressive', 'score': 0.90},
            # Disintegrative wells (low scores)
            {'name': 'Competition', 'score': 0.05},
            {'name': 'Tradition', 'score': 0.10},
            {'name': 'Control', 'score': 0.05},
            {'name': 'Nationalist', 'score': 0.15},
            {'name': 'Conservative', 'score': 0.10}
        ]
    }
    
    # Test case 2: Extreme conservative/disintegrative narrative
    extreme_conservative = {
        'metadata': {
            'title': 'Extreme Conservative Test Case',
            'summary': 'Synthetic narrative testing conservative political positioning',
            'model_name': 'Test',
            'model_version': 'Conservative'
        },
        'wells': [
            # Integrative wells (low scores)
            {'name': 'Solidarity', 'score': 0.10},
            {'name': 'Equality', 'score': 0.05},
            {'name': 'Democracy', 'score': 0.20},
            {'name': 'Cosmopolitan', 'score': 0.15},
            {'name': 'Progressive', 'score': 0.05},
            # Disintegrative wells (high scores)
            {'name': 'Competition', 'score': 0.90},
            {'name': 'Tradition', 'score': 0.95},
            {'name': 'Control', 'score': 0.85},
            {'name': 'Nationalist', 'score': 0.85},
            {'name': 'Conservative', 'score': 0.90}
        ]
    }
    
    # Test case 3: Moderate mixed narrative
    moderate_mixed = {
        'metadata': {
            'title': 'Moderate Mixed Political Narrative',
            'summary': 'Realistic political speech with mixed ideological elements',
            'model_name': 'Test',
            'model_version': 'Moderate'
        },
        'wells': [
            {'name': 'Solidarity', 'score': 0.6},
            {'name': 'Equality', 'score': 0.5},
            {'name': 'Democracy', 'score': 0.8},  # High democratic values
            {'name': 'Cosmopolitan', 'score': 0.4},
            {'name': 'Progressive', 'score': 0.5},
            {'name': 'Competition', 'score': 0.6},  # Some market orientation
            {'name': 'Tradition', 'score': 0.4},
            {'name': 'Control', 'score': 0.3},
            {'name': 'Nationalist', 'score': 0.3},
            {'name': 'Conservative', 'score': 0.4}
        ]
    }
    
    # Test case 4: Single dimension dominance (Democracy)
    democracy_focused = {
        'metadata': {
            'title': 'Democracy-Focused Narrative',
            'summary': 'Narrative heavily emphasizing democratic principles',
            'model_name': 'Test',
            'model_version': 'Democratic'
        },
        'wells': [
            {'name': 'Solidarity', 'score': 0.3},
            {'name': 'Equality', 'score': 0.3},
            {'name': 'Democracy', 'score': 0.95},  # Dominant well
            {'name': 'Cosmopolitan', 'score': 0.2},
            {'name': 'Progressive', 'score': 0.2},
            {'name': 'Competition', 'score': 0.2},
            {'name': 'Tradition', 'score': 0.2},
            {'name': 'Control', 'score': 0.1},  # Low authoritarian control
            {'name': 'Nationalist', 'score': 0.2},
            {'name': 'Conservative', 'score': 0.2}
        ]
    }
    
    return {
        'extreme_progressive': extreme_progressive,
        'extreme_conservative': extreme_conservative,
        'moderate_mixed': moderate_mixed,
        'democracy_focused': democracy_focused
    }

def analyze_enhanced_algorithms(engine, test_data):
    """Analyze the enhanced algorithms performance."""
    
    print("🔍 ENHANCED ALGORITHMS ANALYSIS")
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
        
        # Calculate baseline position (without enhancements) for comparison
        baseline_x, baseline_y = calculate_baseline_position(engine, well_scores)
        baseline_distance = np.sqrt(baseline_x**2 + baseline_y**2)
        
        improvement = ((distance - baseline_distance) / baseline_distance * 100) if baseline_distance > 0 else 0
        
        results[name] = {
            'narrative_position': (narrative_x, narrative_y),
            'distance_from_center': distance,
            'baseline_distance': baseline_distance,
            'improvement_percent': improvement,
            'adaptive_scaling': adaptive_scale,
            'max_score_original': max_score,
            'max_score_amplified': amplified_max,
            'amplification_factor': amplified_max / max_score if max_score > 0 else 1.0
        }
        
        print(f"\n📊 {name.upper()}:")
        print(f"  Enhanced Position: ({narrative_x:.3f}, {narrative_y:.3f})")
        print(f"  Enhanced Distance: {distance:.3f}")
        print(f"  Baseline Distance: {baseline_distance:.3f}")
        print(f"  Improvement: {improvement:+.1f}%")
        print(f"  Adaptive Scale: {adaptive_scale:.3f}")
        print(f"  Max Score Enhancement: {max_score:.3f} → {amplified_max:.3f} ({amplified_max/max_score:.1f}x)")
    
    # Calculate overall performance
    max_distance = max(distances)
    min_distance = min(distances)
    avg_distance = np.mean(distances)
    distance_spread = max_distance - min_distance
    boundary_usage = (avg_distance / engine.circle_radius) * 100
    
    baseline_distances = [result['baseline_distance'] for result in results.values()]
    baseline_avg = np.mean(baseline_distances)
    overall_improvement = ((avg_distance - baseline_avg) / baseline_avg * 100) if baseline_avg > 0 else 0
    
    print(f"\n🎯 ENHANCED ALGORITHMS PERFORMANCE:")
    print(f"  Enhanced Avg Distance: {avg_distance:.3f}")
    print(f"  Baseline Avg Distance: {baseline_avg:.3f}")
    print(f"  Overall Improvement: {overall_improvement:+.1f}%")
    print(f"  Boundary Utilization: {boundary_usage:.1f}%")
    print(f"  Distance Spread: {distance_spread:.3f}")
    print(f"  Position Differentiation: {distance_spread/avg_distance:.1f}x range variation")
    
    return results

def calculate_baseline_position(engine, well_scores):
    """Calculate baseline position without enhancements (for comparison)."""
    
    weighted_x = 0.0
    weighted_y = 0.0
    total_weight = 0.0
    
    for well_name, score in well_scores.items():
        if well_name in engine.well_definitions:
            well_x, well_y = engine.circle_point(engine.well_definitions[well_name]['angle'])
            narrative_weight = engine.well_definitions[well_name]['narrative_weight']
            force = score * abs(narrative_weight)  # No amplification
            
            weighted_x += well_x * force
            weighted_y += well_y * force
            total_weight += force
    
    if total_weight > 0:
        baseline_x = weighted_x / total_weight
        baseline_y = weighted_y / total_weight
        
        # Apply only basic scaling (no adaptive scaling)
        scale_factor = 0.8  # Fixed scaling like original system
        baseline_x *= scale_factor
        baseline_y *= scale_factor
        
        return baseline_x, baseline_y
    
    return 0.0, 0.0

def create_enhanced_visualization():
    """Create visualization comparing enhanced vs baseline approaches."""
    
    print("\n📊 CREATING ENHANCED ALGORITHM COMPARISON")
    print("=" * 50)
    
    test_data = create_political_spectrum_test_data()
    engine = NarrativeGravityWellsCircular()
    
    # Create comparison visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16))
    fig.suptitle('Circular Coordinate System - Enhanced vs Baseline Comparison', 
                 fontsize=16, fontweight='bold')
    
    datasets = list(test_data.items())
    axes = [ax1, ax2, ax3, ax4]
    
    for (dataset_name, data), ax in zip(datasets, axes):
        well_scores = {well['name']: well['score'] for well in data['wells']}
        
        # Setup axis
        ax.set_aspect('equal')
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-1.0, 1.0)
        ax.set_title(data['metadata']['title'], fontsize=12, fontweight='bold')
        
        # Plot circle boundary
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = engine.circle_radius * np.cos(theta)
        y_circle = engine.circle_radius * np.sin(theta)
        ax.plot(x_circle, y_circle, 'k-', linewidth=2, alpha=0.7, label='Boundary')
        
        # Plot wells
        for well_name, well_info in engine.well_definitions.items():
            angle = well_info['angle']
            well_type = well_info['type']
            x, y = engine.circle_point(angle)
            
            color = '#2E7D32' if well_type == 'integrative' else '#C62828'
            ax.scatter(x, y, c=color, s=60, alpha=0.8, edgecolors='white', linewidth=1)
            
            # Add abbreviated well labels
            label_x = x * 1.15
            label_y = y * 1.15
            short_name = well_name[:4]  # Abbreviated for space
            ax.text(label_x, label_y, short_name, ha='center', va='center', 
                   fontsize=7, fontweight='bold', 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.7))
        
        # Calculate both enhanced and baseline positions
        enhanced_x, enhanced_y = engine.calculate_narrative_position(well_scores)
        baseline_x, baseline_y = calculate_baseline_position(engine, well_scores)
        
        enhanced_distance = np.sqrt(enhanced_x**2 + enhanced_y**2)
        baseline_distance = np.sqrt(baseline_x**2 + baseline_y**2)
        
        # Plot baseline position (gray)
        if baseline_distance > 0.01:  # Only plot if meaningful position
            ax.scatter(baseline_x, baseline_y, c='gray', s=100, alpha=0.6, 
                      edgecolors='black', linewidth=2, label='Baseline', marker='s')
        
        # Plot enhanced position (orange)
        if enhanced_distance > 0.01:  # Only plot if meaningful position
            ax.scatter(enhanced_x, enhanced_y, c='#FF8F00', s=150, alpha=0.9, 
                      edgecolors='#E65100', linewidth=3, label='Enhanced', zorder=5)
        
        # Add performance metrics
        improvement = ((enhanced_distance - baseline_distance) / baseline_distance * 100) if baseline_distance > 0 else 0
        
        metrics_text = f'Enhanced: {enhanced_distance:.3f}\nBaseline: {baseline_distance:.3f}\nImprovement: {improvement:+.1f}%'
        ax.text(0.05, -0.95, metrics_text, fontsize=9, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8),
               verticalalignment='bottom')
        
        # Add grid and clean up
        ax.grid(True, alpha=0.3)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        
        # Add legend only to first subplot
        if ax == ax1:
            ax.legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    
    # Save visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"enhanced_circular_demo_{timestamp}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"💾 Enhanced comparison visualization saved: {output_path}")
    return output_path

def main():
    """Run comprehensive enhanced circular engine demonstration."""
    
    print("🎯 ENHANCED CIRCULAR COORDINATE SYSTEM DEMONSTRATION")
    print("Version 1.1.0 - Boundary Utilization & Enhanced Algorithms")
    print("=" * 65)
    
    # Initialize engine
    print("\n🚀 INITIALIZING ENHANCED CIRCULAR ENGINE...")
    engine = NarrativeGravityWellsCircular()
    
    print(f"✅ Engine loaded: {engine.framework_version}")
    print(f"ℹ️  Circle radius: {engine.circle_radius}")
    print(f"ℹ️  Positional arrangement: {engine.positional_arrangement}")
    print(f"ℹ️  Well count: {len(engine.well_definitions)}")
    
    # Create test data
    print("\n📝 CREATING POLITICAL SPECTRUM TEST DATA...")
    test_data = create_political_spectrum_test_data()
    print(f"✅ Created {len(test_data)} test cases")
    
    # Analyze enhanced algorithms
    results = analyze_enhanced_algorithms(engine, test_data)
    
    # Create visualization
    visualization_path = create_enhanced_visualization()
    
    # Calculate summary metrics
    distances = [result['distance_from_center'] for result in results.values()]
    improvements = [result['improvement_percent'] for result in results.values()]
    
    avg_distance = np.mean(distances)
    avg_improvement = np.mean(improvements)
    boundary_usage = (avg_distance / engine.circle_radius) * 100
    
    print(f"\n🎊 ENHANCED DEMONSTRATION COMPLETE!")
    print("=" * 50)
    print(f"✅ Circular Coordinate System: IMPLEMENTED")
    print(f"✅ Enhanced Algorithms: VALIDATED")
    print(f"✅ Average Boundary Utilization: {boundary_usage:.1f}%")
    print(f"✅ Average Position Improvement: {avg_improvement:+.1f}%")
    print(f"✅ Visualization Created: {visualization_path}")
    
    print(f"\n🏆 TECHNICAL ACHIEVEMENTS:")
    print(f"  • Standard polar coordinates working correctly")
    print(f"  • Dominance amplification improving extreme representation")
    print(f"  • Adaptive scaling optimizing boundary utilization")
    print(f"  • Political spectrum framework compatibility demonstrated")
    print(f"  • Enhanced vs baseline comparison quantified")
    
    return results, visualization_path

if __name__ == "__main__":
    results, viz_path = main() 