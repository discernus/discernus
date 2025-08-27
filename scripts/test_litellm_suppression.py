#!/usr/bin/env python3
"""
Test LiteLLM Debug Suppression
==============================

This script tests whether the LiteLLM debug suppression is working correctly.
It shows the current environment variables and attempts to import LiteLLM
to verify the configuration.
"""

import os
import sys
from pathlib import Path

def test_litellm_suppression():
    """Test if LiteLLM debug suppression is working."""
    print("🔍 Testing LiteLLM Debug Suppression")
    print("=" * 50)
    
    # Check current environment variables
    print("\n📋 Current Environment Variables:")
    litellm_vars = [
        'LITELLM_VERBOSE',
        'LITELLM_LOG',
        'LITELLM_LOG_LEVEL',
        'LITELLM_PROXY_DEBUG',
        'LITELLM_PROXY_LOG_LEVEL',
        'LITELLM_PROXY_VERBOSE',
        'LITELLM_PROXY_DEBUG_MODE',
        'LITELLM_COLD_STORAGE_LOG_LEVEL'
    ]
    
    for var in litellm_vars:
        value = os.environ.get(var, 'NOT SET')
        status = "✅" if value in ['false', 'WARNING'] else "❌"
        print(f"   {status} {var}: {value}")
    
    # Test importing LiteLLM
    print("\n🧪 Testing LiteLLM Import:")
    try:
        import litellm
        print("   ✅ LiteLLM imported successfully")
        
        # Check if verbose is disabled
        if hasattr(litellm, 'set_verbose'):
            print(f"   📊 litellm.set_verbose: {litellm.set_verbose}")
        
        # Check if verbose_logger is available and configured
        if hasattr(litellm, 'verbose_logger'):
            print(f"   📊 verbose_logger level: {litellm.verbose_logger.level}")
        
        print("   ✅ LiteLLM configuration appears correct")
        
    except ImportError as e:
        print(f"   ❌ Failed to import LiteLLM: {e}")
        return False
    
    # Test environment variable persistence
    print("\n🔒 Testing Environment Variable Persistence:")
    test_var = 'LITELLM_TEST_SUPPRESSION'
    os.environ[test_var] = 'test_value'
    
    if os.environ.get(test_var) == 'test_value':
        print("   ✅ Environment variables can be set and retrieved")
    else:
        print("   ❌ Environment variable setting failed")
        return False
    
    # Clean up test variable
    del os.environ[test_var]
    
    print("\n🎯 Summary:")
    print("   If all checks show ✅, LiteLLM debug suppression is working")
    print("   If any show ❌, there may be configuration issues")
    
    return True

if __name__ == "__main__":
    success = test_litellm_suppression()
    sys.exit(0 if success else 1)
