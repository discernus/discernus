#!/usr/bin/env python3
"""
Debug LLM Response
==================

Check what the LLM is actually returning to understand why it only calls 1 tool.
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

def debug_llm_response():
    """Debug what the LLM is actually returning"""
    
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
        
        print(f"\n=== Debugging LLM Response ===")
        
        # Create analysis prompt
        prompt = agent._create_analysis_prompt(document_content, framework_content)
        print(f"📝 Prompt length: {len(prompt)} characters")
        print(f"📝 Prompt preview:\n{prompt[:500]}...\n")
        
        # Get tools schema
        tools = agent._get_tools_schema(framework_content)
        print(f"🔧 Tools schema: {json.dumps(tools, indent=2)}")
        
        # Make the LLM call directly to see raw response
        print(f"\n=== Making LLM Call ===")
        response, metadata = llm_gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt,
            system_prompt="You are a helpful assistant. You MUST call all three functions in your response. Complete STEP 1, STEP 2, and STEP 3 by calling record_analysis_scores, record_evidence_quotes, and record_computational_work respectively. Do not stop after the first function call.",
            tools=tools,
            force_function_calling=False
        )
        
        print(f"📤 Raw response: {response}")
        print(f"📊 Metadata: {json.dumps(metadata, indent=2)}")
        
        # Check tool calls
        tool_calls = metadata.get('tool_calls', [])
        print(f"\n🔧 Tool calls found: {len(tool_calls)}")
        for i, tool_call in enumerate(tool_calls):
            print(f"  Tool {i+1}: {tool_call}")
        
    finally:
        print(f"\n🔍 Test artifacts preserved in: {temp_dir}")

if __name__ == "__main__":
    debug_llm_response()
