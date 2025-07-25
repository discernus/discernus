#!/usr/bin/env python3
"""
Discernus CLI - THIN Command Line Interface
===========================================

Leverages existing Redis streams infrastructure for experiment execution.
Implements Alpha System Specification v1.0 requirements.

Commands:
- discernus run <experiment_path>    - Execute experiment end-to-end
- discernus validate <experiment_path> - Validate experiment structure
- discernus list                     - List available experiments
- discernus status [run_id]         - Show system/run status
"""

import click
import redis
import json
import yaml
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Load environment configuration
from dotenv import load_dotenv
load_dotenv()

def get_redis_client():
    """Get Redis client with environment configuration"""
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'), 
        port=int(os.getenv('REDIS_PORT', 6379)), 
        db=int(os.getenv('REDIS_DB', 0)), 
        decode_responses=True
    )

def hash_file(filepath: Path) -> str:
    """Calculate SHA256 hash of file for provenance"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def create_run_folder(experiment_path: Path) -> Path:
    """Create run folder with proper structure per Alpha System spec"""
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_folder = experiment_path / "runs" / timestamp
    
    # Create directory structure
    (run_folder / "logs").mkdir(parents=True, exist_ok=True)
    (run_folder / "assets").mkdir(parents=True, exist_ok=True)  
    (run_folder / "results").mkdir(parents=True, exist_ok=True)
    
    return run_folder

@click.group()
def cli():
    """Discernus - Computational Social Science Research Platform"""
    pass

@cli.command()
def list():
    """List available experiments"""
    projects_dir = Path('projects')
    if not projects_dir.exists():
        click.echo("No projects directory found")
        return
    
    experiments = []
    for p in projects_dir.iterdir():
        if p.is_dir() and (p / 'experiment.yaml').exists():
            experiments.append(p.name)
    
    if experiments:
        click.echo("Available experiments:")
        for exp in experiments:
            click.echo(f"  - {exp}")
    else:
        click.echo("No experiments found")

@cli.command()
@click.argument('experiment_path')
def validate(experiment_path: str):
    """Validate experiment structure (Alpha System Specification)"""
    exp_path = Path(experiment_path)
    if not exp_path.exists():
        click.echo(f"❌ Experiment path {experiment_path} does not exist")
        return
    
    # Load experiment configuration
    exp_file = exp_path / 'experiment.yaml'
    if not exp_file.exists():
        click.echo("❌ experiment.yaml not found")
        return
    
    try:
        with open(exp_file) as f:
            experiment = yaml.safe_load(f)
    except yaml.YAMLError as e:
        click.echo(f"❌ Invalid YAML in experiment.yaml: {e}")
        return
    
    # Validate framework exists
    framework_file = exp_path / experiment['framework']
    if not framework_file.exists():
        click.echo(f"❌ Framework file {experiment['framework']} not found")
        return
    
    # Validate corpus directory
    corpus_dir = exp_path / experiment['corpus_path']
    if not corpus_dir.exists():
        click.echo(f"❌ Corpus directory {experiment['corpus_path']} not found")
        return
    
    # Count corpus files
    corpus_files = list(corpus_dir.glob("*.txt"))
    if not corpus_files:
        click.echo(f"❌ No .txt files found in {experiment['corpus_path']}")
        return
    
    click.echo("✅ Experiment validation passed")
    click.echo(f"   - Framework: {experiment['framework']}")
    click.echo(f"   - Corpus: {len(corpus_files)} documents")
    click.echo(f"   - Name: {experiment.get('name', 'Untitled')}")

@cli.command()
@click.argument('experiment_path')
def run(experiment_path: str):
    """Execute experiment using Redis streams infrastructure"""
    exp_path = Path(experiment_path)
    
    # Validate first - but handle validation errors gracefully
    try:
        ctx = click.get_current_context()
        ctx.invoke(validate, experiment_path=experiment_path)
    except SystemExit:
        # Validation failed, stop execution
        return
    
    # Load experiment
    with open(exp_path / 'experiment.yaml') as f:
        experiment = yaml.safe_load(f)
    
    # Create run folder with provenance
    run_folder = create_run_folder(exp_path)
    
    # Generate asset hashes for provenance
    framework_file = exp_path / experiment['framework']
    framework_hash = hash_file(framework_file)
    
    corpus_dir = exp_path / experiment['corpus_path']
    corpus_hashes = []
    for txt_file in corpus_dir.glob("*.txt"):
        corpus_hashes.append(hash_file(txt_file))
    
    # Create orchestration task for Redis streams
    task_id = run_folder.name
    orchestration_task = {
        'task_id': task_id,
        'experiment': experiment,
        'framework_hash': framework_hash,
        'corpus_hashes': corpus_hashes,
        'experiment_path': str(exp_path),
        'run_folder': str(run_folder)
    }
    
    # Submit to orchestrator via Redis
    redis_client = get_redis_client()
    message_id = redis_client.xadd('orchestrator.tasks', {'data': json.dumps(orchestration_task)})
    
    click.echo(f"✅ Experiment '{experiment['name']}' submitted")
    click.echo(f"   - Task ID: {task_id}")
    click.echo(f"   - Message ID: {message_id}")
    click.echo(f"   - Run folder: {run_folder}")
    click.echo("\n🔄 Processing via Redis streams infrastructure...")
    click.echo("   Use 'discernus status' to monitor progress")

@cli.command()
@click.argument('run_id', required=False)
def status(run_id: Optional[str] = None):
    """Show infrastructure and run status"""
    redis_client = get_redis_client()
    
    try:
        # Check Redis connection
        redis_client.ping()
        click.echo("✅ Redis: Connected")
        
        # Check task queue lengths
        orchestrator_len = redis_client.xlen('orchestrator.tasks')
        tasks_len = redis_client.xlen('tasks') if redis_client.exists('tasks') else 0
        done_len = redis_client.xlen('tasks.done') if redis_client.exists('tasks.done') else 0
        
        click.echo(f"   - Orchestrator queue: {orchestrator_len} tasks")
        click.echo(f"   - Worker queue: {tasks_len} tasks")
        click.echo(f"   - Completed: {done_len} tasks")
        
        if run_id:
            # TODO: Add specific run status checking
            click.echo(f"\n🔍 Run {run_id} status: (Feature coming in Phase 1)")
        
    except Exception as e:
        click.echo(f"❌ Redis: {e}")

def main():
    """Entry point for CLI"""
    cli()

if __name__ == '__main__':
    main() 