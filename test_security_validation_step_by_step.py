#!/usr/bin/env python3
"""
Test script to step through security validation line by line.

This will let us see exactly what pattern is causing the security validation to fail.
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_security_validation_step_by_step():
    """Debug security validation by stepping through the method line by line."""
    
    print("🔍 Debugging security validation step by step...")
    
    try:
        # Import the NotebookExecutor
        from discernus.core.notebook_executor import NotebookExecutor
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        from discernus.core.audit_logger import AuditLogger
        
        print("✅ Imports successful")
        
        # Create minimal dependencies
        from unittest.mock import Mock
        
        security = Mock(spec=ExperimentSecurityBoundary)
        security.experiment_root = Path("/tmp/test_experiment")
        
        audit_logger = Mock(spec=AuditLogger)
        
        # Create NotebookExecutor instance
        executor = NotebookExecutor(
            security=security,
            audit_logger=audit_logger
        )
        
        print("✅ Created NotebookExecutor instance")
        
        # Test notebook content (same as before)
        test_notebook_content = '''
import pandas as pd
import numpy as np

# Load analysis data
try:
    analysis_data = pd.read_json("analysis_data.json")
    print("✅ Data loaded successfully")
except Exception as e:
    print(f"❌ Error loading data: {e}")

# This is the placeholder content that's causing the failure
print("Statistical analysis pending execution")

# Generated functions would go here
def calculate_derived_metrics(data):
    """Calculate derived metrics from analysis data."""
    print("Calculating derived metrics...")
    # Placeholder implementation
    return {"status": "placeholder"}

# Execute the analysis
if 'analysis_data' in locals():
    results = calculate_derived_metrics(analysis_data)
    print(f"✅ Analysis complete: {results}")
else:
    print("❌ No data available for analysis")
'''
        
        print("📝 Test notebook content length:", len(test_notebook_content))
        
        # Let's look at the security validation method source
        print("\n🔍 Security validation method source:")
        import inspect
        source = inspect.getsource(executor._validate_security)
        print(source)
        
        # SET BREAKPOINT HERE - let's step through the method line by line
        print("\n🚨 SETTING BREAKPOINT - about to step through _validate_security")
        print("🚨 Use 's' to step into the method, 'n' to step through lines")
        print("🚨 Use 'p pattern' to print the current pattern being checked")
        print("🚨 Use 'p notebook_content' to see the notebook content")
        print("🚨 Use 'l' to see current code location")
        
        import pdb; pdb.set_trace()
        
        # Test the security validation method directly
        security_valid = executor._validate_security(test_notebook_content)
        
        print(f"\n🔒 Security validation result: {security_valid}")
        
        print("\n✅ Security validation step-by-step debugging complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root with PYTHONPATH set")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_security_validation_step_by_step()
