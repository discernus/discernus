# Narrative Gravity Wells - AI Assistant Context Guide
**Created:** 2025-01-11 | **Last Updated:** 2025-01-11
**Purpose:** Provide complete context for AI assistants working on this project

---

## 🎯 **Project Overview**

### **What This Is**
The Narrative Gravity Wells project is a **research workbench for systematic narrative analysis** - NOT a simple text analysis tool. It's designed to support academic research into computational narrative analysis with rigorous experimental methodology.

### **Current Status (v2.1)**
- ✅ **Frontend**: Complete React research workbench (100%)
- ✅ **Database**: PostgreSQL with full v2.1 schema (100%)  
- ✅ **API Infrastructure**: FastAPI with all endpoints (100%)
- ❌ **Analysis Engine**: **FAKE DATA ONLY** - Returns random numbers (0%)

**CRITICAL ISSUE:** The analysis endpoint `/api/analyze/single-text` returns completely fake/random data instead of real LLM analysis. This is the **primary blocker** for a functional system.

---

## 🧪 **Research Dashboard Objectives**

This is NOT a simple text analyzer. The v2.1 Research Workbench is designed for:

### **1. Unified Experiment Design**
- **Hypothesis-driven research**: Combines prompt templates + framework configs + scoring algorithms as single testable hypotheses
- **Experiment versioning**: Complete provenance tracking (prompt hash, framework version, scoring algorithm, LLM model, timestamp)
- **Comparative analysis**: Side-by-side comparison of up to 4 experimental conditions
- **Replication packages**: Complete experimental context for reproducible research

### **2. Advanced Analysis Capabilities**
- **Hierarchical prompts**: Require LLMs to rank top 2-3 driving wells with relative weights
- **Nonlinear scoring**: Winner-Take-Most, Exponential Weighting, Hierarchical Dominance algorithms
- **Multi-model comparison**: Claude, GPT-4 stability assessment with statistical metrics
- **Framework fit detection**: Flag narratives that don't map well to current wells
- **Evidence extraction**: Real quotes from text with confidence scoring

### **3. Research-Grade Infrastructure**
- **Complete lineage tracking**: How prompt/scoring changes evolved together over time
- **Fork/rollback capability**: Build on successful experimental conditions
- **Research notes**: Link insights to specific experiments and outcomes
- **Statistical validation**: Significance tests, hierarchy sharpness metrics, model agreement

---

## 🏗️ **Technical Architecture**

### **Working Components (Already Built)**
1. **`DirectAPIClient`** - Full LLM integration (OpenAI, Anthropic, Mistral, Google AI)
2. **`PromptTemplateManager`** - Sophisticated prompt generation system
3. **`NarrativeGravityWellsElliptical`** - Complete visualization and analysis engine
4. **`FrameworkManager`** - Multi-framework support system
5. **Legacy Streamlit app** - Working end-to-end reference implementation

### **The Disconnect**
The new FastAPI backend ignores these working components and generates fake data instead of using the sophisticated analysis system that already exists.

### **Key Files & Directories**
```
src/narrative_gravity/
├── api_clients/direct_api_client.py     # LLM integration (OpenAI, Claude, etc.)
├── prompts/template_manager.py          # Sophisticated prompt generation
├── engine.py                           # Analysis & visualization engine
├── framework_manager.py                # Multi-framework support
└── api/main.py                         # FastAPI endpoints (NEEDS INTEGRATION)

frontend/src/
├── components/ExperimentDesigner.tsx    # Main research interface
├── services/apiClient.ts               # Frontend API communication
└── store/experimentStore.ts            # State management

frameworks/                             # Framework definitions (civic_virtue, etc.)
corpus/                                # Text datasets for research
tests/e2e/complete-end-to-end.spec.ts  # Playwright automation
```

---

## 👤 **User Profile & Approach**

### **User Background**
- **Not a developer** - Retired software CMO with 30 years experience
- **Product management & marketing** background (SaaS products, dev tools)
- **"Coding adjacent"** - Strong product sense, relies on AI for implementation
- **Roles**: Product Owner (primary), sometimes Architect and Hygienist

### **Working Style**
- **AI should "lean in more than usual"** on technical decisions
- **Playwright testing available** - AI can iterate code → test → refine independently
- **Check at important decision points** - Don't need approval for implementation details
- **Focus on product outcomes** rather than technical process

---

## 🎯 **Current Priority: Analysis Engine Integration**

### **The Task**
Replace the fake analysis endpoint with real LLM integration using existing working components.

**NOT building from scratch** - connecting existing sophisticated system to new API.

### **Integration Points**
1. **Replace fake endpoint** in `src/narrative_gravity/api/main.py` 
2. **Use `DirectAPIClient`** for real LLM calls
3. **Use `PromptTemplateManager`** for sophisticated prompts  
4. **Return rich data** expected by research workbench frontend
5. **Preserve all functionality** from working legacy system

### **Expected Results**
- **Real LLM analysis** instead of random numbers
- **Hierarchical rankings** with relative weights from LLM responses
- **Actual evidence quotes** extracted from analyzed text
- **Framework fit scores** indicating narrative-well alignment
- **Timing and cost tracking** for research cost management

---

## 🧪 **Testing Infrastructure**

### **Automated Testing Available**
- **Playwright end-to-end**: `tests/e2e/complete-end-to-end.spec.ts`
  - Can validate full user workflows automatically
  - Frontend → API → Database → Results display
- **Unit tests**: Backend component testing
- **Integration tests**: API endpoint validation

### **Services & Commands**
```bash
# Database check
python check_database.py

# Start services individually  
python launch.py --api-only        # Backend (port 8000)
cd frontend && npm run dev          # Frontend (port 3000)

# Run tests
npx playwright test                 # End-to-end automation
pytest tests/                      # Backend unit tests

# Full system (when integration complete)
python launch.py
```

---

## 📋 **Key Project Rules** 

### **Database Architecture**
- **PRIMARY**: PostgreSQL (`postgresql://postgres:postgres@localhost:5432/narrative_gravity`)
- **NEVER assume SQLite** for main app data
- **SQLite only for**: Unit tests (`:memory:`) and logging fallback

### **Code Standards**
- **Follow .cursorrules** for project organization
- **Update CHANGELOG.md** for all significant changes
- **Validate through testing** before declaring completion
- **Use proper import patterns** (see .cursorrules)

### **Quality Gates**
**NEVER declare victory until validated through:**
- ✅ Automated unit tests (individual functions)
- ✅ Integration tests (API endpoints)  
- ✅ Playwright end-to-end tests (full workflows)
- ✅ Manual verification (complete scenarios)

---

## 🚀 **Next Steps Roadmap**

### **Phase 1: Analysis Engine Integration (Current)**
1. **Connect existing LLM clients** to FastAPI endpoint
2. **Implement real prompt generation** using TemplateManager
3. **Return rich analysis data** expected by frontend
4. **Validate through Playwright testing**

### **Phase 2: Research Workbench Enhancement**
1. **Multi-model comparison** infrastructure
2. **Advanced scoring algorithms** (Winner-Take-Most, etc.)
3. **Experiment versioning** and lineage tracking
4. **Statistical validation** tools

### **Phase 3: Academic Publication Preparation**
1. **Human-machine alignment** validation studies
2. **Documentation and transparency** improvements
3. **Replication packages** for academic credibility

---

## 📚 **Reference Documents**

### **Planning & Context**
- `docs/development/planning/2.1/` - Complete v2.1 workstream documentation
- `CHANGELOG.md` - Project evolution and current status
- `.cursorrules` - Project organization and coding standards

### **Architecture**
- `docs/architecture/database_architecture.md` - Database design
- `LAUNCH_GUIDE.md` - Service startup procedures
- `PROJECT_STRUCTURE.md` - File organization

### **For New Conversations**
**Show this file** (`docs/development/CONVERSATION_CONTEXT_GUIDE.md`) to any new AI assistant to provide complete context without manual explanation.

---

## 🎯 **Key Success Metrics**

- ✅ **Real analysis results** replace fake random data
- ✅ **End-to-end workflow** validated through Playwright
- ✅ **Research workbench** functional for experimental design
- ✅ **Systematic comparative analysis** capabilities working
- ✅ **Complete provenance tracking** for reproducible research

**The goal is a functional research infrastructure for systematic narrative analysis research, not just a text analysis demo.** 