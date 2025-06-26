import pytest
import numpy as np
from src.reboot.analysis.statistical_methods import StatisticalMethodRegistry, BaseAnalyzer, GeometricSimilarityAnalyzer
from src.reboot.database.models import AnalysisResultV2

# Mock AnalysisResultV2 for testing purposes
class MockAnalysisResult:
    def __init__(self, x, y, scores_json="{}"):
        self.centroid_x = x
        self.centroid_y = y
        self.raw_scores = scores_json
        self.id = "mock_id" # for error messages

def test_registry_initialization():
    """Tests that the StatisticalMethodRegistry can be initialized."""
    registry = StatisticalMethodRegistry()
    assert registry is not None
    assert len(registry.methods) > 0

def test_retrieve_known_analyzer():
    """Tests that the registry can retrieve a known analyzer instance."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("geometric_similarity")
    assert isinstance(analyzer, BaseAnalyzer)
    assert isinstance(analyzer, GeometricSimilarityAnalyzer)

def test_retrieve_unknown_analyzer_raises_error():
    """Tests that requesting an unknown analyzer raises a ValueError."""
    registry = StatisticalMethodRegistry()
    with pytest.raises(ValueError) as excinfo:
        registry.get_analyzer("non_existent_analyzer")
    assert "Unknown statistical method: non_existent_analyzer" in str(excinfo.value)

def test_dimensional_correlation_perfect_positive():
    """Tests perfect positive correlation (r=1.0)."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("dimensional_correlation")
    
    scores1 = '{"care": 0.8, "fairness": 0.7}'
    scores2 = '{"care": 0.8, "fairness": 0.7}'
    data = [MockAnalysisResult(0,0, scores1), MockAnalysisResult(0,0, scores2)]
    
    result = analyzer.analyze(data)
    
    assert "error" not in result
    # Correlation of a variable with itself is 1. Diagonals are 1.
    # Off-diagonals are also 1 since the data is identical.
    expected_matrix = [[1.0, 1.0], [1.0, 1.0]]
    assert np.array(result["correlation_matrix"]) == pytest.approx(np.array(expected_matrix))

def test_dimensional_correlation_perfect_negative():
    """Tests perfect negative correlation (r=-1.0)."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("dimensional_correlation")
    
    scores1 = '{"d1": 1, "d2": 2, "d3": 3}'
    scores2 = '{"d1": -1, "d2": -2, "d3": -3}'
    data = [MockAnalysisResult(0,0, scores1), MockAnalysisResult(0,0, scores2)]
    
    result = analyzer.analyze(data)
    
    assert "error" not in result
    expected_matrix = [[1.0, -1.0], [-1.0, 1.0]]
    assert np.array(result["correlation_matrix"]) == pytest.approx(np.array(expected_matrix))

def test_dimensional_correlation_mixed_and_missing_dims():
    """Tests correlation with multiple models and missing dimensions."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("dimensional_correlation")
    
    # Model 2 is missing 'd3', Model 3 is anti-correlated on d1,d2
    scores1 = '{"d1": 1, "d2": 2, "d3": 8}'
    scores2 = '{"d1": 1, "d2": 2}'
    scores3 = '{"d1": -1, "d2": -2, "d3": 8}'
    data = [
        MockAnalysisResult(0,0, scores1), 
        MockAnalysisResult(0,0, scores2),
        MockAnalysisResult(0,0, scores3)
    ]
    
    result = analyzer.analyze(data)
    
    # With new logic:
    # corr(m1, m2) on shared dims (d1,d2) is 1.0 because they are identical.
    # corr(m1, m3) will be < 1 because of d3 agreement.
    # corr(m2, m3) will be -1.0 because it only compares d1,d2 where they are anti-correlated.
    assert "error" not in result
    matrix = np.array(result["correlation_matrix"])
    assert matrix[0, 1] == pytest.approx(1.0) # m1 vs m2 on shared dims -> identical -> 1.0
    assert matrix[0, 2] > 0 # m1 vs m3 is positive due to strong agreement on d3
    assert matrix[1, 2] == pytest.approx(-1.0) # m2 vs m3 on shared dims -> anti-correlated -> -1.0

def test_dimensional_correlation_insufficient_data():
    """Tests error handling for insufficient data."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("dimensional_correlation")
    result = analyzer.analyze([MockAnalysisResult(0,0)])
    assert "error" in result

def test_dimensional_correlation_bad_json():
    """Tests error handling for malformed JSON in scores."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("dimensional_correlation")
    scores1 = '{"d1": 1}'
    scores2 = '{"d1": 2' # Malformed
    data = [MockAnalysisResult(0,0, scores1), MockAnalysisResult(0,0, scores2)]
    result = analyzer.analyze(data)
    assert "error" in result

def test_geometric_similarity_two_points():
    """Tests the geometric similarity calculation for two simple points."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("geometric_similarity")
    
    # Points are (0,0) and (3,4), distance should be 5
    data = [MockAnalysisResult(0, 0, "{}"), MockAnalysisResult(3, 4, "{}")]
    
    result = analyzer.analyze(data)
    
    assert "error" not in result
    assert len(result["distances"]) == 1
    assert result["distances"][0] == pytest.approx(5.0)
    assert result["mean_distance"] == pytest.approx(5.0)
    assert result["max_distance"] == pytest.approx(5.0)
    assert result["variance"] == pytest.approx(0.0)

def test_geometric_similarity_multiple_points():
    """Tests the geometric similarity calculation for multiple points."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("geometric_similarity")
    
    # Points: (0,0), (3,4), (6,0)
    # Distances: d(0,1)=5, d(0,2)=6, d(1,2)=5
    data = [
        MockAnalysisResult(0, 0, "{}"),
        MockAnalysisResult(3, 4, "{}"),
        MockAnalysisResult(6, 0, "{}")
    ]
    
    result = analyzer.analyze(data)
    
    assert "error" not in result
    assert len(result["distances"]) == 3
    assert result["distances"] == pytest.approx([5.0, 6.0, 5.0])
    assert result["mean_distance"] == pytest.approx(5.33333)
    assert result["max_distance"] == pytest.approx(6.0)
    assert result["variance"] == pytest.approx(0.22222, abs=1e-5)

def test_geometric_similarity_insufficient_data():
    """Tests that the analyzer handles cases with less than two data points."""
    registry = StatisticalMethodRegistry()
    analyzer = registry.get_analyzer("geometric_similarity")
    
    # Test with one point
    data_one = [MockAnalysisResult(0, 0, "{}")]
    result_one = analyzer.analyze(data_one)
    assert "error" in result_one
    
    # Test with zero points
    data_zero = []
    result_zero = analyzer.analyze(data_zero)
    assert "error" in result_zero 