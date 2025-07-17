#!/usr/bin/env python3
"""
THIN Architecture Validation and Self-Documentation
==================================================

This module makes it easier to do the right thing and harder to do the wrong thing
when working with THIN architecture. It provides:

1. Runtime validation of THIN principles
2. Self-documenting examples embedded in code  
3. Clear error messages that guide toward correct usage
4. Template patterns for common tasks

THIN PRINCIPLES REMINDER:
- Software provides minimal routing infrastructure only
- LLMs handle ALL intelligence decisions  
- NO parsing or interpretation of LLM responses
- Raw text passing between LLMs
- Prompts separated from orchestration logic

USAGE:
    from discernus.core.thin_validation import validate_thin_code, ThinHelper
    
    # Validate your code follows THIN principles
    validate_thin_code(your_function)
    
    # Get examples of THIN patterns
    ThinHelper.show_expert_pattern()
"""

import inspect
import re
import warnings
from typing import Dict, List, Any, Callable
from pathlib import Path

class THINViolationWarning(UserWarning):
    """Warning raised when code violates THIN principles"""
    pass

class ThinValidator:
    """Validates code against THIN principles"""
    
    # Anti-patterns that violate THIN principles
    THICK_PATTERNS = {
        'llm_parsing': [
            r'json\.loads.*response',
            r'parse.*llm.*response', 
            r'extract.*from.*response',
            r'if.*response\.contains',
            r'response\.split\(',
        ],
        'hardcoded_intelligence': [
            r'if.*expert_name.*==.*:',
            r'elif.*agent.*type',
            r'switch.*on.*llm.*type',
            r'hardcoded.*prompt',
        ],
        'complex_orchestration': [
            r'parse.*llm.*decision',
            r'interpret.*response',
            r'analyze.*llm.*output',
            r'process.*llm.*result',
        ]
    }
    
    # THIN patterns that should be encouraged
    THIN_PATTERNS = {
        'clean_separation': [
            r'get_expert_prompt\(',
            r'get_role_prompt\(',
            r'raw.*text.*passing',
            r'llm_client\.call_llm\(',
        ],
        'minimal_routing': [
            r'request.*to.*expert',
            r'pass.*directly.*to.*llm',
            r'no.*interpretation',
            r'minimal.*orchestration',
        ]
    }

    def validate_function(self, func: Callable) -> Dict[str, Any]:
        """Validate a function against THIN principles
        
        Returns:
            Dict with validation results, violations, and recommendations
        """
        source = inspect.getsource(func)
        results = {
            'function_name': func.__name__,
            'is_thin': True,
            'violations': [],
            'recommendations': [],
            'thin_patterns_found': [],
            'score': 0.0
        }
        
        # Check for THICK anti-patterns
        for category, patterns in self.THICK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, source, re.IGNORECASE):
                    results['violations'].append({
                        'category': category,
                        'pattern': pattern,
                        'description': self._get_violation_description(category)
                    })
                    results['is_thin'] = False
        
        # Check for THIN patterns
        for category, patterns in self.THIN_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, source, re.IGNORECASE):
                    results['thin_patterns_found'].append({
                        'category': category,
                        'pattern': pattern
                    })
        
        # Calculate THIN score (0.0 = THICK, 1.0 = THIN)
        total_patterns = len(results['violations']) + len(results['thin_patterns_found'])
        if total_patterns > 0:
            results['score'] = len(results['thin_patterns_found']) / total_patterns
        else:
            results['score'] = 0.5  # Neutral if no patterns found
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _get_violation_description(self, category: str) -> str:
        """Get human-readable description of violation"""
        descriptions = {
            'llm_parsing': "Parsing LLM responses violates THIN - use raw text passing",
            'hardcoded_intelligence': "Hardcoded logic violates THIN - move intelligence to LLM prompts",
            'complex_orchestration': "Complex response processing violates THIN - keep orchestration minimal"
        }
        return descriptions.get(category, "Unknown violation type")
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on violations"""
        recommendations = []
        
        violation_categories = [v['category'] for v in results['violations']]
        
        if 'llm_parsing' in violation_categories:
            recommendations.append("Use raw text passing instead of parsing LLM responses")
            recommendations.append("Let receiving LLM interpret the response directly")
        
        if 'hardcoded_intelligence' in violation_categories:
            recommendations.append("Move decision logic to LLM prompts using get_expert_prompt()")
            recommendations.append("Use prompt templates in agent_roles.py instead of hardcoded prompts")
        
        if 'complex_orchestration' in violation_categories:
            recommendations.append("Simplify orchestration - just route messages between LLMs")
            recommendations.append("Let LLMs handle all interpretation and decision-making")
        
        if results['score'] < 0.3:
            recommendations.append("Consider major refactoring to follow THIN principles")
        elif results['score'] < 0.7:
            recommendations.append("Some improvements needed to be fully THIN")
        
        return recommendations

class ThinHelper:
    """Provides examples and templates for THIN patterns"""
    
    @staticmethod
    def show_expert_pattern():
        """Show the correct pattern for adding expert agents"""
        example = '''
# ✅ CORRECT THIN PATTERN for adding expert agents:

# 1. Add expert to agent_roles.py:
EXPERT_AGENT_PROMPTS['my_new_expert'] = """
You are a my_new_expert, specializing in:
- Your specific expertise area
- Another expertise area

RESEARCH QUESTION: {research_question}
SOURCE TEXTS: {source_texts}
MODERATOR REQUEST: {expert_request}

Your Task:
[Specific instructions for this expert]
"""

# 2. Use in orchestrator (automatically works):
expert_prompt = get_expert_prompt(
    expert_name='my_new_expert',
    research_question=config.research_question, 
    source_texts=config.source_texts,
    expert_request=expert_request
)

# 3. That's it! No orchestrator code changes needed.
'''
        print(example)
    
    @staticmethod
    def show_thin_orchestration_pattern():
        """Show the correct pattern for THIN orchestration"""
        example = '''
# ✅ CORRECT THIN ORCHESTRATION PATTERN:

# 1. Get prompt using THIN system
prompt = get_expert_prompt(expert_name, research_question, source_texts, request)

# 2. Call LLM with raw text
response = llm_client.call_llm(prompt, expert_name)

# 3. Pass response directly to next LLM (NO PARSING!)
next_prompt = f"Previous analysis: {response}\\n\\nYour task: ..."
next_response = llm_client.call_llm(next_prompt, next_expert)

# ❌ WRONG - DON'T DO THIS:
# parsed_data = json.loads(response)  # THICK!
# if parsed_data['sentiment'] == 'positive':  # THICK!
#     next_action = 'analyze_further'  # THICK!
'''
        print(example)
    
    @staticmethod
    def validate_project_structure() -> Dict[str, Any]:
        """Validate overall project follows THIN principles"""
        project_root = Path(__file__).parent.parent.parent
        results = {
            'is_thin': True,
            'issues': [],
            'recommendations': []
        }
        
        # Check for prompt separation
        llm_roles_file = project_root / "discernus/core/agent_roles.py"
        if not llm_roles_file.exists():
            results['is_thin'] = False
            results['issues'].append("Missing agent_roles.py - prompts should be separated")
        
        # Check orchestrator size (should be minimal)
        orchestrator_file = project_root / "discernus/orchestration/orchestrator.py"
        if orchestrator_file.exists():
            lines = len(orchestrator_file.read_text().splitlines())
            if lines > 800:  # Arbitrary threshold
                results['issues'].append(f"Orchestrator is {lines} lines - consider if it's getting THICK")
        
        # Check for anti-pattern files
        anti_pattern_names = ['llm_parser.py', 'response_interpreter.py', 'complex_orchestrator.py']
        for name in anti_pattern_names:
            if (project_root / f"discernus/core/{name}").exists():
                results['is_thin'] = False
                results['issues'].append(f"Found {name} - suggests THICK patterns")
        
        if not results['is_thin']:
            results['recommendations'].append("Review files and refactor to follow THIN principles")
            results['recommendations'].append("Move intelligence to LLM prompts, not Python code")
        
        return results

def validate_thin_code(func: Callable) -> None:
    """Validate a function follows THIN principles and warn if not
    
    Example:
        @validate_thin_code
        def my_orchestration_function():
            # Your code here
            pass
    """
    validator = ThinValidator()
    results = validator.validate_function(func)
    
    if not results['is_thin']:
        violation_summary = ', '.join([v['category'] for v in results['violations']])
        warnings.warn(
            f"Function {func.__name__} violates THIN principles: {violation_summary}. "
            f"Recommendations: {'; '.join(results['recommendations'])}",
            THINViolationWarning,
            stacklevel=2
        )
    
    return results

def check_thin_compliance() -> None:
    """Check overall project THIN compliance and print report"""
    print("🔍 THIN Architecture Compliance Check")
    print("=" * 40)
    
    # Check project structure
    structure_results = ThinHelper.validate_project_structure()
    print(f"📁 Project Structure: {'✅ THIN' if structure_results['is_thin'] else '❌ THICK'}")
    
    if structure_results['issues']:
        print("   Issues:")
        for issue in structure_results['issues']:
            print(f"   - {issue}")
    
    if structure_results['recommendations']:
        print("   Recommendations:")
        for rec in structure_results['recommendations']:
            print(f"   - {rec}")
    
    print()
    print("💡 Quick THIN Reminders:")
    print("   - Prompts in agent_roles.py, not orchestrator code")
    print("   - Raw text passing between LLMs")
    print("   - No parsing or interpretation of LLM responses")
    print("   - LLMs handle ALL intelligence decisions")
    print()
    print("📚 Get examples: ThinHelper.show_expert_pattern()")

if __name__ == "__main__":
    # Self-test
    check_thin_compliance() 