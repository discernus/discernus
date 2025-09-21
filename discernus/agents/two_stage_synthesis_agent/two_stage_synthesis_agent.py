#!/usr/bin/env python3
"""
Two-Stage Synthesis Agent for Discernus
=======================================

Implements two-stage synthesis to prevent hallucination and ensure data-driven reports:

Stage 1: Data-Driven Analysis
- Input: Statistical results, experiment metadata, framework
- Process: Generate coherent analysis anchored in statistical findings
- Output: Complete research report without evidence quotes
- Goal: Establish all analytical claims based solely on data

Stage 2: Evidence Integration  
- Input: Stage 1 report + curated evidence from IntelligentEvidenceRetrievalAgent
- Process: Enhance report with supporting quotes, create evidence appendix
- Output: Final report with integrated evidence and complete audit trail
- Goal: Support existing claims with evidence, no new analytical claims

Anti-Hallucination Architecture:
- Stage separation prevents evidence from influencing analytical conclusions
- Stage 2 is strictly additive (quotes + appendix), no new analysis
- All claims must originate from Stage 1 statistical analysis
- Evidence serves only to illustrate pre-established findings
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.standard_agent import StandardAgent
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class TwoStageSynthesisAgent(StandardAgent):
    """
    Two-stage synthesis agent that prevents hallucination through architectural separation.
    
    The agent ensures all analytical claims originate from statistical data before any
    evidence integration, maintaining strict separation between analysis and illustration.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TwoStageSynthesisAgent.
        
        Args:
            security: Security boundary for experiment access
            storage: Artifact storage interface
            audit: Audit logging interface
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        self.agent_name = "TwoStageSynthesisAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize enhanced LLM gateway for tool calling
        model_registry = ModelRegistry()
        self.llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Stage configuration
        self.stage1_model = "vertex_ai/gemini-2.5-pro"  # Pro for analytical depth
        self.stage2_model = "vertex_ai/gemini-2.5-flash"  # Flash for evidence integration
        
        self.logger.info(f"Initialized {self.agent_name} with two-stage architecture")
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return [
            "two_stage_synthesis",
            "anti_hallucination_architecture", 
            "data_driven_analysis",
            "evidence_integration",
            "evidence_appendix_generation",
            "analytical_claim_validation",
            "statistical_anchoring",
            "tool_calling"
        ]
    
    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        Execute two-stage synthesis process.
        
        Args:
            run_context: The RunContext containing all experiment data
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult with final synthesis report and evidence appendix
        """
        try:
            self.logger.info("TwoStageSynthesisAgent starting two-stage execution")
            self.log_execution_start(**kwargs)
            
            # Validate inputs
            if not self._validate_inputs(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                    error_message="Required inputs missing for synthesis"
                )
            
            # Stage 1: Data-Driven Analysis (no evidence)
            self.logger.info("Stage 1: Generating data-driven analysis...")
            stage1_report = self._execute_stage1_analysis(run_context)
            
            if not stage1_report:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Stage 1 analysis failed"},
                    error_message="Failed to generate data-driven analysis"
                )
            
            # Store Stage 1 report
            stage1_artifact = self._store_stage1_report(stage1_report)
            
            # Stage 2: Evidence Integration
            self.logger.info("Stage 2: Integrating curated evidence...")
            final_report = self._execute_stage2_integration(run_context, stage1_report)
            
            if not final_report:
                return AgentResult(
                    success=False,
                    artifacts=[stage1_artifact],
                    metadata={"agent_name": self.agent_name, "error": "Stage 2 integration failed"},
                    error_message="Failed to integrate evidence into report"
                )
            
            # Store final report with evidence
            final_artifact = self._store_final_report(final_report)
            
            # Create evidence appendix
            appendix_artifact = self._create_evidence_appendix(run_context, final_report)
            
            artifacts = [stage1_artifact, final_artifact]
            if appendix_artifact:
                artifacts.append(appendix_artifact)
            
            self.logger.info(f"Two-stage synthesis completed: {len(artifacts)} artifacts created")
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "stage1_model": self.stage1_model,
                    "stage2_model": self.stage2_model,
                    "synthesis_method": "two_stage_anti_hallucination",
                    "evidence_integration": True,
                    "appendix_created": appendix_artifact is not None
                }
            )
            
        except Exception as e:
            self.logger.error(f"Two-stage synthesis failed: {e}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"Two-stage synthesis failed: {e}"
            )
    
    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Validate that required inputs are available for synthesis."""
        # Check for statistical results
        if not hasattr(run_context, 'statistical_results') or not run_context.statistical_results:
            self.logger.error("No statistical results found in run_context")
            return False
        
        # Check for experiment metadata
        if not run_context.experiment_id:
            self.logger.error("No experiment_id found in run_context")
            return False
        
        # Check for framework path
        if not run_context.framework_path:
            self.logger.error("No framework_path found in run_context")
            return False
        
        self.logger.info("Input validation passed: statistical results, experiment metadata, and framework available")
        return True
    
    def _execute_stage1_analysis(self, run_context: RunContext) -> Optional[str]:
        """
        Execute Stage 1: Data-driven analysis without evidence quotes.
        
        Args:
            run_context: The RunContext containing statistical results
            
        Returns:
            Stage 1 report text or None if failed
        """
        # TODO: Implement Stage 1 data-driven analysis
        self.logger.info("Stage 1 analysis not yet implemented")
        return None
    
    def _execute_stage2_integration(self, run_context: RunContext, stage1_report: str) -> Optional[str]:
        """
        Execute Stage 2: Evidence integration with curated quotes.
        
        Args:
            run_context: The RunContext containing curated evidence
            stage1_report: The Stage 1 report to enhance with evidence
            
        Returns:
            Final report with integrated evidence or None if failed
        """
        # TODO: Implement Stage 2 evidence integration
        self.logger.info("Stage 2 evidence integration not yet implemented")
        return None
    
    def _store_stage1_report(self, report: str) -> str:
        """Store Stage 1 report as artifact."""
        artifact_data = {
            "agent_name": self.agent_name,
            "stage": "stage1_data_driven_analysis",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": self.stage1_model,
            "report_content": report,
            "evidence_included": False,
            "synthesis_method": "data_driven_only"
        }
        
        return self.storage.store_artifact(
            content=artifact_data,
            artifact_type="stage1_synthesis_report",
            experiment_id="stage1_analysis"
        )
    
    def _store_final_report(self, report: str) -> str:
        """Store final report with evidence integration."""
        artifact_data = {
            "agent_name": self.agent_name,
            "stage": "stage2_evidence_integrated",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": self.stage2_model,
            "report_content": report,
            "evidence_included": True,
            "synthesis_method": "two_stage_with_evidence"
        }
        
        return self.storage.store_artifact(
            content=artifact_data,
            artifact_type="final_synthesis_report",
            experiment_id="final_report"
        )
    
    def _create_evidence_appendix(self, run_context: RunContext, final_report: str) -> Optional[str]:
        """Create evidence appendix organized by statistical conclusion."""
        # TODO: Implement evidence appendix creation
        self.logger.info("Evidence appendix creation not yet implemented")
        return None
