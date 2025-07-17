# 🚨 CRITICAL: Read This First - Agent Briefing

## Your Mission: Human Intelligence Amplifier

You are extending **Discernus**, a domain-neutral computational text analysis platform. Your job is to **amplify human intelligence**, not replace human judgment.

**Core Philosophy**: "Thick LLM + Thin Software = Epistemic Trust"

## Strategic Context: Why This Matters

Discernus exists to **dramatically advance understanding of human rhetoric using methods that are both rigorous and scalable**. We're fighting for the marketplace of ideas in an era where computational methods are being weaponized to erode democratic discourse.

**Your Role**: Help researchers, think tanks, journalists, corporations, religious organizations, and citizens understand rhetorical patterns with unprecedented precision and scale.

## 🧪 TESTING FIRST: Verify Everything Works

**Before doing ANY development**, run these tests to ensure the system works:

### ⚡ Quick Test (30 seconds)
```bash
python3 discernus/tests/quick_test.py
```
**If this fails**: There's a fundamental problem. Check environment, imports, and basic setup.

### ✅ Simple Working Tests (3 minutes)
```bash
python3 discernus/tests/simple_working_tests.py
python3 -m unittest discernus.tests.simple_working_tests -v
```
**If this fails**: Check the specific test failure and fix the underlying issue.

### 🔍 Environment Check
```bash
python3 -c "from discernus.tests import print_test_environment; print_test_environment()"
```
**Use this**: To verify Python version, virtual environment, and dependencies.

### ⚠️ Legacy Tests (Use with Caution)
```bash
# These tests may be broken due to complex mock setups:
python3 discernus/tests/comprehensive_test_suite.py
python3 discernus/tests/agent_isolation_test_framework.py
python3 discernus/tests/end_to_end_workflow_test.py
```
**If these fail**: It's expected behavior. Use simple working tests instead.

## 🏗️ THIN Architecture Principles

### ✅ THIN Patterns (DO THIS)
- **LLMs provide intelligence** (analysis, reasoning, content generation)
- **Software provides infrastructure** (routing, execution, storage)
- **Natural language flow** between LLMs (no parsing required)
- **Dynamic agent loading** via `discernus/core/agent_registry.yaml`
- **Framework-agnostic architecture** - no hardcoded field assumptions
- **Secure code execution** for mathematical operations
- **Domain-neutral core** with framework-specific modules

### 🚫 THICK Anti-Patterns (DON'T DO THIS)
- Complex JSON parsing from LLM responses
- Hardcoded prompts in orchestrator code
- If/else logic based on LLM responses
- Mathematical operations in software
- **Framework-specific hardcoded logic** (e.g., assuming 'scores' field exists)
- **Semantic assumptions about field names** (e.g., 'worldview' vs 'analysis')
- Building software intelligence instead of infrastructure

## Quick Architecture Check

Before writing any code, ask yourself:
1. **Am I building software intelligence or infrastructure?**
2. **Could an LLM do this better than code?**
3. **Is this domain-neutral or domain-specific?**
4. **Does this amplify or replace human judgment?**
5. **🚨 Am I making assumptions about framework field names?**
6. **Will this work with ANY compliant framework specification?**

If you're building intelligence, use an LLM. If you're building infrastructure, use minimal code.

**Framework-Agnostic Test**: Your code should work equally well with CFF, PDAF, sentiment analysis, or any other framework without modification.

## Platform Architecture Overview

**Core Components**:
- **WorkflowOrchestrator** (`discernus/orchestration/workflow_orchestrator.py`) - Main execution engine
- **Agent Registry** (`discernus/core/agent_registry.yaml`) - Agent discovery and orchestration
- **Model Registry** (`discernus/gateway/model_registry.py`) - LLM selection and fallback
- **LLM Gateway** (`discernus/gateway/llm_gateway.py`) - Provider abstraction
- **Project Chronolog** (`discernus/core/project_chronolog.py`) - Academic provenance
- **Secure Code Executor** (`discernus/core/secure_code_executor.py`) - Mathematical reliability

**Key Principle**: The system is **framework-agnostic, corpus-agnostic, and domain-agnostic**. Political science is just our lead use case.

**Critical Architecture Rule**: Agents must work with ANY compliant framework specification. Never hardcode assumptions about field names like 'scores', 'worldview', or 'analysis_text'.

## Testing Strategy for Development

### 1. Test-Driven Development Flow
```bash
# Step 1: Verify baseline works
python3 discernus/tests/quick_test.py

# Step 2: Write your code/changes

# Step 3: Test your changes
python3 discernus/tests/simple_working_tests.py

# Step 4: Run specific tests if needed
python3 -m unittest discernus.tests.simple_working_tests.TestYourSpecificTest -v
```

### 2. When Adding New Functionality
1. **Write a simple test first** in `simple_working_tests.py`
2. **Use standard unittest patterns** (not complex mock setups)
3. **Test one thing at a time** (clear, focused tests)
4. **Use minimal mock data** (simple, obvious responses)

### 3. When Debugging
1. **Start with quick test** to verify basic functionality
2. **Check environment** if imports fail
3. **Use simple working tests** for comprehensive validation
4. **Avoid legacy tests** unless specifically needed

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
5. **Framework-Specific Assumptions**: Never hardcode field names or assume specific data structures
6. **SOAR Terminology**: We've moved past SOAR - it's just "Discernus" now
7. **Testing Shortcuts**: Always run tests before, during, and after development
8. **Legacy Test Reliance**: Use simple working tests, not complex legacy tests

**🚨 CRITICAL**: The #1 cause of production failures is agents making hardcoded assumptions about framework field names. Always write framework-agnostic code.

## Emergency Contacts

- **Testing**: `discernus/tests/README.md` - Complete testing guide
- **Architecture questions**: `THIN_ARCHITECTURE_REFERENCE.md`
- **Implementation patterns**: `AGENT_DESIGN_PRINCIPLES.md`
- **Strategic context**: `DISCERNUS_STRATEGIC_VISION.md`
- **Compliance check**: `THIN_COMPLIANCE_CHECKLIST.md`
- **Framework specifications**: `docs/specifications/FRAMEWORK_SPECIFICATION_V4.md`

## Human-Centric Design

**Remember**: Researchers should feel like they're collaborating with a brilliant research assistant, not operating a technical system. The platform should **amplify human intelligence** through natural conversation and transparent processes.

**Success Metric**: If a researcher says "This feels like working with a really smart colleague," you've succeeded.

## Development Workflow

1. **🧪 Test First**: Run `python3 discernus/tests/quick_test.py`
2. **📖 Read Docs**: Understand the component you're working with
3. **🔍 Check Environment**: Use environment check utility if needed
4. **💻 Write Code**: Follow THIN principles and framework-agnostic patterns
5. **✅ Test Changes**: Run simple working tests to validate
6. **🔄 Iterate**: Refine based on test feedback
7. **📝 Document**: Update relevant documentation

**Never skip testing** - it's the fastest way to catch issues and ensure your changes work correctly.

---

*This briefing contains the essential DNA of the project. Read it first, reference it often, and when in doubt, choose the approach that amplifies human intelligence rather than replacing it.* 