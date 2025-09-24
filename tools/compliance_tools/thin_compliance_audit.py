#!/usr/bin/env python3
"""
THIN Architecture Compliance Audit
==================================

Audits the Discernus agent ecosystem for THIN architecture compliance:
- Externalized YAML prompts
- Minimal parsing logic
- Agent architecture patterns
- Redundant/obsolete agents

Usage: python3 scripts/thin_compliance_audit.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime

@dataclass
class ComplianceViolation:
    agent_name: str
    violation_type: str
    description: str
    file_path: str
    line_number: int = 0
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL

class THINComplianceAuditor:
    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir
        self.violations: List[ComplianceViolation] = []
        
        # Patterns indicating THIN violations
        self.parsing_patterns = [
            (r'json\.loads\(', 'JSON parsing'),
            (r'\.split\(', 'String splitting'),
            (r'regex\.|re\.', 'Regex parsing'),
            (r'\.strip\(\)\.split\(', 'Complex string manipulation'),
            (r'content\.split\(', 'Content parsing'),
            (r'response\.split\(', 'Response parsing'),
            (r'\.replace\(.*\)\.split\(', 'Multi-step parsing'),
        ]
        
        self.inline_prompt_patterns = [
            (r'f["\'].*{.*}.*["\']', 'F-string prompts'),
            (r'""".*{.*}.*"""', 'Triple-quoted prompts with variables'),
            (r'".*\n.*"', 'Multi-line string prompts'),
        ]

    def audit_all_agents(self) -> Dict[str, List[ComplianceViolation]]:
        """Run comprehensive THIN compliance audit."""
        print("🔍 Starting THIN Architecture Compliance Audit...")
        
        # Find all agent directories
        agent_dirs = [d for d in self.agents_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        results = {}
        for agent_dir in agent_dirs:
            agent_name = agent_dir.name
            print(f"   Auditing {agent_name}...")
            
            violations = self.audit_agent(agent_dir)
            if violations:
                results[agent_name] = violations
                
        return results

    def audit_agent(self, agent_dir: Path) -> List[ComplianceViolation]:
        """Audit a single agent for THIN compliance."""
        violations = []
        agent_name = agent_dir.name
        
        # Check for YAML externalization
        yaml_files = list(agent_dir.glob('*.yaml')) + list(agent_dir.glob('*.yml'))
        py_files = list(agent_dir.glob('*.py'))
        
        if not yaml_files and py_files:
            violations.append(ComplianceViolation(
                agent_name=agent_name,
                violation_type="MISSING_YAML",
                description="No YAML prompt files found",
                file_path=str(agent_dir),
                severity="HIGH"
            ))
        
        # Check Python files for parsing violations
        for py_file in py_files:
            violations.extend(self.audit_python_file(py_file, agent_name))
            
        return violations

    def audit_python_file(self, py_file: Path, agent_name: str) -> List[ComplianceViolation]:
        """Audit a Python file for THIN violations."""
        violations = []
        
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            violations.append(ComplianceViolation(
                agent_name=agent_name,
                violation_type="FILE_ERROR",
                description=f"Could not read file: {e}",
                file_path=str(py_file),
                severity="LOW"
            ))
            return violations
        
        # Check for parsing violations
        for line_num, line in enumerate(lines, 1):
            for pattern, description in self.parsing_patterns:
                if re.search(pattern, line):
                    violations.append(ComplianceViolation(
                        agent_name=agent_name,
                        violation_type="EXCESSIVE_PARSING",
                        description=f"{description}: {line.strip()}",
                        file_path=str(py_file),
                        line_number=line_num,
                        severity="MEDIUM"
                    ))
            
            # Check for inline prompts
            for pattern, description in self.inline_prompt_patterns:
                if re.search(pattern, line) and len(line.strip()) > 50:
                    violations.append(ComplianceViolation(
                        agent_name=agent_name,
                        violation_type="INLINE_PROMPTS",
                        description=f"{description}: {line.strip()[:100]}...",
                        file_path=str(py_file),
                        line_number=line_num,
                        severity="HIGH"
                    ))
        
        # Check for complex parsing methods
        if 'def parse_' in content or 'def extract_' in content:
            violations.append(ComplianceViolation(
                agent_name=agent_name,
                violation_type="COMPLEX_PARSING_METHODS",
                description="Contains parse_* or extract_* methods",
                file_path=str(py_file),
                severity="MEDIUM"
            ))
        
        return violations

    def identify_redundant_agents(self) -> List[Tuple[str, str, List[str]]]:
        """Identify potentially redundant or obsolete agents."""
        redundancies = []
        
        # Evidence system redundancy
        evidence_agents = []
        curator_agents = []
        
        for agent_dir in self.agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue
                
            name = agent_dir.name.lower()
            if 'evidence' in name:
                evidence_agents.append(agent_dir.name)
            if 'curator' in name or 'curation' in name:
                curator_agents.append(agent_dir.name)
        
        if len(evidence_agents) > 2:
            redundancies.append(("Evidence System", "Multiple evidence agents", evidence_agents))
            
        if len(curator_agents) > 2:
            redundancies.append(("Curation System", "Multiple curator agents", curator_agents))
        
        return redundancies

    def generate_report(self, results: Dict[str, List[ComplianceViolation]]) -> str:
        """Generate comprehensive compliance report."""
        report_lines = [
            "# THIN Architecture Compliance Audit Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Executive Summary",
        ]
        
        total_violations = sum(len(violations) for violations in results.values())
        critical_violations = sum(1 for violations in results.values() 
                                for v in violations if v.severity == "CRITICAL")
        high_violations = sum(1 for violations in results.values() 
                            for v in violations if v.severity == "HIGH")
        
        report_lines.extend([
            f"- **Total Violations**: {total_violations}",
            f"- **Critical Violations**: {critical_violations}",
            f"- **High Priority Violations**: {high_violations}",
            f"- **Agents Audited**: {len([d for d in self.agents_dir.iterdir() if d.is_dir()])}",
            f"- **Non-Compliant Agents**: {len(results)}",
            ""
        ])
        
        # Violation breakdown by type
        violation_types = defaultdict(int)
        for violations in results.values():
            for v in violations:
                violation_types[v.violation_type] += 1
        
        report_lines.extend([
            "## Violation Breakdown",
            ""
        ])
        
        for violation_type, count in sorted(violation_types.items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"- **{violation_type}**: {count} violations")
        
        report_lines.append("")
        
        # Detailed agent violations
        report_lines.extend([
            "## Detailed Agent Analysis",
            ""
        ])
        
        for agent_name, violations in sorted(results.items()):
            report_lines.extend([
                f"### {agent_name}",
                f"**Violations**: {len(violations)}",
                ""
            ])
            
            for v in violations:
                severity_emoji = {"CRITICAL": "🚨", "HIGH": "⚠️", "MEDIUM": "🔸", "LOW": "ℹ️"}.get(v.severity, "•")
                report_lines.append(f"{severity_emoji} **{v.violation_type}**: {v.description}")
                if v.line_number:
                    report_lines.append(f"   📍 {v.file_path}:{v.line_number}")
                else:
                    report_lines.append(f"   📍 {v.file_path}")
            
            report_lines.append("")
        
        # Redundancy analysis
        redundancies = self.identify_redundant_agents()
        if redundancies:
            report_lines.extend([
                "## Redundant Agent Analysis",
                ""
            ])
            
            for category, description, agents in redundancies:
                report_lines.extend([
                    f"### {category}",
                    f"**Issue**: {description}",
                    f"**Agents**: {', '.join(agents)}",
                    ""
                ])
        
        return "\n".join(report_lines)


def main():
    from datetime import datetime
    
    # Find agents directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    agents_dir = project_root / "discernus" / "agents"
    
    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        return 1
    
    # Run audit
    auditor = THINComplianceAuditor(agents_dir)
    results = auditor.audit_all_agents()
    
    # Generate report
    report = auditor.generate_report(results)
    
    # Save report
    report_file = project_root / "THIN_COMPLIANCE_AUDIT.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📊 Audit Complete!")
    print(f"📋 Report saved to: {report_file}")
    print(f"🔍 Total violations: {sum(len(v) for v in results.values())}")
    print(f"🏗️ Non-compliant agents: {len(results)}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
