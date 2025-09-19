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
            
            # Extract required data from RunContext
            # THIN PRINCIPLE: Orchestrator should have already loaded this data
            framework_content = run_context.metadata.get("framework_content")
            corpus_content = run_context.metadata.get("corpus_content")
            analysis_artifacts = run_context.analysis_artifacts
            
            if not framework_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "framework_content not found in RunContext"},
                    error_message="framework_content not found in RunContext"
                )
            
            if not corpus_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "corpus_content not found in RunContext"},
                    error_message="corpus_content not found in RunContext"
                )
            
            if not analysis_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "analysis_artifacts not found in RunContext"},
                    error_message="analysis_artifacts not found in RunContext"
                )
            
            # Generate batch ID for this analysis
            batch_id = f"v2_statistical_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # THIN PRINCIPLE: Let the legacy agent handle all the intelligence
            # We only adapt the interface, not the business logic
            self.logger.info(f"Calling legacy StatisticalAgent.analyze_batch for batch {batch_id}")
            
            legacy_result = self.legacy_agent.analyze_batch(
                framework_content=framework_content,
                experiment_content="",  # Not needed for statistical analysis
                corpus_manifest=corpus_content,
                batch_id=batch_id,
                analysis_artifact_hashes=analysis_artifacts
            )
            
            # Convert legacy result to V2 AgentResult
            if legacy_result.get("success", False):
                # Extract artifacts from legacy result
                artifacts = []
                
                # Add statistical results artifact
                if "statistical_results" in legacy_result:
                    artifacts.append({
                        "type": "statistical_results",
                        "content": legacy_result["statistical_results"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add verification results artifact
                if "verification_results" in legacy_result:
                    artifacts.append({
                        "type": "verification_results",
                        "content": legacy_result["verification_results"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add CSV generation results artifact
                if "csv_results" in legacy_result:
                    artifacts.append({
                        "type": "csv_results",
                        "content": legacy_result["csv_results"],
                        "metadata": {
                            "phase": "statistical",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Update run context with results
                run_context.statistical_results = legacy_result.get("statistical_results", {})
                
                # Log success
                self.audit.log_agent_event(self.agent_name, "statistical_analysis_complete", {
                    "batch_id": batch_id,
                    "artifacts_generated": len(artifacts),
                    "analysis_artifacts_count": len(analysis_artifacts)
                })
                
                return AgentResult(
                    success=True,
                    artifacts=artifacts,
                    metadata={
                        "agent_name": self.agent_name,
                        "batch_id": batch_id,
                        "analysis_artifacts_count": len(analysis_artifacts),
                        "artifacts_count": len(artifacts)
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