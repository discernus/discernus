# README for Cursor Agents

**Start Here**: This document provides everything a new Cursor agent needs to be productive immediately.

## 🚀 30-Second Quick Start

```bash
make check                                        # Verify environment ✅
discernus run projects/simple_test --skip-validation  # Fast test (~47s, $0.014) ✅
```

**That's it!** If both commands work, you're ready to go.

## 💡 Key Changes (August 2025)

**The system has been significantly simplified and stabilized:**

- **✅ Simple CLI**: Use `discernus` command directly (not `python3 -m discernus.cli`)
- **✅ No venv**: System uses stable Python 3.13.5 installation
- **✅ Fixed Symlinks**: Artifact caching works perfectly 
- **✅ Smart Paths**: Works from any directory, canonical frameworks supported
- **✅ Cost Control**: Flash Lite models available for fast development

## 🎯 Recommended Workflow

1. **Environment Check**: `make check` (should pass immediately)
2. **Fast Test**: `discernus run projects/simple_test --skip-validation`
3. **Development**: Use `projects/simple_test/` for iteration (47 seconds, $0.014 per run)
4. **Production**: Use other experiments with Pro models when needed

## 📁 Key Files Updated for You

- **`CURSOR_AGENT_QUICK_START.md`**: Comprehensive 30-second orientation
- **`SYSTEM_STATUS.md`**: Current system status and capabilities
- **`.cursor/rules`**: Updated rules reflecting current best practices
- **`.discernus.yaml`**: Global config with sensible defaults
- **`projects/simple_test/.discernus.yaml`**: Local Flash Lite config for fast testing

## 🔧 Essential Commands

```bash
# Basic operations
discernus list                           # List all experiments
discernus validate projects/simple_test  # Check experiment structure  
discernus run projects/simple_test      # Run experiment

# Fast development
cd projects/simple_test && discernus run .  # Uses local Flash Lite config

# Model overrides (if needed)
discernus run projects/simple_test --analysis-model vertex_ai/gemini-2.5-flash-lite
discernus run projects/simple_test --synthesis-model vertex_ai/gemini-2.5-pro
```

## 🛡️ What's Stable & Reliable

- **Environment**: No more venv issues, system Python works perfectly
- **CLI**: Simple `discernus` command, no complex module paths
- **Paths**: Works from any directory, intelligent framework resolution
- **Caching**: Artifact symlinks fixed, perfect caching performance
- **Costs**: Predictable model costs with Flash Lite options

## 🚫 What NOT to Do (Avoid These)

- **Don't recreate environments** - system is stable
- **Don't use complex Python paths** - `discernus` command works
- **Don't manually create framework symlinks** - canonical paths work automatically
- **Don't ignore .discernus.yaml configs** - they provide useful defaults

## 💰 Cost Management

- **Development/Testing**: `projects/simple_test/` (~$0.014 per run, 47 seconds)
- **Production Analysis**: Other experiments with Pro models (~$0.27 per run)
- **Model Selection**: Flash Lite for speed, Pro for quality

## 📚 Documentation

- **`CURSOR_AGENT_QUICK_START.md`**: Detailed orientation (start here)
- **`SYSTEM_STATUS.md`**: Current system capabilities
- **`README.md`**: Project overview
- **`docs/`**: Complete technical documentation

---

**Bottom Line**: The system is stable, fast, and ready for production use. Start with `make check` and `discernus run projects/simple_test --skip-validation` - you'll be productive in under a minute.