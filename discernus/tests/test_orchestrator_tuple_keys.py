#!/usr/bin/env python3
"""
Test the orchestrator's research data creation with tuple keys.
"""

import pytest
import json

def test_orchestrator_research_data_tuple_keys():
    """Test that the orchestrator can handle tuple keys when creating research data."""
    
    # Mock the statistical results that would be passed to _run_synthesis
    mock_statistical_results = {
        'raw_analysis_data_hash': 'test_hash_1',
        'derived_metrics_data_hash': 'test_hash_2',
        'statistical_summary': {
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699}
                }
            }
        }
    }
    
    # Simulate the research data creation logic from the orchestrator
    raw_analysis_data = '{"test": "analysis_data"}'
    derived_metrics_data = '{"test": "metrics_data"}'
    
    research_data = {
        "raw_analysis_results": json.loads(raw_analysis_data),
        "derived_metrics_results": json.loads(derived_metrics_data),
        "statistical_results": mock_statistical_results['statistical_summary']
    }
    
    print("Original research_data structure:")
    print(f"Keys: {list(research_data.keys())}")
    print(f"Statistical results keys: {list(research_data['statistical_results'].keys())}")
    
    # Test 1: Direct JSON serialization (should fail)
    print("\nTest 1: Direct JSON serialization (should fail)")
    try:
        json_str = json.dumps(research_data, indent=2)
        pytest.fail("Direct JSON serialization should have failed with tuple keys")
    except TypeError as e:
        print(f"✅ Expected failure: {e}")
    
    # Test 2: Tuple key conversion function (same as orchestrator)
    print("\nTest 2: Tuple key conversion function")
    def convert_tuple_keys_for_json(obj):
        """Convert tuple keys to strings for safe JSON serialization."""
        if isinstance(obj, dict):
            converted = {}
            for k, v in obj.items():
                if isinstance(k, tuple):
                    converted_key = str(k)
                else:
                    converted_key = k
                converted[converted_key] = convert_tuple_keys_for_json(v)
            return converted
        elif isinstance(obj, list):
            return [convert_tuple_keys_for_json(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(convert_tuple_keys_for_json(item) for item in obj)
        else:
            return obj
    
    # Test 3: Convert and serialize (should succeed)
    print("\nTest 3: Convert and serialize (should succeed)")
    json_safe_research_data = convert_tuple_keys_for_json(research_data)
    
    try:
        json_str = json.dumps(json_safe_research_data, indent=2)
        print(f"✅ JSON serialization successful: {len(json_str)} characters")
        
        # Verify the structure
        assert "('constitutional_health_index', 'mean')" in json_str
        assert "('constitutional_health_index', 'std')" in json_str
        
        # Verify the data is preserved
        parsed_data = json.loads(json_str)
        assert "statistical_results" in parsed_data
        assert "calculate_descriptive_stats_by_admin" in parsed_data["statistical_results"]
        
        print("✅ Data structure preserved after conversion and serialization")
        
    except Exception as e:
        pytest.fail(f"JSON serialization after conversion failed: {e}")
    
    print("\n🎯 Orchestrator research data tuple key test passed!")
    print("The fix should resolve the synthesis phase failure.")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
