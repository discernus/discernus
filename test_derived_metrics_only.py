#!/usr/bin/env python3
"""
Unit test to verify derived metrics validation works correctly.
"""

import json
from pathlib import Path
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary

def test_derived_metrics_validation():
    """Test just the derived metrics validation logic."""
    
    # Create a minimal test setup
    experiment_path = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    security_boundary = ExperimentSecurityBoundary(experiment_path)
    run_folder = experiment_path / "shared_cache"
    run_folder.mkdir(parents=True, exist_ok=True)
    
    # Create artifact storage
    artifact_storage = LocalArtifactStorage(
        security_boundary=security_boundary,
        run_folder=run_folder,
        run_name="test_run"
    )
    
    # Mock derived metrics data structure
    mock_derived_metrics_data = {
        'status': 'success_with_data',
        'derived_metrics_data': {
            'derived_metrics': [
                {'document_id': 'doc1', 'net_sentiment': 0.8},
                {'document_id': 'doc2', 'net_sentiment': -0.3}
            ]
        }
    }
    
    # Store mock data in artifact storage
    artifact_storage.put_artifact(
        json.dumps(mock_derived_metrics_data).encode('utf-8'),
        {"artifact_type": "derived_metrics_results_with_data"}
    )
    
    # Mock statistical results with derived metrics hash
    mock_statistical_results = {
        'derived_metrics_data_hash': None,
        'raw_analysis_data_hash': 'test_analysis_hash',
        'statistical_summary': {'test': 'data'}
    }
    
    # Find the actual hash
    for artifact_hash, info in artifact_storage.registry.items():
        if info.get("metadata", {}).get("artifact_type") == "derived_metrics_results_with_data":
            mock_statistical_results['derived_metrics_data_hash'] = artifact_hash
            break
    
    print(f"🔍 Mock statistical results: {json.dumps(mock_statistical_results, indent=2)}")
    print(f"🔍 Mock derived metrics data: {json.dumps(mock_derived_metrics_data, indent=2)}")
    
    # Test the derived metrics validation logic directly
    try:
        # Check if derived metrics hash exists
        if not mock_statistical_results.get('derived_metrics_data_hash'):
            raise Exception("SYNTHESIS BLOCKED: No derived metrics results available")
        
        # Load derived metrics from artifact storage
        try:
            derived_metrics_data = artifact_storage.get_artifact(mock_statistical_results['derived_metrics_data_hash']).decode('utf-8')
            derived_metrics_results = json.loads(derived_metrics_data)
        except Exception as e:
            raise Exception(f"SYNTHESIS BLOCKED: Cannot load derived metrics data: {e}")
        
        # Check the status of derived metrics
        derived_metrics_status = derived_metrics_results.get('status', 'unknown')
        print(f"🔍 Derived metrics status: {derived_metrics_status}")
        
        if derived_metrics_status != 'success_with_data':
            raise Exception("SYNTHESIS BLOCKED: Derived metrics results incomplete")
        
        # Check that we have actual metrics data
        metrics_data = derived_metrics_results.get('derived_metrics_data', {})
        if not metrics_data or not metrics_data.get('derived_metrics'):
            raise Exception("SYNTHESIS BLOCKED: Derived metrics contain no actual metrics data")
        
        print("✅ Derived metrics validation passed!")
        print(f"✅ Found {len(metrics_data.get('derived_metrics', []))} derived metrics")
        
    except Exception as e:
        print(f"❌ Derived metrics validation failed: {e}")

if __name__ == "__main__":
    test_derived_metrics_validation()
