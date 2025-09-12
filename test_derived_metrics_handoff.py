#!/usr/bin/env python3
"""
Unit test to debug derived metrics handoff issue between statistical phase and synthesis phase.
"""

import json
from pathlib import Path
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger

def test_derived_metrics_handoff():
    """Test the derived metrics handoff between statistical and synthesis phases."""
    
    # Create a minimal test setup
    experiment_path = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    
    # Create orchestrator instance
    orchestrator = CleanAnalysisOrchestrator(
        experiment_path=experiment_path,
        analysis_model="vertex_ai/gemini-2.5-flash",
        synthesis_model="vertex_ai/gemini-2.5-pro",
        derived_metrics_model="vertex_ai/gemini-2.5-pro"
    )
    
    # Mock the config that validation needs
    orchestrator.config = {
        'framework': 'framework.md',
        'corpus': 'corpus.md',
        'experiment_name': 'nano_test_experiment'
    }
    
    # Initialize components
    from discernus.core.security_boundary import ExperimentSecurityBoundary
    security_boundary = ExperimentSecurityBoundary(experiment_path)
    run_folder = experiment_path / "shared_cache"
    run_folder.mkdir(parents=True, exist_ok=True)
    
    orchestrator.artifact_storage = LocalArtifactStorage(
        security_boundary=security_boundary,
        run_folder=run_folder,
        run_name="test_run"
    )
    audit_logger = AuditLogger(
        security_boundary=security_boundary,
        run_folder=experiment_path / "session" / "test_session"
    )
    
    # Mock statistical results with derived metrics hash
    mock_statistical_results = {
        'derived_metrics_data_hash': 'test_hash_123',
        'raw_analysis_data_hash': 'test_analysis_hash',
        'statistical_summary': {'test': 'data'}
    }
    
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
    orchestrator.artifact_storage.put_artifact(
        json.dumps(mock_derived_metrics_data).encode('utf-8'),
        {"artifact_type": "derived_metrics_results_with_data"}
    )
    
    # Update the hash in statistical results
    for artifact_hash, info in orchestrator.artifact_storage.registry.items():
        if info.get("metadata", {}).get("artifact_type") == "derived_metrics_results_with_data":
            mock_statistical_results['derived_metrics_data_hash'] = artifact_hash
            break
    
    print(f"🔍 Mock statistical results: {json.dumps(mock_statistical_results, indent=2)}")
    print(f"🔍 Mock derived metrics data: {json.dumps(mock_derived_metrics_data, indent=2)}")
    
    # Test the validation method directly
    try:
        orchestrator._validate_assets(mock_statistical_results)
        print("✅ Validation passed!")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        
        # Debug: Check what's actually in the artifact storage
        print("\n🔍 Debug: Artifact storage contents:")
        for artifact_hash, info in orchestrator.artifact_storage.registry.items():
            print(f"  Hash: {artifact_hash[:8]}...")
            print(f"  Type: {info.get('metadata', {}).get('artifact_type', 'unknown')}")
            try:
                content = orchestrator.artifact_storage.get_artifact(artifact_hash).decode('utf-8')
                data = json.loads(content)
                print(f"  Status: {data.get('status', 'no status')}")
                print(f"  Keys: {list(data.keys())}")
            except Exception as decode_error:
                print(f"  Decode error: {decode_error}")
            print()

if __name__ == "__main__":
    test_derived_metrics_handoff()
