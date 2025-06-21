#!/usr/bin/env python3
"""
Generate IDITI test data for enhanced analysis pipeline testing.
Based on the successful IDITI experiment log: 8/8 analyses, $0.0915 cost.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

def generate_iditi_test_data():
    """Generate test data based on the IDITI experiment log."""
    
    # Based on the experiment log data
    experiment_log = {
        "experiment_id": "iditi_validation_study_20250617",
        "experiment_name": "IDITI Framework Validation Study",
        "total_analyses": 8,
        "successful_analyses": 8,
        "total_cost": 0.0915,
        "framework": "iditi",
        "model": "gpt-4o"
    }
    
    # Categories from the experiment log
    categories = [
        "conservative_dignity",
        "conservative_tribalism", 
        "progressive_dignity",
        "progressive_tribalism",
        "extreme_controls",
        "extreme_controls", 
        "mixed_controls",
        "mixed_controls"
    ]
    
    # IDITI framework wells (Dignity and Tribalism)
    # Generate realistic scores based on categories
    structured_data = []
    
    for i in range(8):
        category = categories[i]
        
        # Generate scores based on category
        if "dignity" in category:
            dignity_score = 0.8 + (i * 0.02)  # 0.8-0.94
            tribalism_score = 0.2 + (i * 0.01)  # 0.2-0.27
        elif "tribalism" in category:
            dignity_score = 0.15 + (i * 0.01)  # 0.15-0.22
            tribalism_score = 0.85 + (i * 0.02)  # 0.85-0.99
        elif "extreme" in category:
            # Extreme controls - very high on one dimension
            if i == 4:  # First extreme
                dignity_score = 0.95
                tribalism_score = 0.05
            else:  # Second extreme
                dignity_score = 0.03
                tribalism_score = 0.97
        else:  # mixed controls
            # Balanced scores
            dignity_score = 0.45 + (i * 0.05)
            tribalism_score = 0.55 - (i * 0.05)
        
        record = {
            'run_id': f'iditi_run_{i+1}',
            'experiment_id': 'iditi_validation_study_20250617',
            'run_number': i + 1,
            'text_id': f'text_{i+1}',
            'framework': 'iditi',
            'model_name': 'gpt-4o',
            'success': True,
            'api_cost': 0.011 + (i * 0.001),  # Varies 0.011-0.018
            'duration_seconds': 28 + (i * 2),  # Varies 28-42 seconds
            'framework_fit_score': 0.85 + (i * 0.01),  # 0.85-0.92
            'narrative_x': (dignity_score - tribalism_score) * 0.5,  # Dignity-Tribalism axis
            'narrative_y': (dignity_score + tribalism_score - 1.0) * 0.3,  # Overall intensity
            'narrative_elevation': dignity_score + tribalism_score,
            'polarity': abs(dignity_score - tribalism_score),
            'coherence': 0.78 + (i * 0.02),
            'directional_purity': max(dignity_score, tribalism_score),
            'timestamp': f'2025-06-17T08:36:{str(i*4+1).zfill(2)}',
            'text_content': f'Sample text content for {category} analysis {i+1}',
            'input_length': 1200 + (i * 50),
            'category': category,
            # Well scores
            'well_dignity': dignity_score,
            'well_tribalism': tribalism_score
        }
        
        structured_data.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(structured_data)
    
    # Create output directory
    output_dir = Path('exports/analysis_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f'extracted_results_IDITI_Framework_Validation_Study_{timestamp}.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated IDITI test data: {len(df)} records")
    print(f"📁 Saved to: {output_path}")
    print(f"💰 Total cost: ${df['api_cost'].sum():.4f}")
    print(f"🎯 Categories: {df['category'].unique()}")
    print(f"🔧 Wells: Dignity (mean={df['well_dignity'].mean():.3f}), Tribalism (mean={df['well_tribalism'].mean():.3f})")
    
    # Also create execution results format for the enhanced analysis pipeline
    execution_results = {
        'experiment_name': experiment_log['experiment_name'],
        'total_analyses': experiment_log['total_analyses'], 
        'successful_analyses': experiment_log['successful_analyses'],
        'total_cost': experiment_log['total_cost'],
        'cost_efficiency': experiment_log['total_cost'] / experiment_log['successful_analyses'],
        'results': []
    }
    
    for _, row in df.iterrows():
        result = {
            'analysis_id': row['run_id'],
            'text_id': row['text_id'],
            'framework': row['framework'],
            'llm_model': row['model_name'],
            'success': row['success'],
            'api_cost': row['api_cost'],
            'duration_seconds': row['duration_seconds'],
            'framework_fit_score': row['framework_fit_score'],
            'well_scores': {
                'Dignity': row['well_dignity'],
                'Tribalism': row['well_tribalism']
            },
            'raw_scores': {
                'Dignity': row['well_dignity'],
                'Tribalism': row['well_tribalism']
            },
            'narrative_position_x': row['narrative_x'],
            'narrative_position_y': row['narrative_y'],
            'timestamp': row['timestamp']
        }
        execution_results['results'].append(result)
    
    # Save execution results format
    execution_path = output_dir / f'execution_results_IDITI_{timestamp}.json'
    with open(execution_path, 'w') as f:
        json.dump(execution_results, f, indent=2)
    
    print(f"📋 Execution results saved to: {execution_path}")
    
    return str(output_path), execution_results

def main():
    """Main execution function."""
    csv_path, execution_results = generate_iditi_test_data()
    print(f"\n🎯 Ready to test enhanced analysis pipeline with:")
    print(f"   CSV data: {csv_path}")
    print(f"   Mock execution results: {len(execution_results['results'])} analyses")

if __name__ == "__main__":
    main() 