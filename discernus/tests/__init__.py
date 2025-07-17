"""
Discernus Test Suite
===================

This package contains comprehensive tests for the Discernus platform.

## Quick Start for AI Agents

### ⚡ FASTEST: Quick Test (30 seconds)
```bash
# Instant verification that everything works:
python3 discernus/tests/quick_test.py
```

### ✅ RECOMMENDED: Use Simple Working Tests
```bash
# These tests ACTUALLY WORK out of the box:
python3 discernus/tests/simple_working_tests.py
python3 -m unittest discernus.tests.simple_working_tests -v

# Run specific test:
python3 -m unittest discernus.tests.simple_working_tests.TestBasicFunctionality.test_imports_work -v
```

### 🔧 INTEGRATION: Workflow Integration Tests
```bash
# Test orchestration and agent handoffs (THIN/THICK architecture):
python3 discernus/tests/workflow_integration_tests.py
python3 -m unittest discernus.tests.workflow_integration_tests -v
```

### ⚠️ Legacy Tests (Use with Caution)
```bash
# These tests may be broken due to complex mock setups:
python3 discernus/tests/comprehensive_test_suite.py
python3 discernus/tests/agent_isolation_test_framework.py
python3 discernus/tests/end_to_end_workflow_test.py
```

### Prerequisites:
- Activate virtual environment: `source venv/bin/activate`
- Use Python 3: `python3` (not `python`)
- Install dependencies: `pip install -r requirements.txt`

### Common Issues:
- Missing PyYAML: `pip install PyYAML`
- Path issues: Always run from project root (/Volumes/dev/discernus)
- Mock responses: Check mock_llm_gateway.py for queue consumption
- Empty CSV errors: Usually indicates upstream mock failures

See README.md for detailed documentation.
"""

# Test configuration constants
PYTHON_EXECUTABLE = "python3"
VENV_ACTIVATION_CMD = "source venv/bin/activate"
PROJECT_ROOT = "/Volumes/dev/discernus"

# Common test dependencies (install_name -> import_name)
REQUIRED_PACKAGES = {
    "PyYAML": "yaml",
    "unittest": "unittest", 
    "pathlib": "pathlib",
    "json": "json"
}

# Test execution patterns
TEST_PATTERNS = {
    "quick_test": "python3 discernus/tests/quick_test.py",
    "simple_working": "python3 discernus/tests/simple_working_tests.py",
    "simple_working_unittest": "python3 -m unittest discernus.tests.simple_working_tests -v",
    "workflow_integration": "python3 discernus/tests/workflow_integration_tests.py",
    "workflow_integration_unittest": "python3 -m unittest discernus.tests.workflow_integration_tests -v",
    "working_analysis_agent": "python3 -m unittest discernus.tests.test_analysis_agent.TestAnalysisAgent.test_analysis_agent_loops_and_captures_raw_output -v",
    "comprehensive": "python3 discernus/tests/comprehensive_test_suite.py",
    "isolation": "python3 discernus/tests/agent_isolation_test_framework.py", 
    "end_to_end": "python3 discernus/tests/end_to_end_workflow_test.py",
    "specific_unittest": "python3 -m unittest discernus.tests.{module}.{class}.{method} -v"
}

# Test framework metadata
__version__ = "1.0.0"
__author__ = "Discernus Development Team"
__description__ = "Framework-agnostic, cost-efficient test suite for Discernus platform"

def check_test_environment():
    """
    Quick environment check for AI agents to verify test setup.
    
    Returns:
        dict: Environment status with helpful information
    """
    import sys
    import os
    from pathlib import Path
    
    status = {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "working_directory": os.getcwd(),
        "project_root_detected": Path.cwd().name == "discernus",
        "venv_active": hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix),
        "required_packages": {}
    }
    
    # Check for required packages
    for install_name, import_name in REQUIRED_PACKAGES.items():
        try:
            __import__(import_name)
            status["required_packages"][install_name] = "✅ Available"
        except ImportError:
            status["required_packages"][install_name] = f"❌ Missing - run: pip install {install_name}"
    
    return status

def print_test_environment():
    """Print a formatted test environment report for AI agents."""
    import os
    status = check_test_environment()
    
    print("🧪 Discernus Test Environment Status")
    print("=" * 40)
    print(f"Python: {status['python_version'].split()[0]}")
    print(f"Working Directory: {status['working_directory']}")
    print(f"Project Root: {'✅' if status['project_root_detected'] else '❌'}")
    print(f"Virtual Environment: {'✅' if status['venv_active'] else '❌'}")
    print("\nRequired Packages:")
    for package, availability in status["required_packages"].items():
        print(f"  {package}: {availability}")
    
    if not status['project_root_detected']:
        print(f"\n⚠️  Warning: Run from project root: cd {PROJECT_ROOT}")
    
    if not status['venv_active']:
        print(f"\n⚠️  Warning: Activate virtual environment: {VENV_ACTIVATION_CMD}")
    
    # Check intelligent testing capabilities
    print("\n🧠 Intelligent Testing Capabilities:")
    
    # API-based intelligent testing (prioritize Vertex AI)
    google_available = bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    anthropic_available = bool(os.getenv('ANTHROPIC_API_KEY'))
    api_available = google_available or anthropic_available
    
    if google_available:
        print("  API Testing: ✅ Available (Vertex AI Gemini 2.5 Flash - standardized)")
    elif anthropic_available:
        print("  API Testing: ✅ Available (Anthropic Claude Haiku - fallback)")
    else:
        print("  API Testing: ❌ No API Keys (set GOOGLE_APPLICATION_CREDENTIALS preferred)")
    
    # Local intelligent testing
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            if 'mistral' in result.stdout:
                print("  Local Ollama: ✅ Available (Mistral ready)")
            else:
                print("  Local Ollama: ⚠️ Available, run 'ollama pull mistral'")
        else:
            print("  Local Ollama: ❌ Not responding")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  Local Ollama: ❌ Not installed")
    except Exception:
        print("  Local Ollama: ❌ Error checking")
    
    print("\n🚀 Ready to run tests!")
    print("⚡ FASTEST: python3 discernus/tests/quick_test.py")
    print("✅ RECOMMENDED: python3 discernus/tests/simple_working_tests.py")
    if api_available:
        print("🧠 INTELLIGENT: python3 discernus/tests/intelligent_integration_tests.py (~$0.004)")
    print("🏠 LOCAL: python3 discernus/tests/local_intelligent_tests.py (free, slow)")
    print("🔧 INTEGRATION: python3 discernus/tests/workflow_integration_tests.py")
    print("Example: python3 -m unittest discernus.tests.simple_working_tests.TestBasicFunctionality.test_imports_work -v")
