#!/usr/bin/env python3
"""
Circular Coordinate System Demo
=============================

Demonstrates the enhanced circular coordinate system with Plotly visualization.
"""

import json
from datetime import datetime
from pathlib import Path
import numpy as np
from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular

def create_test_datasets():
    """Create test datasets for visualization."""
    return {
        'extreme_integrative': {
            'metadata': {
                'title': 'Extreme Integrative Example',
                'description': 'High scores for integrative wells'
            },
            'wells': [
                {'name': 'hope', 'score': 0.95},
                {'name': 'justice', 'score': 0.85},
                {'name': 'truth', 'score': 0.90},
                {'name': 'fear', 'score': 0.15},
                {'name': 'manipulation', 'score': 0.10}
            ]
        },
        'extreme_disintegrative': {
            'metadata': {
                'title': 'Extreme Disintegrative Example',
                'description': 'High scores for disintegrative wells'
            },
            'wells': [
                {'name': 'hope', 'score': 0.15},
                {'name': 'justice', 'score': 0.10},
                {'name': 'truth', 'score': 0.20},
                {'name': 'fear', 'score': 0.90},
                {'name': 'manipulation', 'score': 0.85}
            ]
        },
        'moderate_mixed': {
            'metadata': {
                'title': 'Moderate Mixed Example',
                'description': 'Moderate scores across all wells'
            },
            'wells': [
                {'name': 'hope', 'score': 0.55},
                {'name': 'justice', 'score': 0.45},
                {'name': 'truth', 'score': 0.50},
                {'name': 'fear', 'score': 0.45},
                {'name': 'manipulation', 'score': 0.50}
            ]
        },
        'single_dominance': {
            'metadata': {
                'title': 'Single Dominance Example',
                'description': 'One well dominates the narrative'
            },
            'wells': [
                {'name': 'hope', 'score': 0.95},
                {'name': 'justice', 'score': 0.30},
                {'name': 'truth', 'score': 0.25},
                {'name': 'fear', 'score': 0.20},
                {'name': 'manipulation', 'score': 0.15}
            ]
        }
    }

def create_comparison_visualization():
    """Create a comparison visualization showing enhanced vs baseline approaches."""
    
    print("\n📊 CREATING COMPARISON VISUALIZATION")
    print("=" * 50)
    
    # Test data
    test_data = create_test_datasets()
    engine = NarrativeGravityWellsCircular()
    
    # Create comparison visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"circular_comparison_{timestamp}.html"
    
    # Format analyses for comparison
    analyses = [
        {
            'title': name.replace('_', ' ').title(),
            'wells': data['wells'],
            'metadata': data['metadata']
        }
        for name, data in test_data.items()
    ]
    
    # Create visualization
    result = engine.create_comparative_visualization(analyses, output_path)
    print(f"✅ Comparison visualization saved: {result}")
    
    return result

def main():
    """Run complete circular coordinate system demonstration."""
    
    print("🎯 CIRCULAR COORDINATE SYSTEM DEMO")
    print("=" * 50)
    
    # Create test data
    test_data = create_test_datasets()
    
    # Initialize engine
    engine = NarrativeGravityWellsCircular()
    
    # Create individual visualizations
    results = {}
    for name, data in test_data.items():
        print(f"\n📈 Processing: {name}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"circular_{name}_{timestamp}.html"
        
        result = engine.create_visualization(data, output_path)
        results[name] = result
        print(f"✅ Visualization saved: {result}")
    
    # Create comparison visualization
    comparison_path = create_comparison_visualization()
    
    print("\n🎉 DEMO COMPLETE")
    print("=" * 50)
    print("Individual visualizations:")
    for name, path in results.items():
        print(f"- {name}: {path}")
    print(f"\nComparison visualization: {comparison_path}")
    
    return results

if __name__ == "__main__":
    main() 