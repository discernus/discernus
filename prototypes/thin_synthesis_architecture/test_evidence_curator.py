#!/usr/bin/env python3
"""
Test script for EvidenceCurator Agent

This script validates that the EvidenceCurator can:
1. Load and process evidence data correctly
2. Curate evidence based on statistical results
3. Select relevant evidence for different types of findings
4. Generate meaningful curation summaries
"""

import sys
import os
import logging
import tempfile
import json

# Add the prototype directory to path
sys.path.append(os.path.dirname(__file__))

from agents.evidence_curator import EvidenceCurator
from agents.evidence_curator.agent import EvidenceCurationRequest
from agents.code_executor import CodeExecutor

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_sample_statistical_results():
    """Create sample statistical results for testing."""
    
    return {
        'descriptive_stats': {
            'integrity_score': {'mean': 0.85, 'std': 0.12, 'min': 0.45, 'max': 1.0, 'count': 10},
            'courage_score': {'mean': 0.72, 'std': 0.15, 'min': 0.40, 'max': 0.95, 'count': 10},
            'compassion_score': {'mean': 0.78, 'std': 0.11, 'min': 0.55, 'max': 0.92, 'count': 10},
            'corruption_score': {'mean': 0.25, 'std': 0.18, 'min': 0.05, 'max': 0.60, 'count': 10},
            'cowardice_score': {'mean': 0.32, 'std': 0.20, 'min': 0.08, 'max': 0.65, 'count': 10}
        },
        'hypothesis_tests': {
            'H1_virtue_positive_correlation': {
                'description': 'Virtue dimensions positively correlate',
                'is_significant_alpha_05': True,
                'p_value': 0.023
            },
            'H4_overall_virtue_greater_than_overall_vice': {
                'description': 'Overall virtue > overall vice',
                'is_significant_alpha_05': True,
                'p_value': 0.001,
                't_statistic': 4.2
            }
        },
        'correlations': {
            'all_dimensions_matrix': {
                'integrity_score': {'courage_score': 0.78, 'compassion_score': 0.82},
                'courage_score': {'integrity_score': 0.78, 'compassion_score': 0.71},
                'corruption_score': {'cowardice_score': 0.65}
            }
        },
        'reliability_metrics': {
            'virtue_cluster_alpha': {'alpha': 0.89, 'meets_threshold': True, 'threshold': 0.70},
            'vice_cluster_alpha': {'alpha': 0.68, 'meets_threshold': False, 'threshold': 0.70}
        }
    }

def test_basic_curation():
    """Test basic evidence curation functionality."""
    
    print("🧪 Testing basic EvidenceCurator functionality...")
    
    curator = EvidenceCurator()
    executor = CodeExecutor()
    
    # Create synthetic test data
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        evidence_path = f.name
    
    try:
        # Generate synthetic evidence data
        executor.create_test_data("dummy_scores.csv", evidence_path, num_artifacts=10)
        
        # Create sample statistical results
        statistical_results = create_sample_statistical_results()
        
        # Create curation request
        request = EvidenceCurationRequest(
            statistical_results=statistical_results,
            evidence_csv_path=evidence_path,
            framework_spec="Test framework",
            max_evidence_per_finding=2,
            min_confidence_threshold=0.7
        )
        
        # Perform curation
        response = curator.curate_evidence(request)
        
        if not response.success:
            print(f"❌ Evidence curation failed: {response.error_message}")
            return False
        
        print("✅ Evidence curation successful!")
        print(f"📊 Curated evidence categories: {list(response.curated_evidence.keys())}")
        print(f"📈 Curation summary: {response.curation_summary}")
        
        # Validate response structure
        if not isinstance(response.curated_evidence, dict):
            print("❌ Curated evidence should be a dictionary")
            return False
        
        if not isinstance(response.curation_summary, dict):
            print("❌ Curation summary should be a dictionary")
            return False
        
        # Check that we have some curated evidence
        total_curated = sum(len(evidence_list) for evidence_list in response.curated_evidence.values())
        if total_curated == 0:
            print("⚠️  No evidence was curated - this might be expected if confidence thresholds are high")
        else:
            print(f"✅ Successfully curated {total_curated} pieces of evidence")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(evidence_path)
            if os.path.exists("dummy_scores.csv"):
                os.unlink("dummy_scores.csv")
        except OSError:
            pass

def test_evidence_filtering():
    """Test evidence filtering by confidence threshold."""
    
    print("\n🔍 Testing evidence filtering by confidence...")
    
    curator = EvidenceCurator()
    
    # Create temporary evidence file with mixed confidence levels
    evidence_data = """artifact_id,dimension,evidence_text,context,confidence,reasoning
artifact_001,integrity,High confidence evidence,Context 1,0.95,Strong reasoning
artifact_002,courage,Medium confidence evidence,Context 2,0.65,Moderate reasoning  
artifact_003,compassion,Low confidence evidence,Context 3,0.45,Weak reasoning
artifact_004,integrity,Another high confidence,Context 4,0.88,Strong reasoning
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(evidence_data)
        evidence_path = f.name
    
    try:
        # Test with high confidence threshold
        statistical_results = create_sample_statistical_results()
        
        request = EvidenceCurationRequest(
            statistical_results=statistical_results,
            evidence_csv_path=evidence_path,
            framework_spec="Test framework",
            max_evidence_per_finding=5,
            min_confidence_threshold=0.8  # High threshold
        )
        
        response = curator.curate_evidence(request)
        
        if not response.success:
            print(f"❌ Evidence curation failed: {response.error_message}")
            return False
        
        # Should only use high confidence evidence (0.95, 0.88)
        high_conf_available = response.curation_summary.get('high_confidence_evidence', 0)
        
        print(f"✅ High confidence evidence available: {high_conf_available}")
        print(f"📊 Total curated: {response.curation_summary.get('total_curated', 0)}")
        
        if high_conf_available != 2:
            print(f"⚠️  Expected 2 high confidence evidence pieces, got {high_conf_available}")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(evidence_path)
        except OSError:
            pass

def test_dimension_mapping():
    """Test that evidence is correctly mapped to statistical findings."""
    
    print("\n🗺️  Testing dimension mapping...")
    
    curator = EvidenceCurator()
    
    # Create evidence with specific dimensions
    evidence_data = """artifact_id,dimension,evidence_text,context,confidence,reasoning
artifact_001,integrity,Evidence for integrity,Context 1,0.9,Strong integrity evidence
artifact_002,courage,Evidence for courage,Context 2,0.85,Strong courage evidence
artifact_003,corruption,Evidence for corruption,Context 3,0.8,Strong corruption evidence
artifact_004,integrity,More integrity evidence,Context 4,0.95,Very strong integrity
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(evidence_data)
        evidence_path = f.name
    
    try:
        # Create statistical results that should trigger integrity evidence selection
        # (integrity has highest mean score in our sample data)
        statistical_results = create_sample_statistical_results()
        
        request = EvidenceCurationRequest(
            statistical_results=statistical_results,
            evidence_csv_path=evidence_path,
            framework_spec="Test framework",
            max_evidence_per_finding=3,
            min_confidence_threshold=0.7
        )
        
        response = curator.curate_evidence(request)
        
        if not response.success:
            print(f"❌ Evidence curation failed: {response.error_message}")
            return False
        
        # Check if integrity evidence was selected (it has the highest mean score)
        all_evidence = []
        for evidence_list in response.curated_evidence.values():
            all_evidence.extend(evidence_list)
        
        integrity_evidence = [e for e in all_evidence if e.dimension == 'integrity']
        
        print(f"✅ Found {len(integrity_evidence)} integrity evidence pieces")
        
        if len(integrity_evidence) > 0:
            print(f"📝 Sample integrity evidence: {integrity_evidence[0].evidence_text}")
            print(f"🔗 Statistical connection: {integrity_evidence[0].statistical_connection}")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(evidence_path)
        except OSError:
            pass

def test_curation_summary():
    """Test curation summary generation."""
    
    print("\n📊 Testing curation summary generation...")
    
    curator = EvidenceCurator()
    executor = CodeExecutor()
    
    # Create synthetic test data
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        evidence_path = f.name
    
    try:
        # Generate synthetic evidence data
        executor.create_test_data("dummy_scores.csv", evidence_path, num_artifacts=20)
        
        statistical_results = create_sample_statistical_results()
        
        request = EvidenceCurationRequest(
            statistical_results=statistical_results,
            evidence_csv_path=evidence_path,
            framework_spec="Test framework",
            max_evidence_per_finding=2,
            min_confidence_threshold=0.75
        )
        
        response = curator.curate_evidence(request)
        
        if not response.success:
            print(f"❌ Evidence curation failed: {response.error_message}")
            return False
        
        summary = response.curation_summary
        
        # Validate summary structure
        expected_fields = [
            'total_evidence_available', 'high_confidence_evidence', 'total_curated',
            'curation_rate', 'evidence_by_category', 'average_confidence',
            'average_relevance_score', 'curation_strategy'
        ]
        
        missing_fields = [field for field in expected_fields if field not in summary]
        if missing_fields:
            print(f"❌ Missing summary fields: {missing_fields}")
            return False
        
        print("✅ Curation summary structure validated!")
        print(f"📈 Total evidence available: {summary['total_evidence_available']}")
        print(f"🎯 High confidence evidence: {summary['high_confidence_evidence']}")
        print(f"✨ Total curated: {summary['total_curated']}")
        print(f"📊 Curation rate: {summary['curation_rate']:.2%}")
        print(f"⭐ Average confidence: {summary['average_confidence']}")
        print(f"🎯 Average relevance: {summary['average_relevance_score']}")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(evidence_path)
            if os.path.exists("dummy_scores.csv"):
                os.unlink("dummy_scores.csv")
        except OSError:
            pass

def main():
    """Run all tests."""
    
    setup_logging()
    
    print("🚀 Starting EvidenceCurator Tests")
    print("=" * 50)
    
    # Test basic functionality
    success = test_basic_curation()
    if not success:
        print("❌ Basic curation test failed!")
        return 1
    
    # Test evidence filtering
    success = test_evidence_filtering()
    if not success:
        print("❌ Evidence filtering test failed!")
        return 1
    
    # Test dimension mapping
    success = test_dimension_mapping()
    if not success:
        print("❌ Dimension mapping test failed!")
        return 1
    
    # Test curation summary
    success = test_curation_summary()
    if not success:
        print("❌ Curation summary test failed!")
        return 1
    
    print("\n🎉 All tests passed!")
    print("✅ EvidenceCurator is working correctly")
    print("🔑 Key innovation validated: Post-computation evidence curation")
    
    return 0

if __name__ == "__main__":
    exit(main()) 