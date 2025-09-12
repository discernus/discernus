import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any

def _get_dimensional_scores(row: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Parses the raw analysis response from a DataFrame row to extract dimensional scores.

    This helper function is designed to handle the specific nested JSON structure
    and proprietary delimiters found in the 'raw_analysis_response' column.

    Args:
        row: A pandas Series representing a single row of the DataFrame.

    Returns:
        A dictionary containing the dimensional scores, or None if parsing fails
        or the required keys are not found.
    """
    if 'raw_analysis_response' not in row or not isinstance(row['raw_analysis_response'], str):
        return None

    raw_response = row['raw_analysis_response']
    start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
    end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'

    start_idx = raw_response.find(start_marker)
    if start_idx == -1:
        return None

    # Extract content between markers
    json_content_str = raw_response[start_idx + len(start_marker):]
    end_idx = json_content_str.rfind(end_marker)
    if end_idx != -1:
        json_content_str = json_content_str[:end_idx]

    json_content_str = json_content_str.strip()

    try:
        analysis_data = json.loads(json_content_str)
        # Navigate through the nested structure to find dimensional_scores
        if (
            'document_analyses' in analysis_data and
            isinstance(analysis_data['document_analyses'], list) and
            len(analysis_data['document_analyses']) > 0 and
            'dimensional_scores' in analysis_data['document_analyses'][0]
        ):
            return analysis_data['document_analyses'][0]['dimensional_scores']
        else:
            return None
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return None

def calculate_message_completeness_index(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the Message Completeness Index.

    This metric measures how comprehensively the text covers all four framing functions,
    representing the average coverage across the complete framing spectrum.

    Formula:
    (dimensions.problem_definition.raw_score + dimensions.causal_attribution.raw_score +
     dimensions.moral_evaluation.raw_score + dimensions.treatment_recommendation.raw_score) / 4

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated index as a float, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        scores = [
            dimensional_scores['problem_definition']['raw_score'],
            dimensional_scores['causal_attribution']['raw_score'],
            dimensional_scores['moral_evaluation']['raw_score'],
            dimensional_scores['treatment_recommendation']['raw_score']
        ]
        if any(not isinstance(s, (int, float)) for s in scores):
            return None
        return sum(scores) / 4.0
    except (KeyError, TypeError):
        return None

def calculate_framing_coherence_index(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the Framing Coherence Index.

    This metric measures the internal consistency and balanced deployment of framing
    functions using the geometric mean of their scores.

    Formula:
    (dimensions.problem_definition.raw_score * dimensions.causal_attribution.raw_score *
     dimensions.moral_evaluation.raw_score * dimensions.treatment_recommendation.raw_score) ** 0.25

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated index as a float, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        scores = [
            dimensional_scores['problem_definition']['raw_score'],
            dimensional_scores['causal_attribution']['raw_score'],
            dimensional_scores['moral_evaluation']['raw_score'],
            dimensional_scores['treatment_recommendation']['raw_score']
        ]
        if any(not isinstance(s, (int, float)) for s in scores):
            return None
        
        product = 1.0
        for score in scores:
            product *= score
        
        return product ** 0.25
    except (KeyError, TypeError):
        return None

def calculate_salience_weighted_message_completeness(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the Salience-Weighted Message Completeness.

    This metric measures message completeness weighted by the strategic prominence
    (salience) of each framing function.

    Formula:
    (dimensions.problem_definition.raw_score * dimensions.problem_definition.salience + ... ) /
    (dimensions.problem_definition.salience + ... + 0.001)

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated index as a float, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        dimensions = ['problem_definition', 'causal_attribution', 'moral_evaluation', 'treatment_recommendation']
        
        weighted_score_sum = 0.0
        salience_sum = 0.0
        
        for dim in dimensions:
            score = dimensional_scores[dim]['raw_score']
            salience = dimensional_scores[dim]['salience']
            if not isinstance(score, (int, float)) or not isinstance(salience, (int, float)):
                return None
            weighted_score_sum += score * salience
            salience_sum += salience
            
        denominator = salience_sum + 0.001
        
        return weighted_score_sum / denominator
    except (KeyError, TypeError):
        return None

def calculate_strategic_framing_profile(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[int]:
    """
    Calculates the Strategic Framing Profile.

    This metric classifies the primary communication approach by identifying which
    framing function receives the most strategic emphasis (highest salience).

    Formula:
    np.argmax([dimensions.problem_definition.salience, dimensions.causal_attribution.salience,
               dimensions.moral_evaluation.salience, dimensions.treatment_recommendation.salience])

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        An integer representing the profile (0=Problem, 1=Cause, 2=Values, 3=Solution),
        or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        saliences = [
            dimensional_scores['problem_definition']['salience'],
            dimensional_scores['causal_attribution']['salience'],
            dimensional_scores['moral_evaluation']['salience'],
            dimensional_scores['treatment_recommendation']['salience']
        ]
        if any(not isinstance(s, (int, float)) for s in saliences):
            return None
            
        return int(np.argmax(saliences))
    except (KeyError, TypeError):
        return None

def calculate_framing_independence_score(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the Framing Independence Score.

    This metric measures the empirical independence of framing functions by calculating
    the standard deviation of their intensity scores.

    Formula:
    np.std([dimensions.problem_definition.raw_score, dimensions.causal_attribution.raw_score,
            dimensions.moral_evaluation.raw_score, dimensions.treatment_recommendation.raw_score])

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated score as a float, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        scores = [
            dimensional_scores['problem_definition']['raw_score'],
            dimensional_scores['causal_attribution']['raw_score'],
            dimensional_scores['moral_evaluation']['raw_score'],
            dimensional_scores['treatment_recommendation']['raw_score']
        ]
        if any(not isinstance(s, (int, float)) for s in scores):
            return None
            
        return float(np.std(scores))
    except (KeyError, TypeError):
        return None

def calculate_all_derived_metrics(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Dict[str, Optional[Any]]:
    """
    Calculates all derived metrics for a single document's analysis.

    This function acts as a dispatcher, calling each individual metric calculation
    function and collecting the results into a dictionary. It does not use reflection
    and calls each function directly by name.

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters to be passed to calculation functions.

    Returns:
        A dictionary where keys are the metric names and values are the
        calculated results.
    """
    if not dimensional_scores:
        return {
            "message_completeness_index": None,
            "framing_coherence_index": None,
            "salience_weighted_message_completeness": None,
            "strategic_framing_profile": None,
            "framing_independence_score": None,
        }

    results = {
        "message_completeness_index": calculate_message_completeness_index(dimensional_scores, **kwargs),
        "framing_coherence_index": calculate_framing_coherence_index(dimensional_scores, **kwargs),
        "salience_weighted_message_completeness": calculate_salience_weighted_message_completeness(dimensional_scores, **kwargs),
        "strategic_framing_profile": calculate_strategic_framing_profile(dimensional_scores, **kwargs),
        "framing_independence_score": calculate_framing_independence_score(dimensional_scores, **kwargs),
    }
    return results

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates all derived metrics for the Entman Framing Functions framework
    and adds them as new columns to the DataFrame.

    This wrapper function processes each row of the input DataFrame, parses the
    raw analysis JSON, calculates the five derived metrics, and appends them
    as new columns. It makes a copy of the input DataFrame and does not
    modify it in place.

    Args:
        data: A pandas DataFrame containing a 'raw_analysis_response' column
              with the JSON analysis output.
        **kwargs: Additional parameters to be passed to calculation functions.

    Returns:
        A new pandas DataFrame with the original data plus new columns for each
        derived metric.

    Raises:
        ValueError: If the input DataFrame does not contain the required
                    'raw_analysis_response' column.
    """
    if 'raw_analysis_response' not in data.columns:
        raise ValueError("Input DataFrame must contain a 'raw_analysis_response' column.")

    df = data.copy()

    def _process_row(row: pd.Series) -> pd.Series:
        """Helper to process one row and return a Series of metrics."""
        dimensional_scores = _get_dimensional_scores(row)
        all_metrics = calculate_all_derived_metrics(dimensional_scores, **kwargs)
        return pd.Series(all_metrics)

    derived_metrics_df = df.apply(_process_row, axis=1)

    result_df = pd.concat([df, derived_metrics_df], axis=1)

    return result_df