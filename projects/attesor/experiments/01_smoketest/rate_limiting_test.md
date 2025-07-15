# Experiment: Rate Limiting Test
## Validate Rate Limiting Management Before Full Study

**Date**: January 15, 2025  
**Framework**: PDAF v1.1 (Sanitized)  
**Analysis Type**: Rate limiting validation  
**Expected Duration**: 10-15 minutes  
**Purpose**: Test rate limiting and request spacing for larger studies

---

## Objective

Test that the orchestrator can:
1. Handle multiple requests without hitting rate limits
2. Implement appropriate delays between requests
3. Manage concurrent model execution efficiently
4. Scale to handle full study volumes

---

## Methodology

**Rate Limiting Test Design**:
- **Corpus**: 2 speeches (Romney, McCain - both sanitized)
- **Models**: 2 models (Claude + Gemini)
- **Runs**: 3 runs per model (6 total analyses per text = 12 total analyses)
- **Rate Management**: Test delays and request spacing

**Target Metrics**:
- **Request Rate**: Stay under 50 RPM for Anthropic API
- **Token Usage**: Monitor TPM usage
- **Success Rate**: All 12 analyses should complete successfully
- **Duration**: Complete in under 15 minutes

---

## Rate Limiting Configuration

Test higher volume execution with proper delays:

```yaml
models:
  - anthropic/claude-3-5-sonnet-20240620
  - vertex_ai/gemini-2.5-flash
num_runs: 3
remove_synthesis: true
batch_size: 1
delay_between_requests: 2
```

---

## Expected Outputs

**Validation Targets**:
1. **Request Spacing**: Proper delays between API calls
2. **Rate Limit Compliance**: No 429 rate limit errors
3. **Statistical Analysis**: 12 observations (2 texts × 2 models × 3 runs)
4. **Inter-Run Reliability**: Cronbach's alpha calculation with multiple runs

This test validates the system can handle larger analysis volumes with proper rate limiting.

---

## Success Criteria

- **✅ All 12 analyses complete successfully**
- **✅ No rate limit errors (429 responses)**
- **✅ Proper request spacing (2 second delays)**
- **✅ Statistical analysis with 12 observations**
- **✅ Inter-run reliability calculation**

**Failure Modes to Watch For**:
- Rate limit errors (429 responses)
- Request timing issues
- Statistical analysis failures
- Orchestrator timeout errors

This test prepares the system for the full 864-analysis Attesor study. 