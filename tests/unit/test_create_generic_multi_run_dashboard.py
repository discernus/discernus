import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from scripts.create_generic_multi_run_dashboard import (
    extract_scores_from_raw_response,
    extract_analysis_from_raw_response,
    parse_filename_metadata,
    detect_framework_structure
)

class TestDashboardScriptLogic:
    """
    Unit tests for the helper functions in the create_generic_multi_run_dashboard.py script.
    """

    @pytest.mark.parametrize("raw_response, expected_scores", [
        # Test case 1: Clean JSON with surrounding text
        (
            "Here is the analysis:\n"
            '{\n  "scores": {\n    "Dignity": 8.5,\n    "Truth": 7.0\n  },\n'
            '  "analysis": "A brief analysis."\n}\n'
            "Some trailing text.",
            {"Dignity": 8.5, "Truth": 7.0}
        ),
        # Test case 2: JSON only
        (
            '{"scores": {"Hope": 9, "Fear": 2}, "analysis": "another"}',
            {"Hope": 9, "Fear": 2}
        ),
        # Test case 3: Malformed JSON or no JSON
        (
            "This is just text without any JSON.",
            {}
        ),
        # Test case 4: Empty scores dictionary
        (
            '{"scores": {}, "analysis": "empty scores"}',
            {}
        ),
        # Test case 5: No 'scores' key
        (
            '{"analysis": "no scores key"}',
            {}
        ),
        # Test case 6: String with json-like but incorrect structure
        (
            "Here are some {scores: incorrect} values.",
            {}
        ),
    ])
    def test_extract_scores_from_raw_response(self, raw_response, expected_scores):
        assert extract_scores_from_raw_response(raw_response) == expected_scores

    @pytest.mark.parametrize("raw_response, expected_analysis", [
        (
            "Preamble...\n"
            '{\n  "scores": {\n    "Dignity": 8.5\n  },\n'
            '  "analysis": "This is the core analysis."\n}\n'
            "Postamble.",
            "This is the core analysis."
        ),
        (
            '{"scores": {}, "analysis": ""}',
            ""
        ),
        (
            '{"scores": {"Hope": 1}}',
            ""
        ),
        (
            "Some text but no json.",
            ""
        )
    ])
    def test_extract_analysis_from_raw_response(self, raw_response, expected_analysis):
        assert extract_analysis_from_raw_response(raw_response) == expected_analysis

    @pytest.mark.parametrize("filename, expected_metadata", [
        (
            "obama_2009_civic_virtue_20250604_120000.json",
            {'speaker': 'Obama', 'year': '2009', 'framework': 'Civic Virtue'}
        ),
        (
            "trump_multi_run_moral_foundations_20250101_000000.txt",
            {'speaker': 'Trump', 'framework': 'Moral Foundations'}
        ),
        (
            "biden_political_spectrum_2024.md",
            {'speaker': 'Biden', 'framework': 'Political Spectrum', 'year': '2024'}
        ),
        (
            "some_other_file_without_metadata.log",
            {}
        )
    ])
    def test_parse_filename_metadata(self, filename, expected_metadata):
        assert parse_filename_metadata(filename) == expected_metadata

    def test_detect_framework_structure(self):
        # Test with Civic Virtue wells
        civic_virtue_scores = [{'Dignity': 8, 'Truth': 7, 'Hope': 6, 'Justice': 9, 'Pragmatism': 5, 
                                'Tribalism': 2, 'Manipulation': 3, 'Fantasy': 1, 'Resentment': 4, 'Fear': 0}]
        framework = detect_framework_structure(civic_virtue_scores)
        assert framework['framework_type'] == 'civic_virtue'
        assert 'Dignity' in framework['integrative_wells']
        assert 'Fear' in framework['disintegrative_wells']

        # Test with a generic, non-matching set of wells
        generic_scores = [{'A': 1, 'B': 2, 'C': 3, 'D': 4}]
        framework = detect_framework_structure(generic_scores)
        assert framework['framework_type'] == 'unknown'
        assert framework['integrative_wells'] == ['A', 'B']
        assert framework['disintegrative_wells'] == ['C', 'D']
        
        # Test with empty scores
        framework = detect_framework_structure([])
        assert framework == {} 