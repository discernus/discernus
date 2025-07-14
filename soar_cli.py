#!/usr/bin/env python3
"""
SOAR CLI - Simple Atomic Orchestration Research
===============================================

THIN Command-line interface for SOAR (Simple Atomic Orchestration Research).
Provides validate and execute commands for systematic computational research.

USAGE:
    soar validate ./my_project     # Validate project structure and specifications
    soar execute ./my_project      # Execute validated project with dynamic orchestration
    soar list-frameworks           # List available analytical frameworks
    soar version                   # Show version information

PHILOSOPHY:
Making world-class computational research as simple as pointing to a folder.
"""

import sys
import asyncio
import click
from pathlib import Path
from typing import Dict, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    # Core SOAR components
    from discernus.core.framework_loader import FrameworkLoader
    from discernus.core.project_chronolog import initialize_project_chronolog
    from discernus.core.project_chronolog import get_project_chronolog
    from discernus.agents.validation_agent import ValidationAgent
    from discernus.orchestration.ensemble_orchestrator import EnsembleOrchestrator
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ SOAR CLI dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

@click.group()
@click.version_option(version='1.0.0', prog_name='SOAR')
def soar():
    """
    SOAR: Simple Atomic Orchestration Research
    
    Transform computational research from complex orchestration to simple execution,
    while maintaining the highest standards of academic rigor.
    """
    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ SOAR dependencies not available. Installation may be incomplete.")
        sys.exit(1)

@soar.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--interactive', '-i', is_flag=True, help='Interactive issue resolution')
@click.option('--verbose', '-v', is_flag=True, help='Verbose validation output')
def validate(project_path: str, interactive: bool, verbose: bool):
    """
    Validate SOAR project structure and specifications
    
    PROJECT_PATH: Path to SOAR project directory
    
    Validates:
    - Project structure (framework.md, experiment.md, corpus/)
    - Framework specification using validation rubric v1.0
    - Experiment design using experiment rubric v1.0
    - Corpus completeness and manifest
    
    Example:
        soar validate ./my_cff_analysis
    """
    click.echo("🔍 SOAR Project Validation")
    click.echo("=" * 40)
    
    try:
        # Initialize validation agent
        validation_agent = ValidationAgent()
        
        click.echo(f"📁 Project Path: {project_path}")
        click.echo("⏳ Running comprehensive validation...")
        
        # Run validation
        validation_result = validation_agent.validate_project(project_path)
        
        if verbose:
            _show_verbose_validation(validation_result)
        
        # Handle results
        if validation_result['validation_passed']:
            click.echo("\n✅ Project validation PASSED!")
            click.echo(f"   Ready for execution with 'soar execute {project_path}'")
            
            if verbose:
                _show_validation_summary(validation_result)
        else:
            click.echo(f"\n❌ Project validation FAILED!")
            click.echo(f"   Failed at step: {validation_result['step_failed']}")
            click.echo(f"   Issue: {validation_result['message']}")
            
            if interactive:
                # Interactive resolution
                resolution_result = validation_agent.interactive_resolution(validation_result)
                if resolution_result['status'] == 'user_action_required':
                    sys.exit(1)
            else:
                click.echo(f"\n💡 Use 'soar validate {project_path} --interactive' for guided issue resolution")
                sys.exit(1)
        
    except Exception as e:
        click.echo(f"❌ Validation failed with error: {str(e)}", err=True)
        sys.exit(1)

@soar.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Validates and executes a SOAR project with pre-execution confirmation.
    """
    click.echo("🚀 SOAR Project Execution")
    click.echo("=" * 40)
    
    # Initialize project chronolog
    try:
        import datetime
        import getpass
        
        session_id = f"soar_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        user = getpass.getuser()
        command = f"soar execute {project_path}"
        if dev_mode:
            command += " --dev-mode"
        if researcher_profile != 'experienced_computational_social_scientist':
            command += f" --researcher-profile {researcher_profile}"
        
        initialize_project_chronolog(
            project_path=project_path,
            user=user,
            command=command,
            session_id=session_id,
            system_state={
                'soar_cli_version': '2.0',
                'dev_mode': dev_mode,
                'researcher_profile': researcher_profile
            }
        )
        click.echo(f"📝 Project chronolog initialized: {session_id}")
        
    except Exception as e:
        click.echo(f"⚠️ ProjectChronolog initialization failed: {e}")
    
    try:
        # Step 1: Always validate the project first
        click.echo("🔬 Phase 1: Comprehensive Project Validation...")
        validation_agent = ValidationAgent()
        validation_result = validation_agent.validate_project(project_path)
        
        # Check for transient API errors first
        if validation_result.get('error_type') == 'LLM_VALIDATION_FAILED':
            click.secho(f"\n⚠️  Validation Halted: {validation_result.get('message', 'An unexpected error occurred during LLM validation.')}", fg='yellow')
            click.echo("    This could be a temporary issue with the provider, a problem with your API key, or an issue with the prompt.")
            click.echo("    Please review the error details and decide whether to retry the command or investigate your configuration.")
            sys.exit(1)

        if not validation_result.get('validation_passed'):
            click.secho(f"\n❌ Validation FAILED: {validation_result.get('message', 'Unknown error.')}", fg='red')
            click.echo("   Please run 'soar validate' to diagnose and fix the issues in your project files.")
            sys.exit(1)
        
        click.secho("✅ Validation PASSED.", fg='green')

        # Step 2: Pre-Execution Confirmation
        click.echo("\n📋 Phase 2: Pre-Execution Confirmation")
        summary = validation_agent.get_pre_execution_summary(validation_result)
        
        click.echo("Please review the execution plan:")
        for key, value in summary.items():
            click.echo(f"   - {key}: {value}")
        
        if not click.confirm('\nProceed with execution?', default=False):
            click.echo("Execution cancelled by user.")
            sys.exit(0)

        # Step 3: Execute analysis
        click.echo("\n🚀 Phase 3: Executing Analysis...")
        ensemble_orchestrator = EnsembleOrchestrator(project_path)
        results = asyncio.run(ensemble_orchestrator.execute_ensemble_analysis(validation_result))
        
        click.secho(f"\n🎉 Execution Completed: {results.get('status', 'Unknown')}", fg='green')
        
    except Exception as e:
        click.secho(f"❌ Execution failed with error: {str(e)}", fg='red', err=True)
        if dev_mode:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def _generate_experiment_config(project_path: str):
    """Generates the experiment config YAML if it doesn't exist."""
    click.echo("🚀 Phase 1: Configuring experiment from natural language...")
    try:
        from discernus.agents.ensemble_configuration_agent import EnsembleConfigurationAgent
        config_agent = EnsembleConfigurationAgent()
        config_agent.generate_configuration(str(Path(project_path) / "experiment.md"))
        click.echo("✅ Experiment configuration complete.")
    except ImportError:
        click.echo("⚠️ Could not import EnsembleConfigurationAgent. Skipping config generation.")
    except Exception as e:
        click.echo(f"⚠️ Failed to generate experiment configuration: {e}")

@soar.command()
def list_frameworks():
    """List all available analytical frameworks in the system"""
    click.echo("📚 Available Analytical Frameworks")
    click.echo("=" * 40)
    
    try:
        framework_loader = FrameworkLoader()
        frameworks = framework_loader.get_available_frameworks()
        
        if not frameworks:
            click.echo("No frameworks found in the system.")
            return
        
        click.echo(f"Found {len(frameworks)} frameworks:\n")
        
        for i, framework in enumerate(frameworks, 1):
            click.echo(f"{i:2d}. {framework}")
            
            # Try to load framework info
            context = framework_loader.load_framework_context(framework)
            if context['status'] == 'success':
                size_kb = context['file_size'] / 1024
                click.echo(f"     Path: {context['framework_path']}")
                click.echo(f"     Size: {size_kb:.1f} KB")
            click.echo()
        
        click.echo("💡 Use these framework names in your project's framework.md file")
        
    except Exception as e:
        click.echo(f"❌ Error listing frameworks: {str(e)}", err=True)
        sys.exit(1)

@soar.command()
@click.option('--check-thin', is_flag=True, help='Check THIN compliance')
def info(check_thin: bool):
    """Show SOAR system information and status"""
    click.echo("ℹ️  SOAR System Information")
    click.echo("=" * 40)
    
    click.echo(f"Version: 1.0.0")
    click.echo(f"Philosophy: THIN Software + LLM Intelligence")
    click.echo(f"Dependencies: {'✅ Available' if DEPENDENCIES_AVAILABLE else '❌ Missing'}")
    
    if check_thin:
        click.echo("\n🏗️  THIN Compliance Check:")
        
        try:
            # Check FrameworkLoader
            framework_loader = FrameworkLoader()
            framework_check = framework_loader.validate_thin_compliance()
            _show_thin_check("FrameworkLoader", framework_check)
            
            # Check ValidationAgent  
            validation_agent = ValidationAgent()
            validation_check = validation_agent.validate_thin_compliance()
            _show_thin_check("ValidationAgent", validation_check)
            
        except Exception as e:
            click.echo(f"   ❌ THIN compliance check failed: {str(e)}")

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

def _show_verbose_validation(validation_result: Dict[str, Any]):
    """Show detailed validation information"""
    click.echo("\n📋 Validation Details:")
    
    # Structure validation
    if 'structure_result' in validation_result:
        structure = validation_result['structure_result']
        click.echo(f"   📁 Structure: {'✅ PASSED' if structure['validation_passed'] else '❌ FAILED'}")
        if structure.get('found_files'):
            for file_name in structure['found_files']:
                click.echo(f"      ✓ {file_name}")
    
    # Framework validation
    if 'framework_result' in validation_result:
        framework = validation_result['framework_result']
        click.echo(f"   🔬 Framework: {'✅ PASSED' if framework['validation_passed'] else '❌ FAILED'}")
        if 'completeness_percentage' in framework:
            click.echo(f"      Completeness: {framework['completeness_percentage']}%")
    
    # Experiment validation
    if 'experiment_result' in validation_result:
        experiment = validation_result['experiment_result']
        click.echo(f"   🧪 Experiment: {'✅ PASSED' if experiment['validation_passed'] else '❌ FAILED'}")
        if 'completeness_percentage' in experiment:
            click.echo(f"      Completeness: {experiment['completeness_percentage']}%")
    
    # Corpus validation
    if 'corpus_result' in validation_result:
        corpus = validation_result['corpus_result']
        click.echo(f"   📊 Corpus: {'✅ PASSED' if corpus['validation_passed'] else '❌ FAILED'}")
        if 'file_count' in corpus:
            click.echo(f"      Files: {corpus['file_count']}")

def _show_validation_summary(validation_result: Dict[str, Any]):
    """Show validation summary"""
    click.echo(f"\n📊 Validation Summary:")
    click.echo(f"   Project: {Path(validation_result['project_path']).name}")
    click.echo(f"   Timestamp: {validation_result.get('validation_timestamp', 'Unknown')}")
    click.echo(f"   Ready for execution: {'✅ Yes' if validation_result['ready_for_execution'] else '❌ No'}")

# Removed deprecated _load_project_components function - ValidationAgent handles this now

# Removed deprecated _execute_orchestration function - using EnsembleOrchestrator now

if __name__ == '__main__':
    soar() 