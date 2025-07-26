#!/usr/bin/env python3
"""
Quick Agent Test - Direct validation of EnhancedAnalysisAgent
============================================================

Simple smoke test to validate that our enhanced agents work correctly
without the complexity of promptfoo configuration.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary  
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage

def test_enhanced_analysis_agent():
    """Test the EnhancedAnalysisAgent with a simple document"""
    
    print("🧪 Starting Quick Agent Test...")
    
    # Setup test environment - use existing simple_test experiment
    test_dir = project_root / "projects" / "simple_test"
    test_run_dir = test_dir / "test_run"
    test_run_dir.mkdir(exist_ok=True)
    
    # Initialize components
    security_boundary = ExperimentSecurityBoundary(test_dir)
    audit_logger = AuditLogger(security_boundary, test_run_dir)
    artifact_storage = LocalArtifactStorage(security_boundary, test_run_dir)
    
    # Create agent
    agent = EnhancedAnalysisAgent(
        security_boundary=security_boundary,
        audit_logger=audit_logger, 
        artifact_storage=artifact_storage
    )
    
    # Test document
    test_document = {
        'content': """
        My fellow Americans, today we face great challenges but also great opportunities. 
        We must stand together with courage and wisdom to build a better future for our children.
        Justice and truth will guide our path forward.
        """,
        'filename': 'test_speech.txt'
    }
    
    # Simple framework
    test_framework = """
    # Test Framework
    
    Analyze the document for character dimensions:
    - Courage vs Fear
    - Wisdom vs Cunning  
    - Justice vs Resentment
    - Truth vs Manipulation
    
    Rate each dimension on intensity (0.0-1.0) and salience (0.0-1.0).
    """
    
    # Test configuration
    experiment_config = {
        'name': 'quick_agent_test'
    }
    
    try:
        print("📝 Running analysis...")
        
        # Call the agent
        result = agent.analyze_batch(
            documents=[test_document],
            framework_content=test_framework,
            experiment_config=experiment_config,
            model="vertex_ai/gemini-2.5-pro"
        )
        
        print("✅ Analysis completed successfully!")
        print(f"📊 Result keys: {list(result.keys())}")
        
        # Basic validation - check wrapper structure
        if 'result_content' not in result:
            print("❌ Missing result_content in results")
            return False
            
        result_content = result['result_content']
        required_keys = ['analysis_results', 'batch_id', 'agent_name']
        missing_keys = [key for key in required_keys if key not in result_content]
        
        if missing_keys:
            print(f"❌ Missing required keys in result_content: {missing_keys}")
            return False
            
        # Check if analysis results have the expected structure
        analysis_results = result_content.get('analysis_results', {})  
        if 'analysis_summary' not in analysis_results:
            print("❌ Missing analysis_summary in results")
            return False
            
        print("🎉 Agent test passed - enhanced agents are working!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup - audit logger handles its own cleanup
        pass

if __name__ == "__main__":
    success = test_enhanced_analysis_agent()
    sys.exit(0 if success else 1) 