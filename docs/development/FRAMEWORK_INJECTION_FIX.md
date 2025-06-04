# 🎯 Framework Injection & Auto-Detection Fix

## **The Problem You Identified:**
The app couldn't properly detect which framework a JSON analysis was created with because the prompts weren't instructing LLMs to include framework metadata in their responses.

## **Root Cause:**
- **Prompts generated framework-agnostic JSON** → LLM responses lacked framework identification
- **No framework metadata in JSON** → App couldn't auto-detect correct framework  
- **Framework mismatch warnings** → "Unknown well 'Care'" errors when frameworks didn't match

## **Solution Implemented:**

### ✅ **1. Enhanced Prompt Generation**
Updated `generate_prompt.py` to inject framework name into prompts:

```python
class PromptGenerator:
    def __init__(self, config_dir: str = "config", framework_name: str = None):
        self.framework_name = framework_name
        if not framework_name:
            # Auto-detect current framework
            from framework_manager import FrameworkManager
            manager = FrameworkManager()
            self.framework_name = manager.get_active_framework() or "unknown"
```

### ✅ **2. Framework Metadata in JSON Template**
Prompts now instruct LLMs to include framework identification:

```json
{
    "metadata": {
        "framework_name": "moral_foundations",
        "prompt_version": "2025.06.04.18.30",
            "dipoles_version": "2025.06.04",
    "framework_version": "2025.06.04"
    }
}
```

### ✅ **3. Auto-Detection Logic**
Added smart framework detection in `moral_gravity_app.py`:

```python
def detect_framework_from_json(data):
    """Detect which framework a JSON analysis was created with"""
    if 'metadata' in data:
        if 'framework_name' in data['metadata']:
            return data['metadata']['framework_name']
    
    # Fallback: analyze well names to infer framework
    # ...
```

### ✅ **4. Per-Analysis Framework Loading**
Each visualization now uses its original framework:

```python
detected_framework = detect_framework_from_json(data)
analysis_framework_manager = load_framework_for_analysis(detected_framework)
analyzer = NarrativeGravityWellsElliptical(framework_manager=analysis_framework_manager)
```

## **Workflow Now:**

### **🔄 Prompt Generation**
1. **User selects framework** (e.g., `moral_foundations`)
2. **App generates prompt** with `"framework_name": "moral_foundations"` 
3. **LLM receives framework context** in prompt template

### **📥 Analysis Processing**  
1. **LLM returns JSON** with framework metadata included
2. **App detects framework** from `metadata.framework_name`
3. **App loads correct framework** for that specific analysis
4. **Visualization uses original framework** → No well mismatches!

## **Benefits:**

✅ **No more unknown well warnings** - Each analysis uses its original framework  
✅ **True framework-agnostic operation** - Any JSON + any framework combination works  
✅ **Automatic framework detection** - No manual framework selection needed  
✅ **Backward compatibility** - Still works with existing JSON files  
✅ **Future-proof** - New frameworks automatically supported  

## **Key Files Modified:**

- **`generate_prompt.py`**: Framework injection into prompts
- **`moral_gravity_app.py`**: Auto-detection and per-analysis framework loading  
- **Test JSON samples**: Now include `framework_name` metadata

Now each analysis "remembers" which framework it was created with and uses that framework for accurate visualization! 