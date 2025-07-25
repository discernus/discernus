#!/usr/bin/env python3
"""
Resume Experiment - THIN Experiment Resumption Entry Point  
===========================================================

Intelligent experiment resumption that analyzes state, validates context,
and resumes experiments while keeping the WorkflowOrchestrator pristine.

This replaces direct CLI → WorkflowOrchestrator resume calls with:
CLI → resume_experiment.py → WorkflowOrchestrator

Benefits:
- State discovery and analysis
- Resumption point validation
- Workflow change detection
- Clean handoff to pristine WorkflowOrchestrator
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from discernus.core.experiment_lifecycle import ExperimentResumption


async def resume_experiment(project_path: str,
                           state_file: Optional[str] = None,
                           from_step: Optional[int] = None) -> Dict[str, Any]:
    """
    Resume an experiment with intelligent state analysis.
    
    Args:
        project_path: Path to project directory
        state_file: Specific state file to resume from (optional)
        from_step: Step number to resume from (optional)
        
    Returns:
        Resume execution results
        
    Raises:
        ValueError: If resumption validation fails
    """
    
    project_dir = Path(project_path)
    state_file_path = Path(state_file) if state_file else None
    
    print(f"🔄 Resuming Experiment: {project_path}")
    
    # Initialize intelligent experiment resumption
    resumption = ExperimentResumption(str(project_dir))
    
    try:
        # Execute with intelligent lifecycle management
        results = await resumption.resume_experiment(
            state_file=state_file_path,
            from_step=from_step
        )
        
        print(f"✅ Experiment resumed successfully!")
        print(f"   Session ID: {results.get('session_id', 'Unknown')}")
        print(f"   Status: {results.get('status', 'Unknown')}")
        
        return results
        
    except Exception as e:
        print(f"❌ Experiment resumption failed: {str(e)}")
        raise


def main():
    """CLI entry point for resume_experiment.py"""
    if len(sys.argv) < 2:
        print("Usage: python3 resume_experiment.py <project_path> [--state-file FILE] [--from-step N]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    # Parse optional arguments
    state_file = None
    from_step = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--state-file" and i + 1 < len(sys.argv):
            state_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--from-step" and i + 1 < len(sys.argv):
            from_step = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    try:
        results = asyncio.run(resume_experiment(project_path, state_file, from_step))
        print(f"🎉 Experiment resumed with status: {results.get('status')}")
    except Exception as e:
        print(f"❌ Resume failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 