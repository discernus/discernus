import numpy as np
import pandas as pd
from scipy import stats
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def calculate_icc(df: pd.DataFrame, well_columns: List[str]) -> Dict[str, any]:
    """Calculate Intraclass Correlation Coefficient (ICC) for each well."""
    logger.info("📊 Calculating Intraclass Correlation Coefficients (ICC)...")
    icc_results: Dict[str, any] = {}

    for well_col in well_columns:
        try:
            well_data = df.pivot_table(
                values=well_col,
                index='text_id' if 'text_id' in df.columns else df.index,
                columns='model' if 'model' in df.columns else 'rater',
                aggfunc='mean'
            ).dropna()

            if well_data.shape[0] < 2 or well_data.shape[1] < 2:
                icc_results[well_col] = {
                    'icc_value': None,
                    'interpretation': 'insufficient_data',
                    'message': f'Insufficient data: {well_data.shape[0]} texts, {well_data.shape[1]} raters'
                }
                continue

            icc_value = _calculate_icc_two_way(well_data.values)
            icc_results[well_col] = {
                'icc_value': float(icc_value) if icc_value is not None else None,
                'interpretation': interpret_icc(icc_value) if icc_value is not None else 'calculation_failed',
                'sample_size': well_data.shape[0],
                'rater_count': well_data.shape[1],
                'mean_score': float(well_data.values.mean()),
                'std_score': float(well_data.values.std())
            }
        except Exception as e:
            logger.warning(f"Could not calculate ICC for {well_col}: {e}")
            icc_results[well_col] = {
                'icc_value': None,
                'interpretation': 'calculation_error',
                'error': str(e)
            }
    return icc_results


def _calculate_icc_two_way(data: np.ndarray) -> Optional[float]:
    """Calculate ICC(2,1) using ANOVA approach."""
    try:
        n_subjects, n_raters = data.shape
        subject_means = np.mean(data, axis=1)
        rater_means = np.mean(data, axis=0)
        grand_mean = np.mean(data)

        ss_total = np.sum((data - grand_mean) ** 2)
        ss_between_subjects = n_raters * np.sum((subject_means - grand_mean) ** 2)
        ss_between_raters = n_subjects * np.sum((rater_means - grand_mean) ** 2)
        ss_error = ss_total - ss_between_subjects - ss_between_raters

        ms_between_subjects = ss_between_subjects / (n_subjects - 1)
        ms_between_raters = ss_between_raters / (n_raters - 1)
        ms_error = ss_error / ((n_subjects - 1) * (n_raters - 1))

        if ms_error == 0:
            return 1.0

        icc = (ms_between_subjects - ms_error) / (
            ms_between_subjects + (n_raters - 1) * ms_error +
            n_raters * (ms_between_raters - ms_error) / n_subjects
        )
        return max(0.0, min(1.0, icc))
    except Exception as e:
        logger.warning(f"ICC calculation failed: {e}")
        return None


def interpret_icc(icc_value: Optional[float]) -> str:
    """Interpret ICC value according to standard guidelines."""
    if icc_value is None:
        return 'unknown'
    if icc_value < 0.5:
        return 'poor'
    if icc_value < 0.75:
        return 'moderate'
    if icc_value < 0.9:
        return 'good'
    return 'excellent'
