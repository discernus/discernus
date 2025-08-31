#!/usr/bin/env python3
"""
Analyze the quality of extracted DOCX data
"""

import json
import pandas as pd
from pathlib import Path

def analyze_json_data(json_path: str):
    """Analyze the JSON data to understand quality and patterns."""
    print("Analyzing extracted JSON data...")
    print("=" * 50)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total scoring sheets: {len(data)}")
    
    # Analyze metadata completeness
    metadata_fields = ['politician', 'speech_title', 'speech_date', 'grader', 'grading_date', 'category']
    metadata_completeness = {}
    
    for field in metadata_fields:
        non_empty = sum(1 for sheet in data if sheet['metadata'].get(field, '').strip())
        metadata_completeness[field] = {
            'filled': non_empty,
            'empty': len(data) - non_empty,
            'percentage': (non_empty / len(data)) * 100
        }
    
    print("\nMetadata Completeness:")
    for field, stats in metadata_completeness.items():
        print(f"  {field}: {stats['filled']}/{len(data)} ({stats['percentage']:.1f}%)")
    
    # Analyze scoring patterns
    print("\nScoring Analysis:")
    manichaean_scores = []
    people_scores = []
    elite_scores = []
    final_grades = []
    
    for sheet in data:
        for dim in sheet['dimensions']:
            if 'manichaean' in dim['name'].lower():
                manichaean_scores.append(dim['score'])
            elif 'people' in dim['name'].lower():
                people_scores.append(dim['score'])
            elif 'elite' in dim['name'].lower():
                elite_scores.append(dim['score'])
        
        if sheet['final_grade'] is not None:
            final_grades.append(sheet['final_grade'])
    
    print(f"  Manichaean vision scores: {len(manichaean_scores)}")
    if manichaean_scores:
        print(f"    Range: {min(manichaean_scores)} - {max(manichaean_scores)}")
        print(f"    Average: {sum(manichaean_scores)/len(manichaean_scores):.2f}")
        print(f"    Distribution: {sorted(set(manichaean_scores))}")
    
    print(f"  People notion scores: {len(people_scores)}")
    if people_scores:
        print(f"    Range: {min(people_scores)} - {max(people_scores)}")
        print(f"    Average: {sum(people_scores)/len(people_scores):.2f}")
        print(f"    Distribution: {sorted(set(people_scores))}")
    
    print(f"  Evil elite scores: {len(elite_scores)}")
    if elite_scores:
        print(f"    Range: {min(elite_scores)} - {max(elite_scores)}")
        print(f"    Average: {sum(elite_scores)/len(elite_scores):.2f}")
        print(f"    Distribution: {sorted(set(elite_scores))}")
    
    print(f"  Final grades: {len(final_grades)}")
    if final_grades:
        print(f"    Range: {min(final_grades)} - {max(final_grades)}")
        print(f"    Average: {sum(final_grades)/len(final_grades):.2f}")
        print(f"    Distribution: {sorted(set(final_grades))}")
    
    # Check for scoring anomalies
    print("\nScoring Anomalies:")
    anomaly_count = 0
    for i, sheet in enumerate(data):
        for dim in sheet['dimensions']:
            if dim['score'] > 2:  # Van der Veen uses 0-2 scale
                print(f"  Sheet {i+1} ({sheet['metadata'].get('politician', 'Unknown')}): {dim['name']} = {dim['score']}")
                anomaly_count += 1
    
    if anomaly_count == 0:
        print("  No scoring anomalies detected")
    
    # Analyze examples extraction
    print("\nExamples Analysis:")
    total_examples = 0
    sheets_with_examples = 0
    for sheet in data:
        for dim in sheet['dimensions']:
            total_examples += len(dim['examples'])
            if dim['examples']:
                sheets_with_examples += 1
                break
    
    print(f"  Total examples extracted: {total_examples}")
    print(f"  Sheets with examples: {sheets_with_examples}/{len(data)}")
    
    # Show sample of raw content
    print("\nSample Raw Content (first 200 chars):")
    if data:
        sample = data[0]['raw_content'][:200]
        print(f"  {sample}...")

def analyze_csv_data(csv_path: str):
    """Analyze the CSV data to understand quality and patterns."""
    print("\nAnalyzing extracted CSV data...")
    print("=" * 50)
    
    try:
        df = pd.read_csv(csv_path)
        print(f"CSV shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print("\nMissing values per column:")
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                print(f"  {col}: {missing}/{len(df)} ({missing/len(df)*100:.1f}%)")
        
        # Show sample data
        print("\nFirst few rows:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"Error reading CSV: {e}")

def main():
    json_path = "enhanced_training_data.json"
    csv_path = "enhanced_training_data.csv"
    
    if Path(json_path).exists():
        analyze_json_data(json_path)
    else:
        print(f"JSON file not found: {json_path}")
    
    if Path(csv_path).exists():
        analyze_csv_data(csv_path)
    else:
        print(f"CSV file not found: {csv_path}")

if __name__ == "__main__":
    main()
