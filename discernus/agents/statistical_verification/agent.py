#!/usr/bin/env python3
"""
Statistical Verification Agent
==============================

This agent performs adversarial verification of statistical analysis work
by re-executing code and comparing results using a separate LLM.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class StatisticalVerificationAgent:
    """Statistical Verification Agent using tool calling for adversarial attestation"""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "StatisticalVerificationAgent"
        
        # Initialize enhanced LLM gateway
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["adversarial_verification", "statistical_code_re_execution", "attestation"]
        })

    def verify_statistical_analysis(self, 
                                   statistics_artifact_id: str, 
                                   work_artifact_id: str,
                                   csv_artifact_id: str,
                                   model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
        """Verify statistical analysis by re-executing the code and comparing results"""
        
        # Load the artifacts
        statistics_data = self.storage.get_artifact(statistics_artifact_id)
        work_data = self.storage.get_artifact(work_artifact_id)
        csv_data = self.storage.get_artifact(csv_artifact_id)
        
        if not statistics_data or not work_data or not csv_data:
            raise ValueError("Could not load required statistical artifacts")
        
        statistics_content = json.loads(statistics_data.decode('utf-8'))
        work_content = json.loads(work_data.decode('utf-8'))
        csv_content = csv_data.decode('utf-8')
        
        # Create verification prompt
        prompt = self._create_verification_prompt(statistics_content, work_content, csv_content)
        
        # Define the attestation tool schema
        tools = [{
            "type": "function",
            "function": {
                "name": "record_statistical_attestation",
                "description": "Record verification attestation results for statistical analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "verifier_model": {"type": "string"},
                        "verifier_model_version": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "executed_code_digest_sha256": {"type": "string"},
                        "statistics_digest_sha256": {"type": "string"},
                        "re_execution_output": {"type": "string"}
                    },
                    "required": ["success", "verifier_model", "reasoning"]
                }
            }
        }]
        
        # Execute verification LLM call with tools
        system_prompt = "You are a statistical verification specialist. Re-execute the provided statistical code, verify the calculations, and call the record_statistical_attestation tool with your findings."
        
        self.audit.log_agent_event(self.agent_name, "statistical_verification_start", {
            "model": model,
            "statistics_artifact": statistics_artifact_id,
            "work_artifact": work_artifact_id,
            "csv_artifact": csv_artifact_id
        })
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools,
            context=f"Verifying statistical analysis"
        )
        
        if not metadata.get('success'):
            raise Exception(f"Statistical verification LLM call failed: {metadata.get('error', 'Unknown error')}")
        
        # Extract tool calls from response
        tool_calls = metadata.get('tool_calls', [])
        if not tool_calls:
            raise Exception("No tool calls found in statistical verification response")
        
        # Process the first tool call (should be record_statistical_attestation)
        tool_call = tool_calls[0]
        if tool_call.get('function', {}).get('name') != 'record_statistical_attestation':
            raise Exception(f"Expected record_statistical_attestation tool call, got: {tool_call.get('function', {}).get('name')}")
        
        # Parse the tool call arguments
        function_args = json.loads(tool_call['function']['arguments'])
        
        # Save attestation artifact
        attestation_artifact = self._save_statistical_attestation_artifact(function_args)
        
        self.audit.log_agent_event(self.agent_name, "statistical_verification_complete", {
            "success": function_args["success"],
            "attestation_artifact": attestation_artifact,
            "usage": metadata.get('usage', {})
        })
        
        return {
            "success": function_args["success"],
            "attestation_artifact": attestation_artifact,
            "reasoning": function_args["reasoning"],
            "metadata": metadata
        }
    
    def _create_verification_prompt(self, statistics_content: Dict[str, Any], 
                                   work_content: Dict[str, Any],
                                   csv_content: str) -> str:
        """Create the verification prompt for the LLM"""
        return f"""
Verify the following statistical analysis by re-executing the provided code and checking the calculations.

STATISTICAL RESULTS:
{json.dumps(statistics_content, indent=2)}

EXECUTED CODE:
{work_content['executed_code']}

CLAIMED OUTPUT:
{work_content['execution_output']}

CSV DATA (first 10 lines):
{csv_content.split(chr(10))[:10]}

VERIFICATION INSTRUCTIONS:
1. Re-execute the provided statistical code internally
2. Compare your results with the claimed output
3. Verify the mathematical correctness of all statistical calculations
4. Check for appropriate use of statistical tests
5. Validate the CSV data generation
6. Check for any logical errors or inconsistencies
7. Call the record_statistical_attestation tool with your verification results

If verification fails, provide detailed reasoning about what went wrong.
If verification succeeds, confirm the statistical calculations are correct.

For the tool call, provide:
- success: true/false based on your verification
- verifier_model: the model you're using
- verifier_model_version: the version
- reasoning: detailed explanation of your verification process
- executed_code_digest_sha256: SHA-256 hash of the code you verified
- statistics_digest_sha256: SHA-256 hash of the statistics you verified
- re_execution_output: the output from your re-execution (if different from claimed)
"""
    
    def _save_statistical_attestation_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the statistical attestation results as a clean artifact"""
        attestation_data = {
            "success": function_args["success"],
            "verifier_model": function_args["verifier_model"],
            "verifier_model_version": function_args.get("verifier_model_version", "unknown"),
            "reasoning": function_args["reasoning"],
            "executed_code_digest_sha256": function_args.get("executed_code_digest_sha256"),
            "statistics_digest_sha256": function_args.get("statistics_digest_sha256"),
            "re_execution_output": function_args.get("re_execution_output"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(attestation_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "statistical_attestation",
            "verifier_model": function_args["verifier_model"]
        })
