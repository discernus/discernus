# 🏗️ Robust Framework Name Architecture

## **The Problem You Identified:**
Framework names were being derived from folder names, creating a brittle system where:
- Renaming folders breaks existing analyses
- No canonical source of truth for framework identity
- File system structure determines logical framework names

## **Root Issue:**
```
frameworks/
├── moral_foundations/     ← Framework name came from HERE (fragile)
│   ├── dipoles.json      ← But should come from HERE (robust)
│   └── framework.json    ← And HERE (robust)
```

## **Solution Implemented:**

### ✅ **1. Explicit Framework Names in Files**
Added `framework_name` field to all configuration files:

**dipoles.json:**
```json
{
  "framework_name": "civic_virtue",
  "version": "2025.06.04",
  "description": "...",
  "dipoles": [...]
}
```

**framework.json:**
```json
{
  "framework_name": "civic_virtue", 
  "version": "2025.06.04",
  "description": "...",
  "wells": {...}
}
```

### ✅ **2. Updated FrameworkManager**
Now reads framework names from files, not directories:

```python
# OLD: Fragile folder-based naming
framework_name = framework_path.name

# NEW: Robust file-based naming  
framework_name = dipoles_data.get('framework_name') or framework_data.get('framework_name') or framework_path.name
```

### ✅ **3. Smart Framework Detection**
`get_active_framework()` now:
1. **First**: Reads framework name from config files
2. **Fallback**: Uses symlink path if name not found in files
3. **Robust**: Handles missing or corrupted files gracefully

### ✅ **4. Name-to-Directory Mapping**
`switch_framework()` now:
1. **Accepts framework names** (e.g., "moral_foundations")
2. **Maps to directories** internally (e.g., "moral_foundations/") 
3. **Allows folder renaming** without breaking functionality

## **Benefits:**

### **🔒 Robust Identity**
- **Framework names are explicit** in configuration files
- **Independent of file system structure** 
- **Renaming folders doesn't break existing analyses**

### **📁 Flexible Organization**
- Folders can be renamed for organization
- Framework names remain stable
- Multiple folders could theoretically have same framework name

### **🔄 Backward Compatibility**
- Falls back to folder names if no explicit name found
- Existing setups continue working
- Gradual migration path

### **🎯 Consistent Workflow**
- LLMs receive canonical framework names in prompts
- JSON responses contain stable framework identification
- Auto-detection works reliably

## **Architecture Now:**

```
frameworks/
├── civic_virtue/                ← Directory name (can change)
│   ├── dipoles.json            ← framework_name: "civic_virtue" (canonical)
│   └── framework.json          ← framework_name: "civic_virtue" (canonical)
└── political_spectrum/          ← Directory name (can change)  
    ├── dipoles.json            ← framework_name: "political_spectrum" (canonical)
    └── framework.json          ← framework_name: "political_spectrum" (canonical)
```

## **Key Changes Made:**

- **`config/dipoles.json`**: Added `framework_name` field
- **`config/framework.json`**: Added `framework_name` field  
- **`framework_manager.py`**: Updated to read names from files
- **`generate_prompt.py`**: Updated to use file-based framework names
- **All framework directories**: Ensured explicit framework names

Now framework identity is **canonical, explicit, and robust**! 🎯 