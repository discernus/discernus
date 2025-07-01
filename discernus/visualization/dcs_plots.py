"""
DCS (Discernus Coordinate System) Standard Library Plotting Functions
=====================================================================

Publication-quality DCS visualization functions using standard matplotlib/numpy.
Extracted from the "Sarah Experience" notebook - the proven approach to DCS visualization.

Philosophy:
- Standard libraries only (matplotlib, numpy, pandas)
- Framework Specification v3.1+ compatible
- Academic publication ready (Nature/Science journal standards)
- No custom abstractions - follows "Sarah Experience" principles

Functions:
- plot_dcs_framework(): Universal DCS visualization for any framework
- plot_coordinate_space(): Core DCS coordinate plotting with unit circle
- plot_competitive_dynamics(): Competitive relationship visualization
- plot_temporal_evolution(): Campaign/temporal discourse dynamics
- setup_publication_style(): Academic journal plotting standards
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import warnings

def setup_publication_style(style: str = 'nature') -> None:
    """
    Configure matplotlib for academic publication standards
    
    Args:
        style: Publication style ('nature', 'science', 'academic')
    """
    base_config = {
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
    }
    
    if style == 'science':
        base_config.update({
            'font.size': 9,
            'axes.linewidth': 0.8,
            'legend.fontsize': 8
        })
    elif style == 'academic':
        base_config.update({
            'font.size': 10,
            'figure.dpi': 120,
            'legend.fontsize': 9
        })
    
    plt.rcParams.update(base_config)

def extract_framework_anchors(framework_config: Dict) -> Dict[str, Dict]:
    """
    Extract anchor configuration from Framework Specification v3.1+ format
    
    Args:
        framework_config: Framework configuration dictionary
        
    Returns:
        Dictionary of anchor configurations with positions and metadata
    """
    anchors = {}
    
    # Handle both 'anchors' and 'axes' formats for v3.1+ compatibility
    anchor_source = framework_config.get('anchors', framework_config.get('axes', {}))
    
    if not anchor_source:
        raise ValueError("No anchors or axes found in framework configuration")
    
    # Default colors for anchors
    default_colors = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b']
    
    for i, (name, config) in enumerate(anchor_source.items()):
        # Extract position - handle different formats
        if 'position' in config:
            position = tuple(config['position'])
        elif 'angle' in config:
            # Convert angle to unit circle position
            angle_rad = np.radians(config['angle'])
            position = (np.cos(angle_rad), np.sin(angle_rad))
        else:
            # Default positioning in unit circle
            angle = (i * 2 * np.pi) / len(anchor_source)
            position = (np.cos(angle), np.sin(angle))
        
        anchors[name] = {
            'position': position,
            'color': config.get('color', default_colors[i % len(default_colors)]),
            'description': config.get('description', f'{name.title()} anchor'),
            'angle': config.get('angle', np.degrees(np.arctan2(position[1], position[0])))
        }
    
    return anchors

def calculate_signature_coordinates(scores_dict: Dict[str, float], 
                                  framework_config: Dict) -> Tuple[np.ndarray, Dict]:
    """
    Calculate DCS signature coordinates from anchor scores
    
    Args:
        scores_dict: Dictionary of anchor scores
        framework_config: Framework configuration
        
    Returns:
        Tuple of (signature_coordinates, calculation_metadata)
    """
    anchors = extract_framework_anchors(framework_config)
    
    # Extract positions and scores
    anchor_names = list(anchors.keys())
    anchor_positions = np.array([anchors[name]['position'] for name in anchor_names])
    scores = np.array([scores_dict.get(name, 0.0) for name in anchor_names])
    
    # Handle competitive dynamics if specified
    competitive_effects = {}
    if 'competitive_relationships' in framework_config:
        adjusted_scores = scores.copy()
        
        for comp in framework_config['competitive_relationships']:
            if 'anchors' in comp and 'strength' in comp:
                anchor1, anchor2 = comp['anchors']
                strength = comp['strength']
                
                if anchor1 in scores_dict and anchor2 in scores_dict:
                    idx1 = anchor_names.index(anchor1)
                    idx2 = anchor_names.index(anchor2)
                    
                    # Apply competitive dilution when both scores are high
                    if scores[idx1] > 0.6 and scores[idx2] > 0.6:
                        dilution_factor = 1 - (strength * 0.1)
                        adjusted_scores[idx1] *= dilution_factor
                        adjusted_scores[idx2] *= dilution_factor
                        
                        competitive_effects[f"{anchor1}_{anchor2}"] = {
                            'original': [scores[idx1], scores[idx2]],
                            'adjusted': [adjusted_scores[idx1], adjusted_scores[idx2]],
                            'dilution': dilution_factor
                        }
        
        scores = adjusted_scores
    
    # Calculate weighted centroid
    if np.sum(scores) > 0:
        signature = np.average(anchor_positions, weights=scores, axis=0)
        # Keep within unit circle
        magnitude = np.linalg.norm(signature)
        if magnitude > 1.0:
            signature = signature / magnitude
    else:
        signature = np.array([0.0, 0.0])
    
    metadata = {
        'scores': scores_dict,
        'magnitude': float(np.linalg.norm(signature)),
        'competitive_effects': competitive_effects,
        'anchor_count': len(anchors)
    }
    
    return signature, metadata

def plot_coordinate_space(anchors: Dict[str, Dict], 
                         signatures: Dict[str, np.ndarray] = None,
                         ax: plt.Axes = None,
                         show_unit_circle: bool = True,
                         show_grid: bool = True,
                         **kwargs) -> plt.Axes:
    """
    Core DCS coordinate plotting with unit circle
    
    Args:
        anchors: Anchor configuration dictionary
        signatures: Optional signature coordinates to plot
        ax: Optional matplotlib axes
        show_unit_circle: Whether to show unit circle boundary
        show_grid: Whether to show coordinate grid
        **kwargs: Additional plotting arguments
        
    Returns:
        Matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # Unit circle boundary
    if show_unit_circle:
        circle = patches.Circle((0, 0), 1, fill=False, color='black', 
                               linewidth=kwargs.get('circle_linewidth', 1.5), 
                               alpha=kwargs.get('circle_alpha', 0.8))
        ax.add_patch(circle)
    
    # Grid lines
    if show_grid:
        ax.axhline(y=0, color='lightgray', linewidth=0.5, alpha=0.4)
        ax.axvline(x=0, color='lightgray', linewidth=0.5, alpha=0.4)
    
    # Plot anchors
    for name, config in anchors.items():
        x, y = config['position']
        color = config['color']
        
        ax.scatter(x, y, s=kwargs.get('anchor_size', 150), c=color, 
                  marker=kwargs.get('anchor_marker', 's'), 
                  edgecolors='black', linewidth=2, zorder=10, alpha=0.9)
        
        # Position labels
        label_offset = kwargs.get('label_offset', 1.25)
        label_x, label_y = x * label_offset, y * label_offset
        ax.annotate(name.title(), (label_x, label_y), 
                   fontsize=kwargs.get('label_fontsize', 10), 
                   ha='center', va='center', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Plot signatures if provided
    if signatures:
        coords_array = np.array(list(signatures.values()))
        colors = kwargs.get('signature_colors', None)
        
        if colors is None:
            # Default color scheme
            colors = plt.cm.tab10(np.linspace(0, 1, len(signatures)))
        
        for i, (name, coords) in enumerate(signatures.items()):
            color = colors[i] if hasattr(colors, '__len__') else colors
            ax.scatter(coords[0], coords[1], s=kwargs.get('signature_size', 60), 
                      c=color, alpha=kwargs.get('signature_alpha', 0.7), 
                      edgecolors='white', linewidth=0.5, zorder=5)
    
    # Formatting
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect('equal')
    ax.set_xlabel(kwargs.get('xlabel', 'DCS Dimension 1'), 
                  fontsize=kwargs.get('axis_fontsize', 11))
    ax.set_ylabel(kwargs.get('ylabel', 'DCS Dimension 2'), 
                  fontsize=kwargs.get('axis_fontsize', 11))
    
    if kwargs.get('grid', True):
        ax.grid(True, alpha=0.2)
    
    return ax

def plot_competitive_dynamics(framework_config: Dict, 
                            signatures: Dict[str, np.ndarray],
                            competitive_effects: Dict = None,
                            figsize: Tuple[int, int] = (14, 6)) -> Tuple[plt.Figure, Tuple[plt.Axes, plt.Axes]]:
    """
    Competitive relationship visualization with effects analysis
    
    Args:
        framework_config: Framework configuration with competitive relationships
        signatures: Signature coordinates
        competitive_effects: Optional competitive effects data
        figsize: Figure size tuple
        
    Returns:
        Tuple of (figure, (main_ax, effects_ax))
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Extract anchors and competitive relationships
    anchors = extract_framework_anchors(framework_config)
    competitions = framework_config.get('competitive_relationships', [])
    
    # LEFT PLOT: DCS Coordinate Space with Competitive Dynamics
    ax1 = plot_coordinate_space(anchors, signatures, ax=ax1, 
                               signature_colors=plt.cm.tab10(np.linspace(0, 1, len(signatures))))
    
    # Add competitive relationship lines
    for comp in competitions:
        if 'anchors' in comp and 'strength' in comp:
            anchor1, anchor2 = comp['anchors']
            strength = comp['strength']
            
            if anchor1 in anchors and anchor2 in anchors:
                pos1 = anchors[anchor1]['position']
                pos2 = anchors[anchor2]['position']
                
                # Draw competition line with thickness representing strength
                ax1.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                        color='purple', linewidth=strength*3, alpha=0.3, linestyle='--')
                
                # Add midpoint label
                mid_x, mid_y = (pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2
                ax1.text(mid_x, mid_y, f'{strength:.1f}', fontsize=8, ha='center', va='center',
                        bbox=dict(boxstyle='circle,pad=0.2', facecolor='purple', alpha=0.6))
    
    ax1.set_title('Competitive Discourse Space', fontsize=12, weight='bold', pad=15)
    
    # RIGHT PLOT: Competitive Effects Analysis
    if competitive_effects and competitions:
        # Calculate competitive dilution statistics
        dilution_stats = {comp['anchors'][0]: [] for comp in competitions if 'anchors' in comp}
        dilution_stats.update({comp['anchors'][1]: [] for comp in competitions if 'anchors' in comp})
        
        for effect_data in competitive_effects.values():
            for anchor in dilution_stats.keys():
                if anchor in effect_data.get('original_scores', {}):
                    original = effect_data['original_scores'][anchor]
                    adjusted = effect_data['adjusted_scores'][anchor]
                    if original > 0:
                        dilution_pct = ((adjusted - original) / original) * 100
                        dilution_stats[anchor].append(dilution_pct)
        
        # Create box plot of competitive effects
        anchor_names = [name for name in dilution_stats.keys() if dilution_stats[name]]
        dilution_data = [dilution_stats[name] for name in anchor_names]
        
        if dilution_data:
            colors = [anchors[name]['color'] for name in anchor_names]
            box_plot = ax2.boxplot(dilution_data, labels=[name.title() for name in anchor_names],
                                  patch_artist=True, notch=True)
            
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax2.set_ylabel('Competitive Dilution (%)', fontsize=10)
            ax2.set_title('Competitive Dynamics Effects', fontsize=12, weight='bold', pad=15)
            ax2.grid(True, alpha=0.3, axis='y')
        else:
            ax2.text(0.5, 0.5, 'No competitive effects data', ha='center', va='center',
                    transform=ax2.transAxes, fontsize=12)
            ax2.set_title('Competitive Effects (No Data)', fontsize=12, weight='bold')
    else:
        ax2.text(0.5, 0.5, 'No competitive relationships defined', ha='center', va='center',
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Competitive Effects (Not Configured)', fontsize=12, weight='bold')
    
    plt.tight_layout()
    return fig, (ax1, ax2)

def plot_dcs_framework(framework_config: Dict, 
                      experiment_results: Dict,
                      title: str = None,
                      figsize: Tuple[int, int] = (10, 8),
                      **kwargs) -> Tuple[plt.Figure, plt.Axes]:
    """
    Universal DCS visualization for any Framework Specification v3.1+ framework
    
    Args:
        framework_config: Framework configuration dictionary
        experiment_results: Experiment results with condition data
        title: Optional plot title
        figsize: Figure size tuple
        **kwargs: Additional plotting arguments
        
    Returns:
        Tuple of (figure, axes)
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # Extract framework information
    framework_name = framework_config.get('name', 'Unknown Framework')
    anchors = extract_framework_anchors(framework_config)
    
    # Process experiment results
    condition_results = experiment_results.get('condition_results', [])
    signatures = {}
    
    for condition in condition_results:
        condition_id = condition.get('condition_identifier', 'Unknown')
        centroid = condition.get('centroid', [0, 0])
        
        if len(centroid) >= 2:
            signatures[condition_id] = np.array(centroid[:2])
    
    # Plot coordinate space
    ax = plot_coordinate_space(anchors, signatures, ax=ax, **kwargs)
    
    # Add model labels and enhanced styling
    for i, (model_name, coords) in enumerate(signatures.items()):
        # Enhanced scatter plot for models
        ax.scatter(coords[0], coords[1], s=200, alpha=0.8, 
                  edgecolors='black', linewidth=1, zorder=8)
        
        # Model labels with better positioning
        ax.annotate(model_name, (coords[0], coords[1]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=10, ha='left', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))
    
    # Calculate and show overall centroid if multiple models
    if len(signatures) > 1:
        all_coords = np.array(list(signatures.values()))
        overall_centroid = np.mean(all_coords, axis=0)
        ax.scatter(overall_centroid[0], overall_centroid[1], s=250, c='red', 
                  marker='*', edgecolors='darkred', linewidth=3, zorder=15, 
                  label='Overall Centroid')
        ax.legend()
    
    # Title and formatting
    if title is None:
        title = f'DCS Analysis: {framework_name}'
    ax.set_title(title, fontsize=14, weight='bold', pad=20)
    
    return fig, ax

def plot_temporal_evolution(framework_config: Dict,
                          temporal_data: pd.DataFrame,
                          phase_column: str = 'temporal_phase',
                          signature_column: str = 'signature_coords',
                          figsize: Tuple[int, int] = (16, 10)) -> Tuple[plt.Figure, Dict]:
    """
    Advanced temporal analysis showing discourse evolution over time
    
    Args:
        framework_config: Framework configuration
        temporal_data: DataFrame with temporal analysis data
        phase_column: Column name for temporal phases
        signature_column: Column name for signature coordinates
        figsize: Figure size tuple
        
    Returns:
        Tuple of (figure, analysis_data)
    """
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1])
    
    # Main trajectory plot
    ax_main = fig.add_subplot(gs[0, :])
    anchors = extract_framework_anchors(framework_config)
    
    # Plot base coordinate space
    ax_main = plot_coordinate_space(anchors, ax=ax_main)
    
    # Process temporal phases
    phases = temporal_data[phase_column].unique()
    phase_colors = plt.cm.Set1(np.linspace(0, 1, len(phases)))
    phase_data = {}
    
    for i, phase in enumerate(phases):
        phase_mask = temporal_data[phase_column] == phase
        phase_df = temporal_data[phase_mask]
        
        if len(phase_df) > 0:
            # Extract coordinates (assume they're stored in signature_column)
            if signature_column in phase_df.columns:
                coords = np.array([coord for coord in phase_df[signature_column].values 
                                 if isinstance(coord, (list, np.ndarray)) and len(coord) >= 2])
            else:
                # Try to reconstruct from individual score columns
                score_columns = [col for col in phase_df.columns if col.endswith('_score')]
                coords = []
                for _, row in phase_df.iterrows():
                    scores = {col.replace('_score', ''): row[col] for col in score_columns}
                    signature, _ = calculate_signature_coordinates(scores, framework_config)
                    coords.append(signature)
                coords = np.array(coords)
            
            if len(coords) > 0:
                centroid = np.mean(coords, axis=0)
                phase_data[phase] = {
                    'coordinates': coords,
                    'centroid': centroid,
                    'count': len(coords),
                    'color': phase_colors[i]
                }
                
                # Plot individual points
                ax_main.scatter(coords[:, 0], coords[:, 1], 
                               s=60, c=phase_colors[i], alpha=0.6, 
                               edgecolors='white', linewidth=1, zorder=5)
                
                # Plot phase centroid
                ax_main.scatter(centroid[0], centroid[1], s=200, c=phase_colors[i], 
                               marker='D', edgecolors='black', linewidth=2, zorder=12)
                
                # Add phase labels
                ax_main.annotate(f"{phase}\n({len(coords)})", (centroid[0], centroid[1]), 
                               xytext=(15, 15), textcoords='offset points', 
                               fontsize=10, weight='bold', ha='center',
                               bbox=dict(boxstyle='round,pad=0.5', 
                                        facecolor=phase_colors[i], alpha=0.8))
    
    # Draw trajectory if multiple phases
    if len(phase_data) >= 2:
        centroids = [data['centroid'] for data in phase_data.values()]
        trajectory_array = np.array(centroids)
        
        ax_main.plot(trajectory_array[:, 0], trajectory_array[:, 1], 
                    'k-', linewidth=3, alpha=0.8, zorder=8, label='Evolution Trajectory')
        
        # Add arrows between phases
        for i in range(len(trajectory_array) - 1):
            start = trajectory_array[i]
            end = trajectory_array[i + 1]
            ax_main.annotate('', xy=end, xytext=start,
                           arrowprops=dict(arrowstyle='->', lw=2, color='darkred', alpha=0.8))
    
    ax_main.set_title('Temporal Discourse Evolution', fontsize=14, weight='bold', pad=20)
    ax_main.legend()
    
    # Phase statistics plot
    ax_stats = fig.add_subplot(gs[0, 1])
    
    if phase_data:
        phases_list = list(phase_data.keys())
        intensities = [np.linalg.norm(data['centroid']) for data in phase_data.values()]
        colors = [data['color'] for data in phase_data.values()]
        
        bars = ax_stats.bar(range(len(phases_list)), intensities, color=colors, alpha=0.8)
        ax_stats.set_title('Phase\nIntensity', fontsize=11, weight='bold')
        ax_stats.set_ylabel('Discourse Intensity', fontsize=9)
        ax_stats.set_xticks(range(len(phases_list)))
        ax_stats.set_xticklabels([p.replace('_', '\n') for p in phases_list], fontsize=8)
        ax_stats.grid(True, alpha=0.3, axis='y')
    
    # Timeline plot
    ax_timeline = fig.add_subplot(gs[1, :])
    
    if phase_data and len(temporal_data) > 0:
        # Create timeline visualization
        if 'date' in temporal_data.columns:
            # Use actual dates if available
            for phase, data in phase_data.items():
                phase_dates = temporal_data[temporal_data[phase_column] == phase]['date']
                if len(phase_dates) > 0:
                    y_pos = list(phase_data.keys()).index(phase)
                    ax_timeline.scatter(phase_dates, [y_pos] * len(phase_dates), 
                                       c=data['color'], alpha=0.7, s=30)
            
            ax_timeline.set_xlabel('Date', fontsize=10)
        else:
            # Use phase order
            x_positions = list(range(len(phase_data)))
            y_data = [len(data['coordinates']) for data in phase_data.values()]
            
            ax_timeline.bar(x_positions, y_data, 
                           color=[data['color'] for data in phase_data.values()], alpha=0.8)
            ax_timeline.set_xlabel('Phase', fontsize=10)
            ax_timeline.set_xticks(x_positions)
            ax_timeline.set_xticklabels(list(phase_data.keys()))
        
        ax_timeline.set_ylabel('Count', fontsize=10)
        ax_timeline.set_title('Temporal Distribution', fontsize=11, weight='bold')
        ax_timeline.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, phase_data 