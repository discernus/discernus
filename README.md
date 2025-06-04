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

### Basic Usage (Unchanged)
```python
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical, load_analysis_data

# Initialize analyzer
analyzer = NarrativeGravityWellsElliptical()

# Load and visualize analysis
data = load_analysis_data("model_output/sample_analysis.json")
output_path = analyzer.create_visualization(data)
print(f"Visualization saved: {output_path}")
```

### Framework Management (New in v2.0)
```bash
# List available frameworks
python framework_manager.py summary

# Switch to different framework
python framework_manager.py switch civic_virtue

# Generate prompt for active framework
python generate_prompt.py --output prompts/custom/latest.txt
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
│   ├── launch_app.py                 # Application launcher
│   ├── narrative_gravity_app.py      # Main Streamlit interface  
│   ├── narrative_gravity_elliptical.py # Core analysis engine
│   ├── framework_manager.py          # Framework management
│   └── generate_prompt.py            # LLM prompt generator
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
│   ├── docs/development/            # Technical documentation
│   ├── docs/examples/               # Usage examples
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

For detailed technical documentation, see `MODULAR_ARCHITECTURE.md` and `STORAGE_ARCHITECTURE.md`.