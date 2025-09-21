#!/usr/bin/env python3
"""
Test script for IntelligentEvidenceRetrievalAgent foundation
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger

def test_agent_foundation():
    """Test that the agent can be instantiated and has proper capabilities."""
    
    # Use existing nano experiment for testing
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    test_run_dir = nano_dir / "test_run"
    test_run_dir.mkdir(exist_ok=True)
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, test_run_dir)
    audit = AuditLogger(security, test_run_dir)
    
    # Create agent
    agent = IntelligentEvidenceRetrievalAgent(security, storage, audit)
    
    # Test capabilities
    capabilities = agent.get_capabilities()
    expected_capabilities = [
        "intelligent_evidence_curation",
        "strategic_planning", 
        "atomic_evidence_processing",
        "statistical_mapping",
        "dynamic_model_selection",
        "session_caching",
        "tool_calling",
        "structured_output"
    ]
    
    print(f"Agent Name: {agent.agent_name}")
    print(f"Capabilities: {capabilities}")
    
    # Verify all expected capabilities are present
    for capability in expected_capabilities:
        assert capability in capabilities, f"Missing capability: {capability}"
    
    # Test model selection logic
    flash_model = agent.select_execution_model(100, 0.5)  # Small corpus
    pro_model = agent.select_execution_model(500, 4.0)    # Large corpus
    
    print(f"Small corpus model: {flash_model}")
    print(f"Large corpus model: {pro_model}")
    
    assert flash_model == "gemini-2.5-flash", "Should select Flash for small corpus"
    assert pro_model == "gemini-2.5-pro", "Should select Pro for large corpus"
    
    print("✅ IntelligentEvidenceRetrievalAgent foundation test passed!")

if __name__ == "__main__":
    test_agent_foundation()
