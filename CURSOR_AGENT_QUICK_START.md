# 🪄 CURSOR AGENT QUICK-START INCANTATION
**Copy-paste this to any new Cursor agent to prevent $0.50 confusion cycles**

## ⚡ 30-SECOND SETUP (DO THIS FIRST!)
```bash
# 1. Verify environment (NEVER skip this!)
make check

# 2. If anything fails, fix it:
source venv/bin/activate && pip install -r requirements.txt

# 3. Test the CLI works:
discernus --help
```

## 🧠 CRITICAL KNOWLEDGE FOR THIS PROJECT

### **Project Type**: THIN Architecture LLM Research Platform
- **LLMs do intelligence**, software does minimal coordination only
- **Redis streams + MinIO** for all coordination and storage  
- **YAML prompts externalized** - never hardcode intelligence in Python
- **No parsing LLM responses** - pass raw text between agents

### **Your Working Environment**
- **Language**: Python 3.13.5
- **Virtual Environment**: `/Volumes/code/discernus/venv/bin/python3` 
- **Project Root**: `/Volumes/code/discernus`
- **ALWAYS use**: `python3` (never `python`)
- **ALWAYS activate venv first**: `source venv/bin/activate && python3`

### **Architecture Status**: ✅ 95% Complete for Alpha System
- **CLI**: Working (`discernus run`, `validate`, `list`, `status`)
- **Agents**: 6 modern agents with YAML prompts  
- **Infrastructure**: Redis + MinIO + orchestration ready
- **Next**: Implement 3 test experiments + minor completion items

## 🚫 FORBIDDEN PATTERNS (Will waste time/money)
```bash
# NEVER do these:
python (use python3)
pip install (without venv activated)
gh issue view 123 (without | cat - will hang)
git commit -m "Long detailed message..." (will hang)
Recreating venv (just install missing packages)
```

## ✅ REQUIRED PATTERNS (Will save time/money)
```bash
# ALWAYS do these:
source venv/bin/activate && python3 script.py
make check  # Before any work
gh issue view 123 | cat  # Safe GitHub CLI
git commit -m "Brief message"  # Short commits
```

## 📚 KEY FILES TO READ
1. **`.cursor/rules`** - 114 lines of strict behavioral rules
2. **`docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`** - THIN principles


## 🔧 USEFUL COMMANDS
```bash
# Environment & Testing
make check                    # Verify environment
make test                     # Run test suite

# Development
python3 scripts/prompt_engineering_harness.py --list-models
python3 scripts/check_environment.py
git status --porcelain       # Quick git check
```

## 🆘 IF STUCK
1. **Environment issues**: Run `make check` and follow instructions
2. **Import errors**: `source venv/bin/activate && pip install missing_package`
3. **Redis/Infrastructure**: `python3 scripts/background_executor.py`
4. **Architecture questions**: Read `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
