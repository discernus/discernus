# Model Selection Defaults

This document defines the default model selection strategy for the Discernus V2 agent ecosystem, optimized for cost, reliability, and performance.

## Overview

The V2 architecture uses different Gemini models for different tasks based on:
- **Frequency**: How often the task is called per experiment
- **Reliability requirements**: Whether the task must succeed for pipeline integrity
- **Cost sensitivity**: Impact on total experiment cost
- **Tool calling requirements**: Whether the task requires reliable tool calling

## Model Selection Matrix

| Task | Model | Frequency | Rationale |
|------|-------|-----------|-----------|
| **Content Generation** | | | |
| Composite Analysis | `vertex_ai/gemini-2.5-flash` | Per document | High frequency, standard content generation |
| Evidence Extraction | `vertex_ai/gemini-2.5-flash-lite` | Per document | High frequency, simple extraction task |
| Score Extraction | `vertex_ai/gemini-2.5-flash-lite` | Per document | High frequency, simple extraction task |
| Derived Metrics | `vertex_ai/gemini-2.5-flash` | Per document | High frequency, code generation |
| Markup Extraction | `vertex_ai/gemini-2.5-flash-lite` | Per document | High frequency, simple extraction task |
| Statistical Analysis | `vertex_ai/gemini-2.5-pro` | Once per experiment | Complex analysis, low frequency |
| Evidence Curation Planning | `vertex_ai/gemini-2.5-pro` | Once per experiment | Strategic planning, tool calling |
| Evidence Curation Execution | `vertex_ai/gemini-2.5-flash` | Per iteration | High frequency, content generation |
| Synthesis Stage 1 | `vertex_ai/gemini-2.5-pro` | Once per experiment | Complex analysis, research intelligence |
| Synthesis Stage 2 | `vertex_ai/gemini-2.5-flash` | Once per experiment | Evidence integration, content generation |
| **Verification Tasks** | | | |
| Derived Metrics Verification | `vertex_ai/gemini-2.5-flash` | Per document | High frequency, tool calling works reliably |
| Statistical Verification | `vertex_ai/gemini-2.5-pro` | Once per experiment | Low frequency, requires reliable tool calling |

## Cost Optimization Strategy

### High-Frequency Tasks (Per Document)
- **Use Flash/Flash Lite**: Significant cost savings across many documents
- **Examples**: Derived metrics verification (4+ calls), evidence extraction (4+ calls)
- **Cost Impact**: Large experiments with 20+ documents see substantial savings

### Low-Frequency Tasks (Per Experiment)
- **Use Pro when reliability critical**: Statistical verification, strategic planning
- **Use Flash when appropriate**: Synthesis Stage 2, evidence integration
- **Cost Impact**: Minimal since called only once per experiment

## Tool Calling Reliability

### Flash Models
- **Reliability**: Moderate for tool calling
- **Use Cases**: High-frequency verification where cost matters
- **Limitations**: May fail under load or with complex prompts

### Pro Models
- **Reliability**: High for tool calling
- **Use Cases**: Critical verification tasks, strategic planning
- **Advantage**: Consistent tool calling performance

## Implementation Details

### Agent-Specific Defaults

#### V2AnalysisAgent
```python
# Content generation
composite_analysis_model = "vertex_ai/gemini-2.5-flash"
evidence_extraction_model = "vertex_ai/gemini-2.5-flash-lite"
score_extraction_model = "vertex_ai/gemini-2.5-flash-lite"
derived_metrics_model = "vertex_ai/gemini-2.5-flash"
markup_extraction_model = "vertex_ai/gemini-2.5-flash-lite"

# Verification (high frequency)
verification_model = "vertex_ai/gemini-2.5-flash"
```

#### V2StatisticalAgent
```python
# Content generation
statistical_analysis_model = "vertex_ai/gemini-2.5-pro"

# Verification (low frequency)
verification_model = "vertex_ai/gemini-2.5-pro"
```

#### IntelligentEvidenceRetrievalAgent
```python
# Strategic planning
planning_model = "vertex_ai/gemini-2.5-pro"

# Execution (high frequency)
execution_model = "vertex_ai/gemini-2.5-flash"
```

#### TwoStageSynthesisAgent
```python
# Stage 1: Complex analysis
stage1_model = "vertex_ai/gemini-2.5-pro"

# Stage 2: Evidence integration
stage2_model = "vertex_ai/gemini-2.5-flash"
```

## Fallback Strategy

All agents implement a fallback cascade:
1. **Primary model** (as defined above)
2. **Secondary model** (typically Flash if Pro fails)
3. **Tertiary model** (typically Flash Lite as last resort)

## Cost Analysis

### Micro Experiment (4 documents)
- **Derived Metrics Verification**: 4 × Flash = ~$0.04
- **Statistical Verification**: 1 × Pro = ~$0.02
- **Total Verification Cost**: ~$0.06

### Large Experiment (20 documents)
- **Derived Metrics Verification**: 20 × Flash = ~$0.20
- **Statistical Verification**: 1 × Pro = ~$0.02
- **Total Verification Cost**: ~$0.22

**Cost Savings**: Using Flash for high-frequency verification saves ~80% compared to using Pro for all verification tasks.

## Configuration

Model selection can be overridden via agent configuration:

```python
# Override specific model
agent_config = {
    "verification_model": "vertex_ai/gemini-2.5-pro",  # Force Pro for verification
    "content_model": "vertex_ai/gemini-2.5-flash"      # Force Flash for content
}
```

## Future Considerations

### Model Registry Integration
- Move hardcoded model names to centralized registry
- Enable dynamic model selection based on experiment characteristics
- Support for model-specific configuration per task type

### Performance Monitoring
- Track model-specific success rates
- Monitor cost per experiment
- Adjust defaults based on empirical data

### Experimental Models
- New models should be explicitly selected at CLI level
- Never include experimental models in fallback cascades
- Maintain clear separation between production and experimental model usage

## Related Documentation

- [Agent Architecture](AGENT_ARCHITECTURE.md)
- [Cost Optimization](COST_OPTIMIZATION.md)
- [Tool Calling Patterns](TOOL_CALLING_PATTERNS.md)
- [V2 Orchestrator Configuration](V2_ORCHESTRATOR.md)
