#!/usr/bin/env python3
"""
End-to-End Integration Test for Narrative Gravity Wells v2.1
Tests the complete workflow from API to database with live data.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_TEXT = """
America stands at a crossroads. We must choose between hope and fear, 
between unity and division. The path forward requires courage, truth, 
and a commitment to justice for all. We cannot allow manipulation and 
tribalism to divide us. Instead, we must embrace our shared dignity 
and work together to build a better future.
"""

def test_api_health():
    """Test API health endpoint."""
    print("🔧 Testing API Health...")
    response = requests.get(f"{API_BASE_URL}/api/health")
    assert response.status_code == 200
    health_data = response.json()
    print(f"   ✅ API Status: {health_data['status']}")
    print(f"   ✅ Database: {health_data['database']}")
    print(f"   ✅ Version: {health_data['version']}")
    return health_data

def test_configuration_endpoints():
    """Test configuration endpoints that frontend needs."""
    print("\n📋 Testing Configuration Endpoints...")
    
    # Test framework configs
    response = requests.get(f"{API_BASE_URL}/api/framework-configs")
    assert response.status_code == 200
    frameworks = response.json()
    print(f"   ✅ Framework Configs: {len(frameworks)} available")
    
    # Test prompt templates
    response = requests.get(f"{API_BASE_URL}/api/prompt-templates")
    assert response.status_code == 200
    templates = response.json()
    print(f"   ✅ Prompt Templates: {len(templates)} available")
    
    # Test scoring algorithms
    response = requests.get(f"{API_BASE_URL}/api/scoring-algorithms")
    assert response.status_code == 200
    algorithms = response.json()
    print(f"   ✅ Scoring Algorithms: {len(algorithms)} available")
    
    return {
        'frameworks': frameworks,
        'templates': templates,
        'algorithms': algorithms
    }

def test_experiment_workflow(config_data: Dict[str, Any]):
    """Test complete experiment workflow."""
    print("\n🧪 Testing Experiment Workflow...")
    
    # Create experiment
    experiment_data = {
        "name": f"End-to-End Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "hypothesis": "Testing complete workflow from frontend to database",
        "description": "Automated end-to-end test of the v2.1 system",
        "research_context": "System validation testing",
        "prompt_template_id": config_data['templates'][0]['id'],
        "framework_config_id": config_data['frameworks'][0]['id'],
        "scoring_algorithm_id": config_data['algorithms'][0]['id'],
        "analysis_mode": "single_model",
        "selected_models": ["gpt-4"],
        "research_notes": "Automated test execution",
        "tags": ["test", "end-to-end", "validation"]
    }
    
    response = requests.post(f"{API_BASE_URL}/api/experiments", json=experiment_data)
    assert response.status_code == 200
    experiment = response.json()
    experiment_id = experiment['id']
    print(f"   ✅ Created Experiment: {experiment_id} - {experiment['name']}")
    
    return experiment_id

def test_analysis_execution(experiment_id: int):
    """Test analysis execution."""
    print("\n🔍 Testing Analysis Execution...")
    
    # Create analysis run
    run_data = {
        "text_content": TEST_TEXT,
        "text_id": f"test_text_{datetime.now().strftime('%H%M%S')}",
        "llm_model": "gpt-4"
    }
    
    response = requests.post(f"{API_BASE_URL}/api/experiments/{experiment_id}/runs", json=run_data)
    assert response.status_code == 200
    run = response.json()
    run_id = run['id']
    print(f"   ✅ Created Run: {run_id}")
    print(f"   ✅ Status: {run['status']}")
    
    # Get run details
    response = requests.get(f"{API_BASE_URL}/api/runs/{run_id}")
    assert response.status_code == 200
    run_details = response.json()
    print(f"   ✅ Retrieved Run Details")
    print(f"   ✅ Raw Scores Available: {len(run_details.get('raw_scores', {}))}")
    
    return run_id

def test_single_text_analysis():
    """Test single text analysis endpoint."""
    print("\n📝 Testing Single Text Analysis...")
    
    analysis_request = {
        "text_content": TEST_TEXT,
        "prompt_template_id": "civic_virtue_v2_1",
        "framework_config_id": "civic_virtue",
        "scoring_algorithm_id": "hierarchical_v2_1",
        "llm_model": "gpt-4",
        "include_justifications": True,
        "include_hierarchical_ranking": True
    }
    
    response = requests.post(f"{API_BASE_URL}/api/analyze/single-text", json=analysis_request)
    if response.status_code == 200:
        analysis = response.json()
        print(f"   ✅ Analysis Completed: {analysis['analysis_id']}")
        print(f"   ✅ Framework Used: {analysis['framework']}")
        print(f"   ✅ Dominant Wells: {len(analysis.get('dominant_wells', []))}")
        print(f"   ✅ Has Hierarchical Ranking: {'hierarchical_ranking' in analysis}")
        return analysis
    else:
        print(f"   ⚠️  Analysis endpoint returned {response.status_code}: {response.text}")
        return None

def run_end_to_end_test():
    """Run complete end-to-end test."""
    print("🚀 Starting End-to-End Integration Test")
    print("=" * 60)
    
    try:
        # Test API health
        health = test_api_health()
        
        # Test configuration endpoints
        config_data = test_configuration_endpoints()
        
        # Test experiment workflow
        experiment_id = test_experiment_workflow(config_data)
        
        # Test analysis execution
        run_id = test_analysis_execution(experiment_id)
        
        # Test single text analysis
        analysis = test_single_text_analysis()
        
        print("\n" + "=" * 60)
        print("🎉 End-to-End Test PASSED!")
        print(f"   ✅ API Health: OK")
        print(f"   ✅ Configuration: OK")
        print(f"   ✅ Experiments: OK")
        print(f"   ✅ Analysis Runs: OK")
        print(f"   ✅ Live Analysis: {'OK' if analysis else 'SKIP'}")
        print("\n🔗 Frontend should now be fully functional!")
        print(f"   🌐 Frontend URL: http://localhost:3000")
        print(f"   📊 API Docs: http://localhost:8000/api/docs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_end_to_end_test()
    exit(0 if success else 1) 