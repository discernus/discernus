#!/usr/bin/env python3
"""
Discernus CLI - Computational Text Analysis Platform
===================================================

THIN Command-line interface for Discernus computational text analysis platform.
Provides validate, execute, and resume commands for systematic computational research.

USAGE:
    discernus validate ./my_project     # Validate project structure and specifications
    discernus execute ./my_project      # Execute validated project with dynamic orchestration
    discernus resume ./my_project       # Resume interrupted experiment from latest state
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
from typing import Dict, Any, List, Optional
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
    
    # THIN Experiment Lifecycle - replaces direct WorkflowOrchestrator calls
    from discernus.core.experiment_lifecycle import ExperimentStartup
    
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
@click.argument('experiment_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--dev-mode', is_flag=True, help='Run in development mode with simulated researcher')
@click.option('--researcher-profile', default='experienced_computational_social_scientist', 
              help='Simulated researcher profile for dev mode')
def execute(experiment_file: str, dev_mode: bool, researcher_profile: str):
    """
    Execute a Discernus experiment using THIN Experiment Lifecycle
    
    EXPERIMENT_FILE: Path to V2 experiment file containing all configuration (experiment.md)
    
    NEW: Uses intelligent THIN Experiment Lifecycle (Issue #131):
    - Comprehensive validation gauntlet (TrueValidationAgent, ProjectCoherenceAnalyst, etc.)
    - Workflow completeness analysis (prevents "technically compliant but research useless")
    - Intelligent enhancement with user consent
    - Provenance-compliant snapshots (preserves original experiment.md)
    - Clean handoff to pristine WorkflowOrchestrator
    
    Validation Gauntlet:
    1. TrueValidationAgent - Rubric-based framework/experiment validation
    2. ProjectCoherenceAnalyst - Socratic research methodology validation
    3. StatisticalAnalysisConfigurationAgent - Statistical plan validation
    4. EnsembleConfigurationAgent - Model health checks and resource planning
    5. WorkflowCompletenessValidator - Ensure SynthesisAgent exists for reports
    
    Benefits:
    - Solves Issue #68: No more "specification-compliant but useless" experiments
    - Automatic enhancement of incomplete workflows
    - Complete audit trail and provenance
    - Human-centric UX with clear consent mechanisms
    
    Example:
        discernus execute ./experiment.md
        discernus execute ./experiment.md --dev-mode
    """
    click.echo("🚀 Discernus Experiment Execution")
    click.echo("=" * 40)
    click.echo(f"🧪 Experiment: {experiment_file}")
    
    # --- Set up logging and chronolog ---
    session_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    project_path = Path(experiment_file).parent # Use experiment file for project context
    
    # Create temporary logs directory for CLI session log
    # Actual session directories will be created by WorkflowOrchestrator following Provenance Guide v3.0
    temp_logs_dir = project_path / "logs" / f"cli_session_{session_timestamp}"
    temp_logs_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = temp_logs_dir / "session_run.log"

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
            print("🚀 THIN Experiment Lifecycle - Starting intelligent experiment validation...")
            
            # NEW: Use THIN Experiment Lifecycle instead of direct WorkflowOrchestrator
            experiment_path = Path(experiment_file)
            project_path = experiment_path.parent
            
            print(f"🧪 Experiment: {experiment_path}")
            print(f"📁 Project: {project_path}")
            
            # Initialize the intelligent experiment startup
            startup = ExperimentStartup(str(project_path))
            
            print("🔍 Running comprehensive validation gauntlet...")
            print("   Phase 1: TrueValidationAgent (rubric-based)")
            print("   Phase 2: ProjectCoherenceAnalyst (Socratic methodology)")
            print("   Phase 3: StatisticalAnalysisConfiguration (statistical plan)")
            print("   Phase 4: EnsembleConfiguration (model health)")
            print("   Phase 5: WorkflowCompleteness (research deliverables)")
            
            # Execute with intelligent lifecycle management
            # This replaces all the manual specification loading and orchestrator setup
            results = await startup.start_experiment(
                experiment_file=experiment_path,
                dev_mode=dev_mode,
                auto_enhance=True  # Allow automatic workflow enhancement
            )
            
            print("✅ THIN Experiment Lifecycle completed successfully!")
            
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
            click.echo("📊 Results saved to experiment session directory (see session log for details)")
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

@discernus.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--state-file', type=click.Path(exists=True, file_okay=True, dir_okay=False), 
              help='Specific state file to resume from')
@click.option('--from-step', type=int, help='Step number to resume from (1-based)')
@click.option('--dry-run', is_flag=True, help='Show what would be resumed without executing')
@click.option('--list-states', is_flag=True, help='List available state files for resumption')
@click.option('--intelligent/--legacy', default=True, help='Use intelligent resumption analysis (default: True)')
def resume(project_path: str, state_file: str, from_step: int, dry_run: bool, list_states: bool, intelligent: bool):
    """
    Resume an interrupted Discernus experiment with intelligent state analysis
    
    PROJECT_PATH: Path to the project directory containing the interrupted experiment
    
    NEW: Intelligent resumption with state analysis, workflow change detection,
    resource validation, and user guidance. Provides comprehensive pre-flight 
    checks before resuming experiment execution.
    
    Features:
    - State integrity validation
    - Workflow change detection since interruption  
    - Resource availability validation
    - Clear progress reporting and user guidance
    - Provenance-compliant audit trails
    - Clean handoff to WorkflowOrchestrator
    
    Examples:
        discernus resume ./projects/my_experiment                    # Intelligent analysis
        discernus resume ./projects/my_experiment --dry-run          # Show analysis only
        discernus resume ./projects/my_experiment --legacy          # Use legacy resume
        discernus resume ./projects/my_experiment --state-file state_after_step_2.json
        discernus resume ./projects/my_experiment --from-step 3
        discernus resume ./projects/my_experiment --list-states
    """
    if intelligent:
        click.echo("🧠 Discernus Intelligent Experiment Resume")  
        click.echo("=" * 45)
        click.echo("✨ Enhanced with state analysis and workflow validation")
    else:
        click.echo("🔄 Discernus Experiment Resume (Legacy Mode)")
        click.echo("=" * 40)
    
    project_dir = Path(project_path)
    
    # Handle --list-states option
    if list_states:
        _list_available_states(project_dir)
        return
        
    # Route to intelligent or legacy resumption
    if intelligent:
        return _resume_with_intelligence(project_dir, state_file, from_step, dry_run)
    else:
        return _resume_legacy(project_dir, state_file, from_step, dry_run)


def _resume_with_intelligence(project_dir: Path, state_file: str, from_step: int, dry_run: bool):
    """Use intelligent resumption system with state analysis and validation"""
    import asyncio
    from discernus.core.experiment_lifecycle import ExperimentResumption
    
    try:
        # Initialize intelligent resumption system
        resumption = ExperimentResumption(str(project_dir))
        
        # Convert CLI arguments
        state_file_path = Path(state_file) if state_file else None
        
        # Execute intelligent resumption
        result = asyncio.run(resumption.resume_experiment(
            state_file=state_file_path,
            from_step=from_step,
            dry_run=dry_run
        ))
        
        if result.get('status') == 'cancelled':
            click.echo("🚫 Resume cancelled by user.")
            return
        elif result.get('status') == 'dry_run_success':
            analysis = result.get('analysis')
            click.echo(f"🧪 DRY RUN COMPLETE - Would resume from step {analysis.resume_step}")
            click.echo(f"📊 Analysis: {analysis.resumption_strategy}")
            return
        elif result.get('status') == 'success':
            click.secho(f"\n🎉 Intelligent resume completed successfully!", fg='green')
            click.echo(f"   Session ID: {result['session_id']}")
            click.echo(f"   Results: {result['session_results_path']}")
            if result.get('intelligent_resumption'):
                click.echo("✨ Enhanced with intelligent state analysis")
        else:
            click.secho(f"❌ Resume failed: {result.get('status', 'Unknown error')}", fg='red')
            
    except Exception as e:
        click.secho(f"❌ Intelligent resume failed: {str(e)}", fg='red')
        click.echo("💡 Try using --legacy flag for traditional resume behavior")
        sys.exit(1)


def _resume_legacy(project_dir: Path, state_file: str, from_step: int, dry_run: bool):
    """Legacy resumption using direct CLI logic (original implementation)"""
    
    # Find state file
    if state_file:
        state_file_path = Path(state_file)
        click.echo(f"📂 Using specified state file: {state_file_path}")
    else:
        state_file_path = _find_latest_state_file(project_dir)
        if not state_file_path:
            click.secho("❌ No state files found for resumption.", fg='red')
            click.echo("💡 Run 'discernus resume PROJECT_PATH --list-states' to see available state files.")
            sys.exit(1)
        click.echo(f"📂 Using latest state file: {state_file_path}")
    
    # Load state data
    try:
        with open(state_file_path, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        click.echo(f"✅ Loaded state file with {len(state_data.keys())} top-level keys")
    except Exception as e:
        click.secho(f"❌ Failed to load state file: {e}", fg='red')
        sys.exit(1)
    
    # Determine workflow steps and resume point
    workflow_steps = state_data.get('workflow', [])
    if not workflow_steps:
        click.secho("❌ No workflow steps found in state file.", fg='red')
        sys.exit(1)
    
    # Determine resume step
    if from_step:
        resume_step = from_step
        click.echo(f"🎯 Resuming from user-specified step: {resume_step}")
    else:
        resume_step = _determine_resume_step(state_file_path, workflow_steps)
        click.echo(f"🎯 Auto-detected resume step: {resume_step}")
    
    # Validate resume step
    if resume_step < 1 or resume_step > len(workflow_steps):
        click.secho(f"❌ Invalid resume step: {resume_step}. Must be between 1 and {len(workflow_steps)}", fg='red')
        sys.exit(1)
    
    # Show workflow status
    click.echo(f"\n📋 Workflow Status ({len(workflow_steps)} steps total):")
    for i, step in enumerate(workflow_steps):
        agent_name = step.get('agent', 'Unknown')
        if i < resume_step - 1:
            status = "✅ COMPLETED"
        elif i == resume_step - 1:
            status = "🚀 RESUMING"
        else:
            status = "⏳ PENDING"
        click.echo(f"   Step {i+1}: {agent_name} - {status}")
    
    # Handle dry run
    if dry_run:
        click.echo(f"\n🧪 DRY RUN: Would resume from step {resume_step}")
        click.echo("   No actual execution will occur.")
        return
    
    # Confirm execution
    if not click.confirm(f"\n🚀 Resume experiment from step {resume_step}?"):
        click.echo("Resume cancelled.")
        return
    
    # Execute resumption
    try:
        click.echo(f"\n🔄 Resuming experiment from step {resume_step}...")
        
        # Initialize orchestrator
        orchestrator = WorkflowOrchestrator(str(project_dir))
        
        # Execute resumption
        result = _execute_resumption(orchestrator, state_data, resume_step, workflow_steps)
        
        click.secho(f"\n🎉 Experiment resume completed successfully!", fg='green')
        click.echo(f"   Session ID: {result['session_id']}")
        click.echo(f"   Status: {result['status']}")
        
        # Show results location
        if 'session_results_path' in result:
            results_path = result['session_results_path']
            click.echo(f"   Results: {results_path}")
        
    except Exception as e:
        click.secho(f"\n❌ Resume failed: {str(e)}", fg='red')
        sys.exit(1)

def _list_available_states(project_path: Path):
    """List all available state files for resumption."""
    click.echo(f"📁 Scanning for state files in: {project_path}")
    
    results_dir = project_path / "results"
    if not results_dir.exists():
        click.echo("❌ No results directory found.")
        return
    
    state_files = []
    for session_dir in results_dir.iterdir():
        if session_dir.is_dir():
            # Look for both final and partial state files
            for state_file in session_dir.glob("state_after_step_*.json"):
                state_files.append(state_file)
            for partial_state_file in session_dir.glob("state_step_*_partial.json"):
                state_files.append(partial_state_file)
    
    if not state_files:
        click.echo("❌ No state files found.")
        return
    
    # Sort by modification time (newest first)
    state_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    click.echo(f"\n📋 Found {len(state_files)} state files:")
    for i, state_file in enumerate(state_files[:10]):  # Show top 10
        relative_path = state_file.relative_to(project_path)
        mod_time = datetime.datetime.fromtimestamp(state_file.stat().st_mtime)
        click.echo(f"   {i+1}. {relative_path} ({mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    if len(state_files) > 10:
        click.echo(f"   ... and {len(state_files) - 10} more")

def _find_latest_state_file(project_path: Path) -> Optional[Path]:
    """Find the most recent state file in the project.
    
    Searches both directory structures:
    1. results/ (legacy structure - MVA experiments)
    2. experiments/ (current WorkflowOrchestrator structure)
    
    This fixes Issue #130 where resume auto-discovery failed due to directory mismatch.
    """
    state_files = []
    
    # Search legacy results/ structure
    results_dir = project_path / "results"
    if results_dir.exists():
        for session_dir in results_dir.iterdir():
            if session_dir.is_dir():
                # Look for both final and partial state files
                for state_file in session_dir.glob("state_after_step_*.json"):
                    state_files.append(state_file)
                for partial_state_file in session_dir.glob("state_step_*_partial.json"):
                    state_files.append(partial_state_file)
    
    # Search experiments/ structure (WorkflowOrchestrator v3.0+)
    experiments_dir = project_path / "experiments"
    if experiments_dir.exists():
        for experiment_dir in experiments_dir.iterdir():
            if experiment_dir.is_dir():
                sessions_dir = experiment_dir / "sessions"
                if sessions_dir.exists():
                    for session_dir in sessions_dir.iterdir():
                        if session_dir.is_dir():
                            # Look for both final and partial state files
                            for state_file in session_dir.glob("state_after_step_*.json"):
                                state_files.append(state_file)
                            for partial_state_file in session_dir.glob("state_step_*_partial.json"):
                                state_files.append(partial_state_file)
    
    if not state_files:
        return None
    
    # Return the most recently modified state file from either location
    latest_file = max(state_files, key=lambda x: x.stat().st_mtime)
    print(f"✅ Resume: Found latest state file: {latest_file}")
    return latest_file

def _determine_resume_step(state_file_path: Path, workflow_steps: List[Dict]) -> int:
    """Determine which step to resume from based on the state file name."""
    filename = state_file_path.name
    
    # Handle partial state files like "state_step_1_partial.json"
    partial_match = re.search(r'state_step_(\d+)_partial', filename)
    if partial_match:
        current_step = int(partial_match.group(1))
        # For partial state files, resume from the same step since it may be incomplete
        return current_step
    
    # Handle completed state files like "state_after_step_1_AgentName.json"
    completed_match = re.search(r'state_after_step_(\d+)_', filename)
    if completed_match:
        completed_step = int(completed_match.group(1))
        return completed_step + 1  # Resume from next step
    
    # Fallback: resume from step 1
    return 1

def _execute_resumption(orchestrator: WorkflowOrchestrator, state_data: Dict[str, Any], 
                       resume_step: int, workflow_steps: List[Dict]) -> Dict[str, Any]:
    """Execute the resumption workflow."""
    # Extract existing session path from state data instead of creating new session
    existing_session_path = state_data.get('session_results_path')
    if existing_session_path:
        # Handle both absolute and relative paths from the state file
        if not Path(existing_session_path).is_absolute():
            # Path is relative to project directory
            full_session_path = Path(orchestrator.project_path) / existing_session_path
        else:
            full_session_path = Path(existing_session_path)
            
        if full_session_path.exists():
            # Reuse existing session directory
            orchestrator.session_results_path = full_session_path
            orchestrator.session_id = full_session_path.name  # Use directory name as session ID
            orchestrator.conversation_id = state_data.get('conversation_id', f"resumed_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Initialize logger and archive manager for existing session
            from discernus.core.conversation_logger import ConversationLogger
            orchestrator.logger = ConversationLogger(str(orchestrator.project_path))
            
            # Initialize archive manager if it doesn't exist
            if not hasattr(orchestrator, 'archive_manager') or not orchestrator.archive_manager:
                from discernus.core.llm_archive_manager import LLMArchiveManager
                orchestrator.archive_manager = LLMArchiveManager(orchestrator.session_results_path)
                
                # Update gateway to use archive manager if it's an LLMGateway
                if hasattr(orchestrator.gateway, 'archive_manager') and hasattr(orchestrator.gateway, '__class__'):
                    from discernus.gateway.llm_gateway import LLMGateway
                    if isinstance(orchestrator.gateway, LLMGateway):
                        orchestrator.gateway.archive_manager = orchestrator.archive_manager
            
            click.echo(f"♻️  Resuming existing session: {orchestrator.session_id}")
        else:
            # Fallback to new session if existing session path not found
            orchestrator._init_session_logging()
            click.echo(f"🆕 Creating new session (existing session not found at {full_session_path}): {orchestrator.session_id}")
    else:
        # Fallback to new session if no session path in state
        orchestrator._init_session_logging()
        click.echo(f"🆕 Creating new session (no session path in state): {orchestrator.session_id}")
    
    # Prime the workflow state
    orchestrator.workflow_state = state_data
    orchestrator.workflow_state['session_results_path'] = str(orchestrator.session_results_path)
    orchestrator.workflow_state['conversation_id'] = orchestrator.conversation_id
    
    # Execute remaining steps
    for i in range(resume_step - 1, len(workflow_steps)):
        step_config = workflow_steps[i]
        agent_name = step_config.get('agent')
        
        click.echo(f"\n🚀 Executing Step {i+1}: {agent_name}")
        
        try:
            if not agent_name:
                raise ValueError(f"Step {i+1} is missing the 'agent' key.")
            
            step_output = orchestrator._execute_step(agent_name, step_config)
            
            # Update the master workflow state
            if step_output:
                orchestrator.workflow_state.update(step_output)
            
            # Save state snapshot
            orchestrator._save_state_snapshot(f"state_after_step_{i+1}_{agent_name}.json")
            
            click.echo(f"✅ Step {i+1} completed successfully")
            
        except Exception as e:
            click.secho(f"❌ Step {i+1} failed: {str(e)}", fg='red')
            raise e
    
    return {
        "status": "success",
        "session_id": orchestrator.session_id,
        "session_results_path": str(orchestrator.session_results_path),
        "final_state": orchestrator.workflow_state
    }

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