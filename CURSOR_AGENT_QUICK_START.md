# 🪄 CURSOR AGENT QUICK-START INCANTATION
**Copy-paste this to any new Cursor agent to prevent $0.50 confusion cycles**

## ⚡ 30-SECOND SETUP (DO THIS FIRST!)
```bash
# 1. Verify environment (NEVER skip this!)
make check

# 2. Start infrastructure services (MinIO storage required!)
python3 discernus/cli.py start

# 3. Test a simple experiment directly:
python3 discernus/cli.py run projects/simple_test
```

## 🚨 CRITICAL INFRASTRUCTURE KNOWLEDGE

### **Modern CLI (THIN v2.0) - Use This!**
✅ **New discernus CLI uses direct orchestration and works immediately:**
```bash
# Modern approach - works reliably
python3 discernus/cli.py start                     # Auto-start infrastructure
python3 discernus/cli.py run projects/simple_test  # Direct THIN v2.0 orchestration
python3 discernus/cli.py status                    # Check infrastructure status
python3 discernus/cli.py list                      # Show available experiments
```

### **Legacy CLI (DEPRECATED) - Avoid This!**
❌ **The `discernus_cli_legacy_redis.py` uses deprecated Redis orchestration and will hang:**
```bash
# This will hang in orchestrator queue without workers - DEPRECATED
python3 discernus/cli_legacy_redis.py run projects/simple_test
```

### **Infrastructure Services**
- **MinIO**: Content-addressable storage (localhost:9000) - **REQUIRED**
- **Redis**: Legacy CLI coordination (localhost:6379) - **DEPRECATED**
- **Management**: Use `discernus start` and `discernus stop`

## 🧠 CRITICAL KNOWLEDGE FOR THIS PROJECT

### **Project Type**: THIN Architecture LLM Research Platform
- **LLMs do intelligence**, software does minimal coordination only
- **Direct function calls** (THIN v2.0) replace Redis coordination
- **MinIO storage** for all artifacts and provenance
- **YAML prompts externalized** - never hardcode intelligence in Python
- **No parsing LLM responses** - pass raw text between agents

### **Your Working Environment**
- **Language**: Python 3.13.5
- **Virtual Environment**: `/Volumes/code/discernus/venv/bin/python3` 
- **Project Root**: `/Volumes/code/discernus`
- **ALWAYS use**: `python3` (never `python`)
- **ALWAYS activate venv first**: `source venv/bin/activate && python3`

### **Context Window Limits (KEY INSIGHT!)**
- **Gemini 2.5 Flash**: 1M tokens (~47 presidential speeches max)
- **Gemini 2.5 Pro**: 2M tokens (use for larger batches)
- **Error symptom**: "input token count exceeds maximum" - NOT rate limiting
- **Solution**: Reduce batch size or use Pro model

## 🚫 FORBIDDEN PATTERNS (PREVENTS WASTED TOOL CALLS)

### **NEVER Do This:**
- ❌ Skip `make check` and `discernus start`
- ❌ Use legacy Redis CLI (`discernus/cli_legacy_redis.py`)
- ❌ Try to bypass MinIO - it's required for provenance
- ❌ Assume 429 errors are the bottleneck - context limits are the real issue
- ❌ Build complex parsing code (violates THIN principles)

### **ALWAYS Do This:**
- ✅ Start with `python3 discernus/cli.py start`
- ✅ Use `python3 discernus/cli.py run experiment_path` for testing
- ✅ Check context window limits before assuming rate limiting issues
- ✅ Use modern CLI with direct orchestration
- ✅ Check MinIO console at http://localhost:9001 for artifact storage

## 📋 COMMON DEBUGGING SHORTCUTS

```bash
# Infrastructure status check
python3 discernus/cli.py status                 # Complete infrastructure status
lsof -i :9000                                   # MinIO running?
lsof -i :9001                                   # MinIO console

# Test experiment
python3 discernus/cli.py validate projects/simple_test    # Check experiment structure
python3 discernus/cli.py run projects/simple_test --dry-run  # Preview execution
python3 discernus/cli.py run projects/simple_test         # Execute experiment

# Infrastructure management
python3 discernus/cli.py start                  # Start all services
python3 discernus/cli.py stop                   # Stop all services

# View MinIO artifacts
curl http://localhost:9000/minio/health/live
```

## 🎯 CURRENT MISSION (95% Complete Alpha System)

**Focus**: Testing rate limiting vs context window management
**Next**: Complete 3 validation experiments (CAF, ECF, CHF)
**Architecture**: THIN v2.0 with direct function calls proven effective
