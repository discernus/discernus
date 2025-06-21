#!/usr/bin/env python3
"""
Analyze Full Response Corpus

This script demonstrates how to access and analyze the complete database
of LLM responses, including raw text, prompts, and all metadata.
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.statistical_logger import logger

def analyze_corpus():
    """Analyze the full response corpus"""
    
    print("🔍 RESPONSE CORPUS ANALYSIS")
    print("=" * 50)
    
    # Get corpus statistics
    stats = logger.get_corpus_stats()
    
    print(f"📊 CORPUS OVERVIEW:")
    print(f"   Total Runs: {stats['total_runs']}")
    print(f"   Total Jobs: {stats['total_jobs']}")
    print(f"   Unique Models: {stats['unique_models']}")
    print(f"   Total Cost: ${stats['total_cost']:.4f}")
    print()
    
    print("🤖 MODEL DISTRIBUTION:")
    for model in stats['model_distribution']:
        print(f"   {model['model']}: {model['count']} runs")
    print()
    
    print("🎤 SPEAKER DISTRIBUTION:")
    for speaker in stats['speaker_distribution']:
        print(f"   {speaker['speaker']}: {speaker['count']} runs")
    print()
    
    # Get full corpus (limited for demo)
    print("📄 SAMPLE CORPUS ENTRIES:")
    corpus = logger.get_full_response_corpus(filters={'model_name': 'claude-3-5-sonnet-20241022'})
    
    for i, entry in enumerate(corpus[:2]):  # Show first 2 entries
        print(f"\n--- RUN {i+1}: {entry['run_id']} ---")
        print(f"Speaker: {entry['speaker']}")
        print(f"Model: {entry['model_name']}")
        print(f"Cost: ${entry['cost']:.4f}")
        print(f"Duration: {entry['duration_seconds']:.1f}s")
        print(f"Input Length: {len(entry['input_text'])} chars")
        print(f"Raw Response Length: {len(entry['raw_response'])} chars")
        print(f"Analysis: {entry['analysis_text'][:200]}...")
        print(f"Scores: {json.dumps(entry['well_scores'], indent=2)}")
    
    print("\n" + "=" * 50)
    print("✅ Corpus analysis complete!")

def demo_filtered_queries():
    """Demonstrate filtered corpus queries"""
    
    print("\n🔍 FILTERED CORPUS QUERIES")
    print("=" * 50)
    
    # Query by model
    claude_runs = logger.get_full_response_corpus(filters={
        'model_name': 'claude-3-5-sonnet-20241022'
    })
    print(f"Claude runs: {len(claude_runs)}")
    
    # Query by speaker
    trump_runs = logger.get_full_response_corpus(filters={
        'speaker': 'Trump'
    })
    print(f"Trump analyses: {len(trump_runs)}")
    
    # Query high-cost runs
    expensive_runs = logger.get_full_response_corpus(filters={
        'min_cost': 0.01
    })
    print(f"Expensive runs (>$0.01): {len(expensive_runs)}")

if __name__ == "__main__":
    analyze_corpus()
    demo_filtered_queries() 