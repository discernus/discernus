# Discernus: Computational Text Analysis Platform

**Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## 📚 Documentation

**Complete documentation is available at**: [`docs/README.md`](docs/README.md)

The docs directory contains comprehensive guides for:
- **New Users**: Getting started with the platform
- **Developers**: Architecture and technical implementation  
- **Researchers**: Framework integration and academic workflows
- **Framework Developers**: Extension development and community standards

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run validation
python3 discernus_cli.py validate ./my_project

# Execute analysis
python3 discernus_cli.py execute ./my_project
```

## 🏗️ THIN Architecture Principles

### ✅ **THIN Patterns (Do This)**
- **LLM Intelligence**: Analysis, reasoning, and content generation in prompts
- **Software Infrastructure**: Simple routing, storage, and execution
- **Natural Language Flow**: LLM-to-LLM communication without parsing
- **Centralized Prompts**: All prompts in `discernus/core/llm_roles.py`

### ❌ **THICK Anti-Patterns (Don't Do This)**
- Complex JSON parsing from LLM responses
- Hardcoded prompts in orchestrator code
- Mathematical operations in software (use hybrid intelligence pattern)
- Domain-specific assumptions in core platform

## 🎯 Three Foundational Commitments

1. **Mathematical Reliability**: LLM designs → secure code executes → LLM interprets
2. **Cost Transparency**: Upfront estimation, budget controls, predictable pricing
3. **Complete Reproducibility**: Zero mystery, full audit trails, deterministic results

## 📋 Commands

```bash
# Validate project structure and specifications
python3 discernus_cli.py validate ./my_project

# Execute validated project with full orchestration
python3 discernus_cli.py execute ./my_project

# List available analytical frameworks
python3 discernus_cli.py list-frameworks

# Show system information and THIN compliance
python3 discernus_cli.py info --check-thin
```

## 🔗 Key Resources

- **[Complete Documentation](docs/README.md)** - Master index and user guides
- **[Agent Briefing](docs/AGENT_BRIEFING.md)** - Essential principles for contributors
- **[Strategic Vision](docs/DISCERNUS_STRATEGIC_VISION.md)** - Mission and use cases
- **[Quick Start Guide](docs/QUICK_START_GUIDE.md)** - Detailed getting started guide

---

*For complete documentation, examples, and advanced usage, see [`docs/README.md`](docs/README.md)*
