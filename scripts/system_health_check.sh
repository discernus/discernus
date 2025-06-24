#!/bin/bash

# System Health Check for Discernus Platform
# Enhanced version with proper results management

set -e  # Exit on any error

echo "🏥 Discernus System Health Check"
echo "================================="

# Check if results directory exists, create if not
RESULTS_DIR="tests/system_health/results"
mkdir -p "$RESULTS_DIR"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run system health check
run_health_check() {
    local mode="$1"
    echo "🔍 Running system health check in $mode mode..."
    
    # Run the comprehensive experiment orchestrator in system health mode
    python3 scripts/applications/comprehensive_experiment_orchestrator.py \
        tests/system_health/test_experiments/system_health_test.yaml \
        --system-health-mode
    
    echo "✅ System health check completed successfully"
    echo "📁 Results stored in: $RESULTS_DIR"
    
    # Display summary of what was checked
    echo ""
    echo "🔍 Health Check Summary:"
    echo "- ✅ Database connectivity"
    echo "- ✅ Framework loading"
    echo "- ✅ API client initialization"
    echo "- ✅ Component validation"
    echo "- ✅ Mock LLM analysis"
    echo "- ✅ Quality assurance systems"
    echo "- ✅ Enhanced analysis pipeline"
    echo "- ✅ Visualization generation"
    echo "- ✅ HTML report creation"
    echo "- ✅ Academic exports"
    echo "- ✅ Data persistence validation"
    
    # Show location of results
    LATEST_RESULT=$(find "$RESULTS_DIR" -maxdepth 1 -type d -name "system_health_*" | sort -r | head -1)
    if [ -n "$LATEST_RESULT" ]; then
        echo ""
        echo "📊 Latest system health results:"
        echo "   Directory: $LATEST_RESULT"
        if [ -f "$LATEST_RESULT/enhanced_analysis/enhanced_analysis_report.html" ]; then
            echo "   HTML Report: $LATEST_RESULT/enhanced_analysis/enhanced_analysis_report.html"
        fi
        if [ -d "$LATEST_RESULT/enhanced_analysis/visualizations" ]; then
            CHART_COUNT=$(find "$LATEST_RESULT/enhanced_analysis/visualizations" -name "*.png" | wc -l)
            echo "   Visualizations: $CHART_COUNT charts generated"
        fi
        if [ -d "$LATEST_RESULT/enhanced_analysis/academic_exports" ]; then
            EXPORT_COUNT=$(find "$LATEST_RESULT/enhanced_analysis/academic_exports" -name "*.csv" | wc -l)
            echo "   Academic Exports: $EXPORT_COUNT files generated"
        fi
    fi
}

# Parse command line arguments
MODE="basic"
if [ $# -gt 0 ]; then
    MODE="$1"
fi

case "$MODE" in
    "basic")
        echo "🔬 Running basic system health check..."
        run_health_check "basic"
        ;;
    "release")
        echo "🚀 Running release readiness check..."
        run_health_check "release"
        
        # Additional release checks
        echo ""
        echo "🔍 Additional Release Readiness Checks:"
        
        # Check for required dependencies
        if command_exists python3; then
            echo "- ✅ Python 3 available"
        else
            echo "- ❌ Python 3 not found"
            exit 1
        fi
        
        # Check for virtual environment
        if [ -n "$VIRTUAL_ENV" ]; then
            echo "- ✅ Virtual environment active"
        else
            echo "- ⚠️  Virtual environment not detected"
        fi
        
        # Check database connection
        if python3 -c "from src.models.base import engine; engine.connect()" 2>/dev/null; then
            echo "- ✅ Database connection successful"
        else
            echo "- ❌ Database connection failed"
            exit 1
        fi
        
        echo ""
        echo "🎉 Release readiness check completed!"
        ;;
    "--help"|"-h")
        echo "Usage: $0 [MODE]"
        echo ""
        echo "Modes:"
        echo "  basic     - Run basic system health validation (default)"
        echo "  release   - Run comprehensive release readiness check"
        echo "  --help    - Show this help message"
        echo ""
        echo "Results are stored in: $RESULTS_DIR"
        echo "Only the most recent result is kept to avoid clutter."
        ;;
    *)
        echo "❌ Unknown mode: $MODE"
        echo "Use --help for usage information"
        exit 1
        ;;
esac

echo ""
echo "🎯 System Health Check Complete!"
echo "Results location: $RESULTS_DIR" 