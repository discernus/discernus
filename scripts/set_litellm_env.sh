#!/bin/bash
# LiteLLM Debug Suppression Environment Variables
# Source this script to suppress verbose debug output from LiteLLM

export LITELLM_VERBOSE=false
export LITELLM_LOG=WARNING
export LITELLM_PROXY_DEBUG=false
export LITELLM_PROXY_LOG_LEVEL=WARNING
export LITELLM_LOG_LEVEL=WARNING
export LITELLM_COLD_STORAGE_LOG_LEVEL=WARNING
export LITELLM_PROXY_VERBOSE=false
export LITELLM_PROXY_DEBUG_MODE=false
export LITELLM_PROXY_LOG_LEVEL_DEBUG=false

# Additional Discernus-specific environment variables
export DISCERNUS_LOG_LEVEL=WARNING
export DISCERNUS_VERBOSE=false

echo "✅ LiteLLM debug suppression environment variables set"
echo "   LITELLM_LOG_LEVEL=$LITELLM_LOG_LEVEL"
echo "   LITELLM_PROXY_LOG_LEVEL=$LITELLM_PROXY_LOG_LEVEL"
echo "   LITELLM_VERBOSE=$LITELLM_VERBOSE"
