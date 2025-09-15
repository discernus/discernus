#!/usr/bin/env python3
"""
Compare scores from 'show your work' test vs production scores
"""

import json
import re

def extract_show_work_scores():
    """Extract scores from the show your work test."""
    with open('/Volumes/code/discernus/tmp/artifacts/three_shot_visibility_test.json', 'r') as f:
        data = json.load(f)
    
    response_text = data['response']
    
    # Extract final scores from the response
    scores = {}
    
    # Find the final section
    final_section = response_text.split('### **STEP 3: Final Aggregated Result**')[1]
    
    # Extract each dimension's scores - look for the pattern in the final section
    lines = final_section.split('\n')
    
    current_dimension = None
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Look for dimension headers
        if line.startswith('*   **') and line.endswith('**'):
            current_dimension = line.replace('*', '').replace('**', '').strip()
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

def extract_production_scores():
    """Extract scores from production run."""
    with open('/Volumes/code/discernus/tmp/artifacts/extended_analysis_results.json', 'r') as f:
        data = json.load(f)
    
    # Get the scores from the production run
    scores_text = data['score_extraction']['scores_extraction']
    
    # Extract JSON from the response
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', scores_text, re.DOTALL)
    if json_match:
        scores_json = json.loads(json_match.group(1))
        return scores_json
    
    return {}

def compare_scores():
    """Compare show work vs production scores."""
    show_work_scores = extract_show_work_scores()
    production_scores = extract_production_scores()
    
    print("=== SCORE COMPARISON: SHOW YOUR WORK vs PRODUCTION ===")
    print()
    
    # Map dimensions between the two approaches
    dimension_mapping = {
        'People-Centrism': 'manichaean_people_elite_framing',
        'Anti-Elitism/Anti-Establishment': 'anti_pluralist_exclusion', 
        'Nationalism/Sovereignty': 'nationalist_exclusion',
        'Charismatic Leadership (Leader as Voice of People)': 'authenticity_vs_political_class',
        'Direct Appeal/Common Sense': 'economic_populist_appeals',
        'Crisis/Threat Perception': 'crisis_restoration_narrative'
    }
    
    print("SHOW YOUR WORK SCORES:")
    for dim, scores in show_work_scores.items():
        print(f"  {dim}: intensity={scores['intensity']}, salience={scores['salience']}, confidence={scores['confidence']}")
    
    print("\nPRODUCTION SCORES:")
    for dim, scores in production_scores.items():
        print(f"  {dim}: raw_score={scores['raw_score']}, salience={scores['salience']}, confidence={scores['confidence']}")
    
    print("\n=== COMPARISON ANALYSIS ===")
    
    # Compare mapped dimensions
    for show_dim, prod_dim in dimension_mapping.items():
        if show_dim in show_work_scores and prod_dim in production_scores:
            show_intensity = show_work_scores[show_dim]['intensity']
            prod_raw_score = production_scores[prod_dim]['raw_score']
            
            diff = show_intensity - prod_raw_score
            direction = "HIGHER" if diff > 0 else "LOWER" if diff < 0 else "SAME"
            
            print(f"{show_dim} -> {prod_dim}:")
            print(f"  Show Work: {show_intensity}")
            print(f"  Production: {prod_raw_score}")
            print(f"  Difference: {diff:+.2f} ({direction})")
            print()
    
    # Check for systematic bias
    differences = []
    for show_dim, prod_dim in dimension_mapping.items():
        if show_dim in show_work_scores and prod_dim in production_scores:
            show_intensity = show_work_scores[show_dim]['intensity']
            prod_raw_score = production_scores[prod_dim]['raw_score']
            differences.append(show_intensity - prod_raw_score)
    
    if differences:
        avg_diff = sum(differences) / len(differences)
        higher_count = sum(1 for d in differences if d > 0)
        lower_count = sum(1 for d in differences if d < 0)
        same_count = sum(1 for d in differences if d == 0)
        
        print(f"SYSTEMATIC BIAS ANALYSIS:")
        print(f"  Average difference: {avg_diff:+.3f}")
        print(f"  Higher in show work: {higher_count}")
        print(f"  Lower in show work: {lower_count}")
        print(f"  Same: {same_count}")
        
        if avg_diff > 0.05:
            print(f"  CONCLUSION: Show work scores are SYSTEMATICALLY HIGHER")
        elif avg_diff < -0.05:
            print(f"  CONCLUSION: Show work scores are SYSTEMATICALLY LOWER")
        else:
            print(f"  CONCLUSION: No systematic bias detected")

if __name__ == "__main__":
    compare_scores()
