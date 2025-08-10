#!/usr/bin/env python3
"""
Emergency fix for missing final reports in results directories.

This script addresses the immediate customer impact issue where researchers
cannot access their final reports because they're stored in the artifact
cache but not copied to the results directory.
"""

import sys
from pathlib import Path
import json
import shutil

def fix_missing_reports(project_path: str):
    """Fix missing final reports for all runs in a project."""
    project_dir = Path(project_path)
    
    if not project_dir.exists():
        print(f"❌ Project not found: {project_dir}")
        return False
    
    runs_dir = project_dir / "runs"
    if not runs_dir.exists():
        print(f"❌ No runs directory found: {runs_dir}")
        return False
    
    shared_cache = project_dir / "shared_cache" / "artifacts"
    if not shared_cache.exists():
        print(f"❌ No shared cache found: {shared_cache}")
        return False
    
    fixed_count = 0
    total_runs = 0
    
    # Process each run directory
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir():
            continue
            
        total_runs += 1
        results_dir = run_dir / "results"
        final_report_path = results_dir / "final_report.md"
        
        # Skip if final report already exists
        if final_report_path.exists():
            print(f"✅ {run_dir.name}: final_report.md already exists")
            continue
        
        # Look for the report hash in the manifest
        manifest_path = run_dir / "manifest.json"
        report_hash = None
        
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                    
                # Look for report hash in execution stages
                for stage in manifest.get("execution_stages", []):
                    if stage.get("agent") == "ProductionThinSynthesisPipeline":
                        report_hash = stage.get("metadata", {}).get("report_hash")
                        break
            except Exception as e:
                print(f"⚠️ {run_dir.name}: Could not read manifest: {e}")
        
        if not report_hash:
            print(f"⚠️ {run_dir.name}: No report hash found in manifest")
            continue
        
        # Look for the artifact file
        artifact_pattern = f"artifact_{report_hash[:8]}"
        artifact_files = list(shared_cache.glob(f"{artifact_pattern}*"))
        
        if not artifact_files:
            print(f"⚠️ {run_dir.name}: No artifact found for hash {report_hash[:8]}")
            continue
        
        # Copy the first matching artifact
        artifact_file = artifact_files[0]
        
        try:
            if not results_dir.exists():
                results_dir.mkdir(parents=True, exist_ok=True)
                
            shutil.copy2(artifact_file, final_report_path)
            print(f"✅ {run_dir.name}: Copied {artifact_file.name} to final_report.md")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ {run_dir.name}: Failed to copy report: {e}")
    
    print(f"\n📊 Summary: Fixed {fixed_count}/{total_runs} runs")
    return fixed_count > 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/fix_missing_reports.py <project_path>")
        print("Example: python scripts/fix_missing_reports.py projects/simple_test")
        sys.exit(1)
    
    project_path = sys.argv[1]
    success = fix_missing_reports(project_path)
    sys.exit(0 if success else 1)
