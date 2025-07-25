# Developer Documentation Hub

**Welcome to Discernus development!** This directory contains everything developers need, organized by function.

## 🚀 Quick Start for Developers

### ⚡ INSTANT ORIENTATION (New Agents)
**READ FIRST**: [`CURSOR_AGENT_QUICK_START.md`](../CURSOR_AGENT_QUICK_START.md) - **30-second orientation to prevent $0.50 confusion cycles**

### Step 1: Environment Setup
```bash
# Verify/setup environment (ALWAYS START HERE)
make check

# If environment setup needed:
make install && make check
```

### Step 2: Verify System Works
```bash
# Run quick tests (30 seconds)
make test

# Test CLI works
discernus --help
discernus list
```

---

## 📁 Developer Documentation Structure

### 🛠️ [`setup/`](setup/) - Getting Started & Environment
- **[`AGENT_BRIEFING.md`](setup/AGENT_BRIEFING.md)** - Complete developer briefing (comprehensive)
- **[`GITHUB_ISSUES_SETUP.md`](setup/GITHUB_ISSUES_SETUP.md)** - Issue tracking setup

### 🔄 [`workflows/`](workflows/) - Day-to-Day Development
- **[`DEV_MODE_GUIDE.md`](workflows/DEV_MODE_GUIDE.md)** - Development testing workflows
- **[`GIT_BEST_PRACTICES.md`](workflows/GIT_BEST_PRACTICES.md)** - Git workflow patterns  
- **[`TESTING_STRATEGY.md`](workflows/TESTING_STRATEGY.md)** - Testing approaches
- **[`EXTENSION_DEVELOPMENT_GUIDE.md`](workflows/EXTENSION_DEVELOPMENT_GUIDE.md)** - Building extensions
- **[`EXTENSION_GUIDE.md`](workflows/EXTENSION_GUIDE.md)** - Extension system overview

### 🏗️ [`architecture/`](architecture/) - System Design & Principles
- **[`THIN_ARCHITECTURE_REFERENCE.md`](architecture/THIN_ARCHITECTURE_REFERENCE.md)** - **COMPREHENSIVE** architecture guide
- **[`ARCHITECTURE_QUICK_REFERENCE.md`](architecture/ARCHITECTURE_QUICK_REFERENCE.md)** - **QUICK** architecture summary
- **[`AGENT_DESIGN_PRINCIPLES.md`](architecture/AGENT_DESIGN_PRINCIPLES.md)** - Agent development patterns
- **[`CORE_INFRASTRUCTURE_GUIDE.md`](architecture/CORE_INFRASTRUCTURE_GUIDE.md)** - Infrastructure implementation
- **[`PLATFORM_ARCHITECTURE_OVERVIEW.md`](architecture/PLATFORM_ARCHITECTURE_OVERVIEW.md)** - High-level system overview
- **[`THIN_COMPLIANCE_CHECKLIST.md`](architecture/THIN_COMPLIANCE_CHECKLIST.md)** - Architecture validation
- **[`WORKFLOW_SECURITY_ARCHITECTURE.md`](architecture/WORKFLOW_SECURITY_ARCHITECTURE.md)** - Security design

### 🔧 [`troubleshooting/`](troubleshooting/) - Problem Solving
- **[`TROUBLESHOOTING_GUIDE.md`](troubleshooting/TROUBLESHOOTING_GUIDE.md)** - General debugging guide
- **[`CORPUS_SECURITY_CHECKLIST.md`](troubleshooting/CORPUS_SECURITY_CHECKLIST.md)** - Corpus security validation

---

## 💡 Current Development Context (Alpha System)

### **Project Status**: ✅ 95% Complete Alpha System
- **CLI**: Working (`discernus run`, `validate`, `list`, `status`)
- **Infrastructure**: Redis + MinIO + 6 agents with YAML prompts ready
- **Architecture**: Clean THIN implementation with aggressive cleanup completed

### **Current Mission**: Complete Final 5%
1. **Three diverse test experiments** (Political, Corporate, Academic)
2. **BaseAgent abstraction** for standardized logging  
3. **ReportAgent** for final output generation
4. **Prompt "DNA" capture** for provenance
5. **Minor CLI fixes** (click argument handling)

### Essential Commands
```bash
# Environment management
make check              # Verify environment health (ALWAYS START HERE)
make test              # Run test suite
discernus list         # See available experiments
discernus status       # Check Redis infrastructure

# Development workflow  
python3 scripts/prompt_engineering_harness.py --list-models
source venv/bin/activate && python3 script.py  # Manual pattern
```

### Core Principles  
- **THIN Architecture**: LLM intelligence + minimal software coordination
- **95% Complete**: Focus on content creation, not infrastructure rebuilding
- **Environment First**: Always `make check` before development
- **Redis + MinIO**: All coordination via existing infrastructure

---

## 🎯 Common Developer Journeys

### **New Developer Onboarding**
1. **[`CURSOR_AGENT_QUICK_START.md`](../CURSOR_AGENT_QUICK_START.md)** - Instant orientation (30 seconds)
2. **[`setup/AGENT_BRIEFING.md`](setup/AGENT_BRIEFING.md)** - Complete briefing (comprehensive)
3. **[`architecture/ARCHITECTURE_QUICK_REFERENCE.md`](architecture/ARCHITECTURE_QUICK_REFERENCE.md)** - Understand the system
4. **Run**: `make check && make test` - Verify everything works

### **Alpha System Completion** 
1. **[`pm/active_projects/ALPHA_SYSTEM_SPECIFICATION.md`](../../pm/active_projects/ALPHA_SYSTEM_SPECIFICATION.md)** - Requirements
2. **[`pm/active_projects/FRESH_START_BRIEF.md`](../../pm/active_projects/FRESH_START_BRIEF.md)** - Current clean state
3. **[`architecture/THIN_ARCHITECTURE_REFERENCE.md`](architecture/THIN_ARCHITECTURE_REFERENCE.md)** - Architecture patterns
4. **[`workflows/TESTING_STRATEGY.md`](workflows/TESTING_STRATEGY.md)** - Testing approach

### **Debugging Issues**
1. **[`troubleshooting/TROUBLESHOOTING_GUIDE.md`](troubleshooting/TROUBLESHOOTING_GUIDE.md)** - General debugging
2. **Run**: `make check` - Environment issues
3. **Check**: `.cursor/rules` - Behavioral guidelines
4. **Review**: Git status for nested repo issues

---

**🎯 Remember**: This is a **95% complete Alpha System**. Focus on content creation (experiments) and minor completion items, not rebuilding infrastructure. The hard architectural work is done. 