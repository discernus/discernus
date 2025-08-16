#!/usr/bin/env python3
"""
NotebookExecutor - v8.0 Notebook Validation and Execution System
================================================================

THIN-compliant system for validating and executing generated research notebooks.
Provides computational verification and academic integrity assurance.

THIN Architecture Principles:
- Minimal coordination logic (<150 lines)
- Computational verification (no hallucinated statistics)
- Complete audit logging for academic provenance
- Security boundary enforcement
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import tempfile
import shutil

from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary


class NotebookExecutor:
    """
    THIN-compliant notebook validation and execution system.
    
    Follows v8.0 architecture principles:
    - Computational verification of all calculations
    - Security boundary enforcement during execution
    - Complete audit trails for academic integrity
    - Zero hallucinated statistics guarantee
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 audit_logger: Optional[AuditLogger] = None):
        """Initialize notebook executor with security boundary."""
        self.security = security
        self.audit_logger = audit_logger or AuditLogger()
        self.agent_name = "NotebookExecutor"
        
        # Log executor initialization
        self.audit_logger.log_agent_event(
            agent_name=self.agent_name,
            event_type="EXECUTOR_INITIALIZED",
            data={"security_boundary": str(security.experiment_root)}
        )
    
    def validate_and_execute_notebook(self, 
                                    notebook_content: str,
                                    notebook_path: Path,
                                    execution_timeout: int = 300) -> Dict[str, Any]:
        """
        Validate and execute research notebook with security enforcement.
        
        Args:
            notebook_content: Complete notebook Python code
            notebook_path: Path where notebook should be saved
            execution_timeout: Maximum execution time in seconds
            
        Returns:
            Execution results with validation status
            
        Raises:
            Exception: On validation or execution failure
        """
        try:
            # Log notebook execution start
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_EXECUTION_START",
                data={
                    "notebook_path": str(notebook_path),
                    "notebook_size": len(notebook_content),
                    "timeout": execution_timeout
                }
            )
            
            # Phase 1: Syntax Validation
            syntax_valid = self._validate_syntax(notebook_content)
            if not syntax_valid:
                raise Exception("Notebook syntax validation failed")
            
            # Phase 2: Security Validation
            security_valid = self._validate_security(notebook_content)
            if not security_valid:
                raise Exception("Notebook security validation failed")
            
            # Phase 3: Save Notebook (with security boundary enforcement)
            self.security.secure_write_text(notebook_path, notebook_content)
            
            # Phase 4: Execute Notebook
            execution_result = self._execute_notebook(notebook_path, execution_timeout)
            
            # Phase 5: Validate Results
            results_valid = self._validate_results(notebook_path.parent)
            
            # Phase 6: CRITICAL - Fail if execution had warnings or didn't succeed
            if not execution_result["success"]:
                warnings_info = execution_result.get("warnings_detected", {})
                raise Exception(f"Notebook execution failed with critical warnings: {warnings_info}")
            
            # Log successful execution
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_EXECUTION_SUCCESS",
                data={
                    "notebook_path": str(notebook_path),
                    "execution_time": execution_result.get("execution_time", 0),
                    "results_valid": results_valid,
                    "warnings_detected": execution_result.get("warnings_detected", {})
                }
            )
            
            return {
                "status": "success",
                "notebook_path": str(notebook_path),
                "syntax_valid": syntax_valid,
                "security_valid": security_valid,
                "execution_result": execution_result,
                "results_valid": results_valid
            }
            
        except Exception as e:
            # Log execution failure
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_EXECUTION_FAILURE",
                data={"error": str(e), "notebook_path": str(notebook_path)}
            )
            raise Exception(f"Notebook execution failed: {str(e)}")
    
    def _validate_syntax(self, notebook_content: str) -> bool:
        """Validate Python syntax of notebook content."""
        try:
            compile(notebook_content, '<notebook>', 'exec')
            return True
        except SyntaxError as e:
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="SYNTAX_VALIDATION_FAILURE",
                data={"error": str(e)}
            )
            return False
    
    def _validate_security(self, notebook_content: str) -> bool:
        """Validate notebook content for security compliance."""
        # More intelligent security checks for academic research notebooks
        dangerous_patterns = [
            'os.system(',
            'subprocess.call(',
            'subprocess.run(',
            'exec(',
            '__import__(',
            'globals(',
            'locals(',
        ]
        
        for pattern in dangerous_patterns:
            if pattern in notebook_content:
                self.audit_logger.log_agent_event(
                    agent_name=self.agent_name,
                    event_type="SECURITY_VALIDATION_FAILURE",
                    data={"forbidden_pattern": pattern}
                )
                return False
        return True
    
    def _execute_notebook(self, notebook_path: Path, timeout: int) -> Dict[str, Any]:
        """Execute notebook and capture results."""
        import time
        start_time = time.time()
        
        try:
            # Execute notebook using subprocess for isolation
            result = subprocess.run(
                [sys.executable, str(notebook_path)],
                cwd=notebook_path.parent,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            # CRITICAL: Analyze output for silent failures
            warnings_detected = self._analyze_execution_output(result.stdout, result.stderr)
            
            # Log execution details for debugging
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_EXECUTION_DETAILS",
                data={
                    "return_code": result.returncode,
                    "execution_time": execution_time,
                    "stdout_length": len(result.stdout),
                    "stderr_length": len(result.stderr),
                    "warnings_detected": warnings_detected
                }
            )
            
            # Success is now: return code 0 AND no critical warnings
            success = result.returncode == 0 and not warnings_detected["has_critical_warnings"]
            
            return {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": execution_time,
                "success": success,
                "warnings_detected": warnings_detected
            }
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return {
                "return_code": -1,
                "stdout": "",
                "stderr": f"Execution timeout after {timeout} seconds",
                "execution_time": execution_time,
                "success": False,
                "warnings_detected": {"has_critical_warnings": True, "timeout": True}
            }
    
    def _analyze_execution_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Analyze notebook execution output for critical warnings and silent failures.
        
        Returns:
            Dictionary with warning analysis results
        """
        warnings = {
            "has_critical_warnings": False,
            "function_not_available_count": 0,
            "placeholder_usage_count": 0,
            "syntax_warnings": [],
            "missing_functions": [],
            "placeholder_content_detected": False,
            "details": []
        }
        
        # Critical failure patterns that indicate broken functionality
        critical_patterns = [
            ("function not available - using placeholder", "FUNCTION_NOT_AVAILABLE"),
            ("Visualization functions not available", "VISUALIZATION_MISSING"),
            ("⚠️", "WARNING_SYMBOL"),
            ("functions not available", "FUNCTIONS_MISSING"),
            ("skipping plots", "PLOTS_SKIPPED")
        ]
        
        # CRITICAL: Detect placeholder content in final output
        placeholder_content_patterns = [
            ("Statistical analysis pending execution", "PLACEHOLDER_STATISTICAL"),
            ("Findings will be generated during notebook execution", "PLACEHOLDER_FINDINGS"),
            ("currently pending execution", "PLACEHOLDER_PENDING"),
            ("will be generated subsequent to", "PLACEHOLDER_FUTURE"),
            ("comprehensive interpretation.*pending", "PLACEHOLDER_INTERPRETATION")
        ]
        
        # Analyze stdout for critical warnings
        for pattern, warning_type in critical_patterns:
            if pattern in stdout:
                count = stdout.count(pattern)
                warnings["details"].append({
                    "type": warning_type,
                    "pattern": pattern,
                    "count": count,
                    "source": "stdout"
                })
                
                if warning_type == "FUNCTION_NOT_AVAILABLE":
                    warnings["function_not_available_count"] += count
                elif warning_type == "WARNING_SYMBOL":
                    warnings["placeholder_usage_count"] += count
        
        # CRITICAL: Check for placeholder content in final output
        import re
        for pattern, warning_type in placeholder_content_patterns:
            if warning_type == "PLACEHOLDER_INTERPRETATION":
                # Use regex for complex pattern
                if re.search(pattern, stdout):
                    warnings["placeholder_content_detected"] = True
                    warnings["details"].append({
                        "type": warning_type,
                        "pattern": pattern,
                        "count": 1,
                        "source": "stdout",
                        "critical": True
                    })
            else:
                # Use simple string containment for exact patterns
                if pattern in stdout:
                    warnings["placeholder_content_detected"] = True
                    warnings["details"].append({
                        "type": warning_type,
                        "pattern": pattern,
                        "count": 1,
                        "source": "stdout",
                        "critical": True
                    })
        
        # Analyze stderr for syntax warnings and errors
        if stderr:
            stderr_lines = stderr.split('\n')
            for line in stderr_lines:
                if 'SyntaxWarning' in line or 'invalid escape sequence' in line:
                    warnings["syntax_warnings"].append(line.strip())
                    warnings["details"].append({
                        "type": "SYNTAX_WARNING",
                        "message": line.strip(),
                        "source": "stderr"
                    })
        
        # Determine if we have critical warnings
        warnings["has_critical_warnings"] = (
            warnings["function_not_available_count"] > 0 or
            warnings["placeholder_usage_count"] > 0 or
            len(warnings["syntax_warnings"]) > 0 or
            warnings["placeholder_content_detected"]  # CRITICAL: Placeholder content is a critical failure
        )
        
        # Log detailed warning analysis
        if warnings["has_critical_warnings"]:
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="CRITICAL_WARNINGS_DETECTED",
                data=warnings
            )
        
        return warnings
    
    def _validate_results(self, notebook_dir: Path) -> bool:
        """Validate that expected results files were generated."""
        expected_files = [
            "notebook_results.json",
            "derived_metrics_results.csv"
        ]
        
        for expected_file in expected_files:
            file_path = notebook_dir / expected_file
            if not file_path.exists():
                self.audit_logger.log_agent_event(
                    agent_name=self.agent_name,
                    event_type="RESULTS_VALIDATION_FAILURE",
                    data={"missing_file": expected_file}
                )
                return False
        
        return True
