# Narrative Gravity Maps - Project Structure

This document outlines the clean project organization after reorganization and cleanup in v2025.06.04.

## 📁 Core Application Files

```
narrative_gravity_analysis/
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── LICENSE                             # Project license
├── .gitignore                          # Git ignore rules
├── PROJECT_STRUCTURE.md               # This file
└── CHANGELOG.md                        # Version history
```

## 🚀 Application Components

```
├── launch_app.py                       # Application launcher
├── narrative_gravity_app.py            # Main Streamlit interface
├── narrative_gravity_elliptical.py     # Core analysis engine
├── framework_manager.py                # Framework switching system
├── generate_prompt.py                  # LLM prompt generator
├── create_generic_multi_run_dashboard.py # Universal multi-run dashboard system
└── env.example                         # Environment configuration template
```

## 🔧 Operational Infrastructure

```
├── scripts/                           # Startup and utility scripts
│   ├── run_api.py                     # FastAPI server startup
│   ├── run_celery.py                  # Celery worker startup
│   ├── setup_database.py              # Database setup utility
│   ├── run_flagship_analysis.py       # Analysis runner script
│   ├── run_golden_set_gpt4o.py        # Golden set analysis
│   └── README.md                      # Scripts documentation
│
├── src/                               # Source code modules
│   ├── api/                          # FastAPI application
│   ├── models/                       # Database models
│   ├── tasks/                        # Celery task definitions
│   ├── utils/                        # Utility functions
│   │   ├── api_costs.json            # API cost tracking
│   │   ├── cost_limits.json          # Cost management limits
│   │   └── manage_costs.py           # Cost management system
│   ├── prompts/                      # Prompt templates and management
│   │   ├── moral_rhetorical_posture_prompt.txt
│   │   ├── political_spectrum_prompt.txt
│   │   └── template_manager.py
│   └── cli/                          # Command line tools
│
├── alembic/                          # Database migrations
└── alembic.ini                       # Database migration config
```

## 📊 Data and Configuration

```
├── frameworks/                         # Framework definitions
│   ├── civic_virtue/                  # Primary framework
│   │   ├── framework.json             # Mathematical parameters
│   │   ├── dipoles.json               # Conceptual definitions
│   │   └── README.md                  # Framework documentation
│   ├── political_spectrum/            # Alternative framework
│   └── moral_rhetorical_posture/      # Communication style framework
│
├── config/                            # Active configuration (symlinks)
│   ├── dipoles.json -> ../frameworks/civic_virtue/dipoles.json
│   └── framework.json -> ../frameworks/civic_virtue/framework.json
│
├── schemas/                           # JSON schema definitions
│   ├── core_schema_v1.0.0.json       # Core document schema
│   ├── cv_extension_v1.0.0.json      # Civic virtue extension
│   └── README.md                      # Schema documentation
│
├── corpus/                            # Text corpus for analysis
│   └── golden_set/                   # Curated reference texts
│       └── presidential_speeches/    # Presidential speech collection
│
├── model_output/                      # Analysis results
│   ├── *.json                        # Analysis data
│   └── *.png                         # Generated visualizations
│
├── analysis_results/                  # Structured analysis outputs
│   └── golden_set_gpt4o_*/           # Golden set analysis results
│
├── test_results/                      # Test outputs and results
│   ├── *.json                        # Test analysis data
│   └── *.png                         # Test visualizations
│
└── reference_texts/                   # Sample texts for analysis
    ├── recent_us_presidents/          # Recent presidential speeches
    ├── other_texts/                   # Historical political texts
    └── synthetic_narratives/          # Generated test narratives
```

## 📚 Documentation

```
├── docs/                              # All documentation
│   ├── architecture/                  # Technical architecture
│   │   ├── COMPREHENSIVE_ARCHITECTURAL_REVIEW.md
│   │   ├── MODULAR_ARCHITECTURE.md
│   │   ├── STORAGE_ARCHITECTURE.md
│   │   ├── FRAMEWORK_ARCHITECTURE.md
│   │   └── PROMPT_ARCHITECTURE.md
│   │
│   ├── generalization/               # Multi-run dashboard documentation
│   │   ├── GENERIC_DASHBOARD_USAGE.md  # Comprehensive usage guide
│   │   └── GENERALIZATION_SUMMARY.md   # Technical transformation details
│   │
│   ├── user-guides/                  # User documentation
│   │   ├── CORPUS_TOOLING_SUMMARY.md
│   │   ├── EPIC_1_COMPLETION_SUMMARY.md
│   │   ├── GOLDEN_SET_SUMMARY.md
│   │   └── STREAMLIT_APP_STATUS.md
│   │
│   ├── api/                          # API documentation
│   │   └── CSV_FORMAT_STANDARD.md
│   │
│   ├── narrative_gravity_wells_paper.md # Academic paper
│   ├── API_COST_PROTECTION_GUIDE.md    # Cost management
│   ├── COST_MANAGEMENT_GUIDE.md         # Cost controls
│   ├── DIRECT_API_INTEGRATION.md        # API integration
│   ├── ENDPOINT_SETUP_GUIDE.md          # Setup instructions
│   ├── FOUR_LLM_INTEGRATION_SUMMARY.md  # Multi-LLM support
│   ├── MULTI_LLM_STATUS.md              # LLM status tracking
│   ├── PROGRESS_LOG.md                  # Development progress
│   ├── PROJECT_STATUS.md                # Current project status
│   ├── SYSTEM_UPGRADE_2025.md           # System upgrade notes
│   └── TESTING_GUIDE.md                 # Testing documentation
│
├── examples/                          # Usage examples and demos
│   ├── corpus_generation_demo.py      # Corpus generation example
│   ├── *.jsonl                       # Example JSONL files
│   └── sample_*.md                    # Sample documents
│
├── snapshots/                         # Project snapshots
│   └── obama_multirun_elliptical_v1/  # Obama multi-run snapshot
│
├── replication/                       # Paper replication materials
│   └── PAPER_REPLICATION.md           # Replication guide
│
└── dev_instructions/                  # Development instructions
    ├── COMPREHENSIVE_PROJECT_DOCUMENTATION.md
    ├── User Personas - Narrative Gravity Model.md
    └── [various development guides]
```

## 🗃️ Archive and Development History

```
├── archive/                           # Historical/backup files
│   ├── development_versions/          # Previous dashboard versions
│   │   ├── create_obama_elliptical_dashboard_v*.py
│   │   ├── create_obama_elliptical_enhanced_v*.py
│   │   ├── test_multi_run_obama.py
│   │   └── [various development iterations]
│   │
│   ├── test_outputs/                  # Development dashboard outputs
│   │   ├── obama_dashboard_v*.png
│   │   ├── obama_elliptical_enhanced*.png
│   │   └── [various test visualizations]
│   │
│   ├── experimental_tests/            # Experimental test files (NEW)
│   │   ├── test_trump_joint_*.py      # Trump analysis experiments
│   │   ├── test_comparative_*.py      # Comparative analysis tests
│   │   ├── test_multi_llm.py          # Multi-LLM testing
│   │   ├── debug_api_response.py      # API debugging tools
│   │   └── [various experimental scripts]
│   │
│   ├── temp_results/                  # Temporary analysis results (NEW)
│   │   ├── trump_joint_*.json         # Trump analysis results
│   │   ├── test_2025_analysis/        # 2025 test analysis
│   │   ├── test_balanced_analysis/    # Balanced analysis tests
│   │   └── test_results_direct_apis.json
│   │
│   └── RENAME_LOG.md                  # Historical rename log
│
├── tests/                            # Formal test suite
│   ├── integration/                  # Integration tests
│   ├── test_data/                    # Test data files
│   ├── test_results/                 # Test result outputs
│   ├── utilities/                    # Test utilities
│   └── README.md                     # Testing documentation
│
├── api_integration_upload/           # API integration materials
│   ├── COMPREHENSIVE_PROJECT_DOCUMENTATION.md
│   ├── SOURCE_CODE_SUMMARY.md
│   └── [various integration files]
│
└── venv/                             # Python virtual environment
```

## 🎯 Key Principles

### Clean Separation
- **Core files**: Application logic in root directory
- **Source code**: Organized modules in `src/` directory
- **Data**: Organized by type (frameworks, outputs, corpus)
- **Documentation**: Centralized in `docs/` with logical subdirectories
- **Archive**: Historical and experimental files moved out of active workspace

### Framework Architecture
- **Multiple frameworks**: Each in its own subdirectory
- **Active configuration**: Symlinks in `config/` point to active framework
- **Version management**: Prompts organized by framework and version
- **Extensibility**: Easy to add new frameworks without affecting existing ones

### Development Organization
- **Experimental work**: Archived in `archive/experimental_tests/`
- **Temporary results**: Organized in `archive/temp_results/`
- **Production code**: Clean separation in `src/` modules
- **Documentation**: Comprehensive guides in `docs/` hierarchy

### Maintainability
- **Clear naming**: Files and directories have descriptive names
- **Logical grouping**: Related files are grouped together
- **Documentation**: Each major component has associated documentation
- **Version control**: Clean `.gitignore` prevents clutter accumulation
- **Archive system**: Historical files preserved but organized

## 🔄 Daily Workflow

1. **Development**: Work with core files in root directory
2. **Analysis**: Results automatically saved to `model_output/`
3. **Framework switching**: Use `framework_manager.py` to change active framework
4. **Documentation**: Add development notes to `docs/` subdirectories
5. **Experimentation**: Use `archive/experimental_tests/` for temporary work
6. **Archive**: Move completed experimental work to appropriate archive directories

This structure supports both research use and software development while maintaining clarity and organization. The recent cleanup ensures that the root directory contains only essential files, with all experimental and temporary work properly archived. 