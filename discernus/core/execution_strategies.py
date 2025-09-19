#!/usr/bin/env python3
"""
Execution Strategies for V2 Orchestrator
========================================

Different execution strategies for different types of experiment runs.
Each strategy implements the ExecutionStrategy interface and handles
a specific execution pattern.

Strategies:
- FullExperimentStrategy: Complete pipeline with verification
- AnalysisOnlyStrategy: Analysis phase only
- StatisticalPrepStrategy: Analysis + statistical phases
- ResumeFromStatsStrategy: Resume from statistical results
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

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


class ExecutionStrategy(ABC):
    """Abstract base class for execution strategies"""
    
    @abstractmethod
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """
        Execute the strategy.
        
        Args:
            agents: Dictionary of available agents
            run_context: Current run context
            storage: Artifact storage
            audit: Audit logger
            
        Returns:
            ExperimentResult with execution results
        """
        pass


class FullExperimentStrategy(ExecutionStrategy):
    """
    Complete experiment execution with all phases and verification.
    
    Phases:
    1. Coherence validation
    2. Analysis
    3. Statistical analysis
    4. Evidence retrieval
    5. Synthesis
    6. Verification (if enabled)
    """
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """Execute full experiment pipeline"""
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # THIN PRINCIPLE: Orchestrator handles file I/O, not agents
            # Load framework and corpus content and pass to agents via RunContext
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            corpus_content = self._load_corpus_content(Path(run_context.corpus_path))
            
            if not framework_content:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load framework content"
                )
            
            if not corpus_content:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load corpus content"
                )
            
            # Add content to RunContext metadata for agents to use
            run_context.metadata["framework_content"] = framework_content
            run_context.metadata["corpus_content"] = corpus_content
            # Phase 1: Coherence validation
            if "coherence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "coherence"})
                coherence_result = agents["coherence"].execute(run_context=run_context)
                if not coherence_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Coherence validation failed: {coherence_result.error_message}"
                    )
                phases_completed.append("coherence")
                artifacts.extend(coherence_result.artifacts)
                run_context.update_phase("coherence")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "coherence"})
            
            # Phase 2: Analysis
            if "analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                analysis_result = agents["analysis"].execute(run_context=run_context)
                if not analysis_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Analysis failed: {analysis_result.error_message}"
                    )
                phases_completed.append("analysis")
                artifacts.extend(analysis_result.artifacts)
                run_context.update_phase("analysis")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "analysis"})
            
            # Phase 3: Statistical analysis
            if "statistical" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "statistical"})
                statistical_result = agents["statistical"].execute(run_context=run_context)
                if not statistical_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Statistical analysis failed: {statistical_result.error_message}"
                    )
                phases_completed.append("statistical")
                artifacts.extend(statistical_result.artifacts)
                run_context.update_phase("statistical")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "statistical"})
            
            # Phase 4: Evidence retrieval
            if "evidence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "evidence"})
                evidence_result = agents["evidence"].execute(run_context=run_context)
                if not evidence_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Evidence retrieval failed: {evidence_result.error_message}"
                    )
                phases_completed.append("evidence")
                artifacts.extend(evidence_result.artifacts)
                run_context.update_phase("evidence")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "evidence"})
            
            # Phase 5: Synthesis
            if "synthesis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "synthesis"})
                synthesis_result = agents["synthesis"].execute(run_context=run_context)
                if not synthesis_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Synthesis failed: {synthesis_result.error_message}"
                    )
                phases_completed.append("synthesis")
                artifacts.extend(synthesis_result.artifacts)
                run_context.update_phase("synthesis")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "synthesis"})
            
            # Phase 6: Verification (if enabled)
            if run_context.metadata.get("verification_enabled", True) and "verification" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "verification"})
                verification_result = agents["verification"].execute(run_context=run_context)
                if not verification_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Verification failed: {verification_result.error_message}"
                    )
                phases_completed.append("verification")
                artifacts.extend(verification_result.artifacts)
                run_context.update_phase("verification")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "verification"})
            
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
                error_message=f"Strategy execution failed: {str(e)}"
            )
    
    def _load_framework_content(self, framework_path: Path) -> Optional[str]:
        """Load framework content from file."""
        try:
            return framework_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
    
    def _load_corpus_content(self, corpus_path: Path) -> Optional[str]:
        """Load corpus content from file."""
        try:
            return corpus_path.read_text(encoding='utf-8')
        except Exception as e:
            return None


class AnalysisOnlyStrategy(ExecutionStrategy):
    """
    Analysis phase only - for quick analysis runs.
    
    Phases:
    1. Coherence validation
    2. Analysis
    """
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """Execute analysis-only pipeline"""
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # Phase 1: Coherence validation
            if "coherence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "coherence"})
                coherence_result = agents["coherence"].execute(run_context=run_context)
                if not coherence_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Coherence validation failed: {coherence_result.error_message}"
                    )
                phases_completed.append("coherence")
                artifacts.extend(coherence_result.artifacts)
                run_context.update_phase("coherence")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "coherence"})
            
            # Phase 2: Analysis
            if "analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                analysis_result = agents["analysis"].execute(run_context=run_context)
                if not analysis_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Analysis failed: {analysis_result.error_message}"
                    )
                phases_completed.append("analysis")
                artifacts.extend(analysis_result.artifacts)
                run_context.update_phase("analysis")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "analysis"})
            
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
                error_message=f"Strategy execution failed: {str(e)}"
            )
    
    def _load_framework_content(self, framework_path: Path) -> Optional[str]:
        """Load framework content from file."""
        try:
            return framework_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
    
    def _load_corpus_content(self, corpus_path: Path) -> Optional[str]:
        """Load corpus content from file."""
        try:
            return corpus_path.read_text(encoding='utf-8')
        except Exception as e:
            return None


class StatisticalPrepStrategy(ExecutionStrategy):
    """
    Analysis + statistical phases - for statistical preparation.
    
    Phases:
    1. Coherence validation
    2. Analysis
    3. Statistical analysis
    """
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """Execute analysis + statistical pipeline"""
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # Phase 1: Coherence validation
            if "coherence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "coherence"})
                coherence_result = agents["coherence"].execute(run_context=run_context)
                if not coherence_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Coherence validation failed: {coherence_result.error_message}"
                    )
                phases_completed.append("coherence")
                artifacts.extend(coherence_result.artifacts)
                run_context.update_phase("coherence")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "coherence"})
            
            # Phase 2: Analysis
            if "analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                analysis_result = agents["analysis"].execute(run_context=run_context)
                if not analysis_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Analysis failed: {analysis_result.error_message}"
                    )
                phases_completed.append("analysis")
                artifacts.extend(analysis_result.artifacts)
                run_context.update_phase("analysis")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "analysis"})
            
            # Phase 3: Statistical analysis
            if "statistical" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "statistical"})
                statistical_result = agents["statistical"].execute(run_context=run_context)
                if not statistical_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Statistical analysis failed: {statistical_result.error_message}"
                    )
                phases_completed.append("statistical")
                artifacts.extend(statistical_result.artifacts)
                run_context.update_phase("statistical")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "statistical"})
            
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
                error_message=f"Strategy execution failed: {str(e)}"
            )
    
    def _load_framework_content(self, framework_path: Path) -> Optional[str]:
        """Load framework content from file."""
        try:
            return framework_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
    
    def _load_corpus_content(self, corpus_path: Path) -> Optional[str]:
        """Load corpus content from file."""
        try:
            return corpus_path.read_text(encoding='utf-8')
        except Exception as e:
            return None


class ResumeFromStatsStrategy(ExecutionStrategy):
    """
    Resume from statistical results - for continuing experiments.
    
    Phases:
    1. Load resume manifest
    2. Evidence retrieval
    3. Synthesis
    4. Verification (if enabled)
    """
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """Execute resume from statistical results pipeline"""
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # Check if we have statistical results
            if not run_context.statistical_results:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="No statistical results found for resume"
                )
            
            # Phase 1: Evidence retrieval
            if "evidence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "evidence"})
                evidence_result = agents["evidence"].execute(run_context=run_context)
                if not evidence_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Evidence retrieval failed: {evidence_result.error_message}"
                    )
                phases_completed.append("evidence")
                artifacts.extend(evidence_result.artifacts)
                run_context.update_phase("evidence")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "evidence"})
            
            # Phase 2: Synthesis
            if "synthesis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "synthesis"})
                synthesis_result = agents["synthesis"].execute(run_context=run_context)
                if not synthesis_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Synthesis failed: {synthesis_result.error_message}"
                    )
                phases_completed.append("synthesis")
                artifacts.extend(synthesis_result.artifacts)
                run_context.update_phase("synthesis")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "synthesis"})
            
            # Phase 3: Verification (if enabled)
            if run_context.metadata.get("verification_enabled", True) and "verification" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "verification"})
                verification_result = agents["verification"].execute(run_context=run_context)
                if not verification_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Verification failed: {verification_result.error_message}"
                    )
                phases_completed.append("verification")
                artifacts.extend(verification_result.artifacts)
                run_context.update_phase("verification")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "verification"})
            
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
                error_message=f"Strategy execution failed: {str(e)}"
            )
    
    def _load_framework_content(self, framework_path: Path) -> Optional[str]:
        """Load framework content from file."""
        try:
            return framework_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
    
    def _load_corpus_content(self, corpus_path: Path) -> Optional[str]:
        """Load corpus content from file."""
        try:
            return corpus_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
