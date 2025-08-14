#!/usr/bin/env python3
"""
Research Notebook with Externalized Logic Architecture

This notebook demonstrates data externalization - all complex statistical
logic is in separate modules, notebook handles only data flow and execution.
"""

import json
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Import externalized statistical functions
from statistical_functions_only import (
    calculate_descriptive_statistics,
    calculate_correlation_matrix, 
    perform_cohesion_analysis,
    analyze_tension_patterns
)

# Import derived metrics functions from existing notebook
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def load_analysis_data():
    """Load analysis data from external JSON file."""
    data_file = Path('analysis_data.json')
    if not data_file.exists():
        raise FileNotFoundError(f"Analysis data not found: {data_file}")
    
    with open(data_file, 'r') as f:
        return json.load(f)

def convert_to_dataframe(analysis_data):
    """Convert analysis data to pandas DataFrame for statistical analysis."""
    records = []
    
    for doc_analysis in analysis_data['document_analyses']:
        record = {
            'document_id': doc_analysis['document_id'],
            'document_name': doc_analysis['document_name']
        }
        
        # Add all scores
        record.update(doc_analysis['scores'])
        
        records.append(record)
    
    return pd.DataFrame(records)

def calculate_derived_metrics(df):
    """Calculate derived metrics using deterministic formulas."""
    
    # Identity tension
    df['identity_tension'] = np.minimum(
        df['tribal_dominance_score'], df['individual_dignity_score']
    ) * np.abs(df['tribal_dominance_salience'] - df['individual_dignity_salience'])
    
    # Emotional tension  
    df['emotional_tension'] = np.minimum(
        df['fear_score'], df['hope_score']
    ) * np.abs(df['fear_salience'] - df['hope_salience'])
    
    # Success tension
    df['success_tension'] = np.minimum(
        df['envy_score'], df['compersion_score']
    ) * np.abs(df['envy_salience'] - df['compersion_salience'])
    
    # Relational tension
    df['relational_tension'] = np.minimum(
        df['enmity_score'], df['amity_score']
    ) * np.abs(df['enmity_salience'] - df['amity_salience'])
    
    # Goal tension
    df['goal_tension'] = np.minimum(
        df['fragmentative_goals_score'], df['cohesive_goals_score']
    ) * np.abs(df['fragmentative_goals_salience'] - df['cohesive_goals_salience'])
    
    # Strategic contradiction index
    df['strategic_contradiction_index'] = (
        df['identity_tension'] + df['emotional_tension'] + df['success_tension'] +
        df['relational_tension'] + df['goal_tension']
    ) / 5
    
    # Cohesive index
    df['cohesive_index'] = (
        df['individual_dignity_score'] + df['hope_score'] + df['compersion_score'] +
        df['amity_score'] + df['cohesive_goals_score']
    ) / 5
    
    # Fragmentative index
    df['fragmentative_index'] = (
        df['tribal_dominance_score'] + df['fear_score'] + df['envy_score'] +
        df['enmity_score'] + df['fragmentative_goals_score']
    ) / 5
    
    # Overall cohesion index
    df['overall_cohesion_index'] = df['cohesive_index'] - df['fragmentative_index']
    
    return df

def main():
    """Main execution function - pure data orchestration."""
    
    print("🔬 Research Notebook with Externalized Logic")
    print("=" * 60)
    
    try:
        # Step 1: Load data (deterministic)
        print("📊 Loading analysis data...")
        analysis_data = load_analysis_data()
        print(f"✅ Loaded {len(analysis_data['document_analyses'])} documents")
        
        # Step 2: Convert to DataFrame (deterministic)
        print("🔄 Converting to DataFrame...")
        df = convert_to_dataframe(analysis_data)
        print(f"✅ DataFrame created: {df.shape}")
        
        # Step 3: Calculate derived metrics (deterministic)
        print("🧮 Calculating derived metrics...")
        df = calculate_derived_metrics(df)
        print("✅ Derived metrics calculated")
        
        # Step 4: Statistical analysis (externalized functions)
        print("📈 Running statistical analyses...")
        
        # Call externalized statistical functions
        desc_stats = calculate_descriptive_statistics(df)
        correlations = calculate_correlation_matrix(df)
        cohesion_analysis = perform_cohesion_analysis(df)
        tension_analysis = analyze_tension_patterns(df)
        
        # Compile results
        results = {
            'descriptive_statistics': desc_stats,
            'correlation_analysis': correlations,
            'cohesion_analysis': cohesion_analysis,
            'tension_analysis': tension_analysis
        }
        
        print("✅ Statistical analyses complete")
        
        # Step 5: Save results (deterministic)
        print("💾 Saving results...")
        
        # Save detailed results to JSON
        with open('statistical_analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save data to CSV for external analysis
        df.to_csv('complete_analysis_results.csv', index=False)
        
        print("✅ Results saved")
        
        # Step 6: Display summary
        print("\n📋 Analysis Summary:")
        
        if desc_stats['success']:
            print(f"   📊 Descriptive stats: {len(desc_stats['statistics'])} variables")
        
        if correlations['success']:
            print(f"   🔗 Significant correlations: {len(correlations['significant_correlations'])}")
        
        if cohesion_analysis['success']:
            print(f"   ⚖️ Cohesion comparisons: {len(cohesion_analysis['comparisons'])}")
        
        if tension_analysis['success']:
            dominant = tension_analysis['analysis']['dominant_tensions']['highest']
            print(f"   🎯 Dominant tension: {dominant['type']} ({dominant['score']:.3f})")
        
        print("\n🎉 Complete research analysis finished!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
