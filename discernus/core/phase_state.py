#!/usr/bin/env python3
"""
Phase State Management
=====================

Simple, reliable phase completion tracking for resume operations.
Uses boolean state + rich provenance metadata.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class PhaseCompletion:
    """Phase completion state with provenance."""
    completed: bool
    timestamp: Optional[str] = None
    run_id: Optional[str] = None
    artifact_hashes: List[str] = None
    
    def __post_init__(self):
        if self.artifact_hashes is None:
            self.artifact_hashes = []


@dataclass
class ProvenanceRecord:
    """Complete provenance record for a run."""
    run_id: str
    source_run: Optional[str] = None
    resume_point: Optional[str] = None
    phases_completed: List[str] = None
    phases_executed: List[str] = None
    artifacts_copied: List[Dict[str, Any]] = None
    artifacts_created: List[Dict[str, Any]] = None
    execution_timeline: List[Dict[str, Any]] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.phases_completed is None:
            self.phases_completed = []
        if self.phases_executed is None:
            self.phases_executed = []
        if self.artifacts_copied is None:
            self.artifacts_copied = []
        if self.artifacts_created is None:
            self.artifacts_created = []
        if self.execution_timeline is None:
            self.execution_timeline = []
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()


class PhaseStateManager:
    """Manages phase completion state and provenance tracking."""
    
    PHASES = ['validation', 'analysis', 'statistical', 'evidence', 'synthesis']
    
    def __init__(self, run_dir: Path):
        """Initialize phase state manager for a run directory."""
        self.run_dir = run_dir
        self.provenance_file = run_dir / 'provenance.json'
        self.phase_state_file = run_dir / 'phase_state.json'
        
    def get_phase_state(self) -> Dict[str, PhaseCompletion]:
        """Get current phase completion state."""
        if not self.phase_state_file.exists():
            return {phase: PhaseCompletion(completed=False) for phase in self.PHASES}
        
        try:
            with open(self.phase_state_file, 'r') as f:
                data = json.load(f)
            
            state = {}
            for phase in self.PHASES:
                if phase in data:
                    state[phase] = PhaseCompletion(**data[phase])
                else:
                    state[phase] = PhaseCompletion(completed=False)
            return state
        except Exception:
            # If we can't read the state file, assume nothing is completed
            return {phase: PhaseCompletion(completed=False) for phase in self.PHASES}
    
    def mark_phase_complete(self, phase: str, run_id: str, artifact_hashes: List[str]) -> None:
        """Mark a phase as completed with provenance."""
        state = self.get_phase_state()
        state[phase] = PhaseCompletion(
            completed=True,
            timestamp=datetime.now(timezone.utc).isoformat(),
            run_id=run_id,
            artifact_hashes=artifact_hashes
        )
        self._save_phase_state(state)
    
    def get_completed_phases(self) -> List[str]:
        """Get list of completed phases."""
        state = self.get_phase_state()
        return [phase for phase, completion in state.items() if completion.completed]
    
    def get_remaining_phases(self, start_phase: str, end_phase: str) -> List[str]:
        """Get phases that need to be executed between start and end."""
        state = self.get_phase_state()
        start_idx = self.PHASES.index(start_phase)
        end_idx = self.PHASES.index(end_phase)
        
        remaining = []
        for i in range(start_idx, end_idx + 1):
            phase = self.PHASES[i]
            if not state[phase].completed:
                remaining.append(phase)
        
        return remaining
    
    def can_resume_from(self, start_phase: str) -> bool:
        """Check if we can resume from the given phase."""
        state = self.get_phase_state()
        start_idx = self.PHASES.index(start_phase)
        
        # All phases before start_phase must be completed
        for i in range(start_idx):
            phase = self.PHASES[i]
            if not state[phase].completed:
                return False
        
        return True
    
    def get_provenance(self) -> Optional[ProvenanceRecord]:
        """Get provenance record for this run."""
        if not self.provenance_file.exists():
            return None
        
        try:
            with open(self.provenance_file, 'r') as f:
                data = json.load(f)
            return ProvenanceRecord(**data)
        except Exception:
            return None
    
    def create_provenance(self, run_id: str, source_run: Optional[str] = None, 
                         resume_point: Optional[str] = None) -> ProvenanceRecord:
        """Create new provenance record."""
        provenance = ProvenanceRecord(
            run_id=run_id,
            source_run=source_run,
            resume_point=resume_point,
            phases_completed=self.get_completed_phases()
        )
        self._save_provenance(provenance)
        return provenance
    
    def update_provenance(self, **kwargs) -> None:
        """Update provenance record."""
        provenance = self.get_provenance()
        if provenance is None:
            return
        
        for key, value in kwargs.items():
            if hasattr(provenance, key):
                setattr(provenance, key, value)
        
        self._save_provenance(provenance)
    
    def add_artifact_copied(self, artifact_hash: str, artifact_type: str, 
                           source_run: str, copied_at: str = None) -> None:
        """Add artifact copy record to provenance."""
        if copied_at is None:
            copied_at = datetime.now(timezone.utc).isoformat()
        
        artifact_record = {
            "hash": artifact_hash,
            "type": artifact_type,
            "source_run": source_run,
            "copied_at": copied_at
        }
        
        provenance = self.get_provenance()
        if provenance:
            provenance.artifacts_copied.append(artifact_record)
            self._save_provenance(provenance)
    
    def add_artifact_created(self, artifact_hash: str, artifact_type: str, 
                            inputs: List[str] = None, created_at: str = None) -> None:
        """Add artifact creation record to provenance."""
        if created_at is None:
            created_at = datetime.now(timezone.utc).isoformat()
        if inputs is None:
            inputs = []
        
        artifact_record = {
            "hash": artifact_hash,
            "type": artifact_type,
            "created_at": created_at,
            "inputs": inputs
        }
        
        provenance = self.get_provenance()
        if provenance:
            provenance.artifacts_created.append(artifact_record)
            self._save_provenance(provenance)
    
    def add_execution_timeline(self, phase: str, start_time: str, end_time: str) -> None:
        """Add phase execution to timeline."""
        timeline_entry = {
            "phase": phase,
            "start": start_time,
            "end": end_time
        }
        
        provenance = self.get_provenance()
        if provenance:
            provenance.execution_timeline.append(timeline_entry)
            self._save_provenance(provenance)
    
    def _save_phase_state(self, state: Dict[str, PhaseCompletion]) -> None:
        """Save phase state to file."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert to serializable format
        data = {}
        for phase, completion in state.items():
            data[phase] = asdict(completion)
        
        with open(self.phase_state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_provenance(self, provenance: ProvenanceRecord) -> None:
        """Save provenance record to file."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.provenance_file, 'w') as f:
            json.dump(asdict(provenance), f, indent=2)
