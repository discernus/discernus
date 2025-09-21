#!/usr/bin/env python3
"""
Experiment Run Configuration for V2 Orchestrator
================================================

Replaces boolean flags with a single typed configuration object.
Provides clean separation of experiment vs. runtime configuration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum


class ExecutionMode(Enum):
    """Execution modes for experiments"""
    FULL_EXPERIMENT = "full_experiment"
    ANALYSIS_ONLY = "analysis_only"
    STATISTICAL_PREP = "statistical_prep"
    RESUME_FROM_STATS = "resume_from_stats"


class VerificationLevel(Enum):
    """Verification levels"""
    NONE = "none"
    BASIC = "basic"
    FULL = "full"


@dataclass
class ModelConfig:
    """Model configuration for agents"""
    primary_model: str = "vertex_ai/gemini-2.5-flash"
    verification_model: str = "vertex_ai/gemini-2.5-flash-lite"
    analysis_model: str = "vertex_ai/gemini-2.5-flash"
    statistical_model: str = "vertex_ai/gemini-2.5-flash"
    synthesis_model: str = "vertex_ai/gemini-2.5-flash"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            "primary_model": self.primary_model,
            "verification_model": self.verification_model,
            "analysis_model": self.analysis_model,
            "statistical_model": self.statistical_model,
            "synthesis_model": self.synthesis_model
        }


@dataclass
class CacheConfig:
    """Cache configuration"""
    enabled: bool = True
    cache_dir: Optional[str] = None
    max_cache_size_mb: int = 1000
    cache_ttl_hours: int = 24
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "enabled": self.enabled,
            "cache_dir": self.cache_dir,
            "max_cache_size_mb": self.max_cache_size_mb,
            "cache_ttl_hours": self.cache_ttl_hours
        }


@dataclass
class VerificationConfig:
    """Verification configuration"""
    enabled: bool = True
    level: VerificationLevel = VerificationLevel.BASIC
    verify_analysis: bool = True
    verify_statistical: bool = True
    verify_evidence: bool = False
    verify_synthesis: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "enabled": self.enabled,
            "level": self.level.value,
            "verify_analysis": self.verify_analysis,
            "verify_statistical": self.verify_statistical,
            "verify_evidence": self.verify_evidence,
            "verify_synthesis": self.verify_synthesis
        }


@dataclass
class ResumeConfig:
    """Resume configuration"""
    enabled: bool = False
    resume_from_phase: Optional[str] = None
    manifest_path: Optional[str] = None
    auto_save_manifest: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "enabled": self.enabled,
            "resume_from_phase": self.resume_from_phase,
            "manifest_path": self.manifest_path,
            "auto_save_manifest": self.auto_save_manifest
        }


@dataclass
class ExperimentRunConfig:
    """
    Single configuration object for experiment runs.
    
    Replaces multiple boolean flags with a clean, typed configuration.
    """
    
    # Core experiment settings
    experiment_id: str
    framework_path: str
    corpus_path: str
    output_dir: str
    
    # Execution settings
    execution_mode: ExecutionMode = ExecutionMode.FULL_EXPERIMENT
    debug_mode: bool = False
    dry_run: bool = False
    
    # Model configuration
    models: ModelConfig = field(default_factory=ModelConfig)
    
    # Cache configuration
    cache: CacheConfig = field(default_factory=CacheConfig)
    
    # Verification configuration
    verification: VerificationConfig = field(default_factory=VerificationConfig)
    
    # Resume configuration
    resume: ResumeConfig = field(default_factory=ResumeConfig)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "experiment_id": self.experiment_id,
            "framework_path": self.framework_path,
            "corpus_path": self.corpus_path,
            "output_dir": self.output_dir,
            "execution_mode": self.execution_mode.value,
            "debug_mode": self.debug_mode,
            "dry_run": self.dry_run,
            "models": self.models.to_dict(),
            "cache": self.cache.to_dict(),
            "verification": self.verification.to_dict(),
            "resume": self.resume.to_dict(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExperimentRunConfig':
        """Create from dictionary"""
        # Handle enum conversion
        if isinstance(data.get("execution_mode"), str):
            data["execution_mode"] = ExecutionMode(data["execution_mode"])
        
        if isinstance(data.get("verification", {}).get("level"), str):
            data["verification"]["level"] = VerificationLevel(data["verification"]["level"])
        
        # Create nested configs
        if "models" in data:
            data["models"] = ModelConfig(**data["models"])
        
        if "cache" in data:
            data["cache"] = CacheConfig(**data["cache"])
        
        if "verification" in data:
            data["verification"] = VerificationConfig(**data["verification"])
        
        if "resume" in data:
            data["resume"] = ResumeConfig(**data["resume"])
        
        return cls(**data)
    
    def get_agent_model(self, agent_name: str) -> str:
        """Get the appropriate model for an agent"""
        model_mapping = {
            "analysis": self.models.analysis_model,
            "statistical": self.models.statistical_model,
            "synthesis": self.models.synthesis_model,
            "verification": self.models.verification_model,
            "evidence": self.models.primary_model,
            "coherence": self.models.primary_model
        }
        
        return model_mapping.get(agent_name, self.models.primary_model)
    
    def should_verify_phase(self, phase: str) -> bool:
        """Check if a phase should be verified"""
        if not self.verification.enabled:
            return False
        
        verification_mapping = {
            "analysis": self.verification.verify_analysis,
            "statistical": self.verification.verify_statistical,
            "evidence": self.verification.verify_evidence,
            "synthesis": self.verification.verify_synthesis
        }
        
        return verification_mapping.get(phase, False)
    
    def is_resume_enabled(self) -> bool:
        """Check if resume is enabled"""
        return self.resume.enabled and self.resume.resume_from_phase is not None
    
    def get_resume_phase(self) -> Optional[str]:
        """Get the phase to resume from"""
        return self.resume.resume_from_phase if self.is_resume_enabled() else None
    
    def validate(self) -> List[str]:
        """Validate the configuration and return any errors"""
        errors = []
        
        # Check required fields
        if not self.experiment_id:
            errors.append("experiment_id is required")
        
        if not self.framework_path:
            errors.append("framework_path is required")
        
        if not self.corpus_path:
            errors.append("corpus_path is required")
        
        if not self.output_dir:
            errors.append("output_dir is required")
        
        # Check file existence
        from pathlib import Path
        
        if self.framework_path and not Path(self.framework_path).exists():
            errors.append(f"framework_path does not exist: {self.framework_path}")
        
        if self.corpus_path and not Path(self.corpus_path).exists():
            errors.append(f"corpus_path does not exist: {self.corpus_path}")
        
        # Check resume configuration
        if self.is_resume_enabled():
            if not self.resume.manifest_path:
                errors.append("manifest_path is required when resume is enabled")
            elif not Path(self.resume.manifest_path).exists():
                errors.append(f"manifest_path does not exist: {self.resume.manifest_path}")
        
        return errors
