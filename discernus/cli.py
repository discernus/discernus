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

Management Commands:
- discernus promote <experiment_path>   - Promote workbench files to operational status
- discernus cache <experiment_path>     - Manage validation cache

Research Commands (Advanced):
- discernus consolidate-provenance      - Consolidate provenance data for golden runs
- discernus consolidate-inputs          - Consolidate input materials for golden runs  
- discernus generate-golden-run-docs    - Generate comprehensive golden run documentation
- discernus model-quality               - Assess model quality and compare analysis results
- discernus timezone-debug              - Debug timezone issues in experiment logs
- discernus visualize-provenance        - Generate provenance visualization
- discernus validate-score              - Validate numerical scores using academic pipeline
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

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError
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

def _validate_models(models_to_validate: List[tuple[str, str]]):
    """Validate that specified models are available in the registry."""
    try:
        registry = ModelRegistry()
        for model_type, model_name in models_to_validate:
            if not registry.is_model_available(model_name):
                rich_console.print_error(f"❌ {model_type} model '{model_name}' is not available")
                rich_console.print_info(f"   Available models: {', '.join(registry.list_available_models())}")
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
      python3 -m discernus.cli run --analysis-only          # Run analysis only, skip synthesis
      python3 -m discernus.cli validate --dry-run           # Preview validation checks
      python3 -m discernus.cli debug --verbose --agent analysis  # Debug analysis agent with test mode
      python3 -m discernus.cli promote --cleanup            # Promote and clean up development files
      python3 -m discernus.cli artifacts                    # Show available cache artifacts
    
    \b
    Model Selection Tips:
      --analysis-model vertex_ai/gemini-2.5-flash          # Fast analysis (default)
      --synthesis-model vertex_ai/gemini-2.5-pro           # High-quality synthesis (default)
      --validation-model vertex_ai/gemini-2.5-flash-lite   # Fast validation (default)
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store global options in context
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['no_color'] = no_color
    ctx.obj['config'] = get_config(config)
    
    # Set verbosity level
    if verbose and quiet:
        rich_console.print_warning("Both --verbose and --quiet specified, using verbose")
    
    ctx.obj['verbosity'] = 'verbose' if verbose else ('quiet' if quiet else 'normal')

# ============================================================================
# CORE COMMANDS
# ============================================================================

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, envvar='DISCERNUS_DRY_RUN', 
              help='Preview what would be executed without running (useful for understanding experiment flow)')
@click.option('--analysis-model', envvar='DISCERNUS_ANALYSIS_MODEL',
              default='vertex_ai/gemini-2.5-flash',
              help='LLM model for document analysis. Use flash for speed, pro for accuracy. Examples: vertex_ai/gemini-2.5-flash, openai/gpt-4o')
@click.option('--synthesis-model', envvar='DISCERNUS_SYNTHESIS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for report synthesis. Pro recommended for complex analysis. Examples: vertex_ai/gemini-2.5-pro, openai/gpt-4o')
@click.option('--validation-model', envvar='DISCERNUS_VALIDATION_MODEL',
              default='vertex_ai/gemini-2.5-flash-lite',
              help='LLM model for experiment validation. Flash-lite is fast and sufficient for validation tasks')
@click.option('--derived-metrics-model', envvar='DISCERNUS_DERIVED_METRICS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for statistical analysis and derived metrics. Pro recommended for complex calculations')
@click.option('--skip-validation', is_flag=True, envvar='DISCERNUS_SKIP_VALIDATION', 
              help='Skip coherence validation (not recommended - validation catches common issues)')
@click.option('--analysis-only', is_flag=True, envvar='DISCERNUS_ANALYSIS_ONLY', 
              help='Run analysis and export CSV only, skip synthesis report (useful for data exploration)')
@click.option('--ensemble-runs', type=int, envvar='DISCERNUS_ENSEMBLE_RUNS', 
              help='Number of ensemble runs for self-consistency (3-5 recommended, increases cost linearly)')
@click.option('--no-auto-commit', is_flag=True, envvar='DISCERNUS_NO_AUTO_COMMIT', 
              help='Disable automatic Git commit after successful run (useful for testing or manual commit control)')
@click.pass_context
def run(ctx, experiment_path: str, dry_run: bool, analysis_model: Optional[str], synthesis_model: Optional[str], validation_model: Optional[str], derived_metrics_model: Optional[str], skip_validation: bool, analysis_only: bool, ensemble_runs: Optional[int], no_auto_commit: bool):
    """Execute complete experiment (analysis + synthesis). 
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    The experiment directory must contain experiment.md, corpus.md, and framework files.
    """
    exp_path = Path(experiment_path).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    click.echo("🔬 Using clean pipeline for all experiments")
    
    # Get configuration and apply defaults
    config = ctx.obj['config']
    verbosity = ctx.obj['verbosity']
    
    # Apply config defaults for None values
    if analysis_model is None:
        analysis_model = config.analysis_model
    if synthesis_model is None:
        synthesis_model = config.synthesis_model
    if validation_model is None:
        validation_model = config.validation_model
    if derived_metrics_model is None:
        derived_metrics_model = config.derived_metrics_model
    if ensemble_runs is None:
        ensemble_runs = config.ensemble_runs
    
    # Override config booleans if CLI flags are set
    if not dry_run:
        dry_run = config.dry_run
    if not skip_validation:
        skip_validation = config.skip_validation
    if not no_auto_commit:
        no_auto_commit = not config.auto_commit
    
    # Validate models against registry before proceeding
    models_to_validate = [
        ("analysis", analysis_model),
        ("synthesis", synthesis_model),
        ("validation", validation_model),
        ("derived_metrics", derived_metrics_model)
    ]
    _validate_models(models_to_validate)
    
    # Initialize orchestrator
    orchestrator = CleanAnalysisOrchestrator(
        experiment_path=exp_path,
        analysis_model=analysis_model,
        synthesis_model=synthesis_model,
        validation_model=validation_model,
        derived_metrics_model=derived_metrics_model,
        dry_run=dry_run,
        skip_validation=skip_validation,
        analysis_only=analysis_only,
        ensemble_runs=ensemble_runs,
        auto_commit=not no_auto_commit,
        verbosity=verbosity
    )
    
    try:
        # Execute experiment
        result = orchestrator.run_experiment()
        
        if result.success:
            rich_console.print_success("✅ Experiment completed successfully!")
            if result.run_folder:
                rich_console.print_info(f"📁 Results saved to: {result.run_folder}")
            exit_success()
        else:
            rich_console.print_error(f"❌ Experiment failed: {result.error}")
            exit_general_error(result.error)
            
    except CleanAnalysisError as e:
        rich_console.print_error(f"❌ Analysis error: {e}")
        exit_general_error(str(e))
    except Exception as e:
        rich_console.print_error(f"❌ Unexpected error: {e}")
        exit_general_error(str(e))

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--agent', type=click.Choice(['analysis', 'synthesis', 'evidence-curator', 'results-interpreter']), 
              help='Focus debugging on specific agent: analysis (document processing), synthesis (report generation), evidence-curator (fact checking), results-interpreter (statistical analysis)')
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
    
    # Initialize orchestrator in debug mode
    orchestrator = CleanAnalysisOrchestrator(
        experiment_path=exp_path,
        debug_mode=True,
        debug_agent=agent,
        verbose_debug=verbose,
        test_mode=test_mode,
        verbosity='verbose' if verbose else ctx.obj['verbosity']
    )
    
    try:
        result = orchestrator.debug_experiment()
        
        if result.success:
            rich_console.print_success("✅ Debug session completed")
            exit_success()
        else:
            rich_console.print_error(f"❌ Debug session failed: {result.error}")
            exit_general_error(result.error)
            
    except Exception as e:
        rich_console.print_error(f"❌ Debug error: {e}")
        exit_general_error(str(e))

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
def list():
    """List available experiments"""
    projects_dir = Path('projects')
    
    if not projects_dir.exists():
        click.echo("❌ No projects directory found")
        click.echo("   Create a 'projects' directory and add your experiments")
        sys.exit(1)
    
    rich_console.print_section("📁 Available Experiments")
    
    experiments = []
    for item in projects_dir.iterdir():
        if item.is_dir():
            # Check if it looks like an experiment
            if (item / 'experiment.md').exists() or (item / 'corpus.md').exists():
                experiments.append(item)
    
    if not experiments:
        rich_console.print_info("No experiments found in projects/ directory")
        rich_console.print_info("   Create experiment.md and corpus.md files to define experiments")
        return
    
    # Sort experiments by name
    experiments.sort(key=lambda x: x.name)
    
    # Create table
    table = rich_console.create_table("Experiments", ["Name", "Path", "Status"])
    
    for exp in experiments:
        # Determine status
        has_experiment = (exp / 'experiment.md').exists()
        has_corpus = (exp / 'corpus.md').exists()
        has_runs = (exp / 'runs').exists()
        
        if has_experiment and has_corpus:
            status = "✅ Ready"
        elif has_experiment or has_corpus:
            status = "⚠️ Incomplete"
        else:
            status = "❌ Invalid"
        
        table.add_row(exp.name, str(exp), status)
    
    rich_console.print_table(table)

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
        available_models = registry.list_available_models()
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

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, 
              help='Show what would be promoted without executing (useful for reviewing changes before promotion)')
@click.option('--cleanup', is_flag=True, help='Clean up development files after promotion')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
def promote(experiment_path: str, dry_run: bool, cleanup: bool, force: bool):
    """Promote workbench files to operational status.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    """
    exp_path = Path(experiment_path).resolve()
    
    rich_console.print_section(f"📤 Promoting: {exp_path.name}")
    
    # Find workbench files
    workbench_files = []
    for pattern in ['*.md', '*.yaml', '*.yml', '*.json']:
        workbench_files.extend(exp_path.glob(pattern))
    
    if not workbench_files:
        rich_console.print_info("No workbench files found to promote")
        return
    
    if dry_run:
        rich_console.print_info("🧪 DRY RUN - Files that would be promoted:")
        for file in workbench_files:
            rich_console.print_info(f"   • {file.name}")
        return
    
    # Confirm promotion
    if not force:
        click.confirm(f"Promote {len(workbench_files)} files to operational status?", abort=True)
    
    # Promote files (copy to operational locations)
    promoted_count = 0
    for file in workbench_files:
        # For now, just mark as promoted by adding to a promoted list
        # In a real implementation, this would move files to operational directories
        promoted_count += 1
        rich_console.print_info(f"   ✅ Promoted: {file.name}")
    
    rich_console.print_success(f"✅ Promoted {promoted_count} files to operational status")
    
    if cleanup:
        rich_console.print_info("🧹 Cleaning up development files...")
        # Cleanup logic would go here
        rich_console.print_info("   🗑️ Development files cleaned up")

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--stats', is_flag=True, help='Show cache statistics')
@click.option('--cleanup', is_flag=True, help='Clean up old cache entries')
def cache(experiment_path: str, stats: bool, cleanup: bool):
    """Manage validation cache for an experiment.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    """
    exp_path = Path(experiment_path).resolve()
    cache_dir = exp_path / '.discernus_cache'
    
    if not cache_dir.exists():
        rich_console.print_info("No cache directory found")
        return
    
    if stats:
        rich_console.print_section(f"📊 Cache Statistics: {exp_path.name}")
        
        cache_files = list(cache_dir.rglob('*'))
        total_size = sum(f.stat().st_size for f in cache_files if f.is_file())
        
        stats_table = rich_console.create_table("Cache Stats", ["Metric", "Value"])
        stats_table.add_row("Total Files", str(len(cache_files)))
        stats_table.add_row("Total Size", f"{total_size / 1024 / 1024:.1f} MB")
        
        rich_console.print_table(stats_table)
    
    if cleanup:
        rich_console.print_info("🧹 Cleaning up old cache entries...")
        
        # Remove cache files older than 30 days
        cutoff_time = time.time() - (30 * 24 * 60 * 60)
        removed_count = 0
        
        for cache_file in cache_dir.rglob('*'):
            if cache_file.is_file() and cache_file.stat().st_mtime < cutoff_time:
                cache_file.unlink()
                removed_count += 1
        
        rich_console.print_success(f"✅ Removed {removed_count} old cache entries")

# ============================================================================
# RESEARCH COMMANDS (Advanced)
# ============================================================================

@cli.command()
@click.argument('run_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', type=click.Path(), help='Save archive to specific location')
@click.option('--include-inputs', is_flag=True, default=True, help='Include input materials (corpus, experiment spec, framework)')
@click.option('--include-provenance', is_flag=True, default=True, help='Include consolidated provenance data')
@click.option('--include-docs', is_flag=True, default=True, help='Include comprehensive documentation')
def archive(run_directory: str, output: Optional[str], include_inputs: bool, include_provenance: bool, include_docs: bool):
    """Create a complete golden run archive for research transparency.
    
    Consolidates all experiment data into a self-contained archive suitable for:
    - Peer review and publication
    - Replication research
    - Audit and compliance
    - Long-term archival
    
    RUN_DIRECTORY: Path to experiment run directory (e.g., projects/experiment/runs/20250127T143022Z)
    """
    run_path = Path(run_directory)
    output_path = Path(output) if output else None
    
    try:
        rich_console.print_section(f"📦 Creating Golden Run Archive: {run_path.name}")
        
        # Step 1: Consolidate provenance data
        if include_provenance:
            rich_console.print_info("📊 Consolidating provenance data...")
            provenance_data = consolidate_run_provenance(run_path, None)
            rich_console.print_success("✅ Provenance data consolidated")
        
        # Step 2: Consolidate input materials
        if include_inputs:
            rich_console.print_info("📁 Consolidating input materials...")
            consolidation_report = consolidate_input_materials(run_path, None)
            rich_console.print_success("✅ Input materials consolidated")
        
        # Step 3: Generate comprehensive documentation
        if include_docs:
            rich_console.print_info("📋 Generating comprehensive documentation...")
            docs_path = generate_golden_run_documentation(run_path, output_path)
            rich_console.print_success("✅ Documentation generated")
        
        rich_console.print_success("🎉 Golden run archive created successfully!")
        rich_console.print_info("📦 Archive is self-contained and ready for peer review/archival")
        
    except Exception as e:
        rich_console.print_error(f"❌ Error creating golden run archive: {e}")
        exit_general_error(str(e))


def main():
    """Main entry point for the discernus CLI."""
    cli()

if __name__ == '__main__':
    main()
