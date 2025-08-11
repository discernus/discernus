# Cursor Agent Discipline Guide
## Maintaining Architectural Compliance in AI-Assisted Development

### **Quick Compliance Checklist for Cursor Agents**

Before any code changes, agents must verify:

#### **🎯 THIN Architecture Compliance**
- [ ] **Component Size**: Follow tiered limits - Simple agents <200 lines, Core agents <400 lines, Complex agents <600 lines, Orchestration <800 lines
- [ ] **YAML Externalization**: All prompts in separate .yaml files (not inline)
- [ ] **Minimal Parsing**: Trust LLM output, avoid complex JSON/text parsing
- [ ] **Intelligence Externalization**: LLMs handle reasoning, code handles orchestration

#### **📋 Specification Integrity**
- [ ] **Framework Agnostic**: No hardcoded assumptions about specific frameworks
- [ ] **Specification Compliance**: Changes extend specs, don't break existing contracts
- [ ] **Backward Compatibility**: Existing experiments/frameworks remain functional

#### **🔍 Academic Integrity**
- [ ] **Computational Verification**: All statistics computed via code execution
- [ ] **Provenance Preservation**: Complete audit trails from source to conclusion
- [ ] **No Hallucinated Math**: LLMs prohibited from mathematical calculations
- [ ] **Evidence Linking**: Every claim linked to supporting textual evidence

#### **🏗️ Infrastructure Patterns**
- [ ] **Universal Dependencies**: LLMGateway, ModelRegistry, AuditLogger integration
- [ ] **LocalArtifactStorage**: Content-addressable storage for all artifacts
- [ ] **Multi-Model Support**: Configurable models, no provider lock-in
- [ ] **Error Handling**: Comprehensive error reporting and recovery

### **Pre-Commit Agent Workflow**

#### **Step 1: Architecture Review**
```bash
# Agent must verify before any changes:
make check                    # Environment compliance
python3 scripts/thin_compliance_check.py  # THIN pattern validation (MANDATORY)
python3 -m pytest tests/     # Test suite passes

# CURRENT STATUS: 35 VIOLATIONS DETECTED (Fixed false positives!)
# TARGET: Reduce to <20 violations, never increase them

# AUTOMATED ENFORCEMENT: Install pre-commit hook to prevent violations
scripts/install_git_hooks.sh  # One-time setup for automatic THIN checking
```

#### **Step 1.5: THIN Pre-Check (NEW - MANDATORY)**
Before writing ANY parsing, validation, or "smart" logic:
```bash
# Run the THIN discipline checkpoint:
python3 scripts/thin_precheck.py

# This will ask the critical questions that prevent THICK patterns:
# 1. Could an LLM do this better than regex/parsing logic?
# 2. Do we have a pattern for this in ExperimentCoherenceAgent?  
# 3. Am I writing >10 lines of transformation/cleaning code?
# 4. Is this parsing/validating/reformatting LLM output?
# 5. Am I creating multi-strategy fallback systems?

# RULE: If ANY answer is YES -> Use LLM intelligence, not software logic
```

#### **Step 2: Specification Validation**
```bash
# For any specification changes:
python3 -m discernus.core.experiment_coherence_agent validate --all
# Ensures backward compatibility
```

#### **Step 3: Academic Integrity Check**
```bash
# For synthesis/analysis changes:
python3 -m discernus.core.math_toolkit verify_provenance
# Ensures no hallucinated statistics
```

### **Agent Behavioral Guidelines**

#### **🚫 Forbidden Patterns (Auto-Reject)**
1. **Intelligence Creep**: Components >150 lines
2. **Inline Prompts**: LLM prompts embedded in Python code
3. **Complex Parsing**: Multi-step JSON/text extraction logic
4. **Framework Hardcoding**: Specific framework assumptions in orchestration
5. **LLM Math**: Mathematical calculations performed by language models
6. **Database Dependencies**: Centralized storage requirements

#### **🚨 ANTI-PATTERNS WE KEEP REPEATING (HIGH ALERT)**
**Pattern**: Problem → Complex Software Solution → Realize THIN Violation → Revert to LLM

**Examples of What NOT to Do:**
- ❌ **Multi-Strategy JSON Parsing**: `try regex → try escape fixing → try markdown extraction → try brace counting`
- ❌ **Complex Validation Logic**: Writing parsers to validate LLM output instead of asking LLM to reformat
- ❌ **Brittle Text Processing**: Regex-based cleaning of LLM responses
- ❌ **Fallback Chains**: Multiple parsing strategies with complex error handling

**What to Do Instead:**
- ✅ **Simple Parse + LLM Reformat**: `json.loads()` → if fails, ask LLM to fix it
- ✅ **Follow ExperimentCoherenceAgent Pattern**: `_request_llm_reformat()` method
- ✅ **Trust LLM Intelligence**: LLMs understand JSON/text structure better than regex
- ✅ **Single Responsibility**: One parsing attempt, delegate complexity to LLM

#### **✅ Encouraged Patterns (Auto-Approve)**
1. **YAML Externalization**: Prompts in separate configuration files
2. **LLM Envelope Extraction**: Simple delimiter-based output extraction
3. **Specification Extensions**: New capabilities through spec files
4. **MathToolkit Integration**: Verified mathematical operations
5. **Comprehensive RAG**: Knowledge graph utilization
6. **Audit Logging**: Complete provenance tracking

### **Self-Review Protocol for Agents**

Before proposing changes, agents should ask:

1. **"Does this maintain THIN principles?"**
   - Is the LLM doing the thinking and the code doing minimal coordination?
   - Are prompts externalized to YAML files?
   - Is parsing logic minimal and necessary?

2. **"Does this preserve academic integrity?"**
   - Are all statistics computed via secure code execution?
   - Is the provenance chain intact from source to conclusion?
   - Can this work be peer-reviewed and replicated?

3. **"Does this maintain framework agnosticism?"**
   - Will this work with any compliant framework specification?
   - Are we extending capabilities rather than hardcoding assumptions?
   - Can researchers use their own analytical approaches?

4. **"Does this follow established patterns?"**
   - Are we using standard infrastructure (LLMGateway, AuditLogger)?
   - Are we following the agent architecture documented in the system architecture?
   - Are we maintaining backward compatibility?

### **Escalation Triggers**

Agents should request human review for:

- **Architectural Principle Changes**: Any modification to the 26 universal principles
- **Specification Contract Changes**: Breaking changes to Framework/Experiment/Corpus specs
- **Core Pipeline Modifications**: Changes to the 3-stage synthesis architecture
- **New Agent Creation**: Addition of specialized agents to the ecosystem
- **Performance Impact**: Changes affecting scalability or cost characteristics
- **Academic Standards**: Modifications to statistical verification or provenance systems

### **Quick Reference: THIN Patterns**

#### **JSON Parsing (THIN Way)**
```python
# ✅ THIN-Compliant Pattern (from ExperimentCoherenceAgent)
def _parse_response_thin(self, response: str) -> Dict[str, Any]:
    try:
        return json.loads(response)  # Simple attempt first
    except json.JSONDecodeError:
        # Ask LLM to fix instead of complex parsing
        return self._request_llm_reformat(response)

def _request_llm_reformat(self, malformed: str) -> Dict[str, Any]:
    prompt = f"Fix this JSON: {malformed}"
    fixed_response, _ = self.llm_gateway.execute_call(model, prompt)
    return json.loads(fixed_response)
```

#### **Validation (THIN Way)**
```python
# ✅ THIN-Compliant: Let LLM validate instead of writing rules
def validate_thin(self, data: str) -> ValidationResult:
    prompt = f"Validate this data against schema: {data}"
    result, _ = self.llm_gateway.execute_call(model, prompt)
    return self._parse_response_thin(result)
```

### **Quick Reference: Architecture Document Sections**

- **Universal Principles**: Lines 58-765 in `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Agent Architecture**: Lines 361-591 (comprehensive agent catalog and compliance status)
- **Developer Guidelines**: Lines 768-831 (contribution principles and standards)
- **THIN Compliance Template**: Lines 540-565 (reference implementation pattern)
- **ExperimentCoherenceAgent**: Reference implementation for LLM-based parsing/validation

### **Emergency Contacts**

For architectural questions that can't be resolved through documentation:
- **GitHub Issues**: Create issue with `architecture` label
- **Documentation**: Reference system architecture document first
- **Precedent**: Check existing compliant agents for patterns

---

**Remember**: The goal is maintaining architectural integrity while enabling rapid development. When in doubt, favor THIN principles over convenience, academic integrity over speed, and specification compliance over shortcuts.
