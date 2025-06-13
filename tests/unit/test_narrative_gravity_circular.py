import pytest
import numpy as np
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular


@pytest.fixture
def analyzer():
    """Returns a NarrativeGravityWellsCircular instance with default config."""
    # Using a non-existent config directory forces the class to use its default
    # configuration, making the test self-contained.
    return NarrativeGravityWellsCircular(config_dir="non_existent_dir_to_force_defaults")


class TestNarrativeGravityCircularMath:
    """
    Unit tests for the core mathematical functions of the Narrative Gravity circular coordinate model.
    """

    def test_circle_point_calculation(self, analyzer):
        """
        Tests the calculation of points on the circle boundary at key angles.
        """
        # Top point (90 degrees)
        x, y = analyzer.circle_point(90)
        assert np.isclose(x, 0, atol=1e-10)
        assert np.isclose(y, 1.0)

        # Right point (0 degrees)
        x, y = analyzer.circle_point(0)
        assert np.isclose(x, 1.0)
        assert np.isclose(y, 0, atol=1e-10)

        # Bottom point (270 degrees)
        x, y = analyzer.circle_point(270)
        assert np.isclose(x, 0, atol=1e-10)
        assert np.isclose(y, -1.0)

        # Left point (180 degrees)
        x, y = analyzer.circle_point(180)
        assert np.isclose(x, -1.0)
        assert np.isclose(y, 0, atol=1e-10)

    def test_narrative_position_with_single_well(self, analyzer):
        """
        Tests the pull from a single well. A well with maximum score should
        pull the narrative position to the well's location.
        """
        # Test with the default hope well at 0 degrees (right side)
        well_scores = {'hope': 1.0}
        x, y = analyzer.calculate_narrative_position(well_scores)
        
        # With default configuration, hope is at 0 degrees with weight 1.0
        expected_x, expected_y = analyzer.circle_point(0)
        assert np.isclose(x, expected_x)
        assert np.isclose(y, expected_y)

    def test_narrative_position_with_multiple_wells(self, analyzer):
        """
        Tests the weighted average calculation with multiple wells.
        """
        # Test with two wells at opposite positions
        well_scores = {'hope': 0.5, 'fear': 0.5}  # hope at 0°, fear at 216°
        x, y = analyzer.calculate_narrative_position(well_scores)
        
        # Should be somewhere between the two positions
        assert -1.0 <= x <= 1.0
        assert -1.0 <= y <= 1.0

    def test_narrative_position_with_no_scores(self, analyzer):
        """
        Tests that the narrative position is at the origin (0,0) when there
        are no scores or all scores are zero.
        """
        empty_scores = {}
        x, y = analyzer.calculate_narrative_position(empty_scores)
        assert x == 0.0 and y == 0.0

        zero_scores = {'hope': 0.0, 'fear': 0.0}
        x, y = analyzer.calculate_narrative_position(zero_scores)
        assert x == 0.0 and y == 0.0

    def test_narrative_position_with_balanced_opposing_wells(self, analyzer):
        """
        Tests the behavior with opposing wells of equal strength.
        """
        # Use default wells that are positioned to potentially cancel out
        well_scores = {'hope': 1.0, 'fear': 1.0}  # hope at 0°, fear at 216°
        x, y = analyzer.calculate_narrative_position(well_scores)
        
        # Should not be at origin since they're not exactly opposite (0° vs 216°)
        # but should be somewhere between them
        assert -1.0 <= x <= 1.0
        assert -1.0 <= y <= 1.0

    def test_well_definitions_exist(self, analyzer):
        """
        Tests that the analyzer has well definitions configured.
        """
        assert hasattr(analyzer, 'well_definitions')
        assert len(analyzer.well_definitions) > 0
        
        # Check that each well has required properties
        for well_name, well_info in analyzer.well_definitions.items():
            assert 'angle' in well_info
            assert 'type' in well_info
            assert isinstance(well_info['angle'], (int, float))
            assert well_info['type'] in ['integrative', 'disintegrative']

    def test_circle_radius_property(self, analyzer):
        """
        Tests that the circle radius is properly set.
        """
        assert hasattr(analyzer, 'circle_radius')
        assert analyzer.circle_radius == 1.0  # Default unit circle

    def test_weighted_calculation(self, analyzer):
        """
        Tests that wells with different weights affect the calculation appropriately.
        """
        # Test with wells that have different weights in the configuration
        if len(analyzer.well_definitions) >= 2:
            well_names = list(analyzer.well_definitions.keys())[:2]
            well_scores = {well_names[0]: 1.0, well_names[1]: 1.0}
            
            x, y = analyzer.calculate_narrative_position(well_scores)
            
            # Result should be within the unit circle
            distance = np.sqrt(x**2 + y**2)
            assert distance <= 1.0  # Should be within or on the unit circle

    def test_angle_range_handling(self, analyzer):
        """
        Tests that the system properly handles the full 360-degree range.
        """
        # Test points at various angles
        test_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        
        for angle in test_angles:
            x, y = analyzer.circle_point(angle)
            
            # Check that the point is on the unit circle
            distance = np.sqrt(x**2 + y**2)
            assert np.isclose(distance, 1.0), f"Point at {angle}° not on unit circle: ({x}, {y}), distance={distance}"
            
            # Check angle calculation
            calculated_angle = np.degrees(np.arctan2(y, x)) % 360
            expected_angle = angle % 360
            
            # Handle the case where angles might be equivalent (e.g., 0° and 360°)
            angle_diff = abs(calculated_angle - expected_angle)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
                
            assert angle_diff < 1e-10, f"Angle mismatch: expected {expected_angle}°, got {calculated_angle}°"

if __name__ == "__main__":
    pytest.main([__file__]) 