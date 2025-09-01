#!/usr/bin/env python3
"""
PDAF Scores Extractor for Comparative Analysis
==============================================

This script extracts PDAF scores from analysis result files and converts them
to CSV format for comparison with Van der Veen human-coded data.
"""

import json
import csv
import os
import re
from pathlib import Path
from typing import Dict, List, Any

def extract_pdaf_scores_from_artifacts(artifact_registry_path: str, artifacts_dir: str) -> List[Dict[str, Any]]:
    """Extract PDAF scores from all analysis result artifacts."""
    
    print("=== Extracting PDAF Scores from Analysis Artifacts ===")
    
    # Load artifact registry
    with open(artifact_registry_path, 'r') as f:
        registry = json.load(f)
    
    # Find all analysis result artifacts
    analysis_results = []
    for artifact_id, artifact_info in registry.items():
        metadata = artifact_info.get('metadata', {})
        if metadata.get('artifact_type') == 'analysis_result':
            analysis_results.append({
                'artifact_id': artifact_id,
                'artifact_path': artifact_info['artifact_path'],
                'created_at': artifact_info['created_at']
            })
    
    print(f"Found {len(analysis_results)} analysis result artifacts")
    
    # Extract scores from each artifact
    all_scores = []
    
    for result in analysis_results:
        try:
            artifact_file = Path(artifacts_dir) / result['artifact_path']
            
            if artifact_file.exists():
                with open(artifact_file, 'r') as f:
                    artifact_data = json.load(f)
                
                # Extract the JSON content from the raw response
                raw_response = artifact_data.get('raw_analysis_response', '')
                json_match = re.search(
                    r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n(.*?)\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>', 
                    raw_response, 
                    re.DOTALL
                )
                
                if json_match:
                    analysis_json = json.loads(json_match.group(1))
                    
                    # Process each document analysis
                    for doc_analysis in analysis_json.get('document_analyses', []):
                        filename = doc_analysis.get('document_name', '')
                        document_id = doc_analysis.get('document_id', '')
                        dimensional_scores = doc_analysis.get('dimensional_scores', {})
                        
                        # Calculate overall scores
                        raw_scores = []
                        salience_scores = []
                        
                        for dimension, scores in dimensional_scores.items():
                            raw_score = scores.get('raw_score', 0)
                            salience = scores.get('salience', 0)
                            raw_scores.append(raw_score)
                            salience_scores.append(raw_score * salience)
                        
                        overall_raw = sum(raw_scores) / len(raw_scores) if raw_scores else 0
                        overall_salience_weighted = sum(salience_scores) / len(salience_scores) if salience_scores else 0
                        
                        # Create score record
                        score_record = {
                            'artifact_id': result['artifact_id'],
                            'document_id': document_id,
                            'filename': filename,
                            'overall_raw': overall_raw,
                            'overall_salience_weighted': overall_salience_weighted,
                            'created_at': result['created_at']
                        }
                        
                        # Add individual dimension scores
                        for dimension, scores in dimensional_scores.items():
                            score_record[f'{dimension}_raw'] = scores.get('raw_score', 0)
                            score_record[f'{dimension}_salience'] = scores.get('salience', 0)
                            score_record[f'{dimension}_confidence'] = scores.get('confidence', 0)
                        
                        all_scores.append(score_record)
                        
                        print(f"✓ Extracted scores for: {filename}")
                
            else:
                print(f"⚠ Artifact file not found: {artifact_file}")
                
        except Exception as e:
            print(f"✗ Error processing artifact {result['artifact_id']}: {e}")
    
    print(f"Successfully extracted scores from {len(all_scores)} documents")
    return all_scores

def save_scores_to_csv(scores: List[Dict[str, Any]], output_path: str) -> str:
    """Save extracted scores to CSV file."""
    
    if not scores:
        print("No scores to save")
        return ""
    
    # Get all possible column names
    all_columns = set()
    for score in scores:
        all_columns.update(score.keys())
    
    # Sort columns for consistent output
    column_order = [
        'artifact_id', 'document_id', 'filename', 'overall_raw', 'overall_salience_weighted',
        'created_at'
    ]
    
    # Add dimension columns in alphabetical order
    dimension_columns = sorted([col for col in all_columns if col not in column_order])
    column_order.extend(dimension_columns)
    
    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_order)
        writer.writeheader()
        
        for score in scores:
            # Ensure all columns are present (fill missing with empty string)
            row = {col: score.get(col, '') for col in column_order}
            writer.writerow(row)
    
    print(f"✓ Scores saved to: {output_path}")
    return output_path

def create_speech_mapping_for_comparison(scores: List[Dict[str, Any]], mapping_csv_path: str) -> Dict[str, str]:
    """Create a mapping between Discernus filenames and Van der Veen speech names."""
    
    print("=== Creating Speech Mapping for Comparison ===")
    
    # Load existing mapping
    mapping = {}
    if os.path.exists(mapping_csv_path):
        with open(mapping_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row['discernus_filename']] = row['vdv_speech_name']
    
    # Find unmapped speeches
    unmapped = []
    for score in scores:
        filename = score['filename']
        if filename not in mapping:
            unmapped.append(filename)
    
    if unmapped:
        print(f"Found {len(unmapped)} unmapped speeches:")
        for filename in unmapped[:10]:  # Show first 10
            print(f"  - {filename}")
        if len(unmapped) > 10:
            print(f"  ... and {len(unmapped) - 10} more")
    
    mapped_count = len(scores) - len(unmapped)
    print(f"Mapping coverage: {mapped_count}/{len(scores)} speeches ({mapped_count/len(scores)*100:.1f}%)")
    
    return mapping

def main():
    """Main execution function."""
    
    # Configuration
    artifact_registry_path = "/Volumes/code/discernus/projects/vanderveen_presidential_pdaf/shared_cache/artifacts/artifact_registry.json"
    artifacts_dir = "/Volumes/code/discernus/projects/vanderveen_presidential_pdaf/shared_cache/artifacts"
    output_dir = "/Volumes/code/discernus/pm/vanderveen_replication_extension/comparative_analysis"
    mapping_csv_path = os.path.join(output_dir, "speech_mapping.csv")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract PDAF scores
    scores = extract_pdaf_scores_from_artifacts(artifact_registry_path, artifacts_dir)
    
    if scores:
        # Save scores to CSV
        scores_csv_path = os.path.join(output_dir, "pdaf_scores_extracted.csv")
        save_scores_to_csv(scores, scores_csv_path)
        
        # Create speech mapping
        mapping = create_speech_mapping_for_comparison(scores, mapping_csv_path)
        
        # Show summary
        print(f"\n=== Extraction Summary ===")
        print(f"Total documents processed: {len(scores)}")
        print(f"Output CSV: {scores_csv_path}")
        print(f"Speech mapping: {mapping_csv_path}")
        
        # Show sample data
        if scores:
            print(f"\nSample extracted scores:")
            sample = scores[0]
            print(f"  Document: {sample['filename']}")
            print(f"  Overall Raw Score: {sample['overall_raw']:.3f}")
            print(f"  Overall Salience-Weighted: {sample['overall_salience_weighted']:.3f}")
            print(f"  Dimensions: {len([k for k in sample.keys() if k.endswith('_raw')])}")
        
        return scores_csv_path
    else:
        print("No scores extracted. Check error messages above.")
        return None

if __name__ == "__main__":
    try:
        output_file = main()
        if output_file:
            print(f"\n✓ PDAF scores extraction completed successfully!")
            print(f"Ready for correlation analysis with Van der Veen data.")
        else:
            print(f"\n✗ PDAF scores extraction failed.")
            
    except Exception as e:
        print(f"Script error: {e}")
        import traceback
        traceback.print_exc()
