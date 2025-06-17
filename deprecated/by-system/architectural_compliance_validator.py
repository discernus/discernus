#!/usr/bin/env python3
"""
Architectural Compliance Validator
Implements Phase 13 of AI Academic Advisor Methodology v2.0

Validates that experiment results and analysis pipelines comply with architectural principles:
1. Production System Usage
2. Framework Boundary Compliance  
3. Memory Guidance Adherence
4. Downstream System Validation
5. Design Pattern Compliance
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from narrative_gravity.framework_manager import FrameworkManager

class ArchitecturalComplianceValidator:
    """Validates system compliance with architectural principles."""
    
    def __init__(self):
        """Initialize the validator."""
        self.violations = []
        self.warnings = []
        self.checks_passed = []
        
    def validate_experiment_results(self, experiment_path: str) -> Dict[str, Any]:
        """
        Comprehensive architectural compliance validation for experiment results.
        
        Args:
            experiment_path: Path to experiment results directory
            
        Returns:
            Compliance report with violations, warnings, and passed checks
        """
        print(f"🔍 Validating Architectural Compliance: {experiment_path}")
        print("=" * 70)
        
        experiment_dir = Path(experiment_path)
        
        # Reset validation state
        self.violations = []
        self.warnings = []
        self.checks_passed = []
        
        # Run all compliance checks
        self._check_framework_boundary_compliance(experiment_dir)
        self._check_production_system_usage(experiment_dir)
        self._check_visualization_engine_compliance(experiment_dir)
        self._check_data_extraction_compliance(experiment_dir)
        self._check_design_pattern_compliance(experiment_dir)
        self._check_content_quality_compliance(experiment_dir)
        
        # Generate compliance report
        return self._generate_compliance_report(experiment_dir)
    
    def _check_framework_boundary_compliance(self, experiment_dir: Path):
        """Check that data extraction respects framework well definitions."""
        print("\n🎯 Checking Framework Boundary Compliance...")
        
        try:
            # Find structured results
            results_file = experiment_dir / "enhanced_analysis" / "structured_results.json"
            if not results_file.exists():
                self.warnings.append("No structured_results.json found for boundary compliance check")
                return
                
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            # Get framework used
            frameworks_used = results.get('metadata', {}).get('frameworks_used', [])
            if not frameworks_used:
                self.violations.append("No framework information found in results metadata")
                return
                
            framework_name = frameworks_used[0]  # Use first framework
            
            # Load framework definition  
            framework_wells = self._get_framework_wells(framework_name)
            if not framework_wells:
                self.violations.append(f"Could not load wells for framework: {framework_name}")
                return
                
            # Check well columns in results
            well_columns = results.get('metadata', {}).get('well_columns', [])
            expected_wells = {f"well_{well.lower()}" for well in framework_wells}
            actual_wells = set(well_columns)
            
            # Check for violations
            extra_wells = actual_wells - expected_wells
            missing_wells = expected_wells - actual_wells
            
            if extra_wells:
                self.violations.append(
                    f"Framework boundary violation: Found {len(extra_wells)} wells not defined in {framework_name} framework: {extra_wells}"
                )
            
            if missing_wells:
                self.violations.append(
                    f"Framework boundary violation: Missing {len(missing_wells)} expected wells for {framework_name}: {missing_wells}"
                )
                
            if not extra_wells and not missing_wells:
                self.checks_passed.append(
                    f"✅ Framework boundary compliance: {framework_name} has exactly {len(expected_wells)} wells as expected"
                )
                
        except Exception as e:
            self.violations.append(f"Error checking framework boundary compliance: {str(e)}")
    
    def _check_production_system_usage(self, experiment_dir: Path):
        """Check that production systems are used instead of custom implementations."""
        print("🏭 Checking Production System Usage...")
        
        try:
            # Check for evidence of NarrativeGravityVisualizationEngine usage
            vis_files = list(experiment_dir.glob("**/*.png")) + list(experiment_dir.glob("**/*.html"))
            
            if vis_files:
                # Look for production engine artifacts
                html_files = [f for f in vis_files if f.suffix == '.html']
                
                # Check if HTML files contain production engine signatures
                production_signatures = ["NarrativeGravityVisualizationEngine", "narrative-gravity-theme"]
                has_production_signature = False
                
                for html_file in html_files:
                    try:
                        content = html_file.read_text()
                        if any(sig in content for sig in production_signatures):
                            has_production_signature = True
                            break
                    except:
                        continue
                
                if has_production_signature:
                    self.checks_passed.append("✅ Production visualization engine signatures found")
                else:
                    self.violations.append(
                        "Production system violation: Visualizations generated without production NarrativeGravityVisualizationEngine"
                    )
            else:
                self.warnings.append("No visualization files found to check production system usage")
                
        except Exception as e:
            self.violations.append(f"Error checking production system usage: {str(e)}")
    
    def _check_visualization_engine_compliance(self, experiment_dir: Path):
        """Check specific visualization engine compliance."""
        print("🎨 Checking Visualization Engine Compliance...")
        
        try:
            vis_dir = experiment_dir / "enhanced_analysis" / "visualizations"
            if not vis_dir.exists():
                self.warnings.append("No visualizations directory found")
                return
                
            # Look for custom matplotlib/seaborn artifacts (violations)
            custom_viz_indicators = [
                "plt.figure",
                "sns.heatmap", 
                "matplotlib.pyplot",
                "seaborn"
            ]
            
            # Check if any python files contain custom visualization code
            py_files = list(vis_dir.glob("**/*.py"))
            violations_found = False
            
            for py_file in py_files:
                content = py_file.read_text()
                found_indicators = [ind for ind in custom_viz_indicators if ind in content]
                if found_indicators:
                    violations_found = True
                    self.violations.append(
                        f"Visualization engine violation: Custom visualization code found in {py_file}: {found_indicators}"
                    )
            
            if not violations_found and py_files:
                self.checks_passed.append("✅ No custom visualization code found in visualization files")
                
        except Exception as e:
            self.violations.append(f"Error checking visualization engine compliance: {str(e)}")
    
    def _check_data_extraction_compliance(self, experiment_dir: Path):
        """Check that data extraction follows framework-aware patterns."""
        print("📊 Checking Data Extraction Compliance...")
        
        try:
            # Check if extraction code exists and is framework-aware
            extraction_indicators = [
                "_get_framework_wells",
                "framework_definition",
                "framework_aware"
            ]
            
            # Look in scripts and analysis files
            script_files = list(Path("scripts").glob("*extract*.py"))
            
            framework_aware_found = False
            for script_file in script_files:
                try:
                    content = script_file.read_text()
                    if any(indicator in content for indicator in extraction_indicators):
                        framework_aware_found = True
                        break
                except:
                    continue
            
            if framework_aware_found:
                self.checks_passed.append("✅ Framework-aware data extraction patterns found")
            else:
                self.violations.append(
                    "Data extraction violation: No evidence of framework-aware extraction patterns"
                )
                
        except Exception as e:
            self.violations.append(f"Error checking data extraction compliance: {str(e)}")
    
    def _check_design_pattern_compliance(self, experiment_dir: Path):
        """Check compliance with established design patterns."""
        print("🏗️ Checking Design Pattern Compliance...")
        
        try:
            # Check for proper directory structure
            required_dirs = ["enhanced_analysis"]
            missing_dirs = []
            
            for req_dir in required_dirs:
                if not (experiment_dir / req_dir).exists():
                    missing_dirs.append(req_dir)
            
            if missing_dirs:
                self.violations.append(f"Design pattern violation: Missing required directories: {missing_dirs}")
            else:
                self.checks_passed.append("✅ Required directory structure present")
                
            # Check for proper file naming conventions
            expected_files = [
                "structured_results.json",
                "statistical_results.json", 
                "enhanced_analysis_report.html"
            ]
            
            analysis_dir = experiment_dir / "enhanced_analysis"
            missing_files = []
            
            for exp_file in expected_files:
                if not (analysis_dir / exp_file).exists():
                    missing_files.append(exp_file)
            
            if missing_files:
                self.warnings.append(f"Design pattern warning: Missing expected files: {missing_files}")
            else:
                self.checks_passed.append("✅ Expected file naming conventions followed")
                
        except Exception as e:
            self.violations.append(f"Error checking design pattern compliance: {str(e)}")
    
    def _check_content_quality_compliance(self, experiment_dir: Path):
        """Check that HTML reports and outputs accurately reflect actual analysis results."""
        print("🔍 Checking Content Quality Compliance...")
        
        try:
            analysis_dir = experiment_dir / "enhanced_analysis"
            if not analysis_dir.exists():
                self.warnings.append("No enhanced_analysis directory found for content quality check")
                return
            
            # Check HTML report accuracy vs actual statistical results
            html_file = analysis_dir / "enhanced_analysis_report.html"
            stats_file = analysis_dir / "statistical_results.json"
            
            if html_file.exists() and stats_file.exists():
                # Read HTML content
                html_content = html_file.read_text()
                
                # Read statistical results
                with open(stats_file, 'r') as f:
                    stats_data = json.load(f)
                
                # Check statistical tests count accuracy
                actual_hypothesis_tests = len(stats_data.get('hypothesis_testing', {}))
                if "Statistical Tests:</strong> 0" in html_content and actual_hypothesis_tests > 0:
                    self.violations.append(
                        f"Content quality violation: HTML reports 0 statistical tests but {actual_hypothesis_tests} were actually performed"
                    )
                elif actual_hypothesis_tests > 0:
                    self.checks_passed.append(f"✅ HTML report statistical tests count appears accurate")
                
                # Check visualization count accuracy
                vis_dir = analysis_dir / "visualizations"
                if vis_dir.exists():
                    actual_viz_count = len(list(vis_dir.glob("*.png")))
                    if "Visualizations:</strong> 0" in html_content and actual_viz_count > 0:
                        self.violations.append(
                            f"Content quality violation: HTML reports 0 visualizations but {actual_viz_count} PNG files exist"
                        )
                    elif actual_viz_count > 0:
                        self.checks_passed.append(f"✅ HTML report visualization count appears accurate")
            
            # Check for framework loading errors in any log files or outputs
            log_indicators = [
                "'FrameworkManager' object has no attribute 'load_framework'",
                "Could not load framework",
                "Framework loading failed"
            ]
            
            framework_errors_found = False
            for log_file in experiment_dir.glob("**/*.log"):
                try:
                    content = log_file.read_text()
                    for indicator in log_indicators:
                        if indicator in content:
                            framework_errors_found = True
                            self.violations.append(
                                f"Content quality violation: Framework loading error detected in {log_file.name}: {indicator}"
                            )
                            break
                except:
                    continue
            
            if not framework_errors_found:
                self.checks_passed.append("✅ No framework loading errors detected in logs")
            
            # Check visualization richness (look for coordinate system indicators)
            if vis_dir.exists():
                rich_viz_indicators = [
                    "coordinate",
                    "circular",
                    "narrative_gravity",
                    "wells_"
                ]
                
                basic_viz_detected = False
                viz_files = list(vis_dir.glob("*.png"))
                
                # This is a heuristic - check if we have very small/basic looking files
                for viz_file in viz_files:
                    file_size = viz_file.stat().st_size
                    if file_size < 20000:  # Less than 20KB suggests basic plot
                        basic_viz_detected = True
                
                if basic_viz_detected and len(viz_files) > 0:
                    self.warnings.append(
                        "Content quality warning: Some visualization files appear to be basic/small - may indicate missing rich coordinate visualizations"
                    )
                elif len(viz_files) > 0:
                    self.checks_passed.append("✅ Visualization files appear to have reasonable complexity")
                    
        except Exception as e:
            self.violations.append(f"Error checking content quality compliance: {str(e)}")
    
    def _get_framework_wells(self, framework_name: str) -> List[str]:
        """Get the list of wells defined for a specific framework."""
        try:
            framework_path = Path("frameworks") / framework_name / "framework_consolidated.json"
            
            if framework_path.exists():
                with open(framework_path, 'r') as f:
                    framework_data = json.load(f)
                
                wells = []
                dipoles = framework_data.get('dipoles', [])
                for dipole in dipoles:
                    if isinstance(dipole, dict):
                        if 'positive' in dipole and 'negative' in dipole:
                            wells.append(dipole['positive']['name'])
                            wells.append(dipole['negative']['name'])
                
                return wells
                
        except Exception as e:
            print(f"Error loading framework {framework_name}: {e}")
            
        return []
    
    def _generate_compliance_report(self, experiment_dir: Path) -> Dict[str, Any]:
        """Generate comprehensive compliance report."""
        
        total_checks = len(self.violations) + len(self.warnings) + len(self.checks_passed)
        compliance_score = len(self.checks_passed) / max(total_checks, 1) * 100
        
        # Determine compliance level
        if len(self.violations) == 0:
            if len(self.warnings) == 0:
                compliance_level = "FULLY_COMPLIANT"
            else:
                compliance_level = "COMPLIANT_WITH_WARNINGS"
        else:
            compliance_level = "NON_COMPLIANT"
        
        print(f"\n🏆 Architectural Compliance Report")
        print("=" * 50)
        print(f"Compliance Level: {compliance_level}")
        print(f"Compliance Score: {compliance_score:.1f}%")
        print(f"Violations: {len(self.violations)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Checks Passed: {len(self.checks_passed)}")
        
        # Print details
        if self.violations:
            print(f"\n❌ VIOLATIONS ({len(self.violations)}):")
            for i, violation in enumerate(self.violations, 1):
                print(f"  {i}. {violation}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if self.checks_passed:
            print(f"\n✅ PASSED CHECKS ({len(self.checks_passed)}):")
            for i, check in enumerate(self.checks_passed, 1):
                print(f"  {i}. {check}")
        
        report = {
            "experiment_path": str(experiment_dir),
            "validation_timestamp": datetime.now().isoformat(),
            "compliance_level": compliance_level,
            "compliance_score": compliance_score,
            "violations": self.violations,
            "warnings": self.warnings,
            "checks_passed": self.checks_passed,
            "total_checks": total_checks
        }
        
        return report

def main():
    """Main entry point for architectural compliance validation."""
    if len(sys.argv) != 2:
        print("Usage: python3 architectural_compliance_validator.py <experiment_path>")
        sys.exit(1)
    
    experiment_path = sys.argv[1]
    
    validator = ArchitecturalComplianceValidator()
    report = validator.validate_experiment_results(experiment_path)
    
    # Save report
    report_path = Path(experiment_path) / "architectural_compliance_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Compliance report saved: {report_path}")
    
    # Exit with appropriate code
    if report["compliance_level"] == "NON_COMPLIANT":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 