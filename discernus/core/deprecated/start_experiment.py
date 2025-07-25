#!/usr/bin/env python3
"""
Start Experiment - THIN Experiment Lifecycle Entry Point
=========================================================

Intelligent experiment startup that validates, enhances, and executes experiments
while keeping the WorkflowOrchestrator pristine and reusable.

This replaces direct CLI → WorkflowOrchestrator calls with:
CLI → start_experiment.py → WorkflowOrchestrator

Benefits:
- Pre-flight validation (TrueValidationAgent, ProjectCoherenceAnalyst)
- Workflow completeness analysis
- Research deliverables verification  
- Intelligent defaults and enhancements
- Clean handoff to pristine WorkflowOrchestrator
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any

from discernus.core.experiment_lifecycle import ExperimentStartup


async def start_experiment(experiment_file: str, 
                          dev_mode: bool = False,
                          auto_enhance: bool = True) -> Dict[str, Any]:
    """
    Start an experiment with intelligent validation and enhancement.
    
    Args:
        experiment_file: Path to experiment.md file
        dev_mode: Run in development mode
        auto_enhance: Automatically enhance incomplete workflows
        
    Returns:
        Experiment execution results
        
    Raises:
        ValueError: If experiment validation fails
    """
    
    experiment_path = Path(experiment_file)
    project_path = experiment_path.parent
    
    print(f"🚀 Starting Experiment: {experiment_file}")
    print(f"📁 Project Path: {project_path}")
    
    # Initialize intelligent experiment startup
    startup = ExperimentStartup(str(project_path))
    
    try:
        # Execute with intelligent lifecycle management
        results = await startup.start_experiment(
            experiment_file=experiment_path,
            dev_mode=dev_mode,
            auto_enhance=auto_enhance
        )
        
        print(f"✅ Experiment completed successfully!")
        print(f"   Session ID: {results.get('session_id', 'Unknown')}")
        print(f"   Status: {results.get('status', 'Unknown')}")
        
        return results
        
    except Exception as e:
        print(f"❌ Experiment startup failed: {str(e)}")
        raise


def main():
    """CLI entry point for start_experiment.py"""
    if len(sys.argv) < 2:
        print("Usage: python3 start_experiment.py <experiment_file> [--dev-mode] [--no-enhance]")
        sys.exit(1)
    
    experiment_file = sys.argv[1]
    dev_mode = "--dev-mode" in sys.argv
    auto_enhance = "--no-enhance" not in sys.argv
    
    try:
        results = asyncio.run(start_experiment(experiment_file, dev_mode, auto_enhance))
        print(f"🎉 Experiment completed with status: {results.get('status')}")
    except Exception as e:
        print(f"❌ Experiment failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 