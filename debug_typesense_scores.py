#!/usr/bin/env python3
"""
Debug script to investigate Typesense raw scoring values.
"""

import logging
from discernus.core.typesense_corpus_service import TypesenseCorpusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def debug_typesense_scores():
    """Debug the raw Typesense scoring values."""
    
    ts_service = TypesenseCorpusService()
    
    if not ts_service.client:
        print("❌ Typesense not available")
        return
    
    # Create test data with known differences
    test_docs = [
        {
            "content": "The quick brown fox jumps over the lazy dog",
            "file_path": "/test/original.txt",
            "filename": "original.txt",
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 43,
            "context": "Original text"
        },
        {
            "content": "The quick brown fox jumps over the lazy cat",
            "file_path": "/test/one_word_diff.txt",
            "filename": "one_word_diff.txt",
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 43,
            "context": "One word different"
        },
        {
            "content": "A fast brown fox leaps over the sleepy dog",
            "file_path": "/test/several_diff.txt",
            "filename": "several_diff.txt",
            "speaker": "test",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 42,
            "context": "Several words different"
        }
    ]
    
    # Create fresh index
    ts_service.create_index(force_recreate=True)
    ts_service.index_corpus_files(test_docs)
    
    # Test query
    query = "The quick brown fox jumps over the lazy dog"
    
    print(f"\n🔍 Debug Query: '{query}'")
    print("=" * 80)
    
    # Get raw search results
    try:
        search_params = {
            "q": query,
            "query_by": "content",
            "per_page": 10,
            "typo_tolerance_enabled": True,
            "num_typos": 2
        }
        
        raw_response = ts_service.client.collections[ts_service.index_name].documents.search(search_params)
        
        print(f"Raw response structure: {list(raw_response.keys())}")
        
        if 'hits' in raw_response:
            print(f"\nFound {len(raw_response['hits'])} hits:")
            
            for i, hit in enumerate(raw_response['hits']):
                print(f"\n--- Hit {i+1} ---")
                print(f"Available fields: {list(hit.keys())}")
                
                # Show text_match and text_match_info
                if 'text_match' in hit:
                    print(f"text_match: {hit['text_match']}")
                if 'text_match_info' in hit:
                    print(f"text_match_info: {hit['text_match_info']}")
                
                # Show document info
                doc = hit.get('document', {})
                filename = doc.get('filename', 'unknown')
                content = doc.get('content', '')[:50] + "..."
                print(f"filename: {filename}")
                print(f"content: {content}")
                
                # Show highlights
                if 'highlights' in hit:
                    print(f"highlights: {hit['highlights']}")
        
        print(f"\n{'='*80}")
        print("Now testing our service layer:")
        
        # Test our service layer
        results = ts_service.search_quotes(query, fuzziness=2, size=10)
        
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  filename: {result['filename']}")
            print(f"  normalized_score: {result['score']:.1f}%")
            print(f"  raw_score: {result['raw_score']}")
            print(f"  tokens_matched: {result['tokens_matched']}")
            print(f"  query_tokens: {result['query_tokens']}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    debug_typesense_scores()

