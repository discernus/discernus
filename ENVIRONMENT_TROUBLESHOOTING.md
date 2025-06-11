# Environment Troubleshooting Guide

## The Root Issues

After investigation, here are the recurring environment problems and their definitive solutions:

## 🔧 Issue 1: python vs python3 Confusion

### **Problem**
- AI assistants randomly use `python` vs `python3`
- `python` command sometimes doesn't exist
- Leads to "command not found: python" errors

### **Root Cause**
macOS ships with `/usr/bin/python3` but no `/usr/bin/python`. In venv, both exist but `python3` is more reliable.

### **Solution**
```bash
# ✅ ALWAYS use python3
python3 -c "import sys; print(sys.version)"

# ❌ NEVER assume python exists
python -c "import sys; print(sys.version)"  # May fail
```

## 🔧 Issue 2: pip vs pip3 Confusion

### **Problem**
- Sometimes `pip` command not found
- Packages installed in wrong location (system vs venv)

### **Root Cause**
- `pip` only exists when venv is properly activated
- `pip3` exists system-wide but installs to user directory
- Multiple installation locations create confusion

### **Solution**
```bash
# ✅ PREFERRED: Use pip3 explicitly
pip3 install package_name

# ✅ ACCEPTABLE: Use pip only after verifying venv
if [ -n "$VIRTUAL_ENV" ]; then
    pip install package_name
fi
```

## 🔧 Issue 3: Alembic "Not Installed" Despite Being Available

### **Problem**
- `python check_database.py` shows "Alembic not installed"
- But `python3 -c "import alembic"` works
- Intermittent availability

### **Root Cause**
- Alembic installed in multiple locations (system + venv + user)
- Different Python interpreters see different installations
- Virtual environment activation inconsistency

### **Solution**
```bash
# ✅ Always verify with the same Python interpreter
python3 -c "import alembic; print('Available')"

# ✅ Check specific installation location
pip3 show alembic
```

## 🔧 Issue 4: Virtual Environment State Confusion

### **Problem**
- `VIRTUAL_ENV` set but commands still use system Python
- Environment variables persist between sessions
- `(venv)` prompt but wrong executables

### **Root Cause**
- Environment variables can persist without proper PATH setup
- Multiple activation sources create conflicts
- AI assistants don't verify actual executable paths

### **Solution**
```bash
# ✅ Always verify actual executable locations
which python3
which pip3

# ✅ Use our setup script for consistency
source scripts/setup_dev_env.sh
```

## 🚀 Foolproof Patterns

### **Every Development Session**
```bash
# Step 1: Activate virtual environment
source venv/bin/activate

# Step 2: Run setup script (handles everything)
source scripts/setup_dev_env.sh

# Step 3: Verify (script now does this automatically)
# ✅ All checks pass
```

### **AI Assistant Command Patterns**
```bash
# ✅ ALWAYS use these patterns:
python3 -c "import module"              # Not python
pip3 install package                    # Not pip
python3 script.py                       # Not python
python3 -m module.cli                   # Not python

# ✅ Before pip operations:
source scripts/setup_dev_env.sh         # Ensures consistency

# ✅ When checking installations:
python3 -c "import package; print('✅')" # Verify import works
```

## 🔍 Diagnostic Commands

When troubleshooting, use these commands:

```bash
echo "=== ENVIRONMENT DIAGNOSIS ==="
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "Python: $(which python3)"
echo "Pip: $(which pip3)"
echo "Working Directory: $(pwd)"
echo ""
echo "=== CRITICAL IMPORTS ==="
python3 -c "import alembic; print('✅ alembic')" || echo "❌ alembic"
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ narrative_gravity')" || echo "❌ narrative_gravity"
```

## 🎯 Prevention Strategy

1. **Always use the setup script**: `source scripts/setup_dev_env.sh`
2. **Never assume python exists**: Use `python3`
3. **Never assume pip exists**: Use `pip3` or verify venv first
4. **Verify before claiming**: Test imports before saying "installed"
5. **Use consistent patterns**: Follow the command patterns above

## 🔧 Emergency Reset

If environment gets completely confused:
```bash
# Deactivate everything
deactivate 2>/dev/null || true
unset VIRTUAL_ENV
unset PYTHONPATH

# Start fresh
cd /Users/jeffwhatcott/narrative_gravity_analysis
source venv/bin/activate
source scripts/setup_dev_env.sh
```

This guide eliminates the recurring environment debugging cycles that slow development. 