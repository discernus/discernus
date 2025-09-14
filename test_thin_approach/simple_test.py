#!/usr/bin/env python3
"""
Simple test to debug tool calling issues
"""

import json
from pathlib import Path
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry

def test_simple_tool_call():
    """Test a simple tool call to debug the issue."""
    
    experiment_dir = Path("/Volumes/code/discernus/test_thin_approach")
    
    # Initialize components
    security = ExperimentSecurityBoundary(experiment_dir)
    audit = AuditLogger(security, experiment_dir / "logs")
    storage = LocalArtifactStorage(security, experiment_dir / "artifacts")
    gateway = EnhancedLLMGateway(ModelRegistry())
    
    # Simple tool definition
    tools = [{
        "type": "function",
        "function": {
            "name": "record_analysis_scores",
            "description": "Record dimensional analysis scores",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "dimensional_scores": {
                        "type": "object",
                        "properties": {
                            "test_dimension": {
                                "type": "object",
                                "properties": {
                                    "raw_score": {"type": "number"},
                                    "salience": {"type": "number"},
                                    "confidence": {"type": "number"}
                                }
                            }
                        }
                    }
                },
                "required": ["document_id", "dimensional_scores"]
            }
        }
    }]
    
    prompt = """You are a test analyst. Make exactly 1 tool call to record_analysis_scores with:
- document_id: "test_doc"
- dimensional_scores with test_dimension: raw_score=0.8, salience=0.7, confidence=0.9

Make the tool call now."""
    
    print("Making simple tool call test...")
    response = gateway.execute_call_with_tools(
        prompt=prompt,
        model="vertex_ai/gemini-2.5-flash",
        tools=tools,
        max_tokens=1000
    )
    
    print(f"Response type: {type(response)}")
    if isinstance(response, tuple):
        content, metadata = response
        print(f"Content: {content[:200]}...")
        print(f"Metadata keys: {list(metadata.keys())}")
        if 'tool_calls' in metadata:
            print(f"Tool calls: {metadata['tool_calls']}")
        else:
            print("No tool_calls in metadata")
    else:
        print(f"Response: {response}")

if __name__ == "__main__":
    test_simple_tool_call()
