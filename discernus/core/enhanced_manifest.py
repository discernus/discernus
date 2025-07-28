"""
Enhanced manifest for experiment provenance.

Records experiment configuration, inputs, outputs, and execution timeline.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional


class EnhancedManifest:
    """
    Enhanced manifest for experiment provenance.
    
    Records experiment configuration, inputs, outputs, and execution timeline.
    """
    
    def __init__(self, manifest_path: Path):
        """
        Initialize manifest.
        
        Args:
            manifest_path: Path to manifest file
        """
        self.manifest_path = Path(manifest_path)
        
        # Initialize manifest structure
        self.manifest = {
            "manifest_version": "2.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "finalized_at": None,
            "run_metadata": {},
            "experiment_config": {},
            "input_artifacts": {},
            "output_artifacts": {},
            "execution_timeline": [],
            "audit_references": {},
            "cache_analysis": {
                "cache_hits": 0,
                "cache_misses": 0,
                "hit_rate": 0.0,
                "artifact_storage": {
                    "artifacts_dir": "",
                    "total_artifacts": 0,
                    "total_bytes": 0,
                    "total_mb": 0.0
                }
            },
            "cost_tracking": {
                "total_cost_usd": 0.0
            },
            "quality_assurance": {}
        }
        
        # Save initial manifest
        self._save_manifest()
    
    def set_run_metadata(self, experiment_name: str, experiment_path: str, version: str) -> None:
        """
        Set run metadata.
        
        Args:
            experiment_name: Name of experiment
            experiment_path: Path to experiment directory
            version: Discernus version
        """
        self.manifest["run_metadata"] = {
            "experiment_name": experiment_name,
            "experiment_path": experiment_path,
            "discernus_version": version,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "security_boundary": {
                "boundary_type": "filesystem",
                "security_level": "experiment_scoped",
                "experiment_name": experiment_name,
                "experiment_root": experiment_path
            }
        }
        self._save_manifest()
    
    def set_experiment_config(self, config: Dict[str, Any]) -> None:
        """
        Set experiment configuration.
        
        Args:
            config: Experiment configuration
        """
        self.manifest["experiment_config"] = config
        self._save_manifest()
    
    def add_input_artifact(self, artifact_type: str, artifact_hash: str, metadata: Dict[str, Any]) -> None:
        """
        Add input artifact.
        
        Args:
            artifact_type: Type of artifact
            artifact_hash: Content hash of artifact
            metadata: Artifact metadata
        """
        if artifact_type not in self.manifest["input_artifacts"]:
            self.manifest["input_artifacts"][artifact_type] = {
                "hash": artifact_hash,
                "metadata": metadata,
                "registered_at": datetime.now(timezone.utc).isoformat()
            }
        self._save_manifest()
    
    def add_corpus_artifacts(self, artifact_hashes: List[str], metadata_list: List[Dict[str, Any]]) -> None:
        """
        Add corpus artifacts.
        
        Args:
            artifact_hashes: List of content hashes
            metadata_list: List of artifact metadata
        """
        self.manifest["input_artifacts"]["corpus_documents"] = []
        for i, (artifact_hash, metadata) in enumerate(zip(artifact_hashes, metadata_list), 1):
            self.manifest["input_artifacts"]["corpus_documents"].append({
                "document_index": i,
                "hash": artifact_hash,
                "metadata": metadata,
                "registered_at": datetime.now(timezone.utc).isoformat()
            })
        self._save_manifest()
    
    def add_output_artifact(self, artifact_type: str, artifact_hash: str, metadata: Dict[str, Any]) -> None:
        """
        Add output artifact.
        
        Args:
            artifact_type: Type of artifact
            artifact_hash: Content hash of artifact
            metadata: Artifact metadata
        """
        if artifact_type not in self.manifest["output_artifacts"]:
            self.manifest["output_artifacts"][artifact_type] = {
                "hash": artifact_hash,
                "metadata": metadata,
                "registered_at": datetime.now(timezone.utc).isoformat()
            }
        self._save_manifest()
    
    def add_execution_stage(self, stage_name: str, start_time: str, end_time: str,
                          status: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add execution stage.
        
        Args:
            stage_name: Name of stage
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            status: Stage status
            metadata: Additional stage metadata
        """
        stage = {
            "stage_name": stage_name,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": (
                datetime.fromisoformat(end_time) -
                datetime.fromisoformat(start_time)
            ).total_seconds(),
            "status": status,
            "metadata": metadata or {}
        }
        self.manifest["execution_timeline"].append(stage)
        self._save_manifest()
    
    def set_audit_references(self, session_id: str, logs_directory: str,
                           log_files: Dict[str, str]) -> None:
        """
        Set audit references.
        
        Args:
            session_id: Audit session ID
            logs_directory: Path to logs directory
            log_files: Mapping of log types to file paths
        """
        self.manifest["audit_references"] = {
            "session_id": session_id,
            "logs_directory": logs_directory,
            "log_files": log_files,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "current_time": datetime.now(timezone.utc).isoformat()
        }
        self._save_manifest()
    
    def update_cache_analysis(self, hits: int, misses: int, artifacts_dir: str,
                            total_artifacts: int, total_bytes: int) -> None:
        """
        Update cache analysis.
        
        Args:
            hits: Number of cache hits
            misses: Number of cache misses
            artifacts_dir: Path to artifacts directory
            total_artifacts: Total number of artifacts
            total_bytes: Total size in bytes
        """
        total_requests = hits + misses
        hit_rate = hits / total_requests if total_requests > 0 else 0.0
        
        self.manifest["cache_analysis"] = {
            "cache_hits": hits,
            "cache_misses": misses,
            "hit_rate": hit_rate,
            "artifact_storage": {
                "artifacts_dir": artifacts_dir,
                "total_artifacts": total_artifacts,
                "total_bytes": total_bytes,
                "total_mb": total_bytes / (1024 * 1024)
            }
        }
        self._save_manifest()
    
    def update_cost_tracking(self, total_cost_usd: float) -> None:
        """
        Update cost tracking.
        
        Args:
            total_cost_usd: Total cost in USD
        """
        self.manifest["cost_tracking"]["total_cost_usd"] = total_cost_usd
        self._save_manifest()
    
    def finalize(self) -> None:
        """Finalize manifest."""
        self.manifest["finalized_at"] = datetime.now(timezone.utc).isoformat()
        self._save_manifest()
    
    def _save_manifest(self) -> None:
        """Save manifest to disk."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2) 