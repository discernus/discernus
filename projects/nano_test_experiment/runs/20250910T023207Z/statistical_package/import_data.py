#!/usr/bin/env python3
"""
Statistical Analysis Import Script
================================

Import script for loading Discernus statistical preparation data
into external statistical analysis tools (R, Python, SPSS, etc.).
"""

import pandas as pd
import os

# Load data files
scores_df = pd.read_csv('scores.csv')
evidence_df = pd.read_csv('evidence.csv')
metadata_df = pd.read_csv('metadata.csv')

print("Data loaded successfully:")
print(f"- Scores: {len(scores_df)} rows, {len(scores_df.columns)} columns")
print(f"- Evidence: {len(evidence_df)} rows, {len(evidence_df.columns)} columns")
print(f"- Metadata: {len(metadata_df)} rows, {len(metadata_df.columns)} columns")

# Example analysis
print("\nSample analysis:")
print(scores_df.describe())
