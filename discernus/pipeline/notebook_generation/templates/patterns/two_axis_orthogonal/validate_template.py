#!/usr/bin/env python3
"""
Template Validation Script
Tests key components of the template notebook to catch issues quickly.
"""

import sys
import traceback

def test_imports():
    """Test all required imports"""
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd
        import yaml
        from discernus.visualization import setup_style
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_design_system():
    """Test the centralized design system"""
    try:
        from discernus.visualization import setup_style
        setup_style('discernus')
        print("✅ Design system configured successfully")
        return True
    except Exception as e:
        print(f"❌ Design system error: {e}")
        return False

def test_data_generation():
    """Test synthetic data generation"""
    try:
        import numpy as np
        import pandas as pd
        
        np.random.seed(42)
        dates = pd.date_range('2018-01-15', '2018-10-28', periods=127)
        
        speeches = []
        for i, date in enumerate(dates):
            speeches.append({
                'speech_id': f'test_speech_{i+1:03d}',
                'date': date,
                'populism_score': np.random.uniform(0, 2),
                'pluralism_score': np.random.uniform(0, 2),
                'nationalism_score': np.random.uniform(0, 2),
                'patriotism_score': np.random.uniform(0, 2),
                'temporal_phase': 'test_phase'
            })
        
        test_df = pd.DataFrame(speeches)
        print(f"✅ Data generation successful: {len(test_df)} speeches")
        return True
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

def test_coordinate_calculation():
    """Test orthogonal coordinate calculation"""
    try:
        import numpy as np
        
        def calculate_orthogonal_signatures(scores_dict):
            populism = scores_dict['populism_score']
            pluralism = scores_dict['pluralism_score'] 
            nationalism = scores_dict['nationalism_score']
            patriotism = scores_dict['patriotism_score']
            
            vertical_axis = (populism - pluralism) / 2.0
            horizontal_axis = (nationalism - patriotism) / 2.0
            
            return np.array([horizontal_axis, vertical_axis])
        
        test_scores = {
            'populism_score': 1.5,
            'pluralism_score': 0.5,
            'nationalism_score': 1.2,
            'patriotism_score': 0.8
        }
        
        coords = calculate_orthogonal_signatures(test_scores)
        print(f"✅ Coordinate calculation successful: ({coords[0]:.3f}, {coords[1]:.3f})")
        return True
    except Exception as e:
        print(f"❌ Coordinate calculation error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🔍 Validating Template Components")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Design System", test_design_system), 
        ("Data Generation", test_data_generation),
        ("Coordinate Calculation", test_coordinate_calculation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            success = test_func()
            results.append(success)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    overall = "✅ ALL TESTS PASSED" if all(results) else "❌ SOME TESTS FAILED"
    print(f"\nOverall: {overall}")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 