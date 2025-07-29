#!/usr/bin/env python3
"""
Generate Sample Report

This script runs the complete THIN Code-Generated Synthesis Architecture
and saves the full report to a file for review.
"""

import sys
import os
import tempfile
import json
from datetime import datetime

# Add the prototype directory to path
sys.path.append(os.path.dirname(__file__))

from orchestration import ThinSynthesisPipeline
from orchestration.pipeline import PipelineRequest
from agents.code_executor import CodeExecutor

def create_comprehensive_framework():
    """Create a comprehensive framework for demonstration."""
    
    return """# Civic Character Assessment Framework (CAF) - Demonstration

## Overview
This framework assesses civic character through virtue and vice dimensions in political discourse, providing a systematic approach to evaluating the character traits exhibited in public communication.

## Analytical Dimensions

### Virtues (Positive Character Traits)
- **Integrity**: Consistency between stated values and actions, honesty in communication
- **Courage**: Willingness to take principled stands despite opposition or political cost  
- **Compassion**: Demonstrated concern for others' wellbeing, empathy in policy positions
- **Justice**: Commitment to fairness, equal treatment, and procedural fairness
- **Wisdom**: Sound judgment, long-term thinking, evidence-based decision making

### Vices (Negative Character Traits)  
- **Corruption**: Self-serving behavior at public expense, conflicts of interest
- **Cowardice**: Avoiding difficult decisions, failure to take principled stands
- **Cruelty**: Callousness toward others' suffering, harmful policy positions
- **Injustice**: Unfair treatment, discrimination, procedural violations
- **Folly**: Poor judgment, short-sighted thinking, ignoring evidence

## Research Hypotheses

### H1: Virtue Cluster Coherence
Virtue dimensions will demonstrate positive inter-correlations, forming a coherent psychological construct.

### H2: Vice Cluster Coherence
Vice dimensions will demonstrate positive inter-correlations, forming a coherent psychological construct.

### H3: Virtue-Vice Opposition  
Virtue and vice dimensions will demonstrate negative correlations, indicating they represent opposing character traits.

### H4: Overall Civic Character
The overall virtue score will significantly exceed the overall vice score, indicating net positive civic character in democratic discourse.

## Statistical Requirements

### Reliability Assessment
- Calculate Cronbach's alpha for virtue cluster (threshold: α ≥ 0.70)
- Calculate Cronbach's alpha for vice cluster (threshold: α ≥ 0.70)
- Report reliability implications for construct validity

### Correlation Analysis
- Generate correlation matrices for virtue and vice clusters separately
- Generate comprehensive correlation matrix including all dimensions
- Calculate overall virtue vs. overall vice correlation

### Hypothesis Testing
- Test H1-H4 using appropriate statistical methods
- Report p-values, confidence intervals, and effect sizes
- Use α = 0.05 significance level with Bonferroni correction where applicable

### Effect Size Analysis
- Calculate Cohen's d for significant mean differences
- Calculate η² (eta-squared) for ANOVA effects where applicable
- Interpret practical significance alongside statistical significance

## Expected Theoretical Outcomes
1. Strong internal consistency within virtue and vice clusters
2. Moderate to strong negative correlations between virtue and vice dimensions  
3. Overall virtue scores exceeding vice scores in democratic political discourse
4. Meaningful individual differences enabling character assessment
"""

def main():
    """Generate and save a complete sample report."""
    
    print("🎯 Generating Complete Sample Report")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = ThinSynthesisPipeline()
    executor = CodeExecutor()
    
    # Create temporary test data
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as scores_file:
        scores_path = scores_file.name
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as evidence_file:
        evidence_path = evidence_file.name
    
    try:
        # Generate synthetic data
        print("📊 Creating synthetic test data...")
        executor.create_test_data(scores_path, evidence_path, num_artifacts=30)
        
        # Create comprehensive framework
        framework_spec = create_comprehensive_framework()
        
        # Create pipeline request
        request = PipelineRequest(
            framework_spec=framework_spec,
            scores_csv_path=scores_path,
            evidence_csv_path=evidence_path,
            experiment_context="Demonstration of THIN Code-Generated Synthesis Architecture capabilities",
            max_evidence_per_finding=4,
            min_confidence_threshold=0.8,
            interpretation_focus="comprehensive"
        )
        
        # Run the complete pipeline
        print("🚀 Running THIN Code-Generated Synthesis Pipeline...")
        response = pipeline.run(request)
        
        if not response.success:
            print(f"❌ Pipeline failed: {response.error_message}")
            return 1
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"sample_synthesis_report_{timestamp}.md"
        
        # Save the complete report
        with open(report_filename, 'w') as f:
            f.write("# THIN Code-Generated Synthesis Architecture - Sample Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Pipeline Version:** 1.0.0-prototype\n")
            f.write(f"**Architecture:** THIN (Thick LLM + Thin Software)\n\n")
            
            f.write("## Pipeline Performance\n\n")
            f.write(f"- **Total Execution Time:** {response.total_execution_time:.2f} seconds\n")
            f.write(f"- **Report Length:** {response.word_count} words\n")
            f.write(f"- **Key Findings:** {len(response.key_findings)}\n\n")
            
            f.write("### Stage Performance\n\n")
            for stage, timing in response.stage_timings.items():
                success = "✅" if response.stage_success.get(stage, False) else "❌"
                f.write(f"- **{stage.replace('_', ' ').title()}:** {timing:.2f}s {success}\n")
            f.write("\n")
            
            f.write("## Complete Narrative Report\n\n")
            f.write(response.narrative_report)
            f.write("\n\n")
            
            f.write("## Key Findings Summary\n\n")
            for i, finding in enumerate(response.key_findings, 1):
                f.write(f"{i}. {finding}\n")
            f.write("\n")
            
            f.write("## Statistical Results\n\n")
            f.write("```json\n")
            f.write(json.dumps(response.statistical_results, indent=2))
            f.write("\n```\n\n")
            
            f.write("## Evidence Integration Summary\n\n")
            f.write("```json\n") 
            f.write(json.dumps(response.evidence_integration_summary, indent=2))
            f.write("\n```\n\n")
            
            f.write("## Generated Analysis Code\n\n")
            f.write("```python\n")
            f.write(response.generated_code)
            f.write("\n```\n\n")
            
            f.write("---\n\n")
            f.write("*This report was generated using the THIN Code-Generated Synthesis Architecture, ")
            f.write("a breakthrough approach that solves the fundamental scalability limitations of ")
            f.write("monolithic LLM synthesis through post-computation evidence curation and ")
            f.write("sequential focused processing.*\n")
        
        print(f"✅ Complete report saved to: {report_filename}")
        print(f"📊 Report contains {response.word_count} words")
        print(f"⏱️  Generated in {response.total_execution_time:.2f} seconds")
        
        # Also display the executive summary
        print("\n" + "="*60)
        print("EXECUTIVE SUMMARY")
        print("="*60)
        print(response.executive_summary)
        
        return 0
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(scores_path)
            os.unlink(evidence_path)
        except OSError:
            pass

if __name__ == "__main__":
    exit(main()) 