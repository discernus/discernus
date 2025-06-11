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
fi

# Change to project root
cd "${PROJECT_ROOT}"

echo "✅ Development environment configured:"
echo "   PROJECT_ROOT: ${PROJECT_ROOT}"
echo "   PYTHONPATH: ${PYTHONPATH}"
echo "   Current directory: $(pwd)"
echo ""
echo "💡 To verify Python can find your modules, run:"
echo "   python -c \"import sys; print('src/' in ''.join(sys.path))\""
echo ""
echo "🚀 Ready for development!" 