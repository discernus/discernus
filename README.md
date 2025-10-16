# Discernus: Computational Text Analysis Platform

Discernus a computational research platform that applies user-created analytical frameworks to rhetorical texts using large language models. The system extracts framework scores, metrics, and evidence quotes, generates statistical analyses, and produces evidence-integrated research reports with provenance tracking via content addressable file storage and git.

## What It Does

Discernus addresses the scalability and consistency challenges of traditional text analysis. Instead of manual coding, researchers can define their analytical frameworks in natural language. The system then uses Large Language Models (LLMs) to apply these frameworks at scale, producing statistical results, evidence-backed scores, and complete audit trails. This allows for reproducible, transparent, and computationally rigorous analysis of large text corpora.

## What's New in v2.1

**Major Release** - Discernus v2.1 transforms the platform into a production-ready computational research system:

### 🏗️ **THIN Architecture Compliance**
- **90%+ Performance Improvement** on large documents
- **Eliminated Hanging Issues** - CDDF 42-document experiment now runs smoothly
- **Clean Separation** - LLM handles reasoning, software handles parsing

### 💾 **Data Preservation Architecture** 
- **90%+ Cost Reduction** for sensitivity analysis
- **Full Data Preservation** - All raw scores available for re-analysis
- **Experiment-Level Parameterization** - Configure thresholds without code changes

### 🔬 **Framework Fit Score System**
- **Standardized Validity Assessment** across all 12 frameworks
- **Automated Calculation** by Statistical Agent
- **Cross-Framework Comparability** for research design decisions

### 🔄 **Robust Resume Functionality**
- **Production-Ready** experiment resumption
- **Cross-Run Support** with `--run-dir` option
- **Enhanced Error Messages** and validation

### ⚙️ **Enhanced Validation System**
- **Comprehensive Corpus Validation** with clear error guidance
- **Multi-Layer Validation** at corpus, experiment, and runtime levels
- **THIN Architecture Compliance** throughout

```bash
# Resume from most recent run
discernus run projects/experiment --resume --from statistical

# Resume from specific run  
discernus run projects/experiment --run-dir 20250101_120000 --from evidence

# Configure parameters in experiment.md
# Add reliability_filtering section with your thresholds
```

## Quick Start

Get up and running with a simple test experiment.

```bash
# 1. Install dependencies
make install

# 2. Verify your environment
make check

# 3. Run a fast test experiment (8-12 minutes, ~$0.50-1.00)
discernus run projects/nano --skip-validation
```

## Installation

Discernus is designed to run locally without complex dependencies.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/discernus.git
   cd discernus
   ```
2. **Install requirements**:
   ```bash
   make install
   ```
3. **Set up environment variables**:
   Copy the `env.template` to `.env` and add your API keys (e.g., for Google Gemini).

For detailed instructions, see the [Installation Guide](docs/user/INSTALLATION_GUIDE.md).

## Capabilities & Limitations (Alpha Release)

This is an alpha release. The system is under active development.

### Key Capabilities

* **Framework-Agnostic Analysis**: Define analytical frameworks in natural language using YAML specifications.
* **Automated 5-Phase Pipeline**: A consistent pipeline for validation, analysis, statistical processing, evidence curation, and synthesis.
* **LLM-Based Calculations**: Uses the internal code execution capabilities of modern LLMs for mathematical and statistical analysis.
* **Content-Addressable Storage**: All artifacts are stored locally with SHA256 hashes, ensuring reproducibility and eliminating redundant computation.
* **Complete Provenance**: Git-based versioning and detailed audit logs provide a complete, transparent history of every analysis.

### Current Limitations

* **Model Support**: The alpha release exclusively supports the **Google Gemini 2.5 series** (Pro, Flash, and Lite).
* **Synthesis Scalability**: The synthesis phase, which combines all data and evidence, is limited by the LLM's context window. For large experiments (e.g., >400 documents with a complex framework), it's recommended to execute analysis only runs (see below).
* **No UI**: All operations are currently managed through the command-line interface (CLI).
* **Phase-Specific Workflow**: For very large corpora, users can run specific phases (e.g., `--from analysis --to statistical`) to produce document-level artifacts that can be aggregated using external scripting and statistical platforms (e.g., R, Python with pandas).

## Documentation

* **[Quick Start Guide](docs/user/QUICK_START_GUIDE.md)**: 5-minute tutorial to run your first experiment.
* **[User Guide](docs/user/USER_GUIDE.md)**: Complete guide to get started, define experiments, and interpret results.
* **[Installation Guide](docs/user/INSTALLATION_GUIDE.md)**: Detailed setup instructions.
* **[CLI Reference](docs/user/CLI_REFERENCE.md)**: Complete reference for all command-line options.
* **[System Architecture](docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md)**: Technical architecture and implementation details.
* **[Methodology](docs/DISCERNUS_METHODOLOGY.md)**: Research framework and analytical procedures.
* **[Specifications](docs/specifications/)**: Technical specifications for frameworks, experiments, and corpora.

## Contributing

Contributions are welcome! Please see the [System Architecture](docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md) for technical details and development guidelines.
