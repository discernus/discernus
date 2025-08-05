#!/usr/bin/env python3
"""
Discernus CLI Exit Codes
========================

Semantic exit codes following Unix conventions for better CI/CD integration
and error handling.

Exit Code Conventions:
- 0: Success
- 1: General error
- 2: Invalid usage/command line arguments
- 3: Validation failed
- 4: Infrastructure error
- 5: File/permission error
- 6: Configuration error
"""

import sys
from enum import IntEnum


class ExitCode(IntEnum):
    """Semantic exit codes for Discernus CLI."""
    
    # Success
    SUCCESS = 0
    
    # Error categories
    GENERAL_ERROR = 1          # General/unknown error
    INVALID_USAGE = 2          # Invalid command line usage
    VALIDATION_FAILED = 3      # Experiment/config validation failed
    INFRASTRUCTURE_ERROR = 4   # External service/infrastructure error
    FILE_ERROR = 5            # File not found, permission denied, etc.
    CONFIG_ERROR = 6          # Configuration file error


def exit_with_code(code: ExitCode, message: str = None):
    """
    Exit with semantic exit code and optional message.
    
    Args:
        code: ExitCode enum value
        message: Optional error message to print
    """
    if message:
        print(f"Error: {message}", file=sys.stderr)
    
    sys.exit(code.value)


def exit_success(message: str = None):
    """Exit with success code."""
    if message:
        print(message)
    sys.exit(ExitCode.SUCCESS.value)


def exit_general_error(message: str):
    """Exit with general error code."""
    exit_with_code(ExitCode.GENERAL_ERROR, message)


def exit_invalid_usage(message: str):
    """Exit with invalid usage code."""
    exit_with_code(ExitCode.INVALID_USAGE, message)


def exit_validation_failed(message: str):
    """Exit with validation failed code."""
    exit_with_code(ExitCode.VALIDATION_FAILED, message)


def exit_infrastructure_error(message: str):
    """Exit with infrastructure error code."""
    exit_with_code(ExitCode.INFRASTRUCTURE_ERROR, message)


def exit_file_error(message: str):
    """Exit with file error code."""
    exit_with_code(ExitCode.FILE_ERROR, message)


def exit_config_error(message: str):
    """Exit with configuration error code."""
    exit_with_code(ExitCode.CONFIG_ERROR, message)