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
    
    # Check framework character limit (15KB maximum)
    try:
        with open(framework_file, 'r') as f:
            framework_content = f.read()
        framework_size = len(framework_content)
        if framework_size > 15000:
            return False, f"❌ Framework exceeds 15KB limit: {framework_size:,} characters (limit: 15,000). See Framework Specification v7.0 for reduction strategies.", {}
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
def run(experiment_path: str, dry_run: bool, analysis_model: str, synthesis_model: str, skip_validation: bool):
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
            validator = ExperimentCoherenceAgent()
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
    
    execution_mode = "Complete experiment"
    
    if dry_run:
        click.echo("🧪 DRY RUN MODE - No actual execution")
        click.echo(f"   Experiment: {experiment['name']}")
        click.echo(f"   Framework: {experiment['framework']}")
        click.echo(f"   Corpus files: {experiment['_corpus_file_count']}")
        click.echo(f"   Mode: {execution_mode}")
        click.echo(f"   Analysis Model: {analysis_model}")
        click.echo(f"   Synthesis Model: {synthesis_model}")
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
        
        # Execute complete experiment
        result = orchestrator.run_experiment(
            analysis_model=analysis_model,
            synthesis_model=synthesis_model
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


def main():
    """Entry point for the discernus CLI command"""
    cli()


if __name__ == '__main__':
    main() 