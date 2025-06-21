#!/bin/bash
# Wrapper script for comprehensive_experiment_orchestrator.py
# Ensures proper PYTHONPATH for database connectivity

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Calculate project root (two levels up from scripts/production)
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH}"

# Run the orchestrator with all arguments passed through
python3 "${SCRIPT_DIR}/comprehensive_experiment_orchestrator.py" "$@" 