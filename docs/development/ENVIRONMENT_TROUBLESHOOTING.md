# Environment Troubleshooting Guide

> **For basic setup**: See `.cursorrules` for complete development environment guidance  
> **For IDE setup**: See `DEV_ENVIRONMENT.md` for IDE-specific configuration  
> **This guide**: Troubleshooting when things go wrong

## 🔍 Quick Diagnosis

**When environment issues arise, run this diagnostic:**

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

## 🔧 Common Issues and Root Causes

### **"command not found: python"**
**Root Cause**: macOS has `/usr/bin/python3` but no `/usr/bin/python`  
**Solution**: Always use `python3` (this is enforced in cursor rules)

### **"command not found: pip"**  
**Root Cause**: `pip` only exists when venv is properly activated  
**Solution**: Use `pip3` or verify venv first (patterns in cursor rules)

### **"Alembic not installed" but import works**
**Root Cause**: Multiple installations (system + venv + user), different interpreters  
**Diagnosis**: 
```bash
python3 -c "import alembic; print('Available')"
pip3 show alembic
which python3
```

### **Virtual environment confusion**
**Root Cause**: Environment variables persist without proper PATH setup  
**Symptoms**: `(venv)` prompt but wrong executables  
**Diagnosis**:
```bash
which python3  # Should be in venv/bin/
which pip3     # Should be in venv/bin/
```

### **Import failures after setup**
**Root Cause**: PYTHONPATH not properly configured  
**Solution**: Run setup script again
```bash
source scripts/setup_dev_env.sh
```

## 🚨 Emergency Reset

**When environment gets completely confused:**

```bash
# Nuclear option - start completely fresh
deactivate 2>/dev/null || true
unset VIRTUAL_ENV
unset PYTHONPATH

# Clean restart
cd /Users/jeffwhatcott/narrative_gravity_analysis
source venv/bin/activate
source scripts/setup_dev_env.sh

# Verify everything works
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Ready')"
```

## 🎯 Troubleshooting Patterns

### **AI Assistant Command Failures**
1. **First**: Run `source scripts/setup_dev_env.sh`
2. **Then**: Retry the command
3. **If still failing**: Run diagnostic above
4. **Last resort**: Emergency reset

### **Package Installation Issues**
```bash
# Check what Python we're actually using
which python3
python3 --version

# Check if package actually installed
pip3 show package_name

# Force reinstall if needed
pip3 uninstall package_name
pip3 install package_name
```

### **Database Connection Issues**
```bash
# Check if alembic is available to the right Python
python3 -c "import alembic; print('✅ Available')"

# Check database connection
python3 check_database.py

# If alembic issues persist
pip3 install --force-reinstall alembic
```

---

**Note**: This guide supplements the comprehensive setup guidance in `.cursorrules`. Use this only when standard setup procedures fail. 