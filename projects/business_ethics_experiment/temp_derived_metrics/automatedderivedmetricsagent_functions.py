import pandas as pd
import numpy as np
import json
from typing import Optional, Dict, Any, Union

def _get_dimensional_scores(row: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Parses the nested JSON from the raw_analysis_response column for a given row.

    Args:
        row: A pandas Series representing a single row of the DataFrame.

    Returns:
        A dictionary containing the dimensional scores, or None if parsing fails.
    """
    try:
        # The data is deeply nested. This navigates the structure.
        # Path: analysis_result -> result_content -> raw_analysis_response
        raw_response = row.get('analysis_result', {}).get('result_content', {}).get('raw_analysis_response')
        if not isinstance(raw_response, str):
            return None

        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        start_idx = raw_response.find(start_marker)

        if start_idx == -1:
            return None

        # Handle cases where the end marker might be missing
        end_idx = raw_response.find(end_marker, start_idx)
        if end_idx != -1:
            json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
        else:
            json_content = raw_response[start_idx + len(start_marker):].strip()

        analysis_data = json.loads(json_content)

        # Path: json_data -> document_analyses (list) -> first element -> dimensional_scores
        document_analyses = analysis_data.get('document_analyses')
        if not document_analyses or not isinstance(document_analyses, list):
            return None

        # Assuming we always process the first document analysis in the list
        scores = document_analyses[0].get('dimensional_scores')
        if not isinstance(scores, dict):
            return None
            
        return scores
    except (json.JSONDecodeError, KeyError, IndexError, AttributeError, TypeError):
        return None

def calculate_stakeholder_focus_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures stakeholder capitalism emphasis vs shareholder primacy across the stakeholder relations domain.
    
    Formula: ((customer_service + employee_development) / 2) - ((customer_exploitation + employee_exploitation) / 2)

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        cs = scores['customer_service']['raw_score']
        ed = scores['employee_development']['raw_score']
        ce = scores['customer_exploitation']['raw_score']
        ee = scores['employee_exploitation']['raw_score']
        
        stakeholder_avg = (cs + ed) / 2.0
        exploitation_avg = (ce + ee) / 2.0
        
        return stakeholder_avg - exploitation_avg
    except (KeyError, TypeError):
        return None

def calculate_operational_ethics_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures governance and financial integrity across the operational integrity domain.
    
    Formula: ((accountability + financial_responsibility) / 2) - ((opacity + financial_manipulation) / 2)

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        acc = scores['accountability']['raw_score']
        fr = scores['financial_responsibility']['raw_score']
        op = scores['opacity']['raw_score']
        fm = scores['financial_manipulation']['raw_score']
        
        integrity_avg = (acc + fr) / 2.0
        opacity_avg = (op + fm) / 2.0
        
        return integrity_avg - opacity_avg
    except (KeyError, TypeError):
        return None

def calculate_strategic_ethics_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures long-term ethical orientation vs short-term extraction focus.
    
    Formula: (sustainable_purpose - short_term_extraction + 1) / 2

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        sp = scores['sustainable_purpose']['raw_score']
        ste = scores['short_term_extraction']['raw_score']
        
        return (sp - ste + 1.0) / 2.0
    except (KeyError, TypeError):
        return None

def calculate_salience_weighted_stakeholder_focus(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Calculates stakeholder focus weighted by rhetorical prominence and strategic emphasis.
    
    Formula: ((cs_score * cs_salience + ed_score * ed_salience) - (ce_score * ce_salience + ee_score * ee_salience)) / (cs_salience + ed_salience + ce_salience + ee_salience + 0.001)

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated weighted index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        cs_score = scores['customer_service']['raw_score']
        cs_salience = scores['customer_service']['salience']
        ed_score = scores['employee_development']['raw_score']
        ed_salience = scores['employee_development']['salience']
        ce_score = scores['customer_exploitation']['raw_score']
        ce_salience = scores['customer_exploitation']['salience']
        ee_score = scores['employee_exploitation']['raw_score']
        ee_salience = scores['employee_exploitation']['salience']

        numerator = (cs_score * cs_salience + ed_score * ed_salience) - (ce_score * ce_salience + ee_score * ee_salience)
        denominator = cs_salience + ed_salience + ce_salience + ee_salience + 0.001
        
        return numerator / denominator
    except (KeyError, TypeError):
        return None

def calculate_salience_weighted_operational_ethics(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Calculates operational ethics weighted by rhetorical prominence and strategic emphasis.
    
    Formula: ((acc_score * acc_salience + fr_score * fr_salience) - (op_score * op_salience + fm_score * fm_salience)) / (acc_salience + fr_salience + op_salience + fm_salience + 0.001)

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated weighted index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        acc_score = scores['accountability']['raw_score']
        acc_salience = scores['accountability']['salience']
        fr_score = scores['financial_responsibility']['raw_score']
        fr_salience = scores['financial_responsibility']['salience']
        op_score = scores['opacity']['raw_score']
        op_salience = scores['opacity']['salience']
        fm_score = scores['financial_manipulation']['raw_score']
        fm_salience = scores['financial_manipulation']['salience']

        numerator = (acc_score * acc_salience + fr_score * fr_salience) - (op_score * op_salience + fm_score * fm_salience)
        denominator = acc_salience + fr_salience + op_salience + fm_salience + 0.001
        
        return numerator / denominator
    except (KeyError, TypeError):
        return None

def calculate_salience_weighted_strategic_ethics(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Calculates strategic ethics weighted by rhetorical prominence and strategic emphasis.
    
    Formula: (sp_score * sp_salience - ste_score * ste_salience) / (sp_salience + ste_salience + 0.001)

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated weighted index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        sp_score = scores['sustainable_purpose']['raw_score']
        sp_salience = scores['sustainable_purpose']['salience']
        ste_score = scores['short_term_extraction']['raw_score']
        ste_salience = scores['short_term_extraction']['salience']

        numerator = (sp_score * sp_salience) - (ste_score * ste_salience)
        denominator = sp_salience + ste_salience + 0.001
        
        return numerator / denominator
    except (KeyError, TypeError):
        return None

def calculate_corporate_responsibility_contradiction_index(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures conflicts between stated values and practices across all domains.
    
    Formula: sum(min(positive_score, negative_score) * abs(positive_salience - negative_salience)) for all opposing pairs.

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated index as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        pairs = [
            ('customer_service', 'customer_exploitation'),
            ('employee_development', 'employee_exploitation'),
            ('accountability', 'opacity'),
            ('financial_responsibility', 'financial_manipulation'),
            ('sustainable_purpose', 'short_term_extraction')
        ]
        
        total_contradiction = 0.0
        for pos_dim, neg_dim in pairs:
            pos_score = scores[pos_dim]['raw_score']
            pos_salience = scores[pos_dim]['salience']
            neg_score = scores[neg_dim]['raw_score']
            neg_salience = scores[neg_dim]['salience']
            
            contradiction_score = min(pos_score, neg_score) * abs(pos_salience - neg_salience)
            total_contradiction += contradiction_score
            
        return total_contradiction
    except (KeyError, TypeError):
        return None

def calculate_stakeholder_strategy_coherence(row: pd.Series, **kwargs) -> Optional[float]:
    """
    Measures consistency across stakeholder relationship approaches.
    
    Formula: 1 - (abs(customer_service - employee_development) + abs(customer_exploitation - employee_exploitation)) / 2

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters (unused).
        
    Returns:
        Calculated coherence score as a float, or None if data is missing.
    """
    scores = _get_dimensional_scores(row)
    if not scores:
        return None
    try:
        cs = scores['customer_service']['raw_score']
        ed = scores['employee_development']['raw_score']
        ce = scores['customer_exploitation']['raw_score']
        ee = scores['employee_exploitation']['raw_score']
        
        incoherence = (abs(cs - ed) + abs(ce - ee)) / 2.0
        
        return 1.0 - incoherence
    except (KeyError, TypeError):
        return None

def calculate_all_derived_metrics(row: pd.Series, **kwargs) -> Dict[str, Optional[float]]:
    """
    Calls all individual derived metric calculation functions for a given row.
    This function explicitly calls each calculator by name to avoid issues with
    dynamic module loading and function discovery via reflection.

    Args:
        row: A pandas Series representing a single row of the DataFrame.
        **kwargs: Additional parameters to pass to calculator functions.

    Returns:
        A dictionary mapping metric names to their calculated values.
    """
    return {
        "stakeholder_focus_index": calculate_stakeholder_focus_index(row, **kwargs),
        "operational_ethics_index": calculate_operational_ethics_index(row, **kwargs),
        "strategic_ethics_index": calculate_strategic_ethics_index(row, **kwargs),
        "salience_weighted_stakeholder_focus": calculate_salience_weighted_stakeholder_focus(row, **kwargs),
        "salience_weighted_operational_ethics": calculate_salience_weighted_operational_ethics(row, **kwargs),
        "salience_weighted_strategic_ethics": calculate_salience_weighted_strategic_ethics(row, **kwargs),
        "corporate_responsibility_contradiction_index": calculate_corporate_responsibility_contradiction_index(row, **kwargs),
        "stakeholder_strategy_coherence": calculate_stakeholder_strategy_coherence(row, **kwargs),
    }

def calculate_derived_metrics(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Applies all derived metric calculations to a DataFrame.

    This wrapper function iterates through each row of the input DataFrame,
    applies all defined metric calculations, and appends the results as new
    columns. It handles the nested data structure and ensures that the
    output is a clean DataFrame with both original and new data.

    Args:
        data: The input pandas DataFrame containing analysis results.
        **kwargs: Additional parameters to pass to calculator functions.

    Returns:
        A new pandas DataFrame with the original columns plus new columns
        for each calculated derived metric. Missing values are represented as NaN.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input 'data' must be a pandas DataFrame.")

    df = data.copy()

    # Apply the function that calculates all metrics for a row.
    # This returns a Series of dictionaries.
    derived_metrics_series = df.apply(
        lambda row: pd.Series(calculate_all_derived_metrics(row, **kwargs)),
        axis=1
    )

    # Join the new metric columns to the original dataframe.
    result_df = df.join(derived_metrics_series)

    return result_df