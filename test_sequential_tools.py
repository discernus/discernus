#!/usr/bin/env python3
"""
Test Sequential Tool Calling
===========================

Test the new sequential tool calling approach.
"""

import tempfile
import os
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.agents.EnhancedAnalysisAgent.agent_sequential_tools import EnhancedAnalysisAgentSequentialTools
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry

def test_sequential_tools():
    """Test the sequential tool calling approach"""
    
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
        agent = EnhancedAnalysisAgentSequentialTools(
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
        
        print(f"\n=== Testing Sequential Tool Calling ===")
        print(f"Document: {len(document_content)} characters")
        print(f"Framework: {len(framework_content)} characters")
        
        # Run test
        result = agent.analyze_document(
            document_content=document_content,
            framework_content=framework_content,
            document_id="test_doc_1"
        )
        
        print(f"\n=== Results ===")
        print(f"✅ Success: {result.get('success', False)}")
        print(f"🔧 Tool calls: {result.get('tool_calls_count', 0)}/3")
        print(f"📊 Scores artifact: {result.get('scores_artifact', 'None')}")
        print(f"📝 Evidence artifact: {result.get('evidence_artifact', 'None')}")
        print(f"🔧 Work artifact: {result.get('work_artifact', 'None')}")
        
        # Check artifacts
        print(f"\n=== Artifacts ===")
        artifacts_dir = Path(temp_dir) / "artifacts"
        if artifacts_dir.exists():
            for artifact_file in artifacts_dir.glob("*.json"):
                print(f"📁 {artifact_file.name} ({artifact_file.stat().st_size} bytes)")
                
                # Show content of first artifact
                if artifact_file.name.startswith("analysis_scores"):
                    with open(artifact_file, 'r') as f:
                        data = json.load(f)
                        print(f"   Content: {json.dumps(data, indent=2)[:300]}...")
        
    finally:
        print(f"\n🔍 Test artifacts preserved in: {temp_dir}")

if __name__ == "__main__":
    test_sequential_tools()
