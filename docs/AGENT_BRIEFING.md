# 🚨 CRITICAL: Read This First - Agent Briefing

## Your Mission: Human Intelligence Amplifier

You are extending **Discernus**, a domain-neutral computational text analysis platform. Your job is to **amplify human intelligence**, not replace human judgment.

**Core Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## Strategic Context: Why This Matters

Discernus exists to **dramatically advance understanding of human rhetoric using methods that are both rigorous and scalable**. We're fighting for the marketplace of ideas in an era where computational methods are being weaponized to erode democratic discourse.

**Your Role**: Help researchers, think tanks, journalists, corporations, religious organizations, and citizens understand rhetorical patterns with unprecedented precision and scale.

## 🏗️ THIN Architecture Principles

### ✅ THIN Patterns (DO THIS)
- **LLMs provide intelligence** (analysis, reasoning, content generation)
- **Software provides infrastructure** (routing, execution, storage)
- **Natural language flow** between LLMs (no parsing required)
- **Centralized prompts** in `discernus/core/llm_roles.py`
- **Secure code execution** for mathematical operations
- **Domain-neutral core** with framework-specific modules

### 🚫 THICK Anti-Patterns (DON'T DO THIS)
- Complex JSON parsing from LLM responses
- Hardcoded prompts in orchestrator code
- If/else logic based on LLM responses
- Mathematical operations in software
- Framework-specific hardcoded logic
- Building software intelligence instead of infrastructure

## Quick Architecture Check

Before writing any code, ask yourself:
1. **Am I building software intelligence or infrastructure?**
2. **Could an LLM do this better than code?**
3. **Is this domain-neutral or domain-specific?**
4. **Does this amplify or replace human judgment?**

If you're building intelligence, use an LLM. If you're building infrastructure, use minimal code.

## Platform Architecture Overview

**Core Components**:
- **Agent Registry** (`discernus/core/agent_registry.yaml`) - Agent discovery and orchestration
- **Model Registry** (`discernus/gateway/model_registry.py`) - LLM selection and fallback
- **LLM Gateway** (`discernus/gateway/llm_gateway.py`) - Provider abstraction
- **Project Chronolog** (`discernus/core/project_chronolog.py`) - Academic provenance
- **Secure Code Executor** (`discernus/core/secure_code_executor.py`) - Mathematical reliability

**Key Principle**: The system is **framework-agnostic, corpus-agnostic, and domain-agnostic**. Political science is just our lead use case.

## Drupal-Style Ecosystem Strategy

**CORE** (Tightly Controlled):
- Agent registry system
- Model registry and LLM gateway
- Orchestration engine
- Academic provenance system
- Framework loader interface

**MODULES** (Open Ecosystem):
- Framework implementations (PDAF, CFF, sentiment analysis)
- Domain-specific tools (political science, corporate communications)
- Integration modules (external APIs, visualization)

## Common Pitfalls to Avoid

1. **Parsing Obsession**: If you're parsing JSON from LLM responses, you're doing it wrong
2. **Domain Lock-in**: Don't assume political science - think universal text analysis
3. **Orchestrator Intelligence**: Keep orchestrators as simple message routers
4. **Mathematical Software**: Let LLMs design math, secure code execute it
5. **SOAR Terminology**: We've moved past SOAR - it's just "Discernus" now

## Emergency Contacts

- **Architecture questions**: `THIN_ARCHITECTURE_PHILOSOPHY.md`
- **Implementation patterns**: `AGENT_DESIGN_PRINCIPLES.md`
- **Strategic context**: `DISCERNUS_STRATEGIC_VISION.md`
- **Compliance check**: `THIN_COMPLIANCE_CHECKLIST.md`

## Human-Centric Design

**Remember**: Researchers should feel like they're collaborating with a brilliant research assistant, not operating a technical system. The platform should **amplify human intelligence** through natural conversation and transparent processes.

**Success Metric**: If a researcher says "This feels like working with a really smart colleague," you've succeeded.

---

*This briefing contains the essential DNA of the project. Read it first, reference it often, and when in doubt, choose the approach that amplifies human intelligence rather than replacing it.* 