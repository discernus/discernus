#!/usr/bin/env python3
"""
Comprehensive LiteLLM Debug Suppression
=======================================

This script provides the most thorough suppression of LiteLLM debug output,
targeting both the main LiteLLM library and all proxy components that generate
verbose logging.

The problem: LiteLLM Proxy has internal components (guardrail_registry, 
litellm_license, cold_storage_handler, etc.) that use their own loggers
and aren't controlled by standard LiteLLM environment variables.

This solution addresses all logging sources.
"""

import os
import sys
import logging
from pathlib import Path

def suppress_all_litellm_logging():
    """
    Comprehensive suppression of all LiteLLM logging, including proxy components.
    
    This function must be called BEFORE any LiteLLM imports to be fully effective.
    """
    
    # Environment Variables - Set to ERROR level (more restrictive than WARNING)
    env_vars = {
        # Core LiteLLM settings
        'LITELLM_VERBOSE': 'false',
        'LITELLM_LOG': 'ERROR',  # Changed from WARNING to ERROR
        'LITELLM_LOG_LEVEL': 'ERROR',  # Changed from WARNING to ERROR
        
        # Proxy-specific settings
        'LITELLM_PROXY_DEBUG': 'false',
        'LITELLM_PROXY_LOG_LEVEL': 'ERROR',  # Changed from WARNING to ERROR
        'LITELLM_PROXY_VERBOSE': 'false',
        'LITELLM_PROXY_DEBUG_MODE': 'false',
        'LITELLM_PROXY_LOG_LEVEL_DEBUG': 'false',
        
        # JSON logging (can contribute to volume)
        'JSON_LOGS': 'false',
        
        # Cold storage and other components
        'LITELLM_COLD_STORAGE_LOG_LEVEL': 'ERROR',  # Changed from WARNING to ERROR
        
        # Additional Discernus-specific settings
        'DISCERNUS_LOG_LEVEL': 'WARNING',
        'DISCERNUS_VERBOSE': 'false',
    }
    
    # Set all environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    # Configure Python logging to suppress LiteLLM loggers at the root level
    # This is crucial for proxy components that use standard Python logging
    
    # Get the root logger and set it to ERROR level
    root_logger = logging.getLogger()
    
    # Configure specific LiteLLM loggers that we know cause issues
    problematic_loggers = [
        'litellm',
        'LiteLLM',
        'litellm.proxy',
        'LiteLLM Proxy',  # This is the one causing our issues
        'litellm.proxy.guardrails',
        'litellm.proxy.guardrails.guardrail_registry',
        'litellm.proxy.auth.litellm_license',
        'litellm.proxy.cold_storage_handler',
        'litellm_proxy',
        'proxy',
    ]
    
    for logger_name in problematic_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.ERROR)
        logger.disabled = True  # Completely disable these loggers
        
        # Remove all handlers to prevent any output
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    # Also try to configure LiteLLM programmatically if already imported
    try:
        import litellm
        litellm.set_verbose = False
        
        # Configure verbose logger if available
        if hasattr(litellm, 'verbose_logger'):
            litellm.verbose_logger.setLevel(logging.ERROR)
            litellm.verbose_logger.disabled = True
            
        # Try to configure proxy logging if available
        try:
            from litellm.proxy import proxy_config
            if hasattr(proxy_config, 'set_verbose'):
                proxy_config.set_verbose(False)
        except (ImportError, AttributeError):
            pass
        
        print("✅ LiteLLM programmatic configuration applied")
        
    except ImportError:
        print("⚠️  LiteLLM not yet imported - configuration will apply on import")
    
    # Configure logging formatters to suppress specific patterns
    class LiteLLMSuppressingFilter(logging.Filter):
        """Filter to suppress specific LiteLLM log patterns"""
        
        def filter(self, record):
            message = record.getMessage().lower()
            
            # Patterns to suppress
            suppress_patterns = [
                'litellm proxy:debug',
                'discovering guardrails',
                'license str value',
                'cold storage',
                'guardrail_registry',
                'litellm_license',
                'is_premium',
                'guardrail initializer',
            ]
            
            for pattern in suppress_patterns:
                if pattern in message:
                    return False  # Suppress this message
                    
            return True  # Allow other messages
    
    # Add the filter to the root logger
    suppressing_filter = LiteLLMSuppressingFilter()
    root_logger.addFilter(suppressing_filter)
    
    print("✅ Comprehensive LiteLLM debug suppression configured")
    print(f"   Environment variables set: {len(env_vars)}")
    print(f"   Python loggers configured: {len(problematic_loggers)}")
    print(f"   Log message filter installed: Yes")
    
    return env_vars

def verify_suppression():
    """Verify that suppression is working by checking configuration."""
    
    print("\n🔍 Verifying LiteLLM Debug Suppression")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    critical_vars = [
        'LITELLM_VERBOSE',
        'LITELLM_LOG_LEVEL', 
        'LITELLM_PROXY_LOG_LEVEL',
        'LITELLM_PROXY_DEBUG',
        'JSON_LOGS'
    ]
    
    all_good = True
    for var in critical_vars:
        value = os.environ.get(var, 'NOT SET')
        status = "✅" if value != 'NOT SET' else "❌"
        print(f"   {status} {var}: {value}")
        if value == 'NOT SET':
            all_good = False
    
    # Check Python logger configuration
    print("\n📋 Python Logger Configuration:")
    test_loggers = ['litellm', 'LiteLLM Proxy', 'litellm.proxy']
    
    for logger_name in test_loggers:
        logger = logging.getLogger(logger_name)
        level_name = logging.getLevelName(logger.level)
        disabled_status = "DISABLED" if logger.disabled else "ENABLED"
        handler_count = len(logger.handlers)
        
        print(f"   📊 {logger_name}:")
        print(f"      Level: {level_name} | Status: {disabled_status} | Handlers: {handler_count}")
    
    # Check LiteLLM programmatic configuration
    print("\n📋 LiteLLM Programmatic Configuration:")
    try:
        import litellm
        verbose_setting = getattr(litellm, 'set_verbose', None)
        print(f"   ✅ litellm.set_verbose: {verbose_setting}")
        
        if hasattr(litellm, 'verbose_logger'):
            verbose_logger_level = logging.getLevelName(litellm.verbose_logger.level)
            verbose_logger_disabled = litellm.verbose_logger.disabled
            print(f"   ✅ verbose_logger level: {verbose_logger_level}")
            print(f"   ✅ verbose_logger disabled: {verbose_logger_disabled}")
        else:
            print("   ⚠️  verbose_logger not available")
            
    except ImportError:
        print("   ⚠️  LiteLLM not imported")
    
    if all_good:
        print("\n🎯 Status: All suppression mechanisms are properly configured")
    else:
        print("\n⚠️  Status: Some configuration issues detected")
    
    return all_good

if __name__ == "__main__":
    # Apply comprehensive suppression
    env_vars = suppress_all_litellm_logging()
    
    # Verify the configuration
    verify_suppression()
    
    # Save environment variables to a file for sourcing
    env_file = Path(__file__).parent / "litellm_env_vars.sh"
    
    with open(env_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Comprehensive LiteLLM Debug Suppression Environment Variables\n")
        f.write("# Generated by comprehensive_litellm_suppression.py\n\n")
        
        for key, value in env_vars.items():
            f.write(f"export {key}='{value}'\n")
        
        f.write("\necho '✅ LiteLLM debug suppression environment variables loaded'\n")
    
    print(f"\n💾 Environment variables saved to: {env_file}")
    print("   Source this file: source scripts/litellm_env_vars.sh")
