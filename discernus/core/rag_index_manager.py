#!/usr/bin/env python3
"""
RAG Index Manager
=================

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
            storage: The artifact storage system.
            audit: The audit logger.
            security: The experiment security boundary.
        """
        self.storage = storage
        self.audit = audit
        self.security = security
        self.logger = logging.getLogger(__name__)
        self.embeddings = None
        self.current_index_key = None

    def get_corpus_cache_key(self, corpus_documents: List[Dict[str, str]]) -> str:
        """Generates a cache key from the content of corpus documents."""
        hasher = hashlib.sha256()
        for doc in sorted(corpus_documents, key=lambda x: x['id']):
            hasher.update(doc['content'].encode('utf-8'))
        return f"rag_index_{hasher.hexdigest()}"

    def is_index_cached(self, cache_key: str) -> bool:
        """Checks if an index is already cached in artifact storage."""
        # A directory artifact is registered by its hash (which is our cache_key)
        return self.storage.artifact_exists(cache_key)

    def build_index_from_corpus(self, corpus_documents: List[Dict[str, str]], cache_key: str):
        """Builds a new RAG index from corpus documents and saves it."""
        if not corpus_documents:
            self.logger.warning("Corpus is empty. Cannot build RAG index.")
            return

        self.logger.info(f"Building new RAG index for cache key: {cache_key}")
        
        # Create a temporary directory to build the index
        temp_index_dir = self.storage.run_folder / f"tmp_index_{cache_key}"
        temp_index_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.embeddings = embeddings.Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})
            
            # Prepare data for txtai
            data = [(doc["id"], doc["content"], None) for doc in corpus_documents]
            
            self.embeddings.index(data)
            self.embeddings.save(str(temp_index_dir))

            # Store the directory as a content-addressable artifact
            metadata = {
                "artifact_type": "rag_index",
                "document_count": len(corpus_documents),
                "cache_key": cache_key
            }
            dir_hash = self.storage.put_directory_artifact(temp_index_dir, metadata)

            # Important: The true hash of the directory is calculated by the storage,
            # which should match our cache key if the content is identical.
            if dir_hash != cache_key:
                self.logger.warning(f"RAG index hash mismatch. Expected {cache_key}, got {dir_hash}. This may indicate non-determinism.")

            self.current_index_key = dir_hash

        finally:
            # Clean up the temporary directory
            import shutil
            shutil.rmtree(temp_index_dir)

    def load_index(self, cache_key: str):
        """Loads a pre-existing RAG index from the cache."""
        if not self.is_index_cached(cache_key):
            raise FileNotFoundError(f"RAG index with cache key '{cache_key}' not found.")

        self.logger.info(f"Loading RAG index from cache: {cache_key}")
        index_path = self.storage.get_directory_artifact_path(cache_key)
        self.embeddings = embeddings.Embeddings({"content": True})
        self.embeddings.load(str(index_path))
        self.current_index_key = cache_key

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Searches the loaded RAG index."""
        if not self.embeddings:
            raise RuntimeError("No RAG index is loaded. Call build_index or load_index first.")

        results = self.embeddings.search(query, top_k)
        
        # Format results to be consistent
        formatted_results = []
        for res in results:
            formatted_results.append({
                "id": res["id"],
                "text": res["text"],
                "score": res["score"],
            })
        return formatted_results
