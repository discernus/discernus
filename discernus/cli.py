#!/usr/bin/env python3
"""
Discernus CLI v2.0
=================

Command-line interface for running experiments with THIN orchestration.
"""

import argparse
from pathlib import Path

from discernus.core.thin_orchestrator import ThinOrchestrator


def main():
    """Run Discernus CLI."""
    parser = argparse.ArgumentParser(description="Discernus CLI v2.0")
    parser.add_argument("experiment_path", type=str, help="Path to experiment directory")
    parser.add_argument("--model", type=str, default="vertex_ai/gemini-2.5-flash",
                      help="LLM model to use (default: vertex_ai/gemini-2.5-flash)")
    parser.add_argument("--synthesis-only", action="store_true",
                      help="Skip analysis and run synthesis on existing CSVs")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = ThinOrchestrator(Path(args.experiment_path))
    
    # Run experiment
    result = orchestrator.run_experiment(
        model=args.model,
        synthesis_only=args.synthesis_only
    )
    
    print("\n✨ Experiment completed successfully!")


if __name__ == "__main__":
    main() 