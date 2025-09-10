#!/usr/bin/env python3
"""
Test the full resume functionality.
"""

import sys
from pathlib import Path
from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_resume.py <experiment_path>")
        sys.exit(1)
    
    experiment_path = Path(sys.argv[1]).resolve()
    
    print("🔄 Testing full resume functionality")
    
    # Initialize orchestrator with resume mode
    print("🔧 Initializing orchestrator...")
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
    print("✅ Orchestrator initialized")
    
    try:
        # Debug: Check if resume flag is set
        print(f"🔍 Resume flag in orchestrator: {orchestrator.resume_from_stats}")
        
        # Execute resume
        print("🔄 Calling orchestrator.run_experiment()...")
        result = orchestrator.run_experiment()
        print(f"🔄 run_experiment() returned: {result}")
        
        if result.get('status') in ['completed', 'completed_analysis_only', 'completed_statistical_prep', 'completed_resume_synthesis']:
            print("✅ Resume completed successfully!")
            if result.get('results_directory'):
                print(f"📁 Results saved to: {result['results_directory']}")
            if result.get('mode') == 'resume_from_stats' and result.get('resumed_from'):
                print(f"🔄 Resumed from statistical preparation run: {result['resumed_from']}")
        else:
            print(f"❌ Resume failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except CleanAnalysisError as e:
        print(f"❌ Resume error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during resume: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
