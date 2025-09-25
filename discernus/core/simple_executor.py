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
from pathlib import Path

from .run_context import RunContext
from .agent_result import AgentResult
from .standard_agent import StandardAgent
from .local_artifact_storage import LocalArtifactStorage
from .audit_logger import AuditLogger
from .artifact_documentation import ArtifactDocumentationGenerator


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
            
            # Always create run context artifact in CAS for human-readable naming
            self._create_run_context_artifact(run_context, storage)
            
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
            
            # Generate README for experiment artifacts (only after complete pipeline)
            if end_phase == "synthesis" and phases_completed and "synthesis" in phases_completed:
                try:
                    from ..gateway.llm_gateway import LLMGateway
                    from ..gateway.model_registry import ModelRegistry
                    model_registry = ModelRegistry()
                    gateway = LLMGateway(model_registry)
                    doc_generator = ArtifactDocumentationGenerator(storage, gateway)
                    readme_content = doc_generator.generate_artifact_readme(run_context.experiment_dir)
                    
                    # Write README to artifacts directory
                    readme_path = storage.run_folder / "artifacts" / "README.md"
                    readme_path.write_text(readme_content, encoding='utf-8')
                    
                    # Log README generation
                    audit.log_agent_event(
                        agent_name="ArtifactDocumentationGenerator",
                        event_type="readme_generated",
                        data={"readme_path": str(readme_path)}
                    )
                    
                except Exception as e:
                    # Don't fail the experiment if README generation fails
                    audit.log_agent_event(
                        agent_name="ArtifactDocumentationGenerator",
                        event_type="readme_generation_failed",
                        data={"error": str(e)}
                    )
            
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
        
        # Add detailed logging for synthesis phase debugging
        if phase == "synthesis":
            audit.log_agent_event("SimpleExperimentExecutor", "synthesis_debug_start", {
                "phase": phase,
                "agent_name": agent_name,
                "agent_type": type(agent).__name__,
                "run_context_type": type(run_context).__name__
            })
            
            # Log storage state before calling synthesis agent
            try:
                storage = getattr(agent, 'storage', None)
                if storage:
                    audit.log_agent_event("SimpleExperimentExecutor", "synthesis_storage_debug", {
                        "storage_type": type(storage).__name__,
                        "storage_available": storage is not None
                    })
            except Exception as e:
                audit.log_agent_event("SimpleExperimentExecutor", "synthesis_storage_error", {
                    "error": str(e)
                })
        
        try:
            result = agent.execute(run_context=run_context)
        except Exception as e:
            # Log any exceptions during agent execution
            audit.log_agent_event("SimpleExperimentExecutor", "agent_execution_exception", {
                "phase": phase,
                "agent_name": agent_name,
                "exception_type": type(e).__name__,
                "exception_message": str(e)
            })
            import traceback
            audit.log_agent_event("SimpleExperimentExecutor", "agent_execution_traceback", {
                "phase": phase,
                "traceback": traceback.format_exc()
            })
            raise
        
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
    
    def _create_run_context_artifact(self, run_context: RunContext, storage: LocalArtifactStorage):
        """Create a run context artifact in CAS for human-readable naming."""
        try:
            import json
            
            # Build run context data with enhanced information
            run_context_data = {
                "experiment_name": run_context.experiment_id,
                "framework_name": run_context.metadata.get("framework_filename", "unknown_framework"),
                "corpus_name": run_context.metadata.get("corpus_filename", "unknown_corpus"),
                "document_count": run_context.metadata.get("document_count", 0),
                "run_id": f"{run_context.experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",  # Unique run ID
                "completion_date": datetime.now(timezone.utc).isoformat(),
                "experiment_dir": str(run_context.experiment_dir),
                "framework_hash": run_context.metadata.get("framework_hash", ""),
                "corpus_manifest_hash": run_context.metadata.get("corpus_manifest_hash", ""),
                "corpus_document_hashes": run_context.metadata.get("corpus_document_hashes", [])
            }
            
            # Store in CAS
            content_bytes = json.dumps(run_context_data, indent=2).encode('utf-8')
            
            # Enhanced naming with human context
            human_context = {
                "experiment_name": run_context.experiment_id,
                "context_type": "run_context"
            }
            
            artifact_hash = storage.put_artifact(
                content_bytes,
                {"artifact_type": "run_context"},
                human_context
            )
            
            # Store the hash in run_context metadata for reference
            run_context.metadata["run_context_hash"] = artifact_hash
            
        except Exception as e:
            # Don't fail the experiment if run context creation fails
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not create run context artifact: {e}")
