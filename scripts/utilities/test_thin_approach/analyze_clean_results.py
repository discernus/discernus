#!/usr/bin/env python3
"""
Systematic analysis of clean comparison results
Extract and compare scores from show work vs production with identical frameworks
"""

import json
import re
from pathlib import Path

def extract_scores_from_response(response_text, test_type):
    """Extract scores from LLM response based on test type."""
    scores = {}
    
    if test_type == "show_work":
        # Extract from show work format
        scores = _extract_show_work_scores(response_text)
    elif test_type == "production":
        # Extract from production format (JSON with delimiters)
        scores = _extract_production_scores(response_text)
    
    return scores

def _extract_show_work_scores(response_text):
    """Extract scores from show work response format."""
    scores = {}
    
    # Look for the final aggregated result section
    if "**FINAL AGGREGATED RESULT**" in response_text:
        final_section = response_text.split("**FINAL AGGREGATED RESULT**")[1]
        
        # Extract each dimension's scores
        lines = final_section.split('\n')
        current_dimension = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for dimension headers
            if line.startswith('**Dimension') and ':**' in line:
                # Extract dimension name
                dim_match = re.search(r'\*\*Dimension \d+: ([^*]+)\*\*', line)
                if dim_match:
                    current_dimension = dim_match.group(1).strip()
                continue
            
            # Look for intensity, salience, confidence
            if current_dimension and '**Intensity:**' in line:
                intensity_match = re.search(r'\*\*Intensity:\*\*\s*([0-9.]+)', line)
                if intensity_match:
                    intensity = float(intensity_match.group(1))
                    
                    # Look ahead for salience and confidence
                    salience = None
                    confidence = None
                    
                    for j in range(i+1, min(i+10, len(lines))):
                        if '**Salience:**' in lines[j]:
                            salience_match = re.search(r'\*\*Salience:\*\*\s*([0-9.]+)', lines[j])
                            if salience_match:
                                salience = float(salience_match.group(1))
                        elif '**Confidence:**' in lines[j]:
                            confidence_match = re.search(r'\*\*Confidence:\*\*\s*([0-9.]+)', lines[j])
                            if confidence_match:
                                confidence = float(confidence_match.group(1))
                                break
                    
                    if salience is not None and confidence is not None:
                        scores[current_dimension] = {
                            'intensity': intensity,
                            'salience': salience,
                            'confidence': confidence
                        }
                        current_dimension = None
    
    return scores

def _extract_production_scores(response_text):
    """Extract scores from production response format."""
    scores = {}
    
    # Look for JSON with delimiters
    json_match = re.search(r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*(\{.*?\})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>', response_text, re.DOTALL)
    
    if json_match:
        try:
            json_data = json.loads(json_match.group(1))
            
            # Extract dimensional scores
            if 'document_analyses' in json_data and len(json_data['document_analyses']) > 0:
                doc_analysis = json_data['document_analyses'][0]
                if 'dimensional_scores' in doc_analysis:
                    for dim_name, dim_scores in doc_analysis['dimensional_scores'].items():
                        scores[dim_name] = {
                            'intensity': dim_scores.get('raw_score', 0.0),
                            'salience': dim_scores.get('salience', 0.0),
                            'confidence': dim_scores.get('confidence', 0.0)
                        }
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON from production response")
    
    return scores

def analyze_clean_results():
    """Analyze the clean comparison results."""
    test_dir = Path("/Volumes/code/discernus/test_thin_approach/artifacts")
    
    print("=== CLEAN RESULTS ANALYSIS ===")
    print()
    
    # Load show work results
    with open(test_dir / "show_work_pdaf_test.json", 'r') as f:
        show_work_data = json.load(f)
    
    # Load production results
    with open(test_dir / "production_mode_test.json", 'r') as f:
        production_data = json.load(f)
    
    # Load consistency results
    with open(test_dir / "production_consistency_test.json", 'r') as f:
        consistency_data = json.load(f)
    
    # Extract scores
    show_work_scores = extract_scores_from_response(show_work_data['response'], "show_work")
    production_scores = extract_scores_from_response(production_data['response'], "production")
    
    print("1. SHOW WORK SCORES (with PDAF):")
    for dim, scores in show_work_scores.items():
        print(f"   {dim}: intensity={scores['intensity']}, salience={scores['salience']}, confidence={scores['confidence']}")
    
    print(f"\n   Total dimensions: {len(show_work_scores)}")
    
    print("\n2. PRODUCTION SCORES (with PDAF):")
    for dim, scores in production_scores.items():
        print(f"   {dim}: intensity={scores['intensity']}, salience={scores['salience']}, confidence={scores['confidence']}")
    
    print(f"\n   Total dimensions: {len(production_scores)}")
    
    # Compare scores
    print("\n3. SCORE COMPARISON:")
    print("   (Show Work vs Production)")
    
    # Find common dimensions
    common_dims = set(show_work_scores.keys()) & set(production_scores.keys())
    
    if common_dims:
        print(f"\n   Common dimensions: {len(common_dims)}")
        
        differences = []
        for dim in sorted(common_dims):
            show_intensity = show_work_scores[dim]['intensity']
            prod_intensity = production_scores[dim]['intensity']
            diff = show_intensity - prod_intensity
            direction = "HIGHER" if diff > 0 else "LOWER" if diff < 0 else "SAME"
            
            print(f"   {dim}:")
            print(f"     Show Work: {show_intensity}")
            print(f"     Production: {prod_intensity}")
            print(f"     Difference: {diff:+.3f} ({direction})")
            print()
            
            differences.append(diff)
        
        # Analyze systematic bias
        if differences:
            avg_diff = sum(differences) / len(differences)
            higher_count = sum(1 for d in differences if d > 0)
            lower_count = sum(1 for d in differences if d < 0)
            same_count = sum(1 for d in differences if d == 0)
            
            print(f"   SYSTEMATIC BIAS ANALYSIS:")
            print(f"     Average difference: {avg_diff:+.3f}")
            print(f"     Higher in show work: {higher_count}")
            print(f"     Lower in show work: {lower_count}")
            print(f"     Same: {same_count}")
            
            if abs(avg_diff) > 0.05:
                bias_direction = "HIGHER" if avg_diff > 0 else "LOWER"
                print(f"     CONCLUSION: Show work scores are SYSTEMATICALLY {bias_direction}")
            else:
                print(f"     CONCLUSION: No systematic bias detected")
    else:
        print("   No common dimensions found - cannot compare")
    
    # Analyze consistency
    print("\n4. PRODUCTION CONSISTENCY ANALYSIS:")
    
    consistency_scores = []
    for i, run_data in enumerate(consistency_data):
        run_scores = extract_scores_from_response(run_data['response'], "production")
        consistency_scores.append(run_scores)
        print(f"   Run {i+1}: {len(run_scores)} dimensions")
    
    # Check consistency across runs
    if len(consistency_scores) > 1:
        print("\n   Consistency check:")
        all_dims = set()
        for scores in consistency_scores:
            all_dims.update(scores.keys())
        
        consistent_dims = []
        for dim in all_dims:
            if all(dim in scores for scores in consistency_scores):
                intensities = [scores[dim]['intensity'] for scores in consistency_scores]
                if len(set(intensities)) == 1:  # All same
                    consistent_dims.append(dim)
        
        print(f"   Dimensions with identical scores across all runs: {len(consistent_dims)}")
        print(f"   Total dimensions: {len(all_dims)}")
        print(f"   Consistency rate: {len(consistent_dims)/len(all_dims)*100:.1f}%")
    
    print("\n=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    analyze_clean_results()
