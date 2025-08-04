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
- discernus start                       - Start required infrastructure (MinIO)
- discernus stop                        - Stop infrastructure services
"""

import click
import datetime
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from discernus.core.thin_orchestrator import ThinOrchestrator, ThinOrchestratorError


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
    
    return {
        'minio': is_port_open('localhost', 9000),
        'minio_console': is_port_open('localhost', 9001),
    }


def ensure_infrastructure() -> bool:
    """Ensure required infrastructure is running, start it if needed"""
    status = check_infrastructure()
    
    if not status['minio']:
        click.echo("🚀 Starting MinIO infrastructure...")
        try:
            # Use the infrastructure startup script we created
            result = subprocess.run(['./scripts/start_infrastructure.sh'], 
                                  capture_output=True, text=True, cwd='.')
            if result.returncode == 0:
                click.echo("✅ Infrastructure started successfully")
                return True
            else:
                click.echo(f"❌ Failed to start infrastructure: {result.stderr}")
                return False
        except Exception as e:
            click.echo(f"❌ Error starting infrastructure: {e}")
            return False
    
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
    
    # Check framework file exists
    framework_file = experiment_path / config.get('framework', 'framework.md')
    if not framework_file.exists():
        return False, f"❌ Framework file not found: {framework_file}", {}
    
    # Check framework character limit (30KB maximum)
    try:
        with open(framework_file, 'r') as f:
            framework_content = f.read()
        framework_size = len(framework_content)
        if framework_size > 30000:
            return False, f"❌ Framework exceeds 30KB limit: {framework_size:,} characters (limit: 30,000). See Framework Specification v7.0 for reduction strategies.", {}
    except Exception as e:
        return False, f"❌ Error reading framework file: {e}", {}
    
    # Check corpus directory exists
    corpus_path = experiment_path / config.get('corpus_path', 'corpus')
    if not corpus_path.exists():
        return False, f"❌ Corpus directory not found: {corpus_path}", {}
    
    # Count corpus files (recursively search for .txt and .pdf files)
    corpus_files = []
    for file_path in corpus_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.txt', '.pdf'] and not file_path.name.startswith('.'):
            corpus_files.append(file_path)
    
    if len(corpus_files) == 0:
        return False, f"❌ No .txt or .pdf files found in corpus directory: {corpus_path}", {}
    
    config['_corpus_file_count'] = len(corpus_files)
    return True, f"✅ Valid experiment with {len(corpus_files)} corpus files", config


@click.group()
def cli():
    """Discernus - Computational Social Science Research Platform (THIN v2.0)"""
    pass


@cli.command()
@click.argument('experiment_path')
@click.option('--dry-run', is_flag=True, help='Show what would be done without executing')
@click.option('--analysis-model', default='vertex_ai/gemini-2.5-flash-lite', help='LLM model to use for analysis (default: gemini-2.5-flash-lite)')
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', help='LLM model to use for synthesis (default: gemini-2.5-pro)')
@click.option('--skip-validation', is_flag=True, help='Skip experiment coherence validation')
@click.option('--analysis-only', is_flag=True, help='Run analysis and CSV export only, skip synthesis')
@click.option('--ensemble-runs', default=1, help='Number of ensemble runs for self-consistency (default: 1, recommended: 3-5)')
def run(experiment_path: str, dry_run: bool, analysis_model: str, synthesis_model: str, skip_validation: bool, analysis_only: bool, ensemble_runs: int = 1):
    """Execute complete experiment (analysis + synthesis)"""
    exp_path = Path(experiment_path)
    
    click.echo(f"🎯 Discernus v2.0 - Running experiment: {experiment_path}")
    
    # Validate experiment structure
    valid, message, experiment = validate_experiment_structure(exp_path)
    if not valid:
        click.echo(message)
        sys.exit(1)
    
    click.echo(message)
    
    # Validate experiment coherence (unless skipped)
    if not skip_validation:
        click.echo("🔍 Validating experiment coherence...")
        try:
            from discernus.agents.experiment_coherence_agent import ExperimentCoherenceAgent
            validator = ExperimentCoherenceAgent(model=analysis_model)
            validation_result = validator.validate_experiment(exp_path)
            
            if not validation_result.success:
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
                
                click.echo(f"\n💡 To skip validation, use: --skip-validation")
                sys.exit(1)
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
    click.echo("🎯 Initializing THIN v2.0 orchestrator with batch management...")
    
    # Execute using THIN v2.0 direct orchestration
    try:
        click.echo(f"🚀 Starting complete experiment execution...")
        click.echo(f"📝 Using analysis model: {analysis_model}")
        click.echo(f"📝 Using synthesis model: {synthesis_model}")
            
        orchestrator = ThinOrchestrator(exp_path)
        
        # Execute experiment (complete or analysis-only)
        result = orchestrator.run_experiment(
            analysis_model=analysis_model,
            synthesis_model=synthesis_model,
            analysis_only=analysis_only,
            # TODO: Ensemble runs disabled pending architectural review
        # ensemble_runs=ensemble_runs
        ensemble_runs=1
        )
        
        # Show completion with enhanced details
        click.echo("✅ Experiment completed successfully!")
        if isinstance(result, dict) and 'run_id' in result:
            click.echo(f"   📋 Run ID: {result['run_id']}")
            click.echo(f"   📁 Results: {exp_path / 'runs' / result['run_id']}")
            click.echo(f"   📄 Report: {exp_path / 'runs' / result['run_id'] / 'results' / 'final_report.md'}")
        else:
            click.echo(f"📊 Results available in experiment runs directory")
        
    except ThinOrchestratorError as e:
        click.echo(f"❌ Experiment failed: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@cli.command(name='continue')
@click.argument('experiment_path')
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', help='LLM model to use for synthesis (default: gemini-2.5-pro)')
def continue_experiment(experiment_path: str, synthesis_model: str):
    """Intelligently resume experiment from existing artifacts"""
    exp_path = Path(experiment_path)
    
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
@click.argument('experiment_path')
@click.option('--agent', type=click.Choice(['analysis', 'synthesis', 'evidence-curator', 'results-interpreter']), 
              help='Focus debugging on specific agent')
@click.option('--verbose', is_flag=True, help='Enable verbose debug output')
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', help='LLM model to use for synthesis (default: gemini-2.5-pro)')
def debug(experiment_path: str, agent: str, verbose: bool, synthesis_model: str):
    """Interactive debugging mode with detailed agent tracing"""
    exp_path = Path(experiment_path)
    
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
@click.argument('experiment_path')
def validate(experiment_path: str):
    """Validate experiment structure and configuration"""
    exp_path = Path(experiment_path)
    
    click.echo(f"🔍 Validating experiment: {experiment_path}")
    
    valid, message, experiment = validate_experiment_structure(exp_path)
    click.echo(message)
    
    if valid:
        click.echo(f"   📋 Name: {experiment['name']}")
        click.echo(f"   📄 Framework: {experiment['framework']}")
        click.echo(f"   📁 Corpus: {experiment['corpus_path']} ({experiment['_corpus_file_count']} files)")
    
    sys.exit(0 if valid else 1)


@cli.command()
@click.argument('experiment_path')
@click.option('--dry-run', is_flag=True, help='Show what would be promoted without executing')
@click.option('--cleanup', is_flag=True, help='Clean up leftover development files after promotion')
@click.option('--force', is_flag=True, help='Skip cleanup confirmation prompts')
def promote(experiment_path: str, dry_run: bool, cleanup: bool, force: bool):
    """Promote workbench files to operational status"""
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
        click.echo("❌ No projects directory found")
        sys.exit(1)
    
    click.echo("📋 Available experiments:")
    
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
        click.echo("   No experiments found")
        return
    
    for exp in sorted(experiments, key=lambda x: x['path']):
        if exp['valid']:
            click.echo(f"   ✅ {exp['path']}")
            click.echo(f"      📋 {exp['config'].get('name', 'Unnamed')}")
            click.echo(f"      📄 {exp['config'].get('framework', 'framework.md')}")
            click.echo(f"      📁 {exp['config']['_corpus_file_count']} corpus files")
        else:
            click.echo(f"   ❌ {exp['path']} - Invalid")


@cli.command()
@click.argument('experiment_path')
def artifacts(experiment_path: str):
    """Show experiment artifacts and available resumption points"""
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
    click.echo("🔍 Discernus Infrastructure Status")
    
    status = check_infrastructure()
    
    click.echo("📊 Services:")
    click.echo(f"   MinIO Storage: {'✅ Running' if status['minio'] else '❌ Stopped'} (localhost:9000)")
    click.echo(f"   MinIO Console: {'✅ Running' if status['minio_console'] else '❌ Stopped'} (localhost:9001)")
    
    # Test MinIO connection if running
    if status['minio']:
        try:
            from discernus.storage.minio_client import get_default_client
            client = get_default_client()
            click.echo("   MinIO Connection: ✅ Connected")
        except Exception as e:
            click.echo(f"   MinIO Connection: ❌ Failed ({e})")
    
    click.echo("")
    click.echo("💡 Commands:")
    click.echo("   discernus start      - Start infrastructure services")
    click.echo("   discernus stop       - Stop infrastructure services")
    click.echo("   discernus run        - Execute complete experiment")
    click.echo("   discernus continue   - Resume from existing artifacts")
    click.echo("   discernus debug      - Interactive debugging mode")


@cli.command()
def start():
    """Start required infrastructure services"""
    click.echo("🚀 Starting Discernus infrastructure...")
    
    try:
        result = subprocess.run(['./scripts/start_infrastructure.sh'], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            click.echo("✅ Infrastructure started successfully")
        else:
            click.echo("❌ Infrastructure startup failed")
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error starting infrastructure: {e}")
        sys.exit(1)


@cli.command()
def stop():
    """Stop infrastructure services"""
    click.echo("🛑 Stopping Discernus infrastructure...")
    
    try:
        # Stop MinIO
        subprocess.run(['pkill', '-f', 'minio server'], capture_output=True)
        # Stop Redis (if running)
        subprocess.run(['pkill', 'redis-server'], capture_output=True)
        
        click.echo("✅ Infrastructure stopped")
    except Exception as e:
        click.echo(f"❌ Error stopping infrastructure: {e}")


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


@cli.command()
@click.argument('run_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def browse_artifacts(run_directory):
    """
    Generate human-friendly artifact browser for an experiment run.
    
    Creates an HTML report with interactive artifact exploration:
    - Human-readable artifact names and descriptions
    - Search and filter capabilities
    - Artifact content preview
    - Dependency relationship exploration
    
    RUN_DIRECTORY: Path to the experiment run directory
    """
    try:
        from discernus.core.artifact_browser import create_artifact_browser
        
        print(f"🔍 Generating artifact browser for: {run_directory}")
        
        report_path = create_artifact_browser(run_directory)
        
        print(f"✅ Artifact browser created: {report_path}")
        print(f"📊 Open the HTML file in your browser to explore artifacts")
        print(f"🌐 Features:")
        print(f"   • Human-readable artifact names")
        print(f"   • Search and filter capabilities")
        print(f"   • Content preview")
        print(f"   • Dependency relationships")
        
    except Exception as e:
        print(f"❌ Failed to generate artifact browser: {e}")
        sys.exit(1)


def main():
    """Entry point for the discernus CLI command"""
    cli()


if __name__ == '__main__':
    main() 