#!/usr/bin/env python3
"""
THIN CLI for Discernus - Leverages Existing Infrastructure
==========================================================

This CLI does the absolute minimum:
1. Validates experiment structure
2. Creates orchestration task for existing OrchestratorAgent
3. Lets existing Redis/MinIO infrastructure handle everything

NO subprocess management, NO worker processes, NO complex coordination.
"""

import click
import redis
import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime

def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def hash_file(filepath):
    """Calculate SHA256 hash of file"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

@click.group()
def cli():
    """THIN CLI for Discernus - uses existing infrastructure"""
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
def run(experiment_path):
    """Run experiment using existing infrastructure"""
    exp_path = Path(experiment_path)
    if not exp_path.exists():
        click.echo(f"Experiment path {experiment_path} does not exist")
        return
    
    # Validate basic structure
    exp_file = exp_path / 'experiment.yaml'
    if not exp_file.exists():
        click.echo("experiment.yaml not found")
        return
    
    # Load experiment
    with open(exp_file) as f:
        experiment = yaml.safe_load(f)
    
    # Validate framework exists
    framework_file = exp_path / experiment['framework']
    if not framework_file.exists():
        click.echo(f"Framework file {experiment['framework']} not found")
        return
    
    # Validate corpus directory
    corpus_dir = exp_path / experiment['corpus_path']
    if not corpus_dir.exists():
        click.echo(f"Corpus directory {experiment['corpus_path']} not found")
        return
    
    # Create orchestration task for existing infrastructure
    task_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    
    # Hash framework and corpus files
    framework_hash = hash_file(framework_file)
    corpus_hashes = []
    for txt_file in corpus_dir.glob("*.txt"):
        corpus_hashes.append(hash_file(txt_file))
    
    orchestration_task = {
        'task_id': task_id,
        'experiment': experiment,
        'framework_hashes': [framework_hash],
        'corpus_hashes': corpus_hashes,
        'experiment_path': str(exp_path)
    }
    
    # Send to existing orchestrator via Redis
    redis_client = get_redis_client()
    redis_client.xadd('orchestrator.tasks', {'data': json.dumps(orchestration_task)})
    
    click.echo(f"Experiment {experiment['name']} submitted with ID: {task_id}")
    click.echo("Check logs from existing router/orchestrator for progress")

@cli.command()
def status():
    """Show infrastructure status"""
    redis_client = get_redis_client()
    try:
        # Check Redis
        redis_client.ping()
        click.echo("✓ Redis: Connected")
        
        # Check task queue lengths
        orchestrator_len = redis_client.xlen('orchestrator.tasks')
        tasks_len = redis_client.xlen('tasks') if redis_client.exists('tasks') else 0
        
        click.echo(f"  - Orchestrator queue: {orchestrator_len} tasks")
        click.echo(f"  - Worker queue: {tasks_len} tasks")
        
    except Exception as e:
        click.echo(f"✗ Redis: {e}")

if __name__ == '__main__':
    cli() 