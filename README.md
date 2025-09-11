# Discernus: Computational Text Analysis Platform

**Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## 📚 Documentation

### For Users
- **[User Guide](docs/user/README.md)** - Complete user documentation
- **[Quick Start](docs/user/QUICK_START_GUIDE.md)** - 5-minute tutorial
- **[Installation](docs/user/INSTALLATION_GUIDE.md)** - Setup instructions
- **[CLI Reference](docs/user/CLI_REFERENCE.md)** - All commands
- **[Performance Guide](docs/user/PERFORMANCE_GUIDE.md)** - Timing and costs
- **[Release Notes](docs/user/RELEASE_NOTES.md)** - Alpha features

### For Developers
- **[Developer Guide](docs/developer/README.md)** - Technical documentation
- **[Architecture](docs/architecture/)** - System design
- **[Specifications](docs/specifications/)** - Technical specs
- **[Agent Quick Start](CURSOR_AGENT_QUICK_START.md)** - For contributors

## 🚀 Quick Start

```bash
# 1. Set up environment (if needed)
make install

# 2. Verify setup
make check

# 3. Run fast test experiment (~47 seconds, $0.014)
discernus run projects/nano_test_experiment --skip-validation

# 4. List available experiments
discernus list

# 5. Check system status
discernus status

# Or run with local config (from experiment directory)
cd projects/nano_test_experiment && discernus run .
```

### Run Modes

```bash
# Complete research pipeline (default)
discernus run projects/experiment

# Analysis-only mode (quick data exploration)
discernus run projects/experiment --analysis-only

# Statistical preparation mode (for external analysis)
discernus run projects/experiment --statistical-prep

# Resume from statistical preparation
discernus resume projects/experiment

# Create publication-ready archive
discernus archive projects/experiment/runs/LATEST_RUN \
  --include-session-logs --include-artifacts --create-statistical-package
```

**New to Discernus?** Start with the [CLI Quick Reference](docs/developer/CLI_QUICK_REFERENCE.md) for essential commands.

## 🏗️ THIN Architecture Principles

### ✅ **THIN Patterns (Do This)**
- **LLM Intelligence**: Analysis, reasoning, and content generation in prompts
- **Software Infrastructure**: Simple routing, storage, and execution
- **Natural Language Flow**: LLM-to-LLM communication without parsing
- **Framework Agnostic**: Accept any analytical framework - no hardcoded restrictions
- **Centralized Prompts**: Prompts are engineered as part of the agent that consumes them, not hardcoded.

### ❌ **THICK Anti-Patterns (Don't Do This)**
- Complex JSON parsing from LLM responses
- Hardcoded prompts in orchestrator code
- Mathematical operations in software (use hybrid intelligence pattern)
- Domain-specific assumptions in core platform
- Hardcoded framework lists or restrictions

## 🎯 Three Foundational Commitments

1. **Structured Data, Not Code**: LLMs are prompted to return structured, verifiable data (e.g., JSON with scores) rather than executable code for analysis, which simplifies the pipeline and improves reliability.
2. **Cost Transparency**: Upfront estimation, budget controls, predictable pricing
3. **Complete Reproducibility**: Zero mystery, full audit trails, deterministic results

## 📋 Commands

```bash
# Modern CLI (recommended)
discernus run [path]           # Run complete experiment
discernus resume [path]        # Resume from cached analysis  
discernus list                 # List available experiments
discernus status               # Show system status
discernus validate [path]      # Validate experiment structure
discernus archive [path]       # Create publication archive
discernus --help               # Full command reference
```

# Development
make check                     # Verify environment
make test                      # Run test suite
make deps                      # Update dependencies
make clean                     # Clean temporary files

# Legacy make commands (still supported)
make run EXPERIMENT=<path>     # Run complete experiment
make continue EXPERIMENT=<path> # Resume from artifacts
make debug EXPERIMENT=<path>   # Interactive debugging
```

**Tip**: Use `discernus --verbose` for detailed output or `discernus --quiet` for minimal output.

## 🛠️ Development Tools

- **Environment**: Python 3.13.5 with virtual environment
- **Testing**: pytest with comprehensive test suite
- **Code Quality**: black, isort, flake8
- **Storage**: Local filesystem with content-addressable artifacts
- **LLM Gateway**: LiteLLM for multi-provider access
- **CLI Interface**: Rich library for professional terminal experience

## 🔗 Key Resources

- **GitHub Issues**: For bug reports and feature requests
- **Architecture Docs**: `docs/architecture/` for system design
- **Corpus Library**: `corpus/` for text collections and analysis datasets
- **GitHub Repositories**: `corpus/github_repositories/` for integrated external speech corpora
- **Active Projects**: `pm/active_projects/` for current development
- **Frameworks**: `frameworks/` for analytical approaches
- **Experiments**: `projects/` for research experiments

---

