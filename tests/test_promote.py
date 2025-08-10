#!/usr/bin/env python3

import click
from pathlib import Path

@click.command()
@click.argument('experiment_path')
@click.option('--dry-run', is_flag=True, help='Show what would be promoted without executing')
def promote(experiment_path: str, dry_run: bool):
    """Promote workbench files to operational status"""
    exp_path = Path(experiment_path)
    
    click.echo(f"🔄 Test Promote - Path: {experiment_path}")
    click.echo(f"   Exists: {exp_path.exists()}")
    
    workbench_dir = exp_path / "workbench"
    click.echo(f"   Workbench: {workbench_dir}")
    click.echo(f"   Workbench exists: {workbench_dir.exists()}")
    
    if workbench_dir.exists():
        experiment_files = list(workbench_dir.glob("experiment*.md"))
        click.echo(f"   Found files: {experiment_files}")

if __name__ == '__main__':
    promote()