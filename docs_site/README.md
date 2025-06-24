# Discernus
**Computational Discourse Analysis Platform for Academic Research**

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql-blue.svg)](https://www.postgresql.org/)

### Key Documents
[![Documentation Index](https://img.shields.io/badge/docs-Documentation%20Index-blue.svg)](docs/DOCUMENTATION_INDEX.md)
[![Contributing Guide](https://img.shields.io/badge/docs-Contributing%20Guide-blue.svg)](docs/CONTRIBUTING.md)
[![Dev Environment](https://img.shields.io/badge/docs-Dev%20Environment-blue.svg)](docs/platform-development/DEV_ENVIRONMENT.md)

> **Academic Validation Strategy: Expert Consultation + Statistical Evidence + Publication Pipeline**

## 🎯 **MVP Focus: Dual Framework Validation (MFT + PFT)**

Discernus is a **validation-first computational discourse analysis platform** designed for rigorous academic research. Our current focus is establishing academic credibility through systematic validation of our implementation using leading academic theories of moral psychology and political communication to evaluate contemporary textual narratives with expert consultation from framework originators.

**Strategic Objectives:**
- **Expert Endorsement**: Collaboration with Jonathan Haidt lab (MFT) and political framing theory researchers (PFT)
- **Statistical Validation**: r>0.8 correlation with MFQ-30 for MFT; systematic frame detection accuracy for PFT
- **Academic Publication**: Co-authored methodology papers with framework experts across moral psychology and political communication
- **Community Adoption**: Computational social science and political psychology researcher platform usage

## 🔬 **Academic Research Infrastructure**

This platform prioritizes **academic research workflows** and **methodological rigor** over user interfaces. All development focuses on publication-quality methodology, expert consultation integration, and systematic validation evidence.

**Core Research Capabilities:**
- **Framework Validation**: Systematic testing against established psychological measures
- **Multi-LLM Reliability**: Cross-model consistency testing for methodological credibility  
- **Expert Integration**: Academic collaboration workflows with framework originators
- **Publication Pipeline**: Academic export formats and replication packages
- **Quality Assurance**: 6-layer validation preventing research failures

## 🚀 Quickstart Guide: Your First Experiment

This guide provides the minimum steps to get the platform running and execute your first analysis experiment.

### 1. Environment Setup

First, set up your local development environment. For detailed instructions, see the [`docs/platform-development/DEV_ENVIRONMENT.md`](docs/platform-development/DEV_ENVIRONMENT.md).

```bash
# Set up local development environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment and database
cp env.example .env
# Edit .env with your local database settings and API keys
python3 check_database.py
```

### 2. Create an Experiment Definition File

The entire experiment is defined in a single YAML file. Create a file named `my_first_experiment.yaml` and paste the following content. This example will run a basic Moral Foundations Theory (MFT) analysis on a sample text.

```yaml
# my_first_experiment.yaml

# --- High-level metadata about the experiment ---
experiment:
  name: "MFT Validation on Sample Speech"
  description: "A quickstart experiment to test the MFT framework on a sample text."
  version: "1.0.0"
  tags: ["mft", "quickstart", "validation"]
  hypotheses:
    - "The analysis will successfully identify and quantify the five moral foundations in the text."

# --- All the assets required to run the experiment ---
# For a full reference of all options, see docs/specifications/experiment_schema.json
components:
  # Specify the analytical framework to use
  framework:
    name: "moral_foundations_theory"
    version: "1.0" # Make sure this version exists in your frameworks directory

  # Define the corpus of texts to analyze
  corpus:
    name: "Demo Corpus"
    path: "./corpus/demo_texts/" # Path to the directory with .txt files
    pattern: "*.txt" # Glob pattern to find the texts

  # List the Large Language Models to use for the analysis
  models:
    - provider: "openai"
      name: "gpt-4-turbo" # Ensure you have an API key for this model

# --- Settings that control the execution ---
execution_settings:
  enable_qa: true # Run the 6-layer Quality Assurance validation on results
  enable_cache: true # Use cached results to save time and cost on re-runs
```

### 3. Run the Experiment

With your `experiment.yaml` file ready, execute it using the orchestrator script locally.

```bash
# Run the experiment orchestrator
python3 scripts/applications/comprehensive_experiment_orchestrator.py my_first_experiment.yaml
```

### 4. Check the Results

The orchestrator will create a new directory in the `experiments/` folder named after your experiment. Inside, you will find:

-   **`results.json`**: The raw JSON output from the analysis.
-   **`report.html`**: A comprehensive HTML report with visualizations.
-   **`academic_exports/`**: Data formatted for R, Stata, and other statistical tools.

## 🏛️ **Academic Positioning**

### Current Development Phase
**Phase 1**: Dual Framework Implementation Development (June 2025)
- Building robust MFT and PFT analysis using existing infrastructure
- Internal validation testing on political texts with both moral and framing perspectives
- Professional demonstration system for expert review across both frameworks
- Preliminary validation studies with correlation evidence (MFT) and frame detection accuracy (PFT)

### Expert Consultation Strategy  
**Phase 2**: Expert Engagement After Demonstration (Weeks 5-8)
- Haidt lab outreach with working MFT implementation
- Political framing theory researcher engagement with working PFT implementation
- Implementation refinement based on expert feedback across both frameworks
- Large-scale validation study design (expert-approved for both MFT and PFT)
- Academic collaboration framework establishment for dual publications

### Validation Execution
**Phase 3**: Large-Scale Statistical Validation (Weeks 9-12)
- n=500 participant study with MFQ-30 correlations for MFT validation
- Frame detection accuracy studies for PFT validation using known exemplars
- Multi-LLM reliability analysis (target: r=0.91+ between models across both frameworks)
- Publication-quality statistical evidence generation for both frameworks
- Academic paper drafting with expert co-authorship (dual publication strategy)

## 🔧 **Technical Infrastructure**

### Production-Ready Systems
- **Multi-LLM Integration**: OpenAI, Anthropic, Google AI with cost controls
- **Quality Assurance**: 6-layer validation system preventing silent failures
- **Database Infrastructure**: PostgreSQL with complete experimental provenance
- **Academic Export**: R/Stata/Jupyter templates with publication metadata
- **Visualization**: Professional Plotly system with academic theming

### Framework Management v2.0
- **JSON Schema Validation**: 3-tier validation (Schema, Semantic, Academic)
- **Version Control**: Complete component versioning for reproducibility  
- **Academic Standards**: Citation requirements and empirical validation
- **Expert Integration**: Framework originator consultation workflows

## 📊 **Available Frameworks**

### Primary MVP Targets: Dual Framework Implementation

#### Moral Foundations Theory (MFT)
**Academic Focus**: Haidt et al. (2009-2024) validation study
- **5 Foundations**: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation
- **Validation Target**: MFQ-30 correlation analysis (r>0.8)
- **Expert Consultation**: Jonathan Haidt lab collaboration
- **Research Application**: Cross-cultural moral discourse analysis

#### Political Framing Theory (PFT) 
**Academic Focus**: Entman & Lakoff integration study
- **Lakoff Framework**: Three dipoles with arc clustering hypothesis (Authority/Discipline ↔ Empathy/Communication, Competition/Hierarchy ↔ Cooperation/Mutual Support, Self-Reliance ↔ Interdependence)
- **Entman Framework**: Four independent wells (Problem Definition, Causal Attribution, Moral Evaluation, Treatment Recommendation)
- **Validation Target**: Frame detection accuracy and theoretical coherence testing
- **Expert Consultation**: Political communication and cognitive linguistics researchers
- **Research Application**: Political discourse analysis and strategic communication assessment

### Additional Frameworks (Post-MVP)
- **Cultural Theory**: Douglas & Wildavsky cultural analysis
- **Business Ethics Framework**: Corporate communication analysis  

## 🎯 **Academic Validation Strategy**

### Statistical Validation Targets

#### Moral Foundations Theory (MFT)
- **Overall MFT Correlation**: r>0.8 with MFQ-30 (p<0.001)
- **Foundation-Specific**: Care/Harm r>0.89, Fairness r>0.81, etc.
- **Cross-LLM Reliability**: r>0.91 between GPT-4, Claude, Gemini
- **Effect Sizes**: d>0.8 for practical significance

#### Political Framing Theory (PFT)
- **Lakoff Framework**: Arc clustering validation (>75% texts following predicted patterns)
- **Entman Framework**: Frame function detection accuracy (>80% precision/recall)
- **Cross-LLM Reliability**: r>0.91 between models for frame detection
- **Theoretical Coherence**: Family model coherence testing and violation detection

### Expert Consultation Protocol
- **Implementation Review**: Technical accuracy assessment by framework originators (Haidt lab for MFT, political communication researchers for PFT)
- **Methodology Validation**: Academic standards compliance verification across both frameworks
- **Collaboration Framework**: Co-authorship and publication planning for dual framework papers
- **Community Endorsement**: Computational social science and political psychology network recommendations

### Publication Pipeline
- **Target Venues**: Computational Social Science, Political Psychology, Political Communication journals
- **Methodology Contribution**: Systematic dual framework validation for computational text analysis
- **Replication Package**: Complete code, data, and analysis scripts for both frameworks
- **Open Science**: Transparent methodology and reproducible research standards

## 📚 **Documentation & Research**

### Academic Documentation
- **Methodology Guide**: [`docs/specifications/`](docs/specifications/) - Complete validation protocols
- **Research Workflow**: [`docs/research-guide/`](docs/research-guide/) - Academic pipeline documentation
- **Expert Consultation**: [`docs/planning/discernus_mvp_user_journeys.md`](docs/planning/discernus_mvp_user_journeys.md) - Collaboration frameworks

### Technical Documentation  
- **System Architecture**: [`docs/platform-development/architecture/`](docs/platform-development/architecture/) - Infrastructure design
- **API Reference**: Production systems and integration guides
- **Quality Assurance**: 6-layer validation system documentation

## 🏗️ **Development Workflow**

### **🚨 MANDATORY: Search Production Systems First**
```bash
# ALWAYS run before any new development:
python3 scripts/applications/check_existing_systems.py "your functionality description"

# Check production systems inventory:
cat docs/EXISTING_SYSTEMS_INVENTORY.md

# Validate compliance with development standards:
python3 scripts/applications/validate_ai_assistant_compliance.py --check-suggestion "your suggestion"
```

### Clean Architecture Standards
- ✅ **Production**: `src/`, `scripts/applications/`, `docs/specifications/` (stable, tested, documented)
- 🧪 **Experimental**: `experimental/`, `sandbox/` (iteration, prototypes, testing)  
- 🗑️ **Deprecated**: `deprecated/` (obsolete code - avoid using)

### Development Process
1. **Search First**: Use production search tools to find existing systems
2. **Enhance Existing**: Improve production code rather than rebuilding
3. **Build in Experimental**: New development starts in `experimental/prototypes/`
4. **Promote When Ready**: Move to production with quality validation

## 📈 **Project Status**

### ✅ Completed Infrastructure
- **Live Academic Research Pipeline**: Production API integration with quality assurance
- **Multi-LLM Support**: OpenAI, Anthropic, Google AI operational
- **Database System**: PostgreSQL with complete experimental schema
- **Quality Assurance**: 6-layer validation preventing silent failures
- **Academic Export**: R/Stata/Jupyter templates with publication metadata

### 🎯 Current Development (Phase 1)
- **Dual Framework Implementation**: MFT and PFT analysis using existing infrastructure
- **Internal Validation**: Testing on political texts with correlation analysis (MFT) and frame detection (PFT)
- **Demo System**: Professional presentation for expert consultation across both frameworks
- **Preliminary Studies**: Small-scale validation evidence generation for both MFT and PFT

### 🔮 Upcoming Milestones
- **Week 5**: Expert consultation initiation with working demonstration (both MFT and PFT)
- **Week 9**: Large-scale validation study launch (n=500 participants for MFT; frame detection accuracy for PFT)
- **Week 11**: Academic paper drafting with statistical evidence for both frameworks
- **Week 12**: Publication preparation and community outreach across moral psychology and political communication

## 🤝 **Academic Collaboration**

### Expert Consultation Framework
- **Framework Originators**: Direct collaboration with MFT developers (Haidt lab) and political framing theory researchers
- **Academic Standards**: Institutional-quality methodology and documentation across both frameworks
- **Publication Partnership**: Co-authorship and peer review collaboration for dual framework papers
- **Community Integration**: Computational social science and political psychology network engagement

### Research Community
- **Target Audience**: Computational social scientists, digital humanities researchers
- **Collaboration Opportunities**: Framework validation, cross-cultural studies, methodology development
- **Academic Workshops**: Conference presentations and training sessions
- **Open Science**: Transparent methodology and reproducible research standards

## 📖 **Citation**

If you use Discernus in your research, please cite:

```bibtex
@software{discernus_platform,
  title={Discernus: Computational Discourse Analysis Platform for Academic Research},
  author={[Author Name]},
  year={2025},
  url={https://github.com/discernus/discernus},
  version={1.0.0-mvp}
}
```

For the academic methodology papers (when published):
```bibtex
@article{discernus_mft_methodology,
  title={Computational Validation of Moral Foundations Theory: The Discernus MFT Implementation},
  author={[Author Name] and Jonathan Haidt},
  journal={Political Psychology},
  year={2025},
  note={Software available at https://github.com/discernus/discernus}
}

@article{discernus_pft_methodology,
  title={Systematic Political Framing Analysis: Computational Implementation of Entman-Lakoff Integration},
  author={[Author Name] and [Political Communication Researchers]},
  journal={Political Communication},
  year={2025},
  note={Software available at https://github.com/discernus/discernus}
}
```

## 📞 **Contact & Support**

### Academic Collaboration
- **Research Questions**: Academic methodology and framework validation discussions
- **Expert Consultation**: Framework originator collaboration requests
- **Publication Partnership**: Co-authorship and peer review opportunities

### Technical Support
- **Documentation**: Complete guides in [`docs/`](docs/) directory
- **Issues**: Report bugs and request features via GitHub Issues
- **Development**: See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development guidelines

### Community
- **Discussions**: Computational social science methodology discussions
- **Workshops**: Academic training and methodology sessions
- **Conferences**: Presentations at CSS Society, APSA, and related venues

## 📄 **License**

Copyright (c) 2025 Discernus. All rights reserved.

This project is proprietary software designed for academic research collaboration. See the [LICENSE](LICENSE) file for complete terms regarding academic use, collaboration, and citation requirements.

---

**🔬 Academic Research Focus**: This platform prioritizes methodological rigor, expert consultation, and publication-quality evidence over user interface development. Our goal is establishing Discernus as the validated standard for computational discourse analysis in academic research.
