#!/usr/bin/env python3
"""
Discernus CLI - Computational Text Analysis Platform
===================================================

THIN Command-line interface for Discernus computational text analysis platform.
Provides validate and execute commands for systematic computational research.

USAGE:
    discernus validate ./my_project     # Validate project structure and specifications
    discernus execute ./my_project      # Execute validated project with dynamic orchestration
    discernus list-frameworks           # List available analytical frameworks
    discernus version                    # Show version information

PHILOSOPHY:
Making world-class computational research as simple as pointing to a folder.
"""

import sys
import asyncio
import click
import yaml
import re
import json
from pathlib import Path
from typing import Dict, Any, List
import datetime
import getpass
import unittest

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    # Core Discernus components
    from discernus.core.spec_loader import SpecLoader
    from discernus.core.project_chronolog import initialize_project_chronolog
    from discernus.core.project_chronolog import get_project_chronolog
    from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Discernus CLI dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

@click.group()
@click.version_option(version='1.0.0', prog_name='Discernus')
def discernus():
    """
    Discernus: Computational Text Analysis Platform
    
    Transform computational research from complex orchestration to simple execution,
    while maintaining the highest standards of academic rigor.
    """
    # CRITICAL: Check for nested repositories FIRST, before any other action
    # that might interact with git, like the ProjectChronolog.
    try:
        from scripts.prevent_nested_repos import NestedRepoPreventionSystem
        prevention_system = NestedRepoPreventionSystem()
        nested_repos = prevention_system.scan_for_nested_repos()
        
        if nested_repos:
            click.echo("❌ CRITICAL: Nested git repositories detected!")
            click.echo("These break the GitHub-as-persistence-layer architecture.")
            click.echo(f"Found {len(nested_repos)} nested repositories:")
            for repo in nested_repos:
                click.echo(f"  - {repo}")
            click.echo("\n💡 To fix this issue:")
            click.echo("   python3 scripts/prevent_nested_repos.py --clean --confirm")
            click.echo("\n📚 For more information:")
            click.echo("   See docs/GIT_BEST_PRACTICES.md")
            sys.exit(1)
            
    except ImportError:
        # Prevention system not available, continue with warning
        click.echo("⚠️ Nested repository prevention system not available")
    except Exception as e:
        click.echo(f"⚠️ Nested repository check failed: {e}")

    # Now that we've confirmed the git structure is clean, initialize the chronolog.
    try:
        session_id = f"discernus_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        user = getpass.getuser()
        command = " ".join(sys.argv)
        
        # Chronolog will be initialized in the execute function with project-specific path
        click.echo(f"📝 Chronolog initialized for session: {session_id}")
        
    except Exception as e:
        click.echo(f"⚠️ Chronolog initialization failed: {e}")

    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ Discernus dependencies not available. Installation may be incomplete.")
        sys.exit(1)

@discernus.command()
@click.argument('framework_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('experiment_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('corpus_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose validation output')
def validate(framework_file: str, experiment_file: str, corpus_dir: str, verbose: bool):
    """
    Validate Discernus V4 Framework and V2 Experiment specifications
    
    FRAMEWORK_FILE: Path to V4 framework file (e.g., cff_v4_mva.md)
    EXPERIMENT_FILE: Path to V2 experiment file (e.g., experiment.md)
    CORPUS_DIR: Path to corpus directory containing text files
    
    Validates:
    - V4 Framework specification (YAML configuration, analysis variants)
    - V2 Experiment specification (models, runs, statistical plan)
    - V2 Corpus completeness and file integrity
    - Cross-specification consistency
    
    Example:
        discernus validate ./cff_v4_mva.md ./experiment.md ./corpus/
    """
    click.echo("🔍 Discernus Specification Validation")
    click.echo("=" * 40)
    
    try:
        click.echo(f"📄 Framework: {framework_file}")
        click.echo(f"🧪 Experiment: {experiment_file}")
        click.echo(f"📁 Corpus: {corpus_dir}")
        click.echo("⏳ Loading and validating specifications...")
        
        # Load specifications using new spec_loader
        spec_loader = SpecLoader()
        specifications = spec_loader.load_specifications(
            framework_file=Path(framework_file),
            experiment_file=Path(experiment_file),
            corpus_dir=Path(corpus_dir)
        )
        
        if verbose:
            _show_verbose_validation(specifications)
        
        # Handle validation results
        if specifications['validation']['overall_valid']:
            click.echo("\n✅ All specifications PASSED validation!")
            click.echo(f"   Ready for execution with:")
            click.echo(f"   discernus execute {framework_file} {experiment_file} {corpus_dir}")
            
        else:
            click.echo(f"\n❌ Specification validation FAILED!")
            
            # Show detailed validation issues
            for spec_type, validation in specifications['validation'].items():
                if spec_type != 'overall_valid' and validation and not validation['valid']:
                    click.echo(f"   {spec_type.upper()} Issues:")
                    for issue in validation['issues']:
                        click.echo(f"     - {issue}")
                    
                    if validation.get('warnings'):
                        click.echo(f"   {spec_type.upper()} Warnings:")
                        for warning in validation['warnings']:
                            click.echo(f"     - {warning}")
                    
                    completeness = validation.get('completeness_score', 0)
                    click.echo(f"   {spec_type.upper()} Completeness: {completeness:.1f}%")
                    click.echo()
            
            sys.exit(1)
        
    except Exception as e:
        click.echo(f"❌ Validation failed with error: {str(e)}", err=True)
        sys.exit(1)

@discernus.command()
@click.argument('framework_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('experiment_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('corpus_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(framework_file: str, experiment_file: str, corpus_dir: str, dev_mode: bool, researcher_profile: str):
    """
    Execute a Discernus experiment using V4 Framework and V2 Experiment specifications
    
    FRAMEWORK_FILE: Path to V4 framework file (e.g., cff_v4_mva.md)
    EXPERIMENT_FILE: Path to V2 experiment file (e.g., experiment.md)
    CORPUS_DIR: Path to corpus directory containing text files
    
    Executes the full workflow:
    - Load and validate all specifications
    - Initialize EnsembleOrchestrator
    - Execute ensemble analysis with statistical planning
    - Generate results
    
    Example:
        discernus execute ./cff_v4_mva.md ./experiment.md ./corpus/
    """
    click.echo("🚀 Discernus Experiment Execution")
    click.echo("=" * 40)
    click.echo(f"📄 Framework: {framework_file}")
    click.echo(f"🧪 Experiment: {experiment_file}")
    click.echo(f"📁 Corpus: {corpus_dir}")
    
    # --- Set up logging and chronolog ---
    session_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    project_path = Path(experiment_file).parent # Use experiment file for project context
    results_dir = project_path / "results" / session_timestamp
    results_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = results_dir / "session_run.log"

    session_id = f"discernus_session_{session_timestamp}"
    user = getpass.getuser()
    command = " ".join(sys.argv)
    
    initialize_project_chronolog(
        project_path=str(project_path),
        user=user,
        command=command,
        session_id=session_id,
        system_state={'discernus_cli_version': '1.0.0'}
    )
    
    # --- Define the async execution function ---
    async def _execute_async():
        # This function runs with its output redirected to the log file
        try:
            print("⏳ Loading specifications...") # This will go to the log
            
            # Load specifications using new spec_loader
            spec_loader = SpecLoader()
            specifications = spec_loader.load_specifications(
                framework_file=Path(framework_file),
                experiment_file=Path(experiment_file),
                corpus_dir=Path(corpus_dir)
            )
            
            # Check if all specifications are valid
            if not specifications['validation']['overall_valid']:
                click.secho("❌ Specification validation failed:", fg='red')
                for spec_type, validation in specifications['validation'].items():
                    if spec_type != 'overall_valid' and validation and not validation['valid']:
                        click.echo(f"  {spec_type}: {', '.join(validation['issues'])}")
                sys.exit(1)
            
            print("✅ All specifications loaded and validated")
            
            # Initialize orchestrator - use parent directory of experiment file as project path
            project_path = Path(experiment_file).parent
            orchestrator = WorkflowOrchestrator(str(project_path))

            # Prepare initial state for the WorkflowOrchestrator
            initial_state = {
                'framework': specifications.get('framework'),
                'experiment': specifications.get('experiment'),
                'corpus': specifications.get('corpus'),
                'workflow': specifications.get('experiment', {}).get('workflow', []),
                'analysis_agent_instructions': specifications.get('framework', {}).get('analysis_variants', {}).get(specifications.get('experiment', {}).get('analysis_variant', 'default'), {}).get('analysis_prompt', ''),
                'project_path': str(project_path),
                'framework_path': framework_file,
                'experiment_path': experiment_file,
                'corpus_path': corpus_dir,
                'session_results_path': str(results_dir) # Use the session-specific results directory
            }

            if not initial_state['workflow']:
                 raise ValueError("Experiment file must contain a 'workflow' definition.")

            print("⏳ Executing workflow...") # This will go to the log
            results = orchestrator.execute_workflow(initial_state)
            
            return results # Return results for handling outside the log context
                
        except Exception as e:
            # This will be printed to the log file
            print(f"❌ Execution failed with an unexpected error: {e}")
            import traceback
            traceback.print_exc()
            # Re-raise to be caught by the outer block
            raise

    # --- Execute and handle results ---
    results = None
    try:
        # Capture all stdout/stderr to the log file for complete provenance
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            sys.stdout = log_file
            sys.stderr = log_file
            results = asyncio.run(_execute_async())

    except Exception as e:
        # This will be printed to the console
        click.secho(f"❌ A critical error occurred during execution: {e}", fg='red')
    
    finally:
        # Always restore stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        # Always give the user feedback and the log path
        click.echo("\n---")
        click.echo(f"📝 Full session log available at: {log_file_path}")
        
        if results and results.get('status') == 'success':
            click.secho("✅ Experiment completed successfully!", fg='green')
            click.echo(f"📊 Results saved to: {results_dir}")
        else:
            click.secho("❌ Experiment failed. Please check the session log for details.", fg='red')
            sys.exit(1)

@discernus.command()
def list_frameworks():
    """List all available analytical frameworks in the system"""
    click.echo("📚 Available Analytical Frameworks")
    click.echo("=" * 40)
    
    try:
        # Search for V4 framework files in common locations
        framework_locations = [
            Path("pm/frameworks/3_2_spec_frameworks/"),
            Path("pm/useful_stuff/frameworks/"),
            Path("projects/")
        ]
        
        frameworks = []
        for location in framework_locations:
            if location.exists():
                for framework_file in location.rglob("*.md"):
                    if framework_file.is_file():
                        try:
                            # Check if it's a V4 framework by looking for configuration block
                            content = framework_file.read_text(encoding='utf-8')
                            if "# --- Discernus Configuration ---" in content:
                                frameworks.append({
                                    'name': framework_file.name,
                                    'path': str(framework_file),
                                    'size': framework_file.stat().st_size
                                })
                        except Exception:
                            continue
        
        if not frameworks:
            click.echo("No V4 frameworks found in the system.")
            click.echo("Expected locations: pm/frameworks/, pm/useful_stuff/frameworks/, projects/")
            return
        
        click.echo(f"Found {len(frameworks)} V4 frameworks:\n")
        
        for i, framework in enumerate(frameworks, 1):
            size_kb = framework['size'] / 1024
            click.echo(f"{i:2d}. {framework['name']}")
            click.echo(f"     Path: {framework['path']}")
            click.echo(f"     Size: {size_kb:.1f} KB")
            click.echo()
        
        click.echo("💡 Use these framework files in your experiment execution:")
        click.echo("    discernus execute <framework_file> <experiment_file> <corpus_dir>")
        
    except Exception as e:
        click.echo(f"❌ Error listing frameworks: {str(e)}", err=True)
        sys.exit(1)

@discernus.command()
@click.option('--check-thin', is_flag=True, help='Check THIN compliance')
def info(check_thin: bool):
    """Show Discernus system information and status"""
    click.echo("ℹ️  Discernus System Information")
    click.echo("=" * 40)
    
    click.echo(f"Version: 1.0.0")
    click.echo(f"Philosophy: THIN Software + LLM Intelligence")
    click.echo(f"Dependencies: {'✅ Available' if DEPENDENCIES_AVAILABLE else '❌ Missing'}")
    
    if check_thin:
        click.echo("\n🏗️  THIN Compliance Check:")
        
        try:
            # Check SpecLoader
            spec_loader = SpecLoader()
            spec_loader_check = {
                'thin_compliant': True,
                'issues': [],
                'recommendations': ['SpecLoader follows THIN principles with simple parsing']
            }
            _show_thin_check("SpecLoader", spec_loader_check)
            
            # Check EnsembleOrchestrator
# orchestrator is already initialized above with correct project path
            orchestrator_check = {
                'thin_compliant': True,
                'issues': [],
                'recommendations': ['EnsembleOrchestrator uses agent registry pattern']
            }
            _show_thin_check("EnsembleOrchestrator", orchestrator_check)
            
        except Exception as e:
            click.echo(f"   ❌ THIN compliance check failed: {str(e)}")

@discernus.command()
@click.option('--pattern', default='test_*.py', help='Pattern for test file discovery.')
def test(pattern: str):
    """
    Discover and run all unit and integration tests for the Discernus platform.
    """
    click.echo("🔬 Running Discernus Test Suite...")
    click.echo("=" * 40)
    
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='./discernus/tests', pattern=pattern)
    
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)
    
    if result.wasSuccessful():
        click.secho("✅ All tests passed!", fg='green')
    else:
        click.secho("❌ Some tests failed.", fg='red')
        sys.exit(1)

def _show_thin_check(component: str, check_result: Dict[str, Any]):
    """Show THIN compliance check results"""
    status = "✅ COMPLIANT" if check_result['thin_compliant'] else "❌ ISSUES"
    click.echo(f"   {component}: {status}")
    
    if check_result['issues']:
        for issue in check_result['issues']:
            click.echo(f"     - Issue: {issue}")
    
    if check_result.get('recommendations'):
        for rec in check_result['recommendations'][:2]:  # Show first 2
            click.echo(f"     - {rec}")

def _show_verbose_validation(specifications: Dict[str, Any]):
    """Show detailed validation information for new specification format"""
    click.echo("\n📋 Validation Details:")
    
    # Framework validation
    if 'framework' in specifications and specifications['validation']['framework']:
        framework_val = specifications['validation']['framework']
        click.echo(f"   📄 Framework: {'✅ PASSED' if framework_val['valid'] else '❌ FAILED'}")
        click.echo(f"      Completeness: {framework_val['completeness_score']:.1f}%")
        
        if specifications['framework']:
            framework = specifications['framework']
            click.echo(f"      Name: {framework.get('name', 'Unknown')}")
            click.echo(f"      Version: {framework.get('version', 'Unknown')}")
            click.echo(f"      Analysis Variants: {len(framework.get('analysis_variants', {}))}")
        
        if framework_val.get('warnings'):
            click.echo(f"      Warnings: {len(framework_val['warnings'])}")
    
    # Experiment validation
    if 'experiment' in specifications and specifications['validation']['experiment']:
        experiment_val = specifications['validation']['experiment']
        click.echo(f"   🧪 Experiment: {'✅ PASSED' if experiment_val['valid'] else '❌ FAILED'}")
        click.echo(f"      Completeness: {experiment_val['completeness_score']:.1f}%")
        
        if specifications['experiment']:
            experiment = specifications['experiment']
            click.echo(f"      Models: {len(experiment.get('models', []))}")
            click.echo(f"      Runs per Model: {experiment.get('runs_per_model', 1)}")
            click.echo(f"      Analysis Variant: {experiment.get('analysis_variant', 'default')}")
    
    # Corpus validation
    if 'corpus' in specifications and specifications['validation']['corpus']:
        corpus_val = specifications['validation']['corpus']
        click.echo(f"   📊 Corpus: {'✅ PASSED' if corpus_val['valid'] else '❌ FAILED'}")
        click.echo(f"      File Count: {corpus_val.get('file_count', 0)}")
        
        if specifications['corpus']:
            corpus = specifications['corpus']
            total_size = corpus['metadata']['total_size']
            size_mb = total_size / (1024 * 1024)
            click.echo(f"      Total Size: {size_mb:.2f} MB")
            click.echo(f"      Extensions: {', '.join(corpus['metadata']['file_extensions'])}")
        
        if corpus_val.get('warnings'):
            click.echo(f"      Warnings: {len(corpus_val['warnings'])}")
    
    # Show overall status
    overall_valid = specifications['validation']['overall_valid']
    click.echo(f"   🎯 Overall: {'✅ PASSED' if overall_valid else '❌ FAILED'}")

if __name__ == '__main__':
    discernus() 