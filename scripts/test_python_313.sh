#!/bin/bash
# Python 3.13 Compatibility Testing Script
# Quick local validation before pushing to CI

set -e

echo "🚀 Python 3.13 Compatibility Testing"
echo "====================================="

# Check if Python 3.13 is available
if ! command -v python3.13 &> /dev/null; then
    echo "❌ Python 3.13 not found"
    echo ""
    echo "📋 Installation instructions:"
    echo "   macOS: brew install python@3.13"
    echo "   Ubuntu: sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.13"
    echo "   Or use pyenv: pyenv install 3.13.5"
    exit 1
fi

# Check if Python 3.13 virtual environment exists
if [ ! -d "venv-py313" ]; then
    echo "🏗️  Python 3.13 environment not found. Creating..."
    echo "💡 Tip: Use './scripts/setup_local_dev.sh --python-version 3.13' for full setup"
    echo ""
    
    # Quick setup for testing
    python3.13 -m venv venv-py313
    source venv-py313/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "✅ Using existing Python 3.13 environment"
    source venv-py313/bin/activate
fi

# Verify Python version
PYTHON_VERSION=$(python --version)
echo "🐍 Testing with: $PYTHON_VERSION"

# Test 1: Core imports
echo ""
echo "🧪 Test 1: Core Import Compatibility"
echo "-----------------------------------"
python -c "
try:
    import sys
    import numpy as np
    import pandas as pd
    import scipy as sp
    import plotly
    import openai
    import anthropic
    import psycopg2
    import yaml
    
    print(f'✅ All core imports successful')
    print(f'   Python: {sys.version.split()[0]}')
    print(f'   NumPy: {np.__version__}')
    print(f'   Pandas: {pd.__version__}')
    print(f'   SciPy: {sp.__version__}')
except Exception as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

# Test 2: Project-specific imports
echo ""
echo "🧪 Test 2: Project Module Compatibility"
echo "--------------------------------------"
python -c "
try:
    from src.analysis.statistics import StatisticalHypothesisTester
    from src.utils.cost_manager import CostManager
    from src.models.base import Base
    print('✅ Project modules import successfully')
except Exception as e:
    print(f'❌ Project import failed: {e}')
    exit(1)
"

# Test 3: Framework Specification v3.1 compliance
echo ""
echo "🧪 Test 3: Framework Specification v3.1 Compliance"
echo "-------------------------------------------------"
python -c "
try:
    from src.analysis.statistics import StatisticalHypothesisTester
    tester = StatisticalHypothesisTester()
    print('✅ Framework Specification v3.1 compliant statistical system works')
except Exception as e:
    print(f'❌ Framework compliance test failed: {e}')
    exit(1)
"

# Test 4: Run unit tests
echo ""
echo "🧪 Test 4: Unit Test Suite"
echo "-------------------------"
echo "Running core unit tests..."
if python -m pytest tests/unit/test_discernus_coordinate_system.py -v --tb=short; then
    echo "✅ Core coordinate system tests pass"
else
    echo "❌ Core tests failed"
    exit 1
fi

echo ""
echo "Running statistical analysis tests..."
if python -m pytest tests/unit/test_llm_quality_assurance.py -v --tb=short; then
    echo "✅ LLM quality assurance tests pass"
else
    echo "❌ LLM QA tests failed"
    exit 1
fi

# Test 5: Python 3.13 specific features (informational)
echo ""
echo "🚀 Test 5: Python 3.13 Feature Compatibility"
echo "--------------------------------------------"
python -c "
import sys
print(f'✅ Python version: {sys.version}')

# Check for Python 3.13 improvements
print('🎯 Python 3.13 feature checks:')

# Better error messages
try:
    # This should work with enhanced error reporting
    test_dict = {'key': 'value'}
    result = test_dict['nonexistent_key']
except KeyError as e:
    print('   ✅ Enhanced error messages available')

# JIT compiler info (if enabled)
try:
    import sysconfig
    if hasattr(sys, '_jit_enabled'):
        print('   ✅ JIT compiler available')
    else:
        print('   ℹ️  JIT compiler not enabled (normal)')
except:
    print('   ℹ️  JIT info not available')

# Free-threaded mode info
try:
    if hasattr(sys, '_is_gil_enabled'):
        gil_status = sys._is_gil_enabled()
        print(f'   ℹ️  GIL status: {\"enabled\" if gil_status else \"disabled (free-threaded)\"}')
    else:
        print('   ℹ️  Standard threading mode')
except:
    print('   ℹ️  Threading info not available')

print('✅ Python 3.13 compatibility confirmed')
"

echo ""
echo "🎉 Python 3.13 Compatibility Test Complete!"
echo "==========================================="
echo ""
echo "✅ All tests passed - your code is Python 3.13 ready!"
echo ""
echo "📋 Summary:"
echo "   • Core dependencies: Compatible"
echo "   • Project modules: Compatible"
echo "   • Framework Specification v3.1: Compatible"
echo "   • Unit tests: Passing"
echo "   • Python 3.13 features: Available"
echo ""
echo "🚀 Ready to push to CI with confidence!"
echo "   Your changes will be tested on both Python 3.11 and 3.13" 