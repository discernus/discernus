# Alpha Release Model Strategy

## Overview

The Discernus Alpha Release uses **Vertex AI Gemini 2.5 Series models exclusively** for reliability, consistency, and complete testing coverage.

## Why Vertex AI Only?

- **Complete Testing**: All components validated with Vertex AI models
- **Reliability**: Structured output support and predictable error handling
- **Cost Efficiency**: Dynamic Shared Quota provides 60-85% cost savings
- **Optimized Model Selection**: Flash Lite with reasoning=1 provides equivalent quality to Pro models at 41.9% cost savings

## Supported Models

- `vertex_ai/gemini-2.5-flash` - High accuracy analysis model
- `vertex_ai/gemini-2.5-flash-lite` - High-throughput tasks with reasoning=1 for complex analysis
- `vertex_ai/gemini-2.5-pro` - Complex analysis and synthesis

### Model Selection Strategy

- **Analysis Phase**: Flash for analytical accuracy
- **Statistical Phase**: Pro for reasoning
- **Evidence Curation**: Pro for reasoning and large context window
- **Synthesis Phase**: Pro model for reasoning quality
- **Validation Phase**: Flash Lite with reasoning=1 for cost optimization
- **Utility Functions**: Flash Lite models for speed

## Performance Expectations

- **Nano experiments** (2-4 documents): 8-12 minutes
- **Micro experiments** (4-8 documents): 12-18 minutes
- **Small experiments** (8-15 documents): 18-25 minutes
- **Medium experiments** (15-30 documents): 25-35 minutes
- **Large experiments** (30+ documents): 35-45 minutes

## Important Notes

### ⚠️ Alpha Limitations

- **Do not use non-Vertex models** - untested combinations may cause failures
- Support limited to Vertex AI models only

### ✅ What Works

- All experiment types with Vertex AI models
- Complete statistical preparation workflow
- Full provenance and audit capabilities
