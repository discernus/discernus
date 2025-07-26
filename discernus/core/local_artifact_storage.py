#!/usr/bin/env python3
"""
Local Artifact Storage for Discernus THIN v2.0
===============================================

Provides content-addressable storage using the local filesystem instead of MinIO.
Maintains the same SHA-256 hashing and caching behavior but stores artifacts
within the experiment's security boundary.

This enables the "restart = resume" behavior through artifact caching without
requiring external infrastructure dependencies.
"""

import hashlib
import json
from pathlib import Path
from typing import Union, Optional
from .security_boundary import ExperimentSecurityBoundary, SecurityError


class LocalArtifactStorageError(Exception):
    """Local artifact storage specific exceptions"""
    pass


class LocalArtifactStorage:
    """
    Content-addressable artifact storage using local filesystem.
    
    Stores artifacts in a secure directory structure using SHA-256 hashes
    as filenames, providing the same caching behavior as MinIO but without
    external dependencies.
    """
    
    def __init__(self, security_boundary: ExperimentSecurityBoundary, run_folder: Path):
        """
        Initialize local artifact storage.
        
        Args:
            security_boundary: Security boundary to enforce file access
            run_folder: The specific run folder for this experiment
        """
        self.security = security_boundary
        self.run_folder = security_boundary.validate_path(run_folder)
        
        # Create artifacts directory within the run folder
        self.artifacts_dir = self.security.secure_mkdir(run_folder / "artifacts")
        
        # Create a registry to track artifact metadata
        self.registry_file = self.artifacts_dir / "artifact_registry.json"
        self._load_registry()
        
        print(f"🗄️ Local artifact storage initialized: {self.artifacts_dir}")
    
    def _load_registry(self) -> None:
        """Load the artifact registry or create an empty one."""
        try:
            if self.registry_file.exists():
                content = self.security.secure_read_text(self.registry_file)
                self.registry = json.loads(content)
            else:
                self.registry = {}
        except Exception as e:
            print(f"⚠️ Warning: Could not load artifact registry, starting fresh: {e}")
            self.registry = {}
    
    def _save_registry(self) -> None:
        """Save the artifact registry."""
        try:
            registry_json = json.dumps(self.registry, indent=2, sort_keys=True)
            self.security.secure_write_text(self.registry_file, registry_json)
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to save artifact registry: {e}")
    
    def put_artifact(self, content: bytes, metadata: Optional[dict] = None) -> str:
        """
        Store content and return SHA256 hash.
        
        Args:
            content: Raw bytes to store
            metadata: Optional metadata about the artifact
            
        Returns:
            SHA-256 hash of the content
        """
        try:
            # Calculate SHA256 hash
            hash_id = hashlib.sha256(content).hexdigest()
            
            # Check if already exists (cache hit)
            if self.artifact_exists(hash_id):
                print(f"💾 Cache hit for artifact: {hash_id[:12]}...")
                return hash_id
            
            # Store the artifact
            artifact_path = self.artifacts_dir / hash_id
            self.security.secure_write_bytes(artifact_path, content)
            
            # Update registry with metadata
            self.registry[hash_id] = {
                "size_bytes": len(content),
                "created_at": self._get_timestamp(),
                "artifact_path": str(artifact_path.relative_to(self.run_folder)),
                "metadata": metadata or {}
            }
            self._save_registry()
            
            print(f"🗄️ Stored artifact: {hash_id[:12]}... ({len(content)} bytes)")
            return hash_id
            
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to store artifact: {e}")
    
    def get_artifact(self, hash_id: str) -> bytes:
        """
        Retrieve content by SHA256 hash.
        
        Args:
            hash_id: SHA-256 hash of the content
            
        Returns:
            Raw bytes of the artifact
        """
        try:
            if not self.artifact_exists(hash_id):
                raise LocalArtifactStorageError(f"Artifact not found: {hash_id}")
            
            artifact_path = self.artifacts_dir / hash_id
            content = self.security.secure_read_bytes(artifact_path)
            
            print(f"📥 Retrieved artifact: {hash_id[:12]}... ({len(content)} bytes)")
            return content
            
        except SecurityError as e:
            raise LocalArtifactStorageError(f"Security violation retrieving artifact: {e}")
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to retrieve artifact {hash_id}: {e}")
    
    def artifact_exists(self, hash_id: str) -> bool:
        """
        Check if artifact exists.
        
        Args:
            hash_id: SHA-256 hash to check
            
        Returns:
            True if artifact exists, False otherwise
        """
        try:
            artifact_path = self.artifacts_dir / hash_id
            return self.security.is_within_boundary(artifact_path) and artifact_path.exists()
        except Exception:
            return False
    
    def put_file(self, filepath: Union[str, Path], metadata: Optional[dict] = None) -> str:
        """
        Store file contents and return SHA256 hash.
        
        Args:
            filepath: Path to file to store
            metadata: Optional metadata about the file
            
        Returns:
            SHA-256 hash of the file contents
        """
        try:
            content = self.security.secure_read_bytes(filepath)
            
            # Add filename to metadata
            file_metadata = metadata or {}
            file_metadata["original_filename"] = Path(filepath).name
            
            return self.put_artifact(content, file_metadata)
            
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to store file {filepath}: {e}")
    
    def get_artifact_metadata(self, hash_id: str) -> dict:
        """
        Get metadata for an artifact.
        
        Args:
            hash_id: SHA-256 hash of the artifact
            
        Returns:
            Metadata dictionary
        """
        if hash_id not in self.registry:
            raise LocalArtifactStorageError(f"Artifact metadata not found: {hash_id}")
        
        return self.registry[hash_id].copy()
    
    def list_artifacts(self) -> list:
        """
        List all stored artifacts.
        
        Returns:
            List of artifact information dictionaries
        """
        artifacts = []
        for hash_id, info in self.registry.items():
            artifacts.append({
                "hash_id": hash_id,
                "size_bytes": info["size_bytes"],
                "created_at": info["created_at"],
                "metadata": info.get("metadata", {})
            })
        
        return sorted(artifacts, key=lambda x: x["created_at"], reverse=True)
    
    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_artifacts = len(self.registry)
        total_bytes = sum(info["size_bytes"] for info in self.registry.values())
        
        return {
            "total_artifacts": total_artifacts,
            "total_bytes": total_bytes,
            "total_mb": round(total_bytes / (1024 * 1024), 2),
            "artifacts_dir": str(self.artifacts_dir)
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()


# Convenience functions for backward compatibility with MinIO client
def create_local_storage(security_boundary: ExperimentSecurityBoundary, run_folder: Path) -> LocalArtifactStorage:
    """Create a local artifact storage instance."""
    return LocalArtifactStorage(security_boundary, run_folder) 