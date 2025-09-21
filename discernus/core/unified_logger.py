#!/usr/bin/env python3
"""
Unified Logging System for Discernus
===================================

Provides a unified logging interface that combines loguru's structured logging
with Rich console output for immediate display of critical messages.

Features:
- Immediate display for critical messages (errors, warnings)
- Buffered display for info/debug messages
- Consistent formatting across all components
- Priority-based message handling
- Thread-safe operations
"""

import sys
import threading
from typing import Optional, Dict, Any
from pathlib import Path
from loguru import logger
from rich.console import Console
from rich.text import Text
from rich.markup import escape

class UnifiedLogger:
    """
    Unified logging system that provides immediate display for critical messages
    while maintaining structured logging for all messages.
    """
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self._lock = threading.Lock()
        
        # Message priority levels
        self.CRITICAL = 1
        self.ERROR = 2
        self.WARNING = 3
        self.INFO = 4
        self.DEBUG = 5
        
        # Immediate display thresholds
        self.IMMEDIATE_THRESHOLD = self.ERROR  # Show ERROR and above immediately
        
    def _immediate_display(self, level: int, message: str, **kwargs):
        """Display message immediately to console with appropriate styling."""
        with self._lock:
            if level <= self.ERROR:
                # Critical/Error messages - bold red
                self.console.print(f"🚨 {message}", style="bold red", **kwargs)
            elif level == self.WARNING:
                # Warning messages - yellow
                self.console.print(f"⚠️  {message}", style="yellow", **kwargs)
            else:
                # Info/Debug messages - blue
                self.console.print(f"ℹ️  {message}", style="blue", **kwargs)
            
            # Force immediate flush
            sys.stdout.flush()
    
    def _should_display_immediately(self, level: int, critical: bool = False) -> bool:
        """Determine if message should be displayed immediately."""
        return critical or level <= self.IMMEDIATE_THRESHOLD
    
    def critical(self, message: str, critical: bool = True, **kwargs):
        """Log critical message with immediate display."""
        if self._should_display_immediately(self.CRITICAL, critical):
            self._immediate_display(self.CRITICAL, message, **kwargs)
        logger.critical(message, **kwargs)
    
    def error(self, message: str, critical: bool = True, **kwargs):
        """Log error message with immediate display."""
        if self._should_display_immediately(self.ERROR, critical):
            self._immediate_display(self.ERROR, message, **kwargs)
        logger.error(message, **kwargs)
    
    def warning(self, message: str, critical: bool = False, **kwargs):
        """Log warning message with optional immediate display."""
        if self._should_display_immediately(self.WARNING, critical):
            self._immediate_display(self.WARNING, message, **kwargs)
        logger.warning(message, **kwargs)
    
    def info(self, message: str, critical: bool = False, **kwargs):
        """Log info message with optional immediate display."""
        if self._should_display_immediately(self.INFO, critical):
            self._immediate_display(self.INFO, message, **kwargs)
        logger.info(message, **kwargs)
    
    def debug(self, message: str, critical: bool = False, **kwargs):
        """Log debug message with optional immediate display."""
        if self._should_display_immediately(self.DEBUG, critical):
            self._immediate_display(self.DEBUG, message, **kwargs)
        logger.debug(message, **kwargs)
    
    def success(self, message: str, critical: bool = False, **kwargs):
        """Log success message with optional immediate display."""
        if self._should_display_immediately(self.INFO, critical):
            with self._lock:
                self.console.print(f"✅ {message}", style="green", **kwargs)
                sys.stdout.flush()
        logger.info(f"SUCCESS: {message}", **kwargs)
    
    def progress(self, message: str, **kwargs):
        """Log progress message with immediate display."""
        with self._lock:
            self.console.print(f"🔄 {message}", style="cyan", **kwargs)
            sys.stdout.flush()
        logger.info(f"PROGRESS: {message}", **kwargs)
    
    def verification_failed(self, document_index: int, status: str, **kwargs):
        """Log verification failure with immediate display and clear context."""
        message = f"Document {document_index} verification failed with status: {status} - continuing with other documents"
        if self._should_display_immediately(self.WARNING, True):
            self._immediate_display(self.WARNING, message, **kwargs)
        logger.warning(message, **kwargs)
    
    def llm_call(self, model: str, attempt: int, max_attempts: int, **kwargs):
        """Log LLM call attempt with immediate display."""
        message = f"Attempting call with {model} (Attempt {attempt}/{max_attempts})..."
        if self._should_display_immediately(self.INFO, True):
            self._immediate_display(self.INFO, message, **kwargs)
        logger.info(message, **kwargs)
    
    def phase_start(self, phase: str, **kwargs):
        """Log phase start with immediate display."""
        message = f"🚀 Starting {phase}..."
        if self._should_display_immediately(self.INFO, True):
            self._immediate_display(self.INFO, message, **kwargs)
        logger.info(message, **kwargs)
    
    def phase_complete(self, phase: str, **kwargs):
        """Log phase completion with immediate display."""
        message = f"✅ {phase} completed"
        if self._should_display_immediately(self.INFO, True):
            self._immediate_display(self.INFO, message, **kwargs)
        logger.info(message, **kwargs)

# Global unified logger instance
unified_logger = UnifiedLogger()

def get_unified_logger() -> UnifiedLogger:
    """Get the global unified logger instance."""
    return unified_logger

def setup_unified_logging(
    experiment_path: Path,
    run_folder: Path,
    log_level: str = "INFO",
    console_output: bool = True,
    file_output: bool = True,
    structured: bool = True
) -> UnifiedLogger:
    """
    Set up unified logging system for an experiment run.
    
    Args:
        experiment_path: Path to experiment directory
        run_folder: Path to current run folder
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to output to console
        file_output: Whether to output to files
        structured: Whether to use structured logging format
        
    Returns:
        Configured UnifiedLogger instance
    """
    # Import here to avoid circular imports
    from .logging_config import setup_logging
    
    # Set up traditional loguru logging
    setup_logging(experiment_path, run_folder, log_level, console_output, file_output, structured)
    
    # Return configured unified logger
    return unified_logger
