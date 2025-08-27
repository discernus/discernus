# Max Tokens Policy and Best Practices

## Overview

The Discernus project has implemented a centralized, intelligent `max_tokens` management system to prevent response truncation issues while maintaining safety guardrails against runaway token generation.

## Problem Statement

Previously, agents across the codebase were setting low `max_tokens` values (200, 1000, 4000, etc.) which caused:

1. **Response Truncation**: Important analysis, statistical results, or reports being cut off mid-generation
2. **Inconsistent Limits**: Different agents using different arbitrary limits
3. **Silent Failures**: Truncated responses often went unnoticed, leading to incomplete or invalid results
4. **Manual Maintenance**: Each agent required individual attention when token limits needed adjustment

## Solution Architecture

### Centralized Configuration

All `max_tokens` configuration is now managed in `discernus/gateway/models.yaml` with provider-specific safe defaults:

```yaml
provider_defaults:
  vertex_ai:
    safe_max_tokens: 65535    # Vertex AI max_output_tokens limit
  openai:
    safe_max_tokens: 128000   # Most OpenAI models support this limit  
  anthropic:
    safe_max_tokens: 100000   # Conservative limit, most models support higher
  mistral:
    safe_max_tokens: 32000    # Based on model context windows
  perplexity:
    safe_max_tokens: 100000   # Conservative limit
  openrouter:
    safe_max_tokens: 100000   # Varies by underlying model
```

### Intelligent Parameter Handling

The `ProviderParameterManager` now includes intelligent `max_tokens` handling:

1. **Automatic Safe Defaults**: When no `max_tokens` is specified, uses provider-specific safe limits
2. **Truncation Warnings**: Warns when `max_tokens` < 2000 (dangerously low threshold)
3. **Comprehensive Logging**: Logs all token limit decisions for debugging
4. **Provider Compatibility**: Respects provider-specific parameter restrictions

### Agent Simplification

Agents no longer need to specify `max_tokens` in most cases:

**Before:**
```python
response, metadata = self.llm_gateway.execute_call(
    model="vertex_ai/gemini-2.5-flash",
    prompt=prompt,
    max_tokens=8000  # Arbitrary limit that might truncate
)
```

**After:**
```python
response, metadata = self.llm_gateway.execute_call(
    model="vertex_ai/gemini-2.5-flash",
    prompt=prompt
    # max_tokens automatically handled by provider defaults
)
```

## Best Practices

### For Agent Developers

1. **Don't Set max_tokens**: Let the system handle safe defaults automatically
2. **Use High Values Only When Necessary**: If you must set `max_tokens`, use values > 10,000
3. **Monitor Warnings**: Pay attention to truncation warnings in logs
4. **Test Edge Cases**: Verify your agent handles long responses gracefully

### For Infrastructure Developers

1. **Update Provider Defaults**: Adjust `safe_max_tokens` in `models.yaml` when new models are added
2. **Monitor Token Usage**: Watch for patterns indicating insufficient limits
3. **Adjust Thresholds**: Update `DANGEROUSLY_LOW_THRESHOLD` if needed based on usage patterns

## Monitoring and Debugging

### Log Messages

The system provides comprehensive logging:

```
⚠️  WARNING: max_tokens=1000 for vertex_ai/gemini-2.5-flash may truncate responses
```

```
INFO: Using explicit max_tokens=8000 for anthropic/claude-3-5-sonnet-20241022
```

```
DEBUG: Applied safe max_tokens=65535 for vertex_ai/gemini-2.5-pro
```

### When to Investigate

Monitor for these warning patterns:

1. **Frequent Truncation Warnings**: Indicates agents or code still using low limits
2. **Empty or Incomplete Responses**: May indicate truncation at provider level
3. **Inconsistent Results**: Could suggest generation was cut off mid-analysis

## Migration Guide

### Existing Agents

All existing agents have been automatically updated by the `scripts/fix_max_tokens.py` script:

- Removed or commented out problematic `max_tokens` parameters
- Preserved useful comments about token usage
- Updated YAML configuration files

### New Agents

When creating new agents:

1. **Don't specify max_tokens** in most cases
2. **Use the base agent classes** which handle token management correctly
3. **Test with long responses** to ensure your agent handles full outputs properly

## Technical Details

### Provider-Specific Handling

The system respects provider-specific requirements:

- **Vertex AI**: Maps `max_tokens` → `max_output_tokens`
- **OpenAI/Anthropic/Others**: Uses standard `max_tokens` parameter
- **Forbidden Parameters**: Removes `max_tokens` when providers don't support it

### Safety Mechanism

The system includes multiple safety layers:

1. **High Safe Defaults**: Prevent truncation while catching runaway generation
2. **Warning System**: Alerts when dangerously low limits are detected
3. **Provider Limits**: Respects maximum limits supported by each provider
4. **Fallback Behavior**: Graceful degradation when limits aren't configured

## Troubleshooting

### Common Issues

**Q: My agent responses are being truncated**
A: Check logs for truncation warnings. If using explicit `max_tokens`, increase the value or remove it entirely.

**Q: I'm getting token limit warnings**
A: Remove explicit `max_tokens` parameters from your agent code and let the system use safe defaults.

**Q: My agent needs specific token limits**
A: Use values > 10,000 and document why the specific limit is necessary.

### Recovery Steps

If you encounter issues:

1. **Check Logs**: Look for truncation warnings and token limit messages
2. **Remove Explicit Limits**: Let the system use safe defaults
3. **Test Thoroughly**: Verify full responses are generated correctly
4. **Update Configuration**: Adjust provider defaults if needed

## Future Improvements

Planned enhancements:

1. **Dynamic Adjustment**: Automatically adjust limits based on usage patterns
2. **Per-Model Limits**: More granular control at individual model level
3. **Usage Analytics**: Better visibility into token consumption patterns
4. **Adaptive Thresholds**: Context-aware warning thresholds

## References

- `discernus/gateway/models.yaml` - Provider configuration
- `discernus/gateway/provider_parameter_manager.py` - Core logic
- `scripts/fix_max_tokens.py` - Migration script
- `docs/developer/LLM_MODEL_SELECTION_GUIDE.md` - Model selection guidelines
