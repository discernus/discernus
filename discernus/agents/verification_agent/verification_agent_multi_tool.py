#!/usr/bin/env python3
"""
Verification Agent - Multi-Tool Implementation
==============================================

Implements adversarial attestation for the Show Your Work architecture.
Verifies the computational work and analysis results from EnhancedAnalysisAgentMultiTool.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class VerificationAgentMultiTool:
    """
    Verification Agent using adversarial attestation approach.

    Verifies the computational work from EnhancedAnalysisAgentMultiTool by:
    1. Reading analysis_scores.json, evidence_quotes.json, computational_work.json
    2. Re-executing the code from computational_work.json
    3. Comparing results with claimed outputs
    4. Generating attestation.json with verification results
    """

    def __init__(
        self,
        security_boundary: ExperimentSecurityBoundary,
        audit_logger: AuditLogger,
        storage: LocalArtifactStorage,
        llm_gateway: EnhancedLLMGateway,
        model: str = "vertex_ai/gemini-2.5-pro"  # Initially same as primary, later specialized verifiers
    ):
        self.security_boundary = security_boundary
        self.audit_logger = audit_logger
        self.storage = storage
        self.llm_gateway = llm_gateway
        self.model = model

        # Load prompt template
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        """Load the verification prompt template"""
        prompt_path = Path(__file__).parent / "prompt_verification_multi_tool.txt"
        if prompt_path.exists():
            return prompt_path.read_text()
        else:
            # Fallback prompt
            return """
You are a verification agent responsible for validating the computational work and analysis results from another LLM. Your task is to independently verify the claims made in the provided artifacts.

VERIFICATION TASKS:
1. Read and understand the analysis_scores.json, evidence_quotes.json, and computational_work.json
2. Re-execute the Python code from computational_work.json
3. Compare your results with the claimed outputs
4. Assess the validity of the evidence quotes
5. Generate a comprehensive attestation

VERIFICATION CRITERIA:
- Code execution must produce the claimed output
- Derived metrics must be mathematically correct
- Evidence quotes must be reasonable for the claimed scores
- Analysis must be internally consistent

ARTIFACTS TO VERIFY:
{analysis_scores_json}
{evidence_quotes_json}
{computational_work_json}

Call the record_attestation tool with your verification results.
"""

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get the attestation tool schema for structured output"""
        return [{
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
                        "evidence_digest_sha256": {"type": "string"},
                        "re_execution_output": {"type": "string"},
                        "discrepancies_found": {"type": "array", "items": {"type": "string"}},
                        "confidence_level": {"type": "string", "enum": ["high", "medium", "low"]},
                        "verification_details": {
                            "type": "object",
                            "properties": {
                                "code_execution_success": {"type": "boolean"},
                                "output_match": {"type": "boolean"},
                                "evidence_consistency": {"type": "boolean"},
                                "mathematical_accuracy": {"type": "boolean"}
                            }
                        }
                    },
                    "required": ["document_id", "success", "verifier_model", "reasoning"]
                }
            }
        }]

    def _create_verification_prompt(
        self,
        analysis_scores_json: str,
        evidence_quotes_json: str,
        computational_work_json: str
    ) -> str:
        """Create the verification prompt with artifact contents"""
        return self.prompt_template.format(
            analysis_scores_json=analysis_scores_json,
            evidence_quotes_json=evidence_quotes_json,
            computational_work_json=computational_work_json
        )

    def _save_attestation_artifact(self, attestation_data: Dict[str, Any]) -> str:
        """Save attestation artifact"""
        # Convert to JSON bytes
        json_data = json.dumps(attestation_data, indent=2, sort_keys=True)
        artifact_hash = self.storage.put_artifact(
            content=json_data.encode('utf-8'),
            metadata={
                "artifact_type": "attestation",
                "source_agent": "VerificationAgentMultiTool"
            }
        )
        return artifact_hash

    def _load_artifact_content(self, artifact_hash: str) -> str:
        """Load and return artifact content as formatted JSON string"""
        try:
            content_bytes = self.storage.get_artifact(artifact_hash)
            content_dict = json.loads(content_bytes.decode('utf-8'))
            return json.dumps(content_dict, indent=2)
        except Exception as e:
            return f"Error loading artifact {artifact_hash}: {e}"

    def verify_artifacts(
        self,
        analysis_scores_hash: str,
        evidence_quotes_hash: str,
        computational_work_hash: str
    ) -> Dict[str, Any]:
        """
        Verify the computational work and analysis results.

        Args:
            analysis_scores_hash: SHA-256 hash of analysis_scores.json
            evidence_quotes_hash: SHA-256 hash of evidence_quotes.json
            computational_work_hash: SHA-256 hash of computational_work.json

        Returns:
            Dictionary containing verification results and attestation artifact hash
        """
        try:
            # Load artifact contents
            analysis_scores_json = self._load_artifact_content(analysis_scores_hash)
            evidence_quotes_json = self._load_artifact_content(evidence_quotes_hash)
            computational_work_json = self._load_artifact_content(computational_work_hash)

            # Get document ID from analysis scores
            try:
                analysis_data = json.loads(analysis_scores_json)
                document_id = analysis_data.get("document_id", "unknown")
            except:
                document_id = "unknown"

            # Log verification start
            self.audit_logger.log_agent_event(
                agent_name="VerificationAgentMultiTool",
                event_type="verification_start",
                data={
                    "document_id": document_id,
                    "analysis_scores_hash": analysis_scores_hash,
                    "evidence_quotes_hash": evidence_quotes_hash,
                    "computational_work_hash": computational_work_hash,
                    "model": self.model
                }
            )

            # Create verification prompt
            prompt = self._create_verification_prompt(
                analysis_scores_json,
                evidence_quotes_json,
                computational_work_json
            )

            # Get tools schema
            tools = self._get_tools_schema()

            # Execute LLM verification
            print(f"   🔍 Sending verification prompt to {self.model}...")
            response, metadata = self.llm_gateway.execute_call_with_tools(
                model=self.model,
                prompt=prompt,
                system_prompt="You are a verification agent. Carefully analyze the provided artifacts and call the record_attestation tool with your findings. Be thorough and honest in your assessment.",
                tools=tools,
                force_function_calling=True  # Force the model to make function calls (ANY mode)
            )
            tool_calls_list = metadata.get('tool_calls') or []
            print(f"   📥 Received response: success={metadata.get('success', False)}, tool_calls={len(tool_calls_list)}")

            # Log verification complete
            self.audit_logger.log_agent_event(
                agent_name="VerificationAgentMultiTool",
                event_type="verification_complete",
                data={
                    "document_id": document_id,
                    "success": metadata.get('success', False),
                    "tool_calls": len(tool_calls_list),
                    "usage": metadata.get('usage', {})
                }
            )

            if not metadata.get('success') or not tool_calls_list:
                raise Exception(f"LLM verification failed: {metadata.get('error', 'Unknown error')}")

            # Process tool calls
            tool_calls = tool_calls_list
            print(f"   🔧 Processing {len(tool_calls)} tool calls...")
            if len(tool_calls) != 1:
                print(f"   ❌ Expected 1 tool call, got {len(tool_calls)}")
                for i, tc in enumerate(tool_calls):
                    if hasattr(tc, 'function'):
                        print(f"      Tool {i}: {tc.function.name}")
                    else:
                        print(f"      Tool {i}: No function attribute")
                raise Exception(f"Expected 1 tool call, got {len(tool_calls)}")

            # Extract attestation data
            tool_call = tool_calls[0]
            print(f"   🔧 Tool call: {tool_call}")
            if hasattr(tool_call, 'function'):
                print(f"   🔧 Function name: {tool_call.function.name}")
                if tool_call.function.name == "record_attestation":
                    attestation_data = json.loads(tool_call.function.arguments)
                    print(f"   ✅ Successfully parsed attestation data")

                    # Add additional metadata
                    attestation_data.update({
                        "verifier_model": self.model,
                        "verifier_model_version": "1.0",
                        "executed_code_digest_sha256": computational_work_hash,
                        "analysis_digest_sha256": analysis_scores_hash,
                        "evidence_digest_sha256": evidence_quotes_hash
                    })

                    # Save attestation artifact
                    attestation_hash = self._save_attestation_artifact(attestation_data)

                    # Return results
                    return {
                        "success": True,
                        "document_id": document_id,
                        "attestation_artifact": attestation_hash,
                        "verification_success": attestation_data.get("success", False),
                        "confidence_level": attestation_data.get("confidence_level", "unknown"),
                        "discrepancies_found": attestation_data.get("discrepancies_found", []),
                        "usage": metadata.get('usage', {})
                    }
                else:
                    print(f"   ❌ Expected 'record_attestation', got '{tool_call.function.name}'")
                    raise Exception(f"Invalid tool call: expected 'record_attestation', got '{tool_call.function.name}'")
            else:
                print(f"   ❌ Tool call has no function attribute")
                raise Exception("Invalid tool call received")

        except Exception as e:
            # Log error
            self.audit_logger.log_agent_event(
                agent_name="VerificationAgentMultiTool",
                event_type="verification_error",
                data={
                    "document_id": document_id if 'document_id' in locals() else "unknown",
                    "error": str(e)
                }
            )
            raise
