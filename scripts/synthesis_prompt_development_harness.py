#!/usr/bin/env python3
"""
Synthesis Agent Prompt Development Harness
==========================================

A specialized harness for developing and testing enhanced synthesis prompts
using real experimental data from MVA Experiment 3.
"""

import sys
import os
from pathlib import Path
import json
import pandas as pd

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

def load_real_experimental_data():
    """Load actual data from MVA Experiment 3 for realistic testing."""
    try:
        # Use the most recent experimental results
        csv_path = project_root / "projects/MVA/experiments/experiment_3/results/2025-07-18_16-50-03/mva_results.csv"
        df = pd.read_csv(csv_path)
        
        # Convert to the structured format the SynthesisAgent expects
        structured_data = []
        for _, row in df.iterrows():
            record = {
                'corpus_file': row['corpus_file'],
                'run_num': row['run_num'],
                'tribal_dominance_score': row['tribal_dominance_score'],
                'individual_dignity_score': row['individual_dignity_score'],
                'fear_score': row['fear_score'],
                'hope_score': row['hope_score'],
                'envy_score': row['envy_score'],
                'compersion_score': row['compersion_score'],
                'enmity_score': row['enmity_score'],
                'amity_score': row['amity_score'],
                'fragmentative_goal_score': row['fragmentative_goal_score'],
                'cohesive_goal_score': row['cohesive_goal_score'],
                'descriptive_cohesion_index': row['descriptive_cohesion_index'],
                'motivational_cohesion_index': row['motivational_cohesion_index'],
                'full_cohesion_index': row['full_cohesion_index']
            }
            structured_data.append(record)
            
        print(f"✅ Loaded {len(structured_data)} experimental records")
        return structured_data
        
    except Exception as e:
        print(f"❌ Error loading experimental data: {e}")
        return None

def create_enhanced_synthesis_prompt(structured_data, experiment_info, framework_info):
    """Create the enhanced synthesis prompt for academic-quality reports."""
    
    data_summary = {
        'total_runs': len(structured_data),
        'unique_corpus_files': len(set(r['corpus_file'] for r in structured_data)),
        'corpus_files': list(set(r['corpus_file'] for r in structured_data))
    }
    
    prompt = f"""You are a computational social science researcher with expertise in statistical analysis and academic writing. You have access to a secure Python code execution environment with pandas, numpy, scipy, statsmodels, and pingouin libraries.

## EXPERIMENT CONTEXT
- Framework: {framework_info.get('display_name', 'CFF v4.1')}
- Total experimental runs: {data_summary['total_runs']}
- Unique corpus files: {data_summary['unique_corpus_files']}
- Analysis method: Independent anchor scoring (0.0-1.0 scale)

## HYPOTHESES TO TEST
H1: "At least two of the speeches will show statistically significant differences in CFI scores."
H2: "At least two of the speeches will show statistically significant similarities in CFI scores even though they express opposed progressive vs conservative worldviews."
H3: "Six-run analysis of each corpus file using Gemini 2.5 Pro will exhibit a Cronbach's alpha greater than 0.70 for inter-run reliability across all 10 CFF anchors."

## REAL EXPERIMENTAL DATA
```python
experimental_data = {str(structured_data)}
```

## YOUR TASK: Generate a Comprehensive Academic Report

You must write and execute Python code to produce a complete academic report matching this structure:

### 1. EXECUTIVE SUMMARY
- Brief overview of findings for each hypothesis
- Key statistical results summary
- Major insights about framework performance

### 2. STATISTICAL ANALYSIS
Write code to perform:
- **Hypothesis 1 (Differences)**: One-way ANOVA across corpus files for each dimension
- **Hypothesis 2 (Similarities)**: Identify opposing worldview speeches and test for equivalence
- **Hypothesis 3 (Reliability)**: Cronbach's alpha for each of the 10 CFF anchors across runs

### 3. RESULTS TABLES
Generate professional ASCII tables using the tabulate library:
- ANOVA results with F-statistics, p-values, and effect sizes
- Reliability analysis with Cronbach's alpha and 95% confidence intervals
- Descriptive statistics by corpus file

### 4. ACADEMIC INTERPRETATION
- Framework validation insights
- Construct validity assessment using reliability patterns
- Implications for computational discourse analysis

## CRITICAL REQUIREMENTS

1. **Execute Real Code**: Write actual Python that runs and produces results
2. **Use Only Provided Data**: No simulation or generation of additional data points
3. **Professional Formatting**: Use tabulate library for publication-ready tables
4. **Academic Tone**: Neutral, peer-review ready language
5. **Complete Analysis**: Address all three hypotheses with appropriate statistical tests
6. **Framework Validation**: Interpret results in terms of framework performance

## EXPECTED RESULTS
Based on CFF v4.1 independent anchor scoring, expect:
- F-statistics in range 1-10 for social science data
- Some non-significant differences (p > 0.05) showing discriminant validity
- Reliability coefficients (α) between 0.60-0.95 for different anchors
- Clear patterns distinguishing high vs. low performing framework dimensions

Begin by loading the experimental_data into a DataFrame and performing systematic hypothesis testing."""

    return prompt

def main():
    """Main function to test the enhanced synthesis prompt."""
    
    print("🔬 Synthesis Agent Prompt Development Harness")
    print("=" * 60)
    
    # Load real experimental data
    experimental_data = load_real_experimental_data()
    if not experimental_data:
        print("❌ Cannot proceed without experimental data")
        return
    
    # Create experiment and framework context
    experiment_info = {
        'name': 'MVA Experiment 3',
        'hypotheses': {
            'H1': 'At least two of the speeches will show statistically significant differences in CFI scores.',
            'H2': 'At least two of the speeches will show statistically significant similarities despite opposed worldviews.',
            'H3': 'Six-run analysis will exhibit Cronbach\'s alpha > 0.70 for inter-run reliability.'
        }
    }
    
    framework_info = {
        'display_name': 'Cohesive Flourishing Framework (CFF) v4.1',
        'method': 'Independent anchor scoring'
    }
    
    # Create the enhanced synthesis prompt
    synthesis_prompt = create_enhanced_synthesis_prompt(experimental_data, experiment_info, framework_info)
    
    # Configure model for testing
    model_name = "vertex_ai/gemini-2.5-pro"  # Use code execution capable model
    
    print(f"🚀 Testing enhanced synthesis prompt with {model_name}")
    print("=" * 60)
    print("PROMPT PREVIEW (first 500 chars):")
    print(synthesis_prompt[:500] + "...")
    print("=" * 60)
    
    # Execute with LLM Gateway
    try:
        model_registry = ModelRegistry()
        gateway = LLMGateway(model_registry)
        
        print(f"📡 Sending to {model_name}...")
        response, metadata = gateway.execute_call(
            model=model_name, 
            prompt=synthesis_prompt,
            system_prompt="You are an expert computational social science researcher with secure Python code execution capabilities.",
            temperature=0.3  # Lower temperature for accurate statistical analysis
        )
        
        print("\n" + "=" * 60)
        print("📊 SYNTHESIS REPORT GENERATED")
        print("=" * 60)
        print(response)
        
        print("\n" + "=" * 60)
        print("📈 METADATA")
        print("=" * 60)
        print(f"Success: {metadata.get('success', 'Unknown')}")
        print(f"Model: {metadata.get('model', 'Unknown')}")
        if 'usage' in metadata:
            print(f"Usage: {metadata['usage']}")
        
    except Exception as e:
        print(f"❌ Error executing synthesis prompt: {e}")

if __name__ == '__main__':
    main() 