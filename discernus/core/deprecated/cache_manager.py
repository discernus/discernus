#!/usr/bin/env python3
"""
Cache Manager
=============

Manages intelligent caching for the Show Your Work architecture using content-addressable storage.
"""

import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from discernus.core.local_artifact_storage import LocalArtifactStorage


class CacheManager:
    """Manages intelligent caching using content-addressable storage"""
    
    def __init__(self, storage: LocalArtifactStorage):
        """
        Initialize the cache manager
        
        Args:
            storage: The artifact storage instance
        """
        self.storage = storage
        self.cache_metadata = {}
    
    def get_cache_key(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Generate a cache key for content and metadata
        
        Args:
            content: The content to cache
            metadata: Associated metadata
            
        Returns:
            Cache key (SHA-256 hash)
        """
        # Create a deterministic key from content and relevant metadata
        key_data = {
            "content": content,
            "metadata": {k: v for k, v in metadata.items() if k not in ["timestamp", "cache_hits"]}
        }
        
        key_string = str(sorted(key_data.items()))
        return hashlib.sha256(key_string.encode('utf-8')).hexdigest()
    
    def get_cached_artifact(self, cache_key: str) -> Optional[bytes]:
        """
        Get a cached artifact by key
        
        Args:
            cache_key: The cache key
            
        Returns:
            Cached artifact content or None if not found
        """
        try:
            artifact = self.storage.get_artifact(cache_key)
            if artifact:
                # Update cache hit count
                self._update_cache_metadata(cache_key, {"last_accessed": datetime.now(timezone.utc).isoformat()})
                return artifact
        except Exception:
            # Artifact not found or error accessing
            pass
        
        return None
    
    def cache_artifact(self, content: bytes, metadata: Dict[str, Any]) -> str:
        """
        Cache an artifact
        
        Args:
            content: The content to cache
            metadata: Associated metadata
            
        Returns:
            Cache key
        """
        # Generate cache key from content
        cache_key = hashlib.sha256(content).hexdigest()
        
        # Store the artifact
        artifact_id = self.storage.put_artifact(content, metadata)
        
        # Update cache metadata
        self._update_cache_metadata(cache_key, {
            "artifact_id": artifact_id,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "size_bytes": len(content)
        })
        
        return cache_key
    
    def _update_cache_metadata(self, cache_key: str, updates: Dict[str, Any]) -> None:
        """Update cache metadata for a key"""
        if cache_key not in self.cache_metadata:
            self.cache_metadata[cache_key] = {}
        
        self.cache_metadata[cache_key].update(updates)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Cache statistics
        """
        total_keys = len(self.cache_metadata)
        total_size = sum(meta.get("size_bytes", 0) for meta in self.cache_metadata.values())
        
        return {
            "total_cached_items": total_keys,
            "total_size_bytes": total_size,
            "average_size_bytes": total_size / total_keys if total_keys > 0 else 0,
            "cache_metadata": self.cache_metadata
        }
    
    def clear_cache(self) -> None:
        """Clear all cached items"""
        self.cache_metadata.clear()
    
    def is_cached(self, cache_key: str) -> bool:
        """
        Check if an item is cached
        
        Args:
            cache_key: The cache key
            
        Returns:
            True if cached, False otherwise
        """
        return cache_key in self.cache_metadata
