# LLM Model Selection - Quick Reference
## Fast Decision Guide for Discernus Developers

> **Purpose**: Instant model selection for common scenarios. For detailed analysis, see [LLM Model Selection Guide](./LLM_MODEL_SELECTION_GUIDE.md).

---

## 🚀 Quick Decision Tree

```
GEMINI-FIRST ARCHITECTURE (DSQ Advantage)
├─ Document Analysis → vertex_ai/gemini-2.5-flash (DSQ unlimited)
├─ Academic Synthesis → vertex_ai/gemini-2.5-pro (DSQ unlimited)
├─ High-Volume Tasks → vertex_ai/gemini-2.5-flash-lite (DSQ unlimited)
└─ Quality Validation → anthropic/claude-4-sonnet (fixed quota)

Scale-Based Selection:
├─ < 100 docs → gemini-2.5-pro for everything (cost negligible)
├─ 100-1000 docs → task-specific Gemini models
└─ > 1000 docs → gemini-2.5-flash-lite + spot validation
```

---

## 📊 Model Comparison Matrix

| Model | Cost/1M | Context | Rate Limits | Quality | Best For |
|-------|---------|---------|-------------|---------|----------|
| `gemini-2.5-pro` | $1.25/$10 | 2M | DSQ (unlimited*) | ★★★★★ | Academic synthesis, complex reasoning |
| `gemini-2.5-flash` | $0.30/$2.50 | 1M | DSQ (unlimited*) | ★★★★☆ | Document analysis, extraction |
| `gemini-2.5-flash-lite` | $0.10/$0.40 | 1M | DSQ (unlimited*) | ★★★☆☆ | High-volume batch processing |
| `claude-4-sonnet` | $3.00/$15 | 200K | 1000 RPM, 450k TPM | ★★★★★ | Premium validation, peer review |

*DSQ = Dynamic Shared Quota: No fixed limits but occasional 429 errors during peak demand

---

## 🎯 Agent-Specific Defaults

### Current Production Assignments (Gemini-First)
- **EnhancedAnalysisAgent**: `vertex_ai/gemini-2.5-flash` ✅ (DSQ scaling)
- **IntelligentExtractorAgent**: `vertex_ai/gemini-2.5-flash` ✅ (DSQ scaling)
- **ExperimentCoherenceAgent**: `vertex_ai/gemini-2.5-pro` ✅ (DSQ scaling)
- **CLI Synthesis Default**: `vertex_ai/gemini-2.5-pro` ✅ (DSQ scaling)
- **Validation Tasks**: `vertex_ai/gemini-2.5-flash-lite` ✅ (DSQ scaling)

### Architecture Advantages
- **Cost Leadership**: 60-75% cheaper than Claude/GPT equivalents
- **DSQ Scaling**: No fixed rate limits during normal capacity
- **Context Advantage**: Up to 2M tokens vs 200K for premium models
- **Premium Validation**: Claude 4/GPT-5 available for quality assurance

---

## 💰 Cost Optimization Cheat Sheet

### Scale-Based Selection
```python
def gemini_first_model_select(doc_count: int, task: str) -> str:
    """Gemini-first architecture with DSQ cost advantage."""
    if task == "synthesis":
        return "vertex_ai/gemini-2.5-pro"         # Academic quality
    elif doc_count > 1000:
        return "vertex_ai/gemini-2.5-flash-lite"  # 90% cost reduction  
    else:
        return "vertex_ai/gemini-2.5-flash"       # Standard analysis
```

### DSQ Cost Reality
- **Small Projects** (<100 docs): $1-5 total cost with Gemini models
- **Medium Projects** (100-1000 docs): $10-50 with mixed Gemini approach
- **Large Projects** (1000+ docs): $50-200 with flash-lite + pro synthesis
- **Premium Validation**: Add 10-20% for Claude 4 spot-checking

---

## ⚡ Emergency Fallbacks

### DSQ Capacity Issues?
1. **DSQ 429 Errors**: → Retry with exponential backoff (usually resolves quickly)
2. **Persistent DSQ Issues**: → `anthropic/claude-4-sonnet`
3. **All Vertex AI Down**: → `anthropic/claude-4-sonnet` or `openai/gpt-5`

### DSQ vs Fixed Quota Strategy?
1. **Normal Operations**: Use DSQ models for 90%+ of work
2. **Peak Demand Periods**: Increase premium model usage temporarily
3. **Critical Deadlines**: Switch to fixed-quota models for guaranteed capacity
4. **Cost Optimization**: Return to DSQ when capacity normalizes

---

## 🔧 Implementation Snippets

### Agent Constructor Pattern
```python
def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
    # Task-appropriate default with override capability
    self.model = model
    self.model_registry = ModelRegistry()
    self.llm_gateway = LLMGateway(self.model_registry)
```

### Dynamic Selection
```python
# Scale-based selection
model = ("vertex_ai/gemini-2.5-flash-lite" if doc_count > 1000 
         else "vertex_ai/gemini-2.5-flash")

# Task-based selection  
model = ("vertex_ai/gemini-2.5-pro" if task_type == "synthesis"
         else "vertex_ai/gemini-2.5-flash")
```

### Fallback Chain
```python
models_to_try = [
    primary_model,
    self.model_registry.get_fallback_model(primary_model),
    "vertex_ai/gemini-2.5-flash"  # Universal fallback
]
```

---

## ❌ Common Mistakes to Avoid

1. **Using Pro for Everything**: Wastes money on simple tasks
2. **Using Lite for Synthesis**: Compromises academic quality
3. **No Fallback Strategy**: Single point of failure
4. **Ignoring Context Limits**: Truncated analysis results
5. **Provider Lock-in**: No backup when primary fails

---

## 📚 When to Read the Full Guide

- Adding new models to registry
- Optimizing costs for large-scale experiments  
- Troubleshooting model-specific issues
- Setting up cross-model validation
- Understanding provider-specific limitations

**Full Guide**: [LLM Model Selection Guide](./LLM_MODEL_SELECTION_GUIDE.md)
