#!/usr/bin/env python3
"""
V2 Analysis Agent for Discernus
===============================

THIN V2-compliant analysis agent that performs comprehensive document analysis.

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

# Import the existing AnalysisAgent to wrap its logic
from .main import AnalysisAgent


class V2AnalysisAgent(ToolCallingAgent):
    """
    THIN V2-compliant analysis agent for document analysis.
    
    This agent is a thin wrapper around the legacy AnalysisAgent that:
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
        Initialize the V2 AnalysisAgent.
        
        Args:
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        
        self.agent_name = "V2AnalysisAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize the legacy AnalysisAgent to wrap its functionality
        self.legacy_agent = AnalysisAgent(security, audit, storage)

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
            self.logger.info("Starting V2 Analysis Agent execution")
            
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
            corpus_documents = run_context.metadata.get("corpus_documents")

            if not framework_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "framework_content not found in RunContext"},
                    error_message="framework_content not found in RunContext"
                )

            if not corpus_documents:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "corpus_documents not found in RunContext"},
                    error_message="corpus_documents not found in RunContext"
                )

            # Generate batch ID for this analysis
            batch_id = f"v2_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # THIN PRINCIPLE: Let the legacy agent handle all the intelligence
            # We only adapt the interface, not the business logic
            self.logger.info(f"Calling legacy AnalysisAgent.analyze_documents for batch {batch_id}")

            # The legacy agent expects a list of dicts with a 'content' key.
            # The orchestrator now provides this structure directly.
            documents = corpus_documents

            legacy_result = self.legacy_agent.analyze_documents(
                framework_content=framework_content,
                documents=documents
            )
            
            # Convert legacy result to V2 AgentResult
            # THIN PRINCIPLE: Legacy agent returns data directly, not wrapped in success field
            if legacy_result and "composite_analysis" in legacy_result:
                # Extract artifacts from legacy result
                artifacts = []
                
                # Add composite analysis artifact
                if "composite_analysis" in legacy_result:
                    artifacts.append({
                        "type": "composite_analysis",
                        "content": legacy_result["composite_analysis"],
                        "metadata": {
                            "phase": "analysis",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add evidence extraction artifact
                if "evidence_extraction" in legacy_result:
                    artifacts.append({
                        "type": "evidence_extraction",
                        "content": legacy_result["evidence_extraction"],
                        "metadata": {
                            "phase": "analysis",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add score extraction artifact
                if "score_extraction" in legacy_result:
                    artifacts.append({
                        "type": "score_extraction",
                        "content": legacy_result["score_extraction"],
                        "metadata": {
                            "phase": "analysis",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add derived metrics artifact
                if "derived_metrics" in legacy_result:
                    artifacts.append({
                        "type": "derived_metrics",
                        "content": legacy_result["derived_metrics"],
                        "metadata": {
                            "phase": "analysis",
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
                            "phase": "analysis",
                            "batch_id": batch_id,
                            "timestamp": datetime.now().isoformat(),
                            "agent_name": self.agent_name
                        }
                    })
                
                # Add markup extraction artifact
                if "markup_extraction" in legacy_result:
                    artifacts.append({
                        "type": "markup_extraction",
                        "content": legacy_result["markup_extraction"],
                        "metadata": {
                            "phase": "analysis",
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
                run_context.analysis_results = legacy_result
                run_context.analysis_artifacts = artifact_hashes
                
                # Log success
                self.audit.log_agent_event(self.agent_name, "analysis_complete", {
                    "batch_id": batch_id,
                    "artifacts_generated": len(artifacts)
                })
                
                return AgentResult(
                    success=True,
                    artifacts=artifacts,
                    metadata={
                        "agent_name": self.agent_name,
                        "batch_id": batch_id,
                        "artifacts_count": len(artifacts)
                    }
                )
            else:
                # Handle legacy agent failure
                error_msg = legacy_result.get("error", "Unknown error in legacy analysis")
                self.logger.error(f"Legacy AnalysisAgent failed: {error_msg}")
                
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "batch_id": batch_id},
                    error_message=f"Legacy AnalysisAgent failed: {error_msg}"
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
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2AnalysisAgent execution failed: {e}"
            )
    
    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent.
        
        Returns:
            List of capability strings
        """
        return [
            "composite_analysis_with_markup",
            "evidence_extraction", 
            "score_extraction",
            "derived_metrics",
            "verification",
            "markup_extraction"
        ]