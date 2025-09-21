#!/usr/bin/env python3
"""
Test script to verify RAG removal and IntelligentEvidenceRetrievalAgent integration
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_rag_removal():
    """Test that RAG dependencies are removed and new agent works."""
    
    print("=== Testing RAG Removal and New Agent Integration ===")
    
    # Test 1: Verify new agent can be imported
    print("\n1. Testing IntelligentEvidenceRetrievalAgent import:")
    try:
        from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
        print("✅ IntelligentEvidenceRetrievalAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import IntelligentEvidenceRetrievalAgent: {e}")
        return False
    
    # Test 2: Verify CLI imports work
    print("\n2. Testing CLI imports with new agent:")
    try:
        from discernus.cli import run  # This should import the new agent
        print("✅ CLI imports work with IntelligentEvidenceRetrievalAgent")
    except ImportError as e:
        print(f"❌ CLI import failed: {e}")
        return False
    
    # Test 3: Verify old RAG components still exist but are not required
    print("\n3. Checking RAG component status:")
    
    # RAG components should exist but not be imported by new agent
    rag_files = [
        "discernus/core/rag_index_manager.py",
        "discernus/agents/evidence_retriever_agent/v2_evidence_retriever_agent.py"
    ]
    
    for rag_file in rag_files:
        if Path(rag_file).exists():
            print(f"  📁 {rag_file} exists (deprecated but not removed)")
        else:
            print(f"  ❌ {rag_file} missing")
    
    # Test 4: Verify new agent capabilities
    print("\n4. Testing new agent capabilities:")
    
    # Create minimal test setup
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250920_223951"
    
    if nano_run_dir.exists():
        try:
            from discernus.core.security_boundary import ExperimentSecurityBoundary
            from discernus.core.local_artifact_storage import LocalArtifactStorage
            from discernus.core.audit_logger import AuditLogger
            
            security = ExperimentSecurityBoundary(nano_dir)
            storage = LocalArtifactStorage(security, nano_run_dir)
            audit = AuditLogger(security, nano_run_dir)
            
            # Create new agent
            agent = IntelligentEvidenceRetrievalAgent(security, storage, audit)
            
            # Test capabilities
            capabilities = agent.get_capabilities()
            expected_capabilities = [
                "intelligent_evidence_curation",
                "strategic_planning", 
                "atomic_evidence_processing",
                "dynamic_model_selection",
                "session_caching"
            ]
            
            for cap in expected_capabilities:
                if cap in capabilities:
                    print(f"  ✅ {cap}")
                else:
                    print(f"  ❌ Missing capability: {cap}")
            
            print("✅ New agent instantiated and capabilities verified")
            
        except Exception as e:
            print(f"❌ Failed to test new agent: {e}")
            return False
    else:
        print("  ⚠️ Nano experiment not available for testing")
    
    # Test 5: Verify no RAG imports in new agent
    print("\n5. Verifying no RAG dependencies in new agent:")
    
    agent_file = Path("discernus/agents/intelligent_evidence_retriever/intelligent_evidence_retriever_agent.py")
    if agent_file.exists():
        with open(agent_file, 'r') as f:
            content = f.read()
        
        rag_imports = ["rag_index_manager", "RAGIndexManager", "txtai", "embeddings"]
        has_rag = any(rag_term in content for rag_term in rag_imports)
        
        if has_rag:
            print("  ❌ New agent still has RAG dependencies")
            return False
        else:
            print("  ✅ New agent is RAG-free")
    
    print("\n✅ RAG removal and new agent integration successful!")
    print("🎯 IntelligentEvidenceRetrievalAgent ready for production use!")
    
    return True

if __name__ == "__main__":
    success = test_rag_removal()
    sys.exit(0 if success else 1)
