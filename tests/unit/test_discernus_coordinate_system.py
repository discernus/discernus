import pytest
import numpy as np
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.coordinate_engine import DiscernusCoordinateEngine


@pytest.fixture
def analyzer():
    """Returns a DiscernusCoordinateEngine instance with default config."""
    # Using default configuration to make the test self-contained.
    return DiscernusCoordinateEngine()


class TestDiscernusCoordinateSystemMath:
    """
    Unit tests for the core mathematical functions of the Discernus Coordinate System.
    
    Tests the enhanced algorithms including dominance amplification and adaptive scaling.
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

    def test_narrative_position_with_single_anchor(self, analyzer):
        """
        Tests the pull from a single anchor with enhanced algorithms.
        
        With enhanced algorithms (dominance amplification + adaptive scaling),
        a single anchor with maximum score will not pull exactly to the anchor position
        but will be scaled according to the new algorithms.
        """
        # Test with the default hope anchor at 0 degrees (right side)
        anchor_scores = {'hope': 1.0}
        x, y = analyzer.calculate_narrative_position(anchor_scores)
        
        # With enhanced algorithms:
        # 1. Dominance amplification: 1.0 -> 1.1 (since 1.0 > 0.7)
        # 2. Adaptive scaling: applies factor between 0.65-0.95
        # Result should be scaled down from the anchor position
        anchor_x, anchor_y = analyzer.circle_point(0)  # (1.0, 0.0)
        
        # The position should be in the same direction but scaled down
        assert x > 0  # Should be positive (toward hope anchor)
        assert np.isclose(y, 0, atol=0.1)  # Should be near zero (hope is at 0 degrees)
        assert 0.65 <= x <= 0.95  # Should be within adaptive scaling range
        
        # Test the scaling behavior
        distance = np.sqrt(x**2 + y**2)
        assert 0.65 <= distance <= 0.95  # Distance should be in adaptive scaling range

    def test_dominance_amplification(self, analyzer):
        """
        Tests the dominance amplification algorithm.
        """
        # Test scores > 0.7 get 1.1x multiplier
        high_score = 0.8
        amplified = analyzer.apply_dominance_amplification(high_score)
        assert np.isclose(amplified, 0.88, atol=1e-10)  # 0.8 * 1.1
        
        # Test maximum score
        max_score = 1.0
        amplified_max = analyzer.apply_dominance_amplification(max_score)
        assert np.isclose(amplified_max, 1.1, atol=1e-10)  # 1.0 * 1.1
        
        # Test scores <= 0.7 are unchanged
        low_score = 0.5
        unchanged = analyzer.apply_dominance_amplification(low_score)
        assert np.isclose(unchanged, 0.5, atol=1e-10)

    def test_adaptive_scaling(self, analyzer):
        """
        Tests the adaptive scaling algorithm.
        """
        # Test with high variance, high mean scores (should get higher scaling)
        high_scores = {'hope': 1.0, 'justice': 0.9, 'fear': 0.1}
        high_scaling = analyzer.calculate_adaptive_scaling(high_scores)
        
        # Test with low variance, low mean scores (should get lower scaling)
        low_scores = {'hope': 0.3, 'justice': 0.2, 'fear': 0.1}
        low_scaling = analyzer.calculate_adaptive_scaling(low_scores)
        
        # High variance/mean should get higher scaling
        assert high_scaling > low_scaling
        
        # Both should be in valid range
        assert 0.65 <= high_scaling <= 0.95
        assert 0.65 <= low_scaling <= 0.95

    def test_narrative_position_with_multiple_anchors(self, analyzer):
        """
        Tests the weighted average calculation with multiple anchors.
        """
        # Test with two anchors at different positions
        anchor_scores = {'hope': 0.5, 'fear': 0.5}  # hope at 0°, fear at 216°
        x, y = analyzer.calculate_narrative_position(anchor_scores)
        
        # Should be somewhere between the two positions, scaled by adaptive scaling
        assert -1.0 <= x <= 1.0
        assert -1.0 <= y <= 1.0
        
        # Distance should be within adaptive scaling range
        distance = np.sqrt(x**2 + y**2)
        assert distance <= 0.95  # Should not exceed maximum scaling

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

    def test_narrative_position_with_balanced_opposing_anchors(self, analyzer):
        """
        Tests the behavior with opposing anchors of equal strength.
        """
        # Use default anchors that are positioned to potentially cancel out
        anchor_scores = {'hope': 1.0, 'fear': 1.0}  # hope at 0°, fear at 216°
        x, y = analyzer.calculate_narrative_position(anchor_scores)
        
        # Should not be at origin since they're not exactly opposite (0° vs 216°)
        # but should be somewhere between them, scaled by adaptive scaling
        assert -1.0 <= x <= 1.0
        assert -1.0 <= y <= 1.0
        
        # Distance should be within adaptive scaling range
        distance = np.sqrt(x**2 + y**2)
        assert distance <= 0.95

    def test_anchor_definitions_exist(self, analyzer):
        """
        Tests that the analyzer has anchor definitions configured.
        """
        assert hasattr(analyzer, 'well_definitions')  # Legacy attribute name for compatibility
        assert len(analyzer.well_definitions) > 0
        
        # Check that each anchor has required properties
        for anchor_name, anchor_info in analyzer.well_definitions.items():
            assert 'angle' in anchor_info
            assert 'type' in anchor_info
            assert isinstance(anchor_info['angle'], (int, float))
            assert anchor_info['type'] in ['integrative', 'disintegrative']

    def test_circle_radius_property(self, analyzer):
        """
        Tests that the circle radius is properly set.
        """
        assert hasattr(analyzer, 'circle_radius')
        assert analyzer.circle_radius == 1.0  # Default unit circle

    def test_weighted_calculation(self, analyzer):
        """
        Tests that anchors with different weights affect the calculation appropriately.
        """
        # Test with anchors that have different weights in the configuration
        if len(analyzer.well_definitions) >= 2:
            anchor_names = list(analyzer.well_definitions.keys())[:2]
            anchor_scores = {anchor_names[0]: 1.0, anchor_names[1]: 1.0}
            
            x, y = analyzer.calculate_narrative_position(anchor_scores)
            
            # Result should be within the adaptive scaling range
            distance = np.sqrt(x**2 + y**2)
            assert distance <= 0.95  # Should not exceed maximum adaptive scaling

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

    def test_enhanced_algorithms_integration(self, analyzer):
        """
        Tests that the enhanced algorithms work together correctly.
        """
        # Test with a high score that should trigger dominance amplification
        test_scores = {'hope': 0.9}  # > 0.7, should get amplified
        x, y = analyzer.calculate_narrative_position(test_scores)
        
        # Should be scaled by both dominance amplification and adaptive scaling
        # Expected: 0.9 * 1.1 (dominance) * adaptive_scaling (0.65-0.95)
        expected_range_min = 0.9 * 1.1 * 0.65  # ~0.64
        expected_range_max = 0.9 * 1.1 * 0.95  # ~0.94
        
        distance = np.sqrt(x**2 + y**2)
        assert expected_range_min <= distance <= expected_range_max, \
            f"Distance {distance:.3f} not in expected range [{expected_range_min:.3f}, {expected_range_max:.3f}]"


if __name__ == "__main__":
    pytest.main([__file__]) 