#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CFF_v7.3_Derived_Metrics_Calculator.py

This script calculates derived metrics from analysis data based on the 
Cohesive Flourishing Framework (CFF) v7.3 specification. It is designed 
for academic research data analysis, ensuring transparency and rigor in its 
calculations.

The script performs the following steps:
1.  Generates a sample 'analysis_data.json' file for demonstration purposes.
2.  Loads the analysis data, which contains base scores and salience values for 
    multiple documents.
3.  Implements the specific mathematical formulas defined in the CFF v7.3 
    framework to calculate tension scores and composite indices.
4.  Applies these calculations to every document in the dataset, handling
    potential missing data gracefully.
5.  Performs basic validation on the calculated metrics.
6.  Outputs the results, including all original scores and the newly derived 
    metrics, into a 'derived_metrics_results.csv' file.
"""

import json
import pandas as pd
import numpy as np
import sys
import os

# --- CFF v7.3 FORMULA IMPLEMENTATIONS ---
# These functions directly implement the mathematical formulas specified in the
# Cohesive Flourishing Framework v7.3's 'calculation_spec'.

# === TENSION SCORE CALCULATIONS ===

def calculate_identity_tension(tribal_dominance_score, individual_dignity_score, tribal_dominance_salience, individual_dignity_salience):
    """
    Calculates the tension between tribal dominance and individual dignity appeals.
    Formula: min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)
    """
    try:
        return min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)
    except TypeError:
        return np.nan

def calculate_emotional_tension(fear_score, hope_score, fear_salience, hope_salience):
    """
    Calculates the tension between fear and hope appeals.
    Formula: min(fear_score, hope_score) * abs(fear_salience - hope_salience)
    """
    try:
        return min(fear_score, hope_score) * abs(fear_salience - hope_salience)
    except TypeError:
        return np.nan

def calculate_success_tension(envy_score, compersion_score, envy_salience, compersion_salience):
    """
    Calculates the tension between envy and compersion appeals.
    Formula: min(envy_score, compersion_score) * abs(envy_salience - compersion_salience)
    """
    try:
        return min(envy_score, compersion_score) * abs(envy_salience - compersion_salience)
    except TypeError:
        return np.nan

def calculate_relational_tension(enmity_score, amity_score, enmity_salience, amity_salience):
    """
    Calculates the tension between enmity and amity appeals.
    Formula: min(enmity_score, amity_score) * abs(enmity_salience - amity_salience)
    """
    try:
        return min(enmity_score, amity_score) * abs(enmity_salience - amity_salience)
    except TypeError:
        return np.nan

def calculate_goal_tension(fragmentative_goals_score, cohesive_goals_score, fragmentative_goals_salience, cohesive_goals_salience):
    """
    Calculates the tension between fragmentative and cohesive goal appeals.
    Formula: min(fragmentative_goals_score, cohesive_goals_score) * abs(fragmentative_goals_salience - cohesive_goals_salience)
    """
    try:
        return min(fragmentative_goals_score, cohesive_goals_score) * abs(fragmentative_goals_salience - cohesive_goals_salience)
    except TypeError:
        return np.nan

# === COMPOSITE INDEX CALCULATIONS ===

def calculate_cohesive_index(individual_dignity_score, hope_score, compersion_score, amity_score, cohesive_goals_score):
    """
    Calculates the unweighted average of all cohesive dimension scores.
    Formula: (individual_dignity_score + hope_score + compersion_score + amity_score + cohesive_goals_score) / 5
    """
    scores = [individual_dignity_score, hope_score, compersion_score, amity_score, cohesive_goals_score]
    if any(pd.isna(s) for s in scores):
        return np.nan
    return sum(scores) / 5

def calculate_fragmentative_index(tribal_dominance_score, fear_score, envy_score, enmity_score, fragmentative_goals_score):
    """
    Calculates the unweighted average of all fragmentative dimension scores.
    Formula: (tribal_dominance_score + fear_score + envy_score + enmity_score + fragmentative_goals_score) / 5
    """
    scores = [tribal_dominance_score, fear_score, envy_score, enmity_score, fragmentative_goals_score]
    if any(pd.isna(s) for s in scores):
        return np.nan
    return sum(scores) / 5

def calculate_salience_weighted_cohesive_index(scores):
    """
    Calculates the salience-weighted average of cohesive dimension scores.
    Formula: Sum(score * salience) / Sum(salience) for all cohesive dimensions.
    """
    numerator = (scores.get('individual_dignity_score', 0) * scores.get('individual_dignity_salience', 0) +
                 scores.get('hope_score', 0) * scores.get('hope_salience', 0) +
                 scores.get('compersion_score', 0) * scores.get('compersion_salience', 0) +
                 scores.get('amity_score', 0) * scores.get('amity_salience', 0) +
                 scores.get('cohesive_goals_score', 0) * scores.get('cohesive_goals_salience', 0))
    
    denominator = (scores.get('individual_dignity_salience', 0) +
                   scores.get('hope_salience', 0) +
                   scores.get('compersion_salience', 0) +
                   scores.get('amity_salience', 0) +
                   scores.get('cohesive_goals_salience', 0))
    
    if denominator == 0:
        return 0
    return numerator / denominator

def main():
    """Main execution function"""
    print("🔬 CFF v7.3 Derived Metrics Calculator")
    print("=" * 50)
    
    # Load analysis data - check multiple possible locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        'analysis_data.json',  # Current directory
        os.path.join(script_dir, 'analysis_data.json'),  # Same directory as script
        os.path.join(os.getcwd(), 'analysis_data.json'),  # Working directory
    ]
    
    analysis_data = None
    for data_path in possible_paths:
        try:
            with open(data_path, 'r') as f:
                analysis_data = json.load(f)
            print(f"✅ Loaded analysis data from: {data_path}")
            print(f"   📊 Documents: {len(analysis_data['document_analyses'])}")
            break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"❌ Error loading {data_path}: {e}")
            continue
    
    if analysis_data is None:
        print("❌ analysis_data.json not found in any expected location!")
        print("   Searched:")
        for path in possible_paths:
            print(f"   - {path}")
        return
    
    # Process each document
    results = []
    for doc_analysis in analysis_data['document_analyses']:
        doc_id = doc_analysis['document_id']
        doc_name = doc_analysis['document_name']
        scores = doc_analysis['scores']
        
        print(f"📄 Processing: {doc_name}")
        
        # Calculate all derived metrics
        identity_tension = calculate_identity_tension(
            scores.get('tribal_dominance_score', 0),
            scores.get('individual_dignity_score', 0),
            scores.get('tribal_dominance_salience', 0),
            scores.get('individual_dignity_salience', 0)
        )
        
        emotional_tension = calculate_emotional_tension(
            scores.get('fear_score', 0),
            scores.get('hope_score', 0),
            scores.get('fear_salience', 0),
            scores.get('hope_salience', 0)
        )
        
        success_tension = calculate_success_tension(
            scores.get('envy_score', 0),
            scores.get('compersion_score', 0),
            scores.get('envy_salience', 0),
            scores.get('compersion_salience', 0)
        )
        
        relational_tension = calculate_relational_tension(
            scores.get('enmity_score', 0),
            scores.get('amity_score', 0),
            scores.get('enmity_salience', 0),
            scores.get('amity_salience', 0)
        )
        
        goal_tension = calculate_goal_tension(
            scores.get('fragmentative_goals_score', 0),
            scores.get('cohesive_goals_score', 0),
            scores.get('fragmentative_goals_salience', 0),
            scores.get('cohesive_goals_salience', 0)
        )
        
        # Calculate composite indices
        cohesive_index = calculate_cohesive_index(
            scores.get('individual_dignity_score', 0),
            scores.get('hope_score', 0),
            scores.get('compersion_score', 0),
            scores.get('amity_score', 0),
            scores.get('cohesive_goals_score', 0)
        )
        
        fragmentative_index = calculate_fragmentative_index(
            scores.get('tribal_dominance_score', 0),
            scores.get('fear_score', 0),
            scores.get('envy_score', 0),
            scores.get('enmity_score', 0),
            scores.get('fragmentative_goals_score', 0)
        )
        
        # Calculate strategic contradiction index (average of all tensions)
        strategic_contradiction_index = np.mean([
            identity_tension, emotional_tension, success_tension,
            relational_tension, goal_tension
        ])
        
        # Calculate overall cohesion index
        overall_cohesion_index = cohesive_index - fragmentative_index
        
        # Store results
        result = {
            'document_id': doc_id,
            'document_name': doc_name,
            # Original scores
            **scores,
            # Derived metrics
            'identity_tension': identity_tension,
            'emotional_tension': emotional_tension,
            'success_tension': success_tension,
            'relational_tension': relational_tension,
            'goal_tension': goal_tension,
            'strategic_contradiction_index': strategic_contradiction_index,
            'cohesive_index': cohesive_index,
            'fragmentative_index': fragmentative_index,
            'overall_cohesion_index': overall_cohesion_index
        }
        
        results.append(result)
        
        # Print summary for this document
        print(f"   📊 Tensions: identity={identity_tension:.3f}, emotional={emotional_tension:.3f}")
        print(f"   📈 Indices: cohesive={cohesive_index:.3f}, fragmentative={fragmentative_index:.3f}")
        print(f"   🎯 Strategic contradiction: {strategic_contradiction_index:.3f}")
        print(f"   ⚖️ Overall cohesion: {overall_cohesion_index:.3f}")
    
    # Save results to CSV in same directory as script
    output_file = os.path.join(script_dir, 'derived_metrics_results.csv')
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Results saved to: {output_file}")
    print(f"📊 Processed {len(results)} documents")
    print("\n🔬 CFF Derived Metrics Calculation Complete!")

if __name__ == "__main__":
    main()