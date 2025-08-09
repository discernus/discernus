# LLM Model Selection - Quick Reference
## Fast Decision Guide for Discernus Developers

> **Purpose**: Instant model selection for common scenarios. For detailed analysis, see [LLM Model Selection Guide](./LLM_MODEL_SELECTION_GUIDE.md).

---

## 🚀 Quick Decision Tree

```
Document Count?
├─ < 100 docs → Use vertex_ai/gemini-2.5-pro (quality priority)
├─ 100-1000 docs → Task-specific selection ↓
└─ > 1000 docs → Use vertex_ai/gemini-2.5-flash-lite (cost priority)

Task Type?
├─ Analysis/Extraction → vertex_ai/gemini-2.5-flash
├─ Synthesis/Reports → vertex_ai/gemini-2.5-pro  
├─ Validation/Coherence → vertex_ai/gemini-2.5-pro
├─ High-Volume Batch → vertex_ai/gemini-2.5-flash-lite
└─ Cross-Model Check → anthropic/claude-3-5-sonnet-20240620
```

---

## 📊 Model Comparison Matrix

| Model | Cost/1M | Context | Speed | Quality | Best For |
|-------|---------|---------|-------|---------|----------|
| `gemini-2.5-pro` | $1.25/$10 | 2M | Medium | ★★★★★ | Synthesis, Complex Reasoning |
| `gemini-2.5-flash` | $0.30/$2.50 | 1M | Fast | ★★★★☆ | Analysis, Standard Tasks |
| `gemini-2.5-flash-lite` | $0.10/$0.40 | 1M | Fastest | ★★★☆☆ | Batch, Validation |
| `claude-3-5-sonnet` | $3.00/$15 | 200K | Slow | ★★★★★ | Quality Validation |

---

## 🎯 Agent-Specific Defaults

### Current Production Assignments
- **EnhancedAnalysisAgent**: `vertex_ai/gemini-2.5-flash` ✅
- **IntelligentExtractorAgent**: `vertex_ai/gemini-2.5-flash` ✅  
- **ExperimentCoherenceAgent**: `vertex_ai/gemini-2.5-pro` ✅
- **EvidenceQualityMeasurementAgent**: `vertex_ai/gemini-2.5-flash` ✅

### Recommended Upgrades
- **Large Batch Analysis** (>1000 docs): Switch to `gemini-2.5-flash-lite`
- **Academic Validation**: Add `claude-3-5-sonnet` fallback
- **Cost-Sensitive Projects**: Use `gemini-2.5-flash-lite` for non-critical tasks

---

## 💰 Cost Optimization Cheat Sheet

### Scale-Based Selection
```python
def quick_model_select(doc_count: int, task: str) -> str:
    if doc_count > 1000:
        return "vertex_ai/gemini-2.5-flash-lite"  # 75% cost reduction
    elif task == "synthesis":
        return "vertex_ai/gemini-2.5-pro"         # Quality priority  
    else:
        return "vertex_ai/gemini-2.5-flash"       # Balanced default
```

### Budget Guidelines
- **< $10 budget**: Use `gemini-2.5-flash-lite` for everything
- **$10-50 budget**: Mixed approach (lite for analysis, pro for synthesis)
- **> $50 budget**: Quality-first (pro for critical tasks, flash for routine)

---

## ⚡ Emergency Fallbacks

### Primary Model Down?
1. **Vertex AI Issues**: → `anthropic/claude-3-5-sonnet-20240620`
2. **Anthropic Issues**: → `openai/gpt-4o` 
3. **All Premium Down**: → `vertex_ai/gemini-2.5-flash-lite`

### Rate Limited?
1. **Switch Provider**: Vertex AI → Anthropic → OpenAI
2. **Downgrade Tier**: Pro → Flash → Flash-Lite
3. **Batch Delay**: Queue for retry with exponential backoff

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
