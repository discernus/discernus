#!/usr/bin/env python3
"""
Document Processor - THIN Component
===================================

Prepares documents for analysis and handles document artifacts.
Pure software component - no LLM intelligence.
"""

import base64
import hashlib
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

from discernus.core.local_artifact_storage import LocalArtifactStorage


@dataclass
class ProcessedDocument:
    """Processed document ready for analysis."""
    content: str
    filename: str
    artifact_hash: str
    size_bytes: int


class DocumentProcessor:
    """
    Processes and stores documents for analysis.
    
    THIN Principle: Pure software document handling.
    Converts various document formats to analysis-ready format.
    """
    
    def __init__(self, storage: LocalArtifactStorage):
        self.storage = storage
    
    def process_documents(self, corpus_documents: List[Dict[str, Any]], 
                         batch_id: str) -> Tuple[List[ProcessedDocument], List[str]]:
        """
        Process corpus documents for analysis.
        
        Args:
            corpus_documents: Raw document dictionaries
            batch_id: Batch identifier for artifact metadata
            
        Returns:
            Tuple of (processed_documents, document_hashes)
        """
        processed_docs = []
        document_hashes = []
        
        for i, doc in enumerate(corpus_documents):
            # Handle both string and bytes content
            if isinstance(doc.get('content'), bytes):
                doc_content = base64.b64encode(doc['content']).decode('utf-8')
                content_for_analysis = f"[Binary content, base64 encoded: {len(doc_content)} chars]"
            else:
                doc_content = str(doc.get('content', ''))
                content_for_analysis = doc_content
            
            filename = doc.get('filename', f'document_{i+1}')
            
            # Store document as artifact
            doc_hash = self.storage.put_artifact(
                doc_content.encode('utf-8'),
                {
                    "artifact_type": "corpus_document",
                    "batch_id": batch_id,
                    "filename": filename,
                    "document_index": i
                }
            )
            
            processed_doc = ProcessedDocument(
                content=content_for_analysis,
                filename=filename,
                artifact_hash=doc_hash,
                size_bytes=len(doc_content)
            )
            
            processed_docs.append(processed_doc)
            document_hashes.append(doc_hash)
        
        return processed_docs, document_hashes
    
    def format_documents_for_prompt(self, documents: List[ProcessedDocument]) -> str:
        """
        Format processed documents for LLM prompt.
        
        Args:
            documents: List of processed documents
            
        Returns:
            Formatted string for inclusion in LLM prompt
        """
        if not documents:
            return "No documents provided."
        
        formatted_docs = []
        for i, doc in enumerate(documents):
            formatted_docs.append(f"Document {i+1} ({doc.filename}):\n{doc.content}")
        
        return "\n\n".join(formatted_docs)