#!/usr/bin/env python3
"""
Simple Experiment Executor - THIN Architecture
==============================================

Single execution path for all experiment runs. No complex strategies,
no resume functionality, no artifact copying. Just clean phase execution.

Phases:
1. validation (optional)
2. analysis 
3. statistical
4. evidence
5. synthesis
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .run_context import RunContext
from .agent_result import AgentResult
from .standard_agent import StandardAgent
from .local_artifact_storage import LocalArtifactStorage
from .audit_logger import AuditLogger


@dataclass
class ExperimentResult:
    """Result of experiment execution"""
    success: bool
    phases_completed: List[str]
    artifacts: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_seconds: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class SimpleExperimentExecutor:
    """
    Single execution engine for all experiment runs.
    
    No complex strategies, no resume functionality, no artifact copying.
    Just clean phase execution from start to finish.
    """
    
    # Define the execution phases in order
    PHASES = ["validation", "analysis", "statistical", "evidence", "synthesis"]
    
    def __init__(self):
        """Initialize the simple executor."""
        pass
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger,
                start_phase: str = "validation",
                end_phase: str = "synthesis") -> ExperimentResult:
        """
        Execute phases from start_phase to end_phase (inclusive).
        
        Args:
            agents: Dictionary of available agents
            run_context: Current run context
            storage: Artifact storage
            audit: Audit logger
            start_phase: Phase to start from (default: validation)
            end_phase: Phase to end at (default: synthesis)
            
        Returns:
            ExperimentResult with execution results
        """
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # Validate phase parameters
            if start_phase not in self.PHASES:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Invalid start_phase: {start_phase}. Must be one of {self.PHASES}"
                )
            
            if end_phase not in self.PHASES:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Invalid end_phase: {end_phase}. Must be one of {self.PHASES}"
                )
            
            start_idx = self.PHASES.index(start_phase)
            end_idx = self.PHASES.index(end_phase)
            
            if start_idx > end_idx:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"start_phase ({start_phase}) cannot be after end_phase ({end_phase})"
                )
            
            # Execute phases in order
            phases_to_run = self.PHASES[start_idx:end_idx + 1]
            
            # If we're not starting from validation, we need to ensure CAS hashes are populated
            if start_phase != "validation":
                # Run a minimal validation to populate CAS hashes
                self._populate_cas_hashes(run_context, storage, audit)
            
            for phase in phases_to_run:
                result = self._run_phase(phase, agents, run_context, storage, audit)
                
                if not result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Phase {phase} failed: {result.error_message}"
                    )
                
                phases_completed.append(phase)
                artifacts.extend(result.artifacts)
                run_context.update_phase(phase)
            
            # Calculate execution time
            end_time = datetime.now(timezone.utc)
            execution_time = (end_time - start_time).total_seconds()
            
            return ExperimentResult(
                success=True,
                phases_completed=phases_completed,
                artifacts=artifacts,
                metadata=metadata,
                execution_time_seconds=execution_time
            )
            
        except Exception as e:
            return ExperimentResult(
                success=False,
                phases_completed=phases_completed,
                artifacts=artifacts,
                metadata=metadata,
                error_message=f"Execution failed: {str(e)}"
            )
    
    def _run_phase(self, 
                   phase: str, 
                   agents: Dict[str, StandardAgent], 
                   run_context: RunContext,
                   storage: LocalArtifactStorage,
                   audit: AuditLogger) -> AgentResult:
        """
        Run a single phase.
        
        Args:
            phase: Phase name to run
            agents: Dictionary of available agents
            run_context: Current run context
            storage: Artifact storage
            audit: Audit logger
            
        Returns:
            AgentResult from the phase execution
        """
        
        # Map phase names to agent names
        phase_agent_map = {
            "validation": "Validation",
            "analysis": "Analysis", 
            "statistical": "Statistical",
            "evidence": "Evidence",
            "synthesis": "Synthesis"
        }
        
        agent_name = phase_agent_map.get(phase)
        if not agent_name:
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"phase": phase, "error": f"Unknown phase: {phase}"},
                error_message=f"Unknown phase: {phase}"
            )
        
        if agent_name not in agents:
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"phase": phase, "agent": agent_name, "error": "Agent not available"},
                error_message=f"Agent {agent_name} not available for phase {phase}"
            )
        
        # Handle special cases
        if phase == "validation":
            skip_validation = run_context.metadata.get("skip_validation", False)
            if skip_validation:
                # Even when skipping validation, we need to populate CAS hashes
                # This is a minimal validation that just loads and hashes the files
                try:
                    from ..agents.validation_agent.v2_validation_agent import V2ValidationAgent
                    # Create a minimal validation agent just for CAS registration
                    temp_agent = V2ValidationAgent(None, None, None)
                    # Run only the input extraction part (CAS registration)
                    temp_agent._validate_and_extract_inputs(run_context)
                    
                    audit.log_agent_event("SimpleExperimentExecutor", "phase_skipped_with_cas", {
                        "phase": phase, 
                        "reason": "skip_validation flag set, but CAS hashes populated"
                    })
                    return AgentResult(
                        success=True,
                        artifacts=[],
                        metadata={"phase": phase, "skipped": True, "cas_populated": True}
                    )
                except Exception as e:
                    audit.log_agent_event("SimpleExperimentExecutor", "cas_population_failed", {
                        "phase": phase,
                        "error": str(e)
                    })
                    return AgentResult(
                        success=False,
                        artifacts=[],
                        metadata={"phase": phase, "error": f"CAS population failed: {str(e)}"},
                        error_message=f"Failed to populate CAS hashes: {str(e)}"
                    )
        
        # Log phase start
        audit.log_agent_event("SimpleExperimentExecutor", "phase_start", {"phase": phase})
        
        # Show progress to user
        try:
            from ..cli_console import rich_console
            if rich_console:
                phase_messages = {
                    "validation": "🔍 Running validation checks...",
                    "analysis": "📊 Running atomic document analysis...",
                    "statistical": "📈 Running statistical analysis...",
                    "evidence": "📖 Retrieving supporting evidence...",
                    "synthesis": "📝 Generating research report..."
                }
                message = phase_messages.get(phase, f"🔄 Running {phase} phase...")
                rich_console.print_info(message)
        except ImportError:
            pass
        
        # Execute the agent
        agent = agents[agent_name]
        result = agent.execute(run_context=run_context)
        
        # Log phase completion
        if result.success:
            audit.log_agent_event("SimpleExperimentExecutor", "phase_complete", {
                "phase": phase,
                "artifacts_count": len(result.artifacts)
            })
        else:
            audit.log_agent_event("SimpleExperimentExecutor", "phase_failed", {
                "phase": phase,
                "error": result.error_message
            })
        
        return result
    
    def _populate_cas_hashes(self, run_context: RunContext, storage: LocalArtifactStorage, audit: AuditLogger):
        """Populate CAS hashes when starting from a non-validation phase."""
        try:
            from ..agents.validation_agent.v2_validation_agent import V2ValidationAgent
            # Create a minimal validation agent just for CAS registration
            temp_agent = V2ValidationAgent(None, storage, audit)
            # Run only the input extraction part (CAS registration)
            temp_agent._validate_and_extract_inputs(run_context)
            
            audit.log_agent_event("SimpleExperimentExecutor", "cas_hashes_populated", {
                "reason": "Starting from non-validation phase, CAS hashes populated"
            })
        except Exception as e:
            audit.log_agent_event("SimpleExperimentExecutor", "cas_population_failed", {
                "error": str(e)
            })
            raise RuntimeError(f"Failed to populate CAS hashes: {str(e)}")
