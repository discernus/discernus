import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, List, Tuple

def _get_scores_from_row(row: pd.Series) -> Optional[Dict[str, float]]:
    """
    Parses a DataFrame row to extract positive and negative sentiment scores.
    This helper function encapsulates the logic for handling the specific
    nested JSON structure within the 'raw_analysis_response' column.

    Args:
        row: A pandas Series representing a single row of the DataFrame.

    Returns:
        A dictionary with 'positive_sentiment' and 'negative_sentiment' scores,
        or None if parsing fails, data is missing, or the structure is invalid.
    """
    try:
        raw_response = row['raw_analysis_response']
        if not isinstance(raw_response, str):
            return None

        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        end_idx = raw_response.rfind(end_marker)

        if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
            return None

        json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
        analysis = json.loads(json_content)

        # As per the sample, we expect one document analysis per response.
        scores = analysis['document_analyses'][0]['dimensional_scores']
        
        pos_score = float(scores['positive_sentiment']['raw_score'])
        neg_score = float(scores['negative_sentiment']['raw_score'])

        return {
            'positive_sentiment': pos_score,
            'negative_sentiment': neg_score
        }
    except (KeyError, IndexError, json.JSONDecodeError, TypeError, ValueError):
        # Gracefully handle malformed data, missing keys, or parsing errors.
        return None

def calculate_net_sentiment(data: pd.DataFrame, **kwargs) -> Optional[float]:
    """
    Calculates the average Net Sentiment across all documents in the DataFrame.
    This function provides a single aggregate value for the entire dataset.
    Formula for a single document: dimensions.positive_sentiment.raw_score - dimensions.negative_sentiment.raw_score

    Args:
        data: pandas DataFrame with analysis data in the 'raw_analysis_response' column.
        **kwargs: Additional parameters (unused).

    Returns:
        The average net sentiment as a float, or None if no valid data is found.
    """
    net_sentiments: List[float] = []
    for index, row in data.iterrows():
        scores = _get_scores_from_row(row)
        if scores:
            net_score = scores['positive_sentiment'] - scores['negative_sentiment']
            net_sentiments.append(net_score)

    if not net_sentiments:
        return None
    
    return float(np.mean(net_sentiments))

def calculate_sentiment_magnitude(data: pd.DataFrame, **kwargs) -> Optional[float]:
    """
    Calculates the average Sentiment Magnitude across all documents in the DataFrame.
    This function provides a single aggregate value for the entire dataset.
    Formula for a single document: (dimensions.positive_sentiment.raw_score + dimensions.negative_sentiment.raw_score) / 2

    Args:
        data: pandas DataFrame with analysis data in the 'raw_analysis_response' column.
        **kwargs: Additional parameters (unused).

    Returns:
        The average sentiment magnitude as a float, or None if no valid data is found.
    """
    magnitudes: List[float] = []
    for index, row in data.iterrows():
        scores = _get_scores_from_row(row)
        if scores:
            magnitude = (scores['positive_sentiment'] + scores['negative_sentiment']) / 2
            magnitudes.append(magnitude)

    if not magnitudes:
        return None
        
    return float(np.mean(magnitudes))

def calculate_all_derived_metrics(data: pd.DataFrame, **kwargs) -> Dict[str, Optional[float]]:
    """
    Calculates all derived metrics for the sentiment_binary_v1 framework.
    This function computes aggregate metrics (e.g., mean) over the entire DataFrame
    by calling each individual calculation function.

    Args:
        data: pandas DataFrame with dimension scores.
        **kwargs: Additional parameters passed to calculation functions.

    Returns:
        A dictionary where keys are metric names and values are the calculated
        aggregate scores for the entire dataset.
    """
    return {
        "net_sentiment": calculate_net_sentiment(data, **kwargs),
        "sentiment_magnitude": calculate_sentiment_magnitude(data, **kwargs),
    }

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates derived metrics for each row and adds them as new columns
    to the DataFrame.

    This is the primary wrapper function for applying per-document calculations.
    It creates columns for 'net_sentiment' and 'sentiment_magnitude'.

    Args:
        data: pandas DataFrame with analysis data.
        **kwargs: Additional parameters (unused in this implementation).

    Returns:
        A new pandas DataFrame with the original data and additional columns
        for each derived metric. Missing values in new columns are filled with 0.0.
    """
    df = data.copy()

    def _calculate_row_metrics(row: pd.Series) -> Tuple[Optional[float], Optional[float]]:
        """Helper to calculate all metrics for a single row."""
        scores = _get_scores_from_row(row)
        if scores:
            net_sentiment = scores['positive_sentiment'] - scores['negative_sentiment']
            sentiment_magnitude = (scores['positive_sentiment'] + scores['negative_sentiment']) / 2
            return net_sentiment, sentiment_magnitude
        return None, None

    # Apply the row-wise calculation and expand the results into two temporary series
    metric_results = df.apply(_calculate_row_metrics, axis=1, result_type='expand')
    
    # Assign results to new columns in the DataFrame
    df['net_sentiment'] = metric_results[0]
    df['sentiment_magnitude'] = metric_results[1]

    # Fill any missing results with 0.0 as per requirement
    df['net_sentiment'] = df['net_sentiment'].astype(float).fillna(0.0)
    df['sentiment_magnitude'] = df['sentiment_magnitude'].astype(float).fillna(0.0)

    return df