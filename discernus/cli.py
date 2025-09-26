#!/usr/bin/env python3
"""
Discernus CLI v2.1 - Streamlined Researcher Interface
===================================================

Core Commands for Research Workflow:
- discernus run <experiment_path>       - Execute V2 experiment with phase selection
- discernus resume <experiment_path>    - Resume experiment from existing run
- discernus validate <experiment_path>  - Validate experiment structure and configuration
- discernus artifacts <experiment_path>  - Show experiment artifacts and cache status
- discernus costs <experiment_path>     - Show cost breakdown for experiment runs
- discernus status                      - Show system status and component availability

Phase Selection (V2 Architecture):
- discernus run --from validation --to synthesis     - Complete experiment (default)
- discernus run --from analysis --to statistical     - Analysis and statistical phases only
- discernus run --from evidence --to synthesis        - Evidence retrieval and synthesis only
- discernus run --from validation --to validation     - Validation phase only

Resume Functionality:
- discernus run --resume                              - Auto-resume from most recent compatible run
- discernus run --run-dir <run_id>                    - Resume from specific run directory
- discernus resume --from statistical --to synthesis  - Resume from statistical phase
- discernus resume --run-dir <run_id> --from analysis - Resume from specific run

Advanced Options:
- discernus run --verbose-trace                       - Enable comprehensive function-level tracing
- discernus run --skip-validation                     - Skip experiment coherence validation
- discernus run --trace-filter <component>            - Filter tracing to specific components

For detailed usage, see: docs/user/CLI_REFERENCE.md
"""

import click
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, continue without it

# Disable huggingface tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# CleanAnalysisOrchestrator deprecated - using V2 orchestrator only
from discernus.core.config import get_config, get_config_file_path

# Rich CLI integration for professional terminal interface
from .cli_console import rich_console, ExperimentProgressManager

# Apply comprehensive LiteLLM debug suppression before any litellm imports
from discernus.core.logging_config import ensure_litellm_debug_suppression
ensure_litellm_debug_suppression()

# Import LLM Gateway after suppression is configured
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

# Import validation and orchestration components
from discernus.core.validation import ValidationResult, ValidationIssue

# ============================================================================
# EXIT FUNCTIONS
# ============================================================================

def exit_success():
    """Exit with success status."""
    sys.exit(0)

def exit_invalid_usage(message: str):
    """Exit with invalid usage error."""
    rich_console.print_error(f"❌ {message}")
    sys.exit(2)

def exit_file_error(message: str):
    """Exit with file error."""
    rich_console.print_error(f"❌ File Error: {message}")
    sys.exit(3)

def exit_general_error(message: str):
    """Exit with general error."""
    rich_console.print_error(f"❌ Error: {message}")
    sys.exit(1)

def exit_infrastructure_error(message: str):
    """Exit with infrastructure error."""
    rich_console.print_error(f"❌ Infrastructure Error: {message}")
    sys.exit(4)

def exit_validation_failed(message: str):
    """Exit with validation failure."""
    rich_console.print_error(f"❌ Validation Failed: {message}")
    sys.exit(5)


# V2 Imports
from discernus.core.v2_orchestrator import V2Orchestrator, V2OrchestratorConfig
# Removed: execution_strategies import - using SimpleExperimentExecutor instead
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.analysis_agent.v2_analysis_agent import V2AnalysisAgent
from discernus.agents.statistical_agent.v2_statistical_agent import V2StatisticalAgent
from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
from discernus.agents.two_stage_synthesis_agent import TwoStageSynthesisAgent
from discernus.agents.validation_agent.v2_validation_agent import V2ValidationAgent


# Removed _parse_experiment_spec function - THIN architecture delegates file parsing to ValidationAgent


def _validate_models(models_to_validate: List[tuple[str, str]]):
    """Validate that specified models are available in the registry."""
    try:
        registry = ModelRegistry()
        for model_type, model_name in models_to_validate:
            if not registry.get_model_details(model_name):
                rich_console.print_error(f"❌ {model_type} model '{model_name}' is not available")
                rich_console.print_info(f"   Available models: {', '.join(registry.list_models())}")
                exit_invalid_usage(f"Model '{model_name}' not available")
    except Exception as e:
        rich_console.print_error(f"❌ Model validation failed: {e}")
        exit_infrastructure_error(f"Model validation failed: {e}")

def _validate_corpus_documents(experiment_path: Path, corpus_manifest_path: Path) -> tuple[bool, str]:
    """Validate that all corpus documents referenced in manifest exist."""
    try:
        with open(corpus_manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        
        documents = manifest_data.get('documents', [])
        missing_docs = []
        
        for doc in documents:
            doc_path = experiment_path / doc.get('path', '')
            if not doc_path.exists():
                missing_docs.append(str(doc_path))
        
        if missing_docs:
            return False, f"Missing corpus documents: {', '.join(missing_docs)}"
        
        return True, "All corpus documents found"
        
    except Exception as e:
        return False, f"❌ Corpus validation error: {str(e)}"

# Main CLI group
@click.group()
@click.version_option(version='2.0.0', prog_name='Discernus')
@click.pass_context
def cli(ctx):
    """Discernus - Computational Social Science Research Platform (THIN v2.0)
    
    \b
    Quick Start:
      discernus validate projects/my_experiment/  # Validate experiment first
      discernus run projects/my_experiment/       # Run complete experiment
      discernus status                            # Check system status
    
    \b
    Common Examples:
      discernus run                               # Run experiment in current directory
      discernus validate                          # Validate experiment structure
      discernus artifacts                         # Show experiment artifacts
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

# ============================================================================
# RESUME FUNCTIONALITY
# ============================================================================

def find_resumable_run(experiment_path: Path, start_phase: str) -> Optional[Path]:
    """
    Find a resumable run directory that has completed phases up to start_phase.
    
    Args:
        experiment_path: Path to experiment directory
        start_phase: Phase to resume from
        
    Returns:
        Path to resumable run directory, or None if none found
    """
    runs_dir = experiment_path / 'runs'
    if not runs_dir.exists():
        return None
    
    # Get all run directories, sorted by name (most recent first)
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    run_dirs.sort(key=lambda x: x.name, reverse=True)
    
    # Define phase order for validation
    phases = ['validation', 'analysis', 'statistical', 'evidence', 'synthesis']
    start_idx = phases.index(start_phase)
    
    for run_dir in run_dirs:
        # Check if this run has the required artifacts for start_phase
        if _has_required_artifacts(run_dir, start_phase, phases[:start_idx]):
            return run_dir
    
    return None

def _has_required_artifacts(run_dir: Path, start_phase: str, required_phases: List[str]) -> bool:
    """
    Check if a run directory has the required artifacts for the start phase.
    
    Args:
        run_dir: Path to run directory
        start_phase: Phase to resume from
        required_phases: List of phases that must be completed before start_phase
        
    Returns:
        True if all required artifacts exist
    """
    artifacts_dir = run_dir / 'artifacts'
    if not artifacts_dir.exists():
        return False
    
    # Check for phase-specific artifacts
    phase_artifacts = {
        'validation': ['validation_report'],
        'analysis': ['composite_analysis', 'evidence_extraction', 'score_extraction'],
        'statistical': ['statistical_analysis'],
        'evidence': ['curated_evidence'],
        'synthesis': ['synthesis_report', 'final_synthesis_report']
    }
    
    # Check if start_phase artifacts exist
    if start_phase in phase_artifacts:
        required_artifacts = phase_artifacts[start_phase]
        for artifact_type in required_artifacts:
            if not _has_artifact_type(artifacts_dir, artifact_type):
                return False
    
    # Check if all required previous phases are completed
    for phase in required_phases:
        if phase in phase_artifacts:
            phase_complete = any(_has_artifact_type(artifacts_dir, artifact_type) 
                               for artifact_type in phase_artifacts[phase])
            if not phase_complete:
                return False
    
    return True

def _has_artifact_type(artifacts_dir: Path, artifact_type: str) -> bool:
    """Check if artifacts directory contains artifacts of the specified type."""
    registry_file = artifacts_dir / 'artifact_registry.json'
    if not registry_file.exists():
        return False
    
    try:
        import json
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        
        # Check if any artifact has the required type
        for artifact_data in registry.values():
            metadata = artifact_data.get('metadata', {})
            if metadata.get('artifact_type') == artifact_type:
                return True
        
        return False
    except Exception:
        return False

def copy_artifacts_between_runs(source_storage, target_storage, required_phases: List[str]) -> None:
    """
    Copy artifacts from source run to target run for resume functionality.
    
    Args:
        source_storage: LocalArtifactStorage for source run
        target_storage: LocalArtifactStorage for target run
        required_phases: List of phases whose artifacts should be copied
    """
    # Define artifact types for each phase
    phase_artifacts = {
        'validation': ['validation_report', 'framework', 'corpus_manifest', 'experiment_spec', 'corpus_document'],
        'analysis': ['composite_analysis', 'evidence_extraction', 'score_extraction', 'marked_up_document'],
        'statistical': ['statistical_analysis', 'statistical_verification', 'derived_metrics'],
        'evidence': ['curated_evidence'],
        'synthesis': ['synthesis_report', 'final_synthesis_report', 'stage1_synthesis_report']
    }
    
    # Get all artifacts to copy
    artifacts_to_copy = []
    for phase in required_phases:
        if phase in phase_artifacts:
            artifacts_to_copy.extend(phase_artifacts[phase])
    
    # Copy artifacts and merge registries
    for artifact_type in artifacts_to_copy:
        source_artifacts = source_storage.find_artifacts_by_metadata(artifact_type=artifact_type)
        for artifact_hash in source_artifacts:
            try:
                # Get artifact content and metadata from source
                artifact_content = source_storage.get_artifact(artifact_hash)
                artifact_metadata = source_storage.get_artifact_metadata(artifact_hash)
                
                # Store in target with source_run tracking
                updated_metadata = artifact_metadata.copy()
                updated_metadata['source_run'] = source_storage.run_name
                
                target_storage.put_artifact(artifact_content, updated_metadata)
                
            except Exception as e:
                print(f"⚠️ Warning: Could not copy artifact {artifact_hash}: {e}")

# ============================================================================
# CORE COMMANDS
# ============================================================================

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True, path_type=str))
@click.option('--verbose-trace', is_flag=True, help='Enable comprehensive function-level tracing for debugging')
@click.option('--trace-filter', multiple=True, help='Filter tracing to specific components (e.g., statistical, analysis)')
@click.option('--skip-validation', is_flag=True, help='Skip experiment coherence validation for faster execution')
@click.option('--from', 'start_phase', 
              type=click.Choice(['validation', 'analysis', 'statistical', 'evidence', 'synthesis']),
              default='validation', help='Start from this phase (default: validation)')
@click.option('--to', 'end_phase',
              type=click.Choice(['validation', 'analysis', 'statistical', 'evidence', 'synthesis']), 
              default='synthesis', help='End at this phase (default: synthesis)')
@click.option('--resume', is_flag=True, help='Resume from existing run with completed phases')
@click.option('--run-dir', type=str, help='Specify specific run directory to resume from')
@click.pass_context
def run(ctx, experiment_path: str, verbose_trace: bool, trace_filter: tuple, skip_validation: bool, 
        start_phase: str, end_phase: str, resume: bool, run_dir: str):
    """Execute a V2 experiment with simple phase selection."""
    exp_path = Path(experiment_path).resolve()

    # Validate phase parameters
    phases = ['validation', 'analysis', 'statistical', 'evidence', 'synthesis']
    if start_phase not in phases:
        rich_console.print_error(f"❌ Invalid start phase: {start_phase}")
        exit_invalid_usage(f"Start phase must be one of: {', '.join(phases)}")
    
    if end_phase not in phases:
        rich_console.print_error(f"❌ Invalid end phase: {end_phase}")
        exit_invalid_usage(f"End phase must be one of: {', '.join(phases)}")
    
    start_idx = phases.index(start_phase)
    end_idx = phases.index(end_phase)
    
    if start_idx > end_idx:
        rich_console.print_error(f"❌ Start phase ({start_phase}) cannot be after end phase ({end_phase})")
        exit_invalid_usage("Start phase must come before or equal end phase")

    if not exp_path.exists() or not exp_path.is_dir():
        rich_console.print_error(f"❌ Experiment path not found: {exp_path}")
        exit_file_error("Experiment path not found.")

    rich_console.print_section(f"🚀 Running V2 Experiment: {exp_path.name}")

    # Setup verbose tracing if requested
    if verbose_trace:
        from .core.verbose_tracing import setup_verbose_tracing
        setup_verbose_tracing(enabled=True, filters=list(trace_filter) if trace_filter else None)
        rich_console.print_info(f"🔍 Verbose tracing enabled" + (f" (filters: {', '.join(trace_filter)})" if trace_filter else ""))

    try:
        # 1. Handle resume functionality
        source_run_dir = None
        if resume or run_dir:
            if run_dir:
                # Use specified run directory
                source_run_dir = exp_path / "runs" / run_dir
                if not source_run_dir.exists():
                    rich_console.print_error(f"❌ Specified run directory not found: {run_dir}")
                    exit_file_error("Run directory not found.")
            else:
                # Find resumable run automatically
                source_run_dir = find_resumable_run(exp_path, start_phase)
                if not source_run_dir:
                    rich_console.print_error(f"❌ No resumable run found for phase: {start_phase}")
                    rich_console.print_info("💡 Tip: Use --run-dir to specify a specific run directory")
                    exit_general_error("No resumable run found.")
            
            rich_console.print_info(f"🔄 Resuming from run: {source_run_dir.name}")

        # 2. Initialize core components
        run_name = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_folder = exp_path / "runs" / run_name
        run_folder.mkdir(parents=True, exist_ok=True)

        security = ExperimentSecurityBoundary(exp_path)
        storage = LocalArtifactStorage(security, run_folder, run_name)
        audit = AuditLogger(security, run_folder)

        # 3. Copy artifacts from source run if resuming
        if source_run_dir:
            source_storage = LocalArtifactStorage(security, source_run_dir, source_run_dir.name)
            
            # Determine which phases to copy based on start_phase
            phases = ['validation', 'analysis', 'statistical', 'evidence', 'synthesis']
            start_idx = phases.index(start_phase)
            phases_to_copy = phases[:start_idx]
            
            if phases_to_copy:
                rich_console.print_info(f"📦 Copying artifacts from phases: {', '.join(phases_to_copy)}")
                copy_artifacts_between_runs(source_storage, storage, phases_to_copy)
                rich_console.print_success("✅ Artifacts copied successfully")

        # 4. Verify experiment.md exists (basic check only - ValidationAgent will do full validation)
        experiment_file = exp_path / "experiment.md"
        if not experiment_file.exists():
            rich_console.print_error(f"❌ experiment.md not found in: {exp_path}")
            exit_file_error("experiment.md not found.")

        # 5. Configure Orchestrator (THIN architecture - let ValidationAgent handle file discovery)
        config = V2OrchestratorConfig(
            experiment_id=exp_path.name,
            experiment_dir=str(exp_path),
            output_dir=str(run_folder),
            skip_validation=skip_validation
        )

        orchestrator = V2Orchestrator(config, security, storage, audit)

        # 6. Register Agents
        orchestrator.register_agent("Validation", V2ValidationAgent(security, storage, audit))
        orchestrator.register_agent("Analysis", V2AnalysisAgent(security, storage, audit))
        orchestrator.register_agent("Statistical", V2StatisticalAgent(security, storage, audit))
        orchestrator.register_agent("Evidence", IntelligentEvidenceRetrievalAgent(security, storage, audit))
        orchestrator.register_agent("Synthesis", TwoStageSynthesisAgent(security, storage, audit))

        # 7. Use Simple Executor
        from discernus.core.simple_executor import SimpleExperimentExecutor
        executor = SimpleExperimentExecutor()
        
        # Show execution info
        if start_phase == end_phase:
            rich_console.print_info(f"🔄 Running {start_phase} phase only...")
        else:
            rich_console.print_info(f"🚀 Running phases: {start_phase} → {end_phase}")
        
        # 6. Create RunContext and Execute with Simple Executor
        run_context = orchestrator.create_run_context()
        result = executor.execute(
            agents=orchestrator.agents,
            run_context=run_context,
            storage=orchestrator.storage,
            audit=orchestrator.audit,
            start_phase=start_phase,
            end_phase=end_phase
        )

        # Show experiment summary
        if result.success:
            # Show phase-specific success message
            if start_phase == end_phase:
                rich_console.print_success(f"✅ {start_phase.title()} Phase Completed Successfully!")
            else:
                rich_console.print_success(f"✅ Phases {start_phase} → {end_phase} Completed Successfully!")

            # Show phase progress
            phases_completed = result.phases_completed
            if phases_completed:
                rich_console.print_info(f"📊 Phases completed: {', '.join(phases_completed)}")
            else:
                rich_console.print_info("📊 No phases completed")

            rich_console.print_info(f"📁 Artifacts saved in: {storage.run_folder}")
            rich_console.print_info(f"⏱️  Total execution time: {result.execution_time_seconds:.1f} seconds")
            
            # Show cost summary
            try:
                cost_summary = orchestrator.audit.get_session_costs()
                if cost_summary and cost_summary.get("total_cost_usd", 0) > 0:
                    rich_console.print_info(f"💰 Total cost: ${cost_summary['total_cost_usd']:.4f}")
                    rich_console.print_info(f"🔢 Total tokens: {cost_summary.get('total_tokens', 0):,}")
                    
                    # Show top cost operations
                    if cost_summary.get("operations"):
                        top_operations = sorted(cost_summary["operations"].items(), 
                                              key=lambda x: x[1]["cost_usd"], reverse=True)[:3]
                        if top_operations:
                            rich_console.print_info("📊 Top operations:")
                            for op, data in top_operations:
                                rich_console.print_info(f"  • {op}: ${data['cost_usd']:.4f} ({data['calls']} calls)")
                else:
                    rich_console.print_info("💰 No cost data recorded")
            except Exception as e:
                rich_console.print_warning(f"⚠️  Could not retrieve cost data: {e}")

            # Show artifact counts by type (if storage available)
            if hasattr(result, 'artifacts') and result.artifacts:
                try:
                    artifact_types = {}
                    for artifact in result.artifacts:
                        if isinstance(artifact, dict):
                            # ExperimentResult.artifacts contains Dict[str, Any] with artifact info
                            # Try both "artifact_type" and "type" fields for compatibility
                            artifact_type = artifact.get("artifact_type") or artifact.get("type", "unknown")
                            
                            # If it's in metadata, try that too
                            if artifact_type == "unknown" and "metadata" in artifact:
                                metadata = artifact["metadata"]
                                artifact_type = metadata.get("artifact_type") or metadata.get("type", "unknown")
                            
                            artifact_types[artifact_type] = artifact_types.get(artifact_type, 0) + 1
                        elif isinstance(artifact, str):
                            # Fallback for string artifacts (hashes)
                            try:
                                artifact_metadata = storage.get_artifact_metadata(artifact)
                                # Try both "artifact_type" and "type" fields in metadata
                                artifact_type = (artifact_metadata.get("artifact_type") or 
                                              artifact_metadata.get("type", "unknown"))
                                artifact_types[artifact_type] = artifact_types.get(artifact_type, 0) + 1
                            except Exception:
                                artifact_types["unknown"] = artifact_types.get("unknown", 0) + 1
                        else:
                            artifact_types["unknown"] = artifact_types.get("unknown", 0) + 1

                    if artifact_types:
                        artifact_summary = ", ".join([f"{count} {type}" for type, count in artifact_types.items()])
                        rich_console.print_info(f"📦 Generated artifacts: {artifact_summary}")
                except Exception as e:
                    # Don't fail the entire CLI if artifact counting fails
                    rich_console.print_info(f"📦 Generated {len(result.artifacts)} artifacts")

            exit_success()
        else:
            rich_console.print_error(f"❌ V2 Experiment Failed: {result.error_message}")
            exit_general_error(result.error_message)

    except Exception as e:
        rich_console.print_error(f"❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit_infrastructure_error(str(e))



@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.pass_context
def validate(ctx, experiment_path: str):
    """Validate experiment structure and configuration.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    """
    exp_path = Path(experiment_path).resolve()
    
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    click.echo(f"🔍 Validating experiment: {exp_path}")
    
    try:
        # Use ExperimentCoherenceAgent for validation
        from discernus.agents.experiment_coherence_agent import ExperimentCoherenceAgent
        
        validator = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-pro")
        result = validator.validate_experiment(exp_path)
        
        # Show results by priority
        blocking = result.get_issues_by_priority("BLOCKING")
        quality = result.get_issues_by_priority("QUALITY") 
        suggestions = result.get_issues_by_priority("SUGGESTION")
        
        if not blocking and not quality and not suggestions:
            rich_console.print_success("✅ Experiment validation passed - no issues found!")
            rich_console.print_info(f"   📁 Experiment: {exp_path}")
            exit_success()
            return
        
        if blocking:
            rich_console.print_error("🚫 BLOCKING Issues (must fix):")
            for issue in blocking:
                rich_console.print_error(f"  • {issue.description}")
                rich_console.print_error(f"    Fix: {issue.fix}")
        
        if quality:
            rich_console.print_warning("⚠️  QUALITY Issues (should fix):")
            for issue in quality:
                rich_console.print_warning(f"  • {issue.description}")
                rich_console.print_warning(f"    Fix: {issue.fix}")
        
        if suggestions:
            rich_console.print_info("💡 SUGGESTIONS (nice to have):")
            for issue in suggestions:
                rich_console.print_info(f"  • {issue.description}")
                rich_console.print_info(f"    Fix: {issue.fix}")
        
        if blocking:
            exit_validation_failed("Experiment validation failed - blocking issues found")
        else:
            rich_console.print_success("✅ Experiment validation passed with warnings/suggestions")
            exit_success()
            
    except Exception as e:
        rich_console.print_error(f"❌ Validation error: {e}")
        exit_general_error(str(e))


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def artifacts(experiment_path: str):
    """Show experiment artifacts and available cache status for resumption. Defaults to current directory."""
    exp_path = Path(experiment_path).resolve()
    
    rich_console.print_section(f"📦 Artifacts: {exp_path.name}")
    
    # Check for runs directory
    runs_dir = exp_path / 'runs'
    if not runs_dir.exists():
        rich_console.print_info("No runs found - experiment has not been executed yet")
        return
    
    # List recent runs
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    run_dirs.sort(key=lambda x: x.name, reverse=True)  # Most recent first
    
    if not run_dirs:
        rich_console.print_info("No completed runs found")
        return
    
    # Show recent runs
    table = rich_console.create_table("Recent Runs", ["Timestamp", "Status", "Artifacts"])
    
    for run_dir in run_dirs[:10]:  # Show last 10 runs
        # Determine status
        if (run_dir / 'synthesis_report.md').exists():
            status = "✅ Complete"
        elif (run_dir / 'analysis_results.csv').exists():
            status = "🔄 Analysis Only"
        else:
            status = "❌ Failed"
        
        # Count artifacts
        artifact_count = len([f for f in run_dir.iterdir() if f.is_file()])
        
        table.add_row(run_dir.name, status, f"{artifact_count} files")
    
    rich_console.print_table(table)
    
    # Show cache status
    cache_dir = exp_path / '.discernus_cache'
    if cache_dir.exists():
        cache_files = list(cache_dir.rglob('*'))
        rich_console.print_info(f"💾 Cache: {len(cache_files)} cached artifacts")
    else:
        rich_console.print_info("💾 Cache: No cached artifacts")

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--detailed', is_flag=True, help='Show detailed cost breakdown by agent and model')
@click.option('--session', is_flag=True, help='Show costs for current session only')
def costs(experiment_path: str, detailed: bool, session: bool):
    """Show cost breakdown for experiment runs"""
    exp_path = Path(experiment_path).resolve()
    
    rich_console.print_section(f"💰 Cost Analysis: {exp_path.name}")
    
    if session:
        # Show current session costs
        try:
            from discernus.core.orchestration import SimpleOrchestrator
            from discernus.core.security_boundary import ExperimentSecurityBoundary
            
            security = ExperimentSecurityBoundary(exp_path)
            orchestrator = SimpleOrchestrator(security)
            
            cost_summary = orchestrator.audit.get_session_costs()
            _display_cost_summary(cost_summary, detailed)
            
        except Exception as e:
            rich_console.print_error(f"❌ Failed to get session costs: {e}")
            return
    else:
        # Show costs from experiment runs
        runs_dir = exp_path / 'runs'
        if not runs_dir.exists():
            rich_console.print_info("No runs found - experiment has not been executed yet")
            return
        
        # Find most recent run with cost data
        run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
        run_dirs.sort(key=lambda x: x.name, reverse=True)
        
        if not run_dirs:
            rich_console.print_info("No completed runs found")
            return
        
        # Try to load cost data from most recent run
        for run_dir in run_dirs[:3]:  # Check last 3 runs
            # Check for LLM interactions log (where cost data is actually stored)
            llm_log = run_dir / 'logs' / 'llm_interactions.jsonl'
            if llm_log.exists():
                cost_summary = _load_cost_summary_from_llm_log(llm_log)
                rich_console.print_info(f"📊 Cost data from run: {run_dir.name}")
                _display_cost_summary(cost_summary, detailed)
                return
        
        rich_console.print_info("No cost data found in recent runs")

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--from', 'start_phase', 
              type=click.Choice(['validation', 'analysis', 'statistical', 'evidence', 'synthesis']),
              default='validation', help='Start from this phase (default: validation)')
@click.option('--to', 'end_phase',
              type=click.Choice(['validation', 'analysis', 'statistical', 'evidence', 'synthesis']), 
              default='synthesis', help='End at this phase (default: synthesis)')
@click.option('--run-dir', type=str, help='Specify specific run directory to resume from')
def resume(experiment_path: str, start_phase: str, end_phase: str, run_dir: str):
    """Resume an experiment from an existing run with completed phases."""
    exp_path = Path(experiment_path).resolve()
    
    # Validate phase parameters
    phases = ['validation', 'analysis', 'statistical', 'evidence', 'synthesis']
    if start_phase not in phases:
        rich_console.print_error(f"❌ Invalid start phase: {start_phase}")
        exit_invalid_usage(f"Start phase must be one of: {', '.join(phases)}")
    
    if end_phase not in phases:
        rich_console.print_error(f"❌ Invalid end phase: {end_phase}")
        exit_invalid_usage(f"End phase must be one of: {', '.join(phases)}")
    
    start_idx = phases.index(start_phase)
    end_idx = phases.index(end_phase)
    
    if start_idx > end_idx:
        rich_console.print_error(f"❌ Start phase ({start_phase}) cannot be after end phase ({end_phase})")
        exit_invalid_usage("Start phase must be before or equal to end phase")
    
    # Find resumable run
    if run_dir:
        source_run_dir = exp_path / "runs" / run_dir
        if not source_run_dir.exists():
            rich_console.print_error(f"❌ Specified run directory not found: {run_dir}")
            exit_file_error("Run directory not found.")
    else:
        source_run_dir = find_resumable_run(exp_path, start_phase)
        if not source_run_dir:
            rich_console.print_error(f"❌ No resumable run found for phase: {start_phase}")
            rich_console.print_info("💡 Tip: Use --run-dir to specify a specific run directory")
            exit_general_error("No resumable run found.")
    
    rich_console.print_info(f"🔄 Resuming from run: {source_run_dir.name}")
    
    # Delegate to run command with resume flag
    ctx = click.get_current_context()
    ctx.invoke(run, 
               experiment_path=experiment_path,
               verbose_trace=False,
               trace_filter=(),
               skip_validation=False,
               start_phase=start_phase,
               end_phase=end_phase,
               resume=True,
               run_dir=run_dir)

def _display_cost_summary(cost_summary: Dict[str, Any], detailed: bool):
    """Display cost summary in a formatted way"""
    if cost_summary["total_cost_usd"] == 0:
        rich_console.print_info("💰 No costs recorded")
        return
    
    # Basic summary
    rich_console.print_info(f"💰 Total cost: ${cost_summary['total_cost_usd']:.4f}")
    rich_console.print_info(f"🔢 Total tokens: {cost_summary['total_tokens']:,}")
    
    if detailed:
        # Detailed breakdown by operation
        if cost_summary["operations"]:
            rich_console.print_info("\n📊 Cost by Operation:")
            table = rich_console.create_table("Operation", ["Cost (USD)", "Tokens", "Calls"])
            for op, data in sorted(cost_summary["operations"].items(), key=lambda x: x[1]["cost_usd"], reverse=True):
                table.add_row(op, f"${data['cost_usd']:.4f}", f"{data['tokens']:,}", str(data['calls']))
            rich_console.print_table(table)
        
        # Detailed breakdown by model
        if cost_summary["models"]:
            rich_console.print_info("\n🤖 Cost by Model:")
            table = rich_console.create_table("Model", ["Cost (USD)", "Tokens", "Calls"])
            for model, data in sorted(cost_summary["models"].items(), key=lambda x: x[1]["cost_usd"], reverse=True):
                table.add_row(model, f"${data['cost_usd']:.4f}", f"{data['tokens']:,}", str(data['calls']))
            rich_console.print_table(table)
        
        # Detailed breakdown by agent
        if cost_summary["agents"]:
            rich_console.print_info("\n👤 Cost by Agent:")
            table = rich_console.create_table("Agent", ["Cost (USD)", "Tokens", "Calls"])
            for agent, data in sorted(cost_summary["agents"].items(), key=lambda x: x[1]["cost_usd"], reverse=True):
                table.add_row(agent, f"${data['cost_usd']:.4f}", f"{data['tokens']:,}", str(data['calls']))
            rich_console.print_table(table)

def _load_cost_summary_from_llm_log(llm_log_path: Path) -> Dict[str, Any]:
    """Load and aggregate cost data from an LLM interactions log file"""
    total_cost = 0.0
    total_tokens = 0
    operations = {}
    models = {}
    agents = {}
    
    try:
        with open(llm_log_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    
                    # Extract cost data from metadata
                    metadata = entry.get("metadata", {})
                    cost = metadata.get("response_cost_usd", 0.0)
                    tokens = metadata.get("total_tokens", 0)
                    
                    # Only process entries with cost data
                    if cost > 0 or tokens > 0:
                        operation = metadata.get("step", entry.get("interaction_type", "unknown"))
                        model = entry.get("model", "unknown")
                        agent = entry.get("agent_name", "unknown")
                        
                        # Aggregate totals
                        total_cost += cost
                        total_tokens += tokens
                        
                        # Aggregate by operation
                        if operation not in operations:
                            operations[operation] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        operations[operation]["cost_usd"] += cost
                        operations[operation]["tokens"] += tokens
                        operations[operation]["calls"] += 1
                        
                        # Aggregate by model
                        if model not in models:
                            models[model] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        models[model]["cost_usd"] += cost
                        models[model]["tokens"] += tokens
                        models[model]["calls"] += 1
                        
                        # Aggregate by agent
                        if agent not in agents:
                            agents[agent] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        agents[agent]["cost_usd"] += cost
                        agents[agent]["tokens"] += tokens
                        agents[agent]["calls"] += 1
                    
    except Exception as e:
        rich_console.print_warning(f"⚠️  Error reading LLM interactions log: {e}")
    
    return {
        "total_cost_usd": total_cost,
        "total_tokens": total_tokens,
        "operations": operations,
        "models": models,
        "agents": agents
    }

@cli.command()
def status():
    """Show infrastructure and system status"""
    rich_console.print_section("🔍 Discernus System Status")
    
    # Check system components
    status_table = rich_console.create_table("System Components", ["Component", "Status", "Details"])
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    status_table.add_row("Python", "✅ Available", python_version)
    
    # Check Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            git_version = result.stdout.strip()
            status_table.add_row("Git", "✅ Available", git_version)
        else:
            status_table.add_row("Git", "❌ Not Available", "Required for provenance")
    except FileNotFoundError:
        status_table.add_row("Git", "❌ Not Found", "Required for provenance")
    
    # Check model availability
    try:
        registry = ModelRegistry()
        available_models = registry.list_models()
        status_table.add_row("LLM Models", "✅ Available", f"{len(available_models)} models")
    except Exception as e:
        status_table.add_row("LLM Models", "❌ Error", str(e))
    
    # Check projects directory - find repository root first
    def find_repository_root() -> Optional[Path]:
        """Find repository root by looking for .git or pyproject.toml"""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
                return parent
        return None
    
    repo_root = find_repository_root()
    if repo_root:
        projects_dir = repo_root / 'projects'
        if projects_dir.exists():
            experiment_count = len([d for d in projects_dir.iterdir() if d.is_dir() and (d / 'experiment.md').exists()])
            status_table.add_row("Projects", "✅ Available", f"{experiment_count} experiments")
        else:
            status_table.add_row("Projects", "⚠️ Missing", "Create 'projects' directory")
    else:
        status_table.add_row("Projects", "❌ Error", "Could not find repository root")
    
    rich_console.print_table(status_table)
    
    # Configuration info
    config = get_config()
    rich_console.print_info(f"🔧 Default Analysis Model: {config.analysis_model}")
    rich_console.print_info(f"🔧 Default Synthesis Model: {config.synthesis_model}")

# ============================================================================
# MANAGEMENT COMMANDS
# ============================================================================

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--output', '-o', default='export.csv', help='Output CSV file path')
def export_csv(experiment_path, output):
    """Export experiment data to CSV format
    
    Extracts raw scores, derived metrics, and evidence quotes from composite_analysis artifacts.
    """
    rich_console.print_section("📊 Exporting Experiment Data to CSV")
    
    try:
        # Run the export script
        script_path = Path(__file__).parent.parent / "scripts" / "export_csv.py"
        result = subprocess.run([
            sys.executable, str(script_path), experiment_path, "--output", output
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            rich_console.print_success(f"✅ Data exported to {output}")
            if result.stdout:
                print(result.stdout)
        else:
            rich_console.print_error(f"❌ Export failed: {result.stderr}")
            
    except Exception as e:
        rich_console.print_error(f"❌ Error running export: {e}")

# ============================================================================





def main():
    """Main entry point for the discernus CLI."""
    cli()

if __name__ == '__main__':
    main()
