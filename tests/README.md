# 🧪 Narrative Gravity Maps - Smoke Tests

This directory contains smoke tests for the Narrative Gravity Maps application, covering both CLI tools and the Streamlit interface.

## 📂 Test Structure

```
tests/
├── README.md                 # This file - test documentation
├── run_tests.py             # Main test runner script
├── test_requirements.txt    # Testing dependencies
├── test_cli_tools.py        # CLI functionality tests
└── test_streamlit_app.py    # Streamlit interface tests
```

## 🚀 Quick Start

### 1. Install Test Dependencies

```bash
# From the project root directory
pip install -r tests/test_requirements.txt
```

### 2. Run All Tests

```bash
# Simple run - from project root
python tests/run_tests.py

# Or directly
cd tests && python run_tests.py
```

### 3. Run Individual Test Files

```bash
# CLI tests only
python tests/test_cli_tools.py

# Streamlit tests only  
python tests/test_streamlit_app.py
```

## 📊 Test Coverage

### CLI Tools Tests (`test_cli_tools.py`)

- **Framework Manager Tests**
  - ✅ Framework initialization
  - ✅ Framework listing (empty and populated)
  - ✅ Framework validation
  - ✅ CLI command help/usage

- **Prompt Generator Tests**
  - ✅ Configuration loading (dipoles.json, framework.json)
  - ✅ Interactive prompt generation
  - ✅ Batch prompt generation
  - ✅ CLI command help/usage

- **Visualization Engine Tests**
  - ✅ Elliptical visualizer initialization
  - ✅ Analysis data loading
  - ✅ JSON validation and error handling
  - ✅ CLI command help/usage

- **Integration Tests**
  - ✅ CLI commands execution
  - ✅ Help system functionality
  - ✅ Basic command validation

### Streamlit App Tests (`test_streamlit_app.py`)

- **Component Tests**
  - ✅ Session state initialization
  - ✅ Framework name normalization
  - ✅ JSON framework detection
  - ✅ Utility function validation

- **Integration Tests**
  - ✅ File existence checks
  - ✅ Python syntax validation
  - ✅ Import system verification
  - ✅ Requirements file validation

- **App Startup Tests**
  - ⚠️ Full Streamlit startup (skipped by default - long-running)
  - ✅ Launch script validation
  - ✅ Dependencies verification

## 🔧 Configuration

### Test Environment

Tests automatically:
- Set up the Python path to include the project root
- Change working directory to project root
- Create temporary directories for isolated testing
- Clean up resources after each test

### Mock Data

Tests create mock framework structures when needed:
- Temporary `dipoles.json` and `framework.json` files
- Test analysis data in proper JSON format
- Isolated test directories that don't affect the main project

## 📋 Test Results

The test runner provides detailed output:

```
🎯 Narrative Gravity Maps - Smoke Test Runner
============================================================

🔧 Test environment setup:
   Project root: /path/to/narrative_gravity_analysis
   Working directory: /path/to/narrative_gravity_analysis
   Python path includes: /path/to/narrative_gravity_analysis

🔍 Discovering tests in: /path/to/tests
   Pattern: test_*.py

📄 Found 2 test file(s):
   - test_cli_tools.py
   - test_streamlit_app.py

🧪 Running tests from test_cli_tools...
============================================================
[Individual test results...]

📊 TEST SUMMARY
============================================================
✅ PASS test_cli_tools................  15 tests,   0 failures,   0 errors,   0 skipped
✅ PASS test_streamlit_app.............  12 tests,   0 failures,   0 errors,   1 skipped
------------------------------------------------------------
TOTAL:                              27 tests,   0 failures,   0 errors,   1 skipped

🎉 ALL TESTS PASSED!

⏱️  Tests completed in 3.45 seconds
```

## 🐛 Troubleshooting

### Common Issues

#### ImportError: Module not found
```bash
# Make sure you're running from the project root
cd /path/to/narrative_gravity_analysis
python tests/run_tests.py

# Or install the project in development mode
pip install -e .
```

#### Missing Dependencies
```bash
# Install test dependencies
pip install -r tests/test_requirements.txt

# Or install main dependencies first
pip install -r requirements.txt
```

#### Streamlit Import Errors
```bash
# Ensure Streamlit is installed
pip install streamlit>=1.30.0

# Check if other dependencies are missing
pip install matplotlib numpy seaborn plotly pandas
```

#### Framework Configuration Errors
- Tests create their own mock frameworks
- If you see framework-related errors, ensure the `frameworks/` directory exists
- Check that `config/` symlinks are properly set up

### Test-Specific Issues

#### Long-Running Tests
Some tests are skipped by default (marked with `@unittest.skip`):
- `test_streamlit_app_starts` - Actually launches Streamlit server

To enable these tests, edit the test file and remove the `@unittest.skip` decorator.

#### CLI Integration Tests
These tests rely on:
- Scripts being executable from the project root
- Python modules being importable
- Command-line arguments being properly handled

If these fail, check:
1. Working directory is correct
2. Python path includes project root  
3. All required files exist

## 🎯 Adding New Tests

### Test File Structure

```python
#!/usr/bin/env python3
"""
Description of what this test file covers
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from your_module import YourClass

class TestYourFeature(unittest.TestCase):
    """Test cases for your feature"""
    
    def setUp(self):
        """Set up test environment"""
        pass
    
    def tearDown(self):
        """Clean up test environment"""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```

### Best Practices

1. **Use descriptive test names** - `test_framework_validation_with_valid_data`
2. **Clean up resources** - Use `tearDown()` to remove temp files/directories
3. **Test both success and failure cases** - Happy path and error conditions
4. **Use mocks for external dependencies** - Don't rely on external services
5. **Make tests independent** - Each test should be able to run in isolation
6. **Add timeouts for subprocess calls** - Prevent hanging tests

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Smoke Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r tests/test_requirements.txt
    - name: Run smoke tests
      run: |
        python tests/run_tests.py
```

### Local Automation

```bash
# Create a git pre-commit hook
echo '#!/bin/bash\npython tests/run_tests.py' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 📝 Notes

- Tests are designed as **smoke tests** - they verify basic functionality works
- They do **not** replace comprehensive unit/integration testing
- Focus is on "does it work at all" rather than "does it work perfectly"
- Tests are designed to be fast and reliable for CI/CD pipelines

For questions or issues with the test suite, check the main project documentation or create an issue in the project repository. 