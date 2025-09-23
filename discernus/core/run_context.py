#!/usr/bin/env python3
"""
Run Context
===========

Defines the RunContext data class for all inter-agent handoffs in the V2 ecosystem.
This eliminates hidden state by making all data flows explicit and typed.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class RunContext:
    """
    Typed context object for all inter-agent handoffs.
    
    This eliminates hidden state by making all data flows explicit.
    All agents receive and return data through this context object.
    """
    
    # Core experiment data
    experiment_id: str
    experiment_dir: str  # Path to experiment directory containing experiment.md, framework.md, corpus.md
    
    # File paths (populated by ValidationAgent)
    framework_path: Optional[str] = None
    corpus_path: Optional[str] = None
    
    # Analysis phase results
    analysis_results: Optional[Dict[str, Any]] = None
    analysis_artifacts: List[str] = field(default_factory=list)
    
    # Derived metrics
    derived_metrics: Optional[Dict[str, Any]] = None
    derived_metrics_artifacts: List[str] = field(default_factory=list)
    
    # Evidence phase results
    evidence: Optional[Dict[str, Any]] = None
    evidence_artifacts: List[str] = field(default_factory=list)
    
    # Statistical analysis results
    statistical_results: Optional[Dict[str, Any]] = None
    statistical_artifacts: List[str] = field(default_factory=list)
    
    # Synthesis results
    synthesis_results: Optional[Dict[str, Any]] = None
    synthesis_artifacts: List[str] = field(default_factory=list)
    
    # Verification results
    verification_results: Optional[Dict[str, Any]] = None
    verification_artifacts: List[str] = field(default_factory=list)
    
    # Metadata and provenance
    metadata: Dict[str, Any] = field(default_factory=dict)
    artifact_hashes: Dict[str, str] = field(default_factory=dict)
    cache_keys: Dict[str, str] = field(default_factory=dict)
    versions: Dict[str, str] = field(default_factory=dict)
    
    # Execution state
    current_phase: Optional[str] = None
    completed_phases: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamps if not provided"""
        if self.start_time is None:
            self.start_time = datetime.now()
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    def update_phase(self, phase: str) -> None:
        """Update the current phase and mark it as completed"""
        if self.current_phase:
            self.completed_phases.append(self.current_phase)
        self.current_phase = phase
        self.last_updated = datetime.now()
    
    def add_artifact(self, artifact_type: str, artifact_id: str, artifact_hash: str) -> None:
        """Add an artifact to the context with its hash"""
        artifact_list = getattr(self, f"{artifact_type}_artifacts", [])
        artifact_list.append(artifact_id)
        setattr(self, f"{artifact_type}_artifacts", artifact_list)
        
        self.artifact_hashes[artifact_id] = artifact_hash
        self.last_updated = datetime.now()
    
    def get_artifacts_by_type(self, artifact_type: str) -> List[str]:
        """Get all artifacts of a specific type"""
        return getattr(self, f"{artifact_type}_artifacts", [])
    
    def has_phase_completed(self, phase: str) -> bool:
        """Check if a phase has been completed"""
        return phase in self.completed_phases
    
    def get_phase_data(self, phase: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific phase"""
        return getattr(self, f"{phase}_results", None)
    
    def set_phase_data(self, phase: str, data: Dict[str, Any]) -> None:
        """Set data for a specific phase"""
        setattr(self, f"{phase}_results", data)
        self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert RunContext to dictionary for serialization"""
        return {
            "experiment_id": self.experiment_id,
            "experiment_dir": self.experiment_dir,
            "framework_path": self.framework_path,
            "corpus_path": self.corpus_path,
            "analysis_results": self.analysis_results,
            "analysis_artifacts": self.analysis_artifacts,
            "derived_metrics": self.derived_metrics,
            "derived_metrics_artifacts": self.derived_metrics_artifacts,
            "evidence": self.evidence,
            "evidence_artifacts": self.evidence_artifacts,
            "statistical_results": self.statistical_results,
            "statistical_artifacts": self.statistical_artifacts,
            "synthesis_results": self.synthesis_results,
            "synthesis_artifacts": self.synthesis_artifacts,
            "verification_results": self.verification_results,
            "verification_artifacts": self.verification_artifacts,
            "metadata": self.metadata,
            "artifact_hashes": self.artifact_hashes,
            "cache_keys": self.cache_keys,
            "versions": self.versions,
            "current_phase": self.current_phase,
            "completed_phases": self.completed_phases,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RunContext':
        """Create RunContext from dictionary"""
        # Convert timestamp strings back to datetime objects
        if data.get('start_time'):
            data['start_time'] = datetime.fromisoformat(data['start_time'])
        if data.get('last_updated'):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        
        return cls(**data)
