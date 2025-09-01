#!/usr/bin/env python3
"""
Debug script to investigate synthesis issue
"""

import json
from pathlib import Path

def debug_synthesis_issue():
    # Load the successful run's results to understand the data structure
    results_path = Path("/Volumes/code/discernus/projects/bolsonaro_2018/runs/20250901T032022Z/results")

    if not results_path.exists():
        print("Results path not found")
        return

    # Look at the final report from the successful Flash run
    final_report_path = results_path / "final_report.md"
    if final_report_path.exists():
        with open(final_report_path, 'r') as f:
            content = f.read()
            print("Final report exists and has content")
            print(f"Length: {len(content)} characters")

    # Check if there are any artifacts that might show the research data structure
    import sys
    sys.path.append('/Volumes/code/discernus')

    try:
        from discernus.core.local_artifact_storage import LocalArtifactStorage
        from discernus.core.security_boundary import ExperimentSecurityBoundary

        experiment_path = Path('/Volumes/code/discernus/projects/bolsonaro_2018')
        security = ExperimentSecurityBoundary(experiment_path)
        storage = LocalArtifactStorage(security)

        # Look for research data artifacts
        research_data_artifacts = []
        for hash_val, info in storage.registry.items():
            artifact_type = info.get("metadata", {}).get("artifact_type", "")
            if "research_data" in artifact_type or "complete_research" in artifact_type:
                research_data_artifacts.append((hash_val, info))

        print(f"Found {len(research_data_artifacts)} research data artifacts:")
        for hash_val, info in research_data_artifacts:
            print(f"  Hash: {hash_val}")
            print(f"  Type: {info.get('metadata', {}).get('artifact_type', 'unknown')}")
            try:
                content = storage.get_artifact(hash_val)
                data = json.loads(content.decode('utf-8'))
                print(f"  Keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
                if isinstance(data, dict) and 'raw_analysis_results' in data:
                    raw_results = data['raw_analysis_results']
                    print(f"  Raw analysis results type: {type(raw_results)}")
                    if isinstance(raw_results, list):
                        print(f"  Number of analysis results: {len(raw_results)}")
                        if len(raw_results) > 0:
                            print(f"  First result keys: {list(raw_results[0].keys()) if isinstance(raw_results[0], dict) else 'not dict'}")
            except Exception as e:
                print(f"  Error loading: {e}")

    except Exception as e:
        print(f"Error accessing artifacts: {e}")

if __name__ == "__main__":
    debug_synthesis_issue()
