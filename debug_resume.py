#!/usr/bin/env python3
"""
Debug resume functionality to isolate the issue.
"""

import sys
from pathlib import Path
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 debug_resume.py <experiment_path>")
        sys.exit(1)
    
    experiment_path = Path(sys.argv[1]).resolve()
    
    print("🔄 Debug resume functionality")
    
    # Initialize orchestrator with resume mode
    orchestrator = CleanAnalysisOrchestrator(
        experiment_path=experiment_path,
        analysis_model="vertex_ai/gemini-2.5-flash",
        synthesis_model="vertex_ai/gemini-2.5-pro",
        validation_model="vertex_ai/gemini-2.5-flash-lite",
        derived_metrics_model="vertex_ai/gemini-2.5-pro",
        dry_run=False,
        skip_validation=False,
        analysis_only=False,
        statistical_prep=False,
        resume_from_stats=True,
        ensemble_runs=None,
        auto_commit=True,
        verbosity="normal"
    )
    
    try:
        # Test just the artifact loading
        print("📊 Testing artifact loading...")
        analysis_results = orchestrator._load_resume_artifacts("test", "analysis")
        derived_metrics_results = orchestrator._load_resume_artifacts("test", "derived_metrics")
        
        print(f"Analysis results type: {type(analysis_results)}")
        if analysis_results:
            print(f"Analysis results length: {len(analysis_results)}")
            print(f"First analysis result type: {type(analysis_results[0])}")
        
        print(f"Derived metrics results type: {type(derived_metrics_results)}")
        
        # Test just the statistical analysis phase
        print("📊 Testing statistical analysis phase...")
        from discernus.core.audit_logger import AuditLogger
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        security = ExperimentSecurityBoundary(experiment_path)
        audit_logger = AuditLogger(security, experiment_path / "session" / "debug")
        
        if analysis_results and derived_metrics_results:
            # Load config first
            orchestrator.config = orchestrator._load_specs()
            print(f"Config loaded: {orchestrator.config}")
            
            # Initialize artifact storage
            from discernus.core.local_artifact_storage import LocalArtifactStorage
            orchestrator.artifact_storage = LocalArtifactStorage(
                security_boundary=security,
                run_folder=experiment_path / "session" / "debug"
            )
            print("Artifact storage initialized")
            
            statistical_results = orchestrator._run_statistical_analysis_phase(
                "vertex_ai/gemini-2.5-pro", 
                audit_logger, 
                analysis_results, 
                derived_metrics_results
            )
            print(f"Statistical results type: {type(statistical_results)}")
        else:
            print("❌ Could not load artifacts for testing")
            
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
