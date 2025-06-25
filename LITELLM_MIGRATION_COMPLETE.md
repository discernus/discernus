# LiteLLM Migration Guide

## ✅ Migration Complete!

You've successfully migrated from DirectAPIClient to LiteLLMClient with unified cloud + local model support.

## 🔄 What Changed

### **NEW: Unified Model Interface**
```python
# Cloud APIs (same as before)
client.analyze_text(text, framework, "gpt-4o")
client.analyze_text(text, framework, "claude-3-5-sonnet-20241022")

# LOCAL Ollama models (NEW!)
client.analyze_text(text, framework, "ollama/llama3.2")
client.analyze_text(text, framework, "ollama/mistral")
```

### **Preserved Features**
- ✅ **Same Interface**: `analyze_text(text, framework, model_name)` unchanged
- ✅ **TPM Rate Limiting**: All existing rate limiting preserved
- ✅ **Cost Management**: Cost tracking and limits preserved  
- ✅ **Quality Assurance**: Full QA validation preserved
- ✅ **Retry Logic**: Error handling and retries preserved

### **Enhanced Features**
- 🚀 **Local Models**: Run Llama, Mistral locally via Ollama
- 🔄 **Model Switching**: Switch between cloud/local with same interface
- ⚡ **Performance**: Optimized rate limiting for local models (0.5s vs 2s)
- 📊 **Model Discovery**: Dynamic detection of available Ollama models

## 🎯 Usage Examples

### **Research with Local Models (Privacy + Cost Savings)**
```python
# Analyze sensitive data locally
result, cost = client.analyze_text(
    text="Internal company policy document...",
    framework="civic_virtue",
    model_name="ollama/llama3.2"  # Runs locally, $0 cost
)
```

### **Production with Cloud Models (Quality + Speed)**  
```python
# Production analysis with cloud models
result, cost = client.analyze_text(
    text="Public research corpus...",
    framework="moral_foundations_theory", 
    model_name="gpt-4o"  # Cloud model for best quality
)
```

### **Hybrid Workflows (Best of Both)**
```python
# Prototype locally, validate with cloud
models_to_test = ["ollama/llama3.2", "ollama/mistral", "gpt-4o"]
for model in models_to_test:
    result, cost = client.analyze_text(text, framework, model)
    print(f"{model}: {result.get('analysis_quality', 0):.2f}")
```

## 🛠️ Available Models

### **Cloud APIs**
- **OpenAI**: gpt-4o, gpt-4o-mini, gpt-3.5-turbo, o1-preview
- **Anthropic**: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022
- **Mistral**: mistral-large-latest, mistral-small-latest
- **Google**: gemini-2.5-flash, gemini-1.5-pro

### **Local Ollama Models**  
- **ollama/llama3.2**: 3.2B params, fast local inference
- **ollama/mistral**: 7.2B params, quality local analysis
- Install more: `ollama pull llama3.3` → `ollama/llama3.3`

## 🔧 Migration Validation

Run the validation suite:
```bash
python3 scripts/applications/test_litellm_migration.py
```

## 📈 Performance Benefits

| Metric | Before | After |
|--------|--------|-------|
| Model Options | 15 cloud | 15 cloud + unlimited local |
| Cost for Local | N/A | $0.00 |
| Privacy | Cloud only | Local + cloud options |
| Rate Limiting | Fixed | Optimized per provider |
| Development Speed | Cloud delays | Instant local testing |

## 🚀 Next Steps

1. **Update Experiments**: Modify experiment configs to test local models
2. **Cost Optimization**: Use local models for development, cloud for production
3. **Privacy Workflows**: Route sensitive data to local models automatically
4. **Model Comparison**: Compare local vs cloud model performance

## 🔄 Rollback (If Needed)

To rollback to DirectAPIClient:
```bash
# Restore backup (check src/api_clients/ for .backup_ files)
cp src/api_clients/direct_api_client.py.backup_* src/api_clients/direct_api_client.py

# Update imports in your code back to DirectAPIClient
```

## 🎉 Success!

Your Discernus system now has unified cloud + local LLM capabilities while preserving all existing functionality!
