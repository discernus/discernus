#!/usr/bin/env python3
"""
Transaction Integrity Architecture Demonstration

Shows how the multi-layered transaction management system works:
- Framework Transaction Manager
- Data Transaction Manager  
- Quality Transaction Manager

Any uncertainty that could compromise experiment validity triggers graceful
termination with rollback and specific user guidance.
"""

import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from src.utils.framework_transaction_manager import (
        FrameworkTransactionManager
    )
    from src.utils.data_transaction_manager import (
        DataTransactionManager,
        DataValidationResult
    )
    from src.utils.quality_transaction_manager import (
        QualityTransactionManager,
        QualityThresholds,
        QualityValidationResult
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please ensure you're running from the project root directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TransactionIntegrityError(Exception):
    """Base exception for transaction integrity failures"""
    def __init__(self, domain: str, errors: List[str], guidance: Dict[str, Any]):
        self.domain = domain
        self.errors = errors
        self.guidance = guidance
        super().__init__(f"Transaction integrity failure in {domain}: {', '.join(errors)}")

class TransactionIntegrityDemo:
    """
    🔒 TRANSACTION INTEGRITY DEMONSTRATION
    
    Shows multi-layered validation and graceful failure with rollback
    """
    
    def __init__(self):
        self.transaction_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"\n🔒 Transaction Integrity Architecture Demo")
        print(f"Transaction ID: {self.transaction_id}")
        print("=" * 60)
    
    def demonstrate_framework_validation(self) -> bool:
        """Demonstrate Framework Transaction Manager"""
        print(f"\n🔍 Phase 1: Framework Transaction Validation")
        print("-" * 40)
        
        try:
            # Initialize framework transaction manager
            framework_manager = FrameworkTransactionManager(self.transaction_id)
            
            # Validate framework for experiment
            framework_context = {
                'framework_name': 'iditi',
                'framework_version': 'v1.0.0',
                'expected_wells': 2
            }
            
            print(f"✅ Validating framework: iditi v1.0.0")
            framework_manager.validate_for_experiment(framework_context)
            
            # Check transaction validity
            is_valid, errors = framework_manager.is_transaction_valid()
            
            if is_valid:
                print(f"✅ Framework validation PASSED")
                return True
            else:
                print(f"❌ Framework validation FAILED: {', '.join(errors)}")
                guidance = framework_manager.generate_rollback_guidance()
                self._print_guidance("Framework", guidance)
                return False
                
        except Exception as e:
            print(f"❌ Framework validation ERROR: {e}")
            return False
    
    def demonstrate_data_validation(self) -> bool:
        """Demonstrate Data Transaction Manager"""
        print(f"\n🔍 Phase 2: Data Transaction Validation")
        print("-" * 40)
        
        try:
            # Initialize data transaction manager
            data_manager = DataTransactionManager(self.transaction_id)
            
            # Create sample corpus specifications
            corpus_specs = [
                {
                    'id': 'demo_text_1',
                    'file_path': 'corpus/demo_texts/demo_text_1.txt',
                    'content_hash': None  # Will be calculated
                },
                {
                    'id': 'demo_text_2', 
                    'file_path': 'corpus/demo_texts/demo_text_2.txt',
                    'content_hash': None
                }
            ]
            
            print(f"✅ Validating {len(corpus_specs)} corpus files")
            
            # Validate corpus data
            validation_states = data_manager.validate_corpus_for_experiment(corpus_specs)
            
            # Validate database schema
            schema_state = data_manager.validate_database_schema()
            
            # Check transaction validity
            is_valid, errors = data_manager.is_transaction_valid()
            
            if is_valid:
                print(f"✅ Data validation PASSED")
                
                # Show validation details
                valid_files = [s for s in validation_states if s.validation_result == DataValidationResult.VALID]
                print(f"   📄 Validated {len(valid_files)} files successfully")
                
                for state in valid_files:
                    print(f"   ✅ {os.path.basename(state.file_path)}: {state.file_size} bytes, {state.encoding}")
                
                return True
            else:
                print(f"❌ Data validation FAILED: {', '.join(errors[:3])}...")
                guidance = data_manager.generate_rollback_guidance()
                self._print_guidance("Data", guidance)
                return False
                
        except Exception as e:
            print(f"❌ Data validation ERROR: {e}")
            return False
    
    def demonstrate_quality_validation(self) -> bool:
        """Demonstrate Quality Transaction Manager"""
        print(f"\n🔍 Phase 3: Quality Transaction Validation")
        print("-" * 40)
        
        try:
            # Initialize quality transaction manager with stricter thresholds
            thresholds = QualityThresholds(
                min_framework_fit_score=0.75,
                min_statistical_power=0.80,
                min_sample_size=5,  # Lowered for demo
                max_coefficient_variation=0.25
            )
            
            quality_manager = QualityTransactionManager(self.transaction_id, thresholds)
            
            # Create mock analysis results for demonstration
            analysis_results = self._create_mock_analysis_results()
            
            print(f"✅ Validating analysis quality thresholds")
            
            # Validate framework fit scores
            quality_manager.validate_framework_fit_scores(analysis_results)
            
            # Validate statistical significance  
            quality_manager.validate_statistical_significance(analysis_results)
            
            # Validate analysis variance
            quality_manager.validate_analysis_variance(analysis_results)
            
            # Mock LLM responses for quality validation
            llm_responses = [
                {
                    'content': 'This text demonstrates clear dignity-focused rhetoric with respectful discourse and substantive policy discussion. The author maintains professional tone while addressing complex issues with nuanced analysis.',
                    'model': 'gpt-4',
                    'response_time': 2.3
                },
                {
                    'content': 'Strong tribalistic elements present with us-versus-them framing and emotional appeals rather than policy substance.',
                    'model': 'gpt-4', 
                    'response_time': 1.8
                }
            ]
            
            # Validate LLM response quality
            quality_manager.validate_llm_response_quality(llm_responses)
            
            # Check transaction validity
            is_valid, errors = quality_manager.is_transaction_valid()
            
            if is_valid:
                print(f"✅ Quality validation PASSED")
                
                # Show quality metrics
                valid_checks = [s for s in quality_manager.transaction_states 
                              if s.validation_result == QualityValidationResult.VALID]
                print(f"   📊 Passed {len(valid_checks)} quality checks")
                
                return True
            else:
                print(f"❌ Quality validation FAILED: {', '.join(errors[:2])}...")
                guidance = quality_manager.generate_rollback_guidance()
                self._print_guidance("Quality", guidance)
                return False
                
        except Exception as e:
            print(f"❌ Quality validation ERROR: {e}")
            return False
    
    def demonstrate_transaction_coordination(self):
        """Demonstrate coordinated transaction management"""
        print(f"\n🔒 Transaction Coordination Demo")
        print("=" * 60)
        
        # Run all validation phases
        framework_valid = self.demonstrate_framework_validation()
        data_valid = self.demonstrate_data_validation() 
        quality_valid = self.demonstrate_quality_validation()
        
        # Overall transaction result
        print(f"\n🎯 TRANSACTION INTEGRITY RESULT")
        print("-" * 40)
        
        all_valid = framework_valid and data_valid and quality_valid
        
        if all_valid:
            print(f"✅ EXPERIMENT APPROVED - All transaction validations passed")
            print(f"   🔒 Framework integrity: VALID")
            print(f"   🔒 Data integrity: VALID") 
            print(f"   🔒 Quality integrity: VALID")
            print(f"\n🚀 Experiment can proceed with confidence")
            
        else:
            print(f"🚨 EXPERIMENT TERMINATED - Transaction integrity failure")
            print(f"   🔒 Framework integrity: {'VALID' if framework_valid else 'FAILED'}")
            print(f"   🔒 Data integrity: {'VALID' if data_valid else 'FAILED'}")
            print(f"   🔒 Quality integrity: {'VALID' if quality_valid else 'FAILED'}")
            print(f"\n🔄 Complete rollback initiated")
            print(f"💡 User guidance provided for each failure domain")
            
        return all_valid
    
    def demonstrate_failure_scenario(self):
        """Demonstrate transaction failure with detailed guidance"""
        print(f"\n💥 FAILURE SCENARIO DEMONSTRATION")
        print("=" * 60)
        print("Simulating experiment with intentional integrity violations...")
        
        # Simulate framework failure
        print(f"\n🔍 Simulating Framework Failure")
        print("-" * 40)
        print(f"❌ Framework 'invalid_framework' not found in database")
        print(f"🔄 Rolling back framework transaction...")
        
        # Mock guidance output
        print(f"\n🔧 FRAMEWORK FAILURE GUIDANCE:")
        print(f"   • Verify framework exists: python3 scripts/list_frameworks.py")
        print(f"   • Check framework status: python3 scripts/framework_sync.py status")
        print(f"   • Import framework: python3 scripts/framework_sync.py import")
        
        print(f"\n🚨 EXPERIMENT TERMINATION COMPLETE")
        print(f"   Transaction ID: {self.transaction_id}")
        print(f"   Failure Type: Framework Transaction Integrity Error")
        print(f"   Recovery: Follow guidance above to resolve framework issues")
        print(f"   Retry: Re-run experiment after addressing failures")
    
    def _create_mock_analysis_results(self) -> Dict[str, Any]:
        """Create mock analysis results for quality validation demo"""
        return {
            'framework_fit_score': 0.82,  # Above 0.75 threshold
            'well_fit_scores': {
                'Dignity': 0.78,
                'Tribalism': 0.86
            },
            'p_values': {
                'correlation_test': 0.023,  # Below 0.05 threshold (good)
                'significance_test': 0.041
            },
            'confidence_intervals': {
                'dignity_score': {
                    'width': 0.15,  # Below 0.2 threshold (good)
                    'lower': 0.42,
                    'upper': 0.57
                }
            },
            'sample_size': 8,  # Above 5 threshold (good)
            'variance_analysis': {
                'dignity_variance': {
                    'coefficient_of_variation': 0.18,  # Below 0.25 threshold (good)
                    'mean': 0.65,
                    'std_dev': 0.12
                }
            },
            'statistics': {
                'mean': 0.58,
                'std_dev': 0.11
            }
        }
    
    def _print_guidance(self, domain: str, guidance: Dict[str, Any]):
        """Print formatted guidance for transaction failures"""
        print(f"\n🔧 {domain.upper()} FAILURE GUIDANCE:")
        
        if guidance.get('recommendations'):
            for i, rec in enumerate(guidance['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        if guidance.get('commands_to_run'):
            print(f"\n💻 Recommended commands:")
            for cmd in guidance['commands_to_run'][:3]:  # Show first 3
                print(f"   {cmd}")

def main():
    """Run transaction integrity demonstration"""
    print("🔒 NARRATIVE GRAVITY TRANSACTION INTEGRITY ARCHITECTURE")
    print("Comprehensive demonstration of multi-layered experiment validation")
    
    demo = TransactionIntegrityDemo()
    
    try:
        # Run successful transaction demo
        success = demo.demonstrate_transaction_coordination()
        
        # Show failure scenario
        if success:
            demo.demonstrate_failure_scenario()
        
        print(f"\n📚 ARCHITECTURE DOCUMENTATION")
        print(f"Full details: docs/platform-development/architecture/TRANSACTION_INTEGRITY_ARCHITECTURE.md")
        print(f"Implementation: src/utils/*_transaction_manager.py")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        logger.exception("Transaction integrity demo failed")

if __name__ == "__main__":
    main() 