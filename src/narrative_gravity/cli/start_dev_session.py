#!/usr/bin/env python3
"""
Development Session Starter - Priority 2 CLI Tool

Start structured development sessions for systematic component development.
Integrates with Priority 1 infrastructure and Priority 2 development support.

Usage:
    python start_dev_session.py --component-type prompt_template --name hierarchical_v2 --hypothesis "Improve ranking clarity"
    python start_dev_session.py --component-type framework --name environmental_justice --hypothesis "Test domain coverage"
    python start_dev_session.py --help
"""

import argparse
import sys
from pathlib import Path

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.development.session_manager import DevelopmentSessionManager
from src.narrative_gravity.development.seed_prompts import SeedPromptLibrary, ComponentType


def main():
    parser = argparse.ArgumentParser(
        description="Start a structured development session for systematic component development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Start prompt template development session:
    python start_dev_session.py --component-type prompt_template --name hierarchical_v2 \\
        --hypothesis "Improve ranking clarity and evidence extraction"

  Start framework development session:
    python start_dev_session.py --component-type framework --name environmental_justice \\
        --hypothesis "Test framework coverage for environmental narratives"
        
  Start weighting methodology session:
    python start_dev_session.py --component-type weighting_methodology --name enhanced_winner_take_most \\
        --hypothesis "Reduce compression of subtle themes while enhancing dominance"

  Get seed prompt for external development:
    python start_dev_session.py --component-type prompt_template --get-seed-prompt-only \\
        --framework-name civic_virtue --current-challenge "Inconsistent scoring across runs"
        """
    )
    
    parser.add_argument(
        "--component-type",
        required=True,
        choices=["prompt_template", "framework", "weighting_methodology"],
        help="Type of component being developed"
    )
    
    parser.add_argument(
        "--name",
        required=False,
        help="Name of the component being developed"
    )
    
    parser.add_argument(
        "--hypothesis",
        required=False,
        help="Development hypothesis or goal for this session"
    )
    
    parser.add_argument(
        "--base-version",
        help="Starting version for iteration (if modifying existing component)"
    )
    
    parser.add_argument(
        "--target-version",
        help="Intended new version to be created"
    )
    
    parser.add_argument(
        "--researcher-id",
        type=int,
        help="ID of researcher conducting session"
    )
    
    # Seed prompt options
    parser.add_argument(
        "--get-seed-prompt-only",
        action="store_true",
        help="Only generate and display seed prompt without starting session"
    )
    
    parser.add_argument(
        "--framework-name",
        help="Framework name for seed prompt context"
    )
    
    parser.add_argument(
        "--framework-description",
        help="Framework description for seed prompt context"
    )
    
    parser.add_argument(
        "--current-challenge",
        help="Current challenge or problem for seed prompt context"
    )
    
    parser.add_argument(
        "--current-version",
        help="Current component version for seed prompt context"
    )
    
    parser.add_argument(
        "--development-hypothesis",
        help="Development hypothesis for seed prompt context"
    )
    
    parser.add_argument(
        "--list-active",
        action="store_true",
        help="List all currently active development sessions"
    )
    
    args = parser.parse_args()
    
    # Initialize managers
    session_manager = DevelopmentSessionManager()
    seed_library = SeedPromptLibrary()
    
    # List active sessions
    if args.list_active:
        active_sessions = session_manager.list_active_sessions()
        if not active_sessions:
            print("No active development sessions found.")
            return
        
        print("🔬 Active Development Sessions:")
        print("=" * 60)
        for session in active_sessions:
            print(f"Session ID: {session['session_id']}")
            print(f"Name: {session['session_name']}")
            print(f"Component: {session['component_type']}/{session['component_name']}")
            print(f"Started: {session['started_at']}")
            print(f"Iterations: {session['iterations']}")
            print(f"Hypothesis: {session['hypothesis']}")
            print("-" * 40)
        return
    
    # Generate seed prompt only
    if args.get_seed_prompt_only:
        try:
            component_type = ComponentType(args.component_type)
            
            # Build context for seed prompt
            context = {}
            if args.framework_name:
                context['framework_name'] = args.framework_name
            if args.framework_description:
                context['framework_description'] = args.framework_description
            if args.current_challenge:
                context['current_challenge'] = args.current_challenge
            if args.current_version:
                context['current_version'] = args.current_version
            if args.development_hypothesis:
                context['development_hypothesis'] = args.development_hypothesis
            
            # Component-specific context
            if args.component_type == "prompt_template":
                context.setdefault('current_challenge', '[CURRENT_CHALLENGE_TO_BE_SPECIFIED]')
                context.setdefault('framework_name', '[FRAMEWORK_NAME_TO_BE_SPECIFIED]')
                context.setdefault('framework_description', '[FRAMEWORK_DESCRIPTION_TO_BE_SPECIFIED]')
                context.setdefault('framework_wells', '[FRAMEWORK_WELLS_TO_BE_SPECIFIED]')
                context.setdefault('current_version', '[CURRENT_VERSION_TO_BE_SPECIFIED]')
                context.setdefault('development_hypothesis', '[DEVELOPMENT_HYPOTHESIS_TO_BE_SPECIFIED]')
                
            elif args.component_type == "framework":
                context.setdefault('framework_domain', '[FRAMEWORK_DOMAIN_TO_BE_SPECIFIED]')
                context.setdefault('theoretical_source', '[THEORETICAL_SOURCE_TO_BE_SPECIFIED]')
                context.setdefault('existing_dipoles', '[EXISTING_DIPOLES_TO_BE_SPECIFIED]')
                context.setdefault('target_domain', '[TARGET_DOMAIN_TO_BE_SPECIFIED]')
                context.setdefault('development_hypothesis', '[DEVELOPMENT_HYPOTHESIS_TO_BE_SPECIFIED]')
                
            elif args.component_type == "weighting_methodology":
                context.setdefault('current_problem', '[CURRENT_PROBLEM_TO_BE_SPECIFIED]')
                context.setdefault('num_wells', '[NUM_WELLS_TO_BE_SPECIFIED]')
                context.setdefault('current_approach', '[CURRENT_APPROACH_TO_BE_SPECIFIED]')
                context.setdefault('observed_issues', '[OBSERVED_ISSUES_TO_BE_SPECIFIED]')
                context.setdefault('development_focus', '[DEVELOPMENT_FOCUS_TO_BE_SPECIFIED]')
                context.setdefault('development_hypothesis', '[DEVELOPMENT_HYPOTHESIS_TO_BE_SPECIFIED]')
            
            seed_prompt = seed_library.get_prompt(component_type, context)
            
            print("🌱 Structured Development Seed Prompt")
            print("=" * 80)
            print()
            print(seed_prompt)
            print()
            print("=" * 80)
            print("💡 Copy this prompt and use it to start your LLM-assisted development session.")
            print("   Replace [PLACEHOLDER] values with your specific context.")
            print()
            
            # Show success criteria and development steps
            success_criteria = seed_library.get_success_criteria(component_type)
            development_steps = seed_library.get_development_steps(component_type)
            
            print("✅ Success Criteria:")
            for i, criterion in enumerate(success_criteria, 1):
                print(f"   {i}. {criterion}")
            print()
            
            print("📋 Development Steps:")
            for i, step in enumerate(development_steps, 1):
                print(f"   {i}. {step}")
            print()
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
        
        return
    
    # Validate required arguments for session creation
    if not args.name:
        print("❌ Error: --name is required when starting a development session")
        sys.exit(1)
    
    if not args.hypothesis:
        print("❌ Error: --hypothesis is required when starting a development session")
        sys.exit(1)
    
    # Start development session
    try:
        session_name = f"{args.component_type}_{args.name}_session"
        
        session_id = session_manager.start_session(
            session_name=session_name,
            component_type=args.component_type,
            component_name=args.name,
            hypothesis=args.hypothesis,
            base_version=args.base_version,
            target_version=args.target_version,
            researcher_id=args.researcher_id
        )
        
        print()
        print("🎯 Development Session Started Successfully!")
        print(f"Session ID: {session_id}")
        print()
        
        # Generate and display seed prompt
        component_type = ComponentType(args.component_type)
        
        # Build basic context
        context = {
            'current_challenge': '[CURRENT_CHALLENGE_TO_BE_SPECIFIED]',
            'development_hypothesis': args.hypothesis
        }
        
        seed_prompt = session_manager.get_seed_prompt(args.component_type, context)
        
        print("🌱 Structured Development Seed Prompt for Your Session:")
        print("=" * 80)
        print()
        print(seed_prompt)
        print()
        print("=" * 80)
        print()
        
        # Show next steps
        print("📋 Next Steps:")
        print("1. Copy the seed prompt above and start your LLM conversation")
        print("2. Replace [PLACEHOLDER] values with your specific context")
        print("3. Iterate on your component based on the development steps")
        print("4. Use 'log_iteration.py' to record each development iteration")
        print("5. Use 'complete_session.py' when finished")
        print()
        
        print("🔧 Related Commands:")
        print(f"   Log iteration: python log_iteration.py --session-id {session_id}")
        print(f"   Session status: python get_session_status.py --session-id {session_id}")
        print(f"   Complete session: python complete_session.py --session-id {session_id}")
        print()
        
    except Exception as e:
        print(f"❌ Error starting development session: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 