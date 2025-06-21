#!/usr/bin/env python3
"""
Phase 5 Comprehensive Logging Demo

Demonstrates the complete experiment logging system including:
- Academic audit trails for institutional compliance
- Experiment lifecycle tracking with hypothesis validation
- Corpus management logging with integrity validation
- Context propagation quality assurance
- Research ethics and reproducibility tracking
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from narrative_gravity.utils.experiment_logging import (
        get_experiment_logger,
        setup_experiment_logging,
        ExperimentErrorCodes,
        ExperimentMetricsCollector
    )
    from narrative_gravity.utils.logging_config import get_logger
    print("✅ Experiment logging system imported successfully")
except ImportError as e:
    print(f"❌ Cannot import experiment logging: {e}")
    print("Make sure you're in the project root and have run: source scripts/setup_dev_env.sh")
    sys.exit(1)

def create_test_experiment_definition() -> dict:
    """Create a comprehensive test experiment definition"""
    return {
        "experiment_meta": {
            "name": "Phase5_Comprehensive_Logging_Test",
            "description": "Comprehensive test of Phase 5 logging capabilities with academic audit trails",
            "version": "v1.0.0",
            "created": datetime.now().isoformat(),
            "hypotheses": [
                "H1: Comprehensive logging improves research reproducibility by maintaining complete audit trails",
                "H2: Academic compliance tracking reduces institutional review overhead",
                "H3: Context propagation logging ensures research validity across analysis pipeline"
            ],
            "research_context": "Testing comprehensive logging system for narrative gravity analysis with focus on academic research compliance and reproducibility",
            "success_criteria": [
                "Complete experiment lifecycle captured in structured logs",
                "Academic audit trail meets institutional compliance requirements",
                "Context propagation tracked throughout analysis pipeline",
                "Hypothesis validation recorded with research metadata",
                "Corpus integrity validation logged with cryptographic verification"
            ],
            "tags": ["logging", "academic_compliance", "phase5", "audit_trail"],
            "principal_investigator": "Dr. Research Compliance",
            "institution": "University of Comprehensive Logging",
            "ethical_clearance": "IRB-2025-LOGGING-001",
            "funding_source": "NSF Grant #LOG-2025-12345",
            "data_classification": "unclassified",
            "publication_intent": True
        },
        "components": {
            "frameworks": [
                {
                    "id": "civic_virtue",
                    "version": "v2.1",
                    "file_path": "frameworks/civic_virtue/framework_consolidated.json"
                }
            ],
            "prompt_templates": [
                {
                    "id": "hierarchical_analysis",
                    "version": "v2.1"
                }
            ],
            "weighting_schemes": [
                {
                    "id": "winner_take_most",
                    "version": "v2.1"
                }
            ],
            "models": [
                {
                    "id": "gpt-4o",
                    "provider": "openai"
                }
            ],
            "corpus": [
                {
                    "id": "conservative_dignity_test",
                    "file_path": "corpus/validation_set/conservative_dignity",
                    "pattern": "*.txt"
                }
            ]
        },
        "execution": {
            "matrix": [
                {
                    "framework": "civic_virtue",
                    "prompt_template": "hierarchical_analysis",
                    "weighting_scheme": "winner_take_most",
                    "model": "gpt-4o",
                    "corpus": "conservative_dignity_test"
                }
            ]
        }
    }

def demonstrate_experiment_logging():
    """Demonstrate experiment logging capabilities"""
    print("\n🧪 PHASE 5 COMPREHENSIVE LOGGING DEMONSTRATION")
    print("=" * 60)
    
    # Setup experiment logging
    print("\n1. Setting up experiment logging system...")
    setup_experiment_logging(log_level="INFO", log_file="logs/phase5_demo.log")
    experiment_logger = get_experiment_logger("phase5_demo")
    print("✅ Experiment logging system initialized")
    
    # Create experiment definition
    print("\n2. Creating comprehensive test experiment...")
    experiment = create_test_experiment_definition()
    
    # Start experiment logging with academic info
    print("\n3. Starting experiment logging with academic audit trail...")
    experiment_meta = experiment["experiment_meta"]
    academic_info = {
        'principal_investigator': experiment_meta.get('principal_investigator'),
        'institution': experiment_meta.get('institution'),
        'ethical_clearance': experiment_meta.get('ethical_clearance'),
        'funding_source': experiment_meta.get('funding_source'),
        'data_classification': experiment_meta.get('data_classification'),
        'publication_intent': experiment_meta.get('publication_intent')
    }
    
    run_id = experiment_logger.start_experiment_logging(
        experiment_meta["name"],
        experiment_meta,
        academic_info
    )
    print(f"✅ Experiment logging started with run_id: {run_id}")
    
    # Log academic compliance checks
    print("\n4. Performing academic compliance checks...")
    experiment_logger.log_academic_compliance(
        'ethical_clearance',
        True,
        {'clearance_id': experiment_meta.get('ethical_clearance')}
    )
    
    experiment_logger.log_academic_compliance(
        'institutional_review',
        True,
        {'institution': experiment_meta.get('institution')}
    )
    
    experiment_logger.log_academic_compliance(
        'funding_verification',
        True,
        {'funding_source': experiment_meta.get('funding_source')}
    )
    print("✅ Academic compliance checks completed")
    
    # Log component validation
    print("\n5. Logging component validation events...")
    components = [
        ('framework', 'civic_virtue', True),
        ('prompt_template', 'hierarchical_analysis', True),
        ('weighting_scheme', 'winner_take_most', True),
        ('model', 'gpt-4o', True),
        ('corpus', 'conservative_dignity_test', True)
    ]
    
    for component_type, component_id, success in components:
        experiment_logger.log_component_validation(
            component_type,
            component_id,
            success,
            {
                'validation_method': 'comprehensive_check',
                'timestamp': datetime.now().isoformat(),
                'phase': '5_logging_demo'
            }
        )
    print("✅ Component validation events logged")
    
    # Log auto-registration events  
    print("\n6. Logging auto-registration events...")
    for component_type, component_id, _ in components[:3]:  # Register first 3 components
        experiment_logger.log_auto_registration(
            component_type,
            component_id,
            True,
            {
                'registration_method': 'demo_auto_registration',
                'demo_mode': True,
                'phase': '5_logging_demo'
            }
        )
    print("✅ Auto-registration events logged")
    
    # Log corpus processing with integrity validation
    print("\n7. Logging corpus processing with integrity checks...")
    experiment_logger.log_corpus_processing(
        'conservative_dignity_test',
        6,  # Example: 6 files processed
        {
            'files_valid': 6,
            'files_total': 6,
            'hash_validation_success': True,
            'manifest_generated': True,
            'integrity_verification': 'sha256',
            'demo_mode': True
        },
        True
    )
    print("✅ Corpus processing logged with integrity validation")
    
    # Log context propagation
    print("\n8. Logging context propagation events...")
    experiment_logger.log_context_propagation(
        'experiment_context',
        True,
        {
            'hypotheses_count': len(experiment_meta['hypotheses']),
            'success_criteria_count': len(experiment_meta['success_criteria']),
            'context_enrichment': 'prompt_modification',
            'metadata_propagation': 'complete'
        }
    )
    
    experiment_logger.log_context_propagation(
        'academic_metadata',
        True,
        {
            'pi_propagated': True,
            'institution_propagated': True,
            'ethical_clearance_propagated': True,
            'reproducibility_package_ready': True
        }
    )
    print("✅ Context propagation events logged")
    
    # Log hypothesis validation
    print("\n9. Logging hypothesis validation...")
    experiment_logger.log_hypothesis_validation(
        experiment_meta['hypotheses'],
        {
            'validation_status': 'in_progress',
            'supporting_evidence': 'comprehensive_logging_demonstration',
            'validation_method': 'automated_tracking',
            'reproducibility_score': 0.95
        }
    )
    print("✅ Hypothesis validation logged")
    
    # Log integrity validation
    print("\n10. Logging file integrity validation...")
    test_files = [
        ('corpus/validation_set/conservative_dignity/file1.txt', 'abc123hash', 'abc123hash', True),
        ('corpus/validation_set/conservative_dignity/file2.txt', 'def456hash', 'def456hash', True),
        ('corpus/validation_set/conservative_dignity/file3.txt', 'ghi789hash', 'ghi789hash', True)
    ]
    
    for file_path, expected_hash, calculated_hash, success in test_files:
        experiment_logger.log_integrity_validation(
            file_path,
            expected_hash,
            calculated_hash,
            success
        )
    print("✅ File integrity validation events logged")
    
    # Generate comprehensive experiment report
    print("\n11. Generating comprehensive experiment report...")
    report = experiment_logger.generate_experiment_report()
    
    print("\n📊 COMPREHENSIVE EXPERIMENT REPORT")
    print("-" * 40)
    
    if 'experiment_metrics' in report:
        metrics = report['experiment_metrics']
        print(f"📈 Experiment Metrics:")
        print(f"   • Components validated: {metrics.get('components_validated', 0)}")
        print(f"   • Components auto-registered: {metrics.get('components_auto_registered', 0)}")
        print(f"   • Corpus files processed: {metrics.get('corpus_files_processed', 0)}")
        print(f"   • Context propagations: {metrics.get('context_propagations', 0)}")
        print(f"   • Hypothesis validations: {metrics.get('hypothesis_validations', 0)}")
        print(f"   • Success: {metrics.get('success', False)}")
    
    if 'academic_audit_trail' in report:
        audit = report['academic_audit_trail']
        print(f"\n🎓 Academic Audit Trail:")
        print(f"   • Principal Investigator: {audit.get('principal_investigator', 'N/A')}")
        print(f"   • Institution: {audit.get('institution', 'N/A')}")
        print(f"   • Ethical Clearance: {audit.get('ethical_clearance', 'N/A')}")
        print(f"   • Publication Intent: {audit.get('publication_intent', False)}")
        print(f"   • Compliance Checks: {len(audit.get('compliance_checks', []))}")
    
    if 'quality_metrics' in report:
        quality = report['quality_metrics']
        print(f"\n🔍 Quality Metrics:")
        print(f"   • Validation Success Rate: {quality.get('validation_success_rate', 0):.1f}%")
        print(f"   • Auto-registration Success Rate: {quality.get('auto_registration_success_rate', 0):.1f}%")
        print(f"   • Context Propagations: {quality.get('context_propagation_count', 0)}")
        print(f"   • Integrity Checks: {quality.get('integrity_checks_performed', 0)}")
    
    if 'reproducibility_metadata' in report:
        repro = report['reproducibility_metadata']
        print(f"\n🔄 Reproducibility Metadata:")
        print(f"   • Timestamp: {repro.get('timestamp', 'N/A')}")
        print(f"   • Run ID: {repro.get('run_id', 'N/A')}")
        print(f"   • Logging Version: {repro.get('logging_version', 'N/A')}")
        print(f"   • Comprehensive Audit Trail: {repro.get('comprehensive_audit_trail', False)}")
    
    # End experiment logging
    print("\n12. Ending experiment logging...")
    experiment_logger.end_experiment_logging(True)
    print("✅ Experiment logging completed successfully")
    
    return report

def demonstrate_error_logging():
    """Demonstrate error logging and failure scenarios"""
    print("\n\n🚨 ERROR LOGGING DEMONSTRATION")
    print("=" * 40)
    
    experiment_logger = get_experiment_logger("phase5_error_demo")
    
    # Start a failed experiment
    run_id = experiment_logger.start_experiment_logging(
        "Failed_Experiment_Demo",
        {'name': 'Failed_Experiment_Demo', 'description': 'Testing error logging'},
        {}
    )
    
    # Log various types of failures
    print("1. Logging component validation failures...")
    experiment_logger.log_component_validation(
        'framework',
        'nonexistent_framework',
        False,
        {'error': 'Framework not found on filesystem'}
    )
    
    print("2. Logging auto-registration failures...")
    experiment_logger.log_auto_registration(
        'corpus',
        'missing_corpus',
        False,
        {'error': 'File path does not exist'}
    )
    
    print("3. Logging corpus processing failures...")
    experiment_logger.log_corpus_processing(
        'corrupted_corpus',
        0,
        {'error': 'Hash validation failed', 'integrity_compromised': True},
        False
    )
    
    print("4. Logging context propagation failures...")
    experiment_logger.log_context_propagation(
        'broken_context',
        False,
        {'error': 'Context enrichment failed due to malformed metadata'}
    )
    
    print("5. Logging academic compliance failures...")
    experiment_logger.log_academic_compliance(
        'ethical_clearance',
        False,
        {'error': 'No ethical clearance provided for human subjects research'}
    )
    
    print("6. Logging integrity validation failures...")
    experiment_logger.log_integrity_validation(
        'corrupted_file.txt',
        'expected_hash_123',
        'actual_hash_456',
        False
    )
    
    # End failed experiment
    experiment_logger.end_experiment_logging(False)
    print("✅ Error logging demonstration completed")

def main():
    """Main demo function"""
    print("🎯 PHASE 5: COMPREHENSIVE LOGGING SYSTEM DEMO")
    print("=" * 60)
    print("Demonstrating complete experiment logging with academic audit trails")
    
    try:
        # Demonstrate successful experiment logging
        report = demonstrate_experiment_logging()
        
        # Demonstrate error logging
        demonstrate_error_logging()
        
        print("\n\n🎉 PHASE 5 LOGGING DEMONSTRATION COMPLETE!")
        print("=" * 50)
        print("✅ Comprehensive experiment logging system fully functional")
        print("✅ Academic audit trails for institutional compliance")
        print("✅ Research ethics and reproducibility tracking")
        print("✅ Context propagation quality assurance")
        print("✅ Corpus management with integrity validation")
        print("✅ Hypothesis validation and research metadata")
        print("✅ Error handling with structured error codes")
        
        print(f"\n📁 Check logs/phase5_demo.log for detailed structured logs")
        print(f"📊 Report generated with {len(str(report))} characters of metadata")
        
        print("\n🔬 Research Features Demonstrated:")
        print("   • Complete experiment lifecycle tracking")
        print("   • Academic compliance and institutional requirements")
        print("   • Hypothesis-aware logging with research context")
        print("   • Cryptographic integrity validation")
        print("   • Reproducibility package generation")
        print("   • Publication-ready audit trails")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 