#!/usr/bin/env python3
"""
Test script to debug NotebookExecutor with breakpoints.

This will let us step through the execution to see:
1. What notebook content is being executed
2. Why placeholder detection is failing
3. How execution failures are handled
"""

import sys
import json
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_notebook_executor():
    """Debug NotebookExecutor with breakpoints to see what's happening."""
    
    print("🔍 Debugging NotebookExecutor with breakpoints...")
    
    try:
        # Import the components we need
        from discernus.core.notebook_executor import NotebookExecutor
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        from discernus.core.audit_logger import AuditLogger
        
        print("✅ Imports successful")
        
        # Create minimal dependencies
        from unittest.mock import Mock
        
        security = Mock(spec=ExperimentSecurityBoundary)
        security.experiment_root = Path("/tmp/test_experiment")  # Add required attribute
        
        audit_logger = Mock(spec=AuditLogger)
        
        # Create NotebookExecutor instance
        executor = NotebookExecutor(
            security=security,
            audit_logger=audit_logger
        )
        
        print("✅ Created NotebookExecutor instance")
        
        # Create a test notebook with placeholder content (like what's failing)
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
        
        print("📝 Test notebook content:")
        print("=" * 50)
        print(test_notebook_content)
        print("=" * 50)
        
        # Create a temporary directory for execution
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            notebook_path = workspace / "test_notebook.py"
            
            # Write the test notebook
            notebook_path.write_text(test_notebook_content)
            
            # Create mock analysis_data.json
            analysis_data = {
                "document_analyses": [
                    {"document": "doc1", "scores": {"cohesion": 0.8}},
                    {"document": "doc2", "scores": {"cohesion": 0.6}}
                ]
            }
            (workspace / "analysis_data.json").write_text(json.dumps(analysis_data, indent=2))
            
            print(f"📁 Created test workspace: {workspace}")
            print(f"📄 Test notebook: {notebook_path}")
            print(f"📊 Mock data: analysis_data.json")
            
            # SET BREAKPOINT HERE - we want to step through the execution
            print("\n🚨 SETTING BREAKPOINT - about to call validate_and_execute_notebook")
            print("🚨 Use 'n' to step through, 's' to step into, 'c' to continue")
            print("🚨 Use 'p variable_name' to print variables")
            print("🚨 Use 'l' to see current code location")
            
            import pdb; pdb.set_trace()
            
            # This is where we'll step through the execution
            execution_result = executor.validate_and_execute_notebook(
                notebook_content=test_notebook_content,
                notebook_path=notebook_path,
                execution_timeout=60  # Short timeout for testing
            )
            
            print(f"\n📊 Execution result: {json.dumps(execution_result, indent=2)}")
            
            # Check what files were created
            print(f"\n📁 Files in workspace after execution:")
            for file_path in workspace.rglob("*"):
                if file_path.is_file():
                    print(f"   📄 {file_path.relative_to(workspace)}")
                    if file_path.suffix in ['.json', '.csv']:
                        try:
                            content = file_path.read_text()
                            print(f"      Size: {len(content)} chars")
                            if file_path.suffix == '.json':
                                parsed = json.loads(content)
                                print(f"      Keys: {list(parsed.keys())}")
                        except Exception as e:
                            print(f"      Error reading: {e}")
            
            print("\n✅ Debugging complete!")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root with PYTHONPATH set")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_notebook_executor()
