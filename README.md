# Discernus Development Tools

A collection of development utilities, testing harnesses, and productivity tools for the Discernus computational social science platform.

## 🛠️ Tool Categories

### 🔍 Auditing Tools (`scripts/auditing/`)
Quality assurance and compliance checking tools:

- **Dependency auditing** - License compliance and security scanning
- **Code quality checks** - Style, complexity, and maintainability analysis
- **Research integrity** - Provenance and reproducibility validation
- **Performance monitoring** - Resource usage and optimization analysis

### 📋 Compliance Tools (`scripts/compliance_tools/`)
Regulatory and standards compliance utilities:

- **Academic standards** - Citation and methodology validation
- **Data protection** - Privacy and security compliance checks
- **Open science** - Reproducibility and transparency requirements
- **Licensing compliance** - Software license compatibility verification

### 🎯 Cursor Integration (`scripts/cursor_tools/`)
IDE integration and development workflow tools:

- **Project setup** - Automated workspace configuration
- **Code generation** - Template and boilerplate generators
- **Debugging helpers** - Enhanced debugging and logging tools
- **Workflow automation** - Common development task automation

### 🔬 Framework Research (`scripts/framework_researcher/`)
Tools for developing and researching analytical frameworks:

- **Framework synthesis** - Automated framework documentation generation
- **Validation testing** - Inter-rater reliability and quality assessment
- **Research synthesis** - Academic literature integration and analysis
- **Methodology validation** - Statistical and methodological verification

### ✅ Framework Validation (`scripts/framework_validation/`)
Specialized validation tools for analytical frameworks:

- **Specification compliance** - Framework format and structure validation
- **Academic rigor** - Theoretical foundation and citation verification
- **Measurement quality** - Scoring criteria and reliability assessment
- **Documentation completeness** - Usage guide and example validation

### 📚 Librarian Tools (`scripts/librarian/`)
Framework management and curation utilities:

- **Framework validation** - Comprehensive quality checks and compliance testing
- **Framework curation** - Organization and maintenance of framework collections
- **Research synthesis** - Automated documentation and report generation
- **Quality assurance** - Inter-rater reliability testing and validation workflows

### 🎨 Prompt Engineering (`scripts/prompt_engineering/`)
LLM prompt development and optimization tools:

- **Prompt testing harness** - Systematic prompt evaluation and comparison
- **Response analysis** - LLM output quality and consistency assessment
- **Optimization tools** - Prompt refinement and performance tuning
- **Template management** - Reusable prompt patterns and components

### 🧪 Testing Harnesses
Specialized testing tools for research workflows:

- **RAG Testing Harness** (`rag_testing_harness.py`) - Retrieval-Augmented Generation testing
- **LiteLLM Suppression** (`suppress_litellm_debug.py`) - Debug output management
- **Integration Testing** - End-to-end workflow validation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/discernus/tools.git
cd tools

# Install Discernus platform (required for librarian tools)
pip install discernus
# OR install from source:
# pip install git+https://github.com/discernus/discernus.git

# Install additional dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/**/*.py
```

### Basic Usage

```bash
# Audit project dependencies
python scripts/auditing/audit_dependencies.py

# Validate framework compliance
python scripts/compliance_tools/validate_framework.py framework.md

# Test prompts systematically
python scripts/prompt_engineering/test_harness.py --config test_config.yaml

# Generate framework documentation
python scripts/framework_researcher/synthesize_framework.py framework.md

# Validate framework quality
python scripts/librarian/validate_framework.py framework.md
```

## 📚 Tool Documentation

### Librarian Tools

#### Framework Validator
```bash
# Basic validation
python scripts/librarian/validate_framework.py framework.md

# Detailed validation with reports
python scripts/librarian/validate_framework.py framework.md --detailed --output validation_report.md

# Batch validation
python scripts/librarian/validate_framework.py frameworks/*.md --summary
```

#### Framework Synthesizer
```bash
# Generate academic overview
python scripts/librarian/synthesize_framework.py framework.md --type overview

# Create validation report
python scripts/librarian/synthesize_framework.py framework.md --type validation

# Generate usage guide
python scripts/librarian/synthesize_framework.py framework.md --type guide
```

#### Framework Curator
```bash
# Organize frameworks by category
python scripts/librarian/curate_frameworks.py frameworks/ --by-category --output organized/

# Update framework metadata
python scripts/librarian/curate_frameworks.py frameworks/ --update-metadata

# Generate collection index
python scripts/librarian/curate_frameworks.py frameworks/ --index --output index.md
```

### Other Tool Categories

For detailed documentation on other tool categories, see their respective README files in the `scripts/` subdirectories.

## 🏗️ Architecture

### Tool Organization

```
tools/
├── scripts/                    # Main tool collection
│   ├── auditing/              # Quality assurance tools
│   ├── compliance_tools/      # Standards compliance
│   ├── cursor_tools/          # IDE integration
│   ├── framework_researcher/  # Framework development
│   ├── framework_validation/  # Framework quality
│   ├── librarian/             # Framework management
│   └── prompt_engineering/    # LLM optimization
├── tests/                     # Tool test suite
├── docs/                      # Tool documentation
├── examples/                  # Usage examples
└── templates/                 # Reusable templates
```

### Dependencies

#### Core Dependencies
- **Python 3.8+** - Required for all tools
- **Discernus Platform** - Required for librarian tools (LLM gateway access)
- **Standard libraries** - requests, urllib3, json, xml.etree.ElementTree

#### Librarian Tools Dependencies
The librarian tools (`scripts/librarian/`) require the Discernus platform for:
- **LLM Gateway** - Access to language models for analysis and synthesis
- **Model Registry** - Model configuration and management
- **Core utilities** - Shared platform functionality

**Note**: Other development tools can be used independently without the Discernus platform.

### Integration Points

The tools integrate with:
- **Discernus Core Platform** - Main analysis engine and LLM services
- **Discernus Frameworks** - Community frameworks
- **External Tools** - Git, CI/CD, IDEs, academic databases

## 🤝 Contributing

We welcome contributions to the Discernus development tools! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Contribution Areas

- **New tools** - Additional development utilities
- **Tool improvements** - Enhanced functionality and performance
- **Documentation** - Usage guides and examples
- **Testing** - Expanded test coverage and validation
- **Integration** - Better IDE and workflow integration

## 📄 License

This project is licensed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)** - see [LICENSE](LICENSE) for details.

### Why GPL v3?

Development tools use GPL v3 licensing to:
- **Ensure freedom** - Keep development tools free and open source
- **Prevent proprietary capture** - Protect against closed-source derivatives  
- **Maintain community benefit** - Ensure improvements remain open
- **Support research transparency** - Keep research tools auditable and reproducible

### Dual Licensing

For commercial integration and proprietary use cases:
- **Commercial licenses** available for enterprise integration
- **Contact**: licensing@discernus.ai for commercial licensing options

## 🔗 Related Projects

- **[Discernus Core Platform](https://github.com/discernus/discernus)** - Main analysis engine (GPL v3)
- **[Discernus Frameworks](https://github.com/discernus/frameworks)** - Community frameworks (MIT)
- **[Discernus Research](https://github.com/discernus/research)** - Example studies (MIT)

## 📞 Support

- **Documentation**: See `docs/` directory for detailed tool guides
- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions for tool development
- **Email**: tools@discernus.ai for direct support

---

**Discernus™**: Computational Social Science Research Platform