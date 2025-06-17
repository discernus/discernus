# Development Guide

## 🚨 **START HERE: MANDATORY AI ASSISTANT RULES**

**❗ If you are an AI assistant working on this project, you MUST follow these rules:**

```bash
# BEFORE suggesting ANY development work:
python3 scripts/production/check_existing_systems.py "what you want to build"
```

**📚 REQUIRED READING:**
- `.ai_assistant_rules.md` - **MANDATORY** rules for AI assistants
- `docs/EXISTING_SYSTEMS_INVENTORY.md` - What already exists
- `docs/CODE_ORGANIZATION_STANDARDS.md` - Where things belong

---

## 🏗️ **Development Architecture**

### **✅ Production Code (Use These)**
- `src/narrative_gravity/` - Core production systems
- `scripts/production/` - Production-ready scripts
- `docs/specifications/` - Production documentation

### **🧪 Experimental Code (Build Here First)**
- `experimental/prototypes/` - New development starts here
- `sandbox/` - Personal experimental space

### **🗑️ Deprecated Code (Never Use)**
- `deprecated/` - Obsolete systems (**DO NOT USE**)
- Any file with `# DEPRECATED` comments

---

## 🔄 **Development Workflow**

### **For AI Assistants:**
1. **Search First**: `python3 scripts/production/check_existing_systems.py "functionality"`
2. **Enhance Don't Replace**: Use existing production systems when possible
3. **Build in Experimental**: New code goes in `experimental/` first
4. **Validate Compliance**: `python3 scripts/production/validate_ai_assistant_compliance.py`

### **For Human Developers:**
1. **Search First**: Check existing systems before building
2. **Follow Guided Workflow**: `python3 scripts/production/new_development_workflow.py`
3. **Build in Experimental**: Prototype in `experimental/` first
4. **Promote When Ready**: Move to production with quality checks

---

## 🛡️ **Quality Assurance**

### **Existing Production QA Systems (USE THESE):**
- `LLMQualityAssuranceSystem` - 6-layer mathematical validation
- `ComponentQualityValidator` - 15+ quality checks  
- `QAEnhancedDataExporter` - Academic export with QA

### **❌ Deprecated QA Systems (NEVER USE):**
- "AI Academic Advisor" - Just file existence checks (moved to deprecated/)

---

## 📊 **Key Production Systems**

### **Experiment Execution:**
- `scripts/production/execute_experiment_definition.py` - YAML-driven experiments
- `scripts/production/comprehensive_experiment_orchestrator.py` - Multi-phase orchestration

### **Data & Analysis:**
- `src/narrative_gravity/academic/data_export.py` - Academic data export
- `src/narrative_gravity/cli/academic_analysis_pipeline.py` - Complete workflow

### **Framework Management:**
- `src/narrative_gravity/framework_manager.py` - Framework loading/management

---

## 🚨 **Common AI Assistant Violations**

**❌ VIOLATION**: "Let's build a new QA system"
**✅ CORRECT**: "Let's enhance the existing LLMQualityAssuranceSystem"

**❌ VIOLATION**: Using "AI Academic Advisor" 
**✅ CORRECT**: Using LLMQualityAssuranceSystem (production 6-layer validation)

**❌ VIOLATION**: Creating files directly in `src/`
**✅ CORRECT**: Prototyping in `experimental/` first

**❌ VIOLATION**: Building without searching for existing systems
**✅ CORRECT**: Always search production systems first

---

## 🎯 **Success Metrics**

A successful development session:
- ✅ Searched production systems before building
- ✅ Enhanced existing systems when possible  
- ✅ Built new development in experimental/ first
- ✅ Followed clean code organization standards
- ✅ Never referenced deprecated code

---

**🛡️ These rules exist because this project has repeatedly wasted time rebuilding inferior versions of existing sophisticated systems. Following these rules prevents that waste.** 