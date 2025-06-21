#!/usr/bin/env python3
"""
Generate Multi-LLM Test Data for Reliability Analysis

Creates realistic test data simulating analyses from multiple LLM providers
to demonstrate the enhanced analysis pipeline's multi-LLM reliability capabilities.

Based on the successful IDITI framework: 2 wells (Dignity, Tribalism)
Simulates 3 LLMs × 8 texts × 3 replications = 72 total analyses
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random

def generate_multi_llm_reliability_data():
    """Generate comprehensive multi-LLM reliability test data."""
    
    # Configuration based on IDITI multi-LLM validation spec
    experiment_config = {
        "experiment_id": "iditi_multi_llm_reliability_study",
        "experiment_name": "IDITI Multi-LLM Reliability Validation",
        "total_analyses": 72,  # 3 LLMs × 8 texts × 3 replications
        "llm_providers": ["gpt-4o", "claude-3-5-sonnet", "gemini-2.0-flash"],
        "framework": "iditi",
        "wells": ["Dignity", "Tribalism"]
    }
    
    # Text categories from IDITI validation study
    text_categories = [
        {"id": "reagan_1986_challenger", "category": "conservative_dignity", "expected_dignity": 0.85, "expected_tribalism": 0.20},
        {"id": "aoc_2025_rally", "category": "progressive_tribalism", "expected_dignity": 0.25, "expected_tribalism": 0.80},
        {"id": "obama_2004_dnc", "category": "progressive_dignity", "expected_dignity": 0.80, "expected_tribalism": 0.25},
        {"id": "john_lewis_1963", "category": "progressive_dignity", "expected_dignity": 0.85, "expected_tribalism": 0.15},
        {"id": "mccain_concession_2008", "category": "conservative_dignity", "expected_dignity": 0.80, "expected_tribalism": 0.20},
        {"id": "progressive_balanced", "category": "mixed_controls", "expected_dignity": 0.50, "expected_tribalism": 0.50},
        {"id": "conservative_balanced", "category": "mixed_controls", "expected_dignity": 0.55, "expected_tribalism": 0.45},
        {"id": "extreme_dignity_control", "category": "extreme_controls", "expected_dignity": 0.95, "expected_tribalism": 0.05},
    ]
    
    # LLM characteristics (simulate realistic differences)
    llm_characteristics = {
        "gpt-4o": {
            "dignity_bias": 0.02,  # Slight tendency to score dignity higher
            "tribalism_bias": -0.01,
            "consistency": 0.95,  # High consistency
            "cost_per_analysis": 0.015,
            "avg_duration": 8.5
        },
        "claude-3-5-sonnet": {
            "dignity_bias": -0.01,  # Slight tendency to score dignity lower
            "tribalism_bias": 0.02,
            "consistency": 0.92,  # High consistency
            "cost_per_analysis": 0.018,
            "avg_duration": 12.3
        },
        "gemini-2.0-flash": {
            "dignity_bias": 0.00,  # Most neutral
            "tribalism_bias": 0.01,
            "consistency": 0.88,  # Slightly less consistent
            "cost_per_analysis": 0.008,
            "avg_duration": 6.2
        }
    }
    
    # Generate structured data
    structured_data = []
    analysis_id = 1
    base_time = datetime.now() - timedelta(hours=2)
    
    for text in text_categories:
        for llm_provider in experiment_config["llm_providers"]:
            for replication in range(1, 4):  # 3 replications per LLM per text
                
                # Get LLM characteristics
                llm_char = llm_characteristics[llm_provider]
                
                # Calculate scores with realistic variation
                dignity_base = text["expected_dignity"]
                tribalism_base = text["expected_tribalism"]
                
                # Add LLM-specific bias
                dignity_score = dignity_base + llm_char["dignity_bias"]
                tribalism_score = tribalism_base + llm_char["tribalism_bias"]
                
                # Add random variation based on consistency
                dignity_variation = np.random.normal(0, (1 - llm_char["consistency"]) * 0.1)
                tribalism_variation = np.random.normal(0, (1 - llm_char["consistency"]) * 0.1)
                
                dignity_score = max(0, min(1, dignity_score + dignity_variation))
                tribalism_score = max(0, min(1, tribalism_score + tribalism_variation))
                
                # Ensure scores don't exceed 1.0 when combined
                total = dignity_score + tribalism_score
                if total > 1.0:
                    dignity_score = dignity_score / total
                    tribalism_score = tribalism_score / total
                
                # Calculate derived metrics
                narrative_x = (dignity_score - tribalism_score) * 0.6
                narrative_y = (dignity_score + tribalism_score - 1.0) * 0.4
                
                # Add some cost and duration variation
                cost_variation = np.random.uniform(0.8, 1.2)
                duration_variation = np.random.uniform(0.7, 1.4)
                
                analysis_time = base_time + timedelta(minutes=analysis_id * 2)
                
                record = {
                    'run_id': f'multi_llm_run_{analysis_id}',
                    'experiment_id': 'iditi_multi_llm_reliability_study',
                    'run_number': analysis_id,
                    'text_id': text["id"],
                    'framework': 'iditi',
                    'model_name': llm_provider,
                    'replication_number': replication,
                    'success': True,
                    'api_cost': llm_char["cost_per_analysis"] * cost_variation,
                    'duration_seconds': llm_char["avg_duration"] * duration_variation,
                    'framework_fit_score': 0.85 + np.random.uniform(-0.1, 0.1),
                    'narrative_x': narrative_x,
                    'narrative_y': narrative_y,
                    'narrative_elevation': dignity_score + tribalism_score,
                    'polarity': abs(dignity_score - tribalism_score),
                    'coherence': 0.78 + np.random.uniform(-0.05, 0.15),
                    'directional_purity': max(dignity_score, tribalism_score),
                    'timestamp': analysis_time.isoformat(),
                    'text_content': f'Sample text content for {text["id"]} analysis',
                    'input_length': 1200 + random.randint(-200, 400),
                    'category': text["category"],
                    'expected_dignity': text["expected_dignity"],
                    'expected_tribalism': text["expected_tribalism"],
                    # Well scores
                    'well_dignity': dignity_score,
                    'well_tribalism': tribalism_score
                }
                
                structured_data.append(record)
                analysis_id += 1
    
    # Convert to DataFrame
    df = pd.DataFrame(structured_data)
    
    # Create output directory
    output_dir = Path('exports/analysis_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f'multi_llm_reliability_study_{timestamp}.csv'
    df.to_csv(output_path, index=False)
    
    # Calculate summary statistics
    summary_stats = {
        'total_analyses': len(df),
        'llm_providers': df['model_name'].nunique(),
        'unique_texts': df['text_id'].nunique(),
        'replications_per_text_per_llm': df.groupby(['text_id', 'model_name']).size().iloc[0],
        'total_cost': df['api_cost'].sum(),
        'avg_dignity_score': df['well_dignity'].mean(),
        'avg_tribalism_score': df['well_tribalism'].mean(),
        'dignity_std': df['well_dignity'].std(),
        'tribalism_std': df['well_tribalism'].std()
    }
    
    # LLM comparison statistics
    llm_stats = df.groupby('model_name').agg({
        'well_dignity': ['mean', 'std'],
        'well_tribalism': ['mean', 'std'],
        'api_cost': 'sum',
        'duration_seconds': 'mean'
    }).round(4)
    
    print(f"✅ Generated multi-LLM reliability data: {len(df)} analyses")
    print(f"📁 Saved to: {output_path}")
    print(f"🎯 LLM Providers: {list(df['model_name'].unique())}")
    print(f"📝 Text Categories: {list(df['category'].unique())}")
    print(f"💰 Total Cost: ${summary_stats['total_cost']:.4f}")
    print(f"🔄 Replications: {summary_stats['replications_per_text_per_llm']} per text per LLM")
    
    print(f"\n📊 LLM Comparison Summary:")
    for llm in df['model_name'].unique():
        llm_data = df[df['model_name'] == llm]
        dignity_mean = llm_data['well_dignity'].mean()
        tribalism_mean = llm_data['well_tribalism'].mean()
        cost_total = llm_data['api_cost'].sum()
        print(f"  {llm}:")
        print(f"    Dignity: {dignity_mean:.3f} ± {llm_data['well_dignity'].std():.3f}")
        print(f"    Tribalism: {tribalism_mean:.3f} ± {llm_data['well_tribalism'].std():.3f}")
        print(f"    Cost: ${cost_total:.4f}")
    
    # Create execution results format for enhanced analysis pipeline
    execution_results = {
        'experiment_name': experiment_config['experiment_name'],
        'total_analyses': experiment_config['total_analyses'],
        'successful_analyses': len(df),
        'failed_analyses': 0,
        'total_cost': summary_stats['total_cost'],
        'cost_efficiency': summary_stats['total_cost'] / len(df),
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
            'timestamp': row['timestamp'],
            'replication_number': row['replication_number']
        }
        execution_results['results'].append(result)
    
    # Save execution results format
    execution_path = output_dir / f'multi_llm_execution_results_{timestamp}.json'
    with open(execution_path, 'w') as f:
        json.dump(execution_results, f, indent=2)
    
    print(f"📋 Execution results saved to: {execution_path}")
    
    return str(output_path), execution_results, summary_stats

def main():
    """Main execution function."""
    csv_path, execution_results, summary_stats = generate_multi_llm_reliability_data()
    
    print(f"\n🎯 Ready for enhanced multi-LLM reliability analysis:")
    print(f"   CSV data: {csv_path}")
    print(f"   Mock execution results: {len(execution_results['results'])} analyses")
    print(f"   LLM Providers: {summary_stats['llm_providers']}")
    print(f"   Total Cost: ${summary_stats['total_cost']:.4f}")
    print(f"\n💡 Next step: Run enhanced analysis pipeline to test multi-LLM reliability:")
    print(f"   python3 scripts/test_enhanced_analysis_pipeline.py")

if __name__ == "__main__":
    main() 