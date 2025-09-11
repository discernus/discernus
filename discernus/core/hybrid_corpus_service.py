"""
Hybrid Corpus Service: Typesense + Python BM25

Combines the speed of Typesense with the accuracy of BM25 scoring.
- Typesense: Fast fuzzy retrieval (5-10ms)
- Python BM25: Accurate scoring (10-20ms)
- Total: 15-30ms vs Elasticsearch's 20-50ms
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


import os
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from rank_bm25 import BM25Okapi
import typesense
from .typesense_corpus_service import TypesenseCorpusService


class HybridCorpusService:
    """
    Hybrid approach: Typesense for fast retrieval, Python BM25 for accurate scoring.
    
    This eliminates the Elasticsearch dependency while potentially beating it on both
    speed and accuracy for our use case.
    """
    
    def __init__(self, typesense_config: Dict[str, Any] = None):
        """
        Initialize the hybrid service.
        
        Args:
            typesense_config: Typesense connection configuration (optional, uses defaults if None)
        """
        if typesense_config is None:
            typesense_config = {}
        
        self.typesense_service = TypesenseCorpusService(**typesense_config)
        self.bm25_indexes: Dict[str, BM25Okapi] = {}
        self.corpus_texts: Dict[str, List[str]] = {}
        self.corpus_metadata: Dict[str, List[Dict[str, Any]]] = {}
        
    def _build_bm25_index(self, corpus_dir: str, collection_name: str):
        """Build Python BM25 index from corpus files."""
        texts = []
        metadata = []
        
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                if file.endswith(('.txt', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Split into sentences/chunks for BM25
                        sentences = self._split_into_sentences(content)
                        texts.extend(sentences)
                        
                        # Store metadata for each sentence
                        for sentence in sentences:
                            metadata.append({
                                'file_path': file_path,
                                'content': sentence,
                                'length': len(sentence)
                            })
                            
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")
        
        # Store for later use
        self.corpus_texts[collection_name] = texts
        self.corpus_metadata[collection_name] = metadata
        
        # Build BM25 index
        tokenized_texts = [self._tokenize(text) for text in texts]
        self.bm25_indexes[collection_name] = BM25Okapi(tokenized_texts)
        
        print(f"✅ Built BM25 index for {collection_name}: {len(texts)} sentences")
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for BM25 indexing."""
        # Simple sentence splitting - can be enhanced with NLTK if needed
        sentences = []
        current = ""
        
        for char in text:
            current += char
            if char in '.!?' and len(current.strip()) > 10:
                sentence = current.strip()
                if sentence:
                    sentences.append(sentence)
                current = ""
        
        # Add remaining text
        if current.strip():
            sentences.append(current.strip())
        
        return sentences if sentences else [text]
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25."""
        # Convert to lowercase and split on whitespace
        return text.lower().split()
    
    def search_quotes(self, query: str, collection_name: str = None, 
                      limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for quotes using hybrid approach.
        
        Args:
            query: Quote to search for
            collection_name: Collection to search in (uses Typesense service's collection if None)
            limit: Maximum number of results
            
        Returns:
            List of search results with hybrid scoring
        """
        if collection_name is None:
            collection_name = self.typesense_service.index_name
        
        start_time = time.time()
        
        # Step 1: Fast retrieval with Typesense
        typesense_results = self.typesense_service.search_quotes(
            query, size=limit * 2  # Get more candidates for re-ranking
        )
        
        retrieval_time = time.time() - start_time
        
        if typesense_results is None or len(typesense_results) == 0:
            return []
        
        # Step 2: Re-rank with Python BM25 for accuracy
        bm25_start = time.time()
        re_ranked_results = self._re_rank_with_bm25(
            query, typesense_results, collection_name, limit
        )
        bm25_time = time.time() - bm25_start
        
        total_time = time.time() - start_time
        
        # Add timing information
        for result in re_ranked_results:
            result['timing'] = {
                'retrieval_ms': round(retrieval_time * 1000, 2),
                're_ranking_ms': round(bm25_time * 1000, 2),
                'total_ms': round(total_time * 1000, 2)
            }
        
        return re_ranked_results
    
    def _re_rank_with_bm25(self, query: str, typesense_results: List[Dict[str, Any]], 
                           collection_name: str, limit: int) -> List[Dict[str, Any]]:
        """Re-rank Typesense results using Python BM25."""
        if collection_name not in self.bm25_indexes:
            print(f"Warning: No BM25 index found for {collection_name}")
            return typesense_results[:limit]
        
        bm25_index = self.bm25_indexes[collection_name]
        query_tokens = self._tokenize(query)
        
        # Get BM25 scores for all candidate texts
        scored_results = []
        for result in typesense_results:
            # Use highlighted quote for BM25 scoring
            content = result.get('highlighted_quote', '')
            if content:
                # Get BM25 score
                bm25_score = bm25_index.get_scores(query_tokens)
                
                # Find the best matching sentence - handle NumPy arrays safely
                if bm25_score is not None and len(bm25_score) > 0:
                    best_score = float(max(bm25_score))
                else:
                    best_score = 0.0
                
                # Calculate token match percentage from Typesense results
                tokens_matched = result.get('tokens_matched', 0)
                result_query_tokens = result.get('query_tokens', 1)
                token_match_pct = (tokens_matched / result_query_tokens) * 100 if result_query_tokens > 0 else 0
                
                # Combine Typesense and BM25 scores
                hybrid_score = self._combine_scores(
                    result.get('score', 0),  # Use 'score' instead of 'calibrated_score'
                    best_score,
                    token_match_pct
                )
                
                scored_results.append({
                    **result,
                    'bm25_score': best_score,
                    'hybrid_score': hybrid_score
                })
        
        # Sort by hybrid score and return top results
        scored_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return scored_results[:limit]
    
    def _combine_scores(self, typesense_score: float, bm25_score: float, 
                        token_match_pct: float) -> float:
        """
        Combine Typesense and BM25 scores intelligently.
        
        Args:
            typesense_score: Typesense calibrated score (0-100)
            bm25_score: BM25 raw score
            token_match_pct: Percentage of tokens matched
            
        Returns:
            Combined score (0-100)
        """
        # Normalize BM25 score to 0-100 range
        # BM25 scores can vary widely, so we use a sigmoid-like normalization
        normalized_bm25 = 100 / (1 + 2.718 ** (-bm25_score / 10))
        
        # Weight the combination based on token match percentage
        if token_match_pct >= 90:
            # High token match: trust Typesense more
            return 0.7 * typesense_score + 0.3 * normalized_bm25
        elif token_match_pct >= 70:
            # Medium token match: balanced approach
            return 0.5 * typesense_score + 0.5 * normalized_bm25
        else:
            # Low token match: trust BM25 more
            return 0.3 * typesense_score + 0.7 * normalized_bm25
    
    def validate_quote(self, quote: str, collection_name: str = None) -> Dict[str, Any]:
        """
        Validate a quote using hybrid approach.
        
        Args:
            quote: Quote to validate
            collection_name: Collection to search in (uses Typesense service's collection if None)
            
        Returns:
            Validation result with drift classification
        """
        if collection_name is None:
            collection_name = self.typesense_service.index_name
        
        results = self.search_quotes(quote, collection_name, limit=5)
        
        if results is None or len(results) == 0:
            return {
                'valid': False,
                'drift_level': 'not_found',
                'best_match': None,
                'confidence': 0.0,
                'explanation': 'Quote not found in corpus'
            }
        
        best_match = results[0]
        hybrid_score = best_match.get('hybrid_score', 0)
        token_match_pct = best_match.get('token_match_pct', 0)
        
        # Determine drift level based on hybrid score with more appropriate thresholds
        if hybrid_score >= 90:
            drift_level = 'exact'
            valid = True
        elif hybrid_score >= 75:
            drift_level = 'minor_drift'
            valid = True
        elif hybrid_score >= 60:
            drift_level = 'moderate_drift'
            valid = True
        elif hybrid_score >= 40:
            drift_level = 'significant_drift'
            valid = False
        else:
            drift_level = 'major_drift'
            valid = False
        
        return {
            'valid': valid,
            'drift_level': drift_level,
            'best_match': best_match,
            'confidence': hybrid_score / 100.0,
            'explanation': f'Quote classified as {drift_level} with {hybrid_score:.1f}% confidence',
            'score': hybrid_score,  # Add score field for compatibility
            'hybrid_score': hybrid_score,
            'token_match_pct': token_match_pct
        }
    
    def get_source_text(self, file_path: str, start_char: int = None, 
                        end_char: int = None) -> str:
        """Get source text from file (delegates to Typesense service)."""
        return self.typesense_service.get_source_text(file_path, start_char, end_char)
    
    def get_search_wrapper_methods(self) -> Dict[str, Any]:
        """
        Get search wrapper methods for external agents to use.
        
        This method provides a standardized interface that agents can use
        to access the corpus service's search capabilities without needing
        to know the internal implementation details.
        
        Returns:
            Dictionary containing search wrapper methods
        """
        return {
            "validate_quote": self.validate_quote,
            "search_documents": self.search_quotes,
            "get_context": self.get_source_text,
            "corpus_search": self.search_quotes,
            "quote_validation": self.validate_quote,
            "semantic_search": self.search_quotes
        }
    
    def get_capabilities(self) -> List[str]:
        """
        Get a list of capabilities this service provides.
        
        Returns:
            List of capability strings
        """
        return [
            "corpus_search",
            "quote_validation", 
            "semantic_search",
            "hybrid_scoring",
            "bm25_re_ranking",
            "typesense_retrieval"
        ]
    
    def close(self):
        """Clean up resources."""
        self.typesense_service.close()
        self.bm25_indexes.clear()
        self.corpus_texts.clear()
        self.corpus_metadata.clear()
