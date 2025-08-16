#!/usr/bin/env python3
"""
Test script to debug _extract_execution_results method.

This will help us understand why the notebook generation is failing
and why has_real_results is False.
"""

import sys
import json
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_extract_execution_results():
    """Test the _extract_execution_results method to see why it's failing."""
    
    print("🔍 Testing _extract_execution_results method...")
    
    try:
        # Import the method we want to test
        from discernus.core.notebook_generation_orchestrator import NotebookGenerationOrchestrator
        
        # Create a real orchestrator instance (we need the actual method)
        # We'll mock the dependencies we don't need
        from unittest.mock import Mock
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        from discernus.core.audit_logger import AuditLogger
        
        # Create minimal dependencies
        security = Mock(spec=ExperimentSecurityBoundary)
        audit_logger = Mock(spec=AuditLogger)
        
        # Create a real orchestrator instance
        orchestrator = NotebookGenerationOrchestrator(
            experiment_path=Path("/tmp/test"),
            security=security,
            audit_logger=audit_logger
        )
        
        print("✅ Created NotebookGenerationOrchestrator instance")
        
        # Create a temporary workspace directory for testing
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            print(f"📁 Created test workspace: {workspace}")
            
            # Test Case 1: No execution result files exist
            print("\n🧪 Test Case 1: No execution result files exist")
            
            # Mock execution result (simulating what NotebookExecutor returns)
            execution_result = {
                'success': True,
                'stdout': '✅ Complete',
                'stderr': '',
                'return_code': 0
            }
            
            # Call the method
            results = orchestrator._extract_execution_results(workspace, execution_result)
            
            # Convert results to JSON-serializable format
            serializable_results = {}
            for key, value in results.items():
                if isinstance(value, (str, int, float, bool, list, dict)):
                    serializable_results[key] = value
                else:
                    serializable_results[key] = str(value)
            
            print(f"📊 Results: {json.dumps(serializable_results, indent=2)}")
            print(f"🔍 has_real_results: {results.get('has_real_results')}")
            print(f"📝 Summary: {results.get('summary')}")
            
            # Test Case 2: Create execution_manifest.json but no derived_metrics_results.csv
            print("\n🧪 Test Case 2: Only execution_manifest.json exists")
            
            manifest_path = workspace / "execution_manifest.json"
            manifest_content = {
                "execution_summary": {
                    "derived_metrics_calculated": 5,
                    "status": "success"
                },
                "experiment_metadata": {
                    "document_count": 4,
                    "framework": "cff_v8"
                }
            }
            manifest_path.write_text(json.dumps(manifest_content, indent=2))
            
            # Call the method again
            results = orchestrator._extract_execution_results(workspace, execution_result)
            
            # Convert results to JSON-serializable format
            serializable_results = {}
            for key, value in results.items():
                if isinstance(value, (str, int, float, bool, list, dict)):
                    serializable_results[key] = value
                else:
                    serializable_results[key] = str(value)
            
            print(f"📊 Results: {json.dumps(serializable_results, indent=2)}")
            print(f"🔍 has_real_results: {results.get('has_real_results')}")
            print(f"📝 Summary: {results.get('summary')}")
            
            # Test Case 3: Create both files
            print("\n🧪 Test Case 3: Both files exist")
            
            derived_metrics_path = workspace / "derived_metrics_results.csv"
            csv_content = """metric_name,value,document
overall_cohesion_index,0.75,document1
identity_tension,0.45,document1
emotional_balance,0.82,document1"""
            derived_metrics_path.write_text(csv_content)
            
            # Call the method again
            results = orchestrator._extract_execution_results(workspace, execution_result)
            
            # Convert results to JSON-serializable format
            serializable_results = {}
            for key, value in results.items():
                if isinstance(value, (str, int, float, bool, list, dict)):
                    serializable_results[key] = value
                else:
                    serializable_results[key] = str(value)
            
            print(f"📊 Results: {json.dumps(serializable_results, indent=2)}")
            print(f"🔍 has_real_results: {results.get('has_real_results')}")
            print(f"📝 Summary: {results.get('summary')}")
            
            # Test Case 4: Check what files actually exist in workspace
            print("\n🧪 Test Case 4: Files in workspace")
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
            
            print("\n✅ Testing complete!")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root with PYTHONPATH set")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extract_execution_results()
