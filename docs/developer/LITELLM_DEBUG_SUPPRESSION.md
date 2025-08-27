# LiteLLM Debug Suppression System

## Overview

The Discernus platform has implemented a comprehensive system to suppress verbose debug output from LiteLLM and its proxy components. This system ensures clean terminal output during experiments while maintaining full debug logging to files for debugging purposes.

## Problem Solved

Previously, LiteLLM was generating excessive debug output including:
- Verbose proxy logging messages
- Cold storage configuration messages
- Guardrail discovery logs
- Embedding debug information

This made experiments unreadable and violated the project's "human-centric UX" principle.

## Solution Architecture

### 1. Environment Variable Configuration

The system sets multiple environment variables to suppress different types of LiteLLM debug output:

```bash
# Core LiteLLM settings
LITELLM_VERBOSE=false
LITELLM_LOG=WARNING
LITELLM_LOG_LEVEL=WARNING

# Proxy-specific settings
LITELLM_PROXY_DEBUG=false
LITELLM_PROXY_LOG_LEVEL=WARNING
LITELLM_PROXY_VERBOSE=false
LITELLM_PROXY_DEBUG_MODE=false
LITELLM_PROXY_LOG_LEVEL_DEBUG=false

# Cold storage and other components
LITELLM_COLD_STORAGE_LOG_LEVEL=WARNING

# Additional Discernus-specific settings
DISCERNUS_LOG_LEVEL=WARNING
DISCERNUS_VERBOSE=false
```

### 2. Multiple Configuration Points

The system configures LiteLLM debug suppression at multiple levels:

#### A. Python Code Level
- **`discernus/gateway/llm_gateway.py`**: Sets environment variables during LLM Gateway initialization
- **`discernus/cli.py`**: Sets environment variables during CLI startup
- **`discernus/__main__.py`**: Sets environment variables before any imports
- **`discernus/core/logging_config.py`**: Ensures environment variables are set during logging configuration

#### B. Programmatic Configuration
- **`litellm.set_verbose = False`**: Directly disables LiteLLM verbose mode
- **`litellm.verbose_logger.setLevel('WARNING')`**: Configures verbose logger to WARNING level

#### C. Shell Script Level
- **`scripts/set_litellm_env.sh`**: Shell script to set environment variables in current shell
- **`Makefile`**: Make targets for managing LiteLLM debug suppression

### 3. Utility Scripts

#### A. Python Suppression Script
```bash
python3 scripts/suppress_litellm_debug.py
```

This script:
- Sets all necessary environment variables
- Configures LiteLLM programmatically
- Provides feedback on configuration status

#### B. Shell Environment Script
```bash
source scripts/set_litellm_env.sh
```

This script:
- Sets environment variables in current shell
- Provides visual feedback
- Can be sourced for persistent configuration

#### C. Test Script
```bash
python3 scripts/test_litellm_suppression.py
```

This script:
- Tests current environment variable configuration
- Verifies LiteLLM import and configuration
- Provides comprehensive status report

## Usage

### 1. Make Targets

The Makefile provides several targets for managing LiteLLM debug suppression:

```bash
# Check current environment variables
make litellm-check

# Set environment variables using shell script
make litellm-env

# Set environment variables using Python script
make litellm-python

# Test current configuration
make litellm-test

# Complete setup and test
make litellm-setup
```

### 2. Manual Configuration

#### A. For Current Session
```bash
# Set environment variables in current shell
export LITELLM_VERBOSE=false
export LITELLM_LOG_LEVEL=WARNING
export LITELLM_PROXY_LOG_LEVEL=WARNING
```

#### B. For Python Scripts
```python
import os
os.environ['LITELLM_VERBOSE'] = 'false'
os.environ['LITELLM_LOG_LEVEL'] = 'WARNING'
os.environ['LITELLM_PROXY_LOG_LEVEL'] = 'WARNING'
```

### 3. Persistent Configuration

To make the configuration persistent across sessions:

1. **Add to shell profile** (e.g., `~/.zshrc`, `~/.bashrc`):
   ```bash
   source /path/to/discernus/scripts/set_litellm_env.sh
   ```

2. **Use Makefile targets** in each session:
   ```bash
   make litellm-python
   ```

## Verification

### 1. Check Environment Variables
```bash
make litellm-check
```

Expected output:
```
🔍 Checking current LiteLLM environment variables...
LITELLM_VERBOSE: false
LITELLM_LOG_LEVEL: WARNING
LITELLM_PROXY_LOG_LEVEL: WARNING
LITELLM_PROXY_DEBUG: false
```

### 2. Test Configuration
```bash
make litellm-test
```

Expected output:
```
🔍 Testing LiteLLM Debug Suppression
==================================================

📋 Current Environment Variables:
   ✅ LITELLM_VERBOSE: false
   ✅ LITELLM_LOG: WARNING
   ✅ LITELLM_LOG_LEVEL: WARNING
   ✅ LITELLM_PROXY_DEBUG: false
   ✅ LITELLM_PROXY_LOG_LEVEL: WARNING
   ✅ LITELLM_PROXY_VERBOSE: false
   ✅ LITELLM_PROXY_DEBUG_MODE: false
   ✅ LITELLM_COLD_STORAGE_LOG_LEVEL: WARNING

🧪 Testing LiteLLM Import:
   ✅ LiteLLM imported successfully
   📊 litellm.set_verbose: False
   📊 verbose_logger level: 20
   ✅ LiteLLM configuration appears correct
```

### 3. Complete Setup Test
```bash
make litellm-setup
```

This runs both the setup and test in sequence.

## Troubleshooting

### 1. Environment Variables Not Set

**Problem**: Environment variables show as "NOT SET" in tests.

**Solution**: 
```bash
# Set environment variables
make litellm-python

# Or manually
export LITELLM_VERBOSE=false
export LITELLM_LOG_LEVEL=WARNING
```

### 2. Debug Output Still Appearing

**Problem**: LiteLLM debug messages still appear despite configuration.

**Solution**:
1. Check if environment variables are set: `make litellm-check`
2. Verify Python configuration: `make litellm-test`
3. Ensure configuration is applied before LiteLLM import
4. Check for conflicting logging configurations

### 3. Configuration Not Persisting

**Problem**: Configuration resets after shell restart.

**Solution**:
1. Add to shell profile: `source scripts/set_litellm_env.sh`
2. Use Makefile targets in each session: `make litellm-python`
3. Set environment variables in your workflow scripts

## Technical Details

### 1. Environment Variable Priority

The system uses `os.environ.setdefault()` to ensure environment variables are set only if they don't already exist, allowing for override by external configuration.

### 2. Import Order

Environment variables are set before any LiteLLM imports to ensure they take effect immediately.

### 3. Fallback Configuration

If environment variables fail, the system falls back to programmatic configuration using `litellm.set_verbose = False`.

### 4. Logging Integration

The system integrates with Discernus's logging configuration to ensure consistent behavior across all components.

## Benefits

1. **Clean Terminal Output**: Experiments are now readable without debug noise
2. **Maintained Debug Capability**: Full debug logging still goes to files
3. **Multiple Configuration Methods**: Flexible setup options for different use cases
4. **Comprehensive Coverage**: All LiteLLM debug output types are suppressed
5. **Easy Verification**: Simple commands to check and test configuration
6. **Integration**: Works seamlessly with existing Discernus infrastructure

## Future Enhancements

1. **Configuration File**: Add support for `.discernus.yaml` configuration
2. **Dynamic Configuration**: Allow runtime configuration changes
3. **Selective Suppression**: Allow fine-grained control over what gets suppressed
4. **Monitoring**: Add logging to track when suppression is active/inactive

## References

- **LiteLLM Documentation**: [https://docs.litellm.ai/](https://docs.litellm.ai/)
- **Discernus Logging**: `discernus/core/logging_config.py`
- **LLM Gateway**: `discernus/gateway/llm_gateway.py`
- **CLI**: `discernus/cli.py`
