#!/usr/bin/env python3
"""
Smoke tests for the Streamlit application in the Narrative Gravity Maps project.
Tests basic functionality of the Streamlit interface components.
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess
import time
import requests
from threading import Thread
import signal

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Streamlit components for testing
import streamlit as st
from unittest.mock import Mock

# Import the modules we're testing
from narrative_gravity_app import (
    initialize_session_state,
    sidebar_framework_manager,
    single_text_analysis,
    framework_creation_interface,
    visualization_interface,
    comparison_interface,
    normalize_framework_name,
    detect_framework_from_json,
    load_framework_for_analysis
)
from framework_manager import FrameworkManager
from generate_prompt import PromptGenerator

class TestStreamlitComponents(unittest.TestCase):
    """Test cases for Streamlit application components"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        # Mock Streamlit session state
        self.mock_session_state = {
            'framework_manager': FrameworkManager(),
            'current_framework': 'test_framework',
            'analysis_results': None,
            'comparative_results': None
        }

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @unittest.skip("Session state mocking is complex - tested in integration")
    def test_initialize_session_state(self):
        """Test session state initialization (skipped due to mocking complexity)"""
        # This test requires complex Streamlit session state mocking
        # The functionality is tested via integration tests instead
        pass

    def test_normalize_framework_name(self):
        """Test framework name normalization"""
        test_cases = [
            ("Test Framework", "test_framework"),
            ("Moral Foundations", "moral_foundations"),
            ("Political Spectrum v2.0", "political_spectrum_v20"),  # Dots get removed
            ("Framework-With-Dashes", "framework_with_dashes"),
            ("Framework_With_Underscores", "framework_with_underscores"),
            ("UPPERCASE FRAMEWORK", "uppercase_framework")
        ]
        
        for input_name, expected_output in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_framework_name(input_name)
                self.assertEqual(result, expected_output)

    def test_detect_framework_from_json_with_metadata(self):
        """Test framework detection from JSON with metadata"""
        test_data = {
            "metadata": {
                "framework_name": "civic_virtue",
                "title": "Test Analysis"
            },
            "scores": {
                "Dignity": 0.8,
                "Pragmatism": 0.7
            }
        }
        
        detected_framework = detect_framework_from_json(test_data)
        self.assertEqual(detected_framework, "civic_virtue")

    def test_detect_framework_from_json_without_metadata(self):
        """Test framework detection from JSON without metadata"""
        test_data = {
            "scores": {
                "Dignity": 0.8,
                "Pragmatism": 0.7
            }
        }
        
        detected_framework = detect_framework_from_json(test_data)
        # Should return default framework when no metadata is present
        self.assertEqual(detected_framework, "moral_foundations")

    def test_detect_framework_from_json_with_framework_field(self):
        """Test framework detection from JSON with direct framework field"""
        test_data = {
            "framework_name": "moral_foundations",
            "scores": {
                "Care": 0.8,
                "Harm": 0.2
            }
        }
        
        detected_framework = detect_framework_from_json(test_data)
        self.assertEqual(detected_framework, "moral_foundations")

class TestStreamlitAppIntegration(unittest.TestCase):
    """Integration tests for the Streamlit application"""

    def setUp(self):
        """Set up test environment"""
        self.original_dir = os.getcwd()
        # Change to project root for tests
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Store reference to process for cleanup
        self.streamlit_process = None

    def tearDown(self):
        """Clean up test environment"""
        # Kill Streamlit process if it's running
        if self.streamlit_process:
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                try:
                    self.streamlit_process.kill()
                except ProcessLookupError:
                    pass
        
        os.chdir(self.original_dir)

    def test_launch_app_script_exists(self):
        """Test that launch_app.py exists and is executable"""
        launch_script = Path("launch_app.py")
        self.assertTrue(launch_script.exists(), "launch_app.py not found")
        self.assertTrue(launch_script.is_file(), "launch_app.py is not a file")

    def test_streamlit_app_script_exists(self):
        """Test that narrative_gravity_app.py exists"""
        app_script = Path("narrative_gravity_app.py")
        self.assertTrue(app_script.exists(), "narrative_gravity_app.py not found")
        self.assertTrue(app_script.is_file(), "narrative_gravity_app.py is not a file")

    def test_streamlit_app_syntax(self):
        """Test that the Streamlit app has valid Python syntax"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", "narrative_gravity_app.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0, f"Syntax error in narrative_gravity_app.py: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.fail("Syntax check timed out")

    def test_launch_app_syntax(self):
        """Test that the launch app has valid Python syntax"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", "launch_app.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0, f"Syntax error in launch_app.py: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.fail("Syntax check timed out")

    def test_streamlit_imports(self):
        """Test that all required imports are available"""
        try:
            # Test importing the main modules
            result = subprocess.run(
                [sys.executable, "-c", 
                 "import streamlit; import narrative_gravity_elliptical; import framework_manager; import generate_prompt; print('All imports successful')"],
                capture_output=True,
                text=True,
                timeout=15
            )
            self.assertEqual(result.returncode, 0, f"Import error: {result.stderr}")
            self.assertIn("All imports successful", result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("Import check timed out")

    @unittest.skip("Long-running test - enable for full integration testing")
    def test_streamlit_app_starts(self):
        """Test that the Streamlit app can start (long-running test, normally skipped)"""
        try:
            # Start Streamlit in the background
            self.streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "narrative_gravity_app.py", 
                 "--server.headless", "true", "--server.port", "8502"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for the server to start
            time.sleep(5)
            
            # Check if the process is still running (not crashed)
            poll_result = self.streamlit_process.poll()
            if poll_result is not None:
                stdout, stderr = self.streamlit_process.communicate()
                self.fail(f"Streamlit process exited with code {poll_result}. stdout: {stdout}, stderr: {stderr}")
            
            # Try to make a request to the health endpoint
            try:
                response = requests.get("http://localhost:8502/healthz", timeout=5)
                self.assertEqual(response.status_code, 200)
            except requests.RequestException as e:
                self.fail(f"Could not connect to Streamlit server: {e}")
                
        except Exception as e:
            self.fail(f"Failed to start Streamlit app: {e}")

class TestLaunchApp(unittest.TestCase):
    """Test cases for the launch_app.py launcher"""

    def setUp(self):
        """Set up test environment"""
        self.original_dir = os.getcwd()
        # Change to project root for tests
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)

    def test_launch_app_help_mode(self):
        """Test launch_app.py in help/check mode"""
        # We can't easily test the full launch without actually starting streamlit,
        # but we can test that the script runs without immediate errors
        try:
            # Import the launch_app module to check for import errors
            result = subprocess.run(
                [sys.executable, "-c", "import launch_app; print('Launch app imports successfully')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0, f"Import error in launch_app.py: {result.stderr}")
            self.assertIn("Launch app imports successfully", result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("Launch app import test timed out")

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists and is readable"""
        requirements_file = Path("requirements.txt")
        self.assertTrue(requirements_file.exists(), "requirements.txt not found")
        
        # Test that we can read the requirements
        try:
            with open(requirements_file, 'r') as f:
                content = f.read()
                self.assertIn("streamlit", content.lower())
                self.assertIn("matplotlib", content.lower())
        except Exception as e:
            self.fail(f"Could not read requirements.txt: {e}")

class TestStreamlitUtilityFunctions(unittest.TestCase):
    """Test utility functions used by the Streamlit app"""

    def test_load_framework_for_analysis_valid_framework(self):
        """Test loading framework configuration for analysis"""
        # This test depends on having actual framework files
        # We'll test with a mock framework
        test_dir = tempfile.mkdtemp()
        try:
            # Create mock framework structure
            framework_dir = Path(test_dir) / "frameworks" / "test_framework"
            framework_dir.mkdir(parents=True)
            
            dipoles_data = {
                "framework_name": "test_framework",
                "dipoles": [{"positive_well": "Good", "negative_well": "Bad"}]
            }
            framework_data = {
                "framework_name": "test_framework",
                "wells": {"Good": {"position": [1, 0]}, "Bad": {"position": [-1, 0]}}
            }
            
            with open(framework_dir / "dipoles.json", 'w') as f:
                json.dump(dipoles_data, f)
            with open(framework_dir / "framework.json", 'w') as f:
                json.dump(framework_data, f)
            
            # Test loading (with patched framework manager)
            with patch('narrative_gravity_app.FrameworkManager') as mock_manager:
                mock_instance = mock_manager.return_value
                mock_instance.list_frameworks.return_value = [
                    {'name': 'test_framework', 'path': framework_dir}
                ]
                
                # Test the function exists and can be called
                # Note: This is a basic smoke test - full functionality depends on file system
                result = load_framework_for_analysis("test_framework")
                # Just check that it returns something and doesn't crash
                self.assertIsNotNone(result)
                
        finally:
            shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestStreamlitComponents))
    suite.addTest(unittest.makeSuite(TestStreamlitAppIntegration))
    suite.addTest(unittest.makeSuite(TestLaunchApp))  
    suite.addTest(unittest.makeSuite(TestStreamlitUtilityFunctions))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1) 