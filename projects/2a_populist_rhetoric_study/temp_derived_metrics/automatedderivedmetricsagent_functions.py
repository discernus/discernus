import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, List

def _extract_dimensional_scores(row: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Parses the JSON content from the 'raw_analysis_response' column in a DataFrame row.

    Args:
        row: A pandas Series representing a single row of the DataFrame.

    Returns:
        A dictionary containing the dimensional scores if parsing is successful, otherwise None.
    """
    raw_response = row.get('raw_analysis_response')
    if not isinstance(raw_response, str):
        return None

    start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
    end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
    
    start_idx = raw_response.find(start_marker)
    if start_idx == -1:
        return None
        
    # Adjust start_idx to be after the marker
    start_idx += len(start_marker)

    end_idx = raw_response.find(end_marker, start_idx)
    if end_idx == -1:
        # Fallback for cases where end marker might be missing but JSON is valid
        end_idx = len(raw_response)

    json_content = raw_response[start_idx:end_idx].strip()

    if not json_content:
        return None

    try:
        analysis_data = json.loads(json_content)
        # According to the sample data, scores are in the first element of 'document_analyses'
        if 'document_analyses' in analysis_data and len(analysis_data['document_analyses']) > 0:
            return analysis_data['document_analyses'][0].get('dimensional_scores')
        return None
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return None

def calculate_democratic_authoritarian_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic tension between claims of direct popular will and the rejection of legitimate opposition.
    Formula: min(popular_sovereignty_claims.raw_score, anti_pluralist_exclusion.raw_score) * abs(popular_sovereignty_claims.salience - anti_pluralist_exclusion.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None

    try:
        pop_sov_score = scores['popular_sovereignty_claims']['raw_score']
        pop_sov_salience = scores['popular_sovereignty_claims']['salience']
        anti_plur_score = scores['anti_pluralist_exclusion']['raw_score']
        anti_plur_salience = scores['anti_pluralist_exclusion']['salience']

        # Ensure all required values are numbers
        if not all(isinstance(v, (int, float)) for v in [pop_sov_score, pop_sov_salience, anti_plur_score, anti_plur_salience]):
            return None

        tension = min(pop_sov_score, anti_plur_score) * abs(pop_sov_salience - anti_plur_salience)
        return float(tension)
    except (KeyError, TypeError):
        return None

def calculate_internal_external_focus_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic tension between constructing internal people unity and emphasizing external cultural threats.
    Formula: min(homogeneous_people_construction.raw_score, nationalist_exclusion.raw_score) * abs(homogeneous_people_construction.salience - nationalist_exclusion.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None

    try:
        homo_ppl_score = scores['homogeneous_people_construction']['raw_score']
        homo_ppl_salience = scores['homogeneous_people_construction']['salience']
        nat_excl_score = scores['nationalist_exclusion']['raw_score']
        nat_excl_salience = scores['nationalist_exclusion']['salience']

        if not all(isinstance(v, (int, float)) for v in [homo_ppl_score, homo_ppl_salience, nat_excl_score, nat_excl_salience]):
            return None

        tension = min(homo_ppl_score, nat_excl_score) * abs(homo_ppl_salience - nat_excl_salience)
        return float(tension)
    except (KeyError, TypeError):
        return None

def calculate_crisis_elite_attribution_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic tension between temporal crisis narratives and elite conspiracy claims.
    Formula: min(crisis_restoration_narrative.raw_score, elite_conspiracy_systemic_corruption.raw_score) * abs(crisis_restoration_narrative.salience - elite_conspiracy_systemic_corruption.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None

    try:
        # Note: Using 'crisis_restoration_narrative' from the YAML spec, not the truncated sample data key.
        crisis_score = scores['crisis_restoration_narrative']['raw_score']
        crisis_salience = scores['crisis_restoration_narrative']['salience']
        elite_consp_score = scores['elite_conspiracy_systemic_corruption']['raw_score']
        elite_consp_salience = scores['elite_conspiracy_systemic_corruption']['salience']

        if not all(isinstance(v, (int, float)) for v in [crisis_score, crisis_salience, elite_consp_score, elite_consp_salience]):
            return None

        tension = min(crisis_score, elite_consp_score) * abs(crisis_salience - elite_consp_salience)
        return float(tension)
    except (KeyError, TypeError):
        return None

def calculate_populist_strategic_contradiction_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Overall measure of populist strategic coherence vs. contradiction, calculated as the average of the three core tension scores.
    Formula: (tension1 + tension2 + tension3) / 3

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None

    try:
        # Tension 1: Democratic-Authoritarian
        pop_sov_score = scores['popular_sovereignty_claims']['raw_score']
        pop_sov_salience = scores['popular_sovereignty_claims']['salience']
        anti_plur_score = scores['anti_pluralist_exclusion']['raw_score']
        anti_plur_salience = scores['anti_pluralist_exclusion']['salience']
        tension1 = min(pop_sov_score, anti_plur_score) * abs(pop_sov_salience - anti_plur_salience)

        # Tension 2: Internal-External Focus
        homo_ppl_score = scores['homogeneous_people_construction']['raw_score']
        homo_ppl_salience = scores['homogeneous_people_construction']['salience']
        nat_excl_score = scores['nationalist_exclusion']['raw_score']
        nat_excl_salience = scores['nationalist_exclusion']['salience']
        tension2 = min(homo_ppl_score, nat_excl_score) * abs(homo_ppl_salience - nat_excl_salience)

        # Tension 3: Crisis-Elite Attribution
        crisis_score = scores['crisis_restoration_narrative']['raw_score']
        crisis_salience = scores['crisis_restoration_narrative']['salience']
        elite_consp_score = scores['elite_conspiracy_systemic_corruption']['raw_score']
        elite_consp_salience = scores['elite_conspiracy_systemic_corruption']['salience']
        tension3 = min(crisis_score, elite_consp_score) * abs(crisis_salience - elite_consp_salience)

        # Check that all components were valid numbers
        all_values = [
            pop_sov_score, pop_sov_salience, anti_plur_score, anti_plur_salience,
            homo_ppl_score, homo_ppl_salience, nat_excl_score, nat_excl_salience,
            crisis_score, crisis_salience, elite_consp_score, elite_consp_salience
        ]
        if not all(isinstance(v, (int, float)) for v in all_values):
            return None

        psci = (tension1 + tension2 + tension3) / 3.0
        return float(psci)
    except (KeyError, TypeError):
        return None

def _calculate_salience_weighted_index(scores: Dict[str, Any], dimension_names: List[str]) -> Optional[float]:
    """Helper to calculate salience-weighted indices."""
    numerator = 0.0
    denominator = 0.0
    
    try:
        for dim_name in dimension_names:
            score = scores[dim_name]['raw_score']
            salience = scores[dim_name]['salience']
            
            if not isinstance(score, (int, float)) or not isinstance(salience, (int, float)):
                return None # Invalid data type for score or salience

            numerator += score * salience
            denominator += salience
            
        # The + 0.001 term prevents division-by-zero errors
        return float(numerator / (denominator + 0.001))
    except (KeyError, TypeError):
        return None # A required dimension was missing or malformed

def calculate_salience_weighted_core_populism_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Salience-weighted measure of core populist appeals.
    Formula: (SUM for core dims of raw_score * salience) / (SUM for core dims of salience + 0.001)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None
    
    core_dims = [
        'manichaean_people_elite_framing',
        'crisis_restoration_narrative',
        'popular_sovereignty_claims',
        'anti_pluralist_exclusion'
    ]
    return _calculate_salience_weighted_index(scores, core_dims)

def calculate_salience_weighted_populism_mechanisms_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Salience-weighted measure of populist mobilization mechanisms.
    Formula: (SUM for mechanism dims of raw_score * salience) / (SUM for mechanism dims of salience + 0.001)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None
        
    mechanism_dims = [
        'elite_conspiracy_systemic_corruption',
        'authenticity_vs_political_class',
        'homogeneous_people_construction'
    ]
    return _calculate_salience_weighted_index(scores, mechanism_dims)

def calculate_salience_weighted_boundary_distinctions_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Salience-weighted measure of populist boundary-drawing mechanisms.
    Formula: (SUM for boundary dims of raw_score * salience) / (SUM for boundary dims of salience + 0.001)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None
        
    boundary_dims = [
        'nationalist_exclusion',
        'economic_populist_appeals'
    ]
    return _calculate_salience_weighted_index(scores, boundary_dims)

def calculate_salience_weighted_overall_populism_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Comprehensive salience-weighted populist measure across all nine dimensions.
    Formula: (SUM for all dims of raw_score * salience) / (SUM for all dims of salience + 0.001)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        float: Calculated result or None if insufficient data.
    """
    scores = _extract_dimensional_scores(row)
    if scores is None:
        return None
        
    all_dims = [
        'manichaean_people_elite_framing',
        'crisis_restoration_narrative',
        'popular_sovereignty_claims',
        'anti_pluralist_exclusion',
        'elite_conspiracy_systemic_corruption',
        'authenticity_vs_political_class',
        'homogeneous_people_construction',
        'nationalist_exclusion',
        'economic_populist_appeals'
    ]
    return _calculate_salience_weighted_index(scores, all_dims)

def calculate_all_derived_metrics(row: pd.Series, **kwargs) -> Dict[str, Optional[float]]:
    """
    Calculates all derived metrics for a given row by calling each individual calculation function.

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters to pass to calculation functions.

    Returns:
        A dictionary where keys are the metric names and values are the calculated results.
    """
    return {
        "democratic_authoritarian_tension": calculate_democratic_authoritarian_tension(row, **kwargs),
        "internal_external_focus_tension": calculate_internal_external_focus_tension(row, **kwargs),
        "crisis_elite_attribution_tension": calculate_crisis_elite_attribution_tension(row, **kwargs),
        "populist_strategic_contradiction_index": calculate_populist_strategic_contradiction_index(row, **kwargs),
        "salience_weighted_core_populism_index": calculate_salience_weighted_core_populism_index(row, **kwargs),
        "salience_weighted_populism_mechanisms_index": calculate_salience_weighted_populism_mechanisms_index(row, **kwargs),
        "salience_weighted_boundary_distinctions_index": calculate_salience_weighted_boundary_distinctions_index(row, **kwargs),
        "salience_weighted_overall_populism_index": calculate_salience_weighted_overall_populism_index(row, **kwargs),
    }

def calculate_derived_metrics(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Applies all derived metric calculations to a DataFrame and adds them as new columns.

    Args:
        df: The input pandas DataFrame with a 'raw_analysis_response' column.
        **kwargs: Additional parameters to pass to calculation functions.

    Returns:
        A new pandas DataFrame with the original data and the new derived metric columns.
    """
    if 'raw_analysis_response' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'raw_analysis_response' column.")

    df_copy = df.copy()

    # Apply the function that calculates all metrics at once for each row
    derived_metrics_series = df_copy.apply(
        lambda row: calculate_all_derived_metrics(row, **kwargs),
        axis=1
    )

    # Convert the Series of dictionaries into a DataFrame
    derived_metrics_df = pd.DataFrame(derived_metrics_series.tolist(), index=df_copy.index)

    # Join the new metrics DataFrame with the original copy
    result_df = df_copy.join(derived_metrics_df)

    return result_df