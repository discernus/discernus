#!/usr/bin/env python3
"""
Statistical Analysis Cache Manager - THIN Component
==================================================

Manages caching of statistical analysis function generation for development velocity.
Pure software component - no LLM intelligence.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


@dataclass
class StatisticalAnalysisCacheResult:
    """Result of statistical analysis cache lookup."""
    hit: bool
    artifact_hash: Optional[str] = None
    cached_functions: Optional[Dict[str, Any]] = None


class StatisticalAnalysisCacheManager:
    """
    Manages caching of statistical analysis function generation using content-addressable storage.
    
    THIN Principle: Pure software caching infrastructure.
    No LLM intelligence - just deterministic cache management.
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger):
        self.storage = storage
        self.audit = audit
    
    def generate_cache_key(self, framework_content: str, experiment_content: str, 
                          analysis_results: List[Dict[str, Any]], 
                          derived_metrics_results: Dict[str, Any], model: str) -> str:
        """
        Generate deterministic cache key for statistical analysis functions.
        
        Args:
            framework_content: Framework markdown content
            experiment_content: Experiment markdown content
            analysis_results: List of analysis result dictionaries
            derived_metrics_results: Derived metrics results dictionary
            model: LLM model used for function generation
            
        Returns:
            Deterministic cache key based on content hashes and model
        """
        # Create structure hash from analysis results (not content, just structure)
        analysis_structure = []
        for result in analysis_results:
            # Extract just the structure/schema, not the actual values
            structure = {
                'has_analysis_result': 'analysis_result' in result,
                'has_raw_response': 'raw_analysis_response' in result,
                'has_scores_hash': 'scores_hash' in result,
                'has_evidence_hash': 'evidence_hash' in result,
                'filename': result.get('filename', 'unknown')
            }
            analysis_structure.append(structure)
        
        analysis_structure_hash = hashlib.sha256(
            json.dumps(analysis_structure, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Create structure hash from derived metrics results
        derived_metrics_structure = {
            'status': derived_metrics_results.get('status', 'unknown'),
            'has_derived_metrics_results': 'derived_metrics_results' in derived_metrics_results,
            'functions_generated': derived_metrics_results.get('functions_generated', 0)
        }
        
        derived_metrics_structure_hash = hashlib.sha256(
            json.dumps(derived_metrics_structure, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Combine all inputs for cache key
        cache_content = f'{framework_content}{experiment_content}{analysis_structure_hash}{derived_metrics_structure_hash}{model}'
        cache_hash = hashlib.sha256(cache_content.encode()).hexdigest()[:12]
        
        return f"statistical_analysis_{cache_hash}"
    
    def check_cache(self, cache_key: str, agent_name: str = "StatisticalAnalysisAgent") -> StatisticalAnalysisCacheResult:
        """
        Check if statistical analysis functions are already cached.
        
        Args:
            cache_key: Cache key for lookup
            agent_name: Name of the agent for logging
            
        Returns:
            StatisticalAnalysisCacheResult indicating hit/miss and cached functions if available
        """
        # Search through artifact registry for matching statistical analysis functions
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "statistical_analysis_functions" and
                metadata.get("cache_key") == cache_key):
                
                # Cache hit!
                print(f"💾 Cache hit for statistical analysis: {cache_key}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_functions = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(agent_name, "cache_hit", {
                        "cache_key": cache_key,
                        "cached_artifact_hash": artifact_hash,
                        "phase": "statistical_analysis"
                    })
                    
                    return StatisticalAnalysisCacheResult(
                        hit=True,
                        artifact_hash=artifact_hash,
                        cached_functions=cached_functions
                    )
                    
                except Exception as e:
                    print(f"⚠️ Cache hit but failed to load statistical analysis functions: {e}")
                    # Continue searching for other cached results
                    continue
        
        # No cache hit
        print(f"🔍 No cache hit for statistical analysis: {cache_key} - will generate functions...")
        return StatisticalAnalysisCacheResult(hit=False)
    
    def store_functions(self, cache_key: str, functions_result: Dict[str, Any], 
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store statistical analysis functions in cache.
        
        Args:
            cache_key: Cache key for the functions
            functions_result: Complete functions result to cache
            metadata: Additional metadata for the artifact
            
        Returns:
            Hash of the stored artifact
        """
        # Add cache-specific metadata
        cache_metadata = {
            **(metadata or {}),
            "artifact_type": "statistical_analysis_functions",
            "cache_key": cache_key,
            "functions_generated": functions_result.get('functions_generated', 0),
            "generation_model": functions_result.get('model', 'unknown')
        }
        
        # Store the functions result
        functions_json = json.dumps(functions_result, indent=2)
        artifact_hash = self.storage.put_artifact(
            functions_json.encode('utf-8'),
            cache_metadata
        )
        
        print(f"💾 Stored statistical analysis functions in cache: {cache_key}")
        self.audit.log_agent_event("StatisticalAnalysisAgent", "cache_store", {
            "cache_key": cache_key,
            "artifact_hash": artifact_hash,
            "phase": "statistical_analysis"
        })
        
        return artifact_hash
