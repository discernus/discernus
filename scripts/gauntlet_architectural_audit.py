#!/usr/bin/env python3
"""
Gauntlet Architectural Audit Script

This script enhances gauntlet testing to detect experiment-specific code and architectural violations.
It should be run as part of the gauntlet testing protocol to ensure experiment agnosticism.
"""

import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set
import sys

class ArchitecturalAuditor:
    """Audit system for detecting experiment-specific code and architectural violations."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.violations = []
        self.framework_keywords = {
            'civic_character': ['dignity', 'fantasy', 'fear', 'hope', 'justice', 'manipulation', 'pragmatism', 'resentment', 'tribalism', 'truth'],
            'constitutional_health': ['constitutional', 'health', 'democracy', 'institutions'],
            'populist_rhetoric': ['populist', 'populism', 'elite', 'people', 'establishment'],
            'sentiment': ['sentiment', 'positive_sentiment', 'negative_sentiment', 'net_sentiment'],
            'business_ethics': ['ethics', 'corporate', 'stakeholder', 'responsibility'],
            'framing': ['framing', 'entman', 'lakoff']  # Removed 'frame' - too generic
        }
        
        self.experiment_names = [
            'nano_test_experiment', 'micro_test_experiment', '1a_caf_civic_character',
            '1b_chf_constitutional_health', '2a_populist_rhetoric_study', 'business_ethics_experiment',
            'entman_framing_experiment', 'lakoff_framing_experiment'
        ]
    
    def audit_core_system(self) -> List[Dict[str, Any]]:
        """Audit the core system for experiment-specific code."""
        violations = []
        
        # Check core Python files
        core_files = [
            'discernus/core/clean_analysis_orchestrator.py',
            'discernus/agents/experiment_coherence_agent/agent.py',
            'discernus/agents/automated_derived_metrics/agent.py',
            'discernus/agents/automated_statistical_analysis/agent.py',
            'discernus/agents/unified_synthesis_agent/agent.py'
        ]
        
        for file_path in core_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                violations.extend(self._audit_file(full_path, 'core_system'))
        
        return violations
    
    def audit_agent_prompts(self) -> List[Dict[str, Any]]:
        """Audit agent prompts for framework-specific content."""
        violations = []
        
        # Check all agent prompt files
        agents_dir = self.project_root / 'discernus' / 'agents'
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                prompt_files = list(agent_dir.glob('*.yaml')) + list(agent_dir.glob('*.txt'))
                for prompt_file in prompt_files:
                    violations.extend(self._audit_file(prompt_file, 'agent_prompt'))
        
        return violations
    
    def audit_test_files(self) -> List[Dict[str, Any]]:
        """Audit test files for hardcoded experiment references."""
        violations = []
        
        # Check test files for hardcoded experiment names
        test_dir = self.project_root / 'discernus' / 'tests'
        for test_file in test_dir.rglob('*.py'):
            violations.extend(self._audit_file(test_file, 'test_file'))
        
        return violations
    
    def _audit_file(self, file_path: Path, file_type: str) -> List[Dict[str, Any]]:
        """Audit a single file for architectural violations."""
        violations = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return [{
                'type': 'file_read_error',
                'file': str(file_path),
                'error': str(e),
                'severity': 'warning'
            }]
        
        # Check for framework-specific keywords
        for framework, keywords in self.framework_keywords.items():
            for keyword in keywords:
                if keyword in content.lower():
                    # Check if it's in a comment or test data (acceptable)
                    if not self._is_acceptable_usage(content, keyword):
                        violations.append({
                            'type': 'framework_specific_keyword',
                            'file': str(file_path),
                            'keyword': keyword,
                            'framework': framework,
                            'file_type': file_type,
                            'severity': 'high' if file_type == 'core_system' else 'medium'
                        })
        
        # Check for hardcoded experiment names
        for exp_name in self.experiment_names:
            if exp_name in content:
                if not self._is_acceptable_usage(content, exp_name):
                    violations.append({
                        'type': 'hardcoded_experiment_name',
                        'file': str(file_path),
                        'experiment_name': exp_name,
                        'file_type': file_type,
                        'severity': 'high' if file_type == 'core_system' else 'medium'
                    })
        
        # Check for hardcoded paths
        if '/projects/' in content and file_type == 'core_system':
            violations.append({
                'type': 'hardcoded_project_path',
                'file': str(file_path),
                'file_type': file_type,
                'severity': 'high'
            })
        
        return violations
    
    def _is_acceptable_usage(self, content: str, keyword: str) -> bool:
        """Check if keyword usage is acceptable (in comments, tests, or documentation)."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                # Check if it's in a comment
                if line.strip().startswith('#') or line.strip().startswith('//'):
                    continue
                # Check if it's in a docstring
                if '"""' in line or "'''" in line:
                    continue
                # Check if it's in test data
                if 'test' in line.lower() or 'mock' in line.lower():
                    continue
                # Check if it's in a string literal (acceptable)
                if f'"{keyword}"' in line or f"'{keyword}'" in line:
                    continue
                # Check if it's part of a larger word (e.g., "framework" contains "frame")
                if keyword.lower() != line.lower():
                    # Check if it's part of a compound word
                    if f'framework' in line.lower() and keyword.lower() == 'frame':
                        continue
                    if f'dataframe' in line.lower() and keyword.lower() == 'frame':
                        continue
                    if f'inframe' in line.lower() and keyword.lower() == 'frame':
                        continue
                # Otherwise, it's a violation
                return False
        return True
    
    def audit_log_output(self, log_content: str) -> List[Dict[str, Any]]:
        """Audit log output for architectural violations."""
        violations = []
        
        # Check for framework-specific keywords in logs
        for framework, keywords in self.framework_keywords.items():
            for keyword in keywords:
                if keyword in log_content.lower():
                    violations.append({
                        'type': 'framework_keyword_in_logs',
                        'keyword': keyword,
                        'framework': framework,
                        'severity': 'high'
                    })
        
        # Check for hardcoded experiment names in logs
        for exp_name in self.experiment_names:
            if exp_name in log_content:
                violations.append({
                    'type': 'experiment_name_in_logs',
                    'experiment_name': exp_name,
                    'severity': 'medium'
                })
        
        # Check for error patterns that suggest framework-specific code
        error_patterns = [
            r'KeyError.*dignity|truth|justice|sentiment',
            r'AttributeError.*civic|populist|constitutional',
            r'NameError.*fantasy|fear|hope|manipulation'
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, log_content, re.IGNORECASE):
                violations.append({
                    'type': 'framework_specific_error',
                    'pattern': pattern,
                    'severity': 'high'
                })
        
        return violations
    
    def generate_report(self, violations: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive audit report."""
        if not violations:
            return "✅ ARCHITECTURAL AUDIT PASSED: No experiment-specific code detected."
        
        report = ["🔍 ARCHITECTURAL AUDIT REPORT", "=" * 50, ""]
        
        # Group violations by type
        by_type = {}
        for violation in violations:
            vtype = violation['type']
            if vtype not in by_type:
                by_type[vtype] = []
            by_type[vtype].append(violation)
        
        # Report by severity
        high_severity = [v for v in violations if v.get('severity') == 'high']
        medium_severity = [v for v in violations if v.get('severity') == 'medium']
        low_severity = [v for v in violations if v.get('severity') == 'low']
        
        if high_severity:
            report.append("🚨 HIGH SEVERITY VIOLATIONS:")
            for violation in high_severity:
                report.append(f"  • {violation['type']} in {violation.get('file', 'logs')}")
                if 'keyword' in violation:
                    report.append(f"    - Keyword: {violation['keyword']}")
                if 'framework' in violation:
                    report.append(f"    - Framework: {violation['framework']}")
            report.append("")
        
        if medium_severity:
            report.append("⚠️  MEDIUM SEVERITY VIOLATIONS:")
            for violation in medium_severity:
                report.append(f"  • {violation['type']} in {violation.get('file', 'logs')}")
            report.append("")
        
        if low_severity:
            report.append("ℹ️  LOW SEVERITY VIOLATIONS:")
            for violation in low_severity:
                report.append(f"  • {violation['type']} in {violation.get('file', 'logs')}")
            report.append("")
        
        # Summary
        report.append("SUMMARY:")
        report.append(f"  Total violations: {len(violations)}")
        report.append(f"  High severity: {len(high_severity)}")
        report.append(f"  Medium severity: {len(medium_severity)}")
        report.append(f"  Low severity: {len(low_severity)}")
        
        if high_severity:
            report.append("")
            report.append("❌ AUDIT FAILED: High severity violations must be fixed before alpha release.")
        elif medium_severity:
            report.append("")
            report.append("⚠️  AUDIT WARNING: Medium severity violations should be addressed.")
        else:
            report.append("")
            report.append("✅ AUDIT PASSED: No critical violations detected.")
        
        return "\n".join(report)

def main():
    """Main function to run architectural audit."""
    project_root = Path(__file__).parent.parent
    auditor = ArchitecturalAuditor(project_root)
    
    print("🔍 Running Architectural Audit...")
    print("=" * 50)
    
    # Run all audits
    all_violations = []
    all_violations.extend(auditor.audit_core_system())
    all_violations.extend(auditor.audit_agent_prompts())
    all_violations.extend(auditor.audit_test_files())
    
    # Generate and print report
    report = auditor.generate_report(all_violations)
    print(report)
    
    # Exit with appropriate code
    high_severity_count = len([v for v in all_violations if v.get('severity') == 'high'])
    if high_severity_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
