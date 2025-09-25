#!/usr/bin/env python3
"""
Simple CSV export script for Discernus experiment data.
Extracts raw scores, derived metrics, and evidence quotes from composite_analysis artifacts.
"""

import json
import csv
import sys
from pathlib import Path
import argparse

def permissive_json_parse(json_string):
    """Attempt to parse JSON with tolerantjson for LLM output."""
    try:
        import tolerantjson
        return tolerantjson.tolerate(json_string)
    except ImportError:
        # Fallback to standard json if tolerantjson not available
        return None
    except Exception as e:
        # If tolerantjson fails, return None
        print(f"Info: tolerantjson failed: {e}")
        return None


def extract_csv_data(experiment_path, output_file):
    """Extract CSV data from composite_analysis artifacts."""
    experiment_path = Path(experiment_path)
    
    # Find all composite_analysis JSON files
    # Look in artifacts/analysis/ subdirectory if it exists, otherwise search recursively
    if (experiment_path / "artifacts" / "analysis").exists():
        composite_files = list((experiment_path / "artifacts" / "analysis").glob("composite_analysis_*.json"))
        # Also look for score_extraction files as fallback
        score_files = list((experiment_path / "artifacts" / "analysis").glob("score_extraction_*.json"))
    else:
        composite_files = list(experiment_path.glob("**/composite_analysis_*.json"))
        score_files = list(experiment_path.glob("**/score_extraction_*.json"))
    
    if not composite_files and not score_files:
        print(f"No analysis files found in {experiment_path}")
        return
    
    rows = []
    
    for composite_file in composite_files:
        try:
            with open(composite_file, 'r') as f:
                data = json.load(f)
            
            # Extract document analyses
            if 'raw_analysis_response' in data:
                # Parse the JSON from the raw response (remove ```json wrapper)
                raw_response = data['raw_analysis_response']
                if raw_response.startswith('```json\n'):
                    raw_response = raw_response[7:]  # Remove ```json\n
                if raw_response.endswith('\n```'):
                    raw_response = raw_response[:-4]  # Remove \n```
                
                try:
                    # Try standard JSON parsing first
                    response_data = json.loads(raw_response)
                except json.JSONDecodeError as e:
                    # Try permissive parsing with common LLM fixes
                    print(f"Info: Standard JSON parsing failed for {composite_file.name}: {e}")
                    response_data = permissive_json_parse(raw_response)
                    if response_data is None:
                        print(f"Warning: Skipping {composite_file.name} due to JSON parsing error")
                        continue
                    else:
                        print(f"Info: Used permissive parsing for {composite_file.name}")
                document_analyses = response_data.get('document_analyses', [])
                
                for doc in document_analyses:
                    document_id = doc.get('document_id', 'unknown')
                    dimensional_scores = doc.get('dimensional_scores', {})
                    derived_metrics = doc.get('derived_metrics', {})
                    evidence_quotes = doc.get('evidence_quotes', {})
                    
                    # Create rows for each dimension
                    for dimension, scores in dimensional_scores.items():
                        raw_score = scores.get('raw_score', '')
                        salience = scores.get('salience', '')
                        confidence = scores.get('confidence', '')
                        
                        # Get evidence quotes for this dimension
                        dimension_quotes = evidence_quotes.get(dimension, [])
                        
                        # Create a row for each derived metric + evidence quote combination
                        if derived_metrics:
                            for metric_name, metric_value in derived_metrics.items():
                                for quote in dimension_quotes:
                                    rows.append({
                                        'document_id': document_id,
                                        'dimension': dimension,
                                        'raw_score': raw_score,
                                        'salience': salience,
                                        'confidence': confidence,
                                        'derived_metric_name': metric_name,
                                        'derived_metric_value': metric_value,
                                        'evidence_quote': quote
                                    })
                        else:
                            # If no derived metrics, just create rows with scores and quotes
                            for quote in dimension_quotes:
                                rows.append({
                                    'document_id': document_id,
                                    'dimension': dimension,
                                    'raw_score': raw_score,
                                    'salience': salience,
                                    'confidence': confidence,
                                    'derived_metric_name': '',
                                    'derived_metric_value': '',
                                    'evidence_quote': quote
                                })
                            
        except Exception as e:
            print(f"Error processing {composite_file}: {e}")
            continue
    
    # Process score_extraction files as fallback for missing composite_analysis data
    for score_file in score_files:
        try:
            with open(score_file, 'r') as f:
                data = json.load(f)
            
            # Extract document info from filename or metadata
            document_id = score_file.stem.replace('score_extraction_', '')
            
            # Parse the score_extraction response
            if 'score_extraction' in data:
                raw_response = data['score_extraction']
                if raw_response.startswith('```json\n'):
                    raw_response = raw_response[7:]  # Remove ```json\n
                if raw_response.endswith('\n```'):
                    raw_response = raw_response[:-4]  # Remove \n```
                
                try:
                    response_data = json.loads(raw_response)
                except json.JSONDecodeError as e:
                    print(f"Info: Standard JSON parsing failed for {score_file.name}: {e}")
                    response_data = permissive_json_parse(raw_response)
                    if response_data is None:
                        print(f"Warning: Skipping {score_file.name} due to JSON parsing error")
                        continue
                    else:
                        print(f"Info: Used permissive parsing for {score_file.name}")
                
                dimensional_scores = response_data.get('dimensional_scores', {})
                derived_metrics = response_data.get('derived_metrics', {})
                
                # Process each dimension
                for dimension, scores in dimensional_scores.items():
                    raw_score = scores.get('raw_score')
                    salience = scores.get('salience')
                    confidence = scores.get('confidence')
                    
                    # Add derived metrics as separate rows
                    for metric_name, metric_value in derived_metrics.items():
                        rows.append({
                            'document_id': document_id,
                            'dimension': dimension,
                            'raw_score': raw_score,
                            'salience': salience,
                            'confidence': confidence,
                            'derived_metric_name': metric_name,
                            'derived_metric_value': metric_value,
                            'evidence_quote': ''
                        })
                        
        except json.JSONDecodeError as e:
            print(f"Error processing {score_file.name}: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while processing {score_file.name}: {e}")
            continue
    
    # Write CSV
    if rows:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['document_id', 'dimension', 'raw_score', 'salience', 'confidence', 
                         'derived_metric_name', 'derived_metric_value', 'evidence_quote']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Exported {len(rows)} rows to {output_file}")
    else:
        print("No data found to export")


def main():
    parser = argparse.ArgumentParser(description='Export Discernus experiment data to CSV')
    parser.add_argument('experiment_path', help='Path to experiment directory')
    parser.add_argument('--output', '-o', default='export.csv', help='Output CSV file')
    
    args = parser.parse_args()
    extract_csv_data(args.experiment_path, args.output)


if __name__ == "__main__":
    main()
