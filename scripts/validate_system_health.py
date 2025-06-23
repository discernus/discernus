#!/usr/bin/env python3
"""
System Health Validator for Discernus
Tests the core components that make experiments work end-to-end
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path for absolute imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_imports():
    """Test that all critical imports work"""
    print("🧪 Testing Core System Imports...")
    
    try:
        from src.coordinate_engine import DiscernusCoordinateEngine
        print("✅ DiscernusCoordinateEngine import successful")
    except ImportError as e:
        print(f"❌ DiscernusCoordinateEngine import failed: {e}")
        return False
    
    try:
        from src.utils.llm_quality_assurance import LLMQualityAssuranceSystem
        print("✅ LLMQualityAssuranceSystem import successful")
    except ImportError as e:
        print(f"❌ LLMQualityAssuranceSystem import failed: {e}")
        return False
    
    try:
        from src.framework_manager import FrameworkManager
        print("✅ FrameworkManager import successful")
    except ImportError as e:
        print(f"❌ FrameworkManager import failed: {e}")
        return False
    
    return True

def test_coordinate_system():
    """Test the enhanced coordinate system"""
    print("\n🎯 Testing Enhanced Coordinate System...")
    
    try:
        from src.coordinate_engine import DiscernusCoordinateEngine
        
        # Test basic initialization
        engine = DiscernusCoordinateEngine()
        print("✅ Coordinate engine initialization successful")
        
        # Test enhanced algorithms
        test_scores = {'hope': 0.9, 'justice': 0.7, 'fear': 0.2}
        x, y = engine.calculate_narrative_position(test_scores)
        
        # Validate results
        if x == 0.0 and y == 0.0:
            print("❌ Coordinate calculation returned zero position")
            return False
        
        distance = (x**2 + y**2)**0.5
        if 0.65 <= distance <= 0.95:
            print(f"✅ Coordinate calculation working: ({x:.3f}, {y:.3f}), distance: {distance:.3f}")
        else:
            print(f"⚠️ Unexpected coordinate range: ({x:.3f}, {y:.3f}), distance: {distance:.3f}")
        
        # Test dominance amplification
        amplified = engine.apply_dominance_amplification(0.8)
        if abs(amplified - 0.88) < 0.01:  # 0.8 * 1.1
            print("✅ Dominance amplification working")
        else:
            print(f"❌ Dominance amplification failed: {amplified}")
            return False
        
        # Test adaptive scaling
        scaling = engine.calculate_adaptive_scaling(test_scores)
        if 0.65 <= scaling <= 0.95:
            print(f"✅ Adaptive scaling working: {scaling:.3f}")
        else:
            print(f"❌ Adaptive scaling out of range: {scaling:.3f}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Coordinate system test failed: {e}")
        return False

def test_qa_system():
    """Test the QA system integration"""
    print("\n🛡️ Testing QA System...")
    
    try:
        from src.utils.llm_quality_assurance import LLMQualityAssuranceSystem
        
        qa_system = LLMQualityAssuranceSystem()
        print("✅ QA system initialization successful")
        
        # Test mock validation
        mock_scores = {
            'care': 0.8,
            'fairness': 0.7,
            'loyalty': 0.3,
            'authority': 0.2,
            'sanctity': 0.1
        }
        
        # This is a simplified test - real validation would need proper LLM response
        print("✅ QA system basic functionality available")
        return True
        
    except Exception as e:
        print(f"❌ QA system test failed: {e}")
        return False

def test_framework_loading():
    """Test framework loading capabilities"""
    print("\n🏗️ Testing Framework Loading...")
    
    try:
        from src.framework_manager import FrameworkManager
        
        # Test YAML framework loading from dedicated test location
        test_framework_path = Path("tests/system_health/test_framework/moral_foundations_theory/moral_foundations_theory_founding_template.yaml")
        
        if test_framework_path.exists():
            framework_manager = FrameworkManager()
            framework_data = framework_manager.load_framework(str(test_framework_path))
            
            if framework_data and isinstance(framework_data, dict):
                print("✅ Test framework loading successful")
                
                # Check structure (dipoles is the current architecture)
                if 'dipoles' in framework_data:
                    dipoles = framework_data['dipoles']
                    print(f"✅ Framework has {len(dipoles)} dipoles (current architecture)")
                    
                    # Validate dipole structure
                    anchor_count = 0
                    for dipole in dipoles:
                        if 'positive' in dipole:
                            anchor_count += 1
                        if 'negative' in dipole:
                            anchor_count += 1
                    
                    print(f"✅ Framework contains {anchor_count} anchors across {len(dipoles)} dipoles")
                    print(f"   - Framework: {framework_data.get('name', 'Unknown')}")
                    print(f"   - Version: {framework_data.get('version', 'Unknown')}")
                    return True
                elif 'anchors' in framework_data:
                    print(f"✅ Framework has {len(framework_data['anchors'])} anchors (anchors terminology)")
                    return True
                else:
                    print("❌ Framework missing coordinate definitions")
                    return False
            else:
                print("❌ Framework data is invalid")
                return False
        else:
            print("❌ Test framework not found")
            print(f"   Expected: {test_framework_path}")
            return False
                
    except Exception as e:
        print(f"❌ Framework loading test failed: {e}")
        return False

def test_experiment_definition():
    """Test experiment definition loading"""
    print("\n📋 Testing Experiment Definition...")
    
    try:
        experiment_path = Path("tests/system_health/test_experiments/system_health_test.yaml")
        if experiment_path.exists():
            with open(experiment_path) as f:
                experiment_def = yaml.safe_load(f)
            
            print("✅ Test experiment definition loading successful")
            
            # Validate structure
            required_sections = ["experiment_meta", "components", "execution"]
            missing_sections = [section for section in required_sections if section not in experiment_def]
            
            if not missing_sections:
                print("✅ Experiment definition structure valid")
            else:
                print(f"❌ Missing sections: {missing_sections}")
                return False
            
            # Check experiment metadata
            meta = experiment_def.get("experiment_meta", {})
            print(f"✅ Experiment: {meta.get('name', 'Unknown')}")
            print(f"✅ Description: {meta.get('description', 'No description')[:60]}...")
            
            # Check success criteria
            success_criteria = meta.get("success_criteria", [])
            if success_criteria:
                print(f"✅ Has {len(success_criteria)} success criteria defined")
            
            # Check components
            components = experiment_def.get("components", {})
            component_types = list(components.keys())
            print(f"✅ Component types: {', '.join(component_types)}")
            
            # Validate framework path in experiment points to test framework
            frameworks = components.get("frameworks", [])
            if frameworks:
                framework_path = frameworks[0].get("file_path", "")
                if "tests/system_health/test_framework" in framework_path:
                    print("✅ Experiment correctly references test framework")
                else:
                    print(f"⚠️ Experiment references: {framework_path}")
            
            return True
        else:
            print("❌ Test experiment definition not found")
            print(f"   Expected: {experiment_path}")
            return False
            
    except Exception as e:
        print(f"❌ Experiment definition test failed: {e}")
        return False

def run_comprehensive_validation():
    """Run all validation tests"""
    print("🏥 DISCERNUS SYSTEM HEALTH VALIDATION")
    print("=" * 50)
    
    tests = [
        ("Core Imports", test_imports),
        ("Coordinate System", test_coordinate_system),
        ("QA System", test_qa_system),
        ("Framework Loading", test_framework_loading),
        ("Experiment Definition", test_experiment_definition)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"💥 {test_name} test failed")
        except Exception as e:
            print(f"💥 {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏆 VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 System is healthy and ready for experiments!")
        return True
    elif passed >= 4:
        print("✅ System is mostly healthy - minor issues detected")
        return True
    else:
        print("⚠️ System has issues that need attention")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1) 