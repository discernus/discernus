# Discernus: Computational Text Analysis Platform

**Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## 📚 Documentation

### Core Documentation
- **CLI Quick Start**: See `docs/developer/CLI_QUICK_REFERENCE.md`
- **CLI Complete Guide**: See `docs/developer/CLI_COMMAND_REFERENCE.md`
- **CLI Reference**: See `docs/CLI_REFERENCE.md` - *Complete command reference with examples*
- **Configuration**: See `docs/developer/CLI_CONFIGURATION_GUIDE.md`
- **Best Practices**: See `docs/developer/CLI_BEST_PRACTICES.md`

### Research Infrastructure
- **Provenance System**: See `docs/PROVENANCE_SYSTEM.md` - *Complete research transparency and reproducibility*
- **Score Validation**: See `docs/developer/workflows/SCORE_VALIDATION_GUIDE.md`

### System Architecture
- **Architecture**: See `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Agent Quick Start**: See `CURSOR_AGENT_QUICK_START.md`
- **Frameworks**: See `frameworks/` directory for analytical frameworks
- **Specifications**: See `docs/specifications/` for technical specs

## 🚀 Quick Start

```bash
# 1. Set up environment (if needed)
make install

# 2. Verify setup
make check

# 3. Run fast test experiment (~47 seconds, $0.014)
discernus run projects/simple_test --skip-validation

# 4. Validate any score (<5 minutes)
discernus validate-score projects/simple_test "john_mccain_2008_concession.txt" "dignity_score" --score-value 0.65

# Or run with local Flash Lite config (from experiment directory)
cd projects/simple_test && discernus run .

# Or run from anywhere with canonical frameworks
discernus run projects/simple_test
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
- **Centralized Prompts**: Prompts are engineered as part of the agent that consumes them, not hardcoded.

### ❌ **THICK Anti-Patterns (Don't Do This)**
- Complex JSON parsing from LLM responses
- Hardcoded prompts in orchestrator code
- Mathematical operations in software (use hybrid intelligence pattern)
- Domain-specific assumptions in core platform

## 🎯 Three Foundational Commitments

1. **Structured Data, Not Code**: LLMs are prompted to return structured, verifiable data (e.g., JSON with scores) rather than executable code for analysis, which simplifies the pipeline and improves reliability.
2. **Cost Transparency**: Upfront estimation, budget controls, predictable pricing
3. **Complete Reproducibility**: Zero mystery, full audit trails, deterministic results

## 📋 Commands

```bash
# Modern CLI (recommended)
discernus run [path]           # Run complete experiment
discernus continue [path]      # Resume from cached analysis  
discernus validate-score [path] [doc] [score] --score-value [value]  # Academic validation
discernus list                 # List available experiments
discernus status               # Show system status
discernus config show          # Show configuration
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

