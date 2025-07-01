#!/usr/bin/env python3
"""
Framework Prompting Validation Script
=====================================

Validates frameworks for LLM-optimized prompting patterns according to
Framework Specification v3.2 guidelines.

Usage:
    python3 scripts/validate_framework_prompting.py path/to/framework.yaml
    python3 scripts/validate_framework_prompting.py 1_docs/frameworks/3_2_spec_frameworks/
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


class PromptingValidator:
    """Validates framework prompting for LLM optimization"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.suggestions = []
    
    def validate_framework(self, framework_path: str) -> Dict[str, Any]:
        """Validate a single framework file"""
        print(f"🔍 Validating: {framework_path}")
        
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                framework = yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load framework: {e}")
            return self._create_result(framework_path)
        
        # Check for prompting architecture
        prompt_guidance = framework.get('prompt_guidance', {})
        if not prompt_guidance:
            self.errors.append("No prompt_guidance section found")
            return self._create_result(framework_path)
        
        # Validate five-phase architecture
        self._validate_phase_structure(prompt_guidance)
        
        # Validate language consistency
        self._validate_language_consistency(prompt_guidance)
        
        # Validate forward references
        self._validate_forward_references(prompt_guidance, framework)
        
        # Validate cognitive flow
        self._validate_cognitive_flow(prompt_guidance)
        
        # Check for anti-patterns
        self._check_anti_patterns(prompt_guidance)
        
        return self._create_result(framework_path)
    
    def _validate_phase_structure(self, prompt_guidance: Dict[str, Any]):
        """Validate five-phase prompting architecture"""
        required_phases = [
            'role_definition',          # Phase 1: Cognitive priming
            'framework_summary_instructions',  # Phase 2: Framework methodology  
            'analysis_methodology',     # Phase 4: Detailed instructions
            'scoring_requirements',     # Phase 4: Scoring precision
            'json_format_instructions'  # Phase 5: Output format
        ]
        
        missing_phases = []
        for phase in required_phases:
            if phase not in prompt_guidance:
                missing_phases.append(phase)
        
        if missing_phases:
            self.errors.append(f"Missing required prompting phases: {missing_phases}")
        else:
            print("  ✅ Five-phase architecture complete")
    
    def _validate_language_consistency(self, prompt_guidance: Dict[str, Any]):
        """Validate consistent language usage"""
        languages_detected = {}
        
        for section, content in prompt_guidance.items():
            if isinstance(content, str):
                # Simple language detection heuristics
                if re.search(r'\bVocê\b|\bé\b|\bde\b|\bem\b', content):
                    languages_detected[section] = 'Portuguese'
                elif re.search(r'\bYou\b|\bare\b|\bof\b|\bin\b', content):
                    languages_detected[section] = 'English'
                else:
                    languages_detected[section] = 'Unknown'
        
        # Check for consistency
        unique_languages = set(languages_detected.values())
        if len(unique_languages) > 1:
            self.warnings.append(f"Language inconsistency detected: {languages_detected}")
            self.suggestions.append("Use consistent language throughout all prompting elements")
        else:
            primary_language = list(unique_languages)[0] if unique_languages else 'Unknown'
            print(f"  ✅ Language consistency: {primary_language}")
    
    def _validate_forward_references(self, prompt_guidance: Dict[str, Any], framework: Dict[str, Any]):
        """Check for forward references in early phases"""
        role_definition = prompt_guidance.get('role_definition', '')
        framework_instructions = prompt_guidance.get('framework_summary_instructions', '')
        
        # Check if early phases reference framework components
        components = framework.get('components', {})
        component_ids = list(components.keys()) if components else []
        
        early_content = role_definition + ' ' + framework_instructions
        
        forward_refs = []
        for comp_id in component_ids:
            if comp_id in early_content:
                forward_refs.append(comp_id)
        
        # Check for language_cues references
        if 'language_cues' in early_content:
            forward_refs.append('language_cues')
        
        if forward_refs:
            self.warnings.append(f"Possible forward references in early phases: {forward_refs}")
            self.suggestions.append("Move component-specific details to detailed_analysis_instructions")
        else:
            print("  ✅ No forward references in early phases")
    
    def _validate_cognitive_flow(self, prompt_guidance: Dict[str, Any]):
        """Validate cognitive processing flow"""
        role_def = prompt_guidance.get('role_definition', '')
        
        # Check if role definition is too technical
        technical_terms = ['angle', 'component_id', 'language_cues', 'score', 'JSON']
        technical_count = sum(1 for term in technical_terms if term in role_def)
        
        if technical_count > 2:
            self.warnings.append("Role definition too technical - should focus on domain expertise")
            self.suggestions.append("Move technical details to later phases")
        
        # Check for complete JSON examples
        json_instructions = prompt_guidance.get('json_format_instructions', '')
        if '```json' not in json_instructions:
            self.warnings.append("No complete JSON example provided")
            self.suggestions.append("Include complete JSON structure with realistic examples")
        else:
            print("  ✅ Complete JSON examples provided")
    
    def _check_anti_patterns(self, prompt_guidance: Dict[str, Any]):
        """Check for common anti-patterns"""
        all_content = ' '.join(str(v) for v in prompt_guidance.values() if isinstance(v, str))
        
        # Anti-pattern 1: Fragmented information
        total_length = len(all_content)
        if total_length < 500:
            self.warnings.append("Prompting content seems insufficient (<500 chars)")
            self.suggestions.append("Provide more comprehensive analysis guidance")
        
        # Anti-pattern 2: Missing evidence requirements
        if 'evidence' not in all_content and 'citação' not in all_content:
            self.warnings.append("No evidence requirements specified")
            self.suggestions.append("Require textual evidence in output format")
        
        # Anti-pattern 3: Vague scoring instructions
        if 'decimal' not in all_content and 'precisos' not in all_content:
            self.warnings.append("Vague scoring instructions")
            self.suggestions.append("Specify precise decimal scoring requirements")
    
    def _create_result(self, framework_path: str) -> Dict[str, Any]:
        """Create validation result summary"""
        return {
            'framework_path': framework_path,
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy(),
            'suggestions': self.suggestions.copy(),
            'passed': len(self.errors) == 0
        }
    
    def print_summary(self, result: Dict[str, Any]):
        """Print validation summary"""
        path = result['framework_path']
        
        if result['passed']:
            print(f"✅ {path}: PASSED")
        else:
            print(f"❌ {path}: FAILED")
        
        if result['errors']:
            print("  🚨 ERRORS:")
            for error in result['errors']:
                print(f"    • {error}")
        
        if result['warnings']:
            print("  ⚠️  WARNINGS:")
            for warning in result['warnings']:
                print(f"    • {warning}")
        
        if result['suggestions']:
            print("  💡 SUGGESTIONS:")
            for suggestion in result['suggestions']:
                print(f"    • {suggestion}")
        
        print()


def validate_file(file_path: str) -> Dict[str, Any]:
    """Validate a single framework file"""
    validator = PromptingValidator()
    result = validator.validate_framework(file_path)
    validator.print_summary(result)
    return result


def validate_directory(dir_path: str) -> List[Dict[str, Any]]:
    """Validate all YAML files in a directory"""
    directory = Path(dir_path)
    results = []
    
    yaml_files = list(directory.rglob("*.yaml")) + list(directory.rglob("*.yml"))
    
    print(f"🔍 Found {len(yaml_files)} YAML files in {dir_path}")
    print("=" * 60)
    
    for yaml_file in yaml_files:
        result = validate_file(str(yaml_file))
        results.append(result)
    
    # Print overall summary
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print("=" * 60)
    print(f"📊 OVERALL SUMMARY: {passed}/{total} frameworks passed validation")
    
    if passed < total:
        print(f"❌ {total - passed} frameworks need attention")
    else:
        print("✅ All frameworks follow LLM-optimized prompting patterns!")
    
    return results


def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python3 validate_framework_prompting.py <path>")
        print("  <path> can be a framework YAML file or directory")
        sys.exit(1)
    
    target_path = sys.argv[1]
    path_obj = Path(target_path)
    
    print("🧠 Framework Prompting Validation Script")
    print("📋 Checking for LLM-Optimized Prompting Patterns")
    print("=" * 60)
    
    if path_obj.is_file():
        if path_obj.suffix.lower() in ['.yaml', '.yml']:
            validate_file(target_path)
        else:
            print(f"❌ Error: {target_path} is not a YAML file")
            sys.exit(1)
    elif path_obj.is_dir():
        validate_directory(target_path)
    else:
        print(f"❌ Error: {target_path} does not exist")
        sys.exit(1)


if __name__ == "__main__":
    main() 