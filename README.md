# Elliptical Moral Gravity Wells Framework v2.0

**A quantitative framework for analyzing the moral forces driving political narratives**

![Moral Gravity Wells Analysis](https://img.shields.io/badge/analysis-moral--gravity--wells-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Version](https://img.shields.io/badge/version-2.0-orange.svg)

## Overview

The Elliptical Moral Gravity Wells framework positions political narratives within an elliptical coordinate system based on ten moral "gravity wells" that exert attractive force proportional to their moral weight and the narrative's alignment with each well.

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
from moral_gravity_elliptical import MoralGravityWellsElliptical, load_analysis_data

# Initialize analyzer
analyzer = MoralGravityWellsElliptical()

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
python framework_manager.py switch political_spectrum

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

## Architecture Overview

### Storage Structure (New in v2.0)

```
moral_gravity_analysis/
├── frameworks/                    # Multiple dipole frameworks
│   ├── moral_foundations/         # Original 5-dipole system
│   │   ├── dipoles.json          # Conceptual definitions
│   │   ├── framework.json        # Mathematical implementation
│   │   └── README.md             # Framework documentation
│   └── political_spectrum/        # Alternative framework
├── prompts/                       # Generated prompts by framework/version
│   └── moral_foundations/
│       ├── v2025.01.05/          # Current version
│       │   ├── interactive.txt
│       │   ├── batch.txt
│       │   └── metadata.json
│       └── v2025.01.03/          # Legacy version
├── config/                        # Active configuration (symlinks)
│   ├── dipoles.json -> ../frameworks/moral_foundations/dipoles.json
│   └── framework.json -> ../frameworks/moral_foundations/framework.json
└── model_output/                  # Analysis results
```

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

## Current Moral Framework

The default framework includes 10 moral gravity wells arranged in 5 dipoles:

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

The three-tier weighting system reflects moral psychology research:

- **Primary Tier (±1.0)**: Identity forces (Dignity/Tribalism) - most powerful moral motivators
- **Secondary Tier (±0.8)**: Universalizable principles (Truth, Justice, Manipulation, Resentment)
- **Tertiary Tier (±0.6)**: Cognitive moderators (Hope, Pragmatism, Fantasy, Fear)

## Usage Examples

### 1. Standard Analysis
```python
analyzer = MoralGravityWellsElliptical()
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
analyzer = MoralGravityWellsElliptical(config_dir="frameworks/political_spectrum")

# Or switch active framework
# python framework_manager.py switch political_spectrum
analyzer = MoralGravityWellsElliptical()  # Uses active framework
```

### 4. Framework Management
```python
from framework_manager import FrameworkManager

manager = FrameworkManager()
frameworks = manager.list_frameworks()
manager.switch_framework("political_spectrum")
```

## Tools

### Core Analysis
```bash
# Single file analysis
python moral_gravity_elliptical.py model_output/analysis.json

# Comparative analysis  
python moral_gravity_elliptical.py model_output/analysis1.json model_output/analysis2.json

# Custom output path
python moral_gravity_elliptical.py analysis.json --output custom_viz.png
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
    "prompt_version": "2025.01.05.16.30",
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

- **v2.0** (2025.01.05): Modular architecture, multi-framework support, automated prompt generation
- **v1.0** (2025.01.03): Original elliptical framework implementation

## Files Overview

- `moral_gravity_elliptical.py` - Core analysis engine
- `generate_prompt.py` - Automated prompt generation
- `framework_manager.py` - Framework management tool
- `frameworks/` - Multiple dipole framework definitions
- `prompts/` - Generated prompts organized by framework/version
- `config/` - Active framework configuration (symlinks)
- `model_output/` - Analysis results and visualizations

For detailed technical documentation, see `MODULAR_ARCHITECTURE.md` and `STORAGE_ARCHITECTURE.md`.