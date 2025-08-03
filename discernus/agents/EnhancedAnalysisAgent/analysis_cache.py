#!/usr/bin/env python3
"""
Analysis Cache Manager - THIN Component
=======================================

Manages caching of analysis results for perfect THIN caching.
Pure software component - no LLM intelligence.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


@dataclass
class CacheResult:
    """Result of cache lookup."""
    hit: bool
    artifact_hash: Optional[str] = None
    cached_content: Optional[Dict[str, Any]] = None


class AnalysisCacheManager:
    """
    Manages caching of analysis results using content-addressable storage.
    
    THIN Principle: Pure software caching infrastructure.
    No LLM intelligence - just deterministic cache management.
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger):
        self.storage = storage
        self.audit = audit
    
    def generate_batch_id(self, framework_content: str, corpus_documents: List[Dict[str, Any]], model: str) -> str:
        """
        Generate deterministic batch ID for perfect caching.
        
        Args:
            framework_content: Framework markdown content
            corpus_documents: List of document dictionaries
            model: LLM model to use for analysis
            
        Returns:
            Deterministic batch ID based on content hashes and model
        """
        # Create content hash from documents
        corpus_content = ''.join([
            doc.get('filename', '') + str(doc.get('content', ''))
            for doc in corpus_documents
        ])
        doc_content_hash = hashlib.sha256(corpus_content.encode()).hexdigest()[:16]
        
        # Combine framework, document content, and model for batch ID
        batch_content = f'{framework_content}{doc_content_hash}{model}'
        batch_hash = hashlib.sha256(batch_content.encode()).hexdigest()[:12]
        
        return f"batch_{batch_hash}"
    
    def check_cache(self, batch_id: str, agent_name: str) -> CacheResult:
        """
        Check if analysis result is already cached.
        
        Args:
            batch_id: Batch identifier for cache lookup
            agent_name: Name of the agent for logging
            
        Returns:
            CacheResult indicating hit/miss and cached content if available
        """
        # Search through artifact registry for matching analysis result
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "analysis_result" and
                metadata.get("batch_id") == batch_id):
                
                # Cache hit!
                print(f"💾 Cache hit for analysis: {batch_id}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_result = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(agent_name, "cache_hit", {
                        "batch_id": batch_id,
                        "cached_artifact_hash": artifact_hash
                    })
                    
                    return CacheResult(
                        hit=True,
                        artifact_hash=artifact_hash,
                        cached_content=cached_result
                    )
                    
                except Exception as e:
                    print(f"⚠️ Cache hit but failed to load content: {e}")
                    # Continue searching for other cached results
                    continue
        
        # No cache hit
        print(f"🔍 No cache hit for {batch_id} - will perform analysis...")
        return CacheResult(hit=False)
    
    def store_analysis_result(self, batch_id: str, analysis_result: Dict[str, Any], 
                             metadata: Dict[str, Any]) -> str:
        """
        Store analysis result in cache.
        
        Args:
            batch_id: Batch identifier
            analysis_result: Complete analysis result to cache
            metadata: Additional metadata for the artifact
            
        Returns:
            Hash of the stored artifact
        """
        # Add cache-specific metadata
        cache_metadata = {
            **metadata,
            "artifact_type": "analysis_result",
            "batch_id": batch_id
        }
        
        # Store the result
        result_json = json.dumps(analysis_result, indent=2)
        artifact_hash = self.storage.put_artifact(
            result_json.encode('utf-8'),
            cache_metadata
        )
        
        return artifact_hash
    
    def handle_cache_hit(self, cache_result: CacheResult, csv_handler, 
                        current_scores_hash, current_evidence_hash, batch_id):
        """Handle cache hit scenario - extract CSVs and return result."""
        document_hashes = cache_result.cached_content.get('input_artifacts', {}).get('document_hashes', [])
        
        new_scores_hash, new_evidence_hash = csv_handler.extract_and_persist_csvs(
            cache_result.cached_content['raw_analysis_response'],
            document_hashes[0] if document_hashes else "unknown_artifact",
            current_scores_hash, current_evidence_hash)
        
        return {
            "analysis_result": {
                "batch_id": batch_id,
                "result_hash": cache_result.artifact_hash,
                "result_content": cache_result.cached_content,
                "duration_seconds": 0.0,
                "mathematical_validation": True,
                "cached": True
            },
            "scores_hash": new_scores_hash,
            "evidence_hash": new_evidence_hash
        }