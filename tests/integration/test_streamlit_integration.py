import pytest
import sys
import os
import subprocess
import time
import requests
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Note: The functions being tested here are not pure and have side effects,
# making them integration tests rather than unit tests.
from narrative_gravity_app import load_framework_for_analysis

class TestStreamlitAppAndLaunchIntegration:
    """
    Integration tests for the Streamlit application's basic integrity and launch scripts.
    """

    @pytest.fixture(scope="class")
    def project_root(self):
        """Fixture to run tests from the project's root directory."""
        original_dir = os.getcwd()
        root = Path(__file__).parent.parent.parent
        os.chdir(root)
        yield root
        os.chdir(original_dir)

    def test_app_and_launch_scripts_exist(self, project_root):
        """Tests that the main application and launch scripts exist."""
        assert (project_root / "narrative_gravity_app.py").is_file()
        assert (project_root / "launch_app.py").is_file()

    @pytest.mark.parametrize("script_name", [
        "narrative_gravity_app.py",
        "launch_app.py"
    ])
    def test_script_syntax(self, project_root, script_name):
        """Tests that critical scripts have valid Python syntax."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", script_name],
                capture_output=True, text=True, timeout=10, check=False
            )
            assert result.returncode == 0, f"Syntax error in {script_name}: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.fail(f"Syntax check timed out for {script_name}")

    def test_launch_app_help_mode(self, project_root):
        """Tests that launch_app.py responds to --help."""
        result = subprocess.run(
            [sys.executable, "launch_app.py", "--help"],
            capture_output=True, text=True, check=False
        )
        assert result.returncode == 0
        assert "usage: launch_app.py" in result.stdout

    def test_requirements_file_exists(self, project_root):
        """Ensures the requirements.txt file exists."""
        assert (project_root / "requirements.txt").is_file()

    @pytest.mark.skip(reason="Long-running test, enable for full integration runs.")
    def test_streamlit_app_starts(self, project_root):
        """
        Tests if the Streamlit application can be started successfully.
        This is a long-running test and is skipped by default.
        """
        process = None
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "narrative_gravity_app.py",
                 "--server.headless", "true", "--server.port", "8503"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            time.sleep(5)  # Give the server a moment to start

            assert process.poll() is None, f"Streamlit process exited unexpectedly. Stderr: {process.stderr.read()}"

            response = requests.get("http://localhost:8503/healthz", timeout=5)
            assert response.status_code == 200, "Health check failed."

        finally:
            if process:
                process.terminate()
                process.wait(timeout=5)
                if process.poll() is None:
                    process.kill() 