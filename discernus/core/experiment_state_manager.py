#!/usr/bin/env python3
"""
Experiment State Manager
========================

Manages experiment state for potential resume functionality in the Show Your Work architecture.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class ExperimentStateManager:
    """Manages experiment state for resume functionality"""
    
    def __init__(self, run_folder: Path):
        """
        Initialize the experiment state manager
        
        Args:
            run_folder: The run folder for this experiment
        """
        self.run_folder = run_folder
        self.state_file = run_folder / "experiment_state.json"
        self.checkpoint_dir = run_folder / "checkpoints"
        self.checkpoint_dir.mkdir(exist_ok=True)
    
    def save_checkpoint(self, phase: str, data: Dict[str, Any]) -> str:
        """
        Save a checkpoint for a specific phase
        
        Args:
            phase: The phase name (e.g., "analysis", "statistical", "evidence")
            data: The data to save
            
        Returns:
            Checkpoint file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = self.checkpoint_dir / f"{phase}_{timestamp}.json"
        
        checkpoint_data = {
            "phase": phase,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
        
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        return str(checkpoint_file)
    
    def load_checkpoint(self, phase: str) -> Optional[Dict[str, Any]]:
        """
        Load the most recent checkpoint for a phase
        
        Args:
            phase: The phase name
            
        Returns:
            Checkpoint data or None if not found
        """
        checkpoints = list(self.checkpoint_dir.glob(f"{phase}_*.json"))
        if not checkpoints:
            return None
        
        # Get the most recent checkpoint
        latest_checkpoint = max(checkpoints, key=lambda p: p.stat().st_mtime)
        
        with open(latest_checkpoint, 'r') as f:
            return json.load(f)
    
    def save_final_state(self, results: Dict[str, Any]) -> None:
        """
        Save the final experiment state
        
        Args:
            results: The final experiment results
        """
        final_state = {
            "status": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": results
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(final_state, f, indent=2)
    
    def get_current_status(self) -> Dict[str, Any]:
        """
        Get the current experiment status
        
        Returns:
            Current status information
        """
        if not self.state_file.exists():
            return {"status": "not_started"}
        
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def resume_experiment(self) -> Dict[str, Any]:
        """
        Resume a failed or interrupted experiment
        
        Returns:
            Resume information
        """
        status = self.get_current_status()
        
        if status.get("status") == "completed":
            return {"status": "already_completed", "message": "Experiment already completed"}
        
        # Find the last successful checkpoint
        phases = ["analysis", "statistical", "evidence"]
        last_checkpoint = None
        last_phase = None
        
        for phase in phases:
            checkpoint = self.load_checkpoint(phase)
            if checkpoint:
                last_checkpoint = checkpoint
                last_phase = phase
        
        if not last_checkpoint:
            return {"status": "no_checkpoints", "message": "No checkpoints found to resume from"}
        
        return {
            "status": "resumable",
            "last_phase": last_phase,
            "checkpoint": last_checkpoint,
            "message": f"Can resume from {last_phase} phase"
        }
