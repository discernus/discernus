#!/usr/bin/env python3
"""
Test script to see if we can get multiple hits from Typesense for comparison.
"""

import logging
from discernus.core.typesense_corpus_service import TypesenseCorpusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_multiple_hits():
    """Test if we can get multiple hits for comparison."""
    
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
    
    # Test different search strategies
    test_queries = [
        "The quick brown fox jumps over the lazy dog",  # Exact
        "The quick brown fox jumps over the lazy cat",  # One word different
        "A fast brown fox leaps over the sleepy dog",   # Several words different
        "quick brown fox",                              # Partial
        "fox dog",                                      # Very partial
    ]
    
    print("\n🔍 TESTING MULTIPLE SEARCH STRATEGIES")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 60)
        
        # Test different search parameters
        search_strategies = [
            {"name": "High Fuzziness", "fuzziness": 3, "size": 10},
            {"name": "Medium Fuzziness", "fuzziness": 2, "size": 10},
            {"name": "Low Fuzziness", "fuzziness": 1, "size": 10},
            {"name": "No Fuzziness", "fuzziness": 0, "size": 10},
        ]
        
        for strategy in search_strategies:
            print(f"\n  {strategy['name']}:")
            
            try:
                # Test raw API first
                search_params = {
                    "q": query,
                    "query_by": "content",
                    "per_page": strategy["size"],
                    "typo_tolerance_enabled": strategy["fuzziness"] > 0,
                    "num_typos": strategy["fuzziness"]
                }
                
                raw_response = ts_service.client.collections[ts_service.index_name].documents.search(search_params)
                hits = raw_response.get("hits", [])
                
                print(f"    Raw API: {len(hits)} hits")
                
                # Show hit details
                for i, hit in enumerate(hits[:3]):  # Show first 3
                    doc = hit.get("document", {})
                    filename = doc.get("filename", "unknown")
                    text_match = hit.get("text_match", 0)
                    print(f"      Hit {i+1}: {filename} (score: {text_match})")
                
                # Test our service layer
                results = ts_service.search_quotes(query, fuzziness=strategy["fuzziness"], size=strategy["size"])
                print(f"    Service Layer: {len(results)} results")
                
                for i, result in enumerate(results[:3]):  # Show first 3
                    filename = result.get("filename", "unknown")
                    score = result.get("score", 0)
                    raw_score = result.get("raw_score", 0)
                    print(f"      Result {i+1}: {filename} (norm: {score:.1f}%, raw: {raw_score})")
                
            except Exception as e:
                print(f"    Error: {e}")
        
        print("-" * 60)


if __name__ == "__main__":
    test_multiple_hits()

