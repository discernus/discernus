# Discernus: Computational Text Analysis Platform

**Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## 📚 Documentation

- **Architecture**: See `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Quick Start**: See `CURSOR_AGENT_QUICK_START.md`
- **CLI Guide**: See `CLAUDE.md` for development commands
- **Frameworks**: See `frameworks/` directory for analytical frameworks
- **Specifications**: See `docs/specifications/` for technical specs

## 🚀 Quick Start

```bash
# 1. Set up environment
make install

# 2. Verify setup
make check

# 3. Run a simple experiment
make run EXPERIMENT=projects/simple_test
```

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
# Core commands
make run EXPERIMENT=<path>      # Run complete experiment
make continue EXPERIMENT=<path> # Resume from artifacts
make debug EXPERIMENT=<path>    # Interactive debugging

# Development
make check                     # Verify environment
make test                      # Run test suite
make deps                      # Update dependencies
make clean                     # Clean temporary files

# Infrastructure
make start-infra              # Start MinIO and Redis
make stop-infra               # Stop infrastructure services
```

## 🛠️ Development Tools

- **Environment**: Python 3.13.5 with virtual environment
- **Testing**: pytest with comprehensive test suite
- **Code Quality**: black, isort, flake8
- **Infrastructure**: MinIO for artifact storage, Redis for coordination
- **LLM Gateway**: LiteLLM for multi-provider access

## 🔗 Key Resources

- **GitHub Issues**: For bug reports and feature requests
- **Architecture Docs**: `docs/architecture/` for system design
- **Active Projects**: `pm/active_projects/` for current development
- **Frameworks**: `frameworks/` for analytical approaches
- **Experiments**: `projects/` for research experiments

---

