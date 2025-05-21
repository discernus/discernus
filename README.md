# Moral Gravity Well Analysis

A Python-based visualization tool for moral gravity well analysis. This tool creates polar plots to visualize moral dimensions and their relationships, including gravity wells, narrative scores, and centers of mass.

## Setup

1. Ensure you have Python 3.9+ installed
2. Clone this repository
3. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## Usage

### Basic Usage
Run the visualization with the sample data:
```bash
python3 moral_gravity.py
```

### Custom Analysis
To visualize your own analysis, create a JSON file following this structure:
```json
{
    "metadata": {
        "title": "Your Analysis Title",
        "filename": "your_analysis.json",
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
python3 moral_gravity.py your_analysis.json
```

## Visualization Elements

- **Gray Dots**: Moral gravity wells (fixed positions)
- **Blue Dots**: Narrative scores
- **Red Dot**: Center of Mass (COM)
- **Dotted Circle**: Reference circle
- **Dashed Lines**: Connections from center to narrative scores

## File Structure

- `moral_gravity.py`: Main visualization script
- `requirements.txt`: Python package dependencies
- `sample_analysis.json`: Example analysis data

## License

Copyright (c) 2025 Jeff Whatcott. All rights reserved.

This software and its documentation are protected by copyright law. Unauthorized reproduction or distribution of this software, or any portion of it, may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under law. 