#!/usr/bin/env python3
"""
Test runner for Narrative Gravity Maps smoke tests.
Runs all smoke tests and provides comprehensive reporting.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def setup_test_environment():
    """Set up the test environment"""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Add src directory to Python path for imports
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    # Change to project root directory
    os.chdir(project_root)
    
    print(f"🔧 Test environment setup:")
    print(f"   Project root: {project_root}")
    print(f"   Working directory: {os.getcwd()}")
    print(f"   Python path includes: {str(project_root)}")
    print(f"   Python path includes: {str(src_path)}")
    print()

def discover_and_run_tests(test_pattern="test_*.py", verbosity=2):
    """Discover and run all test files using pytest"""
    
    # Discover all test files
    test_dir = Path(__file__).parent
    
    print(f"🔍 Discovering tests in: {test_dir}")
    print(f"   Pattern: {test_pattern} (including subdirectories)")
    
    # Find test files recursively
    test_files = list(test_dir.rglob(test_pattern))
    
    if not test_files:
        print(f"❌ No test files found matching pattern '{test_pattern}'")
        return False, {}
    
    print(f"📄 Found {len(test_files)} test file(s):")
    for test_file in test_files:
        print(f"   - {test_file.relative_to(test_dir)}")
    print()
    
    # Run pytest on all discovered test files
    print(f"🧪 Running all tests with pytest...")
    print("=" * 60)
    
    try:
        # Build pytest command
        pytest_args = [
            sys.executable, "-m", "pytest",
            str(test_dir),  # Run all tests in test directory
            "-v",  # Verbose output
            "--tb=short",  # Short traceback format
            "--disable-warnings"  # Reduce noise from deprecation warnings
        ]
        
        # Set up environment with PYTHONPATH
        env = os.environ.copy()
        project_root = test_dir.parent
        pythonpath = f"{project_root}:{project_root}/src"
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{pythonpath}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = pythonpath
        
        # Run pytest
        result = subprocess.run(pytest_args, capture_output=True, text=True, cwd=test_dir.parent, env=env)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        
        # Parse basic results from output
        results = {"pytest_run": {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": success
        }}
        
        return success, results
        
    except Exception as e:
        print(f"❌ Failed to run pytest: {e}")
        results = {"pytest_run": {
            "returncode": 1,
            "stdout": "",
            "stderr": str(e),
            "success": False
        }}
        return False, results

def print_summary(results):
    """Print a summary of pytest results"""
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    
    if "pytest_run" in results:
        pytest_result = results["pytest_run"]
        success = pytest_result["success"]
        output = pytest_result["stdout"]
        
        # Try to extract basic stats from pytest output
        if "failed" in output.lower() or "error" in output.lower():
            print("❌ SOME TESTS FAILED")
            status = False
        elif "passed" in output.lower():
            print("✅ TESTS PASSED")
            status = True
        else:
            print("⚠️  TEST STATUS UNCLEAR")
            status = pytest_result["success"]
        
        # Try to extract test count from output
        lines = output.split('\n')
        for line in lines:
            if 'passed' in line and ('failed' in line or 'error' in line or 'warning' in line):
                print(f"📋 {line.strip()}")
                break
        
        return status
    else:
        print("❌ NO TEST RESULTS AVAILABLE")
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
    test_files = list(test_dir.rglob("test_*.py"))
    if not test_files:
        print("❌ No test files found! Expected files like test_*.py in tests/ directory or subdirectories")
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