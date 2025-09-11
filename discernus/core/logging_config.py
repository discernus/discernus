#!/usr/bin/env python3
"""
Comprehensive Logging Configuration for Discernus
================================================

Sets up loguru for real-time visibility into system operations, replacing
the current opacity with actual clarity about what's happening.

Features:
- Real-time console output with structured formatting
- File logging for persistence and debugging
- Different log levels for different components
- Color-coded output for immediate visual feedback
- Structured logging for machine parsing
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
import logging

# Remove default loguru handler
logger.remove()

# Global flag to prevent multiple executions
_litellm_suppression_configured = False

def ensure_litellm_debug_suppression():
    """
    Comprehensive suppression of all LiteLLM debug output including proxy components.
    
    This function addresses the root cause of LiteLLM Proxy debug flooding by:
    1. Setting environment variables to ERROR level (more restrictive)
    2. Configuring Python loggers for proxy components
    3. Installing message filters to catch remaining output
    
    Must be called before any LiteLLM imports.
    """
    global _litellm_suppression_configured
    
    # Prevent multiple executions
    if _litellm_suppression_configured:
        return
    
    _litellm_suppression_configured = True
    # Environment Variables - Set to ERROR level for maximum suppression
    env_vars = {
        # Core LiteLLM settings - ERROR level instead of WARNING
        'LITELLM_VERBOSE': 'false',
        'LITELLM_LOG': 'ERROR',  # Changed from WARNING
        'LITELLM_LOG_LEVEL': 'ERROR',  # Changed from WARNING
        
        # Proxy-specific settings - ERROR level
        'LITELLM_PROXY_DEBUG': 'false',
        'LITELLM_PROXY_LOG_LEVEL': 'ERROR',  # Changed from WARNING
        'LITELLM_PROXY_VERBOSE': 'false',
        'LITELLM_PROXY_DEBUG_MODE': 'false',
        'LITELLM_PROXY_LOG_LEVEL_DEBUG': 'false',
        
        # JSON logging suppression
        'JSON_LOGS': 'false',
        
        # Cold storage and components - ERROR level
        'LITELLM_COLD_STORAGE_LOG_LEVEL': 'ERROR',  # Changed from WARNING
        
        # Discernus settings
        'DISCERNUS_LOG_LEVEL': 'WARNING',
        'DISCERNUS_VERBOSE': 'false',
    }
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ.setdefault(key, value)
    
    # Configure Python loggers for proxy components that cause debug flooding
    problematic_loggers = [
        'litellm',
        'LiteLLM',
        'litellm.proxy',
        'LiteLLM Proxy',  # The main culprit from terminal output
        'litellm.proxy.guardrails',
        'litellm.proxy.guardrails.guardrail_registry',
        'litellm.proxy.auth.litellm_license', 
        'litellm.proxy.cold_storage_handler',
        'litellm_proxy',
    ]
    
    for logger_name in problematic_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.ERROR)
        logger.disabled = True  # Completely disable problematic loggers
        
        # Remove handlers to prevent output
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    # Install message filter to catch any remaining debug output
    class LiteLLMDebugFilter(logging.Filter):
        def filter(self, record):
            message = record.getMessage().lower()
            # Suppress specific patterns seen in terminal output
            suppress_patterns = [
                'litellm proxy:debug',
                'discovering guardrails',
                'license str value', 
                'cold storage',
                'guardrail_registry',
                'litellm_license',
                'is_premium',
            ]
            return not any(pattern in message for pattern in suppress_patterns)
    
    # Add filter to root logger
    logging.getLogger().addFilter(LiteLLMDebugFilter())
    
    # Use print instead of logger since logger isn't configured yet
    # Avoid printing directly; rely on logger if needed

# LiteLLM debug suppression is now called explicitly from CLI and LLM Gateway
# to prevent multiple executions and duplicate messages

def setup_logging(
    experiment_path: Path,
    run_folder: Path,
    log_level: str = "INFO",
    console_output: bool = True,
    file_output: bool = True,
    structured: bool = True
) -> None:
    """
    Set up comprehensive logging for an experiment run.
    
    Args:
        experiment_path: Path to experiment directory
        run_folder: Path to current run folder
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to output to console
        file_output: Whether to output to files
        structured: Whether to use structured logging format
    """
    
    # Create logs directory
    logs_dir = run_folder / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Console handler with color and structured formatting
    if console_output:
        if structured:
            # Structured console output with colors
            logger.add(
                sys.stdout,
                format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
                level=log_level,
                colorize=True,
                backtrace=True,
                diagnose=True
            )
        else:
            # Simple console output
            logger.add(
                sys.stdout,
                format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
                level=log_level,
                colorize=True
            )
    
    # File handlers for different log types
    if file_output:
        # Main application log
        logger.add(
            logs_dir / "application.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level=log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        # Error log (only errors and critical)
        logger.add(
            logs_dir / "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="5 MB",
            retention="30 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        # Performance log (timing and metrics)
        logger.add(
            logs_dir / "performance.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {message}",
            level="INFO",
            filter=lambda record: "performance" in record["extra"] or "timing" in record["extra"],
            rotation="5 MB",
            retention="7 days",
            compression="zip"
        )
        
        # LLM interactions log
        logger.add(
            logs_dir / "llm_interactions.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {message}",
            level="INFO",
            filter=lambda record: "llm" in record["extra"] or "model" in record["extra"],
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
    
    # Log system information
    logger.info("Logging system initialized", extra={
        "experiment_path": str(experiment_path),
        "run_folder": str(run_folder),
        "log_level": log_level,
        "console_output": console_output,
        "file_output": file_output,
        "structured": structured
    })

def get_logger(name: str):
    """
    Get a logger instance for a specific component.
    
    Args:
        name: Component name (e.g., "orchestrator", "analysis_agent")
        
    Returns:
        Logger instance configured for the component
    """
    return logger.bind(name=name)

def log_experiment_start(experiment_name: str, run_id: str, **kwargs) -> None:
    """Log experiment start with comprehensive context."""
    logger.info("Experiment started", extra={
        "event": "experiment_start",
        "experiment_name": experiment_name,
        "run_id": run_id,
        **kwargs
    })

def log_experiment_complete(experiment_name: str, run_id: str, duration_seconds: float, **kwargs) -> None:
    """Log experiment completion with timing and results."""
    logger.info("Experiment completed", extra={
        "event": "experiment_complete",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "duration_seconds": duration_seconds,
        **kwargs
    })

def log_experiment_failure(experiment_name: str, run_id: str, error: str, stage: str, **kwargs) -> None:
    """Log experiment failure with detailed context."""
    logger.error("Experiment failed", extra={
        "event": "experiment_failure",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "error": error,
        "stage": stage,
        **kwargs
    })

def log_agent_operation(agent_name: str, operation: str, status: str, **kwargs) -> None:
    """Log agent operation with status and context."""
    level = "INFO" if status == "success" else "WARNING" if status == "partial" else "ERROR"
    logger.log(level, f"Agent operation: {operation}", extra={
        "event": "agent_operation",
        "agent_name": agent_name,
        "operation": operation,
        "status": status,
        **kwargs
    })

def log_llm_interaction(model: str, operation: str, tokens_used: int, cost_usd: float, **kwargs) -> None:
    """Log LLM interaction with cost and usage metrics."""
    logger.info("LLM interaction", extra={
        "event": "llm_interaction",
        "model": model,
        "operation": operation,
        "tokens_used": tokens_used,
        "cost_usd": cost_usd,
        "llm": True,
        **kwargs
    })

def log_performance_metric(metric_name: str, value: float, unit: str, **kwargs) -> None:
    """Log performance metric with timing information."""
    logger.info(f"Performance metric: {metric_name} = {value} {unit}", extra={
        "event": "performance_metric",
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "performance": True,
        **kwargs
    })

def log_stage_transition(from_stage: str, to_stage: str, duration_seconds: float, **kwargs) -> None:
    """Log stage transition with timing information."""
    logger.info(f"Stage transition: {from_stage} → {to_stage}", extra={
        "event": "stage_transition",
        "from_stage": from_stage,
        "to_stage": to_stage,
        "duration_seconds": duration_seconds,
        **kwargs
    })

def log_analysis_phase_start(experiment_name: str, run_id: str, document_count: int, **kwargs) -> None:
    """Log analysis phase start with document count and context."""
    logger.info("Analysis phase started", extra={
        "event": "analysis_phase_start",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "document_count": document_count,
        "stage": "analysis",
        **kwargs
    })

def log_analysis_phase_complete(experiment_name: str, run_id: str, duration_seconds: float, documents_processed: int, **kwargs) -> None:
    """Log analysis phase completion with timing and results."""
    logger.info("Analysis phase completed", extra={
        "event": "analysis_phase_complete",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "duration_seconds": duration_seconds,
        "documents_processed": documents_processed,
        "stage": "analysis",
        **kwargs
    })

def log_synthesis_phase_start(experiment_name: str, run_id: str, analysis_artifacts_count: int, **kwargs) -> None:
    """Log synthesis phase start with artifact count and context."""
    logger.info("Synthesis phase started", extra={
        "event": "synthesis_phase_start",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "analysis_artifacts_count": analysis_artifacts_count,
        "stage": "synthesis",
        **kwargs
    })

def log_synthesis_phase_complete(experiment_name: str, run_id: str, duration_seconds: float, synthesis_artifacts_count: int, **kwargs) -> None:
    """Log synthesis phase completion with timing and results."""
    logger.info("Synthesis phase completed", extra={
        "event": "synthesis_phase_complete",
        "experiment_name": experiment_name,
        "run_id": run_id,
        "duration_seconds": duration_seconds,
        "synthesis_artifacts_count": synthesis_artifacts_count,
        "stage": "synthesis",
        **kwargs
    })

def log_error_with_context(error: Exception, context: Dict[str, Any], **kwargs) -> None:
    """Log error with full context for debugging."""
    logger.error(f"Error occurred: {str(error)}", extra={
        "event": "error",
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
        **kwargs
    }, exc_info=True)

def log_warning_with_context(warning: str, context: Dict[str, Any], **kwargs) -> None:
    """Log warning with context for monitoring."""
    logger.warning(f"Warning: {warning}", extra={
        "event": "warning",
        "warning_message": warning,
        "context": context,
        **kwargs
    })

def log_info_with_context(message: str, context: Dict[str, Any], **kwargs) -> None:
    """Log informational message with context."""
    logger.info(message, extra={
        "event": "info",
        "message": message,
        "context": context,
        **kwargs
    })

def log_debug_with_context(message: str, context: Dict[str, Any], **kwargs) -> None:
    """Log debug message with context."""
    logger.debug(message, extra={
        "event": "debug",
        "message": message,
        "context": context,
        **kwargs
    })

@contextmanager
def perf_timer(operation_name: str, **context):
    """
    Ultra-thin performance timing context manager.
    
    Automatically times operations and logs to performance.log with zero overhead
    when performance logging is disabled.
    
    Usage:
        with perf_timer("llm_call", model="gpt-4", tokens=1500):
            response = call_llm()
        
        with perf_timer("file_io", operation="save", file_size=1024):
            save_artifact()
    
    Args:
        operation_name: Human-readable name for the operation
        **context: Additional context to include in performance log
    """
    start_time = time.perf_counter()
    start_memory = None
    
    # Optional memory tracking (low overhead)
    try:
        import psutil
        process = psutil.Process()
        start_memory = process.memory_info().rss
    except (ImportError, Exception):
        # Graceful degradation if psutil not available
        pass
    
    try:
        yield
    finally:
        # Calculate timing
        duration = time.perf_counter() - start_time
        
        # Calculate memory delta if available
        memory_delta = None
        if start_memory is not None:
            try:
                end_memory = process.memory_info().rss
                memory_delta = end_memory - start_memory
            except Exception:
                pass
        
        # Build performance log entry
        perf_context = {
            "performance": True,
            "timing": True,
            "operation": operation_name,
            "duration_seconds": duration,
            **context
        }
        
        # Add memory info if available
        if memory_delta is not None:
            perf_context["memory_delta_bytes"] = memory_delta
        
        # Log performance data
        logger.info(f"Performance: {operation_name} completed in {duration:.3f}s", extra=perf_context)
        
        # Also log to audit logger if available (for research provenance)
        try:
            from discernus.core.audit_logger import get_audit_logger
            audit = get_audit_logger()
            if audit:
                audit.log_performance_metric(
                    metric_name=f"{operation_name}_duration",
                    value=duration,
                    context=context
                )
        except (ImportError, AttributeError, Exception):
            # Graceful degradation if audit logger not available
            pass

def setup_logging_for_run(run_folder: Path):
    """
    Configures the root logger to output to both console and a file for a specific run.
    """
    log_dir = run_folder / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir / "discernus_run.log"

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # Capture everything

    # Remove existing handlers to avoid duplication if this is called multiple times
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create file handler
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG) # Log everything to the file

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING) # Only show WARNING and above on the console

    # Add handlers to the root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return log_file_path
