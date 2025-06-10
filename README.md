# Narrative Gravity Maps v2.0

**A quantitative methodology for analyzing the moral forces driving persuasive narratives**

![Narrative Gravity Wells Analysis](https://img.shields.io/badge/analysis-narrative--gravity--wells-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Version](https://img.shields.io/badge/version-2.0-orange.svg)

## Overview

**Narrative Gravity Maps** provide a general quantitative methodology for mapping moral and rhetorical forces within persuasive texts. The methodology positions conceptual "gravity wells" on a coordinate system, where each well represents a distinct orientation that exerts attractive force proportional to a narrative's alignment with that orientation.

**This methodology can be instantiated through multiple specialized frameworks:**

- **🏛️ Civic Virtue Framework**: Our most advanced implementation for moral analysis of political discourse
- **🗳️ Political Spectrum Framework**: Focused on left-right political positioning  
- **🎭 Rhetorical Posture Framework**: Emphasizing communication style and approach

**Version 2.0 introduces a modular architecture** that separates conceptual definitions from mathematical implementation, enabling:

- ✅ **Full Backward Compatibility** - All existing code and JSON files work unchanged
- 🎯 **Custom Dipole Systems** - Define your own moral dimensions
- 🔧 **Flexible Weighting** - Experiment with different mathematical frameworks  
- 🤖 **Multi-LLM Support** - Generate prompts for any AI model
- 📊 **Automated Analysis** - Streamlined prompt generation and processing
- 🏗️ **Multi-Framework Storage** - Organized framework and prompt management

## Quick Start

### Basic Analysis
```python
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical, load_analysis_data

# Initialize analyzer
analyzer = NarrativeGravityWellsElliptical()

# Load and visualize analysis
data = load_analysis_data("model_output/sample_analysis.json")
output_path = analyzer.create_visualization(data)
print(f"Visualization saved: {output_path}")
```

### Multi-Run Analysis Dashboard (NEW)
```python
from create_generic_multi_run_dashboard import create_dashboard

# Auto-detect everything from filename
fig = create_dashboard("results.json")

# Manual parameters for specific speaker/framework
fig = create_dashboard("results.json", 
                      speaker="Lincoln", 
                      year="1863", 
                      speech_type="Address",
                      framework="Civic Virtue")
```

### Command Line Usage
```bash
# Generate multi-run dashboard with auto-detection
python create_generic_multi_run_dashboard.py results.json

# Manual parameters
python create_generic_multi_run_dashboard.py results.json \
  --speaker "Kennedy" --year "1961" --speech-type "Inaugural"

# Test auto-detection capabilities
python test_auto_detection.py
```

### Framework Management & Prompt Generation
```bash
# List available frameworks
python framework_manager.py summary

# Switch to different framework
python framework_manager.py switch civic_virtue

# Generate prompts using unified template system
python generate_prompt.py --framework civic_virtue --mode interactive
python generate_prompt.py --framework political_spectrum --mode api

# Experimental prompt generation
python generate_prompt.py --framework civic_virtue --experiment-id scoring_methodology --variant treatment
```

## Installation

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- matplotlib
- seaborn  
- numpy

## Project Structure

The project is organized for clarity and maintainability:

```
narrative_gravity_analysis/
├── 🚀 Core Application
│   ├── frontend/                     # React Research Workbench (RECOMMENDED)
│   ├── launch.py                     # Backend services launcher
│   ├── narrative_gravity_elliptical.py # Core analysis engine
│   ├── framework_manager.py          # Framework management
│   └── generate_prompt.py            # LLM prompt generator
│
├── 🔧 Scripts & Operations
│   ├── scripts/run_api.py            # FastAPI server startup
│   ├── scripts/run_celery.py         # Celery worker startup
│   ├── scripts/setup_database.py     # Database setup utility
│   └── alembic.ini                   # Database migration config
│
├── 📊 Data & Configuration
│   ├── frameworks/                   # Framework definitions
│   │   ├── civic_virtue/            # Primary framework
│   │   ├── political_spectrum/      # Alternative framework
│   │   └── moral_rhetorical_posture/ # Communication style
│   ├── config/                      # Active framework (symlinks)
│   ├── model_output/                # Analysis results

│   └── reference_texts/             # Sample texts
│
├── 📚 Documentation  
│   ├── docs/architecture/           # System architecture docs
│   ├── docs/user-guides/           # User-facing guides
│   ├── docs/api/                   # API documentation
│   ├── docs/development/           # Development docs
│   ├── docs/examples/              # Usage examples
│   └── narrative_gravity_wells_paper.md # Academic paper
│
└── 🗃️ Archive & Tests
    ├── archive/                     # Historical files
    └── tests/                       # Test files
```

See `PROJECT_STRUCTURE.md` for detailed organization documentation.

### Configuration Files

#### `dipoles.json` - Conceptual Framework
Defines moral dimensions without mathematical parameters:
```json
{
  "dipoles": [
    {
      "name": "Identity",
      "positive": {
        "name": "Dignity",
        "description": "Affirms individual moral worth...",
        "language_cues": ["equal dignity", "inherent worth"]
      },
      "negative": {
        "name": "Tribalism",
        "description": "Prioritizes group dominance...", 
        "language_cues": ["real Americans", "our people"]
      }
    }
  ]
}
```

#### `framework.json` - Mathematical Implementation
Defines positioning, weighting, and ellipse parameters:
```json
{
  "ellipse": {
    "semi_major_axis": 1.0,
    "semi_minor_axis": 0.7
  },
  "wells": {
    "Dignity": {"angle": 90, "weight": 1.0, "type": "integrative"},
    "Tribalism": {"angle": 270, "weight": -1.0, "type": "disintegrative"}
  }
}
```

## Civic Virtue Framework (Default)

The **Civic Virtue Framework** is our most advanced implementation, designed for moral analysis of persuasive political discourse. It includes 10 gravity wells arranged in 5 dipoles representing tensions between integrative civic virtues and disintegrative rhetorical forces:

### Integrative Wells (Upper Half)
- **Dignity** (90°, weight: 1.0) - Individual moral worth and universal rights
- **Truth** (45°, weight: 0.8) - Intellectual honesty and evidence-based reasoning  
- **Hope** (20°, weight: 0.6) - Grounded optimism with realistic paths forward
- **Justice** (135°, weight: 0.8) - Impartial, rule-based fairness
- **Pragmatism** (160°, weight: 0.6) - Evidence-based, adaptable solutions

### Disintegrative Wells (Lower Half)
- **Tribalism** (270°, weight: -1.0) - Group dominance over individual agency
- **Manipulation** (315°, weight: -0.8) - Information distortion and exploitation
- **Fantasy** (340°, weight: -0.6) - Denial of trade-offs and complexity
- **Resentment** (225°, weight: -0.8) - Grievance-centered moral scorekeeping  
- **Fear** (200°, weight: -0.6) - Threat-focused reaction and control

### Theoretical Foundation

### Differential Weighting System

Narrative Gravity Maps support sophisticated **differential weighting** where wells can have varying gravitational influence based on theoretical justification. This distinguishes the methodology from simpler approaches that treat all dimensions equally.

#### Civic Virtue Framework Weighting

The three-tier weighting system reflects moral psychology research:

- **Primary Tier (±1.0)**: Identity forces (Dignity/Tribalism) - most powerful moral motivators
- **Secondary Tier (±0.8)**: Universalizable principles (Truth, Justice, Manipulation, Resentment)  
- **Tertiary Tier (±0.6)**: Cognitive moderators (Hope, Pragmatism, Fantasy, Fear)

This hierarchical structure reflects empirical findings that identity-based concerns can override fairness considerations and abstract reasoning in human moral judgment.

#### Framework Creation with Weighting

When creating custom frameworks, you can:

1. **Enable Differential Weighting**: Choose to use varying weights vs. equal weights (1.0)
2. **Define Tier System**: Create primary/secondary/tertiary tiers with custom weight values
3. **Assign Dipoles to Tiers**: Place each dipole in the appropriate theoretical tier
4. **Document Philosophy**: Explain the theoretical basis for your weighting decisions

The framework creation wizard in the Streamlit interface guides you through this process, ensuring your custom frameworks maintain theoretical rigor while enabling empirical validation.

## Usage Examples

### 1. Standard Analysis
```python
analyzer = NarrativeGravityWellsElliptical()
data = load_analysis_data("model_output/mandela_1994_analysis.json")
output = analyzer.create_visualization(data)
```

### 2. Comparative Analysis
```python
analyses = [
    load_analysis_data("model_output/analysis1.json"),
    load_analysis_data("model_output/analysis2.json")
]
output = analyzer.create_comparative_visualization(analyses)
```

### 3. Custom Framework
```python
# Use alternative framework
analyzer = NarrativeGravityWellsElliptical(config_dir="frameworks/political_spectrum")

# Or switch active framework
# python framework_manager.py switch political_spectrum
analyzer = NarrativeGravityWellsElliptical()  # Uses active framework
```

### 4. Framework Management
```python
from framework_manager import FrameworkManager

manager = FrameworkManager()
frameworks = manager.list_frameworks()
manager.switch_framework("civic_virtue")
```

## Tools

### Core Analysis
```bash
# Single file analysis
python narrative_gravity_elliptical.py model_output/analysis.json

# Comparative analysis  
python narrative_gravity_elliptical.py model_output/analysis1.json model_output/analysis2.json

# Custom output path
python narrative_gravity_elliptical.py analysis.json --output custom_viz.png
```

### Framework Management
```bash
# List available frameworks
python framework_manager.py list

# Get active framework
python framework_manager.py active

# Switch frameworks
python framework_manager.py switch political_spectrum

# Validate framework
python framework_manager.py validate moral_foundations

# Full summary
python framework_manager.py summary
```

### Prompt Generation
```bash
# Generate interactive LLM prompt for active framework
python generate_prompt.py --output prompts/latest.txt

# Generate simple analysis prompt  
python generate_prompt.py --simple --output prompts/basic.txt

# Use custom configuration
python generate_prompt.py --config-dir frameworks/custom --output custom_prompt.txt
```

## Creating Custom Frameworks

### 1. Create Framework Directory
```bash
mkdir -p frameworks/environmental_ethics
```

### 2. Define Conceptual Framework (`dipoles.json`)
```json
{
  "version": "2025.01.06",
  "description": "Environmental Ethics Analysis Framework",
  "dipoles": [
    {
      "name": "Stewardship",
      "description": "Environmental responsibility dynamics",
      "positive": {
        "name": "Sustainability",
        "description": "Long-term environmental thinking...",
        "language_cues": ["future generations", "renewable", "carbon neutral"]
      },
      "negative": {
        "name": "Exploitation",
        "description": "Short-term resource extraction...",
        "language_cues": ["maximize profits", "cheap energy", "job creation"]
      }
    }
  ]
}
```

### 3. Define Mathematical Framework (`framework.json`)
```json
{
  "version": "2025.01.06",
  "description": "Environmental Ethics Mathematical Framework",
  "ellipse": {
    "semi_major_axis": 1.0,
    "semi_minor_axis": 0.8
  },
  "wells": {
    "Sustainability": {"angle": 90, "weight": 1.0, "type": "integrative"},
    "Exploitation": {"angle": 270, "weight": -1.0, "type": "disintegrative"}
  }
}
```

### 4. Activate Framework
```bash
python framework_manager.py switch environmental_ethics
python generate_prompt.py --output prompts/environmental_ethics/v2025.01.06/interactive.txt
```

## Multi-Run Analysis Dashboard System

**NEW in v2025.06.04**: A fully generalized multi-run analysis dashboard that works with any speaker, framework, and text type while maintaining statistical rigor and professional visualization quality.

### Features

- **🎯 Universal Compatibility**: Works with any multi-run JSON file structure
- **🔍 Auto-Detection**: Extracts speaker, year, framework from filenames automatically  
- **📊 Framework Agnostic**: Handles any framework structure (civic virtue, custom, etc.)
- **📈 Statistical Analysis**: Variance analysis, confidence intervals, narrative center tracking
- **🤖 LLM Integration**: Generates composite summaries and variance analyses
- **⚙️ Parameter Override**: Manual parameters override auto-detection when needed

### Usage

#### Basic Auto-Detection
```bash
# Automatically detects everything from filename and data
python create_generic_multi_run_dashboard.py obama_multi_run_civic_virtue_20250606_142731.json

# Output: "Obama Unknown Year Speech - Multi-Run Civic Virtue Analysis Dashboard"
```

#### Manual Parameters
```bash
python create_generic_multi_run_dashboard.py results.json \
  --speaker "Lincoln" \
  --year "1863" \
  --speech-type "Gettysburg Address" \
  --framework "Civic Virtue"

# Output: "Lincoln 1863 Gettysburg Address - Multi-Run Civic Virtue Analysis Dashboard"  
```

#### Programmatic Usage
```python
from create_generic_multi_run_dashboard import create_dashboard

# Auto-detect metadata
fig = create_dashboard("multi_run_results.json")

# Manual override
fig = create_dashboard("results.json", 
                      speaker="Kennedy", 
                      year="1961",
                      speech_type="Inaugural Address",
                      framework="Civic Virtue")

if fig:
    fig.savefig("dashboard.png", dpi=300, bbox_inches='tight')
```

### Auto-Detection Capabilities

The system recognizes common filename patterns:

- `obama_multi_run_civic_virtue_20250606_142731.json` → Obama, Civic Virtue
- `trump_2017_populist_framework_20250101_120000.json` → Trump, 2017, Populist Framework  
- `lincoln_wartime_rhetoric_1863.json` → Lincoln, Wartime Rhetoric, 1863

Framework detection:
- **Civic Virtue**: Auto-detected from well names (Dignity, Truth, Hope, etc.)
- **Unknown Frameworks**: Automatically categorizes as integrative/disintegrative
- **Any Size**: Handles 6, 10, 12, or any number of wells

### Dashboard Output

The generated dashboard maintains professional quality with:

```
┌─────────────────────────────────────────────────────────────────┐
│                    [Speaker] [Year] [Type] - Multi-Run         │
│                    [Framework] Analysis Dashboard              │
├─────────────────────┬───────────────────────────────────────────┤
│                     │                                           │
│   Framework Map     │         Bar Chart with                   │
│   (Elliptical)      │      Confidence Intervals                │
│   Mean Scores       │                                           │
│                     │                                           │
├─────────────────────┼───────────────────────────────────────────┤
│   COMPOSITE         │       VARIANCE ANALYSIS                  │
│   SUMMARY           │                                           │
│   (LLM Generated)   │       (LLM Generated)                    │
├─────────────────────┴───────────────────────────────────────────┤
│ Files: xxx.json | Model: xxx | Runs: N | Date: xxx | Job: xxx  │
└─────────────────────────────────────────────────────────────────┘
```

### Testing

```bash
# Test auto-detection capabilities
python test_auto_detection.py

# Shows filename parsing and framework detection examples
```

See `docs/generalization/GENERIC_DASHBOARD_USAGE.md` for comprehensive documentation and `docs/generalization/GENERALIZATION_SUMMARY.md` for technical details of the transformation from speaker-specific to universal system.

## JSON Format Evolution

### Old Format (Still Supported)
```json
{
  "wells": [
    {"name": "Dignity", "score": 1.0, "angle": 90},
    {"name": "Truth", "score": 0.8, "angle": 45}
  ],
  "com": {"x": 0.1, "y": 0.2},
  "mps": 0.25,
  "dps": 0.85
}
```

### New Format (Minimal)
```json
{
  "metadata": {
            "prompt_version": "2025.06.04",
    "framework": "moral_foundations"
  },
  "scores": {
    "Dignity": 1.0,
    "Truth": 0.8
  }
}
```

The system automatically handles both formats with full backward compatibility.

## Research Applications

- **Political Speech Analysis** - Understanding moral appeals in campaign rhetoric
- **Policy Debate Analysis** - Mapping moral arguments in policy discussions  
- **Cross-Cultural Comparison** - Comparing moral emphasis across different societies
- **Historical Analysis** - Tracking moral themes across time periods
- **Framework Development** - Creating domain-specific moral analysis systems

## Contributing

When contributing new frameworks or features:

1. **Framework Structure**: Follow the `dipoles.json` + `framework.json` pattern
2. **Documentation**: Include README.md explaining theoretical basis
3. **Validation**: Use `framework_manager.py validate` to check structure
4. **Testing**: Verify with existing analysis data
5. **Versioning**: Use semantic versioning for framework evolution

## Version History

- **v2025.06.04**: Narrative Gravity Maps methodology - comprehensive restructuring with Civic Virtue Framework
- **v2025.01.05**: Modular architecture, multi-framework support, automated prompt generation
- **v1.0** (2025.01.03): Original framework implementation

## Files Overview

- `narrative_gravity_elliptical.py` - Core analysis engine
- `generate_prompt.py` - Automated prompt generation
- `framework_manager.py` - Framework management tool
- `frameworks/` - Multiple dipole framework definitions
- `prompts/` - Generated prompts organized by framework/version
- `config/` - Active framework configuration (symlinks)
- `model_output/` - Analysis results and visualizations

For detailed technical documentation, see `docs/development/MODULAR_ARCHITECTURE.md` and `docs/development/STORAGE_ARCHITECTURE.md`. For a complete overview of available documentation, see `docs/README.md`.

## Using This Software with the Paper "Narrative Gravity Maps"

If you are reading the paper "Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives," this repository provides the open-source implementation of the methodology and frameworks discussed. While the paper focuses on political narrative analysis using the Civic Virtue Framework, the methodology can be applied to any persuasive narrative type with appropriate frameworks. We encourage you to explore the tools and replicate the analyses.

**Key files and directories related to the paper:**
*   **Replication Guide:** For specific instructions on how to reproduce the analyses and figures presented in the paper, please see [`PAPER_REPLICATION.md`](./PAPER_REPLICATION.md).
*   **Frameworks:** The analytical frameworks (e.g., Civic Virtue Framework) are defined in the `frameworks/` directory.
*   **Reference Texts:** Sample texts, including those used in the paper, can be found in `reference_texts/`.
*   **LLM Scores for Paper Analyses:** The specific LLM-generated scores used for the paper's figures are located in `model_output/paper_analyses/` (as detailed in `PAPER_REPLICATION.md`).

## Getting Started

We recommend starting with the React Research Workbench for the most user-friendly experience.

1.  **Ensure Dependencies are Installed:**
    ```bash
    # Frontend dependencies
    cd frontend
    npm install
    
    # Backend dependencies (if needed)
    pip install -r requirements.txt
    ```
2.  **Launch the Application:**
    ```bash
    # React interface (recommended)
    cd frontend
    npm run dev
    # Open http://localhost:3000
    
    # Or backend services
    python launch.py
    ```

## Workflow: Analyzing New Texts

This application uses a multi-step process to analyze persuasive narratives, involving an external Large Language Model (LLM) like ChatGPT or Claude:

1.  **Generate Prompt (in React App):**
    *   Open the React interface at http://localhost:3000
    *   Go to the "Prompt Editor" tab.
    *   Select the desired framework (e.g., "civic_virtue").
    *   Click "Generate Analysis Prompt". A detailed prompt will appear.

2.  **Use External LLM:**
    *   Copy the generated prompt.
    *   Go to your chosen LLM (e.g., ChatGPT, Claude).
    *   Paste the prompt, followed by the text you want to analyze.
    *   The LLM will output a response, hopefully in JSON format as requested by the prompt.

3.  **Input LLM JSON Response (in React App):**
    *   Copy the JSON portion of the LLM's response.
    *   Back in the React app, go to the "Analysis Results" tab.
    *   Paste this JSON into the text area labeled "Paste JSON response here".

4.  **Generate Visualization (in React App):**
    *   Click "Generate Visualization".
    *   The narrative gravity map and associated metrics will be displayed in the "Comparison Dashboard".

For a quick test of the visualization step without needing an LLM, you can use the test data features in the React interface.

**Example of Expected JSON from LLM:**

**🚨 CRITICAL:** LLM must use decimal scores between 0.0 and 1.0 (NOT 1-10 or any other scale)

```json
{
  "metadata": {
    "title": "Trump's 2025 Second Inaugural Address (analyzed by Claude 3.5 Sonnet)",
    "filename": "2025_06_04_203300_claude_35_sonnet_analysis.json",
    "model_name": "Claude",
    "model_version": "4.0 Sonnet",
    "prompt_version": "2025.06.04.20.19",
    "dipoles_version": "v2025.06.04",
    "framework_version": "v2025.06.04",
    "framework_name": "civic_virtue",
    "summary": "Brief analysis summary explaining the moral positioning..."
  },
  "scores": {
    "Dignity": 0.6,
    "Tribalism": 0.8,
    "Truth": 0.4,
    "Manipulation": 0.7,
    "Justice": 0.5,
    "Resentment": 0.8,
    "Hope": 0.7,
    "Fantasy": 0.6,
    "Pragmatism": 0.3,
    "Fear": 0.9
  }
}
```

**Important Notes:**
- This example shows the exact structure and score format required for the civic_virtue framework
- All scores must be decimal values between 0.0 and 1.0
- **Model Identification**: If using AI platforms (like Perplexity) that run underlying models (like Claude), you may need to manually update the `model_name` and `model_version` fields in the JSON to reflect the actual underlying model for academic accuracy

## Project Status

The project has recently undergone a significant testing overhaul to improve code quality, reliability, and maintainability. This effort focused on establishing a robust unit testing foundation for the backend services.

### Testing Overhaul Summary

The testing overhaul was conducted in two main phases:

**Phase 1: Foundational Unit Tests & Refactoring**
- **Mathematical Engine:** Added comprehensive unit tests for the core elliptical distance calculations in `narrative_gravity_elliptical.py`.
- **Dashboard Logic:** Created unit tests for pure helper functions in the legacy dashboard code.
- **Legacy Test Refactoring:** Migrated all existing `unittest`-style tests to a modern `pytest` framework, separating them into appropriate unit and integration test suites.

**Phase 2: Backend Confidence (src/)**
- **`src/utils`:** Added full unit test coverage for all utility modules, including `sanitization.py`, `auth.py`, `logging_config.py`, and `cost_manager.py`.
- **`src/api`:**
    - Tested and hardened the Pydantic `schemas.py`, upgrading them to V2 and fixing validation logic.
    - Added complete unit tests for the database layer in `crud.py`, using an in-memory SQLite database.
    - Added tests for the business logic in `services.py`.
- **`src/tasks`:** Implemented unit tests for the Celery-based `analysis_tasks.py`, mocking external dependencies like the database and Hugging Face API calls.

This process uncovered and fixed numerous bugs related to Pydantic V2 migration, database type compatibility (PostgreSQL `JSONB` vs. generic `JSON`), import path errors, and incorrect business logic.

**Testing Strategy Update (v2.1):** Integration tests now use SQLite by default for faster, more reliable testing. Unit tests use in-memory SQLite for isolation. PostgreSQL remains the production database, with optional PostgreSQL testing for production-like validation.

### Known Issues
- **`test_api_services.py` Failures:** There are two persistent test failures in `tests/unit/test_api_services.py` related to the `ingest_jsonl_corpus` service function. The fixes for these failures could not be reliably applied due to suspected issues with the development environment's file editing tools. The primary issue appears to be incorrect handling of empty or whitespace-only files during ingestion.

## Getting Started (Legacy Backend)

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run backend services:**
    ```bash
    python launch.py
    ```

**Note:** For the modern React interface, see the main Getting Started section above.

## Running Tests
To run the full test suite:
```bash
pytest
```
To run tests for a specific file:
```bash
pytest tests/unit/test_crud.py
```

# Narrative Gravity Wells: Quantitative Framework for Analyzing Political Discourse

## Abstract

This repository implements the **Narrative Gravity Maps** methodology - a quantitative framework for analyzing the moral and rhetorical forces in political discourse. Through positioning conceptual "gravity wells" on coordinate systems, the framework enables systematic measurement of how narratives orient toward civic virtues versus disintegrative rhetorical forces.

The methodology demonstrates technical consistency with cross-LLM correlation exceeding 0.90, though empirical validation against human moral perception remains an active area of research. The system provides valuable tools for systematic comparative analysis, exploratory research, and methodological development in computational political discourse analysis.

## 🎯 Current Project Status (January 2025)

### ✅ **Technical Infrastructure Complete**
- **Backend Services**: Multi-LLM integration with 99.5% test reliability
- **Database**: PostgreSQL with comprehensive schema for experiments and analysis
- **Frontend**: React research workbench for systematic analysis workflows
- **Testing**: Comprehensive automated testing with Playwright end-to-end validation

### 🔴 **Critical Development Priority**
- **Backend API Integration**: Connecting React frontend to existing analysis engine
- **Missing API Endpoints**: Experiments, runs, and configuration endpoints needed

### 📋 **Research Phase**: Validation-First Development
Moving from infrastructure completion to academic validation studies establishing framework credibility.

---

## 📚 Academic Paper Development

### Current Paper Status
- **Current Version**: v1.0.0 (Validation-Ready Draft)
- **Location**: `paper/drafts/narrative_gravity_maps_v1.0.0.md`
- **Status**: Technical implementation documented, human validation studies required

### Paper Development Workflow
```bash
# Check current paper status
cd paper && python manage_paper.py status

# Create new paper version
python manage_paper.py new-version --type minor

# Check evidence status
python manage_paper.py check-evidence

# Validate claims against available evidence
python manage_paper.py validate-claims

# Generate submission checklist
python manage_paper.py submission-checklist
```

### Paper Directory Structure
```
paper/
├── README.md                     # Paper development guide
├── PAPER_CHANGELOG.md            # Complete version history
├── manage_paper.py               # Automated paper management
├── drafts/                       # Version-controlled paper drafts
├── evidence/                     # Supporting evidence and data
│   ├── technical_validation/     # Cross-LLM consistency data
│   ├── case_studies/            # Political speech analyses
│   ├── validation_studies/      # Human validation (required)
│   └── figures/                 # Charts and visualizations
├── reviews/                      # Peer review and feedback
└── submission/                   # Journal submission materials
```

### Evidence Requirements for Publication
- ✅ **Technical Validation**: Cross-LLM consistency (r > 0.90) documented
- ✅ **Case Studies**: Presidential speech analyses with statistical metrics
- ❌ **Human Validation**: Expert annotation studies (critical gap)
- ❌ **Inter-Rater Reliability**: Human expert agreement studies needed
- ❌ **Cross-Cultural Validation**: Framework applicability across contexts

### Academic Integrity Standards
- **No Validation Overclaims**: Clear distinction between technical consistency and human validation
- **Evidence-Based Progression**: All claims backed by appropriate supporting data
- **Transparent Limitations**: Honest acknowledgment of current gaps and research needs
- **Independent Research**: Rigorous methodology despite non-institutional context

---