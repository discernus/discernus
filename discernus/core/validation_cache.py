#!/usr/bin/env python3
"""
Validation Cache Manager - THIN Component
=========================================

Manages caching of experiment coherence validation results for development velocity.
Pure software component - no LLM intelligence.
"""

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
                print(f"💾 Cache hit for validation: {cache_key}")
                
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
        print(f"🔍 No cache hit for validation: {cache_key} - will perform validation...")
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
