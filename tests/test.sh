#!/bin/bash
# Narrative Gravity Maps - Test Runner Script
# Provides convenient commands for running smoke tests

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to print colored output
print_status() {
    echo -e "${BLUE}🎯${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Function to check if we're in a virtual environment
check_venv() {
    if [[ -z "$VIRTUAL_ENV" ]]; then
        print_warning "Not in a virtual environment. Consider activating your venv first:"
        echo "   source venv/bin/activate  # or your preferred venv"
        echo ""
    fi
}

# Function to install test dependencies
install_deps() {
    print_status "Installing test dependencies..."
    cd "$PROJECT_ROOT"
    
    if [[ -f "tests/test_requirements.txt" ]]; then
        pip install -r tests/test_requirements.txt
        print_success "Test dependencies installed"
    else
        print_error "tests/test_requirements.txt not found"
        exit 1
    fi
}

# Function to run all tests
run_all() {
    print_status "Running all smoke tests..."
    cd "$PROJECT_ROOT"
    python tests/run_tests.py
}

# Function to run CLI tests only
run_cli() {
    print_status "Running CLI tests only..."
    cd "$PROJECT_ROOT"
    python tests/test_cli_tools.py
}

# Function to run Streamlit tests only
run_streamlit() {
    print_status "Running Streamlit tests only..."
    cd "$PROJECT_ROOT"
    python tests/test_streamlit_app.py
}

# Function to run a quick check
run_quick() {
    print_status "Running quick syntax and import checks..."
    cd "$PROJECT_ROOT"
    
    # Check Python syntax
    python -m py_compile narrative_gravity_app.py
    python -m py_compile launch_app.py
    python -m py_compile framework_manager.py
    python -m py_compile generate_prompt.py
    python -m py_compile narrative_gravity_elliptical.py
    
    # Check imports
    python -c "import streamlit; import matplotlib; import numpy; import seaborn; print('✅ All imports successful')"
    
    print_success "Quick checks passed"
}

# Function to show help
show_help() {
    echo "🎯 Narrative Gravity Maps - Test Runner"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install     Install test dependencies"
    echo "  all         Run all smoke tests (default)"
    echo "  cli         Run CLI tests only"
    echo "  streamlit   Run Streamlit tests only"
    echo "  quick       Run quick syntax and import checks"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 install           # Install dependencies"
    echo "  $0 cli               # Test CLI tools only"
    echo "  $0 quick             # Quick validation"
    echo ""
}

# Main script logic
main() {
    local command="${1:-all}"
    
    echo "🎯 Narrative Gravity Maps - Test Runner"
    echo "========================================"
    echo ""
    
    # Check virtual environment
    check_venv
    
    case "$command" in
        "install")
            install_deps
            ;;
        "all"|"")
            run_all
            ;;
        "cli")
            run_cli
            ;;
        "streamlit")
            run_streamlit
            ;;
        "quick")
            run_quick
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 