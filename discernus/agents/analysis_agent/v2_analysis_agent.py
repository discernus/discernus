#!/usr/bin/env python3
"""
V2 Analysis Agent - Atomic Processing Implementation
==================================================

This agent processes documents atomically - each document gets its own artifacts
for all 6 analysis steps. This prevents token limit issues and ensures proper
atomic processing.

THIN Principles:
- Each document processed individually through all 6 steps
- No batch processing that could hit token limits
- Clean separation of concerns
- Atomic artifacts for downstream consumption
"""

import json
import logging
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.core.unified_logger import get_unified_logger
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2AnalysisAgent(StandardAgent):
    """
    V2 Analysis Agent with atomic document processing.
    
    This agent processes each document individually through all 6 analysis steps:
    1. Composite Analysis
    2. Evidence Extraction  
    3. Score Extraction
    4. Derived Metrics Generation
    5. Verification
    6. Markup Extraction
    
    Each document gets its own set of artifacts, preventing token limit issues.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Analysis Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2AnalysisAgent"
        
        # Initialize LLM gateway
        model_registry = get_model_registry()
        self.gateway = LLMGateway(model_registry)
        
        # Initialize unified logger
        self.unified_logger = get_unified_logger()
        
        # Load YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Log initialization
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "agent_type": "V2AnalysisAgent",
            "config_keys": []
        })

    def _load_prompt_template(self) -> str:
        """Load the framework-agnostic prompt template from the YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            error_msg = f"V2AnalysisAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']

    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return [
            "composite_analysis_with_markup",
            "evidence_extraction", 
            "score_extraction",
            "derived_metrics",
            "verification",
            "markup_extraction"
        ]

    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """
        Execute atomic document analysis.
        
        Args:
            run_context: Run context with experiment data
            **kwargs: Additional arguments
            
        Returns:
            AgentResult with analysis artifacts
        """
        try:
            # Extract data from run context
            framework_content = run_context.metadata.get("framework_content")
            corpus_documents = run_context.metadata.get("corpus_documents", [])

            if not framework_content:
                return AgentResult(
                    success=False,
                    error_message="No framework content provided",
                    metadata={"agent_name": self.agent_name}
                )

            if not corpus_documents:
                return AgentResult(
                    success=False,
                    error_message="No corpus documents provided", 
                    metadata={"agent_name": self.agent_name}
                )

            # Generate batch ID for this analysis
            batch_id = f"v2_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Process documents atomically - each document gets its own artifacts
            self.logger.info(f"Starting atomic document processing for batch {batch_id}")
            documents = corpus_documents
            all_artifacts = []
            
            for doc_index, doc in enumerate(documents):
                doc_name = doc.get('id', doc.get('name', doc.get('filename', f'document_{doc_index}')))
                self.logger.info(f"Processing document {doc_index}: {doc_name}")
                
                # Process this document atomically through all 6 steps
                doc_artifacts = self._process_document_atomically(
                    framework_content, doc, doc_index, batch_id
                )
                all_artifacts.extend(doc_artifacts)
            
            # Update RunContext with analysis artifacts for downstream agents
                artifact_hashes = []
            for artifact in all_artifacts:
                if 'metadata' in artifact and 'artifact_hash' in artifact['metadata']:
                    artifact_hashes.append(artifact['metadata']['artifact_hash'])

            # Update run context
                run_context.analysis_artifacts = artifact_hashes
            run_context.analysis_results = {
                "documents_processed": len(documents),
                "processing_mode": "atomic",
                "batch_id": batch_id
            }

            self.logger.info(f"Updated run_context with {len(artifact_hashes)} analysis artifacts: {artifact_hashes}")

            # Return results from atomic processing
            return AgentResult(
                success=True,
                artifacts=all_artifacts,
                metadata={
                    "batch_id": batch_id,
                    "documents_processed": len(documents),
                    "agent_name": self.agent_name,
                    "processing_mode": "atomic"
                }
            )
                
        except Exception as e:
            self.logger.error(f"V2AnalysisAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "analysis_failed", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name},
                error_message=f"V2AnalysisAgent execution failed: {str(e)}"
            )

    def _process_document_atomically(self, 
                                   framework_content: str, 
                                   doc: Dict[str, Any], 
                                   doc_index: int, 
                                   batch_id: str) -> List[Dict[str, Any]]:
        """
        Process a single document through all 6 analysis steps atomically.
        
        Args:
            framework_content: Framework content for analysis
            doc: Document to process
            doc_index: Index of document in corpus
            batch_id: Batch identifier
        
        Returns:
            List of artifacts created for this document
        """
        artifacts = []
        
        try:
            # Step 1: Composite Analysis
            composite_result = self._step1_composite_analysis(framework_content, doc, doc_index, batch_id)
            if composite_result:
                artifacts.append(composite_result)
            
            # Step 2: Evidence Extraction
            evidence_result = self._step2_evidence_extraction(composite_result, doc_index, batch_id)
            if evidence_result:
                artifacts.append(evidence_result)
            
            # Step 3: Score Extraction
            scores_result = self._step3_score_extraction(composite_result, doc_index, batch_id)
            if scores_result:
                artifacts.append(scores_result)
            
            # Step 4: Derived Metrics Generation
            derived_metrics_result = self._step4_derived_metrics(framework_content, scores_result, doc_index, batch_id)
            if derived_metrics_result:
                artifacts.append(derived_metrics_result)
            
            # Step 5: Verification
            verification_result = self._step5_verification(framework_content, derived_metrics_result, scores_result, doc_index, batch_id)
            if verification_result:
                artifacts.append(verification_result)
                
                # Check if verification failed - if so, fail fast for this document
                verification_status = verification_result.get('content', {}).get('verification_status', 'unknown')
                if verification_status != "verified":
                    self.unified_logger.verification_failed(doc_index, verification_status)
                    self.audit.log_agent_event(self.agent_name, "verification_failed", {
                        "document_index": doc_index,
                        "verification_status": verification_status,
                        "batch_id": batch_id
                    })
                    # Return artifacts created so far, but mark as failed for this document
                    return artifacts
            else:
                self.logger.error(f"Verification step failed for document {doc_index}")
                return artifacts
            
            # Step 6: Markup Extraction
            markup_result = self._step6_markup_extraction(composite_result, doc_index, batch_id)
            if markup_result:
                artifacts.append(markup_result)
                
        except Exception as e:
            self.logger.error(f"Atomic processing failed for document {doc_index}: {e}")
            self.audit.log_agent_event(self.agent_name, "atomic_processing_failed", {
                "document_index": doc_index,
                "error": str(e)
            })
        
        return artifacts

    def _step1_composite_analysis(self, framework_content: str, doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 1: Composite Analysis for a single document."""
        try:
            # Create analysis prompt using YAML template
            document_content = doc.get('content', '')
            prompt = self.prompt_template.replace('{framework_content}', framework_content).replace('{document_content}', document_content)

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "composite_analysis",
                "model_used": "vertex_ai/gemini-2.5-flash",
                "raw_analysis_response": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "composite_analysis", "document_index": doc_index}
            )
            
            return {
                "type": "composite_analysis",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "composite_analysis",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 1 failed for document {doc_index}: {e}")
            return None

    def _step2_evidence_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 2: Extract evidence from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            prompt = f"""You are extracting ALL evidence quotes from a discourse analysis. 

ANALYSIS RESULT:
{raw_response}

TASK: Extract ALL evidence quotes from the analysis result. Do NOT curate or select - extract every single quote that appears in the evidence_quotes sections.

REQUIREMENTS:
- Extract EVERY quote from ALL dimensional evidence_quotes sections
- Do NOT curate, select, or filter quotes
- Include ALL quotes regardless of quality or redundancy
- Count the total number of quotes in the composite analysis
- Count the total number of quotes in your output
- Ensure the counts match exactly
- Format as a simple JSON array of strings

OUTPUT FORMAT:
["quote1", "quote2", "quote3", ...]

Return ONLY the JSON array, no other text."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-pro",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # THIN: Store LLM response as-is, no validation
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "evidence_extraction",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "evidence_extraction": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "evidence_extraction", "document_index": doc_index}
            )
            
            return {
                "type": "evidence_extraction",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "evidence_extraction",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 2 failed for document {doc_index}: {e}")
            return None

    def _step3_score_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 3: Extract scores from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            prompt = f"""Extract the dimensional scores from this analysis result:

{raw_response}

Return the scores as a JSON object with dimension names as keys and score values as numbers."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "score_extraction",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "score_extraction": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "score_extraction", "document_index": doc_index}
            )
            
            return {
                "type": "score_extraction",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "score_extraction",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 3 failed for document {doc_index}: {e}")
            return None

    def _step4_derived_metrics(self, framework_content: str, scores_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 4: Generate derived metrics from scores."""
        try:
            if not scores_result or 'content' not in scores_result:
                return None
                
            scores = scores_result['content'].get('score_extraction', '')
            
            # First, check if the framework defines any derived metrics
            if not self._framework_defines_derived_metrics(framework_content):
                self.logger.info(f"Framework defines no derived metrics - creating 'no derived metrics' artifact for document {doc_index}")
                
                # Create artifact indicating no derived metrics are defined
                artifact_data = {
                    "analysis_id": f"analysis_{batch_id}_{doc_index}",
                    "step": "derived_metrics",
                    "model_used": "N/A",
                    "derived_metrics": "Framework defines no derived metrics - skipping calculation",
                    "has_derived_metrics": False,
                    "document_index": doc_index,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                # Store artifact
                content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
                artifact_hash = self.storage.put_artifact(
                    content_bytes,
                    {"artifact_type": "derived_metrics", "document_index": doc_index}
                )
                
                return {
                    "type": "derived_metrics",
                    "content": artifact_data,
                    "metadata": {
                        "artifact_type": "derived_metrics",
                        "phase": "analysis",
                        "batch_id": batch_id,
                        "document_index": doc_index,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": artifact_hash
                    }
                }
            
            prompt = f"""Generate Python code to calculate derived metrics from these dimensional scores.

FRAMEWORK:
{framework_content}

SCORES:
{scores}

STRICT OUTPUT FORMAT (MANDATORY - NO PROSE):
- Output EXACTLY two fenced blocks back-to-back and NOTHING ELSE.
- Block 1: Python code that computes a dictionary named results containing only numeric derived metrics.
- Block 2: A single compact JSON object with the exact content of results, under key results.

Example (structure only):
```python
# must define a dict named `results` with numeric values
results = {{"metric_a": 0.123, "metric_b": 0.456}}
print(json.dumps({{"results": results}}, separators=(",", ":")))
```
```json
{{"results":{{"metric_a":0.123,"metric_b":0.456}}}}
```

REQUIREMENTS:
- Use provided SCORES; implement the framework formulas deterministically
- results keys must be snake_case metric names; values numeric (floats)
- Do not include any narrative, headings, or extra text outside the two blocks
"""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "derived_metrics",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "derived_metrics": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "derived_metrics", "document_index": doc_index}
            )
            
            return {
                "type": "derived_metrics",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "derived_metrics",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 4 failed for document {doc_index}: {e}")
            return None

    def _step5_verification(self, framework_content: str, derived_metrics_result: Dict[str, Any], scores_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 5: Verify derived metrics calculations using tool calling."""
        try:
            if not derived_metrics_result or 'content' not in derived_metrics_result:
                return None
                
            derived_metrics = derived_metrics_result['content'].get('derived_metrics', '')
            scores = scores_result['content'].get('score_extraction', '') if scores_result else '{}'
            
            # Check if derived metrics step indicated no derived metrics are defined
            if derived_metrics_result['content'].get('has_derived_metrics') == False:
                self.logger.info(f"Skipping verification for document {doc_index} - no derived metrics defined")
                return {
                    "type": "verification",
                    "content": {
                        "analysis_id": f"analysis_{batch_id}_{doc_index}",
                        "step": "verification",
                        "model_used": "N/A",
                        "verification_status": "skipped",
                        "verified": True,
                        "reasoning": "Framework defines no derived metrics - verification skipped",
                        "document_index": doc_index,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    },
                    "metadata": {
                        "artifact_type": "verification",
                        "phase": "analysis",
                        "batch_id": batch_id,
                        "document_index": doc_index,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name
                    }
                }
            
            
            # Define verification tool (OpenAI function calling format)
            verification_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "verify_math",
                        "description": "Verify mathematical calculations by re-executing code and comparing results",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "verified": {
                                    "type": "boolean",
                                    "description": "True if calculations are correct, False if incorrect"
                                },
                                "reasoning": {
                                    "type": "string", 
                                    "description": "Detailed explanation of verification process and findings"
                                }
                            },
                            "required": ["verified", "reasoning"]
                        }
                    }
                }
            ]
            
            prompt = f"""You will receive two fenced blocks back-to-back and nothing else:
1) Python code that prints a compact JSON object {{"results": {{...}}}}
2) A compact JSON object {{"results": {{...}}}}

Task:
- Re-execute the Python code in a clean environment
- Parse the JSON block
- Compare the recomputed results to the provided JSON for mathematical reasonableness
- Use APA standard: compare within 2 decimal places for precision
- Focus on whether the calculation logic is sound rather than exact numerical precision
- If mathematically reasonable within 2 decimal places, set verified=true; else verified=false
- Provide concise reasoning

CONTENT:
{derived_metrics}

Call verify_math tool with fields: verified (bool), reasoning (string)."""

            self.audit.log_agent_event(self.agent_name, "step5_started", {
                "batch_id": batch_id,
                "document_index": doc_index,
                "step": "verification",
                "model": "vertex_ai/gemini-2.5-pro"
            })

            # System prompt emphasizing mandatory tool call
            system_prompt = "You are a verification specialist. You MUST re-execute the provided code, verify the calculations, and call the verify_math tool with your findings. This is MANDATORY - you must call the verify_math tool."
            
            # Call LLM with tools (using proper EnhancedLLMGateway format)
            response_content, metadata = self.gateway.execute_call_with_tools(
                model="vertex_ai/gemini-2.5-pro",  # Pro for reliability on verification
                prompt=prompt,
                system_prompt=system_prompt,
                tools=verification_tools,
                force_function_calling=True,  # Force tool calling like deprecated agent
                context=f"Verifying derived metrics for document {doc_index}"
            )
            
            # Emit detailed audit event capturing LLM call outcome for debugging
            try:
                self.audit.log_agent_event(self.agent_name, "verification_llm_result", {
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "step": "verification",
                    "model": metadata.get("model") if isinstance(metadata, dict) else None,
                    "success": metadata.get("success") if isinstance(metadata, dict) else None,
                    "error": metadata.get("error") if isinstance(metadata, dict) else None,
                    "attempts": metadata.get("attempts") if isinstance(metadata, dict) else None,
                    "tool_calls_count": len(metadata.get("tool_calls", [])) if isinstance(metadata, dict) else 0,
                    "usage": metadata.get("usage", {}) if isinstance(metadata, dict) else {}
                })
            except Exception:
                # Audit logging failures should never break the verification step
                pass
            
            # Extract verification result from tool calls (using metadata format like deprecated agent)
            verification_status = "unknown"
            verified_flag = None
            verified_reasoning = None
            if not metadata.get('success'):
                self.logger.error(f"Verification LLM call failed: {metadata.get('error', 'Unknown error')}")
                verification_status = "verification_error"
            else:
                tool_calls = metadata.get('tool_calls', [])
                if tool_calls:
                    tool_call = tool_calls[0]
                    # Support both object and dict shapes from LiteLLM providers
                    try:
                        if isinstance(tool_call, dict):
                            fn = tool_call.get("function", {})
                            fn_name = fn.get("name")
                            fn_args = fn.get("arguments")
                        else:
                            fn_name = getattr(getattr(tool_call, "function", None), "name", None)
                            fn_args = getattr(getattr(tool_call, "function", None), "arguments", None)
                        if fn_name == "verify_math" and fn_args is not None:
                            try:
                                args = json.loads(fn_args)
                                verified_flag = bool(args.get("verified", False))
                                verified_reasoning = args.get("reasoning", None)
                                verification_status = "verified" if verified_flag else "verification_error"
                                if verified_reasoning:
                                    self.logger.info(f"Verification reasoning: {verified_reasoning}")
                            except json.JSONDecodeError as e:
                                self.logger.error(f"Failed to parse tool call arguments: {e}")
                                verification_status = "verification_error"
                        else:
                            self.logger.error("Verification tool call not found or missing arguments")
                            verification_status = "verification_error"
                    except Exception as e:
                        self.logger.error(f"Error reading tool call structure: {e}")
                        verification_status = "verification_error"
                else:
                    self.logger.error("No tool calls found in verification response")
                    verification_status = "verification_error"
            
            # Create artifact with verification status
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "verification",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "verification_status": verification_status,
                "verified": verified_flag,
                "reasoning": verified_reasoning,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "verification", "document_index": doc_index}
            )
            
            artifact_data['artifact_hash'] = artifact_hash
            
            self.audit.log_agent_event(self.agent_name, "step5_completed", {
                "batch_id": batch_id,
                "document_index": doc_index,
                "step": "verification",
                "artifact_hash": artifact_hash,
                "verification_status": verification_status,
                "verified": verified_flag
            })
            
            return {
                "type": "verification",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "verification",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash,
                    "verification_status": verification_status
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 5 failed for document {doc_index}: {e}")
            return None
    
    def _framework_defines_derived_metrics(self, framework_content: str) -> bool:
        """
        Check if the framework defines derived metrics using LLM intelligence.
        
        Returns True if the framework defines derived metrics, False otherwise.
        """
        try:
            prompt = f"""
            Examine this framework and determine if it defines any derived metrics.
            
            Framework content:
            {framework_content}
            
            Look for:
            - Derived metrics definitions
            - Calculated metrics
            - Composite metrics
            - Any metrics that are computed from other metrics
            
            Respond with only "YES" if derived metrics are defined, or "NO" if not.
            """
            
            response, metadata = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are a framework analysis expert. Answer only YES or NO.",
                max_retries=1
            )
            
            if metadata.get("success") and response:
                return response.strip().upper() == "YES"
            
            # If check fails, assume derived metrics exist to be safe
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to check for derived metrics: {e}")
            # If check fails, assume derived metrics exist to be safe
            return True
    

    def _step6_markup_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 6: Extract markup from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            prompt = f"""Extract the marked-up document from this analysis result:

{raw_response}

Return the marked-up document in markdown format."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "markup_extraction",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "marked_up_document": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "marked_up_document", "document_index": doc_index}
            )
            
            return {
                "type": "marked_up_document",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "marked_up_document",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 6 failed for document {doc_index}: {e}")
            return None
    

