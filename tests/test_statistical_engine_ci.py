#!/usr/bin/env python3
"""
Statistical Engine CI Test
==========================

CI-friendly test of the statistical comparison engine using mocked LLM responses.
This test exercises the complete statistical infrastructure without requiring:
- Running LLM services
- API keys
- Network connectivity
- Long execution times

Tests the same functionality as test_statistical_engine.py but with deterministic,
fast execution suitable for continuous integration.
"""

import pytest
import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import patch
from typing import Dict, Any

# Add the parent directory to the path so we can import from discernus
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_llm_responses():
    """Fixture providing realistic but deterministic LLM responses for testing."""
    return {
        "ollama/llama3.2": {
            "scores": {"Fairness": 0.75, "Liberty": 0.60},
            "raw_response": "Based on analysis: {\"Fairness\": {\"score\": 0.75, \"evidence\": \"justice and fairness\", \"reasoning\": \"Strong fairness language\"}, \"Liberty\": {\"score\": 0.60, \"evidence\": \"individual liberty\", \"reasoning\": \"Moderate liberty themes\"}}",
            "parsed": True,
            "parsing_method": "robust_parser"
        },
        "claude-3-5-haiku-20241022": {
            "scores": {"Fairness": 0.82, "Liberty": 0.68},
            "raw_response": "{\"Fairness\": {\"score\": 0.82, \"evidence\": \"equal opportunities\", \"reasoning\": \"Clear fairness emphasis\"}, \"Liberty\": {\"score\": 0.68, \"evidence\": \"protect individual liberty\", \"reasoning\": \"Notable liberty focus\"}}",
            "parsed": True,
            "parsing_method": "robust_parser"
        }
    }


@pytest.fixture
def test_experiment_config():
    """Fixture providing the test experiment configuration."""
    return {
        "experiment_meta": {
            "name": "Test_Statistical_CI",
            "version": "1.0"
        },
        "corpus": {
            "source_type": "single_text",
            "default_text": "Justice and fairness are the foundation of a good society. We must protect individual liberty while ensuring everyone has equal opportunities to succeed."
        },
        "framework": {
            "name": "test_moral_framework_ci",
            "axes": {
                "Fairness_Unfairness": {
                    "integrative": {"name": "Fairness", "angle": 0},
                    "disintegrative": {"name": "Unfairness", "angle": 180}
                },
                "Liberty_Control": {
                    "integrative": {"name": "Liberty", "angle": 90},
                    "disintegrative": {"name": "Control", "angle": 270}
                }
            }
        },
        "models": {
            "supported_providers": ["ollama", "anthropic"],
            "comparison_models": {
                "local": "ollama/llama3.2",
                "cloud": "claude-3-5-haiku-20241022"
            }
        },
        "output": {
            "generate_visualization": False,
            "save_to_database": False
        }
    }


@pytest.mark.asyncio
async def test_statistical_engine_mocked(mock_llm_responses, test_experiment_config):
    """Test the complete statistical engine with mocked LLM responses."""
    # Import only the core functions we need, avoiding FastAPI app initialization
    from discernus.gateway.llm_gateway import get_llm_analysis
    from discernus.engine.signature_engine import calculate_coordinates
    from discernus.analysis.statistical_methods import StatisticalMethodRegistry
    
    # Create a side effect function that returns different responses based on model
    def mock_llm_gateway(text: str, experiment_def: Dict[str, Any], model: str) -> Dict[str, Any]:
        return mock_llm_responses[model]
    
    # Mock the LLM client directly to avoid real API calls
    with patch('discernus.gateway.reboot_litellm_client.LiteLLMClient.analyze_text') as mock_analyze:
        # Configure mock to return different responses based on model
        def get_mock_response(text, experiment_def, model_name):
            response = mock_llm_responses[model_name]
            return response, 0.0  # (result, cost)
        
        mock_analyze.side_effect = get_mock_response
        
        # Test individual model analysis
        models_to_test = ["ollama/llama3.2", "claude-3-5-haiku-20241022"]
        test_text = test_experiment_config["corpus"]["default_text"]
        
        results = []
        for model in models_to_test:
            # Simulate the _run_single_analysis function without importing FastAPI app
            llm_result = await get_llm_analysis(text=test_text, experiment_def=test_experiment_config, model=model)
            scores = llm_result.get("scores", {})
            x, y = calculate_coordinates(test_experiment_config, scores)
            result = {"scores": scores, "centroid": (x, y)}
            
            # Validate result structure
            assert "scores" in result
            assert "centroid" in result
            assert len(result["centroid"]) == 2
            assert isinstance(result["scores"], dict)
            
            # Validate coordinate ranges
            x, y = result["centroid"]
            assert -2 <= x <= 2, f"X coordinate {x} seems unreasonable"
            assert -2 <= y <= 2, f"Y coordinate {y} seems unreasonable"
            
            # Validate scores
            assert "Fairness" in result["scores"]
            assert "Liberty" in result["scores"]
            assert 0.0 <= result["scores"]["Fairness"] <= 1.0
            assert 0.0 <= result["scores"]["Liberty"] <= 1.0
            
            results.append({
                "model": model,
                "centroid": result["centroid"],
                "scores": result["scores"]
            })
        
        # Test core statistical analysis methods that don't require API dependencies
        # Only test the basic methods that are self-contained
        registry = StatisticalMethodRegistry()
        
        # Create mock database results for statistical analysis
        from discernus.database.models import AnalysisResultV2
        
        mock_db_results = []
        for i, result in enumerate(results):
            mock_result = AnalysisResultV2()
            mock_result.id = i + 1
            mock_result.model = result["model"]
            mock_result.centroid_x = result["centroid"][0]
            mock_result.centroid_y = result["centroid"][1]
            mock_result.raw_scores = json.dumps(result["scores"])
            mock_result.text_identifier = "test_text"
            mock_db_results.append(mock_result)
        
        # Test only the basic statistical methods (avoid API-dependent ones for CI)
        basic_methods = [
            "geometric_similarity",
            "dimensional_correlation"
        ]
        
        statistical_results = {}
        for method in basic_methods:
            try:
                result = registry.analyze(method, mock_db_results)
                statistical_results[method] = result
                
                # Validate that each method returns a dictionary
                assert isinstance(result, dict), f"{method} should return a dictionary"
                
                # Method-specific validations
                if method == "geometric_similarity":
                    assert "distances" in result
                    assert "mean_distance" in result
                    assert isinstance(result["distances"], list)
                    assert isinstance(result["mean_distance"], (int, float))
                
                elif method == "dimensional_correlation":
                    assert "correlation_matrix" in result
                    assert "dimensions" in result
                    assert isinstance(result["correlation_matrix"], list)
                    assert isinstance(result["dimensions"], list)
                
            except Exception as e:
                pytest.fail(f"Statistical method {method} failed: {e}")
        
        # Validate that we got results for the basic methods
        assert len(statistical_results) == len(basic_methods)
        
        # Test that the statistical registry can load advanced methods (without executing them)
        advanced_methods = ["hypothesis_testing", "effect_size_analysis", "confidence_intervals"]
        for method in advanced_methods:
            try:
                analyzer = registry.get_analyzer(method)
                assert analyzer is not None, f"Method {method} should be registered"
            except ValueError:
                pytest.fail(f"Advanced method {method} should be registered in registry")
        
        # Test that results are deterministic (same inputs = same outputs)
        # Run the same analysis again and verify consistency
        results_2 = []
        for model in models_to_test:
            llm_result_2 = await get_llm_analysis(text=test_text, experiment_def=test_experiment_config, model=model)
            scores_2 = llm_result_2.get("scores", {})
            x2, y2 = calculate_coordinates(test_experiment_config, scores_2)
            result_2 = {"scores": scores_2, "centroid": (x2, y2)}
            results_2.append(result_2)
        
        # Verify deterministic behavior
        for i, (result1, result2) in enumerate(zip(results, results_2)):
            assert result1["scores"] == result2["scores"], f"Scores should be deterministic for model {i}"
            assert result1["centroid"] == result2["centroid"], f"Coordinates should be deterministic for model {i}"


def test_statistical_method_registry():
    """Test that all expected statistical methods are registered."""
    from discernus.analysis.statistical_methods import StatisticalMethodRegistry
    
    registry = StatisticalMethodRegistry()
    
    expected_methods = [
        "geometric_similarity",
        "dimensional_correlation", 
        "hypothesis_testing",
        "effect_size_analysis",
        "confidence_intervals"
    ]
    
    for method in expected_methods:
        try:
            analyzer = registry.get_analyzer(method)
            assert analyzer is not None, f"Method {method} should return an analyzer"
        except ValueError:
            pytest.fail(f"Method {method} should be registered but was not found")


def test_experiment_config_loading():
    """Test that experiment configuration loading works properly."""
    import yaml
    import os
    
    # Test loading the actual test experiment file (handle both test dir and root dir execution)
    experiment_file = "multi_model_statistical_test.yaml"
    if not os.path.exists(experiment_file):
        experiment_file = "tests/multi_model_statistical_test.yaml"
    
    try:
        with open(experiment_file, "r") as f:
            experiment_def = yaml.safe_load(f)
        
        # Validate required sections
        assert "experiment_meta" in experiment_def
        assert "corpus" in experiment_def
        assert "framework" in experiment_def
        assert "models" in experiment_def
        assert "output" in experiment_def
        
        # Validate statistical analysis configuration
        assert "statistical_analysis" in experiment_def
        assert experiment_def["statistical_analysis"]["enabled"] is True
        
        primary_methods = experiment_def["statistical_analysis"]["primary_methods"]
        assert "geometric_similarity" in primary_methods
        assert "dimensional_correlation" in primary_methods
        assert "hypothesis_testing" in primary_methods
        
    except FileNotFoundError:
        pytest.fail(f"Test experiment file {experiment_file} not found")
    except Exception as e:
        pytest.fail(f"Failed to load experiment configuration: {e}")


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"]) 