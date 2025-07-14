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
import yaml
import re
import litellm
from pathlib import Path
from typing import Dict, Any, List

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
    from discernus.gateway.model_registry import ModelRegistry
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

def _execute_wrapper(project_path: str, dev_mode: bool, researcher_profile: str):
    """Wrapper to run the async execute function."""
    return asyncio.run(_execute_async(project_path, dev_mode, researcher_profile))

async def _execute_async(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Async implementation of the execute function with model health verification.
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
        # Phase 0: Global Model Health Check
        click.echo("🔍 Phase 0: Global Model Health Check...")
        
        # Check all models in the registry
        model_registry = ModelRegistry()
        all_models = list(model_registry.models.keys())
        
        click.echo(f"   Checking {len(all_models)} models in registry...")
        global_health_results = await _verify_model_health(all_models)
        
        if global_health_results["all_healthy"]:
            click.secho(f"✅ All {global_health_results['total_models']} models are healthy.", fg='green')
        else:
            click.secho(f"⚠️  {len(global_health_results['failed_models'])} of {global_health_results['total_models']} models have issues:", fg='yellow')
            for model in global_health_results['failed_models']:
                error_msg = global_health_results['results'][model]['message']
                click.echo(f"   • {model}: {error_msg}")
            
            click.echo(f"   ✅ {global_health_results['healthy_models']} models are working correctly.")
        
        # Phase 1: Project Validation (now with model health context)
        click.echo("\n🔬 Phase 1: Comprehensive Project Validation...")
        validation_agent = ValidationAgent()
        
        # TODO: In future, could pass model health context to validation agent
        # For now, the global health check provides valuable up-front feedback
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
        
        # Phase 2: Experiment-Specific Model Verification
        click.echo("\n🎯 Phase 2: Experiment-Specific Model Verification...")
        
        # Extract models from experiment configuration
        required_models = _extract_models_from_experiment(project_path)
        
        if required_models:
            click.echo(f"   Experiment requires: {', '.join(required_models)}")
            
            # Check if any required models failed global health check
            failed_required = [model for model in required_models if model in global_health_results['failed_models']]
            
            if failed_required:
                click.secho(f"⚠️  {len(failed_required)} required models have health issues:", fg='yellow')
                for model in failed_required:
                    error_msg = global_health_results['results'][model]['message']
                    click.echo(f"   • {model}: {error_msg}")
                
                # Use EnsembleConfigurationAgent for intelligent recommendation
                click.echo("\n🤖 Consulting EnsembleConfigurationAgent for recommendation...")
                
                try:
                    from discernus.agents.ensemble_configuration_agent import EnsembleConfigurationAgent
                    config_agent = EnsembleConfigurationAgent()
                    
                    # Prepare context for the agent
                    situation_context = {
                        'required_models': required_models,
                        'failed_models': failed_required,
                        'healthy_models': [model for model, result in global_health_results['results'].items() 
                                         if result['status'] == 'success'],
                        'health_results': global_health_results,
                        'project_path': project_path
                    }
                    
                    # Get intelligent recommendation
                    recommendation = config_agent.assess_model_health_situation(situation_context)
                    
                    # Present the agent's recommendation
                    click.echo(f"\n💡 Agent Recommendation: {recommendation.get('action', 'Unknown')}")
                    click.echo(f"   {recommendation.get('explanation', 'No explanation provided')}")
                    
                    if recommendation.get('adjusted_models'):
                        click.echo(f"   Suggested models: {', '.join(recommendation['adjusted_models'])}")
                    
                    # Simple confirmation based on agent's recommendation
                    if recommendation.get('action') == 'proceed':
                        if not click.confirm(f"\nProceed with agent's recommendation?"):
                            click.echo("Execution cancelled.")
                            sys.exit(1)
                    elif recommendation.get('action') == 'cancel':
                        click.echo("Agent recommends cancelling. Please address the model issues first.")
                        sys.exit(1)
                    else:
                        # For other recommendations, ask user to decide
                        if not click.confirm(f"\nFollow agent's recommendation?"):
                            click.echo("Execution cancelled.")
                            sys.exit(1)
                    
                    # THIN Implementation: Apply agent's recommendations to experiment configuration
                    if recommendation.get('adjusted_models'):
                        click.echo(f"\n🔧 Applying agent's model adjustments...")
                        validation_result = _apply_model_health_adjustments(
                            validation_result, 
                            recommendation['adjusted_models']
                        )
                        click.echo(f"   Updated models: {', '.join(recommendation['adjusted_models'])}")
                        
                        # CRITICAL: Re-run validation to get updated model configuration
                        click.echo("   🔄 Re-running validation with adjusted models...")
                        validation_result = validation_agent.validate_project(project_path)
                        
                        if not validation_result.get('validation_passed'):
                            click.secho(f"❌ Re-validation failed: {validation_result.get('message')}", fg='red')
                            sys.exit(1)
                        
                    # Update status message
                    click.secho("✅ Model health issues resolved with agent recommendations.", fg='green')
                            
                except ImportError:
                    click.echo("⚠️  EnsembleConfigurationAgent not available. Using fallback logic.")
                    if not click.confirm("\nDo you want to continue despite model health issues?"):
                        click.echo("Execution cancelled.")
                        sys.exit(1)
                except Exception as e:
                    click.echo(f"⚠️  Error consulting agent: {e}")
                    if not click.confirm("\nDo you want to continue despite model health issues?"):
                        click.echo("Execution cancelled.")
                        sys.exit(1)
            else:
                click.secho(f"✅ All required models are healthy.", fg='green')
        else:
            click.echo("   No specific models found in experiment configuration.")

        # Phase 3: Pre-Execution Confirmation
        click.echo("\n📋 Phase 3: Pre-Execution Confirmation")
        summary = validation_agent.get_pre_execution_summary(validation_result)
        
        click.echo("Please review the execution plan:")
        for key, value in summary.items():
            click.echo(f"   {key}: {value}")
        
        if not click.confirm("\nProceed with execution?"):
            click.echo("Execution cancelled by user.")
            sys.exit(0)
        
        # Phase 4: Execute the project
        click.echo("\n🚀 Phase 4: Project Execution")
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
@soar.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(project_path: str, dev_mode: bool, researcher_profile: str):
    """
    Validates and executes a SOAR project with pre-execution confirmation.
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

async def _check_model_health(model_name: str) -> Dict[str, Any]:
    """
    Check the health of a single model.
    """
    try:
        messages = [{"role": "user", "content": "Hello, are you there? Respond with just 'yes'."}]
        
        # Add safety settings specifically for Vertex AI models
        # and REMOVE max_tokens which triggers safety filters
        extra_kwargs = {}
        if model_name.startswith("vertex_ai"):
            extra_kwargs['safety_settings'] = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        else:
            # For non-Vertex AI models, use a small max_tokens to keep costs low
            extra_kwargs['max_tokens'] = 5
        
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
            temperature=0.0,
            **extra_kwargs
        )
        
        # Use getattr for safer attribute access
        content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
        if content.strip():
            return {"status": "success", "message": "Model responded successfully"}
        else:
            return {"status": "failed", "message": "Empty response received"}
            
    except Exception as e:
        return {"status": "failed", "message": str(e)}

async def _verify_model_health(models: List[str]) -> Dict[str, Any]:
    """
    Verify the health of all models in the list.
    """
    if not models:
        return {"all_healthy": True, "results": {}}
    
    results = {}
    tasks = []
    
    for model in models:
        task = _check_model_health(model)
        tasks.append((model, task))
    
    # Execute all health checks in parallel
    for model, task in tasks:
        try:
            result = await task
            results[model] = result
        except Exception as e:
            results[model] = {"status": "failed", "message": f"Health check failed: {str(e)}"}
    
    # Determine overall health
    failed_models = [model for model, result in results.items() if result["status"] == "failed"]
    all_healthy = len(failed_models) == 0
    
    return {
        "all_healthy": all_healthy,
        "results": results,
        "failed_models": failed_models,
        "total_models": len(models),
        "healthy_models": len(models) - len(failed_models)
    }

# Removed deprecated _load_project_components function - ValidationAgent handles this now

# Removed deprecated _execute_orchestration function - using EnsembleOrchestrator now

if __name__ == '__main__':
    soar() 