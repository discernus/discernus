#!/usr/bin/env python3
"""
Clean V8.0 CLI for Discernus
============================

A focused CLI for v8.0 experiments that bypasses the legacy 3000-line orchestrator
and provides direct access to the v8.0 notebook generation pipeline.

Usage:
    discernus-v8 run [experiment_dir]
    
Features:
- Clean v8.0 orchestration (no legacy synthesis)
- Preserves working analysis stage
- Robust logging and provenance
- Coherence validation
- Direct v8.0 agent execution
"""

import click
import sys
from pathlib import Path
from typing import Optional

# Import v8.0 orchestrator
from discernus.core.v8_orchestrator import V8Orchestrator, V8OrchestrationError


@click.group()
@click.version_option(version='8.0.0', prog_name='Discernus V8.0')
def cli():
    """
    Discernus V8.0 - Clean notebook generation pipeline.
    
    A focused implementation for v8.0 experiments that generates
    statistical analysis notebooks without legacy synthesis complexity.
    """
    pass


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--analysis-model', default='vertex_ai/gemini-2.5-flash',
              help='LLM model for analysis tasks')
@click.option('--synthesis-model', default='vertex_ai/gemini-2.5-pro', 
              help='LLM model for v8.0 agent tasks')
@click.option('--validation-model', default='vertex_ai/gemini-2.5-pro',
              help='LLM model for coherence validation')
@click.option('--skip-validation', is_flag=True, 
              help='Skip experiment coherence validation')
@click.option('--dry-run', is_flag=True,
              help='Show what would be done without executing')
def run(experiment_path: str, 
        analysis_model: str,
        synthesis_model: str, 
        validation_model: str,
        skip_validation: bool,
        dry_run: bool):
    """
    Run a v8.0 experiment to generate statistical analysis notebook.
    
    This command:
    1. Loads v8.0 experiment specifications
    2. Validates experiment coherence (unless skipped)
    3. Runs analysis on corpus documents
    4. Executes v8.0 agents to generate notebook functions
    5. Creates final notebook with statistical analysis
    
    EXPERIMENT_PATH: Path to experiment directory (default: current directory)
    """
    exp_path = Path(experiment_path).resolve()
    
    # Validate experiment directory
    if not (exp_path / "experiment.md").exists():
        click.echo("❌ No experiment.md found. This doesn't appear to be a Discernus experiment directory.")
        sys.exit(1)
    
    # Check for any framework file (experiment agnostic)
    framework_files = [f for f in exp_path.glob("*.md") if f.name != "experiment.md"]
    if not framework_files:
        click.echo("❌ No framework file found (expected .md file other than experiment.md).")
        sys.exit(1)
    
    if not (exp_path / "corpus").exists():
        click.echo("❌ No corpus directory found.")
        sys.exit(1)
    
    # Show configuration
    click.echo("🎯 Discernus V8.0 - Statistical Analysis Pipeline")
    click.echo(f"📁 Experiment: {exp_path.name}")
    click.echo(f"🧠 Analysis Model: {analysis_model}")
    click.echo(f"🔬 V8.0 Agent Model: {synthesis_model}")
    click.echo(f"✅ Validation Model: {validation_model}")
    click.echo(f"🔍 Validation: {'Skipped' if skip_validation else 'Enabled'}")
    
    if dry_run:
        click.echo("\n🏃 DRY RUN: Would execute v8.0 pipeline with above configuration")
        return
    
    try:
        # Initialize v8.0 orchestrator
        orchestrator = V8Orchestrator(exp_path)
        
        # Run experiment
        results = orchestrator.run_experiment(
            analysis_model=analysis_model,
            synthesis_model=synthesis_model,
            validation_model=validation_model,
            skip_validation=skip_validation
        )
        
        # Show results
        click.echo(f"\n✅ V8.0 experiment completed successfully!")
        click.echo(f"📊 Run ID: {results['run_id']}")
        click.echo(f"📄 Documents analyzed: {len(results['analysis_results'])}")
        
        if 'artifacts' in results.get('notebook_results', {}):
            artifacts = results['notebook_results']['artifacts']
            click.echo(f"🔬 Notebook artifacts generated: {len(artifacts)}")
            for artifact in artifacts:
                click.echo(f"   • {artifact}")
        
        click.echo(f"\n🎯 V8.0 statistical analysis notebook ready!")
        
    except V8OrchestrationError as e:
        click.echo(f"❌ V8.0 experiment failed: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n⚠️ Experiment interrupted by user")
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument('experiment_path', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def validate(experiment_path: str):
    """
    Validate experiment coherence for v8.0 specifications.
    
    Runs the coherence validation agent to check:
    - Experiment specification completeness
    - Framework v8.0 compatibility  
    - Corpus structure and content
    - Overall experiment coherence
    """
    exp_path = Path(experiment_path).resolve()
    
    if not (exp_path / "experiment.md").exists():
        click.echo("❌ No experiment.md found.")
        sys.exit(1)
    
    click.echo(f"🔍 Validating experiment: {exp_path.name}")
    
    try:
        from discernus.agents.experiment_coherence_agent import ExperimentCoherenceAgent
        
        validator = ExperimentCoherenceAgent(model="vertex_ai/gemini-2.5-pro")
        result = validator.validate_experiment(exp_path)
        
        # Show results by priority
        blocking = result.get_issues_by_priority("BLOCKING")
        quality = result.get_issues_by_priority("QUALITY") 
        suggestions = result.get_issues_by_priority("SUGGESTION")
        
        if not blocking and not quality and not suggestions:
            click.echo("✅ Experiment validation passed - no issues found!")
            return
        
        if blocking:
            click.echo("\n🚫 BLOCKING Issues (must fix):")
            for issue in blocking:
                click.echo(f"  • {issue.description}")
                click.echo(f"    Fix: {issue.fix}")
        
        if quality:
            click.echo("\n⚠️  QUALITY Issues (should fix):")
            for issue in quality:
                click.echo(f"  • {issue.description}")
                click.echo(f"    Fix: {issue.fix}")
        
        if suggestions:
            click.echo("\n💡 SUGGESTIONS (nice to have):")
            for issue in suggestions:
                click.echo(f"  • {issue.description}")
                click.echo(f"    Fix: {issue.fix}")
        
        if blocking:
            click.echo(f"\n❌ Validation failed: {len(blocking)} blocking issues")
            sys.exit(1)
        else:
            click.echo(f"\n✅ Validation passed with {len(quality + suggestions)} non-blocking issues")
            
    except Exception as e:
        click.echo(f"❌ Validation error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
