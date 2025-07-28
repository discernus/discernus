"""
Local artifact storage with perfect caching.

Stores artifacts on local filesystem with content-addressable hashing.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional


class LocalArtifactStorage:
    """
    Local artifact storage with perfect caching.
    
    Stores artifacts on local filesystem with content-addressable hashing.
    """
    
    def __init__(self, artifacts_dir: Path):
        """
        Initialize artifact storage.
        
        Args:
            artifacts_dir: Directory to store artifacts
        """
        self.artifacts_dir = Path(artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create registry
        self.registry_path = self.artifacts_dir / "artifact_registry.json"
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                self.registry = json.load(f)
        else:
            self.registry = {}
            self._save_registry()
    
    def put_artifact(self, content: bytes, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store artifact with content-addressable hashing.
        
        Args:
            content: Artifact content
            metadata: Additional artifact metadata
            
        Returns:
            Content hash
        """
        # Generate content hash
        content_hash = hashlib.sha256(content).hexdigest()
        
        # Check if artifact already exists
        if content_hash in self.registry:
            # Update metadata if provided
            if metadata:
                self.registry[content_hash]["metadata"].update(metadata)
                self._save_registry()
            return content_hash
        
        # Store artifact
        artifact_path = self.artifacts_dir / content_hash
        artifact_path.write_bytes(content)
        
        # Update registry
        self.registry[content_hash] = {
            "path": str(artifact_path.relative_to(self.artifacts_dir)),
            "size": len(content),
            "metadata": metadata or {}
        }
        self._save_registry()
        
        return content_hash
    
    def get_artifact(self, content_hash: str) -> bytes:
        """
        Retrieve artifact by content hash.
        
        Args:
            content_hash: Content hash of artifact
            
        Returns:
            Artifact content
            
        Raises:
            KeyError: If artifact not found
        """
        if content_hash not in self.registry:
            raise KeyError(f"Artifact not found: {content_hash}")
        
        artifact_path = self.artifacts_dir / self.registry[content_hash]["path"]
        return artifact_path.read_bytes()
    
    def get_metadata(self, content_hash: str) -> Dict[str, Any]:
        """
        Get artifact metadata.
        
        Args:
            content_hash: Content hash of artifact
            
        Returns:
            Artifact metadata
            
        Raises:
            KeyError: If artifact not found
        """
        if content_hash not in self.registry:
            raise KeyError(f"Artifact not found: {content_hash}")
        
        return self.registry[content_hash]["metadata"]
    
    def _save_registry(self) -> None:
        """Save artifact registry to disk."""
        with open(self.registry_path, "w") as f:
            json.dump(self.registry, f, indent=2) 