#!/usr/bin/env python3
"""
Hybrid Corpus Service Benchmark

Tests the hybrid approach (Typesense + Python BM25) against:
1. Typesense alone
2. Hybrid approach (Typesense + BM25)

Measures both speed and accuracy to validate our hybrid approach.
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
import sys
import time
import json
from typing import List, Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'discernus'))

from core.typesense_corpus_service import TypesenseCorpusService
from core.hybrid_corpus_service import HybridCorpusService


def create_test_corpus():
    """Create a test corpus with various quote scenarios."""
    test_data = [
        {
            "file_path": "test_doc_1.txt",
            "content": "The quick brown fox jumps over the lazy dog. This is a famous pangram that contains every letter of the alphabet at least once.",
            "date": "2024-01-01T00:00:00"
        },
        {
            "file_path": "test_doc_2.txt", 
            "content": "To be or not to be, that is the question. Whether tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
            "date": "2024-01-02T00:00:00"
        },
        {
            "file_path": "test_doc_3.txt",
            "content": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances.",
            "date": "2024-01-03T00:00:00"
        },
        {
            "file_path": "test_doc_4.txt",
            "content": "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.",
            "date": "2024-01-04T00:00:00"
        },
        {
            "file_path": "test_doc_5.txt",
            "content": "Innovation distinguishes between a leader and a follower. The future belongs to those who believe in the beauty of their dreams.",
            "date": "2024-01-05T00:00:00"
        }
    ]
    
    # Create test corpus directory
    test_dir = "test_corpus_hybrid"
    os.makedirs(test_dir, exist_ok=True)
    
    for doc in test_data:
        file_path = os.path.join(test_dir, doc["file_path"])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
    
    return test_dir


def create_corpus_files_for_indexing(test_dir: str) -> List[Dict[str, Any]]:
    """Create corpus file data for indexing services."""
    corpus_files = []
    
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith(('.txt', '.md')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    corpus_files.append({
                        "file_path": file_path,
                        "filename": file,
                        "content": content,
                        "date": "2024-01-01T00:00:00",
                        "source_type": "corpus",
                        "start_char": 0,
                        "end_char": len(content),
                        "context": content[:100] + "..." if len(content) > 100 else content
                    })
                        
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
    
    return corpus_files


def test_typesense():
    """Test Typesense service."""
    print("🔍 Testing Typesense...")
    
    try:
        ts_service = TypesenseCorpusService(index_name="test_corpus_ts")
        test_dir = create_test_corpus()
        corpus_files = create_corpus_files_for_indexing(test_dir)
        
        # Create collection
        start_time = time.time()
        if not ts_service.create_index():
            print("❌ Failed to create Typesense collection")
            return None
        indexing_time = time.time() - start_time
        
        # Index corpus files
        index_start = time.time()
        if not ts_service.index_corpus_files(corpus_files):
            print("❌ Failed to index corpus files")
            return None
        index_time = time.time() - index_start
        
        # Test search
        search_start = time.time()
        results = ts_service.search_quotes("quick brown fox", size=5)
        search_time = time.time() - search_start
        
        # Test validation
        validation_start = time.time()
        validation = ts_service.validate_quote("quick brown fox")
        validation_time = time.time() - validation_start
        
        ts_service.close()
        
        return {
            'service': 'Typesense',
            'indexing_time_ms': round((indexing_time + index_time) * 1000, 2),
            'search_time_ms': round(search_time * 1000, 2),
            'validation_time_ms': round(validation_time * 1000, 2),
            'total_time_ms': round((indexing_time + index_time + search_time + validation_time) * 1000, 2),
            'results_count': len(results),
            'validation_result': validation
        }
        
    except Exception as e:
        print(f"❌ Typesense test failed: {e}")
        return None


def test_hybrid():
    """Test hybrid service."""
    print("🔍 Testing Hybrid (Typesense + BM25)...")
    
    try:
        hybrid_service = HybridCorpusService({})
        test_dir = create_test_corpus()
        corpus_files = create_corpus_files_for_indexing(test_dir)
        
        # Create collection and index
        start_time = time.time()
        if not hybrid_service.typesense_service.create_index():
            print("❌ Failed to create Typesense collection")
            return None
        
        if not hybrid_service.typesense_service.index_corpus_files(corpus_files):
            print("❌ Failed to index corpus files")
            return None
        
        # Build BM25 index
        hybrid_service._build_bm25_index(test_dir, "test_corpus_hybrid")
        indexing_time = time.time() - start_time
        
        # Test search
        search_start = time.time()
        results = hybrid_service.search_quotes("quick brown fox", "test_corpus_hybrid", limit=5)
        search_time = time.time() - search_start
        
        # Test validation
        validation_start = time.time()
        validation = hybrid_service.validate_quote("quick brown fox", "test_corpus_hybrid")
        validation_time = time.time() - validation_start
        
        hybrid_service.close()
        
        return {
            'service': 'Hybrid (Typesense + BM25)',
            'indexing_time_ms': round(indexing_time * 1000, 2),
            'search_time_ms': round(search_time * 1000, 2),
            'validation_time_ms': round(validation_time * 1000, 2),
            'total_time_ms': round((indexing_time + search_time + validation_time) * 1000, 2),
            'results_count': len(results),
            'validation_result': validation,
            'timing_breakdown': results[0].get('timing', {}) if results else {}
        }
        
    except Exception as e:
        print(f"❌ Hybrid test failed: {e}")
        return None


def run_accuracy_tests():
    """Run accuracy tests with various quote scenarios."""
    print("\n🎯 Running Accuracy Tests...")
    
    test_quotes = [
        # Exact matches
        "The quick brown fox jumps over the lazy dog",
        "To be or not to be, that is the question",
        
        # Minor variations
        "The quick brown fox jumps over the lazy dog.",
        "quick brown fox jumps over lazy dog",
        
        # Moderate variations
        "The quick brown fox jumps over the lazy dog. This is a famous pangram",
        "brown fox jumps over the lazy",
        
        # Significant variations
        "A quick brown fox jumps over a lazy dog",
        "The fox jumps over the dog",
        
        # Completely different
        "This is completely unrelated text",
        "Random words that don't match anything"
    ]
    
    # Test with hybrid service
    try:
        hybrid_service = HybridCorpusService({})
        test_dir = create_test_corpus()
        corpus_files = create_corpus_files_for_indexing(test_dir)
        
        # Setup hybrid service
        if not hybrid_service.typesense_service.create_index():
            print("❌ Failed to create Typesense collection for accuracy tests")
            return []
        
        if not hybrid_service.typesense_service.index_corpus_files(corpus_files):
            print("❌ Failed to index corpus files for accuracy tests")
            return []
        
        hybrid_service._build_bm25_index(test_dir, "test_corpus_accuracy")
        
        accuracy_results = []
        for quote in test_quotes:
            validation = hybrid_service.validate_quote(quote, "test_corpus_accuracy")
            accuracy_results.append({
                'quote': quote[:50] + "..." if len(quote) > 50 else quote,
                'drift_level': validation.get('drift_level', 'unknown'),
                'confidence': validation.get('confidence', 0),
                'valid': validation.get('valid', False)
            })
        
        hybrid_service.close()
        return accuracy_results
        
    except Exception as e:
        print(f"❌ Accuracy test failed: {e}")
        return []


def print_benchmark_results(results: List[Dict[str, Any]]):
    """Print benchmark results in a formatted table."""
    print("\n" + "="*80)
    print("🏆 BENCHMARK RESULTS")
    print("="*80)
    
    if not results:
        print("❌ No results to display")
        return
    
    # Print performance comparison
    print("\n📊 PERFORMANCE COMPARISON")
    print("-" * 80)
    print(f"{'Service':<25} {'Indexing':<10} {'Search':<10} {'Validation':<12} {'Total':<10}")
    print("-" * 80)
    
    for result in results:
        if result:
            print(f"{result['service']:<25} {result['indexing_time_ms']:<10} "
                  f"{result['search_time_ms']:<10} {result['validation_time_ms']:<12} "
                  f"{result['total_time_ms']:<10}")
    
    # Find fastest service
    valid_results = [r for r in results if r]
    if valid_results:
        fastest = min(valid_results, key=lambda x: x['total_time_ms'])
        print(f"\n⚡ FASTEST: {fastest['service']} ({fastest['total_time_ms']}ms)")
        
        # Calculate speedup vs others
        for result in valid_results:
            if result != fastest:
                speedup = result['total_time_ms'] / fastest['total_time_ms']
                print(f"   {result['service']}: {speedup:.1f}x slower")


def print_accuracy_results(accuracy_results: List[Dict[str, Any]]):
    """Print accuracy test results."""
    print("\n🎯 ACCURACY TEST RESULTS")
    print("-" * 80)
    
    if not accuracy_results:
        print("❌ No accuracy results to display")
        return
    
    # Count drift levels
    drift_counts = {}
    for result in accuracy_results:
        drift = result['drift_level']
        drift_counts[drift] = drift_counts.get(drift, 0) + 1
    
    print("Drift Level Distribution:")
    for drift, count in drift_counts.items():
        print(f"  {drift}: {count}")
    
    # Show sample results
    print("\nSample Validations:")
    for i, result in enumerate(accuracy_results[:5]):
        print(f"  {i+1}. '{result['quote']}' -> {result['drift_level']} "
              f"(confidence: {result['confidence']:.2f})")


def main():
    """Run the complete benchmark."""
    print("🚀 HYBRID CORPUS SERVICE BENCHMARK")
    print("Testing Typesense + Python BM25 vs Typesense alone")
    print("="*80)
    
    # Check if services are running
    print("🔍 Checking service availability...")
    
    # Run benchmarks
    results = []
    
    # Test Typesense
    ts_result = test_typesense()
    if ts_result:
        results.append(ts_result)
    
    # Test Hybrid
    hybrid_result = test_hybrid()
    if hybrid_result:
        results.append(hybrid_result)
    
    # Run accuracy tests
    accuracy_results = run_accuracy_tests()
    
    # Display results
    print_benchmark_results(results)
    print_accuracy_results(accuracy_results)
    
    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)
    
    if results:
        print(f"✅ Successfully tested {len(results)} services")
        
        # Performance analysis
        valid_results = [r for r in results if r]
        if len(valid_results) > 1:
            fastest = min(valid_results, key=lambda x: x['total_time_ms'])
            slowest = max(valid_results, key=lambda x: x['total_time_ms'])
            
            print(f"\n🏆 Performance Champion: {fastest['service']}")
            print(f"🐌 Slowest: {slowest['service']}")
            
            if fastest['service'] == 'Hybrid (Typesense + BM25)':
                print("🎉 Hybrid approach wins on performance!")
            else:
                print("⚡ Typesense wins on raw speed!")
    
    print("\n🎯 Next Steps:")
    print("1. Analyze the results to see if hybrid beats Typesense alone")
    print("2. If successful, integrate hybrid service into the orchestrator")
    print("3. Run full experiment to validate end-to-end performance")


if __name__ == "__main__":
    main()
