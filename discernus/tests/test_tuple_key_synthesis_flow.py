#!/usr/bin/env python3
"""
Test the complete synthesis flow with tuple keys to find where the error occurs.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pytest
import json
import tempfile
from pathlib import Path

def test_tuple_key_synthesis_flow():
    """Test the complete synthesis flow with tuple keys to reproduce the error."""
    
    # Create mock data with tuple keys (exactly like what's failing in CHF)
    mock_statistical_results = {
        'calculate_descriptive_stats_by_admin': {
            'administration_stats': {
                ('constitutional_health_index', 'mean'): {'Biden': 0.661, 'Trump': -0.048},
                ('constitutional_health_index', 'std'): {'Biden': 0.241, 'Trump': 0.699},
                ('constitutional_health_index', 'count'): {'Biden': 6, 'Trump': 4}
            }
        },
        'statistical_summary': 'Test summary'
    }
    
    # Test 1: Direct JSON serialization (should fail)
    print("Test 1: Direct JSON serialization")
    try:
        json_str = json.dumps(mock_statistical_results, indent=2)
        pytest.fail("Direct JSON serialization should have failed with tuple keys")
    except TypeError as e:
        print(f"✅ Expected failure: {e}")
    
    # Test 2: Tuple key conversion function
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
    
    converted_results = convert_tuple_keys_for_json(mock_statistical_results)
    
    # Test 3: JSON serialization after conversion (should succeed)
    print("\nTest 3: JSON serialization after conversion")
    try:
        json_str = json.dumps(converted_results, indent=2)
        print(f"✅ JSON serialization successful: {len(json_str)} characters")
        
        # Verify the structure
        assert "('constitutional_health_index', 'mean')" in json_str
        assert "('constitutional_health_index', 'std')" in json_str
        assert "('constitutional_health_index', 'count')" in json_str
        
    except Exception as e:
        pytest.fail(f"JSON serialization after conversion failed: {e}")
    
    # Test 4: Repr serialization (should succeed)
    print("\nTest 4: Repr serialization after conversion")
    try:
        repr_str = repr(converted_results)
        print(f"✅ Repr serialization successful: {len(repr_str)} characters")
        
        # Verify the structure
        assert "('constitutional_health_index', 'mean')" in repr_str
        assert "('constitutional_health_index', 'std')" in repr_str
        assert "('constitutional_health_index', 'count')" in repr_str
        
    except Exception as e:
        pytest.fail(f"Repr serialization after conversion failed: {e}")
    
    # Test 5: Simulate the research data structure that's passed to synthesis
    print("\nTest 5: Simulate research data structure")
    research_data = {
        "raw_analysis_results": {"test": "data"},
        "derived_metrics_results": {"test": "metrics"},
        "statistical_results": mock_statistical_results  # This has tuple keys!
    }
    
    # Test 6: JSON serialization of research data (should fail)
    print("\nTest 6: JSON serialization of research data (should fail)")
    try:
        json_str = json.dumps(research_data, indent=2)
        pytest.fail("Research data JSON serialization should have failed with tuple keys")
    except TypeError as e:
        print(f"✅ Expected failure: {e}")
    
    # Test 7: Convert research data and serialize (should succeed)
    print("\nTest 7: Convert research data and serialize")
    safe_research_data = convert_tuple_keys_for_json(research_data)
    try:
        json_str = json.dumps(safe_research_data, indent=2)
        print(f"✅ Safe research data JSON serialization successful: {len(json_str)} characters")
    except Exception as e:
        pytest.fail(f"Safe research data JSON serialization failed: {e}")
    
    # Test 8: Repr serialization of safe research data (should succeed)
    print("\nTest 8: Repr serialization of safe research data")
    try:
        repr_str = repr(safe_research_data)
        print(f"✅ Safe research data repr serialization successful: {len(repr_str)} characters")
    except Exception as e:
        pytest.fail(f"Safe research data repr serialization failed: {e}")
    
    print("\n🎯 All tuple key tests passed! The conversion function is working correctly.")
    print("The issue must be in another location in the synthesis flow.")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
