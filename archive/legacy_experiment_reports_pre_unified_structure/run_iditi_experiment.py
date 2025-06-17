#!/usr/bin/env python3
"""
IDITI Framework Validation Study
Direct execution script for the three-hypothesis validation experiment
"""

import json
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular
from narrative_gravity.framework_manager import FrameworkManager

class IDITIValidationExperiment:
    """IDITI Framework Validation Study Executor"""
    
    def __init__(self):
        self.framework_manager = FrameworkManager()
        self.results = []
        self.experiment_id = f"iditi_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def load_validation_corpus(self, corpus_file: str) -> List[Dict[str, Any]]:
        """Load the validation corpus from JSONL file."""
        texts = []
        with open(corpus_file, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                texts.append(data)
        return texts
    
    def categorize_text(self, filename: str) -> str:
        """Categorize text based on filename."""
        if 'dignity_control' in filename:
            return 'extreme_dignity'
        elif 'tribalism_control' in filename:
            return 'extreme_tribalism'
        elif 'balanced' in filename:
            return 'mixed_control'
        elif any(name in filename for name in ['john_mccain', 'larry_hogan', 'mitt_romney', 'rick_perry', 'ronald_reagan', 'tillis_coons']):
            return 'conservative_dignity'
        elif any(name in filename for name in ['glenn_beck', 'steve_king', 'trump_nh', 'vance_nat_con']):
            return 'conservative_tribalism'
        elif any(name in filename for name in ['cory_booker', 'elizabeth_warren', 'john_lewis', 'obama', 'tishaura_jones']):
            return 'progressive_dignity'
        elif any(name in filename for name in ['aoc', 'barron', 'bernie_sanders', 'diangelo', 'ibram_x_kendi', 'malcom_x']):
            return 'progressive_tribalism'
        else:
            return 'unknown'
    
    async def analyze_single_text(self, text_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single text with the IDITI framework."""
        try:
            # Initialize the engine with IDITI framework
            engine = NarrativeGravityWellsCircular(
                config_dir="../frameworks/iditi"
            )
            
            # Run the analysis
            result = await engine.analyze_text(text_data['text'])
            
            # Extract key metrics
            analysis_result = {
                'text_id': text_data.get('text_id', 'unknown'),
                'filename': text_data.get('source_file', 'unknown'),
                'category': self.categorize_text(text_data.get('source_file', '')),
                'dignity_score': result.get('wells', {}).get('Dignity', 0.0),
                'tribalism_score': result.get('wells', {}).get('Tribalism', 0.0),
                'narrative_polarity': result.get('nps', 0.0),
                'center_of_mass': result.get('com', [0.0, 0.0]),
                'coherence': result.get('coherence', 0.0),
                'framework_fit': result.get('framework_fit_score', 0.0),
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'raw_result': result
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                'text_id': text_data.get('text_id', 'unknown'),
                'filename': text_data.get('source_file', 'unknown'),
                'category': self.categorize_text(text_data.get('source_file', '')),
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    async def run_experiment(self, corpus_file: str, output_dir: str):
        """Run the complete IDITI validation experiment."""
        print(f"🎯 Starting IDITI Framework Validation Study")
        print(f"   Experiment ID: {self.experiment_id}")
        
        # Load corpus
        texts = self.load_validation_corpus(corpus_file)
        print(f"   Loaded {len(texts)} texts for analysis")
        
        # Create output directory
        output_path = Path(output_dir) / self.experiment_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Run analyses
        results = []
        for i, text_data in enumerate(texts):
            print(f"   Analyzing text {i+1}/{len(texts)}: {text_data.get('source_file', 'unknown')}")
            result = await self.analyze_single_text(text_data)
            results.append(result)
            
            # Save intermediate results
            if (i + 1) % 10 == 0:
                self.save_intermediate_results(results, output_path)
        
        # Save final results
        self.save_final_results(results, output_path)
        
        # Generate analysis report
        self.generate_validation_report(results, output_path)
        
        print(f"✅ Experiment complete! Results saved to: {output_path}")
        
        return results
    
    def save_intermediate_results(self, results: List[Dict], output_path: Path):
        """Save intermediate results."""
        with open(output_path / "intermediate_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    def save_final_results(self, results: List[Dict], output_path: Path):
        """Save final results in multiple formats."""
        # JSON format
        with open(output_path / "final_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # CSV format for analysis
        df = pd.DataFrame([r for r in results if r.get('success', False)])
        df.to_csv(output_path / "results.csv", index=False)
        
        print(f"   Saved results: {len(results)} total, {len(df)} successful")
    
    def generate_validation_report(self, results: List[Dict], output_path: Path):
        """Generate validation report for the three hypotheses."""
        successful_results = [r for r in results if r.get('success', False)]
        
        if not successful_results:
            print("❌ No successful results to analyze")
            return
        
        df = pd.DataFrame(successful_results)
        
        report = {
            'experiment_id': self.experiment_id,
            'timestamp': datetime.now().isoformat(),
            'total_texts': len(results),
            'successful_analyses': len(successful_results),
            'success_rate': len(successful_results) / len(results),
            'hypotheses_validation': {}
        }
        
        # Hypothesis 1: Discriminative Validity
        dignity_texts = df[df['category'].str.contains('dignity', na=False)]
        tribalism_texts = df[df['category'].str.contains('tribalism', na=False)]
        mixed_texts = df[df['category'].str.contains('mixed', na=False)]
        
        report['hypotheses_validation']['hypothesis_1_discriminative_validity'] = {
            'dignity_texts_count': len(dignity_texts),
            'dignity_avg_dignity_score': dignity_texts['dignity_score'].mean() if len(dignity_texts) > 0 else 0,
            'dignity_avg_tribalism_score': dignity_texts['tribalism_score'].mean() if len(dignity_texts) > 0 else 0,
            'tribalism_texts_count': len(tribalism_texts),
            'tribalism_avg_dignity_score': tribalism_texts['dignity_score'].mean() if len(tribalism_texts) > 0 else 0,
            'tribalism_avg_tribalism_score': tribalism_texts['tribalism_score'].mean() if len(tribalism_texts) > 0 else 0,
            'mixed_texts_count': len(mixed_texts),
            'mixed_avg_dignity_score': mixed_texts['dignity_score'].mean() if len(mixed_texts) > 0 else 0,
            'mixed_avg_tribalism_score': mixed_texts['tribalism_score'].mean() if len(mixed_texts) > 0 else 0
        }
        
        # Hypothesis 2: Ideological Agnosticism
        conservative_dignity = df[df['category'] == 'conservative_dignity']
        progressive_dignity = df[df['category'] == 'progressive_dignity']
        conservative_tribalism = df[df['category'] == 'conservative_tribalism']
        progressive_tribalism = df[df['category'] == 'progressive_tribalism']
        
        report['hypotheses_validation']['hypothesis_2_ideological_agnosticism'] = {
            'conservative_dignity_avg_dignity': conservative_dignity['dignity_score'].mean() if len(conservative_dignity) > 0 else 0,
            'progressive_dignity_avg_dignity': progressive_dignity['dignity_score'].mean() if len(progressive_dignity) > 0 else 0,
            'conservative_tribalism_avg_tribalism': conservative_tribalism['tribalism_score'].mean() if len(conservative_tribalism) > 0 else 0,
            'progressive_tribalism_avg_tribalism': progressive_tribalism['tribalism_score'].mean() if len(progressive_tribalism) > 0 else 0
        }
        
        # Hypothesis 3: Ground Truth Alignment
        extreme_controls = df[df['category'].str.contains('extreme', na=False)]
        report['hypotheses_validation']['hypothesis_3_ground_truth_alignment'] = {
            'extreme_controls_count': len(extreme_controls),
            'extreme_controls_avg_coherence': extreme_controls['coherence'].mean() if len(extreme_controls) > 0 else 0,
            'extreme_controls_avg_framework_fit': extreme_controls['framework_fit'].mean() if len(extreme_controls) > 0 else 0
        }
        
        # Save report
        with open(output_path / "validation_report.json", 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   Generated validation report with {len(successful_results)} successful analyses")


async def main():
    """Main execution function."""
    experiment = IDITIValidationExperiment()
    
    corpus_file = "experiment_reports/iditi_validation_corpus.jsonl"
    output_dir = "experiment_reports"
    
    if not Path(corpus_file).exists():
        print(f"❌ Corpus file not found: {corpus_file}")
        return 1
    
    try:
        results = await experiment.run_experiment(corpus_file, output_dir)
        print(f"🎉 Experiment completed successfully!")
        return 0
    except Exception as e:
        print(f"❌ Experiment failed: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main())) 