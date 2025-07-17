#!/usr/bin/env python3
"""
Quick Test for AI Agents
========================

This is the simplest possible test to verify the system is working.
If this fails, there's a fundamental problem.

Usage:
    python3 discernus/tests/quick_test.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the most basic test possible."""
    print("🚀 Quick Test for AI Agents")
    print("=" * 30)
    
    # Test 1: Basic imports
    try:
        from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway
        from discernus.agents.calculation_agent import CalculationAgent
        print("✅ Imports work")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Basic mock gateway
    try:
        mock_gateway = MockLLMGateway(["test_response"])
        response, metadata = mock_gateway.execute_call("test_model", "test_prompt")
        assert response == "test_response"
        assert metadata["success"] is True
        print("✅ Mock gateway works")
    except Exception as e:
        print(f"❌ Mock gateway failed: {e}")
        return False
    
    # Test 3: Basic agent
    try:
        agent = CalculationAgent()
        result = agent.execute({
            'framework': {'calculation_spec': [{'name': 'test', 'formula': '1 + 1'}]},
            'analysis_results': [{'success': True, 'json_output': {'base_score': 0.5}}]
        }, {})
        assert result['analysis_results'][0]['json_output']['test'] == 2
        print("✅ Agent works")
    except Exception as e:
        print(f"❌ Agent failed: {e}")
        return False
    
    # Test 4: Environment check
    try:
        from discernus.tests import check_test_environment
        status = check_test_environment()
        assert status['project_root_detected'] is True
        print("✅ Environment check works")
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return False
    
    print("\n🎉 All quick tests passed!")
    print("💡 Ready to run full test suite:")
    print("   python3 discernus/tests/simple_working_tests.py")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 