#!/usr/bin/env python3
"""
Discernus System Health CLI
Python wrapper for system health validation using the production orchestrator
"""

import sys
import subprocess
import argparse
from pathlib import Path

def main():
    """Main CLI entry point for system health checks"""
    
    parser = argparse.ArgumentParser(
        description="Discernus System Health Check",
        epilog="""
Examples:
  python3 scripts/cli/system_health.py                # Basic health check
  python3 scripts/cli/system_health.py --mode ci      # CI/CD pipeline check  
  python3 scripts/cli/system_health.py --mode release # Pre-release validation
  python3 scripts/cli/system_health.py --mode dev     # Developer onboarding
  python3 scripts/cli/system_health.py --dry-run      # Validation plan only
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--mode",
        choices=["basic", "ci", "release", "dev"],
        default="basic",
        help="System health check mode (default: basic)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show validation plan without execution"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to files"
    )
    
    args = parser.parse_args()
    
    # Build orchestrator command
    project_root = Path(__file__).parent.parent.parent
    orchestrator_path = project_root / "scripts" / "applications" / "comprehensive_experiment_orchestrator.py"
    experiment_path = project_root / "tests" / "system_health" / "test_experiments" / "system_health_test.yaml"
    
    if not orchestrator_path.exists():
        print("❌ Production orchestrator not found")
        return 1
    
    if not experiment_path.exists():
        print("❌ System health test experiment not found")
        return 1
    
    # Build command arguments
    cmd = [
        sys.executable,
        str(orchestrator_path),
        str(experiment_path),
        "--system-health-mode"
    ]
    
    if args.dry_run:
        cmd.append("--dry-run")
    
    if args.verbose or args.mode in ["release", "dev"]:
        cmd.append("--verbose")
    
    # Show what we're running
    mode_descriptions = {
        "basic": "Basic system health validation",
        "ci": "CI/CD system health validation", 
        "release": "Pre-release system health validation",
        "dev": "Developer onboarding system health check"
    }
    
    description = mode_descriptions[args.mode]
    if args.dry_run:
        description = "System health validation plan (dry-run)"
    
    print(f"🏥 Discernus System Health Check")
    print(f"Mode: {args.mode}")
    print(f"Description: {description}")
    print()
    print(f"Running: {' '.join(cmd)}")
    print()
    
    # Execute the orchestrator
    try:
        result = subprocess.run(cmd, cwd=project_root)
        
        if result.returncode == 0:
            print()
            if args.mode == "ci":
                print("✅ CI/CD: System health validation passed")
            elif args.mode == "release":
                print("🚀 RELEASE: System ready for deployment")
            elif args.mode == "dev":
                print("👋 Welcome! Your development environment is healthy")
            else:
                print("✅ System health check completed successfully")
        else:
            print()
            if args.mode == "ci":
                print("🚨 CI/CD: Build should be blocked due to system health issues")
            elif args.mode == "release":
                print("🛑 RELEASE: Do not deploy - system health issues detected")
            elif args.mode == "dev":
                print("Please fix system health issues before development")
            else:
                print("❌ System health check failed")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⏹️  System health check interrupted")
        return 1
    except Exception as e:
        print(f"❌ Failed to run system health check: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 