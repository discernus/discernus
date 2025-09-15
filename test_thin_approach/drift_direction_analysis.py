#!/usr/bin/env python3
"""
Analyze the direction of score drift to determine if there's systematic bias
"""

import json
import re
from pathlib import Path

def extract_scores_from_json(json_str):
    """Extract dimensional scores from JSON string."""
    scores = {}
    
    # Use a simpler approach - find each dimension individually
    dimension_pattern = r'"([^"]+)":\s*\{\s*"raw_score":\s*([0-9.]+),\s*"salience":\s*([0-9.]+),\s*"confidence":\s*([0-9.]+)\s*\}'
    
    matches = list(re.finditer(dimension_pattern, json_str, re.DOTALL))
    
    for match in matches:
        dimension = match.group(1)
        raw_score = float(match.group(2))
        salience = float(match.group(3))
        confidence = float(match.group(4))
        
        scores[dimension] = {
            'raw_score': raw_score,
            'salience': salience,
            'confidence': confidence
        }
    
    return scores

def analyze_drift_direction(scores1, scores2, name1, name2):
    """Analyze the direction of drift between two score sets."""
    print(f"\n=== {name1} vs {name2} ===")
    print(f"{'Dimension':<40} {'Score1':<8} {'Score2':<8} {'Diff':<8} {'Direction':<10}")
    print("-" * 80)
    
    higher_count = 0
    lower_count = 0
    equal_count = 0
    total_abs_diff = 0
    
    for dimension in sorted(set(scores1.keys()) | set(scores2.keys())):
        score1 = scores1.get(dimension, {}).get('raw_score', 0)
        score2 = scores2.get(dimension, {}).get('raw_score', 0)
        diff = score2 - score1  # positive means score2 is higher
        abs_diff = abs(diff)
        total_abs_diff += abs_diff
        
        if diff > 0.01:  # score2 higher
            direction = "↑ Higher"
            higher_count += 1
        elif diff < -0.01:  # score2 lower
            direction = "↓ Lower"
            lower_count += 1
        else:
            direction = "≈ Equal"
            equal_count += 1
        
        print(f"{dimension:<40} {score1:<8.2f} {score2:<8.2f} {diff:<8.3f} {direction:<10}")
    
    avg_abs_diff = total_abs_diff / len(scores1) if scores1 else 0
    
    print("-" * 80)
    print(f"Summary:")
    print(f"  Higher in {name2}: {higher_count}")
    print(f"  Lower in {name2}: {lower_count}")
    print(f"  Equal: {equal_count}")
    print(f"  Average absolute difference: {avg_abs_diff:.3f}")
    
    # Determine bias
    if higher_count > lower_count + 2:
        bias = f"{name2} systematically higher"
    elif lower_count > higher_count + 2:
        bias = f"{name2} systematically lower"
    else:
        bias = "No clear systematic bias"
    
    print(f"  Bias: {bias}")
    
    return {
        'higher_count': higher_count,
        'lower_count': lower_count,
        'equal_count': equal_count,
        'avg_abs_diff': avg_abs_diff,
        'bias': bias
    }

def main():
    # Load all result files
    results = {}
    
    files = {
        'flash_original': '/Volumes/code/discernus/tmp/artifacts/extended_analysis_results.json',
        'flash_enhanced': '/Volumes/code/discernus/tmp/artifacts/enhanced_analysis_results.json',
        'pro_original': '/Volumes/code/discernus/tmp/artifacts/original_pro_results.json',
        'pro_enhanced': '/Volumes/code/discernus/tmp/artifacts/enhanced_pro_results.json'
    }
    
    for name, filepath in files.items():
        try:
            with open(filepath, 'r') as f:
                results[name] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")
            continue
    
    print("=== SCORE DRIFT DIRECTION ANALYSIS ===")
    
    # Extract scores from all versions
    all_scores = {}
    for name, result in results.items():
        if 'composite_analysis' in result:
            all_scores[name] = extract_scores_from_json(result['composite_analysis']['raw_analysis_response'])
    
    # Analyze key comparisons
    comparisons = [
        ('flash_original', 'flash_enhanced', 'Flash Original', 'Flash Enhanced'),
        ('flash_original', 'pro_original', 'Flash Original', 'Pro Original'),
        ('flash_enhanced', 'pro_enhanced', 'Flash Enhanced', 'Pro Enhanced'),
        ('pro_original', 'pro_enhanced', 'Pro Original', 'Pro Enhanced')
    ]
    
    analysis_results = {}
    
    for name1, name2, label1, label2 in comparisons:
        if name1 in all_scores and name2 in all_scores:
            analysis_results[f"{name1}_vs_{name2}"] = analyze_drift_direction(
                all_scores[name1], all_scores[name2], label1, label2
            )
    
    # Overall summary
    print("\n=== OVERALL BIAS SUMMARY ===")
    
    # Check if there's a consistent pattern across all comparisons
    total_higher = sum(result['higher_count'] for result in analysis_results.values())
    total_lower = sum(result['lower_count'] for result in analysis_results.values())
    total_equal = sum(result['equal_count'] for result in analysis_results.values())
    
    print(f"Total dimensions analyzed: {total_higher + total_lower + total_equal}")
    print(f"Higher scores: {total_higher}")
    print(f"Lower scores: {total_lower}")
    print(f"Equal scores: {total_equal}")
    
    if total_higher > total_lower + 5:
        print("\n🎯 CONCLUSION: Systematic upward bias detected")
        print("   Enhanced/Pro approaches tend to score higher")
    elif total_lower > total_higher + 5:
        print("\n🎯 CONCLUSION: Systematic downward bias detected")
        print("   Enhanced/Pro approaches tend to score lower")
    else:
        print("\n🎯 CONCLUSION: No systematic bias detected")
        print("   Score drift appears to be randomly distributed")
    
    # Model-specific analysis
    print("\n=== MODEL-SPECIFIC PATTERNS ===")
    
    # Flash vs Pro patterns
    flash_vs_pro = []
    for key, result in analysis_results.items():
        if 'flash' in key and 'pro' in key:
            flash_vs_pro.append(result)
    
    if flash_vs_pro:
        avg_higher = sum(r['higher_count'] for r in flash_vs_pro) / len(flash_vs_pro)
        avg_lower = sum(r['lower_count'] for r in flash_vs_pro) / len(flash_vs_pro)
        
        print(f"Flash vs Pro average pattern:")
        print(f"  Pro higher: {avg_higher:.1f} dimensions")
        print(f"  Pro lower: {avg_lower:.1f} dimensions")
        
        if avg_higher > avg_lower + 1:
            print("  → Pro tends to score higher")
        elif avg_lower > avg_higher + 1:
            print("  → Pro tends to score lower")
        else:
            print("  → No clear Pro vs Flash bias")
    
    # Enhanced vs Original patterns
    enhanced_vs_original = []
    for key, result in analysis_results.items():
        if 'enhanced' in key and 'original' in key:
            enhanced_vs_original.append(result)
    
    if enhanced_vs_original:
        avg_higher = sum(r['higher_count'] for r in enhanced_vs_original) / len(enhanced_vs_original)
        avg_lower = sum(r['lower_count'] for r in enhanced_vs_original) / len(enhanced_vs_original)
        
        print(f"\nEnhanced vs Original average pattern:")
        print(f"  Enhanced higher: {avg_higher:.1f} dimensions")
        print(f"  Enhanced lower: {avg_lower:.1f} dimensions")
        
        if avg_higher > avg_lower + 1:
            print("  → Enhanced tends to score higher")
        elif avg_lower > avg_higher + 1:
            print("  → Enhanced tends to score lower")
        else:
            print("  → No clear Enhanced vs Original bias")

if __name__ == "__main__":
    main()
