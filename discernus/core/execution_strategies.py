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
import yaml
import re
import json
import hashlib


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
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            corpus_manifest_path = Path(run_context.corpus_path)
            corpus_documents = self._load_corpus_documents(corpus_manifest_path)
            corpus_manifest_content = corpus_manifest_path.read_text(encoding='utf-8')

            if not framework_content:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load framework content"
                )

            if not corpus_documents:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load corpus documents"
                )

            # Add content to RunContext metadata for agents to use
            run_context.metadata["framework_content"] = framework_content
            run_context.metadata["corpus_documents"] = corpus_documents
            run_context.metadata["corpus_manifest_content"] = corpus_manifest_content
            # Phase 1: Validation (skip if flag is set)
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents and not skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "validation"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Running validation checks...")
                except ImportError:
                    pass
                validation_result = agents["Validation"].execute(run_context=run_context)
                if not validation_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Validation failed: {validation_result.error_message}"
                    )
                phases_completed.append("validation")
                artifacts.extend(validation_result.artifacts)
                run_context.update_phase("validation")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "validation"})
            elif skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_skipped", {"phase": "validation", "reason": "skip_validation flag set"})
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("⏭️ Skipping validation checks...")
                except ImportError:
                    pass
            
            # Phase 2: Analysis
            if "Analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📊 Running atomic document analysis...")
                except ImportError:
                    pass
                analysis_result = agents["Analysis"].execute(run_context=run_context)
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
            if "Statistical" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "statistical"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📈 Running statistical analysis...")
                except ImportError:
                    pass
                # Debug: Check run_context before calling StatisticalAgent
                audit.log_agent_event("FullExperimentStrategy", "debug_run_context", {
                    "analysis_artifacts": getattr(run_context, 'analysis_artifacts', None),
                    "analysis_results": getattr(run_context, 'analysis_results', None)
                })
                
                statistical_result = agents["Statistical"].execute(run_context=run_context)
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

                # Load statistical analysis results into RunContext for synthesis agent
                statistical_artifact_hash = None
                for artifact in statistical_result.artifacts:
                    if artifact.get("type") == "statistical_analysis":
                        statistical_artifact_hash = artifact.get("metadata", {}).get("artifact_hash")
                        break
                
                if statistical_artifact_hash:
                    try:
                        stats_content_bytes = storage.get_artifact(statistical_artifact_hash)
                        stats_data = json.loads(stats_content_bytes.decode('utf-8'))
                        run_context.statistical_results = stats_data.get("statistical_analysis_content")
                        audit.log_agent_event("FullExperimentStrategy", "statistical_results_loaded", {
                            "statistical_artifact_hash": statistical_artifact_hash,
                            "content_length": len(run_context.statistical_results) if run_context.statistical_results else 0
                        })
                    except Exception as e:
                        audit.log_agent_event("FullExperimentStrategy", "statistical_results_load_error", {
                            "error": str(e),
                            "statistical_artifact_hash": statistical_artifact_hash
                        })
                        # This is a critical failure, we should not proceed without statistical results
                        return ExperimentResult(
                            success=False,
                            phases_completed=phases_completed,
                            artifacts=artifacts,
                            metadata=metadata,
                            error_message=f"Failed to load critical statistical results: {str(e)}"
                        )

                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "statistical"})
            
            # Phase 4: Evidence retrieval
            if "Evidence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "evidence"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Gathering evidence from documents...")
                except ImportError:
                    pass
                evidence_result = agents["Evidence"].execute(run_context=run_context)
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

                # Load evidence retrieval results into RunContext for synthesis agent
                evidence_artifact_hash = evidence_result.metadata.get("evidence_artifact_hash")
                if evidence_artifact_hash:
                    try:
                        evidence_content = storage.get_artifact(evidence_artifact_hash)
                        evidence_data = json.loads(evidence_content.decode('utf-8'))
                        run_context.evidence = evidence_data.get("evidence_results", [])
                        audit.log_agent_event("FullExperimentStrategy", "evidence_loaded", {
                            "evidence_artifact_hash": evidence_artifact_hash,
                            "evidence_findings": len(run_context.evidence)
                        })
                    except Exception as e:
                        audit.log_agent_event("FullExperimentStrategy", "evidence_load_error", {
                            "error": str(e),
                            "evidence_artifact_hash": evidence_artifact_hash
                        })
                        # Continue execution - evidence might come from other sources

                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "evidence"})
            
            # Phase 5: Synthesis
            if "Synthesis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "synthesis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📝 Generating research report...")
                except ImportError:
                    pass
                synthesis_result = agents["Synthesis"].execute(run_context=run_context)
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
            if run_context.metadata.get("verification_enabled", True) and "Verification" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "verification"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("✅ Verifying research findings...")
                except ImportError:
                    pass
                verification_result = agents["Verification"].execute(run_context=run_context)
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

    def _load_corpus_documents(self, corpus_manifest_path: Path) -> Optional[List[Dict[str, str]]]:
        """Load individual documents based on the corpus manifest."""
        try:
            if not corpus_manifest_path.exists():
                return None
            
            manifest_text = corpus_manifest_path.read_text(encoding='utf-8')

            # Extract YAML block from markdown
            yaml_match = re.search(r"```yaml\n(.*?)```", manifest_text, re.DOTALL)
            if not yaml_match:
                # Assume the whole file is YAML if no markdown fence is found
                yaml_content = manifest_text
            else:
                yaml_content = yaml_match.group(1)

            manifest = yaml.safe_load(yaml_content)
            
            documents = []
            corpus_dir = corpus_manifest_path.parent
            
            for doc_info in manifest.get('documents', []):
                doc_path = corpus_dir / doc_info['filename']
                if doc_path.exists():
                    content = doc_path.read_text(encoding='utf-8')
                    documents.append({
                        "id": doc_info.get('document_id', doc_info['filename']),
                        "content": content,
                    })
            return documents
        except Exception as e:
            # Potentially log this error
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
            # THIN PRINCIPLE: Orchestrator handles file I/O, not agents
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            corpus_manifest_path = Path(run_context.corpus_path)
            corpus_documents = self._load_corpus_documents(corpus_manifest_path)
            corpus_manifest_content = corpus_manifest_path.read_text(encoding='utf-8')

            if not framework_content:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load framework content"
                )
            
            if not corpus_documents:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load corpus documents"
                )

            run_context.metadata["framework_content"] = framework_content
            run_context.metadata["corpus_documents"] = corpus_documents
            run_context.metadata["corpus_manifest_content"] = corpus_manifest_content

            # Phase 1: Validation (skip if flag is set)
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents and not skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "validation"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Running validation checks...")
                except ImportError:
                    pass
                validation_result = agents["Validation"].execute(run_context=run_context)
                if not validation_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Validation failed: {validation_result.error_message}"
                    )
                phases_completed.append("validation")
                artifacts.extend(validation_result.artifacts)
                run_context.update_phase("validation")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "validation"})
            elif skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_skipped", {"phase": "validation", "reason": "skip_validation flag set"})
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("⏭️ Skipping validation checks...")
                except ImportError:
                    pass
            
            # Phase 2: Analysis
            if "Analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📊 Running atomic document analysis...")
                except ImportError:
                    pass
                analysis_result = agents["Analysis"].execute(run_context=run_context)
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

    def _load_corpus_documents(self, corpus_manifest_path: Path) -> Optional[List[Dict[str, str]]]:
        """Load individual documents based on the corpus manifest."""
        try:
            if not corpus_manifest_path.exists():
                return None
            
            manifest_text = corpus_manifest_path.read_text(encoding='utf-8')
            
            # Extract YAML block from markdown
            yaml_match = re.search(r"```yaml\n(.*?)```", manifest_text, re.DOTALL)
            if not yaml_match:
                # Assume the whole file is YAML if no markdown fence is found
                yaml_content = manifest_text
            else:
                yaml_content = yaml_match.group(1)

            manifest = yaml.safe_load(yaml_content)
            
            documents = []
            corpus_dir = corpus_manifest_path.parent
            
            for doc_info in manifest.get('documents', []):
                doc_path = corpus_dir / doc_info['filename']
                if doc_path.exists():
                    content = doc_path.read_text(encoding='utf-8')
                    documents.append({
                        "id": doc_info.get('document_id', doc_info['filename']),
                        "content": content,
                    })
            return documents
        except Exception as e:
            # Potentially log this error
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
            # THIN PRINCIPLE: Orchestrator handles file I/O, not agents
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            corpus_manifest_path = Path(run_context.corpus_path)
            corpus_documents = self._load_corpus_documents(corpus_manifest_path)
            corpus_manifest_content = corpus_manifest_path.read_text(encoding='utf-8')

            if not framework_content:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load framework content"
                )
            
            if not corpus_documents:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to load corpus documents"
                )

            run_context.metadata["framework_content"] = framework_content
            run_context.metadata["corpus_documents"] = corpus_documents
            run_context.metadata["corpus_manifest_content"] = corpus_manifest_content
            
            # Phase 1: Validation (skip if flag is set)
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents and not skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "validation"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Running validation checks...")
                except ImportError:
                    pass
                validation_result = agents["Validation"].execute(run_context=run_context)
                if not validation_result.success:
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message=f"Validation failed: {validation_result.error_message}"
                    )
                phases_completed.append("validation")
                artifacts.extend(validation_result.artifacts)
                run_context.update_phase("validation")
                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "validation"})
            elif skip_validation:
                audit.log_agent_event("FullExperimentStrategy", "phase_skipped", {"phase": "validation", "reason": "skip_validation flag set"})
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("⏭️ Skipping validation checks...")
                except ImportError:
                    pass
            
            # Phase 2: Analysis
            if "Analysis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "analysis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📊 Running atomic document analysis...")
                except ImportError:
                    pass
                analysis_result = agents["Analysis"].execute(run_context=run_context)
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
            if "Statistical" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "statistical"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📈 Running statistical analysis...")
                except ImportError:
                    pass
                # Debug: Check run_context before calling StatisticalAgent
                audit.log_agent_event("FullExperimentStrategy", "debug_run_context", {
                    "analysis_artifacts": getattr(run_context, 'analysis_artifacts', None),
                    "analysis_results": getattr(run_context, 'analysis_results', None)
                })
                
                statistical_result = agents["Statistical"].execute(run_context=run_context)
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

                # Load statistical analysis results into RunContext for synthesis agent
                statistical_artifact_hash = None
                for artifact in statistical_result.artifacts:
                    if artifact.get("type") == "statistical_analysis":
                        statistical_artifact_hash = artifact.get("metadata", {}).get("artifact_hash")
                        break
                
                if statistical_artifact_hash:
                    try:
                        stats_content_bytes = storage.get_artifact(statistical_artifact_hash)
                        stats_data = json.loads(stats_content_bytes.decode('utf-8'))
                        run_context.statistical_results = stats_data.get("statistical_analysis_content")
                        audit.log_agent_event("FullExperimentStrategy", "statistical_results_loaded", {
                            "statistical_artifact_hash": statistical_artifact_hash,
                            "content_length": len(run_context.statistical_results) if run_context.statistical_results else 0
                        })
                    except Exception as e:
                        audit.log_agent_event("FullExperimentStrategy", "statistical_results_load_error", {
                            "error": str(e),
                            "statistical_artifact_hash": statistical_artifact_hash
                        })
                        # This is a critical failure, we should not proceed without statistical results
                        return ExperimentResult(
                            success=False,
                            phases_completed=phases_completed,
                            artifacts=artifacts,
                            metadata=metadata,
                            error_message=f"Failed to load critical statistical results: {str(e)}"
                        )

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

    def _load_corpus_documents(self, corpus_manifest_path: Path) -> Optional[List[Dict[str, str]]]:
        """Load individual documents based on the corpus manifest."""
        try:
            if not corpus_manifest_path.exists():
                return None
            
            manifest_text = corpus_manifest_path.read_text(encoding='utf-8')

            # Extract YAML block from markdown
            yaml_match = re.search(r"```yaml\n(.*?)```", manifest_text, re.DOTALL)
            if not yaml_match:
                # Assume the whole file is YAML if no markdown fence is found
                yaml_content = manifest_text
            else:
                yaml_content = yaml_match.group(1)

            manifest = yaml.safe_load(yaml_content)
            
            documents = []
            corpus_dir = corpus_manifest_path.parent
            
            for doc_info in manifest.get('documents', []):
                doc_path = corpus_dir / doc_info['filename']
                if doc_path.exists():
                    content = doc_path.read_text(encoding='utf-8')
                    documents.append({
                        "id": doc_info.get('document_id', doc_info['filename']),
                        "content": content,
                    })
            return documents
        except Exception as e:
            # Potentially log this error
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
            # THIN PRINCIPLE: Orchestrator handles file I/O, not agents
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            # In resume mode, we may not need to reload all documents, but we need the manifest for context.
            corpus_manifest_path = Path(run_context.corpus_path)
            corpus_manifest_content = corpus_manifest_path.read_text(encoding='utf-8')

            run_context.metadata["framework_content"] = framework_content
            run_context.metadata["corpus_manifest_content"] = corpus_manifest_content

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
            if "Evidence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "evidence"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Gathering evidence from documents...")
                except ImportError:
                    pass
                evidence_result = agents["Evidence"].execute(run_context=run_context)
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

                # Load evidence retrieval results into RunContext for synthesis agent
                evidence_artifact_hash = evidence_result.metadata.get("evidence_artifact_hash")
                if evidence_artifact_hash:
                    try:
                        evidence_content = storage.get_artifact(evidence_artifact_hash)
                        evidence_data = json.loads(evidence_content.decode('utf-8'))
                        run_context.evidence = evidence_data.get("evidence_results", [])
                        audit.log_agent_event("FullExperimentStrategy", "evidence_loaded", {
                            "evidence_artifact_hash": evidence_artifact_hash,
                            "evidence_findings": len(run_context.evidence)
                        })
                    except Exception as e:
                        audit.log_agent_event("FullExperimentStrategy", "evidence_load_error", {
                            "error": str(e),
                            "evidence_artifact_hash": evidence_artifact_hash
                        })
                        # Continue execution - evidence might come from other sources

                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "evidence"})
            
            # Phase 2: Synthesis
            if "Synthesis" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "synthesis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📝 Generating research report...")
                except ImportError:
                    pass
                synthesis_result = agents["Synthesis"].execute(run_context=run_context)
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
            if run_context.metadata.get("verification_enabled", True) and "Verification" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "verification"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("✅ Verifying research findings...")
                except ImportError:
                    pass
                verification_result = agents["Verification"].execute(run_context=run_context)
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
