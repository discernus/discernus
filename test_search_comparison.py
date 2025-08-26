#!/usr/bin/env python3
"""
Test script to compare Elasticsearch vs Typesense for corpus indexing and search.

This script will:
1. Test both systems with the same corpus data
2. Compare indexing performance
3. Compare search performance and accuracy
4. Benchmark quote validation
"""

import time
import json
import logging
from pathlib import Path

# Import both services
from discernus.core.corpus_index_service import CorpusIndexService
from discernus.core.typesense_corpus_service import TypesenseCorpusService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_corpus():
    """Create test corpus data for benchmarking."""
    test_files = [
        {
            "content": "The quick brown fox jumps over the lazy dog. This is a test document about animals and nature.",
            "file_path": "/test/animals.txt",
            "filename": "animals.txt",
            "speaker": "test_speaker",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 89,
            "context": "Test context for animals document"
        },
        {
            "content": "Politics is the art of the possible. We must work together to build a better future for all citizens.",
            "file_path": "/test/politics.txt",
            "filename": "politics.txt",
            "speaker": "test_speaker",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 108,
            "context": "Test context for politics document"
        },
        {
            "content": "Science is not only compatible with spirituality; it is a profound source of spirituality.",
            "file_path": "/test/science.txt",
            "filename": "science.txt",
            "speaker": "test_speaker",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 95,
            "context": "Test context for science document"
        },
        {
            "content": "The only way to do great work is to love what you do. Passion drives innovation and creativity.",
            "file_path": "/test/motivation.txt",
            "filename": "motivation.txt",
            "speaker": "test_speaker",
            "date": "2024-01-01T00:00:00",
            "source_type": "test",
            "start_char": 0,
            "end_char": 102,
            "context": "Test context for motivation document"
        }
    ]
    return test_files


def benchmark_elasticsearch():
    """Benchmark Elasticsearch performance."""
    logger.info("🔍 Benchmarking Elasticsearch...")
    
    try:
        # Initialize service
        start_time = time.time()
        es_service = CorpusIndexService()
        init_time = time.time() - start_time
        
        # Test connection
        if not es_service.es or not es_service.es.ping():
            logger.error("❌ Elasticsearch connection failed")
            return None
        
        # Create index
        start_time = time.time()
        index_created = es_service.create_index(force_recreate=True)
        index_time = time.time() - start_time
        
        if not index_created:
            logger.error("❌ Failed to create Elasticsearch index")
            return None
        
        # Index test data
        test_corpus = create_test_corpus()
        start_time = time.time()
        indexed = es_service.index_corpus_files(test_corpus)
        index_data_time = time.time() - start_time
        
        if not indexed:
            logger.error("❌ Failed to index data in Elasticsearch")
            return None
        
        # Test search performance
        search_queries = [
            "quick brown fox",
            "politics art possible",
            "science spirituality",
            "great work love"
        ]
        
        search_times = []
        search_results = []
        
        for query in search_queries:
            start_time = time.time()
            results = es_service.search_quotes(query, fuzziness="AUTO", size=5)
            search_time = time.time() - start_time
            search_times.append(search_time)
            search_results.append(results)
        
        # Test quote validation
        validation_queries = [
            "The quick brown fox jumps over the lazy dog",
            "Politics is the art of the possible",
            "Science is not only compatible with spirituality"
        ]
        
        validation_times = []
        validation_results = []
        
        for query in validation_queries:
            start_time = time.time()
            result = es_service.validate_quote(query)
            validation_time = time.time() - start_time
            validation_times.append(validation_time)
            validation_results.append(result)
        
        # Get stats
        stats = es_service.get_index_stats()
        
        return {
            "service": "Elasticsearch",
            "init_time": init_time,
            "index_creation_time": index_time,
            "data_indexing_time": index_data_time,
            "avg_search_time": sum(search_times) / len(search_times),
            "avg_validation_time": sum(validation_times) / len(validation_times),
            "search_results": search_results,
            "validation_results": validation_results,
            "stats": stats,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"❌ Elasticsearch benchmark failed: {e}")
        return {"service": "Elasticsearch", "success": False, "error": str(e)}


def benchmark_typesense():
    """Benchmark Typesense performance."""
    logger.info("🔍 Benchmarking Typesense...")
    
    try:
        # Initialize service
        start_time = time.time()
        ts_service = TypesenseCorpusService()
        init_time = time.time() - start_time
        
        # Test connection
        if not ts_service.client:
            logger.error("❌ Typesense connection failed")
            return None
        
        # Create index
        start_time = time.time()
        index_created = ts_service.create_index(force_recreate=True)
        index_time = time.time() - start_time
        
        if not index_created:
            logger.error("❌ Failed to create Typesense collection")
            return None
        
        # Index test data
        test_corpus = create_test_corpus()
        start_time = time.time()
        indexed = ts_service.index_corpus_files(test_corpus)
        index_data_time = time.time() - start_time
        
        if not indexed:
            logger.error("❌ Failed to index data in Typesense")
            return None
        
        # Test search performance
        search_queries = [
            "quick brown fox",
            "politics art possible",
            "science spirituality",
            "great work love"
        ]
        
        search_times = []
        search_results = []
        
        for query in search_queries:
            start_time = time.time()
            results = ts_service.search_quotes(query, fuzziness=2, size=5)
            search_time = time.time() - start_time
            search_times.append(search_time)
            search_results.append(results)
        
        # Test quote validation
        validation_queries = [
            "The quick brown fox jumps over the lazy dog",
            "Politics is the art of the possible",
            "Science is not only compatible with spirituality"
        ]
        
        validation_times = []
        validation_results = []
        
        for query in validation_queries:
            start_time = time.time()
            result = ts_service.validate_quote(query)
            validation_time = time.time() - start_time
            validation_times.append(validation_time)
            validation_results.append(result)
        
        # Get stats
        stats = ts_service.get_index_stats()
        
        return {
            "service": "Typesense",
            "init_time": init_time,
            "index_creation_time": index_time,
            "data_indexing_time": index_data_time,
            "avg_search_time": sum(search_times) / len(search_times),
            "avg_validation_time": sum(validation_times) / len(validation_times),
            "search_results": search_results,
            "validation_results": validation_results,
            "stats": stats,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"❌ Typesense benchmark failed: {e}")
        return {"service": "Typesense", "success": False, "error": str(e)}


def print_comparison(es_results, ts_results):
    """Print comparison results."""
    print("\n" + "="*80)
    print("🔍 SEARCH ENGINE COMPARISON RESULTS")
    print("="*80)
    
    if not es_results or not es_results.get("success"):
        print("❌ Elasticsearch benchmark failed")
        if es_results:
            print(f"   Error: {es_results.get('error', 'Unknown error')}")
    
    if not ts_results or not ts_results.get("success"):
        print("❌ Typesense benchmark failed")
        if ts_results:
            print(f"   Error: {ts_results.get('error', 'Unknown error')}")
    
    if not es_results or not es_results.get("success") or not ts_results or not ts_results.get("success"):
        return
    
    # Performance comparison
    print("\n📊 PERFORMANCE COMPARISON")
    print("-" * 40)
    
    metrics = [
        ("Initialization", "init_time"),
        ("Index Creation", "index_creation_time"),
        ("Data Indexing", "data_indexing_time"),
        ("Average Search", "avg_search_time"),
        ("Average Validation", "avg_validation_time")
    ]
    
    for metric_name, metric_key in metrics:
        es_value = es_results.get(metric_key, 0)
        ts_value = ts_results.get(metric_key, 0)
        
        if es_value and ts_value:
            faster = "Elasticsearch" if es_value < ts_value else "Typesense"
            improvement = abs(es_value - ts_value) / max(es_value, ts_value) * 100
            print(f"{metric_name:20} | ES: {es_value:.4f}s | TS: {ts_value:.4f}s | Faster: {faster} ({improvement:.1f}%)")
    
    # Stats comparison
    print("\n📈 STATISTICS COMPARISON")
    print("-" * 40)
    
    es_stats = es_results.get("stats", {})
    ts_stats = ts_results.get("stats", {})
    
    print(f"Document Count | ES: {es_stats.get('document_count', 'N/A')} | TS: {ts_stats.get('document_count', 'N/A')}")
    print(f"Status         | ES: {es_stats.get('status', 'N/A')} | TS: {ts_stats.get('status', 'N/A')}")
    
    # Search quality comparison
    print("\n🎯 SEARCH QUALITY COMPARISON")
    print("-" * 40)
    
    es_searches = es_results.get("search_results", [])
    ts_searches = ts_results.get("search_results", [])
    
    if es_searches and ts_searches:
        for i, (es_search, ts_search) in enumerate(zip(es_searches, ts_searches)):
            print(f"\nQuery {i+1}:")
            print(f"  ES Results: {len(es_search)} matches")
            print(f"  TS Results: {len(ts_search)} matches")
            
            if es_search and ts_search:
                es_score = es_search[0].get("score", 0) if es_search else 0
                ts_score = ts_search[0].get("score", 0) if ts_search else 0
                print(f"  Best Score: ES: {es_score} | TS: {ts_score}")


def main():
    """Run the benchmark comparison."""
    print("🚀 Starting Search Engine Comparison: Elasticsearch vs Typesense")
    print("=" * 80)
    
    # Run benchmarks
    es_results = benchmark_elasticsearch()
    ts_results = benchmark_typesense()
    
    # Print comparison
    print_comparison(es_results, ts_results)
    
    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)
    
    if es_results and es_results.get("success") and ts_results and ts_results.get("success"):
        print("✅ Both systems successfully completed benchmarks")
        print("📊 Check performance metrics above for detailed comparison")
    else:
        print("❌ Some benchmarks failed - check error messages above")
    
    print("\n🔧 Next Steps:")
    print("1. Review performance metrics")
    print("2. Test with real corpus data")
    print("3. Choose the better system for production use")


if __name__ == "__main__":
    main()
