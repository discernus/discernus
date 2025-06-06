# Narrative Gravity Maps - Project Structure

This document outlines the clean project organization after reorganization in v2025.06.04.

## 📁 Core Application Files

```
narrative_gravity_analysis/
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── LICENSE                             # Project license
├── .gitignore                          # Git ignore rules
└── PROJECT_STRUCTURE.md               # This file
```

## 🚀 Application Components

```
├── launch_app.py                       # Application launcher
├── narrative_gravity_app.py            # Main Streamlit interface
├── narrative_gravity_elliptical.py     # Core analysis engine
├── framework_manager.py                # Framework switching system
└── generate_prompt.py                  # LLM prompt generator
```

## 🔧 Operational Scripts

```
├── scripts/                           # Startup and utility scripts
│   ├── run_api.py                     # FastAPI server startup
│   ├── run_celery.py                  # Celery worker startup
│   ├── setup_database.py              # Database setup utility
│   └── README.md                      # Scripts documentation
│
└── alembic.ini                        # Database migration config (root required)
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
├── model_output/                      # Analysis results
│   ├── *.json                        # Analysis data
│   └── *.png                         # Generated visualizations
│
│
└── reference_texts/                   # Sample texts for analysis
    ├── lincoln_1865_second_inaugural.txt
    ├── mandela_1994_inaugural.txt
    └── [various other political texts]
```

## 📚 Documentation

```
├── docs/                              # All documentation
│   ├── development/                   # Development notes
│   │   ├── MODULAR_ARCHITECTURE.md
│   │   ├── STORAGE_ARCHITECTURE.md
│   │   ├── PROJECT_SNAPSHOT_v2.0.md
│   │   ├── DEVELOPMENT_ROADMAP.md
│   │   ├── USER_STORIES.md
│   │   └── [various technical docs]
│   │
│   └── examples/                      # Usage examples
│       ├── STREAMLIT_QUICKSTART.md
│       └── WORKFLOW_DEMO.md
│
└── narrative_gravity_wells_paper.md   # Academic paper (root level)
```

## 🗃️ Archive and Tests

```
├── archive/                           # Historical/backup files
│   └── model_output_backup_old_weights/
│

├── tests/                            # Test files (future)
└── venv/                             # Python virtual environment
```

## 🎯 Key Principles

### Clean Separation
- **Core files**: Application logic in root directory
- **Data**: Organized by type (frameworks, outputs, prompts)
- **Documentation**: Centralized in `docs/` with logical subdirectories
- **Archive**: Historical files moved out of active workspace

### Framework Architecture
- **Multiple frameworks**: Each in its own subdirectory
- **Active configuration**: Symlinks in `config/` point to active framework
- **Version management**: Prompts organized by framework and version
- **Extensibility**: Easy to add new frameworks without affecting existing ones

### Maintainability
- **Clear naming**: Files and directories have descriptive names
- **Logical grouping**: Related files are grouped together
- **Documentation**: Each major component has associated documentation
- **Version control**: Clean `.gitignore` prevents clutter accumulation

## 🔄 Daily Workflow

1. **Development**: Work with core files in root directory
2. **Analysis**: Results automatically saved to `model_output/`
3. **Framework switching**: Use `framework_manager.py` to change active framework
4. **Documentation**: Add development notes to `docs/development/`
5. **Archive**: Move old files to `archive/` when no longer actively needed

This structure supports both research use and software development while maintaining clarity and organization. 