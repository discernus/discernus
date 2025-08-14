#!/usr/bin/env python3
"""
Direct test of v8.0 pipeline bypassing CLI validation
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Volumes/code/discernus-epic-401')

from discernus.core.thin_orchestrator import ThinOrchestrator

def test_v8_pipeline():
    """Test v8.0 pipeline directly"""
    experiment_path = Path('/Volumes/code/discernus-epic-401/projects/simple_test')
    
    print(f"🔬 Testing v8.0 pipeline directly")
    print(f"📁 Experiment path: {experiment_path}")
    
    # Initialize orchestrator
    orchestrator = ThinOrchestrator(experiment_path)
    
    # Call run_experiment with statistical_prep=True
    try:
        result = orchestrator.run_experiment(
            analysis_model="vertex_ai/gemini-2.5-flash",
            synthesis_model="vertex_ai/gemini-2.5-pro", 
            statistical_prep=True
        )
        
        print("✅ V8.0 pipeline completed successfully!")
        print(f"📊 Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ V8.0 pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_v8_pipeline()
    sys.exit(0 if success else 1)
