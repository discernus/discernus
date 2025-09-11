# Discernus Developer Documentation

**Comprehensive documentation for researchers and developers using the Discernus computational social science platform.**

## 🚀 Getting Started

### For Users
- **[User Guide](../user/README.md)** - Complete user documentation
- **[Quick Start Guide](../user/QUICK_START_GUIDE.md)** - 5-minute tutorial
- **[Installation Guide](../user/INSTALLATION_GUIDE.md)** - Setup instructions
- **[CLI Reference](../user/CLI_REFERENCE.md)** - All commands and options
- **[Performance Guide](../user/PERFORMANCE_GUIDE.md)** - Timing and costs

### For Developers
- **[System Architecture](architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md)** - Complete technical architecture
- **[Logging Architecture](architecture/DUAL_TRACK_LOGGING_ARCHITECTURE.md)** - Logging system design
- **[Search Architecture](architecture/typesense_bm25_pipeline_documentation.md)** - Search system implementation
- **[Provenance System](architecture/PROVENANCE_SYSTEM.md)** - Research tracking implementation
- **[CLI Command Reference](CLI_COMMAND_REFERENCE.md)** - Complete command documentation
- **[CLI Best Practices](CLI_BEST_PRACTICES.md)** - Model selection, cost optimization, workflows
- **[CLI Configuration Guide](CLI_CONFIGURATION_GUIDE.md)** - Config files and environment variables
- **[Agent Briefing](setup/AGENT_BRIEFING.md)** - Quick start for new contributors
- **[Testing Strategy](workflows/TESTING_STRATEGY.md)** - Testing approach and guidelines

## 🚨 Critical Development Protocols

### Critical Regression Remediation
- **[TDD Protocol for Critical Regressions](TDD_CRITICAL_REGRESSION_PROTOCOL.md)** - Proven 6-phase approach that successfully resolved ARCH-002
- **[Batch Processing Regression Remediation Plan](BATCH_PROCESSING_REGRESSION_REMEDIATION_PLAN.md)** - Detailed case study of ARCH-002 resolution

**When critical regressions are identified:**
1. **IMMEDIATE STOP** - No live debugging or expensive API experiments
2. **Document Issue** - Log in `pm/todo/discernus_v10_backlog.md` with ARCH-XXX identifier
3. **Follow TDD Protocol** - Use proven 6-phase approach for cost-effective resolution

## 📚 Documentation Structure

### CLI Documentation
| Document | Audience | Purpose |
|----------|----------|---------|
| [CLI Quick Reference](CLI_QUICK_REFERENCE.md) | All users | Essential commands, quick start |
| [CLI Command Reference](CLI_COMMAND_REFERENCE.md) | Power users | Complete command documentation |
| [CLI Configuration Guide](CLI_CONFIGURATION_GUIDE.md) | Advanced users | Config files, env vars, hierarchy |
| [CLI Best Practices](CLI_BEST_PRACTICES.md) | All users | Optimization, troubleshooting, workflows |

### Setup & Onboarding
- **[Agent Briefing](setup/AGENT_BRIEFING.md)** - New contributor quick start
- **[GitHub Issues Setup](setup/GITHUB_ISSUES_SETUP.md)** - Issue tracking configuration

### Workflows & Processes
- **[Git Best Practices](workflows/GIT_BEST_PRACTICES.md)** - Version control guidelines
- **[Testing Strategy](workflows/TESTING_STRATEGY.md)** - Testing approach and tools
- **[Fast Iteration Testing](testing/FAST_ITERATION_TESTING_METHODS.md)** - Mock testing and prompt engineering harness
- **[Research Provenance Guide](workflows/RESEARCH_PROVENANCE_GUIDE.md)** - Academic audit trails
- **[Provenance Validation Reference](workflows/PROVENANCE_VALIDATION_REFERENCE.md)** - Integrity validation

### Troubleshooting
- **[Troubleshooting Guide](troubleshooting/TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions
- **[Infrastructure Troubleshooting](troubleshooting/INFRASTRUCTURE_TROUBLESHOOTING.md)** - System-level issues
- **[Corpus Security Checklist](troubleshooting/CORPUS_SECURITY_CHECKLIST.md)** - Data security guidelines

## 🎯 Quick Navigation

### I want to...

**Run my first experiment**
→ Start with [CLI Quick Reference](CLI_QUICK_REFERENCE.md)

**Optimize costs and performance**  
→ See [Best Practices](CLI_BEST_PRACTICES.md)

**Set up configuration files**
→ Read [Configuration Guide](CLI_CONFIGURATION_GUIDE.md)

**Understand all CLI options**
→ Reference [Command Reference](CLI_COMMAND_REFERENCE.md)

**Troubleshoot an issue**
→ Check [Troubleshooting Guide](troubleshooting/TROUBLESHOOTING_GUIDE.md)

**Debug infrastructure issues quickly**
→ Use [Fast Iteration Testing](testing/FAST_ITERATION_TESTING_METHODS.md)

**Contribute to development**
→ Begin with [Agent Briefing](setup/AGENT_BRIEFING.md)

**Validate research integrity**
→ Use [Provenance Validation](workflows/PROVENANCE_VALIDATION_REFERENCE.md)

## 🏗️ Architecture Overview

Discernus follows **THIN Architecture Principles**:

- **LLM Intelligence**: Analysis, reasoning, and content generation
- **Software Infrastructure**: Simple routing, storage, and execution
- **Natural Language Flow**: LLM-to-LLM communication without parsing
- **Centralized Prompts**: Prompts engineered as part of consuming agents

### Key Components

**CLI Interface**: Professional terminal experience with Rich library
- Modern conventions (config files, env vars, semantic exit codes)
- Hierarchical configuration (CLI > env > config > defaults)
- Professional output with structured tables and progress bars

**Storage System**: Content-addressable local filesystem
- SHA-256 hashing for integrity and deduplication
- Symlink-based provenance organization
- Git integration for long-term audit trails

**Agent Architecture**: THIN agents with externalized YAML prompts
- Direct function calls (no Redis coordination)
- Intelligent extraction gaskets for LLM-to-math translation
- Framework-agnostic design supporting any analytical approach

## 🔧 Development Environment

### Prerequisites
- Python 3.13.5+ with virtual environment
- Git for version control
- Google Cloud credentials for Vertex AI

### Setup
```bash
# Clone and setup
git clone https://github.com/discernus/discernus.git
cd discernus
make install

# Verify environment
make check

# Run tests
make test
```

### Testing Methods
```bash
# Mock testing for infrastructure (0 cost, instant feedback)
python3 test_infrastructure_mock.py

# Prompt engineering harness (minimal cost, fast iteration)
python3 test_prompt_variations.py

# Full experiment (higher cost, comprehensive testing)
discernus run projects/simple_test
```

### Modern CLI Development
```bash
# Create config for development
discernus config init

# Test with verbose output
discernus --verbose run --dry-run

# Use environment variables
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
discernus run
```

## 📊 Project Status

**Current Phase**: Alpha v1.1 - Performance & UX
- ✅ THIN v2.0 architecture complete
- ✅ Rich CLI integration complete  
- ✅ Configuration system complete
- ✅ Provenance system complete
- 🔄 CLI documentation complete
- 📋 Advanced CLI features (shell completion, etc.)

## 🤝 Contributing

1. **Read the briefing**: Start with [Agent Briefing](setup/AGENT_BRIEFING.md)
2. **Understand THIN**: Review architecture principles in main README
3. **Follow conventions**: Use [Git Best Practices](workflows/GIT_BEST_PRACTICES.md)
4. **Test thoroughly**: Follow [Testing Strategy](workflows/TESTING_STRATEGY.md)
5. **Document changes**: Update relevant documentation

## 🔗 External Resources

- **GitHub Repository**: [discernus/discernus](https://github.com/discernus/discernus)
- **Issue Tracker**: [GitHub Issues](https://github.com/discernus/discernus/issues)
- **Architecture Documentation**: `../architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Technical Specifications**: `../specifications/` directory

---

*Last updated: January 2025 - CLI Documentation Complete*