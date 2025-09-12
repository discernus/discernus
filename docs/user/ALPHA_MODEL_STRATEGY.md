# Alpha Release Model Strategy

## Overview

The Discernus Alpha Release uses **Vertex AI models exclusively** to ensure reliability, consistency, and complete end-to-end testing.

## Why Vertex AI Only?

### 1. **Complete Testing Coverage**
- All system components tested with Vertex AI models
- End-to-end workflows validated with consistent model behavior
- Known performance characteristics and timeout patterns

### 2. **Reliability & Consistency**
- Structured output support for utility agents
- Predictable error handling and fallback behavior
- Consistent response formats across all agents

### 3. **Cost Efficiency**
- Dynamic Shared Quota (DSQ) provides 60-85% cost savings
- Optimized timeout and retry strategies
- No premium model costs for utility operations

## Supported Models

### **Analysis Models**
- `vertex_ai/gemini-2.5-flash` - Primary analysis model (cost-effective)
- `vertex_ai/gemini-2.5-flash-lite` - High-throughput tasks
- `vertex_ai/gemini-2.5-pro` - Complex analysis and synthesis

### **Model Selection Strategy**
- **Analysis Phase**: Flash models for efficiency
- **Synthesis Phase**: Pro model for quality
- **Validation**: Flash models for speed
- **Derived Metrics**: Flash models for calculations

## Future Model Support

### **Post-Alpha Roadmap**
- **Beta Release**: Consider Claude and OpenAI models for synthesis
- **Stable Release**: Full multi-provider support
- **Research Edition**: Specialized models for specific domains

### **Model Addition Criteria**
- Complete end-to-end testing with all system components
- Performance validation across all experiment types
- Cost-benefit analysis for research workflows
- User feedback and demand assessment

## Important Notes

### **⚠️ Alpha Limitations**
- **Do not use non-Vertex models** in alpha release
- Untested model combinations may cause failures
- Support limited to Vertex AI models only

### **✅ What Works**
- All experiment types with Vertex AI models
- Complete statistical preparation workflow
- Full provenance and audit capabilities
- CSV export and data analysis features

## Getting Started

### **Recommended Model Configuration**
```yaml
# In your experiment.md
metadata:
  analysis_model: "vertex_ai/gemini-2.5-flash"
  synthesis_model: "vertex_ai/gemini-2.5-pro"
```

### **Performance Expectations**
- **Nano experiments** (< 1 minute)
- **Micro experiments** (< 3 minutes)  
- **Small experiments** (< 8 minutes)
- **Medium experiments** (< 15 minutes)
- **Large experiments** (< 45 minutes)

## Support & Feedback

### **Alpha Support**
- Report issues with Vertex AI models only
- Performance feedback for model optimization
- Feature requests for future model support

### **Future Model Requests**
- Submit requests for specific models
- Provide use cases and requirements
- Participate in beta testing programs

---

## Document Metadata

- **Version**: 1.0
- **Date**: 2025-09-12
- **Status**: Alpha Release Strategy
- **Next Review**: Post-Alpha Release
