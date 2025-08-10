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

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

# Remove default loguru handler
logger.remove()

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

def get_logger(name: str) -> "logger":
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
