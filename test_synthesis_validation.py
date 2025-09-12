#!/usr/bin/env python3
"""
Unit test to debug synthesis validation handoff issue.
"""

import json
import tempfile
from pathlib import Path
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.local_artifact_storage import LocalArtifactStorage

def test_synthesis_validation_handoff():
    """Test the synthesis validation logic with mock data."""
    
    # Create a temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mock artifact storage
        artifact_storage = LocalArtifactStorage(
            security_boundary="test",
            run_folder=temp_path
        )
        
        # Create orchestrator instance
        orchestrator = CleanAnalysisOrchestrator(
            experiment_path=temp_path,
            artifact_storage=artifact_storage
        )
        
        # Mock the derived metrics data structure that we know exists
        derived_metrics_data = {
            "status": "success",
            "functions_generated": 5,
            "output_file": "automatedderivedmetricsagent_functions.py",
            "module_size": 5938,
            "derived_metrics_results": {
                "generation_metadata": {
                    "status": "success",
                    "functions_generated": 5,
                    "output_file": "automatedderivedmetricsagent_functions.py",
                    "module_size": 5938
                },
                "derived_metrics_data": {
                    "status": "success",
                    "original_count": 2,
                    "derived_count": 2,
                    "derived_metrics": [
                        {
                            "raw_analysis_response": "test response",
                            "net_sentiment": 1.0,
                            "sentiment_intensity": 0.5
                        }
                    ]
                }
            }
        }
        
        # Store the mock data in artifact storage
        derived_metrics_hash = artifact_storage.put_artifact(
            json.dumps(derived_metrics_data, indent=2).encode('utf-8'),
            {"artifact_type": "derived_metrics_results_with_data"}
        )
        
        # Create mock statistical results
        statistical_results = {
            "derived_metrics_data_hash": derived_metrics_hash,
            "status": "success"
        }
        
        # Test the validation logic directly
        print("🔍 Testing synthesis validation logic...")
        
        # Load derived metrics from artifact storage (same as orchestrator does)
        try:
            derived_metrics_data_loaded = artifact_storage.get_artifact(statistical_results['derived_metrics_data_hash']).decode('utf-8')
            derived_metrics_results = json.loads(derived_metrics_data_loaded)
            print(f"✅ Successfully loaded derived metrics data")
        except Exception as e:
            print(f"❌ Failed to load derived metrics data: {e}")
            return False
        
        # Check the status (this was working)
        derived_metrics_status = derived_metrics_results.get('status', 'unknown')
        print(f"🔍 Derived metrics status: {derived_metrics_status}")
        
        if derived_metrics_status != 'success':
            print(f"❌ Status check failed: expected 'success', got '{derived_metrics_status}'")
            return False
        
        # Test the nested structure access (this was failing)
        print("🔍 Testing nested structure access...")
        
        # Current (broken) approach
        metrics_data_broken = derived_metrics_results.get('derived_metrics_data', {})
        print(f"🔍 Broken approach - metrics_data: {metrics_data_broken}")
        
        # Fixed approach
        nested_results = derived_metrics_results.get('derived_metrics_results', {})
        metrics_data_fixed = nested_results.get('derived_metrics_data', {})
        derived_metrics_list = metrics_data_fixed.get('derived_metrics', [])
        
        print(f"🔍 Fixed approach - nested_results keys: {list(nested_results.keys())}")
        print(f"🔍 Fixed approach - metrics_data keys: {list(metrics_data_fixed.keys())}")
        print(f"🔍 Fixed approach - derived_metrics_list length: {len(derived_metrics_list)}")
        
        if not metrics_data_fixed or not derived_metrics_list:
            print(f"❌ Fixed approach still failed")
            return False
        
        print(f"✅ Fixed approach works! Found {len(derived_metrics_list)} derived metrics")
        
        # Test the actual validation logic
        print("🔍 Testing actual validation logic...")
        
        # This should work now
        if not metrics_data_fixed or not derived_metrics_list:
            print(f"❌ Validation would fail")
            return False
        
        print(f"✅ Validation would pass!")
        return True

if __name__ == "__main__":
    success = test_synthesis_validation_handoff()
    if success:
        print("🎉 Test passed! The handoff issue is identified and fixable.")
    else:
        print("❌ Test failed! Need to investigate further.")
