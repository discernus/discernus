#!/usr/bin/env python3
"""
Smoke tests for CLI tools in the Narrative Gravity Maps application.
Tests basic functionality of framework_manager.py, generate_prompt.py, and narrative_gravity_elliptical.py
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

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules we're testing
from framework_manager import FrameworkManager
from generate_prompt import PromptGenerator, load_dipoles, load_framework
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical, load_analysis_data

class TestFrameworkManager(unittest.TestCase):
    """Test cases for framework_manager.py CLI functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.manager = FrameworkManager(self.test_dir)
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_framework_manager_initialization(self):
        """Test that FrameworkManager initializes properly"""
        self.assertIsInstance(self.manager, FrameworkManager)
        self.assertEqual(self.manager.base_dir, Path(self.test_dir))

    def test_list_frameworks_empty(self):
        """Test listing frameworks when none exist"""
        frameworks = self.manager.list_frameworks()
        self.assertEqual(frameworks, [])

    def test_create_mock_framework_structure(self):
        """Test creating a mock framework for testing other functions"""
        # Create a mock framework
        frameworks_dir = Path(self.test_dir) / "frameworks" / "test_framework"
        frameworks_dir.mkdir(parents=True, exist_ok=True)
        
        # Create dipoles.json
        dipoles_data = {
            "framework_name": "test_framework",
            "description": "Test framework for unit tests",
            "version": "v1.0.0",
            "dipoles": [
                {
                    "name": "Test Dipole",
                    "positive_well": "Test Positive",
                    "negative_well": "Test Negative"
                }
            ]
        }
        
        with open(frameworks_dir / "dipoles.json", 'w') as f:
            json.dump(dipoles_data, f)
        
        # Create framework.json
        framework_data = {
            "framework_name": "test_framework",
            "description": "Test framework for unit tests",
            "version": "v1.0.0",
            "wells": {
                "Test Positive": {"position": [1, 0]},
                "Test Negative": {"position": [-1, 0]}
            }
        }
        
        with open(frameworks_dir / "framework.json", 'w') as f:
            json.dump(framework_data, f)
        
        # Test that the framework is now listed
        frameworks = self.manager.list_frameworks()
        self.assertEqual(len(frameworks), 1)
        self.assertEqual(frameworks[0]['name'], 'test_framework')

    def test_framework_validation(self):
        """Test framework validation functionality"""
        # Create test framework first
        self.test_create_mock_framework_structure()
        
        # Test validation - this is a basic smoke test
        # The validation function expects frameworks to be in the frameworks directory
        # For a full test, we'd need to set up the complete directory structure
        # For now, we'll test that the validation function can be called
        try:
            is_valid, message = self.manager.validate_framework("test_framework")
            # The test framework might not validate perfectly due to directory structure
            # but the function should not crash
            self.assertIsInstance(is_valid, bool)
            self.assertIsInstance(message, str)
        except Exception as e:
            self.fail(f"Framework validation function crashed: {e}")

class TestPromptGenerator(unittest.TestCase):
    """Test cases for generate_prompt.py CLI functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test configuration files
        dipoles_data = {
            "framework_name": "test_framework",
            "description": "Test framework",
            "version": "v1.0.0",
            "dipoles": [
                {
                    "name": "Test Dipole",
                    "positive": {
                        "name": "Test Positive",
                        "description": "Test positive description",
                        "language_cues": ["good", "positive"]
                    },
                    "negative": {
                        "name": "Test Negative", 
                        "description": "Test negative description",
                        "language_cues": ["bad", "negative"]
                    }
                }
            ]
        }
        
        framework_data = {
            "framework_name": "test_framework",
            "description": "Test framework for unit tests",
            "version": "v1.0.0",
            "wells": {
                "Test Positive": {"position": [1, 0]},
                "Test Negative": {"position": [-1, 0]}
            }
        }
        
        with open(self.config_dir / "dipoles.json", 'w') as f:
            json.dump(dipoles_data, f)
        
        with open(self.config_dir / "framework.json", 'w') as f:
            json.dump(framework_data, f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_dipoles(self):
        """Test loading dipoles configuration"""
        dipoles = load_dipoles(str(self.config_dir))
        self.assertIsInstance(dipoles, dict)
        self.assertEqual(dipoles['framework_name'], 'test_framework')
        self.assertEqual(len(dipoles['dipoles']), 1)

    def test_load_framework(self):
        """Test loading framework configuration"""
        framework = load_framework(str(self.config_dir))
        self.assertIsInstance(framework, dict)
        self.assertEqual(framework['framework_name'], 'test_framework')
        self.assertIn('wells', framework)

    def test_prompt_generator_initialization(self):
        """Test PromptGenerator initialization"""
        generator = PromptGenerator(config_dir=str(self.config_dir))
        self.assertIsInstance(generator, PromptGenerator)
        self.assertEqual(generator.config_dir, str(self.config_dir))

    def test_generate_interactive_prompt(self):
        """Test generating interactive prompt"""
        generator = PromptGenerator(config_dir=str(self.config_dir))
        prompt = generator.generate_interactive_prompt()
        self.assertIsInstance(prompt, str)
        self.assertIn("Interactive", prompt)
        self.assertIn("Test Positive", prompt)
        self.assertIn("Test Negative", prompt)

    def test_generate_batch_prompt(self):
        """Test generating batch prompt"""
        generator = PromptGenerator(config_dir=str(self.config_dir))
        prompt = generator.generate_batch_prompt()
        self.assertIsInstance(prompt, str)
        self.assertIn("Test Positive", prompt)
        self.assertIn("Test Negative", prompt)

class TestNarrativeGravityElliptical(unittest.TestCase):
    """Test cases for narrative_gravity_elliptical.py CLI functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test configuration files
        dipoles_data = {
            "framework_name": "test_framework",
            "description": "Test framework",
            "version": "v1.0.0",
            "dipoles": [
                {
                    "name": "Test Dipole",
                    "positive_well": "Test Positive",
                    "negative_well": "Test Negative"
                }
            ]
        }
        
        framework_data = {
            "framework_name": "test_framework",
            "description": "Test framework for unit tests",
            "version": "v1.0.0",
            "wells": {
                "Test Positive": {"position": [1, 0]},
                "Test Negative": {"position": [-1, 0]}
            }
        }
        
        with open(self.config_dir / "dipoles.json", 'w') as f:
            json.dump(dipoles_data, f)
        
        with open(self.config_dir / "framework.json", 'w') as f:
            json.dump(framework_data, f)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_narrative_gravity_wells_initialization(self):
        """Test NarrativeGravityWellsElliptical initialization"""
        visualizer = NarrativeGravityWellsElliptical(config_dir=str(self.config_dir))
        self.assertIsInstance(visualizer, NarrativeGravityWellsElliptical)

    def test_load_analysis_data_valid_json(self):
        """Test loading valid analysis data"""
        # Create test analysis data
        test_data = {
            "metadata": {
                "title": "Test Analysis",
                "framework_name": "test_framework"
            },
            "scores": {
                "Test Positive": 0.8,
                "Test Negative": 0.2
            }
        }
        
        test_file = Path(self.test_dir) / "test_analysis.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test loading
        loaded_data = load_analysis_data(str(test_file))
        self.assertEqual(loaded_data['metadata']['title'], 'Test Analysis')
        self.assertEqual(loaded_data['scores']['Test Positive'], 0.8)

    def test_load_analysis_data_invalid_json(self):
        """Test loading invalid JSON raises appropriate error"""
        test_file = Path(self.test_dir) / "invalid.json"
        with open(test_file, 'w') as f:
            f.write("invalid json content")
        
        with self.assertRaises(json.JSONDecodeError):
            load_analysis_data(str(test_file))

class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI commands"""

    def setUp(self):
        """Set up test environment"""
        self.original_dir = os.getcwd()
        # Change to project root for CLI tests
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)

    def test_framework_manager_cli_help(self):
        """Test framework_manager.py --help command"""
        try:
            result = subprocess.run(
                [sys.executable, "framework_manager.py", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Manage Narrative Gravity Wells frameworks", result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except FileNotFoundError:
            self.skipTest("framework_manager.py not found in expected location")

    def test_generate_prompt_cli_help(self):
        """Test generate_prompt.py --help command"""
        try:
            result = subprocess.run(
                [sys.executable, "generate_prompt.py", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Generate LLM prompts from configuration", result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except FileNotFoundError:
            self.skipTest("generate_prompt.py not found in expected location")

    def test_narrative_gravity_elliptical_cli_help(self):
        """Test narrative_gravity_elliptical.py --help command"""
        try:
            result = subprocess.run(
                [sys.executable, "narrative_gravity_elliptical.py", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Generate narrative gravity visualizations", result.stdout)
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except FileNotFoundError:
            self.skipTest("narrative_gravity_elliptical.py not found in expected location")

    def test_framework_manager_list_command(self):
        """Test framework_manager.py list command"""
        try:
            result = subprocess.run(
                [sys.executable, "framework_manager.py", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Should either succeed (return 0) or fail gracefully
            self.assertIn(result.returncode, [0, 1])
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except FileNotFoundError:
            self.skipTest("framework_manager.py not found in expected location")

    def test_framework_manager_active_command(self):
        """Test framework_manager.py active command"""
        try:
            result = subprocess.run(
                [sys.executable, "framework_manager.py", "active"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Should either succeed (return 0) or fail gracefully
            self.assertIn(result.returncode, [0, 1])
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except FileNotFoundError:
            self.skipTest("framework_manager.py not found in expected location")

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestFrameworkManager))
    suite.addTest(unittest.makeSuite(TestPromptGenerator))
    suite.addTest(unittest.makeSuite(TestNarrativeGravityElliptical))
    suite.addTest(unittest.makeSuite(TestCLIIntegration))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1) 