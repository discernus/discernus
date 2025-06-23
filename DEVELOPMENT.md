# Development Guide

## 🚨 **START HERE: MANDATORY AI ASSISTANT RULES**

**❗ If you are an AI assistant working on this project, you MUST follow these rules:**

```bash
# BEFORE suggesting ANY development work:
python3 scripts/applications/check_existing_systems.py "what you want to build"
```

**📚 REQUIRED READING:**
- `.ai_assistant_rules.md` - **MANDATORY** rules for AI assistants
- `docs/EXISTING_SYSTEMS_INVENTORY.md` - What already exists
- `docs/CODE_ORGANIZATION_STANDARDS.md` - Where things belong

---

## 🏗️ **Development Environment**

### **🖥️ Recommended: Local Development (Active Development Phase)**

**Why Local Development Now:**
- ⚡ Faster iteration cycles during refactoring
- 🔍 Easier debugging and IDE integration
- 📁 Direct file system access (no sync issues)
- 🧪 Simplified testing workflow

**Setup:**
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up local environment
cp env.example .env
# Edit .env with local database settings

# 4. Run tests
python3 -m pytest tests/unit/ -v
```

### **🐳 Docker (CI/CD and Final Validation)**

**When to Use Docker:**
- ✅ Final integration testing before commits
- ✅ Production deployment simulation
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Environment consistency validation

**Quick Docker Validation:**
```bash
# Validate your changes work in Docker before committing
docker-compose up -d
docker-compose run --rm app python3 -m pytest tests/unit/ -v
docker-compose down
```

---

## 🔄 **Development Workflow**

### **For AI Assistants:**
1. **Search First**: `python3 scripts/applications/check_existing_systems.py "functionality"`
2. **Enhance Don't Replace**: Use existing production systems when possible
3. **Build in Experimental**: New code goes in `experimental/` first
4. **Test Locally**: `python3 -m pytest tests/unit/ -v`
5. **Validate in Docker**: Quick Docker validation before commits

### **For Human Developers:**
1. **Search First**: Check existing systems before building
2. **Follow Guided Workflow**: `python3 scripts/production/new_development_workflow.py`
3. **Build in Experimental**: Prototype in `experimental/` first
4. **Test Locally**: Fast local testing during development
5. **Docker Validation**: Final validation in containerized environment

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

## 🗄️ **Database Configuration**

### **Local Development:**
```bash
# Option 1: Local PostgreSQL
brew install postgresql  # macOS
sudo apt-get install postgresql  # Ubuntu
# Update .env: DATABASE_URL=postgresql://postgres:password@localhost:5432/discernus

# Option 2: SQLite (for simple testing)
# Update .env: DATABASE_URL=sqlite:///discernus.db
```

### **Docker (Final Validation):**
```bash
# Uses Docker Compose managed PostgreSQL
docker-compose up -d db  # Start just the database
# App connects to Docker-managed database
```

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
- ✅ Fast local testing during development
- ✅ Docker validation before commits
- ✅ Followed clean code organization standards
- ✅ Never referenced deprecated code

---

## 🔄 **Path to Full Containerization**

**This hybrid approach maintains containerization readiness:**
- 📋 All dependencies tracked in `requirements.txt`
- 🔧 Docker files maintained and tested
- 🧪 Regular Docker validation prevents drift
- 📦 Easy transition back to Docker-first when stability increases

**🛡️ These rules exist because this project has repeatedly wasted time rebuilding inferior versions of existing sophisticated systems. Following these rules prevents that waste.** 