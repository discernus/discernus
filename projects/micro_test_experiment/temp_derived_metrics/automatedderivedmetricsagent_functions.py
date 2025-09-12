import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, List

def _extract_scores(raw_response: str) -> Optional[Dict[str, Any]]:
    """
    Parses the raw analysis response string to extract dimensional scores.

    Args:
        raw_response: The string from the 'raw_analysis_response' column.

    Returns:
        A dictionary containing the dimensional scores, or None if parsing fails.
    """
    if not isinstance(raw_response, str):
        return None

    start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
    end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'

    start_idx = raw_response.find(start_marker)
    if start_idx == -1:
        return None

    # Adjust start index to be after the marker
    start_idx += len(start_marker)

    # Find the end marker starting from after the start marker
    end_idx = raw_response.find(end_marker, start_idx)
    if end_idx == -1:
        # If end marker is not found after the start marker, try from the beginning
        # This handles cases where the end marker might be part of the content before the start marker
        end_idx = raw_response.find(end_marker)
        if end_idx == -1 or end_idx < start_idx:
             return None


    json_content = raw_response[start_idx:end_idx].strip()

    try:
        analysis = json.loads(json_content)
        # Assuming one document analysis per response as per the problem structure
        if analysis and 'document_analyses' in analysis and len(analysis['document_analyses']) > 0:
            scores = analysis['document_analyses'][0].get('dimensional_scores')
            # Validate that the required scores are present
            if scores and 'positive_sentiment' in scores and 'negative_sentiment' in scores:
                if 'raw_score' in scores['positive_sentiment'] and 'raw_score' in scores['negative_sentiment']:
                    return scores
        return None
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return None

def _get_all_derived_scores(data: pd.DataFrame) -> List[Optional[Dict[str, float]]]:
    """Helper to calculate all derived scores for each row in the DataFrame."""
    all_scores = []
    if 'raw_analysis_response' not in data.columns:
        return [None] * len(data)

    for raw_response in data['raw_analysis_response']:
        scores = _extract_scores(raw_response)
        if scores:
            try:
                pos_score = float(scores['positive_sentiment']['raw_score'])
                neg_score = float(scores['negative_sentiment']['raw_score'])

                net_sentiment = pos_score - neg_score
                sentiment_magnitude = (pos_score + neg_score) / 2

                all_scores.append({
                    "net_sentiment": net_sentiment,
                    "sentiment_magnitude": sentiment_magnitude
                })
            except (TypeError, ValueError):
                all_scores.append(None)
        else:
            all_scores.append(None)
    return all_scores

def calculate_net_sentiment(data: pd.DataFrame, **kwargs) -> Optional[float]:
    """
    Calculates the average Net Sentiment for the entire dataset.
    This function returns a single scalar value representing the mean across all valid rows.

    Formula: mean(positive_sentiment.raw_score - negative_sentiment.raw_score)

    Args:
        data: pandas DataFrame with a 'raw_analysis_response' column.
        **kwargs: Additional parameters (unused).

    Returns:
        A single float representing the average net sentiment, or None if no valid data is found.
    """
    derived_scores = _get_all_derived_scores(data)
    valid_scores = [s['net_sentiment'] for s in derived_scores if s is not None and 'net_sentiment' in s]

    if not valid_scores:
        return None

    return np.mean(valid_scores)

def calculate_sentiment_magnitude(data: pd.DataFrame, **kwargs) -> Optional[float]:
    """
    Calculates the average Sentiment Magnitude for the entire dataset.
    This function returns a single scalar value representing the mean across all valid rows.

    Formula: mean((positive_sentiment.raw_score + negative_sentiment.raw_score) / 2)

    Args:
        data: pandas DataFrame with a 'raw_analysis_response' column.
        **kwargs: Additional parameters (unused).

    Returns:
        A single float representing the average sentiment magnitude, or None if no valid data is found.
    """
    derived_scores = _get_all_derived_scores(data)
    valid_scores = [s['sentiment_magnitude'] for s in derived_scores if s is not None and 'sentiment_magnitude' in s]

    if not valid_scores:
        return None

    return np.mean(valid_scores)

def calculate_all_derived_metrics(data: pd.DataFrame, **kwargs) -> Dict[str, Optional[float]]:
    """
    Calculates all derived metrics for the framework, returning a dictionary of aggregate scores.
    Each value in the dictionary is a single scalar representing the mean of that metric
    across the entire dataset.

    Args:
        data: pandas DataFrame with dimension scores.
        **kwargs: Additional parameters.

    Returns:
        A dictionary where keys are metric names and values are the calculated scalar results.
    """
    return {
        "net_sentiment": calculate_net_sentiment(data, **kwargs),
        "sentiment_magnitude": calculate_sentiment_magnitude(data, **kwargs)
    }

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates all derived metrics for each row and adds them as new columns to the DataFrame.

    This wrapper function processes each document (row) individually, calculates the
    derived metrics based on its dimensional scores, and appends the results as
    new columns to the DataFrame.

    Args:
        data: pandas DataFrame with a 'raw_analysis_response' column.
        **kwargs: Additional parameters (unused).

    Returns:
        A new pandas DataFrame with the original data plus new columns for each derived metric.
        Rows where metrics could not be calculated will have np.nan.
    """
    df = data.copy()

    if 'raw_analysis_response' not in df.columns:
        df['net_sentiment'] = np.nan
        df['sentiment_magnitude'] = np.nan
        return df

    all_derived_scores = _get_all_derived_scores(df)

    # Create a DataFrame from the list of score dictionaries
    # This is more efficient than applying a function row-by-row
    derived_df = pd.DataFrame(all_derived_scores, index=df.index)

    # Join the new derived metrics columns to the original copied DataFrame
    result_df = df.join(derived_df)

    return result_df