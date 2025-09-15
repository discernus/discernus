#!/usr/bin/env python3
"""
Debug Tool Calling Reliability
=============================

Test the EnhancedAnalysisAgentMultiTool to understand why it only calls 1 of 3 tools.
"""

import tempfile
import os
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry

def test_tool_calling_reliability():
    """Test multiple runs to see tool calling patterns"""
    
    # Create temporary experiment directory
    temp_dir = tempfile.mkdtemp()
    print(f"🔍 Using temp directory: {temp_dir}")
    
    try:
        # Create required experiment.md file
        experiment_path = os.path.join(temp_dir, "experiment.md")
        with open(experiment_path, "w") as f:
            f.write("# Test Experiment\n")
        
        # Create dependencies
        security = ExperimentSecurityBoundary(Path(temp_dir))
        audit = AuditLogger(security, Path(temp_dir))
        storage = LocalArtifactStorage(security, Path(temp_dir))
        model_registry = ModelRegistry()
        llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Create agent
        agent = EnhancedAnalysisAgentMultiTool(
            security_boundary=security,
            audit_logger=audit,
            storage=storage,
            llm_gateway=llm_gateway,
            model="vertex_ai/gemini-2.5-flash"
        )
        
        # Test document and framework
        document_content = """The people are being betrayed by the elite establishment. 
We need to restore power to the working class and drain the swamp.
The crisis is real and only I can fix it."""
        
        framework_content = """# Simple Test Framework

## Dimensions
- populism: Measures populist rhetoric
- authoritarianism: Measures authoritarian tendencies

## Scoring
Each dimension scored 0.0-1.0 with confidence and salience"""
        
        print(f"\n=== Testing Tool Calling Reliability ===")
        print(f"Document: {len(document_content)} characters")
        print(f"Framework: {len(framework_content)} characters")
        
        # Run multiple tests
        results = []
        for i in range(5):
            print(f"\n--- Test Run {i+1}/5 ---")
            
            try:
                result = agent.analyze_document(
                    document_content=document_content,
                    framework_content=framework_content,
                    document_id=f"test_doc_{i+1}"
                )
                
                tool_calls_count = result.get("tool_calls_count", 0)
                success = result.get("success", False)
                
                print(f"✅ Success: {success}")
                print(f"🔧 Tool calls: {tool_calls_count}/3")
                print(f"📊 Scores artifact: {result.get('scores_artifact', 'None')}")
                print(f"📝 Evidence artifact: {result.get('evidence_artifact', 'None')}")
                print(f"🔧 Work artifact: {result.get('work_artifact', 'None')}")
                
                results.append({
                    "run": i+1,
                    "success": success,
                    "tool_calls_count": tool_calls_count,
                    "has_scores": bool(result.get('scores_artifact')),
                    "has_evidence": bool(result.get('evidence_artifact')),
                    "has_work": bool(result.get('work_artifact'))
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    "run": i+1,
                    "success": False,
                    "error": str(e)
                })
        
        # Analyze results
        print(f"\n=== Analysis ===")
        successful_runs = [r for r in results if r.get("success", False)]
        print(f"Successful runs: {len(successful_runs)}/5")
        
        if successful_runs:
            tool_call_counts = [r["tool_calls_count"] for r in successful_runs]
            print(f"Tool call counts: {tool_call_counts}")
            print(f"Average tool calls: {sum(tool_call_counts)/len(tool_call_counts):.1f}")
            
            # Check which tools are being called
            scores_count = sum(1 for r in successful_runs if r.get("has_scores", False))
            evidence_count = sum(1 for r in successful_runs if r.get("has_evidence", False))
            work_count = sum(1 for r in successful_runs if r.get("has_work", False))
            
            print(f"Scores tool called: {scores_count}/{len(successful_runs)}")
            print(f"Evidence tool called: {evidence_count}/{len(successful_runs)}")
            print(f"Work tool called: {work_count}/{len(successful_runs)}")
        
        # Check artifacts
        print(f"\n=== Artifacts ===")
        artifacts_dir = Path(temp_dir) / "artifacts"
        if artifacts_dir.exists():
            for artifact_file in artifacts_dir.glob("*.json"):
                print(f"📁 {artifact_file.name} ({artifact_file.stat().st_size} bytes)")
                
                # Show content of first few artifacts
                if artifact_file.name.startswith("analysis_scores"):
                    with open(artifact_file, 'r') as f:
                        data = json.load(f)
                        print(f"   Content: {json.dumps(data, indent=2)[:200]}...")
        
    finally:
        print(f"\n🔍 Test artifacts preserved in: {temp_dir}")

if __name__ == "__main__":
    test_tool_calling_reliability()
