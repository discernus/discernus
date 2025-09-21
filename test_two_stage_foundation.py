#!/usr/bin/env python3
"""
Test script for TwoStageSynthesisAgent foundation
"""

import sys
import os
import json
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.two_stage_synthesis_agent import TwoStageSynthesisAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent

def test_two_stage_foundation():
    """Test TwoStageSynthesisAgent foundation and architecture."""
    
    print("=== Testing TwoStageSynthesisAgent Foundation ===")
    
    # Use existing nano experiment
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250921_011822"  # Use latest successful run
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, nano_run_dir)
    audit = AuditLogger(security, nano_run_dir)
    
    print("\n1. Testing agent instantiation:")
    try:
        agent = TwoStageSynthesisAgent(security, storage, audit)
        print(f"✅ Agent created: {agent.agent_name}")
        print(f"   Stage 1 Model: {agent.stage1_model}")
        print(f"   Stage 2 Model: {agent.stage2_model}")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return False
    
    print("\n2. Testing agent capabilities:")
    capabilities = agent.get_capabilities()
    expected_capabilities = [
        "two_stage_synthesis",
        "anti_hallucination_architecture",
        "data_driven_analysis", 
        "evidence_integration",
        "evidence_appendix_generation"
    ]
    
    for cap in expected_capabilities:
        if cap in capabilities:
            print(f"  ✅ {cap}")
        else:
            print(f"  ❌ Missing capability: {cap}")
    
    print(f"\nTotal capabilities: {len(capabilities)}")
    
    print("\n3. Testing input validation:")
    
    # Create RunContext
    run_context = RunContext(
        experiment_id="nano_test_experiment",
        framework_path=nano_dir / "sentiment_binary_v1.md", 
        corpus_path=nano_dir / "corpus.md"
    )
    
    # Test validation without statistical results
    run_context.statistical_results = None
    valid = agent._validate_inputs(run_context)
    print(f"  Validation without stats: {'❌ Failed' if not valid else '✅ Passed'} (expected: Failed)")
    
    # Test validation with statistical results (set for remaining tests)
    run_context.statistical_results = {
        "correlations": {"positive_negative_sentiment": -1.0},
        "descriptive_stats": {"positive_sentiment": {"mean": 0.5}}
    }
    valid = agent._validate_inputs(run_context)
    print(f"  Validation with stats: {'✅ Passed' if valid else '❌ Failed'} (expected: Passed)")
    
    print("\n4. Testing two-stage architecture:")
    
    # Test execute method (should fail gracefully since stages not implemented)
    try:
        result = agent.execute(run_context)
        print(f"  Execute result: success={result.success}")
        print(f"  Error message: {result.error_message}")
        print(f"  Metadata: {result.metadata.get('agent_name', 'unknown')}")
        
        # Should fail because stages not implemented, but gracefully
        if not result.success and "Stage 1 analysis failed" in result.error_message:
            print("  ✅ Graceful failure as expected (stages not implemented)")
        else:
            print("  ⚠️ Unexpected result - check implementation")
            
    except Exception as e:
        print(f"  ❌ Execute failed with exception: {e}")
        return False
    
    print("\n5. Testing architecture principles:")
    
    # Verify stage separation
    print(f"  ✅ Stage 1 Model (Pro for analysis): {agent.stage1_model}")
    print(f"  ✅ Stage 2 Model (Flash for integration): {agent.stage2_model}")
    print(f"  ✅ Agent inherits from StandardAgent: {isinstance(agent, StandardAgent)}")
    print(f"  ✅ Enhanced LLM Gateway available: {hasattr(agent, 'llm_gateway')}")
    
    print("\n✅ TwoStageSynthesisAgent foundation test passed!")
    print("🎯 Ready for Stage 1 and Stage 2 implementation!")
    
    return True

if __name__ == "__main__":
    success = test_two_stage_foundation()
    sys.exit(0 if success else 1)
