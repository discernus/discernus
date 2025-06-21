# Research Guide: Complete Experimental Methodology

**The definitive guide for researchers conducting narrative gravity experiments**

*Last Updated: June 14, 2025*  
*Documentation Architecture: MECE (Mutually Exclusive, Collectively Exhaustive)*

---

## 🎯 **Quick Navigation by Research Phase**

### **🚀 Phase 1: Getting Started** → [`getting-started/`](getting-started/)
- **New to the platform?** → [`RESEARCH_ONBOARDING.md`](getting-started/RESEARCH_ONBOARDING.md)
- **Understanding the workflow?** → [`RESEARCH_WORKFLOW_OVERVIEW.md`](getting-started/RESEARCH_WORKFLOW_OVERVIEW.md)
- **Quality standards?** → [`RESEARCH_QUALITY_STANDARDS.md`](getting-started/RESEARCH_QUALITY_STANDARDS.md)

### **📋 Phase 2: Methodology Design** → [`methodology/`](methodology/)
- **Experimental design principles** → [`EXPERIMENTAL_DESIGN_FRAMEWORK.md`](methodology/EXPERIMENTAL_DESIGN_FRAMEWORK.md)
- **5-dimensional design space** → [`RESEARCH_METHODOLOGY_GUIDE.md`](methodology/RESEARCH_METHODOLOGY_GUIDE.md)
- **Component specifications** → [`FORMAL_SPECIFICATIONS.md`](methodology/FORMAL_SPECIFICATIONS.md)

### **🔧 Phase 3: Asset Development** → [`development-guides/`](development-guides/)
- **Framework development** → [`FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md`](development-guides/FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md)
- **Prompt template development** → [`PROMPT_TEMPLATE_DEVELOPMENT.md`](development-guides/PROMPT_TEMPLATE_DEVELOPMENT.md)
- **Weighting scheme development** → [`WEIGHTING_SCHEME_DEVELOPMENT.md`](development-guides/WEIGHTING_SCHEME_DEVELOPMENT.md)
- **Corpus management** → [`CORPUS_DEVELOPMENT_GUIDE.md`](development-guides/CORPUS_DEVELOPMENT_GUIDE.md)

### **⚡ Phase 4: Execution** → [`practical-guides/`](practical-guides/)
- **CLI experiment workflow** → [`CLI_EXPERIMENT_GUIDE.md`](practical-guides/CLI_EXPERIMENT_GUIDE.md)
- **Batch processing** → [`EXPERIMENT_EXECUTION_GUIDE.md`](practical-guides/EXPERIMENT_EXECUTION_GUIDE.md)
- **Quality assurance** → [`RESEARCH_QA_GUIDE.md`](practical-guides/RESEARCH_QA_GUIDE.md)

### **📊 Phase 5: Analysis & Publication** → [`academic-workflow/`](academic-workflow/)
- **Interactive analysis** → [`JUPYTER_ANALYSIS_GUIDE.md`](academic-workflow/JUPYTER_ANALYSIS_GUIDE.md)
- **Academic export** → [`ACADEMIC_PUBLICATION_GUIDE.md`](academic-workflow/ACADEMIC_PUBLICATION_GUIDE.md)
- **Validation studies** → [`VALIDATION_METHODOLOGY.md`](academic-workflow/VALIDATION_METHODOLOGY.md)

---

## 🏗️ **Complete Research Architecture**

### **Research Asset Components**
The platform supports systematic development of five core research asset types:

#### **1. Theoretical Frameworks** 🏛️
*Define the conceptual space for analysis*
- **Purpose**: Theoretical lenses (civic virtue, political spectrum, moral foundations)
- **Development**: [`FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md`](development-guides/FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md)
- **Current Status**: 5 operational frameworks with WCAG AA accessibility

#### **2. Prompt Templates** 📝
*Instruct evaluators how to perform analysis*
- **Purpose**: LLM analysis instructions (hierarchical, traditional, evidence-based)
- **Development**: [`PROMPT_TEMPLATE_DEVELOPMENT.md`](development-guides/PROMPT_TEMPLATE_DEVELOPMENT.md)
- **Current Status**: Formal specification system with validation pipeline

#### **3. Weighting Schemes** ⚖️
*Mathematical interpretation of analysis results*
- **Purpose**: Score aggregation algorithms (winner-take-most, linear, hierarchical)
- **Development**: [`WEIGHTING_SCHEME_DEVELOPMENT.md`](development-guides/WEIGHTING_SCHEME_DEVELOPMENT.md)
- **Current Status**: Mathematical validation framework operational

#### **4. Evaluator Selection** 🤖👥
*Choose and validate analysis agents*
- **Purpose**: LLM vs human evaluator optimization
- **Development**: [`EVALUATOR_SELECTION_GUIDE.md`](development-guides/EVALUATOR_SELECTION_GUIDE.md)
- **Current Status**: Multi-model comparison framework

#### **5. Corpus Development** 📚
*Create and validate analysis datasets*
- **Purpose**: Text data preparation and quality assurance
- **Development**: [`CORPUS_DEVELOPMENT_GUIDE.md`](development-guides/CORPUS_DEVELOPMENT_GUIDE.md)
- **Current Status**: Intelligent ingestion with validation pipeline

### **Experimental Methodology**
The platform implements a **5-dimensional experimental design space**:

1. **TEXTS** - Content being analyzed
2. **FRAMEWORKS** - Theoretical lenses applied
3. **PROMPTS** - Analysis instructions
4. **WEIGHTING** - Mathematical interpretation
5. **EVALUATORS** - Analysis agents (LLM/human)

**Systematic Research Approach**: Each dimension represents independent methodological choices, enabling rigorous hypothesis testing about interaction effects and optimal configurations.

---

## 📚 **Documentation Organization Principles**

### **MECE Architecture**
This research guide follows **Mutually Exclusive, Collectively Exhaustive** principles:

- **Mutually Exclusive**: No overlap between sections - each doc has single, clear purpose
- **Collectively Exhaustive**: Complete coverage of research workflow - no gaps
- **Hierarchical Navigation**: Organized by research phase and asset type
- **Cross-Referenced Integration**: Clear links between related concepts

### **Audience Separation**
- **Research Guide** (this directory): Everything researchers need for experiments
- **Platform Development**: [`../platform-development/`](../platform-development/) - Software engineering
- **User Guides**: [`../user-guides/`](../user-guides/) - Practical how-to documentation
- **Academic Workflow**: [`../academic/`](../academic/) - Publication and validation

### **Quality Standards**
- **Academic Rigor**: All methodology grounded in research best practices
- **Reproducibility**: Complete documentation for independent replication
- **Accessibility**: WCAG AA compliance for all research outputs
- **Version Control**: Systematic tracking of all research asset evolution

---

## 🔄 **Integration with Platform Capabilities**

### **Operational Status** ✅
- **Framework System**: 5 frameworks operational with v2025.06.14 (WCAG AA compliant)
- **Experiment Engine**: Declarative JSON-based experiment execution system
- **Quality Assurance**: 6-layer validation system preventing invalid research data
- **Academic Pipeline**: Publication-ready output generation with confidence metadata
- **Database Architecture**: Production-ready PostgreSQL with complete versioning

### **Revolutionary Capabilities** 🚀
Following the June 13-14 breakthrough, the platform enables:
- **100% Success Rate**: Declarative experiment execution with meaningful results
- **Quality-Assured Research**: Automatic detection and prevention of analysis issues
- **Production Academic Output**: Publication-ready visualizations and data exports
- **Systematic Asset Development**: Complete lifecycle management for all research components

---

## 🎯 **How to Use This Guide**

### **For New Researchers**
1. **Start**: [`getting-started/RESEARCH_ONBOARDING.md`](getting-started/RESEARCH_ONBOARDING.md)
2. **Understand**: [`getting-started/RESEARCH_WORKFLOW_OVERVIEW.md`](getting-started/RESEARCH_WORKFLOW_OVERVIEW.md)
3. **Execute**: Follow phase-by-phase documentation through your first experiment

### **For Experienced Users**
- **Quick Reference**: Navigate directly to relevant sections using phase-based organization
- **Asset Development**: Use development guides for creating new research components
- **Advanced Methodology**: Leverage experimental design framework for complex studies

### **For Academic Publication**
- **Methodology Documentation**: Complete formal specifications for methods sections
- **Replication Materials**: All code, data, and procedures for independent validation
- **Quality Assurance**: Confidence metadata and validation reports for peer review

---

**This research guide provides everything needed to conduct world-class computational narrative analysis research with full academic rigor and reproducibility.**

*Maintained by: Narrative Gravity Research Team*  
*Next Review: After Phase 3 completion (community contribution guidelines)* 