#!/usr/bin/env python3
"""
Unified Cache Manager
====================

A single, coherent caching system for all pipeline phases that follows the fundamental principle:
Cache Key = Hash(All Inputs That Affect Output)

This replaces the fragmented, inconsistent caching approaches with a unified strategy
that will actually provide cache hits.
"""

import hashlib
import json
import logging
from typing import Dict, Any, Optional, NamedTuple
from pathlib import Path

from .local_artifact_storage import LocalArtifactStorage
from .audit_logger import AuditLogger


class CacheResult(NamedTuple):
    """Result of cache lookup operation."""
    hit: bool
    cached_content: Optional[Dict[str, Any]] = None
    artifact_hash: Optional[str] = None


class UnifiedCacheManager:
    """
    Unified cache manager for all pipeline phases.
    
    Uses deterministic, input-based cache keys to ensure proper cache behavior:
    - Same inputs → Cache hit
    - Different inputs → Cache miss
    - No timestamps or random elements in cache keys
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: Optional[AuditLogger] = None):
        self.storage = storage
        self.audit = audit
        self.logger = logging.getLogger(__name__)
    
    def generate_phase_cache_key(self,
                                framework_content: str,
                                experiment_content: str,
                                corpus_content: str,
                                model: str,
                                phase_name: str,
                                phase_specific_inputs: str = "",
                                dependency_hashes: str = "") -> str:
        """
        Generate deterministic cache key for any phase.
        
        Args:
            framework_content: Full framework markdown content
            experiment_content: Full experiment.md content
            corpus_content: Full corpus manifest content
            model: LLM model used for this phase
            phase_name: Name of the phase (validation, analysis, derived_metrics, statistical_analysis)
            phase_specific_inputs: Any phase-specific inputs (e.g., prompt hashes)
            dependency_hashes: Hashes of results from previous phases this phase depends on
            
        Returns:
            Deterministic cache key: "{phase_name}_{hash}"
        """
        # Include prompt template hash to invalidate cache when prompts change
        prompt_hash = self._get_prompt_template_hash(phase_name)
        
        # Combine all inputs that affect the output
        combined_input = (
            f"{framework_content}"
            f"{experiment_content}"
            f"{corpus_content}"
            f"{model}"
            f"{phase_name}"
            f"{phase_specific_inputs}"
            f"{dependency_hashes}"
            f"{prompt_hash}"
        )
        
        # Generate deterministic hash
        cache_hash = hashlib.sha256(combined_input.encode()).hexdigest()[:12]
        
        return f"{phase_name}_{cache_hash}"
    
    def check_cache(self, cache_key: str, agent_name: str = "UnifiedCache") -> CacheResult:
        """
        Check if results are already cached for this cache key.
        
        Args:
            cache_key: Deterministic cache key
            agent_name: Name of agent for logging
            
        Returns:
            CacheResult indicating hit/miss and cached content if available
        """
        # Search through artifact registry for matching cached result
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if metadata.get("cache_key") == cache_key:
                # Cache hit!
                self.logger.info(f"💾 Cache hit: {cache_key}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_result = json.loads(cached_content.decode('utf-8'))
                    
                    if self.audit:
                        self.audit.log_agent_event(agent_name, "cache_hit", {
                            "cache_key": cache_key,
                            "cached_artifact_hash": artifact_hash
                        })
                    
                    return CacheResult(
                        hit=True,
                        cached_content=cached_result,
                        artifact_hash=artifact_hash
                    )
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Cache hit but failed to load content: {e}")
                    continue
        
        # No cache hit
        self.logger.info(f"🔍 Cache miss: {cache_key}")
        return CacheResult(hit=False)
    
    def store_cache(self, cache_key: str, result: Dict[str, Any], 
                   agent_name: str = "UnifiedCache") -> str:
        """
        Store results in cache with the given cache key.
        
        Args:
            cache_key: Deterministic cache key
            result: Results to cache
            agent_name: Name of agent for logging
            
        Returns:
            Artifact hash of stored cache entry
        """
        try:
            # Add cache metadata to result
            cached_result = {
                **result,
                "cache_metadata": {
                    "cache_key": cache_key,
                    "cached_at": "2025-01-15T14:30:00Z",  # Use fixed timestamp for deterministic caching
                    "agent_name": agent_name
                }
            }
            
            # Store in artifact storage
            content = json.dumps(cached_result, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content,
                {
                    "artifact_type": "cached_result",
                    "cache_key": cache_key,
                    "agent": agent_name
                }
            )
            
            if self.audit:
                self.audit.log_agent_event(agent_name, "cache_store", {
                    "cache_key": cache_key,
                    "artifact_hash": artifact_hash
                })
            
            self.logger.info(f"💾 Cached result: {cache_key} → {artifact_hash}")
            return artifact_hash
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store cache: {e}")
            raise
    
    def _get_prompt_template_hash(self, phase_name: str) -> str:
        """Get hash of the current prompt template to invalidate cache when prompts change."""
        try:
            # Map phase names to prompt template paths
            prompt_paths = {
                "validation": "agents/experiment_coherence_agent/prompt.yaml",
                "analysis": "agents/analysis_agent/prompt.yaml", 
                "derived_metrics": "agents/automated_derived_metrics/prompt.yaml",
                "statistical_analysis": "agents/statistical_agent/prompt.yaml"
            }
            
            prompt_path = Path(__file__).parent.parent / prompt_paths.get(phase_name, "")
            if prompt_path.exists():
                prompt_content = prompt_path.read_text(encoding='utf-8')
                return hashlib.sha256(prompt_content.encode()).hexdigest()[:8]
        except Exception:
            pass
        return "unknown"


class ValidationCacheManager(UnifiedCacheManager):
    """Specialized cache manager for validation phase."""
    
    def generate_validation_cache_key(self,
                                    framework_content: str,
                                    experiment_content: str,
                                    corpus_content: str,
                                    validation_model: str) -> str:
        """Generate cache key for validation phase."""
        return self.generate_phase_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            model=validation_model,
            phase_name="validation"
        )


class AnalysisCacheManager(UnifiedCacheManager):
    """Specialized cache manager for analysis phase."""
    
    def generate_analysis_cache_key(self,
                                   framework_content: str,
                                   experiment_content: str,
                                   corpus_content: str,
                                   analysis_model: str) -> str:
        """Generate cache key for analysis phase."""
        return self.generate_phase_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            model=analysis_model,
            phase_name="analysis"
        )


class DerivedMetricsCacheManager(UnifiedCacheManager):
    """Specialized cache manager for derived metrics phase."""
    
    def generate_derived_metrics_cache_key(self,
                                         framework_content: str,
                                         experiment_content: str,
                                         corpus_content: str,
                                         derived_metrics_model: str,
                                         analysis_results_hash: str) -> str:
        """Generate cache key for derived metrics phase."""
        return self.generate_phase_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            model=derived_metrics_model,
            phase_name="derived_metrics",
            dependency_hashes=analysis_results_hash
        )


class StatisticalAnalysisCacheManager(UnifiedCacheManager):
    """Specialized cache manager for statistical analysis phase."""
    
    def generate_statistical_analysis_cache_key(self,
                                               framework_content: str,
                                               experiment_content: str,
                                               corpus_content: str,
                                               statistical_model: str,
                                               analysis_results_hash: str,
                                               derived_metrics_hash: str) -> str:
        """Generate cache key for statistical analysis phase."""
        dependency_hashes = f"{analysis_results_hash}{derived_metrics_hash}"
        return self.generate_phase_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            model=statistical_model,
            phase_name="statistical_analysis",
            dependency_hashes=dependency_hashes
        )
