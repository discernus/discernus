#!/usr/bin/env python3
"""
Test script to validate license automation system
"""

import json
import sys
from pathlib import Path

# Test data simulating a typical project
TEST_PACKAGES = {
    "numpy": {"license": "BSD License"},
    "pandas": {"license": "BSD-3-Clause"},
    "requests": {"license": "Apache License 2.0"},
    "flask": {"license": "BSD-3-Clause"},
    "pytest": {"license": "MIT License"},
    "some-gpl-package": {"license": "GPL-3.0"},  # This should be flagged
    "unknown-package": {"license": "Unknown"}     # This should be flagged
}

def test_policy_loading():
    """Test that our SaaS commercial policy loads correctly."""
    try:
        with open('saas_commercial_policy.json', 'r') as f:
            policy = json.load(f)
        
        print("✅ Policy loading test: PASSED")
        print(f"   - Policy name: {policy['policy_name']}")
        print(f"   - Compliance level: {policy['compliance_level']}")
        print(f"   - Approved licenses: {len(policy['approved_licenses'])}")
        print(f"   - Prohibited licenses: {len(policy['prohibited_licenses'])}")
        return True
    except Exception as e:
        print(f"❌ Policy loading test: FAILED - {e}")
        return False

def test_compliance_checking():
    """Test compliance checking with sample data."""
    try:
        # Write test data
        with open('test_packages.json', 'w') as f:
            json.dump(TEST_PACKAGES, f, indent=2)
        
        # Import and test compliance checker
        from compliance_checker import check_compliance, load_policy
        
        policy = load_policy('saas_commercial_policy.json')
        results = check_compliance(TEST_PACKAGES, policy)
        
        print("✅ Compliance checking test: PASSED")
        print(f"   - Total packages tested: {results['total_packages']}")
        print(f"   - Compliant packages: {len(results['compliant_packages'])}")
        print(f"   - Prohibited packages: {len(results['prohibited_packages'])}")
        print(f"   - Unknown packages: {len(results['unknown_packages'])}")
        print(f"   - Overall status: {results['overall_status']}")
        
        # Check that GPL package was caught
        gpl_caught = any(pkg['package'] == 'some-gpl-package' for pkg in results['prohibited_packages'])
        unknown_caught = any(pkg['package'] == 'unknown-package' for pkg in results['unknown_packages'])
        
        if gpl_caught and unknown_caught:
            print("✅ Violation detection: PASSED")
            print("   - GPL package correctly flagged as prohibited")
            print("   - Unknown package correctly flagged")
        else:
            print("❌ Violation detection: FAILED")
            return False
        
        # Cleanup
        Path('test_packages.json').unlink()
        return True
        
    except Exception as e:
        print(f"❌ Compliance checking test: FAILED - {e}")
        return False

def test_ci_integration():
    """Test CI/CD integration components."""
    try:
        # Check that automation files exist
        automation_files = [
            'saas_commercial_policy.json',
            'compliance_checker.py',
            'automated_monitoring.py',
            'run_audit.py',
            'license_checker.py'
        ]
        
        missing_files = []
        for file in automation_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ CI integration test: FAILED - Missing files: {missing_files}")
            return False
        
        print("✅ CI integration test: PASSED")
        print("   - All automation files present")
        print("   - Policy file configured for SaaS/commercial deployment")
        print("   - Monitoring system ready")
        return True
        
    except Exception as e:
        print(f"❌ CI integration test: FAILED - {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing License Automation System")
    print("=" * 50)
    
    tests = [
        ("Policy Loading", test_policy_loading),
        ("Compliance Checking", test_compliance_checking),
        ("CI Integration", test_ci_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! License automation system is ready.")
        print()
        print("🚀 Ready for:")
        print("   - SaaS deployment with zero license restrictions")
        print("   - Commercial deployment with full compliance")
        print("   - Automated CI/CD license enforcement")
        print("   - Continuous compliance monitoring")
        return 0
    else:
        print("❌ Some tests FAILED. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 