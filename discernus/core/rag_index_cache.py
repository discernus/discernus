#!/usr/bin/env python3
"""
RAG Index Cache Manager

Manages caching of txtai RAG indexes to eliminate redundant rebuilding
and improve development velocity. Follows the same pattern as other
caching managers in the system.
"""

import hashlib
import json
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, NamedTuple
from dataclasses import dataclass

try:
    from txtai.embeddings import Embeddings
except ImportError:
    raise ImportError("txtai is required. Install with: pip install txtai")

from .local_artifact_storage import LocalArtifactStorage
from .audit_logger import AuditLogger


@dataclass
class RAGCacheResult:
    """Result of RAG index cache lookup."""
    hit: bool
    cached_index: Optional[Embeddings] = None
    cache_key: str = ""
    artifact_hash: str = ""


class RAGIndexCacheManager:
    """
    Manages caching of txtai RAG indexes for performance optimization.
    
    Provides deterministic caching based on evidence artifact hashes,
    eliminating the need to rebuild RAG indexes when evidence hasn't changed.
    
    Key Features:
    - Deterministic cache keys based on evidence artifact content
    - txtai index save/load functionality
    - Integration with LocalArtifactStorage
    - Follows established caching patterns
    """
    
    def __init__(self, artifact_storage: LocalArtifactStorage, audit_logger: AuditLogger):
        """Initialize RAG index cache manager."""
        self.artifact_storage = artifact_storage
        self.audit_logger = audit_logger
        self.agent_name = "RAGIndexCacheManager"
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name, 
                "initialization", 
                {"cache_type": "rag_index"}
            )
    
    def generate_cache_key(self, evidence_artifact_hashes: List[str]) -> str:
        """
        Generate deterministic cache key based on evidence artifacts.
        
        Args:
            evidence_artifact_hashes: List of evidence artifact hashes
            
        Returns:
            Deterministic cache key string
        """
        if not evidence_artifact_hashes:
            return "rag_index_empty"
        
        # Sort hashes for deterministic key generation
        sorted_hashes = sorted(evidence_artifact_hashes)
        
        # Create combined hash of all evidence artifact hashes
        combined_content = '|'.join(sorted_hashes)
        combined_hash = hashlib.sha256(combined_content.encode('utf-8')).hexdigest()[:16]
        
        cache_key = f"rag_index_{combined_hash}"
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "cache_key_generated",
                {
                    "cache_key": cache_key,
                    "evidence_count": len(evidence_artifact_hashes),
                    "input_hash": combined_hash
                }
            )
        
        return cache_key
    
    def check_cache(self, cache_key: str) -> RAGCacheResult:
        """
        Check if RAG index exists in cache.
        
        Args:
            cache_key: Cache key to look up
            
        Returns:
            RAGCacheResult with hit status and cached index if found
        """
        try:
            # Look for cached index in artifact storage
            for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                metadata = artifact_info.get("metadata", {})
                if (metadata.get("artifact_type") == "rag_index_cache" and 
                    metadata.get("rag_cache_key") == cache_key):
                    
                    # Verify artifact actually exists before attempting to load
                    if not self.artifact_storage.artifact_exists(artifact_hash):
                        print(f"⚠️ Cache metadata found but artifact missing: {cache_key} (hash: {artifact_hash[:8]})")
                        continue
                    
                    # Load the cached index
                    cached_index = self._load_index_from_artifact(artifact_hash)
                    if cached_index is not None:
                        if self.audit_logger:
                            self.audit_logger.log_agent_event(
                                self.agent_name,
                                "cache_hit",
                                {
                                    "cache_key": cache_key,
                                    "artifact_hash": artifact_hash[:8]
                                }
                            )
                        
                        return RAGCacheResult(
                            hit=True,
                            cached_index=cached_index,
                            cache_key=cache_key,
                            artifact_hash=artifact_hash
                        )
            
            # Cache miss
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "cache_miss",
                    {"cache_key": cache_key}
                )
            
            return RAGCacheResult(hit=False, cache_key=cache_key)
            
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error(
                    "rag_cache_check_failed",
                    str(e),
                    {"cache_key": cache_key, "agent": self.agent_name}
                )
            return RAGCacheResult(hit=False, cache_key=cache_key)
    
    def store_index(self, cache_key: str, index: Embeddings, evidence_count: int = 0) -> str:
        """
        Store RAG index in cache with complete persistence of documents attribute.

        Args:
            cache_key: Cache key for the index
            index: txtai Embeddings index to cache
            evidence_count: Number of evidence pieces indexed

        Returns:
            Artifact hash of stored index
        """
        try:
            # Create temporary directory for index storage
            temp_dir = Path(tempfile.mkdtemp())
            index_path = temp_dir / "rag_index"

            try:
                # Save txtai index to temporary location
                index.save(str(index_path))

                # Preserve custom documents attribute if it exists
                documents_data = None
                if hasattr(index, 'documents') and index.documents:
                    documents_path = temp_dir / "documents.json"
                    with open(documents_path, 'w', encoding='utf-8') as f:
                        json.dump(index.documents, f, ensure_ascii=False, indent=2)
                    documents_data = documents_path

                # txtai saves indexes as directories, so we need to tar them up
                import tarfile
                tar_path = temp_dir / "rag_index.tar.gz"

                with tarfile.open(tar_path, 'w:gz') as tar:
                    if index_path.exists():
                        if index_path.is_dir():
                            # Add directory contents
                            tar.add(index_path, arcname='rag_index')
                        else:
                            # Single file (shouldn't happen with txtai but handle it)
                            tar.add(index_path, arcname='rag_index')

                    # Add documents.json if it exists (for provenance and future use)
                    if documents_data and documents_data.exists():
                        tar.add(documents_data, arcname='documents.json')

                with open(tar_path, 'rb') as f:
                    index_data = f.read()

                # Store as artifact with enhanced metadata
                metadata = {
                    "artifact_type": "rag_index_cache",
                    "rag_cache_key": cache_key,
                    "evidence_count": evidence_count,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "index_size_bytes": len(index_data),
                    "has_documents": documents_data is not None,
                    "documents_count": len(index.documents) if hasattr(index, 'documents') and index.documents else 0
                }

                artifact_hash = self.artifact_storage.put_artifact(index_data, metadata)

                if self.audit_logger:
                    self.audit_logger.log_agent_event(
                        self.agent_name,
                        "index_cached",
                        {
                            "cache_key": cache_key,
                            "artifact_hash": artifact_hash[:8],
                            "evidence_count": evidence_count,
                            "size_bytes": len(index_data),
                            "has_documents": metadata["has_documents"],
                            "documents_count": metadata["documents_count"]
                        }
                    )

                return artifact_hash

            finally:
                # Cleanup temporary directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error(
                    "rag_index_cache_store_failed",
                    str(e),
                    {"cache_key": cache_key, "agent": self.agent_name}
                )
            raise Exception(f"Failed to store RAG index in cache: {e}")
    
    def _load_index_from_artifact(self, artifact_hash: str) -> Optional[Embeddings]:
        """
        Load txtai index from artifact storage with complete documents attribute restoration.

        Args:
            artifact_hash: Hash of cached index artifact

        Returns:
            Loaded txtai Embeddings index or None if failed
        """
        try:
            # Retrieve cached index data
            index_data = self.artifact_storage.get_artifact(artifact_hash)
            if not index_data:
                return None

            # Create temporary directory for loading
            temp_dir = Path(tempfile.mkdtemp())

            try:
                # All cached indexes are tar.gz files (since txtai saves as directories)
                import tarfile
                tar_path = temp_dir / "rag_index.tar.gz"

                # Write the cached data to tar file
                with open(tar_path, 'wb') as f:
                    f.write(index_data)

                # Extract the tar file (with filter for Python 3.14 compatibility)
                with tarfile.open(tar_path, 'r:gz') as tar:
                    # Use data filter for security (Python 3.12+)
                    try:
                        tar.extractall(temp_dir, filter='data')
                    except TypeError:
                        # Fallback for older Python versions
                        tar.extractall(temp_dir)

                index_path = temp_dir / "rag_index"
                documents_path = temp_dir / "documents.json"

                # Load txtai index
                embeddings = Embeddings()
                embeddings.load(str(index_path))

                # Restore documents attribute if it exists (for provenance and future use)
                if documents_path.exists():
                    try:
                        with open(documents_path, 'r', encoding='utf-8') as f:
                            embeddings.documents = json.load(f)

                        if self.audit_logger:
                            self.audit_logger.log_agent_event(
                                self.agent_name,
                                "documents_restored",
                                {
                                    "artifact_hash": artifact_hash[:8],
                                    "documents_count": len(embeddings.documents)
                                }
                            )
                    except Exception as e:
                        if self.audit_logger:
                            self.audit_logger.log_error(
                                "documents_restore_failed",
                                str(e),
                                {"artifact_hash": artifact_hash[:8], "agent": self.agent_name}
                            )
                        # Set empty documents list as fallback
                        embeddings.documents = []
                else:
                    # No documents.json found - create empty list for compatibility
                    embeddings.documents = []

                return embeddings

            finally:
                # Cleanup temporary directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error(
                    "rag_index_load_failed",
                    str(e),
                    {"artifact_hash": artifact_hash[:8], "agent": self.agent_name}
                )
            return None
    
    def get_cache_stats(self) -> dict:
        """Get statistics about cached RAG indexes."""
        stats = {
            "total_cached_indexes": 0,
            "total_cache_size_bytes": 0,
            "cache_keys": []
        }
        
        try:
            for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                metadata = artifact_info.get("metadata", {})
                if metadata.get("artifact_type") == "rag_index_cache":
                    stats["total_cached_indexes"] += 1
                    stats["total_cache_size_bytes"] += metadata.get("index_size_bytes", 0)
                    stats["cache_keys"].append({
                        "cache_key": metadata.get("rag_cache_key"),
                        "evidence_count": metadata.get("evidence_count", 0),
                        "created_at": metadata.get("created_at"),
                        "size_bytes": metadata.get("index_size_bytes", 0)
                    })
        except Exception:
            pass
        
        return stats
