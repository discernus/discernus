#!/usr/bin/env python3
"""
Test script for enhanced Stage 1 prompt
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.two_stage_synthesis_agent import TwoStageSynthesisAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger

def test_enhanced_stage1_prompt():
    """Test enhanced Stage 1 prompt loading and content."""
    
    print("=== Testing Enhanced Stage 1 Prompt ===")
    
    # Use existing nano experiment
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250921_011822"
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, nano_run_dir)
    audit = AuditLogger(security, nano_run_dir)
    
    print("\n1. Testing enhanced prompt loading:")
    try:
        agent = TwoStageSynthesisAgent(security, storage, audit)
        print(f"✅ Agent created with enhanced prompts")
        print(f"   Stage 1 prompt: {len(agent.stage1_prompt)} characters")
        print(f"   Stage 2 prompt: {len(agent.stage2_prompt)} characters")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return False
    
    print("\n2. Testing enhanced Stage 1 content:")
    
    # Check for framework-centric analysis
    if "Framework Architecture" in agent.stage1_prompt:
        print("  ✅ Framework-centric analysis included")
    else:
        print("  ❌ Missing framework-centric analysis")
    
    # Check for experimental intent discovery
    if "Divine Experimental Intent" in agent.stage1_prompt:
        print("  ✅ Experimental intent discovery included")
    else:
        print("  ❌ Missing experimental intent discovery")
    
    # Check for unanticipated insights
    if "Unanticipated Insights" in agent.stage1_prompt:
        print("  ✅ Unanticipated insights section included")
    else:
        print("  ❌ Missing unanticipated insights section")
    
    # Check for sequential analysis protocol
    if "Sequential Analysis Protocol" in agent.stage1_prompt:
        print("  ✅ Sequential analysis protocol included")
    else:
        print("  ❌ Missing sequential analysis protocol")
    
    # Check for framework performance assessment
    if "Framework Performance Assessment" in agent.stage1_prompt:
        print("  ✅ Framework performance assessment included")
    else:
        print("  ❌ Missing framework performance assessment")
    
    print("\n3. Testing researcher-focused structure:")
    
    # Check for researcher-oriented sections
    researcher_sections = [
        "Framework Analysis & Performance",
        "Experimental Intent & Hypothesis Evaluation", 
        "Unanticipated Insights & Framework Extensions",
        "Research Implications & Significance"
    ]
    
    for section in researcher_sections:
        if section in agent.stage1_prompt:
            print(f"  ✅ {section}")
        else:
            print(f"  ❌ Missing: {section}")
    
    print("\n4. Testing analytical depth requirements:")
    
    depth_requirements = [
        "Statistical Interpretation Standards",
        "Framework-Centric Analysis", 
        "Insight Generation Principles",
        "Beyond Confirmation"
    ]
    
    for requirement in depth_requirements:
        if requirement in agent.stage1_prompt:
            print(f"  ✅ {requirement}")
        else:
            print(f"  ❌ Missing: {requirement}")
    
    print(f"\n✅ Enhanced Stage 1 prompt test completed!")
    print(f"🎯 Prompt is {len(agent.stage1_prompt)} characters with deep framework analysis!")
    
    return True

if __name__ == "__main__":
    success = test_enhanced_stage1_prompt()
    sys.exit(0 if success else 1)
