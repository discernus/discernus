# LLM API Parameter Cleanup Implementation Handoff

## Context: Critical API Parameter Sensitivity Issue

**Issue Discovered**: LLMs are extremely sensitive to API request parameters. The Vertex AI safety filter issue was caused by `max_tokens=2000` parameter triggering stricter content filtering, not actual content policy violations.

**Key Lesson**: Web interfaces work reliably because they use minimal, clean parameters. API calls should follow the same pattern.

## Approved Implementation Plan

### Phase 1: Centralized Provider Parameter Manager (Current Task)

**User Requirements**:
1. **Fail Fast Approach**: Remove fallback logic - prefer failures over meaningless analysis
2. **Parameter Management First**: Focus on clean parameter handling before prompt generation
3. **Provider Coverage**: OpenAI, Anthropic, Vertex AI, Ollama (with model-specific tweaks), Mistral, prepare for Perplexity
4. **Separate File**: Create dedicated module, keep it clear and discoverable
5. **No LiteLLM Forking**: Don't modify litellm itself

### Implementation Architecture

```python
# File: discernus/gateway/provider_parameter_manager.py
class ProviderParameterManager:
    """Centralized handling of provider-specific parameter sensitivities"""
    
    def get_clean_parameters(self, provider: str, base_params: dict) -> dict:
        """Clean parameters based on provider sensitivities"""
        
    def get_provider_from_model(self, model_name: str) -> str:
        """Extract provider from model name"""
        
    def get_provider_specific_config(self, provider: str) -> dict:
        """Get provider-specific configuration"""
```

### Current Code Issues to Fix

**Location**: `discernus/gateway/litellm_client.py`

**Issues Found**:
1. **Parameter Bloat**: Sends temperature, timeout, max_tokens to all models
2. **Scattered Logic**: Vertex AI logic duplicated in multiple methods
3. **Complex Fallback**: Multiple conflicting strategies for handling issues

**Specific Code Sections to Replace**:
- `_litellm_call_with_retry()` lines 500-550
- `_litellm_call_basic()` lines 526-570  
- `_get_safety_settings_for_vertex_ai()` method
- Parameter building logic in both completion methods

### Provider-Specific Requirements

**Vertex AI (Critical)**:
- Remove `max_tokens` parameter (causes safety filter issues)
- Add safety_settings for academic research
- Minimal other parameters

**OpenAI**:
- Minimal parameters (maybe just temperature if needed)
- Standard completion format

**Anthropic**:
- Clean parameters
- Handle rate limiting appropriately

**Ollama**:
- Local model optimization
- Per-model tweaks (especially Mistral dropout issues)
- Longer timeouts for local processing

**Mistral**:
- Include API key configuration
- Handle provider-specific parameters

**Perplexity (Future)**:
- Prepare configuration structure

### Current State

**Files Modified**: 
- `pm/soar/soar_v2/SOAR v2.0 Developer Briefing.md` - Added API best practices section
- `pm/soar/soar_v2/Simple Atomic Orchestrated Research (SOAR) v2.0.md` - Added conversational design section

**Last Commit**: "Update SOAR v2.0 specification with LLM API best practices and conversational design insights"

**Memory Created**: ID 3044313 - LLM API Parameter Sensitivity and Conversational Design Best Practices

## Next Steps for Implementation

### 1. Create Provider Parameter Manager
```python
# File: discernus/gateway/provider_parameter_manager.py
class ProviderParameterManager:
    """THIN-compliant provider parameter management"""
    
    PROVIDER_CONFIGS = {
        'vertex_ai': {
            'forbidden_params': ['max_tokens'],
            'required_params': {
                'safety_settings': [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            },
            'default_params': {}
        },
        'openai': {
            'forbidden_params': [],
            'required_params': {},
            'default_params': {}
        },
        'anthropic': {
            'forbidden_params': [],
            'required_params': {},
            'default_params': {}
        },
        'ollama': {
            'forbidden_params': [],
            'required_params': {},
            'default_params': {'timeout': 300}  # Longer timeout for local
        },
        'mistral': {
            'forbidden_params': [],
            'required_params': {},
            'default_params': {}
        }
    }
```

### 2. Update LiteLLM Client
- Replace scattered parameter logic with manager calls
- Simplify completion methods
- Remove fallback logic (fail fast instead)
- Add comprehensive logging for failures

### 3. Test with Current Failing Cases
- Vertex AI political content (AOC, Bernie Sanders speeches)
- Mistral API connectivity
- Parameter sensitivity across providers

### 4. Integration Points
- Update `discernus/gateway/litellm_client.py` to use the manager
- Ensure existing orchestration code continues to work
- Test with `projects/soar_2_cff_poc/` project

## Success Criteria

1. **Vertex AI Issue Fixed**: Political content analysis works without parameter issues
2. **Clean Parameter Handling**: Each provider gets only appropriate parameters
3. **Fail Fast Behavior**: Clear, logged failures instead of confusing fallbacks
4. **Mistral Integration**: API key configuration and working calls
5. **Extensible Design**: Easy to add Perplexity and other providers

## Related Documentation

- **SOAR v2.0 Developer Briefing**: `pm/soar/soar_v2/SOAR v2.0 Developer Briefing.md#llm-api-best-practices`
- **Main SOAR Specification**: `pm/soar/soar_v2/Simple Atomic Orchestrated Research (SOAR) v2.0.md#llm-api-best-practices-and-conversational-design`
- **Memory**: ID 3044313 contains key insights about parameter sensitivity

## Code Quality Requirements

- **THIN Compliance**: Minimal code, maximum AI intelligence utilization
- **Self-Documenting**: Clear variable names, comprehensive docstrings
- **Error Handling**: Detailed logging for debugging parameter issues
- **Extensible**: Easy to add new providers and parameter configurations

The next agent should focus on implementing the ProviderParameterManager first, then integrating it into the existing LiteLLM client while removing the complex fallback logic. 