#!/usr/bin/env python3
"""
V2 Statistical Agent - Atomic Processing Implementation
=====================================================

This agent processes atomic score and derived metrics artifacts from the AnalysisAgent
and performs comprehensive statistical analysis.

THIN Principles:
- Each document's scores are processed individually
- LLM handles all statistical intelligence
- Agent only adapts interfaces, no business logic
- Atomic artifacts for downstream consumption
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2StatisticalAgent(StandardAgent):
    """
    V2 Statistical Agent for atomic processing of score artifacts.
    
    This agent processes individual score and derived metrics artifacts
    from the AnalysisAgent and performs comprehensive statistical analysis.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2StatisticalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        self.logger.info(f"Initialized {self.agent_name}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and metadata.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": "V2StatisticalAgent",
            "capabilities": [
                "statistical_analysis",
                "statistical_verification",
                "atomic_score_processing"
            ],
            "input_types": ["score_extraction_artifacts", "derived_metrics_artifacts"],
            "output_types": ["statistical_analysis", "statistical_verification"],
            "models_used": ["vertex_ai/gemini-2.5-pro", "vertex_ai/gemini-2.5-flash-lite"]
        }
    
    def execute(self, run_context: RunContext) -> AgentResult:
        """
        Execute statistical analysis on atomic score artifacts.
        
        Args:
            run_context: Run context containing analysis artifacts and metadata
            
        Returns:
            AgentResult with statistical analysis artifacts
        """
        try:
            self.logger.info("Starting V2 Statistical Agent execution")
            self.audit.log_agent_event(self.agent_name, "execution_started", {
                "run_context_type": type(run_context).__name__
            })
            
            # Validate run context
            if not run_context:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "run_context is required"},
                    error_message="run_context is required"
                )
            
            # Extract data from RunContext
            framework_content = run_context.metadata.get("framework_content")
            if not framework_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "framework_content not found"},
                    error_message="framework_content not found in RunContext"
                )
            
            # Get analysis artifacts (list of artifact hashes)
            analysis_artifacts = run_context.analysis_artifacts
            self.logger.info(f"Received analysis_artifacts: {analysis_artifacts}")
            if not analysis_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "analysis_artifacts not found"},
                    error_message="analysis_artifacts not found in RunContext"
                )
            
            # Process atomic score artifacts
            score_data = self._collect_atomic_scores(analysis_artifacts)
            if not score_data:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no score data found"},
                    error_message="No score data found in analysis artifacts"
                )
            
            # Generate batch ID
            batch_id = f"stats_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            
            # Step 1: Statistical Analysis (Python code generation + execution)
            statistical_analysis_content = self._step1_statistical_analysis(framework_content, score_data, batch_id)
            if not statistical_analysis_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical analysis failed"},
                    error_message="Statistical analysis failed"
                )
            
            # Store Step 1 artifact
            statistical_artifact_data = {
                "analysis_id": f"stats_{batch_id}",
                "step": "statistical_analysis",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "statistical_analysis_content": statistical_analysis_content,
                "documents_processed": len(score_data),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            statistical_content_bytes = json.dumps(statistical_artifact_data, indent=2).encode('utf-8')
            statistical_artifact_hash = self.storage.put_artifact(
                statistical_content_bytes,
                {"artifact_type": "statistical_analysis", "batch_id": batch_id}
            )
            
            # Step 2: Independent Verification
            verification_result = self._step2_verification(statistical_analysis_content, batch_id)
            if not verification_result:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical verification failed"},
                    error_message="Statistical verification failed"
                )
            
            # Check if verification passed
            if verification_result.get("verification_status") != "verified":
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical verification failed", "verification_status": verification_result.get("verification_status")},
                    error_message=f"Statistical verification failed: {verification_result.get('verification_status')}"
                )
            
            # Store verification artifact
            verification_artifact_data = {
                "analysis_id": f"stats_{batch_id}",
                "step": "statistical_verification",
                "model_used": "vertex_ai/gemini-2.5-flash-lite",
                "verification_result": verification_result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            verification_content_bytes = json.dumps(verification_artifact_data, indent=2).encode('utf-8')
            verification_artifact_hash = self.storage.put_artifact(
                verification_content_bytes,
                {"artifact_type": "statistical_verification", "batch_id": batch_id}
            )
            
            # Create artifacts list with proper hashes
            artifacts = [
                {
                    "type": "statistical_analysis",
                    "content": statistical_artifact_data,
                    "metadata": {
                        "artifact_type": "statistical_analysis",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": statistical_artifact_hash
                    }
                },
                {
                    "type": "statistical_verification",
                    "content": verification_artifact_data,
                    "metadata": {
                        "artifact_type": "statistical_verification",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": verification_artifact_hash
                    }
                }
            ]
            
            # Update run context with proper artifact hashes
            run_context.statistical_artifacts = [statistical_artifact_hash, verification_artifact_hash]
            run_context.statistical_results = statistical_analysis_content  # Pass the raw content to synthesis agent
            
            self.audit.log_agent_event(self.agent_name, "execution_completed", {
                "batch_id": batch_id,
                "artifacts_created": len(artifacts),
                "documents_processed": len(score_data)
            })
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "batch_id": batch_id,
                    "documents_processed": len(score_data),
                    "artifacts_created": len(artifacts)
                }
            )
            
        except Exception as e:
            self.logger.error(f"V2StatisticalAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "execution_failed", {
                "error": str(e)
            })
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2StatisticalAgent execution failed: {str(e)}"
            )
    
    def _collect_atomic_scores(self, analysis_artifacts: List[str]) -> List[Dict[str, Any]]:
        """
        Collect score data from atomic score extraction artifacts.
        
        Args:
            analysis_artifacts: List of artifact hashes from analysis phase
            
        Returns:
            List of score data dictionaries
        """
        self.logger.info(f"Collecting scores from {len(analysis_artifacts)} analysis artifacts")
        score_data = []
        
        for artifact_hash in analysis_artifacts:
            try:
                # Load artifact
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if not artifact_bytes:
                    self.logger.warning(f"Could not load artifact {artifact_hash}")
                    continue
                
                artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                self.logger.info(f"Processing artifact {artifact_hash}: step={artifact_data.get('step')}")
                
                # Check if this is a score extraction artifact
                if artifact_data.get("step") == "score_extraction":
                    # Extract the scores from the LLM response
                    scores_response = artifact_data.get("score_extraction", "")
                    if scores_response:
                        # Parse the JSON from the LLM response
                        try:
                            # Extract JSON from markdown code block if present
                            if "```json" in scores_response:
                                json_start = scores_response.find("```json") + 7
                                json_end = scores_response.find("```", json_start)
                                if json_end > json_start:
                                    scores_json = scores_response[json_start:json_end].strip()
                                else:
                                    scores_json = scores_response[json_start:].strip()
                            else:
                                scores_json = scores_response.strip()
                            
                            scores = json.loads(scores_json)
                            
                            # Add document metadata
                            score_data.append({
                                "document_index": artifact_data.get("document_index", 0),
                                "analysis_id": artifact_data.get("analysis_id", ""),
                                "scores": scores,
                                "timestamp": artifact_data.get("timestamp", ""),
                                "data_type": "scores"
                            })
                            
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Could not parse scores from artifact {artifact_hash}: {e}")
                            continue
                
                # Check if this is a derived metrics artifact
                elif artifact_data.get("step") == "derived_metrics":
                    # Check if this is a "no derived metrics" artifact
                    if artifact_data.get("has_derived_metrics") == False:
                        self.logger.info(f"Skipping derived metrics artifact {artifact_hash} - framework has no derived metrics")
                        continue
                    
                    # Extract the derived metrics from the LLM response
                    derived_metrics_response = artifact_data.get("derived_metrics", "")
                    if derived_metrics_response:
                        # Parse the JSON from the LLM response (similar to scores)
                        try:
                            # Extract JSON from the second code block (derived metrics contain both Python and JSON)
                            if "```json" in derived_metrics_response:
                                # Find the JSON block (usually the second one after the Python block)
                                json_blocks = []
                                start_pos = 0
                                while True:
                                    json_start = derived_metrics_response.find("```json", start_pos)
                                    if json_start == -1:
                                        break
                                    json_start += 7
                                    json_end = derived_metrics_response.find("```", json_start)
                                    if json_end > json_start:
                                        json_blocks.append(derived_metrics_response[json_start:json_end].strip())
                                    start_pos = json_end + 3
                                
                                # Use the last JSON block (the results)
                                if json_blocks:
                                    derived_metrics_json = json_blocks[-1]
                                    derived_metrics = json.loads(derived_metrics_json)
                                    
                                    # Extract the results if they're nested
                                    if "results" in derived_metrics:
                                        derived_metrics = derived_metrics["results"]
                                    
                                    # Add document metadata
                                    score_data.append({
                                        "document_index": artifact_data.get("document_index", 0),
                                        "analysis_id": artifact_data.get("analysis_id", ""),
                                        "scores": derived_metrics,
                                        "timestamp": artifact_data.get("timestamp", ""),
                                        "data_type": "derived_metrics"
                                    })
                                    
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Could not parse derived metrics from artifact {artifact_hash}: {e}")
                            continue
                
            except Exception as e:
                self.logger.warning(f"Error processing artifact {artifact_hash}: {e}")
                continue
        
        return score_data
    
    def _step1_statistical_analysis(self, framework_content: str, score_data: List[Dict[str, Any]], batch_id: str) -> Optional[str]:
        """
        Step 1: Generate Python statistical analysis code and execute it.
        
        Args:
            framework_content: Framework content for context
            score_data: List of score data from atomic artifacts
            batch_id: Batch identifier
            
        Returns:
            Complete LLM response with Python code and results, or None if failed
        """
        try:
            # Prepare statistical analysis prompt for Python code generation
            prompt = f"""You are a statistical analysis expert. Generate and execute Python code to analyze the following dimensional scores.

FRAMEWORK CONTEXT:
{framework_content}

SCORE DATA:
{json.dumps(score_data, indent=2)}

TASK: Write Python code to perform comprehensive statistical analysis including:
1. Descriptive statistics for each dimension
2. Correlation analysis between dimensions  
3. Statistical significance testing where appropriate
4. Summary of key findings

REQUIREMENTS:
- Use pandas, numpy, scipy.stats, and other standard libraries
- Write clear, well-commented Python code
- Execute the code and show the results
- Provide interpretations of the statistical findings
- Include any relevant plots or visualizations

Generate the Python code, execute it, and present both the code and results in a clear format that researchers can understand and audit."""

            self.audit.log_agent_event(self.agent_name, "step1_started", {
                "batch_id": batch_id,
                "step": "statistical_analysis",
                "model": "vertex_ai/gemini-2.5-pro",
                "documents_count": len(score_data)
            })
            
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
            
            # Return the complete LLM response (Python code + results + explanations)
            # No parsing - just store whatever the LLM produced
            if content and content.strip():
                self.audit.log_agent_event(self.agent_name, "step1_completed", {
                    "batch_id": batch_id,
                    "step": "statistical_analysis",
                    "response_length": len(content)
                })
                
                return content.strip()
            else:
                self.logger.error("Statistical analysis returned empty response")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed: {e}")
            return None
    
    def _step2_verification(self, statistical_analysis_content: str, batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Step 2: Independently verify statistical analysis by re-executing the Python code.
        
        Args:
            statistical_analysis_content: Complete response from step 1 with Python code and results
            batch_id: Batch identifier
            
        Returns:
            Verification result with tool call status or None if failed
        """
        try:
            # Define verification tool (OpenAI function calling format)
            verification_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "verify_statistical_analysis",
                        "description": "Evaluate if the statistical analysis is substantive and well-executed",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "verified": {
                                    "type": "boolean",
                                    "description": "Whether the statistical analysis appears substantive and methodologically sound"
                                },
                                "reasoning": {
                                    "type": "string",
                                    "description": "Detailed explanation of the analysis quality assessment and methodology evaluation"
                                }
                            },
                            "required": ["verified", "reasoning"]
                        }
                    }
                }
            ]
            
            # Truncate if too long to avoid prompt length issues
            content = statistical_analysis_content[:2000] + "..." if len(statistical_analysis_content) > 2000 else statistical_analysis_content
            
            prompt = f"""Evaluate if this statistical analysis is substantive and well-executed:

{content}

Call verify_statistical_analysis tool: does this appear to be a substantive statistical analysis with appropriate methodology?"""

            self.audit.log_agent_event(self.agent_name, "step2_started", {
                "batch_id": batch_id,
                "step": "statistical_verification",
                "model": "vertex_ai/gemini-2.5-flash-lite"
            })
            
            # System prompt emphasizing mandatory tool call
            system_prompt = "You are a statistical analysis reviewer. You MUST evaluate the quality and substance of the statistical analysis and call the verify_statistical_analysis tool with your findings. This is MANDATORY - you must call the verify_statistical_analysis tool."
            
            # Call LLM with tools (using proper EnhancedLLMGateway format)
            response_content, metadata = self.gateway.execute_call_with_tools(
                model="vertex_ai/gemini-2.5-pro",
                prompt=prompt,
                system_prompt=system_prompt,
                tools=verification_tools,
                force_function_calling=True,  # Force tool calling like deprecated agent
                context=f"Verifying statistical analysis for batch {batch_id}"
            )
            
            # Extract verification result from tool calls (using metadata format like deprecated agent)
            verification_status = "unknown"
            if not metadata.get('success'):
                self.logger.error(f"Statistical verification LLM call failed: {metadata.get('error', 'Unknown error')}")
                verification_status = "verification_failed"
            else:
                tool_calls = metadata.get('tool_calls', [])
                if tool_calls:
                    tool_call = tool_calls[0]
                    if tool_call.function.name == "verify_statistical_analysis":
                        try:
                            args = json.loads(tool_call.function.arguments)
                            verification_status = "verified" if args.get("verified", False) else "verification_failed"
                            self.logger.info(f"Statistical verification reasoning: {args.get('reasoning', 'No reasoning provided')}")
                        except json.JSONDecodeError as e:
                            self.logger.error(f"Failed to parse statistical verification tool call arguments: {e}")
                            verification_status = "verification_failed"
                else:
                    self.logger.error("No tool calls found in statistical verification response")
                    verification_status = "verification_failed"
            
            verification_result = {
                "verification_status": verification_status,
                "batch_id": batch_id,
                "model_used": "vertex_ai/gemini-2.5-flash-lite",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            self.audit.log_agent_event(self.agent_name, "step2_completed", {
                "batch_id": batch_id,
                "step": "statistical_verification",
                "verification_status": verification_status
            })
            
            return verification_result
            
        except Exception as e:
            self.logger.error(f"Step 2 failed: {e}")
            return None
    