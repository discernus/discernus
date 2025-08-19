#!/usr/bin/env python3
"""
Test CSV Export Fix: Fix the statistical results CSV export logic

The issue is that the CSV export logic is looking for the wrong structure.
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Volumes/code/discernus-epic-401')

def test_csv_export_fix():
    """Test and fix the CSV export logic"""
    print("🔍 CSV EXPORT LOGIC FIX")
    print("=" * 50)
    
    # Load analysis data
    analysis_file = Path("projects/simple_test/runs/20250817T001427Z/analysis_data.json")
    with open(analysis_file) as f:
        analysis_data = json.load(f)
    
    df = pd.DataFrame(analysis_data)
    print(f"✅ Loaded analysis data: {df.shape}")
    
    # Change to run directory to import functions
    run_dir = Path("projects/simple_test/runs/20250817T001427Z")
    sys.path.insert(0, str(run_dir))
    
    # Get actual function results
    from automatedderivedmetricsagent_functions import calculate_derived_metrics
    from automatedstatisticalanalysisagent_functions import perform_statistical_analysis
    
    derived_results = calculate_derived_metrics(df)
    statistical_results = perform_statistical_analysis(df)
    
    print(f"\n📊 FUNCTION RESULTS:")
    print("-" * 30)
    print(f"derived_results: {type(derived_results)} - {derived_results.shape}")
    print(f"statistical_results: {type(statistical_results)} - {list(statistical_results.keys())}")
    
    # Show the actual structure of statistical_results
    print(f"\n🔍 STATISTICAL RESULTS STRUCTURE:")
    print("-" * 30)
    for key, value in statistical_results.items():
        print(f"{key}: {type(value)}")
        if isinstance(value, dict):
            print(f"  Keys: {list(value.keys())[:5]}...")
            if 'analysis_metadata' in value:
                print(f"  Sample metadata: {value['analysis_metadata']}")
    
    print(f"\n🧪 TESTING CSV EXPORT LOGIC:")
    print("-" * 30)
    
    # Test the current broken logic
    print("❌ CURRENT BROKEN LOGIC:")
    stats_data = []
    for test_name, test_results in statistical_results.items():
        if isinstance(test_results, dict) and 'statistic' in test_results:
            stats_data.append({
                'test_name': test_name,
                'statistic': test_results.get('statistic', 'N/A'),
                'p_value': test_results.get('p_value', 'N/A'),
                'significance': test_results.get('significance', 'N/A')
            })
    
    print(f"  Found {len(stats_data)} statistical tests (should be >0)")
    
    # Test the fixed logic
    print("\n✅ FIXED LOGIC:")
    stats_data_fixed = []
    
    for test_name, test_results in statistical_results.items():
        if isinstance(test_results, dict):
            # Handle basic statistics
            if test_name == 'calculate_basic_statistics':
                for dimension, stats in test_results.items():
                    if isinstance(stats, dict) and 'mean' in stats:
                        stats_data_fixed.append({
                            'test_name': f'basic_stats_{dimension}',
                            'statistic': stats.get('mean', 'N/A'),
                            'std': stats.get('std', 'N/A'),
                            'count': stats.get('count', 'N/A'),
                            'missing': stats.get('missing', 'N/A')
                        })
            
            # Handle other statistical results
            elif 'analysis_metadata' in test_results:
                # This is a nested analysis result
                metadata = test_results['analysis_metadata']
                stats_data_fixed.append({
                    'test_name': test_name,
                    'sample_size': metadata.get('sample_size', 'N/A'),
                    'alpha_level': metadata.get('alpha_level', 'N/A'),
                    'variables_analyzed': len(metadata.get('variables_analyzed', [])),
                    'timestamp': metadata.get('timestamp', 'N/A')
                })
    
    print(f"  Found {len(stats_data_fixed)} statistical results")
    
    if stats_data_fixed:
        print("  Sample results:")
        for i, result in enumerate(stats_data_fixed[:3]):
            print(f"    {i+1}. {result}")
    
    # Test derived metrics export
    print(f"\n🧪 TESTING DERIVED METRICS EXPORT:")
    print("-" * 30)
    
    # Extract only the derived metric columns (not raw scores)
    derived_columns = [col for col in derived_results.columns if col not in analysis_data.columns]
    print(f"Derived columns found: {len(derived_columns)}")
    if derived_columns:
        print(f"Sample derived columns: {derived_columns[:5]}")
        derived_metrics_only = derived_results[['document_name'] + derived_columns].copy()
        print(f"Derived metrics DataFrame: {derived_metrics_only.shape}")
    else:
        print("⚠️ No derived metrics calculated")
    
    print(f"\n🎯 FIX SUMMARY:")
    print("-" * 30)
    print("The CSV export logic needs to be updated to handle the actual")
    print("structure of statistical_results, which contains nested analysis")
    print("results rather than flat test statistics.")

if __name__ == "__main__":
    test_csv_export_fix()
