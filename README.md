# Discernus
**Computational Discourse Analysis Platform for Academic Research**

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql-blue.svg)](https://www.postgresql.org/)

> **Academic Validation Strategy: Expert Consultation + Statistical Evidence + Publication Pipeline**

## 🎯 **MVP Focus: Moral Foundations Theory Validation**

Discernus is a **validation-first computational discourse analysis platform** designed for rigorous academic research. Our current focus is establishing academic credibility through systematic validation of Moral Foundations Theory implementation against established measures (MFQ-30) with expert consultation from framework originators.

**Strategic Objectives:**
- **Expert Endorsement**: Collaboration with Jonathan Haidt lab for MFT validation
- **Statistical Validation**: r>0.8 correlation with MFQ-30 across all foundations
- **Academic Publication**: Co-authored methodology paper with framework experts
- **Community Adoption**: Computational social science researcher platform usage

## 🔬 **Academic Research Infrastructure**

This platform prioritizes **academic research workflows** and **methodological rigor** over user interfaces. All development focuses on publication-quality methodology, expert consultation integration, and systematic validation evidence.

**Core Research Capabilities:**
- **Framework Validation**: Systematic testing against established psychological measures
- **Multi-LLM Reliability**: Cross-model consistency testing for methodological credibility  
- **Expert Integration**: Academic collaboration workflows with framework originators
- **Publication Pipeline**: Academic export formats and replication packages
- **Quality Assurance**: 6-layer validation preventing research failures

## 🏛️ **Academic Positioning**

### Current Development Phase
**Phase 1**: MFT Implementation Development (December 2024)
- Building robust MFT analysis using existing infrastructure
- Internal validation testing on political texts
- Professional demonstration system for expert review
- Preliminary validation study with correlation evidence

### Expert Consultation Strategy  
**Phase 2**: Expert Engagement After Demonstration (Weeks 5-8)
- Haidt lab outreach with working MFT implementation
- Implementation refinement based on expert feedback
- Large-scale validation study design (expert-approved)
- Academic collaboration framework establishment

### Validation Execution
**Phase 3**: Large-Scale Statistical Validation (Weeks 9-12)
- n=500 participant study with MFQ-30 correlations
- Multi-LLM reliability analysis (target: r=0.91+ between models)
- Publication-quality statistical evidence generation
- Academic paper drafting with expert co-authorship

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

## 🚀 **Quick Start for Researchers**

### Prerequisites
- **Python 3.9+**
- **PostgreSQL database** 
- **OpenAI API key** (for MFT analysis)

### Installation
```bash
# Clone repository
git clone https://github.com/discernus/discernus.git
cd discernus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup development environment
source scripts/setup_dev_env.sh

# Setup database
python launch.py --setup-db
```

### Research Workflow
```bash
# 1. Check system status
python scripts/production/check_existing_systems.py "MFT analysis"

# 2. Run MFT analysis
python scripts/analyze_mft.py --text "your_text.txt" --output results.json

# 3. Generate academic export
python scripts/export_academic_data.py --study-name "mft_validation_2024" --format all

# 4. Create publication visualizations
python scripts/create_publication_figures.py --experiment mft_validation_2024
```

## 📊 **Available Frameworks**

### Primary: Moral Foundations Theory (MFT)
**Academic Focus**: Haidt et al. (2009-2024) validation study
- **5 Foundations**: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation
- **Validation Target**: MFQ-30 correlation analysis
- **Expert Consultation**: Jonathan Haidt lab collaboration
- **Research Application**: Cross-cultural moral discourse analysis

### Additional Frameworks (Post-MVP)
- **Political Framing Theory**: Issue framing and narrative positioning
- **Cultural Theory**: Douglas & Wildavsky cultural analysis
- **Business Ethics Framework**: Corporate communication analysis  
- **Identity Framework**: Recognition and identity dynamics

## 🎯 **Academic Validation Strategy**

### Statistical Validation Targets
- **Overall MFT Correlation**: r>0.8 with MFQ-30 (p<0.001)
- **Foundation-Specific**: Care/Harm r>0.89, Fairness r>0.81, etc.
- **Cross-LLM Reliability**: r>0.91 between GPT-4, Claude, Gemini
- **Effect Sizes**: d>0.8 for practical significance

### Expert Consultation Protocol
- **Implementation Review**: Technical accuracy assessment by framework originators
- **Methodology Validation**: Academic standards compliance verification
- **Collaboration Framework**: Co-authorship and publication planning
- **Community Endorsement**: Computational social science network recommendations

### Publication Pipeline
- **Target Venues**: Computational Social Science, Political Psychology journals
- **Methodology Contribution**: Systematic framework validation for computational text analysis
- **Replication Package**: Complete code, data, and analysis scripts
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
python3 scripts/production/check_existing_systems.py "your functionality description"

# Check production systems inventory:
cat docs/EXISTING_SYSTEMS_INVENTORY.md

# Validate compliance with development standards:
python3 scripts/production/validate_ai_assistant_compliance.py --check-suggestion "your suggestion"
```

### Clean Architecture Standards
- ✅ **Production**: `src/`, `scripts/production/`, `docs/specifications/` (stable, tested, documented)
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
- **MFT Implementation**: Framework-specific analysis using existing infrastructure
- **Internal Validation**: Testing on political texts with correlation analysis
- **Demo System**: Professional presentation for expert consultation
- **Preliminary Studies**: Small-scale validation evidence generation

### 🔮 Upcoming Milestones
- **Week 5**: Expert consultation initiation with working demonstration
- **Week 9**: Large-scale validation study launch (n=500 participants)
- **Week 11**: Academic paper drafting with statistical evidence
- **Week 12**: Publication preparation and community outreach

## 🤝 **Academic Collaboration**

### Expert Consultation Framework
- **Framework Originators**: Direct collaboration with MFT developers
- **Academic Standards**: Institutional-quality methodology and documentation
- **Publication Partnership**: Co-authorship and peer review collaboration
- **Community Integration**: Computational social science network engagement

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
  year={2024},
  url={https://github.com/discernus/discernus},
  version={1.0.0-mvp}
}
```

For the academic methodology paper (when published):
```bibtex
@article{discernus_methodology,
  title={Systematic Framework Validation for Computational Text Analysis: The Discernus Platform},
  author={[Author Name] and Jonathan Haidt},
  journal={Computational Social Science},
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

Copyright (c) 2024 Discernus. All rights reserved.

This project is proprietary software designed for academic research collaboration. See the [LICENSE](LICENSE) file for complete terms regarding academic use, collaboration, and citation requirements.

---

**🔬 Academic Research Focus**: This platform prioritizes methodological rigor, expert consultation, and publication-quality evidence over user interface development. Our goal is establishing Discernus as the validated standard for computational discourse analysis in academic research.
