# Moral Gravity Well Analysis

A Python-based visualization tool for moral gravity well analysis. This tool creates polar plots to visualize moral dimensions and their relationships, including gravity wells, narrative scores, and centers of mass. It supports both single-model analysis and multi-model comparisons.

## Setup

1. Ensure you have Python 3.9+ installed
2. Clone this repository
3. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## Workflow

### Single Model Analysis

1. **Prepare Your Files**
   - Create a text file containing your narrative (e.g., `narrative.txt`)
   - Choose an appropriate prompt from the `prompts/` directory:
     - `5_dipole_liberal_democratic_norm_prompt.txt`: Standard 10-dimension analysis for political/civic narratives
     - (Additional prompt types for corporate, cultural, etc. contexts coming soon)
   - Customize the prompt if needed for your specific LLM

2. **Generate Analysis**
   - Submit both files to your chosen LLM
   - Request output in the required JSON format (see below)
   - Save the LLM's response as a JSON file (e.g., `analysis.json`)

3. **Create Visualization**
   ```bash
   python3 moral_gravity_map.py analysis.json
   ```
   The visualization will be saved in `model_output/` with a timestamp and model name.

### Multi-Model Analysis

1. **Generate Multiple Analyses**
   - Follow steps 1-2 above for each LLM
   - Use consistent narrative and prompt files across models
   - Save each response with a descriptive name (e.g., `gpt4_analysis.json`, `claude_analysis.json`)

2. **Create Comparison**
   - Place all JSON files in a directory (e.g., `analyses/`)
   - Run the comparison tool:
   ```bash
   python3 generate_comparison.py analyses/*.json
   ```
   This will create a combined visualization showing all models' interpretations.

### Required JSON Format
```json
{
    "metadata": {
        "title": "Your Analysis Title",
        "filename": "your_analysis.json",
        "model_name": "Model Name",
        "model_version": "Version",
        "summary": "Your analysis summary text..."
    },
    "wells": [
        {"name": "Dignity", "angle": 90, "score": 0.8},
        {"name": "Truth", "angle": 30, "score": 0.7},
        {"name": "Hope", "angle": 60, "score": 0.9},
        {"name": "Justice", "angle": 150, "score": 0.8},
        {"name": "Pragmatism", "angle": 120, "score": 0.7},
        {"name": "Tribalism", "angle": 270, "score": 0.2},
        {"name": "Fear", "angle": 300, "score": 0.1},
        {"name": "Resentment", "angle": 330, "score": 0.1},
        {"name": "Manipulation", "angle": 210, "score": 0.1},
        {"name": "Fantasy", "angle": 240, "score": 0.1}
    ],
    "metrics": {
        "com": {"x": 0.3, "y": 0.4},
        "mps": 0.8,
        "dps": 0.7
    }
}
```

## Usage

### Basic Usage
Run a single visualization with the sample data:
```bash
python3 moral_gravity_map.py
```

### Multi-Model Comparison
To generate a comparison visualization of multiple analyses:
```bash
python3 generate_comparison.py
```

This will create a visualization comparing the analyses from different models, with:
- Distinct colors for each model using the tab20 colormap
- Smart handling of overlapping points with circular arrangement
- Flexible legend layout (2-3 columns based on model count)
- Enhanced visibility with alpha transparency

## Visualization Elements

- **Gray Dots**: Moral gravity wells (fixed positions)
- **Blue Dots**: Narrative scores
- **Red Dot**: Center of Mass (COM)
- **Dotted Circle**: Reference circle
- **Dashed Lines**: Connections from center to narrative scores
- **Multi-Color Dots**: Different models in comparison view

## Directory Structure

- `moral_gravity_map.py`: Main visualization script
- `generate_comparison.py`: Multi-model comparison script
- `prompts/`: Analysis prompts for different contexts
  - `5_dipole_liberal_democratic_norm_prompt.txt`: Standard 10-dimension political analysis
  - (Additional prompts for different contexts will be added here)
- `analysis/`: Analysis documentation and comparisons
- `model_output/`: Generated visualizations and data
- `requirements.txt`: Python package dependencies
- `old_files/`: Archive of previous versions

## Development

### Branching Strategy

This repository follows a two-branch development model:

- `main` branch:
  - Contains stable, released code only
  - Protected from direct development changes
  - Tagged with version numbers (e.g., v1.0.0)
  - Updated only through reviewed pull requests from `dev`

- `dev` branch:
  - Contains all active development work
  - Feature branches merge into `dev` first
  - Changes are tested and reviewed here
  - When stable, changes are merged to `main` for release

### Contributing

1. Always create your changes in the `dev` branch
2. Test your changes thoroughly
3. Create a pull request from `dev` to `main` for releases
4. Tag new releases in `main` with version numbers

## License

Copyright (c) 2025 Jeff Whatcott. All rights reserved.

This software and its documentation are protected by copyright law. Unauthorized reproduction or distribution of this software, or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under law. 