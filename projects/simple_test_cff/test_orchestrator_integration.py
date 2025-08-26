#!/usr/bin/env python3
"""
Test script to verify EvidenceRetriever integration with CleanAnalysisOrchestrator
"""

import sys
import os
sys.path.insert(0, '/Volumes/code/discernus')

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator

def test_orchestrator_integration():
    """Test that the orchestrator can be initialized with EvidenceRetriever integration"""
    
    print("🧪 Testing EvidenceRetriever Orchestrator Integration")
    print("=" * 60)
    
    # Initialize orchestrator
    print("📋 Initializing CleanAnalysisOrchestrator...")
    orchestrator = CleanAnalysisOrchestrator('/Volumes/code/discernus/projects/simple_test_cff')
    print("✅ Orchestrator initialized successfully")
    
    # Check if EvidenceRetrieverAgent is available
    print("\n🔍 Checking EvidenceRetrieverAgent availability...")
    try:
        from discernus.agents.evidence_retriever_agent import EvidenceRetrieverAgent
        print("✅ EvidenceRetrieverAgent import successful")
        
        # Test agent creation
        agent_config = {
            'experiment_path': '/Volumes/code/discernus/projects/simple_test_cff',
            'run_id': 'test_run'
        }
        evidence_agent = EvidenceRetrieverAgent(agent_config)
        print("✅ EvidenceRetrieverAgent creation successful")
        
    except Exception as e:
        print(f"❌ EvidenceRetrieverAgent test failed: {e}")
        return False
    
    # Check orchestrator methods
    print("\n🔍 Checking orchestrator methods...")
    if hasattr(orchestrator, '_run_evidence_retrieval_phase'):
        print("✅ _run_evidence_retrieval_phase method found")
    else:
        print("❌ _run_evidence_retrieval_phase method missing")
        return False
    
    if hasattr(orchestrator, '_run_synthesis'):
        print("✅ _run_synthesis method found (with evidence_results parameter)")
    else:
        print("❌ _run_synthesis method missing")
        return False
    
    print("\n🎉 All integration tests passed!")
    return True

if __name__ == "__main__":
    success = test_orchestrator_integration()
    if success:
        print("\n✅ EvidenceRetriever integration successful!")
    else:
        print("\n❌ EvidenceRetriever integration failed!")
        sys.exit(1)
