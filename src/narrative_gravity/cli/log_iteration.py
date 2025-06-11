#!/usr/bin/env python3
"""
Development Iteration Logger - Priority 2 CLI Tool

Log iterations within development sessions with performance tracking.
Supports systematic documentation of development progress and metrics.

Usage:
    python log_iteration.py --session-id abc123 --hypothesis "Test evidence extraction" --changes "Added quote requirements" --results results.json
    python log_iteration.py --session-id abc123 --interactive
    python log_iteration.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.development.session_manager import DevelopmentSessionManager, SessionMetrics


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        sys.exit(1)


def interactive_input() -> Dict[str, Any]:
    """Interactive session for gathering iteration data."""
    print("🔬 Interactive Development Iteration Logging")
    print("=" * 50)
    print()
    
    # Basic iteration info
    hypothesis = input("Iteration Hypothesis: ")
    changes = input("Changes Made: ")
    notes = input("Notes (optional): ")
    
    # Test results
    print("\n📊 Test Results:")
    test_results = {}
    
    while True:
        key = input("Test result key (or press Enter to finish): ").strip()
        if not key:
            break
        value = input(f"Value for '{key}': ").strip()
        
        # Try to convert to number if possible
        try:
            if '.' in value:
                test_results[key] = float(value)
            else:
                test_results[key] = int(value)
        except ValueError:
            test_results[key] = value
    
    # Performance metrics
    print("\n📈 Performance Metrics (optional):")
    metrics = {}
    
    cv = input("Coefficient of Variation (0.0-1.0): ").strip()
    if cv:
        try:
            metrics['coefficient_variation'] = float(cv)
        except ValueError:
            print("⚠️  Warning: Invalid CV value, skipping")
    
    hierarchy = input("Hierarchy Clarity Score (0.0-1.0): ").strip()
    if hierarchy:
        try:
            metrics['hierarchy_clarity_score'] = float(hierarchy)
        except ValueError:
            print("⚠️  Warning: Invalid hierarchy score, skipping")
    
    framework_fit = input("Framework Fit Average (0.0-1.0): ").strip()
    if framework_fit:
        try:
            metrics['framework_fit_average'] = float(framework_fit)
        except ValueError:
            print("⚠️  Warning: Invalid framework fit score, skipping")
    
    evidence_quality = input("Evidence Quality Score (0.0-1.0): ").strip()
    if evidence_quality:
        try:
            metrics['evidence_quality_score'] = float(evidence_quality)
        except ValueError:
            print("⚠️  Warning: Invalid evidence quality score, skipping")
    
    math_valid = input("Mathematical Validity (y/n): ").strip().lower()
    if math_valid in ['y', 'yes', 'true']:
        metrics['mathematical_validity'] = True
    elif math_valid in ['n', 'no', 'false']:
        metrics['mathematical_validity'] = False
    
    # Custom metrics
    print("\nCustom Metrics (optional):")
    custom_metrics = {}
    while True:
        key = input("Custom metric name (or press Enter to finish): ").strip()
        if not key:
            break
        value = input(f"Value for '{key}': ").strip()
        
        # Try to convert to number if possible
        try:
            if '.' in value:
                custom_metrics[key] = float(value)
            else:
                custom_metrics[key] = int(value)
        except ValueError:
            custom_metrics[key] = value
    
    if custom_metrics:
        metrics['custom_metrics'] = custom_metrics
    
    # Version creation
    version_created = input("\nNew version created (optional): ").strip()
    
    return {
        'hypothesis': hypothesis,
        'changes': changes,
        'notes': notes,
        'test_results': test_results,
        'metrics': metrics,
        'version_created': version_created if version_created else None
    }


def main():
    parser = argparse.ArgumentParser(
        description="Log an iteration within a development session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Log iteration with JSON results file:
    python log_iteration.py --session-id abc123-def456 \\
        --hypothesis "Test evidence extraction improvements" \\
        --changes "Added explicit quote requirements and examples" \\
        --results test_results.json

  Log iteration with inline metrics:
    python log_iteration.py --session-id abc123-def456 \\
        --hypothesis "Test hierarchy amplification" \\
        --changes "Modified winner-take-most parameters" \\
        --cv 0.18 --hierarchy-score 0.85 \\
        --notes "Significant improvement in thematic distinction"

  Interactive logging mode:
    python log_iteration.py --session-id abc123-def456 --interactive

  Example test_results.json format:
    {
        "texts_tested": 5,
        "avg_score_consistency": 0.82,
        "ranking_accuracy": 0.91,
        "evidence_quality": "improved"
    }
        """
    )
    
    parser.add_argument(
        "--session-id",
        required=True,
        help="Development session ID"
    )
    
    parser.add_argument(
        "--hypothesis",
        help="Hypothesis for this iteration"
    )
    
    parser.add_argument(
        "--changes",
        help="Description of changes made in this iteration"
    )
    
    parser.add_argument(
        "--results",
        help="Path to JSON file containing test results"
    )
    
    parser.add_argument(
        "--notes",
        default="",
        help="Additional notes and observations"
    )
    
    parser.add_argument(
        "--version-created",
        help="New component version ID if created in this iteration"
    )
    
    # Performance metrics
    parser.add_argument(
        "--cv",
        type=float,
        help="Coefficient of variation (0.0-1.0)"
    )
    
    parser.add_argument(
        "--hierarchy-score",
        type=float,
        help="Hierarchy clarity score (0.0-1.0)"
    )
    
    parser.add_argument(
        "--framework-fit",
        type=float,
        help="Framework fit average (0.0-1.0)"
    )
    
    parser.add_argument(
        "--evidence-quality",
        type=float,
        help="Evidence quality score (0.0-1.0)"
    )
    
    parser.add_argument(
        "--math-valid",
        action="store_true",
        help="Mathematical validity flag"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Use interactive mode for input"
    )
    
    args = parser.parse_args()
    
    # Initialize session manager
    session_manager = DevelopmentSessionManager()
    
    # Interactive mode
    if args.interactive:
        iteration_data = interactive_input()
        hypothesis = iteration_data['hypothesis']
        changes = iteration_data['changes']
        notes = iteration_data['notes']
        test_results = iteration_data['test_results']
        version_created = iteration_data['version_created']
        
        # Build metrics object
        metrics_dict = iteration_data['metrics']
        performance_metrics = SessionMetrics(**metrics_dict) if metrics_dict else None
        
    else:
        # Command line mode
        if not args.hypothesis:
            print("❌ Error: --hypothesis is required (or use --interactive)")
            sys.exit(1)
        
        if not args.changes:
            print("❌ Error: --changes is required (or use --interactive)")
            sys.exit(1)
        
        hypothesis = args.hypothesis
        changes = args.changes
        notes = args.notes
        version_created = args.version_created
        
        # Load test results
        if args.results:
            test_results = load_json_file(args.results)
        else:
            test_results = {}
        
        # Build performance metrics
        metrics_dict = {}
        if args.cv is not None:
            metrics_dict['coefficient_variation'] = args.cv
        if args.hierarchy_score is not None:
            metrics_dict['hierarchy_clarity_score'] = args.hierarchy_score
        if args.framework_fit is not None:
            metrics_dict['framework_fit_average'] = args.framework_fit
        if args.evidence_quality is not None:
            metrics_dict['evidence_quality_score'] = args.evidence_quality
        if args.math_valid:
            metrics_dict['mathematical_validity'] = True
        
        performance_metrics = SessionMetrics(**metrics_dict) if metrics_dict else None
    
    # Log the iteration
    try:
        iteration_number = session_manager.log_iteration(
            session_id=args.session_id,
            iteration_hypothesis=hypothesis,
            changes_made=changes,
            test_results=test_results,
            performance_metrics=performance_metrics,
            notes=notes,
            version_created=version_created
        )
        
        print()
        print("✅ Iteration Logged Successfully!")
        print(f"Session ID: {args.session_id}")
        print(f"Iteration Number: {iteration_number}")
        print()
        
        # Show session status
        try:
            status = session_manager.get_session_status(args.session_id)
            print("📊 Updated Session Status:")
            print(f"   Total Iterations: {status['iterations']}")
            print(f"   Current Metrics: {status['current_metrics']}")
            print()
            
        except Exception as e:
            print(f"⚠️  Could not retrieve session status: {e}")
        
        # Show next steps
        print("📋 Next Steps:")
        print("1. Continue development iterations as needed")
        print("2. Log additional iterations with new hypotheses")
        print("3. Complete session when development goals are achieved")
        print()
        
        print("🔧 Related Commands:")
        print(f"   Session status: python get_session_status.py --session-id {args.session_id}")
        print(f"   Complete session: python complete_session.py --session-id {args.session_id}")
        print("   Quality validation: python validate_component.py --component-type [type] --file [path]")
        print()
        
    except Exception as e:
        print(f"❌ Error logging iteration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 