#!/usr/bin/env python3
"""
Validation Cache Manager - THIN Component
=========================================

Manages caching of experiment coherence validation results for development velocity.
Pure software component - no LLM intelligence.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


@dataclass
class ValidationCacheResult:
    """Result of validation cache lookup."""
    hit: bool
    artifact_hash: Optional[str] = None
    cached_validation: Optional[Dict[str, Any]] = None


class ValidationCacheManager:
    """
    Manages caching of experiment coherence validation using content-addressable storage.
    
    THIN Principle: Pure software caching infrastructure.
    No LLM intelligence - just deterministic cache management.
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger):
        self.storage = storage
        self.audit = audit
    
    def generate_cache_key(self, framework_content: str, experiment_content: str, 
                          corpus_content: str, model: str) -> str:
        """
        Generate deterministic cache key for validation results.
        
        Args:
            framework_content: Framework markdown content
            experiment_content: Experiment markdown content
            corpus_content: Corpus manifest content
            model: LLM model used for validation
            
        Returns:
            Deterministic cache key based on content hashes and model
        """
        # Combine all input content for cache key
        combined_content = f'{framework_content}{experiment_content}{corpus_content}{model}'
        cache_hash = hashlib.sha256(combined_content.encode()).hexdigest()[:12]
        
        return f"validation_{cache_hash}"
    
    def check_cache(self, cache_key: str, agent_name: str = "ExperimentCoherenceAgent") -> ValidationCacheResult:
        """
        Check if validation result is already cached.
        
        Args:
            cache_key: Cache key for lookup
            agent_name: Name of the agent for logging
            
        Returns:
            ValidationCacheResult indicating hit/miss and cached validation if available
        """
        # Search through artifact registry for matching validation result
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "validation_result" and
                metadata.get("cache_key") == cache_key):
                
                # Verify artifact actually exists before claiming cache hit
                if not self.storage.artifact_exists(artifact_hash):
                    print(f"⚠️ Cache metadata found but artifact missing: {cache_key} (hash: {artifact_hash[:8]})")
                    continue
                
                # Cache hit!
                pass  # Reduced verbosity - validation cache hit
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_validation = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(agent_name, "cache_hit", {
                        "cache_key": cache_key,
                        "cached_artifact_hash": artifact_hash,
                        "phase": "validation"
                    })
                    
                    return ValidationCacheResult(
                        hit=True,
                        artifact_hash=artifact_hash,
                        cached_validation=cached_validation
                    )
                    
                except Exception as e:
                    print(f"⚠️ Cache hit but failed to load validation result: {e}")
                    # Continue searching for other cached results
                    continue
        
        # No cache hit
        pass  # Reduced verbosity - no validation cache hit
        return ValidationCacheResult(hit=False)
    
    def store_validation_result(self, cache_key: str, validation_result: Dict[str, Any], 
                               model: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store validation result in cache for future use.
        
        Args:
            cache_key: Cache key for the validation
            validation_result: Complete validation result to cache
            model: Model used for validation
            metadata: Additional metadata for the artifact
            
        Returns:
            Hash of the stored artifact
        """
        # Add cache-specific metadata
        cache_metadata = {
            **(metadata or {}),
            "artifact_type": "validation_result",
            "cache_key": cache_key,
            "validation_model": model,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "success": validation_result.get('success', False)
        }
        
        # Store the validation result
        validation_json = json.dumps(validation_result, indent=2)
        artifact_hash = self.storage.put_artifact(
            validation_json.encode('utf-8'),
            cache_metadata
        )
        
        print(f"💾 Stored validation result in cache: {cache_key} (success: {validation_result.get('success', False)})")
        self.audit.log_agent_event("ExperimentCoherenceAgent", "cache_store", {
            "cache_key": cache_key,
            "artifact_hash": artifact_hash,
            "validation_success": validation_result.get('success', False),
            "phase": "validation"
        })
        
        return artifact_hash
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive cache statistics.
        
        Returns:
            Dictionary containing cache statistics
        """
        validation_artifacts = []
        total_size_bytes = 0
        
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type") == "validation_result":
                validation_artifacts.append({
                    "artifact_hash": artifact_hash,
                    "cache_key": metadata.get("cache_key"),
                    "validation_model": metadata.get("validation_model"),
                    "success": metadata.get("success"),
                    "cached_at": metadata.get("cached_at"),
                    "size_bytes": len(artifact_info.get("content", b""))
                })
                total_size_bytes += len(artifact_info.get("content", b""))
        
        return {
            "total_validation_artifacts": len(validation_artifacts),
            "total_size_bytes": total_size_bytes,
            "total_size_mb": total_size_bytes / (1024 * 1024),
            "artifacts": validation_artifacts
        }
    
    def cleanup_old_cache_entries(self, max_age_hours: int = 24) -> int:
        """
        Clean up old cache entries based on age.
        
        Args:
            max_age_hours: Maximum age in hours before cleanup
            
        Returns:
            Number of entries cleaned up
        """
        from datetime import datetime, timezone, timedelta
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        cleaned_count = 0
        
        artifacts_to_remove = []
        
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type") == "validation_result":
                cached_at_str = metadata.get("cached_at")
                if cached_at_str:
                    try:
                        cached_at = datetime.fromisoformat(cached_at_str.replace('Z', '+00:00'))
                        if cached_at < cutoff_time:
                            artifacts_to_remove.append(artifact_hash)
                    except ValueError:
                        # Invalid timestamp, remove it
                        artifacts_to_remove.append(artifact_hash)
        
        # Remove old artifacts
        for artifact_hash in artifacts_to_remove:
            try:
                # Note: This assumes the storage has a remove_artifact method
                # If not, we'll just remove from registry
                if hasattr(self.storage, 'remove_artifact'):
                    self.storage.remove_artifact(artifact_hash)
                del self.storage.registry[artifact_hash]
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Failed to remove old cache entry {artifact_hash}: {e}")
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} old cache entries (older than {max_age_hours} hours)")
        
        return cleaned_count
    
    def cleanup_failed_validations(self) -> int:
        """
        Clean up cache entries for failed validations.
        
        Returns:
            Number of entries cleaned up
        """
        cleaned_count = 0
        artifacts_to_remove = []
        
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if (metadata.get("artifact_type") == "validation_result" and 
                not metadata.get("success", True)):
                artifacts_to_remove.append(artifact_hash)
        
        # Remove failed validation artifacts
        for artifact_hash in artifacts_to_remove:
            try:
                if hasattr(self.storage, 'remove_artifact'):
                    self.storage.remove_artifact(artifact_hash)
                del self.storage.registry[artifact_hash]
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Failed to remove failed validation cache entry {artifact_hash}: {e}")
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} failed validation cache entries")
        
        return cleaned_count
    
    def get_cache_efficiency_report(self) -> Dict[str, Any]:
        """
        Generate cache efficiency report for monitoring.
        
        Returns:
            Dictionary containing efficiency metrics
        """
        stats = self.get_cache_statistics()
        
        # Calculate efficiency metrics
        total_artifacts = stats["total_validation_artifacts"]
        total_size_mb = stats["total_size_mb"]
        
        if total_artifacts == 0:
            return {
                "status": "No cache entries",
                "efficiency": "N/A",
                "recommendations": ["Cache is empty - no optimization needed"]
            }
        
        # Size-based efficiency (assuming optimal size is under 100MB)
        size_efficiency = "Good" if total_size_mb < 100 else "Moderate" if total_size_mb < 500 else "High"
        
        # Age-based analysis
        recent_entries = 0
        old_entries = 0
        
        for artifact in stats["artifacts"]:
            cached_at_str = artifact.get("cached_at")
            if cached_at_str:
                try:
                    from datetime import datetime, timezone, timedelta
                    cached_at = datetime.fromisoformat(cached_at_str.replace('Z', '+00:00'))
                    age_hours = (datetime.now(timezone.utc) - cached_at).total_seconds() / 3600
                    
                    if age_hours < 24:
                        recent_entries += 1
                    elif age_hours > 168:  # 1 week
                        old_entries += 1
                except ValueError:
                    pass
        
        recommendations = []
        if old_entries > total_artifacts * 0.3:  # More than 30% are old
            recommendations.append("Consider running cache cleanup for entries older than 1 week")
        
        if total_size_mb > 500:
            recommendations.append("Cache size is large - consider cleanup or size limits")
        
        if not recommendations:
            recommendations.append("Cache is well-optimized")
        
        return {
            "status": "Active",
            "total_entries": total_artifacts,
            "total_size_mb": total_size_mb,
            "size_efficiency": size_efficiency,
            "recent_entries": recent_entries,
            "old_entries": old_entries,
            "efficiency": "High" if size_efficiency == "Good" and old_entries < total_artifacts * 0.2 else "Moderate",
            "recommendations": recommendations
        }
