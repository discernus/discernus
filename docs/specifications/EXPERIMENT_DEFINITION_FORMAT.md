# Experiment Definition Format Specification

## Overview

This specification defines a declarative format for experiment definitions, enabling researchers to specify complex multi-dimensional experiments using structured configuration files rather than custom Python scripts.

## Use Case Example

**Research Scenario**: A researcher wants to analyze 4 texts (2 existing, 2 new) using 2 frameworks (1 new, 1 modified CV framework) across 2 specific LLMs with standard templates.

**Solution**: Create an experiment package with definition file + resources.

## Directory Structure

```
my_comparative_study/
├── experiment.json              # Main experiment definition
├── texts/                       # New texts to ingest
│   ├── new_speech_1.txt
│   └── new_speech_2.txt
├── frameworks/                  # New/modified frameworks
│   ├── my_innovation_framework.json
│   └── cv_modified_v2.json
├── prompts/                     # Custom prompt templates (optional)
│   └── evidence_focused_v1.json
├── metadata.json                # Study metadata
└── results/                     # Generated output directory
    ├── raw_data/
    ├── analysis_reports/
    └── qa_reports/
```

## Experiment Definition Format (`experiment.json`)

```json
{
  "experiment": {
    "name": "Cross-Framework Presidential Rhetoric Analysis",
    "version": "1.0.0",
    "description": "Comparative analysis of presidential rhetoric using innovation framework vs modified civic virtue",
    "hypothesis": "Innovation-focused framework will show different patterns than civic virtue in technology-era speeches",
    "research_context": "Testing new theoretical framework against established baseline",
    "tags": ["comparative", "framework-validation", "presidential-rhetoric"],
    "created_by": "researcher@university.edu",
    "created_date": "2025-06-13"
  },
  "texts": {
    "sources": [
      {
        "type": "existing",
        "text_id": "obama_inaugural_2009",
        "notes": "Baseline modern presidential rhetoric"
      },
      {
        "type": "existing", 
        "text_id": "biden_sotu_2024",
        "notes": "Technology-era policy discourse"
      },
      {
        "type": "new",
        "file_path": "texts/new_speech_1.txt",
        "text_id": "tech_ceo_address_2025",
        "metadata": {
          "title": "Technology Innovation Address",
          "author": "Tech CEO",
          "date": "2025-03-15",
          "document_type": "address"
        }
      },
      {
        "type": "new",
        "file_path": "texts/new_speech_2.txt", 
        "text_id": "academic_innovation_speech",
        "metadata": {
          "title": "Academic Innovation in Democracy",
          "author": "University President",
          "date": "2025-05-20",
          "document_type": "speech"
        }
      }
    ]
  },
  "frameworks": {
    "configurations": [
      {
        "type": "existing",
        "framework_id": "civic_virtue",
        "version": "v2025.06.12",
        "alias": "cv_baseline",
        "notes": "Standard civic virtue framework for comparison"
      },
      {
        "type": "modified",
        "base_framework_id": "civic_virtue", 
        "file_path": "frameworks/cv_modified_v2.json",
        "alias": "cv_innovation_focused",
        "notes": "CV framework with innovation-oriented weighting"
      },
      {
        "type": "new",
        "file_path": "frameworks/my_innovation_framework.json",
        "alias": "innovation_framework",
        "notes": "Novel framework focusing on innovation vs tradition dimensions"
      }
    ]
  },
  "models": {
    "evaluators": [
      {
        "model": "gpt-4.1-mini",
        "alias": "gpt4_mini",
        "parameters": {
          "temperature": 0.1,
          "max_tokens": 4000
        }
      },
      {
        "model": "claude-3-sonnet",
        "alias": "claude3",
        "parameters": {
          "temperature": 0.1,
          "max_tokens": 4000
        }
      }
    ]
  },
  "templates": {
    "prompt_templates": [
      {
        "type": "existing",
        "template_id": "hierarchical_v2.1.0",
        "alias": "standard_hierarchical"
      }
    ],
    "weighting_schemes": [
      {
        "type": "existing",
        "scheme_id": "standard",
        "alias": "standard_weighting"
      }
    ]
  },
  "execution": {
    "design_matrix": {
      "type": "full_factorial",
      "dimensions": ["texts", "frameworks", "models"],
      "fixed_components": {
        "prompt_template": "standard_hierarchical",
        "weighting_scheme": "standard_weighting"
      }
    },
    "replication": {
      "runs_per_combination": 3,
      "randomize_order": true
    },
    "quality_assurance": {
      "enabled": true,
      "confidence_threshold": 0.7,
      "require_second_opinion_below": 0.5
    },
    "cost_controls": {
      "max_total_cost": 5.00,
      "cost_per_run_limit": 0.10,
      "confirm_before_execution": true
    }
  },
  "outputs": {
    "data_formats": ["csv", "feather", "json", "stata_dta"],
    "include_qa_reports": true,
    "include_visualizations": true,
    "academic_export": {
      "enabled": true,
      "primary_format": "r_package",
      "additional_formats": ["python_package", "stata_package"],
      "statistical_analysis": {
        "descriptive_statistics": true,
        "reliability_analysis": true,
        "comparative_analysis": true,
        "correlation_matrices": true,
        "significance_tests": ["t_test", "anova", "chi_square"]
      },
      "visualization_package": {
        "individual_plots": true,
        "comparative_plots": true,
        "interactive_html": true,
        "publication_ready_pdf": true,
        "custom_themes": ["academic", "presentation"]
      },
      "replication_package": {
        "include_code": true,
        "include_data": true,
        "include_documentation": true,
        "analysis_scripts": ["r_analysis.R", "python_analysis.py", "stata_analysis.do"],
        "readme_documentation": true
      },
      "manuscript_support": {
        "methods_section": true,
        "results_tables": true,
        "figure_captions": true,
        "supplementary_materials": true
      }
    }
  }
}
```

## Execution Workflow

### Step 1: Prepare Experiment Package

```bash
# Create experiment directory
mkdir my_comparative_study
cd my_comparative_study

# Add new texts
mkdir texts
cp /path/to/tech_ceo_speech.txt texts/new_speech_1.txt
cp /path/to/academic_speech.txt texts/new_speech_2.txt

# Add new/modified frameworks  
mkdir frameworks
# (Create framework JSON files using framework specification)

# Create experiment definition
# (Use experiment.json template above)
```

### Step 2: Validate Experiment Definition

```bash
# Validate experiment specification
python3 scripts/validate_experiment.py my_comparative_study/

# Output:
# ✅ Experiment definition valid
# ✅ All text files found
# ✅ Framework specifications valid  
# ✅ Model configurations valid
# 📊 Estimated execution: 36 runs, ~$1.20, 45 minutes
```

### Step 3: Execute Experiment

```bash
# Execute experiment with QA integration
python3 scripts/execute_experiment.py my_comparative_study/ --qa-enhanced

# Interactive confirmation:
# 🧪 Experiment: Cross-Framework Presidential Rhetoric Analysis
# 📊 Design Matrix: 4 texts × 3 frameworks × 2 models × 3 runs = 72 total runs
# 💰 Estimated cost: $1.20 (within $5.00 limit)
# ⏱️  Estimated time: 45 minutes
# 
# Proceed? [y/N]: y
```

### Step 4: Automated Execution

```bash
# System automatically:
# 1. Ingests new texts using intelligent ingestion
# 2. Validates and registers new frameworks  
# 3. Executes full experimental matrix
# 4. Applies QA validation to all runs
# 5. Generates academic exports and reports
# 6. Creates replication package
```

## Framework Definition Format (`frameworks/*.json`)

```json
{
  "framework_specification": {
    "name": "Innovation vs Tradition Framework",
    "version": "v1.0.0",
    "description": "Framework analyzing rhetoric along innovation-tradition dimensions",
    "theoretical_foundation": "Technology adoption theory, institutional change theory",
    "domain": "technology_policy",
    "coordinate_system": "circular"
  },
  "wells": [
    {
      "name": "Innovation",
      "description": "Emphasis on technological progress, disruption, future-orientation",
      "angle_degrees": 0,
      "well_type": "constructive",
      "weight": 1.0
    },
    {
      "name": "Adaptation", 
      "description": "Balanced approach to technological change with institutional stability",
      "angle_degrees": 45,
      "well_type": "constructive", 
      "weight": 0.8
    },
    {
      "name": "Tradition",
      "description": "Emphasis on established institutions, proven approaches, stability",
      "angle_degrees": 180,
      "well_type": "constructive",
      "weight": 0.9
    },
    {
      "name": "Resistance",
      "description": "Opposition to change, technological skepticism, status quo bias",
      "angle_degrees": 225, 
      "well_type": "problematic",
      "weight": 1.0
    }
  ],
  "positioning_strategy": "dipole_clustering",
  "validation_status": "experimental",
  "academic_citations": [
    "Rogers, E. (2003). Diffusion of Innovations",
    "March, J. (1991). Exploration and Exploitation in Organizational Learning"
  ]
}
```

## Benefits of This Approach

### For Researchers
- **Declarative**: Specify what you want, not how to code it
- **Reusable**: Share experiment definitions with colleagues
- **Traceable**: Complete provenance from definition to results
- **Validatable**: Check feasibility before execution
- **Extensible**: Add new resources without changing core definition

### For Reproducibility  
- **Self-Contained**: Everything needed for replication in one package
- **Version Controlled**: Track changes to experimental design
- **Platform Independent**: JSON format works across tools
- **Academic Standard**: Meets publication requirements for transparency

### For System Integration
- **QA Enhanced**: Automatic integration with 6-layer quality assurance
- **Cost Controlled**: Built-in budget management and confirmation
- **Resource Management**: Intelligent handling of new vs existing resources
- **Output Standardized**: Consistent academic export formats

## Implementation Plan

### Phase 1: Core Infrastructure
- `scripts/validate_experiment.py` - Experiment definition validation
- `scripts/execute_experiment.py` - Automated execution engine
- JSON schema validation for experiment definitions
- Resource ingestion pipeline integration

### Phase 2: Enhanced Features  
- Interactive experiment builder CLI tool
- Web interface for experiment definition
- Template library for common experimental designs
- Advanced design matrix generators

### Phase 3: Advanced Capabilities
- Experiment scheduling and queuing
- Distributed execution across multiple LLM providers
- Real-time progress monitoring and cost tracking
- Automatic result interpretation and reporting

## Example Execution Output

```
🧪 Executing Experiment: Cross-Framework Presidential Rhetoric Analysis
📋 Validated experiment definition: ✅ 
📥 Ingesting new texts: ✅ 2 texts processed
🔧 Registering frameworks: ✅ 2 new frameworks validated
🚀 Starting experimental matrix execution...

Progress: [████████████████████████████████████████] 72/72 runs (100%)
⏱️  Total time: 43m 15s
💰 Total cost: $1.18 (within budget)
🔍 QA Summary: 68 HIGH confidence, 4 MEDIUM confidence, 0 LOW confidence

📊 Generating reports...
✅ Academic data export: my_comparative_study/results/academic_export_20250613.csv
✅ QA validation report: my_comparative_study/results/qa_validation_report.json  
✅ Visualization package: my_comparative_study/results/visualizations/
✅ Replication package: my_comparative_study/results/replication_package.zip

🎉 Experiment complete! Results ready for analysis.
```

## Academic Output Format Specifications

### Data Export Formats

**Available Data Formats:**
- `"csv"` - Universal compatibility, Excel-readable
- `"feather"` - Optimized for R/Python, fast loading
- `"json"` - Python-friendly with metadata
- `"stata_dta"` - Native Stata format (requires pyreadstat)
- `"parquet"` - Efficient columnar format for large datasets
- `"excel"` - Excel workbook with multiple sheets

### Academic Package Types

**Primary Format Options:**
- `"r_package"` - Complete R analysis package with .Rmd templates
- `"python_package"` - Jupyter notebooks with pandas/scipy analysis
- `"stata_package"` - .do files with publication-ready analysis
- `"spss_package"` - SPSS syntax files and data formats
- `"universal"` - Multi-platform package with all formats

**R Package Contents:**
```
study_name_r_package/
├── data/
│   ├── experiment_data.feather
│   ├── qa_validation_results.csv
│   └── metadata.json
├── analysis/
│   ├── descriptive_analysis.Rmd
│   ├── reliability_analysis.Rmd
│   ├── comparative_analysis.Rmd
│   └── visualization_templates.R
├── output/
│   ├── figures/
│   ├── tables/
│   └── reports/
└── README.md
```

**Python Package Contents:**
```
study_name_python_package/
├── data/
│   ├── experiment_data.feather
│   ├── qa_validation_results.csv
│   └── metadata.json
├── notebooks/
│   ├── 01_descriptive_analysis.ipynb
│   ├── 02_reliability_analysis.ipynb
│   ├── 03_comparative_analysis.ipynb
│   └── 04_visualization_dashboard.ipynb
├── scripts/
│   ├── analysis_functions.py
│   └── plotting_utilities.py
└── requirements.txt
```

### Statistical Analysis Options

**Descriptive Statistics:**
- Summary statistics (mean, median, std, CV)
- Distribution analysis with normality tests
- Missing data patterns and quality metrics
- Text-level and well-level summaries

**Reliability Analysis:**
- Coefficient of variation across runs
- Intraclass correlation coefficients
- Cronbach's alpha for internal consistency
- Test-retest reliability metrics

**Comparative Analysis:**
- ANOVA for group comparisons
- Post-hoc tests (Tukey HSD, Bonferroni)
- Effect size calculations (Cohen's d, eta-squared)
- Non-parametric alternatives (Kruskal-Wallis, Mann-Whitney)

**Advanced Statistics:**
- Correlation matrices with significance tests
- Regression analysis (linear, logistic)
- Factor analysis and dimensionality reduction
- Cluster analysis and pattern detection

### Visualization Package Options

**Individual Plots:**
- Well score distributions (histograms, boxplots)
- Narrative positioning scatter plots
- QA confidence score distributions
- Framework fit score analysis

**Comparative Plots:**
- Multi-text comparison matrices
- Framework comparison heatmaps
- Model consistency analysis
- Reliability trend analysis

**Interactive Visualizations:**
- Plotly-based interactive dashboards
- Hoverable data points with full context
- Zoomable narrative positioning maps
- Filterable multi-dimensional views

**Publication-Ready Outputs:**
- High-resolution PDF figures (300+ DPI)
- Vector graphics (SVG, EPS) for journals
- Customizable themes (APA style, journal-specific)
- Figure captions and numbering

### Manuscript Support Features

**Methods Section Generation:**
```markdown
## Methods

### Narrative Analysis Framework
This study employed the Civic Virtue framework (v2025.06.12) for analyzing 
presidential discourse. The framework positions ten conceptual wells on a 
circular coordinate system, measuring rhetoric along five dipoles: 
Dignity-Tribalism, Justice-Resentment, Truth-Manipulation, 
Pragmatism-Fear, and Hope-Fantasy.

### Quality Assurance Protocol
All analyses underwent 6-layer quality validation including input validation,
LLM response verification, statistical coherence checking, mathematical 
consistency verification, cross-validation, and anomaly detection.
```

**Results Tables Generation:**
- APA-style statistical tables
- Correlation matrices with significance indicators
- Descriptive statistics tables
- ANOVA results with effect sizes

**Supplementary Materials:**
- Complete analysis provenance logs
- Raw data with data dictionary
- Code reproducibility documentation
- Quality assurance detailed reports

### Example Academic Workflow Configurations

**Political Science Researcher (R-focused):**
```json
"academic_export": {
  "primary_format": "r_package",
  "statistical_analysis": {
    "descriptive_statistics": true,
    "comparative_analysis": true,
    "significance_tests": ["anova", "t_test"]
  },
  "visualization_package": {
    "publication_ready_pdf": true,
    "custom_themes": ["academic"]
  },
  "manuscript_support": {
    "methods_section": true,
    "results_tables": true
  }
}
```

**Computational Social Science (Multi-platform):**
```json
"academic_export": {
  "primary_format": "python_package",
  "additional_formats": ["r_package", "stata_package"],
  "statistical_analysis": {
    "descriptive_statistics": true,
    "reliability_analysis": true,
    "correlation_matrices": true
  },
  "replication_package": {
    "analysis_scripts": ["python_analysis.py", "r_analysis.R", "stata_analysis.do"]
  }
}
```

**Psychology Researcher (SPSS/Stata focus):**
```json
"academic_export": {
  "primary_format": "stata_package", 
  "additional_formats": ["spss_package"],
  "data_formats": ["stata_dta", "csv"],
  "statistical_analysis": {
    "reliability_analysis": true,
    "significance_tests": ["t_test", "chi_square"]
  }
}
```

This approach transforms complex experimental design from a programming task into a declarative specification task, dramatically lowering the barrier for sophisticated comparative research. 