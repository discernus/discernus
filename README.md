# Moral Gravity Wells Analysis

This Python application creates a visualization of moral gravity wells using a polar plot. The visualization shows positive and negative moral wells, their relative strengths, and calculates various metrics including the Center of Mass (COM), Moral Polarity Score (MPS), and Directional Purity Score (DPS).

## Requirements

- Python 3.7 or higher
- matplotlib
- numpy

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:
```bash
python moral_gravity.py
```

This will display a polar plot showing:
- Positive wells (blue shades)
- Negative wells (orange shades)
- Center of Mass (red star)
- Metrics in a text box

The size and color intensity of each point represents the strength of that moral well. 