#!/usr/bin/env python3
"""
Compare scores between original and enhanced versions to check for drift
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
    print(f"Found {len(matches)} dimension matches")
    
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
        print(f"Extracted: {dimension} = {raw_score}")
    
    return scores

def main():
    # Load original results
    with open('/Volumes/code/discernus/tmp/artifacts/extended_analysis_results.json', 'r') as f:
        original_results = json.load(f)
    
    # Load enhanced results
    with open('/Volumes/code/discernus/tmp/artifacts/enhanced_analysis_results.json', 'r') as f:
        enhanced_results = json.load(f)
    
    # Extract scores from both versions
    original_scores = extract_scores_from_json(original_results['composite_analysis']['raw_analysis_response'])
    enhanced_scores = extract_scores_from_json(enhanced_results['composite_analysis']['raw_analysis_response'])
    
    print("=== SCORE DRIFT ANALYSIS ===")
    print()
    
    # Compare scores
    dimensions = set(original_scores.keys()) | set(enhanced_scores.keys())
    
    print(f"{'Dimension':<40} {'Original':<15} {'Enhanced':<15} {'Drift':<10}")
    print("-" * 80)
    
    total_drift = 0
    drift_count = 0
    
    for dimension in sorted(dimensions):
        orig = original_scores.get(dimension, {})
        enh = enhanced_scores.get(dimension, {})
        
        orig_score = orig.get('raw_score', 0)
        enh_score = enh.get('raw_score', 0)
        
        drift = abs(orig_score - enh_score)
        total_drift += drift
        drift_count += 1
        
        orig_str = f"{orig_score:.2f}" if orig else "N/A"
        enh_str = f"{enh_score:.2f}" if enh else "N/A"
        drift_str = f"{drift:.3f}" if orig and enh else "N/A"
        
        print(f"{dimension:<40} {orig_str:<15} {enh_str:<15} {drift_str:<10}")
    
    print("-" * 80)
    avg_drift = total_drift / drift_count if drift_count > 0 else 0
    print(f"Average Score Drift: {avg_drift:.3f}")
    
    # Check verification status
    print()
    print("=== VERIFICATION STATUS ===")
    orig_verified = original_results.get('verification', {}).get('verified', False)
    enh_verified = enhanced_results.get('verification', {}).get('verified', False)
    
    print(f"Original Version: {'✓ Verified' if orig_verified else '✗ Not Verified'}")
    print(f"Enhanced Version: {'✓ Verified' if enh_verified else '✗ Not Verified'}")
    
    # Check markup
    print()
    print("=== MARKUP STATUS ===")
    markup_available = enhanced_results.get('markup_extraction', {}).get('marked_up_document', '')
    if markup_available:
        print(f"✓ Marked-up document available ({len(markup_available)} characters)")
        print(f"  Sample: {markup_available[:200]}...")
    else:
        print("✗ No marked-up document available")

if __name__ == "__main__":
    main()
