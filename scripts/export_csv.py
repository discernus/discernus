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
    """Extract CSV data from analysis artifacts using smaller, more reliable files."""
    experiment_path = Path(experiment_path)
    
    # Find all the smaller, more reliable analysis files
    # Look in artifacts/analysis/ subdirectory if it exists, otherwise search recursively
    if (experiment_path / "artifacts" / "analysis").exists():
        score_files = list((experiment_path / "artifacts" / "analysis").glob("score_extraction_*.json"))
        evidence_files = list((experiment_path / "artifacts" / "analysis").glob("evidence_extraction_*.json"))
    else:
        score_files = list(experiment_path.glob("**/score_extraction_*.json"))
        evidence_files = list(experiment_path.glob("**/evidence_extraction_*.json"))
    
    if not score_files:
        print(f"No score_extraction files found in {experiment_path}")
        return
    
    # Separate data structures for document-level and dimension-level data
    document_rows = []  # One row per document with derived metrics
    dimension_rows = []  # One row per document-dimension with scores
    
    # Process score_extraction files for scores and metrics
    for score_file in score_files:
        try:
            with open(score_file, 'r') as f:
                data = json.load(f)
            
            # Extract document info from filename
            document_id = score_file.stem.replace('score_extraction_', '')
            
            # Parse the score_extraction response
            if 'score_extraction' in data:
                raw_response = data['score_extraction']
                # Handle both single and double quote markdown wrappers
                if raw_response.startswith('```json\n'):
                    raw_response = raw_response[7:]  # Remove ```json\n
                elif raw_response.startswith('```json'):
                    raw_response = raw_response[7:]  # Remove ```json
                if raw_response.endswith('\n```'):
                    raw_response = raw_response[:-4]  # Remove \n```
                elif raw_response.endswith('```'):
                    raw_response = raw_response[:-3]  # Remove ```
                
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
                
                # Create one document-level row with all derived metrics
                if derived_metrics:
                    doc_row = {'document_id': document_id}
                    doc_row.update(derived_metrics)
                    document_rows.append(doc_row)
                
                # Create dimension-level rows (one per dimension)
                for dimension, scores in dimensional_scores.items():
                    dimension_rows.append({
                        'document_id': document_id,
                        'dimension': dimension,
                        'raw_score': scores.get('raw_score'),
                        'salience': scores.get('salience'),
                        'confidence': scores.get('confidence')
                    })
                        
        except json.JSONDecodeError as e:
            print(f"Error processing {score_file.name}: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while processing {score_file.name}: {e}")
            continue
    
    # Process evidence_extraction files for evidence quotes
    evidence_rows = []  # Separate structure for evidence
    for evidence_file in evidence_files:
        try:
            with open(evidence_file, 'r') as f:
                data = json.load(f)
            
            # Extract document info from filename
            document_id = evidence_file.stem.replace('evidence_extraction_', '')
            
            # Parse the evidence_extraction response
            if 'evidence_extraction' in data:
                raw_response = data['evidence_extraction']
                
                try:
                    # Handle both old format (flat array) and new format (structured objects)
                    # First clean up any markdown formatting
                    if raw_response.startswith('```json\n'):
                        raw_response = raw_response[7:]  # Remove ```json\n
                    if raw_response.endswith('\n```'):
                        raw_response = raw_response[:-4]  # Remove \n```
                    
                    # Try to extract JSON array part (before any extra text)
                    bracket_count = 0
                    json_end = 0
                    for i, char in enumerate(raw_response):
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                json_end = i + 1
                                break
                    
                    if json_end > 0:
                        json_part = raw_response[:json_end]
                        evidence_quotes = json.loads(json_part)
                        
                        if isinstance(evidence_quotes, list):
                            # Check if it's the new structured format or old flat format
                            if evidence_quotes and isinstance(evidence_quotes[0], dict) and 'dimension' in evidence_quotes[0]:
                                # New structured format with dimension associations
                                for evidence_item in evidence_quotes:
                                    if evidence_item.get('quote', '').strip():
                                        evidence_rows.append({
                                            'document_id': document_id,
                                            'dimension': evidence_item.get('dimension', ''),
                                            'raw_score': evidence_item.get('raw_score', ''),
                                            'evidence_quote': evidence_item.get('quote', '')
                                        })
                            else:
                                # Old flat format - treat as dimension 'evidence'
                                for quote in evidence_quotes:
                                    if quote.strip():
                                        evidence_rows.append({
                                            'document_id': document_id,
                                            'dimension': 'evidence',
                                            'raw_score': '',
                                            'evidence_quote': quote
                                        })
                except json.JSONDecodeError as e:
                    print(f"Info: Could not parse evidence from {evidence_file.name}: {e}")
                    continue
                        
        except json.JSONDecodeError as e:
            print(f"Error processing {evidence_file.name}: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while processing {evidence_file.name}: {e}")
            continue
    
    # Write separate CSV files for different data structures
    base_path = Path(output_file)
    base_name = base_path.stem
    base_dir = base_path.parent
    
    files_written = 0
    
    # Write document-level data (derived metrics)
    if document_rows:
        doc_file = base_dir / f"{base_name}_documents.csv"
        with open(doc_file, 'w', newline='', encoding='utf-8') as f:
            if document_rows:
                fieldnames = ['document_id'] + list(document_rows[0].keys() - {'document_id'})
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(document_rows)
        print(f"Exported {len(document_rows)} document rows to {doc_file}")
        files_written += 1
    
    # Write dimension-level data (dimensional scores)
    if dimension_rows:
        dim_file = base_dir / f"{base_name}_dimensions.csv"
        with open(dim_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['document_id', 'dimension', 'raw_score', 'salience', 'confidence']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dimension_rows)
        print(f"Exported {len(dimension_rows)} dimension rows to {dim_file}")
        files_written += 1
    
    # Write evidence data
    if evidence_rows:
        ev_file = base_dir / f"{base_name}_evidence.csv"
        with open(ev_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['document_id', 'dimension', 'raw_score', 'evidence_quote']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(evidence_rows)
        print(f"Exported {len(evidence_rows)} evidence rows to {ev_file}")
        files_written += 1
    
    if files_written == 0:
        print("No data found to export")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Discernus experiment data to CSV.")
    parser.add_argument("experiment_path", help="Path to the experiment directory.")
    parser.add_argument("--output", "-o", default="export.csv", help="Output CSV file path.")
    args = parser.parse_args()
    
    extract_csv_data(args.experiment_path, args.output)