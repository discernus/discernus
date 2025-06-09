import pytest
import numpy as np
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.narrative_gravity import engine


@pytest.fixture
def analyzer():
    """Returns a NarrativeGravityWellsElliptical instance with default config."""
    # Using a non-existent config directory forces the class to use its default
    # configuration, making the test self-contained.
    return engine.NarrativeGravityWellsElliptical(config_dir="non_existent_dir_to_force_defaults")


class TestNarrativeGravityEllipticalMath:
    """
    Unit tests for the core mathematical functions of the Narrative Gravity model.
    """

    def test_ellipse_point_calculation(self, analyzer):
        """
        Tests the calculation of points on the ellipse boundary at key angles.
        """
        # Top point (90 degrees)
        x, y = analyzer.ellipse_point(90)
        assert np.isclose(x, 0)
        assert np.isclose(y, 1.0)

        # Right point (0 degrees)
        x, y = analyzer.ellipse_point(0)
        assert np.isclose(x, 0.7)
        assert np.isclose(y, 0)

        # Bottom point (270 degrees)
        x, y = analyzer.ellipse_point(270)
        assert np.isclose(x, 0)
        assert np.isclose(y, -1.0)

        # Left point (180 degrees)
        x, y = analyzer.ellipse_point(180)
        assert np.isclose(x, -0.7)
        assert np.isclose(y, 0)

    def test_narrative_position_with_single_integrative_well(self, analyzer):
        """
        Tests the pull from a single integrative well. 'Dignity' at the top
        of the ellipse should pull the narrative position straight up.
        """
        well_scores = {'Dignity': 10.0}
        x, y = analyzer.calculate_narrative_position(well_scores)
        
        # Expected y is 0.8 (due to 0.8 scaling factor)
        assert np.isclose(x, 0)
        assert np.isclose(y, 0.8)

    def test_narrative_position_with_single_disintegrative_well(self, analyzer):
        """
        Tests the pull from a single disintegrative well. 'Tribalism' at the
        bottom of the ellipse should pull the narrative position straight down.
        """
        well_scores = {'Tribalism': 10.0}
        x, y = analyzer.calculate_narrative_position(well_scores)

        # Expected y is -0.8 (due to 0.8 scaling factor)
        assert np.isclose(x, 0)
        assert y < 0
        assert np.isclose(y, -0.8)

    def test_narrative_position_with_no_scores(self, analyzer):
        """
        Tests that the narrative position is at the origin (0,0) when there
        are no scores or all scores are zero.
        """
        empty_scores = {}
        x, y = analyzer.calculate_narrative_position(empty_scores)
        assert x == 0.0 and y == 0.0

        zero_scores = {'Dignity': 0.0, 'Tribalism': 0.0}
        x, y = analyzer.calculate_narrative_position(zero_scores)
        assert x == 0.0 and y == 0.0

    def test_narrative_position_with_balanced_opposing_wells(self, analyzer):
        """
        Tests that equal scores on directly opposing wells should cancel each
        other out, resulting in a position at the origin.
        """
        well_scores = {'Dignity': 10.0, 'Tribalism': 10.0}
        x, y = analyzer.calculate_narrative_position(well_scores)
        
        assert np.isclose(x, 0)
        assert np.isclose(y, 0)

    def test_calculate_elliptical_distance(self, analyzer):
        """
        Tests the distance calculation which uses elliptical geometry, not
        simple Euclidean distance.
        """
        pos_a = (0.0, 0.0)
        pos_b = (3.0, 4.0)
        
        # The formula is sqrt(((x_a - x_b)^2 / b^2) + ((y_a - y_b)^2 / a^2))
        # From default config: a=1.0, b=0.7
        expected_distance = np.sqrt((3.0**2 / analyzer.ellipse_b**2) + (4.0**2 / analyzer.ellipse_a**2))
        actual_distance = analyzer.calculate_elliptical_distance(pos_a, pos_b)
        
        assert np.isclose(actual_distance, expected_distance)