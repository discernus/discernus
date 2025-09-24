#!/usr/bin/env python3
"""
Discernus CLI v2.1 - Streamlined Researcher Interface
===================================================

Core Commands for Research Workflow:
- discernus run <experiment_path>       - Execute complete experiment (analysis + synthesis)
- discernus run --analysis-only         - Run analysis phase only, skip statistical and synthesis
- discernus run --statistical-prep      - Run analysis and statistical phases, skip synthesis
- discernus run --resume-from-stats     - Resume from statistical phase, skip analysis
- discernus run --resume-from-analysis  - Resume from analysis phase, skip validation and analysis
- discernus validate <experiment_path>  - Validate experiment structure  
- discernus debug <experiment_path>     - Interactive debugging with detailed tracing
- discernus list                        - List available experiments
- discernus status                      - Show system status
- discernus artifacts                   - Show experiment artifacts and cache status

For Alpha Release:
- discernus run <experiment>            - Run complete experiment (recommended)
- discernus run <experiment> --analysis-only    - Run analysis phase only
- discernus run <experiment> --statistical-prep - Run analysis + statistical phases
- discernus run <experiment> --resume-from-stats - Resume from statistical phase
- discernus validate <experiment>       - Validate experiment before running
- discernus debug <experiment>          - Debug with detailed tracing
- discernus status                      - Check system status
- discernus artifacts <experiment>      - Show experiment artifacts

Advanced features (database resume/caching/provenance) coming soon.
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
from discernus.core.exit_codes import (
    ExitCode, exit_success, exit_general_error, exit_invalid_usage, 
    exit_validation_failed, exit_infrastructure_error, exit_file_error, exit_config_error
)

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

# Import provenance and documentation components
from discernus.core.provenance_consolidator import consolidate_run_provenance
from discernus.core.input_materials_consolidator import consolidate_input_materials
from discernus.core.golden_run_documentation_generator import generate_golden_run_documentation

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
@click.pass_context
def run(ctx, experiment_path: str, verbose_trace: bool, trace_filter: tuple, skip_validation: bool, 
        start_phase: str, end_phase: str):
    """Execute a V2 experiment with simple phase selection.
    
    Execution modes:
    - Default: Run complete pipeline (validation + analysis + statistical + evidence + synthesis)
    - --from analysis: Start from analysis phase, skip validation
    - --to statistical: End at statistical phase, skip evidence and synthesis
    - --from analysis --to synthesis: Run analysis through synthesis
    
    Examples:
    - discernus run projects/my_experiment
    - discernus run projects/my_experiment --from analysis
    - discernus run projects/my_experiment --to statistical
    - discernus run projects/my_experiment --from analysis --to synthesis
    """
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
        # 1. Initialize core components
        run_name = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_folder = exp_path / "runs" / run_name
        run_folder.mkdir(parents=True, exist_ok=True)

        security = ExperimentSecurityBoundary(exp_path)
        storage = LocalArtifactStorage(security, run_folder, run_name)
        audit = AuditLogger(security, run_folder)

        # 2. Verify experiment.md exists (basic check only - ValidationAgent will do full validation)
        experiment_file = exp_path / "experiment.md"
        if not experiment_file.exists():
            rich_console.print_error(f"❌ experiment.md not found in: {exp_path}")
            exit_file_error("experiment.md not found.")

        # 3. Configure Orchestrator (THIN architecture - let ValidationAgent handle file discovery)
        config = V2OrchestratorConfig(
            experiment_id=exp_path.name,
            experiment_dir=str(exp_path),
            output_dir=str(run_folder),
            skip_validation=skip_validation
        )

        orchestrator = V2Orchestrator(config, security, storage, audit)

        # 4. Register Agents
        orchestrator.register_agent("Validation", V2ValidationAgent(security, storage, audit))
        orchestrator.register_agent("Analysis", V2AnalysisAgent(security, storage, audit))
        orchestrator.register_agent("Statistical", V2StatisticalAgent(security, storage, audit))
        orchestrator.register_agent("Evidence", IntelligentEvidenceRetrievalAgent(security, storage, audit))
        orchestrator.register_agent("Synthesis", TwoStageSynthesisAgent(security, storage, audit))

        # 5. Use Simple Executor
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
            cost_summary = orchestrator.audit.get_session_costs()
            if cost_summary["total_cost_usd"] > 0:
                rich_console.print_info(f"💰 Total cost: ${cost_summary['total_cost_usd']:.4f}")
                rich_console.print_info(f"🔢 Total tokens: {cost_summary['total_tokens']:,}")
                
                # Show top cost operations
                if cost_summary["operations"]:
                    top_operations = sorted(cost_summary["operations"].items(), 
                                          key=lambda x: x[1]["cost_usd"], reverse=True)[:3]
                    if top_operations:
                        rich_console.print_info("📊 Top operations:")
                        for op, data in top_operations:
                            rich_console.print_info(f"  • {op}: ${data['cost_usd']:.4f} ({data['calls']} calls)")

            # Show artifact counts by type (if storage available)
            if hasattr(result, 'artifacts') and result.artifacts:
                try:
                    artifact_types = {}
                    for artifact_hash in result.artifacts:
                        if isinstance(artifact_hash, str):
                            try:
                                artifact_metadata = storage.get_artifact_metadata(artifact_hash)
                                # Artifact type is stored in metadata.artifact_type, not directly
                                artifact_type = artifact_metadata.get("metadata", {}).get("artifact_type", "unknown")
                                artifact_types[artifact_type] = artifact_types.get(artifact_type, 0) + 1
                            except Exception:
                                # Fallback for artifacts without metadata
                                artifact_types["unknown"] = artifact_types.get("unknown", 0) + 1
                        else:
                            # Fallback for non-string artifacts
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
        from discernus.agents.deprecated.experiment_coherence_agent import ExperimentCoherenceAgent
        
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
            cost_log = run_dir / 'logs' / 'cost_tracking.jsonl'
            if cost_log.exists():
                cost_summary = _load_cost_summary_from_log(cost_log)
                rich_console.print_info(f"📊 Cost data from run: {run_dir.name}")
                _display_cost_summary(cost_summary, detailed)
                return
        
        rich_console.print_info("No cost data found in recent runs")

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

def _load_cost_summary_from_log(cost_log_path: Path) -> Dict[str, Any]:
    """Load and aggregate cost data from a cost log file"""
    total_cost = 0.0
    total_tokens = 0
    operations = {}
    models = {}
    agents = {}
    
    try:
        with open(cost_log_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    
                    cost = entry.get("cost_usd", 0.0)
                    tokens = entry.get("tokens_used", 0)
                    operation = entry.get("operation", "unknown")
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
        rich_console.print_warning(f"⚠️  Error reading cost log: {e}")
    
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
    
    # Check projects directory
    projects_dir = Path('projects')
    if projects_dir.exists():
        experiment_count = len([d for d in projects_dir.iterdir() if d.is_dir() and (d / 'experiment.md').exists()])
        status_table.add_row("Projects", "✅ Available", f"{experiment_count} experiments")
    else:
        status_table.add_row("Projects", "⚠️ Missing", "Create 'projects' directory")
    
    rich_console.print_table(status_table)
    
    # Configuration info
    config = get_config()
    rich_console.print_info(f"🔧 Default Analysis Model: {config.analysis_model}")
    rich_console.print_info(f"🔧 Default Synthesis Model: {config.synthesis_model}")

# ============================================================================
# MANAGEMENT COMMANDS
# ============================================================================



# ============================================================================





def main():
    """Main entry point for the discernus CLI."""
    cli()

if __name__ == '__main__':
    main()
