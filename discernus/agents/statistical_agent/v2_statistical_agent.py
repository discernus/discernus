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
            
            # Step 1: Statistical Analysis
            statistical_result = self._step1_statistical_analysis(framework_content, score_data, batch_id)
            if not statistical_result:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical analysis failed"},
                    error_message="Statistical analysis failed"
                )
            
            # Step 2: Verification
            verification_result = self._step2_verification(statistical_result, batch_id)
            
            # Create artifacts
            artifacts = []
            
            # Add statistical analysis artifact
            artifacts.append({
                "type": "statistical_analysis",
                "content": statistical_result,
                "metadata": {
                    "artifact_type": "statistical_analysis",
                    "phase": "statistical",
                    "batch_id": batch_id,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name
                }
            })
            
            # Add verification artifact if available
            if verification_result:
                artifacts.append({
                    "type": "statistical_verification",
                    "content": verification_result,
                    "metadata": {
                        "artifact_type": "statistical_verification",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name
                    }
                })
            
            # Update run context
            run_context.statistical_artifacts = [artifact["metadata"].get("artifact_hash", "") for artifact in artifacts if "artifact_hash" in artifact["metadata"]]
            run_context.statistical_results = statistical_result
            
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
                                "timestamp": artifact_data.get("timestamp", "")
                            })
                            
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Could not parse scores from artifact {artifact_hash}: {e}")
                            continue
                
            except Exception as e:
                self.logger.warning(f"Error processing artifact {artifact_hash}: {e}")
                continue
        
        return score_data
    
    def _step1_statistical_analysis(self, framework_content: str, score_data: List[Dict[str, Any]], batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Step 1: Perform statistical analysis on collected score data.
        
        Args:
            framework_content: Framework content for context
            score_data: List of score data from atomic artifacts
            batch_id: Batch identifier
            
        Returns:
            Statistical analysis result or None if failed
        """
        try:
            # Prepare statistical analysis prompt
            prompt = f"""You are a statistical analysis expert. Analyze the following dimensional scores using appropriate statistical methods.

FRAMEWORK CONTEXT:
{framework_content}

SCORE DATA:
{json.dumps(score_data, indent=2)}

TASK: Perform comprehensive statistical analysis including:
1. Descriptive statistics for each dimension
2. Correlation analysis between dimensions
3. Statistical significance testing where appropriate
4. Summary of key findings

REQUIREMENTS:
- Use appropriate statistical methods for the data
- Provide clear interpretations of results
- Include confidence intervals where relevant
- Format results as structured JSON

OUTPUT FORMAT:
```json
{{
  "descriptive_statistics": {{
    "dimension_name": {{
      "mean": 0.0,
      "std": 0.0,
      "min": 0.0,
      "max": 0.0,
      "count": 0
    }}
  }},
  "correlations": {{
    "dimension1_dimension2": 0.0
  }},
  "significance_tests": {{
    "test_name": {{
      "statistic": 0.0,
      "p_value": 0.0,
      "significant": true
    }}
  }},
  "summary": "Key findings and interpretations"
}}
```

Return ONLY the JSON, no other text."""

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
            
            # Parse the response
            try:
                # Extract JSON from markdown code block if present
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    if json_end > json_start:
                        json_content = content[json_start:json_end].strip()
                    else:
                        json_content = content[json_start:].strip()
                else:
                    json_content = content.strip()
                
                statistical_result = json.loads(json_content)
                
                # Add metadata
                statistical_result.update({
                    "batch_id": batch_id,
                    "documents_processed": len(score_data),
                    "model_used": "vertex_ai/gemini-2.5-pro",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
                
                self.audit.log_agent_event(self.agent_name, "step1_completed", {
                    "batch_id": batch_id,
                    "step": "statistical_analysis",
                    "response_length": len(content)
                })
                
                return statistical_result
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Could not parse statistical analysis response: {e}")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed: {e}")
            return None
    
    def _step2_verification(self, statistical_result: Dict[str, Any], batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Step 2: Verify statistical analysis results.
        
        Args:
            statistical_result: Results from step 1
            batch_id: Batch identifier
            
        Returns:
            Verification result or None if failed
        """
        try:
            prompt = f"""You are a statistical verification expert. Review the following statistical analysis for accuracy and appropriateness.

STATISTICAL ANALYSIS:
{json.dumps(statistical_result, indent=2)}

TASK: Verify the statistical analysis by:
1. Checking if the statistical methods used are appropriate
2. Validating calculations where possible
3. Identifying any potential issues or limitations
4. Providing a verification assessment

REQUIREMENTS:
- Be thorough but concise
- Focus on methodological appropriateness
- Note any limitations or concerns
- Provide clear verification status

OUTPUT FORMAT:
```json
{{
  "verification_status": "verified|concerns|failed",
  "methodology_check": "appropriate|questionable|inappropriate",
  "calculation_validation": "valid|partial|invalid",
  "concerns": ["list of any concerns"],
  "recommendations": ["list of recommendations"],
  "overall_assessment": "Brief summary of verification"
}}
```

Return ONLY the JSON, no other text."""

            self.audit.log_agent_event(self.agent_name, "step2_started", {
                "batch_id": batch_id,
                "step": "statistical_verification",
                "model": "vertex_ai/gemini-2.5-flash-lite"
            })
            
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
            
            # Parse the response
            try:
                # Extract JSON from markdown code block if present
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    if json_end > json_start:
                        json_content = content[json_start:json_end].strip()
                    else:
                        json_content = content[json_start:].strip()
                else:
                    json_content = content.strip()
                
                verification_result = json.loads(json_content)
                
                # Add metadata
                verification_result.update({
                    "batch_id": batch_id,
                    "model_used": "vertex_ai/gemini-2.5-flash-lite",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
                
                self.audit.log_agent_event(self.agent_name, "step2_completed", {
                    "batch_id": batch_id,
                    "step": "statistical_verification",
                    "response_length": len(content)
                })
                
                return verification_result
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Could not parse verification response: {e}")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 2 failed: {e}")
            return None