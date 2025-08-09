#!/usr/bin/env python3
"""
THIN Architecture Compliance Checker
====================================

Automated validation of THIN architectural principles for Cursor agent discipline.
Designed to be run before commits to catch architectural violations early.
"""

import os
import sys
import ast
import yaml
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class THINComplianceChecker:
    """Automated THIN architecture compliance validation."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.violations = []
        
    def check_component_size(self, file_path: Path) -> List[str]:
        """Check if components are under 150 lines (THIN Principle)."""
        violations = []
        
        if file_path.suffix == '.py' and 'agents/' in str(file_path):
            try:
                lines = file_path.read_text().splitlines()
                # Remove comments and empty lines for accurate count
                code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                
                if len(code_lines) > 150:
                    violations.append(f"THIN VIOLATION: {file_path} has {len(code_lines)} code lines (>150 limit)")
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_yaml_externalization(self, file_path: Path) -> List[str]:
        """Check for inline prompts that should be externalized to YAML."""
        violations = []
        
        if file_path.suffix == '.py':
            try:
                content = file_path.read_text()
                
                # Check for common inline prompt patterns
                inline_patterns = [
                    'prompt = """',
                    'prompt = "',
                    'system_prompt = """',
                    'system_prompt = "',
                    'template = """',
                    'instruction = """'
                ]
                
                for pattern in inline_patterns:
                    if pattern in content:
                        violations.append(f"YAML EXTERNALIZATION VIOLATION: {file_path} contains inline prompt: {pattern}")
                        
                # Check if corresponding YAML file exists for agent files
                if 'agents/' in str(file_path) and file_path.name not in ['__init__.py']:
                    yaml_path = file_path.parent / 'prompt.yaml'
                    if not yaml_path.exists():
                        violations.append(f"MISSING YAML: {file_path} should have corresponding prompt.yaml file")
                        
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_parsing_complexity(self, file_path: Path) -> List[str]:
        """Check for complex parsing logic that violates THIN principles."""
        violations = []
        
        if file_path.suffix == '.py':
            try:
                content = file_path.read_text()
                
                # Patterns indicating complex parsing
                complex_parsing_patterns = [
                    'json.loads(',
                    'json.dumps(',
                    'regex.findall(',
                    're.search(',
                    're.findall(',
                    '.split()',
                    '.replace(',
                    'BeautifulSoup(',
                    'lxml.etree',
                    'xml.etree'
                ]
                
                parsing_count = sum(1 for pattern in complex_parsing_patterns if pattern in content)
                
                if parsing_count > 3:  # Allow minimal parsing, flag excessive
                    violations.append(f"PARSING COMPLEXITY VIOLATION: {file_path} has {parsing_count} parsing operations (consider LLM envelope extraction)")
                    
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_framework_agnosticism(self, file_path: Path) -> List[str]:
        """Check for framework-specific hardcoding."""
        violations = []
        
        if file_path.suffix == '.py' and 'orchestration' in str(file_path):
            try:
                content = file_path.read_text()
                
                # Framework-specific patterns that indicate hardcoding
                framework_patterns = [
                    'caf_',
                    'chf_',
                    'ecf_',
                    'cff_',
                    'pdaf_',
                    'moral_foundations',
                    'populist_rhetoric',
                    'civic_character'
                ]
                
                for pattern in framework_patterns:
                    if pattern.lower() in content.lower():
                        violations.append(f"FRAMEWORK HARDCODING VIOLATION: {file_path} contains framework-specific code: {pattern}")
                        
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_academic_integrity_patterns(self, file_path: Path) -> List[str]:
        """Check for academic integrity violations."""
        violations = []
        
        if file_path.suffix == '.py':
            try:
                content = file_path.read_text()
                
                # Patterns indicating LLM mathematical calculations (forbidden)
                llm_math_patterns = [
                    'calculate',
                    'compute',
                    'sum(',
                    'mean(',
                    'std(',
                    'correlation',
                    'regression',
                    'statistical'
                ]
                
                # Check if file contains LLM math without MathToolkit
                if any(pattern in content.lower() for pattern in llm_math_patterns):
                    if 'MathToolkit' not in content and 'math_toolkit' not in content:
                        violations.append(f"ACADEMIC INTEGRITY VIOLATION: {file_path} may contain LLM mathematical calculations without MathToolkit verification")
                        
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_infrastructure_patterns(self, file_path: Path) -> List[str]:
        """Check for proper infrastructure integration."""
        violations = []
        
        if file_path.suffix == '.py' and 'agents/' in str(file_path) and file_path.name not in ['__init__.py']:
            try:
                content = file_path.read_text()
                
                # Required infrastructure patterns
                required_patterns = {
                    'LLMGateway': 'LLMGateway integration required for all agents',
                    'AuditLogger': 'AuditLogger integration required for provenance',
                    'ModelRegistry': 'ModelRegistry required for multi-model support'
                }
                
                for pattern, message in required_patterns.items():
                    if pattern not in content:
                        violations.append(f"INFRASTRUCTURE VIOLATION: {file_path} missing {pattern} - {message}")
                        
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def run_compliance_check(self, target_path: Optional[Path] = None) -> Tuple[bool, List[str]]:
        """Run comprehensive THIN compliance check."""
        if target_path:
            files_to_check = [target_path] if target_path.is_file() else list(target_path.rglob('*.py'))
        else:
            # Check key directories
            files_to_check = []
            for directory in ['discernus/agents/', 'discernus/core/', 'discernus/orchestration/']:
                dir_path = self.project_root / directory
                if dir_path.exists():
                    files_to_check.extend(dir_path.rglob('*.py'))
        
        all_violations = []
        
        for file_path in files_to_check:
            # Skip test files and __pycache__
            if '__pycache__' in str(file_path) or '/tests/' in str(file_path):
                continue
                
            violations = []
            violations.extend(self.check_component_size(file_path))
            violations.extend(self.check_yaml_externalization(file_path))
            violations.extend(self.check_parsing_complexity(file_path))
            violations.extend(self.check_framework_agnosticism(file_path))
            violations.extend(self.check_academic_integrity_patterns(file_path))
            violations.extend(self.check_infrastructure_patterns(file_path))
            
            all_violations.extend(violations)
        
        return len(all_violations) == 0, all_violations

def main():
    """Main entry point for compliance checking."""
    project_root = Path(__file__).parent.parent
    checker = THINComplianceChecker(project_root)
    
    target = None
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if not target.exists():
            print(f"ERROR: Target path {target} does not exist")
            sys.exit(1)
    
    print("🔍 Running THIN Architecture Compliance Check...")
    
    is_compliant, violations = checker.run_compliance_check(target)
    
    if is_compliant:
        print("✅ THIN COMPLIANCE: All checks passed!")
        sys.exit(0)
    else:
        print(f"❌ THIN VIOLATIONS FOUND: {len(violations)} issues detected\n")
        
        for violation in violations:
            print(f"  • {violation}")
        
        print(f"\n📋 NEXT STEPS:")
        print(f"  1. Review docs/developer/CURSOR_AGENT_DISCIPLINE_GUIDE.md")
        print(f"  2. Fix violations following THIN architectural principles")
        print(f"  3. Re-run: python3 scripts/thin_compliance_check.py")
        
        sys.exit(1)

if __name__ == '__main__':
    main()
