"""
Framework Validation Metrics
============================

Core mathematical validation metrics implementing Mathematical Foundations v1.0.
Focus: Territorial coverage, anchor independence, cartographic resolution.

Critical Path: Brazil 2018 Democratic Tension Axis Model validation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.stats import pearsonr
import warnings

def calculate_territorial_coverage(
    signatures: np.ndarray,
    framework_config: Dict,
    pca_components: int = 3,
    variance_threshold: float = 0.95
) -> Dict[str, float]:
    """
    Calculate territorial coverage using PCA-based theoretical space explanation.
    
    From Mathematical Foundations v1.0:
    "For signature matrix S with theoretical weights W:
     weighted_signature_matrix = S ⊙ W  (element-wise multiplication)
     pca = PCA(weighted_signature_matrix)
     territorial_coverage = Σ(explained_variance_ratio_i) for i capturing 95% variance"
    
    Args:
        signatures: Array of signature coordinates (n_samples, 2)
        framework_config: Framework configuration dictionary
        pca_components: Number of PCA components to analyze
        variance_threshold: Variance threshold for coverage calculation
        
    Returns:
        Dictionary with coverage metrics
    """
    # TODO: Implement theoretical weighting multiplication
    # For now, use unweighted signatures
    
    if len(signatures) < 2:
        return {
            'territorial_coverage': 0.0,
            'explained_variance_ratio': [],
            'cumulative_variance': 0.0,
            'components_for_threshold': 0
        }
    
    try:
        # Basic PCA analysis
        pca = PCA(n_components=min(pca_components, signatures.shape[1], signatures.shape[0]))
        pca.fit(signatures)
        
        explained_variance = pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        # Find components needed for variance threshold
        components_needed = np.where(cumulative_variance >= variance_threshold)[0]
        components_for_threshold = components_needed[0] + 1 if len(components_needed) > 0 else len(explained_variance)
        
        # Calculate coverage score
        coverage_score = cumulative_variance[components_for_threshold - 1] if components_for_threshold > 0 else 0.0
        
        return {
            'territorial_coverage': float(coverage_score),
            'explained_variance_ratio': explained_variance.tolist(),
            'cumulative_variance': float(cumulative_variance[-1]),
            'components_for_threshold': int(components_for_threshold)
        }
        
    except Exception as e:
        warnings.warn(f"Error calculating territorial coverage: {e}")
        return {
            'territorial_coverage': 0.0,
            'explained_variance_ratio': [],
            'cumulative_variance': 0.0,
            'components_for_threshold': 0
        }

def calculate_anchor_independence_index(
    anchor_scores: Dict[str, List[float]],
    method: str = 'pearson'
) -> Dict[str, float]:
    """
    Calculate anchor independence using correlation analysis.
    
    From Mathematical Foundations v1.0:
    "correlation_matrix = corr(anchor_score_vectors)
     off_diagonal_correlations = {r_ij : i ≠ j}
     anchor_independence = 1 - max(|off_diagonal_correlations|)"
    
    Args:
        anchor_scores: Dictionary of anchor names to score lists
        method: Correlation method ('pearson', 'spearman', 'cosine')
        
    Returns:
        Dictionary with independence metrics
    """
    if len(anchor_scores) < 2:
        return {
            'anchor_independence_index': 1.0,
            'max_correlation': 0.0,
            'correlation_matrix': {},
            'method': method
        }
    
    try:
        # Create correlation matrix
        anchor_names = list(anchor_scores.keys())
        score_matrix = np.array([anchor_scores[name] for name in anchor_names]).T
        
        if method == 'pearson':
            correlation_matrix = np.corrcoef(score_matrix.T)
        else:
            # TODO: Implement spearman and cosine correlation methods
            correlation_matrix = np.corrcoef(score_matrix.T)
        
        # Extract off-diagonal correlations
        n = len(anchor_names)
        off_diagonal_correlations = []
        
        for i in range(n):
            for j in range(i + 1, n):
                if not np.isnan(correlation_matrix[i, j]):
                    off_diagonal_correlations.append(abs(correlation_matrix[i, j]))
        
        # Calculate independence index
        max_correlation = max(off_diagonal_correlations) if off_diagonal_correlations else 0.0
        independence_index = 1.0 - max_correlation
        
        # Create named correlation matrix
        correlation_dict = {}
        for i, name1 in enumerate(anchor_names):
            correlation_dict[name1] = {}
            for j, name2 in enumerate(anchor_names):
                correlation_dict[name1][name2] = float(correlation_matrix[i, j])
        
        return {
            'anchor_independence_index': float(independence_index),
            'max_correlation': float(max_correlation),
            'correlation_matrix': correlation_dict,
            'method': method
        }
        
    except Exception as e:
        warnings.warn(f"Error calculating anchor independence: {e}")
        return {
            'anchor_independence_index': 0.0,
            'max_correlation': 1.0,
            'correlation_matrix': {},
            'method': method
        }

def calculate_cartographic_resolution(
    signatures: np.ndarray,
    cluster_labels: Optional[List] = None,
    method: str = 'silhouette'
) -> Dict[str, float]:
    """
    Calculate cartographic resolution using clustering quality metrics.
    
    From Mathematical Foundations v1.0:
    "For signatures with arc positioning:
     weighting_adjusted_signatures = signatures × local_weighting_corrections
     silhouette_score = silhouette_analysis(weighting_adjusted_signatures, cluster_labels)"
    
    Args:
        signatures: Array of signature coordinates
        cluster_labels: Optional cluster labels for signatures
        method: Resolution calculation method
        
    Returns:
        Dictionary with resolution metrics
    """
    if len(signatures) < 2:
        return {
            'cartographic_resolution': 0.0,
            'silhouette_score': 0.0,
            'method': method
        }
    
    try:
        # TODO: Implement weighting corrections
        # For now, use unweighted signatures
        
        if cluster_labels is None:
            # Create basic clustering based on coordinate quadrants
            cluster_labels = []
            for sig in signatures:
                if sig[0] >= 0 and sig[1] >= 0:
                    cluster_labels.append(0)  # Q1
                elif sig[0] < 0 and sig[1] >= 0:
                    cluster_labels.append(1)  # Q2
                elif sig[0] < 0 and sig[1] < 0:
                    cluster_labels.append(2)  # Q3
                else:
                    cluster_labels.append(3)  # Q4
        
        # Calculate silhouette score
        if len(set(cluster_labels)) > 1:
            silhouette_avg = silhouette_score(signatures, cluster_labels)
        else:
            silhouette_avg = 0.0
        
        return {
            'cartographic_resolution': float(max(0.0, silhouette_avg)),
            'silhouette_score': float(silhouette_avg),
            'method': method,
            'n_clusters': len(set(cluster_labels))
        }
        
    except Exception as e:
        warnings.warn(f"Error calculating cartographic resolution: {e}")
        return {
            'cartographic_resolution': 0.0,
            'silhouette_score': 0.0,
            'method': method
        }

def calculate_framework_fitness_score(
    territorial_coverage: float,
    anchor_independence: float,
    cartographic_resolution: float,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Calculate composite framework fitness score.
    
    From Mathematical Foundations v1.0:
    "composite_performance = w₁ × territorial_coverage_adjusted + 
                            w₂ × cartographic_resolution_adjusted +
                            w₃ × navigational_accuracy_adjusted +
                            w₄ × temporal_coherence"
    
    Args:
        territorial_coverage: Territorial coverage score [0-1]
        anchor_independence: Anchor independence index [0-1]
        cartographic_resolution: Cartographic resolution score [0-1]
        weights: Optional custom weights for components
        
    Returns:
        Dictionary with fitness metrics
    """
    # Default weights for Brazil 2018 framework
    if weights is None:
        weights = {
            'territorial_coverage': 0.35,
            'anchor_independence': 0.35,
            'cartographic_resolution': 0.30
        }
    
    # Normalize weights
    total_weight = sum(weights.values())
    if total_weight > 0:
        weights = {k: v / total_weight for k, v in weights.items()}
    else:
        weights = {'territorial_coverage': 0.33, 'anchor_independence': 0.33, 'cartographic_resolution': 0.34}
    
    # Calculate composite score
    fitness_score = (
        weights['territorial_coverage'] * territorial_coverage +
        weights['anchor_independence'] * anchor_independence +
        weights['cartographic_resolution'] * cartographic_resolution
    )
    
    # Determine fitness grade
    if fitness_score >= 0.90:
        grade = 'A'
    elif fitness_score >= 0.80:
        grade = 'B'
    elif fitness_score >= 0.70:
        grade = 'C'
    elif fitness_score >= 0.60:
        grade = 'D'
    else:
        grade = 'F'
    
    return {
        'framework_fitness_score': float(fitness_score),
        'fitness_grade': grade,
        'component_scores': {
            'territorial_coverage': float(territorial_coverage),
            'anchor_independence': float(anchor_independence),
            'cartographic_resolution': float(cartographic_resolution)
        },
        'weights_used': weights
    } 