"""
Jupyter-Native DCS Analysis Interface
====================================

This module provides simple, Jupyter-friendly interfaces to DCS analysis capabilities.
Designed to satisfy the five Jupyter Native Integration Heuristics:

1. Data Fluidity: All functions return standard pandas DataFrames
2. Standard Library Integration: Built on matplotlib/seaborn/plotly  
3. Pedagogical Clarity: Well-documented with examples
4. Self-Containment: Minimal dependencies, clear imports
5. Modularity & Hackability: Copy-friendly functions

Usage:
    import discernus.analysis.jupyter_native_dcs as dcs
    
    # Simple function interfaces
    results_df = dcs.analyze_model_similarity(condition_results)
    fig = dcs.plot_circular_comparison(anchors, analysis_a, analysis_b)
    correlation_df = dcs.calculate_score_correlations(model_data)
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Any, Optional
import json

# Import existing functionality
from .statistical_methods import StatisticalMethodRegistry
from ..reporting.reboot_plotly_circular import RebootPlotlyCircularVisualizer


def analyze_model_similarity(condition_results: List[Dict], 
                           methods: List[str] = None) -> pd.DataFrame:
    """
    Analyze similarity between models using multiple statistical methods.
    
    Args:
        condition_results: List of model analysis results
        methods: Statistical methods to apply (default: ['geometric_similarity', 'dimensional_correlation'])
    
    Returns:
        DataFrame with similarity metrics for each method
        
    Example:
        >>> results = analyze_model_similarity(model_outputs)
        >>> print(results['mean_distance'])  # Direct DataFrame access
    """
    if methods is None:
        methods = ['geometric_similarity', 'dimensional_correlation']
    
    registry = StatisticalMethodRegistry()
    
    # Convert to expected format for statistical methods
    analysis_data = []
    for result in condition_results:
        # Mock AnalysisResultV2 object
        class MockResult:
            def __init__(self, result_dict):
                self.centroid_x = result_dict['centroid'][0]
                self.centroid_y = result_dict['centroid'][1] 
                self.raw_scores = json.dumps(result_dict['raw_scores'])
                self.model = result_dict['condition_identifier']
                self.id = result_dict.get('id', 'unknown')
        
        analysis_data.append(MockResult(result))
    
    # Run statistical analyses
    results = {}
    for method in methods:
        try:
            method_result = registry.analyze(method, analysis_data)
            results[method] = method_result
        except Exception as e:
            results[method] = {'error': str(e)}
    
    # Convert to DataFrame format
    summary_data = []
    for method, result in results.items():
        if 'error' not in result:
            if method == 'geometric_similarity':
                summary_data.append({
                    'method': method,
                    'mean_distance': result.get('mean_distance', np.nan),
                    'max_distance': result.get('max_distance', np.nan),
                    'variance': result.get('variance', np.nan)
                })
            elif method == 'dimensional_correlation':
                correlation_matrix = result.get('correlation_matrix', [])
                if correlation_matrix:
                    # Calculate average correlation
                    correlations = []
                    for i in range(len(correlation_matrix)):
                        for j in range(len(correlation_matrix[i])):
                            if i != j:
                                correlations.append(correlation_matrix[i][j])
                    avg_correlation = np.mean(correlations) if correlations else np.nan
                    summary_data.append({
                        'method': method,
                        'average_correlation': avg_correlation,
                        'model_count': result.get('model_count', 0)
                    })
        else:
            summary_data.append({
                'method': method,
                'error': result['error']
            })
    
    return pd.DataFrame(summary_data)


def calculate_score_correlations(model_data: Dict[str, List[Dict]]) -> pd.DataFrame:
    """
    Calculate score correlations between models across all texts.
    
    Args:
        model_data: Dict mapping model names to lists of analysis results
        
    Returns:
        DataFrame with pairwise model correlations
        
    Example:
        >>> corr_df = calculate_score_correlations(model_groups)
        >>> corr_df.pivot('model_1', 'model_2', 'correlation')  # Correlation matrix
    """
    # Aggregate scores by model
    model_scores = {}
    all_text_ids = set()
    
    for model, results in model_data.items():
        model_scores[model] = {}
        for result in results:
            text_id = result.get('text_id', result.get('id', 'unknown'))
            all_text_ids.add(text_id)
            model_scores[model][text_id] = result['scores']
    
    # Create correlation matrix
    models = list(model_scores.keys())
    correlation_data = []
    
    for i, model_1 in enumerate(models):
        for j, model_2 in enumerate(models):
            if i <= j:  # Only upper triangular + diagonal
                # Collect scores for common texts
                common_texts = set(model_scores[model_1].keys()) & set(model_scores[model_2].keys())
                
                if len(common_texts) < 2:
                    correlation = np.nan
                else:
                    # Get all foundation scores for common texts
                    scores_1 = []
                    scores_2 = []
                    
                    for text_id in common_texts:
                        text_scores_1 = model_scores[model_1][text_id]
                        text_scores_2 = model_scores[model_2][text_id]
                        
                        # Get common foundations
                        common_foundations = set(text_scores_1.keys()) & set(text_scores_2.keys())
                        
                        for foundation in common_foundations:
                            scores_1.append(text_scores_1[foundation])
                            scores_2.append(text_scores_2[foundation])
                    
                    if len(scores_1) >= 2:
                        correlation = np.corrcoef(scores_1, scores_2)[0, 1]
                    else:
                        correlation = np.nan
                
                correlation_data.append({
                    'model_1': model_1,
                    'model_2': model_2, 
                    'correlation': correlation,
                    'common_texts': len(common_texts) if 'common_texts' in locals() else 0
                })
    
    return pd.DataFrame(correlation_data)


def plot_circular_comparison(anchors: Dict, 
                           analysis_a: Dict, 
                           analysis_b: Dict,
                           title: str = "Model Comparison") -> go.Figure:
    """
    Create circular coordinate comparison plot between two analyses.
    
    Args:
        anchors: Anchor definitions with angles and types
        analysis_a: First analysis with scores and centroid
        analysis_b: Second analysis with scores and centroid  
        title: Plot title
        
    Returns:
        Plotly figure object for display in Jupyter
        
    Example:
        >>> fig = plot_circular_comparison(framework_anchors, model_1_result, model_2_result)
        >>> fig.show()  # Direct Jupyter display
    """
    visualizer = RebootPlotlyCircularVisualizer()
    
    return visualizer.plot_comparison(
        anchors=anchors,
        analysis_a=analysis_a,
        label_a=analysis_a.get('model', 'Model A'),
        analysis_b=analysis_b, 
        label_b=analysis_b.get('model', 'Model B'),
        title=title,
        show=False  # Return figure instead of showing
    )


def plot_multi_model_overview(model_summaries: Dict[str, Dict],
                             anchors: Dict = None) -> go.Figure:
    """
    Create overview plot showing all model centroids.
    
    Args:
        model_summaries: Dict mapping model names to summary data with centroids
        anchors: Optional anchor definitions for context
        
    Returns:
        Plotly figure object
        
    Example:
        >>> summaries = {model: {'centroid': avg_centroid} for model, avg_centroid in centroids.items()}
        >>> fig = plot_multi_model_overview(summaries)
        >>> fig.show()
    """
    models = list(model_summaries.keys())
    centroids = [summary['centroid'] for summary in model_summaries.values()]
    
    x_coords = [c[0] for c in centroids]
    y_coords = [c[1] for c in centroids]
    
    # Create base circular plot
    fig = go.Figure()
    
    # Add unit circle
    theta = np.linspace(0, 2 * np.pi, 361)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    
    fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add model centroids
    colors = px.colors.qualitative.Set1[:len(models)]
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        text=models,
        textposition='top center',
        marker=dict(size=15, color=colors, line=dict(width=2, color='white')),
        name='Model Centroids',
        hovertemplate='<b>%{text}</b><br>Position: (%{x:.3f}, %{y:.3f})<extra></extra>'
    ))
    
    # Layout
    fig.update_layout(
        title="Multi-Model Comparison Overview",
        xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-1.2, 1.2]),
        showlegend=False,
        width=600,
        height=600
    )
    
    return fig


def export_for_stata(analysis_results: pd.DataFrame, 
                    filepath: str,
                    variable_labels: Dict[str, str] = None) -> str:
    """
    Export analysis results to Stata format with proper variable labels.
    
    Args:
        analysis_results: DataFrame with analysis results
        filepath: Output filepath (.dta extension)
        variable_labels: Optional mapping of column names to descriptive labels
        
    Returns:
        Confirmation message with filepath
        
    Example:
        >>> export_for_stata(results_df, 'analysis_results.dta')
        'Data exported to analysis_results.dta'
    """
    try:
        # Try to use pandas' Stata export
        analysis_results.to_stata(filepath, variable_labels=variable_labels)
        return f"Data exported to {filepath}"
    except ImportError:
        # Fallback to CSV with metadata
        csv_path = filepath.replace('.dta', '.csv')
        analysis_results.to_csv(csv_path, index=False)
        
        # Write variable labels as separate file
        if variable_labels:
            labels_path = filepath.replace('.dta', '_labels.txt')
            with open(labels_path, 'w') as f:
                for var, label in variable_labels.items():
                    f.write(f"{var}: {label}\n")
            return f"Data exported to {csv_path} (Stata not available, exported as CSV with labels in {labels_path})"
        else:
            return f"Data exported to {csv_path} (Stata not available, exported as CSV)"


def create_publication_figure(plot_function, *args, **kwargs) -> Tuple[go.Figure, str]:
    """
    Create publication-ready figure with proper formatting.
    
    Args:
        plot_function: Function that returns a Plotly figure
        *args, **kwargs: Arguments passed to plot_function
        
    Returns:
        Tuple of (figure, save_instruction)
        
    Example:
        >>> fig, save_cmd = create_publication_figure(plot_circular_comparison, anchors, model_a, model_b)
        >>> exec(save_cmd)  # Saves as high-quality PNG
    """
    fig = plot_function(*args, **kwargs)
    
    # Apply publication formatting
    fig.update_layout(
        font=dict(family="Arial", size=12),
        title=dict(font=dict(size=16)),
        width=800,
        height=600,
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    # Generate save command
    save_cmd = "fig.write_image('publication_figure.png', width=800, height=600, scale=2)"
    
    return fig, save_cmd


# Convenience function for common workflow
def quick_model_comparison(model_groups: Dict[str, List[Dict]], 
                          anchors: Dict = None) -> Dict[str, Any]:
    """
    Perform complete model comparison analysis with common metrics.
    
    Args:
        model_groups: Dict mapping model names to lists of analysis results
        anchors: Optional anchor definitions
        
    Returns:
        Dict containing DataFrames and figures for complete analysis
        
    Example:
        >>> results = quick_model_comparison(model_data)
        >>> results['similarity_df']  # Similarity metrics
        >>> results['correlation_df']  # Score correlations
        >>> results['overview_fig'].show()  # Overview plot
    """
    # Calculate model averages
    model_summaries = {}
    condition_results = []
    
    for model, results in model_groups.items():
        if results:
            # Calculate average centroid
            centroids = [r['centroid'] for r in results if 'centroid' in r]
            if centroids:
                avg_centroid = (
                    np.mean([c[0] for c in centroids]),
                    np.mean([c[1] for c in centroids])
                )
                model_summaries[model] = {'centroid': avg_centroid}
                
                # Add to condition results for similarity analysis
                condition_results.append({
                    'condition_identifier': model,
                    'centroid': avg_centroid,
                    'raw_scores': results[0].get('scores', {})  # Use first result's scores as representative
                })
    
    # Run analyses
    similarity_df = analyze_model_similarity(condition_results)
    correlation_df = calculate_score_correlations(model_groups)
    overview_fig = plot_multi_model_overview(model_summaries, anchors)
    
    return {
        'similarity_df': similarity_df,
        'correlation_df': correlation_df,
        'overview_fig': overview_fig,
        'model_summaries': model_summaries,
        'condition_results': condition_results
    }


# Copy-friendly function examples for researchers
def copy_friendly_circular_plot(anchors_dict, scores_dict, title="Custom Analysis"):
    """
    Simple circular plot function designed to be copied and modified.
    
    Copy this function into your notebook and modify as needed.
    """
    import plotly.graph_objects as go
    import numpy as np
    
    fig = go.Figure()
    
    # Draw circle boundary
    theta = np.linspace(0, 2 * np.pi, 361)
    x_circle = np.cos(theta) 
    y_circle = np.sin(theta)
    fig.add_trace(go.Scatter(x=x_circle, y=y_circle, mode='lines', 
                            line=dict(color='black', width=2), 
                            showlegend=False))
    
    # Plot anchors and calculate centroid
    centroid_x, centroid_y = 0, 0
    total_weight = 0
    
    for anchor_name, score in scores_dict.items():
        if anchor_name in anchors_dict:
            angle = np.deg2rad(anchors_dict[anchor_name]['angle'])
            weight = anchors_dict[anchor_name].get('weight', 1.0)
            
            x = np.cos(angle)
            y = np.sin(angle)
            
            # Add anchor
            fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers+text',
                                   text=[anchor_name], textposition='top center',
                                   marker=dict(size=12, color='blue'),
                                   showlegend=False))
            
            # Calculate centroid contribution
            force = score * weight
            centroid_x += x * force
            centroid_y += y * force
            total_weight += force
    
    # Add centroid
    if total_weight > 0:
        centroid_x /= total_weight
        centroid_y /= total_weight
        fig.add_trace(go.Scatter(x=[centroid_x], y=[centroid_y], 
                               mode='markers',
                               marker=dict(size=20, color='red'),
                               name='Centroid'))
    
    fig.update_layout(title=title, 
                     xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
                     yaxis=dict(range=[-1.2, 1.2]))
    
    return fig


def copy_friendly_correlation_analysis(model_data_dict):
    """
    Simple correlation analysis function designed to be copied and modified.
    
    Copy this function into your notebook and modify as needed.
    """
    import pandas as pd
    import numpy as np
    
    # Flatten data structure
    all_results = []
    for model, results in model_data_dict.items():
        for result in results:
            result_copy = result.copy()
            result_copy['model'] = model
            all_results.append(result_copy)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Calculate pairwise correlations
    models = df['model'].unique()
    correlation_matrix = pd.DataFrame(index=models, columns=models)
    
    for model1 in models:
        for model2 in models:
            if model1 == model2:
                correlation_matrix.loc[model1, model2] = 1.0
            else:
                # Get scores for both models
                scores1 = df[df['model'] == model1]['scores'].tolist()
                scores2 = df[df['model'] == model2]['scores'].tolist()
                
                # Extract comparable score values
                score_pairs = []
                for s1, s2 in zip(scores1, scores2):
                    common_keys = set(s1.keys()) & set(s2.keys())
                    for key in common_keys:
                        score_pairs.append((s1[key], s2[key]))
                
                if len(score_pairs) >= 2:
                    values1, values2 = zip(*score_pairs)
                    correlation = np.corrcoef(values1, values2)[0, 1]
                else:
                    correlation = np.nan
                
                correlation_matrix.loc[model1, model2] = correlation
    
    return correlation_matrix 