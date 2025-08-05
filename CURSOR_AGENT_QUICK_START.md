# Cursor Agent Quick Start Guide

**30-Second Orientation for New Cursor Agents**

## 🚀 Environment Verification (Run First!)

```bash
# 1. Check environment setup (ESSENTIAL)
make check

# 2. Verify CLI works (use the simple 'discernus' command)
discernus list

# 3. Run simple test (fast, cost-effective)
discernus run projects/simple_test --skip-validation

# 4. Alternative: From experiment directory (uses local config)
cd projects/simple_test && discernus run .
```

## ✅ **MAJOR UPDATE**: Simplified CLI & Environment

**As of August 2025, the environment has been significantly simplified:**

- **✅ Direct CLI**: Use `discernus` command (not `python3 -m discernus.cli`)
- **✅ System Python**: No venv, uses system Python 3.13.5 with user packages
- **✅ Fixed Symlinks**: Artifact caching now works correctly
- **✅ Path Flexibility**: CLI works from any directory with canonical framework support

## 🛡️ Recommended Commands for Agents

**Use these clean, simple commands:**

```bash
# ✅ PREFERRED: Direct CLI commands (simple and reliable)
discernus list                                    # List experiments
discernus run projects/simple_test               # Run from project root
cd projects/simple_test && discernus run .      # Run with local config

# ✅ ALTERNATIVE: Makefile shortcuts (if needed)
make run EXPERIMENT=projects/simple_test

# ❌ DEPRECATED: Old complex commands (still work but unnecessary)
python3 -m discernus.cli list                   # Too verbose
./scripts/safe_python.sh -m discernus.cli list  # Too complex
```

## 📊 Project Status: 98% Complete Alpha System

- **✅ Core Infrastructure**: CLI, agents, orchestration working perfectly
- **✅ Framework System**: V7.3 specifications with validation
- **✅ Experiment System**: V7.1 specifications with coherence validation
- **✅ Synthesis Pipeline**: 4-agent THIN architecture operational
- **✅ Mathematical Toolkit**: Comprehensive statistical functions
- **✅ Environment**: Simplified, reliable, fast
- **✅ Artifact System**: Fixed symlinks, perfect caching
- **🔄 Advanced Features**: Framework validation, gasket architecture (see `pm/active_projects/`)

## ❌ Common Pitfalls (Avoid These)

### Environment Confusion (Fixed!)
```bash
# ❌ DON'T recreate environments - system is stable now
rm -rf venv && python3 -m venv venv  # UNNECESSARY

# ✅ DO use direct CLI commands
discernus run projects/simple_test    # SIMPLE & RELIABLE
```

### Path & Framework Issues (Fixed!)
```bash
# ❌ DON'T manually create framework.md symlinks
ln -s ../../frameworks/reference/core/caf_v7.3.md framework.md  # UNNECESSARY

# ✅ DO use canonical framework paths (works automatically)
# Just reference "../../frameworks/..." in experiment.md - CLI handles it
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
./scripts/safe_python.sh -m discernus.cli run projects/simple_test  # SAFEST
```

## 🎯 Current Mission: Stable Platform with Test Experiments

### Recommended Test Experiments:
1. **`projects/simple_test/`** - Fast, cost-effective validation (Flash Lite models, ~$0.014/run)
2. **`projects/1a_caf_civic_character/`** - CAF framework validation
3. **`projects/1b_chf_character_heuristics/`** - CHF framework validation  
4. **`projects/1c_ecf_emotional_climate/`** - ECF framework validation

### Key Features Working:
- **✅ CLI Path Flexibility**: Works from any directory
- **✅ Canonical Frameworks**: No need for local framework.md files  
- **✅ Model Configuration**: Project-specific .discernus.yaml support
- **✅ Artifact Caching**: Perfect symlink system

## 🛠️ Working Environment Details

- **Python**: 3.13.5 system installation (no venv)
- **CLI**: `discernus` command (installed as entry point)
- **Models**: Gemini 2.5 Flash Lite (default analysis), Pro (default synthesis)
- **Context Window**: Gemini 2.5 Pro (2M tokens), Flash (1M tokens)
- **Storage**: Local filesystem with perfect artifact caching

## 🔧 Common Debugging Shortcuts

```bash
# Check environment
make check

# List experiments
discernus list

# Validate experiment structure
discernus validate projects/simple_test

# Run with debugging
discernus debug projects/simple_test --verbose

# Skip validation if needed
discernus run projects/simple_test --skip-validation
```

## 🛡️ Quick Command Reference

**Essential Commands for Cursor Agents:**

```bash
# Environment checks
make check                                       # Verify system setup

# Basic operations
discernus list                                   # List all experiments
discernus validate projects/simple_test          # Check experiment structure
discernus run projects/simple_test              # Run experiment
discernus continue projects/simple_test         # Resume experiment

# Model configuration examples
discernus run projects/simple_test --analysis-model vertex_ai/gemini-2.5-flash-lite
cd projects/simple_test && discernus run .      # Uses local .discernus.yaml config

# Fast testing
discernus run projects/simple_test --skip-validation  # Skip validation for speed
```

## 📚 Key Documentation

- **Architecture**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Active Projects**: `pm/active_projects/` (current development)
- **Frameworks**: `frameworks/` (analytical approaches)
- **Quick Start**: This file (30-second orientation)

## 🎯 Success Pattern

1. **Verify Environment**: `make check` ✅
2. **Test CLI**: `discernus list` ✅  
3. **Run Fast Test**: `discernus run projects/simple_test --skip-validation` ✅
4. **Check Results**: Look in `projects/simple_test/runs/` ✅

**Total time: ~1 minute to full working system!** 🚀

## 💡 Pro Tips for Cursor Agents

- **Use `projects/simple_test/`** for fast iteration (~47 seconds, $0.014 per run)
- **Run from experiment directory** to use local model config: `cd projects/simple_test && discernus run .`
- **Canonical frameworks work automatically** - no need to create local framework.md files
- **CLI works from anywhere** - path resolution is intelligent
- **Symlinks are fixed** - artifact caching works perfectly
