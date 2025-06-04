#!/usr/bin/env python3
"""
Test runner for Narrative Gravity Maps smoke tests.
Runs all smoke tests and provides comprehensive reporting.
"""

import unittest
import sys
import os
import time
from pathlib import Path
from io import StringIO

def setup_test_environment():
    """Set up the test environment"""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Change to project root directory
    os.chdir(project_root)
    
    print(f"🔧 Test environment setup:")
    print(f"   Project root: {project_root}")
    print(f"   Working directory: {os.getcwd()}")
    print(f"   Python path includes: {str(project_root)}")
    print()

def discover_and_run_tests(test_pattern="test_*.py", verbosity=2):
    """Discover and run all test files matching the pattern"""
    
    # Discover all test files
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()
    
    print(f"🔍 Discovering tests in: {test_dir}")
    print(f"   Pattern: {test_pattern}")
    
    # Load test suites
    test_suites = []
    test_files = list(test_dir.glob(test_pattern))
    
    if not test_files:
        print(f"❌ No test files found matching pattern '{test_pattern}'")
        return False
    
    print(f"📄 Found {len(test_files)} test file(s):")
    for test_file in test_files:
        print(f"   - {test_file.name}")
    print()
    
    # Import and run each test module
    results = {}
    overall_success = True
    
    for test_file in test_files:
        test_module_name = test_file.stem
        print(f"🧪 Running tests from {test_module_name}...")
        print("=" * 60)
        
        try:
            # Import the test module
            import importlib.util
            spec = importlib.util.spec_from_file_location(test_module_name, test_file)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # Load tests from the module
            suite = loader.loadTestsFromModule(test_module)
            
            # Run the tests
            stream = StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=verbosity)
            result = runner.run(suite)
            
            # Store results
            results[test_module_name] = {
                'result': result,
                'output': stream.getvalue(),
                'success': result.wasSuccessful()
            }
            
            # Print results for this module
            print(stream.getvalue())
            
            if not result.wasSuccessful():
                overall_success = False
                
        except Exception as e:
            print(f"❌ Failed to run tests in {test_module_name}: {e}")
            results[test_module_name] = {
                'result': None,
                'output': f"Failed to run: {e}",
                'success': False
            }
            overall_success = False
        
        print()
    
    return overall_success, results

def print_summary(results):
    """Print a summary of all test results"""
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    
    for module_name, data in results.items():
        result = data['result']
        success = data['success']
        
        if result:
            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
            
            total_tests += tests_run
            total_failures += failures
            total_errors += errors
            total_skipped += skipped
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {module_name:.<30} {tests_run:>3} tests, {failures:>3} failures, {errors:>3} errors, {skipped:>3} skipped")
        else:
            print(f"❌ FAIL {module_name:.<30} Failed to run")
    
    print("-" * 60)
    print(f"TOTAL:                            {total_tests:>3} tests, {total_failures:>3} failures, {total_errors:>3} errors, {total_skipped:>3} skipped")
    
    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("💥 SOME TESTS FAILED!")
        return False

def main():
    """Main test runner function"""
    print("🎯 Narrative Gravity Maps - Smoke Test Runner")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    # Setup test environment
    setup_test_environment()
    
    # Check if we have any test files
    test_dir = Path(__file__).parent
    if not any(test_dir.glob("test_*.py")):
        print("❌ No test files found! Expected files like test_*.py in tests/ directory")
        return 1
    
    # Run tests
    try:
        overall_success, results = discover_and_run_tests()
        
        # Print summary
        print()
        success = print_summary(results)
        
        # Print timing
        end_time = time.time()
        duration = end_time - start_time
        print(f"\n⏱️  Tests completed in {duration:.2f} seconds")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Unexpected error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 