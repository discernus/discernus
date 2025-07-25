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
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

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
    (run_folder / "results" / "batch_analysis").mkdir(parents=True, exist_ok=True)
    (run_folder / "results" / "synthesis").mkdir(parents=True, exist_ok=True)
    (run_folder / "results" / "reports").mkdir(parents=True, exist_ok=True)
    
    return run_folder

def create_run_manifest(run_folder: Path, experiment: Dict[str, Any], 
                       framework_hash: str, corpus_hashes: List[str], 
                       experiment_path: Path) -> Dict[str, Any]:
    """Create complete run manifest with all provenance data"""
    manifest = {
        "run_metadata": {
            "run_id": run_folder.name,
            "experiment_name": experiment.get('name', 'Unknown'),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "experiment_path": str(experiment_path),
            "discernus_version": "alpha_v1.0"
        },
        "experiment_config": experiment,
        "asset_hashes": {
            "framework_hash": f"sha256:{framework_hash}",
            "corpus_hashes": [f"sha256:{h}" for h in corpus_hashes],
            "experiment_config_hash": f"sha256:{hashlib.sha256(json.dumps(experiment, sort_keys=True).encode()).hexdigest()}"
        },
        "agent_prompts": {},  # Will be populated as agents run
        "processing_stages": {
            "validation": {"status": "completed", "timestamp": datetime.utcnow().isoformat() + "Z"},
            "run_setup": {"status": "completed", "timestamp": datetime.utcnow().isoformat() + "Z"},
            "batch_analysis": {"status": "pending"},
            "synthesis": {"status": "pending"},
            "report_generation": {"status": "pending"}
        },
        "cost_tracking": {
            "estimated_cost_usd": 0.0,
            "actual_cost_usd": 0.0
        }
    }
    
    # Save manifest
    manifest_path = run_folder / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    click.echo(f"📋 Created run manifest: {manifest_path}")
    return manifest

def validate_experiment_structure(exp_path: Path):
    """Enhanced validation with detailed error reporting"""
    # Check experiment.md exists
    exp_file = exp_path / 'experiment.md'
    if not exp_file.exists():
        return False, "❌ experiment.md not found", {}
    
    # Parse experiment configuration
    try:
        with open(exp_file) as f:
            content = f.read()
            # Extract YAML from markdown
            if '---' in content:
                parts = content.split('---')
                if len(parts) >= 2:
                    yaml_content = parts[1].strip()
                else:
                    yaml_content = parts[0].strip()
            else:
                yaml_content = content
            experiment = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return False, f"❌ Invalid YAML in experiment.md: {e}", {}
    except Exception as e:
        return False, f"❌ Error parsing experiment.md: {e}", {}
    
    # Validate required fields
    required_fields = ['name', 'framework', 'corpus_path']
    missing_fields = [field for field in required_fields if field not in experiment]
    if missing_fields:
        return False, f"❌ Missing required fields: {', '.join(missing_fields)}", {}
    
    # Validate framework exists
    framework_file = exp_path / experiment['framework']
    if not framework_file.exists():
        return False, f"❌ Framework file {experiment['framework']} not found", {}
    
    # Validate corpus directory
    corpus_dir = exp_path / experiment['corpus_path']
    if not corpus_dir.exists():
        return False, f"❌ Corpus directory {experiment['corpus_path']} not found", {}
    
    # Count and validate corpus files
    corpus_files = []
    try:
        for txt_file in corpus_dir.iterdir():
            if txt_file.is_file() and txt_file.suffix == '.txt':
                corpus_files.append(txt_file)
        if not corpus_files:
            return False, f"❌ No .txt files found in {experiment['corpus_path']}", {}
    except Exception as e:
        return False, f"❌ Error reading corpus directory: {str(e)}", {}
    
    # Check for corpus manifest (recommended)
    corpus_manifest = corpus_dir / "corpus.md"
    if not corpus_manifest.exists():
        pass  # Don't print warning during list operation to avoid click confusion
    
    return True, "✅ Validation passed", experiment

@click.group()
def cli():
    """Discernus - Computational Social Science Research Platform"""
    pass

@cli.command()
def list():
    """List available experiments with enhanced information"""
    projects_dir = Path('projects')
    if not projects_dir.exists():
        click.echo("❌ No projects directory found")
        return
    
    experiments = []
    for p in projects_dir.iterdir():
        if p.is_dir() and (p / 'experiment.md').exists():
            # Get basic experiment info
            valid, msg, exp_config = validate_experiment_structure(p)
            if valid:
                corpus_dir = p / exp_config.get('corpus_path', 'corpus')
                corpus_count = len([f for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']) if corpus_dir.exists() else 0
            else:
                corpus_count = 0
            
            experiments.append({
                'name': p.name,
                'path': str(p),
                'valid': valid,
                'title': exp_config.get('name', 'Untitled') if valid else 'Invalid',
                'corpus_count': corpus_count
            })
    
    if experiments:
        click.echo("📚 Available experiments:")
        for exp in experiments:
            status_icon = "✅" if exp['valid'] else "❌"
            click.echo(f"  {status_icon} {exp['name']}")
            click.echo(f"     Title: {exp['title']}")
            if exp['valid']:
                click.echo(f"     Corpus: {exp['corpus_count']} documents")
            click.echo(f"     Path: {exp['path']}")
            
        click.echo(f"\n📊 Summary: {len([e for e in experiments if e['valid']])} valid, {len([e for e in experiments if not e['valid']])} invalid")
    else:
        click.echo("❌ No experiments found")

@cli.command()
@click.argument('experiment_path')
def validate(experiment_path: str):
    """Enhanced experiment validation with detailed feedback"""
    exp_path = Path(experiment_path)
    if not exp_path.exists():
        click.echo(f"❌ Experiment path {experiment_path} does not exist")
        return
    
    click.echo(f"🔍 Validating experiment: {experiment_path}")
    
    valid, message, experiment = validate_experiment_structure(exp_path)
    
    if not valid:
        click.echo(message)
        return
    
    click.echo(message)
    click.echo(f"   📝 Name: {experiment.get('name', 'Untitled')}")
    click.echo(f"   🧠 Framework: {experiment['framework']}")
    
    # Show corpus details
    corpus_dir = exp_path / experiment['corpus_path']
    corpus_files = [f for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']
    click.echo(f"   📄 Corpus: {len(corpus_files)} documents")
    
    # Show file sizes
    total_size = sum(f.stat().st_size for f in corpus_files)
    click.echo(f"   💾 Total size: {total_size / 1024:.1f} KB")
    
    # Check for recent runs
    runs_dir = exp_path / "runs"
    if runs_dir.exists():
        recent_runs = sorted([d for d in runs_dir.iterdir() if d.is_dir()], key=lambda x: x.stat().st_mtime, reverse=True)[:3]
        if recent_runs:
            total_runs = len([d for d in runs_dir.iterdir() if d.is_dir()])
            click.echo(f"   🕒 Recent runs: {total_runs} total, latest: {recent_runs[0].name}")

@cli.command()
@click.argument('experiment_path')
@click.option('--dry-run', is_flag=True, help='Show what would be done without executing')
def run(experiment_path: str, dry_run: bool):
    """Execute experiment with enhanced progress tracking"""
    exp_path = Path(experiment_path)
    
    click.echo(f"🚀 Starting experiment execution: {experiment_path}")
    
    # Enhanced validation
    valid, message, experiment = validate_experiment_structure(exp_path)
    if not valid:
        click.echo(message)
        return
    
    click.echo("✅ Validation passed")
    
    if dry_run:
        click.echo("🧪 DRY RUN MODE - No actual execution")
        click.echo(f"   Would create run folder in: {exp_path / 'runs'}")
        corpus_dir = exp_path / experiment['corpus_path']
        corpus_count = len([f for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']) if corpus_dir.exists() else 0
        click.echo(f"   Would process {corpus_count} documents")
        click.echo(f"   Would use framework: {experiment['framework']}")
        return
    
    # Create run folder with enhanced structure
    run_folder = create_run_folder(exp_path)
    click.echo(f"📁 Created run folder: {run_folder}")
    
    # Generate comprehensive asset hashes
    click.echo("🔐 Generating provenance hashes...")
    framework_file = exp_path / experiment['framework']
    framework_hash = hash_file(framework_file)
    
    corpus_dir = exp_path / experiment['corpus_path']
    corpus_hashes = []
    corpus_files = [f for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']
    
    with click.progressbar(corpus_files, label='Hashing corpus files') as files:
        for txt_file in files:
            corpus_hashes.append(hash_file(txt_file))
    
    # Create comprehensive manifest
    manifest = create_run_manifest(run_folder, experiment, framework_hash, corpus_hashes, exp_path)
    
    # Create orchestration task for Redis list coordination (per architecture spec 4.2)
    task_id = run_folder.name
    orchestration_task = {
        'task_id': task_id,
        'experiment': experiment,
        'framework_hashes': [framework_hash],  # FIXED: Make plural as expected by OrchestratorAgent
        'corpus_hashes': corpus_hashes,
        'experiment_path': str(exp_path),
        'run_folder': str(run_folder),
        'manifest_path': str(run_folder / "manifest.json")
    }
    
    # Submit to orchestrator via Redis list (no streams, no consumer groups per architecture 4.2)
    click.echo("📡 Submitting to Redis orchestration...")
    redis_client = get_redis_client()
    
    try:
        # Use LPUSH to orchestrator list instead of XADD to stream
        redis_client.lpush('orchestrator.tasks', json.dumps(orchestration_task))
        
        click.echo("✅ Experiment submitted successfully!")
        click.echo(f"   🆔 Task ID: {task_id}")  
        click.echo(f"   📂 Run folder: {run_folder}")
        click.echo(f"   📊 Processing: {len(corpus_files)} documents")
        click.echo("\n🔄 Experiment processing started...")
        click.echo("   💡 Use 'discernus status' to monitor progress")
        click.echo(f"   💡 Use 'discernus status {task_id}' for specific run details")
        
    except Exception as e:
        click.echo(f"❌ Failed to submit experiment: {e}")
        return

@cli.command()
@click.argument('run_id', required=False)
@click.option('--watch', is_flag=True, help='Watch status continuously')
def status(run_id: Optional[str] = None, watch: bool = False):
    """Enhanced status monitoring with run details"""
    redis_client = get_redis_client()
    
    def show_status():
        try:
            # Check Redis connection
            redis_client.ping()
            click.echo("✅ Redis: Connected")
            
            # Check infrastructure queues (using llen for lists per architecture spec 4.2)
            orchestrator_len = redis_client.llen('orchestrator.tasks') if redis_client.exists('orchestrator.tasks') else 0
            tasks_len = redis_client.llen('tasks') if redis_client.exists('tasks') else 0
            done_len = redis_client.llen('tasks.done') if redis_client.exists('tasks.done') else 0
            error_len = redis_client.llen('tasks.error') if redis_client.exists('tasks.error') else 0
            
            click.echo("📊 Infrastructure Status:")
            click.echo(f"   📥 Orchestrator queue: {orchestrator_len} tasks")
            click.echo(f"   ⚙️  Worker queue: {tasks_len} tasks")  
            click.echo(f"   ✅ Completed: {done_len} tasks")
            if error_len > 0:
                click.echo(f"   ❌ Errors: {error_len} tasks")
            
            if run_id:
                click.echo(f"\n🔍 Run Status: {run_id}")
                
                # Check for run completion signals
                run_status = redis_client.get(f"task:{run_id}:status")
                if run_status:
                    click.echo(f"   Status: {run_status}")
                    
                # Check for result hashes
                result_hash = redis_client.get(f"task:{run_id}:result_hash")
                if result_hash:
                    click.echo(f"   📄 Result: {result_hash[:12]}...")
                    
                # Check run folder if it exists
                found_run = False
                projects_path = Path('projects')
                if projects_path.exists():
                    for proj_dir in projects_path.iterdir():
                        if proj_dir.is_dir():
                            runs_dir = proj_dir / 'runs'
                            if runs_dir.exists():
                                run_folder = runs_dir / run_id
                                if run_folder.exists():
                                    click.echo(f"   📁 Folder: {run_folder}")
                                    found_run = True
                                    
                                    # Check manifest
                                    manifest_file = run_folder / "manifest.json"
                                    if manifest_file.exists():
                                        with open(manifest_file) as f:
                                            manifest = json.load(f)
                                        
                                        click.echo("   📋 Processing Stages:")
                                        for stage, info in manifest.get('processing_stages', {}).items():
                                            status_icon = {"completed": "✅", "pending": "⏳", "in_progress": "🔄", "failed": "❌"}.get(info.get('status'), "❓")
                                            click.echo(f"      {status_icon} {stage.replace('_', ' ').title()}: {info.get('status', 'unknown')}")
                                    
                                    break
                
                if not found_run:
                    click.echo(f"   ❓ Run folder not found for {run_id}")
            
        except Exception as e:
            click.echo(f"❌ Redis connection failed: {e}")
    
    if watch:
        click.echo("👀 Watching status (Ctrl+C to stop)...")
        try:
            while True:
                click.clear()
                show_status()
                time.sleep(2)
        except KeyboardInterrupt:
            click.echo("\n👋 Status monitoring stopped")
    else:
        show_status()

def main():
    """Entry point for CLI"""
    cli()

if __name__ == '__main__':
    main() 