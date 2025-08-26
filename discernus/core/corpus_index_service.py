"""
Corpus Index Service using Elasticsearch for fast, fuzzy quote lookup.

This service provides deterministic but appropriately fuzzy search of corpus files
that allows mapping LLM errors to the reality of source text.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

logger = logging.getLogger(__name__)


class CorpusIndexService:
    """
    Service for indexing and searching corpus files using Elasticsearch.
    
    Provides fast, fuzzy search capabilities for quote validation and fact checking.
    """
    
    def __init__(self, elasticsearch_url: str = "http://localhost:9200", index_name: str = "corpus"):
        """
        Initialize the corpus index service.
        
        Args:
            elasticsearch_url: URL for Elasticsearch instance
            index_name: Name of the Elasticsearch index
        """
        self.elasticsearch_url = elasticsearch_url
        self.index_name = index_name
        self.es = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Elasticsearch."""
        try:
            self.es = Elasticsearch([self.elasticsearch_url])
            if self.es.ping():
                logger.info(f"Connected to Elasticsearch at {self.elasticsearch_url}")
            else:
                logger.error(f"Failed to connect to Elasticsearch at {self.elasticsearch_url}")
                self.es = None
        except ConnectionError as e:
            logger.error(f"Connection error to Elasticsearch: {e}")
            self.es = None
    
    def create_index(self, force_recreate: bool = False) -> bool:
        """
        Create the corpus index with appropriate mappings.
        
        Args:
            force_recreate: If True, delete existing index before creating
            
        Returns:
            True if index created successfully, False otherwise
        """
        if not self.es:
            logger.error("No Elasticsearch connection available")
            return False
        
        try:
            # Delete existing index if force_recreate is True
            if force_recreate and self.es.indices.exists(index=self.index_name):
                self.es.indices.delete(index=self.index_name)
                logger.info(f"Deleted existing index: {self.index_name}")
            
            # Create index with mappings
            if not self.es.indices.exists(index=self.index_name):
                mapping = {
                    "mappings": {
                        "properties": {
                            "content": {
                                "type": "text",
                                "analyzer": "standard",
                                "search_analyzer": "standard"
                            },
                            "file_path": {
                                "type": "keyword"
                            },
                            "filename": {
                                "type": "keyword"
                            },
                            "speaker": {
                                "type": "keyword"
                            },
                            "date": {
                                "type": "date"
                            },
                            "source_type": {
                                "type": "keyword"
                            },
                            "start_char": {
                                "type": "integer"
                            },
                            "end_char": {
                                "type": "integer"
                            },
                            "context": {
                                "type": "text",
                                "analyzer": "standard"
                            }
                        }
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "analysis": {
                            "analyzer": {
                                "fuzzy_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": ["lowercase", "stop"]
                                }
                            }
                        }
                    }
                }
                
                self.es.indices.create(index=self.index_name, body=mapping)
                logger.info(f"Created Elasticsearch index: {self.index_name}")
                return True
            else:
                logger.info(f"Index {self.index_name} already exists")
                return True
                
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def index_corpus_files(self, corpus_files: List[Dict[str, Any]]) -> bool:
        """
        Index corpus files into Elasticsearch.
        
        Args:
            corpus_files: List of corpus file dictionaries with content and metadata
            
        Returns:
            True if indexing successful, False otherwise
        """
        if not self.es:
            logger.error("No Elasticsearch connection available")
            return False
        
        try:
            # Ensure index exists
            if not self.es.indices.exists(index=self.index_name):
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
                self.es.index(index=self.index_name, id=doc_id, body=doc)
            
            # Refresh index to make documents searchable
            self.es.indices.refresh(index=self.index_name)
            logger.info(f"Indexed {len(corpus_files)} corpus files")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing corpus files: {e}")
            return False
    
    def search_quotes(self, quote_text: str, fuzziness: str = "AUTO", size: int = 10) -> List[Dict[str, Any]]:
        """
        Search for quotes using fuzzy matching.
        
        Args:
            quote_text: The quote text to search for
            fuzziness: Fuzzy matching level ("0", "1", "2", "AUTO")
            size: Maximum number of results to return
            
        Returns:
            List of search results with source file information
        """
        if not self.es:
            logger.error("No Elasticsearch connection available")
            return []
        
        try:
            # Build search query with fuzzy matching
            query = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "fuzzy": {
                                    "content": {
                                        "value": quote_text,
                                        "fuzziness": fuzziness,
                                        "prefix_length": 2
                                    }
                                }
                            },
                            {
                                "match": {
                                    "content": {
                                        "query": quote_text,
                                        "operator": "and"
                                    }
                                }
                            }
                        ],
                        "minimum_should_match": 1
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {
                            "pre_tags": ["<mark>"],
                            "post_tags": ["</mark>"],
                            "fragment_size": 200
                        }
                    }
                },
                "size": size
            }
            
            response = self.es.search(index=self.index_name, body=query)
            
            # Process results
            results = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                highlight = hit.get("highlight", {}).get("content", [])
                
                result = {
                    "score": hit["_score"],
                    "file_path": source.get("file_path", ""),
                    "filename": source.get("filename", ""),
                    "speaker": source.get("speaker", ""),
                    "date": source.get("date", ""),
                    "start_char": source.get("start_char", 0),
                    "end_char": source.get("end_char", 0),
                    "highlighted_content": highlight[0] if highlight else "",
                    "full_content": source.get("content", "")
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
        if not self.es:
            return {
                "valid": False,
                "error": "No Elasticsearch connection available",
                "drift_level": "unknown"
            }
        
        try:
            # Search for the quote
            results = self.search_quotes(quote_text, fuzziness="AUTO", size=5)
            
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
            
            # Determine drift level based on score and content similarity
            if score > 10.0:  # High score indicates exact or very close match
                drift_level = "exact"
                valid = True
            elif score > 5.0:  # Medium score indicates minor drift
                drift_level = "minor_drift"
                valid = True
            elif score > 2.0:  # Lower score indicates significant drift
                drift_level = "significant_drift"
                valid = True
            else:  # Very low score indicates major drift or mismatch
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
                "message": f"Quote found with {drift_level} (score: {score:.2f})"
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
        """Get statistics about the corpus index."""
        if not self.es:
            return {"error": "No Elasticsearch connection available"}
        
        try:
            stats = self.es.indices.stats(index=self.index_name)
            count = self.es.count(index=self.index_name)
            
            return {
                "index_name": self.index_name,
                "document_count": count["count"],
                "index_size": stats["indices"][self.index_name]["total"]["store"]["size_in_bytes"],
                "status": "healthy" if self.es.ping() else "disconnected"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        """Close the Elasticsearch connection."""
        if self.es:
            self.es.close()
            logger.info("Closed Elasticsearch connection")
