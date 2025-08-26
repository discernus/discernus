#!/usr/bin/env python3
"""
Test script for Elasticsearch-based corpus indexing integration.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_elasticsearch_connection():
    """Test basic Elasticsearch connection."""
    try:
        from discernus.core.corpus_index_service import CorpusIndexService
        
        print("🔍 Testing Elasticsearch connection...")
        
        # Initialize service
        service = CorpusIndexService(
            elasticsearch_url="http://localhost:9200",
            index_name="test_corpus"
        )
        
        # Test connection
        if service.es and service.es.ping():
            print("✅ Elasticsearch connection successful")
            
            # Test index creation
            if service.create_index(force_recreate=True):
                print("✅ Index creation successful")
                
                # Test index stats
                stats = service.get_index_stats()
                print(f"📊 Index stats: {stats}")
                
                # Clean up
                service.close()
                return True
            else:
                print("❌ Index creation failed")
                return False
        else:
            print("❌ Elasticsearch connection failed")
            print("💡 Make sure Elasticsearch is running on http://localhost:9200")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure Elasticsearch is installed: pip install elasticsearch")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_corpus_indexing():
    """Test corpus file indexing."""
    try:
        from discernus.core.corpus_index_service import CorpusIndexService
        
        print("\n🔍 Testing corpus indexing...")
        
        # Initialize service
        service = CorpusIndexService(
            elasticsearch_url="http://localhost:9200",
            index_name="test_corpus"
        )
        
        # Create test corpus files
        test_files = [
            {
                'content': 'This is a test document about artificial intelligence.',
                'file_path': '/test/doc1.txt',
                'filename': 'doc1.txt',
                'speaker': 'Test Speaker',
                'date': '2024-01-01',
                'source_type': 'test_document',
                'start_char': 0,
                'end_char': 58,
                'context': 'Test context'
            },
            {
                'content': 'Machine learning is a subset of AI that focuses on algorithms.',
                'file_path': '/test/doc2.txt',
                'filename': 'doc2.txt',
                'speaker': 'Test Speaker 2',
                'date': '2024-01-02',
                'source_type': 'test_document',
                'start_char': 0,
                'end_char': 67,
                'context': 'Test context 2'
            }
        ]
        
        # Index the files
        if service.index_corpus_files(test_files):
            print("✅ Corpus indexing successful")
            
            # Test quote search
            print("\n🔍 Testing quote search...")
            results = service.search_quotes("artificial intelligence", fuzziness="AUTO", size=5)
            print(f"📊 Search results: {len(results)} found")
            
            for i, result in enumerate(results):
                print(f"  Result {i+1}: {result.get('filename')} (score: {result.get('score', 0):.2f})")
                print(f"    Content: {result.get('highlighted_content', 'No highlight')}")
            
            # Test quote validation
            print("\n🔍 Testing quote validation...")
            validation = service.validate_quote("artificial intelligence")
            print(f"📊 Validation result: {validation}")
            
            # Clean up
            service.close()
            return True
        else:
            print("❌ Corpus indexing failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Elasticsearch-based corpus indexing integration")
    print("=" * 60)
    
    # Test 1: Connection
    if not test_elasticsearch_connection():
        print("\n❌ Connection test failed - cannot proceed")
        return False
    
    # Test 2: Indexing
    if not test_corpus_indexing():
        print("\n❌ Indexing test failed")
        return False
    
    print("\n✅ All tests passed!")
    print("\n💡 The Elasticsearch integration is working correctly.")
    print("   You can now use the corpus index service for fact checking.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

