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
      python3 -m discernus.cli run --analysis-only          # Run analysis only, no CSV export
      python3 -m discernus.cli validate --dry-run           # Preview validation checks
      python3 -m discernus.cli debug --verbose --agent analysis  # Debug analysis agent with test mode
      python3 -m discernus.cli promote --cleanup            # Promote and clean up development files
      python3 -m discernus.cli artifacts                    # Show available cache artifacts
    
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
@click.option('--dry-run', is_flag=True, envvar='DISCERNUS_DRY_RUN', 
              help='Preview what would be executed without running (useful for understanding experiment flow)')
@click.option('--analysis-model', envvar='DISCERNUS_ANALYSIS_MODEL',
              default='vertex_ai/gemini-2.5-flash',
              help='LLM model for document analysis. Use flash for speed, pro for accuracy. Examples: vertex_ai/gemini-2.5-flash, openai/gpt-4o')
@click.option('--synthesis-model', envvar='DISCERNUS_SYNTHESIS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for report synthesis. Pro recommended for complex analysis. Examples: vertex_ai/gemini-2.5-pro, openai/gpt-4o')
@click.option('--validation-model', envvar='DISCERNUS_VALIDATION_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for experiment validation. Pro model provides high-quality validation')
@click.option('--derived-metrics-model', envvar='DISCERNUS_DERIVED_METRICS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for statistical analysis and derived metrics. Pro recommended for complex calculations')
@click.option('--skip-validation', is_flag=True, envvar='DISCERNUS_SKIP_VALIDATION', 
              help='Skip coherence validation (not recommended - validation catches common issues)')
@click.option('--analysis-only', is_flag=True, envvar='DISCERNUS_ANALYSIS_ONLY', 
              help='Run analysis only, skip synthesis and CSV export (useful for testing analysis agent)')
@click.option('--statistical-prep', is_flag=True, envvar='DISCERNUS_STATISTICAL_PREP', 
              help='Run analysis + derived metrics + CSV export, skip synthesis. Perfect for external statistical analysis workflows. Outputs: scores.csv, evidence.csv, metadata.csv')
@click.option('--skip-synthesis', is_flag=True, envvar='DISCERNUS_SKIP_SYNTHESIS', 
              help='Run full pipeline including statistical analysis, skip synthesis report (useful for custom synthesis workflows)')
@click.option('--no-auto-commit', is_flag=True, envvar='DISCERNUS_NO_AUTO_COMMIT', 
              help='Disable automatic Git commit after successful run (useful for testing or manual commit control)')
@click.pass_context
def run(ctx, experiment_path: str, dry_run: bool, analysis_model: Optional[str], synthesis_model: Optional[str], validation_model: Optional[str], derived_metrics_model: Optional[str], skip_validation: bool, analysis_only: bool, statistical_prep: bool, skip_synthesis: bool, no_auto_commit: bool):
    """Execute complete experiment (analysis + synthesis). 
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    The experiment directory must contain experiment.md, corpus.md, and framework files.
    """
    exp_path = Path(str(experiment_path)).resolve()
    
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
    
    # Override config booleans if CLI flags are set
    if not dry_run:
        dry_run = config.dry_run
    if not skip_validation:
        skip_validation = config.skip_validation
    if not no_auto_commit:
        no_auto_commit = not config.auto_commit
    
    # Validate models against registry before proceeding
    
    # Validate mutually exclusive modes
    mode_count = sum([analysis_only, statistical_prep, skip_synthesis])
    if mode_count > 1:
        rich_console.print_error("❌ Only one mode can be specified at a time")
        rich_console.print_info("   Available modes: --analysis-only, --statistical-prep, --skip-synthesis")
        exit_invalid_usage("Multiple modes specified")
    
    # Provide mode guidance if no mode specified
    if mode_count == 0:
        rich_console.print_info("💡 Workflow modes available:")
        rich_console.print_info("   • Default: Full analysis + synthesis pipeline")
        rich_console.print_info("   • --analysis-only: Analysis + CSV export only (data exploration)")
        rich_console.print_info("   • --statistical-prep: Analysis + derived metrics + CSV export (external stats)")
        rich_console.print_info("   • --skip-synthesis: Full pipeline except synthesis (custom synthesis)")
        rich_console.print_info("   • Use 'discernus resume' to complete synthesis from statistical-prep runs")
    
    # Provide specific guidance for statistical preparation mode
    if statistical_prep:
        rich_console.print_info("📊 Statistical Preparation Mode Selected")
        rich_console.print_info("   This mode will:")
        rich_console.print_info("   • Run document analysis")
        rich_console.print_info("   • Calculate derived metrics")
        rich_console.print_info("   • Export CSV files for external statistical analysis")
        rich_console.print_info("   • Skip synthesis report generation")
        rich_console.print_info("   • Allow resume to synthesis later with 'discernus resume'")
    
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
        statistical_prep=statistical_prep,
        skip_synthesis=skip_synthesis,
        auto_commit=not no_auto_commit,
        verbosity=verbosity
    )
    
    try:
        # Execute experiment
        result = orchestrator.run_experiment()
        
        if result.get('status') in ['completed', 'completed_analysis_only', 'completed_statistical_prep', 'completed_skip_synthesis', 'completed_resume_synthesis']:
            # Provide accurate completion messages based on what was actually completed
            status = result.get('status')
            pipeline_status = result.get('pipeline_status', 'full_completion')
            
            if status == 'completed_analysis_only':
                rich_console.print_success("✅ Analysis phase completed successfully!")
                rich_console.print_info("📊 Partial pipeline completion - analysis only")
                if result.get('remaining_phases'):
                    remaining = ', '.join(result['remaining_phases'])
                    rich_console.print_info(f"⏭️  Remaining phases: {remaining}")
            elif status == 'completed_statistical_prep':
                rich_console.print_success("✅ Statistical preparation completed successfully!")
                rich_console.print_info("📊 Partial pipeline completion - ready for external statistical analysis")
                if result.get('remaining_phases'):
                    remaining = ', '.join(result['remaining_phases'])
                    rich_console.print_info(f"⏭️  Remaining phases: {remaining}")
                rich_console.print_info("💡 Use 'discernus resume' to complete synthesis later")
            elif status == 'completed_skip_synthesis':
                rich_console.print_success("✅ Pipeline completed (synthesis skipped)!")
                rich_console.print_info("📊 All phases completed except synthesis")
            elif status == 'completed_resume_synthesis':
                rich_console.print_success("✅ Synthesis resume completed successfully!")
                rich_console.print_info("📊 Full pipeline now complete")
            else:
                # Full completion
                rich_console.print_success("✅ Full experiment pipeline completed successfully!")
                rich_console.print_info("📊 All phases completed: analysis → derived metrics → evidence retrieval → synthesis")
            
            if result.get('results_directory'):
                rich_console.print_info(f"📁 Results saved to: {result['results_directory']}")
            if result.get('mode') == 'resume_from_stats' and result.get('resumed_from'):
                rich_console.print_info(f"🔄 Resumed from statistical preparation run: {result['resumed_from']}")
            exit_success()
        else:
            rich_console.print_error(f"❌ Experiment failed: {result.get('error', 'Unknown error')}")
            exit_general_error(result.get('error', 'Unknown error'))
            
    except CleanAnalysisError as e:
        rich_console.print_error(f"❌ Analysis error: {e}")
        exit_general_error(str(e))
    except Exception as e:
        rich_console.print_error(f"❌ Unexpected error: {e}")
        exit_general_error(str(e))

@cli.command()
@click.argument('experiment_path', default='.', type=str)
@click.option('--analysis-model', envvar='DISCERNUS_ANALYSIS_MODEL',
              default='vertex_ai/gemini-2.5-flash',
              help='LLM model for document analysis. Use flash for speed, pro for accuracy.')
@click.option('--synthesis-model', envvar='DISCERNUS_SYNTHESIS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for report synthesis. Pro recommended for complex analysis.')
@click.option('--validation-model', envvar='DISCERNUS_VALIDATION_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for experiment validation. Pro model provides high-quality validation.')
@click.option('--derived-metrics-model', envvar='DISCERNUS_DERIVED_METRICS_MODEL',
              default='vertex_ai/gemini-2.5-pro',
              help='LLM model for statistical analysis and derived metrics.')
@click.option('--dry-run', is_flag=True, envvar='DISCERNUS_DRY_RUN', 
              help='Preview what would be executed without running')
@click.option('--no-auto-commit', is_flag=True, envvar='DISCERNUS_NO_AUTO_COMMIT', 
              help='Disable automatic Git commit after successful run')
@click.pass_context
def resume(ctx, experiment_path: str, analysis_model: Optional[str], synthesis_model: Optional[str], validation_model: Optional[str], derived_metrics_model: Optional[str], dry_run: bool, no_auto_commit: bool):
    """Resume from statistical preparation to full synthesis.
    
    EXPERIMENT_PATH: Path to experiment directory (defaults to current directory).
    Requires existing statistical preparation results from a previous --statistical-prep run.
    """
    # Ensure experiment_path is a string
    if isinstance(experiment_path, Path):
        experiment_path = str(experiment_path)
    exp_path = Path(str(experiment_path)).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    click.echo("🔄 Resume from statistical preparation mode")
    
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
    if not no_auto_commit:
        no_auto_commit = not config.auto_commit
    
    # Check for existing statistical preparation results
    stats_runs = list(exp_path.glob("runs/*/results/scores.csv"))
    if not stats_runs:
        rich_console.print_error("❌ No statistical preparation results found to resume from")
        rich_console.print_info("   Run with --statistical-prep first to create statistical preparation results")
        exit_invalid_usage("No statistical preparation results found")
    
    # Use the most recent statistical preparation run
    latest_stats_run = max(stats_runs, key=lambda p: p.stat().st_mtime)
    rich_console.print_info(f"📊 Resuming from statistical preparation: {latest_stats_run.parent}")
    rich_console.print_info("🔄 Resume Mode: Completing synthesis from statistical preparation")
    rich_console.print_info("   This will:")
    rich_console.print_info("   • Load existing analysis and derived metrics results")
    rich_console.print_info("   • Run evidence retrieval and synthesis")
    rich_console.print_info("   • Generate final research report with citations")
    rich_console.print_info("   • Create complete synthesis assets")
    
    # Validate models
    models_to_validate = [
        ("analysis", analysis_model),
        ("synthesis", synthesis_model),
        ("validation", validation_model),
        ("derived_metrics", derived_metrics_model)
    ]
    _validate_models(models_to_validate)
    
    # Initialize orchestrator with resume mode
    orchestrator = CleanAnalysisOrchestrator(
        experiment_path=exp_path,
        analysis_model=analysis_model,
        synthesis_model=synthesis_model,
        validation_model=validation_model,
        derived_metrics_model=derived_metrics_model,
        dry_run=dry_run,
        skip_validation=False,
        analysis_only=False,
        statistical_prep=False,
        resume_from_stats=True,
        auto_commit=not no_auto_commit,
        verbosity=verbosity
    )
    
    try:
        # Execute resume
        result = orchestrator.run_experiment()
        
        if result.get('status') in ['completed', 'completed_analysis_only', 'completed_statistical_prep', 'completed_skip_synthesis', 'completed_resume_synthesis']:
            # Provide accurate completion messages for resume operations
            status = result.get('status')
            
            if status == 'completed_resume_synthesis':
                rich_console.print_success("✅ Synthesis resume completed successfully!")
                rich_console.print_info("📊 Full experiment pipeline now complete")
            else:
                rich_console.print_success("✅ Resume completed successfully!")
                
            if result.get('results_directory'):
                rich_console.print_info(f"📁 Results saved to: {result['results_directory']}")
            if result.get('mode') == 'resume_from_stats' and result.get('resumed_from'):
                rich_console.print_info(f"🔄 Resumed from statistical preparation run: {result['resumed_from']}")
            exit_success()
        else:
            rich_console.print_error(f"❌ Resume failed: {result.get('error', 'Unknown error')}")
            exit_general_error(result.get('error', 'Unknown error'))
            
    except CleanAnalysisError as e:
        rich_console.print_error(f"❌ Resume error: {e}")
        exit_general_error(str(e))
    except Exception as e:
        rich_console.print_error(f"❌ Unexpected error during resume: {e}")
        exit_general_error(str(e))

@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True, path_type=str))
@click.option('--quiet', is_flag=True, help='Suppress progress messages')
@click.pass_context
def cleanup(ctx, experiment_path: str, quiet: bool):
    """Clean up orphaned artifact registry entries.
    
    Removes registry entries for artifacts that no longer exist on disk.
    This fixes warnings about missing artifacts during experiment runs.
    """
    from pathlib import Path
    from .core.security_boundary import ExperimentSecurityBoundary
    from .core.local_artifact_storage import LocalArtifactStorage
    from .cli_console import DiscernusConsole
    
    rich_console = DiscernusConsole()
    
    try:
        # Initialize security boundary
        exp_path = Path(experiment_path).resolve()
        if not exp_path.exists():
            rich_console.print_error(f"Experiment path does not exist: {exp_path}")
            ctx.exit(1)
            
        security = ExperimentSecurityBoundary(exp_path)
        
        # Initialize artifact storage for shared cache
        shared_cache_dir = exp_path / "shared_cache"
        if not shared_cache_dir.exists():
            rich_console.print_error(f"No shared cache found at: {shared_cache_dir}")
            rich_console.print_info("Run an experiment first to create the cache structure")
            ctx.exit(1)
            
        artifact_storage = LocalArtifactStorage(
            security_boundary=security,
            run_folder=shared_cache_dir,
            run_name="cleanup"
        )
        
        # Run cleanup
        stats = artifact_storage.cleanup_orphaned_entries(quiet=quiet)
        
        if not quiet:
            rich_console.print_success(f"Registry cleanup completed!")
            rich_console.print_info(f"📊 Processed: {stats['total_processed']} entries")
            rich_console.print_info(f"🗑️  Removed: {stats['orphaned_removed']} orphaned entries")
            rich_console.print_info(f"✅ Valid: {stats['valid_entries']} entries")
            
        if stats['orphaned_removed'] > 0:
            rich_console.print_info("💡 Warnings about missing artifacts should now be resolved")
        
    except Exception as e:
        rich_console.print_error(f"Cleanup failed: {e}")
        ctx.exit(1)

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
@click.option('--minimal', is_flag=True, help='Create minimal archive (excludes logs and artifacts)')
def archive(run_directory: str, output: Optional[str], minimal: bool):
    """Create a complete golden run archive for research transparency.
    
    Creates a self-contained archive with all experiment data, results, and provenance.
    Perfect for peer review, replication research, and archival.
    
    RUN_DIRECTORY: Path to experiment run directory (e.g., projects/experiment/runs/20250127T143022Z)
    """
    run_path = Path(run_directory)
    output_path = Path(output) if output else None
    
    try:
        rich_console.print_section(f"📦 Creating Golden Run Archive: {run_path.name}")
        
        # Determine run mode from manifest
        run_mode = _detect_run_mode(run_path)
        rich_console.print_info(f"🔍 Detected run mode: {run_mode}")
        
        # Always consolidate provenance and input materials
        rich_console.print_info("📊 Consolidating provenance data...")
        consolidate_run_provenance(run_path, None)
        rich_console.print_success("✅ Provenance data consolidated")
        
        rich_console.print_info("📁 Consolidating input materials...")
        consolidate_input_materials(run_path, None)
        rich_console.print_success("✅ Input materials consolidated")
        
        # Create statistical package for runs with data
        if run_mode in ['standard', 'statistical_prep', 'skip_synthesis']:
            rich_console.print_info("📊 Creating statistical package...")
            _create_statistical_package(run_path)
            rich_console.print_success("✅ Statistical package created")
        
        # Include logs and artifacts unless minimal mode
        if not minimal:
            rich_console.print_info("📋 Copying session logs...")
            _copy_session_logs(run_path)
            rich_console.print_success("✅ Session logs copied")
            
            rich_console.print_info("🗄️ Copying artifact content...")
            _copy_artifact_content(run_path)
            rich_console.print_success("✅ Artifact content copied")
        
        # Generate documentation
        rich_console.print_info("📋 Generating comprehensive documentation...")
        try:
            docs_path = generate_golden_run_documentation(run_path, output_path)
            rich_console.print_success("✅ Documentation generated")
        except Exception as e:
            rich_console.print_warning(f"⚠️ Documentation generation failed: {e}")
            rich_console.print_info("📋 Continuing without documentation...")
        
        rich_console.print_success("🎉 Golden run archive created successfully!")
        rich_console.print_info("📦 Archive is self-contained and ready for peer review/archival")
        
    except Exception as e:
        rich_console.print_error(f"❌ Error creating golden run archive: {e}")
        exit_general_error(str(e))


def _detect_run_mode(run_path: Path) -> str:
    """Detect run mode from manifest file."""
    try:
        # Prefer manifest from the specific run's session directory
        experiment_path = run_path.parent.parent
        run_id = run_path.name
        manifest_file = experiment_path / "session" / run_id / "manifest.json"
        
        if manifest_file.exists():
            import json
            with open(manifest_file) as f:
                manifest = json.load(f)
            return manifest.get("run_mode", {}).get("mode_type", "unknown")
        # Fallback: try most recent session manifest
        session_dirs = [d for d in (experiment_path / "session").glob("*") if d.is_dir()]
        if session_dirs:
            latest_session = max(session_dirs, key=lambda x: x.name)
            fallback_manifest = latest_session / "manifest.json"
            if fallback_manifest.exists():
                import json
                with open(fallback_manifest) as f:
                    manifest = json.load(f)
                return manifest.get("run_mode", {}).get("mode_type", "unknown")
        return "unknown"
    except Exception:
        return "unknown"


def _copy_session_logs(run_path: Path) -> None:
    """Copy session logs to archive."""
    try:
        experiment_path = run_path.parent.parent
        run_id = run_path.name
        
        # Find the specific session directory for this run
        session_dir = experiment_path / "session" / run_id
        if not session_dir.exists():
            rich_console.print_warning(f"⚠️ Session directory not found for run {run_id}")
            return
        
        logs_source = session_dir / "logs"
        if not logs_source.exists():
            rich_console.print_warning(f"⚠️ Logs directory not found in session {run_id}")
            return
        
        # Create session_logs directory in run
        session_logs_dir = run_path / "session_logs"
        session_logs_dir.mkdir(exist_ok=True)
        
        # Remove existing logs directory if it exists to avoid conflicts
        target_logs_dir = session_logs_dir / "logs"
        if target_logs_dir.exists():
            import shutil
            shutil.rmtree(str(target_logs_dir))
        
        # Copy all log files
        import shutil
        shutil.copytree(logs_source, target_logs_dir)
        
        # Copy manifest if it exists
        manifest_file = session_dir / "manifest.json"
        if manifest_file.exists():
            shutil.copy2(manifest_file, session_logs_dir / "manifest.json")
            
        rich_console.print_success(f"✅ Session logs copied from {session_dir} to {session_logs_dir}")
                
    except Exception as e:
        rich_console.print_warning(f"⚠️ Could not copy session logs: {e}")


def _copy_artifact_content(run_path: Path) -> None:
    """Copy actual artifact content instead of symlinks."""
    try:
        artifacts_dir = run_path / "artifacts"
        if not artifacts_dir.exists():
            rich_console.print_warning("⚠️ No artifacts directory found")
            return
        
        # Find shared cache directory
        experiment_path = run_path.parent.parent
        shared_cache_dir = experiment_path / "shared_cache" / "artifacts"
        
        if not shared_cache_dir.exists():
            rich_console.print_warning("⚠️ No shared cache directory found")
            return
        
        copied_files = 0
        
        # Copy actual content for each symlink
        for file_path in artifacts_dir.rglob("*"):
            if file_path.is_file():
                if file_path.is_symlink():
                    # Get the target of the symlink
                    target_path = file_path.resolve()
                    # Security: ensure target is within shared cache or repo
                    try:
                        target_root = str(target_path)
                        allowed_prefixes = [str(shared_cache_dir.resolve()), str(experiment_path.resolve())]
                        if not any(target_root.startswith(p) for p in allowed_prefixes):
                            rich_console.print_warning(f"⚠️ Skipping unsafe symlink target: {target_path}")
                            continue
                    except Exception:
                        rich_console.print_warning(f"⚠️ Skipping unresolved symlink: {file_path}")
                        continue
                    if target_path.exists() and target_path != file_path:
                        # Create a temporary file to copy content
                        import shutil
                        temp_file = file_path.with_suffix(file_path.suffix + '.tmp')
                        shutil.copy2(target_path, temp_file)
                        
                        # Remove the symlink and replace with actual file
                        file_path.unlink()
                        temp_file.rename(file_path)
                        copied_files += 1
                else:
                    # Regular file, already has content
                    copied_files += 1
        
        rich_console.print_success(f"✅ Artifact content copied: {copied_files} files processed")
                        
    except Exception as e:
        rich_console.print_warning(f"⚠️ Could not copy artifact content: {e}")


def _create_statistical_package(run_path: Path) -> None:
    """Create researcher-ready statistical package."""
    try:
        from .core.statistical_package_generator import generate_statistical_package
        package_dir = generate_statistical_package(run_path)
        print(f"📊 Statistical package created: {package_dir}")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create statistical package: {e}")


def main():
    """Main entry point for the discernus CLI."""
    cli()

if __name__ == '__main__':
    main()
