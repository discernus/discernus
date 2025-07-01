#!/bin/bash
# Monitored Flagship Experiment Runner
# ===================================
# 
# Runs the flagship ensemble experiment with comprehensive error monitoring
# Safe for overnight execution with full error capture

set -e  # Exit on any error

echo "🔍 Starting Monitored Flagship Ensemble Experiment"
echo "=================================================="

# Change to project directory
cd "$(dirname "$0")"

# Create output log for terminal output
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_LOG="flagship_experiment_output_${TIMESTAMP}.log"

echo "📁 Terminal output will be saved to: ${OUTPUT_LOG}"
echo "🕐 Started at: $(date)"
echo ""

# Run the monitored experiment with output capture
python3 monitored_experiment_runner.py 0_workspace/byu_populism_project/experiments/exp_02_flagship_ensemble/exp_02_flagship_ensemble.yaml 2>&1 | tee "${OUTPUT_LOG}"

echo ""
echo "🏁 Experiment completed at: $(date)"
echo "📁 Terminal output saved to: ${OUTPUT_LOG}"
echo "📋 Check error_logs_* directories for detailed error analysis" 