#!/usr/bin/env python3
"""
Demo script for Phase 4 Context Propagation

Tests the ExperimentContext and context-enriched prompt functionality.
"""

import json
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the orchestrator
from comprehensive_experiment_orchestrator import ExperimentOrchestrator, ExperimentContext

def demo_context_creation():
    """Demo experiment context creation and functionality"""
    print("🚀 PHASE 4 CONTEXT PROPAGATION DEMO")
    print("=" * 50)
    
    # Create a sample experiment context
    context = ExperimentContext(
        name="Demo Context Propagation Study",
        description="Testing hypothesis-aware analysis with context propagation",
        version="v1.0.0",
        created="2025-06-16",
        hypotheses=[
            "Context-enriched prompts improve analysis quality",
            "Experimental metadata propagates through pipeline",
            "Hypothesis validation can be tracked systematically"
        ],
        research_context="Demo study for Phase 4 context propagation validation",
        success_criteria=[
            "Context extracted successfully",
            "Prompts enriched with experimental information",
            "Analysis metadata includes context"
        ],
        tags=["demo", "phase4", "context_propagation"],
        principal_investigator="AI Research Assistant",
        institution="Narrative Gravity Research Platform"
    )
    
    print("📊 EXPERIMENT CONTEXT CREATED:")
    print(context.generate_context_summary())
    print()
    
    return context

def demo_prompt_enrichment(context):
    """Demo context-enriched prompt generation"""
    print("✨ PROMPT ENRICHMENT DEMO:")
    print("-" * 30)
    
    # Sample base prompt
    base_prompt = """Analyze the following text using the specified framework.

TEXT TO ANALYZE:
{text_content}

Provide scores (0.0-1.0) for each framework well with supporting evidence."""
    
    # Sample analysis run information
    analysis_run_info = {
        'framework': 'iditi',
        'corpus_item': 'dignity_test_single',
        'prompt_template': 'hierarchical_analysis',
        'weighting_scheme': 'hierarchical_weighted',
        'model': 'gpt-4o-mini'
    }
    
    # Create orchestrator and set context
    orchestrator = ExperimentOrchestrator()
    orchestrator.experiment_context = context
    
    # Generate enriched prompt
    enriched_prompt = orchestrator.create_context_enriched_prompt(base_prompt, analysis_run_info)
    
    print("🔍 BASE PROMPT:")
    print(base_prompt[:200] + "..." if len(base_prompt) > 200 else base_prompt)
    print()
    
    print("🎯 CONTEXT-ENRICHED PROMPT:")
    print(enriched_prompt[:500] + "..." if len(enriched_prompt) > 500 else enriched_prompt)
    print()
    
    return enriched_prompt

def demo_metadata_generation(context):
    """Demo analysis metadata generation"""
    print("📋 METADATA GENERATION DEMO:")
    print("-" * 30)
    
    orchestrator = ExperimentOrchestrator()
    orchestrator.experiment_context = context
    
    # Sample analysis run info
    analysis_run_info = {
        'framework': 'iditi',
        'corpus_item': 'dignity_test_single',
        'prompt_template': 'hierarchical_analysis',
        'weighting_scheme': 'hierarchical_weighted',
        'model': 'gpt-4o-mini'
    }
    
    # Generate metadata
    metadata = orchestrator.prepare_analysis_metadata(analysis_run_info)
    
    print("📊 ANALYSIS METADATA:")
    print(json.dumps(metadata, indent=2))
    print()
    
    return metadata

def demo_context_aware_output(context):
    """Demo context-aware output generation"""
    print("📈 CONTEXT-AWARE OUTPUT DEMO:")
    print("-" * 30)
    
    orchestrator = ExperimentOrchestrator()
    orchestrator.experiment_context = context
    
    # Sample analysis results
    analysis_results = {
        'text_id': 'reagan_speech_1986',
        'framework': 'iditi',
        'analysis_timestamp': '2025-06-16T20:03:00',
        'wells_analysis': {
            'dignity': 0.82,
            'tribalism': 0.15
        },
        'center_of_mass': {'x': 0.075, 'y': 0.766},
        'narrative_distance': 0.770
    }
    
    # Sample analysis run info
    analysis_run_info = {
        'framework': 'iditi',
        'corpus_item': 'dignity_test_single',
        'model': 'gpt-4o-mini'
    }
    
    # Generate context-aware output
    enriched_output = orchestrator.generate_context_aware_output(analysis_results, analysis_run_info)
    
    print("📊 CONTEXT-AWARE OUTPUT STRUCTURE:")
    for key in enriched_output.keys():
        if key in ['experiment_context', 'analysis_run_context', 'hypothesis_validation', 'academic_metadata']:
            print(f"  ✅ {key}: {type(enriched_output[key]).__name__}")
        else:
            print(f"  📄 {key}: {type(enriched_output[key]).__name__}")
    print()
    
    print("🎯 HYPOTHESIS VALIDATION SECTION:")
    print(json.dumps(enriched_output['hypothesis_validation'], indent=2))
    print()
    
    return enriched_output

def demo_validation_report(context):
    """Demo validation report generation"""
    print("📋 VALIDATION REPORT DEMO:")
    print("-" * 30)
    
    orchestrator = ExperimentOrchestrator()
    orchestrator.experiment_context = context
    
    # Sample results list
    all_results = [
        {'experiment_context': {'experiment_name': 'Demo Study'}, 'academic_metadata': {}, 'hypothesis_validation': {}},
        {'experiment_context': {'experiment_name': 'Demo Study'}, 'academic_metadata': {}, 'hypothesis_validation': {}},
        {'experiment_context': {'experiment_name': 'Demo Study'}, 'academic_metadata': {}, 'hypothesis_validation': {}}
    ]
    
    # Generate validation report
    report = orchestrator.create_validation_report(all_results)
    
    print("📊 VALIDATION REPORT STRUCTURE:")
    for key in report.keys():
        print(f"  📈 {key}: {type(report[key]).__name__}")
    print()
    
    print("🎯 HYPOTHESIS SUMMARY:")
    print(json.dumps(report['hypothesis_summary'], indent=2))
    print()
    
    print("📊 CONTEXT PROPAGATION STATS:")
    print(json.dumps(report['context_propagation_stats'], indent=2))
    print()
    
    return report

def main():
    """Run the complete Phase 4 demo"""
    try:
        # Demo 1: Context Creation
        context = demo_context_creation()
        print()
        
        # Demo 2: Prompt Enrichment
        enriched_prompt = demo_prompt_enrichment(context)
        print()
        
        # Demo 3: Metadata Generation
        metadata = demo_metadata_generation(context)
        print()
        
        # Demo 4: Context-Aware Output
        enriched_output = demo_context_aware_output(context)
        print()
        
        # Demo 5: Validation Report
        report = demo_validation_report(context)
        
        print("🎉 PHASE 4 CONTEXT PROPAGATION DEMO COMPLETE!")
        print("=" * 50)
        print("✅ All context propagation features working successfully")
        print("✅ Experiment context preserved throughout pipeline")
        print("✅ Hypothesis tracking integrated into analysis workflow")
        print("✅ Academic metadata prepared for publication-ready exports")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 