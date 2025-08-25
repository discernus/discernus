#!/usr/bin/env python3
"""
RAG Index Manager
=================

A dedicated, concern-specific component for building and managing RAG indexes.
This adheres to THIN principles by centralizing RAG logic instead of bloating
the orchestrator.
"""

from typing import List, Dict, Any, Tuple
from txtai.embeddings import Embeddings


class RAGIndexManager:
    """Handles the creation and management of txtai RAG indexes."""

    def __init__(self, artifact_storage):
        """
        Initialize the RAGIndexManager.

        Args:
            artifact_storage: An instance of LocalArtifactStorage.
        """
        self.artifact_storage = artifact_storage

    def build_index_from_documents(
        self, documents: List[Dict[str, Any]]
    ) -> Embeddings:
        """
        Build a searchable txtai index from a list of document dictionaries.

        This method encapsulates the best practices learned from research:
        - It explicitly enables content storage via the {"content": True} flag.
        - It formats the data correctly for txtai's .index() method.

        Args:
            documents: A list of document dictionaries, each expected to have
                       at least a 'content' key.

        Returns:
            The configured and indexed txtai Embeddings object.
        """
        # Initialize txtai with content storage enabled, per best practices.
        rag_index = Embeddings({"content": True})

        # Format the documents into a list of tuples for indexing.
        # The format is (unique_id, data, tags). We use the list index as the id.
        documents_to_index = [
            (i, doc["content"], None) for i, doc in enumerate(documents)
        ]

        # Build the index.
        rag_index.index(documents_to_index)

        return rag_index

    def build_comprehensive_index(
        self, source_documents: List[Dict[str, Any]]
    ) -> Embeddings:
        """
        Build a comprehensive RAG index with full metadata preservation.

        This method is designed for fact-checking and other use cases that require
        access to both document content and metadata for retrieval.

        Args:
            source_documents: List of document dictionaries with 'content' and 'metadata' keys.

        Returns:
            The configured and indexed txtai Embeddings object with stored documents.
        """
        # Initialize txtai with content storage enabled, per best practices.
        rag_index = Embeddings({"content": True})

        # Prepare documents for txtai indexing with metadata preservation
        documents = []
        for i, doc in enumerate(source_documents):
            documents.append({
                'id': i,
                'text': doc['content'],
                'metadata': doc.get('metadata', {})
            })

        # Store documents separately for content retrieval (txtai only stores embeddings)
        rag_index.documents = documents

        # Index the documents using txtai
        rag_index.index(documents)

        return rag_index
