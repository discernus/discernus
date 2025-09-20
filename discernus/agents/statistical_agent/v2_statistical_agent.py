#!/usr/bin/env python3
"""
V2 Statistical Agent for Discernus
==================================

THIN V2-compliant statistical agent that performs comprehensive statistical analysis.

THIN PRINCIPLES:
- Intelligence resides in the LLM, not in parsing logic
- Agent only adapts interfaces, does not add business logic
- No parsing antipatterns - let LLM handle data interpretation
- Orchestrator handles file I/O, agent handles analysis only
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...core.standard_agent import StandardAgent
from ...core.agent_base_classes import ToolCallingAgent
from ...core.agent_result import AgentResult
from ...core.run_context import RunContext
from ...core.agent_config import AgentConfig
from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.audit_logger import AuditLogger
from ...core.verbose_tracing import trace_calls, trace_section, trace_data

# Import the existing StatisticalAgent to wrap its logic
from .main import StatisticalAgent


class V2StatisticalAgent(ToolCallingAgent):
    """
    THIN V2-compliant statistical agent for statistical analysis.
    
    This agent is a thin wrapper around the legacy StatisticalAgent that:
    1. Adapts the interface to V2 StandardAgent
    2. Converts result formats
    3. Does NO parsing, file I/O, or business logic
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[AgentConfig] = None):
        """
        Initialize the V2 StatisticalAgent.
        
        Args:
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        
        self.agent_name = "V2StatisticalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize the legacy StatisticalAgent to wrap its functionality
        self.legacy_agent = StatisticalAgent(security, storage, audit)

    @trace_calls(include_args=True, include_return=True)
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """
        V2 StandardAgent execute method.
        
        THIN PRINCIPLE: This method only adapts interfaces and converts formats.
        It does NOT parse data, read files, or add business logic.
        
        Args:
            run_context: The RunContext object containing all necessary data
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult: Standardized result with artifacts and metadata
        """
        try:
            self.logger.info("Starting V2 Statistical Agent execution")
            
            # Validate run context
            if not run_context:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "run_context is required"},
                    error_message="run_context is required"
                )
            
            with trace_section("Extract data from RunContext"):
                # THIN PRINCIPLE: Orchestrator should have already loaded this data
                framework_content = run_context.metadata.get("framework_content")
                corpus_manifest_content = run_context.metadata.get("corpus_manifest_content")
                analysis_artifacts = run_context.analysis_artifacts
                
                # Trace the data we received
                trace_data("framework_content", f"Length: {len(framework_content) if framework_content else 'None'}")
                trace_data("corpus_manifest_content", f"Length: {len(corpus_manifest_content) if corpus_manifest_content else 'None'}")
                trace_data("analysis_artifacts", analysis_artifacts)
                trace_data("run_context.analysis_results", hasattr(run_context, 'analysis_results') and run_context.analysis_results is not None)
            
            if not framework_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "framework_content not found in RunContext"},
                    error_message="framework_content not found in RunContext"
                )
            
            if not corpus_manifest_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "corpus_manifest_content not found in RunContext"},
                    error_message="corpus_manifest_content not found in RunContext"
                )
            
            if not analysis_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "analysis_artifacts not found in RunContext"},
                    error_message="analysis_artifacts not found in RunContext"
                )
            
            with trace_section("Call legacy StatisticalAgent"):
                # Generate batch ID for this analysis
                batch_id = f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                trace_data("batch_id", batch_id)
                
                # THIN PRINCIPLE: Let the legacy agent handle all the intelligence
                # We only adapt the interface, not the business logic
                self.logger.info(f"Calling legacy StatisticalAgent.analyze_batch for batch {batch_id}")
                
                legacy_result = self.legacy_agent.analyze_batch(
                    framework_content=framework_content,
                    experiment_content="",  # Not needed for statistical analysis
                    corpus_manifest=corpus_manifest_content,
                    batch_id=batch_id,
                    analysis_artifact_hashes=analysis_artifacts
                )
                
                trace_data("legacy_result", f"Type: {type(legacy_result)}, Keys: {list(legacy_result.keys()) if isinstance(legacy_result, dict) else 'Not a dict'}")
            
            # Convert legacy result to V2 AgentResult
            # THIN PRINCIPLE: Legacy agent returns data directly, not wrapped in success field
            if legacy_result and "statistical_analysis" in legacy_result:
                # Extract artifacts from legacy result
                artifacts = []
                
                # Add statistical analysis artifact
                if "statistical_analysis" in legacy_result:
                    artifacts.append({
                        "type": "statistical_analysis",
                        "content": legacy_result["statistical_analysis"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add verification artifact
                if "verification" in legacy_result:
                    artifacts.append({
                        "type": "verification",
                        "content": legacy_result["verification"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add CSV generation artifact
                if "csv_generation" in legacy_result:
                    artifacts.append({
                        "type": "csv_generation",
                        "content": legacy_result["csv_generation"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add total cost info artifact
                if "total_cost_info" in legacy_result:
                    artifacts.append({
                        "type": "total_cost_info",
                        "content": legacy_result["total_cost_info"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Store artifacts in the artifact storage system
                artifact_hashes = []
                for artifact in artifacts:
                    # Store each artifact in the storage system
                    # Convert content to bytes and create metadata
                    content_bytes = json.dumps(artifact["content"]).encode('utf-8')
                    metadata = {
                        "type": artifact["type"],
                        **artifact["metadata"]
                    }
                    artifact_hash = self.storage.put_artifact(content_bytes, metadata)
                    artifact_hashes.append(artifact_hash)
                
                # Update run context with results
                statistical_analysis = legacy_result.get("statistical_analysis", {})
                run_context.statistical_results = statistical_analysis
                run_context.statistical_artifacts = artifact_hashes
                
                # Log success
                self.audit.log_agent_event(self.agent_name, "statistical_analysis_complete", {
                    "batch_id": batch_id,
                    "artifacts_generated": len(artifact_hashes),
                    "analysis_artifacts_count": len(analysis_artifacts)
                })
                
                return AgentResult(
                    success=True,
                    artifacts=artifact_hashes,
                    metadata={
                        "agent_name": self.agent_name,
                        "batch_id": batch_id,
                        "analysis_artifacts_count": len(analysis_artifacts),
                        "artifacts_count": len(artifact_hashes)
                    }
                )
            else:
                # Handle legacy agent failure
                error_msg = legacy_result.get("error", "Unknown error in legacy statistical analysis")
                self.logger.error(f"Legacy StatisticalAgent failed: {error_msg}")
                
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "batch_id": batch_id},
                    error_message=f"Legacy StatisticalAgent failed: {error_msg}"
                )
                
        except Exception as e:
            self.logger.error(f"V2StatisticalAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "statistical_analysis_failed", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2StatisticalAgent execution failed: {e}"
            )
    
    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent.
        
        Returns:
            List of capability strings
        """
        return [
            "statistical_analysis",
            "statistical_verification",
            "csv_generation",
            "computational_work",
            "significance_testing"
        ]