#!/usr/bin/env python3
"""
Verbose Tracing System for Discernus
====================================

Provides comprehensive function-level tracing for debugging complex execution flows.
This replaces the primitive "add debug prints" approach with systematic tracing.

Features:
- Function entry/exit logging with parameters and return values
- Call stack depth visualization
- Performance timing
- Conditional activation via environment variable
- Integration with existing loguru infrastructure
"""

import os
import time
import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional
from contextlib import contextmanager

# Use standard Python logging instead of loguru for compatibility
logger = logging.getLogger("verbose_tracing")

# Global tracing state
_tracing_enabled = os.getenv('DISCERNUS_VERBOSE_TRACE', 'false').lower() == 'true'
_trace_depth = 0
_trace_filters = set(os.getenv('DISCERNUS_TRACE_FILTERS', '').split(',')) if os.getenv('DISCERNUS_TRACE_FILTERS') else set()

def enable_tracing(filters: Optional[list] = None):
    """Enable verbose tracing globally."""
    global _tracing_enabled, _trace_filters
    _tracing_enabled = True
    if filters:
        _trace_filters = set(filters)
    
    # Set logger to DEBUG level to capture trace messages
    logger.setLevel(logging.DEBUG)
    
    # Add console handler if not already present
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('TRACE: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Don't propagate to root logger
    
    logger.info(f"Verbose tracing enabled (filters: {list(_trace_filters)})")

def disable_tracing():
    """Disable verbose tracing globally."""
    global _tracing_enabled
    _tracing_enabled = False
    logger.info("Verbose tracing disabled")

def should_trace(func_name: str, class_name: str = None) -> bool:
    """Determine if a function should be traced based on filters."""
    if not _tracing_enabled:
        return False
    
    if not _trace_filters:
        return True
    
    # Check if any filter matches
    full_name = f"{class_name}.{func_name}" if class_name else func_name
    return any(filter_name in full_name.lower() for filter_name in _trace_filters)

def trace_calls(include_args: bool = True, include_return: bool = True, max_arg_length: int = 200):
    """
    Decorator for comprehensive function tracing.
    
    Args:
        include_args: Whether to log function arguments
        include_return: Whether to log return values
        max_arg_length: Maximum length for argument/return value strings
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global _trace_depth
            
            # Get function metadata
            func_name = func.__name__
            class_name = None
            if args and hasattr(args[0], '__class__'):
                class_name = args[0].__class__.__name__
            
            # Check if we should trace this function
            if not should_trace(func_name, class_name):
                return func(*args, **kwargs)
            
            # Create indentation for call depth
            indent = "  " * _trace_depth
            full_name = f"{class_name}.{func_name}" if class_name else func_name
            
            # Format arguments
            arg_info = ""
            if include_args and (args or kwargs):
                try:
                    # Get function signature for parameter names
                    sig = inspect.signature(func)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    
                    # Format arguments with names
                    arg_parts = []
                    for name, value in bound_args.arguments.items():
                        if name == 'self':
                            continue
                        value_str = repr(value)
                        if len(value_str) > max_arg_length:
                            value_str = value_str[:max_arg_length] + "..."
                        arg_parts.append(f"{name}={value_str}")
                    
                    if arg_parts:
                        arg_info = f" with {', '.join(arg_parts)}"
                except Exception as e:
                    arg_info = f" (arg formatting error: {e})"
            
            # Log function entry
            logger.debug(f"{indent}→ {full_name}(){arg_info}")
            
            # Execute function with timing
            _trace_depth += 1
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful exit
                execution_time = time.perf_counter() - start_time
                return_info = ""
                if include_return and result is not None:
                    try:
                        result_str = repr(result)
                        if len(result_str) > max_arg_length:
                            result_str = result_str[:max_arg_length] + "..."
                        return_info = f" → {result_str}"
                    except Exception as e:
                        return_info = f" → (return formatting error: {e})"
                
                logger.debug(f"{indent}← {full_name}(){return_info} [{execution_time:.3f}s]")
                
                return result
                
            except Exception as e:
                # Log exception exit
                execution_time = time.perf_counter() - start_time
                logger.debug(f"{indent}✗ {full_name}() raised {type(e).__name__}: {e} [{execution_time:.3f}s]")
                raise
            finally:
                _trace_depth -= 1
        
        return wrapper
    return decorator

@contextmanager
def trace_section(section_name: str, **context):
    """Context manager for tracing code sections."""
    global _trace_depth
    
    if not _tracing_enabled:
        yield
        return
    
    indent = "  " * _trace_depth
    logger.debug(f"{indent}▼ {section_name}", extra={
        "trace": True,
        "section": section_name,
        "depth": _trace_depth,
        "event": "section_start",
        **context
    })
    
    _trace_depth += 1
    start_time = time.perf_counter()
    
    try:
        yield
        execution_time = time.perf_counter() - start_time
        logger.debug(f"{indent}▲ {section_name} [{execution_time:.3f}s]", extra={
            "trace": True,
            "section": section_name,
            "depth": _trace_depth - 1,
            "event": "section_end",
            "execution_time": execution_time
        })
    except Exception as e:
        execution_time = time.perf_counter() - start_time
        logger.debug(f"{indent}✗ {section_name} failed: {e} [{execution_time:.3f}s]", extra={
            "trace": True,
            "section": section_name,
            "depth": _trace_depth - 1,
            "event": "section_exception",
            "execution_time": execution_time,
            "exception": str(e)
        })
        raise
    finally:
        _trace_depth -= 1

def trace_data(name: str, data: Any, max_length: int = 500):
    """Log data structures for debugging."""
    if not _tracing_enabled:
        return
    
    indent = "  " * _trace_depth
    try:
        data_str = repr(data)
        if len(data_str) > max_length:
            data_str = data_str[:max_length] + "..."
        logger.debug(f"{indent}📊 {name}: {data_str}", extra={
            "trace": True,
            "data_name": name,
            "depth": _trace_depth,
            "event": "data"
        })
    except Exception as e:
        logger.debug(f"{indent}📊 {name}: (formatting error: {e})", extra={
            "trace": True,
            "data_name": name,
            "depth": _trace_depth,
            "event": "data_error"
        })

# Convenience function for quick tracing setup
def setup_verbose_tracing(enabled: bool = True, filters: Optional[list] = None):
    """Setup verbose tracing with optional filters."""
    if enabled:
        enable_tracing(filters)
    else:
        disable_tracing()
