#!/bin/bash
"""
Safe Python Command for Cursor Agents
=====================================

This script provides a safe way to run Python commands that handles
common agent confusion patterns around python vs python3 and macOS
environment issues.

Usage: ./scripts/safe_python.sh <command> [args...]
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
check_directory() {
    if [[ ! -f "requirements.txt" ]]; then
        print_error "Not in project root (no requirements.txt found)"
        print_info "Fix: cd /Volumes/code/discernus"
        exit 1
    fi
    print_success "Project root: $(pwd)"
}

# Find the best Python command
find_python() {
    # Try python3 first
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_success "Using python3: $(which python3)"
        return 0
    fi
    
    # Try python
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
        print_warning "Using python (consider upgrading to python3)"
        return 0
    fi
    
    print_error "No Python found!"
    print_info "Install Python 3: brew install python@3.13"
    exit 1
}

# Check Python version
check_python_version() {
    local version=$($PYTHON_CMD --version 2>&1)
    print_info "Python version: $version"
    
    # Check if it's Python 3
    if [[ $version == Python\ 3* ]]; then
        print_success "Python 3 detected"
    else
        print_warning "Not Python 3 - some features may not work"
    fi
}

# Check macOS-specific environment
check_macos_environment() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "macOS detected"
        
        # Check if using Homebrew Python
        if [[ "$PYTHON_CMD" == *"/opt/homebrew"* ]]; then
            print_success "Using Homebrew Python (macOS standard)"
        elif [[ "$PYTHON_CMD" == *"/usr/bin"* ]]; then
            print_warning "Using system Python - consider Homebrew for better package management"
        fi
    fi
}

# Check for common agent mistakes
check_agent_mistakes() {
    # Check if we're in a venv directory
    if [[ "$PWD" == *"venv"* ]]; then
        print_error "You're inside a venv directory!"
        print_info "Fix: cd /Volumes/code/discernus"
        exit 1
    fi
    
    # Check if venv exists (agents might try to use it)
    if [[ -d "venv" ]]; then
        print_warning "venv directory exists but we don't use it anymore"
        print_info "We removed venv to eliminate agent confusion"
    fi
}

# Main execution
main() {
    print_info "Safe Python Command for Cursor Agents"
    echo "=========================================="
    
    # Check environment
    check_directory
    find_python
    check_python_version
    check_macos_environment
    check_agent_mistakes
    
    # If no arguments provided, show help
    if [[ $# -eq 0 ]]; then
        print_info "Usage: ./scripts/safe_python.sh <command> [args...]"
        echo ""
        print_info "Examples:"
        echo "  ./scripts/safe_python.sh -m discernus.cli list"
        echo "  ./scripts/safe_python.sh scripts/check_environment.py"
        echo "  ./scripts/safe_python.sh -c 'import sys; print(sys.version)'"
        echo ""
        print_info "Common commands:"
        echo "  ./scripts/safe_python.sh -m discernus.cli run projects/simple_test"
        echo "  ./scripts/safe_python.sh scripts/check_environment.py"
        exit 0
    fi
    
    # Run the command
    print_info "Running: $PYTHON_CMD $*"
    echo "=========================================="
    
    exec "$PYTHON_CMD" "$@"
}

# Run main function with all arguments
main "$@" 