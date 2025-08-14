Of course. As a statistical analysis expert, I will enhance your existing Python notebook by adding the requested statistical functions. I will carefully integrate the new code, ensuring that all existing functionality remains intact and operational.

Here is the complete, enhanced Python script. The new code is added between the existing formula implementations and the `main` function, and the `main` function has been updated to execute the statistical analysis and save the results.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CFF_v7.3_Derived_Metrics_Calculator.py

This script calculates derived metrics from analysis data based on the 
Cohesive Flourishing Framework (CFF) v7.3 specification. It is designed 
for academic research data analysis, ensuring transparency and rigor in its 
calculations.

The script performs the following steps:
1.  Loads analysis data from 'analysis_data.json'.
2.  Implements the specific mathematical formulas defined in the CFF v7.3 
    framework to calculate tension scores and composite indices.
3.  Applies these calculations to every document in the dataset, handling
    potential missing data gracefully.
4.  Outputs the results, including all original scores and the newly derived 
    metrics, into a 'derived_metrics_results.csv' file.
5.  Performs and saves a comprehensive statistical analysis of the derived
    metrics, including descriptive statistics, correlation analysis, and
    comparative tests.
"""

import json
import pandas as pd
import numpy as np
import sys
import os
from scipy import stats
from itertools import combinations

# --- CFF v7.3 FORMULA IMPLEMENTATIONS ---
# These functions directly implement the mathematical formulas specified in the
# Cohesive Flourishing Framework v7.3's 'calculation_spec'.

# === TENSION SCORE CALCULATIONS ===

def calculate_identity_tension(tribal_dominance_score, individual_dignity_score, tribal_dominance_salience, individual_dignity_salience):
    """
    Calculates the tension between tribal dominance and individual dignity appeals.
    Formula: min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)
    """
    try:
        return min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)
    except TypeError:
        return np.nan

def calculate_emotional_tension(fear_score, hope_score, fear_salience, hope_salience):
    """
    Calculates the tension between fear and hope appeals.
    Formula: min(fear_score, hope_score) * abs(fear_salience - hope_salience)
    """
    try:
        return min(fear_score, hope_score) * abs(fear_salience - hope_salience)
    except TypeError:
        return np.nan

def calculate_success_tension(envy_score, compersion_score, envy_salience, compersion_salience):
    """
    Calculates the tension between envy and compersion appeals.
    Formula: min(envy_score, compersion_score) * abs(envy_salience - compersion_salience)
    """
    try:
        return min(envy_score, compersion_score) * abs(envy_salience - compersion_salience)
    except TypeError:
        return np.nan

def calculate_relational_tension(enmity_score, amity_score, enmity_salience, amity_salience):
    """
    Calculates the tension between enmity and amity appeals.
    Formula: min(enmity_score, amity_score) * abs(enmity_salience - amity_salience)
    """
    try:
        return min(enmity_score, amity_score) * abs(enmity_salience - amity_salience)
    except TypeError:
        return np.nan

def calculate_goal_tension(fragmentative_goals_score, cohesive_goals_score, fragmentative_goals_salience, cohesive_goals_salience):
    """
    Calculates the tension between fragmentative and cohesive goal appeals.
    Formula: min(fragmentative_goals_score, cohesive_goals_score) * abs(fragmentative_goals_salience - cohesive_goals_salience)
    """
    try:
        return min(fragmentative_goals_score, cohesive_goals_score) * abs(fragmentative_goals_salience - cohesive_goals_salience)
    except TypeError:
        return np.nan

# === COMPOSITE INDEX CALCULATIONS ===

def calculate_cohesive_index(individual_dignity_score, hope_score, compersion_score, amity_score, cohesive_goals_score):
    """
    Calculates the unweighted average of all cohesive dimension scores.
    Formula: (individual_dignity_score + hope_score + compersion_score + amity_score + cohesive_goals_score) / 5
    """
    scores = [individual_dignity_score, hope_score, compersion_score, amity_score, cohesive_goals_score]
    if any(pd.isna(s) for s in scores):
        return np.nan
    return sum(scores) / 5

def calculate_fragmentative_index(tribal_dominance_score, fear_score, envy_score, enmity_score, fragmentative_goals_score):
    """
    Calculates the unweighted average of all fragmentative dimension scores.
    Formula: (tribal_dominance_score + fear_score + envy_score + enmity_score + fragmentative_goals_score) / 5
    """
    scores = [tribal_dominance_score, fear_score, envy_score, enmity_score, fragmentative_goals_score]
    if any(pd.isna(s) for s in scores):
        return np.nan
    return sum(scores) / 5

def calculate_salience_weighted_cohesive_index(scores):
    """
    Calculates the salience-weighted average of cohesive dimension scores.
    Formula: Sum(score * salience) / Sum(salience) for all cohesive dimensions.
    """
    numerator = (scores.get('individual_dignity_score', 0) * scores.get('individual_dignity_salience', 0) +
                 scores.get('hope_score', 0) * scores.get('hope_salience', 0) +
                 scores.get('compersion_score', 0) * scores.get('compersion_salience', 0) +
                 scores.get('amity_score', 0) * scores.get('amity_salience', 0) +
                 scores.get('cohesive_goals_score', 0) * scores.get('cohesive_goals_salience', 0))
    
    denominator = (scores.get('individual_dignity_salience', 0) +
                   scores.get('hope_salience', 0) +
                   scores.get('compersion_salience', 0) +
                   scores.get('amity_salience', 0) +
                   scores.get('cohesive_goals_salience', 0))
    
    if denominator == 0:
        return 0
    return numerator / denominator

# --- STATISTICAL ANALYSIS FUNCTIONS ---

def calculate_descriptive_statistics(df):
    """
    Calculates descriptive statistics for all numeric columns in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        
    Returns:
        pd.DataFrame: A DataFrame with descriptive statistics (mean, median, 
                      std dev, min, max, etc.) for each numeric variable.
    """
    print("   - Calculating descriptive statistics...")
    try:
        numeric_df = df.select_dtypes(include=np.number)
        desc_stats = numeric_df.describe().transpose()
        # For clarity, rename the '50%' column to 'median'
        desc_stats.rename(columns={'50%': 'median'}, inplace=True)
        return desc_stats[['count', 'mean', 'std', 'median', 'min', 'max']]
    except Exception as e:
        print(f"     Error calculating descriptive statistics: {e}")
        return pd.DataFrame()

def calculate_correlation_matrix(df):
    """
    Calculates a Pearson correlation matrix for key derived metrics.
    Includes correlation coefficients, p-values, and a significance flag.
    
    Args:
        df (pd.DataFrame): DataFrame containing the derived metrics.
        
    Returns:
        pd.DataFrame: A DataFrame showing the pairwise correlation analysis.
    """
    print("   - Performing correlation analysis...")
    try:
        metrics_to_correlate = [
            'cohesive_index', 'fragmentative_index', 'overall_cohesion_index',
            'strategic_contradiction_index', 'identity_tension', 'emotional_tension',
            'success_tension', 'relational_tension', 'goal_tension'
        ]
        # Ensure only existing columns are used
        valid_metrics = [col for col in metrics_to_correlate if col in df.columns]
        
        corr_df = df[valid_metrics].dropna()
        
        if len(corr_df) < 2:
            print("     Not enough data to calculate correlations.")
            return pd.DataFrame()

        results = []
        for col1, col2 in combinations(valid_metrics, 2):
            r, p_value = stats.pearsonr(corr_df[col1], corr_df[col2])
            results.append({
                'Variable 1': col1,
                'Variable 2': col2,
                'Pearson Correlation': r,
                'P-value': p_value,
                'Significant (p<0.05)': p_value < 0.05
            })
        return pd.DataFrame(results)
    except Exception as e:
        print(f"     Error calculating correlation matrix: {e}")
        return pd.DataFrame()

def perform_cohesion_analysis(df):
    """
    Compares cohesive vs. fragmentative indices using a paired t-test.
    This test is appropriate as the indices are calculated for each document.
    
    Args:
        df (pd.DataFrame): DataFrame with 'cohesive_index' and 'fragmentative_index'.
        
    Returns:
        pd.DataFrame: A DataFrame summarizing the t-test results.
    """
    print("   - Comparing cohesive vs. fragmentative indices...")
    try:
        # Prepare data by dropping rows where either index is NaN
        paired_data = df[['cohesive_index', 'fragmentative_index']].dropna()
        
        if len(paired_data) < 2:
            print("     Not enough paired data to perform t-test.")
            return pd.DataFrame([{"Error": "Insufficient data"}])
            
        t_stat, p_value = stats.ttest_rel(paired_data['cohesive_index'], paired_data['fragmentative_index'])
        
        result = {
            'Comparison': 'Cohesive Index vs. Fragmentative Index',
            'Test': 'Paired T-Test',
            'T-statistic': t_stat,
            'P-value': p_value,
            'Significant (p<0.05)': p_value < 0.05
        }
        return pd.DataFrame([result])
    except Exception as e:
        print(f"     Error performing cohesion analysis: {e}")
        return pd.DataFrame([{"Error": str(e)}])

def analyze_tension_patterns(df):
    """
    Analyzes each tension score to see if its mean is significantly different from zero
    using a one-sample t-test.
    
    Args:
        df (pd.DataFrame): DataFrame containing the tension scores.
        
    Returns:
        pd.DataFrame: A DataFrame summarizing the one-sample t-test results for each tension score.
    """
    print("   - Analyzing tension score patterns...")
    try:
        tension_cols = [
            'identity_tension', 'emotional_tension', 'success_tension',
            'relational_tension', 'goal_tension'
        ]
        results = []
        for col in tension_cols:
            if col not in df.columns:
                continue
            
            # Prepare data by dropping NaNs for the specific tension score
            tension_data = df[col].dropna()
            
            if len(tension_data) < 2:
                print(f"     Not enough data for '{col}' to perform t-test.")
                continue
            
            t_stat, p_value = stats.ttest_1samp(tension_data, 0)
            results.append({
                'Tension Metric': col,
                'Test': 'One-Sample T-Test (vs 0)',
                'T-statistic': t_stat,
                'P-value': p_value,
                'Significant (p<0.05)': p_value < 0.05
            })
        return pd.DataFrame(results)
    except Exception as e:
        print(f"     Error analyzing tension patterns: {e}")
        return pd.DataFrame()

# --- MAIN EXECUTION ---

def main():
    """Main execution function"""
    print("🔬 CFF v7.3 Derived Metrics Calculator")
    print("=" * 50)
    
    # Load analysis data - check multiple possible locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        'analysis_data.json',  # Current directory
        os.path.join(script_dir, 'analysis_data.json'),  # Same directory as script
        os.path.join(os.getcwd(), 'analysis_data.json'),  # Working directory
    ]
    
    analysis_data = None
    for data_path in possible_paths:
        try:
            with open(data_path, 'r') as f:
                analysis_data = json.load(f)
            print(f"✅ Loaded analysis data from: {data_path}")
            print(f"   📊 Documents: {len(analysis_data['document_analyses'])}")
            break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"❌ Error loading {data_path}: {e}")
            continue
    
    if analysis_data is None:
        print("❌ analysis_data.json not found in any expected location!")
        print("   Searched:")
        for path in possible_paths:
            print(f"   - {path}")
        return
    
    # Process each document
    results = []
    for doc_analysis in analysis_data['document_analyses']:
        doc_id = doc_analysis['document_id']
        doc_name = doc_analysis['document_name']
        scores = doc_analysis['scores']
        
        print(f"📄 Processing: {doc_name}")
        
        # Calculate all derived metrics
        identity_tension = calculate_identity_tension(
            scores.get('tribal_dominance_score'),
            scores.get('individual_dignity_score'),
            scores.get('tribal_dominance_salience'),
            scores.get('individual_dignity_salience')
        )
        
        emotional_tension = calculate_emotional_tension(
            scores.get('fear_score'),
            scores.get('hope_score'),
            scores.get('fear_salience'),
            scores.get('hope_salience')
        )
        
        success_tension = calculate_success_tension(
            scores.get('envy_score'),
            scores.get('compersion_score'),
            scores.get('envy_salience'),
            scores.get('compersion_salience')
        )
        
        relational_tension = calculate_relational_tension(
            scores.get('enmity_score'),
            scores.get('amity_score'),
            scores.get('enmity_salience'),
            scores.get('amity_salience')
        )
        
        goal_tension = calculate_goal_tension(
            scores.get('fragmentative_goals