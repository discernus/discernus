#!/usr/bin/env python3
"""
Pipeline Model Testing
=====================

Tests the complete analysis pipeline with both local (Ollama) and cloud models.
Uses the test_pipeline experiment which is configured to:
- Skip database persistence (save_to_database: false)
- Skip visualization generation (generate_visualization: false)
- Use simplified framework for faster testing

This test verifies:
1. Local Ollama models work (ollama/llama3.2)
2. Cheap cloud models work (claude-3-5-haiku-20241022)
3. Both produce valid coordinate outputs
4. No database pollution occurs
5. Pipeline handles errors gracefully
"""

import asyncio
import json
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to the path so we can import from discernus
sys.path.insert(0, str(Path(__file__).parent.parent))

from discernus.api.main import _run_single_analysis
from discernus.analysis.statistical_methods import StatisticalMethodRegistry


async def test_model(model_name: str, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single model with the test experiment."""
    print(f"🧪 Testing {model_name}...")
    start_time = time.time()
    
    try:
        # Get test text from experiment
        test_text = experiment_def["corpus"]["default_text"]
        
        # Run the analysis
        result = await _run_single_analysis(test_text, model_name, experiment_def)
        
        duration = time.time() - start_time
        
        # Validate the result structure
        assert "scores" in result, "Missing 'scores' in result"
        assert "centroid" in result, "Missing 'centroid' in result"
        assert len(result["centroid"]) == 2, "Centroid should have x,y coordinates"
        assert isinstance(result["scores"], dict), "Scores should be a dictionary"
        
        # Validate coordinates are reasonable (between -1 and 1 typically)
        x, y = result["centroid"]
        assert -2 <= x <= 2, f"X coordinate {x} seems unreasonable"
        assert -2 <= y <= 2, f"Y coordinate {y} seems unreasonable"
        
        print(f"✅ {model_name}: SUCCESS")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Coordinates: ({x:.3f}, {y:.3f})")
        print(f"   Scores: {list(result['scores'].keys())}")
        
        return {
            "model": model_name,
            "status": "success",
            "duration": duration,
            "coordinates": result["centroid"],
            "scores": result["scores"]
        }
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ {model_name}: FAILED - {str(e)}")
        print(f"   Duration: {duration:.2f}s")
        
        return {
            "model": model_name,
            "status": "failed",
            "duration": duration,
            "error": str(e)
        }


async def main():
    """Run the complete pipeline test."""
    print("🚀 Starting Pipeline Model Tests")
    print("=" * 50)
    
    try:
        # Load the test experiment from tests folder
        print("📋 Loading test_pipeline experiment...")
        experiment_file = "tests/test_pipeline.yaml"
        with open(experiment_file, "r") as f:
            experiment_def = yaml.safe_load(f)
        
        # Verify test experiment configuration
        output_config = experiment_def.get("output", {})
        assert output_config.get("save_to_database", True) == False, "Test experiment should have save_to_database: false"
        assert output_config.get("generate_visualization", True) == False, "Test experiment should have generate_visualization: false"
        
        print("✅ Test experiment loaded and configured properly")
        print(f"   Framework: {experiment_def['framework']['name']}")
        print(f"   Default model: {experiment_def['models']['default_model']}")
        print(f"   DB persistence: {output_config.get('save_to_database', True)}")
        print(f"   Visualization: {output_config.get('generate_visualization', True)}")
        print("")
        
        # Test models
        models_to_test = [
            "ollama/llama3.2",  # Local model
            "claude-3-5-haiku-20241022"  # Cheap cloud model
        ]
        
        print(f"🎯 Testing {len(models_to_test)} models...")
        print("")
        
        # Run tests for each model
        results = []
        for model in models_to_test:
            result = await test_model(model, experiment_def)
            results.append(result)
            print("")  # Empty line between tests
        
        # Summary
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        successful_tests = [r for r in results if r["status"] == "success"]
        failed_tests = [r for r in results if r["status"] == "failed"]
        
        print(f"✅ Successful: {len(successful_tests)}/{len(results)}")
        print(f"❌ Failed: {len(failed_tests)}/{len(results)}")
        print("")
        
        if successful_tests:
            print("🎉 SUCCESSFUL TESTS:")
            for result in successful_tests:
                x, y = result["coordinates"]
                print(f"   {result['model']}: ({x:.3f}, {y:.3f}) in {result['duration']:.2f}s")
            print("")
        
        if failed_tests:
            print("💥 FAILED TESTS:")
            for result in failed_tests:
                print(f"   {result['model']}: {result['error']}")
            print("")
        
        # Statistical comparison if we have multiple successful results
        if len(successful_tests) >= 2:
            print("📊 STATISTICAL COMPARISON TEST")
            print("=" * 50)
            
            # Group results by model for statistical analysis
            model_groups = {}
            for result in successful_tests:
                model = result["model"]
                model_groups[model] = [{
                    "centroid": result["coordinates"],
                    "scores": result["scores"]
                }]
            
            # Test statistical methods
            try:
                print("🧮 Testing geometric similarity...")
                similarity_result = _calculate_geometric_similarity(model_groups)
                print(f"   Geometric distance: {similarity_result.get('average_distance', 'N/A'):.4f}")
                print(f"   Similarity level: {similarity_result.get('similarity_level', 'unknown')}")
                
                print("🧮 Testing dimensional correlation...")
                correlation_result = _calculate_dimensional_correlation(model_groups)
                print(f"   Score correlation: {correlation_result.get('score_correlation', 'N/A'):.4f}")
                print(f"   Coordinate correlation: {correlation_result.get('coordinate_correlation', 'N/A'):.4f}")
                
                print("✅ Statistical engine test: SUCCESS")
                print("")
                
            except Exception as e:
                print(f"❌ Statistical engine test: FAILED - {e}")
                print("")
        
        # Overall status
        if len(successful_tests) == len(results):
            print("🎊 ALL TESTS PASSED! Pipeline is working with both local and cloud models.")
            return 0
        elif len(successful_tests) > 0:
            print("⚠️  PARTIAL SUCCESS: Some models working, others failed.")
            return 1
        else:
            print("💀 ALL TESTS FAILED: Pipeline has serious issues.")
            return 2
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        return 3


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