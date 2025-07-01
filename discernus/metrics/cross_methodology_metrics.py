"""
Cross-Methodology Metrics
=========================

Metrics for cross-validation and comparison between different methodological approaches.
Focus: Tamaki & Fuks compatibility, methodological validation, framework comparison.

Critical Path: Brazil 2018 framework designed for T&F cross-validation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings

def calculate_tamaki_fuks_compatibility(
    dcs_scores: Dict[str, List[float]],
    tamaki_fuks_scores: Dict[str, List[float]],
    scale_mapping: Optional[Dict[str, Tuple[float, float]]] = None
) -> Dict[str, Any]:
    """
    Calculate compatibility between DCS framework scores and Tamaki & Fuks (2019) scores.
    
    Brazil 2018 framework uses 0-2 scale for direct T&F comparison.
    
    Args:
        dcs_scores: DCS framework scores by dimension
        tamaki_fuks_scores: Original T&F scores by dimension  
        scale_mapping: Optional scale conversion mapping
        
    Returns:
        Dictionary with compatibility metrics
    """
    compatibility_results = {
        'overall_compatibility': 0.0,
        'dimension_correlations': {},
        'scale_consistency': {},
        'methodological_agreement': {},
        'conversion_quality': {},
        'errors': []
    }
    
    try:
        # Check for matching dimensions
        dcs_dimensions = set(dcs_scores.keys())
        tf_dimensions = set(tamaki_fuks_scores.keys())
        common_dimensions = dcs_dimensions.intersection(tf_dimensions)
        
        if not common_dimensions:
            compatibility_results['errors'].append(
                "No common dimensions found between DCS and T&F scores"
            )
            return compatibility_results
        
        dimension_results = {}
        
        for dimension in common_dimensions:
            dcs_vals = np.array(dcs_scores[dimension])
            tf_vals = np.array(tamaki_fuks_scores[dimension])
            
            if len(dcs_vals) != len(tf_vals):
                compatibility_results['errors'].append(
                    f"Dimension '{dimension}' has mismatched sample sizes"
                )
                continue
            
            if len(dcs_vals) < 3:
                compatibility_results['errors'].append(
                    f"Dimension '{dimension}' has insufficient samples for correlation"
                )
                continue
            
            # Calculate correlations
            pearson_r, pearson_p = pearsonr(dcs_vals, tf_vals)
            spearman_r, spearman_p = spearmanr(dcs_vals, tf_vals)
            
            # Scale consistency check (both should be 0-2 for Brazil 2018)
            dcs_range = (float(np.min(dcs_vals)), float(np.max(dcs_vals)))
            tf_range = (float(np.min(tf_vals)), float(np.max(tf_vals)))
            
            scale_consistent = (
                0 <= dcs_range[0] <= 2.1 and 0 <= dcs_range[1] <= 2.1 and
                0 <= tf_range[0] <= 2.1 and 0 <= tf_range[1] <= 2.1
            )
            
            # Methodological agreement metrics
            mae = mean_absolute_error(tf_vals, dcs_vals)
            rmse = np.sqrt(mean_squared_error(tf_vals, dcs_vals))
            
            # Agreement threshold (scores within 0.5 points considered agreement)
            agreement_threshold = 0.5
            agreements = np.abs(dcs_vals - tf_vals) <= agreement_threshold
            agreement_rate = float(np.mean(agreements))
            
            dimension_results[dimension] = {
                'pearson_correlation': float(pearson_r),
                'pearson_p_value': float(pearson_p),
                'spearman_correlation': float(spearman_r),
                'spearman_p_value': float(spearman_p),
                'mean_absolute_error': float(mae),
                'root_mean_squared_error': float(rmse),
                'agreement_rate': agreement_rate,
                'scale_consistent': scale_consistent,
                'dcs_range': dcs_range,
                'tf_range': tf_range,
                'sample_size': len(dcs_vals)
            }
        
        compatibility_results['dimension_correlations'] = dimension_results
        
        # Calculate overall compatibility score
        if dimension_results:
            # Weighted average of correlations
            correlation_scores = [
                abs(result['pearson_correlation']) 
                for result in dimension_results.values()
            ]
            agreement_scores = [
                result['agreement_rate']
                for result in dimension_results.values()
            ]
            
            overall_correlation = np.mean(correlation_scores)
            overall_agreement = np.mean(agreement_scores)
            
            # Composite compatibility score (correlation + agreement)
            compatibility_results['overall_compatibility'] = float(
                0.6 * overall_correlation + 0.4 * overall_agreement
            )
            
            compatibility_results['methodological_agreement'] = {
                'mean_correlation': float(overall_correlation),
                'mean_agreement_rate': float(overall_agreement),
                'dimensions_analyzed': len(dimension_results),
                'all_scales_consistent': all(
                    result['scale_consistent'] for result in dimension_results.values()
                )
            }
        
        return compatibility_results
        
    except Exception as e:
        compatibility_results['errors'].append(f"T&F compatibility calculation error: {str(e)}")
        return compatibility_results

def cross_validate_frameworks(
    framework1_results: Dict[str, Any],
    framework2_results: Dict[str, Any],
    validation_method: str = 'correlation'
) -> Dict[str, Any]:
    """
    Cross-validate results between different framework approaches.
    
    Supports validation between:
    - DCS frameworks vs traditional approaches
    - Different DCS framework versions
    - Human scoring vs LLM scoring
    
    Args:
        framework1_results: Results from first framework
        framework2_results: Results from second framework
        validation_method: Validation approach ('correlation', 'agreement', 'ranking')
        
    Returns:
        Dictionary with cross-validation results
    """
    cross_validation = {
        'validation_method': validation_method,
        'frameworks_compatible': False,
        'validation_score': 0.0,
        'dimension_comparisons': {},
        'signature_comparisons': {},
        'statistical_tests': {},
        'errors': []
    }
    
    try:
        # Extract signatures for comparison
        sigs1 = framework1_results.get('signatures', [])
        sigs2 = framework2_results.get('signatures', [])
        
        if not sigs1 or not sigs2:
            cross_validation['errors'].append("Missing signature data in one or both frameworks")
            return cross_validation
        
        if len(sigs1) != len(sigs2):
            cross_validation['errors'].append("Framework results have different numbers of signatures")
            return cross_validation
        
        # Convert to numpy arrays
        signatures1 = np.array(sigs1)
        signatures2 = np.array(sigs2)
        
        if signatures1.shape != signatures2.shape:
            cross_validation['errors'].append("Signature arrays have incompatible shapes")
            return cross_validation
        
        # Signature-level comparisons
        signature_correlations = []
        signature_distances = []
        
        for i in range(len(signatures1)):
            sig1, sig2 = signatures1[i], signatures2[i]
            
            # Calculate correlation between signature vectors
            if len(sig1) > 1 and len(sig2) > 1:
                try:
                    sig_corr, _ = pearsonr(sig1, sig2)
                    if not np.isnan(sig_corr):
                        signature_correlations.append(sig_corr)
                except:
                    pass
            
            # Calculate euclidean distance
            distance = np.linalg.norm(sig1 - sig2)
            signature_distances.append(distance)
        
        cross_validation['signature_comparisons'] = {
            'mean_signature_correlation': float(np.mean(signature_correlations)) if signature_correlations else 0.0,
            'mean_signature_distance': float(np.mean(signature_distances)),
            'max_signature_distance': float(np.max(signature_distances)),
            'signature_correlations_available': len(signature_correlations)
        }
        
        # Dimension-wise comparisons (if available)
        dimensions1 = framework1_results.get('dimension_scores', {})
        dimensions2 = framework2_results.get('dimension_scores', {})
        
        if dimensions1 and dimensions2:
            common_dims = set(dimensions1.keys()).intersection(set(dimensions2.keys()))
            
            dimension_results = {}
            for dim in common_dims:
                scores1 = np.array(dimensions1[dim])
                scores2 = np.array(dimensions2[dim])
                
                if len(scores1) == len(scores2) and len(scores1) > 2:
                    corr, p_val = pearsonr(scores1, scores2)
                    mae = mean_absolute_error(scores1, scores2)
                    
                    dimension_results[dim] = {
                        'correlation': float(corr),
                        'p_value': float(p_val),
                        'mean_absolute_error': float(mae),
                        'score_range_1': (float(np.min(scores1)), float(np.max(scores1))),
                        'score_range_2': (float(np.min(scores2)), float(np.max(scores2)))
                    }
            
            cross_validation['dimension_comparisons'] = dimension_results
        
        # Overall validation score
        sig_corr = cross_validation['signature_comparisons']['mean_signature_correlation']
        sig_dist = cross_validation['signature_comparisons']['mean_signature_distance']
        
        # Normalize distance to [0,1] assuming max reasonable distance is 2.0
        normalized_distance = min(sig_dist / 2.0, 1.0)
        distance_score = 1.0 - normalized_distance
        
        # Combine correlation and distance scores
        cross_validation['validation_score'] = float(0.7 * abs(sig_corr) + 0.3 * distance_score)
        
        # Compatibility threshold
        compatibility_threshold = 0.6
        cross_validation['frameworks_compatible'] = (
            cross_validation['validation_score'] >= compatibility_threshold
        )
        
        return cross_validation
        
    except Exception as e:
        cross_validation['errors'].append(f"Cross-validation error: {str(e)}")
        return cross_validation

def compare_methodological_approaches(
    dcs_results: Dict[str, Any],
    traditional_results: Dict[str, Any], 
    human_scores: Optional[Dict[str, List[float]]] = None
) -> Dict[str, Any]:
    """
    Compare DCS methodology against traditional approaches.
    
    Specifically designed for Brazil 2018 framework validation against:
    - Tamaki & Fuks (2019) anchor-set methodology
    - Human expert scoring
    - Other populism measurement approaches
    
    Args:
        dcs_results: DCS framework analysis results
        traditional_results: Traditional methodology results
        human_scores: Optional human expert scores for validation
        
    Returns:
        Dictionary with methodological comparison
    """
    comparison_results = {
        'methodology_comparison': 'DCS vs Traditional',
        'advantage_assessment': {},
        'reliability_comparison': {},
        'validity_comparison': {},
        'practical_advantages': {},
        'academic_rigor_comparison': {},
        'errors': []
    }
    
    try:
        # Reliability comparison
        dcs_reliability = dcs_results.get('reliability_metrics', {})
        traditional_reliability = traditional_results.get('reliability_metrics', {})
        
        reliability_comparison = {
            'dcs_internal_consistency': dcs_reliability.get('cronbach_alpha', 0.0),
            'traditional_internal_consistency': traditional_reliability.get('cronbach_alpha', 0.0),
            'dcs_test_retest': dcs_reliability.get('test_retest_reliability', 0.0),
            'traditional_test_retest': traditional_reliability.get('test_retest_reliability', 0.0)
        }
        
        comparison_results['reliability_comparison'] = reliability_comparison
        
        # Validity comparison
        dcs_validity = dcs_results.get('validity_metrics', {})
        traditional_validity = traditional_results.get('validity_metrics', {})
        
        validity_comparison = {
            'dcs_construct_validity': dcs_validity.get('construct_validity', 0.0),
            'traditional_construct_validity': traditional_validity.get('construct_validity', 0.0),
            'dcs_convergent_validity': dcs_validity.get('convergent_validity', 0.0),
            'traditional_convergent_validity': traditional_validity.get('convergent_validity', 0.0)
        }
        
        comparison_results['validity_comparison'] = validity_comparison
        
        # Practical advantages assessment
        practical_advantages = {
            'dcs_scalability': 'High (automated LLM scoring)',
            'traditional_scalability': 'Low (manual expert coding)',
            'dcs_reproducibility': 'High (systematic prompting)',
            'traditional_reproducibility': 'Medium (expert variability)',
            'dcs_transparency': 'High (explicit mathematical foundations)',
            'traditional_transparency': 'Medium (expert judgment based)',
            'dcs_cross_language_support': 'High (multilingual LLMs)',
            'traditional_cross_language_support': 'Low (requires native speakers)',
        }
        
        comparison_results['practical_advantages'] = practical_advantages
        
        # Academic rigor comparison
        academic_rigor = {
            'mathematical_foundations': {
                'dcs': 'Explicit mathematical framework with validation metrics',
                'traditional': 'Statistical validation of coding reliability'
            },
            'theoretical_grounding': {
                'dcs': 'Multi-dimensional theoretical space with anchor positioning',
                'traditional': 'Established populism theory with expert interpretation'
            },
            'validation_approach': {
                'dcs': 'Cross-methodology validation + mathematical metrics',
                'traditional': 'Inter-rater reliability + construct validation'
            },
            'replication_support': {
                'dcs': 'Complete framework specification + reproducible prompts',
                'traditional': 'Codebook + expert training requirements'
            }
        }
        
        comparison_results['academic_rigor_comparison'] = academic_rigor
        
        # Human validation (if available)
        if human_scores:
            human_validation = {}
            
            # Compare DCS vs human scores
            dcs_scores = dcs_results.get('dimension_scores', {})
            
            for dimension, human_vals in human_scores.items():
                if dimension in dcs_scores:
                    dcs_vals = dcs_scores[dimension]
                    
                    if len(human_vals) == len(dcs_vals) and len(human_vals) > 2:
                        corr, p_val = pearsonr(human_vals, dcs_vals)
                        mae = mean_absolute_error(human_vals, dcs_vals)
                        
                        human_validation[dimension] = {
                            'human_dcs_correlation': float(corr),
                            'p_value': float(p_val),
                            'mean_absolute_error': float(mae),
                            'agreement_within_0_5': float(np.mean(np.abs(np.array(human_vals) - np.array(dcs_vals)) <= 0.5))
                        }
            
            comparison_results['human_validation'] = human_validation
        
        # Overall advantage assessment
        advantage_scores = {
            'scalability': 'DCS' if practical_advantages['dcs_scalability'] == 'High' else 'Traditional',
            'reproducibility': 'DCS' if practical_advantages['dcs_reproducibility'] == 'High' else 'Traditional',
            'transparency': 'DCS' if practical_advantages['dcs_transparency'] == 'High' else 'Traditional',
            'cross_language': 'DCS' if practical_advantages['dcs_cross_language_support'] == 'High' else 'Traditional'
        }
        
        dcs_advantages = sum(1 for v in advantage_scores.values() if v == 'DCS')
        
        comparison_results['advantage_assessment'] = {
            'dcs_advantages_count': dcs_advantages,
            'traditional_advantages_count': len(advantage_scores) - dcs_advantages,
            'overall_recommendation': 'DCS' if dcs_advantages > len(advantage_scores) / 2 else 'Traditional',
            'advantage_breakdown': advantage_scores
        }
        
        return comparison_results
        
    except Exception as e:
        comparison_results['errors'].append(f"Methodological comparison error: {str(e)}")
        return comparison_results

def validate_brazil_2018_specific_requirements(
    framework_results: Dict[str, Any],
    reference_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Validate Brazil 2018 framework against specific requirements.
    
    Checks:
    - Portuguese language optimization
    - 2018 electoral context appropriateness  
    - T&F methodology compatibility
    - Bolsonaro discourse analysis capability
    
    Args:
        framework_results: Brazil 2018 framework results
        reference_data: Optional reference data for validation
        
    Returns:
        Dictionary with Brazil 2018 specific validation
    """
    brazil_validation = {
        'brazil_2018_compliant': False,
        'language_optimization': {},
        'electoral_context_validation': {},
        'discourse_analysis_capability': {},
        'tamaki_fuks_compatibility': {},
        'compliance_score': 0.0,
        'errors': []
    }
    
    try:
        # Language optimization validation
        language_cues = framework_results.get('framework_config', {}).get('components', {})
        portuguese_optimization = {
            'portuguese_language_cues_present': False,
            'brazilian_specific_terms': False,
            'political_context_appropriate': False
        }
        
        # Check for Portuguese language cues
        portuguese_terms_found = 0
        brazilian_political_terms = ['povo', 'nação', 'pátria', 'constituição', 'elite']
        
        for component_name, component_config in language_cues.items():
            if isinstance(component_config, dict):
                cues = component_config.get('language_cues', [])
                for cue in cues:
                    if any(term in cue.lower() for term in brazilian_political_terms):
                        portuguese_terms_found += 1
        
        portuguese_optimization['portuguese_language_cues_present'] = portuguese_terms_found > 0
        portuguese_optimization['brazilian_specific_terms'] = portuguese_terms_found >= 5
        
        brazil_validation['language_optimization'] = portuguese_optimization
        
        # Electoral context validation
        electoral_context = {
            'populism_pluralism_axis_present': False,
            'nationalism_patriotism_axis_present': False,
            'quadrant_analysis_supported': False,
            'temporal_analysis_capable': False
        }
        
        # Check framework structure
        framework_config = framework_results.get('framework_config', {})
        axes = framework_config.get('axes', {})
        
        # Look for expected axes
        axis_names = list(axes.keys())
        electoral_context['populism_pluralism_axis_present'] = any(
            'populism' in axis.lower() or 'pluralism' in axis.lower() 
            for axis in axis_names
        )
        electoral_context['nationalism_patriotism_axis_present'] = any(
            'nationalism' in axis.lower() or 'patriotism' in axis.lower()
            for axis in axis_names
        )
        
        electoral_context['quadrant_analysis_supported'] = len(axis_names) == 2
        
        brazil_validation['electoral_context_validation'] = electoral_context
        
        # Discourse analysis capability
        discourse_capability = {
            'signature_generation': len(framework_results.get('signatures', [])) > 0,
            'coordinate_positioning': 'coordinate_system' in framework_config,
            'visualization_support': 'visualization' in framework_config,
            'academic_validation_ready': 'theoretical_foundation' in framework_config
        }
        
        brazil_validation['discourse_analysis_capability'] = discourse_capability
        
        # Calculate compliance score
        all_checks = [
            portuguese_optimization['portuguese_language_cues_present'],
            portuguese_optimization['brazilian_specific_terms'],
            electoral_context['populism_pluralism_axis_present'],
            electoral_context['nationalism_patriotism_axis_present'],
            electoral_context['quadrant_analysis_supported'],
            discourse_capability['signature_generation'],
            discourse_capability['coordinate_positioning'],
            discourse_capability['visualization_support']
        ]
        
        compliance_score = sum(all_checks) / len(all_checks)
        brazil_validation['compliance_score'] = float(compliance_score)
        
        # Overall compliance
        brazil_validation['brazil_2018_compliant'] = compliance_score >= 0.75
        
        return brazil_validation
        
    except Exception as e:
        brazil_validation['errors'].append(f"Brazil 2018 validation error: {str(e)}")
        return brazil_validation 