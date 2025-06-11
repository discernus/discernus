# Academic Software Installation Guide - Priority 3

**Status**: ✅ Complete Integration Ready  
**Priority 3 Infrastructure**: Fully implemented and tested  
**Academic Tool Support**: Python, R, Stata, Jupyter integration

## 🎯 Overview

Priority 3 Academic Tool Integration is **already complete** with comprehensive data export, analysis template generation, and documentation tools. This guide covers optional software installation to enable **execution** of generated analysis templates.

**✅ What's Already Working:**
- Data export to all academic formats (CSV, Feather, Stata, JSON)
- AI-generated analysis templates (Jupyter, R, Stata scripts)
- Academic documentation generation
- Complete CLI tool suite
- Statistical packages installed (scipy, pyreadstat)

**📋 Optional Software Installation:**
This guide covers installing academic software to **execute** the generated templates:
- Anaconda/Jupyter for notebook execution
- RStudio for R script execution  
- Stata for publication-grade statistical analysis

## 🚀 Quick Start - Priority 3 is Ready Now!

**You can use Priority 3 immediately without installing additional software:**

```bash
# Export your experimental data in academic formats
python src/narrative_gravity/cli/export_academic_data.py \
    --study-name your_study_2025 \
    --format all \
    --frameworks civic_virtue,political_spectrum

# Generate analysis templates
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --study-name your_study_2025 \
    --templates all

# Generate academic documentation
python src/narrative_gravity/cli/generate_documentation.py \
    --study-name your_study_2025 \
    --doc-type all

# Run complete pipeline
python src/narrative_gravity/cli/academic_pipeline.py \
    --study-name your_study_2025 \
    --execute-all
```

**This will create publication-ready data and analysis code without requiring any additional software installation.**

## 📊 Current Priority 3 Capabilities

### ✅ **Implemented and Working**

**Data Export Pipeline**:
- PostgreSQL → CSV (universal compatibility)
- PostgreSQL → Feather (R-optimized format) 
- PostgreSQL → JSON (Python with complete metadata)
- PostgreSQL → Stata .dta (publication-grade format)
- Complete data dictionaries and variable documentation

**Analysis Template Generation**:
- **Jupyter Notebooks**: Statistical analysis with scipy integration
- **R Scripts**: Advanced modeling with tidyverse, lme4, ggplot2
- **Stata Scripts**: Publication-ready analysis with LaTeX export

**Academic Documentation**:
- **Methodology Papers**: Auto-generated from experimental data
- **Statistical Reports**: APA-style formatting with significance testing
- **Replication Packages**: Complete ZIP packages with data, code, docs

**Integration & Validation**:
- **Master Pipeline Orchestrator**: Single-command execution
- **Comprehensive Testing**: Data integrity, template validation, integration tests
- **Quality Assurance**: Academic standards compliance verification

## 🔧 Optional Software Installation

### Option 1: Python-Only Workflow (Recommended)

**Already Complete - No Installation Needed!**

Your current setup with Priority 3 provides everything needed for academic analysis:
- Data export in all formats ✅
- Statistical analysis code generation ✅  
- Academic documentation generation ✅
- Publication-ready outputs ✅

**To execute Jupyter notebooks** (optional):
```bash
# Jupyter is likely already available in your venv
pip install jupyter

# Run generated notebooks
jupyter lab exports/academic_formats/notebooks/your_study_exploration.ipynb
```

### Option 2: Anaconda Installation (Enhanced Python)

**Purpose**: Enhanced Python environment with pre-installed scientific packages

**Installation**:
```bash
# Download Anaconda
curl -O https://repo.anaconda.com/archive/Anaconda3-2023.09-MacOSX-arm64.sh

# Install
bash Anaconda3-2023.09-MacOSX-arm64.sh

# Activate
conda activate base

# Your Priority 3 tools will work with Anaconda Python
```

**Benefits**:
- Pre-installed scientific packages
- Conda environment management
- Enhanced Jupyter notebook experience

### Option 3: R and RStudio Installation

**Purpose**: Execute generated R scripts for advanced statistical modeling

**Installation**:
```bash
# Install R (macOS)
brew install r

# Or download from: https://cran.r-project.org/bin/macosx/

# Install RStudio Desktop
# Download from: https://posit.co/download/rstudio-desktop/
```

**Required R Packages** (install in R/RStudio):
```r
# Install required packages
install.packages(c(
    "tidyverse",      # Data manipulation
    "arrow",          # Feather format support
    "lme4",           # Mixed-effects models
    "lmerTest",       # Statistical testing
    "performance",    # Model assessment
    "ggplot2",        # Visualization
    "corrplot",       # Correlation plots
    "psych"           # Psychological statistics
))
```

**Execute Generated R Scripts**:
```bash
# Your Priority 3 pipeline generates R scripts automatically
Rscript exports/academic_formats/r_scripts/your_study_analysis.R
```

### Option 4: Stata Installation

**Purpose**: Publication-grade statistical analysis with LaTeX export

**Installation**:
- Purchase Stata license from: https://www.stata.com/
- Install Stata IC/SE/MP based on your needs
- Configure PyStata bridge for Python integration

**PyStata Configuration** (after Stata installation):
```bash
# Install PyStata in your venv
pip install stata_setup

# Configure PyStata (run in Python)
python -c "
import stata_setup
stata_setup.config('path/to/stata', 'be')  # 'be', 'se', 'mp'
"
```

**Execute Generated Stata Scripts**:
```bash
# Your Priority 3 pipeline generates Stata .do files automatically
stata-se do exports/academic_formats/stata_scripts/your_study_publication.do
```

## 🔗 Priority 3 Integration Architecture

### Database Integration (✅ Complete)

**PostgreSQL Schema Support**:
- `experiments` table: Experiment metadata and framework versions
- `runs` table: Individual LLM analysis results with scores
- `framework_versions` table: Framework definitions and versioning
- `prompt_templates` table: Prompt templates with versioning

**Data Flow**:
```
CLI Batch Analysis → PostgreSQL → Priority 3 Export → Academic Formats
                                                   ↓
                  Publication-Ready Analysis ← Template Generation
```

### Multi-Tool Workflow (✅ Complete)

**Seamless Integration**:
1. **Data Export**: One command exports to all academic formats
2. **Template Generation**: AI-generated analysis code for Python/R/Stata
3. **Documentation**: Auto-generated methodology and replication guides
4. **Validation**: Comprehensive testing and quality assurance

**Example Complete Workflow**:
```bash
# 1. Export your experimental data
python src/narrative_gravity/cli/export_academic_data.py \
    --study-name validation_study_2025 \
    --frameworks civic_virtue,political_spectrum \
    --start-date 2025-06-01 \
    --format all

# 2. Generate analysis templates  
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --study-name validation_study_2025 \
    --templates all

# 3. Generate documentation
python src/narrative_gravity/cli/generate_documentation.py \
    --study-name validation_study_2025 \
    --doc-type all

# 4. Create replication package
python src/narrative_gravity/cli/export_academic_data.py \
    --study-name validation_study_2025 \
    --replication-package \
    --description "Complete validation study for LLM narrative analysis"

# 5. Execute pipeline orchestrator (all-in-one)
python src/narrative_gravity/cli/academic_pipeline.py \
    --study-name validation_study_2025 \
    --execute-all
```

## ✅ Validation and Testing

### Automated Testing (✅ Complete)

**Test your Priority 3 installation**:
```bash
# Run Priority 3 integration tests
python -m pytest tests/integration/test_priority3_academic_pipeline.py -v

# Test statistical packages
python -c "
import scipy.stats
import pyreadstat
import pandas as pd
print('✅ All Priority 3 packages working correctly!')
"

# Test template generation
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --study-name installation_test \
    --templates jupyter
```

### Data Integrity Validation

**Verify academic data export**:
```bash
# Test data export with validation
python src/narrative_gravity/cli/export_academic_data.py \
    --study-name integrity_test \
    --format csv,json \
    --output-dir test_export

# Verify files created
ls test_export/
# Should show: integrity_test.csv, integrity_test.json, integrity_test_data_dictionary.json
```

### End-to-End Pipeline Testing

**Complete workflow validation**:
```bash
# Run complete pipeline with validation
python src/narrative_gravity/cli/academic_pipeline.py \
    --study-name end_to_end_test \
    --execute-all

# Check validation results
cat academic_pipeline_output/validation/end_to_end_test_results.json
```

## 📋 Troubleshooting

### Common Issues and Solutions

**Issue**: "Module not found" errors
**Solution**: Ensure development environment is set up:
```bash
source scripts/setup_dev_env.sh
python -c "from src.narrative_gravity.academic import data_export; print('✅ Priority 3 imports working')"
```

**Issue**: Database connection errors
**Solution**: Verify PostgreSQL connection:
```bash
python check_database.py
```

**Issue**: Statistical packages missing
**Solution**: Install required packages:
```bash
pip install scipy==1.13.1 pyreadstat==1.2.7
```

**Issue**: Generated code execution fails
**Solution**: Install optional software (Anaconda, R, Stata) as needed, or use generated code as templates

### Priority 3 Status Verification

**Verify complete Priority 3 implementation**:
```bash
# Check all academic modules exist
ls src/narrative_gravity/academic/
# Should show: __init__.py, data_export.py, analysis_templates.py, documentation.py

# Check all CLI tools exist  
ls src/narrative_gravity/cli/*academic* src/narrative_gravity/cli/*analysis* src/narrative_gravity/cli/*documentation*
# Should show all Priority 3 CLI tools

# Test complete functionality
python src/narrative_gravity/cli/academic_pipeline.py --help
```

## 🎯 Next Steps After Installation

### Immediate Use (No Additional Software Needed)

1. **Export Your Data**: Use existing experimental data in PostgreSQL
2. **Generate Templates**: Create analysis code for your preferred tools
3. **Generate Documentation**: Create methodology papers and replication guides
4. **Validation**: Run comprehensive pipeline testing

### Enhanced Workflow (With Optional Software)

1. **Jupyter Analysis**: Execute generated notebooks for interactive exploration
2. **R Statistical Modeling**: Run advanced statistical analysis and visualization
3. **Stata Publication Analysis**: Generate publication-ready statistical tables
4. **Integrated Workflow**: Seamless data → analysis → publication pipeline

## 📊 Summary

**Priority 3 Academic Tool Integration is complete and functional without requiring any additional software installation.** The infrastructure provides:

- ✅ **Data Export**: All academic formats from PostgreSQL
- ✅ **Analysis Templates**: AI-generated code for Python/R/Stata  
- ✅ **Documentation**: Methodology papers and replication packages
- ✅ **Integration**: Complete CLI tool suite with validation
- ✅ **Testing**: Comprehensive test coverage and quality assurance

**Optional software installation** (Anaconda, R, Stata) enables **execution** of generated templates but is not required for the core Priority 3 functionality.

**You can begin using the academic analysis pipeline immediately with your existing PostgreSQL experimental data.**

---

**Generated**: January 6, 2025  
**Priority 3 Status**: ✅ Complete and Production-Ready  
**Integration Level**: Full PostgreSQL → Academic Tools → Publication Materials 