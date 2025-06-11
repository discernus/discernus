#!/usr/bin/env python3
"""
Frontend Integration Test for Narrative Gravity Wells v2.1
Tests the complete frontend-to-API integration with live data.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_frontend_accessibility():
    """Test that the frontend is accessible and serving content."""
    print("🌐 Testing Frontend Accessibility...")
    response = requests.get(FRONTEND_URL)
    assert response.status_code == 200
    assert "Narrative Gravity Wells" in response.text
    print("   ✅ Frontend is accessible and serving content")
    return True

def test_api_endpoints_for_frontend():
    """Test all API endpoints that the frontend depends on."""
    print("\n📡 Testing API Endpoints for Frontend...")
    
    endpoints_to_test = [
        ("/api/health", "Health check"),
        ("/api/framework-configs", "Framework configurations"),
        ("/api/prompt-templates", "Prompt templates"),
        ("/api/scoring-algorithms", "Scoring algorithms"),
        ("/api/experiments", "Experiments list"),
    ]
    
    for endpoint, description in endpoints_to_test:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        assert response.status_code == 200, f"{description} endpoint failed"
        data = response.json()
        assert data is not None, f"{description} returned no data"
        print(f"   ✅ {description}: OK")
    
    return True

def test_experiment_creation_workflow():
    """Test the complete experiment creation workflow that the frontend uses."""
    print("\n🧪 Testing Experiment Creation Workflow...")
    
    # Get configuration data first (like frontend would)
    frameworks = requests.get(f"{API_BASE_URL}/api/framework-configs").json()
    templates = requests.get(f"{API_BASE_URL}/api/prompt-templates").json()
    algorithms = requests.get(f"{API_BASE_URL}/api/scoring-algorithms").json()
    
    # Create experiment with valid configuration
    experiment_data = {
        "name": f"Frontend Integration Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "hypothesis": "Testing frontend-to-API integration",
        "description": "Automated test of frontend experiment creation workflow",
        "research_context": "Frontend integration validation",
        "prompt_template_id": templates[0]['id'],
        "framework_config_id": frameworks[0]['id'],
        "scoring_algorithm_id": algorithms[0]['id'],
        "analysis_mode": "single_model",
        "selected_models": ["gpt-4"],
        "research_notes": "Frontend integration test",
        "tags": ["frontend", "integration", "test"]
    }
    
    response = requests.post(f"{API_BASE_URL}/api/experiments", json=experiment_data)
    assert response.status_code == 200
    experiment = response.json()
    experiment_id = experiment['id']
    print(f"   ✅ Created Experiment: {experiment_id}")
    
    # Test experiment retrieval
    response = requests.get(f"{API_BASE_URL}/api/experiments/{experiment_id}")
    assert response.status_code == 200
    retrieved_experiment = response.json()
    assert retrieved_experiment['id'] == experiment_id
    print(f"   ✅ Retrieved Experiment: {experiment_id}")
    
    return experiment_id

def test_analysis_execution_workflow(experiment_id: int):
    """Test the analysis execution workflow that the frontend uses."""
    print("\n🔍 Testing Analysis Execution Workflow...")
    
    # Create analysis run (like frontend would)
    run_data = {
        "text_content": "This is a test of the frontend integration. We are testing the complete workflow from the React frontend through the FastAPI backend to the PostgreSQL database. This should demonstrate that all components are working together properly.",
        "text_id": f"frontend_test_{datetime.now().strftime('%H%M%S')}",
        "llm_model": "gpt-4"
    }
    
    response = requests.post(f"{API_BASE_URL}/api/experiments/{experiment_id}/runs", json=run_data)
    assert response.status_code == 200
    run = response.json()
    run_id = run['id']
    print(f"   ✅ Created Analysis Run: {run_id}")
    
    # Test run retrieval
    response = requests.get(f"{API_BASE_URL}/api/runs/{run_id}")
    assert response.status_code == 200
    run_details = response.json()
    assert run_details['id'] == run_id
    assert 'raw_scores' in run_details
    assert len(run_details['raw_scores']) > 0
    print(f"   ✅ Retrieved Run Details with {len(run_details['raw_scores'])} scores")
    
    # Test experiment runs list
    response = requests.get(f"{API_BASE_URL}/api/experiments/{experiment_id}/runs")
    assert response.status_code == 200
    runs_list = response.json()
    assert len(runs_list) > 0
    assert any(run['id'] == run_id for run in runs_list)
    print(f"   ✅ Listed Experiment Runs: {len(runs_list)} runs found")
    
    return run_id

def test_single_text_analysis():
    """Test the single text analysis endpoint that the frontend uses."""
    print("\n📝 Testing Single Text Analysis...")
    
    analysis_request = {
        "text_content": "Democracy requires active participation from all citizens. We must work together to build a more just and equitable society for everyone.",
        "prompt_template_id": "civic_virtue_v2_1",
        "framework_config_id": "civic_virtue",
        "scoring_algorithm_id": "hierarchical_v2_1",
        "llm_model": "gpt-4",
        "include_justifications": True,
        "include_hierarchical_ranking": True
    }
    
    response = requests.post(f"{API_BASE_URL}/api/analyze/single-text", json=analysis_request)
    assert response.status_code == 200
    analysis = response.json()
    
    # Validate response structure
    required_fields = [
        'analysis_id', 'text_content', 'framework', 'model',
        'raw_scores', 'hierarchical_ranking', 'well_justifications',
        'calculated_metrics', 'narrative_position', 'framework_fit_score',
        'dominant_wells', 'execution_time'
    ]
    
    for field in required_fields:
        assert field in analysis, f"Missing required field: {field}"
    
    print(f"   ✅ Analysis Completed: {analysis['analysis_id']}")
    print(f"   ✅ Framework: {analysis['framework']}")
    print(f"   ✅ Raw Scores: {len(analysis['raw_scores'])} wells")
    print(f"   ✅ Dominant Wells: {len(analysis['dominant_wells'])}")
    print(f"   ✅ Has Hierarchical Ranking: {'hierarchical_ranking' in analysis}")
    print(f"   ✅ Has Well Justifications: {'well_justifications' in analysis}")
    
    return analysis

def test_data_consistency():
    """Test that data is consistent across different API endpoints."""
    print("\n🔄 Testing Data Consistency...")
    
    # Get experiments list
    experiments_response = requests.get(f"{API_BASE_URL}/api/experiments")
    experiments = experiments_response.json()
    
    if experiments:
        # Test first experiment
        experiment = experiments[0]
        experiment_id = experiment['id']
        
        # Get experiment details
        detail_response = requests.get(f"{API_BASE_URL}/api/experiments/{experiment_id}")
        experiment_detail = detail_response.json()
        
        # Verify consistency
        assert experiment['id'] == experiment_detail['id']
        assert experiment['name'] == experiment_detail['name']
        print(f"   ✅ Experiment data consistency verified")
        
        # Get experiment runs
        runs_response = requests.get(f"{API_BASE_URL}/api/experiments/{experiment_id}/runs")
        runs = runs_response.json()
        
        if runs:
            # Test first run
            run = runs[0]
            run_id = run['id']
            
            # Get run details
            run_detail_response = requests.get(f"{API_BASE_URL}/api/runs/{run_id}")
            run_detail = run_detail_response.json()
            
            # Verify consistency
            assert run['id'] == run_detail['id']
            assert run['experiment_id'] == run_detail['experiment_id']
            print(f"   ✅ Run data consistency verified")
    
    return True

def run_frontend_integration_test():
    """Run complete frontend integration test."""
    print("🚀 Starting Frontend Integration Test")
    print("=" * 60)
    
    try:
        # Test frontend accessibility
        test_frontend_accessibility()
        
        # Test API endpoints
        test_api_endpoints_for_frontend()
        
        # Test experiment workflow
        experiment_id = test_experiment_creation_workflow()
        
        # Test analysis workflow
        run_id = test_analysis_execution_workflow(experiment_id)
        
        # Test single text analysis
        analysis = test_single_text_analysis()
        
        # Test data consistency
        test_data_consistency()
        
        print("\n" + "=" * 60)
        print("🎉 Frontend Integration Test PASSED!")
        print("\n📊 Test Results Summary:")
        print(f"   ✅ Frontend Accessibility: OK")
        print(f"   ✅ API Endpoints: OK")
        print(f"   ✅ Experiment Creation: OK")
        print(f"   ✅ Analysis Execution: OK")
        print(f"   ✅ Single Text Analysis: OK")
        print(f"   ✅ Data Consistency: OK")
        
        print("\n🔗 System Status:")
        print(f"   🌐 Frontend: http://localhost:3000 (READY)")
        print(f"   📡 API: http://localhost:8000 (READY)")
        print(f"   📊 API Docs: http://localhost:8000/api/docs")
        print(f"   🗄️  Database: PostgreSQL (CONNECTED)")
        
        print("\n✨ The frontend is now fully functional with live data!")
        print("   You can now use the React application to:")
        print("   • Create and manage experiments")
        print("   • Execute analysis runs")
        print("   • View results and visualizations")
        print("   • Compare different models and frameworks")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Frontend Integration Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_frontend_integration_test()
    exit(0 if success else 1) 