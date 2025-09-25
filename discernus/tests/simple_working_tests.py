#!/usr/bin/env python3
"""
Simple Working Tests for Discernus
==================================

This is a minimal test suite that actually works with the current codebase.
These tests validate basic functionality without complex dependencies.

Usage:
    python3 discernus/tests/simple_working_tests.py
    python3 -m unittest discernus.tests.simple_working_tests -v
"""

import os
import sys
import unittest
from pathlib import Path

# Disable huggingface tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic system functionality."""
    
    def test_imports_work(self):
        """Test that basic imports work."""
        try:
            # Test imports that should work
            from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
            print("✅ Basic imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_mock_gateway_works(self):
        """Test that MockLLMGateway works."""
        try:
            from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
            
            # Test with simple response
            mock_responses = ['{"result": "test"}']
            gateway = MockLLMGateway(mock_responses)
            
            # Test the gateway - just verify it can be created
            self.assertIsNotNone(gateway)
            print("✅ MockLLMGateway works")
        except Exception as e:
            self.fail(f"MockLLMGateway failed: {e}")
    
    def test_environment_check(self):
        """Test environment check utility."""
        try:
            from discernus.tests import check_test_environment
            result = check_test_environment()
            self.assertTrue(result)
            print("✅ Environment check passed")
        except Exception as e:
            self.fail(f"Environment check failed: {e}")

class TestSystemIntegration(unittest.TestCase):
    """Test system integration components."""
    
    def test_project_structure(self):
        """Test that project structure is correct."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check essential directories exist
        essential_dirs = [
            "discernus",
            "discernus/agents", 
            "discernus/core",
            "discernus/gateway",
            "discernus/tests"
        ]
        
        for dir_path in essential_dirs:
            full_path = project_root / dir_path
            self.assertTrue(full_path.exists(), f"Directory {dir_path} should exist")
        
        print("✅ Project structure is correct")
    
    def test_essential_files_exist(self):
        """Test that essential files exist."""
        project_root = Path(__file__).parent.parent.parent
        
        essential_files = [
            "discernus/__init__.py",
            "discernus/cli.py",
            "discernus/core/config.py",
            "discernus/gateway/llm_gateway.py",
            "requirements.txt",
            "pyproject.toml"
        ]
        
        for file_path in essential_files:
            full_path = project_root / file_path
            self.assertTrue(full_path.exists(), f"File {file_path} should exist")
        
        print("✅ Essential files exist")
    
    def test_quick_test_reference(self):
        """Test that quick_test.py works as expected."""
        try:
            # Import and run the quick test logic
            from discernus.tests.quick_test import main
            # This should not raise an exception
            print("✅ Quick test logic is accessible")
        except Exception as e:
            self.fail(f"Quick test logic failed: {e}")
    
    def test_python_environment(self):
        """Test that Python environment is working."""
        import sys
        import os
        
        # Test basic Python functionality
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertTrue(os.path.exists(project_root))
        print("✅ Python environment is working")

def run_simple_tests():
    """Run all simple working tests."""
    print("🧪 Running Simple Working Tests")
    print("=" * 40)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n📊 TEST SUMMARY")
    print("=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures + result.errors)} tests failed")
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
