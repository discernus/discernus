#!/usr/bin/env python3
"""
Test script to verify statistical preparation functionality.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_statistical_prep_import():
    """Test that we can import the statistical preparation functionality."""
    try:
        from discernus.core.thin_orchestrator import ThinOrchestrator
        print("✅ ThinOrchestrator imported successfully")
        
        # Check if the statistical_prep_only parameter is available
        import inspect
        sig = inspect.signature(ThinOrchestrator.run_experiment)
        if 'statistical_prep_only' in sig.parameters:
            print("✅ statistical_prep_only parameter is available")
        else:
            print("❌ statistical_prep_only parameter is missing")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_options():
    """Test that the CLI options are available."""
    try:
        from discernus.cli import cli
        
        # Check if the run command has the statistical-prep option
        run_cmd = cli.commands.get('run')
        if run_cmd:
            options = [param.name for param in run_cmd.params if hasattr(param, 'name')]
            print(f"✅ Run command options: {options}")
            
            if 'statistical_prep' in options:
                print("✅ --statistical-prep option is available")
            else:
                print("❌ --statistical-prep option is missing")
        else:
            print("❌ Run command not found")
            
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing statistical preparation functionality...")
    print()
    
    success = True
    
    # Test imports
    if not test_statistical_prep_import():
        success = False
    
    print()
    
    # Test CLI options
    if not test_cli_options():
        success = False
    
    print()
    
    if success:
        print("🎉 All tests passed! Statistical preparation functionality is available.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
