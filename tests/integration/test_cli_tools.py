import pytest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
import subprocess

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.narrative_gravity.framework_manager import FrameworkManager
from scripts.generate_prompt import PromptGenerator, load_dipoles, load_framework
from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular

# --- Fixtures for setting up test environments ---

@pytest.fixture
def temp_test_dir():
    """Create a temporary directory for tests and clean up after."""
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir, ignore_errors=True)

@pytest.fixture
def framework_manager(temp_test_dir):
    """Fixture for FrameworkManager tests."""
    return FrameworkManager(temp_test_dir)

@pytest.fixture
def prompt_generator_fixture(temp_test_dir):
    """Fixture for PromptGenerator tests with mock config."""
    config_dir = Path(temp_test_dir) / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    dipoles_data = {
        "framework_name": "test_framework", "dipoles": [{
            "name": "Test Dipole",
            "positive": {"name": "Test Positive", "description": "d", "language_cues": ["c"]},
            "negative": {"name": "Test Negative", "description": "d", "language_cues": ["c"]}
        }]
    }
    framework_data = {
        "framework_name": "test_framework", "wells": {
            "Test Positive": {"position": [1, 0]}, "Test Negative": {"position": [-1, 0]}
        }
    }
    
    with open(config_dir / "dipoles.json", 'w') as f:
        json.dump(dipoles_data, f)
    with open(config_dir / "framework.json", 'w') as f:
        json.dump(framework_data, f)
        
    return PromptGenerator(config_dir=str(config_dir)), str(config_dir)

# --- Test Classes ---

class TestFrameworkManagerIntegration:
    """Integration tests for framework_manager.py CLI functionality."""

    def test_framework_manager_initialization(self, framework_manager):
        assert isinstance(framework_manager, FrameworkManager)

    def test_list_frameworks_empty(self, framework_manager):
        assert framework_manager.list_frameworks() == []

    def test_create_and_list_framework(self, framework_manager):
        # Create a mock framework structure
        frameworks_dir = Path(framework_manager.base_dir) / "frameworks" / "test_framework"
        frameworks_dir.mkdir(parents=True, exist_ok=True)
        
        # Create both required files
        with open(frameworks_dir / "dipoles.json", 'w') as f:
            json.dump({
                "framework_name": "test_framework",
                "version": "1.0.0",
                "description": "Test framework",
                "dipoles": []
            }, f)
        
        with open(frameworks_dir / "framework.json", 'w') as f:
            json.dump({
                "framework_name": "test_framework", 
                "version": "1.0.0",
                "description": "Test framework",
                "wells": {}
            }, f)
        
        frameworks = framework_manager.list_frameworks()
        assert len(frameworks) == 1
        assert frameworks[0]['name'] == 'test_framework'

class TestPromptGeneratorIntegration:
    """Integration tests for generate_prompt.py CLI functionality."""

    def test_load_dipoles_and_framework(self, prompt_generator_fixture):
        _, config_dir = prompt_generator_fixture
        dipoles = load_dipoles(config_dir)
        framework = load_framework(config_dir)
        assert dipoles['framework_name'] == 'test_framework'
        assert framework['framework_name'] == 'test_framework'

    def test_generate_prompts(self, prompt_generator_fixture):
        generator, config_dir = prompt_generator_fixture
        
        # Create the framework directory structure that the generator expects
        temp_dir = Path(config_dir).parent
        frameworks_dir = temp_dir / "frameworks" / "test_framework"
        frameworks_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the test files to the expected location
        import shutil
        shutil.copy(Path(config_dir) / "dipoles.json", frameworks_dir / "dipoles.json")
        shutil.copy(Path(config_dir) / "framework.json", frameworks_dir / "framework.json")
        
        # Change to temp directory so the generator can find the frameworks
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            interactive_prompt = generator.generate_interactive_prompt()
            batch_prompt = generator.generate_batch_prompt()
            assert "Interactive" in interactive_prompt
            assert "Test Positive" in interactive_prompt
            assert "Test Positive" in batch_prompt
        finally:
            os.chdir(original_cwd)

class TestNarrativeGravityCircularIntegration:
    """Integration tests for circular coordinate system engine."""

    def test_circular_engine_initialization(self, temp_test_dir):
        """Test that the circular engine can be initialized properly."""
        engine = NarrativeGravityWellsCircular(config_dir=temp_test_dir)
        assert hasattr(engine, 'circle_radius')
        assert engine.circle_radius == 1.0
        assert hasattr(engine, 'well_definitions')
        assert isinstance(engine.well_definitions, dict)

class TestCLIExecutionIntegration:
    """Tests the CLI execution of the tools via subprocess."""

    def run_cli_command(self, command):
        """Helper to run a CLI command and return its output."""
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result.stdout, result.stderr, result.returncode

    def test_framework_manager_cli_help(self):
        stdout, _, exit_code = self.run_cli_command(["python", "src/narrative_gravity/framework_manager.py", "--help"])
        assert exit_code == 0
        assert "usage:" in stdout

    def test_generate_prompt_cli_help(self):
        stdout, _, exit_code = self.run_cli_command(["python", "scripts/generate_prompt.py", "--help"])
        assert exit_code == 0
        assert "usage:" in stdout

    def test_narrative_gravity_circular_cli_help(self):
        # Test the circular coordinate system engine CLI
        stdout, _, exit_code = self.run_cli_command(["python", "src/narrative_gravity/engine_circular.py", "--help"])
        assert exit_code == 0
        assert "usage:" in stdout 