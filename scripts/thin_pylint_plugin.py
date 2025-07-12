#!/usr/bin/env python3
"""
THIN Pylint Plugin - Catches THICK patterns in linting
=====================================================

Custom pylint plugin that detects THICK antipatterns and reports them
as linting errors in VSCode/Cursor.
"""

import ast
import re
from typing import Union
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

class THINChecker(BaseChecker):
    """Pylint checker for THIN architecture compliance"""
    
    __implements__ = IAstroidChecker
    
    name = 'thin-compliance'
    
    msgs = {
        'W9001': (
            'THICK: Regex import detected - use LLM for parsing instead',
            'thick-regex-import',
            'Replace regex parsing with llm_client.call_llm() calls'
        ),
        'W9002': (
            'THICK: Content processing function "%s" - use LLM calls instead',
            'thick-content-processing',
            'Use llm_client.call_llm() for content processing instead of custom functions'
        ),
        'W9003': (
            'THICK: Complex conditional logic (%d if/elif statements) - use LLM logic instead',
            'thick-complex-logic',
            'Use LLM calls for complex decision making instead of conditional logic'
        ),
        'W9004': (
            'THICK: String manipulation "%s" detected - use LLM formatting instead',
            'thick-string-manipulation',
            'Use LLM calls for string processing instead of manual manipulation'
        ),
        'W9005': (
            'THICK: HTML/XML parsing import - use LLM for extraction instead',
            'thick-html-xml-parsing',
            'Use LLM calls for content extraction instead of parsing libraries'
        ),
        'W9006': (
            'THICK: Function too long (%d lines) - keep under 50 lines',
            'thick-function-too-long',
            'Break large functions into smaller THIN orchestration functions'
        ),
        'W9007': (
            'THICK: Missing LLM usage in content processing function',
            'thick-missing-llm-usage',
            'Functions that process content should use llm_client.call_llm()'
        )
    }
    
    def visit_import(self, node):
        """Check for THICK imports"""
        # Check for regex imports
        for alias in node.names:
            if alias[0] in ('re', 'regex'):
                self.add_message('thick-regex-import', node=node)
            
            # Check for parsing library imports
            if alias[0] in ('bs4', 'beautifulsoup4', 'lxml', 'html.parser'):
                self.add_message('thick-html-xml-parsing', node=node)
    
    def visit_importfrom(self, node):
        """Check for THICK from imports"""
        if node.modname in ('re', 'regex'):
            self.add_message('thick-regex-import', node=node)
        
        if node.modname in ('bs4', 'xml.etree', 'html.parser'):
            self.add_message('thick-html-xml-parsing', node=node)
    
    def visit_functiondef(self, node):
        """Check function definitions for THICK patterns"""
        # Check for THICK function names
        thick_prefixes = ['parse_', 'extract_', 'validate_', 'analyze_', 'process_']
        for prefix in thick_prefixes:
            if node.name.startswith(prefix):
                self.add_message('thick-content-processing', node=node, args=(node.name,))
                break
        
        # Check function length
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            func_length = node.end_lineno - node.lineno
            if func_length > 50:
                self.add_message('thick-function-too-long', node=node, args=(func_length,))
        
        # Check for complex conditional logic
        if_count = self._count_if_statements(node)
        if if_count > 3:
            self.add_message('thick-complex-logic', node=node, args=(if_count,))
        
        # Check for missing LLM usage in content processing functions
        if any(node.name.startswith(prefix) for prefix in thick_prefixes):
            if not self._has_llm_usage(node):
                self.add_message('thick-missing-llm-usage', node=node)
    
    def visit_call(self, node):
        """Check function calls for THICK patterns"""
        # Check for string manipulation methods
        if hasattr(node.func, 'attr'):
            thick_methods = ['split', 'replace', 'strip', 'find', 'index', 'startswith', 'endswith']
            if node.func.attr in thick_methods:
                self.add_message('thick-string-manipulation', node=node, args=(node.func.attr,))
        
        # Check for regex function calls
        if hasattr(node.func, 'attr') and hasattr(node.func, 'value'):
            if hasattr(node.func.value, 'id') and node.func.value.id == 're':
                if node.func.attr in ('search', 'match', 'findall', 'sub', 'compile'):
                    self.add_message('thick-regex-import', node=node)
    
    def _count_if_statements(self, node):
        """Count if/elif statements in a function"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                count += 1
                # Count elif statements
                current = child
                while current.orelse and len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                    count += 1
                    current = current.orelse[0]
        return count
    
    def _has_llm_usage(self, node):
        """Check if function has LLM usage"""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                # Check for llm_client.call_llm() patterns
                if hasattr(child.func, 'attr') and child.func.attr == 'call_llm':
                    return True
                # Check for direct LLM usage
                if hasattr(child.func, 'id') and 'llm' in child.func.id.lower():
                    return True
        return False

def register(linter: PyLinter):
    """Register the checker with pylint"""
    linter.register_checker(THINChecker(linter))

# For standalone usage
if __name__ == '__main__':
    print("THIN Pylint Plugin")
    print("Use with: pylint --load-plugins=thin_pylint_plugin your_file.py") 