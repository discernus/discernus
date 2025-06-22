import logging
from typing import Dict, List
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def calculate_cronbach_alpha(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    """Calculate Cronbach's Alpha for internal consistency."""
    logger.info("📊 Calculating Cronbach's Alpha...")
    try:
        well_matrix = df[well_columns].dropna()
        if well_matrix.empty or well_matrix.shape[1] < 2:
            return {
                'alpha_value': None,
                'interpretation': 'insufficient_data',
                'message': 'Need at least 2 wells with data'
            }
        n_items = well_matrix.shape[1]
        item_variances = well_matrix.var(axis=0, ddof=1)
        total_variance = well_matrix.sum(axis=1).var(ddof=1)
        if total_variance == 0:
            alpha = 1.0
        else:
            alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        return {
            'alpha_value': float(alpha),
            'interpretation': interpret_cronbach_alpha(alpha),
            'n_items': n_items,
            'sample_size': len(well_matrix),
            'item_statistics': {
                well: {
                    'mean': float(well_matrix[well].mean()),
                    'std': float(well_matrix[well].std()),
                    'item_total_correlation': float(well_matrix[well].corr(well_matrix.drop(columns=[well]).sum(axis=1)))
                } for well in well_columns if well in well_matrix.columns
            }
        }
    except Exception as e:
        logger.warning(f"Cronbach's Alpha calculation failed: {e}")
        return {
            'alpha_value': None,
            'interpretation': 'calculation_error',
            'error': str(e)
        }


def interpret_cronbach_alpha(alpha: float) -> str:
    """Interpret Cronbach's Alpha value."""
    if alpha is None:
        return 'unknown'
    if alpha < 0.6:
        return 'poor'
    if alpha < 0.7:
        return 'questionable'
    if alpha < 0.8:
        return 'acceptable'
    if alpha < 0.9:
        return 'good'
    return 'excellent'
