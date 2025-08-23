#!/usr/bin/env python3
"""
Test Script for Prompt Engineering Harness
==========================================

Simple validation tests to ensure the harness is working correctly.
Run this before using the harness for actual prompt testing.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from discernus.gateway.model_registry import ModelRegistry
        print("✅ ModelRegistry imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ModelRegistry: {e}")
        return False
    
    try:
        import litellm
        print("✅ LiteLLM imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LiteLLM: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    return True

def test_model_registry():
    """Test that the model registry is accessible."""
    print("\n🔍 Testing model registry...")
    
    try:
        from discernus.gateway.model_registry import ModelRegistry
        registry = ModelRegistry()
        models = registry.list_models()
        
        if models:
            print(f"✅ Model registry accessible with {len(models)} models")
            print(f"   Sample models: {', '.join(list(models)[:3])}")
            return True
        else:
            print("⚠️ Model registry accessible but no models found")
            return True
            
    except Exception as e:
        print(f"❌ Failed to access model registry: {e}")
        return False

def test_example_files():
    """Test that example prompt files exist."""
    print("\n🔍 Testing example files...")
    
    examples_dir = Path(__file__).parent / "examples"
    example_files = list(examples_dir.glob("*.txt"))
    
    if example_files:
        print(f"✅ Found {len(example_files)} example files:")
        for file in example_files:
            print(f"   - {file.name}")
        return True
    else:
        print("❌ No example files found")
        return False

def test_harness_script():
    """Test that the main harness script exists and is executable."""
    print("\n🔍 Testing harness script...")
    
    harness_script = Path(__file__).parent / "harness.py"
    
    if harness_script.exists():
        print("✅ Harness script exists")
        
        # Check if it's executable
        if harness_script.stat().st_mode & 0o111:
            print("✅ Harness script is executable")
        else:
            print("⚠️ Harness script exists but may not be executable")
        
        return True
    else:
        print("❌ Harness script not found")
        return False

def main():
    """Run all tests."""
    print("🧪 Prompt Engineering Harness Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_model_registry,
        test_example_files,
        test_harness_script
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The harness is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Run: python3 scripts/prompt_engineering/harness.py --list-models")
        print("   2. Test with: python3 scripts/prompt_engineering/harness.py --help")
        print("   3. Try an example: python3 scripts/prompt_engineering/harness.py --model 'vertex_ai/gemini-2.5-flash' --prompt 'Hello'")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
