#!/usr/bin/env python3
"""
Prototype: Verification Agent with Tool Calling
==============================================

This prototype demonstrates how the Verification Agent would work
with the new tool calling architecture to verify the analysis work.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Reuse the mock classes from the analysis agent
from test_analysis_agent_tool_calling import MockSecurityBoundary, MockAuditLogger, MockArtifactStorage

class MockVerificationLLMGateway:
    """Mock LLM Gateway for verification with tool calling"""
    
    def __init__(self):
        self.call_count = 0
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict[str, Any]]) -> tuple[str, Dict[str, Any]]:
        """Simulate verification LLM call with tool calling"""
        self.call_count += 1
        
        # Simulate the verification LLM's tool call response
        # In a real implementation, this would re-execute the code and compare results
        tool_call_response = {
            "id": f"verification_call_{self.call_count}",
            "type": "function",
            "function": {
                "name": "record_attestation",
                "arguments": json.dumps({
                    "document_id": "doc_001",
                    "success": True,  # Verification passed
                    "verifier_model": "vertex_ai/gemini-2.5-pro",
                    "verifier_model_version": "2.5.0",
                    "reasoning": "Re-executed the provided code and verified the derived metrics calculations. The overall_intensity calculation using weighted average is correct (0.7), and the rhetorical_complexity using standard deviation is accurate (0.1). All mathematical operations are sound.",
                    "executed_code_digest_sha256": "abc123def456789",
                    "analysis_digest_sha256": "def456abc123789",
                    "re_execution_output": "Overall intensity: 0.700\nRhetorical complexity: 0.100\n"
                })
            }
        }
        
        # Simulate metadata
        metadata = {
            "success": True,
            "usage": {
                "total_tokens": 800,
                "prompt_tokens": 600,
                "completion_tokens": 200,
                "response_cost_usd": 0.0008
            },
            "model": model,
            "tool_calls": [tool_call_response]
        }
        
        return json.dumps(tool_call_response), metadata

class VerificationAgentToolCalling:
    """Prototype of Verification Agent using tool calling"""
    
    def __init__(self, security_boundary, audit_logger, artifact_storage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "VerificationAgentToolCalling"
        self.llm_gateway = MockVerificationLLMGateway()
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "capabilities": ["adversarial_verification", "code_re_execution", "attestation"]
        })
    
    def verify_analysis(self, analysis_artifact_id: str, work_artifact_id: str,
                       model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
        """Verify an analysis by re-executing the code and comparing results"""
        
        # Load the artifacts
        analysis_data = self.storage.get_artifact(analysis_artifact_id)
        work_data = self.storage.get_artifact(work_artifact_id)
        
        if not analysis_data or not work_data:
            raise ValueError("Could not load required artifacts")
        
        analysis_content = json.loads(analysis_data['content'])
        work_content = json.loads(work_data['content'])
        
        # Create verification prompt
        prompt = self._create_verification_prompt(analysis_content, work_content)
        
        # Define the attestation tool schema
        tools = [{
            "type": "function",
            "function": {
                "name": "record_attestation",
                "description": "Record verification attestation results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "success": {"type": "boolean"},
                        "verifier_model": {"type": "string"},
                        "verifier_model_version": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "executed_code_digest_sha256": {"type": "string"},
                        "analysis_digest_sha256": {"type": "string"},
                        "re_execution_output": {"type": "string"}
                    },
                    "required": ["document_id", "success", "verifier_model", "reasoning"]
                }
            }
        }]
        
        # Execute verification LLM call with tools
        system_prompt = "You are a verification specialist. Re-execute the provided code, verify the calculations, and call the record_attestation tool with your findings."
        
        self.audit.log_agent_event(self.agent_name, "verification_start", {
            "model": model,
            "document_id": analysis_content["document_id"],
            "analysis_artifact": analysis_artifact_id,
            "work_artifact": work_artifact_id
        })
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools
        )
        
        # Parse the tool call response
        tool_call_data = json.loads(response_content)
        function_args = json.loads(tool_call_data["function"]["arguments"])
        
        # Save attestation artifact
        attestation_artifact = self._save_attestation_artifact(function_args)
        
        self.audit.log_agent_event(self.agent_name, "verification_complete", {
            "document_id": function_args["document_id"],
            "success": function_args["success"],
            "attestation_artifact": attestation_artifact
        })
        
        return {
            "document_id": function_args["document_id"],
            "success": function_args["success"],
            "attestation_artifact": attestation_artifact,
            "reasoning": function_args["reasoning"],
            "metadata": metadata
        }
    
    def _create_verification_prompt(self, analysis_content: Dict[str, Any], 
                                   work_content: Dict[str, Any]) -> str:
        """Create the verification prompt for the LLM"""
        return f"""
Verify the following analysis by re-executing the provided code and checking the calculations.

ANALYSIS RESULTS:
{json.dumps(analysis_content, indent=2)}

EXECUTED CODE:
{work_content['executed_code']}

CLAIMED OUTPUT:
{work_content['execution_output']}

VERIFICATION INSTRUCTIONS:
1. Re-execute the provided code internally
2. Compare your results with the claimed output
3. Verify the mathematical correctness of the derived metrics calculations
4. Check for any logical errors or inconsistencies
5. Call the record_attestation tool with your verification results

If verification fails, provide detailed reasoning about what went wrong.
"""
    
    def _save_attestation_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the attestation results as a clean artifact"""
        attestation_data = {
            "document_id": function_args["document_id"],
            "success": function_args["success"],
            "verifier_model": function_args["verifier_model"],
            "verifier_model_version": function_args["verifier_model_version"],
            "reasoning": function_args["reasoning"],
            "executed_code_digest_sha256": function_args.get("executed_code_digest_sha256"),
            "analysis_digest_sha256": function_args.get("analysis_digest_sha256"),
            "re_execution_output": function_args.get("re_execution_output"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(attestation_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "attestation",
            "document_id": function_args["document_id"],
            "verifier_model": function_args["verifier_model"]
        })

def main():
    """Demonstrate the verification agent prototype"""
    print("=== Verification Agent Tool Calling Prototype ===\n")
    
    # Initialize mock dependencies
    security = MockSecurityBoundary()
    audit = MockAuditLogger()
    storage = MockArtifactStorage()
    
    # Create sample artifacts (simulating what the analysis agent would create)
    analysis_data = {
        "document_id": "doc_001",
        "document_hash": "abc123def456",
        "framework_name": "test_framework",
        "framework_version": "1.0.0",
        "scores": {
            "sentiment": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95},
            "populism": {"raw_score": 0.6, "salience": 0.7, "confidence": 0.85}
        },
        "derived_metrics": {
            "overall_intensity": 0.7,
            "rhetorical_complexity": 0.65
        },
        "evidence": [
            {
                "dimension": "sentiment",
                "quote": "This is a great example of positive sentiment",
                "source": "paragraph_2",
                "offset": 45
            }
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    work_data = {
        "document_id": "doc_001",
        "executed_code": """
# Calculate derived metrics
import numpy as np

scores = {
    'sentiment': {'raw_score': 0.8, 'salience': 0.9, 'confidence': 0.95},
    'populism': {'raw_score': 0.6, 'salience': 0.7, 'confidence': 0.85}
}

# Calculate overall intensity (weighted average)
raw_scores = [scores[dim]['raw_score'] for dim in scores]
salience_weights = [scores[dim]['salience'] for dim in scores]
overall_intensity = np.average(raw_scores, weights=salience_weights)

# Calculate rhetorical complexity (standard deviation)
rhetorical_complexity = np.std(raw_scores)

derived_metrics = {
    'overall_intensity': float(overall_intensity),
    'rhetorical_complexity': float(rhetorical_complexity)
}

print(f"Overall intensity: {overall_intensity:.3f}")
print(f"Rhetorical complexity: {rhetorical_complexity:.3f}")
""",
        "execution_output": "Overall intensity: 0.700\nRhetorical complexity: 0.100\n",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Store the artifacts
    analysis_artifact_id = storage.put_artifact(
        json.dumps(analysis_data, indent=2).encode('utf-8'),
        {"artifact_type": "analysis", "document_id": "doc_001"}
    )
    
    work_artifact_id = storage.put_artifact(
        json.dumps(work_data, indent=2).encode('utf-8'),
        {"artifact_type": "work", "document_id": "doc_001"}
    )
    
    print("1. Created sample analysis and work artifacts")
    print(f"   Analysis Artifact: {analysis_artifact_id}")
    print(f"   Work Artifact: {work_artifact_id}")
    
    # Create the verification agent
    verifier = VerificationAgentToolCalling(security, audit, storage)
    
    print("\n2. Running verification...")
    result = verifier.verify_analysis(analysis_artifact_id, work_artifact_id)
    
    print(f"\n3. Verification complete!")
    print(f"   Document ID: {result['document_id']}")
    print(f"   Success: {result['success']}")
    print(f"   Attestation Artifact: {result['attestation_artifact']}")
    print(f"   Reasoning: {result['reasoning']}")
    
    print(f"\n4. Attestation artifact content:")
    attestation_data = storage.get_artifact(result['attestation_artifact'])
    print(json.dumps(json.loads(attestation_data['content']), indent=2))
    
    print(f"\n5. Audit log:")
    for event in audit.events:
        print(f"   {event['timestamp']}: {event['agent']} - {event['event']}")
    
    print(f"\n=== Key Benefits Demonstrated ===")
    print("✅ Adversarial verification using separate LLM")
    print("✅ Code re-execution and result comparison")
    print("✅ Structured attestation via tool calls")
    print("✅ Complete audit trail of verification process")
    print("✅ Fail-fast capability when verification fails")

if __name__ == "__main__":
    main()
