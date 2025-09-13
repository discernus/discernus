#!/usr/bin/env python3
"""
Verification Agent for Show Your Work Architecture
=================================================

This agent performs adversarial verification of analysis work by re-executing
code and comparing results using a separate LLM.
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


class VerificationAgent:
    """Verification Agent using tool calling for adversarial attestation"""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "VerificationAgent"
        
        # Initialize enhanced LLM gateway
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["adversarial_verification", "code_re_execution", "attestation"]
        })

    def verify_analysis(self, 
                       analysis_artifact_id: str, 
                       work_artifact_id: str,
                       model: str = None) -> Dict[str, Any]:
        """Verify an analysis by re-executing the code and comparing results"""
        
        # Select verifier model (Phase 2: specialized verifiers, Phase 1: fallback to Gemini)
        if model is None:
            model = self._select_verifier_model()
        
        # Load the artifacts
        analysis_data = self.storage.get_artifact(analysis_artifact_id)
        work_data = self.storage.get_artifact(work_artifact_id)
        
        if not analysis_data or not work_data:
            raise ValueError("Could not load required artifacts")
        
        analysis_content = json.loads(analysis_data.decode('utf-8'))
        work_content = json.loads(work_data.decode('utf-8'))
        
        document_id = analysis_content.get('document_id', 'unknown')
        
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
            "document_id": document_id,
            "analysis_artifact": analysis_artifact_id,
            "work_artifact": work_artifact_id
        })
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools,
            context=f"Verifying analysis for document {document_id}"
        )
        
        if not metadata.get('success'):
            raise Exception(f"Verification LLM call failed: {metadata.get('error', 'Unknown error')}")
        
        # Extract tool calls from response
        tool_calls = metadata.get('tool_calls', [])
        if not tool_calls:
            raise Exception("No tool calls found in verification response")
        
        # Process the first tool call (should be record_attestation)
        tool_call = tool_calls[0]
        if tool_call.get('function', {}).get('name') != 'record_attestation':
            raise Exception(f"Expected record_attestation tool call, got: {tool_call.get('function', {}).get('name')}")
        
        # Parse the tool call arguments
        function_args = json.loads(tool_call['function']['arguments'])
        
        # Save attestation artifact
        attestation_artifact = self._save_attestation_artifact(function_args)
        
        self.audit.log_agent_event(self.agent_name, "verification_complete", {
            "document_id": function_args["document_id"],
            "success": function_args["success"],
            "attestation_artifact": attestation_artifact,
            "usage": metadata.get('usage', {})
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
If verification succeeds, confirm the calculations are correct.

For the tool call, provide:
- document_id: {analysis_content.get('document_id', 'unknown')}
- success: true/false based on your verification
- verifier_model: the model you're using
- verifier_model_version: the version
- reasoning: detailed explanation of your verification process
- executed_code_digest_sha256: SHA-256 hash of the code you verified
- analysis_digest_sha256: SHA-256 hash of the analysis you verified
- re_execution_output: the output from your re-execution (if different from claimed)
"""
    
    def _save_attestation_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the attestation results as a clean artifact"""
        attestation_data = {
            "document_id": function_args["document_id"],
            "success": function_args["success"],
            "verifier_model": function_args["verifier_model"],
            "verifier_model_version": function_args.get("verifier_model_version", "unknown"),
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
    
    def _select_verifier_model(self) -> str:
        """Select the appropriate verifier model based on availability and phase"""
        try:
            # Try to get specialized verifier models from registry
            registry = ModelRegistry()
            available_models = registry.list_models()
            
            # Phase 2: Try specialized verifiers first
            primary_verifier = "openrouter/deepseek/deepseek-prover-v2"
            secondary_verifier = "openrouter/meta-llama/llama-3.1-405b-instruct"
            
            if primary_verifier in available_models:
                self.audit.log_agent_event(self.agent_name, "model_selection", {
                    "selected_model": primary_verifier,
                    "selection_reason": "primary_verifier_available",
                    "phase": "phase_2"
                })
                return primary_verifier
            
            if secondary_verifier in available_models:
                self.audit.log_agent_event(self.agent_name, "model_selection", {
                    "selected_model": secondary_verifier,
                    "selection_reason": "secondary_verifier_available",
                    "phase": "phase_2"
                })
                return secondary_verifier
            
            # Phase 1: Fallback to Gemini Pro
            fallback_model = "vertex_ai/gemini-2.5-pro"
            if fallback_model in available_models:
                self.audit.log_agent_event(self.agent_name, "model_selection", {
                    "selected_model": fallback_model,
                    "selection_reason": "specialized_verifiers_unavailable",
                    "phase": "phase_1"
                })
                return fallback_model
            
            # Last resort: Gemini Flash
            last_resort = "vertex_ai/gemini-2.5-flash"
            self.audit.log_agent_event(self.agent_name, "model_selection", {
                "selected_model": last_resort,
                "selection_reason": "fallback_models_unavailable",
                "phase": "phase_1"
            })
            return last_resort
            
        except Exception as e:
            # If registry fails, use Gemini Pro as safe fallback
            self.audit.log_agent_event(self.agent_name, "model_selection_error", {
                "error": str(e),
                "fallback_model": "vertex_ai/gemini-2.5-pro"
            })
            return "vertex_ai/gemini-2.5-pro"
