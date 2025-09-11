#!/usr/bin/env python3
"""
Discernus Statistical Package - Python Import Script
==================================================

Import and prepare data for statistical analysis in Python.
Compatible with pandas, numpy, scipy, statsmodels, and scikit-learn.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def load_discernus_data(package_dir="."):
    """
    Load all datasets from Discernus statistical package.
    
    Args:
        package_dir: Path to statistical package directory
        
    Returns:
        dict: Dictionary containing all datasets
    """
    package_path = Path(package_dir)
    
    datasets = {}
    
    # Load analysis scores
    scores_file = package_path / "analysis_scores.csv"
    if scores_file.exists():
        datasets['scores'] = pd.read_csv(scores_file)
        print(f"Loaded scores: {len(datasets['scores'])} documents")
    
    # Load supporting evidence
    evidence_file = package_path / "supporting_evidence.csv"
    if evidence_file.exists():
        datasets['evidence'] = pd.read_csv(evidence_file)
        print(f"Loaded evidence: {len(datasets['evidence'])} quotes")
    
    # Load document metadata
    metadata_file = package_path / "document_metadata.csv"
    if metadata_file.exists():
        datasets['metadata'] = pd.read_csv(metadata_file)
        print(f"Loaded metadata: {len(datasets['metadata'])} documents")
    
    return datasets

def prepare_for_analysis(datasets):
    """
    Prepare data for statistical analysis.
    
    Args:
        datasets: Dictionary from load_discernus_data()
        
    Returns:
        dict: Prepared datasets ready for analysis
    """
    prepared = {}
    
    if 'scores' in datasets:
        scores = datasets['scores'].copy()
        
        # Convert numeric columns
        numeric_cols = scores.select_dtypes(include=[np.number]).columns
        scores[numeric_cols] = scores[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Create analysis-ready dataframe
        prepared['analysis_data'] = scores
        
        print(f"Prepared analysis data: {prepared['analysis_data'].shape}")
    
    return prepared

# Example usage
if __name__ == "__main__":
    # Load data
    data = load_discernus_data()
    
    # Prepare for analysis
    prepared = prepare_for_analysis(data)
    
    # Basic descriptive statistics
    if 'analysis_data' in prepared:
        print("\nDescriptive Statistics:")
        print(prepared['analysis_data'].describe())
        
        print("\nMissing Values:")
        print(prepared['analysis_data'].isnull().sum())
