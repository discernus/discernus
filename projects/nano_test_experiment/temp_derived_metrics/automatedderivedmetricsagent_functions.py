import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, List

def _extract_dimensional_scores(row: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Extracts the dimensional_scores dictionary from a DataFrame row containing nested JSON.

    Args:
        row: A pandas Series representing a row of the DataFrame.

    Returns:
        A dictionary containing the dimensional scores, or None if extraction fails.
    """
    try:
        raw_response = row.analysis_result['result_content']['raw_analysis_response']
        
        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        if start_idx == -1:
            return None
            
        # No end marker check needed if we slice from the start
        json_content = raw_response[start_idx + len(start_marker):]
        end_idx = json_content.find(end_marker)
        if end_idx != -1:
            json_content = json_content[:end_idx]

        analysis = json.loads(json_content.strip())
        
        if 'document_analyses' in analysis and len(analysis['document_analyses']) > 0:
            return analysis['document_analyses'][0].get('dimensional_scores')
        return None

    except (KeyError, TypeError, AttributeError, json.JSONDecodeError, IndexError):
        return None

def calculate_net_sentiment(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the net sentiment score.
    Formula: positive_sentiment - negative_sentiment

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated net sentiment score, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        positive_score = dimensional_scores.get('positive_sentiment', {}).get('raw_score')
        negative_score = dimensional_scores.get('negative_sentiment', {}).get('raw_score')

        if positive_score is not None and negative_score is not None:
            return float(positive_score) - float(negative_score)
    except (ValueError, TypeError):
        return None
    return None

def calculate_sentiment_intensity(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Optional[float]:
    """
    Calculates the total sentiment intensity.
    Formula: positive_sentiment + negative_sentiment

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters (unused).

    Returns:
        The calculated sentiment intensity, or None if data is insufficient.
    """
    if not dimensional_scores:
        return None
    try:
        positive_score = dimensional_scores.get('positive_sentiment', {}).get('raw_score')
        negative_score = dimensional_scores.get('negative_sentiment', {}).get('raw_score')

        if positive_score is not None and negative_score is not None:
            return float(positive_score) + float(negative_score)
    except (ValueError, TypeError):
        return None
    return None

def calculate_all_derived_metrics(dimensional_scores: Optional[Dict[str, Any]], **kwargs) -> Dict[str, Optional[float]]:
    """
    Calculates all derived metrics for a single document's scores.

    Args:
        dimensional_scores: A dictionary of dimensional scores for a single document.
        **kwargs: Additional parameters passed to individual calculation functions.

    Returns:
        A dictionary containing all calculated derived metric scores.
    """
    results = {
        "net_sentiment": calculate_net_sentiment(dimensional_scores, **kwargs),
        "sentiment_intensity": calculate_sentiment_intensity(dimensional_scores, **kwargs)
    }
    return results

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Wrapper function to calculate all derived metrics and add them as new columns to the DataFrame.

    Args:
        data: The input pandas DataFrame with analysis results.
        **kwargs: Additional parameters passed to calculation functions.

    Returns:
        A new DataFrame with the original data and the new derived metric columns.
    """
    df = data.copy()

    derived_metrics_results = []
    for _, row in df.iterrows():
        dimensional_scores = _extract_dimensional_scores(row)
        all_metrics = calculate_all_derived_metrics(dimensional_scores, **kwargs)
        derived_metrics_results.append(all_metrics)
    
    if not derived_metrics_results:
        # Add empty columns if no rows were processed
        df['net_sentiment'] = pd.Series(dtype=float)
        df['sentiment_intensity'] = pd.Series(dtype=float)
        return df

    derived_df = pd.DataFrame(derived_metrics_results, index=df.index)
    
    # Fill NaN with 0.0 or another appropriate default if needed, here we keep NaN
    # derived_df = derived_df.fillna(0.0)

    final_df = df.join(derived_df)

    return final_df
