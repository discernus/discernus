#!/usr/bin/env python3
"""
Derived Metrics Cache Manager - THIN Component
==============================================

Manages caching of derived metrics function generation for development velocity.
Pure software component - no LLM intelligence.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


@dataclass
class DerivedMetricsCacheResult:
    """Result of derived metrics cache lookup."""
    hit: bool
    artifact_hash: Optional[str] = None
    cached_functions: Optional[Dict[str, Any]] = None


class DerivedMetricsCacheManager:
    """
    Manages caching of derived metrics function generation using content-addressable storage.
    
    THIN Principle: Pure software caching infrastructure.
    No LLM intelligence - just deterministic cache management.
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger):
        self.storage = storage
        self.audit = audit
    
    def generate_cache_key(self, framework_content: str, analysis_results: List[Dict[str, Any]], model: str) -> str:
        """
        Generate deterministic cache key for derived metrics functions.
        
        Args:
            framework_content: Framework markdown content
            analysis_results: List of analysis result dictionaries
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
        
        # Combine framework, analysis structure, and model for cache key
        cache_content = f'{framework_content}{analysis_structure_hash}{model}'
        cache_hash = hashlib.sha256(cache_content.encode()).hexdigest()[:12]
        
        return f"derived_metrics_{cache_hash}"
    
    def check_cache(self, cache_key: str, agent_name: str = "DerivedMetricsAgent") -> DerivedMetricsCacheResult:
        """
        Check if derived metrics functions are already cached.
        
        Args:
            cache_key: Cache key for lookup
            agent_name: Name of the agent for logging
            
        Returns:
            DerivedMetricsCacheResult indicating hit/miss and cached functions if available
        """
        # Search through artifact registry for matching derived metrics functions
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "derived_metrics_functions" and
                metadata.get("cache_key") == cache_key):
                
                # Verify artifact actually exists before claiming cache hit
                if not self.storage.artifact_exists(artifact_hash):
                    print(f"⚠️ Cache metadata found but artifact missing: {cache_key} (hash: {artifact_hash[:8]})")
                    continue
                
                # Cache hit!
                print(f"💾 Cache hit for derived metrics: {cache_key}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_functions = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(agent_name, "cache_hit", {
                        "cache_key": cache_key,
                        "cached_artifact_hash": artifact_hash,
                        "phase": "derived_metrics"
                    })
                    
                    return DerivedMetricsCacheResult(
                        hit=True,
                        artifact_hash=artifact_hash,
                        cached_functions=cached_functions
                    )
                    
                except Exception as e:
                    print(f"⚠️ Cache hit but failed to load derived metrics functions: {e}")
                    # Continue searching for other cached results
                    continue
        
        # No cache hit
        print(f"🔍 No cache hit for derived metrics: {cache_key} - will generate functions...")
        return DerivedMetricsCacheResult(hit=False)
    
    def store_functions(self, cache_key: str, functions_result: Dict[str, Any], 
                       workspace_path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store derived metrics functions in cache with actual function code.
        
        Args:
            cache_key: Cache key for the functions
            functions_result: Complete functions result to cache
            workspace_path: Path to workspace containing generated functions file
            metadata: Additional metadata for the artifact
            
        Returns:
            Hash of the stored artifact
        """
        # Create enhanced functions result that includes the actual function code
        enhanced_functions_result = functions_result.copy()
        
        # If workspace_path is provided, read the actual function file content
        if workspace_path:
            from pathlib import Path
            functions_file = Path(workspace_path) / "automatedderivedmetricsagent_functions.py"
            if functions_file.exists():
                try:
                    function_code = functions_file.read_text(encoding='utf-8')
                    enhanced_functions_result['function_code_content'] = function_code
                    enhanced_functions_result['cached_with_code'] = True
                    print(f"💾 Cached function code content ({len(function_code)} chars)")
                except Exception as e:
                    print(f"⚠️ Failed to read function file for caching: {e}")
                    enhanced_functions_result['cached_with_code'] = False
            else:
                print(f"⚠️ Function file not found for caching: {functions_file}")
                enhanced_functions_result['cached_with_code'] = False
        else:
            enhanced_functions_result['cached_with_code'] = False
        
        # Add cache-specific metadata
        cache_metadata = {
            **(metadata or {}),
            "artifact_type": "derived_metrics_functions",
            "cache_key": cache_key,
            "functions_generated": enhanced_functions_result.get('functions_generated', 0),
            "generation_model": enhanced_functions_result.get('model', 'unknown'),
            "has_function_code": enhanced_functions_result.get('cached_with_code', False)
        }
        
        # Store the enhanced functions result
        functions_json = json.dumps(enhanced_functions_result, indent=2)
        artifact_hash = self.storage.put_artifact(
            functions_json.encode('utf-8'),
            cache_metadata
        )
        
        print(f"💾 Stored derived metrics functions in cache: {cache_key} (with code: {enhanced_functions_result.get('cached_with_code', False)})")
        self.audit.log_agent_event("DerivedMetricsAgent", "cache_store", {
            "cache_key": cache_key,
            "artifact_hash": artifact_hash,
            "has_function_code": enhanced_functions_result.get('cached_with_code', False),
            "phase": "derived_metrics"
        })
        
        return artifact_hash
