#!/usr/bin/env python3
"""
Quick Test for AI Agents
========================

This is the simplest possible test to verify the system is working.
If this fails, there's a fundamental problem.

Usage:
    python3 discernus/tests/quick_test.py
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
# Disable huggingface tokenizers parallelism warning before any imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"

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
        from discernus.agents.automated_statistical_analysis.agent import AutomatedStatisticalAnalysisAgent
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
        agent = AutomatedStatisticalAnalysisAgent()
        # Simple test - just check agent can be instantiated
        assert agent is not None
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