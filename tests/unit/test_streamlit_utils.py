import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from narrative_gravity_app import (
    normalize_framework_name,
    detect_framework_from_json
)

class TestStreamlitUtils:
    """
    Unit tests for pure utility functions used in the Streamlit application.
    """

    @pytest.mark.parametrize("input_name, expected_output", [
        ("Test Framework", "test_framework"),
        ("Moral Foundations", "moral_foundations"),
        ("Political Spectrum v2.0", "political_spectrum_v20"),
        ("Framework-With-Dashes", "framework_with_dashes"),
        ("Framework_With_Underscores", "framework_with_underscores"),
        ("UPPERCASE FRAMEWORK", "uppercase_framework")
    ])
    def test_normalize_framework_name(self, input_name, expected_output):
        """Tests that framework names are correctly sanitized for internal use."""
        assert normalize_framework_name(input_name) == expected_output

    def test_detect_framework_from_json_with_metadata(self):
        """Tests detecting framework from the 'metadata' block of a JSON object."""
        test_data = {
            "metadata": {"framework_name": "civic_virtue"},
            "scores": {"Dignity": 0.8}
        }
        assert detect_framework_from_json(test_data) == "civic_virtue"

    def test_detect_framework_from_json_without_metadata(self):
        """Tests that a default framework is returned if no metadata is present."""
        test_data = {"scores": {"Dignity": 0.8}}
        # The function is expected to return a default, which is 'moral_foundations'
        assert detect_framework_from_json(test_data) == "moral_foundations"

    def test_detect_framework_from_json_with_direct_framework_field(self):
        """Tests detecting framework from a direct 'framework_name' field."""
        test_data = {
            "framework_name": "political_spectrum",
            "scores": {"Left": 0.9, "Right": 0.1}
        }
        assert detect_framework_from_json(test_data) == "political_spectrum" 