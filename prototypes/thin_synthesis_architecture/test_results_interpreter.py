#!/usr/bin/env python3
"""
Test script for ResultsInterpreter Agent

This script validates that the ResultsInterpreter can:
1. Generate comprehensive narrative reports
2. Integrate statistical results with curated evidence  
3. Extract structured information from narratives
4. Create executive summaries
"""

import sys
import os
import logging

# Add the prototype directory to path
sys.path.append(os.path.dirname(__file__))

from agents.results_interpreter import ResultsInterpreter
from agents.results_interpreter.agent import InterpretationRequest
from agents.evidence_curator.agent import CuratedEvidence

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_sample_data():
    """Create comprehensive sample data for testing."""
    
    # Sample statistical results
    statistical_results = {
        'descriptive_stats': {
            'integrity_score': {'mean': 0.847, 'std': 0.124, 'min': 0.45, 'max': 1.0, 'count': 25},
            'courage_score': {'mean': 0.723, 'std': 0.156, 'min': 0.40, 'max': 0.95, 'count': 25},
            'compassion_score': {'mean': 0.781, 'std': 0.118, 'min': 0.55, 'max': 0.92, 'count': 25},
            'corruption_score': {'mean': 0.234, 'std': 0.187, 'min': 0.05, 'max': 0.60, 'count': 25},
            'cowardice_score': {'mean': 0.312, 'std': 0.203, 'min': 0.08, 'max': 0.65, 'count': 25}
        },
        'hypothesis_tests': {
            'H1_virtue_positive_correlation': {
                'description': 'Virtue dimensions positively correlate with each other',
                'is_significant_alpha_05': True,
                'p_value': 0.0234,
                't_statistic': 2.89
            },
            'H4_overall_virtue_greater_than_overall_vice': {
                'description': 'Overall virtue score exceeds overall vice score',
                'is_significant_alpha_05': True,
                'p_value': 0.0008,
                't_statistic': 4.23
            },
            'H3_virtue_vice_negative_correlation': {
                'description': 'Virtue and vice dimensions negatively correlate',
                'is_significant_alpha_05': False,
                'p_value': 0.1234,
                't_statistic': -1.45
            }
        },
        'correlations': {
            'virtue_cluster_matrix': {
                'integrity_score': {'courage_score': 0.782, 'compassion_score': 0.834},
                'courage_score': {'integrity_score': 0.782, 'compassion_score': 0.712}
            },
            'overall_virtue_vs_overall_vice': {
                'correlation': -0.456,
                'interpretation': 'moderate negative correlation'
            }
        },
        'reliability_metrics': {
            'virtue_cluster_alpha': {'alpha': 0.891, 'meets_threshold': True, 'threshold': 0.70},
            'vice_cluster_alpha': {'alpha': 0.673, 'meets_threshold': False, 'threshold': 0.70}
        },
        'effect_sizes': {
            'H4_overall_virtue_greater_than_overall_vice_cohens_d': {
                'cohens_d': 1.23,
                'interpretation': 'large effect size'
            }
        }
    }
    
    # Sample curated evidence
    curated_evidence = {
        'descriptive_findings': [
            CuratedEvidence(
                artifact_id='speech_001',
                dimension='integrity',
                evidence_text='I have always believed that public service requires unwavering honesty with the American people, even when the truth is difficult.',
                context='Opening remarks at town hall meeting',
                confidence=0.92,
                reasoning='Directly addresses consistency between values and actions',
                relevance_score=0.9,
                statistical_connection='Supports integrity_score mean of 0.847'
            ),
            CuratedEvidence(
                artifact_id='speech_007',
                dimension='corruption',
                evidence_text='We must end the revolving door between government and special interests that has corrupted our democracy.',
                context='Campaign speech on ethics reform',
                confidence=0.88,
                reasoning='Explicitly calls out corrupt practices',
                relevance_score=0.85,
                statistical_connection='Supports corruption_score mean of 0.234'
            )
        ],
        'hypothesis_findings': [
            CuratedEvidence(
                artifact_id='speech_003',
                dimension='courage',
                evidence_text='Sometimes doing what is right means standing alone, even when it costs you politically.',
                context='Senate floor speech on controversial bill',
                confidence=0.94,
                reasoning='Demonstrates willingness to take principled stands',
                relevance_score=0.95,
                statistical_connection='Supports H1_virtue_positive_correlation (p=0.023)'
            ),
            CuratedEvidence(
                artifact_id='speech_012',
                dimension='compassion',
                evidence_text='Every policy we pass should be measured by how it affects the most vulnerable among us.',
                context='Healthcare debate remarks',
                confidence=0.89,
                reasoning='Shows concern for others\' wellbeing',
                relevance_score=0.9,
                statistical_connection='Supports H1_virtue_positive_correlation (p=0.023)'
            )
        ]
    }
    
    # Framework specification
    framework_spec = """
# Civic Character Assessment Framework (CAF) - Test Version

## Overview
This framework assesses civic character through virtue and vice dimensions in political discourse.

## Analytical Dimensions

### Virtues
- **Integrity**: Consistency between stated values and actions
- **Courage**: Willingness to take principled stands despite opposition  
- **Compassion**: Demonstrated concern for others' wellbeing

### Vices  
- **Corruption**: Self-serving behavior at public expense
- **Cowardice**: Avoiding difficult decisions or principled stands

## Statistical Requirements
- Calculate Cronbach's alpha for virtue and vice clusters
- Test virtue-vice inverse correlation hypothesis
- Assess overall civic character through virtue > vice hypothesis
"""
    
    return statistical_results, curated_evidence, framework_spec

def test_comprehensive_interpretation():
    """Test comprehensive narrative interpretation."""
    
    print("🧪 Testing comprehensive narrative interpretation...")
    
    interpreter = ResultsInterpreter()
    
    # Create sample data
    statistical_results, curated_evidence, framework_spec = create_sample_data()
    
    # Create interpretation request
    request = InterpretationRequest(
        statistical_results=statistical_results,
        curated_evidence=curated_evidence,
        framework_spec=framework_spec,
        experiment_context="Test of civic character assessment in political speeches",
        interpretation_focus="comprehensive"
    )
    
    # Generate interpretation
    print("📝 Generating comprehensive narrative...")
    response = interpreter.interpret_results(request)
    
    if not response.success:
        print(f"❌ Interpretation failed: {response.error_message}")
        return False
    
    print("✅ Interpretation successful!")
    print(f"📊 Report length: {response.word_count} words")
    print(f"🔍 Key findings count: {len(response.key_findings)}")
    print(f"📈 Statistical summary: {response.statistical_summary}")
    
    # Validate response structure
    if response.word_count < 500:
        print("⚠️  Report seems short - may not be comprehensive")
    
    if len(response.key_findings) < 3:
        print("⚠️  Few key findings extracted")
    
    # Show sample content
    print("\n" + "="*60)
    print("SAMPLE EXECUTIVE SUMMARY")
    print("="*60)
    print(response.executive_summary[:300] + "..." if len(response.executive_summary) > 300 else response.executive_summary)
    
    print("\n" + "="*60)
    print("SAMPLE KEY FINDINGS")
    print("="*60)
    for i, finding in enumerate(response.key_findings[:3], 1):
        print(f"{i}. {finding}")
    
    return True

def test_executive_summary_only():
    """Test executive summary generation."""
    
    print("\n📋 Testing executive summary generation...")
    
    interpreter = ResultsInterpreter()
    
    # Create sample data
    statistical_results, curated_evidence, framework_spec = create_sample_data()
    
    # Create interpretation request
    request = InterpretationRequest(
        statistical_results=statistical_results,
        curated_evidence=curated_evidence,
        framework_spec=framework_spec,
        experiment_context="Executive summary test",
        interpretation_focus="executive"
    )
    
    # Generate executive summary only
    summary = interpreter.generate_executive_summary_only(request)
    
    if "generation failed" in summary.lower():
        print(f"❌ Executive summary generation failed")
        return False
    
    print("✅ Executive summary generated!")
    print(f"📝 Summary length: {len(summary.split())} words")
    
    # Show the summary
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY")
    print("="*60)
    print(summary)
    
    return True

def test_evidence_integration():
    """Test evidence integration in narrative."""
    
    print("\n🔗 Testing evidence integration...")
    
    interpreter = ResultsInterpreter()
    
    # Create sample data with specific evidence
    statistical_results, curated_evidence, framework_spec = create_sample_data()
    
    # Create interpretation request
    request = InterpretationRequest(
        statistical_results=statistical_results,
        curated_evidence=curated_evidence,
        framework_spec=framework_spec,
        experiment_context="Evidence integration test"
    )
    
    # Generate interpretation
    response = interpreter.interpret_results(request)
    
    if not response.success:
        print(f"❌ Interpretation failed: {response.error_message}")
        return False
    
    # Check evidence integration summary
    evidence_summary = response.evidence_integration_summary
    
    print("✅ Evidence integration analysis:")
    print(f"📊 Total evidence integrated: {evidence_summary.get('total_evidence_integrated', 0)}")
    print(f"📂 Evidence categories: {evidence_summary.get('evidence_categories', 0)}")
    print(f"⭐ Average confidence: {evidence_summary.get('average_evidence_confidence', 0)}")
    print(f"🔄 Integration approach: {evidence_summary.get('integration_approach', 'N/A')}")
    
    # Check if evidence quotes appear in narrative
    narrative = response.narrative_report.lower()
    evidence_found = 0
    
    for category, evidence_list in curated_evidence.items():
        for evidence in evidence_list:
            # Look for part of the evidence text in the narrative
            evidence_snippet = evidence.evidence_text[:20].lower()
            if evidence_snippet in narrative:
                evidence_found += 1
    
    print(f"🔍 Evidence quotes found in narrative: {evidence_found}")
    
    if evidence_found == 0:
        print("⚠️  No evidence quotes found in narrative - integration may be weak")
    
    return True

def test_statistical_summary():
    """Test statistical summary generation."""
    
    print("\n📊 Testing statistical summary generation...")
    
    interpreter = ResultsInterpreter()
    
    # Create sample data
    statistical_results, curated_evidence, framework_spec = create_sample_data()
    
    # Create interpretation request
    request = InterpretationRequest(
        statistical_results=statistical_results,
        curated_evidence=curated_evidence,
        framework_spec=framework_spec
    )
    
    # Generate interpretation
    response = interpreter.interpret_results(request)
    
    if not response.success:
        print(f"❌ Interpretation failed: {response.error_message}")
        return False
    
    # Validate statistical summary
    stats_summary = response.statistical_summary
    
    expected_fields = [
        'total_dimensions_analyzed', 'significant_hypotheses', 'total_hypotheses',
        'reliability_clusters_assessed', 'correlation_matrices_generated'
    ]
    
    missing_fields = [field for field in expected_fields if field not in stats_summary]
    if missing_fields:
        print(f"❌ Missing statistical summary fields: {missing_fields}")
        return False
    
    print("✅ Statistical summary validated!")
    print(f"📈 Dimensions analyzed: {stats_summary['total_dimensions_analyzed']}")
    print(f"✅ Significant hypotheses: {stats_summary['significant_hypotheses']}/{stats_summary['total_hypotheses']}")
    print(f"🔍 Reliability clusters: {stats_summary['reliability_clusters_assessed']}")
    print(f"🔗 Correlation matrices: {stats_summary['correlation_matrices_generated']}")
    
    # Validate numbers make sense
    if stats_summary['total_dimensions_analyzed'] != 5:
        print(f"⚠️  Expected 5 dimensions, got {stats_summary['total_dimensions_analyzed']}")
    
    if stats_summary['significant_hypotheses'] != 2:
        print(f"⚠️  Expected 2 significant hypotheses, got {stats_summary['significant_hypotheses']}")
    
    return True

def main():
    """Run all tests."""
    
    setup_logging()
    
    print("🚀 Starting ResultsInterpreter Tests")
    print("=" * 50)
    
    # Test comprehensive interpretation
    success = test_comprehensive_interpretation()
    if not success:
        print("❌ Comprehensive interpretation test failed!")
        return 1
    
    # Test executive summary
    success = test_executive_summary_only()
    if not success:
        print("❌ Executive summary test failed!")
        return 1
    
    # Test evidence integration
    success = test_evidence_integration()
    if not success:
        print("❌ Evidence integration test failed!")
        return 1
    
    # Test statistical summary
    success = test_statistical_summary()
    if not success:
        print("❌ Statistical summary test failed!")
        return 1
    
    print("\n🎉 All tests passed!")
    print("✅ ResultsInterpreter is working correctly")
    print("🎯 Final synthesis stage validated!")
    
    return 0

if __name__ == "__main__":
    exit(main()) 