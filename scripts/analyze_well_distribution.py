#!/usr/bin/env python3
"""
Analyze Well Distribution - Why Civic Virtue Framework Creates Elliptical Patterns
"""

import numpy as np
import json
from pathlib import Path

def analyze_well_distribution():
    """Analyze the angular distribution of wells in civic virtue framework"""
    
    print('🔍 CIVIC VIRTUE WELL ANGLE ANALYSIS')
    print('=' * 60)
    
    # Load framework
    with open('frameworks/civic_virtue/framework.json', 'r') as f:
        framework = json.load(f)
    
    integrative_angles = []
    disintegrative_angles = []
    
    print('📍 Well Positions:')
    for well_name, config in framework['wells'].items():
        angle = config['angle']
        well_type = config['type']
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        print(f'   {well_name:12} {angle:3d}° → ({x:5.2f}, {y:5.2f}) [{well_type}]')
        
        if well_type == 'integrative':
            integrative_angles.append(angle)
        else:
            disintegrative_angles.append(angle)
    
    print(f'\n📊 ANGLE DISTRIBUTION:')
    print(f'   Integrative wells: {integrative_angles}')
    print(f'   Disintegrative wells: {disintegrative_angles}')
    
    print(f'\n🎯 CLUSTERING ANALYSIS:')
    int_span = max(integrative_angles) - min(integrative_angles)
    dis_span = max(disintegrative_angles) - min(disintegrative_angles)
    
    print(f'   Integrative cluster: {min(integrative_angles)}°-{max(integrative_angles)}° (span: {int_span}°)')
    print(f'   Disintegrative cluster: {min(disintegrative_angles)}°-{max(disintegrative_angles)}° (span: {dis_span}°)')
    
    # Find gaps
    all_angles = sorted(integrative_angles + disintegrative_angles)
    gaps = []
    for i in range(len(all_angles)):
        next_angle = all_angles[(i + 1) % len(all_angles)]
        current_angle = all_angles[i]
        
        if next_angle < current_angle:  # Wrap around 360°
            gap = (360 - current_angle) + next_angle
        else:
            gap = next_angle - current_angle
            
        if gap > 30:  # Significant gap
            gaps.append((current_angle, next_angle, gap))
    
    print(f'\n🕳️  LARGE GAPS (>30°):')
    for start, end, gap_size in gaps:
        if end < start:  # Wrapped around
            print(f'   {start}°-360° + 0°-{end}° = {gap_size:.0f}° gap')
        else:
            print(f'   {start}°-{end}° = {gap_size:.0f}° gap')
    
    print(f'\n❗ WHY THIS CREATES ELLIPTICAL PATTERNS:')
    print(f'   • Wells clustered in only 2 opposite regions (top vs bottom)')
    print(f'   • Large gaps mean no attraction in horizontal directions')
    print(f'   • Result: All narratives pulled toward vertical axis')
    print(f'   • Creates linear/elliptical distribution, not full circular spread')
    
    # Calculate theoretical center positions for pure cases
    print(f'\n🧮 THEORETICAL POSITIONING:')
    
    # Pure integrative
    int_x = sum(np.cos(np.deg2rad(a)) for a in integrative_angles) / len(integrative_angles)
    int_y = sum(np.sin(np.deg2rad(a)) for a in integrative_angles) / len(integrative_angles)
    
    # Pure disintegrative  
    dis_x = sum(np.cos(np.deg2rad(a)) for a in disintegrative_angles) / len(disintegrative_angles)
    dis_y = sum(np.sin(np.deg2rad(a)) for a in disintegrative_angles) / len(disintegrative_angles)
    
    print(f'   Pure integrative narrative → ({int_x:.3f}, {int_y:.3f})')
    print(f'   Pure disintegrative narrative → ({dis_x:.3f}, {dis_y:.3f})')
    print(f'   Distance between extremes: {np.sqrt((int_x-dis_x)**2 + (int_y-dis_y)**2):.3f}')
    
    # Show why X coordinates are near zero
    print(f'\n📐 X-COORDINATE ANALYSIS:')
    print(f'   Integrative average X: {int_x:.3f} (near zero due to 60°-120° spread)')
    print(f'   Disintegrative average X: {dis_x:.3f} (near zero due to 240°-300° spread)')
    print(f'   Result: All narratives positioned near Y-axis (vertical line)')

def compare_to_full_circle():
    """Show what a full circular distribution would look like"""
    
    print(f'\n🔄 COMPARISON: FULL CIRCULAR DISTRIBUTION')
    print('=' * 60)
    
    print('If wells were evenly distributed around full circle:')
    
    # 10 wells evenly distributed
    even_angles = [i * 36 for i in range(10)]  # 360/10 = 36° apart
    
    for i, angle in enumerate(even_angles):
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        print(f'   Well_{i+1}: {angle:3d}° → ({x:5.2f}, {y:5.2f})')
    
    print(f'\n✅ This would create true circular spread!')
    print(f'   • Narratives could be positioned anywhere in 2D space')
    print(f'   • Full range of X and Y coordinates possible')
    print(f'   • No elliptical constraint')

if __name__ == '__main__':
    analyze_well_distribution()
    compare_to_full_circle() 