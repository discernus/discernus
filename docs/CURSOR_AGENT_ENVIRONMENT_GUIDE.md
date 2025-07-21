# Cursor Agent Environment Guide

## 🚨 CRITICAL: Environment First!

**Before doing ANYTHING, run:**
```bash
make check
```

If that fails, run:
```bash  
make install
```

## ✅ Required Commands Pattern

**ALWAYS use this pattern:**
```bash
source venv/bin/activate && python3 your_script.py
```

**Or use Make commands (safer):**
```bash
make test           # Run tests
make harness-list   # List models for testing
make deps          # Install dependencies
```

## 🚫 NEVER Do These Things

❌ `python` (always `python3`)  
❌ `pip install package` (without venv)  
❌ Recreate venv unless asked  
❌ System python for project code  

## 🔧 Quick Fixes

**Environment broken?**
```bash
make install && make check
```

**Missing packages?**
```bash  
source venv/bin/activate && pip install -r requirements.txt
```

**Not sure what's wrong?**
```bash
python3 scripts/check_environment.py
```

## 💡 Smart Patterns

**Test a model quickly:**
```bash
make harness-simple MODEL="vertex_ai/gemini-2.5-flash" PROMPT="What is 2+2?"
```

**Run tests before coding:**
```bash
make test
```

**Check environment before everything:**
```bash
make check
```

---

**Remember: These rules save Cursor usage and prevent velocity kills!** 