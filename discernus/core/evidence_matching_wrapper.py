#!/usr/bin/env python3
"""
Evidence Matching Wrapper
=========================

Framework-agnostic wrapper for matching evidence quotes to statistical findings.
This wrapper provides intelligent evidence retrieval that works with any analytical
framework, maintaining experiment agnosticism while enabling evidence-based synthesis.

Phase 1: Foundation - Basic txtai integration and evidence index building
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
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from txtai.embeddings import Embeddings

from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry
from ..core.local_artifact_storage import LocalArtifactStorage
from ..core.audit_logger import AuditLogger


class EvidenceMatchingWrapper:
    """
    Framework-agnostic wrapper for matching evidence quotes to statistical findings.
    
    This wrapper provides intelligent evidence retrieval that works with any analytical
    framework, maintaining experiment agnosticism while enabling evidence-based synthesis.
    """
    
    def __init__(self, model: str, artifact_storage: LocalArtifactStorage, audit_logger: Optional[AuditLogger] = None):
        """
        Initialize the Evidence Matching Wrapper.
        
        Args:
            model: LLM model to use for query generation
            artifact_storage: Local artifact storage for evidence access
            audit_logger: Optional audit logger for operation tracking
        """
        self.model = model
        self.artifact_storage = artifact_storage
        self.audit_logger = audit_logger
        self.llm_gateway = LLMGateway(ModelRegistry())
        
        # Core components
        self.index: Optional[Embeddings] = None
        self.evidence_data: List[Dict[str, Any]] = []
        self.evidence_metadata: Dict[str, Any] = {}
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        if self.audit_logger:
            self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "initialized", {
                "model": model,
                "artifact_storage_type": type(artifact_storage).__name__
            })
    
    def build_index(self, evidence_artifact_hashes: List[str]) -> bool:
        """
        Build txtai index from evidence artifacts with metadata preservation.
        
        Args:
            evidence_artifact_hashes: List of evidence artifact hashes
            
        Returns:
            True if index built successfully, False otherwise
        """
        try:
            if not evidence_artifact_hashes:
                self.logger.warning("No evidence artifact hashes provided")
                return False
            
            self.logger.info(f"Building evidence index from {len(evidence_artifact_hashes)} artifacts...")
            
            # Load and parse evidence artifacts
            evidence_documents = []
            for i, hash_id in enumerate(evidence_artifact_hashes):
                try:
                    content = self.artifact_storage.get_artifact(hash_id, quiet=True)
                    if content:
                        evidence_data = json.loads(content.decode('utf-8'))
                        
                        # Extract evidence pieces from the artifact
                        evidence_list = evidence_data.get('evidence_data', [])
                        if not evidence_list:
                            # Try alternative structure
                            evidence_list = evidence_data.get('evidence_collection', [])
                        
                        for evidence in evidence_list:
                            quote_text = evidence.get('quote_text', '')
                            # Only index evidence with actual quotes (not empty, None, or whitespace)
                            if quote_text and quote_text.strip():
                                evidence_documents.append({
                                    'id': len(evidence_documents),
                                    'text': quote_text.strip(),
                                    'metadata': {
                                        'document_name': evidence.get('document_name', 'Unknown'),
                                        'dimension': evidence.get('dimension', 'Unknown'),
                                        'confidence': evidence.get('confidence', 0.0),
                                        'extraction_method': evidence.get('extraction_method', 'Unknown'),
                                        'source_type': evidence.get('source_type', 'Unknown')
                                    }
                                })
                                
                except Exception as e:
                    self.logger.warning(f"Failed to load evidence artifact {hash_id}: {e}")
                    continue
            
            if not evidence_documents:
                self.logger.error("No valid evidence documents found in artifacts")
                return False
            
            # Store evidence data for later use
            self.evidence_data = evidence_documents
            
            # Build txtai index with comprehensive metadata preservation
            self.index = Embeddings({"content": True})
            
            # Prepare documents for txtai indexing - txtai expects list of dicts
            documents_to_index = []
            for doc in evidence_documents:
                # Create searchable text combining metadata and content
                search_text = f"{doc['metadata'].get('document_name', '')} {doc['metadata'].get('dimension', '')} evidence: {doc['text']}"
                
                documents_to_index.append({
                    "id": doc['id'],
                    "text": search_text,
                    "document_name": doc['metadata'].get('document_name', ''),
                    "dimension": doc['metadata'].get('dimension', ''),
                    "quote_text": doc['text'],
                    "confidence": doc['metadata'].get('confidence', 0.0),
                    "extraction_method": doc['metadata'].get('extraction_method', ''),
                    "source_type": doc['metadata'].get('source_type', '')
                })
            
            # Build the index
            self.index.index(documents_to_index)
            
            # Store documents separately for content retrieval (txtai only stores embeddings)
            self.index.documents = evidence_documents
            
            # Store metadata summary
            self.evidence_metadata = {
                'total_evidence_pieces': len(evidence_documents),
                'total_artifacts_processed': len(evidence_artifact_hashes),
                'index_built_at': self._get_timestamp()
            }
            
            self.logger.info(f"Successfully built evidence index with {len(evidence_documents)} pieces")
            
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "index_built", {
                    "evidence_count": len(evidence_documents),
                    "artifacts_processed": len(evidence_artifact_hashes)
                })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build evidence index: {e}")
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "index_build_failed", {
                    "error": str(e)
                })
            return False
    
    def build_index_from_data(self, evidence_data: List[Dict[str, Any]]) -> bool:
        """
        Build txtai index from pre-loaded evidence data.
        
        Args:
            evidence_data: List of evidence dictionaries with quote_text, document_name, dimension, etc.
            
        Returns:
            True if index built successfully, False otherwise
        """
        try:
            if not evidence_data:
                self.logger.warning("No evidence data provided")
                return False
            
            self.logger.info(f"Building evidence index from {len(evidence_data)} evidence pieces...")
            
            # Store evidence data for later use
            self.evidence_data = evidence_data
            
            # Build txtai index with comprehensive metadata preservation
            self.index = Embeddings({"content": True})
            
            # Prepare documents for txtai indexing - txtai expects list of dicts
            documents_to_index = []
            for i, evidence in enumerate(evidence_data):
                quote_text = evidence.get('quote_text', '')
                if quote_text and quote_text.strip():
                    # Create searchable text combining metadata and content
                    search_text = f"{evidence.get('document_name', '')} {evidence.get('dimension', '')} evidence: {quote_text.strip()}"
                    
                    documents_to_index.append({
                        "id": i,
                        "text": search_text,
                        "document_name": evidence.get('document_name', ''),
                        "dimension": evidence.get('dimension', ''),
                        "quote_text": quote_text.strip(),
                        "confidence": evidence.get('confidence', 0.0),
                        "extraction_method": evidence.get('extraction_method', 'Unknown'),
                        "source_type": evidence.get('source_type', 'Unknown')
                    })
            
            if not documents_to_index:
                self.logger.error("No valid evidence documents found in data")
                return False
            
            # Build the index
            self.index.index(documents_to_index)
            
            # Store documents separately for content retrieval (txtai only stores embeddings)
            # Convert to the format expected by the compatibility layer
            formatted_documents = []
            for evidence in evidence_data:
                formatted_doc = {
                    'text': evidence.get('quote_text', ''),
                    'metadata': {
                        'document_name': evidence.get('document_name', 'Unknown'),
                        'dimension': evidence.get('dimension', 'Unknown'),
                        'confidence': evidence.get('confidence', 0.0)
                    }
                }
                formatted_documents.append(formatted_doc)
            
            self.index.documents = formatted_documents
            
            # Store metadata summary
            self.evidence_metadata = {
                'total_evidence_pieces': len(evidence_data),
                'total_artifacts_processed': 0,  # Not from artifacts
                'index_built_at': self._get_timestamp()
            }
            
            self.logger.info(f"Successfully built evidence index with {len(evidence_data)} pieces")
            
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "index_built_from_data", {
                    "evidence_count": len(evidence_data)
                })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build index from data: {e}")
            return False
    
    def search_evidence(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generic evidence search with optional filtering.
        
        Args:
            query: Search query string
            filters: Optional metadata filters (dimension, confidence, document_name)
            limit: Maximum number of evidence pieces to return
            
        Returns:
            List of evidence dictionaries matching the query and filters
        """
        if not self.index:
            self.logger.warning("No evidence index available. Call build_index() first.")
            return []
        
        try:
            # Perform semantic search
            self.logger.info(f"Executing RAG search with query: '{query}'")
            search_results = self.index.search(query, limit=limit * 2)  # Get more results for filtering
            
            # Apply metadata filters if provided
            filtered_results = []
            for result in search_results:
                # Format the result first to get consistent structure
                formatted_result = self._format_search_result(result)
                
                if self._matches_filters(formatted_result, filters):
                    filtered_results.append(formatted_result)
                
                if len(filtered_results) >= limit:
                    break
            
            self.logger.info(f"RAG search for query '{query}' returned {len(filtered_results)} results after filtering.")
            # Log the top N results for traceability
            for i, result in enumerate(filtered_results[:3]): # Log top 3
                self.logger.debug(f"  Result {i+1}: Score={result.get('relevance_score', 0.0):.4f}, Quote='{result.get('quote_text', '')[:100]}...'")

            return filtered_results
            
        except Exception as e:
            self.logger.error(f"Evidence search failed: {e}")
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "search_failed", {
                    "query": query,
                    "error": str(e)
                })
            return []
    
    def get_evidence_by_metadata(
        self,
        metadata_filters: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve evidence based on metadata filters without semantic search.
        
        Args:
            metadata_filters: Dictionary of metadata filters to apply
            limit: Maximum number of evidence pieces to return
            
        Returns:
            List of evidence dictionaries matching the metadata filters
        """
        if not self.evidence_data:
            self.logger.warning("No evidence data available. Call build_index() first.")
            return []
        
        try:
            filtered_evidence = []
            
            for evidence in self.evidence_data:
                if self._matches_filters(evidence, metadata_filters):
                    filtered_evidence.append({
                        "quote_text": evidence['text'],
                        "document_name": evidence['metadata'].get('document_name', 'Unknown'),
                        "dimension": evidence['metadata'].get('dimension', 'Unknown'),
                        "confidence": evidence['metadata'].get('confidence', 0.0),
                        "relevance_score": 1.0,  # No semantic scoring for metadata-only search
                        "metadata": evidence['metadata']
                    })
                    
                    if len(filtered_evidence) >= limit:
                        break
            
            self.logger.debug(f"Metadata filter returned {len(filtered_evidence)} results")
            return filtered_evidence
            
        except Exception as e:
            self.logger.error(f"Metadata-based evidence retrieval failed: {e}")
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "metadata_search_failed", {
                    "filters": metadata_filters,
                    "error": str(e)
                })
            return []
    
    def get_index_status(self) -> Dict[str, Any]:
        """
        Get current status of the evidence index.
        
        Returns:
            Dictionary with index status information
        """
        return {
            "index_built": self.index is not None,
            "evidence_count": len(self.evidence_data),
            "metadata": self.evidence_metadata,
            "model": self.model
        }
    
    def _matches_filters(self, evidence: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        """
        Check if evidence matches the provided filters.
        
        Args:
            evidence: Evidence dictionary to check
            filters: Optional filters to apply
            
        Returns:
            True if evidence matches all filters, False otherwise
        """
        if not filters:
            return True
        
        try:
            for filter_key, filter_value in filters.items():
                if filter_key == 'dimension':
                    # Check both metadata and top-level dimension
                    evidence_dimension = evidence.get('metadata', {}).get('dimension') or evidence.get('dimension')
                    if evidence_dimension != filter_value:
                        return False
                elif filter_key == 'document_name':
                    # Check both metadata and top-level document_name
                    evidence_doc_name = evidence.get('metadata', {}).get('document_name') or evidence.get('document_name')
                    if evidence_doc_name != filter_value:
                        return False
                elif filter_key == 'confidence_min':
                    # Check both metadata and top-level confidence
                    evidence_confidence = evidence.get('metadata', {}).get('confidence') or evidence.get('confidence', 0.0)
                    if evidence_confidence < filter_value:
                        return False
                elif filter_key == 'confidence_max':
                    # Check both metadata and top-level confidence
                    evidence_confidence = evidence.get('metadata', {}).get('confidence') or evidence.get('confidence', 0.0)
                    if evidence_confidence > filter_value:
                        return False
                else:
                    # Unknown filter key
                    self.logger.warning(f"Unknown filter key: {filter_key}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Filter matching failed: {e}")
            return False
    
    def _format_search_result(self, result: Any) -> Dict[str, Any]:
        """
        Format txtai search result into standard evidence format.
        
        Args:
            result: Raw search result from txtai
            
        Returns:
            Formatted evidence dictionary
        """
        try:
            if isinstance(result, dict):
                # txtai returns dict with id, text, score
                # Try to extract metadata from the text if it's not in metadata
                text = result.get('text', '')
                doc_id = result.get('id')
                
                # If we have a doc_id, try to get the original document
                if doc_id is not None and hasattr(self.index, 'documents') and self.index.documents:
                    try:
                        doc_id_int = int(doc_id) if isinstance(doc_id, str) else doc_id
                        if 0 <= doc_id_int < len(self.index.documents):
                            doc = self.index.documents[doc_id_int]
                            return {
                                "quote_text": doc.get('quote_text', doc.get('text', '')),
                                "document_name": doc.get('metadata', {}).get('document_name', 'Unknown'),
                                "dimension": doc.get('metadata', {}).get('dimension', 'Unknown'),
                                "confidence": doc.get('metadata', {}).get('confidence', 0.0),
                                "relevance_score": result.get('score', 0.0),
                                "metadata": doc.get('metadata', {})
                            }
                    except (ValueError, TypeError):
                        pass
                
                # Fallback: try to parse metadata from text
                # Text format: "test_doc3.txt wisdom evidence: Brevity is the soul of wit."
                if ' evidence: ' in text:
                    parts = text.split(' evidence: ')
                    if len(parts) == 2:
                        metadata_part = parts[0]
                        quote_text = parts[1]
                        
                        # Parse metadata part: "test_doc3.txt wisdom"
                        metadata_parts = metadata_part.split(' ')
                        if len(metadata_parts) >= 2:
                            document_name = metadata_parts[0]
                            dimension = metadata_parts[1]
                            
                            return {
                                "quote_text": quote_text,
                                "document_name": document_name,
                                "dimension": dimension,
                                "confidence": 0.0,  # Default confidence
                                "relevance_score": result.get('score', 0.0),
                                "metadata": {
                                    'document_name': document_name,
                                    'dimension': dimension,
                                    'confidence': 0.0,
                                    'extraction_method': 'Unknown',
                                    'source_type': 'Unknown'
                                }
                            }
                elif ' evidence:' in text:
                    # Handle case without space before evidence
                    parts = text.split(' evidence:')
                    if len(parts) == 2:
                        metadata_part = parts[0]
                        quote_text = parts[1]
                        
                        # Parse metadata part: "test_doc3.txt wisdom"
                        metadata_parts = metadata_part.split(' ')
                        if len(metadata_parts) >= 2:
                            document_name = metadata_parts[0]
                            dimension = metadata_parts[1]
                            
                            return {
                                "quote_text": quote_text,
                                "document_name": document_name,
                                "dimension": dimension,
                                "confidence": 0.0,  # Default confidence
                                "relevance_score": result.get('score', 0.0),
                                "metadata": {
                                    'document_name': document_name,
                                    'dimension': dimension,
                                    'confidence': 0.0,
                                    'extraction_method': 'Unknown',
                                    'source_type': 'Unknown'
                                }
                            }
                
                # Final fallback
                return {
                    "quote_text": text,
                    "document_name": "Unknown",
                    "dimension": "Unknown",
                    "confidence": 0.0,
                    "relevance_score": result.get('score', 0.0),
                    "metadata": {}
                }
            elif isinstance(result, tuple) and len(result) >= 2:
                # txtai returns tuple (id, score) - this is the most common case
                doc_id, score = result[0], result[1]
                if hasattr(self.index, 'documents') and self.index.documents:
                    # Convert doc_id to int if it's a string
                    try:
                        doc_id_int = int(doc_id) if isinstance(doc_id, str) else doc_id
                        if 0 <= doc_id_int < len(self.index.documents):
                            doc = self.index.documents[doc_id_int]
                            return {
                                "quote_text": doc.get('quote_text', doc.get('text', '')),
                                "document_name": doc.get('document_name', 'Unknown'),
                                "dimension": doc.get('dimension', 'Unknown'),
                                "confidence": doc.get('confidence', 0.0),
                                "relevance_score": score,
                                "metadata": {
                                    'document_name': doc.get('document_name', 'Unknown'),
                                    'dimension': doc.get('dimension', 'Unknown'),
                                    'confidence': doc.get('confidence', 0.0),
                                    'extraction_method': doc.get('extraction_method', 'Unknown'),
                                    'source_type': doc.get('source_type', 'Unknown')
                                }
                            }
                    except (ValueError, TypeError):
                        pass
            
            # Fallback for unexpected result format
            return {
                "quote_text": str(result),
                "document_name": "Unknown",
                "dimension": "Unknown",
                "confidence": 0.0,
                "relevance_score": 0.0,
                "metadata": {}
            }
            
        except Exception as e:
            self.logger.warning(f"Result formatting failed: {e}")
            return {
                "quote_text": "Error formatting result",
                "document_name": "Unknown",
                "dimension": "Unknown",
                "confidence": 0.0,
                "relevance_score": 0.0,
                "metadata": {}
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    
    def generate_search_queries(self, statistical_findings: List[str], max_queries: int = 5) -> List[str]:
        """
        Generate intelligent search queries from statistical findings.
        
        This method uses LLM to analyze statistical findings and generate
        targeted search queries that are likely to find relevant evidence.
        
        Args:
            statistical_findings: List of statistical findings to analyze
            max_queries: Maximum number of queries to generate
            
        Returns:
            List of generated search queries
        """
        if not statistical_findings:
            return []
        
        if not self.llm_gateway:
            self.logger.warning("No LLM gateway available for query generation")
            return self._generate_fallback_queries(statistical_findings, max_queries)
        
        try:
            # Prepare the prompt for query generation
            prompt = self._build_query_generation_prompt(statistical_findings, max_queries)
            
            # Generate queries using LLM
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert research analyst specializing in evidence retrieval.",
                context="Generating semantic search queries"
            )
            
            # Log cost information to audit logger
            if self.audit_logger and metadata.get("usage"):
                usage_data = metadata["usage"]
                try:
                    self.audit_logger.log_cost(
                        operation="semantic_query_generation",
                        model=metadata.get("model", self.model),
                        tokens_used=usage_data.get("total_tokens", 0),
                        cost_usd=usage_data.get("response_cost_usd", 0.0),
                        agent_name="EvidenceMatchingWrapper",
                        metadata={
                            "prompt_tokens": usage_data.get("prompt_tokens", 0),
                            "completion_tokens": usage_data.get("completion_tokens", 0),
                            "attempts": metadata.get("attempts", 1),
                            "findings_count": len(statistical_findings)
                        }
                    )
                except Exception as e:
                    self.logger.error(f"Error logging cost for semantic query generation: {e}")
            
            if response and response.strip():
                queries = self._parse_generated_queries(response)
                # Limit to max_queries and filter out empty/duplicate queries
                unique_queries = list(dict.fromkeys([q.strip() for q in queries if q.strip()]))
                return unique_queries[:max_queries]
            
        except Exception as e:
            self.logger.error(f"LLM query generation failed: {e}")
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "query_generation_failed", {
                    "error": str(e),
                    "findings_count": len(statistical_findings)
                })
        
        # Fallback to rule-based query generation
        return self._generate_fallback_queries(statistical_findings, max_queries)
    
    def _build_query_generation_prompt(self, statistical_findings: List[str], max_queries: int) -> str:
        """Build the prompt for LLM query generation."""
        findings_text = "\n".join([f"- {finding}" for finding in statistical_findings])
        
        prompt = f"""You are an expert research analyst. Your task is to generate {max_queries} targeted search queries to find evidence that supports the statistical findings below.

The queries should be:
1. Specific and focused on key concepts from the findings
2. Likely to return relevant evidence quotes
3. 2-5 words each (concise but descriptive)
4. Different from each other to maximize evidence coverage

Statistical Findings:
{findings_text}

Generate exactly {max_queries} search queries, one per line, starting with a dash (-):
- [query 1]
- [query 2]
- [query 3]
- [query 4]
- [query 5]"""
        
        return prompt
    
    def _parse_generated_queries(self, response: str) -> List[str]:
        """Parse the LLM response to extract search queries."""
        queries = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                # Remove the dash and clean up
                query = line[1:].strip()
                if query:
                    queries.append(query)
            elif line and not line.startswith('-'):
                # Some lines might not have dashes, treat as queries
                queries.append(line)
        
        return queries
    
    def _generate_fallback_queries(self, statistical_findings: List[str], max_queries: int) -> List[str]:
        """
        Generate fallback queries using rule-based approach when LLM is unavailable.
        
        Args:
            statistical_findings: List of statistical findings to analyze
            max_queries: Maximum number of queries to generate
            
        Returns:
            List of generated fallback queries
        """
        queries = []
        
        # Extract key terms from all findings
        all_key_terms = []
        for finding in statistical_findings:
            # Extract key terms (words that are likely to be important)
            words = finding.split()
            # Filter out common stop words and short words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'only', 'majority', 'respondents', 'participants', 'consider', 'primary', 'source', 'from', 'believe', 'comes', 'formal'}
            
            key_terms = [word.lower() for word in words if len(word) > 2 and word.lower() not in stop_words and not word.isdigit()]
            all_key_terms.extend(key_terms)
        
        # Remove duplicates and prioritize longer/more meaningful terms
        unique_terms = list(dict.fromkeys(all_key_terms))
        unique_terms.sort(key=lambda x: len(x), reverse=True)  # Sort by length, longer terms first
        
        # Generate queries from key terms
        for i in range(0, min(len(unique_terms), max_queries)):
            if i < len(unique_terms):
                queries.append(unique_terms[i])
        
        # If we don't have enough queries, add some generic ones
        while len(queries) < max_queries:
            queries.append("evidence")
        
        return queries[:max_queries]
    
    def search_evidence_with_auto_queries(self, statistical_findings: List[str], 
                                        max_queries: int = 5, 
                                        results_per_query: int = 3,
                                        filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for evidence using automatically generated queries from statistical findings.
        
        This is a convenience method that combines query generation with evidence search.
        
        Args:
            statistical_findings: List of statistical findings to analyze
            max_queries: Maximum number of queries to generate
            results_per_query: Number of results to return per query
            filters: Optional metadata filters to apply
            
        Returns:
            List of evidence results, ranked by relevance
        """
        if not self.index:
            self.logger.warning("No evidence index available. Call build_index() first.")
            return []
        
        # Generate search queries
        queries = self.generate_search_queries(statistical_findings, max_queries)
        
        if not queries:
            self.logger.warning("No search queries generated")
            return []
        
        # Search for evidence using each query
        all_results = []
        seen_quotes = set()  # Track unique quotes to avoid duplicates
        
        for query in queries:
            try:
                results = self.search_evidence(query, limit=results_per_query, filters=filters)
                
                for result in results:
                    quote_text = result.get('quote_text', '')
                    if quote_text and quote_text not in seen_quotes:
                        all_results.append(result)
                        seen_quotes.add(quote_text)
                        
                        # Stop if we have enough unique results
                        if len(all_results) >= max_queries * results_per_query:
                            break
                
                if len(all_results) >= max_queries * results_per_query:
                    break
                    
            except Exception as e:
                self.logger.warning(f"Search failed for query '{query}': {e}")
                continue
        
        # Sort by relevance score (higher is better)
        all_results.sort(key=lambda x: x.get('relevance_score', 0.0), reverse=True)
        
        self.logger.info(f"Auto-query search returned {len(all_results)} unique evidence pieces from {len(queries)} queries")
        return all_results

    def search(self, query: str, limit: int = 5) -> List[Tuple[int, float]]:
        """
        Compatibility method for txtai-style search interface.
        
        This allows our wrapper to be used as a drop-in replacement for txtai indexes
        in synthesis agents and other components.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of (doc_id, score) tuples matching txtai interface
        """
        if not self.index:
            return []
        
        try:
            # Use our intelligent search method
            results = self.search_evidence(query, limit=limit)
            
            # Convert to txtai-compatible format: (doc_id, score)
            txtai_results = []
            for i, result in enumerate(results):
                # Use the index in our results list as doc_id
                doc_id = i
                # Convert relevance_score to a 0-1 scale if needed
                score = min(1.0, max(0.0, result.get('relevance_score', 0.0)))
                txtai_results.append((doc_id, score))
            
            return txtai_results
            
        except Exception as e:
            self.logger.error(f"Search compatibility method failed: {e}")
            return []

    @property
    def documents(self) -> List[Dict[str, Any]]:
        """
        Compatibility property for txtai-style document access.
        
        This allows synthesis agents to access evidence documents in the expected format.
        
        Returns:
            List of evidence documents with txtai-compatible structure
        """
        if not self.index:
            return []
        
        # Convert our evidence data to txtai-compatible format
        txtai_documents = []
        for evidence in self.evidence_data:
            txtai_doc = {
                'text': evidence.get('quote_text', ''),
                'metadata': {
                    'document_name': evidence.get('document_name', 'Unknown'),
                    'dimension': evidence.get('dimension', 'Unknown'),
                    'confidence': evidence.get('confidence', 0.0)
                }
            }
            txtai_documents.append(txtai_doc)
        
        return txtai_documents
    
    def find_supporting_evidence(
        self,
        statistical_finding: str,
        framework_context: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find evidence that directly supports a statistical finding using LLM intelligence.
        
        This method provides a high-level interface for finding evidence that supports
        specific statistical findings within a framework context.
        
        Args:
            statistical_finding: Description of the statistical finding
            framework_context: Framework description for context
            limit: Maximum number of evidence pieces to return
            
        Returns:
            List of evidence dictionaries with relevance scores
        """
        try:
            # Generate targeted search queries for this finding
            queries = self.generate_search_queries([statistical_finding], max_queries=3)
            
            if not queries:
                self.logger.warning(f"No search queries generated for finding: {statistical_finding}")
                return []
            
            # Search for evidence using the generated queries
            all_results = []
            seen_quotes = set()
            
            for query in queries:
                results = self.search_evidence(query, limit=limit, filters=None)
                
                for result in results:
                    quote_text = result.get('quote_text', '')
                    if quote_text and quote_text not in seen_quotes:
                        all_results.append(result)
                        seen_quotes.add(quote_text)
                        
                        if len(all_results) >= limit:
                            break
                
                if len(all_results) >= limit:
                    break
            
            # Sort by relevance score
            all_results.sort(key=lambda x: x.get('relevance_score', 0.0), reverse=True)
            
            self.logger.info(f"Found {len(all_results)} supporting evidence pieces for finding: {statistical_finding}")
            return all_results[:limit]
            
        except Exception as e:
            self.logger.error(f"Error finding supporting evidence: {e}")
            if self.audit_logger:
                self.audit_logger.log_agent_event("EvidenceMatchingWrapper", "find_supporting_evidence_failed", {
                    "finding": statistical_finding,
                    "error": str(e)
                })
            return []