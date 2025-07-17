# 📋 THIN Compliance Checklist

## Before You Code: Quick Check

### 🎯 Purpose Check
- [ ] **Human Intelligence Amplifier**: Does this amplify human judgment or replace it?
- [ ] **Domain Neutral**: Will this work for political science, corporate communications, religious studies, etc.?
- [ ] **Research Assistant Feel**: Would this make a researcher feel like they're collaborating with a brilliant colleague?

### 🏗️ Architecture Check

#### ✅ THIN Patterns (Good)
- [ ] **LLM Intelligence**: Complex reasoning and analysis done by LLMs
- [ ] **Software Infrastructure**: Code handles routing, execution, storage only
- [ ] **Natural Language Flow**: LLMs communicate in natural language
- [ ] **Centralized Prompts**: Prompts in `discernus/core/agent_roles.py`
- [ ] **Secure Math**: Mathematical operations use `SecureCodeExecutor`
- [ ] **Registry-Based**: Uses agent registry and model registry

#### 🚫 THICK Anti-Patterns (Bad)
- [ ] **No JSON Parsing**: Not parsing structured data from LLM responses
- [ ] **No Hardcoded Prompts**: Prompts not embedded in orchestrator code
- [ ] **No Software Intelligence**: No if/else logic based on LLM responses
- [ ] **No Math in Software**: No calculations in Python (use LLM + SecureCodeExecutor)
- [ ] **No Framework Lock-in**: No hardcoded framework-specific logic

### 🔧 Implementation Check

#### Code Quality
- [ ] **Minimal Code**: Could this be simpler? Could an LLM do it better?
- [ ] **Clear Separation**: Intelligence vs. infrastructure clearly separated
- [ ] **Registry Usage**: Uses agent registry for discovery, model registry for selection
- [ ] **Error Handling**: Graceful fallbacks without complex logic

#### Integration
- [ ] **Agent Registry**: New agents defined in `agent_registry.yaml`
- [ ] **Model Registry**: Model selection uses registry, not hardcoded names
- [ ] **LLM Gateway**: LLM calls go through gateway with provider abstraction
- [ ] **Project Chronolog**: Actions logged for academic provenance

### 📊 Quality Check

#### User Experience
- [ ] **Conversational**: Feels like natural collaboration
- [ ] **Transparent**: User can see what's happening
- [ ] **Controllable**: Human maintains agency and oversight
- [ ] **Explainable**: Decisions and processes are clear

#### Academic Standards
- [ ] **Reproducible**: Complete audit trail available
- [ ] **Provenance**: Full chronolog of decisions and actions
- [ ] **Fallback Safe**: Graceful degradation when things fail
- [ ] **Cost Transparent**: Resource usage visible and controlled

## 🚨 Red Flags (Stop and Reconsider)

### Immediate Red Flags
- **Parsing JSON from LLM responses** → Use natural language instead
- **Hardcoded prompts in orchestrator** → Move to `agent_roles.py`
- **Complex if/else on LLM output** → Let LLM make decisions
- **Mathematical operations in code** → Use LLM + SecureCodeExecutor
- **Framework-specific hardcoding** → Make it domain-neutral

### Subtle Red Flags
- **"Helper functions" for LLM responses** → Probably parsing in disguise
- **Complex orchestrator logic** → Should be simple message routing
- **Domain-specific assumptions** → Should work for any text analysis
- **Brittle error handling** → Should gracefully degrade
- **Limited extensibility** → Should support unknown future needs

## 🎯 Success Patterns

### What Good THIN Code Looks Like
- **Agent spawning** via registry with dynamic prompts
- **Model selection** via registry with intelligent fallbacks
- **Natural language** communication between components
- **Secure execution** for mathematical reliability
- **Complete logging** for academic transparency

### What Good THIN Architecture Feels Like
- **Researchers feel empowered**, not constrained
- **System feels conversational**, not transactional
- **Complexity handled by LLMs**, not code
- **Extensibility through configuration**, not coding
- **Quality through transparency**, not black boxes

---

## Quick Self-Assessment

**Score yourself**: How many ✅ patterns vs 🚫 anti-patterns?

- **90%+ THIN**: You're following the philosophy well
- **70-90% THIN**: Good direction, consider refactoring some areas
- **<70% THIN**: Significant rework needed - consult `AGENT_BRIEFING.md`

**When in doubt**: Choose the approach that amplifies human intelligence rather than replacing it. 