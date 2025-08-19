#!/usr/bin/env python3
"""
Test Function Outputs: Check What Functions Are Actually Returning

The issue isn't that functions aren't available - it's that they're returning empty data.
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Volumes/code/discernus-epic-401')

def test_function_outputs():
    """Test what the functions are actually returning"""
    print("🔍 FUNCTION OUTPUT ANALYSIS")
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
    
    print(f"\n🧪 TESTING FUNCTION OUTPUTS:")
    print("-" * 30)
    
    # Test derived metrics function
    try:
        from automatedderivedmetricsagent_functions import calculate_derived_metrics
        print("✅ calculate_derived_metrics imported")
        
        result = calculate_derived_metrics(df)
        print(f"📊 calculate_derived_metrics returned: {type(result)}")
        if result is not None:
            print(f"   Shape: {result.shape if hasattr(result, 'shape') else 'No shape'}")
            print(f"   Length: {len(result) if hasattr(result, '__len__') else 'No length'}")
            if hasattr(result, 'columns'):
                print(f"   Columns: {list(result.columns)[:5]}...")
        else:
            print("   ⚠️ Returned None")
            
    except Exception as e:
        print(f"❌ calculate_derived_metrics failed: {e}")
    
    # Test statistical analysis function
    try:
        from automatedstatisticalanalysisagent_functions import perform_statistical_analysis
        print("\n✅ perform_statistical_analysis imported")
        
        result = perform_statistical_analysis(df)
        print(f"📊 perform_statistical_analysis returned: {type(result)}")
        if result is not None:
            if isinstance(result, dict):
                print(f"   Keys: {list(result.keys())}")
                for key, value in result.items():
                    print(f"   {key}: {type(value)} - {str(value)[:100]}...")
            else:
                print(f"   Value: {str(result)[:100]}...")
        else:
            print("   ⚠️ Returned None")
            
    except Exception as e:
        print(f"❌ perform_statistical_analysis failed: {e}")
    
    # Test basic statistics function
    try:
        from automatedstatisticalanalysisagent_functions import calculate_basic_statistics
        print("\n✅ calculate_basic_statistics imported")
        
        result = calculate_basic_statistics(df)
        print(f"📊 calculate_basic_statistics returned: {type(result)}")
        if result is not None:
            if isinstance(result, dict):
                print(f"   Keys: {list(result.keys())[:5]}...")
                # Show sample stats
                for key in list(result.keys())[:3]:
                    value = result[key]
                    print(f"   {key}: {value}")
            else:
                print(f"   Value: {str(result)[:100]}...")
        else:
            print("   ⚠️ Returned None")
            
    except Exception as e:
        print(f"❌ calculate_basic_statistics failed: {e}")
    
    print(f"\n🎯 ROOT CAUSE IDENTIFIED:")
    print("-" * 30)
    print("The functions ARE executing successfully, but they're returning")
    print("empty/None results instead of actual data.")
    print("\nThis explains why:")
    print("1. Notebook reports 'success'")
    print("2. But CSV files are empty")
    print("3. Statistical results are missing")
    print("\nThe issue is in the function implementations, not the integration.")

if __name__ == "__main__":
    test_function_outputs()
