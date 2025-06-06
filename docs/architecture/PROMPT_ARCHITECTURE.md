# Unified Prompt Template Architecture

## Overview

The Unified Prompt Template Architecture combines the sophistication of the v2.0 prompt generation system with the flexibility needed for production API use. It provides template-based prompt construction, framework-agnostic design, and A/B testing capabilities.

## Architecture Benefits

### **1. Consistency Across Use Cases**
- **Same prompt quality** for manual and API use
- **Unified template system** eliminates hard-coded prompts
- **Version tracking** and metadata embedding across all prompts

### **2. Experimentation Support**
- **A/B testing framework** for prompt optimization
- **Configurable components** for easy tweaking
- **Experimental tracking** with variant management

### **3. Framework Agnostic Design**
- **Universal template system** works with all frameworks
- **Dynamic content generation** from framework configurations
- **Automatic adaptation** to new frameworks

### **4. Production Quality**
- **Reliable JSON extraction** optimized for API use
- **Sophisticated methodology** for human interaction
- **Consistent scoring requirements** across all modes

## System Components

### 1. PromptTemplateManager (`src/prompts/template_manager.py`)

**Core class providing unified prompt generation:**

```python
from src.prompts.template_manager import PromptTemplateManager

# Initialize manager
template_manager = PromptTemplateManager()

# API prompts (optimized for automation)
api_prompt = template_manager.generate_api_prompt(text, "civic_virtue", "gpt-4")

# Interactive prompts (full v2.0 sophistication)
interactive_prompt = template_manager.generate_interactive_prompt("civic_virtue")

# Experimental prompts (A/B testing)
experimental_prompt = template_manager.generate_experimental_prompt(
    text, "civic_virtue", "scoring_methodology", "treatment_a"
)
```

### 2. Prompt Settings (`src/prompts/prompt_settings.json`)

**Configuration file for prompt behavior:**

```json
{
  "enforce_decimal_scale": true,
  "include_model_identification": true,
  "include_analysis_methodology": true,
  "max_language_cues": 3,
  "api_mode_settings": {
    "abbreviated_methodology": true,
    "focus_on_json_reliability": true
  },
  "interactive_mode_settings": {
    "include_workflow_guidance": true,
    "include_comparative_analysis": true
  }
}
```

### 3. Experimental Framework (`src/prompts/templates/experiments/`)

**A/B testing configurations for prompt optimization:**

```json
{
  "control": {
    "description": "Standard scoring methodology",
    "scoring_requirements": "Standard 0.0-1.0 scale instructions"
  },
  "treatment_a": {
    "description": "Enhanced with concrete examples",
    "scoring_requirements": "Detailed thresholds and examples"
  }
}
```

## Usage Patterns

### **Production API Usage**

```python
# In HuggingFaceClient
class HuggingFaceClient:
    def __init__(self):
        self.template_manager = PromptTemplateManager()
    
    def analyze_text(self, text: str, framework: str, model: str):
        # Generate optimized API prompt
        prompt = self.template_manager.generate_api_prompt(text, framework, model)
        
        # Process with LLM...
        return analysis_result
```

**API prompts are optimized for:**
- ✅ **Reliable JSON extraction**
- ✅ **Consistent scoring behavior**
- ✅ **Minimal prompt length** (cost optimization)
- ✅ **Clear instructions** without verbosity

### **Manual Research Usage**

```bash
# Generate interactive prompt for manual LLM use
python generate_prompt.py --framework civic_virtue --mode interactive --output research_prompt.txt
```

**Interactive prompts include:**
- ✅ **Model identification verification**
- ✅ **Workflow guidance** for multi-file analysis
- ✅ **Comprehensive methodology** explanation
- ✅ **Response structure** guidance
- ✅ **Comparative analysis** instructions

### **Experimental Research Usage**

```python
# Test different scoring methodologies
client = HuggingFaceClient()

# Control group
control_result = client.analyze_text(text, "civic_virtue", "gpt-4")

# Treatment group  
treatment_result = client.analyze_text_experimental(
    text, "civic_virtue", "gpt-4", "scoring_methodology", "treatment_a"
)

# Compare results for prompt optimization
```

## Prompt Generation Modes

### 1. **API Mode** - Production Automation
```python
prompt = template_manager.generate_api_prompt(text, framework, model)
```

**Characteristics:**
- Concise and focused
- Optimized for JSON reliability
- Abbreviated methodology section
- No interactive workflow elements

### 2. **Interactive Mode** - Manual Research
```python
prompt = template_manager.generate_interactive_prompt(framework)
```

**Characteristics:**
- Full v2.0 sophistication
- Model identification verification
- Workflow guidance for comparative analysis
- Comprehensive methodology explanation

### 3. **Experimental Mode** - A/B Testing
```python
prompt = template_manager.generate_experimental_prompt(
    text, framework, experiment_id, variant
)
```

**Characteristics:**
- Configurable prompt components
- Variant tracking for analysis
- Hypothesis testing support
- Performance metrics collection

## Framework Integration

### **Automatic Framework Discovery**

The system automatically loads framework configurations:

```
frameworks/
├── civic_virtue/
│   ├── dipoles.json      # Well definitions
│   └── framework.json    # Framework metadata
├── political_spectrum/
│   ├── dipoles.json
│   └── framework.json
└── moral_rhetorical_posture/
    ├── dipoles.json
    └── framework.json
```

### **Template Generation Process**

1. **Load Framework Config** - Dipoles and framework metadata
2. **Build Components** - Header, wells, methodology, format
3. **Apply Mode Settings** - API/Interactive/Experimental variations
4. **Assemble Prompt** - Combine components into final prompt
5. **Version Tracking** - Embed metadata for reproducibility

## Experimentation Framework

### **Creating Experiments**

1. **Define Hypothesis**
```json
{
  "hypothesis": "Explicit scoring examples improve inter-rater reliability",
  "metrics": ["score_variance", "consistency_across_models"]
}
```

2. **Create Variants**
```json
{
  "control": {"scoring_requirements": "Standard instructions"},
  "treatment": {"scoring_requirements": "Enhanced with examples"}
}
```

3. **Run Experiment**
```python
for variant in ["control", "treatment"]:
    result = client.analyze_text_experimental(
        text, framework, model, experiment_id, variant
    )
    collect_metrics(result)
```

### **Available Experiment Types**

#### **Scoring Methodology**
- **Control**: Standard 0.0-1.0 scale instructions
- **Treatment A**: Concrete examples and thresholds
- **Treatment B**: Comparative anchor points
- **Treatment C**: Process-focused step-by-step methodology

#### **Role Definition**
- **Control**: Basic analyst role
- **Treatment A**: Domain expert with credentials
- **Treatment B**: Academic researcher persona
- **Treatment C**: Experienced political analyst

#### **Analysis Methodology**
- **Control**: Standard conceptual approach
- **Treatment A**: Abbreviated for API efficiency
- **Treatment B**: Enhanced with philosophical context
- **Treatment C**: Step-by-step analytical process

## Migration and Backward Compatibility

### **Upgrading from v2.0 System**

1. **Existing Scripts Continue Working**
   - `generate_prompt.py` updated to use new system
   - Old command-line interface preserved
   - Output format maintained

2. **API Integration**
   - `HuggingFaceClient` updated to use template manager
   - Prompt quality improved automatically
   - No breaking changes to public interface

3. **Configuration Migration**
   - Framework configs remain unchanged
   - Settings moved to `prompt_settings.json`
   - Experimental configs added to `templates/experiments/`

### **Current System Benefits Over v2.0**

| **Aspect** | **v2.0 System** | **New Unified System** |
|------------|-----------------|------------------------|
| **Prompt Generation** | Hard-coded in `generate_prompt.py` | Template-based, modular |
| **API Integration** | Basic string building | Sophisticated template manager |
| **Experimentation** | Manual prompt editing | A/B testing framework |
| **Framework Support** | Single framework focus | Universal multi-framework |
| **Consistency** | Manual coordination | Automatic synchronization |
| **Production Use** | Research-oriented only | Both research and production |

## Future Enhancements

### **Planned Features**

1. **Machine Learning Integration**
   - Automatic prompt optimization based on results
   - Performance-driven template selection
   - Adaptive prompt generation

2. **Advanced Experimentation**
   - Multi-variant testing (A/B/C/D)
   - Statistical significance testing
   - Automated experiment management

3. **Template Library**
   - Community-contributed prompt templates
   - Framework-specific optimizations
   - Domain-adapted variations

4. **Performance Analytics**
   - Prompt effectiveness metrics
   - Cost optimization analysis
   - Quality improvement tracking

## Example Usage Scenarios

### **Scenario 1: Academic Research**

```python
# Generate sophisticated interactive prompt for manual analysis
template_manager = PromptTemplateManager()
prompt = template_manager.generate_interactive_prompt("civic_virtue")

# Save for use with ChatGPT/Claude
with open("research_prompt.txt", "w") as f:
    f.write(prompt)
```

### **Scenario 2: Production Analysis**

```python
# Automated analysis of large corpus
client = HuggingFaceClient()
for chunk in corpus_chunks:
    result = client.analyze_text(chunk.content, "civic_virtue", "gpt-4")
    store_results(result)
```

### **Scenario 3: Prompt Optimization**

```python
# A/B test different scoring methodologies
results = {}
for variant in ["control", "treatment_a", "treatment_b"]:
    results[variant] = []
    for text in test_corpus:
        result = client.analyze_text_experimental(
            text, "civic_virtue", "gpt-4", "scoring_methodology", variant
        )
        results[variant].append(result)

# Analyze which prompt variant produces most reliable results
analyze_experiment_results(results)
```

## Summary

The Unified Prompt Template Architecture provides:

✅ **Production Quality** - Reliable, consistent prompts for API use  
✅ **Research Sophistication** - Full v2.0 capabilities for manual analysis  
✅ **Experimentation Support** - A/B testing framework for optimization  
✅ **Framework Agnostic** - Works with all current and future frameworks  
✅ **Easy Configuration** - JSON-based settings for rapid iteration  
✅ **Version Tracking** - Reproducible research with metadata embedding

This system eliminates the gap between sophisticated research prompts and production API prompts, providing a unified foundation for both manual research and automated analysis while supporting continuous improvement through systematic experimentation. 