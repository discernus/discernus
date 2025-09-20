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
from typing import Union, Optional, Dict, Any
from .security_boundary import ExperimentSecurityBoundary, SecurityError
import shutil


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
    
    def __init__(self, security_boundary: ExperimentSecurityBoundary, run_folder: Path, run_name: Optional[str] = None):
        """
        Initialize local artifact storage.
        
        Args:
            security_boundary: Security boundary to enforce file access
            run_folder: The specific run folder for this experiment  
            run_name: Optional explicit run name for source_run tracking (defaults to run_folder.name)
        """
        self.security = security_boundary
        self.run_folder = security_boundary.validate_path(run_folder)
        self.run_name = run_name or run_folder.name
        
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
        Store content with human-readable filename and return SHA256 hash.
        
        Args:
            content: Raw bytes to store
            metadata: Optional metadata about the artifact
            
        Returns:
            SHA-256 hash of the content
        """
        try:
            # Calculate SHA256 hash
            hash_id = hashlib.sha256(content).hexdigest()
            short_hash = hash_id[:8]
            
            # Generate human-readable filename
            human_filename = self._generate_human_filename(metadata, short_hash)
            
            # Check if already exists (cache hit)
            if self.artifact_exists(hash_id):
                pass  # Reduced verbosity - cache hit
                return hash_id
            
            # Store the artifact with human-readable filename
            artifact_path = self.artifacts_dir / human_filename
            self.security.secure_write_bytes(artifact_path, content)
            
            # Update registry with metadata
            self._register_artifact(
                hash_id,
                metadata,
                size_bytes=len(content),
                human_filename=human_filename,
            )
            
            pass  # Reduced verbosity - stored artifact
            return hash_id
            
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to store artifact: {e}")

    def store_artifact(self, *args, **kwargs) -> str:
        """
        Adapter method for backward compatibility with store_artifact calls.
        
        Handles different calling patterns:
        1. store_artifact(name, data) - from agent_base_classes
        2. store_artifact(content=..., artifact_type=..., experiment_id=...) - from evidence retriever
        
        Returns:
            SHA-256 hash of the stored content
        """
        try:
            # Handle named parameter calls (evidence retriever pattern)
            if 'content' in kwargs:
                content = kwargs['content']
                # Build metadata from other parameters
                metadata = {}
                if 'artifact_type' in kwargs:
                    metadata['artifact_type'] = kwargs['artifact_type']
                if 'experiment_id' in kwargs:
                    metadata['experiment_id'] = kwargs['experiment_id']
                
                # Convert content to bytes if needed
                if isinstance(content, dict):
                    import json
                    content = json.dumps(content, indent=2).encode('utf-8')
                elif isinstance(content, str):
                    content = content.encode('utf-8')
                
                return self.put_artifact(content, metadata)
            
            # Handle positional calls (agent_base_classes pattern) 
            elif len(args) >= 2:
                name, data = args[0], args[1]
                # Convert data to bytes
                if isinstance(data, dict):
                    import json
                    content = json.dumps(data, indent=2).encode('utf-8')
                elif isinstance(data, str):
                    content = data.encode('utf-8')
                else:
                    content = str(data).encode('utf-8')
                
                metadata = {
                    'artifact_name': name,
                    'artifact_type': 'tool_call_data'
                }
                return self.put_artifact(content, metadata)
            
            else:
                raise LocalArtifactStorageError("Invalid arguments for store_artifact")
                
        except Exception as e:
            raise LocalArtifactStorageError(f"Failed to store artifact: {e}")

    def _register_artifact(
        self,
        hash_id: str,
        metadata: Dict[str, Any],
        size_bytes: Optional[int] = None,
        human_filename: Optional[str] = None,
        is_directory: bool = False,
    ):
        """Register an artifact in the registry."""
        relative_path = human_filename or hash_id
        self.registry[hash_id] = {
            "size_bytes": size_bytes,
            "created_at": self._get_timestamp(),
            "artifact_path": relative_path,
            "human_filename": human_filename,
            "metadata": metadata or {},
            "source_run": self.run_name,
            "is_directory": is_directory,
        }
        self._save_registry()
    
    def _generate_human_filename(self, metadata: Optional[dict], short_hash: str) -> str:
        """
        Generate human-readable filename with crypto hash.
        
        Args:
            metadata: Artifact metadata
            short_hash: 8-character hash for uniqueness
            
        Returns:
            Human-readable filename like 'analysis_response_mccain_concession_04d1d18a.json'
        """
        if not metadata:
            return f"artifact_{short_hash}"
        
        artifact_type = metadata.get("artifact_type", "unknown")
        
        # Generate descriptive name based on type and content
        if artifact_type == "analysis_json_v6":
            return f"analysis_response_{short_hash}.json"
        elif artifact_type == "statistical_results":
            return f"statistical_results_{short_hash}.json"
        elif artifact_type == "curated_evidence":
            return f"curated_evidence_{short_hash}.json"
        elif artifact_type == "analysis_plan":
            return f"analysis_plan_{short_hash}.md"
        elif artifact_type == "final_report":
            timestamp = self._get_timestamp()[:10]  # YYYY-MM-DD
            return f"final_report_{timestamp}_{short_hash}.md"
        elif artifact_type == "synthesis_report":
            timestamp = self._get_timestamp()[:10]  # YYYY-MM-DD
            return f"synthesis_report_{timestamp}_{short_hash}.md"
        elif artifact_type == "corpus_document":
            # Extract meaningful name from original_filename
            original_name = metadata.get("original_filename", "")
            if original_name:
                # Extract just the filename without path and extension
                base_name = Path(original_name).stem
                extension = Path(original_name).suffix or ".txt"
                return f"{base_name}_{short_hash}{extension}"
            return f"corpus_document_{short_hash}.txt"
        elif artifact_type == "framework":
            # Extract framework name from original_filename
            original_name = metadata.get("original_filename", "")
            if original_name:
                # Extract just the filename without path and extension
                base_name = Path(original_name).stem
                extension = Path(original_name).suffix or ".md"
                return f"{base_name}_{short_hash}{extension}"
            return f"framework_{short_hash}.md"
        elif artifact_type == "composite_analysis":
            return f"composite_analysis_{short_hash}.json"
        elif artifact_type == "evidence_extraction":
            return f"evidence_extraction_{short_hash}.json"
        elif artifact_type == "score_extraction":
            return f"score_extraction_{short_hash}.json"
        elif artifact_type == "derived_metrics":
            return f"derived_metrics_{short_hash}.json"
        elif artifact_type == "verification":
            return f"verification_{short_hash}.json"
        elif artifact_type == "marked_up_document":
            return f"marked_up_document_{short_hash}.md"
        elif artifact_type == "statistical_analysis":
            return f"statistical_analysis_{short_hash}.json"
        elif artifact_type == "statistical_verification":
            return f"statistical_verification_{short_hash}.json"
        elif artifact_type == "statistical_analysis_cache":
            return f"statistical_analysis_cache_{short_hash}.json"
        elif artifact_type == "csv_generation":
            return f"csv_generation_{short_hash}.json"
        elif artifact_type == "evidence_retrieval":
            return f"evidence_retrieval_{short_hash}.json"
        elif artifact_type == "validation_report":
            return f"validation_report_{short_hash}.json"
        elif artifact_type == "synthesis_report_v2_markdown":
            return f"synthesis_report_v2_markdown_{short_hash}.md"
        else:
            return f"{artifact_type}_{short_hash}"
    
    def get_artifact(self, hash_id: str, quiet: bool = False) -> bytes:
        """
        Retrieve content by SHA256 hash.
        
        Args:
            hash_id: SHA-256 hash of the content
            quiet: If True, suppress retrieval logging (useful for bulk operations)
            
        Returns:
            Raw bytes of the artifact
        """
        try:
            if not self.artifact_exists(hash_id):
                raise LocalArtifactStorageError(f"Artifact not found: {hash_id}")
            
            # Get human filename from registry
            human_filename = self.registry[hash_id].get("human_filename", hash_id)
            artifact_path = self.artifacts_dir / human_filename
            
            # Fallback to hash-based filename for legacy artifacts
            if not artifact_path.exists():
                artifact_path = self.artifacts_dir / hash_id
            
            content = self.security.secure_read_bytes(artifact_path)
            
            # Only log if not in quiet mode
            if not quiet:
                pass  # Reduced verbosity - retrieved artifact
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
            if hash_id not in self.registry:
                return False
            
            # Check if the actual file exists
            human_filename = self.registry[hash_id].get("human_filename", hash_id)
            artifact_path = self.artifacts_dir / human_filename
            
            # Fallback to hash-based filename for legacy artifacts
            if not artifact_path.exists():
                artifact_path = self.artifacts_dir / hash_id
                
            return self.security.is_within_boundary(artifact_path) and artifact_path.exists()
        except Exception:
            return False

    def _calculate_content_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of content."""
        return hashlib.sha256(content).hexdigest()

    def put_directory_artifact(
        self, source_dir: Path, metadata: Dict[str, Any]
    ) -> str:
        """
        Store a directory as a content-addressable artifact.

        Args:
            source_dir: The path to the source directory to store.
            metadata: A dictionary of metadata to associate with the artifact.

        Returns:
            The SHA-256 hash of the directory contents.
        """
        if not source_dir.is_dir():
            raise LocalArtifactStorageError(f"Source path is not a directory: {source_dir}")

        dir_hash = self._calculate_directory_hash(source_dir)
        target_dir = self.artifacts_dir / dir_hash

        if not target_dir.exists():
            shutil.copytree(source_dir, target_dir)
            self._register_artifact(
                dir_hash,
                metadata,
                is_directory=True,
                human_filename=dir_hash,  # Use hash as the "filename" for directories
            )
        
        return dir_hash

    def get_directory_artifact_path(self, dir_hash: str) -> Path:
        """
        Get the path to a stored directory artifact.

        Args:
            dir_hash: The hash of the directory artifact.

        Returns:
            The path to the artifact directory.
        """
        artifact_path = self.artifacts_dir / dir_hash
        if not self.artifact_exists(dir_hash) or not artifact_path.is_dir():
            raise LocalArtifactStorageError(f"Directory artifact not found: {dir_hash}")
        return artifact_path

    def _calculate_directory_hash(self, directory: Path) -> str:
        """
        Calculate a deterministic SHA-256 hash for a directory's contents.
        """
        hasher = hashlib.sha256()
        # We sort the paths to ensure the hash is consistent regardless of
        # filesystem order.
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                # Add relative path to the hash to account for structure
                hasher.update(str(path.relative_to(directory)).encode())
                # Add file content to the hash
                with open(path, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
        return hasher.hexdigest()
    
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
    
    def cleanup_orphaned_entries(self, quiet: bool = False) -> Dict[str, int]:
        """
        Remove orphaned registry entries for artifacts that no longer exist on disk.
        
        Args:
            quiet: If True, suppress progress messages
            
        Returns:
            Dictionary with cleanup statistics
        """
        if not quiet:
            print("🧹 Cleaning up orphaned artifact registry entries...")
        
        orphaned_entries = []
        valid_entries = {}
        
        for hash_id, info in self.registry.items():
            artifact_path = self.artifacts_dir / info.get("artifact_path", f"artifact_{hash_id[:8]}")
            
            if artifact_path.exists():
                # Artifact file exists, keep the registry entry
                valid_entries[hash_id] = info
            else:
                # Artifact file missing, mark as orphaned
                orphaned_entries.append(hash_id)
                if not quiet:
                    print(f"   🗑️  Removing orphaned entry: {info.get('human_filename', hash_id[:12])}")
        
        # Update registry with only valid entries
        if orphaned_entries:
            self.registry = valid_entries
            self._save_registry()
            
            if not quiet:
                print(f"✅ Cleanup complete: removed {len(orphaned_entries)} orphaned entries")
        else:
            if not quiet:
                print("✅ No orphaned entries found - registry is clean")
        
        return {
            "orphaned_removed": len(orphaned_entries),
            "valid_entries": len(valid_entries),
            "total_processed": len(orphaned_entries) + len(valid_entries)
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()


# Convenience functions for backward compatibility with MinIO client
def create_local_storage(security_boundary: ExperimentSecurityBoundary, run_folder: Path) -> LocalArtifactStorage:
    """Create a local artifact storage instance."""
    return LocalArtifactStorage(security_boundary, run_folder) 