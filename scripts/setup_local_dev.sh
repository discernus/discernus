#!/bin/bash
# Local Development Setup Script for Discernus
# Supports Python 3.11 (stable) and 3.13 (future) with validation

set -e

# Parse command line arguments
PYTHON_VERSION="3.11"  # Default to stable version
FORCE_RECREATE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --python-version)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        --force-recreate)
            FORCE_RECREATE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--python-version 3.11|3.13] [--force-recreate]"
            echo ""
            echo "Options:"
            echo "  --python-version  Choose Python version (3.11 or 3.13, default: 3.11)"
            echo "  --force-recreate  Force recreation of virtual environment"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Use Python 3.11 (stable)"
            echo "  $0 --python-version 3.13    # Use Python 3.13 (future)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🏗️  Setting up Discernus for Local Development"
echo "=============================================="
echo "🐍 Target Python Version: $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Run this script from the Discernus project root"
    exit 1
fi

# Validate Python version choice
if [[ "$PYTHON_VERSION" != "3.11" && "$PYTHON_VERSION" != "3.13" ]]; then
    echo "❌ Error: Unsupported Python version: $PYTHON_VERSION"
    echo "   Supported versions: 3.11 (stable), 3.13 (future)"
    exit 1
fi

# Check if requested Python version is available
PYTHON_CMD="python$PYTHON_VERSION"
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "❌ Error: Python $PYTHON_VERSION not found"
    echo ""
    if [[ "$PYTHON_VERSION" == "3.13" ]]; then
        echo "📋 To install Python 3.13:"
        echo "   macOS: brew install python@3.13"
        echo "   Ubuntu: sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.13"
        echo "   Or use pyenv: pyenv install 3.13.5"
    else
        echo "📋 To install Python 3.11:"
        echo "   macOS: brew install python@3.11"
        echo "   Ubuntu: sudo apt install python3.11"
    fi
    exit 1
fi

# Set virtual environment name based on Python version
VENV_NAME="venv"
if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    VENV_NAME="venv-py313"
fi

# Handle virtual environment creation/recreation
if [[ "$FORCE_RECREATE" == true && -d "$VENV_NAME" ]]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf "$VENV_NAME"
fi

# 1. Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment with Python $PYTHON_VERSION..."
    "$PYTHON_CMD" -m venv "$VENV_NAME"
    echo "✅ Virtual environment created: $VENV_NAME"
else
    echo "✅ Virtual environment already exists: $VENV_NAME"
fi

# 2. Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_NAME/bin/activate" || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# 3. Verify Python version
ACTUAL_VERSION=$(python --version)
echo "🐍 Using: $ACTUAL_VERSION"

# 4. Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# 5. Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# 6. Set up environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment configuration..."
    cp env.example .env
    echo "✅ Created .env from env.example"
    echo "📝 Please edit .env to configure your local database"
else
    echo "✅ .env already exists"
fi

# 7. Version-specific validation
echo "🧪 Testing installation..."
if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo "🚀 Running Python 3.13 compatibility validation..."
    if python3 -c "
import sys
print(f'✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')

# Test core dependencies with 3.13 features
try:
    import numpy as np
    import pandas as pd
    import pytest
    import openai
    import anthropic
    print(f'✅ Core dependencies available')
    print(f'   NumPy: {np.__version__}')
    print(f'   Pandas: {pd.__version__}')
    print('✅ Python 3.13 features and dependencies compatible')
except Exception as e:
    print(f'❌ Python 3.13 compatibility issue: {e}')
    exit(1)
"; then
        echo "✅ Python 3.13 setup successful"
    else
        echo "❌ Python 3.13 setup verification failed"
        exit 1
    fi
else
    # Standard validation for 3.11
    if python3 -c "import numpy, pandas, pytest; print('✅ Core dependencies available')"; then
        echo "✅ Installation successful"
    else
        echo "❌ Installation verification failed"
        exit 1
    fi
fi

# 8. Run a quick test
echo "🔬 Running quick test suite..."
if python3 -m pytest tests/unit/test_discernus_coordinate_system.py -v --tb=short; then
    echo "✅ Tests passing - ready for development!"
else
    echo "⚠️  Some tests failed, but environment is set up"
fi

echo ""
echo "🎉 Local development setup complete!"
echo ""
echo "Next steps:"
echo "1. source $VENV_NAME/bin/activate"
echo "2. Edit .env for your database configuration"
echo "3. python3 -m pytest tests/unit/ -v"
echo "4. Start developing!"
echo ""

if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo "🚀 Python 3.13 Features Available:"
    echo "   • Enhanced error messages and debugging"
    echo "   • Experimental JIT compiler"
    echo "   • Free-threaded mode (experimental)"
    echo "   • Better interactive interpreter"
    echo ""
fi

echo "💡 Remember: Validate in CI before committing:"
echo "   git push origin feature/your-branch"
echo "   Check GitHub Actions for multi-version testing" 