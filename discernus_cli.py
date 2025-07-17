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

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    # Core Discernus components
    from discernus.core.framework_loader import FrameworkLoader
    from discernus.core.project_chronolog import initialize_project_chronolog
    from discernus.core.project_chronolog import get_project_chronolog
    from discernus.agents import ProjectCoherenceAnalyst
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
    # Initialize chronolog here to capture all CLI interactions
    try:
        import datetime
        import getpass
        
        session_id = f"discernus_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        user = getpass.getuser()
        command = " ".join(sys.argv)
        
        # Initialize chronolog for academic provenance
        initialize_project_chronolog(
            project_path=".",  # CLI-level logging
            user=user,
            command=command,
            session_id=session_id,
            system_state={'discernus_cli_version': '1.0.0'}
        )
        click.echo(f"📝 Chronolog initialized for session: {session_id}")
        
    except Exception as e:
        click.echo(f"⚠️ Chronolog initialization failed: {e}")

    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ Discernus dependencies not available. Installation may be incomplete.")
        sys.exit(1)

@discernus.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose validation output')
def validate(project_path: str, verbose: bool):
    """
    Validate Discernus project structure and specifications
    
    PROJECT_PATH: Path to Discernus project directory
    
    Validates:
    - Project structure (framework.md, experiment.md, corpus/)
    - Framework specification using validation rubric v1.0
    - Experiment design using experiment rubric v1.0
    - Corpus completeness and manifest
    - Model health and availability
    
    Example:
        discernus validate ./my_cff_analysis
    """
    click.echo("🔍 Discernus Project Validation")
    click.echo("=" * 40)
    
    async def _validate_async():
        try:
            # Initialize validation agent
            validation_agent = ProjectCoherenceAnalyst()
            
            click.echo(f"📁 Project Path: {project_path}")
            click.echo("⏳ Running comprehensive validation...")
            
            # Run validation
            validation_result = await validation_agent.validate_project(project_path)
            
            if verbose:
                _show_verbose_validation(validation_result)
            
            # Handle results
            if validation_result.get('validation_passed'):
                click.echo("\n✅ Project validation PASSED!")
                click.echo(f"   Ready for execution with 'discernus execute {project_path}'")
                
            else:
                click.echo(f"\n❌ Project validation FAILED!")
                if "feedback" in validation_result:
                    click.echo("   The project is not methodologically sound. The research assistant advises:")
                    click.echo(f"   > {validation_result['feedback']}")
                else:
                    click.echo(f"   Failed at step: {validation_result.get('step_failed', 'Unknown')}")
                    click.echo(f"   Issue: {validation_result.get('message', 'No details provided.')}")
                
                sys.exit(1)
            
        except Exception as e:
            click.echo(f"❌ Validation failed with error: {str(e)}", err=True)
            sys.exit(1)

    asyncio.run(_validate_async())

@discernus.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Execute a validated Discernus project
    
    PROJECT_PATH: Path to validated Discernus project directory
    
    Assumes project has been validated. Executes the full workflow:
    - Parse experiment configuration
    - Initialize WorkflowOrchestrator
    - Execute workflow with statistical planning in-memory
    - Generate results
    
    Example:
        discernus execute ./my_cff_analysis
    """
    click.echo("🚀 Discernus Project Execution")
    click.echo("=" * 40)
    
    async def _execute_async():
        try:
            click.echo(f"📁 Project Path: {project_path}")
            click.echo("⏳ Initializing workflow orchestrator...")
            
            # Initialize orchestrator with project path
            orchestrator = WorkflowOrchestrator(project_path)
            
            # Parse experiment configuration
            experiment_config = _parse_experiment_config(project_path)
            
            # Create initial state for workflow
            initial_state = {
                'project_path': project_path,
                'experiment_config': experiment_config
            }
            
            click.echo("⏳ Executing workflow...")
            results = await orchestrator.execute_workflow(initial_state)
            
            if results.get('status') == 'success':
                click.secho("✅ Experiment completed successfully!", fg='green')
            else:
                click.secho(f"❌ Experiment failed: {results.get('error', 'Unknown error')}", fg='red')
                sys.exit(1)
                
        except Exception as e:
            click.secho(f"❌ Execution failed with an unexpected error: {e}", fg='red')
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    asyncio.run(_execute_async())

@discernus.command()
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
            # Check FrameworkLoader
            framework_loader = FrameworkLoader()
            framework_check = framework_loader.validate_thin_compliance()
            _show_thin_check("FrameworkLoader", framework_check)
            
            # Check ValidationAgent  
            validation_agent = ProjectCoherenceAnalyst()
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

def _parse_experiment_config(project_path: str) -> Dict[str, Any]:
    """
    Parse experiment configuration from experiment.md file.
    """
    experiment_file = Path(project_path) / "experiment.md"
    
    # Default configuration
    default_config = {
        'models': ['openai/gpt-4o'],  # Default to proven working model
        'num_runs': 1,
        'batch_size': 1
    }
    
    if not experiment_file.exists():
        return default_config
    
    try:
        content = experiment_file.read_text()
        
        # Look for YAML configuration blocks
        yaml_pattern = r'```yaml\n(.*?)\n```'
        matches = re.findall(yaml_pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                config = yaml.safe_load(match)
                if isinstance(config, dict):
                    # Merge with defaults
                    default_config.update(config)
                    return default_config
            except yaml.YAMLError:
                continue
                
    except Exception as e:
        click.echo(f"⚠️ Error reading experiment file: {e}")
    
    return default_config

if __name__ == '__main__':
    discernus() 