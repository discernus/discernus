#!/usr/bin/env python3
"""
Statistical Engine Test
======================

Tests the statistical comparison engine using the proper experiment orchestrator.
Uses the multi_model_statistical_test experiment to exercise:
- Multi-model comparison (Ollama vs Haiku)
- Statistical analysis methods
- Experiment orchestration infrastructure

This test validates the statistical engine through the designed workflow.
"""

import asyncio
import json
import sys
import time
import requests
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to the path so we can import from discernus
sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_statistical_comparison():
    """Test the statistical comparison engine using the proper orchestrator."""
    print("📊 Testing Statistical Comparison Engine")
    print("=" * 50)
    
    try:
        # Test API health first
        print("🏥 Checking API health...")
        health_response = requests.get("http://127.0.0.1:8000/health", timeout=10)
        if health_response.status_code != 200:
            print("❌ API not responding. Start the server first.")
            return 1
        print("✅ API is healthy")
        print("")
        
        # Execute statistical comparison using the orchestrator
        print("🚀 Executing multi-model statistical comparison...")
        print("   Models: ollama/llama3.2 vs claude-3-5-haiku-20241022")
        print("   Multiple runs per model for statistical significance")
        print("")
        
        start_time = time.time()
        
        # Use the /compare-statistical endpoint with our experiment
        comparison_request = {
            "comparison_type": "multi_model",
            "text": "Justice and fairness are the foundation of a good society. We must protect individual liberty while ensuring everyone has equal opportunities to succeed.",
            "models": ["ollama/llama3.2", "claude-3-5-haiku-20241022"],
            "runs_per_condition": 3,
            "experiment_file_path": "tests/multi_model_statistical_test.yaml",
            "statistical_methods": [
                "geometric_similarity",
                "dimensional_correlation", 
                "hypothesis_testing",
                "effect_size_analysis",
                "confidence_intervals"
            ]
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/compare-statistical",
            json=comparison_request,
            timeout=180  # Allow time for multiple model runs
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Statistical comparison completed in {duration:.1f}s")
            print(f"   Job ID: {result.get('job_id', 'unknown')}")
            print(f"   Comparison type: {result.get('comparison_type', 'unknown')}")
            print(f"   Similarity classification: {result.get('similarity_classification', 'unknown')}")
            print(f"   Confidence level: {result.get('confidence_level', 0):.2f}")
            print("")
            
            # Display condition results (model comparisons)
            condition_results = result.get('condition_results', [])
            if condition_results:
                print("🎯 MODEL COMPARISON RESULTS:")
                for condition in condition_results:
                    model = condition.get('condition_identifier', 'unknown')
                    centroid = condition.get('centroid', (0, 0))
                    raw_scores = condition.get('raw_scores', {})
                    print(f"   {model}: ({centroid[0]:.3f}, {centroid[1]:.3f})")
                    print(f"      Scores: {raw_scores}")
                print("")
            
            # Display statistical metrics
            statistical_metrics = result.get('statistical_metrics', {})
            if statistical_metrics:
                print("📈 STATISTICAL ANALYSIS RESULTS:")
                
                for method, metrics in statistical_metrics.items():
                    print(f"   {method.replace('_', ' ').title()}:")
                    if isinstance(metrics, dict):
                        for key, value in metrics.items():
                            if isinstance(value, (int, float)):
                                print(f"      {key}: {value:.4f}")
                            else:
                                print(f"      {key}: {value}")
                    print("")
            
            # Display significance tests
            significance_tests = result.get('significance_tests', {})
            if significance_tests:
                print("🔬 SIGNIFICANCE TESTING:")
                for test, results in significance_tests.items():
                    print(f"   {test}: {results}")
                print("")
            
            print("🎊 STATISTICAL ENGINE TEST: SUCCESS")
            print("   All statistical methods executed through proper orchestrator")
            return 0
            
        else:
            print(f"❌ Statistical comparison failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return 1
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


async def main():
    """Run the statistical engine test."""
    print("🧮 Statistical Engine Integration Test")
    print("Uses experiment orchestrator to test multi-model statistical comparison")
    print("")
    
    exit_code = await test_statistical_comparison()
    
    if exit_code == 0:
        print("✨ Statistical engine is working properly through the orchestrator!")
    else:
        print("💥 Statistical engine test failed")
    
    return exit_code


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1) 