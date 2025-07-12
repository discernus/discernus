# THIN Monitoring System for Cursor Agents

A real-time system to prevent Cursor AI agents from writing THICK antipatterns and constrain them to THIN architecture principles.

## 🚀 Quick Setup (5 minutes)

### 1. Install and Test
```bash
python3 scripts/setup_thin_monitoring.py
```

### 2. Start Real-time Monitoring
```bash
python3 scripts/cursor_thin_watcher.py &
```

### 3. Code with THIN Constraints Active
- Cursor will now follow THIN rules
- Warning files appear for THICK patterns
- Linting errors show in editor

## 🎯 What This System Does

### **Constrains Cursor AI Agents**
- **`.cursor/rules`** - System prompt rules Cursor must follow
- **`.cursor/settings.json`** - Stop sequences for THICK patterns
- **Real-time warnings** - Alert when THICK code is written

### **Real-Time THICK Detection**
- **File monitoring** - Watches Python files as you type
- **Warning files** - Creates visible alerts Cursor can see
- **Pattern detection** - Catches regex, parsing, complex logic

### **IDE Integration**
- **VSCode/Cursor linting** - Shows THICK violations as errors
- **Custom pylint plugin** - Detects antipatterns in real-time
- **Editor highlighting** - Visual feedback for violations

## 🚨 THICK Patterns It Catches

### **Forbidden Imports**
```python
import re          # ❌ Use LLM for parsing
import bs4         # ❌ Use LLM for extraction
import xml.etree   # ❌ Use LLM for processing
```

### **Forbidden Function Names**
```python
def parse_content()    # ❌ Use llm_client.call_llm()
def extract_data()     # ❌ Use llm_client.call_llm()
def validate_input()   # ❌ Use llm_client.call_llm()
```

### **Forbidden Patterns**
```python
# ❌ Complex logic - use LLM instead
if condition1:
    if condition2:
        if condition3:
            if condition4:
                return result

# ❌ String manipulation - use LLM instead
text.split(',').replace(' ', '').strip()

# ❌ Regex patterns - use LLM instead
re.search(r'pattern', text)
```

## ✅ THIN Patterns It Enforces

### **Simple Orchestration**
```python
def load_framework(path):
    content = Path(path).read_text()
    validation = llm_client.call_llm(f"Validate framework: {content}")
    return {'content': content, 'validation': validation}
```

### **LLM Content Processing**
```python
def process_content(content):
    result = llm_client.call_llm(f"Process this content: {content}")
    return result
```

### **Basic File Operations**
```python
def store_result(session_id, result):
    result_file = Path(f"results/{session_id}.json")
    result_file.write_text(json.dumps(result))
```

## 📊 System Components

### **1. Cursor Constraints**
- **`.cursor/rules`** - THIN architecture rules
- **`.cursor/settings.json`** - Stop sequences and constraints

### **2. Real-Time Monitoring**
- **`cursor_thin_watcher.py`** - File system watcher
- **Warning files** - `.THICK_WARNING_*` alerts

### **3. Editor Integration**
- **`thin_pylint_plugin.py`** - Custom linting rules
- **`.vscode/settings.json`** - IDE configuration

## 🔧 Manual Commands

### **Start Monitoring**
```bash
python3 scripts/cursor_thin_watcher.py
```

### **Test Linting**
```bash
pylint --load-plugins=scripts.thin_pylint_plugin your_file.py
```

### **Check Setup**
```bash
python3 scripts/setup_thin_monitoring.py
```

## 🎯 Success Indicators

### **Cursor Behavior Changes**
- ✅ Suggests `llm_client.call_llm()` instead of parsing
- ✅ Avoids regex imports and string manipulation
- ✅ Keeps functions under 50 lines
- ✅ Uses simple orchestration patterns

### **Real-Time Feedback**
- ✅ Warning files appear when writing THICK code
- ✅ Linting errors show violations immediately
- ✅ File monitoring catches patterns as you type

### **Development Flow**
- ✅ Less refactoring from THICK to THIN
- ✅ Faster development with fewer wrong turns
- ✅ Consistent THIN architecture across team

## 🚨 Troubleshooting

### **Linting Not Working**
```bash
# Check plugin path
export PYTHONPATH="${PYTHONPATH}:./scripts"
pylint --load-plugins=scripts.thin_pylint_plugin test_file.py
```

### **Cursor Not Following Rules**
```bash
# Verify rules file
cat .cursor/rules
cat .cursor/settings.json
```

### **Monitoring Not Starting**
```bash
# Install dependencies
pip install watchdog pylint

# Test monitoring
python3 scripts/cursor_thin_watcher.py
```

## 💡 Usage Tips

### **For Cursor Users**
- Cursor will read `.cursor/rules` automatically
- Stop sequences prevent THICK pattern generation
- System prompts constrain AI behavior

### **For VSCode Users**
- Linting shows THICK violations as errors
- Warning files appear in file explorer
- Real-time feedback during coding

### **For Development Teams**
- Enforces THIN discipline across all developers
- Prevents THICK code from entering codebase
- Reduces architecture drift over time

## 🎉 The THIN Advantage

**Before THIN Monitoring:**
- Cursor writes complex parsing logic
- THICK patterns creep into codebase
- Refactoring required after code review

**After THIN Monitoring:**
- Cursor suggests LLM calls instead
- THIN patterns enforced automatically
- Architecture stays consistent

**Result:** Faster development, fewer bugs, cleaner architecture. 