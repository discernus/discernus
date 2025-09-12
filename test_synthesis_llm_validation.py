#!/usr/bin/env python3
"""
Prompt testing harness to validate whether synthesis LLM can handle data issues better than brittle validation.
"""

import json
import tempfile
from pathlib import Path
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

def test_synthesis_llm_with_various_data_scenarios():
    """Test synthesis LLM with different data quality scenarios."""
    
    # Initialize LLM gateway
    model_registry = ModelRegistry()
    llm_gateway = LLMGateway(model_registry)
    
    # Test scenarios
    scenarios = [
        {
            "name": "Complete Valid Data",
            "data": {
                "raw_analysis_results": [
                    {
                        "document_name": "test_doc.txt",
                        "dimensional_scores": {
                            "positive_sentiment": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95},
                            "negative_sentiment": {"raw_score": 0.2, "salience": 0.1, "confidence": 0.95}
                        }
                    }
                ],
                "derived_metrics_results": {
                    "derived_metrics": [
                        {"net_sentiment": 0.6, "sentiment_intensity": 0.7}
                    ]
                },
                "statistical_results": {
                    "descriptive_stats": {"mean": 0.6, "std": 0.1},
                    "correlations": {"positive_negative": -0.8}
                }
            }
        },
        {
            "name": "Missing Derived Metrics",
            "data": {
                "raw_analysis_results": [
                    {
                        "document_name": "test_doc.txt",
                        "dimensional_scores": {
                            "positive_sentiment": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95},
                            "negative_sentiment": {"raw_score": 0.2, "salience": 0.1, "confidence": 0.95}
                        }
                    }
                ],
                "derived_metrics_results": None,
                "statistical_results": {
                    "descriptive_stats": {"mean": 0.6, "std": 0.1}
                }
            }
        },
        {
            "name": "Empty Derived Metrics",
            "data": {
                "raw_analysis_results": [
                    {
                        "document_name": "test_doc.txt",
                        "dimensional_scores": {
                            "positive_sentiment": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95}
                        }
                    }
                ],
                "derived_metrics_results": {
                    "derived_metrics": []
                },
                "statistical_results": {
                    "descriptive_stats": {"mean": 0.8, "std": 0.0}
                }
            }
        },
        {
            "name": "Malformed Data Structure",
            "data": {
                "raw_analysis_results": "invalid_string_instead_of_array",
                "derived_metrics_results": {
                    "wrong_key": "should_be_derived_metrics"
                },
                "statistical_results": None
            }
        },
        {
            "name": "Partial Data - Only Analysis",
            "data": {
                "raw_analysis_results": [
                    {
                        "document_name": "test_doc.txt",
                        "dimensional_scores": {
                            "positive_sentiment": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95}
                        }
                    }
                ]
                # Missing derived_metrics_results and statistical_results
            }
        }
    ]
    
    # Test each scenario
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"🧪 Testing Scenario: {scenario['name']}")
        print(f"{'='*60}")
        
        # Create synthesis prompt
        prompt = f"""
You are a research synthesis agent. You need to generate a research report based on the provided data.

IMPORTANT: The data may be incomplete, malformed, or missing some components. Your job is to:
1. Identify what data is available and what is missing
2. Work with what you have
3. Clearly note any limitations or missing information
4. Generate the best possible report given the available data

Data provided:
{json.dumps(scenario['data'], indent=2)}

Please analyze this data and provide:
1. A brief assessment of data quality and completeness
2. What components are available vs missing
3. A short research report based on available data
4. Any limitations or recommendations for improvement

Be specific about what you can and cannot do with the available data.
"""
        
        try:
            print(f"📤 Sending prompt to LLM...")
            response, metadata = llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-pro",
                prompt=prompt,
                temperature=0.1
            )
            
            print(f"✅ LLM Response received ({len(response)} chars)")
            print(f"📊 Response preview: {response[:300]}...")
            
            # Check if response indicates good handling
            if "missing" in response.lower() or "incomplete" in response.lower():
                print("🎯 LLM correctly identified missing/incomplete data")
            if "limitation" in response.lower() or "cannot" in response.lower():
                print("🎯 LLM appropriately noted limitations")
            if "available" in response.lower() or "based on" in response.lower():
                print("🎯 LLM worked with available data")
                
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
    
    print(f"\n{'='*60}")
    print("🏁 Testing complete!")
    print(f"{'='*60}")

def test_current_validation_approach():
    """Test our current brittle validation approach with the same scenarios."""
    
    print(f"\n{'='*60}")
    print("🔧 Testing Current Brittle Validation Approach")
    print(f"{'='*60}")
    
    # Simulate the current validation logic
    def validate_derived_metrics(derived_metrics_results):
        """Simulate current validation logic."""
        if not derived_metrics_results:
            return False, "No derived metrics results available"
        
        if not isinstance(derived_metrics_results, dict):
            return False, "Derived metrics results not a dictionary"
        
        # Check nested structure (this is where it breaks)
        nested_results = derived_metrics_results.get('derived_metrics_results', {})
        metrics_data = nested_results.get('derived_metrics_data', {})
        derived_metrics_list = metrics_data.get('derived_metrics', [])
        
        if not metrics_data or not derived_metrics_list:
            return False, "Derived metrics contain no actual metrics data"
        
        return True, "Validation passed"
    
    # Test scenarios
    test_cases = [
        ({"derived_metrics_results": {"derived_metrics_data": {"derived_metrics": [{"test": 1}]}}}, "Valid nested structure"),
        ({"derived_metrics_results": {"derived_metrics_data": {"derived_metrics": []}}}, "Empty derived metrics"),
        ({"derived_metrics_results": {"derived_metrics_data": {}}}, "Missing derived_metrics key"),
        ({"derived_metrics_results": {}}, "Missing derived_metrics_data key"),
        ({"wrong_key": "value"}, "Wrong structure entirely"),
        (None, "None data"),
        ("invalid_string", "Invalid type")
    ]
    
    for data, description in test_cases:
        print(f"\n🧪 Testing: {description}")
        print(f"   Data: {data}")
        
        try:
            success, message = validate_derived_metrics(data)
            if success:
                print(f"   ✅ {message}")
            else:
                print(f"   ❌ {message}")
        except Exception as e:
            print(f"   💥 Exception: {e}")

if __name__ == "__main__":
    print("🚀 Starting Synthesis LLM vs Brittle Validation Comparison")
    
    # Test current validation approach
    test_current_validation_approach()
    
    # Test LLM approach
    test_synthesis_llm_with_various_data_scenarios()
    
    print("\n🎯 Conclusion: Compare the results above to see which approach handles data issues more gracefully.")
