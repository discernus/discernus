#!/usr/bin/env python3
"""
Isolated Unit Test: Why Statistical Results Aren't Making It Into Final Notebook

This test isolates each component to find the exact failure point.
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Volumes/code/discernus-epic-401')

def test_1_data_loading():
    """Test 1: Can we load the analysis data?"""
    print("🔍 TEST 1: Data Loading")
    print("=" * 50)
    
    try:
        # Load analysis data
        analysis_file = Path("projects/simple_test/runs/20250817T001427Z/analysis_data.json")
        if not analysis_file.exists():
            print("❌ analysis_data.json not found")
            return False
            
        with open(analysis_file) as f:
            analysis_data = json.load(f)
        
        print(f"✅ Loaded analysis data: {len(analysis_data)} documents")
        print(f"📊 Sample data: {analysis_data[0]['document_name']}")
        print(f"📈 Dimensions: {list(analysis_data[0].keys())[1:4]}...")
        return True
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_2_derived_metrics_calculation():
    """Test 2: Can we calculate derived metrics?"""
    print("\n🔍 TEST 2: Derived Metrics Calculation")
    print("=" * 50)
    
    try:
        # Load analysis data
        with open("projects/simple_test/runs/20250817T001427Z/analysis_data.json") as f:
            analysis_data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(analysis_data)
        print(f"✅ DataFrame created: {df.shape}")
        
        # Check if derived metrics functions exist
        derived_functions_file = Path("projects/simple_test/runs/20250817T001427Z/automatedderivedmetricsagent_functions.py")
        if not derived_functions_file.exists():
            print("❌ Derived metrics functions file not found")
            return False
            
        print("✅ Derived metrics functions file exists")
        
        # Try to import and use the functions
        import importlib.util
        spec = importlib.util.spec_from_file_location("derived_metrics", derived_functions_file)
        derived_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(derived_module)
        
        print("✅ Derived metrics module imported")
        
        # Check what functions are available
        available_functions = [name for name in dir(derived_module) if name.startswith('calculate_')]
        print(f"📋 Available functions: {available_functions}")
        
        return True
        
    except Exception as e:
        print(f"❌ Derived metrics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3_statistical_analysis_execution():
    """Test 3: Can we execute statistical analysis?"""
    print("\n🔍 TEST 3: Statistical Analysis Execution")
    print("=" * 50)
    
    try:
        # Load analysis data
        with open("projects/simple_test/runs/20250817T001427Z/analysis_data.json") as f:
            analysis_data = json.load(f)
        
        df = pd.DataFrame(analysis_data)
        print(f"✅ DataFrame loaded: {df.shape}")
        
        # Check if statistical functions exist
        stats_functions_file = Path("projects/simple_test/runs/20250817T001427Z/automatedstatisticalanalysisagent_functions.py")
        if not stats_functions_file.exists():
            print("❌ Statistical functions file not found")
            return False
            
        print("✅ Statistical functions file exists")
        
        # Import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location("statistical_analysis", stats_functions_file)
        stats_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stats_module)
        
        print("✅ Statistical module imported")
        
        # Check what functions are available
        available_functions = [name for name in dir(stats_module) if name.startswith(('calculate_', 'perform_', 'test_'))]
        print(f"📋 Available functions: {available_functions}")
        
        # Try to execute basic statistics
        if hasattr(stats_module, 'calculate_basic_statistics'):
            print("🧪 Testing calculate_basic_statistics...")
            basic_stats = stats_module.calculate_basic_statistics(df)
            print(f"✅ Basic stats result: {type(basic_stats)}")
            if basic_stats:
                print(f"📊 Sample stats: {list(basic_stats.keys())[:3]}")
            else:
                print("⚠️ Basic stats returned None/empty")
        else:
            print("❌ calculate_basic_statistics function not found")
            
        # Try to execute complete analysis
        if hasattr(stats_module, 'run_complete_statistical_analysis'):
            print("🧪 Testing run_complete_statistical_analysis...")
            complete_stats = stats_module.run_complete_statistical_analysis(df)
            print(f"✅ Complete stats result: {type(complete_stats)}")
            if complete_stats:
                print(f"📊 Analysis keys: {list(complete_stats.keys())}")
            else:
                print("⚠️ Complete stats returned None/empty")
        else:
            print("❌ run_complete_statistical_analysis function not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Statistical analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_4_notebook_template_integration():
    """Test 4: Can the notebook template access the functions?"""
    print("\n🔍 TEST 4: Notebook Template Integration")
    print("=" * 50)
    
    try:
        # Check if the notebook can import its own functions
        notebook_file = Path("projects/simple_test/runs/20250817T001427Z/research_notebook.py")
        if not notebook_file.exists():
            print("❌ Research notebook not found")
            return False
            
        print("✅ Research notebook exists")
        
        # Read the notebook to see what functions it's trying to call
        with open(notebook_file) as f:
            notebook_content = f.read()
        
        # Check for function calls
        function_calls = [
            'perform_statistical_analysis',
            'calculate_derived_metrics', 
            'integrate_evidence_with_statistics'
        ]
        
        for func in function_calls:
            if func in notebook_content:
                print(f"✅ {func} referenced in notebook")
            else:
                print(f"❌ {func} NOT referenced in notebook")
        
        # Check if functions are imported
        if 'from automatedstatisticalanalysisagent_functions import' in notebook_content:
            print("✅ Statistical functions imported")
        else:
            print("❌ Statistical functions NOT imported")
            
        if 'from automatedderivedmetricsagent_functions import' in notebook_content:
            print("✅ Derived metrics functions imported")
        else:
            print("❌ Derived metrics functions NOT imported")
            
        return True
        
    except Exception as e:
        print(f"❌ Notebook template test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_5_function_availability_in_notebook():
    """Test 5: Are the functions actually available when notebook runs?"""
    print("\n🔍 TEST 5: Function Availability in Notebook Runtime")
    print("=" * 50)
    
    try:
        # Create a minimal test environment
        import sys
        import os
        
        # Add the run directory to Python path
        run_dir = Path("projects/simple_test/runs/20250817T001427Z")
        sys.path.insert(0, str(run_dir))
        
        # Change to run directory
        os.chdir(run_dir)
        
        print(f"✅ Changed to directory: {os.getcwd()}")
        
        # Try to import the functions
        try:
            from automatedstatisticalanalysisagent_functions import calculate_basic_statistics
            print("✅ calculate_basic_statistics imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import calculate_basic_statistics: {e}")
            
        try:
            from automatedderivedmetricsagent_functions import calculate_identity_tension
            print("✅ calculate_identity_tension imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import calculate_identity_tension: {e}")
        
        # Test function execution
        try:
            # Load test data
            with open("analysis_data.json") as f:
                test_data = json.load(f)
            
            df = pd.DataFrame(test_data)
            print(f"✅ Test data loaded: {df.shape}")
            
            # Test basic statistics
            if 'calculate_basic_statistics' in locals():
                result = calculate_basic_statistics(df)
                print(f"✅ Basic stats executed: {type(result)}")
                if result:
                    print(f"📊 Result keys: {list(result.keys())[:3]}")
                else:
                    print("⚠️ Basic stats returned None/empty")
            else:
                print("❌ calculate_basic_statistics not available")
                
        except Exception as e:
            print(f"❌ Function execution failed: {e}")
            import traceback
            traceback.print_exc()
            
        return True
        
    except Exception as e:
        print(f"❌ Function availability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all isolated tests"""
    print("🧪 ISOLATED UNIT TESTING: Statistical Pipeline Failure Analysis")
    print("=" * 70)
    
    tests = [
        test_1_data_loading,
        test_2_derived_metrics_calculation,
        test_3_statistical_analysis_execution,
        test_4_notebook_template_integration,
        test_5_function_availability_in_notebook
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {test.__name__} - {status}")
    
    passed = sum(results)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed - the issue is elsewhere")
    else:
        print("❌ Found the failure point(s) - see above for details")

if __name__ == "__main__":
    main()
