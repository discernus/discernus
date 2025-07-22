# Developer Documentation Hub

**Welcome to Discernus development!** This directory contains everything developers need, organized by function.

## 🚀 Quick Start for Developers

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

# Test a model quickly
make harness-simple MODEL="vertex_ai/gemini-2.5-flash" PROMPT="What is 2+2?"
```

### Step 3: Choose Your Path
- **New to the project?** → Start with [`setup/`](setup/) directory
- **Ready to develop?** → See [`workflows/`](workflows/) directory  
- **Need architecture info?** → Explore [`architecture/`](architecture/) directory
- **Having problems?** → Check [`troubleshooting/`](troubleshooting/) directory

---

## 📁 Developer Documentation Structure

### 🛠️ [`setup/`](setup/) - Getting Started & Environment
- **[`AGENT_BRIEFING.md`](setup/AGENT_BRIEFING.md)** - **READ FIRST** - Complete developer onboarding
- **[`CURSOR_AGENT_ENVIRONMENT_GUIDE.md`](setup/CURSOR_AGENT_ENVIRONMENT_GUIDE.md)** - Environment troubleshooting reference
- **[`AI_AGENT_GITHUB_GUIDE.md`](setup/AI_AGENT_GITHUB_GUIDE.md)** - GitHub CLI for AI agents
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
- **[`PLATFORM_ARCHITECTURE_OVERVIEW.md`](architecture/PLATFORM_ARCHITECTURE_OVERVIEW.md)** - **HIGH-LEVEL** system overview
- **[`AGENT_DESIGN_PRINCIPLES.md`](architecture/AGENT_DESIGN_PRINCIPLES.md)** - Agent development patterns
- **[`THIN_COMPLIANCE_CHECKLIST.md`](architecture/THIN_COMPLIANCE_CHECKLIST.md)** - Architecture validation
- **[`CORE_INFRASTRUCTURE_GUIDE.md`](architecture/CORE_INFRASTRUCTURE_GUIDE.md)** - Infrastructure implementation

### 🔧 [`troubleshooting/`](troubleshooting/) - Problem Solving
- **[`TROUBLESHOOTING_GUIDE.md`](troubleshooting/TROUBLESHOOTING_GUIDE.md)** - General debugging guide
- **[`system_health_and_reliability.md`](troubleshooting/system_health_and_reliability.md)** - System health monitoring

---

## 💡 Development Patterns

### Essential Commands (Never Forget These)
```bash
# Environment management
make check              # Verify environment health
make test              # Run test suite
source venv/bin/activate && python3 script.py  # Manual pattern

# Development workflow  
git status             # Check for nested repos
make harness-simple    # Quick model testing
make deps             # Install dependencies
```

### Core Principles
- **THIN Architecture**: LLM intelligence + minimal software
- **Framework Agnostic**: Works with any compliant framework
- **Human-Centric**: Amplify intelligence, don't replace judgment
- **Environment First**: Always `make check` before development

---

## 🎯 Common Developer Journeys

### **New Developer Onboarding**
1. [`setup/AGENT_BRIEFING.md`](setup/AGENT_BRIEFING.md) - Read the complete briefing
2. [`setup/CURSOR_AGENT_ENVIRONMENT_GUIDE.md`](setup/CURSOR_AGENT_ENVIRONMENT_GUIDE.md) - Environment troubleshooting
3. [`workflows/DEV_MODE_GUIDE.md`](workflows/DEV_MODE_GUIDE.md) - Test the system works
4. [`architecture/ARCHITECTURE_QUICK_REFERENCE.md`](architecture/ARCHITECTURE_QUICK_REFERENCE.md) - Understand the system

### **Building New Features**
1. [`architecture/THIN_ARCHITECTURE_REFERENCE.md`](architecture/THIN_ARCHITECTURE_REFERENCE.md) - Understand THIN patterns
2. [`workflows/TESTING_STRATEGY.md`](workflows/TESTING_STRATEGY.md) - Plan your tests
3. [`architecture/AGENT_DESIGN_PRINCIPLES.md`](architecture/AGENT_DESIGN_PRINCIPLES.md) - Follow design patterns
4. [`architecture/THIN_COMPLIANCE_CHECKLIST.md`](architecture/THIN_COMPLIANCE_CHECKLIST.md) - Validate compliance

### **Debugging Issues**
1. [`troubleshooting/TROUBLESHOOTING_GUIDE.md`](troubleshooting/TROUBLESHOOTING_GUIDE.md) - General debugging
2. [`setup/CURSOR_AGENT_ENVIRONMENT_GUIDE.md`](setup/CURSOR_AGENT_ENVIRONMENT_GUIDE.md) - Environment issues
3. [`setup/AI_AGENT_GITHUB_GUIDE.md`](setup/AI_AGENT_GITHUB_GUIDE.md) - GitHub authentication issues
4. [`troubleshooting/system_health_and_reliability.md`](troubleshooting/system_health_and_reliability.md) - System health

---

**🎉 Happy developing!** The goal is **development velocity** while maintaining **THIN architecture principles** and **human-centric design**. 