# DCS Stage 6 Template Base: Standard Library Foundation
# Extracted from production Tamaki-Fuks template for universal reuse
# Framework-agnostic mathematical and visualization foundations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import json
import yaml
from pathlib import Path
from datetime import datetime

def setup_publication_style():
    """Configure matplotlib for Nature/academic journal standards
    
    This configuration works for ANY framework and provides publication-ready styling
    consistent with Nature, Science, and other top-tier academic journals.
    """
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8,
        'figure.dpi': 150,  # Good for notebooks, 300 for final export
        'axes.linewidth': 0.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'grid.linewidth': 0.5,
        'grid.alpha': 0.3,
        'legend.frameon': False,
        'legend.fontsize': 7
    })

def calculate_signature_coordinates(scores_dict, anchor_positions):
    """Calculate signature position within unit circle using weighted centroid
    
    Universal coordinate calculation that works with ANY number of anchors.
    
    Args:
        scores_dict: Dictionary mapping anchor names to scores (0-1)
        anchor_positions: Dictionary mapping anchor names to (x, y) coordinates
        
    Returns:
        np.array: [x, y] coordinates of signature position within unit circle
    """
    # Extract positions and weights in same order
    anchor_names = list(scores_dict.keys())
    positions = np.array([anchor_positions[name] for name in anchor_names])
    weights = np.array([scores_dict[name] for name in anchor_names])
    
    # Calculate weighted centroid
    if np.sum(weights) > 0:
        signature = np.average(positions, weights=weights, axis=0)
        
        # Keep within unit circle (normalize if outside)
        magnitude = np.linalg.norm(signature)
        if magnitude > 1.0:
            signature = signature / magnitude
            
        return signature
    else:
        return np.array([0.0, 0.0])

def load_framework_from_yaml(framework_path):
    """Load ANY Framework Specification v3.2 compliant framework from YAML
    
    Auto-detects framework characteristics and extracts anchor positions,
    colors, relationships, and metadata for template configuration.
    
    Args:
        framework_path: Path to framework YAML file
        
    Returns:
        dict: Framework configuration with standardized structure
    """
    with open(framework_path, 'r') as f:
        framework_yaml = yaml.safe_load(f)
    
    # Extract anchors with auto-calculated positions (spec compliant)
    anchors = {}
    
    # Handle v3.1 (anchors) and v3.2 (components) format according to spec
    if 'components' in framework_yaml:
        # v3.2 format - use components section
        anchor_configs = framework_yaml['components']
    else:
        # v3.1 format - use anchors section
        anchor_configs = framework_yaml.get('anchors', {})
    
    for name, config in anchor_configs.items():
        # Calculate position from angle
        angle = config.get('angle', 0)  # degrees
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        anchors[name] = {
            'position': (x, y),
            'angle': angle,
            'color': config.get('color', auto_assign_color(name, len(anchor_configs))),
            'description': config.get('description', ''),
            'type': config.get('type', 'anchor')
        }
    
    # Extract relationships (competitive, complementary, etc.)
    relationships = framework_yaml.get('competitive_relationships', [])
    
    # Extract metadata
    metadata = {
        'name': framework_yaml.get('name', 'Unknown Framework'),
        'version': framework_yaml.get('version', '1.0'),
        'description': framework_yaml.get('description', ''),
        'theoretical_foundation': extract_theoretical_foundation(framework_yaml),
        'anchor_count': len(anchors),
        'relationship_count': len(relationships)
    }
    
    return {
        'anchors': anchors,
        'relationships': relationships,
        'metadata': metadata
    }

def auto_assign_color(anchor_name, total_anchors):
    """Auto-assign academic-quality colors using ColorBrewer palette
    
    Uses established academic color schemes that work well in publication
    and are colorblind-friendly.
    
    Args:
        anchor_name: Name of the anchor
        total_anchors: Total number of anchors (for palette selection)
        
    Returns:
        str: Hex color code
    """
    # ColorBrewer Set1 palette (academic standard)
    colors = [
        '#d62728',  # Red
        '#1f77b4',  # Blue  
        '#2ca02c',  # Green
        '#ff7f0e',  # Orange
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf'   # Cyan
    ]
    
    # Use anchor name hash for consistent color assignment
    color_index = hash(anchor_name) % len(colors)
    return colors[color_index]

def extract_theoretical_foundation(framework_yaml):
    """Extract theoretical foundation information from framework YAML
    
    Looks for theoretical foundation info in description, metadata, or other fields
    to provide proper academic attribution.
    
    Args:
        framework_yaml: Parsed framework YAML
        
    Returns:
        str: Theoretical foundation description
    """
    # Check various possible locations for theoretical info
    description = framework_yaml.get('description', '')
    
    # Extract theoretical foundation from description if present
    if 'theoretical' in description.lower() or 'foundation' in description.lower():
        lines = description.split('\n')
        for line in lines:
            if 'theoretical' in line.lower() or 'foundation' in line.lower():
                return line.strip()
    
    # Fallback to framework name and description
    name = framework_yaml.get('name', 'Unknown Framework')
    return f"{name} theoretical framework"

def plot_unit_circle_base(ax, anchors, title="DCS Coordinate Analysis"):
    """Plot universal DCS coordinate space foundation
    
    Creates the base unit circle with anchors that works for ANY framework.
    Individual templates can add framework-specific elements on top.
    
    Args:
        ax: Matplotlib axis
        anchors: Dictionary of anchor configurations
        title: Plot title
        
    Returns:
        ax: Configured matplotlib axis
    """
    # Unit circle boundary
    circle = patches.Circle((0, 0), 1, fill=False, color='black', linewidth=1.5, alpha=0.8)
    ax.add_patch(circle)
    
    # Subtle grid for reference
    ax.axhline(y=0, color='lightgray', linewidth=0.5, alpha=0.4)
    ax.axvline(x=0, color='lightgray', linewidth=0.5, alpha=0.4)
    
    # Plot anchors
    for name, config in anchors.items():
        x, y = config['position']
        color = config['color']
        ax.scatter(x, y, s=150, c=color, marker='s', edgecolors='black', 
                  linewidth=2, zorder=10, alpha=0.9)
        
        # Position labels with automatic spacing
        label_x, label_y = x * 1.25, y * 1.25
        ax.annotate(name.title(), (label_x, label_y), 
                   fontsize=10, ha='center', va='center', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Formatting
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=12, weight='bold', pad=15)
    ax.set_xlabel('DCS Dimension 1', fontsize=10)
    ax.set_ylabel('DCS Dimension 2', fontsize=10)
    
    return ax

def calculate_framework_statistics(signatures, framework_metadata):
    """Calculate universal framework statistics
    
    Computes standard statistical measures that apply to any framework:
    discourse intensity, coordinate space utilization, etc.
    
    Args:
        signatures: Dictionary mapping speech_id to coordinates
        framework_metadata: Framework metadata dictionary
        
    Returns:
        dict: Statistical summary
    """
    all_coords = np.array(list(signatures.values()))
    overall_centroid = np.mean(all_coords, axis=0)
    
    return {
        'total_speeches': len(signatures),
        'framework_name': framework_metadata['name'],
        'anchor_count': framework_metadata['anchor_count'],
        'overall_centroid': overall_centroid.tolist(),
        'discourse_intensity': float(np.linalg.norm(overall_centroid)),
        'coordinate_space_utilization': float(np.std(all_coords)),
        'x_spread': float(np.std(all_coords[:, 0])),
        'y_spread': float(np.std(all_coords[:, 1])),
        'max_distance_from_origin': float(np.max([np.linalg.norm(coord) for coord in all_coords])),
        'min_distance_from_origin': float(np.min([np.linalg.norm(coord) for coord in all_coords]))
    }

def detect_temporal_patterns(results_df, signatures):
    """Auto-detect temporal patterns in the data
    
    Identifies if the dataset has temporal information and extracts
    patterns for temporal analysis visualization.
    
    Args:
        results_df: DataFrame with speech data
        signatures: Dictionary mapping speech_id to coordinates
        
    Returns:
        dict: Temporal pattern information
    """
    temporal_info = {
        'has_temporal_data': False,
        'temporal_column': None,
        'phases': [],
        'phase_centroids': {}
    }
    
    # Check for date/time columns
    date_columns = [col for col in results_df.columns 
                   if 'date' in col.lower() or 'time' in col.lower()]
    
    if date_columns:
        temporal_info['has_temporal_data'] = True
        temporal_info['temporal_column'] = date_columns[0]
    
    # Check for phase columns
    phase_columns = [col for col in results_df.columns 
                    if 'phase' in col.lower() or 'period' in col.lower()]
    
    if phase_columns:
        phase_col = phase_columns[0]
        phases = results_df[phase_col].unique()
        temporal_info['phases'] = list(phases)
        
        # Calculate phase centroids
        for phase in phases:
            phase_mask = results_df[phase_col] == phase
            phase_speeches = results_df[phase_mask]['speech_id'].values
            phase_coords = np.array([signatures[speech_id] for speech_id in phase_speeches 
                                   if speech_id in signatures])
            if len(phase_coords) > 0:
                temporal_info['phase_centroids'][phase] = np.mean(phase_coords, axis=0).tolist()
    
    return temporal_info 