#!/bin/bash
# Development Environment Wrapper
# Simple wrapper for the Background Executor

# Ensure we're in the project root
cd "$(dirname "$0")/.." || exit 1

# Make the background executor executable
chmod +x scripts/background_executor.py

# Function to show usage
show_usage() {
    echo "Discernus Development Environment"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start         Start all services and enter interactive mode"
    echo "  test          Run Phase 3 pipeline test"
    echo "  status        Show service status"
    echo "  stop          Stop all services"
    echo "  logs          Show recent logs"
    echo ""
    echo "Examples:"
    echo "  $0 start      # Start services, monitor autonomously"
    echo "  $0 test       # Run full pipeline test with 10min timeout"
    echo "  $0 status     # Check if services are running"
}

# Function to stop services
stop_services() {
    echo "Stopping services..."
    pkill -f "scripts/background_executor.py" 2>/dev/null
    pkill -f "scripts/router.py" 2>/dev/null
    echo "Services stopped"
}

# Function to show logs
show_logs() {
    echo "=== Recent Background Executor Logs ==="
    if [[ -d logs/background_executor ]]; then
        tail -n 50 logs/background_executor/executor_*.log 2>/dev/null | tail -n 50
    else
        echo "No logs found"
    fi
}

# Main command handling
case "${1:-start}" in
    "start")
        echo "Starting Discernus development environment..."
        python3 scripts/background_executor.py
        ;;
    "test")
        echo "Running Phase 3 pipeline test..."
        python3 scripts/background_executor.py test phase3_pipeline
        ;;
    "status")
        echo "Checking service status..."
        python3 scripts/background_executor.py status
        ;;
    "stop")
        stop_services
        ;;
    "logs")
        show_logs
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac 