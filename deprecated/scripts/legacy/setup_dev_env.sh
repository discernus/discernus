#!/bin/bash
# Development Environment Setup Script
# Run with: source scripts/setup_dev_env.sh

# Get the project root (directory containing this script's parent)
if [ -n "${BASH_SOURCE[0]}" ]; then
    export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
else
    # Fallback for when not sourced
    export PROJECT_ROOT="/Users/jeffwhatcott/narrative_gravity_analysis"
fi

echo "🔧 Setting up Narrative Gravity development environment..."

# CRITICAL: Ensure we're in the virtual environment
if [ -z "$VIRTUAL_ENV" ] || [ "$VIRTUAL_ENV" != "${PROJECT_ROOT}/venv" ]; then
    echo "⚠️  Virtual environment not active or incorrect. Activating..."
    if [ -f "${PROJECT_ROOT}/venv/bin/activate" ]; then
        source "${PROJECT_ROOT}/venv/bin/activate"
        echo "✅ Virtual environment activated: ${PROJECT_ROOT}/venv"
    else
        echo "❌ Virtual environment not found at ${PROJECT_ROOT}/venv"
        echo "💡 Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        return 1
    fi
else
    echo "✅ Virtual environment already active: $VIRTUAL_ENV"
fi

# Add project directories to Python path
export PYTHONPATH="${PROJECT_ROOT}:${PROJECT_ROOT}/src:${PYTHONPATH}"

# Set project-specific environment variables
export NARRATIVE_GRAVITY_ROOT="${PROJECT_ROOT}"
export NARRATIVE_GRAVITY_SRC="${PROJECT_ROOT}/src"
export NARRATIVE_GRAVITY_SCRIPTS="${PROJECT_ROOT}/scripts"

# Add scripts to PATH for CLI convenience
export PATH="${PROJECT_ROOT}/scripts:${PATH}"

# Load environment variables
if [ -f "${PROJECT_ROOT}/.env" ]; then
    echo "📋 Loading .env file..."
    set -a  # automatically export all variables
    source "${PROJECT_ROOT}/.env"
    set +a
else
    echo "⚠️  .env file not found at ${PROJECT_ROOT}/.env"
fi

# Change to project root
cd "${PROJECT_ROOT}"

echo "✅ Development environment configured:"
echo "   PROJECT_ROOT: ${PROJECT_ROOT}"
echo "   VIRTUAL_ENV: ${VIRTUAL_ENV}"
echo "   PYTHONPATH: ${PYTHONPATH}"
echo "   Current directory: $(pwd)"
echo ""

# VERIFICATION SECTION
echo "🔍 Environment Verification:"

# Python availability check
if command -v python >/dev/null 2>&1; then
    PYTHON_PATH=$(which python)
    echo "   ✅ python: $PYTHON_PATH"
else
    echo "   ⚠️  python: not available (use python3)"
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON3_PATH=$(which python3)
    echo "   ✅ python3: $PYTHON3_PATH"
else
    echo "   ❌ python3: not available"
    return 1
fi

# Pip availability check
if command -v pip >/dev/null 2>&1; then
    PIP_PATH=$(which pip)
    echo "   ✅ pip: $PIP_PATH"
else
    echo "   ⚠️  pip: not available (use pip3)"
fi

# Critical imports check
if python3 -c "import alembic; print('   ✅ alembic: available')" 2>/dev/null; then
    :
else
    echo "   ❌ alembic: not available - run 'pip install alembic'"
fi

if python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('   ✅ narrative_gravity imports: working')" 2>/dev/null; then
    :
else
    echo "   ❌ narrative_gravity imports: failed"
fi

echo ""
echo "🎯 CONSISTENT COMMAND PATTERNS:"
echo "   ✅ ALWAYS USE: python3 (not python)"
echo "   ✅ ALWAYS USE: pip3 (not pip) or pip after venv activation"
echo "   ✅ CHECK: Virtual environment is active before pip installs"
echo ""
echo "🚀 Ready for development!"

# Create helpful aliases for this session
alias py=python3
alias pip=pip3 