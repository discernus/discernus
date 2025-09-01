#!/usr/bin/env python3
"""
Correlation Analysis: Van der Veen vs. Discernus PDAF
=====================================================

This script performs correlation analysis between human-coded scores from the
original Van der Veen study and automated PDAF scores from our Discernus analysis.
"""

import pandas as pd
import numpy as np
import csv
from pathlib import Path
from typing import Dict, List, Any, Tuple

def load_pdaf_scores(pdaf_csv_path: str) -> pd.DataFrame:
    """Load the extracted PDAF scores."""
    
    print("=== Loading PDAF Scores ===")
    pdaf_df = pd.read_csv(pdaf_csv_path)
    
    print(f"Loaded {len(pdaf_df)} PDAF score records")
    print(f"Columns: {list(pdaf_df.columns)}")
    
    # Show sample data
    print(f"\nSample PDAF scores:")
    sample = pdaf_df.iloc[0]
    print(f"  Document: {sample['filename']}")
    print(f"  Overall Raw: {sample['overall_raw']:.3f}")
    print(f"  Overall Salience-Weighted: {sample['overall_salience_weighted']:.3f}")
    
    return pdaf_df

def load_vanderveen_data(vdv_csv_path: str) -> pd.DataFrame:
    """Load and process the Van der Veen human-coded data."""
    
    print(f"\n=== Loading Van der Veen Data ===")
    
    # Load the CSV
    vdv_df = pd.read_csv(vdv_csv_path)
    
    print(f"Loaded {len(vdv_df)} Van der Veen records")
    print(f"Column names: {list(vdv_df.columns)}")
    
    # Clean up the data - remove rows with no speech name
    # Note: The column name is "Speech " (with trailing space)
    speech_col = 'Speech '  # Column name with trailing space
    vdv_df = vdv_df.dropna(subset=[speech_col])
    print(f"After cleaning: {len(vdv_df)} records")
    
    # Calculate average scores across coders for each speech
    processed_data = []
    
    for _, row in vdv_df.iterrows():
        speech_name = row[speech_col].strip('"')
        
        # Extract scores from first coder
        score1 = pd.to_numeric(row['Score'], errors='coerce')
        manichaean1 = pd.to_numeric(row['Manichaean vision'], errors='coerce')
        people1 = pd.to_numeric(row['Populist notion of the people'], errors='coerce')
        elite1 = pd.to_numeric(row['Evil elite'], errors='coerce')
        
        # Extract scores from second coder
        score2 = pd.to_numeric(row['Score.1'], errors='coerce')
        manichaean2 = pd.to_numeric(row['Manichaean vision.1'], errors='coerce')
        people2 = pd.to_numeric(row['Populist notion of the people.1'], errors='coerce')
        elite2 = pd.to_numeric(row['Evil elite.1'], errors='coerce')
        
        # Extract scores from third coder (if available)
        score3 = pd.to_numeric(row['Score.2'], errors='coerce')
        manichaean3 = pd.to_numeric(row['Manichaean vision.2'], errors='coerce')
        people3 = pd.to_numeric(row['Populist notion of the people.2'], errors='coerce')
        elite3 = pd.to_numeric(row['Evil elite.2'], errors='coerce')
        
        # Calculate averages (ignoring NaN values)
        scores = [s for s in [score1, score2, score3] if pd.notna(s)]
        manichaean_scores = [s for s in [manichaean1, manichaean2, manichaean3] if pd.notna(s)]
        people_scores = [s for s in [people1, people2, people3] if pd.notna(s)]
        elite_scores = [s for s in [elite1, elite2, elite3] if pd.notna(s)]
        
        avg_score = np.mean(scores) if scores else np.nan
        avg_manichaean = np.mean(manichaean_scores) if manichaean_scores else np.nan
        avg_people = np.mean(people_scores) if people_scores else np.nan
        avg_elite = np.mean(elite_scores) if elite_scores else np.nan
        
        processed_data.append({
            'speech_name': speech_name,
            'avg_score': avg_score,
            'avg_manichaean': avg_manichaean,
            'avg_people': avg_people,
            'avg_elite': avg_elite
        })
    
    vdv_processed = pd.DataFrame(processed_data)
    print(f"Processed {len(vdv_processed)} Van der Veen records")
    
    # Show sample data
    if len(vdv_processed) > 0:
        sample = vdv_processed.iloc[0]
        print(f"\nSample Van der Veen scores:")
        print(f"  Speech: {sample['speech_name']}")
        print(f"  Overall: {sample['avg_score']:.3f}")
        print(f"  Manichaean: {sample['avg_manichaean']:.3f}")
        print(f"  People: {sample['avg_people']:.3f}")
        print(f"  Elite: {sample['avg_elite']:.3f}")
    
    return vdv_processed

def load_speech_mapping(mapping_csv_path: str) -> Dict[str, str]:
    """Load the speech mapping between Van der Veen and Discernus."""
    
    print(f"\n=== Loading Speech Mapping ===")
    
    mapping = {}
    if Path(mapping_csv_path).exists():
        with open(mapping_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row['discernus_filename']] = row['vdv_speech_name']
        
        print(f"Loaded {len(mapping)} speech mappings")
    else:
        print("No speech mapping file found")
    
    return mapping

def merge_datasets(pdaf_df: pd.DataFrame, vdv_df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """Merge the PDAF and Van der Veen datasets using the speech mapping."""
    
    print(f"\n=== Merging Datasets ===")
    
    # The mapping is already correct: Discernus filename -> Van der Veen speech name
    # We can use it directly
    print(f"Using {len(mapping)} speech mappings directly")
    
    # Add Van der Veen speech name to PDAF data
    pdaf_df['vdv_speech_name'] = pdaf_df['filename'].map(mapping)
    
    # Check mapping coverage
    mapped_count = pdaf_df['vdv_speech_name'].notna().sum()
    print(f"PDAF speeches mapped to Van der Veen: {mapped_count}/{len(pdaf_df)} ({mapped_count/len(pdaf_df)*100:.1f}%)")
    
    # Show some mapping examples
    print(f"\nMapping examples:")
    for i, row in pdaf_df.head().iterrows():
        if pd.notna(row['vdv_speech_name']):
            print(f"  {row['filename']} -> {row['vdv_speech_name']}")
    
    # Merge the datasets
    merged_df = pd.merge(
        pdaf_df, 
        vdv_df, 
        left_on='vdv_speech_name', 
        right_on='speech_name', 
        how='inner'
    )
    
    print(f"\nMerged dataset: {len(merged_df)} records")
    print(f"Final mapping coverage: {len(merged_df)}/{len(pdaf_df)} ({len(merged_df)/len(pdaf_df)*100:.1f}%)")
    
    return merged_df

def perform_correlation_analysis(merged_df: pd.DataFrame) -> Dict[str, float]:
    """Perform correlation analysis between the two datasets."""
    
    print(f"\n=== Performing Correlation Analysis ===")
    
    correlations = {}
    
    # Overall score correlation
    if 'overall_salience_weighted' in merged_df.columns and 'avg_score' in merged_df.columns:
        corr_overall = merged_df['overall_salience_weighted'].corr(merged_df['avg_score'])
        correlations['overall_score'] = corr_overall
        print(f"Overall Score Correlation: r = {corr_overall:.3f}")
    
    # Individual dimension correlations
    dimension_mappings = {
        'manichaean_people_elite_framing_raw': 'avg_manichaean',
        'homogeneous_people_construction_raw': 'avg_people',
        'elite_conspiracy_systemic_corruption_raw': 'avg_elite'
    }
    
    for pdaf_dim, vdv_dim in dimension_mappings.items():
        if pdaf_dim in merged_df.columns and vdv_dim in merged_df.columns:
            corr = merged_df[pdaf_dim].corr(merged_df[vdv_dim])
            correlations[f'{pdaf_dim}_vs_{vdv_dim}'] = corr
            print(f"{pdaf_dim} vs {vdv_dim}: r = {corr:.3f}")
    
    # Additional dimension correlations
    additional_dims = [
        'crisis_restoration_narrative_raw',
        'popular_sovereignty_claims_raw',
        'anti_pluralist_exclusion_raw',
        'authenticity_vs_political_class_raw',
        'nationalist_exclusion_raw',
        'economic_populist_appeals_raw'
    ]
    
    for dim in additional_dims:
        if dim in merged_df.columns and 'avg_score' in merged_df.columns:
            corr = merged_df[dim].corr(merged_df['avg_score'])
            correlations[f'{dim}_vs_overall'] = corr
            print(f"{dim} vs Overall: r = {corr:.3f}")
    
    return correlations

def generate_correlation_report(merged_df: pd.DataFrame, correlations: Dict[str, float], output_path: str):
    """Generate a comprehensive correlation report."""
    
    print(f"\n=== Generating Correlation Report ===")
    
    report_lines = []
    report_lines.append("# Correlation Analysis Report: Van der Veen vs. Discernus PDAF")
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Total Records:** {len(merged_df)}")
    report_lines.append(f"**Mapping Coverage:** {len(merged_df)} speeches")
    report_lines.append("")
    
    # Summary statistics
    report_lines.append("## Summary Statistics")
    report_lines.append("")
    
    if 'overall_salience_weighted' in merged_df.columns and 'avg_score' in merged_df.columns:
        pdaf_mean = merged_df['overall_salience_weighted'].mean()
        pdaf_std = merged_df['overall_salience_weighted'].std()
        vdv_mean = merged_df['avg_score'].mean()
        vdv_std = merged_df['avg_score'].std()
        
        report_lines.append(f"**PDAF Overall Scores:**")
        report_lines.append(f"- Mean: {pdaf_mean:.3f}")
        report_lines.append(f"- Std Dev: {pdaf_std:.3f}")
        report_lines.append("")
        report_lines.append(f"**Van der Veen Overall Scores:**")
        report_lines.append(f"- Mean: {vdv_mean:.3f}")
        report_lines.append(f"- Std Dev: {vdv_std:.3f}")
        report_lines.append("")
    
    # Correlation results
    report_lines.append("## Correlation Results")
    report_lines.append("")
    
    for correlation_name, corr_value in correlations.items():
        report_lines.append(f"**{correlation_name}:** r = {corr_value:.3f}")
        
        # Interpret correlation strength
        if abs(corr_value) >= 0.7:
            strength = "Strong"
        elif abs(corr_value) >= 0.5:
            strength = "Moderate"
        elif abs(corr_value) >= 0.3:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        report_lines.append(f"- Strength: {strength}")
        report_lines.append("")
    
    # Sample data
    report_lines.append("## Sample Data")
    report_lines.append("")
    report_lines.append("First 5 records from merged dataset:")
    report_lines.append("")
    
    sample_cols = ['filename', 'overall_salience_weighted', 'avg_score', 'avg_manichaean', 'avg_people', 'avg_elite']
    available_cols = [col for col in sample_cols if col in merged_df.columns]
    
    if available_cols:
        sample_data = merged_df[available_cols].head()
        report_lines.append(sample_data.to_string(index=False))
    
    # Write report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✓ Correlation report generated: {output_path}")

def main():
    """Main execution function."""
    
    # Configuration
    base_dir = "/Volumes/code/discernus/pm/vanderveen_replication_extension/comparative_analysis"
    pdaf_csv_path = os.path.join(base_dir, "pdaf_scores_extracted.csv")
    vdv_csv_path = "/Volumes/code/discernus/pm/vanderveen_replication_extension/original_data/combined-data-set-xlsx.csv"
    mapping_csv_path = os.path.join(base_dir, "speech_mapping.csv")
    
    print("=== Van der Veen vs. Discernus PDAF Correlation Analysis ===")
    
    try:
        # Load datasets
        pdaf_df = load_pdaf_scores(pdaf_csv_path)
        vdv_df = load_vanderveen_data(vdv_csv_path)
        mapping = load_speech_mapping(mapping_csv_path)
        
        # Merge datasets
        merged_df = merge_datasets(pdaf_df, vdv_df, mapping)
        
        if len(merged_df) > 0:
            # Perform correlation analysis
            correlations = perform_correlation_analysis(merged_df)
            
            # Save merged dataset
            merged_csv_path = os.path.join(base_dir, "correlation_results.csv")
            merged_df.to_csv(merged_csv_path, index=False)
            print(f"\n✓ Merged dataset saved: {merged_csv_path}")
            
            # Generate correlation report
            report_path = os.path.join(base_dir, "correlation_report.md")
            generate_correlation_report(merged_df, correlations, report_path)
            
            print(f"\n=== Analysis Complete ===")
            print(f"Successfully analyzed {len(merged_df)} matched speeches")
            print(f"Ready for detailed interpretation of correlation results")
            
        else:
            print("No matched records found. Check speech mapping.")
            
    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import os
    main()
