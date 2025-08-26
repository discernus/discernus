"""
Typesense-based Corpus Index Service for fast, fuzzy quote lookup.

This service provides deterministic but appropriately fuzzy search of corpus files
that allows mapping LLM errors to the reality of source text.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from typesense import Client
from typesense.exceptions import ObjectNotFound, RequestMalformed

logger = logging.getLogger(__name__)


class TypesenseCorpusService:
    """
    Service for indexing and searching corpus files using Typesense.
    
    Provides fast, fuzzy search capabilities for quote validation and fact checking.
    """
    
    def __init__(self, api_key: str = "xyz", nodes: List[Dict] = None, index_name: str = "corpus"):
        """
        Initialize the Typesense corpus service.
        
        Args:
            api_key: API key for Typesense (default: "xyz" for local development)
            nodes: List of Typesense nodes (default: localhost:8108)
            index_name: Name of the Typesense collection
        """
        if nodes is None:
            nodes = [{"host": "localhost", "port": "8108", "protocol": "http"}]
        
        self.index_name = index_name
        self.client = Client({
            "api_key": api_key,
            "nodes": nodes,
            "connection_timeout_seconds": 2
        })
        
        # Test connection
        try:
            # Try to retrieve collections to test connection
            self.client.collections.retrieve()
            logger.info(f"Connected to Typesense at {nodes[0]['host']}:{nodes[0]['port']}")
        except Exception as e:
            logger.warning(f"Could not connect to Typesense: {e}")
            self.client = None
    
    def create_index(self, force_recreate: bool = False) -> bool:
        """
        Create the corpus collection with appropriate schema.
        
        Args:
            force_recreate: If True, delete existing collection before creating
            
        Returns:
            True if collection created successfully, False otherwise
        """
        if not self.client:
            logger.error("No Typesense client available")
            return False
        
        try:
            # Delete existing collection if force_recreate is True
            if force_recreate:
                try:
                    self.client.collections[self.index_name].delete()
                    logger.info(f"Deleted existing collection: {self.index_name}")
                except ObjectNotFound:
                    pass  # Collection didn't exist
            
            # Create collection with schema
            schema = {
                "name": self.index_name,
                "fields": [
                    {"name": "content", "type": "string"},
                    {"name": "file_path", "type": "string"},
                    {"name": "filename", "type": "string"},
                    {"name": "speaker", "type": "string"},
                    {"name": "date", "type": "string"},
                    {"name": "source_type", "type": "string"},
                    {"name": "start_char", "type": "int32"},
                    {"name": "end_char", "type": "int32"},
                    {"name": "context", "type": "string"}
                ],
                "default_sorting_field": "start_char"
            }
            
            self.client.collections.create(schema)
            logger.info(f"Created Typesense collection: {self.index_name}")
            return True
                
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False
    
    def index_corpus_files(self, corpus_files: List[Dict[str, Any]]) -> bool:
        """
        Index corpus files into Typesense.
        
        Args:
            corpus_files: List of corpus file dictionaries with content and metadata
            
        Returns:
            True if indexing successful, False otherwise
        """
        if not self.client:
            logger.error("No Typesense client available")
            return False
        
        try:
            # Ensure collection exists
            try:
                self.client.collections[self.index_name].retrieve()
            except ObjectNotFound:
                if not self.create_index():
                    return False
            
            # Index each file
            for file_data in corpus_files:
                doc = {
                    "content": file_data.get("content", ""),
                    "file_path": file_data.get("file_path", ""),
                    "filename": file_data.get("filename", ""),
                    "speaker": file_data.get("speaker", ""),
                    "date": file_data.get("date", ""),
                    "source_type": file_data.get("source_type", "corpus"),
                    "start_char": file_data.get("start_char", 0),
                    "end_char": file_data.get("end_char", 0),
                    "context": file_data.get("context", "")
                }
                
                # Use file path as document ID for deduplication
                doc_id = file_data.get("file_path", "").replace("/", "_").replace("\\", "_")
                if not doc_id:
                    doc_id = f"doc_{int(time.time() * 1000)}"
                
                try:
                    self.client.collections[self.index_name].documents.upsert(doc)
                except Exception as e:
                    logger.warning(f"Failed to index document {doc_id}: {e}")
                    continue
            
            logger.info(f"Indexed {len(corpus_files)} corpus files")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing corpus files: {e}")
            return False
    
    def search_quotes(self, quote_text: str, fuzziness: int = 1, size: int = 10) -> List[Dict[str, Any]]:
        """
        Search for quotes using fuzzy matching with highlighting.
        
        Args:
            quote_text: The quote text to search for
            fuzziness: Fuzzy matching level (0-4)
            size: Maximum number of results to return
            
        Returns:
            List of search results with highlighted quotes and minimal context
        """
        if not self.client:
            logger.error("No Typesense client available")
            return []
        
        try:
            # Build search parameters with highlighting
            search_parameters = {
                "q": quote_text,
                "query_by": "content",
                "filter_by": "",
                "sort_by": "_text_match:desc",
                "per_page": size,
                "typo_tolerance_enabled": True,
                "num_typos": fuzziness,
                # Highlighting parameters for quote extraction
                "highlight_full_fields": True,
                "highlight_start_tag": "<mark>",
                "highlight_end_tag": "</mark>",
                "snippet_length": 150,  # Context around the match
                "highlight_affix_num_tokens": 3  # Words before/after the match
            }
            
            response = self.client.collections[self.index_name].documents.search(search_parameters)
            
            # Process results with highlighted content
            results = []
            hits = response.get("hits", [])
            
            if hits:
                for hit in hits:
                    document = hit["document"]
                    raw_score = hit.get("text_match", 0)
                    
                    # Extract token matching info
                    text_match_info = hit.get("text_match_info", {})
                    tokens_matched = text_match_info.get("tokens_matched", 0)
                    query_tokens = len(quote_text.split())
                    
                    # Calibrate score based on query length and token matching
                    if query_tokens > 0:
                        token_similarity = (tokens_matched / query_tokens) * 100
                        length_factor = min(1.2, max(0.8, 10 / query_tokens))
                        calibrated_score = min(100, token_similarity * length_factor)
                    else:
                        calibrated_score = 0
                    
                    # Extract highlighted content (quote + minimal context)
                    highlighted_content = hit.get("highlights", [{}])[0].get("snippet", "")
                    if not highlighted_content:
                        # Fallback: extract content around the match position
                        content = document.get("content", "")
                        match_pos = content.lower().find(quote_text.lower())
                        if match_pos >= 0:
                            start = max(0, match_pos - 50)
                            end = min(len(content), match_pos + len(quote_text) + 50)
                            highlighted_content = content[start:end]
                        else:
                            highlighted_content = content[:200] + "..."
                    
                    # Clean up highlighting tags for clean text
                    clean_content = highlighted_content.replace("<mark>", "").replace("</mark>", "")
                    
                    result = {
                        "score": calibrated_score,  # Calibrated 0-100 score
                        "raw_score": raw_score,  # Raw text_match for debugging
                        "tokens_matched": tokens_matched,
                        "query_tokens": query_tokens,
                        "file_path": document.get("file_path", ""),
                        "filename": document.get("filename", ""),
                        "speaker": document.get("speaker", ""),
                        "date": document.get("date", ""),
                        "start_char": document.get("start_char", 0),
                        "end_char": document.get("end_char", 0),
                        # Return only the highlighted quote + minimal context
                        "highlighted_quote": clean_content,
                        "raw_highlighted": highlighted_content,  # With tags for debugging
                        # Remove full content to save memory
                        "content_length": len(document.get("content", ""))
                    }
                    results.append(result)
            
            logger.info(f"Found {len(results)} results for quote: {quote_text[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching quotes: {e}")
            return []
    
    def validate_quote(self, quote_text: str, expected_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a quote against the corpus index.
        
        Args:
            quote_text: The quote text to validate
            expected_file: Optional expected source file for validation
            
        Returns:
            Validation result with drift analysis and source mapping
        """
        if not self.client:
            return {
                "valid": False,
                "error": "No Typesense client available",
                "drift_level": "unknown"
            }
        
        try:
            # Search for the quote
            results = self.search_quotes(quote_text, fuzziness=2, size=5)
            
            if not results:
                return {
                    "valid": False,
                    "drift_level": "hallucination",
                    "message": "Quote not found in corpus",
                    "suggestions": []
                }
            
            # Analyze the best match
            best_match = results[0]
            score = best_match["score"]
            
            # Determine drift level based on score and token matching
            tokens_matched = best_match.get("tokens_matched", 0)
            query_tokens = best_match.get("query_tokens", 1)
            
            # Calculate token match percentage
            token_match_pct = (tokens_matched / query_tokens) * 100
            
            # Use standard 40/60/80 thresholds with normalized scores
            # These thresholds are now directly comparable to Elasticsearch BM25 scores
            if score >= 80:  # High similarity - exact or very close match
                drift_level = "exact"
                valid = True
            elif score >= 60:  # Medium similarity - minor differences
                drift_level = "minor_drift"
                valid = True
            elif score >= 40:  # Lower similarity - significant differences
                drift_level = "significant_drift"
                valid = True
            else:  # Low similarity - major differences or mismatch
                drift_level = "major_drift"
                valid = False
            
            # Check if expected file matches
            file_match = False
            if expected_file:
                file_match = best_match["file_path"] == expected_file
            
            return {
                "valid": valid,
                "drift_level": drift_level,
                "score": score,
                "best_match": best_match,
                "file_match": file_match,
                "all_matches": results,
                "message": f"Quote found with {drift_level} (score: {score})"
            }
            
        except Exception as e:
            logger.error(f"Error validating quote: {e}")
            return {
                "valid": False,
                "error": str(e),
                "drift_level": "error"
            }
    
    def get_source_text(self, file_path: str, start_char: int, end_char: int) -> Optional[str]:
        """
        Extract exact text from source file at specified character positions.
        
        Args:
            file_path: Path to the source file
            start_char: Starting character position
            end_char: Ending character position
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if start_char < len(content) and end_char <= len(content):
                    return content[start_char:end_char]
                else:
                    logger.warning(f"Character positions {start_char}-{end_char} out of range for file {file_path}")
                    return None
        except Exception as e:
            logger.error(f"Error reading source file {file_path}: {e}")
            return None
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the corpus collection."""
        if not self.client:
            return {"error": "No Typesense client available"}
        
        try:
            collection_info = self.client.collections[self.index_name].retrieve()
            
            return {
                "index_name": self.index_name,
                "document_count": collection_info.get("num_documents", 0),
                "index_size": "N/A",  # Typesense doesn't provide size info
                "status": "healthy" if self.client else "disconnected"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        """Close the Typesense connection."""
        # Typesense client doesn't need explicit closing
        logger.info("Typesense connection closed")
