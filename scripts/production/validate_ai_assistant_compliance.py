#!/usr/bin/env python3
"""
AI Assistant Compliance Validator

Validates that AI assistant suggestions follow mandatory project rules.
Designed to catch violations before they cause problems.

Usage:
    python3 scripts/production/validate_ai_assistant_compliance.py --check-suggestion "build new QA system"
    python3 scripts/production/validate_ai_assistant_compliance.py --audit-recent-changes
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any

class AIAssistantComplianceValidator:
    """Validates AI assistant compliance with project rules."""
    
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.project_root = Path(__file__).parent.parent.parent
        
        # Forbidden patterns that indicate rule violations
        self.forbidden_patterns = {
            "deprecated_usage": [
                "AI Academic Advisor",
                "architectural_compliance_validator",
                "deprecated/",
                "archive/",
                "# DEPRECATED"
            ],
            "direct_production_building": [
                "create new file in src/",
                "build in scripts/",
                "new system in src/"
            ],
            "rebuilding_existing": [
                "build new QA system",
                "create quality assurance",
                "new validation system",
                "rebuild experiment",
                "replace existing"
            ]
        }
        
        # Required production systems that should be referenced
        self.production_systems = {
            "quality_assurance": [
                "LLMQualityAssuranceSystem",
                "ComponentQualityValidator",
                "src/narrative_gravity/utils/llm_quality_assurance.py"
            ],
            "experiment_execution": [
                "execute_experiment_definition.py",
                "comprehensive_experiment_orchestrator.py",
                "DeclarativeExperimentExecutor"
            ],
            "data_export": [
                "QAEnhancedDataExporter",
                "AcademicAnalysisPipeline",
                "src/narrative_gravity/academic/"
            ]
        }
    
    def check_suggestion_compliance(self, suggestion: str) -> Tuple[bool, List[str], List[str]]:
        """Check if a suggestion complies with project rules."""
        violations = []
        warnings = []
        suggestion_lower = suggestion.lower()
        
        # Check for forbidden patterns
        for category, patterns in self.forbidden_patterns.items():
            for pattern in patterns:
                if pattern.lower() in suggestion_lower:
                    violations.append(f"VIOLATION: {category} - Contains forbidden pattern: '{pattern}'")
        
        # Check for building without searching
        build_keywords = ["build", "create", "develop", "implement", "add new"]
        search_keywords = ["check_existing_systems", "search first", "existing system"]
        
        has_build_intent = any(keyword in suggestion_lower for keyword in build_keywords)
        has_search_reference = any(keyword in suggestion_lower for keyword in search_keywords)
        
        if has_build_intent and not has_search_reference:
            violations.append("VIOLATION: Building suggestion without mandatory production search")
        
        # Check for references to production systems when appropriate
        for category, systems in self.production_systems.items():
            category_keywords = {
                "quality_assurance": ["quality", "validation", "qa", "assurance"],
                "experiment_execution": ["experiment", "execution", "orchestrator"],
                "data_export": ["export", "data", "academic"]
            }
            
            if any(keyword in suggestion_lower for keyword in category_keywords.get(category, [])):
                if not any(system.lower() in suggestion_lower for system in systems):
                    warnings.append(f"WARNING: {category} mentioned but no production system referenced")
        
        is_compliant = len(violations) == 0
        return is_compliant, violations, warnings
    
    def audit_recent_file_changes(self) -> Tuple[bool, List[str]]:
        """Audit recent file changes for compliance violations."""
        violations = []
        
        try:
            # Check for new files in wrong locations
            result = subprocess.run(
                ["find", ".", "-name", "*.py", "-newer", ".ai_assistant_rules.md"],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.stdout:
                new_files = result.stdout.strip().split('\n')
                for file_path in new_files:
                    if file_path.startswith('./src/') and 'experimental' not in file_path:
                        violations.append(f"VIOLATION: New file in production without experimental testing: {file_path}")
                    
                    if 'deprecated' in file_path:
                        violations.append(f"VIOLATION: New file in deprecated directory: {file_path}")
            
        except Exception as e:
            violations.append(f"ERROR: Could not audit file changes: {e}")
        
        return len(violations) == 0, violations
    
    def check_production_search_performed(self) -> bool:
        """Check if production search was performed recently."""
        try:
            # Check if check_existing_systems.py was run recently
            search_script = self.project_root / "scripts/production/check_existing_systems.py"
            if search_script.exists():
                # This is a simple heuristic - in practice you might want more sophisticated tracking
                return True
        except Exception:
            pass
        
        return False
    
    def generate_compliance_report(self, suggestion: str = None) -> str:
        """Generate a comprehensive compliance report."""
        report = []
        report.append("🛡️ AI ASSISTANT COMPLIANCE REPORT")
        report.append("=" * 50)
        
        overall_compliant = True
        
        if suggestion:
            compliant, violations, warnings = self.check_suggestion_compliance(suggestion)
            overall_compliant &= compliant
            
            report.append(f"\n📝 SUGGESTION ANALYSIS:")
            report.append(f"Suggestion: {suggestion[:100]}...")
            report.append(f"Compliant: {'✅ YES' if compliant else '❌ NO'}")
            
            if violations:
                report.append(f"\n❌ VIOLATIONS ({len(violations)}):")
                for violation in violations:
                    report.append(f"  • {violation}")
            
            if warnings:
                report.append(f"\n⚠️ WARNINGS ({len(warnings)}):")
                for warning in warnings:
                    report.append(f"  • {warning}")
        
        # Check file changes
        files_compliant, file_violations = self.audit_recent_file_changes()
        overall_compliant &= files_compliant
        
        if file_violations:
            report.append(f"\n📁 FILE CHANGE VIOLATIONS:")
            for violation in file_violations:
                report.append(f"  • {violation}")
        
        # Overall status
        report.append(f"\n🎯 OVERALL COMPLIANCE: {'✅ COMPLIANT' if overall_compliant else '❌ NON-COMPLIANT'}")
        
        if not overall_compliant:
            report.append(f"\n🔧 REQUIRED ACTIONS:")
            report.append(f"1. Review .ai_assistant_rules.md")
            report.append(f"2. Run: python3 scripts/production/check_existing_systems.py")
            report.append(f"3. Use existing production systems instead of rebuilding")
            report.append(f"4. Move new development to experimental/ first")
        
        return "\n".join(report)

def validate_orchestrator_usage(suggestion_text: str) -> Dict[str, Any]:
    """
    🚨 CRITICAL: Prevent AI assistants from suggesting custom scripts!
    
    This function detects violations of the "orchestrator-first" rule where
    AI assistants suggest custom scripts for experiment tasks that should
    use the production orchestrator.
    """
    suggestion_lower = suggestion_text.lower()
    
    # Red flags: Custom script suggestions
    custom_script_flags = [
        "create a script", "write a script", "custom script", "new script",
        "standalone script", "separate script", "python script for",
        "let's create", "build a script", "script to handle",
        "quick script", "simple script", "statistical analysis script",
        "data extraction script", "analysis script", "experiment script"
    ]
    
    # Green flags: Orchestrator usage
    orchestrator_flags = [
        "comprehensive_experiment_orchestrator", "orchestrator", 
        "enhanced_analysis_pipeline", "experiment transaction",
        "resume from checkpoint", "transaction-safe",
        "use the orchestrator", "orchestrator handles"
    ]
    
    # Critical violations: Statistical analysis in custom scripts
    statistical_violations = [
        "statistical analysis script", "hypothesis testing script",
        "data analysis script", "statistical script", "stats script",
        "analysis outside orchestrator", "custom statistical"
    ]
    
    violations = []
    red_flag_count = 0
    green_flag_count = 0
    
    # Check for custom script violations
    for flag in custom_script_flags:
        if flag in suggestion_lower:
            violations.append(f"❌ CUSTOM SCRIPT SUGGESTION: '{flag}' - Use orchestrator instead!")
            red_flag_count += 1
    
    # Check for statistical analysis violations (critical)
    for violation in statistical_violations:
        if violation in suggestion_lower:
            violations.append(f"🚨 CRITICAL VIOLATION: '{violation}' - Statistics are built into orchestrator!")
            red_flag_count += 2  # Double weight for statistical violations
    
    # Check for orchestrator usage (good!)
    for flag in orchestrator_flags:
        if flag in suggestion_lower:
            green_flag_count += 1
    
    # Determine compliance level
    if red_flag_count > 0 and green_flag_count == 0:
        compliance_level = "VIOLATION"
        compliance_score = 0
    elif red_flag_count > green_flag_count:
        compliance_level = "POOR"
        compliance_score = 25
    elif green_flag_count > 0 and red_flag_count == 0:
        compliance_level = "EXCELLENT"
        compliance_score = 100
    elif green_flag_count > red_flag_count:
        compliance_level = "GOOD"
        compliance_score = 75
    else:
        compliance_level = "ACCEPTABLE"
        compliance_score = 50
    
    return {
        "orchestrator_compliance": {
            "compliance_level": compliance_level,
            "compliance_score": compliance_score,
            "red_flags": red_flag_count,
            "green_flags": green_flag_count,
            "violations": violations,
            "recommendation": _get_orchestrator_recommendation(compliance_level)
        }
    }

def _get_orchestrator_recommendation(compliance_level: str) -> str:
    """Get recommendation based on orchestrator compliance level"""
    recommendations = {
        "VIOLATION": "🚨 STOP! Use comprehensive_experiment_orchestrator.py instead of custom scripts! It includes complete statistical analysis, visualization, and academic export systems.",
        "POOR": "⚠️ Prefer the production orchestrator over custom scripts. The orchestrator handles experiments as atomic transactions with full statistical analysis built-in.",
        "ACCEPTABLE": "✅ Good direction, but emphasize orchestrator usage more. All experiment work should go through the transaction-safe orchestrator.",
        "GOOD": "✅ Great orchestrator usage! The transaction-safe approach prevents lost work and provides complete analysis pipelines.",
        "EXCELLENT": "🎯 Perfect! Using the orchestrator correctly for all experiment work. This prevents custom script proliferation and ensures complete analysis."
    }
    return recommendations.get(compliance_level, "Use the orchestrator for all experiment work.")

def main():
    parser = argparse.ArgumentParser(
        description="Validate AI assistant compliance with project rules"
    )
    
    parser.add_argument("--check-suggestion", 
                       help="Check if a specific suggestion complies with rules")
    parser.add_argument("--audit-recent-changes", action="store_true",
                       help="Audit recent file changes for compliance")
    parser.add_argument("--quick-check", action="store_true",
                       help="Quick compliance status check")
    
    args = parser.parse_args()
    
    validator = AIAssistantComplianceValidator()
    
    if args.quick_check:
        print("🔍 Quick Compliance Check:")
        print("✅ Rules file exists:", Path(".ai_assistant_rules.md").exists())
        print("✅ Production search tool exists:", 
              Path("scripts/production/check_existing_systems.py").exists())
        print("✅ Systems inventory exists:", 
              Path("docs/EXISTING_SYSTEMS_INVENTORY.md").exists())
        return
    
    if args.check_suggestion:
        suggestion = args.check_suggestion
        
        # Run standard compliance check
        report = validator.generate_compliance_report(suggestion)
        print(report)
        
        # Run orchestrator compliance check (CRITICAL)
        orchestrator_compliance = validate_orchestrator_usage(suggestion)
        orch_result = orchestrator_compliance["orchestrator_compliance"]
        
        print(f"\n🎯 ORCHESTRATOR COMPLIANCE: {orch_result['compliance_level']} ({orch_result['compliance_score']}%)")
        if orch_result["violations"]:
            for violation in orch_result["violations"]:
                print(f"   {violation}")
        print(f"💡 {orch_result['recommendation']}")
        
        # Exit with error code if non-compliant
        exit_code = 0
        if "❌ NON-COMPLIANT" in report:
            exit_code = 1
        if orch_result['compliance_level'] in ["VIOLATION", "POOR"]:
            exit_code = 1
            print("\n🚨 CRITICAL: Custom script suggestions violate orchestrator-first rule!")
            print("🔧 CORRECTIVE ACTION REQUIRED:")
            print("   • Use comprehensive_experiment_orchestrator.py for ALL experiment work")
            print("   • Statistical analysis is built into the orchestrator pipeline")
            print("   • Checkpoint/resume prevents losing expensive LLM analysis work")
            print("   • Never suggest custom scripts for experiment tasks")
        
        sys.exit(exit_code)
    
    elif args.audit_recent_changes:
        report = validator.generate_compliance_report()
        print(report)
        
        if "❌ NON-COMPLIANT" in report:
            sys.exit(1)
    
    else:
        print("Usage: Specify --check-suggestion or --audit-recent-changes")
        print("See --help for more options")

if __name__ == "__main__":
    main() 