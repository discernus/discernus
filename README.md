# Narrative Gravity Maps: Quantitative Framework for Analyzing Persuasive Narratives

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql-blue.svg)](https://www.postgresql.org/)

**Narrative Gravity Maps** is a research platform for quantitative analysis of persuasive narratives through configurable analytical frameworks. The system maps narrative "gravity wells" that represent conceptual forces attracting or repelling audience attention, enabling systematic analysis of persuasive discourse across any domain.

## 🎯 **Focus: Academic Research Pipeline**

This platform prioritizes **academic research workflows** over user interfaces. All frontend development has been archived pending completion of the core research pipeline and academic publication.

**Core Research Capabilities:**
- **Database-driven analysis**: PostgreSQL backend with comprehensive provenance tracking
- **Framework management**: 5 formal frameworks with v2.0 specification system
- **Batch processing**: CLI tools for systematic experimentation
- **Academic standards**: Publication-ready output formats and replication packages

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Research Frameworks](#research-frameworks)
- [CLI Tools](#cli-tools)
- [Database Architecture](#database-architecture)
- [Academic Workflow](#academic-workflow)
- [Development](#development)
- [Citation](#citation)

## Overview

### What are Narrative Gravity Maps?

Narrative Gravity Maps visualize the **conceptual forces** within persuasive texts by mapping them onto a coordinate system with **gravity wells** representing different values, emotions, or rhetorical strategies defined by analytical frameworks. Each well has a position (angle) and gravitational strength (weight), creating a force field that attracts narrative elements.

**Example - Civic Virtue Framework (one of 5 available frameworks):**
- **Framework-defined attractive forces**: Dignity (90°), Truth (45°), Hope (20°), Justice (135°), Pragmatism (160°)
- **Framework-defined repulsive forces**: Tribalism (270°), Manipulation (315°), Fantasy (340°), Resentment (225°), Fear (200°)

### Research Applications

- **Persuasive Discourse Analysis**: Mapping conceptual appeals across any domain using appropriate frameworks
- **Argumentative Structure Analysis**: Understanding rhetorical patterns in debates and policy discussions  
- **Cross-Cultural Research**: Comparing emphasis patterns across societies using cultural frameworks
- **Historical Analysis**: Tracking narrative themes across time periods with domain-appropriate frameworks
- **Framework Development**: Creating domain-specific analysis systems for any field of study

## Key Features

### 🔬 **Research-Grade Infrastructure**
- **PostgreSQL Backend**: Complete experimental provenance and version control
- **Component Versioning**: Formal specifications for frameworks, prompts, and weighting schemes
- **Batch Processing**: Systematic experimentation with statistical validation
- **Academic Standards**: Publication-ready outputs with comprehensive metadata

### 📊 **Formal Framework System**
- **5 Complete Frameworks**: Civic virtue, political spectrum, moral foundations, identity, rhetorical posture
- **v2.0 Specification**: JSON schema with 3-tier validation (Schema, Semantic, Academic)
- **Circular Coordinates**: Universal compatibility with academic tools (R, Stata, Python)
- **Theoretical Foundations**: Academic citations and empirical validation requirements

### 🛠️ **Command-Line Tools**
- **Framework Management**: Create, validate, migrate, and sync analytical frameworks for any domain
- **Intelligent Corpus Ingestion**: LLM-powered metadata extraction from messy text files
- **Academic Export**: Multi-format datasets with analysis templates
- **Database Operations**: Complete CLI interface for research workflows

### 🎯 **Analysis Pipeline**
- **Multi-LLM Support**: OpenAI, Anthropic, and other providers for framework-agnostic analysis
- **Hierarchical Prompting**: Advanced template system eliminating flat score distributions
- **Enhanced Visualization**: Plotly-based circular coordinate system for any framework type
- **Statistical Rigor**: Confidence intervals, variance analysis, reproducibility across domains

## Quick Start

### Prerequisites

- **Python 3.9+**
- **PostgreSQL database** 
- **OpenAI API key** (for LLM analysis)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/narrative_gravity_analysis.git
cd narrative_gravity_analysis

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

### Basic Research Workflow

```bash
# 1. Check framework status
python scripts/framework_sync.py status

# 2. Generate analysis prompt
python scripts/generate_prompt.py --framework civic_virtue --output my_prompt.txt

# 3. Run LLM analysis (external step with ChatGPT/Claude)
# Use the generated prompt with your chosen LLM

# 4. Process results (when you have LLM JSON response)
python scripts/process_analysis_results.py results.json

# 5. Generate visualizations
python scripts/create_visualization.py results.json --output analysis.html
```

### Backend Services

```bash
# Launch all backend services
python launch.py

# Or launch specific services
python launch.py --api-only     # Just the API (port 8000)
python launch.py --celery-only  # Just background workers
```

**Services:**
- **API Server**: http://localhost:8000 (with docs at /api/docs)
- **Celery Workers**: Background processing for batch operations

## Example Frameworks

The system includes 5 domain-specific frameworks demonstrating the methodology's versatility:

### 1. Civic Virtue Framework (Primary Example)
**Domain**: Political discourse analysis
- **10 wells**: Framework-defined attraction/repulsion forces for civic analysis
- **Hierarchical weighting**: Demonstrates differential weighting capabilities
- **Use case**: Political speeches, policy debates, campaign rhetoric

### 2. Political Spectrum Framework  
**Domain**: Political positioning analysis
- **6 wells**: Framework-defined progressive/conservative dimensions
- **Equal weighting**: Demonstrates uniform weighting approach
- **Use case**: Ideological analysis, partisan classification

### 3. Moral Foundations Theory (MFT) Framework
**Domain**: Cross-cultural moral analysis
- **10 wells**: Framework-defined universal moral dimensions
- **Equal weighting**: Descriptive framework approach
- **Use case**: Cross-cultural comparative analysis

### 4. Fukuyama Identity Framework
**Domain**: Identity and recognition analysis
- **6 wells**: Framework-defined identity dynamics
- **Vertical arrangement**: Demonstrates positioning flexibility
- **Use case**: Identity-focused discourse analysis

### 5. Moral Rhetorical Posture Framework
**Domain**: Communication style analysis
- **6 wells**: Framework-defined communication approaches
- **Communication focus**: Style vs content analysis capabilities
- **Use case**: Conflict analysis, mediation contexts

**Note**: These are examples demonstrating the platform's capability to support frameworks from any analytical domain.

## CLI Tools

### Framework Management

```bash
# Check framework synchronization status
python scripts/framework_sync.py status

# Export framework from database for editing
python scripts/framework_sync.py export civic_virtue

# Import edited framework back to database  
python scripts/framework_sync.py import civic_virtue

# Validate framework compliance
python scripts/validate_framework_spec.py --framework civic_virtue

# Validate all frameworks
python scripts/validate_framework_spec.py --all
```

### Corpus Management

```bash
# Intelligent ingestion from messy text files
python scripts/intelligent_ingest.py /path/to/text/files/

# YouTube transcript extraction and processing
python scripts/intelligent_ingest_youtube.py "https://youtube.com/watch?v=VIDEO_ID"

# Check corpus status and FAIR compliance
python scripts/corpus_status.py --show-stats
```

### Academic Export

```bash
# Export data for academic analysis
python scripts/export_academic_data.py --study-name "my_study_2025" --format all

# Install R packages for analysis
Rscript scripts/install_essential_r_packages.R

# Generate analysis templates
python scripts/generate_analysis_templates.py --study-name "my_study_2025"
```

## Database Architecture

### Core Tables
- **`framework_versions`**: Formal framework specifications with validation status
- **`prompt_templates`**: Versioned prompt templates with performance metrics
- **`weighting_methodologies`**: Mathematical weighting schemes and algorithms
- **`experiments`**: Research experiment definitions and configurations
- **`runs`**: Individual analysis runs with complete provenance
- **`documents`**: Corpus documents with stable identifiers and metadata

### Version Control
- **Component versioning**: Every framework, prompt, and weighting scheme versioned
- **Experimental provenance**: Complete audit trail from input to output
- **Database migrations**: Alembic-managed schema evolution
- **Backup procedures**: Automated backup and recovery systems

### Research Workflow Integration
```bash
# Database operations
python check_database.py                    # Verify connection and schema
python scripts/setup_database.py           # Initialize or update schema
python -c "from alembic import command; from alembic.config import Config; cfg = Config('alembic.ini'); command.upgrade(cfg, 'head')"  # Apply migrations
```

## Academic Workflow

### 1. Experimental Design
```bash
# Create experiment configuration (using any framework)
python scripts/create_experiment.py --name "discourse_analysis_2024" --framework civic_virtue --prompt hierarchical_v2_1_0

# Batch processing setup
python scripts/setup_batch_analysis.py experiments/discourse_analysis_2024.yaml
```

### 2. Data Collection
```bash
# Process corpus of persuasive texts (any domain)
python scripts/intelligent_ingest.py corpus/raw_texts/ --confidence-threshold 80

# Validate corpus quality
python scripts/corpus_status.py --validate-metadata
```

### 3. Analysis Execution
```bash
# Run systematic analysis
python scripts/run_batch_analysis.py experiments/discourse_analysis_2024.yaml

# Monitor progress
python scripts/check_analysis_status.py --experiment discourse_analysis_2024
```

### 4. Statistical Analysis
```bash
# Export for academic analysis
python scripts/export_academic_data.py --experiment discourse_analysis_2024 --format all

# Generate statistical reports
Rscript analysis_results/discourse_analysis_2024/statistical_analysis.R

# Create publication visualizations
python scripts/create_publication_figures.py --experiment discourse_analysis_2024
```

### 5. Replication Package
```bash
# Generate complete replication package
python scripts/create_replication_package.py --experiment discourse_analysis_2024

# Validate replication package
python scripts/validate_replication.py replication_packages/discourse_analysis_2024/
```

## Development

### Environment Setup
```bash
# Setup development environment (required for each session)
source scripts/setup_dev_env.sh

# Verify imports are working
python -c "from src.narrative_gravity.engine import NarrativeGravityWellsCircular; print('✅ Imports working!')"
```

### Contributing to Framework Development
```bash
# Create new framework
mkdir frameworks/my_new_framework
# Edit framework.json following v2.0 specification

# Validate framework
python scripts/validate_framework_spec.py frameworks/my_new_framework/framework.json

# Import to database
python scripts/framework_sync.py import my_new_framework
```

### Testing
```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests  
python -m pytest tests/integration/ -v

# Run end-to-end tests
python -m pytest tests/e2e/ -v
```

## Project Structure

The project is organized for academic research workflows:

```
narrative_gravity_analysis/
├── 🔬 Research Pipeline
│   ├── src/narrative_gravity/           # Core analysis modules
│   │   ├── engine_circular.py          # Circular coordinate analysis engine
│   │   ├── framework_manager.py        # Framework management system
│   │   ├── models/                     # Database models and schemas
│   │   ├── academic/                   # Academic export and analysis tools
│   │   └── corpus/                     # Corpus management and ingestion
│   ├── scripts/                        # CLI tools and utilities
│   └── frameworks/                     # Framework specifications (v2.0)
│
├── 🗄️ Data Management  
│   ├── corpus/                         # Research corpus with FAIR compliance
│   ├── analysis_results/               # Analysis outputs and visualizations
│   ├── exports/academic_formats/       # Academic datasets and templates
│   └── schemas/                        # JSON schemas and specifications
│
├── 📚 Documentation & Research
│   ├── docs/                          # Complete documentation suite
│   │   ├── architecture/              # System architecture
│   │   ├── specifications/            # Technical specifications
│   │   ├── user-guides/              # User and workflow guides
│   │   └── development/              # Development documentation
│   ├── paper/                         # Academic paper development
│   └── tests/                         # Comprehensive test suite
│
└── 🏗️ Infrastructure
    ├── launch.py                      # Backend services launcher
    ├── alembic/                       # Database migrations
    ├── logs/                          # System logs
    └── archive/deprecated_interfaces/ # Archived frontend work
```

## Citation

If you use this software in your research, please cite:

```bibtex
@software{narrative_gravity_maps,
  title={Narrative Gravity Maps: A Quantitative Framework for Analyzing Persuasive Narratives},
  author={[Your Name]},
  year={2025},
  url={https://github.com/yourusername/narrative_gravity_analysis},
  version={2.0}
}
```

For the academic paper (when published):
```bibtex
@article{narrative_gravity_maps_paper,
  title={Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives},
  author={[Your Name]},
  journal={[Journal Name]},
  year={2025},
  note={Software available at https://github.com/yourusername/narrative_gravity_analysis}
}
```

## License

Copyright (c) 2025 Jeff Whatcott. All rights reserved.

This project is proprietary software. No part of this software may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the copyright holder. See the [LICENSE](LICENSE) file for complete terms.

## Support and Documentation

- **📖 Documentation**: See `docs/` directory for comprehensive guides
- **🐛 Issues**: Report bugs and request features via GitHub Issues
- **💬 Discussions**: Academic questions and methodology discussions welcome
- **📧 Contact**: [Your email for academic collaboration]

---

**🎯 Research Focus**: This platform prioritizes robust academic methodology over user interface polish. All frontend development has been archived to focus resources on core research capabilities, statistical validation, and publication preparation.

## 🚨 **BEFORE BUILDING ANYTHING NEW**

**Rule: Search production code first, build in experimental!**

```bash
# ALWAYS run this before starting any new development:
python3 scripts/production/check_existing_systems.py "your functionality description"

# Check the production systems inventory:
cat docs/EXISTING_SYSTEMS_INVENTORY.md

# Check clean code organization standards:
cat docs/CODE_ORGANIZATION_STANDARDS.md
```

**Why?** This project has repeatedly built inferior versions of existing sophisticated systems. Example: Built "AI Academic Advisor" (file existence checks) to replace LLMQualityAssuranceSystem (6-layer mathematical validation).

**🏗️ New Clean Organization**:
- ✅ **Production**: `src/`, `scripts/production/`, `docs/specifications/` (stable, tested, documented)
- 🧪 **Experimental**: `experimental/`, `sandbox/` (iteration, prototypes, testing)  
- 🗑️ **Deprecated**: `deprecated/` (obsolete code - avoid using)

**🔄 Development Workflow**:
1. **Search first**: Use production search tool to find existing systems
2. **Enhance existing**: Improve production code rather than rebuilding
3. **Build in experimental**: New development starts in `experimental/`
4. **Promote when ready**: Move to production with quality checks
