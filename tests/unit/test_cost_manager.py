import pytest
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.narrative_gravity.utils.cost_manager import CostManager, CostEntry, CostLimits

@pytest.fixture
def temp_cost_files(tmp_path):
    """Fixture to create temporary cost and limit files for testing."""
    cost_file = tmp_path / "costs.json"
    limits_file = tmp_path / "limits.json"
    return str(cost_file), str(limits_file)

@pytest.fixture
def cost_manager(temp_cost_files):
    """Fixture to get a CostManager instance with temporary files."""
    cost_file, limits_file = temp_cost_files
    return CostManager(cost_file=cost_file, limits_file=limits_file)

class TestCostManager:
    """
    Unit tests for the CostManager class.
    """

    # --- Cost Estimation Tests ---
    @pytest.mark.parametrize("provider, model, text, expected_cost", [
        ("openai", "gpt-4o", "This is a test.", 0.0045325), # Corrected expected cost
        ("anthropic", "claude-3.5-sonnet", "A much longer sentence for testing.", 0.004527),
        ("google_ai", "gemini-1.5-pro", "Google model test.", 0.00181),
        ("mistral", "mistral-large", "Mistral test.", 0.007232)
    ])
    def test_estimate_cost(self, cost_manager, provider, model, text, expected_cost):
        """Tests cost estimation for various models."""
        cost, _, _ = cost_manager.estimate_cost(text, provider, model)
        assert pytest.approx(cost, rel=1e-2) == expected_cost

    def test_estimate_cost_for_unknown_model(self, cost_manager):
        """Tests fallback estimation for an unknown model."""
        cost, _, _ = cost_manager.estimate_cost("test", "unknown_provider", "unknown_model")
        # Correctly rounded value
        assert cost == 0.004505

    # --- Limit Checking Tests ---
    def test_check_limits_before_request_within_limits(self, cost_manager):
        """Tests that a request within all limits is approved."""
        is_allowed, reason = cost_manager.check_limits_before_request(0.01)
        assert is_allowed == True
        assert "Within limits" in reason

    def test_check_limits_exceeds_single_request_limit(self, cost_manager):
        """Tests that a request is denied if it exceeds the single request limit."""
        cost_manager.limits.single_request_limit = 0.05
        is_allowed, reason = cost_manager.check_limits_before_request(0.10)
        assert is_allowed == False
        assert "exceeds single request limit" in reason

    def test_check_limits_exceeds_daily_limit(self, cost_manager):
        """Tests that a request is denied if it exceeds the daily limit."""
        cost_manager.limits.daily_limit = 0.50
        # Add a recent cost entry
        cost_manager.costs.append(CostEntry(
            timestamp=datetime.now().isoformat(), provider="openai", model="gpt-4o",
            cost=0.49, tokens_input=0, tokens_output=0, request_type="analysis"
        ))
        is_allowed, reason = cost_manager.check_limits_before_request(0.02)
        assert is_allowed == False
        assert "exceed daily limit" in reason

    # --- Spending Summary Tests ---
    def test_get_spending_summary(self, cost_manager):
        """Tests the calculation of the spending summary."""
        now = datetime.now()
        cost_manager.costs = [
            CostEntry(timestamp=(now - timedelta(hours=1)).isoformat(), cost=0.10, provider="p", model="m", tokens_input=0, tokens_output=0, request_type="r"),
            CostEntry(timestamp=(now - timedelta(days=2)).isoformat(), cost=0.20, provider="p", model="m", tokens_input=0, tokens_output=0, request_type="r"),
            CostEntry(timestamp=(now - timedelta(days=8)).isoformat(), cost=0.40, provider="p", model="m", tokens_input=0, tokens_output=0, request_type="r"),
        ]
        
        summary = cost_manager.get_spending_summary()
        
        assert summary['daily'] == pytest.approx(0.10)
        assert summary['weekly'] == pytest.approx(0.30)
        assert summary['monthly'] == pytest.approx(0.70)
        assert "usage_by_provider" in summary
        assert "usage_by_model" in summary

    # --- Cost Addition and Saving ---
    def test_add_cost_and_save(self, cost_manager, temp_cost_files):
        """Tests that adding a cost updates the internal list and saves correctly."""
        cost_file, _ = temp_cost_files
        
        cost_manager.add_cost(
            provider="openai", model="gpt-4o", cost=0.01,
            tokens_input=1000, tokens_output=200
        )
        
        assert len(cost_manager.costs) == 1
        assert cost_manager.costs[0].cost == 0.01
        
        # Check if the file was written correctly
        with open(cost_file, 'r') as f:
            saved_data = json.load(f)
        
        assert len(saved_data) == 1
        assert saved_data[0]['model'] == 'gpt-4o' 