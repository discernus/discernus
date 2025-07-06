# 🤖 NEW CURSOR AGENT QUICK START

> **Memory-efficient orientation for new agents. Read this FIRST.**

## **🎯 What is Discernus?**
Academic research platform using **THIN architecture**: LLMs provide intelligence, software provides minimal infrastructure. Agents talk to each other, software just routes messages.

## **⚡ THIN Architecture (30-second version)**

**✅ DO THIS:**
- Add expert agents to `discernus/core/llm_roles.py` → `EXPERT_AGENT_PROMPTS`
- Pass raw text between LLMs (no parsing!)
- Use `get_expert_prompt()` function
- Add libraries to extension YAML files

**❌ DON'T DO THIS:**
- Parse JSON from LLM responses (`json.loads(response)`)
- Add hardcoded prompts in orchestrator  
- Complex if/else logic on LLM responses
- Intelligence decisions in Python code

## **📁 Key File Locations**

```
discernus/
├── core/
│   ├── llm_roles.py           ← ADD NEW EXPERT AGENTS HERE
│   ├── secure_code_executor.py ← Code execution infrastructure  
│   ├── capability_registry.py  ← Extension system
│   └── orchestrator.py         ← Multi-LLM orchestration
├── extensions/                 ← ADD NEW TOOLS/LIBRARIES HERE
└── docs/
    ├── EXTENSION_GUIDE.md      ← How to add your favorite tools
    └── GLOSSARY.md             ← Terminology reference
```

## **🚀 Common Tasks (Copy-Paste Ready)**

### **Add New Expert Agent**
```python
# In discernus/core/llm_roles.py, add to EXPERT_AGENT_PROMPTS:
'my_expert_agent': """You are a my_expert_agent specializing in [YOUR DOMAIN].

RESEARCH QUESTION: {research_question}
SOURCE TEXTS: {source_texts}
EXPERT REQUEST: {expert_request}

Your Task: [Specific instructions for this expert]
If you need calculations, write Python code in ```python blocks.
"""
```

### **Add New Libraries/Tools**
```yaml
# Create extensions/my_tools.yaml:
name: my_research_tools
libraries:
  - spacy>=3.4.0
  - transformers
agents:
  my_expert:
    prompt: |
      You are an expert with access to spaCy and transformers...
```

### **Test Your Changes**
```python
# Validate THIN compliance
from discernus.core.thin_validation import check_thin_compliance
check_thin_compliance()

# Test extension
from discernus.core.capability_registry import CapabilityRegistry
registry = CapabilityRegistry()
issues = registry.validate_extension("extensions/my_tools.yaml")
```

## **🔍 How System Works (1 minute)**

1. **User** asks research question
2. **Design LLM** proposes methodology  
3. **Human** approves/rejects design
4. **Moderator LLM** orchestrates analysis using expert agents
5. **Expert Agents** provide specialized analysis (you add these!)
6. **Code Execution** happens automatically in secure sandbox
7. **Results** logged to git with full provenance

## **🛠️ Emergency Commands**

```bash
# Quick test
python3 discernus/tests/simple_test.py

# Run development test
python3 discernus/dev_tools/dev_test_runner.py

# Start web interface  
python3 discernus/web/app.py

# Validate THIN compliance
python3 -c "from discernus.core.thin_validation import check_thin_compliance; check_thin_compliance()"
```

## **📚 Need More Detail?**

- **🔧 Add tools**: `docs/EXTENSION_GUIDE.md`
- **🏗️ Architecture**: `README.md` (THIN guide section)
- **📖 Terminology**: `docs/GLOSSARY.md`  
- **🚀 Deployment**: `docs/DEPLOYMENT_COLLABORATION_GUIDE.md`

## **💡 Pro Tips**

1. **Before reading big files**: Use `codebase_search` to find specific functionality
2. **Adding complexity?** Ask: "Could an LLM do this instead of Python?"
3. **Parsing LLM responses?** You're probably doing it wrong (THIN violation)
4. **Need help?** Check existing expert agents in `llm_roles.py` for patterns

---

**🎯 Goal: Get productive in 5 minutes, not 5 hours. Welcome to THIN development!** 