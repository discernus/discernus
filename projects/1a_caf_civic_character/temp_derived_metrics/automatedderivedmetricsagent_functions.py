```python
import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, List

# --- Helper Functions ---

def _get_dimensional_scores(row: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Parses the nested JSON in 'raw_analysis_response' to extract dimensional scores.

    Args:
        row: A pandas Series representing a single row of the DataFrame.

    Returns:
        A dictionary containing the dimensional scores, or None if parsing fails.
    """
    try:
        # Navigate through the nested dictionary structure
        result_content = row.get('analysis_result', {}).get('result_content', {})
        if not result_content:
            return None

        raw_response = result_content.get('raw_analysis_response')
        if not isinstance(raw_response, str):
            return None

        # Extract the JSON string using the specified delimiters
        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        if start_idx == -1:
            return None
        
        # Find the end of the JSON content
        # The end marker is optional, so we look for the last closing brace of the main object
        # as a fallback, but prioritize the explicit end marker.
        end_idx = raw_response.find(end_marker, start_idx)
        
        if end_idx != -1:
            json_content_str = raw_response[start_idx + len(start_marker):end_idx].strip()
        else:
            # Fallback if end marker is not present
            json_content_str = raw_response[start_idx + len(start_marker):].strip()

        analysis_data = json.loads(json_content_str)

        document_analyses = analysis_data.get('document_analyses')
        if not document_analyses or not isinstance(document_analyses, list):
            return None

        # Assume we always process the first document analysis in the list
        scores = document_analyses[0].get('dimensional_scores')
        return scores

    except (json.JSONDecodeError, KeyError, IndexError, TypeError, AttributeError):
        return None

def _get_score_component(scores: Optional[Dict], dimension: str, component: str) -> Optional[float]:
    """Safely retrieves a score component (e.g., 'raw_score', 'salience') for a dimension."""
    if not scores:
        return None
    value = scores.get(dimension, {}).get(component)
    return float(value) if value is not None else None

# --- Character Tension Indices ---

def calculate_identity_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic contradiction between Dignity and Tribalism appeals.
    Formula: min(dignity.raw_score, tribalism.raw_score) * abs(dignity.salience - tribalism.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    dignity_score = _get_score_component(scores, 'dignity', 'raw_score')
    tribalism_score = _get_score_component(scores, 'tribalism', 'raw_score')
    dignity_salience = _get_score_component(scores, 'dignity', 'salience')
    tribalism_salience = _get_score_component(scores, 'tribalism', 'salience')

    if any(v is None for v in [dignity_score, tribalism_score, dignity_salience, tribalism_salience]):
        return None
    
    return min(dignity_score, tribalism_score) * abs(dignity_salience - tribalism_salience)

def calculate_truth_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic contradiction between Truth and Manipulation appeals.
    Formula: min(truth.raw_score, manipulation.raw_score) * abs(truth.salience - manipulation.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    truth_score = _get_score_component(scores, 'truth', 'raw_score')
    manipulation_score = _get_score_component(scores, 'manipulation', 'raw_score')
    truth_salience = _get_score_component(scores, 'truth', 'salience')
    manipulation_salience = _get_score_component(scores, 'manipulation', 'salience')

    if any(v is None for v in [truth_score, manipulation_score, truth_salience, manipulation_salience]):
        return None
        
    return min(truth_score, manipulation_score) * abs(truth_salience - manipulation_salience)

def calculate_justice_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic contradiction between Justice and Resentment appeals.
    Formula: min(justice.raw_score, resentment.raw_score) * abs(justice.salience - resentment.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    justice_score = _get_score_component(scores, 'justice', 'raw_score')
    resentment_score = _get_score_component(scores, 'resentment', 'raw_score')
    justice_salience = _get_score_component(scores, 'justice', 'salience')
    resentment_salience = _get_score_component(scores, 'resentment', 'salience')

    if any(v is None for v in [justice_score, resentment_score, justice_salience, resentment_salience]):
        return None
        
    return min(justice_score, resentment_score) * abs(justice_salience - resentment_salience)

def calculate_emotional_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic contradiction between Hope and Fear appeals.
    Formula: min(hope.raw_score, fear.raw_score) * abs(hope.salience - fear.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    hope_score = _get_score_component(scores, 'hope', 'raw_score')
    fear_score = _get_score_component(scores, 'fear', 'raw_score')
    hope_salience = _get_score_component(scores, 'hope', 'salience')
    fear_salience = _get_score_component(scores, 'fear', 'salience')

    if any(v is None for v in [hope_score, fear_score, hope_salience, fear_salience]):
        return None
        
    return min(hope_score, fear_score) * abs(hope_salience - fear_salience)

def calculate_reality_tension(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures the strategic contradiction between Pragmatism and Fantasy appeals.
    Formula: min(pragmatism.raw_score, fantasy.raw_score) * abs(pragmatism.salience - fantasy.salience)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    pragmatism_score = _get_score_component(scores, 'pragmatism', 'raw_score')
    fantasy_score = _get_score_component(scores, 'fantasy', 'raw_score')
    pragmatism_salience = _get_score_component(scores, 'pragmatism', 'salience')
    fantasy_salience = _get_score_component(scores, 'fantasy', 'salience')

    if any(v is None for v in [pragmatism_score, fantasy_score, pragmatism_salience, fantasy_salience]):
        return None
        
    return min(pragmatism_score, fantasy_score) * abs(pragmatism_salience - fantasy_salience)

# --- Intermediate Calculations for Civic Character Index ---

VIRTUES: List[str] = ["dignity", "truth", "justice", "hope", "pragmatism"]
VICES: List[str] = ["tribalism", "manipulation", "resentment", "fear", "fantasy"]

def calculate_virtue_salience_total(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Sum of all virtue dimension salience weights for normalization.
    Formula: sum(virtue.salience for virtue in VIRTUES)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    total_salience = 0.0
    for virtue in VIRTUES:
        salience = _get_score_component(scores, virtue, 'salience')
        if salience is None:
            return None
        total_salience += salience
    return total_salience

def calculate_vice_salience_total(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Sum of all vice dimension salience weights for normalization.
    Formula: sum(vice.salience for vice in VICES)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    total_salience = 0.0
    for vice in VICES:
        salience = _get_score_component(scores, vice, 'salience')
        if salience is None:
            return None
        total_salience += salience
    return total_salience

def calculate_combined_salience_total(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Total salience across all dimensions for normalization.
    Formula: virtue_salience_total + vice_salience_total

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    virtue_total = calculate_virtue_salience_total(row)
    vice_total = calculate_vice_salience_total(row)
    
    if virtue_total is None or vice_total is None:
        return None
        
    return virtue_total + vice_total

def calculate_weighted_virtue_score(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Sum of all virtue scores multiplied by their respective salience weights.
    Formula: sum(virtue.raw_score * virtue.salience for virtue in VIRTUES)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    weighted_score = 0.0
    for virtue in VIRTUES:
        raw_score = _get_score_component(scores, virtue, 'raw_score')
        salience = _get_score_component(scores, virtue, 'salience')
        if raw_score is None or salience is None:
            return None
        weighted_score += raw_score * salience
    return weighted_score

def calculate_weighted_vice_score(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Sum of all vice scores multiplied by their respective salience weights.
    Formula: sum(vice.raw_score * vice.salience for vice in VICES)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    scores = _get_dimensional_scores(row)
    weighted_score = 0.0
    for vice in VICES:
        raw_score = _get_score_component(scores, vice, 'raw_score')
        salience = _get_score_component(scores, vice, 'salience')
        if raw_score is None or salience is None:
            return None
        weighted_score += raw_score * salience
    return weighted_score

# --- Final Salience-Weighted Civic Character Index ---

def calculate_civic_character_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Primary summary metric measuring overall character orientation.
    Formula: (weighted_virtue_score - weighted_vice_score) / (combined_salience_total + 0.001)

    Args:
        row: pandas Series with dimension scores.
        **kwargs: Additional parameters (unused).

    Returns:
        Calculated result or None if insufficient data.
    """
    weighted_virtue = calculate_weighted_virtue_score(row)
    weighted_vice = calculate_weighted_vice_score(row)
    combined_salience = calculate_combined_salience_total(row)

    if any(v is None for v in [weighted_virtue, weighted_vice, combined_salience]):
        return None

    denominator = combined_salience + 0.001
    
    return (weighted_virtue - weighted_vice) / denominator

# --- Aggregator and Wrapper Functions ---

def calculate_all_derived_metrics(row: pd.Series, **kwargs) -> Dict[str, Optional[float]]:
    """
    Calculates all derived metrics for a single row of analysis data.
    This function explicitly calls each individual metric calculation function.

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters to be passed to calculation functions.

    Returns:
        A dictionary mapping metric names to their calculated values.
    """
    results = {
        "identity_tension": calculate_identity_tension(row, **kwargs),
        "truth_tension": calculate_truth_tension(row, **kwargs),
        "justice_tension": calculate_justice_tension(row, **kwargs),
        "emotional_tension": calculate_emotional_tension(row, **kwargs),
        "reality_tension": calculate_reality_tension(row, **kwargs),
        "virtue_salience_total": calculate_virtue_salience_total(row, **kwargs),
        "vice_salience_total": calculate_vice_salience_total(row, **kwargs),
        "combined_salience_total": calculate_combined_salience_total(row, **kwargs),
        "weighted_virtue_score": calculate_weighted_virtue_score(row, **kwargs),
        "weighted_vice_score": calculate_weighted_vice_score(row, **kwargs),
        "civic_character_index": calculate_civic_character_index(row, **kwargs),
    }
    return results

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Wrapper function to calculate all derived metrics and add them as new columns to the DataFrame.

    This function iterates over each row of the input DataFrame, applies all individual
    calculation functions, and appends the results as new columns.

    Args:
        data: A pandas DataFrame containing the analysis results in a structure
              matching the framework specification.
        **kwargs: Additional parameters to be passed to calculation functions.

    Returns:
        A new pandas DataFrame with the original data plus new columns for each
        calculated derived metric.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input 'data' must be a pandas DataFrame.")

    if data.empty:
        # Define columns to add even if the input is empty
        metric_names = [
            "identity_tension", "truth_tension", "justice_tension", 
            "emotional_tension", "reality_tension", "virtue_salience_total", 
            "vice_salience_total", "combined_salience_total", 
            "weighted_virtue_score", "weighted_vice_score", "civic_character_index"
        ]
        empty_df = data.copy()
        for name in metric_names:
            empty_df[name] = pd.Series(dtype=float)
        return empty_df

    df = data.copy()

    # Apply the function that calculates all metrics for each row
    derived_metrics_series = df.apply(
        lambda row: calculate_all_derived_metrics(row, **kwargs),
        axis=1
    )

    # Convert the Series of dictionaries into a DataFrame
    derived_metrics_df = derived_metrics_series.apply(pd.Series)

    # Join the new metrics DataFrame with the original one
    result_df = df.join(derived_metrics_df)

    return result_df
```