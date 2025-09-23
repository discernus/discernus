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
    Complete experiment execution with simplified alpha pipeline.
    
    Phases:
    1. Coherence validation (optional)
    2. Analysis (4 steps: composite, evidence, scores, markup)
    3. Statistical analysis (with framework-corpus fit)
    4. Evidence retrieval
    5. Synthesis (two-stage: data-driven + evidence integration)
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
            # Phase 1: Validation (always required to populate file paths)
            # ValidationAgent will populate framework_path and corpus_path
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "validation"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        if skip_validation:
                            rich_console.print_info("🔍 Loading experiment files (validation skipped)...")
                        else:
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
            
            # Pure Postal Service: ValidationAgent has already registered all source files in CAS
            # Orchestrator just passes hash addresses - no parsing, no file I/O
            
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
                    # THIN: Pass artifact hash, let synthesis agent read it directly
                    run_context.statistical_artifacts = [statistical_artifact_hash]
                    audit.log_agent_event("FullExperimentStrategy", "statistical_artifacts_passed", {
                        "statistical_artifact_hash": statistical_artifact_hash
                    })
                else:
                    audit.log_agent_event("FullExperimentStrategy", "no_statistical_artifacts", {})
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message="No statistical analysis artifacts found"
                    )

                audit.log_agent_event("FullExperimentStrategy", "phase_complete", {"phase": "statistical"})
            
            # Phase 4: Evidence retrieval
            if "Evidence" in agents:
                audit.log_agent_event("FullExperimentStrategy", "phase_start", {"phase": "evidence"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📖 Retrieving supporting evidence...")
                except ImportError:
                    pass

                evidence_result = agents["Evidence"].execute(run_context)
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

                # CAS-everywhere: Evidence artifacts are discoverable via metadata, no need to pass pointers
                audit.log_agent_event("FullExperimentStrategy", "evidence_artifacts_created", {
                    "evidence_artifact_count": len(evidence_result.artifacts)
                })

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
            
            # Verification phase removed for alpha - synthesis is the final step
            
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
            corpus_dir = corpus_manifest_path.parent / 'corpus'
            
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
            # Phase 1: Validation (always required to populate file paths)
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents:
                audit.log_agent_event("AnalysisOnlyStrategy", "phase_start", {"phase": "validation"})
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
                audit.log_agent_event("AnalysisOnlyStrategy", "phase_complete", {"phase": "validation"})
            
            # Validate paths exist after ValidationAgent has populated them
            if not run_context.framework_path or not Path(run_context.framework_path).exists():
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Framework file not found: {run_context.framework_path}"
                )

            if not run_context.corpus_path or not Path(run_context.corpus_path).exists():
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Corpus manifest not found: {run_context.corpus_path}"
                )
            
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
            corpus_dir = corpus_manifest_path.parent / 'corpus'
            
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
                    # THIN: Pass artifact hash, let synthesis agent read it directly
                    run_context.statistical_artifacts = [statistical_artifact_hash]
                    audit.log_agent_event("FullExperimentStrategy", "statistical_artifacts_passed", {
                        "statistical_artifact_hash": statistical_artifact_hash
                    })
                else:
                    audit.log_agent_event("FullExperimentStrategy", "no_statistical_artifacts", {})
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message="No statistical analysis artifacts found"
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
            corpus_dir = corpus_manifest_path.parent / 'corpus'
            
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

                # THIN: Pass evidence artifact hashes, let synthesis agent read them
                if evidence_result.artifacts:
                    run_context.evidence_artifacts = evidence_result.artifacts
                    audit.log_agent_event("FullExperimentStrategy", "evidence_artifacts_passed", {
                        "evidence_artifacts_count": len(evidence_result.artifacts)
                    })
                else:
                    audit.log_agent_event("FullExperimentStrategy", "no_evidence_artifacts", {})

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
            
            # Verification phase removed for alpha - synthesis is the final step
            
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


class ResumeFromAnalysisStrategy(ExecutionStrategy):
    """
    Resume from analysis artifacts - for continuing experiments after analysis.
    
    Phases:
    1. Load analysis artifacts
    2. Statistical analysis
    3. Evidence retrieval
    4. Synthesis
    """
    
    def execute(self, 
                agents: Dict[str, StandardAgent], 
                run_context: RunContext,
                storage: LocalArtifactStorage,
                audit: AuditLogger) -> ExperimentResult:
        """Execute resume from analysis artifacts pipeline"""
        
        start_time = datetime.now(timezone.utc)
        phases_completed = []
        artifacts = []
        metadata = {}
        
        try:
            # Phase 1: Validation (always required to populate file paths)
            skip_validation = run_context.metadata.get("skip_validation", False)
            if "Validation" in agents:
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_start", {"phase": "validation"})
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
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_complete", {"phase": "validation"})
            
            # Validate paths exist after ValidationAgent has populated them
            if not run_context.framework_path or not Path(run_context.framework_path).exists():
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Framework file not found: {run_context.framework_path}"
                )

            if not run_context.corpus_path or not Path(run_context.corpus_path).exists():
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message=f"Corpus manifest not found: {run_context.corpus_path}"
                )
            
            # THIN PRINCIPLE: Orchestrator handles file I/O, not agents
            framework_content = self._load_framework_content(Path(run_context.framework_path))
            corpus_manifest_path = Path(run_context.corpus_path)
            corpus_documents = self._load_corpus_documents(corpus_manifest_path)
            corpus_manifest_content = corpus_manifest_path.read_text(encoding='utf-8')

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

            # Load analysis artifacts from the most recent completed analysis run
            analysis_artifacts = self._load_latest_analysis_artifacts(run_context.experiment_id)
            if not analysis_artifacts:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="No analysis artifacts found for resume"
                )
            
            # Copy analysis artifacts to current run's storage
            copied_artifacts = self._copy_analysis_artifacts(analysis_artifacts, run_context.experiment_id, storage)
            if not copied_artifacts:
                return ExperimentResult(
                    success=False,
                    phases_completed=phases_completed,
                    artifacts=artifacts,
                    metadata=metadata,
                    error_message="Failed to copy analysis artifacts for resume"
                )
            
            # Set the copied analysis artifacts in run_context
            run_context.analysis_artifacts = copied_artifacts
            
            # Phase 1: Statistical analysis
            if "Statistical" in agents:
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_start", {"phase": "statistical"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📈 Running statistical analysis...")
                except ImportError:
                    pass
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
                    # THIN: Pass artifact hash, let synthesis agent read it directly
                    run_context.statistical_artifacts = [statistical_artifact_hash]
                    audit.log_agent_event("ResumeFromAnalysisStrategy", "statistical_artifacts_passed", {
                        "statistical_artifact_hash": statistical_artifact_hash
                    })
                else:
                    audit.log_agent_event("ResumeFromAnalysisStrategy", "no_statistical_artifacts", {})
                    return ExperimentResult(
                        success=False,
                        phases_completed=phases_completed,
                        artifacts=artifacts,
                        metadata=metadata,
                        error_message="No statistical analysis artifacts found"
                    )

                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_complete", {"phase": "statistical"})
            
            # Phase 2: Evidence retrieval
            if "Evidence" in agents:
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_start", {"phase": "evidence"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("🔍 Running evidence retrieval...")
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

                # THIN: Pass evidence artifact hashes, let synthesis agent read them
                if evidence_result.artifacts:
                    run_context.evidence_artifacts = evidence_result.artifacts
                    audit.log_agent_event("ResumeFromAnalysisStrategy", "evidence_artifacts_passed", {
                        "evidence_artifacts_count": len(evidence_result.artifacts)
                    })
                else:
                    audit.log_agent_event("ResumeFromAnalysisStrategy", "no_evidence_artifacts", {})

                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_complete", {"phase": "evidence"})
            
            # Phase 3: Synthesis
            if "Synthesis" in agents:
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_start", {"phase": "synthesis"})
                # Show progress to user
                try:
                    from ..cli_console import rich_console
                    if rich_console:
                        rich_console.print_info("📝 Running synthesis...")
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
                audit.log_agent_event("ResumeFromAnalysisStrategy", "phase_complete", {"phase": "synthesis"})
            
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

    def _load_latest_analysis_artifacts(self, experiment_id: str) -> Optional[List[str]]:
        """Load analysis artifacts from the most recent completed analysis run."""
        try:
            # Find the experiment directory
            experiment_path = Path(f"projects/{experiment_id}")
            if not experiment_path.exists():
                return None
            
            # Find all runs with analysis artifacts
            runs_dir = experiment_path / "runs"
            if not runs_dir.exists():
                return None
            
            # Look for runs that have analysis artifacts (composite_analysis, evidence_extraction, score_extraction)
            analysis_runs = []
            for run_dir in runs_dir.iterdir():
                if run_dir.is_dir():
                    artifacts_dir = run_dir / "artifacts"
                    if artifacts_dir.exists():
                        # Check if this run has analysis artifacts
                        has_composite = any(artifacts_dir.glob("composite_analysis_*.json"))
                        has_evidence = any(artifacts_dir.glob("evidence_extraction_*.json"))
                        has_scores = any(artifacts_dir.glob("score_extraction_*.json"))
                        
                        if has_composite and has_evidence and has_scores:
                            analysis_runs.append(run_dir)
            
            if not analysis_runs:
                return None
            
            # Get the most recent run
            latest_run = max(analysis_runs, key=lambda p: p.stat().st_mtime)
            
            # Load artifact hashes from the artifact registry
            artifact_registry_path = latest_run / "artifacts" / "artifact_registry.json"
            if not artifact_registry_path.exists():
                return None
            
            with open(artifact_registry_path, 'r') as f:
                artifact_registry = json.load(f)
            
            # Extract analysis artifact hashes
            analysis_artifacts = []
            for artifact_hash, artifact_info in artifact_registry.items():
                artifact_type = artifact_info.get("metadata", {}).get("artifact_type")
                if artifact_type in ["composite_analysis", "evidence_extraction", "score_extraction", "marked_up_document"]:
                    analysis_artifacts.append(artifact_hash)
            
            return analysis_artifacts
            
        except Exception as e:
            return None

    def _copy_analysis_artifacts(self, analysis_artifacts: List[str], experiment_id: str, storage) -> Optional[List[str]]:
        """Copy analysis artifacts from the source run to the current run's storage."""
        try:
            # Find the source run directory
            experiment_path = Path(f"projects/{experiment_id}")
            runs_dir = experiment_path / "runs"
            
            # Find the most recent run with analysis artifacts
            analysis_runs = []
            for run_dir in runs_dir.iterdir():
                if run_dir.is_dir():
                    artifacts_dir = run_dir / "artifacts"
                    if artifacts_dir.exists():
                        has_composite = any(artifacts_dir.glob("composite_analysis_*.json"))
                        has_evidence = any(artifacts_dir.glob("evidence_extraction_*.json"))
                        has_scores = any(artifacts_dir.glob("score_extraction_*.json"))
                        
                        if has_composite and has_evidence and has_scores:
                            analysis_runs.append(run_dir)
            
            if not analysis_runs:
                return None
            
            latest_run = max(analysis_runs, key=lambda p: p.stat().st_mtime)
            source_artifacts_dir = latest_run / "artifacts"
            
            # Load artifact registry from source run
            artifact_registry_path = source_artifacts_dir / "artifact_registry.json"
            if not artifact_registry_path.exists():
                return None
            
            with open(artifact_registry_path, 'r') as f:
                artifact_registry = json.load(f)
            
            # Copy each analysis artifact to current storage
            copied_artifacts = []
            for artifact_hash in analysis_artifacts:
                if artifact_hash in artifact_registry:
                    artifact_info = artifact_registry[artifact_hash]
                    artifact_path = source_artifacts_dir / artifact_info["artifact_path"]
                    
                    if artifact_path.exists():
                        # Read the artifact content
                        with open(artifact_path, 'rb') as f:
                            artifact_bytes = f.read()
                        
                        # Store in current run's storage
                        new_hash = storage.put_artifact(artifact_bytes, artifact_info.get("metadata", {}))
                        copied_artifacts.append(new_hash)
            
            return copied_artifacts
            
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
            corpus_dir = corpus_manifest_path.parent / 'corpus'
            
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
