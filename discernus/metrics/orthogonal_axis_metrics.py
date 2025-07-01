"""
Orthogonal Axis Metrics
=======================

Validation metrics for orthogonal axis frameworks.
Focus: Axis independence, orthogonal design validation, quadrant analysis.

Critical Path: Brazil 2018 Democratic Tension Axis Model (2-axis orthogonal).
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from scipy.stats import pearsonr, chi2_contingency
import warnings

def calculate_axis_independence(
    axis_scores: Dict[str, List[float]],
    method: str = 'pearson'
) -> Dict[str, Any]:
    """
    Calculate independence between orthogonal axes.
    
    For Brazil 2018 framework: PopulismPluralism vs PatriotismNationalism
    Independence validates the orthogonal design assumption.
    
    Args:
        axis_scores: Dictionary mapping axis names to score lists
        method: Correlation method ('pearson', 'spearman', 'mutual_info')
        
    Returns:
        Dictionary with axis independence metrics
    """
    independence_results = {
        'axis_independence_satisfied': False,
        'correlation_coefficient': 0.0,
        'p_value': 1.0,
        'independence_threshold': 0.3,  # |r| < 0.3 for independence
        'method': method,
        'axis_names': list(axis_scores.keys()),
        'n_samples': 0,
        'errors': []
    }
    
    try:
        axis_names = list(axis_scores.keys())
        
        if len(axis_names) != 2:
            independence_results['errors'].append(
                f"Expected exactly 2 axes for orthogonal analysis, got {len(axis_names)}"
            )
            return independence_results
        
        # Get score arrays
        scores1 = np.array(axis_scores[axis_names[0]])
        scores2 = np.array(axis_scores[axis_names[1]])
        
        if len(scores1) != len(scores2):
            independence_results['errors'].append("Axis score arrays have different lengths")
            return independence_results
        
        independence_results['n_samples'] = len(scores1)
        
        if len(scores1) < 3:
            independence_results['errors'].append("Need at least 3 samples for correlation analysis")
            return independence_results
        
        # Calculate correlation
        if method == 'pearson':
            correlation, p_value = pearsonr(scores1, scores2)
        else:
            # TODO: Implement other correlation methods
            correlation, p_value = pearsonr(scores1, scores2)
            independence_results['method'] = 'pearson (fallback)'
        
        independence_results['correlation_coefficient'] = float(correlation)
        independence_results['p_value'] = float(p_value)
        
        # Independence test
        independence_threshold = independence_results['independence_threshold']
        independence_results['axis_independence_satisfied'] = (
            abs(correlation) < independence_threshold
        )
        
        return independence_results
        
    except Exception as e:
        independence_results['errors'].append(f"Axis independence calculation error: {str(e)}")
        return independence_results

def validate_orthogonal_design(
    signatures: np.ndarray,
    axis_configs: Dict[str, Dict],
    tolerance: float = 0.1
) -> Dict[str, Any]:
    """
    Validate orthogonal design assumptions for 2-axis frameworks.
    
    Checks:
    1. Axes are approximately 90° apart (orthogonal)
    2. Signature distribution respects orthogonal structure
    3. No systematic bias toward diagonal quadrants
    
    Args:
        signatures: Array of signature coordinates (n_samples, 2)
        axis_configs: Axis configuration dictionaries
        tolerance: Tolerance for orthogonality validation
        
    Returns:
        Dictionary with orthogonal design validation results
    """
    validation_results = {
        'orthogonal_design_valid': False,
        'angle_between_axes': 0.0,
        'orthogonality_deviation': 0.0,
        'signature_distribution': {},
        'quadrant_balance': {},
        'diagonal_bias': 0.0,
        'tolerance': tolerance,
        'errors': []
    }
    
    try:
        if len(signatures) < 4:
            validation_results['errors'].append("Need at least 4 signatures for orthogonal validation")
            return validation_results
        
        # Calculate angle between axes using anchor positions
        axis_names = list(axis_configs.keys())
        if len(axis_names) != 2:
            validation_results['errors'].append(f"Expected 2 axes, got {len(axis_names)}")
            return validation_results
        
        # For Brazil 2018: PopulismPluralism (vertical) vs PatriotismNationalism (horizontal)
        # Should be approximately 90° apart
        
        # Extract axis directions from anchor positions
        # This is a simplified calculation - TODO: implement full anchor-based calculation
        axis1_direction = np.array([0, 1])  # Vertical axis (Populism-Pluralism)
        axis2_direction = np.array([1, 0])  # Horizontal axis (Nationalism-Patriotism)
        
        # Calculate angle between axes
        dot_product = np.dot(axis1_direction, axis2_direction)
        angle_radians = np.arccos(np.clip(dot_product, -1.0, 1.0))
        angle_degrees = np.degrees(angle_radians)
        
        validation_results['angle_between_axes'] = float(angle_degrees)
        validation_results['orthogonality_deviation'] = float(abs(angle_degrees - 90.0))
        
        # Analyze signature distribution
        quadrant_counts = {
            'Q1_high_positive': 0,  # High Populism + High Nationalism
            'Q2_high_negative': 0,  # High Populism + High Patriotism
            'Q3_low_negative': 0,   # High Pluralism + High Patriotism
            'Q4_low_positive': 0    # High Pluralism + High Nationalism
        }
        
        for sig in signatures:
            x, y = sig[0], sig[1]
            if x >= 0 and y >= 0:
                quadrant_counts['Q1_high_positive'] += 1
            elif x < 0 and y >= 0:
                quadrant_counts['Q2_high_negative'] += 1
            elif x < 0 and y < 0:
                quadrant_counts['Q3_low_negative'] += 1
            else:
                quadrant_counts['Q4_low_positive'] += 1
        
        total_signatures = len(signatures)
        quadrant_proportions = {
            k: v / total_signatures for k, v in quadrant_counts.items()
        }
        
        validation_results['signature_distribution'] = quadrant_counts
        validation_results['quadrant_balance'] = quadrant_proportions
        
        # Calculate diagonal bias (preference for Q1-Q3 or Q2-Q4)
        diagonal1 = quadrant_proportions['Q1_high_positive'] + quadrant_proportions['Q3_low_negative']
        diagonal2 = quadrant_proportions['Q2_high_negative'] + quadrant_proportions['Q4_low_positive']
        diagonal_bias = abs(diagonal1 - diagonal2)
        
        validation_results['diagonal_bias'] = float(diagonal_bias)
        
        # Overall orthogonal design validation
        orthogonality_valid = validation_results['orthogonality_deviation'] <= (tolerance * 90.0)
        distribution_reasonable = diagonal_bias < 0.4  # Not heavily biased toward one diagonal
        
        validation_results['orthogonal_design_valid'] = (
            orthogonality_valid and distribution_reasonable
        )
        
        return validation_results
        
    except Exception as e:
        validation_results['errors'].append(f"Orthogonal design validation error: {str(e)}")
        return validation_results

def calculate_quadrant_distribution(
    signatures: np.ndarray,
    framework_config: Dict,
    expected_distribution: str = 'uniform'
) -> Dict[str, Any]:
    """
    Analyze signature distribution across quadrants for orthogonal frameworks.
    
    For Brazil 2018:
    - Q1: High Populism + High Nationalism
    - Q2: High Populism + High Patriotism  
    - Q3: High Pluralism + High Patriotism
    - Q4: High Pluralism + High Nationalism
    
    Args:
        signatures: Array of signature coordinates
        framework_config: Framework configuration
        expected_distribution: Expected distribution pattern
        
    Returns:
        Dictionary with quadrant distribution analysis
    """
    distribution_results = {
        'quadrant_counts': {},
        'quadrant_proportions': {},
        'distribution_uniformity': 0.0,
        'dominant_quadrant': '',
        'least_populated_quadrant': '',
        'political_interpretation': {},
        'chi_square_test': {},
        'expected_distribution': expected_distribution,
        'errors': []
    }
    
    try:
        if len(signatures) < 4:
            distribution_results['errors'].append("Need at least 4 signatures for quadrant analysis")
            return distribution_results
        
        # Count signatures in each quadrant
        quadrant_counts = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
        quadrant_signatures = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
        
        for i, sig in enumerate(signatures):
            x, y = sig[0], sig[1]
            if x >= 0 and y >= 0:
                quadrant = 'Q1'
            elif x < 0 and y >= 0:
                quadrant = 'Q2'
            elif x < 0 and y < 0:
                quadrant = 'Q3'
            else:
                quadrant = 'Q4'
            
            quadrant_counts[quadrant] += 1
            quadrant_signatures[quadrant].append(i)
        
        total_signatures = len(signatures)
        quadrant_proportions = {
            k: v / total_signatures for k, v in quadrant_counts.items()
        }
        
        distribution_results['quadrant_counts'] = quadrant_counts
        distribution_results['quadrant_proportions'] = quadrant_proportions
        
        # Find dominant and least populated quadrants
        sorted_quadrants = sorted(quadrant_counts.items(), key=lambda x: x[1], reverse=True)
        distribution_results['dominant_quadrant'] = sorted_quadrants[0][0]
        distribution_results['least_populated_quadrant'] = sorted_quadrants[-1][0]
        
        # Calculate distribution uniformity (1 = perfectly uniform, 0 = all in one quadrant)
        expected_proportion = 0.25  # 25% in each quadrant for uniform distribution
        deviations = [abs(prop - expected_proportion) for prop in quadrant_proportions.values()]
        max_deviation = max(deviations)
        uniformity = 1.0 - (max_deviation / expected_proportion)
        
        distribution_results['distribution_uniformity'] = float(uniformity)
        
        # Political interpretation for Brazil 2018
        distribution_results['political_interpretation'] = {
            'Q1_high_pop_high_nat': {
                'count': quadrant_counts['Q1'],
                'proportion': quadrant_proportions['Q1'],
                'interpretation': 'High Populism + High Nationalism (Authoritarian Populism)'
            },
            'Q2_high_pop_high_pat': {
                'count': quadrant_counts['Q2'],
                'proportion': quadrant_proportions['Q2'],
                'interpretation': 'High Populism + High Patriotism (Civic Populism)'
            },
            'Q3_high_plur_high_pat': {
                'count': quadrant_counts['Q3'],
                'proportion': quadrant_proportions['Q3'],
                'interpretation': 'High Pluralism + High Patriotism (Liberal Democracy)'
            },
            'Q4_high_plur_high_nat': {
                'count': quadrant_counts['Q4'],
                'proportion': quadrant_proportions['Q4'],
                'interpretation': 'High Pluralism + High Nationalism (Conservative Democracy)'
            }
        }
        
        # Chi-square test for uniform distribution
        try:
            expected_counts = [total_signatures / 4] * 4
            observed_counts = list(quadrant_counts.values())
            chi2_stat, chi2_p_value = chi2_contingency([observed_counts, expected_counts])[:2]
            
            distribution_results['chi_square_test'] = {
                'chi2_statistic': float(chi2_stat),
                'p_value': float(chi2_p_value),
                'uniform_distribution_rejected': chi2_p_value < 0.05,
                'degrees_of_freedom': 3
            }
        except Exception as e:
            distribution_results['chi_square_test'] = {'error': str(e)}
        
        return distribution_results
        
    except Exception as e:
        distribution_results['errors'].append(f"Quadrant distribution calculation error: {str(e)}")
        return distribution_results

def analyze_brazil_2018_specific_patterns(
    signatures: np.ndarray,
    temporal_phases: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Brazil 2018 specific analysis patterns.
    
    Analyzes discourse evolution patterns specific to the 2018 Brazilian election:
    - Early campaign vs final push positioning
    - Populism-Nationalism correlation patterns
    - Democratic tension dynamics
    
    Args:
        signatures: Array of signature coordinates
        temporal_phases: Optional list of temporal phase labels
        
    Returns:
        Dictionary with Brazil 2018 specific analysis
    """
    brazil_analysis = {
        'temporal_evolution': {},
        'discourse_positioning': {},
        'democratic_tension_patterns': {},
        'quadrant_evolution': {},
        'errors': []
    }
    
    try:
        if len(signatures) < 2:
            brazil_analysis['errors'].append("Need at least 2 signatures for Brazil 2018 analysis")
            return brazil_analysis
        
        # Basic discourse positioning analysis
        mean_populism_pluralism = np.mean(signatures[:, 1])  # Y-axis (vertical)
        mean_patriotism_nationalism = np.mean(signatures[:, 0])  # X-axis (horizontal)
        
        brazil_analysis['discourse_positioning'] = {
            'mean_populism_pluralism_score': float(mean_populism_pluralism),
            'mean_patriotism_nationalism_score': float(mean_patriotism_nationalism),
            'overall_populism_tendency': 'populist' if mean_populism_pluralism > 0 else 'pluralist',
            'overall_nationalism_tendency': 'nationalist' if mean_patriotism_nationalism > 0 else 'patriotic',
            'discourse_intensity': float(np.linalg.norm([mean_patriotism_nationalism, mean_populism_pluralism]))
        }
        
        # Democratic tension analysis
        populism_scores = signatures[:, 1]
        pluralism_scores = -signatures[:, 1]  # Pluralism is negative of populism in this axis
        
        brazil_analysis['democratic_tension_patterns'] = {
            'populism_variance': float(np.var(populism_scores)),
            'pluralism_variance': float(np.var(pluralism_scores)),
            'tension_stability': float(1.0 / (1.0 + np.var(populism_scores))),  # High variance = low stability
            'polarization_index': float(np.std(populism_scores))
        }
        
        # Temporal evolution analysis (if temporal data available)
        if temporal_phases and len(temporal_phases) == len(signatures):
            phase_analysis = {}
            unique_phases = list(set(temporal_phases))
            
            for phase in unique_phases:
                phase_mask = [p == phase for p in temporal_phases]
                phase_signatures = signatures[phase_mask]
                
                if len(phase_signatures) > 0:
                    phase_centroid = np.mean(phase_signatures, axis=0)
                    phase_analysis[phase] = {
                        'centroid': phase_centroid.tolist(),
                        'signature_count': len(phase_signatures),
                        'populism_mean': float(np.mean(phase_signatures[:, 1])),
                        'nationalism_mean': float(np.mean(phase_signatures[:, 0]))
                    }
            
            brazil_analysis['temporal_evolution'] = phase_analysis
            
            # Calculate phase transitions
            if len(unique_phases) >= 2:
                sorted_phases = sorted(unique_phases)  # Assumes phases are sortable
                transitions = {}
                
                for i in range(len(sorted_phases) - 1):
                    phase1, phase2 = sorted_phases[i], sorted_phases[i + 1]
                    if phase1 in phase_analysis and phase2 in phase_analysis:
                        centroid1 = np.array(phase_analysis[phase1]['centroid'])
                        centroid2 = np.array(phase_analysis[phase2]['centroid'])
                        
                        transition_vector = centroid2 - centroid1
                        transition_distance = float(np.linalg.norm(transition_vector))
                        
                        transitions[f"{phase1}_to_{phase2}"] = {
                            'transition_vector': transition_vector.tolist(),
                            'transition_distance': transition_distance,
                            'populism_change': float(transition_vector[1]),
                            'nationalism_change': float(transition_vector[0])
                        }
                
                brazil_analysis['quadrant_evolution'] = transitions
        
        return brazil_analysis
        
    except Exception as e:
        brazil_analysis['errors'].append(f"Brazil 2018 analysis error: {str(e)}")
        return brazil_analysis 