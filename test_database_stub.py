#!/usr/bin/env python3
"""
Database Logging Stub Test - Debug without expensive API calls
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append('src')

from utils.statistical_logger import StatisticalLogger, RunData, JobData

def create_stub_run_data(run_number: int, job_id: str) -> RunData:
    """Create fake run data for testing"""
    fake_scores = {
        "prosperity": 0.75 + (run_number * 0.02),  # Slight variation
        "liberty": 0.68 + (run_number * 0.01),
        "security": 0.82 - (run_number * 0.01),
        "justice": 0.73 + (run_number * 0.015),
        "civic_duty": 0.79 - (run_number * 0.005),
        "moral_leadership": 0.71 + (run_number * 0.02),
        "unity": 0.77 - (run_number * 0.01),
        "tradition": 0.64 + (run_number * 0.025)
    }
    
    fake_narrative_position = {
        "x": 0.15 + (run_number * 0.01),
        "y": 0.23 - (run_number * 0.005)
    }
    
    fake_analysis = f"This is a detailed fake analysis for run {run_number}. The speaker demonstrates strong civic virtue themes with particular emphasis on prosperity and security. The narrative gravitates toward {fake_narrative_position['x']:.3f}, {fake_narrative_position['y']:.3f} in the elliptical space."
    
    fake_raw_response = f"""
{{
  "prosperity": {fake_scores['prosperity']:.3f},
  "liberty": {fake_scores['liberty']:.3f},
  "security": {fake_scores['security']:.3f},
  "justice": {fake_scores['justice']:.3f},
  "civic_duty": {fake_scores['civic_duty']:.3f},
  "moral_leadership": {fake_scores['moral_leadership']:.3f},
  "unity": {fake_scores['unity']:.3f},
  "tradition": {fake_scores['tradition']:.3f},
  "analysis": "{fake_analysis}"
}}
"""
    
    fake_raw_prompt = f"Analyze this text for civic virtue themes using the following framework... [FAKE PROMPT FOR RUN {run_number}]"
    
    return RunData(
        run_id=f"{job_id}_run_{run_number}",
        job_id=job_id,
        run_number=run_number,
        well_scores=fake_scores,
        narrative_position=fake_narrative_position,
        analysis_text=fake_analysis,
        model_name="claude-3-5-sonnet",
        framework="civic_virtue",
        timestamp=datetime.now().isoformat(),
        cost=0.0167,  # Fake cost
        duration_seconds=6.2 + (run_number * 0.3),  # Slight variation
        success=True,
        error_message=None,
        raw_prompt=fake_raw_prompt,
        raw_response=fake_raw_response,
        input_text="My fellow Americans, we gather here today to address the challenges facing our great nation... [FAKE SPEECH TEXT]",
        model_parameters={"temperature": 0.3, "max_tokens": 2000},
        api_metadata={"request_id": f"fake_req_{run_number}", "model_version": "claude-3-5-sonnet-20241022"}
    )

def create_stub_job_data(job_id: str, run_count: int = 5) -> JobData:
    """Create fake job data for testing"""
    fake_mean_scores = {
        "prosperity": 0.751,
        "liberty": 0.684,
        "security": 0.814,
        "justice": 0.738,
        "civic_duty": 0.787,
        "moral_leadership": 0.721,
        "unity": 0.764,
        "tradition": 0.652
    }
    
    fake_variance_stats = {
        "total_variance": 0.0234,
        "max_individual_variance": 0.0089,
        "well_count": 8,
        "threshold_category": "minimal"
    }
    
    return JobData(
        job_id=job_id,
        speaker="Barack Obama",
        speech_type="Inaugural Address",
        text_length=13897,
        framework="civic_virtue",
        model_name="claude-3-5-sonnet",
        total_runs=run_count,
        successful_runs=run_count,
        total_cost=0.0835,
        total_duration_seconds=32.4,
        timestamp=datetime.now().isoformat(),
        mean_scores=fake_mean_scores,
        variance_stats=fake_variance_stats,
        threshold_category="minimal"
    )

def test_database_logging_stub():
    """Test database logging with stub data"""
    print("🔧 DATABASE LOGGING STUB TEST")
    print("=" * 50)
    
    # Initialize logger
    logger = StatisticalLogger()
    print(f"✅ Database initialized: {'PostgreSQL' if logger.use_postgresql else 'SQLite'}")
    
    # Create fake job
    job_id = f"stub_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📋 Creating stub job: {job_id}")
    
    # Test logging job data FIRST (foreign key constraint)
    print("\n📊 Testing job data logging...")
    job_data = create_stub_job_data(job_id, 5)
    try:
        logger.log_job(job_data)
        print("   ✅ Job data logged successfully")
    except Exception as e:
        print(f"   ❌ Job logging failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test logging individual runs (AFTER job exists)
    print("\n🔄 Testing individual run logging...")
    for i in range(1, 6):  # 5 fake runs
        run_data = create_stub_run_data(i, job_id)
        print(f"   Run {i}: cost=${run_data.cost:.4f}, duration={run_data.duration_seconds:.1f}s")
        
        try:
            logger.log_run(run_data)
            print(f"   ✅ Run {i} logged successfully")
        except Exception as e:
            print(f"   ❌ Run {i} failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Test variance statistics
    print("\n📈 Testing variance statistics logging...")
    fake_well_stats = {
        "prosperity": {"mean": 0.751, "std": 0.0089, "variance": 0.000079},
        "liberty": {"mean": 0.684, "std": 0.0067, "variance": 0.000045},
        "security": {"mean": 0.814, "std": 0.0045, "variance": 0.000020},
        "justice": {"mean": 0.738, "std": 0.0078, "variance": 0.000061},
        "civic_duty": {"mean": 0.787, "std": 0.0034, "variance": 0.000012},
        "moral_leadership": {"mean": 0.721, "std": 0.0089, "variance": 0.000079},
        "unity": {"mean": 0.764, "std": 0.0056, "variance": 0.000031},
        "tradition": {"mean": 0.652, "std": 0.0123, "variance": 0.000151}
    }
    
    fake_framework_info = {
        "integrative_wells": ["prosperity", "liberty", "security", "justice"],
        "disintegrative_wells": ["civic_duty", "moral_leadership", "unity", "tradition"]
    }
    
    try:
        logger.log_variance_statistics(job_id, fake_well_stats, fake_framework_info)
        print("   ✅ Variance statistics logged successfully")
    except Exception as e:
        print(f"   ❌ Variance logging failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test performance metrics
    print("\n⚡ Testing performance metrics logging...")
    try:
        logger.log_performance_metrics(
            job_id=job_id,
            model_name="claude-3-5-sonnet",
            framework="civic_virtue",
            success_rate=1.0,
            avg_cost=0.0167,
            avg_duration=6.48,
            total_variance=0.0234,
            max_variance=0.0089
        )
        print("   ✅ Performance metrics logged successfully")
    except Exception as e:
        print(f"   ❌ Performance logging failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test database querying
    print("\n🔍 Testing database queries...")
    try:
        stats = logger.get_corpus_stats()
        print(f"   Total Runs: {stats.get('total_runs', 0)}")
        print(f"   Total Jobs: {stats.get('total_jobs', 0)}")
        print(f"   Total Cost: ${stats.get('total_cost', 0):.4f}")
        print(f"   Unique Models: {stats.get('unique_models', 0)}")
        print("   ✅ Database queries working")
    except Exception as e:
        print(f"   ❌ Database queries failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 ALL STUB TESTS PASSED!")
    print(f"📋 Job ID for testing: {job_id}")
    return True

if __name__ == "__main__":
    success = test_database_logging_stub()
    if success:
        print("\n✅ Ready for live API testing!")
    else:
        print("\n❌ Fix database issues before proceeding")
        sys.exit(1) 