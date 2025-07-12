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
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from discernus.agents.validation_agent import ValidationAgent
    from discernus.core.framework_loader import FrameworkLoader
    from discernus.core.thin_litellm_client import ThinLiteLLMClient
    # Removed import of deprecated ThinOrchestrator
    SOAR_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  SOAR dependencies not available: {e}")
    print("   Please ensure discernus package is properly installed.")
    SOAR_DEPENDENCIES_AVAILABLE = False

@click.group()
@click.version_option(version='1.0.0', prog_name='SOAR')
def soar():
    """
    SOAR: Simple Atomic Orchestration Research
    
    Transform computational research from complex orchestration to simple execution,
    while maintaining the highest standards of academic rigor.
    """
    if not SOAR_DEPENDENCIES_AVAILABLE:
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
@click.option('--auto-validate', is_flag=True, help='Auto-validate before execution')
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(project_path: str, auto_validate: bool, dev_mode: bool, researcher_profile: str):
    """
    Execute validated SOAR project with dynamic orchestration
    
    PROJECT_PATH: Path to validated SOAR project directory
    
    Execution includes:
    - Dynamic worker count determination based on experiment complexity
    - Multi-agent analysis using framework specifications
    - Synthesis and competitive validation
    - Publication-ready results generation
    
    Example:
        soar execute ./my_cff_analysis
        soar execute ./my_cff_analysis --dev-mode
    """
    click.echo("🚀 SOAR Project Execution")
    click.echo("=" * 40)
    
    try:
        # Auto-validate if requested
        if auto_validate:
            click.echo("⏳ Auto-validating project...")
            validation_agent = ValidationAgent()
            validation_result = validation_agent.validate_project(project_path)
            
            if not validation_result['validation_passed']:
                click.echo(f"❌ Auto-validation failed: {validation_result['message']}")
                click.echo(f"   Use 'soar validate {project_path} --interactive' to fix issues")
                sys.exit(1)
            else:
                click.echo("✅ Auto-validation passed")
        
        # THIN: Validate first, then execute full orchestration
        click.echo(f"📁 Project Path: {project_path}")
        click.echo("📚 Validating project components...")
        
        project_path_obj = Path(project_path)
        framework_path = str(project_path_obj / "framework.md")
        experiment_path = str(project_path_obj / "experiment.md") 
        corpus_path = str(project_path_obj / "corpus")
        
        # Step 1: Validate project compatibility
        validation_agent = ValidationAgent()
        validation_results = validation_agent.validate_and_execute_sync(
            framework_path=framework_path,
            experiment_path=experiment_path,
            corpus_path=corpus_path,
            dev_mode=dev_mode
        )
        
        if validation_results['status'] != 'validated':
            click.echo(f"❌ Project validation failed: {validation_results['message']}")
            sys.exit(1)
        
        click.echo("✅ Project validation passed - starting full analysis...")
        
        # Step 2: Execute simple ensemble analysis
        from discernus.orchestration.ensemble_orchestrator import EnsembleOrchestrator
        
        # Initialize ensemble orchestrator
        ensemble_orchestrator = EnsembleOrchestrator(project_path)
        
        # Execute ensemble analysis pipeline
        results = asyncio.run(ensemble_orchestrator.execute_ensemble_analysis(validation_results))
        
        # Show results
        click.echo(f"\n🎉 Execution completed!")
        click.echo(f"   Status: {results.get('status', 'Unknown')}")
        click.echo(f"   Results: {results.get('message', 'No message')}")
        
    except Exception as e:
        click.echo(f"❌ Execution failed with error: {str(e)}", err=True)
        if dev_mode:
            import traceback
            traceback.print_exc()
        sys.exit(1)

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
    click.echo(f"Dependencies: {'✅ Available' if SOAR_DEPENDENCIES_AVAILABLE else '❌ Missing'}")
    
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

def _extract_research_question(experiment_content: str) -> str:
    """THIN: Let LLM extract research question"""
    try:
        llm_client = ThinLiteLLMClient()
        prompt = f"Extract the primary research question from this experiment:\n\n{experiment_content}\n\nReturn just the research question, nothing else."
        return llm_client.call_llm(prompt, "research_question_extractor")
    except:
        return "Research question not found"

# Removed deprecated _load_project_components function - ValidationAgent handles this now

# Removed deprecated _execute_orchestration function - using EnsembleOrchestrator now

if __name__ == '__main__':
    soar() 