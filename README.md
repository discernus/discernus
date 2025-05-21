# Moral Gravity Well Analysis

A Python-based visualization tool for moral gravity well analysis. This tool creates polar plots to visualize moral dimensions and their relationships, including gravity wells, narrative scores, and centers of mass. It supports both single-model analysis and multi-model comparisons.

## Setup

1. Ensure you have Python 3.9+ installed
2. Clone this repository
3. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
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

### Custom Analysis
To visualize your own analysis, create a JSON file following this structure:
```json
{
    "metadata": {
        "title": "Your Analysis Title",
        "filename": "your_analysis.json",
        "model_name": "Model Name",
        "summary": "Your analysis summary text..."
    },
    "wells": [
        {"name": "Dimension1", "angle": 0, "score": 0.7},
        {"name": "Dimension2", "angle": 90, "score": 0.8}
        // ... add more dimensions
    ],
    "metrics": {
        "com": {
            "x": 0.0,
            "y": 0.0
        }
    }
}
```

Then run:
```bash
python3 moral_gravity_map.py your_analysis.json
```

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
- `config/`
  - `gwllmp.ini`: Configuration settings
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