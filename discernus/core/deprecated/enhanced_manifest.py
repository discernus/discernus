#!/usr/bin/env python3
"""
Enhanced Manifest System for Discernus THIN v2.0
=================================================

Creates comprehensive provenance manifests that combine:
- Input artifact hashes and metadata
- Execution timeline and performance metrics
- LLM interaction records and costs
- Artifact transformation chains
- Cache hit analysis for optimization

Provides the definitive record for experiment reproducibility and auditing.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage


class EnhancedManifest:
    """
    Enhanced manifest system that creates comprehensive provenance records
    by combining experiment metadata, audit logs, and artifact information.
    """
    
    def __init__(self, 
                 security_boundary: ExperimentSecurityBoundary, 
                 run_folder: Path,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        """
        Initialize enhanced manifest system.
        
        Args:
            security_boundary: Security boundary for file operations
            run_folder: The specific run folder for this experiment
            audit_logger: Audit logger instance for this run
            artifact_storage: Artifact storage instance for this run
        """
        self.security = security_boundary
        self.run_folder = security_boundary.validate_path(run_folder)
        self.audit = audit_logger
        self.storage = artifact_storage
        
        # Initialize manifest data structure
        self.manifest_data = {
            "manifest_version": "2.0",
            "created_at": self._get_timestamp(),
            "run_metadata": {},
            "experiment_config": {},
            "run_mode": {
                "mode_type": "standard",  # standard, analysis_only, statistical_prep, skip_synthesis
                "analysis_only": False,
                "statistical_prep": False,
                "skip_synthesis": False,
                "resume_from_stats": False,
                "ensemble_runs": None,
                "dry_run": False
            },
            "resume_capability": {
                "can_resume_from_stats": False,
                "statistical_prep_completed": False,
                "resume_artifacts": [],
                "resume_metadata": {}
            },
            "input_artifacts": {},
            "execution_timeline": [],
            "llm_interactions": [],
            "artifact_transformations": [],
            "performance_metrics": {},
            "cache_analysis": {
                "cache_hits": 0,
                "cache_misses": 0,
                "hit_rate": 0.0
            },
            "cost_tracking": {
                "total_cost_usd": 0.0
            },
            "quality_assurance": {},
            "audit_references": {}
        }
        
        # Use logger rather than print; initialization message recorded in session logs
        # (Keeping minimal to avoid noisy console output.)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat()
    
    def set_run_metadata(self, experiment_name: str, experiment_path: str, 
                        discernus_version: str = "thin_v2.0_alpha") -> None:
        """
        Set basic run metadata.
        
        Args:
            experiment_name: Name of the experiment
            experiment_path: Path to experiment directory
            discernus_version: Version of Discernus system
        """
        run_id = self.run_folder.name
        
        self.manifest_data["run_metadata"] = {
            "run_id": run_id,
            "experiment_name": experiment_name,
            "experiment_path": experiment_path,
            "discernus_version": discernus_version,
            "created_at": self.manifest_data["created_at"],
            "security_boundary": self.security.get_boundary_info(),
            "audit_session_id": self.audit.session_id
        }
        
        self.audit.log_orchestrator_event("manifest_metadata_set", {
            "run_id": run_id,
            "experiment_name": experiment_name
        })
    
    def set_experiment_config(self, config: Dict[str, Any]) -> None:
        """
        Set experiment configuration from experiment.md.
        
        Args:
            config: Experiment configuration dictionary
        """
        self.manifest_data["experiment_config"] = config.copy()
        
        self.audit.log_orchestrator_event("manifest_config_set", {
            "config_keys": list(config.keys())
        })
    
    def set_run_mode(self, analysis_only: bool = False, statistical_prep: bool = False, 
                    skip_synthesis: bool = False, resume_from_stats: bool = False,
                    ensemble_runs: Optional[int] = None, dry_run: bool = False) -> None:
        """
        Set run mode information for statistical preparation workflows.
        
        Args:
            analysis_only: Whether this is an analysis-only run
            statistical_prep: Whether this is a statistical preparation run
            skip_synthesis: Whether synthesis is being skipped
            resume_from_stats: Whether this is resuming from statistical preparation
            ensemble_runs: Number of ensemble runs (if any)
            dry_run: Whether this is a dry run
        """
        # Determine primary mode type
        if resume_from_stats:
            mode_type = "resume_from_stats"
        elif analysis_only:
            mode_type = "analysis_only"
        elif statistical_prep:
            mode_type = "statistical_prep"
        elif skip_synthesis:
            mode_type = "skip_synthesis"
        else:
            mode_type = "standard"
        
        self.manifest_data["run_mode"] = {
            "mode_type": mode_type,
            "analysis_only": analysis_only,
            "statistical_prep": statistical_prep,
            "skip_synthesis": skip_synthesis,
            "resume_from_stats": resume_from_stats,
            "ensemble_runs": ensemble_runs,
            "dry_run": dry_run
        }
        
        self.audit.log_orchestrator_event("manifest_run_mode_set", {
            "mode_type": mode_type,
            "statistical_prep": statistical_prep,
            "resume_from_stats": resume_from_stats
        })
    
    def set_resume_capability(self, can_resume: bool, statistical_prep_completed: bool = False,
                            resume_artifacts: List[str] = None, resume_metadata: Dict[str, Any] = None) -> None:
        """
        Set resume capability information for statistical preparation workflows.
        
        Args:
            can_resume: Whether this run can be resumed from statistical preparation
            statistical_prep_completed: Whether statistical preparation phase was completed
            resume_artifacts: List of artifact hashes needed for resume
            resume_metadata: Additional metadata for resume functionality
        """
        self.manifest_data["resume_capability"] = {
            "can_resume_from_stats": can_resume,
            "statistical_prep_completed": statistical_prep_completed,
            "resume_artifacts": resume_artifacts or [],
            "resume_metadata": resume_metadata or {}
        }
        
        self.audit.log_orchestrator_event("manifest_resume_capability_set", {
            "can_resume": can_resume,
            "statistical_prep_completed": statistical_prep_completed,
            "resume_artifacts_count": len(resume_artifacts) if resume_artifacts else 0
        })
    
    def add_input_artifact(self, artifact_type: str, artifact_hash: str, 
                          metadata: Dict[str, Any]) -> None:
        """
        Add input artifact to manifest.
        
        Args:
            artifact_type: Type of artifact (framework, experiment_config, corpus_document)
            artifact_hash: SHA-256 hash of the artifact
            metadata: Artifact metadata including original filename, size, etc.
        """
        self.manifest_data["input_artifacts"][artifact_type] = {
            "hash": artifact_hash,
            "metadata": metadata,
            "registered_at": self._get_timestamp()
        }
        
        self.audit.log_artifact_operation("input_registered", artifact_hash, artifact_type, metadata)
    
    def add_corpus_artifacts(self, corpus_hashes: List[str], corpus_metadata: List[Dict[str, Any]]) -> None:
        """
        Add corpus document artifacts to manifest.
        
        Args:
            corpus_hashes: List of SHA-256 hashes for corpus documents
            corpus_metadata: List of metadata dictionaries for each document
        """
        corpus_artifacts = []
        for i, (hash_id, metadata) in enumerate(zip(corpus_hashes, corpus_metadata)):
            artifact_info = {
                "hash": hash_id,
                "metadata": metadata,
                "document_index": i + 1,
                "registered_at": self._get_timestamp()
            }
            corpus_artifacts.append(artifact_info)
            
            self.audit.log_artifact_operation("corpus_document_registered", hash_id, "corpus_document", metadata)
        
        self.manifest_data["input_artifacts"]["corpus_documents"] = corpus_artifacts
    
    def add_execution_stage(self, stage_name: str, agent_name: str, 
                           start_time: str, end_time: Optional[str] = None,
                           status: str = "in_progress", 
                           metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add or update execution stage information.
        
        Args:
            stage_name: Name of the execution stage
            agent_name: Agent responsible for this stage
            start_time: Stage start timestamp
            end_time: Stage end timestamp (None if still in progress)
            status: Stage status (in_progress, completed, failed)
            metadata: Additional stage metadata
        """
        # Find existing stage or create new one
        existing_stage = None
        for stage in self.manifest_data["execution_timeline"]:
            if stage["stage_name"] == stage_name:
                existing_stage = stage
                break
        
        if existing_stage:
            # Update existing stage
            existing_stage.update({
                "end_time": end_time,
                "status": status,
                "duration_seconds": self._calculate_duration(existing_stage["start_time"], end_time) if end_time else None,
                "metadata": metadata or existing_stage.get("metadata", {})
            })
        else:
            # Create new stage
            stage_info = {
                "stage_name": stage_name,
                "agent_name": agent_name,
                "start_time": start_time,
                "end_time": end_time,
                "status": status,
                "duration_seconds": self._calculate_duration(start_time, end_time) if end_time else None,
                "metadata": metadata or {}
            }
            self.manifest_data["execution_timeline"].append(stage_info)
        
        self.audit.log_orchestrator_event("execution_stage_updated", {
            "stage_name": stage_name,
            "agent_name": agent_name,
            "status": status
        })
    
    def record_llm_interaction(self, interaction_hash: str, model: str, 
                              agent_name: str, stage: str,
                              prompt_length: int, response_length: int,
                              metadata: Dict[str, Any]) -> None:
        """
        Record LLM interaction in manifest.
        
        Args:
            interaction_hash: Hash reference from audit logger
            model: LLM model identifier
            agent_name: Agent that made the interaction
            stage: Processing stage this interaction belongs to
            prompt_length: Length of prompt in characters
            response_length: Length of response in characters
            metadata: Additional metadata (tokens, cost, etc.)
        """
        interaction_record = {
            "interaction_hash": interaction_hash,
            "model": model,
            "agent_name": agent_name,
            "stage": stage,
            "prompt_length": prompt_length,
            "response_length": response_length,
            "timestamp": self._get_timestamp(),
            "metadata": metadata
        }
        
        self.manifest_data["llm_interactions"].append(interaction_record)
        
        # Update cost tracking
        if "cost" in metadata:
            current_cost = self.manifest_data["cost_tracking"].get("total_cost_usd", 0.0)
            self.manifest_data["cost_tracking"]["total_cost_usd"] = current_cost + metadata["cost"]
    
    def record_artifact_transformation(self, stage: str, input_hashes: List[str], 
                                     output_hash: str, agent_name: str,
                                     llm_interaction_hash: Optional[str] = None,
                                     cache_status: str = "miss") -> None:
        """
        Record artifact transformation chain.
        
        Args:
            stage: Processing stage name
            input_hashes: List of input artifact hashes
            output_hash: Hash of produced output artifact
            agent_name: Agent that performed the transformation
            llm_interaction_hash: Reference to LLM interaction if applicable
            cache_status: Whether this was a cache hit or miss
        """
        transformation = {
            "stage": stage,
            "input_hashes": input_hashes,
            "output_hash": output_hash,
            "agent_name": agent_name,
            "llm_interaction_hash": llm_interaction_hash,
            "cache_status": cache_status,
            "timestamp": self._get_timestamp()
        }
        
        self.manifest_data["artifact_transformations"].append(transformation)
        
        # Update cache analysis
        cache_stats = self.manifest_data["cache_analysis"]
        current_hits = cache_stats.get("cache_hits", 0)
        current_misses = cache_stats.get("cache_misses", 0)
        
        if cache_status == "hit":
            cache_stats["cache_hits"] = current_hits + 1
        else:
            cache_stats["cache_misses"] = current_misses + 1
        
        total_operations = cache_stats["cache_hits"] + cache_stats["cache_misses"]
        cache_stats["hit_rate"] = cache_stats["cache_hits"] / total_operations if total_operations > 0 else 0.0
    
    def add_performance_metric(self, metric_name: str, value: Union[float, int],
                              stage: Optional[str] = None) -> None:
        """
        Add performance metric to manifest.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            stage: Optional stage this metric belongs to
        """
        if stage:
            stage_key = f"{stage}_{metric_name}"
        else:
            stage_key = metric_name
        
        self.manifest_data["performance_metrics"][stage_key] = {
            "value": value,
            "timestamp": self._get_timestamp(),
            "stage": stage
        }
    
    def set_quality_assurance_info(self, qa_data: Dict[str, Any]) -> None:
        """
        Set quality assurance information.
        
        Args:
            qa_data: Quality assurance data dictionary
        """
        self.manifest_data["quality_assurance"] = qa_data
    
    def finalize_manifest(self) -> str:
        """
        Finalize the manifest and save it to disk.
        
        Returns:
            Path to saved manifest file
        """
        # Add final timestamps
        self.manifest_data["finalized_at"] = self._get_timestamp()
        
        # Add audit trail references
        audit_summary = self.audit.get_session_summary()
        self.manifest_data["audit_references"] = audit_summary
        
        # Add artifact storage statistics
        storage_stats = self.storage.get_cache_stats()
        self.manifest_data["cache_analysis"]["artifact_storage"] = storage_stats
        
        # Calculate total execution time
        if self.manifest_data["execution_timeline"]:
            start_times = [stage["start_time"] for stage in self.manifest_data["execution_timeline"] if stage["start_time"]]
            end_times = [stage["end_time"] for stage in self.manifest_data["execution_timeline"] if stage["end_time"]]
            
            if start_times and end_times:
                earliest_start = min(start_times)
                latest_end = max(end_times)
                total_duration = self._calculate_duration(earliest_start, latest_end)
                self.manifest_data["performance_metrics"]["total_execution_time"] = {
                    "value": total_duration,
                    "unit": "seconds",
                    "start_time": earliest_start,
                    "end_time": latest_end
                }
        
        # Save manifest to file
        manifest_file = self.run_folder / "manifest.json"
        manifest_json = json.dumps(self.manifest_data, indent=2, sort_keys=True)
        self.security.secure_write_text(manifest_file, manifest_json)
        
        # Log manifest finalization
        self.audit.log_orchestrator_event("manifest_finalized", {
            "manifest_file": str(manifest_file.relative_to(self.security.experiment_root)),
            "total_stages": len(self.manifest_data["execution_timeline"]),
            "total_llm_interactions": len(self.manifest_data["llm_interactions"]),
            "total_artifacts": len(self.manifest_data["artifact_transformations"]),
            "cache_hit_rate": self.manifest_data["cache_analysis"].get("hit_rate", 0.0)
        })
        
        # Record save in logs if needed via external logger; avoid direct prints
        return str(manifest_file)
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        if not start or not end:
            return 0.0
        
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0
    
    def get_manifest_data(self) -> Dict[str, Any]:
        """Get current manifest data (for debugging/inspection)."""
        return self.manifest_data.copy()


def create_enhanced_manifest(security_boundary: ExperimentSecurityBoundary,
                           run_folder: Path,
                           audit_logger: AuditLogger,
                           artifact_storage: LocalArtifactStorage) -> EnhancedManifest:
    """Create an enhanced manifest instance."""
    return EnhancedManifest(security_boundary, run_folder, audit_logger, artifact_storage) 