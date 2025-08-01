# Cursor Agent Quick Start Guide

**30-Second Orientation for New Cursor Agents**

## 🚀 Environment Verification (Run First!)

```bash
# 1. Check environment setup
make check

# 2. Verify CLI works
python3 -m discernus.cli list

# 3. Run simple test
make run EXPERIMENT=projects/simple_test
```

## 📊 Project Status: 95% Complete Alpha System

- **✅ Core Infrastructure**: CLI, agents, orchestration working
- **✅ Framework System**: V4 specifications with validation
- **✅ Experiment System**: V2 specifications with coherence validation
- **✅ Synthesis Pipeline**: 4-agent THIN architecture operational
- **✅ Mathematical Toolkit**: Comprehensive statistical functions
- **🔄 Gasket Architecture**: In planning phase (see `pm/active_projects/`)

## ❌ Forbidden Patterns (Waste Time & Money)

### Environment Recreation (Don't Do This)
```bash
# ❌ DON'T recreate venv - it's already set up
rm -rf venv && python3 -m venv venv  # WASTES TIME

# ✅ DO use existing environment
source venv/bin/activate && python3  # CORRECT
```

### Terminal Hanging Commands (Don't Do This)
```bash
# ❌ DON'T use long git commit messages - they hang
git commit -m "Very long detailed message that explains everything..."  # HANGS

# ✅ DO use short commit messages
git commit -m "Fix CLI validation"  # WORKS

# ❌ DON'T use gh issue view without | cat
gh issue view 68  # HANGS

# ✅ DO pipe through cat
gh issue view 68 | cat  # WORKS
```

### Deprecated Components (Don't Use These)
```bash
# ❌ DON'T use deprecated CLI - it's been moved to deprecated/
python3 discernus/cli_legacy_redis.py run projects/simple_test  # DEPRECATED

# ✅ DO use current CLI
python3 -m discernus.cli run projects/simple_test  # CURRENT
```

## 🎯 Current Mission: 3 Test Experiments + Completion Items

### Active Experiments to Test:
1. **`projects/1a_caf_civic_character/`** - CAF framework validation
2. **`projects/1b_chf_character_heuristics/`** - CHF framework validation  
3. **`projects/1c_ecf_emotional_climate/`** - ECF framework validation

### Completion Items:
- Framework validation across all 3 experiments
- Gasket architecture implementation planning
- Documentation updates

## 🛠️ Working Environment Details

- **Python**: 3.13.5 (use `python3`, not `python`)
- **Virtual Environment**: `./venv/bin/python3` (always activate first)
- **Context Window**: Gemini 2.5 Pro (2M tokens), Flash (1M tokens)
- **Infrastructure**: MinIO (artifact storage), Redis (coordination)

## 🔧 Common Debugging Shortcuts

```bash
# Check environment
make check

# Run tests
make test

# Start infrastructure
make start-infra

# Clean temporary files
make clean

# Debug experiment
make debug EXPERIMENT=projects/simple_test
```

## 📚 Key Documentation

- **Architecture**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Active Projects**: `pm/active_projects/` (current development)
- **Frameworks**: `frameworks/` (analytical approaches)
- **Quick Start**: This file (30-second orientation)

## 🎯 Success Pattern

1. **Verify Environment**: `make check` ✅
2. **Test CLI**: `python3 -m discernus.cli list` ✅  
3. **Run Experiment**: `make run EXPERIMENT=projects/simple_test` ✅
4. **Check Results**: Look in `projects/simple_test/runs/` ✅

**You're ready to contribute!** 🚀
