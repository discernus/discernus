#!/usr/bin/env python3
"""
Nano and Micro Integration Test Runner
=====================================

Simple script to run the nano and micro integration tests with proper setup.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    """Run the nano and micro integration tests."""
    print("🧪 Nano and Micro Integration Test Runner")
    print("=" * 50)
    
    # Check for required environment variables
    required_vars = ['GOOGLE_APPLICATION_CREDENTIALS']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables before running the tests.")
        return 1
    
    print("✅ Environment variables found")
    print(f"   GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    
    # Import and run tests
    try:
        import unittest
        from test_nano_micro_integration import TestNanoMicroIntegration
        
        print("\n🚀 Running integration tests...")
        print("   Model: vertex_ai/gemini-2.5-flash-lite")
        print("   Estimated cost: ~$0.003")
        print("   Expected duration: 5-10 minutes")
        print()
        
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestNanoMicroIntegration)
        
        # Run tests with verbose output
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        # Print summary
        print("\n" + "=" * 50)
        if result.wasSuccessful():
            print("🎉 All tests passed!")
            print(f"   Tests run: {result.testsRun}")
            print(f"   Failures: {len(result.failures)}")
            print(f"   Errors: {len(result.errors)}")
            return 0
        else:
            print("❌ Some tests failed!")
            print(f"   Tests run: {result.testsRun}")
            print(f"   Failures: {len(result.failures)}")
            print(f"   Errors: {len(result.errors)}")
            
            if result.failures:
                print("\nFailures:")
                for test, traceback in result.failures:
                    print(f"   - {test}: {traceback}")
            
            if result.errors:
                print("\nErrors:")
                for test, traceback in result.errors:
                    print(f"   - {test}: {traceback}")
            
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root with the virtual environment activated.")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
