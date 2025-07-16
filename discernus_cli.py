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
import litellm
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
    from discernus.orchestration.ensemble_orchestrator import EnsembleOrchestrator
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
        
        # This is a global initialization, so project_path is not yet known.
        # We can log to a general system log or handle this differently later.
        # For now, let's just print that we would be logging.
        # initialize_project_chronolog(
        #     project_path=".", # General log
        #     user=user,
        #     command=command,
        #     session_id=session_id,
        #     system_state={'discernus_cli_version': '2.0'}
        # )
        # click.echo(f"📝 Global chronolog initialized for session: {session_id}")
        
    except Exception as e:
        click.echo(f"⚠️ Global Chronolog initialization failed: {e}")

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
            if validation_result['validation_passed']:
                click.echo("\n✅ Project validation PASSED!")
                click.echo(f"   Ready for execution with 'discernus execute {project_path}'")
                
                if verbose:
                    _show_validation_summary(validation_result)
            else:
                click.echo(f"\n❌ Project validation FAILED!")
                click.echo(f"   Failed at step: {validation_result['step_failed']}")
                click.echo(f"   Issue: {validation_result['message']}")
                
                click.echo(f"\n💡 Use 'discernus validate {project_path} --interactive' for guided issue resolution")
                sys.exit(1)
            
        except Exception as e:
            click.echo(f"❌ Validation failed with error: {str(e)}", err=True)
            sys.exit(1)

    asyncio.run(_validate_async())

def _execute_wrapper(project_path: str, dev_mode: bool, researcher_profile: str):
    """Wrapper to run the async execute function."""
    return asyncio.run(_execute_async(project_path, dev_mode, researcher_profile))

async def _execute_async(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Async implementation of the execute function with model health verification.
    """
    click.echo("🚀 Discernus Project Execution")
    click.echo("=" * 40)
    
    try:
        # Phase 1: Project Validation
        click.echo("\n🔬 Phase 1: Comprehensive Project Validation...")
        validation_agent = ProjectCoherenceAnalyst()
        validation_result = await validation_agent.validate_project(project_path)
        
        if not validation_result.get('validation_passed'):
            click.secho(f"\n❌ Validation FAILED: {validation_result.get('message', 'Unknown error.')}", fg='red')
            click.echo("   Please run 'discernus validate' to diagnose and fix the issues in your project files.")
            sys.exit(1)
        
        click.secho("✅ Validation PASSED.", fg='green')
        
        # Phase 2: Pre-Execution Confirmation
        click.echo("\n📋 Phase 2: Pre-Execution Confirmation")
        summary = validation_agent.get_pre_execution_summary(validation_result)
        
        click.echo("Please review the execution plan:")
        for key, value in summary.items():
            click.echo(f"   {key}: {value}")
        
        if not click.confirm("\nProceed with execution?"):
            click.echo("Execution cancelled by user.")
            sys.exit(0)
        
        # Phase 3: Execute the project
        click.echo("\n🚀 Phase 3: Project Execution")
        orchestrator = EnsembleOrchestrator(project_path)
        
        # Run the experiment
        results = await orchestrator.execute_ensemble_analysis(validation_result)
        
        if results.get('status') == 'success':
            click.secho("✅ Experiment completed successfully!", fg='green')
        else:
            click.secho("❌ Experiment failed.", fg='red')
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Execution failed: {e}")
        sys.exit(1)

# Update the click command to use the wrapper
@discernus.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Validates and executes a Discernus project with pre-execution confirmation.
    """
    _execute_wrapper(project_path, dev_mode, researcher_profile)

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

def _show_validation_summary(validation_result: Dict[str, Any]):
    """Show validation summary"""
    click.echo(f"\n📊 Validation Summary:")
    click.echo(f"   Project: {Path(validation_result['project_path']).name}")
    click.echo(f"   Timestamp: {validation_result.get('validation_timestamp', 'Unknown')}")
    click.echo(f"   Ready for execution: {'✅ Yes' if validation_result['ready_for_execution'] else '❌ No'}")

def _apply_model_health_adjustments(validation_result: Dict[str, Any], adjusted_models: List[str]) -> Dict[str, Any]:
    """
    THIN implementation: Apply agent's model health recommendations to experiment configuration.
    
    Args:
        validation_result: The validation result containing project path
        adjusted_models: List of healthy models recommended by the agent
    
    Returns:
        Updated validation result (the actual experiment.md file is updated)
    """
    if not adjusted_models:
        return validation_result
    
    # Get the project path from validation result
    project_path = validation_result.get('project_path')
    if not project_path:
        click.echo("⚠️ No project path found in validation result")
        return validation_result
    
    # Read the experiment.md file directly
    experiment_file = Path(project_path) / "experiment.md"
    if not experiment_file.exists():
        click.echo("⚠️ Experiment file not found")
        return validation_result
    
    try:
        experiment_content = experiment_file.read_text()
        
        # Replace the models in the YAML configuration
        yaml_pattern = r'```yaml\n(.*?)\n```'
        yaml_match = re.search(yaml_pattern, experiment_content, re.DOTALL)
        
        if yaml_match:
            # Parse existing YAML and update models
            try:
                existing_config = yaml.safe_load(yaml_match.group(1))
                if isinstance(existing_config, dict):
                    existing_config['models'] = adjusted_models
                    
                    # Generate new YAML block
                    new_yaml = yaml.dump(existing_config, default_flow_style=False)
                    new_yaml_block = f"```yaml\n{new_yaml}```"
                    
                    # Replace the YAML block in the experiment content
                    updated_content = re.sub(yaml_pattern, new_yaml_block, experiment_content, flags=re.DOTALL)
                    
                    # Write the updated content back to the file
                    experiment_file.write_text(updated_content)
                    
                    click.echo(f"   ✅ Updated experiment.md with adjusted models")
                    
            except yaml.YAMLError as e:
                click.echo(f"⚠️ Error updating YAML configuration: {e}")
        else:
            # If no YAML block exists, add one
            yaml_block = f"\n```yaml\nmodels: {adjusted_models}\n```\n"
            updated_content = experiment_content + yaml_block
            experiment_file.write_text(updated_content)
            click.echo(f"   ✅ Added YAML configuration to experiment.md")
    
    except Exception as e:
        click.echo(f"⚠️ Error updating experiment file: {e}")
    
    return validation_result

def _extract_models_from_experiment(project_path: str) -> List[str]:
    """
    Extract the list of models from the experiment.md file.
    """
    experiment_file = Path(project_path) / "experiment.md"
    
    if not experiment_file.exists():
        return []
    
    try:
        content = experiment_file.read_text()
        
        # Look for YAML configuration blocks
        yaml_pattern = r'```yaml\n(.*?)\n```'
        matches = re.findall(yaml_pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                config = yaml.safe_load(match)
                if isinstance(config, dict) and 'models' in config:
                    return config['models']
            except yaml.YAMLError:
                continue
        
        # Fallback: look for models listed in text
        model_pattern = r'(?:models?|LLMs?):\s*\n((?:\s*[-*]\s*.+\n)*)'
        matches = re.findall(model_pattern, content, re.IGNORECASE)
        
        for match in matches:
            models = []
            for line in match.split('\n'):
                line = line.strip()
                if line.startswith(('-', '*')):
                    model = line[1:].strip()
                    if model:
                        models.append(model)
            if models:
                return models
                
    except Exception as e:
        click.echo(f"⚠️ Error reading experiment file: {e}")
    
    return []

if __name__ == '__main__':
    discernus() 