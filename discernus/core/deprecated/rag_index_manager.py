#!/usr/bin/env python3
"""
DEPRECATED: RAG Index Manager
============================

This module has been deprecated as of 2025-01-21.
The V2 architecture uses IntelligentEvidenceRetrievalAgent instead of RAG-based evidence retrieval.

Original functionality:
- Text indexing and search using txtai
- Evidence retrieval for synthesis agents
- RAG-based evidence curation

Replacement:
- IntelligentEvidenceRetrievalAgent provides LLM-driven strategic evidence curation
- No RAG dependencies required
- Session caching for cost optimization

Original docstring:
==================

Handles the creation, caching, and querying of RAG (Retrieval-Augmented Generation)
indexes for the V2 agent ecosystem. This ensures that index building is efficient
and indexes can be reused across runs when the underlying data has not changed.
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
from txtai import embeddings

from .local_artifact_storage import LocalArtifactStorage
from .audit_logger import AuditLogger
from .security_boundary import ExperimentSecurityBoundary


class RAGIndexManager:
    """Manages the lifecycle of RAG indexes."""

    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger, security: ExperimentSecurityBoundary):
        """
        Initializes the RAGIndexManager.
        
        Args:
            storage: LocalArtifactStorage instance for persisting indexes
            audit: AuditLogger instance for logging operations
            security: ExperimentSecurityBoundary for security validation
        """
        self.storage = storage
        self.audit = audit
        self.security = security
        self.logger = logging.getLogger(__name__)
        
        # Cache for loaded indexes to avoid repeated loading
        self._index_cache: Dict[str, Any] = {}
        
        self.logger.info("RAGIndexManager initialized")

    def build_index(self, 
                   evidence_artifacts: List[str], 
                   experiment_id: str,
                   index_name: str = "evidence_index") -> str:
        """
        Builds a RAG index from evidence artifacts.
        
        Args:
            evidence_artifacts: List of artifact hashes containing evidence
            experiment_id: Experiment identifier for security validation
            index_name: Name for the index (used in artifact naming)
            
        Returns:
            Hash of the stored index artifact
            
        Raises:
            SecurityError: If experiment_id is not valid
        """
        self.logger.info(f"Building RAG index '{index_name}' for experiment '{experiment_id}'")
        
        # Security validation
        if not self.security.is_valid_experiment(experiment_id):
            raise SecurityError(f"Invalid experiment ID: {experiment_id}")
        
        # Load and prepare evidence data
        evidence_data = []
        for artifact_hash in evidence_artifacts:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                
                if artifact_data.get('artifact_type') == 'evidence_extraction':
                    evidence_content = artifact_data.get('content', {})
                    quotes = evidence_content.get('quotes', [])
                    
                    for quote in quotes:
                        evidence_data.append({
                            'text': quote.get('text', ''),
                            'document_index': quote.get('document_index', ''),
                            'relevance': quote.get('relevance', ''),
                            'strength_rating': quote.get('strength_rating', '')
                        })
                        
            except Exception as e:
                self.logger.warning(f"Failed to load evidence artifact {artifact_hash}: {e}")
                continue
        
        if not evidence_data:
            self.logger.warning("No evidence data found for index building")
            return None
        
        # Create embeddings index
        index = embeddings.Embeddings({
            'path': 'sentence-transformers/all-MiniLM-L6-v2',
            'content': True
        })
        
        # Index the evidence data
        index_data = []
        for i, evidence in enumerate(evidence_data):
            index_data.append({
                'id': i,
                'text': evidence['text'],
                'document_index': evidence['document_index'],
                'relevance': evidence['relevance'],
                'strength_rating': evidence['strength_rating']
            })
        
        index.index(index_data)
        
        # Store the index as an artifact
        index_artifact = {
            'artifact_type': 'rag_index',
            'index_name': index_name,
            'experiment_id': experiment_id,
            'evidence_count': len(evidence_data),
            'index_data': index_data,
            'created_at': json.dumps(datetime.now().isoformat())
        }
        
        artifact_hash = self.storage.store_artifact(
            content=json.dumps(index_artifact, indent=2),
            artifact_type="rag_index",
            experiment_id=experiment_id
        )
        
        self.logger.info(f"RAG index built and stored with hash: {artifact_hash}")
        self.audit.log_agent_event("RAGIndexManager", "index_built", {
            "index_name": index_name,
            "experiment_id": experiment_id,
            "evidence_count": len(evidence_data),
            "artifact_hash": artifact_hash
        })
        
        return artifact_hash

    def query_index(self, 
                   index_hash: str, 
                   query: str, 
                   limit: int = 10) -> List[Dict[str, Any]]:
        """
        Queries a RAG index for relevant evidence.
        
        Args:
            index_hash: Hash of the stored index artifact
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of relevant evidence items
        """
        self.logger.info(f"Querying RAG index {index_hash} with query: '{query[:50]}...'")
        
        # Load index if not cached
        if index_hash not in self._index_cache:
            try:
                artifact_bytes = self.storage.get_artifact(index_hash)
                artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                
                # Recreate the embeddings index
                index = embeddings.Embeddings({
                    'path': 'sentence-transformers/all-MiniLM-L6-v2',
                    'content': True
                })
                
                index_data = artifact_data.get('index_data', [])
                index.index(index_data)
                
                self._index_cache[index_hash] = index
                
            except Exception as e:
                self.logger.error(f"Failed to load RAG index {index_hash}: {e}")
                return []
        
        # Query the index
        try:
            results = self._index_cache[index_hash].search(query, limit)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'text': result.get('text', ''),
                    'document_index': result.get('document_index', ''),
                    'relevance': result.get('relevance', ''),
                    'strength_rating': result.get('strength_rating', ''),
                    'score': result.get('score', 0.0)
                })
            
            self.logger.info(f"RAG query returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Failed to query RAG index: {e}")
            return []

    def get_index_info(self, index_hash: str) -> Optional[Dict[str, Any]]:
        """
        Gets information about a stored RAG index.
        
        Args:
            index_hash: Hash of the stored index artifact
            
        Returns:
            Dictionary with index information or None if not found
        """
        try:
            artifact_bytes = self.storage.get_artifact(index_hash)
            artifact_data = json.loads(artifact_bytes.decode('utf-8'))
            
            return {
                'index_name': artifact_data.get('index_name', ''),
                'experiment_id': artifact_data.get('experiment_id', ''),
                'evidence_count': artifact_data.get('evidence_count', 0),
                'created_at': artifact_data.get('created_at', '')
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get index info for {index_hash}: {e}")
            return None

    def clear_cache(self):
        """Clears the index cache to free memory."""
        self._index_cache.clear()
        self.logger.info("RAG index cache cleared")