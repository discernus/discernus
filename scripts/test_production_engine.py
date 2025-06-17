#!/usr/bin/env python3
"""
Test Production Engine Enhanced Algorithms
"""

import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular

def test_production_engine():
    """Test the production engine with enhanced algorithms"""
    
    print('🔧 Testing Production Engine with Enhanced Algorithms')
    print('=' * 60)
    
    # Load civic virtue framework
    with open('frameworks/civic_virtue/framework.json', 'r') as f:
        framework = json.load(f)

    # Create production engine
    engine = NarrativeGravityWellsCircular()

    # Override with civic virtue wells
    engine.well_definitions = {}
    for well_name, well_config in framework['wells'].items():
        engine.well_definitions[well_name] = {
            'angle': well_config['angle'],
            'type': well_config['type'],
            'weight': well_config['weight']
        }

    print(f'✅ Enhanced algorithms enabled: {engine.enhanced_algorithms_enabled}')
    print(f'✅ Wells loaded: {len(engine.well_definitions)}')
    
    # Test cases
    test_cases = {
        "dignity_focused": {
            'Dignity': 0.90, 'Truth': 0.85, 'Justice': 0.80, 'Hope': 0.75, 'Pragmatism': 0.70,
            'Tribalism': 0.15, 'Fear': 0.10, 'Resentment': 0.08, 'Manipulation': 0.05, 'Fantasy': 0.12
        },
        "tribal_focused": {
            'Dignity': 0.20, 'Truth': 0.15, 'Justice': 0.25, 'Hope': 0.18, 'Pragmatism': 0.22,
            'Tribalism': 0.85, 'Fear': 0.80, 'Resentment': 0.75, 'Manipulation': 0.78, 'Fantasy': 0.70
        },
        "balanced": {
            'Dignity': 0.60, 'Truth': 0.65, 'Justice': 0.55, 'Hope': 0.50, 'Pragmatism': 0.58,
            'Tribalism': 0.40, 'Fear': 0.35, 'Resentment': 0.38, 'Manipulation': 0.32, 'Fantasy': 0.42
        }
    }

    print(f'\n🧮 Testing Enhanced Algorithm Results:')
    print('-' * 60)
    
    for test_name, scores in test_cases.items():
        # Test production engine methods
        x, y = engine.calculate_narrative_position(scores)
        distance = (x**2 + y**2)**0.5
        adaptive_scale = engine.calculate_adaptive_scaling(scores)
        
        # Test dominance amplification on max score
        max_score = max(scores.values())
        amplified = engine.apply_dominance_amplification(max_score)
        
        print(f'\n📊 {test_name.upper()}:')
        print(f'   Position: ({x:.3f}, {y:.3f})')
        print(f'   Distance: {distance:.3f}')
        print(f'   Adaptive scaling: {adaptive_scale:.3f}')
        print(f'   Dominance amplification: {max_score:.3f} → {amplified:.3f} ({amplified/max_score:.2f}x)')
    
    # Test if we get different X coordinates (not all near 0)
    positions = []
    for scores in test_cases.values():
        x, y = engine.calculate_narrative_position(scores)
        positions.append((x, y))
    
    x_coords = [pos[0] for pos in positions]
    x_variance = max(x_coords) - min(x_coords)
    
    print(f'\n🎯 Enhanced Algorithms Validation:')
    print(f'   X-coordinate variance: {x_variance:.3f}')
    if x_variance > 0.1:
        print(f'   ✅ SUCCESS: Enhanced algorithms providing full circular positioning!')
    else:
        print(f'   ❌ Still getting vertical line pattern (X variance too low)')
    
    return positions

if __name__ == "__main__":
    test_production_engine() 