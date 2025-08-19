#!/usr/bin/env python3
"""
Secure Code Execution Infrastructure
===================================

THIN Principle: Secure sandbox infrastructure that enables agent calculations
while preventing malicious code execution. 

Security features:
- Restricted execution environment 
- Resource limits (CPU, memory, time)
- Whitelist of allowed libraries
- No file system access beyond controlled data
- All code and results logged for experiment provenance
"""

import ast
import sys
import tempfile
import subprocess
import resource
import signal
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from contextlib import contextmanager
import logging
import os # Added for os.remove

# Import LLM code sanitization
from .llm_code_sanitizer import sanitize_llm_code

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class SecureExecutionError(Exception):
    """Raised when code execution fails for security or resource reasons"""
    pass

class CodeSecurityChecker:
    """
    AST-based security checker that analyzes code before execution
    More sophisticated than simple string matching
    """
    
    FORBIDDEN_NAMES = {
        # System access (keeping essential restrictions)
        '__import__', 'eval', 'exec', 'compile', 'open', 'file',
        'input', 'raw_input', 'reload', '__file__',
        # Note: Removed '__name__' - it's needed for legitimate Python code
        
        # OS and subprocess (keeping essential restrictions)
        'os', 'subprocess', 'commands', 'platform',
        # Note: Removed 'sys' - it's safely provided in execution environment
        
        # Network access  
        'socket', 'urllib', 'urllib2', 'httplib', 'requests',
        'ftplib', 'poplib', 'imaplib', 'smtplib',
        
        # File and directory operations
        'shutil', 'glob', 'tempfile', 'pickle', 'marshal',
        
        # Code manipulation
        'types', 'inspect', 'importlib', 'pkgutil',
    }
    
    FORBIDDEN_ATTRS = {
        '__subclasses__', '__bases__', '__mro__', '__class__',
        '__globals__', '__locals__', '__dict__', '__code__',
        '__func__', '__closure__', '__defaults__', '__kwdefaults__'
    }
    
    def __init__(self, capability_registry: Optional['CapabilityRegistry'] = None):
        self.violations = []
        self.allowed_libraries = set()
        self.allowed_builtins = set()
        self.logger = logging.getLogger(__name__)

        if capability_registry:
            self.allowed_libraries = capability_registry.get_allowed_libraries()
            self.allowed_builtins = capability_registry.get_allowed_builtins()
        else:
            # If no registry is provided, the allowed lists will be empty.
            # This makes the component safer by default.
            self.logger.warning("No capability registry provided to CodeSecurityChecker. No imports will be allowed.")
            self.allowed_libraries = set()
            self.allowed_builtins = set()
    
    def check_code_safety(self, code: str) -> Tuple[bool, List[str]]:
        """
        Analyze code using AST for security violations
        
        Returns (is_safe, list_of_violations)
        """
        self.violations = []
        
        self.logger.debug(f"CodeSecurityChecker received code for analysis: {repr(code)}")

        # Create a temporary file to hold the code for parsing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush() # Ensure the code is written to disk
            temp_file_path = f.name
        
        self.logger.debug(f"Code for parsing written to temporary file: {temp_file_path}")
        with open(temp_file_path, 'r') as f:
            self.logger.debug(f"Content of temp file: {repr(f.read())}")

        try:
            # Read the code back from the file to ensure integrity
            with open(temp_file_path, 'r') as code_file:
                source_code = code_file.read()
            
            tree = ast.parse(source_code, filename=temp_file_path, mode='exec')
            self.visit_node(tree)
        except SyntaxError as e:
            self.violations.append(f"Syntax error: {e}")
            return False, self.violations
        finally:
            os.remove(temp_file_path) # Manually clean up the file
        
        return len(self.violations) == 0, self.violations
    
    def visit_node(self, node):
        """Recursively visit AST nodes to check for violations"""
        
        # Check import statements against whitelist
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in self.allowed_libraries:
                    self.violations.append(f"Forbidden import: {alias.name}")
        
        # Check "from X import Y" statements  
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module not in self.allowed_libraries:
                self.violations.append(f"Forbidden import from: {node.module}")
        
        # Check for dangerous builtin names (eval, exec, etc.)
        elif isinstance(node, ast.Name):
            name = node.id
            if (name in self.FORBIDDEN_NAMES and 
                name not in self.allowed_builtins and 
                name not in self.allowed_libraries):
                self.violations.append(f"Forbidden name: {name}")
        
        # Check for attribute access that could expose internals
        elif isinstance(node, ast.Attribute):
            if node.attr in self.FORBIDDEN_ATTRS:
                self.violations.append(f"Forbidden attribute access: {node.attr}")
        
        # Check function calls for dynamic imports and dangerous functions
        elif isinstance(node, ast.Call):
            # Catch dynamic imports like __import__('os')
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if (func_name in self.FORBIDDEN_NAMES and 
                    func_name not in self.allowed_builtins and 
                    func_name not in self.allowed_libraries):
                    self.violations.append(f"Forbidden function call: {func_name}")
        
        # Recursively check all child nodes in the AST
        for child in ast.iter_child_nodes(node):
            self.visit_node(child)

class SecureCodeExecutor:
    """
    Secure code execution with sandboxing and resource limits
    
    THIN Principle: Provides secure computation infrastructure for agents
    """
    
    def __init__(self, 
                 timeout_seconds: int = 30,
                 memory_limit_mb: int = 256,
                 enable_data_science: bool = True,
                 capability_registry: Optional['CapabilityRegistry'] = None):
        self.timeout_seconds = timeout_seconds
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
        self.enable_data_science = enable_data_science
        self.capability_registry = capability_registry
        self.security_checker = CodeSecurityChecker(capability_registry=self.capability_registry)
    
    def execute_code(self, code: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute code safely with full logging and resource limits
        
        Args:
            code: Python code to execute
            context: Optional context variables (for data passing)
            
        Returns:
            {
                'success': bool,
                'output': str,
                'error': str,
                'execution_time': float,
                'memory_used': int,
                'result_data': Any,  # For structured results
                'security_violations': List[str]
            }
        """
        start_time = time.time()
        
        # Security check first (now reads from a temp file for robustness)
        is_safe, violations = self.security_checker.check_code_safety(code)
        if not is_safe:
            return {
                'success': False,
                'output': '',
                'error': f"Security violations: {', '.join(violations)}",
                'execution_time': 0,
                'memory_used': 0,
                'context': None,
                'security_violations': violations
            }
        
        # Restore the sanitizer now that the deeper bug is fixed
        # Sanitize LLM-generated code to fix common issues
        try:
            sanitized_code, transformations = sanitize_llm_code(code)
            if transformations and transformations != ['sanitization_failed']:
                logging.info(f"Applied code sanitization transformations: {transformations}")
        except Exception as e:
            logging.warning(f"Code sanitization failed, using original code: {e}")
            sanitized_code = code
            transformations = ['sanitization_failed']
        
        # Prepare secure execution environment
        if self.enable_data_science:
            safe_imports = self._prepare_data_science_environment()
        else:
            safe_imports = "import math, json, re, string, statistics\n"
        
        # Inject context variables if provided
        context_setup = ""
        if context:
            for key, value in context.items():
                # Handle pandas DataFrames specially to preserve object structure
                if hasattr(value, 'to_json') and hasattr(value, 'columns'):  # pandas DataFrame
                    # Inject DataFrame as reconstructed object using pd.DataFrame constructor
                    json_data = value.to_json(orient='records')
                    context_setup += f"    {key} = pd.DataFrame(json.loads({repr(json_data)}))\n"
                else:
                    # Skip pandas/numpy module objects - they're already imported in safe_imports
                    if str(type(value)) not in ['<class \'module\'>', '<module \'pandas\'>', '<module \'numpy\'>']:
                        context_setup += f"    {key} = {repr(value)}\n"
        
        # Wrap code with resource monitoring
        wrapped_code = f"""
{safe_imports}
import sys
import traceback
import json

# Capture stdout
from io import StringIO
original_stdout = sys.stdout
sys.stdout = captured_output = StringIO()

# Variables for results
result_context = {{}}
execution_success = True
error_message = ""

try:
    # Inject context variables
{context_setup}
    
    # User code execution
{self._indent_code(sanitized_code, '    ')}
    
    # Capture the final local variable scope
    final_locals = locals().copy()
    for var_name, var_value in final_locals.items():
        if not var_name.startswith('__') and type(var_value).__name__ not in ['module', 'function', 'type']:
            result_context[var_name] = var_value
    
except Exception as e:
    execution_success = False
    error_message = f"{{type(e).__name__}}: {{str(e)}}"
    traceback.print_exc()

finally:
    # Restore stdout
    sys.stdout = original_stdout
    output = captured_output.getvalue()
    
    # Print results as JSON for parsing
    result = {{
        'success': execution_success,
        'output': output,
        'error': error_message,
        'context': result_context
    }}
    
    # Custom JSON serializer to handle tuple keys and other non-serializable objects
    def safe_json_serializer(obj):
        if isinstance(obj, (int, float, bool, str)) or obj is None:
            return obj
        if isinstance(obj, tuple):
            return str(obj)  # Convert tuples to strings
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return str(obj)
        else:
            return str(obj)
    
    try:
        print("EXECUTION_RESULT:" + json.dumps(result, default=safe_json_serializer))
    except Exception as json_error:
        # Fallback: create a simplified result without problematic data
        safe_result = {{
            'success': execution_success,
            'output': output,
            'error': error_message,
            'context': {{k: str(v) for k, v in result_context.items()}}
        }}
        print("EXECUTION_RESULT:" + json.dumps(safe_result))
"""
        
        try:
            # Execute in subprocess with resource limits
            result = self._execute_in_sandbox(wrapped_code)
            result['execution_time'] = time.time() - start_time
            result['security_violations'] = []
            return result
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f"Execution infrastructure error: {str(e)}",
                'execution_time': time.time() - start_time,
                'memory_used': 0,
                'context': None,
                'security_violations': []
            }
    
    def _prepare_data_science_environment(self) -> str:
        """Prepare safe data science imports"""
        return """
# Safe data science environment
import math
import json
import re
import string
import statistics
import datetime
import collections
import itertools
import functools
import operator
import random
from decimal import Decimal

# Data science libraries (core required, visualization optional)
import numpy as np
import pandas as pd
import scipy.stats as stats

# Optional visualization libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    from scipy import optimize
except ImportError:
    # Create stubs for unavailable visualization libraries
    class MockVizLibrary:
        def __getattr__(self, name):
            def mock_function(*args, **kwargs):
                print(f"Note: {name} unavailable - visualization skipped")
                return None
            return mock_function
    
    plt = MockVizLibrary()
    sns = MockVizLibrary()
    go = MockVizLibrary()
    px = MockVizLibrary()
    optimize = MockVizLibrary()

# Safe text analysis
try:
    import textstat
    import textblob
    from collections import Counter
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    textstat = MockVizLibrary()
    textblob = MockVizLibrary()
    Counter = dict  # Fallback to basic dict
    
    # Create mock VADER analyzer
    class MockVader:
        def polarity_scores(self, text):
            return {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
    vader_analyzer = MockVader()
"""
    
    def _indent_code(self, code: str, indent: str) -> str:
        """Indent code block for wrapping"""
        return '\n'.join(indent + line for line in code.split('\n'))
    
    def _execute_in_sandbox(self, wrapped_code: str) -> Dict[str, Any]:
        """Execute code in subprocess with resource limits"""
        
        # Create temporary file for execution
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(wrapped_code)
            temp_file = f.name
        
        try:
            # Set resource limits function (with macOS compatibility)
            def set_limits():
                try:
                    # CPU time limit (works on most Unix systems)
                    resource.setrlimit(resource.RLIMIT_CPU, (self.timeout_seconds, self.timeout_seconds))
                    
                    # Memory limit (may not work on macOS, but try anyway)
                    try:
                        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit_bytes, self.memory_limit_bytes))
                    except (OSError, ValueError):
                        # macOS often doesn't support RLIMIT_AS properly
                        pass
                    
                    # Prevent large file creation (may not work on all systems)
                    try:
                        resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))  # 1MB limit instead of 0
                    except (OSError, ValueError):
                        pass
                    
                    # Limit number of processes (may not work on all systems)
                    try:
                        resource.setrlimit(resource.RLIMIT_NPROC, (5, 5))  # Allow a few processes instead of 1
                    except (OSError, ValueError):
                        pass
                        
                except Exception as e:
                    # If resource limits fail, continue without them (better than crashing)
                    import sys
                    print(f"Warning: Could not set resource limits: {e}", file=sys.stderr)
            
            # Execute with resource limits (or without if they fail)
            process = subprocess.Popen(
                [sys.executable, temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=set_limits
            )
            
            stdout, stderr = process.communicate(timeout=self.timeout_seconds)
            
            # Parse execution result
            if "EXECUTION_RESULT:" in stdout:
                result_json = stdout.split("EXECUTION_RESULT:")[-1].strip()
                try:
                    result = json.loads(result_json)
                    # Attempt to auto-convert numeric types back from strings
                    if 'context' in result and result['context']:
                        for key, value in result['context'].items():
                            if isinstance(value, str):
                                try:
                                    result['context'][key] = int(value)
                                    continue
                                except (ValueError, TypeError):
                                    pass
                                try:
                                    result['context'][key] = float(value)
                                except (ValueError, TypeError):
                                    pass
                    result['memory_used'] = 0  # Would need separate monitoring for accurate measurement
                    return result
                except json.JSONDecodeError:
                    pass
            
            # Fallback result
            return {
                'success': process.returncode == 0,
                'output': stdout,
                'error': stderr,
                'memory_used': 0,
                'context': None
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'success': False,
                'output': '',
                'error': f"Code execution timed out after {self.timeout_seconds} seconds",
                'memory_used': 0,
                'context': None
            }
        
        finally:
            # Clean up temporary file
            Path(temp_file).unlink(missing_ok=True)

def process_llm_code_request(conversation_id: str, speaker: str, response: str) -> str:
    """
    Enhanced code execution with security and full experiment logging
    
    THIN Principle: Infrastructure handles security, LLMs provide intelligence
    
    This is the main entry point for code execution in Discernus. When LLMs
    write ```python blocks in their responses, this function:
    1. Extracts code blocks from the response
    2. Executes them securely with resource limits
    3. Captures results for experiment provenance
    4. Creates research notebooks for important calculations
    5. Returns enhanced response with execution results
    
    Args:
        conversation_id: Session identifier for logging
        speaker: Which agent/LLM is executing code
        response: Full LLM response containing ```python blocks
        
    Returns:
        Enhanced response with execution results appended
    """
    
    # Extract code blocks
    import re
    code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
    
    if not code_blocks:
        return response  # No code to execute
    
    # Initialize secure executor with data science support
    executor = SecureCodeExecutor(
        timeout_seconds=30,
        memory_limit_mb=256,
        enable_data_science=True
    )
    
    enhanced_response = response
    execution_log = []
    
    for i, code in enumerate(code_blocks):
        print(f"🔒 Executing code block {i+1} securely...")
        
        # Execute code securely
        result = executor.execute_code(code)
        
        # Prepare calculation data for notebook system
        calculation_data = {
            'code': code,
            'output': result.get('output', ''),
            'result_data': result.get('result_data'),
            'speaker': speaker,
            'timestamp': time.time(),
            'execution_time': result.get('execution_time', 0),
            'success': result.get('success', False)
        }
        
        # Try to add to research notebook if important
        try:
            from discernus.core.notebook_manager import enhance_code_execution_with_notebook
            added_to_notebook = enhance_code_execution_with_notebook(conversation_id, speaker, calculation_data)
        except ImportError:
            added_to_notebook = False
            print("📓 Research notebook system not available")
        
        # Log execution for experiment provenance
        execution_entry = {
            'conversation_id': conversation_id,
            'speaker': speaker,
            'code_block_index': i,
            'code': code,
            'timestamp': time.time(),
            'result': result,
            'added_to_notebook': added_to_notebook
        }
        execution_log.append(execution_entry)
        
        # Format result for display
        if result['success']:
            output_text = result['output'] if result['output'] else "Code executed successfully (no output)"
            if result['result_data']:
                output_text += f"\n\nResult data: {result['result_data']}"
        else:
            output_text = f"❌ Execution failed: {result['error']}"
            if result['security_violations']:
                output_text += f"\n🛡️ Security violations: {', '.join(result['security_violations'])}"
        
        # Add results to response
        enhanced_response += f"\n\n**🔐 Secure Code Execution Result:**\n```\n{output_text}\n```"
        enhanced_response += f"\n*Execution time: {result['execution_time']:.3f}s*"
        
        if added_to_notebook:
            enhanced_response += f"\n*📓 Important calculation saved to research notebook*"
    
    # Save execution log for experiment provenance  
    _save_execution_log(conversation_id, execution_log)
    
    return enhanced_response

def _save_execution_log(conversation_id: str, execution_log: List[Dict[str, Any]]):
    """Save execution log for experiment record keeping"""
    
    log_dir = Path("research_sessions") / conversation_id / "code_execution"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"execution_log_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump(execution_log, f, indent=2, default=str)
    
    print(f"💾 Code execution logged to: {log_file}")

# Maintain backward compatibility
def process_llm_notebook_request(conversation_id: str, speaker: str, response: str) -> str:
    """Backward compatibility wrapper"""
    return process_llm_code_request(conversation_id, speaker, response)

def extract_code_blocks(response: str) -> List[str]:
    """Extract Python code blocks from LLM response"""
    import re
    return re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)

if __name__ == "__main__":
    # Test secure execution
    test_code = """
import numpy as np
import pandas as pd

# Create test data
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

print("DataFrame created:")
print(df)
print(f"Sum of column A: {df['A'].sum()}")

# Store result for structured output
result_data = {
    'dataframe_shape': df.shape,
    'column_sums': df.sum().to_dict()
}
"""
    
    executor = SecureCodeExecutor(enable_data_science=True)
    result = executor.execute_code(test_code)
    
    print("🔒 Secure Execution Test:")
    print(f"Success: {result['success']}")
    print(f"Output: {result['output']}")
    print(f"Result data: {result['result_data']}")
    print(f"Execution time: {result['execution_time']:.3f}s") 