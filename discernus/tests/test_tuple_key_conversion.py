#!/usr/bin/env python3
"""
Test the tuple key conversion functionality.
"""

import pytest
import json

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

class TestTupleKeyConversion:
    """Test tuple key conversion functionality."""
    
    def test_convert_tuple_keys_for_json(self):
        """Test that tuple keys are converted to strings for JSON serialization."""
        # Test data with tuple keys (like pandas groupby().agg() produces)
        test_data = {
            'calculate_descriptive_stats_by_admin': {
                'administration_stats': {
                    ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                    ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699},
                    ('constitutional_health_index', 'count'): {'Biden': 6, 'Trump': 4}
                }
            }
        }
        
        # Convert tuple keys
        converted_data = convert_tuple_keys_for_json(test_data)
        
        # Verify tuple keys were converted to strings
        assert isinstance(converted_data['calculate_descriptive_stats_by_admin']['administration_stats'], dict)
        
        # Check that the tuple keys are now strings
        admin_stats = converted_data['calculate_descriptive_stats_by_admin']['administration_stats']
        assert "('constitutional_health_index', 'mean')" in admin_stats
        assert "('constitutional_health_index', 'std')" in admin_stats
        assert "('constitutional_health_index', 'count')" in admin_stats
        
        # Verify the values are preserved
        assert admin_stats["('constitutional_health_index', 'mean')"]['Biden'] == 0.661
        assert admin_stats["('constitutional_health_index', 'std')"]['Trump'] == 0.699
        
        # Verify the conversion can be JSON serialized
        json_str = json.dumps(converted_data, indent=2)
        assert json_str is not None
        assert len(json_str) > 0
        
        print("✅ Tuple key conversion test passed!")
        print(f"Original data had {len(test_data['calculate_descriptive_stats_by_admin']['administration_stats'])} tuple keys")
        print(f"Converted data has {len(converted_data['calculate_descriptive_stats_by_admin']['administration_stats'])} string keys")
        print(f"JSON serialization successful: {len(json_str)} characters")
        
        # Test that the original data would fail JSON serialization
        try:
            json.dumps(test_data, indent=2)
            pytest.fail("Original data with tuple keys should have failed JSON serialization")
        except TypeError:
            print("✅ Original data correctly failed JSON serialization (as expected)")
            pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
