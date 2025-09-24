#!/usr/bin/env python3
"""
Debug Cost Logging Implementation
================================

This script debugs why cost logging isn't working by checking the audit logger
and testing the log_llm_interaction method directly.
"""

import json
import sys
from pathlib import Path

# Add discernus to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary

def test_audit_logger():
    """Test the audit logger directly."""
    
    print("🔍 Testing Audit Logger")
    print("=" * 30)
    
    # Use an existing experiment directory
    test_run_dir = Path("projects/micro")
    
    try:
        # Initialize audit logger
        security = ExperimentSecurityBoundary(test_run_dir)
        audit = AuditLogger(security, test_run_dir)
        
        print("✅ Audit logger initialized")
        
        # Test log_llm_interaction method
        print("\n🧪 Testing log_llm_interaction method...")
        
        interaction_hash = audit.log_llm_interaction(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt="Test prompt",
            response="Test response",
            agent_name="TestAgent",
            interaction_type="test",
            metadata={
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
                "response_cost_usd": 0.001,
                "step": "test"
            }
        )
        
        print(f"✅ Interaction logged with hash: {interaction_hash}")
        
        # Check if file was created
        llm_log = test_run_dir / "logs" / "llm_interactions.jsonl"
        if llm_log.exists():
            print(f"✅ LLM interactions log created: {llm_log}")
            
            # Read and display the log
            with open(llm_log, 'r') as f:
                content = f.read()
                print(f"📄 Log content:\n{content}")
        else:
            print("❌ LLM interactions log not created")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing audit logger: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up test directory
        import shutil
        if test_run_dir.exists():
            shutil.rmtree(test_run_dir)

def check_agent_audit_logger():
    """Check if agents have access to audit logger."""
    
    print("\n🔍 Checking Agent Audit Logger Access")
    print("=" * 40)
    
    try:
        from discernus.agents.analysis_agent.v2_analysis_agent import V2AnalysisAgent
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        from discernus.core.local_artifact_storage import LocalArtifactStorage
        from discernus.core.audit_logger import AuditLogger
        
        # Create test components
        test_path = Path("projects/micro")
        security = ExperimentSecurityBoundary(test_path)
        storage = LocalArtifactStorage()
        audit = AuditLogger(security, test_path)
        
        # Test agent initialization
        agent = V2AnalysisAgent(security, storage, audit)
        
        print("✅ Agent initialized successfully")
        print(f"✅ Agent has audit logger: {hasattr(agent, 'audit')}")
        print(f"✅ Audit logger has log_llm_interaction: {hasattr(agent.audit, 'log_llm_interaction')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking agent audit logger: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function."""
    
    print("🐛 Discernus Cost Logging Debug")
    print("=" * 50)
    print()
    
    # Test audit logger directly
    audit_success = test_audit_logger()
    
    # Check agent audit logger access
    agent_success = check_agent_audit_logger()
    
    if audit_success and agent_success:
        print("\n✅ Debug completed successfully!")
        print("The audit logger is working correctly.")
        print("The issue might be that the agents aren't calling the logging method.")
    else:
        print("\n❌ Debug found issues:")
        if not audit_success:
            print("- Audit logger has problems")
        if not agent_success:
            print("- Agent audit logger access has problems")

if __name__ == "__main__":
    main()
