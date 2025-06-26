import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import json

from src.reboot.api.main import app
from src.reboot.database.session import get_db
from src.reboot.database.models import AnalysisJobV2, AnalysisResultV2

client = TestClient(app)

# --- Mock Data ---
MOCK_ANALYSIS_RESULT_GPT = {
    "scores": {"care": 0.8, "fairness": 0.2},
    "centroid": (0.6, 0.4)
}
MOCK_ANALYSIS_RESULT_CLAUDE = {
    "scores": {"care": 0.7, "fairness": 0.3},
    "centroid": (0.4, 0.4)
}

@pytest.fixture
def mock_experiment_file(tmp_path):
    exp_content = """
    framework:
        name: moral_foundations_theory
    prompt_template: mft_v1
    """
    p = tmp_path / "test_experiment.yaml"
    p.write_text(exp_content)
    return str(p)

@pytest.fixture
def clean_database():
    """Clean up any test data from the database before and after tests."""
    db = next(get_db())
    try:
        # Clean up before test
        db.query(AnalysisResultV2).delete()
        db.query(AnalysisJobV2).delete()
        db.commit()
        yield
        # Clean up after test
        db.query(AnalysisResultV2).delete()
        db.query(AnalysisJobV2).delete()
        db.commit()
    finally:
        db.close()

@patch("src.reboot.api.main._run_single_analysis", new_callable=AsyncMock)
def test_compare_statistical_multi_model_success(mock_run_analysis, mock_experiment_file, clean_database):
    """
    Tests the full multi-model comparison workflow with real database integration.
    """
    # Mock the analysis function
    mock_run_analysis.side_effect = [
        MOCK_ANALYSIS_RESULT_GPT,
        MOCK_ANALYSIS_RESULT_CLAUDE
    ]
    
    request_body = {
        "comparison_type": "multi_model",
        "text": "This is a test text.",
        "models": ["gpt-4o", "claude-3-opus-20240229"],
        "statistical_methods": ["geometric_similarity", "dimensional_correlation"],
        "experiment_file_path": mock_experiment_file
    }
    
    response = client.post("/compare-statistical", json=request_body)
    
    assert response.status_code == 200
    
    res = response.json()
    assert len(res["condition_results"]) == 2
    assert res["condition_results"][0]["condition_identifier"] == "gpt-4o"
    assert res["condition_results"][0]["centroid"] == [0.6, 0.4]
    assert res["condition_results"][1]["condition_identifier"] == "claude-3-opus-20240229"
    assert res["condition_results"][1]["centroid"] == [0.4, 0.4]
    
    assert "geometric_similarity" in res["statistical_metrics"]
    assert "dimensional_correlation" in res["statistical_metrics"]
    
    # Verify the statistical methods returned results
    geo_metrics = res["statistical_metrics"]["geometric_similarity"]
    assert "mean_distance" in geo_metrics
    assert isinstance(geo_metrics["mean_distance"], (int, float))
    
    corr_metrics = res["statistical_metrics"]["dimensional_correlation"]
    assert "correlation_matrix" in corr_metrics
    assert isinstance(corr_metrics["correlation_matrix"], list)
    
    # Verify data was saved to database
    db = next(get_db())
    try:
        jobs = db.query(AnalysisJobV2).all()
        assert len(jobs) == 1
        
        results = db.query(AnalysisResultV2).all()
        assert len(results) == 2
        
        # Verify the results are linked to the job
        job = jobs[0]
        for result in results:
            assert result.job_id == job.id
        
        # Verify job status was updated to complete
        assert job.status == "COMPLETE"
    finally:
        db.close()

def test_compare_statistical_unsupported_type(mock_experiment_file):
    """
    Tests that an unsupported comparison type returns an error.
    """
    request_body = {
        "comparison_type": "multi_user",
        "text": "A test",
        "models": ["gpt-4o"],
        "experiment_file_path": mock_experiment_file
    }
    response = client.post("/compare-statistical", json=request_body)
    assert response.status_code == 400
    assert "not yet supported" in response.json()["detail"]

def test_compare_statistical_bad_request():
    """
    Tests that the endpoint returns a 422 Unprocessable Entity for a malformed request.
    """
    request_body = {
        "text": "This is a test text.",
        "models": ["gpt-4o", "claude-3-opus-20240229"]
    }
    response = client.post("/compare-statistical", json=request_body)
    assert response.status_code == 422

def test_compare_statistical_multi_model_missing_params(mock_experiment_file):
    """
    Tests that multi_model comparison fails when required parameters are missing.
    """
    request_body = {
        "comparison_type": "multi_model",
        "text": "This is a test text.",
        # Missing models parameter
        "experiment_file_path": mock_experiment_file
    }
    response = client.post("/compare-statistical", json=request_body)
    assert response.status_code == 400
    assert "Multi-model comparison requires" in response.json()["detail"] 