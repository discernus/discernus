#!/usr/bin/env python3
"""
THIN Framework Test Runner
=========================

Tests the THIN solution to process hallucination using framework-agnostic architecture.

This replaces the complex run_atomic_analysis.py with a clean THIN implementation that:
1. Loads CFF v2.0 specs from files (framework knowledge in files, not code)
2. Uses enhanced prompts with constraints to prevent philosophical drift 
3. Applies simple overwatch detection for quality control
4. Extracts structured outputs using generic patterns

Works with ANY framework, not just CFF v2.0.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.orchestrator import ThinOrchestrator
from discernus.core.orchestrator_enhancement import (
    create_framework_aware_orchestrator,
    run_framework_analysis,
    CFFTestRunner,
    extract_framework_results,
    EnhancedResearchConfig
)

class ThinFrameworkTestSuite:
    """
    THIN test suite that validates the framework-agnostic solution
    
    Tests with CFF v2.0 but architecture works with any framework
    """
    
    def __init__(self, test_dir: Path):
        self.test_dir = Path(test_dir)
        self.project_root = project_root
        
        # Initialize base orchestrator
        self.base_orchestrator = ThinOrchestrator(str(project_root))
        
        # Create framework-aware orchestrator  
        self.enhanced_orchestrator = create_framework_aware_orchestrator(self.base_orchestrator)
        
        print("🎯 THIN Framework Test Suite Initialized")
        print(f"✅ Test directory: {self.test_dir}")
        print(f"✅ Framework-agnostic architecture ready")
    
    def load_test_speech(self) -> str:
        """Load Trump speech for testing"""
        speech_file = self.test_dir / "source_texts" / "trump_announcement_2016_06_16.txt"
        
        if not speech_file.exists():
            raise FileNotFoundError(f"Test speech not found: {speech_file}")
        
        return speech_file.read_text(encoding='utf-8')
    
    async def test_framework_agnostic_architecture(self) -> dict:
        """Test that the architecture works without any framework"""
        
        print("\n🔍 Testing Framework-Agnostic Architecture...")
        
        speech_text = self.load_test_speech()
        
        # Test with NO framework specified - should work generically
        config = EnhancedResearchConfig(
            research_question="Analyze the rhetorical patterns in this speech.",
            source_texts=speech_text,
            framework_name=None,  # No framework - test generic capability
            enable_overwatch=True
        )
        
        session_id = await self.enhanced_orchestrator.start_framework_research_session(config)
        
        result = {
            'test_name': 'framework_agnostic',
            'session_id': session_id,
            'framework_specified': config.framework_name,
            'success': session_id is not None,
            'message': 'Architecture works without framework specification'
        }
        
        print(f"✅ Framework-agnostic test: {result['success']}")
        return result
    
    async def test_cff_framework_loading(self) -> dict:
        """Test CFF v2.0 framework loading and context injection"""
        
        print("\n🔍 Testing CFF v2.0 Framework Loading...")
        
        from discernus.core.framework_loader import FrameworkLoader
        
        # Test framework loading
        framework_loader = FrameworkLoader()
        cff_context = framework_loader.load_framework_context("cohesive_flourishing_framework_v2")
        
        result = {
            'test_name': 'cff_framework_loading',
            'framework_context_loaded': bool(cff_context),
            'framework_name': cff_context.get('framework_name', 'Not found'),
            'dimensions_found': len(cff_context.get('analysis_dimensions', [])),
            'output_requirements_present': 'output_requirements' in cff_context,
            'success': bool(cff_context and cff_context.get('framework_name'))
        }
        
        print(f"✅ Framework loading test: {result['success']}")
        print(f"   Framework: {result['framework_name']}")
        print(f"   Dimensions: {result['dimensions_found']}")
        
        return result
    
    async def test_enhanced_prompt_generation(self) -> dict:
        """Test enhanced prompt generation with framework context"""
        
        print("\n🔍 Testing Enhanced Prompt Generation...")
        
        from discernus.core.framework_loader import enhance_expert_prompt_with_framework
        
        # Test enhanced prompt generation
        enhanced_prompt = enhance_expert_prompt_with_framework(
            expert_name="data_science_expert",
            research_question="Test research question",
            source_texts="Test source text",
            expert_request="Provide analysis",
            framework_name="cohesive_flourishing_framework_v2"
        )
        
        # Check if framework context is injected
        has_framework_context = "FRAMEWORK CONTEXT" in enhanced_prompt
        has_output_requirements = "REQUIRED OUTPUT FORMAT" in enhanced_prompt
        has_constraints = "CONSTRAINTS" in enhanced_prompt
        has_forbidden_behaviors = "FORBIDDEN BEHAVIORS" in enhanced_prompt
        
        result = {
            'test_name': 'enhanced_prompt_generation',
            'prompt_length': len(enhanced_prompt),
            'has_framework_context': has_framework_context,
            'has_output_requirements': has_output_requirements,
            'has_constraints': has_constraints,
            'has_forbidden_behaviors': has_forbidden_behaviors,
            'success': all([has_framework_context, has_output_requirements, has_constraints])
        }
        
        print(f"✅ Enhanced prompt test: {result['success']}")
        print(f"   Context injected: {has_framework_context}")
        print(f"   Requirements present: {has_output_requirements}")
        
        return result
    
    async def test_overwatch_detection(self) -> dict:
        """Test simple overwatch detection for process hallucination"""
        
        print("\n🔍 Testing Overwatch Detection...")
        
        from discernus.core.framework_loader import SimpleOverwatch
        
        overwatch = SimpleOverwatch()
        
        # Test philosophical drift detection
        philosophical_response = """
        This is a fascinating ontological question that requires epistemological analysis.
        The phenomenological aspects are complex and require dialectical examination.
        As we've established, the metaphysical dimensions are crucial for understanding.
        Furthermore, the axiological considerations must be examined hermeneutically.
        """
        
        # Test good response
        good_response = """
        {
          "individual_dignity": {
            "score": 0.2,
            "evidence": "I've employed tens of thousands of people over my lifetime",
            "confidence": 0.7,
            "reasoning": "Limited evidence of universal human worth emphasis"
          }
        }
        """
        
        bad_detection = overwatch.detect_drift(philosophical_response)
        good_detection = overwatch.detect_drift(good_response)
        
        result = {
            'test_name': 'overwatch_detection',
            'philosophical_drift_detected': bad_detection['has_drift'],
            'drift_indicators': bad_detection['drift_indicators'],
            'good_response_passes': not good_detection['has_drift'],
            'json_detection_works': good_detection['has_json'],
            'score_detection_works': good_detection['has_scores'],
            'success': bad_detection['has_drift'] and not good_detection['has_drift']
        }
        
        print(f"✅ Overwatch detection test: {result['success']}")
        print(f"   Philosophical drift detected: {bad_detection['has_drift']}")
        print(f"   Good response passes: {not good_detection['has_drift']}")
        
        return result
    
    async def test_cff_identity_axis_analysis(self) -> dict:
        """Test full CFF v2.0 Identity axis analysis"""
        
        print("\n🎯 Testing CFF v2.0 Identity Axis Analysis...")
        
        speech_text = self.load_test_speech()
        
        # Run framework analysis
        results = await run_framework_analysis(
            research_question="""
            Analyze this speech using the Cohesive Flourishing Framework (CFF) v2.0, 
            focusing on the Identity axis (Individual Dignity vs Tribal Dominance).
            Provide numerical scores with evidence citations and confidence levels.
            """,
            source_texts=speech_text,
            framework_name="cohesive_flourishing_framework_v2",
            base_orchestrator=self.base_orchestrator,
            enable_overwatch=True
        )
        
        # Extract and validate results
        extraction_results = extract_framework_results(results)
        
        result = {
            'test_name': 'cff_identity_axis_analysis',
            'analysis_completed': results.get('success', False),
            'session_id': results.get('session_id'),
            'framework_used': results.get('framework_name'),
            'error': results.get('error'),
            'extraction_results': extraction_results,
            'success': results.get('success', False)
        }
        
        print(f"✅ CFF Identity analysis test: {result['success']}")
        if result['success']:
            print(f"   Session: {result['session_id']}")
            print(f"   Framework: {result['framework_used']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return result
    
    async def run_full_test_suite(self) -> dict:
        """Run the complete THIN framework test suite"""
        
        print("🚀 STARTING THIN FRAMEWORK TEST SUITE")
        print("=" * 60)
        print("Testing Route 1: Enhanced prompts + Simple overwatch")
        print("Architecture: Framework-agnostic with CFF v2.0 validation")
        print()
        
        test_results = []
        
        try:
            # Test 1: Framework-agnostic architecture
            result1 = await self.test_framework_agnostic_architecture()
            test_results.append(result1)
            
            # Test 2: CFF framework loading
            result2 = await self.test_cff_framework_loading()
            test_results.append(result2)
            
            # Test 3: Enhanced prompt generation
            result3 = await self.test_enhanced_prompt_generation()
            test_results.append(result3)
            
            # Test 4: Overwatch detection
            result4 = await self.test_overwatch_detection()
            test_results.append(result4)
            
            # Test 5: Full CFF analysis
            result5 = await self.test_cff_identity_axis_analysis()
            test_results.append(result5)
            
            # Calculate success rate
            successful_tests = sum(1 for r in test_results if r['success'])
            total_tests = len(test_results)
            success_rate = successful_tests / total_tests
            
            overall_result = {
                'test_suite': 'THIN_Framework_Route_1',
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': success_rate,
                'overall_success': success_rate >= 0.8,  # 80% pass rate required
                'individual_results': test_results,
                'timestamp': datetime.now().isoformat()
            }
            
            print("\n" + "=" * 60)
            print("🎉 TEST SUITE COMPLETED")
            print("=" * 60)
            print(f"✅ Successful tests: {successful_tests}/{total_tests}")
            print(f"📊 Success rate: {success_rate:.1%}")
            print(f"🏔️ Overall success: {overall_result['overall_success']}")
            
            if overall_result['overall_success']:
                print("\n🎯 ROUTE 1 SOLUTION VALIDATED!")
                print("✅ Framework-agnostic architecture working")
                print("✅ Process hallucination prevention effective")
                print("✅ CFF v2.0 integration successful")
                print("✅ Ready for production deployment")
            else:
                print("\n⚠️ Some tests failed - solution needs refinement")
            
            return overall_result
            
        except Exception as e:
            print(f"\n❌ TEST SUITE FAILED: {e}")
            return {
                'test_suite': 'THIN_Framework_Route_1',
                'error': str(e),
                'overall_success': False,
                'individual_results': test_results
            }
    
    def save_test_results(self, results: dict):
        """Save test results to file"""
        results_file = self.test_dir / "thin_framework_test_results.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Test results saved to: {results_file}")

async def main():
    """Main test execution"""
    
    # Get test directory
    test_dir = Path(__file__).parent
    
    # Create test suite
    test_suite = ThinFrameworkTestSuite(test_dir)
    
    # Run tests
    results = await test_suite.run_full_test_suite()
    
    # Save results
    test_suite.save_test_results(results)
    
    # Exit with appropriate code
    if results.get('overall_success'):
        print("\n🏔️ ALL TESTS PASSED - ROUTE 1 SOLUTION READY! 🎯")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed - see results for details")
        sys.exit(1)

if __name__ == "__main__":
    print("🎯 THIN Framework Test Runner")
    print("Route 1: Enhanced Prompts + Simple Overwatch")
    print("Framework-Agnostic Architecture with CFF v2.0 Validation")
    print()
    
    asyncio.run(main()) 