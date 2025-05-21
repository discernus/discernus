# Visualization Code
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import json
import sys
import os
from datetime import datetime
from typing import Dict, List
from textwrap import wrap
from pathlib import Path
import shutil

def create_output_directory(json_path: str, data: Dict) -> tuple[str, str]:
    """Create output directory structure and return paths."""
    # Create base output directory if it doesn't exist
    base_dir = Path("model_output")
    base_dir.mkdir(exist_ok=True)
    
    # Get model name from metadata
    model_name = data['metadata'].get('model_name', 'unknown_model')
    model_name = model_name.lower().replace(' ', '_')
    
    # Create timestamped subfolder with descriptive name including model
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    json_name = Path(json_path).stem
    
    # Create new filenames with model name
    base_filename = f"{json_name}_{model_name}"
    json_filename = f"{base_filename}.json"
    png_filename = f"{base_filename}.png"
    
    # Create subfolder name
    subfolder_name = f"{timestamp}_{model_name}_{json_name}"
    output_dir = base_dir / subfolder_name
    output_dir.mkdir(exist_ok=True)
    
    # Set up output paths with new filenames
    json_output_path = output_dir / json_filename
    png_output_path = output_dir / png_filename
    
    # Copy input JSON to output directory with new name
    shutil.copy2(json_path, json_output_path)
    
    return str(json_output_path), str(png_output_path)

def load_analysis_data(json_path: str) -> Dict:
    """Load and validate the analysis data from a JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Basic validation
    required_keys = {'wells', 'metrics'}
    if not all(key in data for key in required_keys):
        raise ValueError(f"JSON must contain all required keys: {required_keys}")
    
    return data

def plot_gravity_map(data: Dict, json_path: str):
    """Generate the moral gravity wells visualization from analysis data."""
    # Create output directory and get file paths
    json_output_path, png_output_path = create_output_directory(json_path, data)
    
    # Extract data
    wells = data['wells']
    metrics = data['metrics']
    metadata = data['metadata']
    
    # Set up the figure with white background
    plt.style.use('default')
    fig = plt.figure(figsize=(12, 10))  # Further reduce height
    
    # Create main polar axis for the plot
    ax = plt.subplot2grid((8, 1), (0, 0), rowspan=6, projection='polar')  # More granular grid, main plot takes most space
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Make the outer circle invisible
    ax.spines['polar'].set_color('none')

    # Add two-line title
    fig.text(0.5, 0.92, "Moral Gravity Map", 
            fontsize=16, fontweight='bold', 
            horizontalalignment='center')
    
    # Add subtitle with model info if available
    subtitle = metadata['title']
    if 'model' in metadata:
        subtitle += f" (analyzed by {metadata['model']})"
    
    fig.text(0.5, 0.89, subtitle,
            fontsize=12, style='italic',
            horizontalalignment='center')
    
    # Convert angles to radians for plotting
    angles_rad = [np.deg2rad(well['angle']) for well in wells]
    scores = [well['score'] for well in wells]
    names = [well['name'] for well in wells]
    
    # Plot the unit circle
    circle = plt.Circle((0, 0), 1.0, transform=ax.transData._b, fill=False, color='gray', linestyle=':', alpha=0.5)
    ax.add_artist(circle)
    
    # Plot all wells as gray dots on the circle
    ax.scatter(angles_rad, [1]*len(wells), color='gray', s=50, zorder=3)
    
    # Plot the score points and connect them to center with dashed lines
    for angle, score in zip(angles_rad, scores):
        # Plot score point
        ax.scatter(angle, score, color='blue', s=50, zorder=3)
        # Draw dashed line from center to score point
        ax.plot([angle, angle], [0, score], color='blue', linestyle='--', alpha=0.5, zorder=2)

    # Plot the Center of Mass
    com_x = metrics['com']['x']
    com_y = metrics['com']['y']
    com_r = np.sqrt(com_x**2 + com_y**2)
    com_theta = np.arctan2(com_y, com_x)
    ax.scatter(com_theta, com_r, s=100, color='red', zorder=4)
    # Add COM label with value
    ax.text(com_theta, com_r + 0.1, f"COM = ({com_x:.2f}, {com_y:.2f})",
            ha='center', va='bottom', color='red')

    # Add well labels
    for well, angle in zip(names, angles_rad):
        # Special handling for Dignity and Tribalism - center them
        if well in ["Dignity", "Tribalism"]:
            ha = 'center'
        else:
            ha = 'left' if -np.pi/2 <= angle <= np.pi/2 else 'right'
        
        # Special positioning for specific labels
        label_radius = 1.2
        if well == "Resentment":
            label_radius = 1.25  # Slightly reduced from 1.3 to move label left
            ha = 'left'  # Force left alignment to move it right of the circle
        
        ax.text(angle, label_radius, well, ha=ha, va='center', rotation=0)

    # Set the plot limits and remove unnecessary elements
    ax.set_ylim(0, 1.4)  # Reduced upper limit to remove outer circle
    ax.set_rticks([])  # Remove radial ticks
    ax.set_xticks([])  # Remove angular ticks
    ax.grid(False)     # Remove grid

    # Create legend patches
    gravity_patch = mpatches.Patch(color='gray', label='Gravity Wells')
    narrative_patch = mpatches.Patch(color='blue', label='Narrative Scores')
    com_patch = mpatches.Patch(color='red', label='Center of Mass')
    
    # Add legend in a more compact bottom section
    legend_ax = plt.subplot2grid((8, 1), (6, 0))
    legend_ax.axis('off')
    legend = legend_ax.legend(handles=[gravity_patch, narrative_patch, com_patch],
                            loc='center',
                            ncol=3,
                            bbox_to_anchor=(0.5, 0.8))  # Reduced from 1.2 to 0.8 to move legend down
    
    # Wrap text manually with appropriate width
    wrapped_text = '\n'.join(wrap(metadata['summary'], width=100))
    
    # Add the summary text closer to the legend
    fig.text(0.5, 0.12, wrapped_text,
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=10,
             style='italic',
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=5))

    plt.subplots_adjust(top=0.85, bottom=0.05, hspace=0)
    
    # Save with the custom filename
    plt.savefig(png_output_path, bbox_inches='tight', dpi=300)
    plt.close()  # Close the current figure
    
    # Create a new figure for display
    fig = plt.figure()
    img = plt.imread(png_output_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
    print(f"\nOutput files saved to: {os.path.dirname(png_output_path)}")

def main():
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = 'sample_analysis.json'
    
    try:
        data = load_analysis_data(json_path)
        plot_gravity_map(data, json_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 