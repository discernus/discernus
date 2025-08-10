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
        """Check if components follow tiered THIN limits based on complexity."""
        violations = []
        
        if file_path.suffix == '.py' and 'agents/' in str(file_path):
            try:
                lines = file_path.read_text().splitlines()
                # Remove comments and empty lines for accurate count
                code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                
                # Tiered THIN limits based on agent complexity
                agent_name = file_path.stem
                limit, category = self._get_thin_limit(file_path, agent_name)
                
                if len(code_lines) > limit:
                    violations.append(f"THIN VIOLATION ({category}): {file_path} has {len(code_lines)} code lines (>{limit} limit for {category})")
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def _get_thin_limit(self, file_path: Path, agent_name: str) -> tuple[int, str]:
        """Get appropriate THIN limit based on agent complexity."""
        
        # Simple Wrapper Agents (LLM prompt + basic coordination)
        simple_agents = ['raw_data_analysis_planner', 'derived_metrics_analysis_planner', 
                        'evidence_indexer_agent', 'classification_agent', 'csv_export_agent']
        
        # Core Processing Agents (Single major responsibility)
        core_agents = ['enhanced_analysis_agent', 'intelligent_extractor_agent', 
                      'experiment_coherence_agent', 'evidence_quality_measurement']
        
        # Complex Integration Agents (Multiple data types, caching, RAG)
        complex_agents = ['comprehensive_knowledge_curator', 'txtai_evidence_curator',
                         'evidence_curator', 'rag_enhanced_interpreter']
        
        # Orchestration Agents (Pipeline coordination)
        orchestration_agents = ['pipeline', 'investigative_synthesis_agent']
        
        if any(simple in str(file_path).lower() for simple in simple_agents):
            return 200, "Simple Agent"  # Allow reasonable implementation space
        elif any(core in str(file_path).lower() for core in core_agents):
            return 400, "Core Agent"    # Single responsibility with infrastructure
        elif any(complex in str(file_path).lower() for complex in complex_agents):
            return 600, "Complex Agent" # Multiple integrations, justified complexity
        elif any(orch in str(file_path).lower() for orch in orchestration_agents):
            return 800, "Orchestration Agent"  # Pipeline coordination complexity
        else:
            return 200, "Default Agent"  # Conservative default
    
    def check_yaml_externalization(self, file_path: Path) -> List[str]:
        """Check for inline prompts that should be externalized to YAML."""
        violations = []
        
        if file_path.suffix == '.py':
            try:
                content = file_path.read_text()
                lines = content.splitlines()
                
                # Check for actual inline prompt patterns (not print statements or comments)
                inline_prompt_count = 0
                
                for line_num, line in enumerate(lines, 1):
                    stripped = line.strip()
                    
                    # Skip comments, print statements, logging, and error messages
                    if (stripped.startswith('#') or
                        stripped.startswith('print(') or
                        'logging.' in stripped or
                        'logger.' in stripped or
                        'raise ' in stripped or
                        'f"' in stripped):  # Skip f-strings used for formatting
                        continue
                    
                    # Look for actual inline prompt patterns
                    inline_patterns = [
                        'prompt = """',
                        'prompt = "',
                        'system_prompt = """',
                        'system_prompt = "',
                        'template = """',
                        'instruction = """',
                        'user_prompt = """',
                        'user_prompt = "'
                    ]
                    
                    for pattern in inline_patterns:
                        if pattern in stripped:
                            inline_prompt_count += 1
                            violations.append(f"YAML EXTERNALIZATION VIOLATION: {file_path}:{line_num} contains inline prompt: {pattern}")
                
                # Check if corresponding YAML file exists for agent files (but be more selective)
                if ('agents/' in str(file_path) and 
                    file_path.name not in ['__init__.py'] and
                    file_path.name == 'agent.py'):  # Only check main agent files
                    yaml_path = file_path.parent / 'prompt.yaml'
                    if not yaml_path.exists():
                        # Only flag if the agent actually uses LLM calls
                        if ('llm_gateway' in content.lower() or 'execute_call' in content):
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
                lines = content.splitlines()
                
                # Only check for actual complex parsing patterns in context
                complex_parsing_count = 0
                
                for line_num, line in enumerate(lines, 1):
                    stripped = line.strip()
                    
                    # Skip imports, comments, print statements, and basic operations
                    if (stripped.startswith('import ') or 
                        stripped.startswith('from ') or
                        stripped.startswith('#') or
                        stripped.startswith('print(') or
                        'logging.' in stripped or
                        'logger.' in stripped):
                        continue
                    
                    # Look for actual complex parsing patterns
                    if any(pattern in stripped for pattern in [
                        're.search(',
                        're.findall(',
                        're.sub(',
                        'BeautifulSoup(',
                        'lxml.etree',
                        'xml.etree'
                    ]):
                        complex_parsing_count += 1
                    
                    # Check for multi-step JSON parsing with error handling
                    if 'json.loads(' in stripped and ('try:' in content or 'except' in content):
                        # This could be complex if it's part of multi-strategy parsing
                        context_lines = lines[max(0, line_num-3):min(len(lines), line_num+3)]
                        context = '\n'.join(context_lines)
                        if ('regex' in context.lower() or 'fallback' in context.lower() or 
                            'strategy' in context.lower()):
                            complex_parsing_count += 1
                
                if complex_parsing_count > 2:  # Allow some parsing, flag excessive patterns
                    violations.append(f"PARSING COMPLEXITY VIOLATION: {file_path} has {complex_parsing_count} complex parsing operations (consider LLM envelope extraction)")
                    
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
                
                # Only check agent files that actually do LLM calls
                if 'agents/' not in str(file_path):
                    return violations
                
                # Patterns indicating LLM mathematical calculations (forbidden)
                # Only flag if LLM is being asked to do math without MathToolkit
                suspicious_patterns = []
                
                # Look for prompts that ask LLMs to do math
                if ('execute_call' in content and 
                    any(pattern in content.lower() for pattern in [
                        'calculate the', 'compute the', 'find the mean', 'find the correlation',
                        'statistical analysis', 'regression analysis', 'anova'
                    ])):
                    if 'MathToolkit' not in content and 'math_toolkit' not in content:
                        suspicious_patterns.append("LLM mathematical calculation requests")
                
                if suspicious_patterns:
                    violations.append(f"ACADEMIC INTEGRITY VIOLATION: {file_path} may contain LLM mathematical calculations without MathToolkit verification: {', '.join(suspicious_patterns)}")
                        
            except Exception as e:
                violations.append(f"ERROR: Could not analyze {file_path}: {e}")
                
        return violations
    
    def check_infrastructure_patterns(self, file_path: Path) -> List[str]:
        """Check for proper infrastructure integration."""
        violations = []
        
        # Only check main agent files that actually perform LLM operations
        if (file_path.suffix == '.py' and 
            'agents/' in str(file_path) and 
            file_path.name == 'agent.py'):  # Only main agent files
            
            try:
                content = file_path.read_text()
                
                # Only check infrastructure if the agent actually uses LLM calls
                if not ('execute_call' in content or 'llm_gateway' in content.lower()):
                    return violations  # Skip non-LLM agents
                
                # Required infrastructure patterns for LLM agents
                required_patterns = {
                    'LLMGateway': 'LLMGateway integration required for all LLM agents',
                    'AuditLogger': 'AuditLogger integration required for provenance'
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
