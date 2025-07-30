#!/usr/bin/env python3
"""
LLM Code Sanitizer - THIN Architecture for Code Quality
======================================================

Uses Meta's libcst library to surgically fix common issues in LLM-generated code
while preserving intent and letting LLMs generate natural analytical code.

Key principle: Let LLMs be LLMs, clean up on our side using battle-tested tooling.
"""

import re
import logging
import ast
from typing import Optional, Union

import libcst as cst
from libcst import matchers as m


class LLMCodeSanitizer(cst.CSTTransformer):
    """
    Transforms LLM-generated code to fix common syntax and safety issues.
    
    Uses libcst's concrete syntax tree to apply surgical fixes while preserving
    the LLM's analytical intent and code structure.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.transformations_applied = []
    
    def sanitize_code(self, code: str) -> tuple[str, list[str]]:
        """
        Apply all sanitization transformations to LLM-generated code.
        
        Args:
            code: Raw LLM-generated Python code
            
        Returns:
            Tuple of (sanitized_code, list_of_transformations_applied)
        """
        try:
            # Reset transformation tracking
            self.transformations_applied = []
            
            # Step 1: Pre-processing fixes for common string issues
            preprocessed_code = self._preprocess_string_literals(code)
            
            # Step 2: Try to fix syntax with autopep8 first
            try:
                import autopep8
                autopep8_fixed = autopep8.fix_code(preprocessed_code, options={'aggressive': 1})
                if autopep8_fixed != preprocessed_code:
                    self.transformations_applied.append("autopep8_syntax_fixes")
                    preprocessed_code = autopep8_fixed
            except Exception as e:
                self.logger.debug(f"autopep8 failed: {e}")
            
            # Step 3: Try to fix with ruff if available
            try:
                import subprocess
                import tempfile
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(preprocessed_code)
                    temp_file = f.name
                
                try:
                    result = subprocess.run(['ruff', 'check', '--fix', temp_file], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        with open(temp_file, 'r') as f:
                            ruff_fixed = f.read()
                        if ruff_fixed != preprocessed_code:
                            self.transformations_applied.append("ruff_syntax_fixes")
                            preprocessed_code = ruff_fixed
                finally:
                    import os
                    os.unlink(temp_file)
                    
            except Exception as e:
                self.logger.debug(f"ruff failed: {e}")
            
            # Step 4: Parse and transform with libcst
            try:
                tree = cst.parse_module(preprocessed_code)
                transformed_tree = tree.visit(self)
                sanitized_code = transformed_tree.code
                
            except (cst.ParserSyntaxError, Exception) as e:
                self.logger.warning(f"CST parsing failed, applying fallback fixes: {e}")
                sanitized_code = self._apply_fallback_fixes(preprocessed_code)
                self.transformations_applied.append("fallback_string_fixes")
            
            # Step 5: Final syntax validation
            try:
                ast.parse(sanitized_code)
                self.transformations_applied.append("syntax_validated")
            except SyntaxError as e:
                self.logger.warning(f"Final syntax validation failed: {e}")
                # Try one more aggressive fix with black
                try:
                    import black
                    mode = black.FileMode()
                    black_fixed = black.format_str(sanitized_code, mode=mode)
                    # Validate the black output
                    ast.parse(black_fixed)
                    sanitized_code = black_fixed
                    self.transformations_applied.append("black_formatting")
                except Exception as black_error:
                    self.logger.error(f"Black formatting failed: {black_error}")
                    # Return the best we have
                    pass
            
            return sanitized_code, self.transformations_applied
            
        except Exception as e:
            self.logger.error(f"Code sanitization failed: {e}")
            # Return original code if sanitization fails - fail gracefully
            return code, ["sanitization_failed"]
    
    def _preprocess_string_literals(self, code: str) -> str:
        """
        Fix common string literal issues before CST parsing.
        
        This handles cases where LLMs create problematic string assignments
        from evidence text containing quotes and special characters.
        """
        fixed_code = code
        
        # Enhanced string literal fixing with multiple approaches
        lines = fixed_code.split('\n')
        fixed_lines = []
        
        for line_num, line in enumerate(lines):
            original_line = line
            fixed_line = line
            
            # Approach 1: Handle simple string assignments with quote issues
            if re.search(r'^\s*\w+\s*=\s*["\'].*["\']', line):
                if self._has_quote_issues(line):
                    fixed_line = self._convert_to_safe_string(line)
                    if fixed_line != line:
                        self.transformations_applied.append(f"fixed_string_quotes_line_{line_num + 1}")
            
            # Approach 2: Handle f-strings with embedded quotes
            elif re.search(r'f["\'].*\{.*\}.*["\']', line):
                if self._has_quote_issues(line):
                    fixed_line = self._fix_fstring_quotes(line)
                    if fixed_line != line:
                        self.transformations_applied.append(f"fixed_fstring_quotes_line_{line_num + 1}")
            
            # Approach 3: Handle print statements with problematic strings
            elif re.search(r'print\s*\([^)]*["\'][^"\']*["\'][^)]*\)', line):
                if self._has_quote_issues(line):
                    fixed_line = self._fix_print_statement(line)
                    if fixed_line != line:
                        self.transformations_applied.append(f"fixed_print_quotes_line_{line_num + 1}")
            
            # Approach 4: Catch any remaining unterminated strings
            if self._has_unterminated_string(fixed_line):
                fixed_line = self._fix_unterminated_string(fixed_line)
                if fixed_line != original_line:
                    self.transformations_applied.append(f"fixed_unterminated_string_line_{line_num + 1}")
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines)
    
    def _has_quote_issues(self, line: str) -> bool:
        """Check if a line has problematic quote patterns."""
        # Look for unescaped quotes inside string literals
        patterns = [
            r'"[^"]*\'[^"]*"',  # Double quotes containing single quotes
            r"'[^']*\"[^']*'",  # Single quotes containing double quotes
            r'"[^"]*"[^"]*"',   # Multiple quote segments
            r"'[^']*'[^']*'",   # Multiple single quote segments
        ]
        
        return any(re.search(pattern, line) for pattern in patterns)
    
    def _convert_to_safe_string(self, line: str) -> str:
        """Convert problematic string assignment to safe triple-quoted version."""
        # Extract the variable name and content
        match = re.match(r'^(\s*)(\w+)\s*=\s*(["\'])(.*)\3(.*)$', line)
        if not match:
            return line
        
        indent, var_name, quote_char, content, remainder = match.groups()
        
        # Use triple quotes to safely contain the content
        safe_line = f'{indent}{var_name} = """{content}"""{remainder}'
        return safe_line
    
    def _fix_fstring_quotes(self, line: str) -> str:
        """Fix f-strings with problematic quote patterns."""
        # Convert f-strings to regular strings to avoid quote issues
        # f"text with {variable}" -> "text with " + str(variable)
        # This is a simplified approach - could be more sophisticated
        
        # For now, just convert f-strings to triple-quoted strings
        if 'f"' in line:
            line = line.replace('f"', '"""').replace('"', '"""')
        elif "f'" in line:
            line = line.replace("f'", '"""').replace("'", '"""')
        
        return line
    
    def _fix_print_statement(self, line: str) -> str:
        """Fix print statements with problematic quote patterns."""
        # Look for print statements and make their strings safe
        if 'print(' in line:
            # Simple approach: convert any quotes inside print to triple quotes
            # More sophisticated parsing could be added later
            
            # Find the content inside print()
            match = re.search(r'print\s*\(([^)]+)\)', line)
            if match:
                print_content = match.group(1)
                # If it contains problematic quotes, wrap in triple quotes
                if self._has_quote_issues(print_content):
                    safe_content = f'"""{print_content.strip("\"\'").strip()}"""'
                    return line.replace(print_content, safe_content)
        
        return line
    
    def _has_unterminated_string(self, line: str) -> bool:
        """Check if a line has unterminated string literals."""
        # Count quotes to see if they're balanced
        double_quotes = line.count('"') - line.count('\\"')  # Exclude escaped quotes
        single_quotes = line.count("'") - line.count("\\'")  # Exclude escaped quotes
        
        # If odd number of quotes, likely unterminated
        return (double_quotes % 2 != 0) or (single_quotes % 2 != 0)
    
    def _fix_unterminated_string(self, line: str) -> str:
        """Fix unterminated string literals by converting to triple quotes."""
        # Simple approach: if we detect unterminated strings, wrap the whole line's
        # string content in triple quotes
        
        # Look for patterns like: variable = "unterminated string
        match = re.match(r'^(\s*)(\w+\s*=\s*)(["\'])(.*)$', line)
        if match:
            indent, assignment, quote_char, content = match.groups()
            # If content doesn't end with the same quote, it's likely unterminated
            if not content.endswith(quote_char):
                return f'{indent}{assignment}"""{content}"""'
        
        return line
    
    def _fix_unterminated_strings_aggressive(self, code: str) -> str:
        """Aggressively fix unterminated strings by scanning character by character."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Count quotes to detect unterminated strings
            double_quotes = line.count('"') - line.count('\\"')
            single_quotes = line.count("'") - line.count("\\'")
            
            # If we have an odd number of quotes, try to fix it
            if (double_quotes % 2 != 0) or (single_quotes % 2 != 0):
                # Look for print statements with unterminated strings
                if 'print(' in line:
                    # Find the opening parenthesis
                    paren_start = line.find('print(')
                    if paren_start != -1:
                        # Look for the first quote after print(
                        quote_pos = line.find('"', paren_start)
                        if quote_pos != -1:
                            # Find the next quote to see if it's unterminated
                            next_quote = line.find('"', quote_pos + 1)
                            if next_quote == -1:
                                # Unterminated string in print statement
                                # Replace the entire print statement with a safe version
                                before_print = line[:paren_start]
                                after_print = line[paren_start:]
                                # Extract the string content and wrap in triple quotes
                                string_start = after_print.find('"')
                                if string_start != -1:
                                    string_content = after_print[string_start + 1:]
                                    # Remove any trailing content after the string
                                    if ')' in string_content:
                                        string_content = string_content[:string_content.find(')')]
                                    fixed_print = f'{before_print}print("""{string_content}""")'
                                    # Add closing parenthesis if missing
                                    if not fixed_print.endswith(')'):
                                        fixed_print += ')'
                                    fixed_lines.append(fixed_print)
                                    continue
                
                # For other cases, try to wrap the entire line in triple quotes
                if '"' in line:
                    # Find the first quote and wrap everything after it
                    first_quote = line.find('"')
                    before_quote = line[:first_quote]
                    after_quote = line[first_quote + 1:]
                    # Remove any trailing content that might be problematic
                    if ')' in after_quote:
                        after_quote = after_quote[:after_quote.find(')')]
                    fixed_line = f'{before_quote}"""{after_quote}"""'
                    fixed_lines.append(fixed_line)
                    continue
            
            # If no fixes needed, keep the line as is
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _apply_fallback_fixes(self, code: str) -> str:
        """Apply regex-based fixes when CST parsing fails."""
        fixed_code = code
        
        # First, try to fix the most common unterminated string issues
        fixed_code = self._fix_unterminated_strings_aggressive(fixed_code)
        
        # Fix common syntax error patterns
        fixes = [
            # Fix unterminated strings - more aggressive patterns
            (r'print\s*\(\s*"([^"]*?)(?:\n|$)', r'print("""\1""")'),
            (r'print\s*\(\s*\'([^\']*?)(?:\n|$)', r'print("""\1""")'),
            (r'=\s*"([^"]*?)(?:\n|$)', r'= """\1"""'),
            (r'=\s*\'([^\']*?)(?:\n|$)', r'= """\1"""'),
            
            # Fix unterminated strings in assignments
            (r'= "([^"]*)"([^"]*$)', r'= """\1\2"""'),
            (r"= '([^']*)'([^']*$)", r'= """\1\2"""'),
            
            # Fix common indentation issues (unexpected indent) 
            # This often happens with multi-line strings or dictionary values
            (r'^(\s+)(\S.*?): \("([^"]*)"$', r'\1\2: (\n\1    "\3"'),
            
            # Remove forbidden attribute access
            (r'(\w+)\.__class__', r'\1.dtype'),
            (r'(\w+)\.__globals__', r'\1.shape'),
            (r'(\w+)\.__locals__', r'\1.shape'),
            (r'(\w+)\.__dict__', r'\1.columns'),
            (r'(\w+)\.__code__', r'\1.dtypes'),
            (r'(\w+)\.__subclasses__\(\)', r'\1.describe()'),
            (r'(\w+)\.__bases__', r'\1.shape'),
            (r'(\w+)\.__mro__', r'\1.info()'),
            
            # Replace problematic introspection calls
            (r'type\(([^)]+)\)', r'\1.dtype'),
            # Disabled isinstance regex - handled by CST transformation instead
            # (r'isinstance\(([^,)]+),\s*[^)]+\)', r'hasattr(\1, "shape")'),
        ]
        
        for pattern, replacement in fixes:
            if re.search(pattern, fixed_code, re.MULTILINE):
                fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.MULTILINE)
                self.transformations_applied.append(f"fallback_fix_{pattern[:20]}")
        
        return fixed_code
    
    def leave_SimpleStatementLine(self, original_node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine) -> cst.SimpleStatementLine:
        """Transform assignment statements that might have string issues."""
        # Check if this is an assignment with a potentially problematic string
        if len(updated_node.body) == 1 and isinstance(updated_node.body[0], cst.Assign):
            assign = updated_node.body[0]
            
            # Check if the value is a string that might need DataFrame operation conversion
            if isinstance(assign.value, cst.SimpleString):
                # If this looks like evidence text assignment, suggest DataFrame operation
                if self._looks_like_evidence_assignment(assign):
                    # Convert to DataFrame operation comment + safe assignment
                    safe_assignment = self._convert_to_dataframe_operation(assign)
                    if safe_assignment != assign:
                        new_body = [safe_assignment]
                        self.transformations_applied.append("evidence_to_dataframe_op")
                        return updated_node.with_changes(body=new_body)
        
        return updated_node
    
    def _looks_like_evidence_assignment(self, assign: cst.Assign) -> bool:
        """Check if assignment looks like evidence text that should use DataFrame operations."""
        if not isinstance(assign.value, cst.SimpleString):
            return False
        
        # Check for common evidence text patterns
        string_value = assign.value.value
        evidence_indicators = [
            'quote', 'evidence', 'text', 'We ', 'They ', 'Our ', 
            'justice', 'democracy', 'policy', 'institution'
        ]
        
        return any(indicator in string_value for indicator in evidence_indicators)
    
    def _convert_to_dataframe_operation(self, assign: cst.Assign) -> cst.Assign:
        """Convert evidence text assignment to DataFrame operation."""
        # Create a comment explaining the conversion
        comment = cst.SimpleStatementLine(
            body=[cst.Expr(cst.SimpleString('# Converted to DataFrame operation for safety'))]
        )
        
        # Replace the string assignment with DataFrame operation
        # For now, just make the string safe - in future versions could be more sophisticated
        if isinstance(assign.value, cst.SimpleString):
            safe_value = assign.value.with_changes(
                value='"""' + assign.value.value[1:-1] + '"""'
            )
            return assign.with_changes(value=safe_value)
        
        return assign

    def leave_Attribute(self, original_node: cst.Attribute, updated_node: cst.Attribute) -> cst.Attribute:
        """Remove forbidden attribute access patterns."""
        if isinstance(updated_node.attr, cst.Name):
            attr_name = updated_node.attr.value
            
            # List of forbidden attributes from security sandbox
            forbidden_attrs = [
                '__class__', '__globals__', '__locals__', '__dict__', 
                '__code__', '__subclasses__', '__bases__', '__mro__'
            ]
            
            if attr_name in forbidden_attrs:
                # Replace with safe DataFrame introspection
                if attr_name == '__class__':
                    # Convert obj.__class__ to type(obj) or safe DataFrame method
                    self.transformations_applied.append(f"removed_forbidden_attr_{attr_name}")
                    # For now, remove the entire attribute access - could be more sophisticated
                    return updated_node.with_changes(attr=cst.Name("dtype"))  # Safe pandas attribute
                else:
                    self.transformations_applied.append(f"removed_forbidden_attr_{attr_name}")
                    # Replace with safe alternative or comment it out
                    return updated_node.with_changes(attr=cst.Name("shape"))  # Safe pandas attribute
        
        return updated_node
    
    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        """Transform function calls that might be problematic."""
        if isinstance(updated_node.func, cst.Name):
            func_name = updated_node.func.value
            
            # Replace problematic introspection functions more carefully
            if func_name in ['type', 'isinstance'] and self._looks_like_introspection_call(updated_node):
                # Instead of converting to a method call, convert to a simple attribute check
                self.transformations_applied.append(f"converted_introspection_{func_name}")
                
                # Get the first argument if available
                if len(updated_node.args) > 0:
                    first_arg = updated_node.args[0].value
                    # Convert to a safe DataFrame attribute check
                    return cst.Call(
                        func=cst.Name("hasattr"),
                        args=[
                            cst.Arg(first_arg),
                            cst.Arg(cst.SimpleString('"shape"'))  # Safe attribute that all DataFrames have
                        ]
                    )
        
        return updated_node
    
    def _looks_like_introspection_call(self, call_node: cst.Call) -> bool:
        """Check if a function call looks like problematic introspection."""
        # Simple heuristic: if it has arguments that might be DataFrame columns or evidence
        if len(call_node.args) > 0:
            for arg in call_node.args:
                if isinstance(arg.value, cst.Attribute):
                    # This might be introspecting DataFrame attributes
                    return True
        return False


def sanitize_llm_code(code: str) -> tuple[str, list[str]]:
    """
    Convenience function to sanitize LLM-generated code.
    
    Args:
        code: Raw LLM-generated Python code
        
    Returns:
        Tuple of (sanitized_code, transformations_applied)
    """
    sanitizer = LLMCodeSanitizer()
    return sanitizer.sanitize_code(code)


# Example usage and testing
if __name__ == "__main__":
    # Test with problematic code that LLMs might generate
    test_code = '''
import pandas as pd
import numpy as np

# Problematic string assignment (common LLM pattern)
sample_quote = "We don't owe objectivity to oppressors"
another_quote = 'They said "justice" but meant revenge'

# This should work fine
scores_mean = scores_df['score'].mean()
evidence_count = evidence_df.shape[0]
'''
    
    sanitized, transformations = sanitize_llm_code(test_code)
    print("Original code:")
    print(test_code)
    print("\nSanitized code:")
    print(sanitized)
    print(f"\nTransformations applied: {transformations}") 