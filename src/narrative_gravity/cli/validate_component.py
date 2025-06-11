#!/usr/bin/env python3
"""
Component Quality Validator - Priority 2 CLI Tool

Validate quality of developed components using automated quality assurance.
Supports comprehensive quality assessment for academic standards.

Usage:
    python validate_component.py --component-type prompt_template --file prompt.txt
    python validate_component.py --component-type framework --file framework.json --theoretical-foundation foundation.txt
    python validate_component.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.development.quality_assurance import ComponentQualityValidator, QualityLevel
from src.narrative_gravity.development.seed_prompts import ComponentType


def load_file_content(file_path: str) -> str:
    """Load text content from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        sys.exit(1)


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


def format_quality_level(level: QualityLevel) -> str:
    """Format quality level with appropriate emoji."""
    level_emojis = {
        QualityLevel.EXCELLENT: "🟢",
        QualityLevel.GOOD: "🟡", 
        QualityLevel.ACCEPTABLE: "🟠",
        QualityLevel.NEEDS_IMPROVEMENT: "🔴",
        QualityLevel.UNACCEPTABLE: "💀"
    }
    return f"{level_emojis.get(level, '❓')} {level.value.upper()}"


def print_quality_report(report):
    """Print comprehensive quality assessment report."""
    print()
    print("📋 COMPONENT QUALITY ASSESSMENT REPORT")
    print("=" * 80)
    print()
    
    # Header information
    print(f"Component Type: {report.component_type.value}")
    print(f"Component Name: {report.component_name}")
    print(f"Version: {report.version}")
    print()
    
    # Overall assessment
    print("🎯 OVERALL ASSESSMENT")
    print("-" * 40)
    print(f"Overall Score: {report.overall_score:.2f}/1.00")
    print(f"Quality Level: {format_quality_level(report.overall_level)}")
    print(f"Academic Readiness: {'✅ YES' if report.academic_readiness else '❌ NO'}")
    print()
    
    # Quality checks breakdown
    print("🔍 DETAILED QUALITY CHECKS")
    print("-" * 40)
    
    passed_checks = [check for check in report.checks if check.passed]
    failed_checks = [check for check in report.checks if not check.passed]
    
    print(f"Passed: {len(passed_checks)}/{len(report.checks)} checks")
    print()
    
    if failed_checks:
        print("❌ FAILED CHECKS:")
        for check in failed_checks:
            severity_emoji = {"error": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(check.severity, "❓")
            print(f"   {severity_emoji} {check.check_name}")
            print(f"      Score: {check.score:.2f}")
            print(f"      Issue: {check.message}")
            if check.recommendation:
                print(f"      Fix: {check.recommendation}")
            print()
    
    if passed_checks:
        print("✅ PASSED CHECKS:")
        for check in passed_checks:
            print(f"   ✓ {check.check_name} ({check.score:.2f})")
        print()
    
    # Recommendations
    if report.recommendations:
        print("💡 RECOMMENDATIONS")
        print("-" * 40)
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
        print()
    
    # Validation requirements
    if report.validation_requirements:
        print("📋 VALIDATION REQUIREMENTS")
        print("-" * 40)
        for i, req in enumerate(report.validation_requirements, 1):
            print(f"{i}. {req}")
        print()
    
    # Academic readiness guidance
    print("🎓 ACADEMIC READINESS GUIDANCE")
    print("-" * 40)
    if report.academic_readiness:
        print("✅ This component meets basic academic standards.")
        print("   Ready for validation studies and publication consideration.")
    else:
        print("❌ This component does NOT meet academic standards.")
        print("   Significant improvements required before academic use.")
    
    print()
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Validate component quality using automated quality assurance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate prompt template:
    python validate_component.py --component-type prompt_template \\
        --file prompt_hierarchical_v2.txt \\
        --template-type hierarchical \\
        --framework-context framework_context.json

  Validate framework:
    python validate_component.py --component-type framework \\
        --file civic_virtue_framework.json \\
        --framework-name "Civic Virtue Framework" \\
        --theoretical-foundation theoretical_background.txt

  Validate weighting methodology:
    python validate_component.py --component-type weighting_methodology \\
        --file winner_take_most_v3.json \\
        --methodology-name "Enhanced Winner Take Most" \\
        --test-scenarios test_cases.json

  Validate component compatibility:
    python validate_component.py --component-type compatibility \\
        --prompt-file prompt.txt \\
        --framework-file framework.json \\
        --weighting-file weighting.json

  Export quality report:
    python validate_component.py --component-type prompt_template \\
        --file prompt.txt --export-report quality_report.json
        """
    )
    
    parser.add_argument(
        "--component-type",
        required=True,
        choices=["prompt_template", "framework", "weighting_methodology", "compatibility"],
        help="Type of component to validate"
    )
    
    parser.add_argument(
        "--file",
        help="Path to component file (required for single component validation)"
    )
    
    # Prompt template specific options
    parser.add_argument(
        "--template-type",
        default="hierarchical",
        choices=["standard", "hierarchical"],
        help="Type of prompt template (default: hierarchical)"
    )
    
    parser.add_argument(
        "--framework-context",
        help="Path to JSON file containing framework context for prompt validation"
    )
    
    # Framework specific options
    parser.add_argument(
        "--framework-name",
        help="Name of the framework being validated"
    )
    
    parser.add_argument(
        "--theoretical-foundation",
        help="Path to file containing theoretical foundation description"
    )
    
    # Weighting methodology specific options
    parser.add_argument(
        "--methodology-name",
        help="Name of the weighting methodology being validated"
    )
    
    parser.add_argument(
        "--test-scenarios",
        help="Path to JSON file containing test scenarios for weighting validation"
    )
    
    # Component compatibility options
    parser.add_argument(
        "--prompt-file",
        help="Path to prompt template file (for compatibility validation)"
    )
    
    parser.add_argument(
        "--framework-file",
        help="Path to framework file (for compatibility validation)"
    )
    
    parser.add_argument(
        "--weighting-file",
        help="Path to weighting methodology file (for compatibility validation)"
    )
    
    # Output options
    parser.add_argument(
        "--export-report",
        help="Export quality report to JSON file"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed output, only show summary"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = ComponentQualityValidator()
    
    # Validate based on component type
    try:
        if args.component_type == "prompt_template":
            if not args.file:
                print("❌ Error: --file is required for prompt template validation")
                sys.exit(1)
            
            template_content = load_file_content(args.file)
            
            framework_context = None
            if args.framework_context:
                framework_context = load_json_file(args.framework_context)
            
            report = validator.validate_prompt_template(
                template_content=template_content,
                template_type=args.template_type,
                framework_context=framework_context
            )
            
        elif args.component_type == "framework":
            if not args.file:
                print("❌ Error: --file is required for framework validation")
                sys.exit(1)
            
            framework_data = load_json_file(args.file)
            framework_name = args.framework_name or Path(args.file).stem
            
            theoretical_foundation = None
            if args.theoretical_foundation:
                theoretical_foundation = load_file_content(args.theoretical_foundation)
            
            report = validator.validate_framework(
                framework_data=framework_data,
                framework_name=framework_name,
                theoretical_foundation=theoretical_foundation
            )
            
        elif args.component_type == "weighting_methodology":
            if not args.file:
                print("❌ Error: --file is required for weighting methodology validation")
                sys.exit(1)
            
            methodology_data = load_json_file(args.file)
            methodology_name = args.methodology_name or Path(args.file).stem
            
            test_scenarios = None
            if args.test_scenarios:
                test_scenarios = load_json_file(args.test_scenarios)
            
            report = validator.validate_weighting_methodology(
                methodology_data=methodology_data,
                methodology_name=methodology_name,
                test_scenarios=test_scenarios
            )
            
        elif args.component_type == "compatibility":
            if not all([args.prompt_file, args.framework_file, args.weighting_file]):
                print("❌ Error: --prompt-file, --framework-file, and --weighting-file are required for compatibility validation")
                sys.exit(1)
            
            prompt_template = load_file_content(args.prompt_file)
            framework_data = load_json_file(args.framework_file)
            weighting_data = load_json_file(args.weighting_file)
            
            report = validator.validate_component_compatibility(
                prompt_template=prompt_template,
                framework_data=framework_data,
                weighting_data=weighting_data
            )
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        sys.exit(1)
    
    # Display results
    if not args.quiet:
        print_quality_report(report)
    else:
        # Quiet mode - just show summary
        print(f"Quality Score: {report.overall_score:.2f}")
        print(f"Quality Level: {report.overall_level.value}")
        print(f"Academic Ready: {report.academic_readiness}")
        print(f"Checks Passed: {len([c for c in report.checks if c.passed])}/{len(report.checks)}")
    
    # Export report if requested
    if args.export_report:
        try:
            # Convert report to dictionary for JSON serialization
            report_dict = {
                "component_type": report.component_type.value,
                "component_name": report.component_name,
                "version": report.version,
                "overall_score": report.overall_score,
                "overall_level": report.overall_level.value,
                "academic_readiness": report.academic_readiness,
                "checks": [
                    {
                        "check_name": check.check_name,
                        "passed": check.passed,
                        "score": check.score,
                        "message": check.message,
                        "recommendation": check.recommendation,
                        "severity": check.severity
                    }
                    for check in report.checks
                ],
                "recommendations": report.recommendations,
                "validation_requirements": report.validation_requirements
            }
            
            with open(args.export_report, 'w') as f:
                json.dump(report_dict, f, indent=2)
            
            print(f"📄 Quality report exported to: {args.export_report}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not export report: {e}")
    
    # Exit with appropriate code
    if report.overall_level in [QualityLevel.UNACCEPTABLE, QualityLevel.NEEDS_IMPROVEMENT]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main() 