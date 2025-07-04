#!/usr/bin/env python3
"""
Discernus Ultra-Thin Code Execution
==============================

Minimal code execution following "trust the academic context" philosophy.
Just detect ```python blocks and execute them safely.
"""

import re
import subprocess
import tempfile
import os
from pathlib import Path


def extract_code_blocks(llm_response):
    """Extract Python code blocks from LLM response"""
    pattern = r'```python\n(.*?)\n```'
    return re.findall(pattern, llm_response, re.DOTALL)


def is_safe_code(code):
    """Basic safety check - just block obviously dangerous imports"""
    dangerous = ['requests', 'urllib', 'socket', 'subprocess', 'os.system']
    return not any(danger in code for danger in dangerous)


def execute_code_block(code):
    """Execute code block and return results"""
    if not is_safe_code(code):
        return "Code blocked: contains potentially unsafe operations"
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            
            result = subprocess.run(
                ['python3', f.name], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            os.unlink(f.name)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
                
    except subprocess.TimeoutExpired:
        return "Code execution timed out (30s limit)"
    except Exception as e:
        return f"Execution failed: {e}"


def process_llm_notebook_request(conversation_id, speaker, response):
    """Minimal: detect code blocks and execute"""
    
    code_blocks = extract_code_blocks(response)
    
    if not code_blocks:
        return response  # No code to execute
    
    # Execute each code block and append results
    enhanced_response = response
    
    for code in code_blocks:
        result = execute_code_block(code)
        enhanced_response += f"\n\n**Code Output:**\n```\n{result}\n```"
    
    return enhanced_response 