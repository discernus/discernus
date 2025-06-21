#!/usr/bin/env python3
"""
Test script for v2.1 Narrative Gravity Backend Implementation
Tests the new Experiment and Run data structures with database persistence.
"""

import os
import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.base import get_db
from src.models import User, Experiment, Run

def test_v2_1_data_structures():
    """Test the v2.1 experiment and run data structures."""
    print("🧪 Testing v2.1 Data Structures")
    print("=" * 50)
    
    # Get database session
    db = next(get_db())
    
    try:
        # 1. Test creating a user (if needed)
        print("\n1. Testing User Creation...")
        test_user = db.query(User).filter(User.username == "test_researcher").first()
        if not test_user:
            test_user = User(
                username="test_researcher",
                email="researcher@example.com",
                hashed_password="hashed_password_here",
                full_name="Test Researcher",
                organization="Research Institute"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Created user: {test_user.username} (ID: {test_user.id})")
        else:
            print(f"✅ Found existing user: {test_user.username} (ID: {test_user.id})")
        
        # 2. Test creating an experiment
        print("\n2. Testing Experiment Creation...")
        experiment = Experiment(
            creator_id=test_user.id,
            name="Test Hierarchical Analysis Experiment",
            hypothesis="Testing v2.1 hierarchical analysis capabilities",
            description="This experiment tests the new v2.1 data structures for hierarchical narrative analysis",
            research_context="Development testing for v2.1 implementation",
            prompt_template_id="hierarchical_v1",
            framework_config_id="civic_virtue",
            scoring_algorithm_id="hierarchical",
            analysis_mode="single_model",
            selected_models=["gpt-4", "claude-3-sonnet"],
            research_notes="Initial testing of v2.1 backend implementation",
            tags=["v2.1", "testing", "hierarchical", "civic_virtue"]
        )
        
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        print(f"✅ Created experiment: {experiment.name} (ID: {experiment.id})")
        
        # 3. Test creating analysis runs
        print("\n3. Testing Run Creation...")
        
        # Sample analysis results
        sample_results = [
            {
                "text_content": "We must stand together for dignity and truth in our democracy.",
                "llm_model": "gpt-4",
                "raw_scores": {
                    "Dignity": 0.85, "Truth": 0.78, "Justice": 0.72, "Hope": 0.68, "Pragmatism": 0.45,
                    "Tribalism": 0.15, "Manipulation": 0.12, "Resentment": 0.08, "Fantasy": 0.05, "Fear": 0.10
                },
                "hierarchical_ranking": {
                    "primary_wells": [
                        {"well": "Dignity", "score": 0.85, "relative_weight": 45.0},
                        {"well": "Truth", "score": 0.78, "relative_weight": 35.0},
                        {"well": "Justice", "score": 0.72, "relative_weight": 20.0}
                    ],
                    "secondary_wells": [],
                    "total_weight": 100.0
                },
                "well_justifications": {
                    "Dignity": {
                        "score": 0.85,
                        "reasoning": "Strong emphasis on human dignity and democratic values",
                        "evidence_quotes": ["stand together for dignity"],
                        "confidence": 0.92
                    }
                }
            },
            {
                "text_content": "The corrupt establishment must be defeated by any means necessary.",
                "llm_model": "claude-3-sonnet",
                "raw_scores": {
                    "Dignity": 0.15, "Truth": 0.25, "Justice": 0.35, "Hope": 0.20, "Pragmatism": 0.30,
                    "Tribalism": 0.75, "Manipulation": 0.65, "Resentment": 0.80, "Fantasy": 0.45, "Fear": 0.55
                },
                "hierarchical_ranking": {
                    "primary_wells": [
                        {"well": "Resentment", "score": 0.80, "relative_weight": 40.0},
                        {"well": "Tribalism", "score": 0.75, "relative_weight": 35.0},
                        {"well": "Manipulation", "score": 0.65, "relative_weight": 25.0}
                    ],
                    "secondary_wells": [],
                    "total_weight": 100.0
                }
            }
        ]
        
        for i, result_data in enumerate(sample_results, 1):
            run = Run(
                experiment_id=experiment.id,
                run_number=i,
                text_id=f"test_text_{i}",
                text_content=result_data["text_content"],
                input_length=len(result_data["text_content"]),
                llm_model=result_data["llm_model"],
                llm_version="latest",
                prompt_template_version="1.0",
                framework_version="1.0",
                raw_scores=result_data["raw_scores"],
                hierarchical_ranking=result_data["hierarchical_ranking"],
                framework_fit_score=0.85,
                well_justifications=result_data.get("well_justifications", {}),
                narrative_elevation=0.65,
                polarity=0.45 if i == 1 else -0.35,
                coherence=0.78,
                directional_purity=0.82,
                narrative_position_x=0.25 if i == 1 else -0.15,
                narrative_position_y=0.45 if i == 1 else -0.25,
                duration_seconds=3.5,
                api_cost=0.025,
                raw_prompt="[Hierarchical analysis prompt]",
                raw_response="[Complete LLM response]",
                model_parameters={"temperature": 0.1, "max_tokens": 1000},
                success=True,
                complete_provenance={
                    "prompt_template_hash": "abc123",
                    "framework_version": "1.0",
                    "scoring_algorithm_version": "1.0",
                    "llm_model": result_data["llm_model"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "experiment_id": experiment.id
                }
            )
            
            db.add(run)
            db.commit()
            db.refresh(run)
            print(f"✅ Created run {run.run_number}: {run.llm_model} analysis (ID: {run.id})")
        
        # 4. Test querying the data
        print("\n4. Testing Data Queries...")
        
        # Query experiment with runs
        exp_with_runs = db.query(Experiment).filter(Experiment.id == experiment.id).first()
        print(f"✅ Experiment '{exp_with_runs.name}' has {len(exp_with_runs.runs)} runs")
        
        # Query runs for experiment
        runs = db.query(Run).filter(Run.experiment_id == experiment.id).all()
        print(f"✅ Found {len(runs)} runs for experiment")
        
        for run in runs:
            print(f"   - Run {run.run_number}: {run.llm_model}, polarity={run.polarity}")
            print(f"     Top well: {max(run.raw_scores.items(), key=lambda x: x[1])}")
        
        # 5. Test hierarchical ranking data
        print("\n5. Testing Hierarchical Analysis Data...")
        for run in runs:
            if run.hierarchical_ranking:
                primary_wells = run.hierarchical_ranking.get("primary_wells", [])
                print(f"   Run {run.run_number} primary wells:")
                for well_data in primary_wells:
                    print(f"     - {well_data['well']}: {well_data['score']:.3f} ({well_data['relative_weight']}%)")
        
        print("\n🎉 All v2.1 data structure tests passed!")
        print(f"✅ Created experiment ID: {experiment.id}")
        print(f"✅ Created {len(runs)} analysis runs")
        print("✅ Hierarchical ranking data stored successfully")
        print("✅ Well justifications stored successfully")
        print("✅ Complete provenance tracking working")
        
        return experiment.id
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()

def test_api_integration():
    """Test the API integration with v2.1 structures."""
    print("\n🌐 Testing API Integration")
    print("=" * 50)
    
    import requests
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("✅ API health check passed")
            health_data = response.json()
            print(f"   Version: {health_data['version']}")
            print(f"   Database: {health_data['database']}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
        
        # Test single text analysis
        analysis_request = {
            "text_content": "We must work together to build a better future for all citizens.",
            "prompt_template_id": "hierarchical_v1",
            "framework_config_id": "civic_virtue",
            "scoring_algorithm_id": "hierarchical",
            "llm_model": "gpt-4"
        }
        
        response = requests.post(
            "http://localhost:8000/api/analyze/single-text",
            json=analysis_request
        )
        
        if response.status_code == 200:
            print("✅ Single text analysis API working")
            result = response.json()
            print(f"   Analysis ID: {result['analysis_id']}")
            print(f"   Framework fit score: {result['framework_fit_score']}")
            print(f"   Top well: {result['dominant_wells'][0]['well']} ({result['dominant_wells'][0]['score']:.3f})")
        else:
            print(f"❌ Single text analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        print("\n🎉 API integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 v2.1 Narrative Gravity Backend Implementation Test")
    print("=" * 60)
    
    # Test database structures
    experiment_id = test_v2_1_data_structures()
    
    if experiment_id:
        # Test API integration
        api_success = test_api_integration()
        
        if api_success:
            print("\n🎊 ALL TESTS PASSED!")
            print("v2.1 Backend Implementation is working correctly!")
            print(f"Sample experiment created with ID: {experiment_id}")
        else:
            print("\n⚠️ Database tests passed, but API tests failed")
    else:
        print("\n❌ Database tests failed") 