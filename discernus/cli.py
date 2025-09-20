#!/usr/bin/env python3
"""
Discernus CLI v2.1 - Streamlined Researcher Interface
===================================================

Core Commands for Research Workflow:
- discernus run <experiment_path>       - Execute complete experiment (analysis + synthesis)
- discernus validate <experiment_path>  - Validate experiment structure  
- discernus debug <experiment_path>     - Interactive debugging with detailed tracing
- discernus list                        - List available experiments
- discernus status                      - Show system status
- discernus artifacts                   - Show experiment artifacts and cache status

For Alpha Release:
- discernus run <experiment>            - Run complete experiment (recommended)
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
from discernus.core.execution_strategies import FullExperimentStrategy
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.analysis_agent.v2_analysis_agent import V2AnalysisAgent
from discernus.agents.statistical_agent.v2_statistical_agent import V2StatisticalAgent
from discernus.agents.evidence_retriever_agent.v2_evidence_retriever_agent import V2EvidenceRetrieverAgent
from discernus.agents.unified_synthesis_agent.v2_unified_synthesis_agent import V2UnifiedSynthesisAgent
from discernus.agents.validation_agent.v2_validation_agent import V2ValidationAgent


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
@click.version_option(version='0.2.0', prog_name='Discernus')
@click.option('--verbose', '-v', is_flag=True, envvar='DISCERNUS_VERBOSE', help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, envvar='DISCERNUS_QUIET', help='Enable quiet output (minimal)')
@click.option('--no-color', is_flag=True, envvar='DISCERNUS_NO_COLOR', help='Disable colored output')
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.pass_context
def cli(ctx, verbose, quiet, no_color, config):
    """Discernus - Computational Social Science Research Platform (THIN v2.0)
    
    \b
    Quick Start:
      python3 -m discernus.cli validate projects/my_experiment/  # Validate experiment first
      python3 -m discernus.cli run projects/my_experiment/       # Run complete experiment
      python3 -m discernus.cli debug projects/my_experiment/     # Debug with detailed tracing
    
    \b
    Common Examples:
      python3 -m discernus.cli run                          # Run experiment in current directory
      python3 -m discernus.cli run --dry-run                # Preview what would be executed
      python3 -m discernus.cli validate --dry-run           # Preview validation checks
      python3 -m discernus.cli debug --verbose              # Debug with detailed tracing
      python3 -m discernus.cli status                       # Check system status
    
    \b
    Model Selection Tips:
      --analysis-model vertex_ai/gemini-2.5-flash          # Fast analysis (default)
      --synthesis-model vertex_ai/gemini-2.5-pro           # High-quality synthesis (default)
      --validation-model vertex_ai/gemini-2.5-pro          # High-quality validation (default)
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store global options in context
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['no_color'] = no_color
    ctx.obj['config'] = get_config()
    
    # Set verbosity level
    if verbose and quiet:
        rich_console.print_warning("Both --verbose and --quiet specified, using verbose")
    
    ctx.obj['verbosity'] = 'verbose' if verbose else ('quiet' if quiet else 'normal')

# ============================================================================
# CORE COMMANDS
# ============================================================================

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True, path_type=str))
@click.option('--verbose-trace', is_flag=True, help='Enable comprehensive function-level tracing for debugging')
@click.option('--trace-filter', multiple=True, help='Filter tracing to specific components (e.g., statistical, analysis)')
@click.pass_context
def run(ctx, experiment_path: str, verbose_trace: bool, trace_filter: tuple):
    """Execute a V2 experiment."""
    exp_path = Path(experiment_path).resolve()

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

        # 2. Find framework and corpus files
        framework_file = None
        if (exp_path / "framework.md").exists():
            framework_file = exp_path / "framework.md"
        else:
            # Look for any other .md file that is not corpus.md or experiment.md
            for md_file in exp_path.glob('*.md'):
                if md_file.name not in ['corpus.md', 'experiment.md']:
                    framework_file = md_file
                    break
        
        if not framework_file:
            rich_console.print_error(f"❌ Framework file (.md) not found in: {exp_path}")
            exit_file_error("Framework file not found.")

        corpus_file = exp_path / "corpus.md"
        if not corpus_file.exists():
            rich_console.print_error(f"❌ corpus.md not found in: {exp_path}")
            exit_file_error("corpus.md not found.")

        # 3. Configure Orchestrator
        config = V2OrchestratorConfig(
            experiment_id=exp_path.name,
            framework_path=str(framework_file),
            corpus_path=str(corpus_file),
            output_dir=str(run_folder)
        )

        orchestrator = V2Orchestrator(config, security, storage, audit)

        # 4. Register Agents
        orchestrator.register_agent("Validation", V2ValidationAgent(security, storage, audit))
        orchestrator.register_agent("Analysis", V2AnalysisAgent(security, storage, audit))
        orchestrator.register_agent("Statistical", V2StatisticalAgent(security, storage, audit))
        orchestrator.register_agent("Evidence", V2EvidenceRetrieverAgent(security, storage, audit))
        orchestrator.register_agent("Synthesis", V2UnifiedSynthesisAgent(security, storage, audit))

        # 5. Execute Strategy with Progress Reporting
        strategy = FullExperimentStrategy()
        result = orchestrator.execute_strategy(strategy)

        # Show experiment summary
        if result.success:
            rich_console.print_success("✅ V2 Experiment Completed Successfully!")

            # Show phase progress
            phases_completed = result.phases_completed
            if phases_completed:
                rich_console.print_info(f"📊 Phases completed: {', '.join(phases_completed)}")
            else:
                rich_console.print_info("📊 No phases completed")

            rich_console.print_info(f"📁 Artifacts saved in: {storage.run_folder}")
            rich_console.print_info(f"⏱️  Total execution time: {result.execution_time_seconds:.1f} seconds")

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
@click.option('--agent', type=click.Choice(['analysis', 'synthesis', 'statistical', 'fact-checker', 'validation']), 
              help='Focus debugging on specific agent: analysis (document processing), synthesis (report generation), statistical (statistical analysis), fact-checker (fact validation), validation (experiment coherence)')
@click.option('--verbose', is_flag=True, help='Enable detailed debug output')
@click.option('--test-mode', is_flag=True, help='Run in test mode with limited data')
@click.pass_context
def debug(ctx, experiment_path: str, agent: Optional[str], verbose: bool, test_mode: bool):
    """Interactive debugging mode with detailed tracing.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    """
    exp_path = Path(experiment_path).resolve()
    
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    click.echo(f"🐛 Debug mode for experiment: {exp_path}")
    
    if agent:
        click.echo(f"🎯 Focusing on agent: {agent}")
    
    if test_mode:
        click.echo("🧪 Running in test mode with limited data")
    
    # V2 orchestrator doesn't support debug mode yet
    # TODO: Implement debug functionality in V2 orchestrator
    rich_console.print_error("❌ Debug command not yet implemented in V2 orchestrator")
    rich_console.print_info("   The V2 orchestrator is still under development.")
    rich_console.print_info("   For now, please use the full 'discernus run' command.")
    exit_invalid_usage("Debug command not implemented in V2 orchestrator")

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, 
              help='Preview what validation would check without actually running it (useful for understanding validation requirements)')
@click.pass_context
def validate(ctx, experiment_path: str, dry_run: bool):
    """Validate experiment structure and configuration.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    """
    exp_path = Path(experiment_path).resolve()
    
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    click.echo(f"🔍 Validating experiment: {exp_path}")
    
    if dry_run:
        click.echo("🧪 DRY RUN - Validation checks that would be performed:")
        click.echo("   • Experiment manifest structure")
        click.echo("   • Corpus manifest and document availability")
        click.echo("   • Framework specification compliance")
        click.echo("   • Model availability and configuration")
        click.echo("   • Output directory permissions")
        return
    
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
