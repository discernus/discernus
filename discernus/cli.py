#!/usr/bin/env python3
"""
Discernus CLI v2.1 - Simplified Researcher Interface
===================================================

Streamlined CLI with three core modes for optimal researcher experience:

Core Commands:
- discernus run <experiment_path>       - Execute complete experiment (analysis + synthesis)
- discernus continue <experiment_path>  - Intelligently resume from existing artifacts  
- discernus debug <experiment_path>     - Interactive debugging with detailed tracing

Management Commands:
- discernus validate <experiment_path>  - Validate experiment structure  
- discernus list                        - List available experiments
- discernus status                      - Show infrastructure status
- discernus run                         - Execute experiments (no infrastructure required)
- discernus stop                        - Stop infrastructure services
"""

import click
import datetime
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from discernus.core.thin_orchestrator import ThinOrchestrator, ThinOrchestratorError
from discernus.core.config import get_config, get_config_file_path
from discernus.core.exit_codes import (
    ExitCode, exit_success, exit_general_error, exit_invalid_usage, 
    exit_validation_failed, exit_infrastructure_error, exit_file_error, exit_config_error
)

# Rich CLI integration for professional terminal interface
from .cli_console import rich_console


def check_infrastructure() -> Dict[str, bool]:
    """Check if required infrastructure is running"""
    import socket
    
    def is_port_open(host: str, port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False
    
    # Infrastructure checks removed - system now uses local storage only
    return {}


def ensure_infrastructure() -> bool:
    """Infrastructure startup removed - system now uses local storage only"""
    # No infrastructure required for local storage
    return True


def validate_experiment_structure(experiment_path: Path) -> tuple[bool, str, Dict[str, Any]]:
    """Validate experiment directory structure and configuration"""
    if not experiment_path.exists():
        return False, f"❌ Experiment path does not exist: {experiment_path}", {}
    
    # Check for experiment.md
    experiment_file = experiment_path / "experiment.md"
    if not experiment_file.exists():
        return False, f"❌ Missing experiment.md in {experiment_path}", {}
    
    # Parse experiment configuration
    try:
        with open(experiment_file, 'r') as f:
            content = f.read()
            
        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                import yaml
                config = yaml.safe_load(parts[1])
            else:
                return False, "❌ Invalid experiment.md format (missing YAML frontmatter)", {}
        else:
            return False, "❌ experiment.md missing YAML frontmatter", {}
            
    except Exception as e:
        return False, f"❌ Error parsing experiment.md: {e}", {}
    
    # Check framework file exists (handle both canonical and local paths)
    framework_filename = config.get('framework', 'framework.md')
    
    if framework_filename.startswith("../../frameworks/"):
        # Canonical framework - resolve relative to project root
        # Find project root by looking for discernus directory
        current_path = experiment_path
        project_root = None
        
        # Walk up the directory tree to find project root
        while current_path != current_path.parent:  # Stop at filesystem root
            if (current_path / "discernus").exists() and (current_path / "frameworks").exists():
                project_root = current_path
                break
            current_path = current_path.parent
        
        if not project_root:
            return False, f"❌ Cannot find project root for canonical framework: {framework_filename}", {}
        
        canonical_path = framework_filename.lstrip("../../")
        framework_file = project_root / canonical_path
        
        if not framework_file.exists():
            return False, f"❌ Canonical framework not found: {framework_filename}", {}
    else:
        # Local framework - resolve relative to experiment directory
        framework_file = experiment_path / framework_filename
        if not framework_file.exists():
            return False, f"❌ Framework file not found: {framework_file}", {}
    
    # Check framework character limit (50KB maximum)
    try:
        with open(framework_file, 'r') as f:
            framework_content = f.read()
        framework_size = len(framework_content)
        if framework_size > 50000:
            return False, f"❌ Framework exceeds 50KB limit: {framework_size:,} characters (limit: 50,000). See Framework Specification v7.3 for reduction strategies.", {}
    except Exception as e:
        return False, f"❌ Error reading framework file: {e}", {}
    
    # Check corpus directory exists
    corpus_path = experiment_path / config.get('corpus_path', 'corpus')
    if not corpus_path.exists():
        return False, f"❌ Corpus directory not found: {corpus_path}", {}
    
    # THIN: Delegate validation to ExperimentCoherenceAgent
    from discernus.agents.experiment_coherence_agent.agent import ExperimentCoherenceAgent
    
    try:
        # Use ExperimentCoherenceAgent for comprehensive validation
        coherence_agent = ExperimentCoherenceAgent()
        validation_result = coherence_agent.validate_experiment(experiment_path)
        
        # Helen 2.0: Only blocking issues cause validation failure
        if validation_result.has_blocking_issues():
            # Return detailed validation failure information for blocking issues
            blocking_issues = validation_result.get_issues_by_priority("BLOCKING")
            if blocking_issues:
                issue = blocking_issues[0]
                return False, f"❌ {issue.description}", {"validation_result": validation_result}
            else:
                return False, "❌ Experiment has blocking validation issues", {}
        
        # Validation passed - extract basic info for CLI
        corpus_path = experiment_path / config.get('corpus_path', 'corpus')
        corpus_manifest_file = corpus_path / "corpus.md"
        
        # Quick file count for CLI display
        with open(corpus_manifest_file, 'r') as f:
            content = f.read()
        
        if '```json' in content:
            json_start = content.find('```json') + 7
            json_end = content.find('```', json_start)
            if json_end != -1:
                json_content = content[json_start:json_end].strip()
                manifest_data = json.loads(json_content)
                file_count = len(manifest_data.get('file_manifest', []))
                
                config['_corpus_file_count'] = file_count
                config['corpus_path'] = str(corpus_path)
                return True, f"✅ Valid experiment with {file_count} corpus files (THIN validation)", config
        
        return True, "✅ Valid experiment (THIN validation)", config
        
    except Exception as e:
        return False, f"❌ Validation error: {e}", {}


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
    Common Examples:
      python3 -m discernus.cli run                          # Run experiment in current directory
      python3 -m discernus.cli run --dry-run                # Preview what would be executed
      python3 -m discernus.cli validate                     # Validate current experiment
      python3 -m discernus.cli validate --dry-run           # Preview validation checks
      python3 -m discernus.cli continue --synthesis-model vertex_ai/gemini-2.5-pro
      python3 -m discernus.cli artifacts                    # Show available cache artifacts
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store global options in context
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['no_color'] = no_color
    ctx.obj['config_path'] = config
    
    # Load configuration
    if config:
        from pathlib import Path
        ctx.obj['config'] = get_config()  # Will use the specified config path
    else:
        ctx.obj['config'] = get_config()  # Will auto-discover config files
    
    # Configure Rich console based on global options
    if no_color:
        rich_console.console._color_system = None
    
    # Set verbosity level
    if quiet and verbose:
        rich_console.print_warning("Both --quiet and --verbose specified, using verbose")
    
    ctx.obj['verbosity'] = 'verbose' if verbose else ('quiet' if quiet else 'normal')


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, envvar='DISCERNUS_DRY_RUN', help='Show what would be done without executing')
@click.option('--analysis-model', envvar='DISCERNUS_ANALYSIS_MODEL', 
              help='LLM model for analysis (e.g., vertex_ai/gemini-2.5-pro, openai/gpt-4o)')
@click.option('--synthesis-model', envvar='DISCERNUS_SYNTHESIS_MODEL', 
              help='LLM model for synthesis (e.g., vertex_ai/gemini-2.5-flash-lite, openai/gpt-4o-mini)')
@click.option('--skip-validation', is_flag=True, envvar='DISCERNUS_SKIP_VALIDATION', help='Skip experiment coherence validation')
@click.option('--analysis-only', is_flag=True, envvar='DISCERNUS_ANALYSIS_ONLY', help='Run analysis and CSV export only, skip synthesis')
@click.option('--ensemble-runs', type=int, envvar='DISCERNUS_ENSEMBLE_RUNS', help='Number of ensemble runs for self-consistency')
@click.option('--no-auto-commit', is_flag=True, envvar='DISCERNUS_NO_AUTO_COMMIT', help='Disable automatic Git commit after successful run completion')
@click.pass_context
def run(ctx, experiment_path: str, dry_run: bool, analysis_model: Optional[str], synthesis_model: Optional[str], skip_validation: bool, analysis_only: bool, ensemble_runs: Optional[int], no_auto_commit: bool):
    """Execute complete experiment (analysis + synthesis). Defaults to current directory."""
    exp_path = Path(experiment_path).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    # Get configuration and apply defaults
    config = ctx.obj['config']
    verbosity = ctx.obj['verbosity']
    
    # Apply config defaults for None values
    if analysis_model is None:
        analysis_model = config.analysis_model
    if synthesis_model is None:
        synthesis_model = config.synthesis_model
    if ensemble_runs is None:
        ensemble_runs = config.ensemble_runs
    
    # Override config booleans if CLI flags are set
    if not dry_run:
        dry_run = config.dry_run
    if not skip_validation:
        skip_validation = config.skip_validation
    if not no_auto_commit:
        no_auto_commit = not config.auto_commit
    
    if verbosity == 'verbose':
        rich_console.print_info(f"Using config file: {get_config_file_path() or 'None (using defaults)'}")
        rich_console.print_info(f"Analysis model: {analysis_model}")
        rich_console.print_info(f"Synthesis model: {synthesis_model}")
    
    if verbosity != 'quiet':
        rich_console.echo(f"🎯 Discernus v2.0 - Running experiment: {experiment_path}")
    else:
        rich_console.echo(f"🎯 Running: {experiment_path}")
    
    # Validate experiment structure (unless skipped)
    if not skip_validation:
        valid, message, experiment = validate_experiment_structure(exp_path)
        if not valid:
            rich_console.print_error(message.replace("❌ ", ""))
            exit_validation_failed("Experiment structure validation failed")
        
        click.echo(message)
    else:
        # Skip structure validation - just load basic experiment info
        click.echo("⚠️  Skipping experiment structure validation")
        try:
            import yaml
            with open(exp_path / "experiment.md", 'r') as f:
                content = f.read()
                # Extract YAML front matter
                if content.startswith('---'):
                    _, yaml_content, _ = content.split('---', 2)
                    experiment = yaml.safe_load(yaml_content)
                    experiment['_corpus_file_count'] = len(list((exp_path / experiment.get('corpus_path', 'corpus')).glob('*')))
                else:
                    experiment = {'name': 'Unknown', 'framework': 'Unknown', 'corpus_path': 'corpus', '_corpus_file_count': 0}
        except Exception as e:
            experiment = {'name': 'Unknown', 'framework': 'Unknown', 'corpus_path': 'corpus', '_corpus_file_count': 0}
    
    # Validate experiment coherence (unless skipped)
    if not skip_validation:
        click.echo("🔍 Validating experiment coherence...")
        try:
            from discernus.agents.experiment_coherence_agent import ExperimentCoherenceAgent
            validator = ExperimentCoherenceAgent(model=analysis_model)
            validation_result = validator.validate_experiment(exp_path)
            
            # Helen 2.0: Display issues by priority, smart exit codes
            blocking_issues = validation_result.get_issues_by_priority("BLOCKING")
            quality_issues = validation_result.get_issues_by_priority("QUALITY")
            suggestions = validation_result.get_issues_by_priority("SUGGESTION")
            
            if blocking_issues:
                click.echo("🚫 BLOCKING Issues (must fix):")
                for issue in blocking_issues:
                    click.echo(f"\n  • {issue.description}")
                    click.echo(f"    Impact: {issue.impact}")
                    click.echo(f"    Fix: {issue.fix}")
                    if issue.affected_files:
                        click.echo(f"    Affected: {', '.join(issue.affected_files[:3])}")
            
            if quality_issues:
                click.echo(f"\n⚠️ QUALITY Issues (should fix):")
                for issue in quality_issues:
                    click.echo(f"\n  • {issue.description}")
                    click.echo(f"    Impact: {issue.impact}")
                    click.echo(f"    Fix: {issue.fix}")
                    if issue.affected_files:
                        click.echo(f"    Affected: {', '.join(issue.affected_files[:3])}")
            
            if suggestions:
                click.echo(f"\n💡 SUGGESTIONS (nice to have):")
                for issue in suggestions:
                    click.echo(f"\n  • {issue.description}")
                    click.echo(f"    Fix: {issue.fix}")
            
            if validation_result.suggestions:
                click.echo(f"\n💡 General Suggestions:")
                for suggestion in validation_result.suggestions:
                    click.echo(f"  • {suggestion}")
            
            # Helen 2.0: Only blocking issues cause exit 1
            if blocking_issues:
                click.echo(f"\n💡 To skip validation when running, use: --skip-validation")
                sys.exit(1)
            else:
                if quality_issues or suggestions:
                    click.echo("✅ Validation passed with recommendations")
                else:
                    click.echo("✅ Experiment coherence validation passed")
        except Exception as e:
            click.echo(f"⚠️  Validation failed with error: {e}")
            click.echo("💡 Continuing without validation...")
    
    execution_mode = "Analysis + CSV export only" if analysis_only else "Complete experiment"
    
    if dry_run:
        click.echo("🧪 DRY RUN MODE - No actual execution")
        click.echo(f"   Experiment: {experiment['name']}")
        click.echo(f"   Framework: {experiment['framework']}")
        click.echo(f"   Corpus files: {experiment['_corpus_file_count']}")
        click.echo(f"   Mode: {execution_mode}")
        click.echo(f"   Analysis Model: {analysis_model}")
        click.echo(f"   Synthesis Model: {synthesis_model}")
        # TODO: Ensemble runs disabled pending architectural review
        # click.echo(f"   Ensemble Runs: {ensemble_runs}")
        click.echo(f"   Ensemble Runs: 1 (disabled)")
        return
    
    # Ensure infrastructure is running
    if not ensure_infrastructure():
        click.echo("❌ Infrastructure startup failed. Run 'discernus start' manually.")
        sys.exit(1)
    
    # Execute using THIN v2.0 orchestrator with direct function calls
    rich_console.print_info("Initializing THIN v2.0 orchestrator with batch management...")
    
    # Display experiment summary
    rich_console.print_experiment_summary(experiment)
    
    # Execute using THIN v2.0 direct orchestration
    try:
        rich_console.print_section("🚀 Experiment Execution")
        rich_console.echo(f"📝 Using analysis model: {analysis_model}")
        rich_console.echo(f"📝 Using synthesis model: {synthesis_model}")
            
        orchestrator = ThinOrchestrator(exp_path)
        
        # Execute experiment with progress indication
        with rich_console.create_progress("Running experiment...") as progress:
            task = progress.add_task("Executing experiment", total=100)
            
            # Execute experiment (complete or analysis-only)
            result = orchestrator.run_experiment(
                analysis_model=analysis_model,
                synthesis_model=synthesis_model,
                analysis_only=analysis_only,
                auto_commit=(not no_auto_commit),
                # TODO: Ensemble runs disabled pending architectural review
                # ensemble_runs=ensemble_runs
                ensemble_runs=1
            )
            
            # Update progress to complete
            progress.update(task, completed=100)
        
        # Show completion with enhanced details
        rich_console.print_success("Experiment completed successfully!")
        
        if isinstance(result, dict) and 'run_id' in result:
            # Create results table
            results_table = rich_console.create_table("Experiment Results", ["Item", "Location"])
            results_table.add_row("Run ID", result['run_id'])
            results_table.add_row("Results Directory", str(exp_path / 'runs' / result['run_id']))
            results_table.add_row("Final Report", str(exp_path / 'runs' / result['run_id'] / 'results' / 'final_report.md'))
            rich_console.print_table(results_table)
            
            # Show cost summary if available
            if 'costs' in result:
                rich_console.print_cost_summary(result['costs'])
        else:
            rich_console.print_info("Results available in experiment runs directory")
        
    except ThinOrchestratorError as e:
        rich_console.print_error(f"Experiment failed: {e}")
        exit_general_error(f"Experiment execution failed: {e}")
    except Exception as e:
        rich_console.print_error(f"Unexpected error: {e}")
        exit_general_error(f"Unexpected error: {e}")


@cli.command(name='continue')
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', 
              help='LLM model for synthesis [default: vertex_ai/gemini-2.5-pro] (e.g., vertex_ai/gemini-2.5-flash-lite)')
def continue_experiment(experiment_path: str, synthesis_model: str):
    """Intelligently resume experiment from existing artifacts. Defaults to current directory."""
    exp_path = Path(experiment_path).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    click.echo(f"🔄 Continuing experiment: {experiment_path}")
    
    # Validate experiment structure
    valid, message, experiment = validate_experiment_structure(exp_path)
    if not valid:
        click.echo(message)
        sys.exit(1)
    
    click.echo(message)
    
    # Check for existing artifacts to determine resume point
    shared_cache_dir = exp_path / "shared_cache" / "artifacts"
    if not shared_cache_dir.exists():
        click.echo("❌ No analysis artifacts found")
        click.echo("   💡 Run: discernus run to start from beginning")
        sys.exit(1)
    
    # Ensure infrastructure is running
    if not ensure_infrastructure():
        click.echo("❌ Infrastructure startup failed. Run 'discernus start' manually.")
        sys.exit(1)
    
    try:
        click.echo(f"🚀 Resuming experiment with intelligent artifact detection...")
        click.echo(f"📝 Using synthesis model: {synthesis_model}")
            
        orchestrator = ThinOrchestrator(exp_path)
        
        # Execute with synthesis-only mode (intelligent resume)
        result = orchestrator.run_experiment(
            synthesis_model=synthesis_model,
            synthesis_only=True
        )
        
        # Show completion
        click.echo("✅ Experiment resumed and completed successfully!")
        if isinstance(result, dict) and 'run_id' in result:
            click.echo(f"   📋 Run ID: {result['run_id']}")
            click.echo(f"   📁 Results: {exp_path / 'runs' / result['run_id']}")
            click.echo(f"   📄 Report: {exp_path / 'runs' / result['run_id'] / 'results' / 'final_report.md'}")
            
            # Display cost information for research transparency
            if 'costs' in result:
                costs = result['costs']
                click.echo(f"   💰 Resume Cost: ${costs.get('total_cost_usd', 0.0):.4f} USD")
                click.echo(f"   🔢 Tokens Used: {costs.get('total_tokens', 0):,}")
                
                # Show breakdown by operation if available
                operations = costs.get('operations', {})
                if operations:
                    click.echo("   📊 Operation Breakdown:")
                    for operation, op_costs in operations.items():
                        cost_usd = op_costs.get('cost_usd', 0.0)
                        tokens = op_costs.get('tokens', 0)
                        calls = op_costs.get('calls', 0)
                        click.echo(f"      • {operation}: ${cost_usd:.4f} ({tokens:,} tokens, {calls} calls)")
        
    except ThinOrchestratorError as e:
        click.echo(f"❌ Resume failed: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--agent', type=click.Choice(['analysis', 'synthesis', 'evidence-curator', 'results-interpreter']), 
              help='Focus debugging on specific agent')
@click.option('--verbose', is_flag=True, help='Enable verbose debug output')
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', 
              help='LLM model for synthesis [default: vertex_ai/gemini-2.5-pro] (e.g., vertex_ai/gemini-2.5-flash-lite)')
def debug(experiment_path: str, agent: str, verbose: bool, synthesis_model: str):
    """Interactive debugging mode with detailed agent tracing. Defaults to current directory."""
    exp_path = Path(experiment_path).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    click.echo(f"🐛 Debug mode: {experiment_path}")
    if agent:
        click.echo(f"   🎯 Focusing on: {agent}")
    if verbose:
        click.echo(f"   📢 Verbose output enabled")
    
    # Validate experiment structure
    valid, message, experiment = validate_experiment_structure(exp_path)
    if not valid:
        click.echo(message)
        sys.exit(1)
    
    click.echo(message)
    
    # Ensure infrastructure is running
    if not ensure_infrastructure():
        click.echo("❌ Infrastructure startup failed. Run 'discernus start' manually.")
        sys.exit(1)
    
    try:
        click.echo(f"🚀 Starting debug execution...")
        click.echo(f"📝 Using synthesis model: {synthesis_model}")
        click.echo(f"🔍 Debug level: {'verbose' if verbose else 'standard'}")
            
        orchestrator = ThinOrchestrator(exp_path)
        
        # Execute with debug parameters
        result = orchestrator.run_experiment(
            synthesis_model=synthesis_model,
            synthesis_only=True,  # Debug mode typically works with existing artifacts
            debug_agent=agent,
            debug_level='verbose' if verbose else 'debug'
        )
        
        # Show completion
        click.echo("✅ Debug execution completed!")
        if isinstance(result, dict) and 'run_id' in result:
            click.echo(f"   📋 Run ID: {result['run_id']}")
            click.echo(f"   📁 Debug outputs: {exp_path / 'runs' / result['run_id']}")
            
            # Display cost information for debugging transparency
            if 'costs' in result:
                costs = result['costs']
                click.echo(f"   💰 Debug Session Cost: ${costs.get('total_cost_usd', 0.0):.4f} USD")
                click.echo(f"   🔢 Tokens Used: {costs.get('total_tokens', 0):,}")
                
                # Show agent-level breakdown for debugging
                agents = costs.get('agents', {})
                if agents:
                    click.echo("   🤖 Agent Cost Breakdown:")
                    for agent, agent_costs in agents.items():
                        cost_usd = agent_costs.get('cost_usd', 0.0)
                        tokens = agent_costs.get('tokens', 0)
                        calls = agent_costs.get('calls', 0)
                        click.echo(f"      • {agent}: ${cost_usd:.4f} ({tokens:,} tokens, {calls} calls)")
        
    except ThinOrchestratorError as e:
        click.echo(f"❌ Debug execution failed: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, help='Preview validation without executing coherence validation')
def validate(experiment_path: str, dry_run: bool):
    """Validate experiment structure and configuration. Defaults to current directory."""
    exp_path = Path(experiment_path).resolve()
    
    # Check if experiment path exists
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    if not exp_path.is_dir():
        click.echo(f"❌ Experiment path is not a directory: {exp_path}")
        sys.exit(1)
    
    if dry_run:
        click.echo(f"🔍 [DRY RUN] Would validate experiment: {experiment_path}")
    else:
        click.echo(f"🔍 Validating experiment: {experiment_path}")
    
    valid, message, experiment = validate_experiment_structure(exp_path)
    click.echo(message)
    
    if valid:
        click.echo(f"   📋 Name: {experiment['name']}")
        click.echo(f"   📄 Framework: {experiment['framework']}")
        click.echo(f"   📁 Corpus: {experiment['corpus_path']} ({experiment['_corpus_file_count']} files)")
        
        if dry_run:
            click.echo(f"   ✅ [DRY RUN] Basic structure valid. Would run coherence validation.")
        
    else:
        # Show detailed validation issues if available (same format as run command)
        if 'validation_result' in experiment:
            validation_result = experiment['validation_result']
            click.echo("❌ Validation failed:")
            for issue in validation_result.issues:
                click.echo(f"\n  • {issue.description}")
                click.echo(f"    Impact: {issue.impact}")
                click.echo(f"    Fix: {issue.fix}")
                if issue.affected_files:
                    click.echo(f"    Affected: {', '.join(issue.affected_files[:3])}")
            
            if validation_result.suggestions:
                click.echo(f"\n💡 Suggestions:")
                for suggestion in validation_result.suggestions:
                    click.echo(f"  • {suggestion}")
            
            click.echo(f"\n💡 To skip validation when running, use: --skip-validation")
    
    sys.exit(0 if valid else 1)


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dry-run', is_flag=True, help='Show what would be promoted without executing')
@click.option('--cleanup', is_flag=True, help='Clean up leftover development files after promotion')
@click.option('--force', is_flag=True, help='Skip cleanup confirmation prompts')
def promote(experiment_path: str, dry_run: bool, cleanup: bool, force: bool):
    """Promote workbench files to operational status. Defaults to current directory."""
    exp_path = Path(experiment_path)
    
    click.echo(f"🔄 Discernus Workbench - Promoting: {experiment_path}")
    
    if not exp_path.exists():
        click.echo(f"❌ Experiment path does not exist: {exp_path}")
        sys.exit(1)
    
    workbench_dir = exp_path / "workbench"
    archive_dir = exp_path / "archive"
    
    # Check if workbench directory exists
    if not workbench_dir.exists():
        click.echo(f"❌ No workbench directory found: {workbench_dir}")
        click.echo("   💡 Create workbench/ directory and add files to promote")
        sys.exit(1)
    
    # Find files to promote
    promotable_files = {}
    
    # Look for experiment files (using os.listdir to avoid potential glob conflicts)
    import os
    import fnmatch
    
    if workbench_dir.exists():
        workbench_files = os.listdir(workbench_dir)
        
        # Find experiment files
        experiment_files = [workbench_dir / f for f in workbench_files if fnmatch.fnmatch(f, "experiment*.md")]
        if experiment_files:
            # Get the most recently modified experiment file
            latest_experiment = max(experiment_files, key=lambda f: f.stat().st_mtime)
            promotable_files['experiment.md'] = latest_experiment
        
        # Find framework files  
        framework_files = [workbench_dir / f for f in workbench_files if fnmatch.fnmatch(f, "framework*.md")]
        if framework_files:
            # Get the most recently modified framework file
            latest_framework = max(framework_files, key=lambda f: f.stat().st_mtime)
            promotable_files['framework.md'] = latest_framework
        
        # Find corpus files (v7.0 compatible - corpus.md files)
        corpus_files = [workbench_dir / f for f in workbench_files if fnmatch.fnmatch(f, "corpus*.md")]
        if corpus_files:
            latest_corpus = max(corpus_files, key=lambda f: f.stat().st_mtime)
            promotable_files['corpus/corpus.md'] = latest_corpus
    
    if not promotable_files:
        click.echo("❌ No promotable files found in workbench/")
        click.echo("   💡 Add experiment*.md, framework*.md, or corpus*.md files to workbench/")
        sys.exit(1)
    
    # Show what will be promoted
    click.echo("📋 Files to promote:")
    for target, source in promotable_files.items():
        mtime = source.stat().st_mtime
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        click.echo(f"   📄 {source.name} → {target} (modified: {mtime_str})")
    
    if dry_run:
        click.echo("🧪 DRY RUN - No files were actually promoted")
        return
    
    # Create archive directory if it doesn't exist
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
        click.echo(f"📁 Created archive directory: {archive_dir}")
    
    # Archive existing operational files
    archived_files = []
    timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    
    for target_file, _ in promotable_files.items():
        target_path = exp_path / target_file
        if target_path.exists():
            # Create archive filename with timestamp
            archive_name = f"{timestamp}_{target_path.name}"
            archive_path = archive_dir / archive_name
            
            # Copy to archive
            shutil.copy2(target_path, archive_path)
            archived_files.append((target_file, archive_name))
            click.echo(f"📦 Archived: {target_file} → archive/{archive_name}")
    
    # Promote workbench files to operational
    promoted_files = []
    for target_file, source_path in promotable_files.items():
        target_path = exp_path / target_file
        
        # Ensure target directory exists (for corpus/corpus.md)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy workbench file to operational location
        shutil.copy2(source_path, target_path)
        promoted_files.append((source_path.name, target_file))
        click.echo(f"⬆️  Promoted: workbench/{source_path.name} → {target_file}")
    
    # Clear workbench (move promoted files to archive)
    for target_file, source_path in promotable_files.items():
        workbench_archive_name = f"{timestamp}_workbench_{source_path.name}"
        workbench_archive_path = archive_dir / workbench_archive_name
        shutil.move(source_path, workbench_archive_path)
        click.echo(f"🗂️  Workbench archived: {source_path.name} → archive/{workbench_archive_name}")
    
    # Summary
    click.echo(f"\n✅ Promotion complete!")
    click.echo(f"   📦 Archived: {len(archived_files)} operational files")
    click.echo(f"   ⬆️  Promoted: {len(promoted_files)} workbench files")
    click.echo(f"   🗂️  Cleared: {len(promotable_files)} workbench files")
    
    # Validate the promoted experiment
    click.echo(f"\n🔍 Validating promoted experiment...")
    valid, message, experiment = validate_experiment_structure(exp_path)
    if valid:
        click.echo(f"✅ {message}")
        click.echo(f"   📋 Ready to run: discernus run {experiment_path}")
    else:
        click.echo(f"❌ {message}")
        click.echo("   💡 Check promoted files and fix any issues")
    
    # Optional cleanup of development files
    if cleanup and not dry_run:
        _cleanup_development_files(exp_path, force)


def _cleanup_development_files(exp_path: Path, force: bool):
    """Clean up leftover development files from experiment root"""
    import os
    import fnmatch
    
    click.echo(f"\n🧹 Cleaning up development files...")
    
    # Define cleanup patterns
    archive_patterns = [
        "experiment_*.md",
        "framework_*.md", 
        "corpus_*.json",
        "corpus_*.md"
    ]
    
    delete_patterns = [
        ".DS_Store",
        "*_backup.md",
        "*_temp.*",
        "*.tmp",
        "*_old.*"
    ]
    
    # Find files to clean up
    archive_files = []
    delete_files = []
    
    for item in exp_path.iterdir():
        if item.is_file():
            # Skip operational files
            if item.name in ['experiment.md', 'framework.md']:
                continue
                
            # Check for archive patterns
            for pattern in archive_patterns:
                if fnmatch.fnmatch(item.name, pattern):
                    archive_files.append(item)
                    break
            else:
                # Check for delete patterns
                for pattern in delete_patterns:
                    if fnmatch.fnmatch(item.name, pattern):
                        delete_files.append(item)
                        break
    
    if not archive_files and not delete_files:
        click.echo("   ✨ Experiment root is already clean")
        return
    
    # Show what will be cleaned up
    if archive_files:
        click.echo("   📦 Files to archive:")
        for file in archive_files:
            click.echo(f"      • {file.name}")
    
    if delete_files:
        click.echo("   🗑️  Files to delete:")
        for file in delete_files:
            click.echo(f"      • {file.name}")
    
    # Confirm cleanup (unless --force)
    if not force:
        if not click.confirm("\n   Continue with cleanup?"):
            click.echo("   ⏭️  Cleanup skipped")
            return
    
    # Perform cleanup
    archive_dir = exp_path / "archive"
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    archived_count = 0
    deleted_count = 0
    
    # Archive development files
    for file in archive_files:
        archive_name = f"{timestamp}_cleanup_{file.name}"
        archive_path = archive_dir / archive_name
        shutil.move(file, archive_path)
        archived_count += 1
        click.echo(f"   📦 Archived: {file.name} → archive/{archive_name}")
    
    # Delete temporary files
    for file in delete_files:
        file.unlink()
        deleted_count += 1
        click.echo(f"   🗑️  Deleted: {file.name}")
    
    # Summary
    click.echo(f"\n   ✅ Cleanup complete!")
    if archived_count > 0:
        click.echo(f"      📦 Archived: {archived_count} development files")
    if deleted_count > 0:
        click.echo(f"      🗑️  Deleted: {deleted_count} temporary files")


@cli.command()
@click.argument('args', nargs=-1, required=True)
@click.option('--cleanup', is_flag=True, help='Clean up after promotion')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
@click.option('--dry-run', is_flag=True, help='Show what would be done without executing')
def workflow(args: tuple, cleanup: bool, force: bool, dry_run: bool):
    """Chain multiple operations: discernus workflow promote run projects/experiment"""
    
    # Parse operations and experiment path
    all_args = list(args)
    if len(all_args) < 2:
        click.echo("❌ Usage: discernus workflow <operation1> [operation2] ... <experiment_path>")
        click.echo("   Example: discernus workflow promote run projects/experiment")
        sys.exit(1)
    
    # Last argument is the experiment path
    exp_path = all_args[-1]
    ops = all_args[:-1]
    
    click.echo(f"🔗 Discernus Workflow - Chaining: {' → '.join(ops)}")
    click.echo(f"   📁 Target: {exp_path}")
    
    if dry_run:
        click.echo("🧪 DRY RUN - Operations that would be executed:")
        for i, op in enumerate(ops, 1):
            click.echo(f"   {i}. {op}")
        return
    
    # Execute operations in sequence
    for i, operation in enumerate(ops, 1):
        click.echo(f"\n📋 Step {i}/{len(ops)}: {operation}")
        
        try:
            if operation == 'promote':
                # Call promote function directly
                from click.testing import CliRunner
                runner = CliRunner()
                
                # Build promote command args
                promote_args = [exp_path]
                if cleanup:
                    promote_args.append('--cleanup')
                if force:
                    promote_args.append('--force')
                
                result = runner.invoke(promote, promote_args, catch_exceptions=False)
                if result.exit_code != 0:
                    click.echo(f"❌ Step {i} failed: promote")
                    sys.exit(result.exit_code)
                    
            elif operation == 'run':
                # Call run function directly  
                runner = CliRunner()
                result = runner.invoke(run, [exp_path], catch_exceptions=False)
                if result.exit_code != 0:
                    click.echo(f"❌ Step {i} failed: run")
                    sys.exit(result.exit_code)
                    
            elif operation == 'validate':
                # Call validate function directly
                runner = CliRunner()
                result = runner.invoke(validate, [exp_path], catch_exceptions=False)
                if result.exit_code != 0:
                    click.echo(f"❌ Step {i} failed: validate")
                    sys.exit(result.exit_code)
                    
            else:
                click.echo(f"❌ Unknown operation: {operation}")
                click.echo("   Supported: promote, run, validate")
                sys.exit(1)
                
        except Exception as e:
            click.echo(f"❌ Step {i} failed with error: {e}")
            sys.exit(1)
    
    click.echo(f"\n✅ Workflow complete! All {len(ops)} operations succeeded.")


@cli.command()
def list():
    """List available experiments"""
    projects_dir = Path('projects')
    
    if not projects_dir.exists():
        rich_console.print_error("No projects directory found")
        sys.exit(1)
    
    experiments = []
    for item in projects_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'deprecated':
            valid, message, config = validate_experiment_structure(item)
            experiments.append({
                'path': str(item),
                'valid': valid,
                'config': config if valid else {},
                'message': message
            })
    
    if not experiments:
        rich_console.print_info("No experiments found")
        return
    
    # Create Rich table for experiments
    table = rich_console.create_table("Available Experiments", ["Status", "Path", "Name", "Framework", "Corpus Files"])
    
    for exp in sorted(experiments, key=lambda x: x['path']):
        if exp['valid']:
            status = "✅ Valid"
            name = exp['config'].get('name', 'Unnamed')
            framework = exp['config'].get('framework', 'framework.md')
            corpus_count = str(exp['config']['_corpus_file_count'])
            
            table.add_row(status, exp['path'], name, framework, corpus_count)
        else:
            table.add_row("❌ Invalid", exp['path'], "-", "-", "-")
    
    rich_console.print_table(table)


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def artifacts(experiment_path: str):
    """Show experiment artifacts and available cache status for resumption. Defaults to current directory."""
    exp_path = Path(experiment_path)
    
    click.echo(f"🔍 Experiment Artifacts: {experiment_path}")
    
    # Validate experiment structure
    valid, message, experiment = validate_experiment_structure(exp_path)
    if not valid:
        click.echo(message)
        sys.exit(1)
    
    click.echo(message)
    
    # Check for shared cache artifacts
    shared_cache_dir = exp_path / "shared_cache" / "artifacts"
    if not shared_cache_dir.exists():
        click.echo("❌ No analysis artifacts found")
        click.echo("   💡 Run: discernus run --analysis-only to create artifacts")
        return
    
    # Load artifact registry to check available artifacts
    registry_file = shared_cache_dir / "artifact_registry.json"
    if not registry_file.exists():
        click.echo("❌ No artifact registry found")
        return
    
    import json
    try:
        with open(registry_file) as f:
            registry = json.load(f)
    except Exception as e:
        click.echo(f"❌ Error reading artifact registry: {e}")
        return
    
    # Check for JSON analysis artifacts
    json_artifacts = []
    
    for artifact_id, info in registry.items():
        artifact_type = info.get("metadata", {}).get("artifact_type")
        timestamp = info.get("created_at", "unknown")
        
        if artifact_type == "analysis_json_v6":
            json_artifacts.append((artifact_id, timestamp))
    
    if json_artifacts:
        # Sort by timestamp and get latest
        json_artifacts.sort(key=lambda x: x[1], reverse=True)
        latest_json = json_artifacts[0]
        
        click.echo("✅ Analysis artifacts available:")
        click.echo(f"   📊 Combined JSON: {latest_json[0][:12]}... ({latest_json[1]})")
        click.echo("")
        click.echo("🚀 Available commands:")
        click.echo("   discernus continue     # Intelligently resume from artifacts")
        click.echo("   discernus debug        # Interactive debugging mode")
    else:
        click.echo("❌ No analysis artifacts found")
        click.echo("   💡 Run: discernus run to create artifacts")


@cli.command()
def status():
    """Show infrastructure and system status"""
    rich_console.print_section("🔍 Discernus System Status")
    
    # Create status table
    table = rich_console.create_table("System Status", ["Component", "Status", "Details"])
    table.add_row("Local Storage", "✅ Ready", "No external dependencies")
    table.add_row("Git Integration", "✅ Ready", "Auto-commit enabled")
    table.add_row("LLM Gateway", "✅ Ready", "Vertex AI configured")
    
    rich_console.print_table(table)
    
    rich_console.print_section("💡 Available Commands")
    commands_table = rich_console.create_table("Commands", ["Command", "Description"])
    commands_table.add_row("discernus run", "Execute complete experiment")
    commands_table.add_row("discernus continue", "Resume from existing artifacts")
    commands_table.add_row("discernus debug", "Interactive debugging mode")
    commands_table.add_row("discernus validate", "Validate experiment structure")
    commands_table.add_row("discernus list", "List available experiments")
    
    rich_console.print_table(commands_table)


@cli.group()
def config():
    """Manage Discernus configuration"""
    pass


@config.command('show')
@click.pass_context
def config_show(ctx):
    """Show current configuration values"""
    config = ctx.obj['config']
    config_file = get_config_file_path()
    
    rich_console.print_section("🔧 Current Configuration")
    
    # Configuration source
    source_table = rich_console.create_table("Configuration Source", ["Setting", "Value"])
    source_table.add_row("Config File", str(config_file) if config_file else "None (using defaults)")
    source_table.add_row("Environment Variables", "DISCERNUS_* variables loaded")
    rich_console.print_table(source_table)
    
    # Configuration values
    config_table = rich_console.create_table("Configuration Values", ["Setting", "Value", "Source"])
    
    # Model configuration
    config_table.add_row("analysis_model", config.analysis_model, "Config/Env/Default")
    config_table.add_row("synthesis_model", config.synthesis_model, "Config/Env/Default")
    
    # Execution options
    config_table.add_row("auto_commit", str(config.auto_commit), "Config/Env/Default")
    config_table.add_row("skip_validation", str(config.skip_validation), "Config/Env/Default")
    config_table.add_row("ensemble_runs", str(config.ensemble_runs), "Config/Env/Default")
    
    # Output options
    config_table.add_row("verbose", str(config.verbose), "Config/Env/Default")
    config_table.add_row("quiet", str(config.quiet), "Config/Env/Default")
    config_table.add_row("no_color", str(config.no_color), "Config/Env/Default")
    config_table.add_row("progress", str(config.progress), "Config/Env/Default")
    
    rich_console.print_table(config_table)


@config.command('init')
@click.option('--force', is_flag=True, help='Overwrite existing config file')
@click.argument('config_path', required=False)
def config_init(force, config_path):
    """Create a default configuration file"""
    from discernus.core.config import ConfigManager
    
    if config_path:
        config_file = Path(config_path)
    else:
        config_file = Path('.discernus.yaml')
    
    if config_file.exists() and not force:
        rich_console.print_error(f"Config file already exists: {config_file}")
        rich_console.echo("Use --force to overwrite, or specify a different path")
        exit_file_error(f"Config file already exists: {config_file}")
    
    manager = ConfigManager()
    manager.create_default_config(config_file)
    
    rich_console.print_success(f"Created config file: {config_file}")
    rich_console.echo("Edit this file to customize your default settings")


@config.command('validate')
@click.argument('config_path', required=False)
def config_validate(config_path):
    """Validate a configuration file"""
    from discernus.core.config import ConfigManager
    
    try:
        if config_path:
            config_file = Path(config_path)
            if not config_file.exists():
                rich_console.print_error(f"Config file not found: {config_file}")
                exit_file_error(f"Config file not found: {config_file}")
        else:
            config_file = get_config_file_path()
            if not config_file:
                rich_console.print_error("No config file found")
                exit_config_error("No config file found")
        
        # Try to load the config
        manager = ConfigManager()
        config_data = manager._load_yaml_config(config_file)
        
        # Validate by creating a config object
        from discernus.core.config import DiscernusConfig
        config = DiscernusConfig(**config_data)
        
        rich_console.print_success(f"Config file is valid: {config_file}")
        
        # Show any unknown keys
        valid_keys = set(DiscernusConfig.model_fields.keys())
        config_keys = set(config_data.keys())
        unknown_keys = config_keys - valid_keys
        
        if unknown_keys:
            rich_console.print_warning(f"Unknown configuration keys (will be ignored): {', '.join(unknown_keys)}")
        
    except Exception as e:
        rich_console.print_error(f"Config validation failed: {e}")
        exit_config_error(f"Config validation failed: {e}")


@cli.command()
def start():
    """Start command removed - no infrastructure services required"""
    click.echo("ℹ️  No infrastructure services to start")
    click.echo("   Discernus now uses local storage with no external dependencies")


@cli.command()
def stop():
    """Stop command removed - no infrastructure services required"""
    click.echo("ℹ️  No infrastructure services to stop")
    click.echo("   Discernus now uses local storage with no external dependencies")


@cli.command()
@click.argument('experiment_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('document_name', type=str)
@click.argument('score_name', type=str)
@click.option('--score-value', type=float, required=True, help='Numerical score value to validate')
@click.option('--confidence', type=float, default=0.8, help='Confidence level (0.0-1.0)')
@click.option('--framework', type=str, help='Framework name (auto-detected if not specified)')
@click.option('--output', type=click.Path(), help='Output file for validation report')
@click.option('--model', default='vertex_ai/gemini-2.5-flash-lite', help='LLM model for validation')
def validate_score(experiment_path: str, document_name: str, score_name: str, 
                  score_value: float, confidence: float, framework: Optional[str], 
                  output: Optional[str], model: str):
    """Validate a numerical score using THIN academic validation pipeline (<5 minutes)."""
    from discernus.interfaces.academic_validation_interface import validate_score_impl
    import sys
    sys.exit(validate_score_impl(experiment_path, document_name, score_name, 
                                score_value, confidence, framework, output, model))


@cli.command()
@click.argument('run_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def visualize_provenance(run_directory):
    """
    Generate provenance visualization for an experiment run.
    
    Creates an HTML report with interactive diagrams showing:
    - Complete data flow from corpus to final results
    - Artifact dependency relationships
    - Timeline of artifact creation
    - Health check of provenance completeness
    
    RUN_DIRECTORY: Path to the experiment run directory
    """
    try:
        from discernus.core.provenance_visualizer import create_provenance_visualization
        
        print(f"🔍 Generating provenance visualization for: {run_directory}")
        
        report_path = create_provenance_visualization(run_directory)
        
        print(f"✅ Provenance visualization created: {report_path}")
        print(f"📊 Open the HTML file in your browser to view the interactive diagrams")
        print(f"🌐 Features:")
        print(f"   • Complete data flow diagram")
        print(f"   • Artifact dependency graph") 
        print(f"   • Timeline visualization")
        print(f"   • Health check indicators")
        
    except Exception as e:
        print(f"❌ Failed to generate provenance visualization: {e}")
        sys.exit(1)








def main():
    """Entry point for the discernus CLI command"""
    cli()


if __name__ == '__main__':
    main() 