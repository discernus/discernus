#!/usr/bin/env python3
"""
Test script to investigate Typesense scoring mechanisms and find the right approach
for quote validation in our fact-checking system.
"""

import json
import logging
from discernus.core.typesense_corpus_service import TypesenseCorpusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_typesense_scoring():
    """Test different Typesense scoring approaches."""
    
    # Initialize service
    ts_service = TypesenseCorpusService()
    
    if not ts_service.client:
        print("❌ Typesense not available")
        return
    
    # Create test data with known similarity levels
    test_docs = [
        {
            "content": "The quick brown fox jumps over the lazy dog",
            "file_path": "/test/exact.txt",
            "filename": "exact.txt",
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 43,
            "context": "Exact match test"
        },
        {
            "content": "The quick brown fox jumps over the lazy cat",  # One word different
            "file_path": "/test/minor.txt", 
            "filename": "minor.txt",
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 43,
            "context": "Minor difference test"
        },
        {
            "content": "A fast brown fox leaps over the sleepy dog",  # Several words different
            "file_path": "/test/major.txt",
            "filename": "major.txt", 
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 42,
            "context": "Major difference test"
        },
        {
            "content": "Politics is the art of the possible in democratic societies",  # Completely different
            "file_path": "/test/unrelated.txt",
            "filename": "unrelated.txt",
            "speaker": "test", 
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 58,
            "context": "Unrelated content test"
        }
    ]
    
    # Create fresh index
    ts_service.create_index(force_recreate=True)
    ts_service.index_corpus_files(test_docs)
    
    # Test query
    query = "The quick brown fox jumps over the lazy dog"
    
    print(f"\n🔍 Testing query: '{query}'")
    print("=" * 80)
    
    # Test different search approaches
    approaches = [
        {"name": "Default Search", "params": {"fuzziness": 1, "size": 10}},
        {"name": "Strict Search", "params": {"fuzziness": 0, "size": 10}}, 
        {"name": "Fuzzy Search", "params": {"fuzziness": 2, "size": 10}},
        {"name": "Very Fuzzy", "params": {"fuzziness": 3, "size": 10}}
    ]
    
    for approach in approaches:
        print(f"\n📊 {approach['name']}:")
        print("-" * 40)
        
        results = ts_service.search_quotes(query, **approach['params'])
        
        for i, result in enumerate(results):
            score = result.get('score', 0)
            filename = result.get('filename', 'unknown')
            content_preview = result.get('highlighted_content', '')[:50] + "..."
            
            print(f"  {i+1}. {filename}: Score={score}")
            print(f"     Content: {content_preview}")
    
    # Test raw Typesense API to see actual response format
    print(f"\n🔬 Raw Typesense API Response:")
    print("=" * 80)
    
    try:
        search_params = {
            "q": query,
            "query_by": "content", 
            "per_page": 4,
            "typo_tolerance_enabled": True,
            "num_typos": 2
        }
        
        raw_response = ts_service.client.collections[ts_service.index_name].documents.search(search_params)
        
        print(f"Raw response keys: {list(raw_response.keys())}")
        
        if 'hits' in raw_response:
            for i, hit in enumerate(raw_response['hits']):
                print(f"\nHit {i+1}:")
                print(f"  Available fields: {list(hit.keys())}")
                
                if 'text_match' in hit:
                    print(f"  text_match: {hit['text_match']}")
                if 'text_match_info' in hit:
                    print(f"  text_match_info: {hit['text_match_info']}")
                if 'highlights' in hit:
                    print(f"  highlights: {hit['highlights']}")
                
                doc = hit.get('document', {})
                filename = doc.get('filename', 'unknown')
                print(f"  filename: {filename}")
                
    except Exception as e:
        print(f"Error with raw API: {e}")


if __name__ == "__main__":
    test_typesense_scoring()

