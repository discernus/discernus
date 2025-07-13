# HANDOFF CONTEXT: Attesor Study Ensemble Infrastructure
## Session Summary: Ensemble Constraint Solving & Documentation Architecture

### 🎯 **Core Achievement: THIN Ensemble Design Philosophy**

**Key Insight**: Instead of building complex programmatic constraint solvers, use **LLM intelligence** to evaluate ensemble requirements and provide feasible alternatives.

**THIN Approach Established**:
- Simple YAML model registry (context windows, costs, TPM limits)
- LLM-based constraint solving: feed requirements → get feasible ensemble design
- Avoided THICK infrastructure violation: deleted complex `model_registry.py` (270+ lines)

### 📊 **Attesor Study Technical Requirements**

**Scale**: 864 total analyses (8 speeches × 6 agents × 6 LLMs × 3 corpus sets)
**Models**: 6 LLMs spanning cheap (Gemini Flash, Claude Haiku) to premium (GPT-4o, Claude Sonnet, Gemini Pro, Mistral Large)
**Constraint**: Multi-model IRR and Cronbach's alpha requires identical batch processing
**Bottleneck**: GPT-4o limits ensemble to 7 speeches per batch (with 25K token framework)

### 🏗️ **Infrastructure Completed**

#### 1. **Validation Rubric Enhancement** ✅
- **File**: `docs/experiment_specification_validation_rubric.md`
- **Added**: Ensemble specification requirements to Analysis Plan section
- **Features**: Model selection criteria, budget constraints, statistical requirements, performance requirements
- **Integration**: Added to YAML experiment template with ensemble_requirements section

#### 2. **Documentation Architecture** ✅
- **Moved**: Both validation rubrics from `pm/` to `docs/` directory
- **Updated**: All references across codebase (3 files updated)
- **Cleaned**: Removed THICK model registry infrastructure

#### 3. **SOAR v2.0 Enhancement** ✅
- **File**: `pm/soar/soar_v2/Simple Atomic Orchestrated Research (SOAR) v2.0.md`
- **Added**: Ensemble specification guidance with examples
- **Approach**: Descriptive requirements → LLM constraint solving → feasible alternatives

### 📋 **Critical Next Steps (From TODO Backlog)**

#### **Priority 1: Streamlined Orchestrator Design** (in_progress)
- **Task**: `design_streamlined_orchestrator`
- **Goal**: Remove synthesis/adversarial components, focus on raw score collection
- **Requirements**: Simple agent → LLM → score extraction pipeline
- **Blocks**: All other implementation tasks depend on this

#### **Priority 2: Multi-LLM Support Implementation** (pending)
- **Task**: `implement_multi_llm_support`
- **Models**: 6 LLMs (2 cheaper + 4 premium) with cost tracking
- **Dependency**: Requires streamlined orchestrator design
- **Challenge**: TPM limit coordination across models

#### **Priority 3: Corpus Management System** (pending)
- **Task**: `create_corpus_management`
- **Requirements**: 3 corpus sets (original, sanitized English, Esperanto)
- **Features**: File mapping, hash-based identity protection
- **Integration**: Must work with batch processing constraints

### 🔧 **Technical Specifications Established**

#### **Batch Size Calculator Logic**:
```python
# Constraint-based batch sizing
min_batch_size = min(model.max_speeches_per_batch for model in ensemble)
batch_count = ceil(total_speeches / min_batch_size)
```

#### **Context Window Math**:
- **Framework**: 25K tokens (PDAF v1.1 optimized)
- **Average Speech**: 12K tokens
- **GPT-4o**: 128K context → 7 speeches max per batch
- **Result**: 8 speeches require 2 batches (7 + 1)

### 🎨 **Architecture Decisions Made**

#### **THIN Constraint Solving**:
```python
def design_ensemble(experiment_yaml: str) -> str:
    models_info = load_yaml("config/models.yaml")
    prompt = f"""
    Available models: {models_info}
    Experiment requirements: {experiment_yaml}
    Design optimal ensemble or explain constraints.
    """
    return llm.complete(prompt)
```

#### **Sequential Feed Optimization** (User Proposed):
- **Concept**: Prime agents with framework once, then feed texts sequentially
- **Benefit**: ~99.3% reduction in framework loading tokens
- **Implementation**: Requires conversation state management and TPM coordination

### 🚨 **Known Challenges & Considerations**

#### **1. Context Window Degradation**
- **Research**: Found studies showing LLM performance degradation in long contexts
- **Reality**: Modern models (Gemini 2.5 Pro 1M, GPT-4o 128K) maintain performance
- **Decision**: Use recent model capabilities, ignore outdated 32K thresholds

#### **2. Agent Isolation vs. Shared Context**
- **Question**: Should each agent have separate Redis pubsub or shared chronolog?
- **Concern**: Cross-contamination in multi-agent analysis
- **Status**: Needs literature review and architectural decision

#### **3. Conversation State Management**
- **Opportunity**: Sequential text feeding with maintained agent state
- **Challenge**: TPM limit coordination across multiple running agents
- **Analogy**: Internal combustion engine with timing coordination

### 📚 **Key Files & Locations**

- **Experiment Validation**: `docs/experiment_specification_validation_rubric.md`
- **Framework Validation**: `docs/framework_specification_validation_rubric.md`
- **SOAR v2.0 Spec**: `pm/soar/soar_v2/Simple Atomic Orchestrated Research (SOAR) v2.0.md`
- **Attesor Study**: `pm/attesor_study_strategic_overview.md`
- **PDAF Framework**: `projects/attesor/` directory

### 🎯 **Recommended Next Actions**

1. **Complete Streamlined Orchestrator Design** (blocks everything else)
2. **Implement Simple Model Registry** (YAML-based, not programmatic)
3. **Build Batch Processing Logic** (constraint-based batch sizing)
4. **Create Cost Forecasting** (864 analyses cost estimation)
5. **Implement Wave Processing** (TPM-aware parallel execution)

### 💡 **Strategic Insights**

- **THIN Philosophy**: Let LLMs handle constraint solving intelligence
- **Constraint-Based Design**: Ensemble limited by weakest model
- **Statistical Validity**: IRR/Cronbach's alpha requires identical batch processing
- **Cost Optimization**: Use cheaper models for validation, premium for production

### 🎯 **For Next Agent**

The foundation is solid. Focus on **streamlined orchestrator design** as Priority 1 - everything else depends on this architectural decision. The THIN approach is established, documentation is organized, and user requirements are clear. Build the simplest possible orchestrator that collects raw scores without synthesis complexity.

**Key Memory**: User prefers structured, framework-based planning with explicit sign-off before execution. Get approval on orchestrator design before building. 