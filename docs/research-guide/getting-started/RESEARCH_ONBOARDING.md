# Research Onboarding Guide

**Your journey from newcomer to productive narrative gravity researcher**

*Last Updated: June 14, 2025*  
*Estimated Completion Time: 2-4 hours*

---

## 🎯 **Welcome to Narrative Gravity Research**

This guide will take you from complete newcomer to running your first experiment. By the end, you'll understand the platform's capabilities, research methodology, and be ready to conduct systematic narrative analysis research.

### **What You'll Learn**
- **Platform Overview**: Revolutionary research capabilities and current status
- **Research Methodology**: 5-dimensional experimental design framework
- **Asset Development**: How to create and validate research components
- **Experiment Execution**: From design to analysis to publication
- **Quality Assurance**: Academic rigor and reproducibility standards

---

## 📋 **Prerequisites & Setup**

### **Required Background**
- **Basic Research Skills**: Understanding of experimental design and academic writing
- **Text Analysis Interest**: Working with political/literary/social texts
- **Technical Comfort**: Command-line interface (CLI) familiarity helpful but not required

### **Platform Setup**
```bash
# 1. Environment Setup (CRITICAL)
source scripts/setup_dev_env.sh

# 2. Verify Setup
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Setup complete!')"

# 3. Check Database Connection
python check_database.py

# 4. Explore Available Components
python src/narrative_gravity/cli/component_manager.py list
```

**🚨 IMPORTANT**: Always run `source scripts/setup_dev_env.sh` before any Python commands.

---

## 🏗️ **Platform Overview: Revolutionary Capabilities**

### **Current Operational Status** ✅ **June 2025**

Following the **June 13-14 revolutionary breakthrough**, the platform achieved:

#### **🎯 100% Operational Experiment System**
- **Declarative Experiments**: JSON-based experiment definitions with full execution
- **Quality Assurance**: 6-layer validation preventing invalid research data
- **Academic Output**: Publication-ready visualizations and data exports
- **Database Integration**: Production PostgreSQL with complete versioning

#### **🏛️ Research Asset Ecosystem**
- **5 Operational Frameworks**: All with WCAG AA accessibility compliance
- **Formal Specifications**: Complete prompt template and weighting scheme standards  
- **Component Versioning**: Systematic tracking of all research asset evolution
- **Quality Validation**: Automated testing and academic rigor enforcement

#### **📊 Academic Integration Pipeline**
- **Interactive Analysis**: Jupyter notebooks with advanced visualizations
- **Publication Export**: R, Stata, CSV formats with replication packages
- **Confidence Metadata**: Quality reporting and validation for peer review
- **Human Validation**: Protocols for LLM vs expert comparison studies

### **Research Methodology: 5-Dimensional Design Space**

The platform implements systematic experimental methodology where each dimension represents independent choices:

1. **TEXTS** - What content is analyzed (speeches, articles, social media)
2. **FRAMEWORKS** - What theoretical lens is applied (civic virtue, political spectrum)
3. **PROMPTS** - How evaluators are instructed (hierarchical, traditional, evidence-based)
4. **WEIGHTING** - How results are mathematically interpreted (linear, winner-take-most)
5. **EVALUATORS** - What agents perform analysis (GPT-4, Claude, human experts)

**Revolutionary Insight**: Systematic exploration of this 5D space enables rigorous hypothesis testing about optimal configurations for different research goals.

---

## 🔬 **Understanding Research Assets**

### **1. Theoretical Frameworks** 🏛️

**Purpose**: Define the conceptual space for narrative analysis

**Current Frameworks**:
- **civic_virtue**: Dignity/Truth/Justice dipoles for moral political analysis
- **political_spectrum**: Left-right political positioning with authority dimensions
- **fukuyama_identity**: Identity-based political analysis following Francis Fukuyama
- **mft_persuasive_force**: Moral foundations theory for persuasive communication
- **moral_rhetorical_posture**: Communication style and moral stance analysis

**Development Status**: All frameworks at v2025.06.14 with WCAG AA color accessibility

**Key Insight**: Frameworks are *theoretical lenses*, not analysis instructions. They define what conceptual space to analyze, not how to perform the analysis.

### **2. Prompt Templates** 📝

**Purpose**: Instruct evaluators (LLMs/humans) how to perform analysis

**Available Approaches**:
- **hierarchical_analysis**: Ranking-based with dominance detection
- **traditional_analysis**: Comprehensive dimensional scoring
- **evidence_based_analysis**: Citation-required justification focus

**Development Status**: Formal specification system with validation pipeline operational

**Key Insight**: Prompts are *analysis instructions*, framework-agnostic and optimized for specific response patterns.

### **3. Weighting Schemes** ⚖️

**Purpose**: Mathematical interpretation of analysis results

**Available Methods**:
- **hierarchical_weighted**: Primary/secondary/tertiary importance (45%/35%/20%)
- **linear_traditional**: Equal weight averaging across dimensions
- **winner_take_most**: Amplify dominant signals, suppress noise

**Development Status**: Mathematical validation framework with automated testing

**Key Insight**: Weighting is *mathematical interpretation*, determining how scores become meaningful visualizations.

### **4. Evaluator Selection** 🤖👥

**Purpose**: Choose and validate analysis agents

**Options**:
- **LLM Models**: GPT-4, Claude-3, Gemini-Pro with systematic comparison
- **Human Experts**: Trained evaluators with inter-rater reliability protocols
- **Hybrid Approaches**: Multi-model consensus with human validation

**Development Status**: Multi-model comparison framework operational

### **5. Corpus Development** 📚

**Purpose**: Create and validate analysis datasets

**Capabilities**:
- **Intelligent Ingestion**: YouTube transcripts, PDF processing, web scraping
- **Quality Validation**: Automated text quality assessment and cleaning
- **Golden Set Creation**: Curated, analysis-ready datasets with metadata

**Development Status**: Production pipeline with comprehensive quality assurance

---

## ⚡ **Your First Experiment Journey**

### **Phase 1: Exploration** (30 minutes)

#### **Step 1: Explore Available Components**
```bash
# See all available research assets
python src/narrative_gravity/cli/component_manager.py list

# Examine a specific framework
python src/narrative_gravity/cli/component_manager.py show framework "civic_virtue" "2.1.0"

# Check component compatibility
python src/narrative_gravity/cli/component_manager.py validate-compatibility \
    "hierarchical_analysis v2.1.0" \
    "civic_virtue v2.1.0" \
    "hierarchical_weighted v2.1.0"
```

#### **Step 2: Understand the Corpus**
```bash
# Explore available texts
ls corpus/golden_set/presidential_speeches/

# Check corpus quality
python src/narrative_gravity/cli/corpus_manager.py validate \
    "corpus/golden_set/presidential_speeches/"
```

### **Phase 2: First Experiment** (60 minutes)

#### **Step 3: Create Your First Experiment**
```bash
# Create experiment configuration
cat > my_first_experiment.yaml << 'EOF'
experiment:
  name: "Onboarding_Lincoln_Analysis"
  hypothesis: "Testing platform capabilities with Lincoln's Second Inaugural"
  description: "New researcher onboarding experiment using established high-quality text"

components:
  llm_analysis_approach: "hierarchical_analysis v2.1.0"
  theoretical_framework: "civic_virtue v2.1.0" 
  mathematical_weighting: "hierarchical_weighted v2.1.0"

analysis:
  mode: "single_model"
  selected_models: ["gpt-4o-mini"]
  target_texts: ["corpus/presidential_speeches/lincoln_1865_second_inaugural.txt"]
EOF

# Create experiment in database
python src/narrative_gravity/cli/experiment_manager.py create \
    --config my_first_experiment.yaml \
    --validate-components
```

#### **Step 4: Execute Analysis**
```bash
# Run your first experiment
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id [YOUR_EXPERIMENT_ID] \
    --text-file "corpus/presidential_speeches/lincoln_1865_second_inaugural.txt" \
    --model "gpt-4o-mini"
```

### **Phase 3: Analysis & Results** (45 minutes)

#### **Step 5: Generate Analysis Notebook**
```bash
# Create interactive analysis
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --experiment-id [YOUR_EXPERIMENT_ID] \
    --template-type jupyter \
    --output-dir "analysis_results/onboarding_analysis/"

# Launch interactive analysis
cd analysis_results/onboarding_analysis/
jupyter notebook enhanced_analysis.ipynb
```

#### **Step 6: Explore Results**
In the Jupyter notebook you'll find:
- **📊 Interactive Visualizations**: Elliptical plots with hover details
- **📈 Statistical Analysis**: Comprehensive metrics and confidence intervals
- **🔍 Quality Reports**: Validation and reliability assessments
- **📝 Academic Export**: Publication-ready data and visualizations

### **Phase 4: Understanding Quality Assurance** (30 minutes)

#### **Step 7: Examine Quality Reports**
Your results include:
- **Analysis Confidence**: Reliability metrics and consistency scores
- **Framework Fit**: How well the framework captured the text's content
- **Component Validation**: All research assets passed quality checks
- **Replication Package**: Complete materials for independent validation

#### **Step 8: Compare Approaches** (Optional)
```bash
# Try different approach for comparison
python src/narrative_gravity/cli/experiment_manager.py create \
    --name "Onboarding_Traditional_Comparison" \
    --hypothesis "Comparing hierarchical vs traditional analysis" \
    --prompt-template "traditional_analysis v2.1.0" \
    --framework "civic_virtue v2.1.0" \
    --weighting "linear_traditional v2.1.0" \
    --models "gpt-4o-mini"
```

---

## 🎓 **Understanding the Research Ecosystem**

### **Academic Rigor Standards**

The platform enforces **academic publication standards** throughout:

#### **Reproducibility Requirements**
- **Complete Provenance**: Every analysis tracked with component versions
- **Replication Packages**: All code, data, and procedures documented
- **Quality Metadata**: Confidence intervals and validation reports included
- **Version Control**: Systematic tracking of all research asset evolution

#### **Accessibility Compliance**
- **WCAG AA Standards**: All visualizations pass accessibility requirements
- **Journal Compatibility**: Colors work in grayscale print publications
- **Academic Export**: Multiple formats (R, Stata, CSV, Jupyter)

#### **Quality Assurance Integration**
- **6-Layer Validation**: Automatic detection of analysis issues
- **Component Testing**: All research assets validated before use
- **Academic Review Ready**: Confidence metadata for peer review

### **Research Workflow Philosophy**

#### **Validation-First Approach**
1. **Component Development**: Systematic creation and testing of research assets
2. **Method Validation**: Rigorous comparison of analytical approaches
3. **Substantive Research**: Apply validated methods to research questions
4. **Academic Publication**: Export publication-ready materials

#### **Systematic Methodology**
- **Hypothesis-Driven**: Clear predictions about component performance
- **Controlled Comparisons**: Systematic testing across design dimensions
- **Effect Size Focus**: Meaningful differences, not just statistical significance
- **Replication Ready**: Independent validation capabilities

---

## 🚀 **Next Steps: Becoming a Power User**

### **Immediate Next Activities**

#### **1. Explore Advanced Features** (1-2 hours)
- **Multi-Model Comparison**: Test GPT-4 vs Claude vs Gemini
- **Framework Comparison**: Civic virtue vs political spectrum analysis
- **Batch Processing**: Analyze multiple texts systematically

#### **2. Learn Asset Development** (2-4 hours)
- **Framework Development**: [`FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md`](../development-guides/FRAMEWORK_DEVELOPMENT_AND_MAINTENANCE.md)
- **Prompt Engineering**: [`PROMPT_TEMPLATE_DEVELOPMENT.md`](../development-guides/PROMPT_TEMPLATE_DEVELOPMENT.md)
- **Corpus Management**: [`CORPUS_DEVELOPMENT_GUIDE.md`](../development-guides/CORPUS_DEVELOPMENT_GUIDE.md)

#### **3. Design Your Research Study** (Variable)
- **Research Question Formation**: What do you want to investigate?
- **Experimental Design**: Use the 5-dimensional framework for systematic study
- **Hypothesis Development**: Clear predictions about optimal configurations

### **Advanced Capabilities to Explore**

#### **Human Validation Studies**
- **LLM vs Expert Comparison**: Validate computational analysis against human experts
- **Inter-rater Reliability**: Systematic assessment of analysis consistency
- **Bias Detection**: Identify systematic differences across evaluator types

#### **Methodological Research**
- **Component Optimization**: A/B testing of prompts, frameworks, weighting
- **Cross-Framework Validation**: How do different theoretical approaches compare?
- **Scalability Studies**: Performance across different text types and lengths

#### **Academic Publication Pipeline**
- **Methods Sections**: Complete formal specifications for academic papers
- **Replication Materials**: Everything needed for independent validation
- **Peer Review Support**: Quality assurance reports and confidence metadata

---

## 📚 **Resources & Support**

### **Documentation Navigation**
- **Methodology**: [`../methodology/`](../methodology/) - Experimental design and formal specifications
- **Development Guides**: [`../development-guides/`](../development-guides/) - Asset creation and maintenance
- **Practical Guides**: [`../practical-guides/`](../practical-guides/) - Execution and troubleshooting
- **Academic Workflow**: [`../academic-workflow/`](../academic-workflow/) - Publication and validation

### **Getting Help**
- **Platform Issues**: Check [`RESEARCH_QUALITY_STANDARDS.md`](RESEARCH_QUALITY_STANDARDS.md)
- **Methodology Questions**: Reference experimental design framework
- **Technical Problems**: Platform development team via GitHub issues
- **Research Consultation**: Academic workflow and validation guidance

### **Community & Collaboration**
- **Research Standards**: All methodology documented and validated
- **Component Sharing**: Systematic development and quality assurance
- **Academic Collaboration**: Publication-ready outputs and replication packages
- **Continuous Improvement**: Feedback integration and iterative enhancement

---

## 🎯 **Validation Checklist**

Before proceeding to advanced research, verify you can:

### **Basic Platform Operation** ✅
- [ ] Set up development environment successfully
- [ ] List and examine available research components
- [ ] Create and execute a simple experiment
- [ ] Generate and explore analysis results

### **Research Understanding** ✅
- [ ] Understand the 5-dimensional experimental design space
- [ ] Distinguish between frameworks, prompts, and weighting schemes
- [ ] Interpret quality assurance reports and confidence metadata
- [ ] Navigate the complete research workflow from design to publication

### **Quality Assurance** ✅
- [ ] Recognize when analysis results are high vs low quality
- [ ] Understand component compatibility and validation requirements
- [ ] Use replication packages and academic export capabilities
- [ ] Apply academic rigor standards throughout research process

**When you can check all boxes above, you're ready for advanced research with the platform!**

---

**Congratulations! You now have the foundation to conduct world-class computational narrative analysis research with full academic rigor and reproducibility.**

*Next Recommended Reading*: [`RESEARCH_WORKFLOW_OVERVIEW.md`](RESEARCH_WORKFLOW_OVERVIEW.md) for detailed methodology and advanced capabilities. 